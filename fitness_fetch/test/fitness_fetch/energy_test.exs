defmodule FitnessFetch.EnergyTest do
  # async: false — the anchor-override test mutates Application env.
  use ExUnit.Case, async: false
  alias FitnessFetch.Energy
  doctest FitnessFetch.Energy

  test "resting scales proportionally from the anchor (2034 @ 187.4)" do
    assert Energy.resting_calories(187.4) == 2034
    assert Energy.resting_calories(165.0) == round(2034 * 165.0 / 187.4)
    # lighter → lower resting
    assert Energy.resting_calories(165.0) < Energy.resting_calories(187.4)
  end

  test "total burn adds active to resting; nil active is treated as 0" do
    assert Energy.total_burn(187.4, 1000) == 3034
    assert Energy.total_burn(187.4, nil) == 2034
  end

  test "active_above_resting subtracts the baseline burned during the activity" do
    # resting 2034/day @187.4 → ~85 cal over a 3600 s activity
    assert Energy.active_above_resting(500, 3600, 187.4) == 415
    # never negative (short easy effort under the baseline)
    assert Energy.active_above_resting(10, 7200, 187.4) == 0
    # nil-safe
    assert Energy.active_above_resting(nil, nil, 187.4) == 0
  end

  test "the resting anchor is configurable" do
    Application.put_env(:fitness_fetch, :resting_anchor, {180.0, 1900})
    on_exit(fn -> Application.delete_env(:fitness_fetch, :resting_anchor) end)

    assert Energy.anchor() == {180.0, 1900}
    assert Energy.resting_calories(180.0) == 1900
  end
end
