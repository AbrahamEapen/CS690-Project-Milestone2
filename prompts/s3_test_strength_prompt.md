# S-3 test strength prompt (Deliverable 5a–5c, test-writer delegation)

Tool: Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15. Given to the main agent, which passed the test-writing part to the `test-writer` subagent (`.claude/agents/test-writer.md`).

---

Prompt given to the main agent, verbatim:

```text
Use the test-writer subagent to draft the Deliverable 5 tests for S-3 from docs/design/S-3.md
(§4, §6, §7, §8). Expected values come only from the doc. Do not edit src/, tests/acceptance/
or tests/unit/test_ranking_validation.py. Write three new files:

5a tests/unit/test_ranking_edge_cases.py: a unit test for every §7 edge case that has none yet
(first list each §7 edge case and the existing test that covers it, if any, in
tests/acceptance/ or tests/unit/), and at least one invalid input for each §4 function:
rank_applicants, RankingStore.set_requirements, set_profile, candidates_for_posting
(unknown posting), and the frozen Candidate / RankedEntry dataclasses.

5b tests/integration/test_ranked_endpoint.py: no mocks. Use the real api.app with the real
module-level api.store (S-1 ApplicationStore) and api.ranking_store (S-3 data module), with
unique posting IDs. Cover: unknown posting → 404 {"detail": {"error": "posting_not_found"}};
a posting with requirements and no applications → 200 []; a posting whose every application
is Rejected or unscored → 200 []; and seed_demo into a fresh ApplicationStore and RankingStore,
checked against the demo table in docs/plans/S-3-plan.md.

5c tests/property/test_ranking_properties.py, Hypothesis: one property each for R3, R4, R5 and
R6, each naming its rule in a comment. Do not re-sort or recompute the expected order the way
the code does. Check a relation that must hold for every input (e.g. no flagged entry before
an unflagged one; adjacent entries in a group never increase in fit_score, and ties ascend
by application_id; the output IDs are the input IDs, each exactly once; the input list and
S-1 stages are unchanged). Generate unique application IDs, scores 0..100, and skills from a
small pool that includes synonym and case variants.

Run all tests. Report each file's pass/fail counts and any failure with its reason. A failure
here may be a real bug, so report it and do not weaken the test.
Save this prompt to prompts/s3_test_strength_prompt.md and the report verbatim to
evidence/delegation/test-writer-strength.md. Do not commit; stop for my review.
The next ledger entry is 51.
```

Prompt the main agent passed to the `test-writer` subagent, verbatim: the prompt above with its first words "Use the test-writer subagent to draft" changed to "Draft", its last three lines (saving, commit and ledger, which are the main agent's job) removed, and two lines added at the end: the full test command from AGENTS.md as changed in 6895fd1 ("The full test command is now: python -m pytest --cov=jobsboard.ranking --cov=jobsboard.ranking_store --cov=jobsboard.api --cov-branch --cov-report=term-missing --cov-fail-under=80") and "Do not commit. Your final message is your report."
