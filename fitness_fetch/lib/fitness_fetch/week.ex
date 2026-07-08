defmodule FitnessFetch.Week do
  @moduledoc """
  Resolve a `{from, to}` date range from CLI options shared by the mix tasks:

    * `--from YYYY-MM-DD --to YYYY-MM-DD` — explicit range
    * `--week YYYY-MM-DD` — the Mon–Sun week ending on that Sunday
    * neither — the current Mon–Sun week
  """

  @spec range(keyword()) :: {Date.t(), Date.t()}
  def range(opts) do
    cond do
      opts[:from] || opts[:to] ->
        {parse!(opts[:from], "--from"), parse!(opts[:to], "--to")}

      opts[:week] ->
        sunday = parse!(opts[:week], "--week")
        {Date.add(sunday, -6), sunday}

      true ->
        today = Date.utc_today()
        monday = Date.add(today, -(Date.day_of_week(today) - 1))
        {monday, Date.add(monday, 6)}
    end
  end

  @spec parse!(String.t() | nil, String.t()) :: Date.t()
  def parse!(nil, flag), do: Mix.raise("#{flag} is required (YYYY-MM-DD)")

  def parse!(s, flag) do
    case Date.from_iso8601(s) do
      {:ok, d} -> d
      _ -> Mix.raise("#{flag} must be YYYY-MM-DD, got: #{s}")
    end
  end
end
