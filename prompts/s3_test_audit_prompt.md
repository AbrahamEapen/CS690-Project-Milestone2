# S-3 test audit prompt (Deliverable 3b)

Given to the main Claude Code agent (Claude Opus 5.5) on 2026-11-15, which passed it to the
`test-writer` subagent (`.claude/agents/test-writer.md`).

```text
Use the test-writer subagent to audit tests/acceptance/test_s3_ranking.py against AC-6,
AC-7, AC-8, AC-21, AC-22 and AC-23 in backlog/backlog.md and sections 6 and 7 of
docs/design/S-3.md (the open questions are settled in section 8). Report every criterion
without a test, every expected value that does not follow from its criterion, and every
assert that only checks a type or a length. Write a test in that file for each criterion
that has none. Do not edit src/.
```
