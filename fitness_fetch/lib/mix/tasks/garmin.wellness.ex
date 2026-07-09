defmodule Mix.Tasks.Garmin.Wellness do
  @shortdoc "Fetch a week of Garmin sleep, resting HR, and blood pressure"

  @moduledoc """
  Fetch Garmin Connect wellness data (sleep, resting HR, blood pressure) for a
  date range and print it as weekly-log tables.

      mise exec -- mix garmin.wellness                              # current Mon–Sun week
      mise exec -- mix garmin.wellness --week 2026-07-12
      mise exec -- mix garmin.wellness --from 2026-07-06 --to 2026-07-12

  Auth uses `GARMIN_EMAIL`/`GARMIN_PASSWORD` from `.mise.local.toml`. If the SSO
  login fails (Cloudflare / MFA), set `GARMIN_BEARER` to an OAuth2 token instead.
  See the README.
  """
  use Mix.Task
  alias FitnessFetch.{Week, Garmin}
  alias FitnessFetch.Garmin.Format

  @impl true
  def run(argv) do
    Application.ensure_all_started(:req)

    {opts, _rest, _invalid} =
      OptionParser.parse(argv, strict: [from: :string, to: :string, week: :string])

    {from, to} = Week.range(opts)

    case Garmin.wellness(from, to) do
      {:ok, data} ->
        IO.puts(Format.report(data, from, to))

      {:error, reason} ->
        Mix.raise("""
        Garmin fetch failed: #{inspect(reason)}

        The SSO login is the fragile part (Cloudflare / MFA not yet supported).
        Workaround: obtain an OAuth2 token elsewhere (e.g. Python `garth`) and set
        GARMIN_BEARER in fitness_fetch/.mise.local.toml, then re-run.
        """)
    end
  end
end
