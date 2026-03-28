# Parse VeloViewer activities CSV and split out the current week (Mon-Sun)
#
# IMPORTANT: Despite column headers suggesting imperial units,
# all data is raw SI (metres and seconds). Conversions:
#   - "Dist mi" → actually metres
#   - "Elv ft" → actually metres
#   - "Speed mph" → actually m/s
#   - "Elapsed Time" / "Moving Time" → seconds
#   - "Pace /mi" → actually seconds per metre (needs conversion)

defmodule ActivityParser do
  @metres_to_miles 0.000621371
  @metres_to_feet 3.28084

  def run(csv_path) do
    [header_line | data_lines] = File.read!(csv_path) |> parse_csv_lines()
    headers = header_line

    activities =
      data_lines
      |> Enum.reject(&(length(&1) < 2))
      |> Enum.map(fn row -> Enum.zip(headers, row) |> Map.new() end)

    # Find current week boundaries (Monday-Sunday)
    today = Date.utc_today()
    monday = Date.add(today, -(Date.day_of_week(today) - 1))
    sunday = Date.add(monday, 6)

    IO.puts("=== Week of #{monday} to #{sunday} ===\n")

    week_activities =
      activities
      |> Enum.filter(fn act ->
        case parse_date(act["When"]) do
          {:ok, date} -> Date.compare(date, monday) != :lt and Date.compare(date, sunday) != :gt
          _ -> false
        end
      end)
      |> Enum.sort_by(fn act -> act["When"] end)

    if Enum.empty?(week_activities) do
      IO.puts("No activities found for this week.")
    else
      IO.puts("Found #{length(week_activities)} activities:\n")

      Enum.each(week_activities, fn act ->
        dist_m = parse_float(act["Dist mi"])
        dist_mi = Float.round(dist_m * @metres_to_miles, 2)
        elev_m = parse_float(act["Elv ft"])
        elev_ft = Float.round(elev_m * @metres_to_feet, 0)
        moving_secs = parse_float(act["Moving Time"]) |> round()
        duration = format_duration(moving_secs)
        avg_hr = act["Heart"]
        power = act["Pwr W"]
        sport = act["Sport Type"]
        name = act["Name"]
        day = act["Day of Week"]
        date = act["When"] |> String.slice(0, 10)

        IO.puts("#{date} (#{day}) — #{sport}: #{name}")
        IO.puts("  Distance: #{dist_mi} mi | Elevation: #{elev_ft} ft | Duration: #{duration}")

        details = []
        details = if power != "" and power != "0", do: details ++ ["Power: #{power}W"], else: details
        details = if avg_hr != "" and avg_hr != "0" and avg_hr != nil, do: details ++ ["Avg HR: #{avg_hr}"], else: details

        if details != [], do: IO.puts("  #{Enum.join(details, " | ")}")

        desc = act["Description"]
        if desc != "" and desc != nil, do: IO.puts("  Notes: #{desc}")

        IO.puts("")
      end)

      # Weekly summary
      {total_dist, total_elev, total_time} =
        Enum.reduce(week_activities, {0.0, 0.0, 0}, fn act, {d, e, t} ->
          {
            d + parse_float(act["Dist mi"]),
            e + parse_float(act["Elv ft"]),
            t + (parse_float(act["Moving Time"]) |> round())
          }
        end)

      sport_counts =
        Enum.frequencies_by(week_activities, fn act -> act["Sport Type"] end)

      IO.puts("=== Weekly Summary ===")
      IO.puts("Activities: #{length(week_activities)}")
      IO.puts("Total distance: #{Float.round(total_dist * @metres_to_miles, 1)} mi")
      IO.puts("Total elevation: #{Float.round(total_elev * @metres_to_feet, 0)} ft")
      IO.puts("Total moving time: #{format_duration(total_time)}")
      IO.puts("By sport: #{sport_counts |> Enum.map(fn {k, v} -> "#{k} (#{v})" end) |> Enum.join(", ")}")
    end
  end

  defp parse_csv_lines(content) do
    content
    |> String.trim()
    |> String.split("\n")
    |> Enum.map(&parse_csv_row/1)
  end

  defp parse_csv_row(line) do
    line
    |> String.trim()
    |> do_parse_csv([], "", false)
    |> Enum.reverse()
  end

  defp do_parse_csv("", acc, current, _in_quotes), do: [current | acc]
  defp do_parse_csv(<<"\"", rest::binary>>, acc, current, false), do: do_parse_csv(rest, acc, current, true)
  defp do_parse_csv(<<"\"\"", rest::binary>>, acc, current, true), do: do_parse_csv(rest, acc, current <> "\"", true)
  defp do_parse_csv(<<"\"", rest::binary>>, acc, current, true), do: do_parse_csv(rest, acc, current, false)
  defp do_parse_csv(<<",", rest::binary>>, acc, current, false), do: do_parse_csv(rest, [current | acc], "", false)
  defp do_parse_csv(<<c::utf8, rest::binary>>, acc, current, in_quotes), do: do_parse_csv(rest, acc, current <> <<c::utf8>>, in_quotes)

  defp parse_date(nil), do: :error
  defp parse_date(""), do: :error
  defp parse_date(datetime_str) do
    case String.slice(datetime_str, 0, 10) |> Date.from_iso8601() do
      {:ok, date} -> {:ok, date}
      _ -> :error
    end
  end

  defp parse_float(nil), do: 0.0
  defp parse_float(""), do: 0.0
  defp parse_float(val) when is_binary(val) do
    case Float.parse(val) do
      {f, _} -> f
      :error -> 0.0
    end
  end
  defp parse_float(val) when is_number(val), do: val / 1

  defp format_duration(secs) when secs < 0, do: "0:00"
  defp format_duration(secs) do
    hours = div(secs, 3600)
    mins = div(rem(secs, 3600), 60)
    s = rem(secs, 60)

    if hours > 0 do
      "#{hours}:#{String.pad_leading("#{mins}", 2, "0")}:#{String.pad_leading("#{s}", 2, "0")}"
    else
      "#{mins}:#{String.pad_leading("#{s}", 2, "0")}"
    end
  end
end

[csv_path | _] = System.argv()
ActivityParser.run(csv_path)
