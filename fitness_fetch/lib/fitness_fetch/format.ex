defmodule FitnessFetch.Format do
  @moduledoc """
  Turns raw Strava activity maps into console output shaped for the weekly log:
  a details block per activity plus a ready-to-paste markdown table row
  (cycling or running format, matching `weekly-logs/*.md`).

  Strava returns SI units (metres, seconds, m/s, °C); we convert to the
  imperial units the logs use.
  """

  @m_to_mi 0.000621371
  @m_to_ft 3.28084
  @ms_to_mph 2.23694

  @doc "Render a full report for a list of activities over `[from, to]`."
  @spec report([map()], Date.t(), Date.t()) :: String.t()
  def report(activities, from, to) do
    header =
      "=== Strava activities #{Calendar.strftime(from, "%b %-d")} – #{Calendar.strftime(to, "%b %-d, %Y")} ===\n" <>
        "#{length(activities)} activit#{if length(activities) == 1, do: "y", else: "ies"} found\n"

    body =
      activities
      |> Enum.map(&activity_block/1)
      |> Enum.join("\n")

    Enum.join([header, body, summary(activities)], "\n")
  end

  defp activity_block(act) do
    name = act["name"] || "(unnamed)"
    sport = act["sport_type"] || act["type"] || "Workout"
    {:ok, date} = FitnessFetch.Strava.local_date(act)
    day = "#{Calendar.strftime(date, "%a %b")} #{date.day}"

    dist_mi = round2(meters_to_miles(act["distance"]))
    elev_ft = round0(meters_to_feet(act["total_elevation_gain"]))
    moving = format_duration(act["moving_time"])
    elapsed = format_duration(act["elapsed_time"])

    details =
      [
        "  #{dist_mi} mi | #{elev_ft} ft | moving #{moving} (elapsed #{elapsed})",
        "  #{hr_detail(act)}#{power_or_pace_detail(act, sport)}",
        temp_detail(act)
      ]
      |> Enum.reject(&(&1 in [nil, ""]))
      |> Enum.join("\n")

    """
    #{name} — #{sport} — #{day}
    #{details}
      log row:
        #{table_row(act, sport, day, dist_mi, elev_ft, moving)}
    """
  end

  # --- ready-to-paste weekly-log table rows -------------------------------

  defp table_row(act, sport, day, dist_mi, elev_ft, moving) do
    if ride?(sport) do
      # | Session | Date | Bike | Duration | Distance | NP/Avg Pwr | Avg HR | RPE | Notes |
      "| #{act["name"]} | #{day} | ? | #{moving} | #{dist_mi} mi | #{power_cell(act)} | #{hr_cell(act)} | | #{elev_ft} ft. |"
    else
      # | Session | Date | Type | Duration | Distance | Avg Pace | Avg HR | RPE | Notes |
      "| #{act["name"]} | #{day} | #{sport} | #{moving} | #{dist_mi} mi | #{pace_cell(act)} | #{hr_cell(act)} | | #{elev_ft} ft. |"
    end
  end

  defp power_cell(act) do
    cond do
      act["device_watts"] && act["weighted_average_watts"] ->
        "#{round0(act["weighted_average_watts"])}W NP / #{round0(act["average_watts"])}W avg"

      act["average_watts"] ->
        "~#{round0(act["average_watts"])}W est"

      true ->
        "HR/RPE"
    end
  end

  defp pace_cell(act) do
    case pace_per_mile(act) do
      nil -> "—"
      pace -> "#{pace}/mi"
    end
  end

  defp hr_cell(act) do
    if act["has_heartrate"] && act["average_heartrate"] do
      "#{round0(act["average_heartrate"])} (#{round0(act["max_heartrate"])} max)"
    else
      "—"
    end
  end

  # --- detail lines -------------------------------------------------------

  defp hr_detail(act) do
    if act["has_heartrate"] && act["average_heartrate"] do
      "HR #{round0(act["average_heartrate"])} avg / #{round0(act["max_heartrate"])} max"
    else
      "HR n/a"
    end
  end

  defp power_or_pace_detail(act, sport) do
    cond do
      ride?(sport) && act["average_watts"] ->
        speed = round1(act["average_speed"] * @ms_to_mph)
        " | #{power_cell(act)} | #{speed} mph"

      ride?(sport) ->
        speed = round1((act["average_speed"] || 0) * @ms_to_mph)
        " | #{speed} mph"

      true ->
        case pace_per_mile(act) do
          nil -> ""
          pace -> " | #{pace}/mi"
        end
    end
  end

  defp temp_detail(act) do
    case act["average_temp"] do
      nil -> nil
      c -> "  temp #{round0(c * 9 / 5 + 32)}°F (Garmin device temp — reads high in sun)"
    end
  end

  # --- weekly summary -----------------------------------------------------

  defp summary([]), do: "\n(no activities)"

  defp summary(activities) do
    by_sport = Enum.frequencies_by(activities, &(&1["sport_type"] || &1["type"]))
    total_mi = activities |> Enum.map(&meters_to_miles(&1["distance"])) |> Enum.sum() |> round1()
    total_ft = activities |> Enum.map(&meters_to_feet(&1["total_elevation_gain"])) |> Enum.sum() |> round0()
    total_time = activities |> Enum.map(&(&1["moving_time"] || 0)) |> Enum.sum() |> format_duration()

    sports = by_sport |> Enum.map(fn {k, v} -> "#{k} ×#{v}" end) |> Enum.join(", ")

    """
    === Weekly totals ===
      #{length(activities)} activities: #{sports}
      Distance: #{total_mi} mi | Elevation: #{total_ft} ft | Moving time: #{total_time}
    """
  end

  # --- helpers ------------------------------------------------------------

  defp ride?(sport), do: String.contains?(sport, ["Ride", "Bike", "Gravel", "Velomobile"])

  defp pace_per_mile(act) do
    miles = meters_to_miles(act["distance"])
    secs = act["moving_time"]

    if miles > 0 and is_number(secs) and secs > 0 do
      per_mile = round(secs / miles)
      "#{div(per_mile, 60)}:#{pad(rem(per_mile, 60))}"
    end
  end

  defp meters_to_miles(nil), do: 0.0
  defp meters_to_miles(m), do: m * @m_to_mi

  defp meters_to_feet(nil), do: 0.0
  defp meters_to_feet(m), do: m * @m_to_ft

  defp format_duration(nil), do: "0:00"
  defp format_duration(secs) when is_number(secs) do
    secs = round(secs)
    h = div(secs, 3600)
    m = div(rem(secs, 3600), 60)
    s = rem(secs, 60)

    if h > 0 do
      "#{h}:#{pad(m)}:#{pad(s)}"
    else
      "#{m}:#{pad(s)}"
    end
  end

  defp pad(n), do: String.pad_leading("#{n}", 2, "0")
  defp round0(nil), do: 0
  defp round0(n), do: round(n)
  defp round1(nil), do: 0.0
  defp round1(n), do: Float.round(n / 1, 1)
  defp round2(n), do: Float.round(n / 1, 2)
end
