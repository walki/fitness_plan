defmodule FitnessFetch.FormatTest do
  use ExUnit.Case, async: true
  alias FitnessFetch.Format

  # Strava returns SI units: distance/elevation in metres, times in seconds,
  # speed in m/s, temp in °C.

  @from ~D[2026-06-29]
  @to ~D[2026-07-05]

  defp ride(overrides \\ %{}) do
    Map.merge(
      %{
        "name" => "Ride to Yellow Springs",
        "sport_type" => "GravelRide",
        "start_date_local" => "2026-07-04T09:00:00Z",
        # 62.77 mi, 1,473 ft
        "distance" => 101_020.0,
        "total_elevation_gain" => 448.96,
        "moving_time" => 19_043,
        "elapsed_time" => 39_143,
        "average_speed" => 5.3,
        "has_heartrate" => true,
        "average_heartrate" => 104.0,
        "max_heartrate" => 142.0,
        "device_watts" => false
      },
      overrides
    )
  end

  defp run(overrides \\ %{}) do
    Map.merge(
      %{
        "name" => "Trail run",
        "sport_type" => "TrailRun",
        "start_date_local" => "2026-07-02T07:00:00Z",
        # ~6.11 mi, 786 ft
        "distance" => 9834.0,
        "total_elevation_gain" => 239.57,
        "moving_time" => 4902,
        "elapsed_time" => 4957,
        "average_speed" => 2.006,
        "has_heartrate" => true,
        "average_heartrate" => 140.0,
        "max_heartrate" => 157.0
      },
      overrides
    )
  end

  describe "cycling rows" do
    test "no power meter → HR/RPE, imperial conversions, moving time" do
      out = Format.report([ride()], @from, @to)

      assert out =~ "62.77 mi"
      assert out =~ "1473 ft"
      assert out =~ "Sat Jul 4"
      assert out =~ "| HR/RPE |"
      assert out =~ "104 (142 max)"
      # 19_043 s = 5:17:23
      assert out =~ "5:17:23"
    end

    test "power meter → NP / avg watts" do
      out =
        Format.report(
          [ride(%{"device_watts" => true, "weighted_average_watts" => 199, "average_watts" => 174.2})],
          @from,
          @to
        )

      assert out =~ "199W NP / 174W avg"
    end

    test "estimated watts (no meter) → ~W est" do
      out = Format.report([ride(%{"average_watts" => 151.4})], @from, @to)
      assert out =~ "~151W est"
    end

    test "average temperature converts °C → °F with the device-temp caveat" do
      out = Format.report([ride(%{"average_temp" => 35})], @from, @to)
      # 35°C = 95°F
      assert out =~ "95°F"
      assert out =~ "device temp"
    end
  end

  describe "running rows" do
    test "renders pace per mile and running table format" do
      out = Format.report([run()], @from, @to)

      assert out =~ "6.11 mi"
      assert out =~ "TrailRun"
      # 4902 s / 6.11 mi ≈ 13:22/mi
      assert out =~ ~r{13:2\d/mi}
      assert out =~ "140 (157 max)"
    end

    test "run without heart rate shows a blank HR cell" do
      out = Format.report([run(%{"has_heartrate" => false, "average_heartrate" => nil})], @from, @to)
      assert out =~ "| — |"
    end
  end

  describe "weekly summary" do
    test "counts activities by sport and totals distance" do
      out = Format.report([ride(), run()], @from, @to)

      assert out =~ "2 activities"
      assert out =~ "GravelRide ×1"
      assert out =~ "TrailRun ×1"
      # 62.77 + 6.11 ≈ 68.9 mi
      assert out =~ "68.9 mi"
    end

    test "empty list is handled gracefully" do
      out = Format.report([], @from, @to)
      assert out =~ "0 activities found"
      assert out =~ "(no activities)"
    end
  end
end
