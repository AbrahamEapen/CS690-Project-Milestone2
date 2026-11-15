# S-3 Task 7 validation tests prompt (Deliverable 4, test-writer delegation)

Tool: Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15. Given to the main agent, which passed the test-writing part to the `test-writer` subagent (`.claude/agents/test-writer.md`).

---

Prompt given to the main agent, verbatim:

```text
Use the test-writer subagent to write tests/unit/test_ranking_validation.py from
docs/design/S-3.md §5, §7, D3, D9, D10 and D11 (Task 7 in docs/plans/S-3-plan.md; no AC,
so each test names the rule, decision or edge case it checks). Cover:
- InvalidFitScore(application_id, fit_score) for -1, 101, 50.0, "50", None, True; 0 and 100 accepted;
- InvalidSkill(raw) for a non-str skill, a skill blank after strip(), and skills given as a
  single str (D10 as amended in 622086e), for required skills and candidate skills;
- DuplicateApplication(application_id) for a repeated application_id;
- the D10 order: required skills before candidates; per candidate, duplicate ID, then fit
  score, then skills; non-str skills (sorted by repr) before blank ones;
- exceptions subclass ValueError and keep their constructor arguments as attributes (D3, D9);
- RankingStore.set_requirements and set_profile raise the same errors on set (D11), and an
  empty requirement set is allowed.
Expected values come only from the doc. If the doc does not decide something, list it as a
question instead of testing it. Do not edit src/ or tests/acceptance/.
Run the new file: the tests should fail because validation is not built (some valid-input
tests may already pass); report which fail and why.
Save this prompt to prompts/s3_task_7_tests_prompt.md and the subagent's report verbatim to
evidence/delegation/test-writer-task7.md. Do not commit; stop for my review.
The next ledger entry is 43.
```

Prompt the main agent passed to the `test-writer` subagent, verbatim: the prompt above with its first words "Use the test-writer subagent to write" changed to "Write", its last three lines (saving, commit and ledger, which are the main agent's job) removed, and "Do not commit. Your final message is your report." added at the end.
