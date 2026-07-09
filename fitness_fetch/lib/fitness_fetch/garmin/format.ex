defmodule FitnessFetch.Garmin.Format do
  @moduledoc """
  Render normalized Garmin wellness data (`FitnessFetch.Garmin.wellness/2`) into
  the weekly-log tables: sleep, resting HR, and blood pressure.
  """

  @doc "Full report for a wellness map over `[from, to]`."
  @spec report(map(), Date.t(), Date.t()) :: String.t()
  def report(%{sleep: sleep, resting_hr: rhr, blood_pressure: bp}, from, to) do
    range = "#{Calendar.strftime(from, "%b %-d")} – #{Calendar.strftime(to, "%b %-d, %Y")}"

    Enum.join(
      [
        "=== Garmin wellness #{range} ===",
        sleep_section(sleep),
        rhr_section(rhr),
        bp_section(bp)
      ],
      "\n\n"
    )
  end

  @doc "Sleep table rows for the weekly log."
  def sleep_section([]), do: "### Sleep\n(no sleep data)"

  def sleep_section(sleep) do
    rows =
      sleep
      |> Enum.sort_by(& &1.date, Date)
      |> Enum.map(fn s ->
        "| #{day(s.date)} | #{blank(s.score)} | #{blank(s.quality)} | #{duration(s.duration_seconds)} | #{blank(s.bedtime)} | #{blank(s.wake)} |"
      end)

    """
    ### Sleep

    | Date | Score | Quality | Duration | Bedtime | Wake |
    |------|-------|---------|----------|---------|------|
    #{Enum.join(rows, "\n")}
    """
  end

  @doc "Resting HR list for the weekly log."
  def rhr_section([]), do: "### Resting HR\n(no resting HR data)"

  def rhr_section(rhr) do
    rows =
      rhr
      |> Enum.sort_by(& &1.date, Date)
      |> Enum.map(fn r -> "| #{day(r.date)} | #{blank(r.resting_hr)} |" end)

    """
    ### Resting HR

    | Date | Resting HR |
    |------|------------|
    #{Enum.join(rows, "\n")}
    """
  end

  @doc "Blood-pressure table rows for the weekly log."
  def bp_section([]), do: "### BP\n(no readings — target 2×/week)"

  def bp_section(bp) do
    rows =
      bp
      |> Enum.sort_by(&{&1.date, &1.time})
      |> Enum.map(fn b ->
        "| #{day(b.date)} | #{blank(b.time)} | #{b.systolic}/#{b.diastolic} | #{blank(b.pulse)} | #{blank(b.category)} |"
      end)

    """
    ### BP readings

    | Date | Time | Reading | HR | Category |
    |------|------|---------|-----|----------|
    #{Enum.join(rows, "\n")}
    """
  end

  # --- helpers ------------------------------------------------------------

  defp day(nil), do: "?"
  defp day(%Date{} = d), do: Calendar.strftime(d, "%b %-d")

  defp duration(nil), do: "—"

  defp duration(seconds) when is_integer(seconds) do
    h = div(seconds, 3600)
    m = div(rem(seconds, 3600), 60)
    "#{h}h #{m}m"
  end

  defp blank(nil), do: ""
  defp blank(v), do: to_string(v)
end
