# fitness_fetch

Elixir app that pulls training data from external services so we stop
copy-pasting it into the weekly logs by hand.

Both the Garmin watch (runs) and the Coros Dura (rides) sync into **Strava**, so
Strava is the unified activity source and the first one wired up. It's a
supervised OTP app on purpose — today it runs as manual mix tasks, but the
supervision tree gives us room to add scheduled `GenServer`/`Supervisor`-based
fetching later.

## Toolchain

Managed by **mise** (see `../.mise.toml`): Erlang 28.4.1 + Elixir 1.18.3.

```sh
mise install          # once, from the repo root — installs the pinned toolchain
```

Run mix commands through mise so the pinned toolchain **and** the credentials in
`../.mise.local.toml` are loaded:

```sh
mise exec -- mix deps.get
mise exec -- mix compile
```

## One-time Strava setup

1. **Create a Strava API application** at <https://www.strava.com/settings/api>.
   - Authorization Callback Domain: `localhost`
   - Note the **Client ID** and **Client Secret**.

2. **Add credentials.** Copy `../.mise.local.toml.example` to
   `../.mise.local.toml` and fill in `STRAVA_CLIENT_ID` and
   `STRAVA_CLIENT_SECRET`. (This file is gitignored.)

3. **Authorize and get a refresh token:**

   ```sh
   mise exec -- mix strava.auth          # prints a consent URL
   ```

   Open the URL, click **Authorize**. Strava redirects to a `localhost` URL that
   won't load — copy the `code=...` value from the address bar, then:

   ```sh
   mise exec -- mix strava.auth <code>   # prints your refresh_token
   ```

   Paste the printed `STRAVA_REFRESH_TOKEN` into `../.mise.local.toml`.

## Fetching activities

```sh
mise exec -- mix strava.fetch                               # current Mon–Sun week
mise exec -- mix strava.fetch --from 2026-07-06 --to 2026-07-12
mise exec -- mix strava.fetch --week 2026-07-12             # Mon–Sun week ending this Sunday
```

Output: a details block per activity plus a **ready-to-paste markdown table
row** in the weekly-log format (cycling vs running chosen by sport type). Power
comes through as `NP / avg` when a power meter was used, `~W est` for Strava's
estimate, or `HR/RPE` for the Cutthroat (no power meter). Distances/elevations
are converted from Strava's SI units to miles/feet.

`RPE` and the `Bike` column are left blank for you to fill — Strava doesn't know
your perceived effort or which bike you rode.

## Layout

```
lib/fitness_fetch/strava.ex      Strava API client (token refresh + activities)
lib/fitness_fetch/format.ex      SI→imperial conversion + weekly-log formatting
lib/mix/tasks/strava.auth.ex     one-time OAuth helper
lib/mix/tasks/strava.fetch.ex    fetch + print for a date range
```

## Roadmap

- **Garmin** (sleep, BP, resting HR) via a Garmin Connect client.
- **MyFitnessPal** (food, weight) — hardest; no official API.
- Scheduled/automatic fetching using the supervision tree once the manual flow
  proves out.
