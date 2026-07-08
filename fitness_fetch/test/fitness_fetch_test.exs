defmodule FitnessFetch.FormatTest do
  use ExUnit.Case, async: true
  alias FitnessFetch.Format

  # Strava returns SI units: distance/elevation in metres, times in seconds,
  # speed in m/s, temp in °C.

  defp ride do
    %{
      "name" => "Ride to Yellow Springs",
      "sport_type" => "GravelRide",
      "start_date_local" => "2026-07-04T09:00:00Z",
      # 62.77 mi
      "distance" => 101_020.0,
      # 1,473 ft
      "total_elevation_gain" => 448.96,
      "moving_time" => 19_043,
      "elapsed_time" => 39_143,
      "average_speed" => 5.3,
      "has_heartrate" => true,
      "average_heartrate" => 104.0,
      "max_heartrate" => 142.0,
      "device_watts" => false
    }
  end

  defp run do
    %{
      "name" => "Trail run",
      "sport_type" => "TrailRun",
      "start_date_local" => "2026-07-02T07:00:00Z",
      # ~6.11 mi
      "distance" => 9834.0,
      # 786 ft
      "total_elevation_gain" => 239.57,
      "moving_time" => 4902,
      "elapsed_time" => 4957,
      "average_speed" => 2.006,
      "has_heartrate" => true,
      "average_heartrate" => 140.0,
      "max_heartrate" => 157.0
    }
  end

  test "ride renders a cycling table row with HR/RPE power (no power meter)" do
    out = Format.report([ride()], ~D[2026-06-29], ~D[2026-07-05])

    assert out =~ "62.77 mi"
    assert out =~ "1473 ft"
    assert out =~ "Sat Jul 4"
    # HR/RPE because device_watts is false (Cutthroat)
    assert out =~ "| HR/RPE |"
    assert out =~ "104 (142 max)"
    # moving time 19043s = 5:17:23
    assert out =~ "5:17:23"
  end

  test "run renders a running table row with pace" do
    out = Format.report([run()], ~D[2026-06-29], ~D[2026-07-05])

    assert out =~ "6.11 mi"
    assert out =~ "TrailRun"
    # 4902s / 6.11mi ≈ 13:22/mi
    assert out =~ ~r{13:2\d/mi}
    assert out =~ "140 (157 max)"
  end

  test "weekly totals summarize distance and sport counts" do
    out = Format.report([ride(), run()], ~D[2026-06-29], ~D[2026-07-05])

    assert out =~ "2 activities"
    assert out =~ "GravelRide ×1"
    assert out =~ "TrailRun ×1"
  end
end
