# S-3 Task 7 validation tests, follow-up prompt (Deliverable 4, test-writer delegation)

Tool: Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15. Given to the main agent, which passed the test-writing part to the `test-writer` subagent (`.claude/agents/test-writer.md`).

---

Prompt given to the main agent, verbatim:

```text
Use the test-writer subagent again on tests/unit/test_ranking_validation.py, from
docs/design/S-3.md D10 and D11 as amended in 30ec446. Add:
- Q1: set_profile with a bad fit_score and a bad skill in one call raises InvalidFitScore (D11 order);
- Q2: set_requirements and set_profile that raise leave the earlier value in the store
  (check with candidates_for_posting; for set_requirements also the case where no earlier
  value existed, which must still raise PostingNotFound afterwards);
- Q3: skills given as "" raise InvalidSkill("") for rank_applicants, set_requirements and set_profile.
Strengthen test_d11_set_profile_fit_score_bounds_accepted and
test_d11_set_profile_overwrite_is_not_a_duplicate so they check the stored profile through
candidates_for_posting (for example, the overwrite gives fit_score 60).
Expected values come only from the doc. Do not edit src/ or tests/acceptance/.
Run the file and report pass/fail counts and failure reasons.
Save this prompt to prompts/s3_task_7_tests_followup_prompt.md and the report verbatim to
evidence/delegation/test-writer-task7-followup.md. Then commit the test file, both prompts and
both reports as "task 7a: validation unit tests from test-writer (§5, D3, D10, D11)" and add
ledger entry 44 (subagent test-writer). In entry 44's review field, note that the first report's
"37 DID NOT RAISE" is an arithmetic slip; the run shows 39 (25 InvalidSkill + 12 InvalidFitScore
+ 2 DuplicateApplication), plus 5 AttributeError and 2 TypeError, which makes 46.
Then stop for my review.
```

Prompt the main agent passed to the `test-writer` subagent, verbatim: the prompt above with its first words "Use the test-writer subagent again on tests/unit/test_ranking_validation.py," changed to "Work on tests/unit/test_ranking_validation.py (written by you earlier),", its save, commit, ledger and stop lines (the main agent's job) removed, and "Do not commit. Your final message is your report." added at the end.
