# Memory Backup

This folder contains a snapshot of Claude's memory files for this project as of **June 21, 2026**.

## Why this exists

Memory files normally live at:
```
C:\Users\roger\.claude\projects\C--Users-roger-projects-fitness-fitness-plan\memory\
```

That's filesystem-based on the local machine, scoped to the Windows user account. Memories should persist across Claude account switches (personal → team) as long as the Windows user (`roger`) and the working directory stay the same.

**This backup is insurance.** If memories are ever lost or wiped (account switch, machine change, file deletion), they can be restored from this folder back to the live memory directory.

## Files

- `MEMORY.md` — the index file, listing all memories with one-line descriptions
- All other `.md` files — individual memory entries

## How to restore

If memories are lost:

```bash
# From the repo root, restore all memories
cp memory-backup/*.md "$HOME/.claude/projects/C--Users-roger-projects-fitness-fitness-plan/memory/"
```

Or on Windows:
```powershell
Copy-Item memory-backup\*.md "$env:USERPROFILE\.claude\projects\C--Users-roger-projects-fitness-fitness-plan\memory\"
```

## Keeping this fresh

This snapshot is a point-in-time backup. If memories are updated by Claude during sessions, this folder will drift from the live ones. Roger or Claude can refresh the snapshot occasionally:

```bash
cp /c/Users/roger/.claude/projects/C--Users-roger-projects-fitness-fitness-plan/memory/*.md memory-backup/
```

Then commit the changes.

## What's in here as of Jun 21, 2026

| File | Description |
|------|-------------|
| `project_overview.md` | Fitness plan repo: markdown/CSV files, not a software project |
| `user_background.md` | Roger uses Claude Chat for brainstorming, Code for edits/commits |
| `fueling_products.md` | SiS gels + Tailwind are go-tos; don't propose substitutes |
| `garmin_data_caveats.md` | Garmin temp is device-in-sun, not air temp; other interpretation notes |
| `strength_training_context.md` | Left knee (post-ACL 2007) + left elbow (Jan 2026) rehab-style programming |
| `bp_framing.md` | On meds, doc-managed. Track BP, don't alarm. Weight loss is the lever. |
| `life_context_over_metrics.md` | Don't moralize single-day food/drink. Trends matter, single days don't. |
| `auto_regulation.md` | Roger picks weights by feel/form. Prescribe movement + reps + intent. |
| `logging_tools.md` | MFP printable diary URL, Hevy app, Garmin, Coros Dura. |
