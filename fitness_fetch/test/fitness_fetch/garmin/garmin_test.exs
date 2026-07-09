defmodule FitnessFetch.GarminTest do
  # async: false — sets GARMIN_BEARER + :req_options globally.
  use ExUnit.Case, async: false
  alias FitnessFetch.Garmin

  describe "parse_sleep/2" do
    test "normalizes score, quality, duration and times" do
      body = %{
        "dailySleepDTO" => %{
          "sleepTimeSeconds" => 23_880,
          "sleepScores" => %{"overall" => %{"value" => 66, "qualifierKey" => "FAIR"}},
          "sleepStartTimestampLocal" => 1_751_330_760_000,
          "sleepEndTimestampLocal" => 1_751_354_640_000
        }
      }

      s = Garmin.parse_sleep(body, ~D[2026-06-30])
      assert s.score == 66
      assert s.quality == "Fair"
      assert s.duration_seconds == 23_880
      assert s.bedtime =~ ~r/\d{1,2}:\d{2}\s(AM|PM)/
      assert s.wake =~ ~r/\d{1,2}:\d{2}\s(AM|PM)/
    end

    test "returns nil when the DTO is missing" do
      assert Garmin.parse_sleep(%{}, ~D[2026-06-30]) == nil
    end
  end

  describe "parse_resting_hr/2" do
    test "extracts the resting heart rate" do
      assert Garmin.parse_resting_hr(%{"restingHeartRate" => 52}, ~D[2026-06-30]) ==
               %{date: ~D[2026-06-30], resting_hr: 52}
    end

    test "nil when absent" do
      assert Garmin.parse_resting_hr(%{}, ~D[2026-06-30]) == nil
    end
  end

  describe "parse_blood_pressure/1" do
    test "flattens measurementSummaries with real Garmin fields" do
      # Shape confirmed live: local timestamp is an offset-less ISO string,
      # category comes as categoryName.
      body = %{
        "measurementSummaries" => [
          %{
            "measurements" => [
              %{
                "systolic" => 114,
                "diastolic" => 77,
                "pulse" => 52,
                "category" => "NORMAL",
                "categoryName" => "NORMAL",
                "measurementTimestampLocal" => "2026-06-30T07:39:08.0"
              }
            ]
          }
        ]
      }

      assert [reading] = Garmin.parse_blood_pressure(body)
      assert reading.systolic == 114
      assert reading.diastolic == 77
      assert reading.pulse == 52
      assert reading.category == "Normal"
      assert reading.date == ~D[2026-06-30]
      assert reading.time == "7:39 AM"
    end

    test "derives an AHA category when Garmin omits one" do
      body = [%{"systolic" => 135, "diastolic" => 85, "pulse" => 60, "measurementTimestampLocal" => nil}]
      assert [%{category: "Stage 1"}] = Garmin.parse_blood_pressure(body)
    end

    test "empty for an unexpected shape" do
      assert Garmin.parse_blood_pressure(%{"unexpected" => true}) == []
    end
  end

  describe "wellness/2 (stubbed API, GARMIN_BEARER set)" do
    setup do
      System.put_env("GARMIN_BEARER", "test-bearer")
      Application.put_env(:fitness_fetch, :req_options, plug: {Req.Test, FitnessFetch.Strava})

      on_exit(fn ->
        System.delete_env("GARMIN_BEARER")
        Application.delete_env(:fitness_fetch, :req_options)
      end)

      :ok
    end

    test "assembles sleep, resting HR, and BP for the range" do
      Req.Test.stub(FitnessFetch.Strava, fn conn ->
        cond do
          conn.request_path == "/userprofile-service/socialProfile" ->
            Req.Test.json(conn, %{"displayName" => "roger"})

          String.starts_with?(conn.request_path, "/wellness-service/wellness/dailySleepData/") ->
            Req.Test.json(conn, %{
              "dailySleepDTO" => %{
                "sleepTimeSeconds" => 23_880,
                "sleepScores" => %{"overall" => %{"value" => 66, "qualifierKey" => "FAIR"}}
              }
            })

          String.starts_with?(conn.request_path, "/usersummary-service/usersummary/daily/") ->
            Req.Test.json(conn, %{"restingHeartRate" => 52})

          String.starts_with?(conn.request_path, "/bloodpressure-service/bloodpressure/range/") ->
            Req.Test.json(conn, %{
              "measurementSummaries" => [
                %{"measurements" => [%{"systolic" => 114, "diastolic" => 77, "pulse" => 52, "category" => "NORMAL"}]}
              ]
            })
        end
      end)

      assert {:ok, data} = Garmin.wellness(~D[2026-06-29], ~D[2026-06-30])

      # two days in range → two sleep + two RHR entries
      assert length(data.sleep) == 2
      assert length(data.resting_hr) == 2
      assert Enum.all?(data.resting_hr, &(&1.resting_hr == 52))
      assert [%{systolic: 114}] = data.blood_pressure
    end
  end
end
