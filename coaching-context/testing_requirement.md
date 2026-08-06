---
name: always-write-tests-for-code
description: "Standing rule: any code/functionality built in this repo MUST ship with tests. Not optional."
type: feedback
---

**Roger's directive (Jul 6, 2026):** "You must write tests for the functionality." Said while building the `fitness_fetch` Elixir app — after an initial pass shipped with only partial (formatting) tests.

**Why:** Roger holds real code to a real bar. This repo isn't just markdown coaching files anymore — the `fitness_fetch` data pipeline is genuine software and is expected to be engineered properly, tests included.

**How to apply:**
- When writing/changing functionality in the `fitness_fetch` app (see logging_tools) or any future code, write tests in the same pass — don't defer them or call the work done without them.
- Make external I/O testable by design (e.g. Strava HTTP is injected via `:req_options` → `Req.Test`), so there's no excuse to skip a module because "it hits the network."
- Run the suite (`mise exec -- mix test`) and confirm green before saying it's done.
- Cover success paths, error/edge paths (missing env, empty results), and any data-conversion logic (SI→imperial, pagination, filtering).
