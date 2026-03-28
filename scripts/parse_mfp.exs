# Parse MyFitnessPal exports — Nutrition Summary and Measurement Summary
#
# Usage:
#   elixir scripts/parse_mfp.exs exports/Nutrition-Summary-*.csv exports/Measurement-Summary-*.csv
#
# Splits out the current week (Monday-Sunday) and shows daily nutrition totals + weight.

defmodule MFPParser do
  def run(args) do
    {nutrition_path, measurement_path} = parse_args(args)

    today = Date.utc_today()
    monday = Date.add(today, -(Date.day_of_week(today) - 1))
    sunday = Date.add(monday, 6)

    IO.puts("=== MFP Week of #{monday} to #{sunday} ===\n")

    if nutrition_path, do: process_nutrition(nutrition_path, monday, sunday)
    if measurement_path, do: process_measurements(measurement_path, monday, sunday)
  end

  defp parse_args(args) do
    nutrition = Enum.find(args, &String.contains?(&1, "Nutrition"))
    measurement = Enum.find(args, &String.contains?(&1, "Measurement"))
    {nutrition, measurement}
  end

  defp process_nutrition(path, monday, sunday) do
    [_header | rows] =
      File.read!(path)
      |> String.trim()
      |> String.split("\n")
      |> Enum.map(&parse_csv_row/1)

    meals =
      rows
      |> Enum.filter(fn row ->
        case Date.from_iso8601(Enum.at(row, 0, "")) do
          {:ok, date} -> Date.compare(date, monday) != :lt and Date.compare(date, sunday) != :gt
          _ -> false
        end
      end)

    if Enum.empty?(meals) do
      IO.puts("No nutrition data for this week.\n")
    else
      # Group by date and sum daily totals
      daily =
        meals
        |> Enum.group_by(fn row -> Enum.at(row, 0) end)
        |> Enum.sort_by(fn {date, _} -> date end)

      IO.puts("--- Nutrition ---\n")

      weekly_totals = %{calories: 0.0, fat: 0.0, carbs: 0.0, protein: 0.0, days: 0}

      weekly_totals =
        Enum.reduce(daily, weekly_totals, fn {date, day_meals}, acc ->
          {:ok, d} = Date.from_iso8601(date)
          day_name = Calendar.strftime(d, "%A")

          cals = sum_col(day_meals, 2)
          fat = sum_col(day_meals, 3)
          carbs = sum_col(day_meals, 11)
          protein = sum_col(day_meals, 14)

          IO.puts("#{date} (#{day_name})")
          IO.puts("  Calories: #{round(cals)} | Protein: #{round(protein)}g | Carbs: #{round(carbs)}g | Fat: #{round(fat)}g")

          meal_names = Enum.map(day_meals, fn row -> Enum.at(row, 1) end) |> Enum.join(", ")
          IO.puts("  Meals logged: #{meal_names}")

          note = day_meals |> Enum.map(fn row -> Enum.at(row, 18, "") end) |> Enum.reject(&(&1 == "")) |> Enum.join("; ")
          if note != "", do: IO.puts("  Notes: #{note}")

          IO.puts("")

          %{acc | calories: acc.calories + cals, fat: acc.fat + fat, carbs: acc.carbs + carbs, protein: acc.protein + protein, days: acc.days + 1}
        end)

      days = max(weekly_totals.days, 1)
      IO.puts("--- Weekly Nutrition Averages (#{days} days logged) ---")
      IO.puts("  Avg calories: #{round(weekly_totals.calories / days)}")
      IO.puts("  Avg protein: #{round(weekly_totals.protein / days)}g")
      IO.puts("  Avg carbs: #{round(weekly_totals.carbs / days)}g")
      IO.puts("  Avg fat: #{round(weekly_totals.fat / days)}g")
      IO.puts("")
    end
  end

  defp process_measurements(path, monday, sunday) do
    [_header | rows] =
      File.read!(path)
      |> String.trim()
      |> String.split("\n")
      |> Enum.map(&parse_csv_row/1)

    week_weights =
      rows
      |> Enum.filter(fn row ->
        case Date.from_iso8601(Enum.at(row, 0, "")) do
          {:ok, date} -> Date.compare(date, monday) != :lt and Date.compare(date, sunday) != :gt
          _ -> false
        end
      end)
      |> Enum.sort_by(fn row -> Enum.at(row, 0) end)

    IO.puts("--- Weight ---\n")

    if Enum.empty?(week_weights) do
      IO.puts("No weigh-ins this week.\n")
    else
      Enum.each(week_weights, fn row ->
        date = Enum.at(row, 0)
        weight = Enum.at(row, 1)
        {:ok, d} = Date.from_iso8601(date)
        day_name = Calendar.strftime(d, "%A")
        IO.puts("  #{date} (#{day_name}): #{weight} lbs")
      end)

      weights = Enum.map(week_weights, fn row -> parse_float(Enum.at(row, 1)) end)
      avg = Float.round(Enum.sum(weights) / length(weights), 1)
      low = Float.round(Enum.min(weights), 1)
      high = Float.round(Enum.max(weights), 1)

      IO.puts("")
      IO.puts("  Avg: #{avg} lbs | Low: #{low} lbs | High: #{high} lbs")
      IO.puts("")
    end
  end

  defp sum_col(rows, idx) do
    Enum.reduce(rows, 0.0, fn row, acc -> acc + parse_float(Enum.at(row, idx, "0")) end)
  end

  defp parse_float(""), do: 0.0
  defp parse_float(nil), do: 0.0
  defp parse_float(val) do
    case Float.parse(val) do
      {f, _} -> f
      :error -> 0.0
    end
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
end

MFPParser.run(System.argv())
