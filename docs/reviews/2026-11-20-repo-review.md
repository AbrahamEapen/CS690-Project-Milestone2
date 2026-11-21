# Repository review — 2026-11-20

Reviewer: Claude (Claude Opus 5.5, `claude-opus-5-5`), at Ketan Verma's request. LEDGER entry 57.
Scope: `main` at `aff2104` (GitHub ZIP, no history), all of `src/jobsboard/`, the test suites, `MILESTONE2.md`, `LEDGER.md`, `prompts/`, `contribution/`.
This is a read-only review: no code or test was changed.

## Checks run

| Command | Result |
| --- | --- |
| `python -m pytest --cov=jobsboard.ranking --cov=jobsboard.ranking_store --cov=jobsboard.api --cov-branch --cov-report=term-missing --cov-fail-under=80` (Python 3.13.18, pinned `requirements.txt`) | 154 passed, 97.54%; `api.py` missing 26, 36, 47 — identical to `evidence/coverage.txt` |
| Every `prompts/*.md` path cited in `LEDGER.md` exists | 0 missing |
| Every ledger entry has all seven fields | 56 / 56 |
| `set_requirements("p", None)` and `set_requirements("p", 5)` (probe) | `TypeError`, not `InvalidSkill` (finding C3) |

## Code findings

No correctness bugs were found. Ranking (R3/R4/D2), the minimum flag (R1/R2), synonyms (D7), filtering (D8), validation order (D10) and store semantics (D11) match `docs/design/S-3.md`.

| # | Severity | File | Finding | Suggested action |
| --- | --- | --- | --- | --- |
| C1 | Low | `src/jobsboard/api.py:1` | Module docstring still says "S-1 HTTP API", but the file now also serves the S-3 `/ranked` route. | Change to "S-1 and S-3 HTTP API (S-1.md §4, S-3.md §4)". |
| C2 | Low | `src/jobsboard/ranking.py:107` | `rank_applicants` is typed `required_skills: frozenset[str]`, but D10 says any iterable is accepted and the code accepts one. | Type it `Iterable[str]` to match D10, or note the narrower contract in §4. |
| C3 | Low | `ranking.py` `validate_skills` | A non-iterable `skills` (`None`, `5`) raises `TypeError` from `list()`, not `InvalidSkill`. D10 covers "any iterable" and a single `str`, but is silent on non-iterables, so this is a design gap rather than a bug. | Team decision: either add it to D10 as accepted behaviour, or raise `InvalidSkill(skills)` and add a test (through `test-writer`, per `AGENTS.md`). |
| C4 | Info | `api.py` module-level `store`, `ranking_store` | Plain dicts with no lock; FastAPI runs sync handlers in a thread pool. Safe for the demo and tests (D5 keeps data in memory until S-4), but concurrent writes are not guarded. | Record as an S-4 risk; no change now. |
| C5 | Info | `api.py` lines 36, 47 | Uncovered S-1 error paths (blank `applicant_id` → 422, unknown application → 404). `MILESTONE2.md` §5d already explains them. | Optional: one integration test each would bring `api.py` to 98%+ (line 26 stays subprocess-only). |

## Repository and documentation findings

| # | Severity | Where | Finding | Suggested action |
| --- | --- | --- | --- | --- |
| R1 | High (grading) | `contribution/` | Deliverable 9 asks for "one signed statement per member", but only `Abraham_Eapen_contribution.md` / `.pdf` exist. Ketan Verma's and Aditya Pothuri's are missing. | Each member writes and signs their own; the content must come from them. |
| R2 | Medium | `prompts/README.md` | The index stops at ledger entry 24 (Milestone 1). The 18 Milestone 2 prompt files (entries 25–56) are not listed. | Add the Milestone 2 rows (done in this session, ledger entry 59). |
| R3 | Medium | `MILESTONE2.md` §1a | "No items as of 2026-11-15." If Milestone 1 feedback has arrived since, this section is out of date. | Add each feedback item with what was changed (needs the actual feedback). |
| R4 | Low | `LEDGER.md` | Every Milestone 2 entry (25–56) names Abraham as the human reviewer. Nothing records what Ketan or Aditya did in Milestone 2, which weakens the "everyone works with the agent" claim in `MILESTONE2.md` (Team roles). | Add entries for teammates' real reviews or decisions, if any; otherwise state the split of work honestly in Team roles. |
| R5 | Low | `MILESTONE2.md` | Section order is 5f, 5b, 5d, 5e; 5a and 5c are only mentioned through ledger entries. | Reorder to 5a–5f, or add one-line 5a/5c pointers to `tests/unit/` and `tests/property/`. |
| R6 | Info | `AGENTS.md` | "Never push" plus the `Bash(git push *)` deny rule are good. The reflection's own lesson — "the restart step belongs in `AGENTS.md`" — has not been added yet. | Add one line: start Claude Code from the repo root so `.claude/agents/` loads. |

## What is strong

- The acceptance-test lock is real: the deny rule, `evidence/permission-denied.md`, and the `git diff --stat m2-tests-locked m2-green` check together close the most likely shortcut.
- Mutation testing is triaged with reasons tied to D9, and the one real survivor was killed by a spec-derived test.
- The ledger is complete and self-consistent: seven fields on every entry, every cited prompt file present.
