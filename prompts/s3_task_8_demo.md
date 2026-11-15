# S-3 bounded task 8, demo seed and "Try the story" (Deliverable 4b)

Tool: Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15. The plan was approved by Abraham Eapen before any edit, and the diff was approved before the commit.

---

```text
Implement Task 8 (D13 demo seed and README "Try the story"; no AC) from docs/design/S-3.md,
following Task 8 and the demo table in docs/plans/S-3-plan.md (7 postings, including demo-empty).
Change only src/jobsboard/ranking_store.py (add seed_demo), src/jobsboard/api.py (call it once
at import when os.environ.get("JOBSBOARD_DEMO") == "1"), and README.md (add "Try the story").
Do not change tests/, src/jobsboard/pipeline.py, src/jobsboard/ranking.py, docs/, or any other file.
seed_demo uses ApplicationStore._put for the fixed demo-acN-x IDs (D13) and move_stage to put
demo-ac23-y in Rejected. Without JOBSBOARD_DEMO=1 nothing is seeded.
"Try the story" gives the one start command (JOBSBOARD_DEMO=1 uvicorn jobsboard.api:app --app-dir src)
and, for each AC (AC-6, AC-7, AC-8, AC-21, AC-22, AC-23), a URL to open and what it shows, plus
the empty state (demo-empty → []) and the error state (an unknown posting → 404).
Show me a plan and wait. Stop when the full README test command passes (100 tests) and,
with the app running under JOBSBOARD_DEMO=1, every demo URL returns what the table says
(show me the curl output for each).
After I approve the diff, save this prompt as prompts/s3_task_8_demo.md, commit as
"task 8: demo seed and Try the story (D13)", and add ledger entry 47.
```
