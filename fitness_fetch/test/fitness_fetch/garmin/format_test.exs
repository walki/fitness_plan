defmodule FitnessFetch.Garmin.FormatTest do
  use ExUnit.Case, async: true
  alias FitnessFetch.Garmin.Format

  @from ~D[2026-06-29]
  @to ~D[2026-07-05]

  defp wellness do
    %{
      sleep: [
        %{
          date: ~D[2026-06-30],
          score: 66,
          quality: "Fair",
          duration_seconds: 23_880,
          bedtime: "11:46 PM",
          wake: "6:46 AM"
        }
      ],
      resting_hr: [%{date: ~D[2026-06-30], resting_hr: 52}],
      blood_pressure: [
        %{date: ~D[2026-06-30], time: "7:39 AM", systolic: 114, diastolic: 77, pulse: 52, category: "Normal"}
      ]
    }
  end

  test "sleep section renders the weekly-log sleep table" do
    out = Format.report(wellness(), @from, @to)
    assert out =~ "| Date | Score | Quality | Duration | Bedtime | Wake |"
    # 23_880 s = 6h 38m
    assert out =~ "| Jun 30 | 66 | Fair | 6h 38m | 11:46 PM | 6:46 AM |"
  end

  test "resting HR section" do
    out = Format.report(wellness(), @from, @to)
    assert out =~ "| Jun 30 | 52 |"
  end

  test "BP section renders reading/pulse/category" do
    out = Format.report(wellness(), @from, @to)
    assert out =~ "| Date | Time | Reading | HR | Category |"
    assert out =~ "| Jun 30 | 7:39 AM | 114/77 | 52 | Normal |"
  end

  test "empty sections degrade gracefully" do
    out = Format.report(%{sleep: [], resting_hr: [], blood_pressure: []}, @from, @to)
    assert out =~ "(no sleep data)"
    assert out =~ "(no resting HR data)"
    assert out =~ "no readings"
  end
end
