defmodule Mix.Tasks.Energy do
  @shortdoc "Self-computed daily calorie burn (resting-from-weight + active-from-Strava)"

  @moduledoc """
  Build a daily calorie-burn table without trusting Garmin's flaky daily total.

  Burn = **resting** (scaled from body weight, see `FitnessFetch.Energy`) +
  **active** (per-activity calories from Strava, which estimates rides from
  power — dodging the HR-dropout problem).

  Pass daily weights as `date=lbs` pairs (any you have — missing days carry the
  last known weight forward, marked `*`):

      mise exec -- mix energy --week 2026-07-05 \\
        --weights 2026-06-29=188.8,2026-06-30=189.4,2026-07-01=189.2,2026-07-02=188.0,2026-07-03=189.2

  Also accepts `--from/--to`. Output is a markdown table for the weekly-log body
  metrics (pair with your MFP "Cal In" to get net).
  """
  use Mix.Task
  alias FitnessFetch.{Strava, Energy, Week}

  @impl true
  def run(argv) do
    Application.ensure_all_started(:req)

    {opts, _rest, _invalid} =
      OptionParser.parse(argv, strict: [from: :string, to: :string, week: :string, weights: :string])

    {from, to} = Week.range(opts)
    weights = parse_weights(opts[:weights])
    by_day = Enum.group_by(Strava.weekly_energy(from, to), &day_of/1)

    IO.puts(render(from, to, weights, by_day))
  end

  defp day_of(activity) do
    case Strava.local_date(activity) do
      {:ok, d} -> d
      _ -> nil
    end
  end

  defp render(from, to, weights, by_day) do
    {rows, _last, carried?} =
      from
      |> Date.range(to)
      |> Enum.reduce({[], nil, false}, fn day, {rows, last_weight, carried?} ->
        {weight, is_carried} =
          case Map.get(weights, day) do
            nil -> {last_weight, not is_nil(last_weight)}
            w -> {w, false}
          end

        acts = Map.get(by_day, day, [])
        {rows_line, carried?} = row(day, weight, is_carried, acts, carried?)
        {[rows_line | rows], weight || last_weight, carried?}
      end)

    {anchor_w, anchor_c} = Energy.anchor()

    """
    === Daily calorie burn #{Calendar.strftime(from, "%b %-d")} – #{Calendar.strftime(to, "%b %-d, %Y")} ===
    resting anchor: #{anchor_c} cal @ #{anchor_w} lb

    | Day | Weight | Resting | Active | Total Burn |
    |-----|--------|---------|--------|------------|
    #{Enum.reverse(rows) |> Enum.join("\n")}
    #{if carried?, do: "\n* weight carried forward from the last known day (resting shifts only a few cal, so this is fine)", else: ""}
    """
  end

  defp row(day, nil, _is_carried, acts, carried?) do
    raw = acts |> Enum.map(&(&1["calories"] || 0)) |> Enum.sum() |> round()
    {"| #{fmt_day(day)} | ? | ? | #{raw} | ? (need a weight) |", carried?}
  end

  defp row(day, weight, is_carried, acts, carried?) do
    active =
      acts
      |> Enum.map(&Energy.active_above_resting(&1["calories"], &1["moving_time"], weight))
      |> Enum.sum()

    resting = Energy.resting_calories(weight)
    mark = if is_carried, do: "*", else: ""
    line = "| #{fmt_day(day)} | #{fmt_weight(weight)}#{mark} | #{resting} | #{active} | #{resting + active} |"
    {line, carried? or is_carried}
  end

  defp parse_weights(nil), do: %{}

  defp parse_weights(str) do
    str
    |> String.split(",", trim: true)
    |> Map.new(fn pair ->
      [date, w] = String.split(pair, "=", parts: 2)
      {Date.from_iso8601!(String.trim(date)), parse_float!(String.trim(w))}
    end)
  end

  defp parse_float!(s) do
    case Float.parse(s) do
      {f, _} -> f
      :error -> Mix.raise("bad weight value: #{s}")
    end
  end

  defp fmt_day(d), do: "#{Calendar.strftime(d, "%a %b")} #{d.day}"
  defp fmt_weight(w), do: :erlang.float_to_binary(w / 1, decimals: 1)
end
