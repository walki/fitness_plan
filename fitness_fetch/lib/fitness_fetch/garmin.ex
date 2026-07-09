defmodule FitnessFetch.Garmin do
  @moduledoc """
  Garmin Connect wellness client — sleep, resting HR, and blood pressure.

  Uses the reverse-engineered `connectapi.garmin.com` endpoints with a bearer
  token from `FitnessFetch.Garmin.Auth`. Responses are normalized into small
  maps that `FitnessFetch.Garmin.Format` turns into weekly-log tables.

  These endpoints are undocumented and their shapes can drift; the `parse_*`
  functions dig defensively and are unit-tested against representative payloads.
  """

  alias FitnessFetch.Garmin.Auth

  @connectapi "https://connectapi.garmin.com"
  @api_ua "com.garmin.android.apps.connectmobile"

  @doc """
  Fetch a week (or range) of wellness data. Returns
  `%{sleep: [...], resting_hr: [...], blood_pressure: [...]}`.
  """
  @spec wellness(Date.t(), Date.t()) :: {:ok, map()} | {:error, term()}
  def wellness(%Date{} = from, %Date{} = to) do
    with {:ok, token} <- Auth.bearer(),
         {:ok, display_name} <- display_name(token) do
      dates = Date.range(from, to) |> Enum.to_list()

      {:ok,
       %{
         sleep: Enum.map(dates, &sleep(token, display_name, &1)) |> Enum.reject(&is_nil/1),
         resting_hr: Enum.map(dates, &resting_hr(token, display_name, &1)) |> Enum.reject(&is_nil/1),
         blood_pressure: blood_pressure(token, from, to)
       }}
    end
  end

  @doc "Resolve the athlete's Garmin display name (needed by wellness endpoints)."
  @spec display_name(String.t()) :: {:ok, String.t()} | {:error, term()}
  def display_name(token) do
    case get(token, "/userprofile-service/socialProfile").body do
      %{"displayName" => name} when is_binary(name) -> {:ok, name}
      other -> {:error, {:no_display_name, other}}
    end
  end

  @doc "Normalized sleep for one date, or nil if unavailable."
  def sleep(token, display_name, %Date{} = date) do
    get(token, "/wellness-service/wellness/dailySleepData/#{display_name}",
      date: Date.to_iso8601(date),
      nonSleepBufferMinutes: 60
    ).body
    |> parse_sleep(date)
  end

  @doc "Normalized resting HR for one date, or nil if unavailable."
  def resting_hr(token, display_name, %Date{} = date) do
    get(token, "/usersummary-service/usersummary/daily/#{display_name}",
      calendarDate: Date.to_iso8601(date)
    ).body
    |> parse_resting_hr(date)
  end

  @doc "Normalized blood-pressure readings across a date range."
  def blood_pressure(token, %Date{} = from, %Date{} = to) do
    get(token, "/bloodpressure-service/bloodpressure/range/#{Date.to_iso8601(from)}/#{Date.to_iso8601(to)}",
      includeAll: true
    ).body
    |> parse_blood_pressure()
  end

  # --- normalization (public for tests) -----------------------------------

  @doc false
  def parse_sleep(%{"dailySleepDTO" => dto}, date) when is_map(dto) do
    %{
      date: date,
      score: get_in(dto, ["sleepScores", "overall", "value"]),
      quality: dto |> get_in(["sleepScores", "overall", "qualifierKey"]) |> humanize_quality(),
      duration_seconds: dto["sleepTimeSeconds"],
      bedtime: ms_to_time(dto["sleepStartTimestampLocal"]),
      wake: ms_to_time(dto["sleepEndTimestampLocal"])
    }
  end

  def parse_sleep(_, _), do: nil

  @doc false
  def parse_resting_hr(%{"restingHeartRate" => rhr}, date) when is_integer(rhr) do
    %{date: date, resting_hr: rhr}
  end

  def parse_resting_hr(_, _), do: nil

  @doc false
  def parse_blood_pressure(%{"measurementSummaries" => summaries}) when is_list(summaries) do
    summaries
    |> Enum.flat_map(fn s -> s["measurements"] || [] end)
    |> Enum.map(&parse_bp_measurement/1)
    |> Enum.reject(&is_nil/1)
  end

  def parse_blood_pressure(list) when is_list(list) do
    list |> Enum.map(&parse_bp_measurement/1) |> Enum.reject(&is_nil/1)
  end

  def parse_blood_pressure(_), do: []

  defp parse_bp_measurement(%{"systolic" => sys, "diastolic" => dia} = m) do
    {date, time} = split_timestamp(m["measurementTimestampLocal"])

    %{
      date: date,
      time: time,
      systolic: sys,
      diastolic: dia,
      pulse: m["pulse"],
      category: humanize_category(m["categoryName"] || m["category"]) || category_for(sys, dia)
    }
  end

  defp parse_bp_measurement(_), do: nil

  # --- helpers ------------------------------------------------------------

  defp humanize_quality(nil), do: nil
  defp humanize_quality(key), do: key |> to_string() |> String.capitalize()

  # "NORMAL" -> "Normal", "STAGE_1" -> "Stage 1"
  defp humanize_category(nil), do: nil

  defp humanize_category(cat) do
    cat |> to_string() |> String.split(~r/[_\s]+/) |> Enum.map_join(" ", &String.capitalize/1)
  end

  # Garmin timestamps are epoch-ms in local time.
  defp ms_to_time(ms) when is_integer(ms) do
    ms |> DateTime.from_unix!(:millisecond) |> Calendar.strftime("%-I:%M %p")
  end

  defp ms_to_time(_), do: nil

  defp split_timestamp(ms) when is_integer(ms) do
    dt = DateTime.from_unix!(ms, :millisecond)
    {DateTime.to_date(dt), Calendar.strftime(dt, "%-I:%M %p")}
  end

  # Garmin BP local timestamps look like "2026-06-30T07:39:08.0" — ISO-ish but
  # with NO timezone offset, so parse as a NaiveDateTime.
  defp split_timestamp(iso) when is_binary(iso) do
    case NaiveDateTime.from_iso8601(iso) do
      {:ok, ndt} ->
        {NaiveDateTime.to_date(ndt), Calendar.strftime(ndt, "%-I:%M %p")}

      _ ->
        case DateTime.from_iso8601(iso) do
          {:ok, dt, _} -> {DateTime.to_date(dt), Calendar.strftime(dt, "%-I:%M %p")}
          _ -> {nil, nil}
        end
    end
  end

  defp split_timestamp(_), do: {nil, nil}

  # AHA categories (Garmin usually supplies its own; this is a fallback).
  defp category_for(sys, dia) when is_number(sys) and is_number(dia) do
    cond do
      sys < 120 and dia < 80 -> "Normal"
      sys < 130 and dia < 80 -> "Elevated"
      sys < 140 or dia < 90 -> "Stage 1"
      sys < 180 or dia < 120 -> "Stage 2"
      true -> "Crisis"
    end
  end

  defp category_for(_, _), do: nil

  defp get(token, path, params \\ []) do
    Req.get!(client(),
      url: @connectapi <> path,
      params: params,
      headers: [{"authorization", "Bearer #{token}"}, {"user-agent", @api_ua}]
    )
  end

  defp client do
    base = Req.new([])

    case Application.get_env(:fitness_fetch, :req_options) do
      nil -> base
      extra -> Req.merge(base, extra)
    end
  end
end
