# S-3 review of task 5 (Deliverable 4, reviewer delegation)

Tool: Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15. Given to the main agent, which passed the review part to the `reviewer` subagent (`.claude/agents/reviewer.md`).

---

Prompt given to the main agent, verbatim:

```text
Use the reviewer subagent to review task 5 (src/jobsboard/ranking_store.py and
src/jobsboard/api.py, commit d3b2641) against docs/design/S-3.md (§4, R6, R7, D5, D8,
D10, D11, D12) and AC-8. Report only what the reviewer finds. Save its report verbatim to
evidence/delegation/reviewer-task5.md and this prompt to prompts/s3_review_task5_prompt.md.
Do not fix anything yet. The next ledger entry is 41.
```

Prompt the main agent passed to the `reviewer` subagent, verbatim:

```text
Review task 5 (src/jobsboard/ranking_store.py and src/jobsboard/api.py, commit d3b2641) against docs/design/S-3.md (§4, R6, R7, D5, D8, D10, D11, D12) and AC-8 in backlog/backlog.md. Report only what you find. Do not fix anything.
```
