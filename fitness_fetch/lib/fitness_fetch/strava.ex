defmodule FitnessFetch.Strava do
  @moduledoc """
  Minimal Strava API client.

  Refreshes a short-lived access token from a stored long-lived refresh token,
  then pulls athlete activities in a date range. Both the Garmin watch (runs)
  and the Coros Dura (rides) sync into Strava, so this is the unified activity
  source.

  Credentials come from environment variables, injected by mise via
  `.mise.local.toml`:

    * `STRAVA_CLIENT_ID`
    * `STRAVA_CLIENT_SECRET`
    * `STRAVA_REFRESH_TOKEN`

  Run the one-time `mix strava.auth` flow to obtain the refresh token.
  See `fitness_fetch/README.md`.
  """

  @token_url "https://www.strava.com/oauth/token"
  @api "https://www.strava.com/api/v3"

  @doc "Fetch a fresh access token using the stored refresh token."
  @spec access_token() :: {:ok, String.t()} | {:error, term()}
  def access_token do
    resp =
      Req.post!(@token_url,
        form: [
          client_id: fetch_env!("STRAVA_CLIENT_ID"),
          client_secret: fetch_env!("STRAVA_CLIENT_SECRET"),
          grant_type: "refresh_token",
          refresh_token: fetch_env!("STRAVA_REFRESH_TOKEN")
        ]
      )

    case resp.body do
      %{"access_token" => token} -> {:ok, token}
      other -> {:error, other}
    end
  end

  @doc """
  Exchange a one-time authorization `code` (from the browser consent flow) for
  tokens. Used by `mix strava.auth`. Returns the raw token response map.
  """
  @spec exchange_code(String.t()) :: map()
  def exchange_code(code) do
    Req.post!(@token_url,
      form: [
        client_id: fetch_env!("STRAVA_CLIENT_ID"),
        client_secret: fetch_env!("STRAVA_CLIENT_SECRET"),
        grant_type: "authorization_code",
        code: code
      ]
    ).body
  end

  @doc """
  List activities whose LOCAL start date falls within `[from_date, to_date]`
  (inclusive), oldest first. Returns raw Strava activity maps.
  """
  @spec list_activities(Date.t(), Date.t()) :: [map()]
  def list_activities(%Date{} = from_date, %Date{} = to_date) do
    {:ok, token} = access_token()

    # Pad the epoch window by a day on each side to sidestep timezone edges,
    # then filter precisely on each activity's LOCAL start date.
    after_ts = date_to_unix(Date.add(from_date, -1))
    before_ts = date_to_unix(Date.add(to_date, 2))

    token
    |> fetch_pages(after_ts, before_ts, 1, [])
    |> Enum.filter(fn act ->
      case local_date(act) do
        {:ok, d} ->
          Date.compare(d, from_date) != :lt and Date.compare(d, to_date) != :gt

        _ ->
          false
      end
    end)
    |> Enum.sort_by(& &1["start_date_local"])
  end

  @doc "Extract the local calendar `Date` from an activity map."
  @spec local_date(map()) :: {:ok, Date.t()} | {:error, term()}
  def local_date(%{"start_date_local" => s}) when is_binary(s) do
    s |> String.slice(0, 10) |> Date.from_iso8601()
  end

  def local_date(_), do: :error

  defp fetch_pages(token, after_ts, before_ts, page, acc) do
    resp =
      Req.get!("#{@api}/athlete/activities",
        auth: {:bearer, token},
        params: [after: after_ts, before: before_ts, page: page, per_page: 100]
      )

    case resp.body do
      list when is_list(list) and list != [] ->
        fetch_pages(token, after_ts, before_ts, page + 1, [list | acc])

      _ ->
        acc |> Enum.reverse() |> List.flatten()
    end
  end

  defp date_to_unix(%Date{} = d) do
    {:ok, dt} = DateTime.new(d, ~T[00:00:00], "Etc/UTC")
    DateTime.to_unix(dt)
  end

  defp fetch_env!(key) do
    System.get_env(key) ||
      raise """
      Missing environment variable #{key}.

      Set it in .mise.local.toml under [env], e.g.:

          [env]
          #{key} = "..."

      See fitness_fetch/README.md for the Strava setup steps.
      """
  end
end
