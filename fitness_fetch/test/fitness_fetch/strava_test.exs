defmodule FitnessFetch.StravaTest do
  # async: false — the tests toggle global Application/System env.
  use ExUnit.Case, async: false
  alias FitnessFetch.Strava

  setup do
    Application.put_env(:fitness_fetch, :req_options, plug: {Req.Test, FitnessFetch.Strava})

    System.put_env(%{
      "STRAVA_CLIENT_ID" => "id",
      "STRAVA_CLIENT_SECRET" => "secret",
      "STRAVA_REFRESH_TOKEN" => "refresh"
    })

    on_exit(fn ->
      Application.delete_env(:fitness_fetch, :req_options)
      Enum.each(~w(STRAVA_CLIENT_ID STRAVA_CLIENT_SECRET STRAVA_REFRESH_TOKEN), &System.delete_env/1)
    end)

    :ok
  end

  describe "access_token/0" do
    test "returns the access token from a successful refresh" do
      Req.Test.stub(FitnessFetch.Strava, fn conn ->
        assert conn.request_path == "/oauth/token"
        Req.Test.json(conn, %{"access_token" => "abc123", "expires_at" => 123})
      end)

      assert {:ok, "abc123"} = Strava.access_token()
    end

    test "returns an error tuple when the response carries no token" do
      Req.Test.stub(FitnessFetch.Strava, fn conn ->
        Req.Test.json(conn, %{"message" => "Bad Request"})
      end)

      assert {:error, %{"message" => "Bad Request"}} = Strava.access_token()
    end

    test "raises a helpful error when a credential env var is missing" do
      System.delete_env("STRAVA_CLIENT_ID")

      assert_raise RuntimeError, ~r/Missing environment variable STRAVA_CLIENT_ID/, fn ->
        Strava.access_token()
      end
    end
  end

  describe "exchange_code/1" do
    test "returns the token body including the refresh token" do
      Req.Test.stub(FitnessFetch.Strava, fn conn ->
        Req.Test.json(conn, %{
          "access_token" => "acc",
          "refresh_token" => "ref",
          "athlete" => %{"firstname" => "Roger", "lastname" => "Walker"}
        })
      end)

      body = Strava.exchange_code("thecode")
      assert body["refresh_token"] == "ref"
      assert body["athlete"]["firstname"] == "Roger"
    end
  end

  describe "list_activities/2" do
    test "paginates, filters to the local date range, and sorts oldest first" do
      pages = %{
        1 => [
          activity("In range B", "2026-07-04T09:00:00Z"),
          activity("In range A", "2026-07-01T07:00:00Z")
        ],
        2 => [
          activity("Out of range (after)", "2026-07-09T07:00:00Z"),
          activity("In range C", "2026-07-05T07:00:00Z"),
          activity("Out of range (before)", "2026-06-20T07:00:00Z")
        ],
        3 => []
      }

      stub_token_and_activities(pages)

      names =
        ~D[2026-06-29]
        |> Strava.list_activities(~D[2026-07-05])
        |> Enum.map(& &1["name"])

      assert names == ["In range A", "In range B", "In range C"]
    end

    test "returns [] when there are no activities in range" do
      stub_token_and_activities(%{1 => []})
      assert Strava.list_activities(~D[2026-06-29], ~D[2026-07-05]) == []
    end
  end

  describe "local_date/1" do
    test "extracts the local calendar date" do
      assert Strava.local_date(%{"start_date_local" => "2026-07-04T09:00:00Z"}) ==
               {:ok, ~D[2026-07-04]}
    end

    test "errors on a missing field" do
      assert Strava.local_date(%{}) == :error
    end
  end

  # --- helpers ---

  defp activity(name, start_local) do
    %{
      "name" => name,
      "sport_type" => "Run",
      "start_date_local" => start_local,
      "distance" => 1000.0
    }
  end

  defp stub_token_and_activities(pages) do
    Req.Test.stub(FitnessFetch.Strava, fn conn ->
      case conn.request_path do
        "/oauth/token" ->
          Req.Test.json(conn, %{"access_token" => "abc"})

        "/api/v3/athlete/activities" ->
          conn = Plug.Conn.fetch_query_params(conn)
          page = String.to_integer(conn.query_params["page"] || "1")
          Req.Test.json(conn, Map.get(pages, page, []))
      end
    end)
  end
end
