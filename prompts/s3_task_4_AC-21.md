# S-3 bounded task 4, AC-21 (Deliverable 4b)

Tool: Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15. The plan was approved by Abraham Eapen before any edit, and the diff was approved before the commit.

---

```text
Implement AC-21 from docs/design/S-3.md, following Task 4 in docs/plans/S-3-plan.md
(SKILL_SYNONYMS matching per R1/D7, required skills grouped per D1, missing_required per §5).
Change only src/jobsboard/ranking.py.
Do not change tests/, src/jobsboard/pipeline.py, src/jobsboard/api.py, docs/, or any other file.
Show me a plan and wait. Stop when test_ac21_synonym_meets_minimum in
tests/acceptance/test_s3_ranking.py passes, and run the full README test command.
Before I approve the diff, show me (in the console only, do not add test files) the
missing_required that rank_applicants returns for these cases:
  a) required {"Postgres", "PostgreSQL"}, candidate skills {}            -> expect ("Postgres",)
  b) required {"Java", " java"},         candidate skills {}            -> expect ("Java",)
  c) required {"Word"},                  candidate skills {"Microsoft Word "} -> expect ()
  d) required {"PostgreSQL"},            candidate skills {"POSTGRES"}  -> expect ()
  e) required {"kdb+", "Java"},          candidate skills {}            -> expect ("Java", "kdb+")
After I approve the diff, save this prompt as prompts/s3_task_4_AC-21.md, commit as
"task 4: synonyms meet the minimum (AC-21)", and add the next ledger entry.
```
