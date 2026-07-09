defmodule FitnessFetch.Garmin.Auth do
  @moduledoc """
  Garmin Connect authentication.

  Garmin has no official API. The working approach (same as the Python `garth`
  library) is a reverse-engineered handshake:

    1. SSO sign-in at `sso.garmin.com` (grab a CSRF token, POST credentials,
       parse a service `ticket` out of the response).
    2. Exchange the ticket for an **OAuth1** token at `connectapi.garmin.com`
       (request signed with a public consumer key/secret).
    3. Exchange the OAuth1 token for a short-lived **OAuth2** bearer token.

  The bearer token is what `FitnessFetch.Garmin` uses for wellness endpoints.
  Tokens are cached to `~/.fitness_fetch/garmin_token.json` and the OAuth2 token
  is refreshed from the cached OAuth1 token when it expires.

  Credentials come from the environment (via `.mise.local.toml`):

    * `GARMIN_EMAIL`, `GARMIN_PASSWORD`

  ## Escape hatch

  The SSO handshake is the fragile part (Cloudflare, and MFA is not yet
  supported). If it fails, set `GARMIN_BEARER` to an OAuth2 access token
  obtained elsewhere (e.g. Python `garth`) and everything downstream works.

  > MFA accounts are not yet handled — `login/0` raises a clear error if Garmin
  > returns an MFA challenge.
  """

  @sso "https://sso.garmin.com/sso"
  @connectapi "https://connectapi.garmin.com"
  @consumer_url "https://thegarth.s3.amazonaws.com/oauth_consumer.json"

  # Garth's UAs: a browser-like UA for the SSO pages, the mobile app UA for the
  # connectapi OAuth calls.
  @sso_ua "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
  @api_ua "com.garmin.android.apps.connectmobile"

  @token_path Path.join([System.user_home() || ".", ".fitness_fetch", "garmin_token.json"])

  @doc """
  Return a valid OAuth2 bearer token, doing whatever is necessary: honor the
  `GARMIN_BEARER` override, reuse a cached token, refresh an expired one, or run
  a full login.
  """
  @spec bearer() :: {:ok, String.t()} | {:error, term()}
  def bearer do
    cond do
      override = System.get_env("GARMIN_BEARER") ->
        {:ok, override}

      token = valid_cached_token() ->
        {:ok, token["access_token"]}

      oauth1 = cached_oauth1() ->
        with {:ok, oauth2} <- exchange_oauth2(oauth1) do
          cache(%{"oauth1" => oauth1, "oauth2" => stamp(oauth2)})
          {:ok, oauth2["access_token"]}
        end

      true ->
        with {:ok, %{oauth1: oauth1, oauth2: oauth2}} <- login() do
          cache(%{"oauth1" => oauth1, "oauth2" => stamp(oauth2)})
          {:ok, oauth2["access_token"]}
        end
    end
  end

  @doc """
  Run the full SSO → OAuth1 → OAuth2 login using `GARMIN_EMAIL`/`GARMIN_PASSWORD`.
  Returns `%{oauth1: map, oauth2: map}`.
  """
  @spec login() :: {:ok, map()} | {:error, term()}
  def login do
    email = fetch_env!("GARMIN_EMAIL")
    password = fetch_env!("GARMIN_PASSWORD")

    with {:ok, ticket} <- sso_ticket(email, password),
         {:ok, oauth1} <- oauth1_token(ticket),
         {:ok, oauth2} <- exchange_oauth2(oauth1) do
      {:ok, %{oauth1: oauth1, oauth2: oauth2}}
    end
  end

  # --- SSO -----------------------------------------------------------------

  defp sso_ticket(email, password) do
    params = [
      id: "gauth-widget",
      embedWidget: "true",
      gauthHost: @sso,
      service: "#{@sso}/embed",
      source: "#{@sso}/embed",
      redirectAfterAccountLoginUrl: "#{@sso}/embed",
      redirectAfterAccountCreationUrl: "#{@sso}/embed"
    ]

    # 1. prime cookies
    req = req_client(base_url: @sso, headers: [{"user-agent", @sso_ua}])
    Req.get!(req, url: "/embed", params: [id: "gauth-widget", embedWidget: "true", gauthHost: @sso])

    # 2. fetch the sign-in page for the CSRF token
    signin = Req.get!(req, url: "/signin", params: params)
    csrf = extract(signin.body, ~r/name="_csrf"\s+value="([^"]+)"/)

    if is_nil(csrf) do
      {:error, :no_csrf}
    else
      # 3. submit credentials
      res =
        Req.post!(req,
          url: "/signin",
          params: params,
          headers: [{"referer", "#{@sso}/signin"}],
          form: [username: email, password: password, embed: "true", _csrf: csrf]
        )

      cond do
        String.contains?(to_string(res.body), "mfa") and is_nil(ticket(res.body)) ->
          {:error, :mfa_required}

        ticket = ticket(res.body) ->
          {:ok, ticket}

        true ->
          {:error, :login_failed}
      end
    end
  end

  defp ticket(body), do: extract(to_string(body), ~r/embed\?ticket=([^"]+)"/)

  # --- OAuth1 --------------------------------------------------------------

  defp oauth1_token(ticket) do
    {key, secret} = consumer_credentials()

    url = "#{@connectapi}/oauth-service/oauth/preauthorized"

    query = [
      {"ticket", ticket},
      {"login-url", "#{@sso}/embed"},
      {"accepts-mfa-tokens", "true"}
    ]

    header = oauth1_header("GET", url, key, secret, nil, nil, query)

    resp =
      Req.get!(req_client(),
        url: url,
        params: query,
        headers: [{"authorization", header}, {"user-agent", @api_ua}]
      )

    parsed = URI.decode_query(to_string(resp.body))

    case parsed do
      %{"oauth_token" => t, "oauth_token_secret" => s} ->
        {:ok, %{"token" => t, "secret" => s, "mfa_token" => parsed["mfa_token"], "key" => key, "consumer_secret" => secret}}

      _ ->
        {:error, {:oauth1_failed, parsed}}
    end
  end

  # --- OAuth2 --------------------------------------------------------------

  defp exchange_oauth2(oauth1) do
    key = oauth1["key"] || elem(consumer_credentials(), 0)
    secret = oauth1["consumer_secret"] || elem(consumer_credentials(), 1)
    url = "#{@connectapi}/oauth-service/oauth/exchange/user/2.0"

    header = oauth1_header("POST", url, key, secret, oauth1["token"], oauth1["secret"], [])
    form = if oauth1["mfa_token"], do: [mfa_token: oauth1["mfa_token"]], else: []

    resp =
      Req.post!(req_client(),
        url: url,
        headers: [
          {"authorization", header},
          {"user-agent", @api_ua},
          {"content-type", "application/x-www-form-urlencoded"}
        ],
        form: form
      )

    case resp.body do
      %{"access_token" => _} = token -> {:ok, token}
      other -> {:error, {:oauth2_failed, other}}
    end
  end

  # --- OAuth1 signing (RFC 5849, HMAC-SHA1) --------------------------------

  @doc false
  # Public for testing against a known vector.
  def oauth1_header(method, url, consumer_key, consumer_secret, token, token_secret, extra_params) do
    oauth_params =
      %{
        "oauth_consumer_key" => consumer_key,
        "oauth_nonce" => nonce(),
        "oauth_signature_method" => "HMAC-SHA1",
        "oauth_timestamp" => Integer.to_string(System.system_time(:second)),
        "oauth_version" => "1.0"
      }
      |> maybe_put("oauth_token", token)

    all = Enum.map(oauth_params, fn {k, v} -> {k, v} end) ++ extra_params
    sig = oauth1_signature(method, url, all, consumer_secret, token_secret)

    header_params =
      oauth_params
      |> Map.put("oauth_signature", sig)
      |> Enum.map(fn {k, v} -> "#{enc(k)}=\"#{enc(v)}\"" end)
      |> Enum.sort()
      |> Enum.join(", ")

    "OAuth " <> header_params
  end

  @doc false
  # Pure signature-base-string → HMAC-SHA1 → base64. Params is a list of
  # {key, value} pairs (all oauth_* plus any query/body params).
  def oauth1_signature(method, url, params, consumer_secret, token_secret) do
    param_string =
      params
      |> Enum.map(fn {k, v} -> {enc(to_string(k)), enc(to_string(v))} end)
      |> Enum.sort()
      |> Enum.map(fn {k, v} -> "#{k}=#{v}" end)
      |> Enum.join("&")

    base = "#{method}&#{enc(url)}&#{enc(param_string)}"
    key = "#{enc(consumer_secret)}&#{enc(token_secret || "")}"

    :crypto.mac(:hmac, :sha, key, base) |> Base.encode64()
  end

  # RFC 3986 percent-encoding (unreserved: A-Z a-z 0-9 - _ . ~)
  defp enc(s), do: URI.encode(to_string(s), &URI.char_unreserved?/1)

  defp nonce, do: :crypto.strong_rand_bytes(16) |> Base.encode16(case: :lower)

  defp maybe_put(map, _k, nil), do: map
  defp maybe_put(map, k, v), do: Map.put(map, k, v)

  # --- consumer credentials, token cache, misc ----------------------------

  defp consumer_credentials do
    case Req.get!(req_client(), url: @consumer_url).body do
      %{"consumer_key" => k, "consumer_secret" => s} -> {k, s}
      _ -> raise "could not fetch Garmin OAuth consumer credentials from #{@consumer_url}"
    end
  end

  defp valid_cached_token do
    with %{"oauth2" => oauth2} <- read_cache(),
         true <- is_map(oauth2),
         exp when is_integer(exp) <- oauth2["expires_at"],
         true <- exp - 60 > System.system_time(:second) do
      oauth2
    else
      _ -> nil
    end
  end

  defp cached_oauth1 do
    case read_cache() do
      %{"oauth1" => oauth1} when is_map(oauth1) -> oauth1
      _ -> nil
    end
  end

  defp stamp(%{"expires_in" => secs} = oauth2) when is_integer(secs) do
    Map.put(oauth2, "expires_at", System.system_time(:second) + secs)
  end

  defp stamp(oauth2), do: oauth2

  defp read_cache do
    with {:ok, body} <- File.read(@token_path),
         {:ok, json} <- Jason.decode(body) do
      json
    else
      _ -> nil
    end
  end

  defp cache(map) do
    File.mkdir_p!(Path.dirname(@token_path))
    File.write!(@token_path, Jason.encode!(map))
  end

  defp req_client(opts \\ []) do
    base = Req.new(opts)

    case Application.get_env(:fitness_fetch, :req_options) do
      nil -> base
      extra -> Req.merge(base, extra)
    end
  end

  defp extract(body, regex) do
    case Regex.run(regex, to_string(body)) do
      [_, captured] -> captured
      _ -> nil
    end
  end

  defp fetch_env!(key) do
    System.get_env(key) ||
      raise "Missing environment variable #{key}. Set it in fitness_fetch/.mise.local.toml (see README)."
  end
end
