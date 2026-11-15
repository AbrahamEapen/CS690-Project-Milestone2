# S-3 bounded task 7b, input validation (Deliverable 4b)

Tool: Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15. The plan was approved by Abraham Eapen before any edit, and the diff was approved before the commit.

---

```text
Implement Task 7 (input validation; §5, D3, D9, D10, D11 as amended in 622086e and 30ec446)
from docs/design/S-3.md, following Task 7 in docs/plans/S-3-plan.md.
Change only src/jobsboard/ranking.py and src/jobsboard/ranking_store.py.
Do not change tests/, src/jobsboard/pipeline.py, src/jobsboard/api.py, docs/, or any other file.
rank_applicants validates all input before ranking, raising the first problem in D10 order;
the RankingStore setters use the same helpers, check fit_score before skills, and store
nothing when they raise.
Show me a plan and wait. Stop when tests/unit/test_ranking_validation.py and all acceptance
tests pass, and run the full README test command.
After I approve the diff, save this prompt as prompts/s3_task_7b_validation.md, commit as
"task 7b: input validation (§5, D3, D10, D11)", and add ledger entry 45.
```
