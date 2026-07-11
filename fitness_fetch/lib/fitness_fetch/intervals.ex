defmodule FitnessFetch.Intervals do
  @moduledoc """
  intervals.icu client — pulls **already-computed** training metrics so we don't
  compute anything ourselves (keeps `fitness_fetch` a data-pull automation, not
  an analytics engine — intervals.icu *is* the analytics engine).

  intervals.icu ingests Strava/Coros/Garmin, so it sees everything. We pull:

    * **activities** — per-activity computed metrics (TSS, IF, decoupling,
      efficiency factor, normalized power, …)
    * **wellness** — daily CTL (fitness) / ATL (fatigue) / form, resting HR,
      sleep — the fitness/freshness history a one-off pull can't reconstruct.

  Credentials (from `.mise.local.toml`):

    * `INTERVALS_ATHLETE_ID` — e.g. "i123456"
    * `INTERVALS_API_KEY` — from intervals.icu → Settings → Developer

  Auth is HTTP Basic with username `API_KEY` and the key as the password.

  > Field names below are intervals.icu's documented `icu_*` fields; if a first
  > live pull shows a rename, adjust `normalize_*`.
  """

  @base "https://intervals.icu/api/v1"

  @doc "Per-activity computed metrics over `[from, to]`, oldest first."
  @spec activities(Date.t(), Date.t()) :: [map()]
  def activities(%Date{} = from, %Date{} = to) do
    case get("/athlete/#{athlete_id()}/activities", oldest: Date.to_iso8601(from), newest: Date.to_iso8601(to)) do
      list when is_list(list) ->
        list
        |> Enum.map(&normalize_activity/1)
        |> Enum.reject(&is_nil(&1.date))
        |> Enum.sort_by(& &1.date, Date)

      _ ->
        []
    end
  end

  @doc "Daily wellness (CTL/ATL/form, resting HR, sleep) over `[from, to]`, oldest first."
  @spec wellness(Date.t(), Date.t()) :: [map()]
  def wellness(%Date{} = from, %Date{} = to) do
    case get("/athlete/#{athlete_id()}/wellness", oldest: Date.to_iso8601(from), newest: Date.to_iso8601(to)) do
      list when is_list(list) ->
        list
        |> Enum.map(&normalize_wellness/1)
        |> Enum.reject(&is_nil(&1.date))
        |> Enum.sort_by(& &1.date, Date)

      _ ->
        []
    end
  end

  # --- normalization (public for tests) -----------------------------------

  @doc false
  def normalize_activity(a) do
    %{
      date: parse_date(a["start_date_local"]),
      name: a["name"],
      type: a["type"],
      tss: a["icu_training_load"],
      intensity: a["icu_intensity"],
      ftp: a["icu_ftp"],
      np: a["icu_weighted_avg_watts"],
      ef: a["icu_efficiency_factor"],
      decoupling: a["decoupling"],
      avg_hr: a["average_heartrate"],
      max_hr: a["max_heartrate"]
    }
  end

  @doc false
  def normalize_wellness(w) do
    ctl = w["ctl"]
    atl = w["atl"]

    %{
      date: parse_date(w["id"]),
      ctl: ctl,
      atl: atl,
      form: form(ctl, atl),
      resting_hr: w["restingHR"],
      sleep_secs: w["sleepSecs"],
      weight: w["weight"]
    }
  end

  @doc "Form (TSB) = CTL − ATL, rounded; nil if either is missing."
  def form(ctl, atl) when is_number(ctl) and is_number(atl), do: round(ctl - atl)
  def form(_, _), do: nil

  # --- helpers ------------------------------------------------------------

  defp parse_date(nil), do: nil

  defp parse_date(s) when is_binary(s) do
    case s |> String.slice(0, 10) |> Date.from_iso8601() do
      {:ok, d} -> d
      _ -> nil
    end
  end

  defp get(path, params) do
    Req.get!(client(),
      url: @base <> path,
      params: params,
      auth: {:basic, "API_KEY:#{api_key()}"}
    ).body
  end

  defp client do
    base = Req.new([])

    case Application.get_env(:fitness_fetch, :req_options) do
      nil -> base
      extra -> Req.merge(base, extra)
    end
  end

  defp athlete_id, do: fetch_env!("INTERVALS_ATHLETE_ID")
  defp api_key, do: fetch_env!("INTERVALS_API_KEY")

  defp fetch_env!(key) do
    System.get_env(key) ||
      raise "Missing environment variable #{key}. Set it in fitness_fetch/.mise.local.toml (see README)."
  end
end
