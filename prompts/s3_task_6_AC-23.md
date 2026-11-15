# S-3 bounded task 6, AC-23 (Deliverable 4b)

Tool: Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15. The plan was approved by Abraham Eapen before any edit, and the diff was approved before the commit.

---

```text
Implement AC-23 from docs/design/S-3.md, following Task 6 in docs/plans/S-3-plan.md.
Change only src/jobsboard/ranking_store.py.
Do not change tests/, src/jobsboard/pipeline.py, src/jobsboard/ranking.py, src/jobsboard/api.py,
docs/, or any other file.
Show me a plan and wait. Stop when test_ac23_ranked_endpoint_lists_only_scored_non_rejected in
tests/acceptance/test_s3_ranking.py passes and all 10 tests pass, and run the full README test command.
After I approve the diff, save this prompt as prompts/s3_task_6_AC-23.md, commit as
"task 6: ranked list excludes unscored and Rejected (AC-23)", and add ledger entry 42.
```
