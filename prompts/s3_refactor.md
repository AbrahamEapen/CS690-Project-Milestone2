# S-3 refactor (Deliverable 4e)

Tool: Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15. The plan was approved by Abraham Eapen before any edit, and the diff was approved before the commit.

---

```text
Refactor task (Deliverable 4e; no behavior change): ranking_store.py imports the private
_validate_fit_score and _validate_skills from ranking.py. Make them public
(validate_fit_score, validate_skills) in ranking.py and update their callers; also drop the
unused fit score from the demo-ac23 "z" row in _DEMO_POSTINGS (give the no-profile case a
clearer shape). Change only src/jobsboard/ranking.py and src/jobsboard/ranking_store.py.
Do not change tests/, api.py, pipeline.py, docs/, or any other file.
Show me a plan and wait. Stop when the full README test command still gives 100 passed.
After I approve the diff, save the test output with
  python -m pytest --cov=jobsboard --cov-branch --cov-report=term-missing --cov-fail-under=80 | tee evidence/refactor.txt
save this prompt as prompts/s3_refactor.md, commit as "refactor: public validators, clearer demo rows (4e)",
and add ledger entry 49.
```
