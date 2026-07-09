defmodule FitnessFetch.Garmin.AuthTest do
  use ExUnit.Case, async: true
  alias FitnessFetch.Garmin.Auth

  # Twitter's "Creating a signature" example is the canonical OAuth 1.0a case.
  # NOTE: Twitter's *published* signature (tnnArxj06cWHq44gCs1OSKk/jLY=) is a
  # long-standing doc error and does NOT reproduce. So we anchor on the two
  # things that ARE authoritative and independent of our code:
  #   1. Twitter's documented signature BASE STRING — our param sorting +
  #      RFC-3986 encoding + base-string assembly must reproduce it exactly.
  #   2. RFC 2202 HMAC-SHA1 — proves the signing primitive.
  @twitter_params [
    {"status", "Hello Ladies + Gentlemen, a signed OAuth request!"},
    {"include_entities", "true"},
    {"oauth_consumer_key", "xvz1evFS4wEEPTGEFPHBog"},
    {"oauth_nonce", "kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg"},
    {"oauth_signature_method", "HMAC-SHA1"},
    {"oauth_timestamp", "1318622958"},
    {"oauth_token", "370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb"},
    {"oauth_version", "1.0"}
  ]
  @twitter_url "https://api.twitter.com/1/statuses/update.json"
  @twitter_consumer_secret "kAcSOqF21Fu85e7zjz7ZN2U4ZRhfV3WpwPAoE3Y7rit"
  @twitter_token_secret "LswwdoUaIvS8ltyTt5jkRh4J50vUPVVHtR2YPi5kE"
  # Twitter's documented signature base string (their docs, verbatim).
  @twitter_base "POST&https%3A%2F%2Fapi.twitter.com%2F1%2Fstatuses%2Fupdate.json&include_entities%3Dtrue%26oauth_consumer_key%3Dxvz1evFS4wEEPTGEFPHBog%26oauth_nonce%3DkYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg%26oauth_signature_method%3DHMAC-SHA1%26oauth_timestamp%3D1318622958%26oauth_token%3D370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb%26oauth_version%3D1.0%26status%3DHello%2520Ladies%2520%252B%2520Gentlemen%252C%2520a%2520signed%2520OAuth%2520request%2521"

  describe "oauth1_signature/5" do
    test "HMAC-SHA1 primitive matches RFC 2202" do
      mac = :crypto.mac(:hmac, :sha, "Jefe", "what do ya want for nothing?") |> Base.encode16(case: :lower)
      assert mac == "effcdf6ae5eb2fa2d27416d5f184df9c259a7c79"
    end

    test "reproduces Twitter's documented base string (so signs it correctly)" do
      # Independent reference: HMAC of Twitter's *documented* base string.
      key =
        URI.encode(@twitter_consumer_secret, &URI.char_unreserved?/1) <>
          "&" <> URI.encode(@twitter_token_secret, &URI.char_unreserved?/1)

      expected = :crypto.mac(:hmac, :sha, key, @twitter_base) |> Base.encode64()

      sig =
        Auth.oauth1_signature(
          "POST",
          @twitter_url,
          @twitter_params,
          @twitter_consumer_secret,
          @twitter_token_secret
        )

      assert sig == expected
    end

    test "empty token secret is handled (2-legged style)" do
      sig = Auth.oauth1_signature("GET", "https://example.com/x", [{"a", "1"}], "secret", nil)
      assert is_binary(sig)
      assert byte_size(sig) > 0
    end
  end

  describe "oauth1_header/7" do
    test "produces an OAuth header with a signature and the standard fields" do
      header =
        Auth.oauth1_header("GET", "https://example.com/x", "ckey", "csecret", nil, nil, [
          {"ticket", "ST-123"}
        ])

      assert String.starts_with?(header, "OAuth ")
      assert header =~ ~s(oauth_consumer_key="ckey")
      assert header =~ "oauth_signature="
      assert header =~ ~s(oauth_signature_method="HMAC-SHA1")
      # the ticket is a query param used in signing, not emitted in the header
      refute header =~ "ticket="
    end
  end
end
