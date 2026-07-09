defmodule Mix.Tasks.Strava.Fetch do
  @shortdoc "Fetch Strava activities for a date range (defaults to this week)"

  @moduledoc """
  Fetch Strava activities for a date range and print them shaped for the weekly
  log — a details block plus a ready-to-paste markdown table row per activity.

      mise exec -- mix strava.fetch                               # current Mon–Sun week
      mise exec -- mix strava.fetch --from 2026-07-06 --to 2026-07-12
      mise exec -- mix strava.fetch --week 2026-07-12             # Mon–Sun week ending this Sunday

  Run via `mise exec` so the credentials in `.mise.local.toml` are loaded into
  the environment.
  """
  use Mix.Task
  alias FitnessFetch.{Strava, Format, Week}

  @impl true
  def run(argv) do
    Application.ensure_all_started(:req)

    {opts, _rest, _invalid} =
      OptionParser.parse(argv, strict: [from: :string, to: :string, week: :string])

    {from, to} = Week.range(opts)
    activities = Strava.list_detailed(from, to)
    IO.puts(Format.report(activities, from, to))
  end
end
