defmodule Mix.Tasks.Intervals.Week do
  @shortdoc "Pull intervals.icu computed metrics (TSS/IF/decoupling/EF) + fitness/form"

  @moduledoc """
  Pull intervals.icu's **already-computed** training metrics for a date range:
  a per-activity table (TSS, IF, decoupling, efficiency factor, NP) plus the
  daily fitness/fatigue/form (CTL/ATL/TSB) trend.

      mise exec -- mix intervals.week                              # current Mon–Sun week
      mise exec -- mix intervals.week --week 2026-07-12
      mise exec -- mix intervals.week --from 2026-07-06 --to 2026-07-12

  Needs `INTERVALS_ATHLETE_ID` + `INTERVALS_API_KEY` in `.mise.local.toml`.
  """
  use Mix.Task
  alias FitnessFetch.{Week, Intervals}
  alias FitnessFetch.Intervals.Format

  @impl true
  def run(argv) do
    Application.ensure_all_started(:req)

    {opts, _rest, _invalid} =
      OptionParser.parse(argv, strict: [from: :string, to: :string, week: :string])

    {from, to} = Week.range(opts)

    activities = Intervals.activities(from, to)
    wellness = Intervals.wellness(from, to)

    IO.puts(Format.report(activities, wellness, from, to))
  end
end
