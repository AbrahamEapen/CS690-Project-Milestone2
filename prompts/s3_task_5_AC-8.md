# S-3 bounded task 5, AC-8 (Deliverable 4b)

Tool: Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15. The plan was approved by Abraham Eapen before any edit, and the diff was approved before the commit.

---

```text
Implement AC-8 from docs/design/S-3.md, following Task 5 in docs/plans/S-3-plan.md.
Change only src/jobsboard/ranking_store.py (new file) and src/jobsboard/api.py.
Do not change tests/, src/jobsboard/pipeline.py, src/jobsboard/ranking.py, docs/, or any other file.
The RankingStore setters store values without validating them; validation is Task 7.
candidates_for_posting filters by posting_id and by having a profile only; the Rejected
filter is Task 6. Unknown posting -> 404 {"detail": {"error": "posting_not_found"}} (§4, D12).
Show me a plan and wait. Stop when test_ac8_flagged_applicant_kept_and_stage_unchanged in
tests/acceptance/test_s3_ranking.py passes, and run the full README test command.
After I approve the diff, save this prompt as prompts/s3_task_5_AC-8.md, commit as
"task 5: flagged applicant kept, stage unchanged (AC-8)", and add the next ledger entry.
```
