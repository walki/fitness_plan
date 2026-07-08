defmodule Mix.Tasks.Strava.Auth do
  @shortdoc "One-time Strava OAuth flow to get a refresh token"

  @moduledoc """
  One-time Strava OAuth helper to obtain a refresh token.

  ## Step 1 — print the consent URL (needs STRAVA_CLIENT_ID set)

      mise exec -- mix strava.auth

  Open the URL, click Authorize. Strava redirects to
  `http://localhost/exchange?...&code=THECODE&...` — the page won't load,
  that's fine. Copy the `code` value from the address bar.

  ## Step 2 — exchange the code for tokens

      mise exec -- mix strava.auth THECODE

  Copy the printed `refresh_token` into `.mise.local.toml` under `[env]`.
  """
  use Mix.Task
  alias FitnessFetch.Strava

  @redirect "http://localhost/exchange"
  @scope "activity:read_all"

  @impl true
  def run([]) do
    client_id =
      System.get_env("STRAVA_CLIENT_ID") ||
        Mix.raise("Set STRAVA_CLIENT_ID in .mise.local.toml first (see fitness_fetch/README.md)")

    url =
      "https://www.strava.com/oauth/authorize?" <>
        URI.encode_query(
          client_id: client_id,
          redirect_uri: @redirect,
          response_type: "code",
          approval_prompt: "force",
          scope: @scope
        )

    IO.puts("""

    1. Open this URL in your browser and click "Authorize":

       #{url}

    2. Strava redirects to a localhost URL that won't load — that's expected.
       Copy the `code=...` value out of the address bar, then run:

       mise exec -- mix strava.auth <code>
    """)
  end

  def run([code | _]) do
    Application.ensure_all_started(:req)

    case Strava.exchange_code(code) do
      %{"refresh_token" => refresh, "access_token" => access} = body ->
        athlete = body["athlete"] || %{}
        name = String.trim("#{athlete["firstname"]} #{athlete["lastname"]}")

        IO.puts("""

        Success#{if name != "", do: " — authorized as #{name}", else: ""}.

        Add this line to .mise.local.toml under [env]:

            STRAVA_REFRESH_TOKEN = "#{refresh}"

        (Access tokens expire ~6h and are refreshed automatically on each fetch.
         Current one, for reference: #{access})
        """)

      other ->
        Mix.raise("Token exchange failed: #{inspect(other)}")
    end
  end
end
