defmodule FitnessFetch.Intervals.Format do
  @moduledoc """
  Render intervals.icu computed metrics: a per-activity metrics table and the
  week's fitness/fatigue/form (CTL/ATL/TSB) trend.
  """

  @spec report([map()], [map()], Date.t(), Date.t()) :: String.t()
  def report(activities, wellness, from, to) do
    range = "#{Calendar.strftime(from, "%b %-d")} – #{Calendar.strftime(to, "%b %-d, %Y")}"

    Enum.join(
      [
        "=== intervals.icu #{range} ===",
        activities_section(activities),
        form_section(wellness)
      ],
      "\n\n"
    )
  end

  def activities_section([]), do: "### Activity metrics\n(no activities)"

  def activities_section(activities) do
    {complete, incomplete} = Enum.split_with(activities, fn a -> a.type || a.name end)

    rows =
      Enum.map(complete, fn a ->
        "| #{day(a.date)} | #{blank(a.name)} | #{blank(a.type)} | #{blank(a.tss)} | #{iff(a.intensity)} | #{watts(a.np)} | #{ef(a.ef)} | #{pct(a.decoupling)} | #{hr(a)} |"
      end)

    """
    ### Activity metrics (computed by intervals.icu)

    | Date | Activity | Type | TSS | IF | NP | EF | Decoupling | HR |
    |------|----------|------|-----|----|----|----|-----------|-----|
    #{Enum.join(rows, "\n")}
    #{ftp_note(complete)}#{incomplete_note(incomplete)}
    """
  end

  # intervals sometimes returns activity stubs (type/name/metrics not yet
  # processed — e.g. backfill still syncing). Flag them rather than print blanks.
  defp incomplete_note([]), do: ""

  defp incomplete_note(incomplete) do
    days = Enum.map_join(incomplete, ", ", &day(&1.date))
    "\n#{length(incomplete)} activity(ies) not yet processed by intervals.icu (no type/metrics — likely backfill still syncing): #{days}"
  end

  # Surface the FTP intervals.icu assumed — TSS/IF/spike-fixing all key off it,
  # so if it looks wrong, the metrics above are suspect.
  defp ftp_note(activities) do
    ftps = activities |> Enum.map(& &1.ftp) |> Enum.reject(&is_nil/1) |> Enum.uniq() |> Enum.sort()

    case ftps do
      [] -> ""
      list -> "\nFTP intervals.icu assumed: #{Enum.map_join(list, ", ", &"#{&1}W")} — sanity-check this."
    end
  end

  def form_section([]), do: "### Fitness / Form\n(no wellness data)"

  def form_section(wellness) do
    rows =
      Enum.map(wellness, fn w ->
        "| #{day(w.date)} | #{num(w.ctl)} | #{num(w.atl)} | #{signed(w.form)} | #{blank(w.resting_hr)} |"
      end)

    latest = List.last(wellness)

    """
    ### Fitness / Form (CTL = fitness, ATL = fatigue, Form = CTL−ATL)

    | Date | Fitness (CTL) | Fatigue (ATL) | Form (TSB) | RHR |
    |------|---------------|---------------|------------|-----|
    #{Enum.join(rows, "\n")}

    Latest form: **#{signed(latest && latest.form)}** (positive = fresh, negative = fatigued).
    """
  end

  # --- helpers ------------------------------------------------------------

  defp day(nil), do: "?"
  defp day(%Date{} = d), do: Calendar.strftime(d, "%b %-d")

  defp blank(nil), do: ""
  defp blank(v), do: to_string(v)

  defp num(nil), do: "—"
  defp num(v) when is_float(v), do: :erlang.float_to_binary(v, decimals: 1)
  defp num(v), do: to_string(v)

  defp signed(nil), do: "—"
  defp signed(v) when is_number(v) and v > 0, do: "+#{v}"
  defp signed(v), do: to_string(v)

  # intervals reports IF as a percent (93.2 → 0.93); show our decimal convention.
  defp iff(nil), do: "—"
  defp iff(v), do: :erlang.float_to_binary(v / 100, decimals: 2)

  defp ef(nil), do: "—"
  defp ef(v), do: :erlang.float_to_binary(v / 1, decimals: 2)

  defp pct(nil), do: "—"
  defp pct(v), do: "#{:erlang.float_to_binary(v / 1, decimals: 1)}%"

  defp watts(nil), do: "—"
  defp watts(v), do: "#{round(v)}W"

  defp hr(%{avg_hr: nil}), do: "—"
  defp hr(%{avg_hr: avg, max_hr: max}) when is_number(max), do: "#{round(avg)} (#{round(max)} max)"
  defp hr(%{avg_hr: avg}), do: "#{round(avg)}"
end
