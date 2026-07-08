defmodule FitnessFetch.Energy do
  @moduledoc """
  Self-computed daily calorie burn = resting + active.

  Garmin's *resting* calories track body weight (its BMR estimate), so we scale
  a known anchor by weight instead of trusting Garmin's flaky daily total.
  *Active* calories come per-activity from Strava (which estimates rides from
  power — so it dodges the HR-dropout problem that tanks Garmin's estimate).

  Anchor: Garmin reported **2034 resting cal/day at 187.4 lb** (Jul 2026).
  Override with `config :fitness_fetch, :resting_anchor, {weight_lbs, cal}` — or
  re-anchor as Roger's weight (and Garmin's number) move.
  """

  @default_anchor {187.4, 2034}

  @doc """
  Resting (BMR) calories for a body weight, scaled proportionally from the
  anchor. Returns a rounded integer.

      iex> FitnessFetch.Energy.resting_calories(187.4)
      2034
  """
  @spec resting_calories(number(), {number(), number()}) :: integer()
  def resting_calories(weight_lbs, anchor \\ anchor()) when is_number(weight_lbs) do
    {anchor_weight, anchor_cal} = anchor
    round(anchor_cal * weight_lbs / anchor_weight)
  end

  @doc """
  Total daily burn = resting(weight) + active calories.

      iex> FitnessFetch.Energy.total_burn(187.4, 500)
      2534
  """
  @spec total_burn(number(), number() | nil, {number(), number()}) :: integer()
  def total_burn(weight_lbs, active_calories, anchor \\ anchor()) do
    resting_calories(weight_lbs, anchor) + round(active_calories || 0)
  end

  @doc """
  Active calories *above resting* for one activity.

  Strava's per-activity `calories` is the activity TOTAL — it mirrors the
  device's number, which already includes the baseline metabolic cost burned
  during the activity. Since daily burn adds a *full day* of resting, we
  subtract the resting-equivalent for the activity's duration to avoid
  double-counting those hours. Never negative.

      iex> FitnessFetch.Energy.active_above_resting(500, 3600, 187.4)
      415
  """
  @spec active_above_resting(number() | nil, number() | nil, number(), {number(), number()}) ::
          integer()
  def active_above_resting(activity_calories, moving_seconds, weight_lbs, anchor \\ anchor()) do
    resting_per_sec = resting_calories(weight_lbs, anchor) / 86_400
    net = (activity_calories || 0) - resting_per_sec * (moving_seconds || 0)

    net |> round() |> max(0)
  end

  @doc "The configured resting anchor `{weight_lbs, cal}` (default #{inspect(@default_anchor)})."
  @spec anchor() :: {number(), number()}
  def anchor, do: Application.get_env(:fitness_fetch, :resting_anchor, @default_anchor)
end
