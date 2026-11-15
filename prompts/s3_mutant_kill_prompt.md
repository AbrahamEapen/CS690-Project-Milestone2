# S-3 mutant kill prompt (Deliverable 5e, test-writer delegation)

Tool: Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15. Given to the main agent, which passed the test-writing part to the `test-writer` subagent (`.claude/agents/test-writer.md`).

---

Prompt given to the main agent, verbatim:

```text
Use the test-writer subagent to kill one surviving mutant from evidence/mutation-before.txt:
jobsboard.ranking_store.x_seed_demo__mutmut_9, which changes the demo applications'
applicant_id=f"applicant-{letter}" to applicant_id=None (see `mutmut show` for it).
Write the expected value from docs/design/S-1.md §4 and §5 (applicant_id is a non-empty str;
an Application's JSON fields are all strings), not from the code: every application that
seed_demo puts into a fresh ApplicationStore has an applicant_id that is a str and is not blank.
Add the test to tests/integration/test_ranked_endpoint.py, next to the other D13 seed tests.
Do not edit src/ or tests/acceptance/. Run the full README test command, then
`mutmut run "jobsboard.ranking_store.x_seed_demo__mutmut_9"` and show that it is now killed.
Save this prompt to prompts/s3_mutant_kill_prompt.md and the report verbatim to
evidence/delegation/test-writer-mutant.md. Do not commit; stop for my review.
The next ledger entry is 53.
```

Prompt the main agent passed to the `test-writer` subagent, verbatim: the prompt above with its first words "Use the test-writer subagent to kill" changed to "Kill", its last three lines (saving, commit and ledger, which are the main agent's job) removed, and these lines added at the end: "Use the venv: .venv/bin/python and .venv/bin/mutmut. The full README test command is: python -m pytest --cov=jobsboard.ranking --cov=jobsboard.ranking_store --cov=jobsboard.api --cov-branch --cov-report=term-missing --cov-fail-under=80" and "Do not commit. Your final message is your report."
