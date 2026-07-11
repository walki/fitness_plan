# fitness_fetch

Elixir app that pulls training data from external services so we stop
copy-pasting it into the weekly logs by hand.

Both the Garmin watch (runs) and the Coros Dura (rides) sync into **Strava**, so
Strava is the unified activity source and the first one wired up. It's a
supervised OTP app on purpose — today it runs as manual mix tasks, but the
supervision tree gives us room to add scheduled `GenServer`/`Supervisor`-based
fetching later.

> Run all commands **from this `fitness_fetch/` directory** — that's where
> `.mise.local.toml` (credentials) lives, and mise loads env from the current
> directory upward.

## Toolchain

Managed by **mise**: Erlang 28.5.0.3 + Elixir 1.20.2 (tools pinned in
`../.mise.toml`).

```sh
mise install          # once — installs the pinned toolchain (prebuilt on Windows)
mise exec -- mix deps.get
mise exec -- mix compile
mise exec -- mix test
```

## One-time Strava setup

1. **Create a Strava API application** at <https://www.strava.com/settings/api>.
   - Authorization Callback Domain: `localhost`
   - Upload any icon (there's one at `assets/app_icon.png`).
   - Note the **Client ID** and **Client Secret**.

2. **Add credentials.** Copy `.mise.local.toml.example` to `.mise.local.toml`
   and fill in `STRAVA_CLIENT_ID` and `STRAVA_CLIENT_SECRET`. (Gitignored.)

3. **Authorize and get a refresh token:**

   ```sh
   mise exec -- mix strava.auth          # prints a consent URL
   ```

   Open the URL, click **Authorize**. Strava redirects to a `localhost` URL that
   won't load — copy the `code=...` value from the address bar, then:

   ```sh
   mise exec -- mix strava.auth <code>   # prints your refresh_token
   ```

   Paste the printed `STRAVA_REFRESH_TOKEN` into `.mise.local.toml`.

## Fetching activities

```sh
mise exec -- mix strava.fetch                               # current Mon–Sun week
mise exec -- mix strava.fetch --from 2026-07-06 --to 2026-07-12
mise exec -- mix strava.fetch --week 2026-07-12             # Mon–Sun week ending this Sunday
```

Output: a details block per activity plus a **ready-to-paste markdown table
row** in the weekly-log format (cycling / running / strength chosen by sport
type). Distances and elevations are converted from Strava's SI units. Notes:

- **Bike column** is the resolved gear name (e.g. `Salsa Cutthroat`), or `?` if
  Strava has no gear on the activity.
- **Power** shows `NP / avg` for power-meter rides, `~W est` for Strava's
  estimate, or `HR/RPE` when there's nothing.
- **Strength** (`WeightTraining` etc.) renders a 4-column strength-table row,
  followed by the **`logged (Hevy)`** block — the actual sets/reps Hevy writes
  into the Strava description (compare against what was planned).
- Cardio activities show their description as a `notes` block when present.
- **`RPE`** is left blank — Strava doesn't know perceived effort.

`strava.fetch` makes one extra detail request per activity to pull descriptions
(and calories), so it's a bit slower than a bare listing — worth it for the
logged-workout detail.

## Daily calorie burn

Self-computed daily burn = **resting** (scaled from body weight) + **active**
(per-activity calories from Strava, netted of the baseline burned during the
activity so it isn't double-counted). Strava estimates rides from power, so this
dodges the HR-dropout problem that tanks Garmin's daily estimate.

```sh
mise exec -- mix energy --week 2026-07-05 \
  --weights 2026-06-29=188.8,2026-06-30=189.4,2026-07-01=189.2,2026-07-02=188.0
```

Pass whatever daily weights you have as `date=lbs` pairs; missing days carry the
last known weight forward (marked `*` — resting barely moves, so it's fine).
Output is a markdown table for the weekly-log body-metrics section (pair with
your MFP "Cal In" to get net).

The resting anchor is **2034 cal @ 187.4 lb** (Garmin, Jul 2026). Re-anchor as
weight drops via `config :fitness_fetch, :resting_anchor, {weight, cal}`.

Runs consistently ~50–200 cal under Garmin's daily total because we don't count
non-exercise daily movement (steps/NEAT) — a consistent, predictable offset, so
the trend stays reliable.

## Garmin wellness (sleep / resting HR / blood pressure)

Garmin has **no official API**. This uses the same reverse-engineered handshake
as the Python `garth` library: SSO sign-in → OAuth1 → OAuth2 bearer, then the
undocumented `connectapi.garmin.com` wellness endpoints.

1. Put `GARMIN_EMAIL` / `GARMIN_PASSWORD` in `.mise.local.toml`.
2. Fetch a week:

   ```sh
   mise exec -- mix garmin.wellness --week 2026-07-12
   ```

Output: weekly-log tables for **sleep** (score/quality/duration/bedtime/wake),
**resting HR**, and **BP** (reading/pulse/category). Tokens are cached to
`~/.fitness_fetch/garmin_token.json` and the short-lived OAuth2 token is
refreshed automatically.

> **The SSO login is the fragile part** — Cloudflare can block it and **MFA is
> not yet supported** (the task errors clearly if Garmin returns an MFA
> challenge). Escape hatch: obtain an OAuth2 token elsewhere (e.g. Python
> `garth`) and set `GARMIN_BEARER` in `.mise.local.toml`; everything downstream
> works regardless of the login flow. The data + formatting layers are unit
> tested; the live handshake needs real credentials to validate.

## intervals.icu (computed metrics + fitness/form)

intervals.icu ingests Strava/Coros/Garmin and does the analytics we deliberately
keep *out* of this app — so we just **pull its computed numbers**.

1. Put `INTERVALS_ATHLETE_ID` + `INTERVALS_API_KEY` (intervals.icu → Settings →
   Developer) in `.mise.local.toml`.
2. `mise exec -- mix intervals.week --week 2026-07-12`

Prints a per-activity metrics table (TSS, IF, decoupling, efficiency factor,
NP) and the daily **fitness/fatigue/form** trend (CTL/ATL/TSB) — the piece that
shows, objectively, whether you're fresh or fatigued heading into a race. Auth
is HTTP Basic (username `API_KEY`, password = your key).

## Layout

```
lib/fitness_fetch/strava.ex        Strava API client (tokens, activities, gear, calories)
lib/fitness_fetch/format.ex        SI→imperial + weekly-log row formatting
lib/fitness_fetch/energy.ex        resting-from-weight + active-above-resting math
lib/fitness_fetch/week.ex          Mon–Sun date-range resolution for the tasks
lib/fitness_fetch/garmin.ex        Garmin wellness client (sleep, RHR, BP)
lib/fitness_fetch/garmin/auth.ex   Garmin SSO→OAuth1→OAuth2 login + token cache
lib/fitness_fetch/garmin/format.ex Garmin wellness → weekly-log tables
lib/mix/tasks/strava.auth.ex       one-time Strava OAuth helper
lib/mix/tasks/strava.fetch.ex      fetch + print activities for a date range
lib/mix/tasks/energy.ex            daily calorie-burn table
lib/mix/tasks/garmin.wellness.ex   fetch + print a week of Garmin wellness
lib/fitness_fetch/intervals.ex     intervals.icu client (computed metrics + wellness)
lib/fitness_fetch/intervals/format.ex  metrics + fitness/form tables
lib/mix/tasks/intervals.week.ex    fetch + print intervals.icu metrics for a week
```

## Roadmap

- **MyFitnessPal** (food, weight) — hardest; no official API.
- Garmin **MFA** support (interactive code step).
- Scheduled/automatic fetching using the supervision tree once the manual flow
  proves out.
