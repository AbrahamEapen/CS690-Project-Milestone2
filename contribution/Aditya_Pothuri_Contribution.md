# Contribution Statement: Project Milestone 2

**Name:** Aditya Pothuri, Project Lead
**Team:** Internal Jobs Board Portal (Ketan Verma, Aditya Pothuri, Abraham Eapen)

## 1. Personal authorship

- **Test runs.** I re-ran the tests and confirmed confirmed as reported by my teammates
- **Checks of the agent's and teammates' work.** I reviewed the ledger log entries, Backlog stories and Design docs and confirmed S-3 meets the criteria
- **Review of Abraham's and Ketan's work** On 2026-11-21 I reviewed Abraham and Ketan's Milestone 2 work and reviewed Ketan's suggested changes
- **Decisions (2026-11-20 review session).** I made each of the following decisions; the agent typed them into the repository:
  - which review findings to fix now (C1, C2, R2, R3, R6) and which to leave for a team decision (C3, C4) (LEDGER entries 57, 58);
  - that no Milestone 1 feedback had been received as of 2026-11-20, recorded in `MILESTONE2.md` §1a (entry 59).

## 2. AI-assisted authorship

I produced the following with Claude (Claude Opus 5.5, `claude-opus-5-5`). I read each item and approved it before it was committed.

Ledger Entry #70. A conflict with Port 8000 while iniating uvicorn jobsboard.api:app --app-dir src --reload

## 3. Review

- **AI tool's work.**
  - **Repository review.** I read the review's findings and chose which to act on. I left C3 (non-iterable skills raise `TypeError`) and C4 (no locking on the in-memory stores) for a team decision rather than letting the agent change behaviour on its own.
  - **Test results.** The full test command gave 159  passed and 100.00% coverage, the same as `evidence/coverage.txt`; nothing in `tests/acceptance/` changed (entry 58).


I confirm that this statement is accurate, and that I can explain any part of the submission I am credited with.

*Drafted with Claude (Claude Opus 5.5) from my answers; content provided by me.*

**Signature:** /s/ Aditya Pothuri **Date:** 2026-11-21
