defmodule FitnessFetch.WeekTest do
  use ExUnit.Case, async: true
  alias FitnessFetch.Week

  test "--week resolves the Mon–Sun week ending on that Sunday" do
    assert Week.range(week: "2026-07-05") == {~D[2026-06-29], ~D[2026-07-05]}
  end

  test "--from/--to gives an explicit range" do
    assert Week.range(from: "2026-07-06", to: "2026-07-12") == {~D[2026-07-06], ~D[2026-07-12]}
  end

  test "no options → the current Mon–Sun week" do
    {from, to} = Week.range([])
    assert Date.day_of_week(from) == 1
    assert Date.day_of_week(to) == 7
    assert Date.diff(to, from) == 6
  end

  test "a bad date raises" do
    assert_raise Mix.Error, ~r/must be YYYY-MM-DD/, fn -> Week.range(week: "nope") end
  end
end
