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
  alias FitnessFetch.{Strava, Format}

  @impl true
  def run(argv) do
    Application.ensure_all_started(:req)

    {opts, _rest, _invalid} =
      OptionParser.parse(argv, strict: [from: :string, to: :string, week: :string])

    {from, to} = date_range(opts)
    activities = Strava.list_activities(from, to)
    IO.puts(Format.report(activities, from, to))
  end

  defp date_range(opts) do
    cond do
      opts[:from] || opts[:to] ->
        {parse_date!(opts[:from], "--from"), parse_date!(opts[:to], "--to")}

      opts[:week] ->
        sunday = parse_date!(opts[:week], "--week")
        {Date.add(sunday, -6), sunday}

      true ->
        today = Date.utc_today()
        monday = Date.add(today, -(Date.day_of_week(today) - 1))
        {monday, Date.add(monday, 6)}
    end
  end

  defp parse_date!(nil, flag), do: Mix.raise("#{flag} is required (YYYY-MM-DD)")

  defp parse_date!(s, flag) do
    case Date.from_iso8601(s) do
      {:ok, d} -> d
      _ -> Mix.raise("#{flag} must be YYYY-MM-DD, got: #{s}")
    end
  end
end
