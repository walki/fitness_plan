# Coaching Context

Auxiliary reference for coaching Roger — the durable **principles, athlete caveats, and tool/data notes** that inform *how* to coach him. This lives in the repo (not only in Claude's machine-local memory) so any session, on any machine, has the context without re-deriving it.

**This is not a backup.** An earlier version of this folder was framed as a "memory backup" — a mirror of Claude's private memory kept for insurance. That framing was the wrong idea: redundant, drift-prone, and a smell (Roger's call, Aug 3, 2026). The repo is the source of truth; this is first-class reference content that travels with it.

## Source of truth vs. context
- **Plan state** — goals, current phase, weight trend, test results, the active week — lives in `current-state.md`, `big-picture.md`, and the active `weekly-logs/` entry. That's the hand-off mechanism between machines.
- **This folder** holds the *coaching principles* — the standing "how to work with Roger" knowledge that rarely changes week to week but shapes every decision.

## What's here
| File | Summary |
|------|---------|
| `project_overview.md` | Fitness plan repo: coaching files + the `fitness_fetch` app, not a generic software project |
| `user_background.md` | Roger uses Claude Chat to brainstorm, Code to edit/commit |
| `fueling_products.md` | SiS gels + Tailwind are the proven go-tos — don't propose substitutes |
| `garmin_data_caveats.md` | Garmin temp is device-in-sun not air temp; other interpretation notes |
| `strength_training_context.md` | Left knee (post-ACL 2007) + left elbow (Jan 2026): rehab-style programming, not more reps |
| `bp_framing.md` | On meds, doc-managed. Track BP, don't alarm. Weight loss to 165 is the lever |
| `life_context_over_metrics.md` | Don't moralize single-day food/drink (funerals, family, social, vacation). Trends matter, single days don't |
| `auto_regulation.md` | Roger picks load by feel + form. Prescribe movement + reps + intent; let him set weight |
| `weight_loss_is_the_through_line.md` | Weight loss to 165 is the #1 lever. Run the body-metrics table EVERY check-in |
| `test_thresholds_dont_infer.md` | Anchor quality workouts to TESTED numbers (FTP ramp/20-min, 5K TT/VDOT); re-test 6–8 wks |
| `testing_requirement.md` | Standing rule: any code built in this repo ships with tests |
| `logging_tools.md` | Data auto-pulled via `fitness_fetch` (Strava/Garmin/intervals/energy); MFP food + weigh-ins hand-pasted |
| `caffeine_night_run_gi.md` | Pre-leg caffeine before a middle-of-the-night effort is a GI liability for Roger — don't recommend for overnight efforts |

## Keeping it fresh
When a durable coaching principle is established or corrected (a preference, a learned lesson, a standing rule), add or update the entry here in the same pass — the same moment it would go into memory. Keep this index current when files are added or removed. Point-in-time observations (this week's numbers) do **not** belong here; those go in the weekly log.
