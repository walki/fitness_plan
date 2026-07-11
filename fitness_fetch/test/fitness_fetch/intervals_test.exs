defmodule FitnessFetch.IntervalsTest do
  # async: false — sets INTERVALS_* env + :req_options globally.
  use ExUnit.Case, async: false
  alias FitnessFetch.Intervals

  describe "normalize_activity/1" do
    test "picks the computed icu_* fields" do
      a =
        Intervals.normalize_activity(%{
          "start_date_local" => "2026-07-09T15:00:00",
          "name" => "Did not miss the rain",
          "type" => "Ride",
          "icu_training_load" => 136,
          "icu_intensity" => 70,
          "icu_ftp" => 230,
          "icu_weighted_avg_watts" => 161.0,
          "icu_efficiency_factor" => 1.30,
          "decoupling" => 4.2,
          "average_heartrate" => 124.0,
          "max_heartrate" => 160.0
        })

      assert a.date == ~D[2026-07-09]
      assert a.tss == 136
      assert a.ftp == 230
      assert a.np == 161.0
      assert a.decoupling == 4.2
      assert a.avg_hr == 124.0
    end
  end

  describe "normalize_wellness/1 + form/2" do
    test "computes form as CTL − ATL" do
      w = Intervals.normalize_wellness(%{"id" => "2026-07-10", "ctl" => 62.4, "atl" => 71.0, "restingHR" => 49})
      assert w.date == ~D[2026-07-10]
      assert w.form == round(62.4 - 71.0)
      assert w.resting_hr == 49
    end

    test "form is nil when a component is missing" do
      assert Intervals.form(50, nil) == nil
      assert Intervals.form(50, 40) == 10
    end
  end

  describe "activities/2 + wellness/2 (stubbed API)" do
    setup do
      System.put_env(%{"INTERVALS_ATHLETE_ID" => "i123", "INTERVALS_API_KEY" => "key"})
      Application.put_env(:fitness_fetch, :req_options, plug: {Req.Test, FitnessFetch.Strava})

      on_exit(fn ->
        Enum.each(~w(INTERVALS_ATHLETE_ID INTERVALS_API_KEY), &System.delete_env/1)
        Application.delete_env(:fitness_fetch, :req_options)
      end)

      :ok
    end

    test "activities are normalized and sorted oldest first" do
      Req.Test.stub(FitnessFetch.Strava, fn conn ->
        assert conn.request_path == "/api/v1/athlete/i123/activities"

        Req.Test.json(conn, [
          %{"start_date_local" => "2026-07-09T15:00:00", "name" => "Ride B", "icu_training_load" => 136},
          %{"start_date_local" => "2026-07-06T12:00:00", "name" => "Ride A", "icu_training_load" => 90}
        ])
      end)

      acts = Intervals.activities(~D[2026-07-06], ~D[2026-07-12])
      assert Enum.map(acts, & &1.name) == ["Ride A", "Ride B"]
      assert Enum.map(acts, & &1.tss) == [90, 136]
    end

    test "wellness is normalized with form" do
      Req.Test.stub(FitnessFetch.Strava, fn conn ->
        assert conn.request_path == "/api/v1/athlete/i123/wellness"

        Req.Test.json(conn, [
          %{"id" => "2026-07-10", "ctl" => 60.0, "atl" => 72.0, "restingHR" => 49}
        ])
      end)

      assert [w] = Intervals.wellness(~D[2026-07-06], ~D[2026-07-12])
      assert w.form == -12
    end
  end
end
