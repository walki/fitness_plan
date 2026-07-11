defmodule FitnessFetch.Intervals.FormatTest do
  use ExUnit.Case, async: true
  alias FitnessFetch.Intervals.Format

  @from ~D[2026-07-06]
  @to ~D[2026-07-12]

  test "activity metrics table shows TSS, decoupling, EF, NP" do
    activities = [
      %{
        date: ~D[2026-07-09],
        name: "Did not miss the rain",
        type: "Ride",
        tss: 136,
        intensity: 70,
        np: 161.0,
        ef: 1.30,
        decoupling: 4.2,
        avg_hr: 124.0,
        max_hr: 160.0
      }
    ]

    out = Format.report(activities, [], @from, @to)
    assert out =~ "| Jul 9 | Did not miss the rain | Ride | 136 | 70% | 161W | 1.3 | 4.2% | 124 (160 max) |"
  end

  test "form section shows CTL/ATL/form and calls out the latest" do
    wellness = [
      %{date: ~D[2026-07-09], ctl: 61.0, atl: 65.0, form: -4, resting_hr: 48, sleep_secs: nil, weight: nil},
      %{date: ~D[2026-07-10], ctl: 60.0, atl: 72.0, form: -12, resting_hr: 49, sleep_secs: nil, weight: nil}
    ]

    out = Format.report([], wellness, @from, @to)
    assert out =~ "| Jul 10 | 60.0 | 72.0 | -12 | 49 |"
    assert out =~ "Latest form: **-12**"
  end

  test "positive form is rendered with a leading +" do
    wellness = [%{date: ~D[2026-07-06], ctl: 55.0, atl: 48.0, form: 7, resting_hr: 45, sleep_secs: nil, weight: nil}]
    out = Format.report([], wellness, @from, @to)
    assert out =~ "Latest form: **+7**"
  end

  test "empty inputs degrade gracefully" do
    out = Format.report([], [], @from, @to)
    assert out =~ "(no activities)"
    assert out =~ "(no wellness data)"
  end
end
