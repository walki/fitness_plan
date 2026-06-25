---
name: roger-s-data-logging-tools-and-formats
description: "Roger uses MFP for food (printable diary URL is the preferred format), Hevy app for strength, Garmin for cardio, BPM monitor for BP. Coros Dura on order replacing Garmin head unit."
metadata: 
  node_type: memory
  type: reference
  originSessionId: c08792a8-673b-4a3d-ac4c-5b4079505d25
---

**Food tracking — MyFitnessPal**
- Roger's MFP username: `rogerwalker`
- Preferred share format (as of Jun 17, 2026): **Printable Diary URL**
  - `https://www.myfitnesspal.com/reports/printable-diary/rogerwalker?from=YYYY-MM-DD&to=YYYY-MM-DD`
  - Includes: Calories, Carbs, Fat, Protein, Cholesterol, Sodium, Sugar, Fiber by meal + daily TOTALS
  - More columns than the old per-meal paste (which only had Cal/Carbs/Fat/Protein/Sodium/Fiber)
  - When Roger pastes from printable diary, totals match exactly with old format — no rework needed
- Roger logs honestly, including restaurant estimates (which are inherently ±20% — don't sweat individual entries)

**Strength tracking — Hevy app (hevyapp.com)**
- Started using Jun 5, 2026 for Friday pull session
- Hevy gives clean per-exercise / per-set breakdowns Roger can paste
- Format: movement name → "Set 1: X lbs x Y reps"
- Replaces the older "free-form list" format he was using

**Cardio tracking — Garmin Connect**
- All bike, run, walk, ride activities sync from Garmin watch/head unit
- Roger pastes the Garmin Connect activity stats blob (HR, power, pace, elevation, etc.)
- **Garmin head unit known issue:** sensor dropouts on climbs (Brecksville May 25, FBG last 15 mi)
- **Coros Dura purchased post-FBG** (Jun 13) to replace Garmin head unit for cycling — long battery, gravel-focused, better sensor reliability under climbing load. Garmin watch likely stays for running.

**BP tracking — Garmin Index BPM**
- Target: 2x/week readings
- Output: time, systolic, diastolic, HR, AHA category
- See [[bp_framing]] — track, don't alarm

**Weight + Cal balance**
- Roger pastes a small table: Date / Cal In / Garmin Burn / Cal Diff / Weight
- Weighs in daily, morning
- See trend analysis approach: 7-day rolling avg is the signal, daily is noise

**Sleep — Garmin sleep tracking**
- Score (0-100), Quality (Poor/Fair/Good), Duration, Bedtime, Wake Time
- Roger sometimes disputes Garmin's score vs subjective feel — trust his subjective read when they conflict

**Memory location**
Memory files live at:
`C:\Users\roger\.claude\projects\C--Users-roger-projects-fitness-fitness-plan\memory\`
(filesystem-based, persist across Claude account switches as long as the Windows user "roger" and working directory stay the same)
