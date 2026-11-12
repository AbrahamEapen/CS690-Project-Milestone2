# Milestone 2 — S-3: Ranked applicants with a minimum flag

Team: Ketan Verma, Aditya Pothuri, Abraham Eapen. Agent: Claude Code (Claude Opus 5.5) for the whole team.
Repository: https://github.com/AbrahamEapen/CS690-Project-Milestone2. It starts from the Milestone 1 files (https://github.com/ap3478/CS690-Project, without history) at commit c17dcad.

## Deliverables map

| Deliverable | Paths and tags |
| --- | --- |
| 1 Follow-up, story, open questions | this file §1; `docs/design/S-3.md` §8; `docs/design/S-3-gap-check-2.md`; `prompts/s3_gap_check_2_prompt.md` |
| 2 Agent setup | `AGENTS.md`, `CLAUDE.md`, `.claude/settings.json`, `.claude/agents/test-writer.md`, `.claude/agents/reviewer.md`, `evidence/permission-denied.md` |
| 3 Acceptance tests | `tests/acceptance/`, `evidence/test-audit.md`, `evidence/red.txt`, tag `m2-tests-locked` |
| 4 Plan and build | `docs/plans/S-3-plan.md`, `prompts/`, `evidence/delegation/`, `evidence/green.txt`, `evidence/refactor.txt`, `evidence/screens/`, README "Try the story", tag `m2-green` |
| 5 Test strength | `tests/unit/`, `tests/integration/`, `tests/property/`, `pyproject.toml`, `evidence/coverage.txt`, `evidence/mutation-before.txt`, `evidence/mutation-after.txt` |
| 6 Headless review | `scripts/review_story.sh`, `agent/review-schema.json`, `evidence/headless-review.json` |
| 7 Ledger | `LEDGER.md`, `prompts/` |
| 8 Report | this file |
| 9 Contribution | `contribution/` (one signed statement per member) |

## Team roles

_TODO (Deliverable 8): who led the agent setup, the acceptance tests, the build, and the test-strength work._

## 1. Follow-up, the story, and its open questions

### 1a. Milestone 1 follow-up

_TODO: Milestone 1 feedback has not been received yet. Respond to each item here, or write "No items."_

The Milestone 1 repository was `ap3478/CS690-Project`. Milestone 2 continues in a new repository, so commit SHAs in the Milestone 1 ledger refer to the old repository.

### 1b. The story

**S-3.** As an HR recruiter, I want all applicants for a posting listed by fit score, with anyone missing a required skill flagged "Does not meet minimum" and never ranked above an applicant who meets them all, so that I review qualified candidates first instead of reading every resume.

Evidence: E-11, E-12, E-13, E-14 (the meaning of "meets minimum" rests on A-5). Design doc: `docs/design/S-3.md`.

| AC ID | Given | When | Then |
| --- | --- | --- | --- |
| AC-6 | posting P requires {Java, kdb+}; applicant A has both with fit score 40; applicant B has only Java with fit score 90 | the recruiter opens the ranked list for P | A is listed above B, and B shows the flag "Does not meet minimum" while A shows no flag |
| AC-7 | posting P requires {Java}; applicants A, B, C all have Java, with fit scores 55, 80, 70 | the recruiter opens the ranked list for P | the list shows B, C, A in that order, with no flags |
| AC-8 | posting P requires {Java, kdb+}; applicant B (stage Applied) has only Java | the recruiter opens the ranked list for P | B still appears in the list, flagged "Does not meet minimum", and B's stage is still Applied |
| AC-21 | posting P requires {PostgreSQL}; applicant A has {Postgres} with fit score 60; applicant B has {MySQL} with fit score 90 | the recruiter opens the ranked list for P | A is listed above B; A shows no flag, and B shows the flag "Does not meet minimum" (D7) |
| AC-22 | posting P requires {Java}; applications "b" and "a" both have Java with fit score 70 | the recruiter opens the ranked list for P | the list shows "a" then "b", with no flags (D2) |
| AC-23 | posting P requires {Java}; X has Java, score 50, stage Applied; Y has Java, score 80, moved to Rejected; Z has no fit score yet | the recruiter requests `GET /postings/P/ranked` | the response is 200 and lists only X, unflagged (D8) |

AC-21 to AC-23 are new in Milestone 2. They follow from settling OQ-3, OQ-1 and OQ-4 (1c) and were added to `backlog/backlog.md` after the design doc changed.

Files where the story's code lives:
- `src/jobsboard/ranking.py` — `Candidate`, `RankedEntry`, `rank_applicants`, errors, named settings (new)
- `src/jobsboard/ranking_store.py` — the in-memory data module, `PostingNotFound`, `seed_demo` (new)
- `src/jobsboard/api.py` — the `GET /postings/{posting_id}/ranked` route (changed)
- Tests: `tests/acceptance/test_s3_ranking.py`, `tests/unit/`, `tests/integration/`, `tests/property/`

### 1c. Open questions settled

All four are recorded in `docs/design/S-3.md` §8 with their sources (commit a0710e9); Q-5, Q-6 and Q-9 are marked settled in `evidence/evidence_log.md`.

| OQ | Decision | Source |
| --- | --- | --- |
| OQ-1 (Q-6) ties | D2: `fit_score` descending, then `application_id` ascending | Team decision: deterministic, needs no new data |
| OQ-2 (Q-5) override | D6: no override in S-3; split out as backlog story S-15 | Team decision; INT-04:P06–P07 |
| OQ-3 (Q-9) synonyms | D7: fixed `SKILL_SYNONYMS` {postgres, postgresql}, {word, microsoft word}, both directions | INT-03:P03 examples; team decision to add no unevidenced pairs |
| OQ-4 unscored / Rejected | D8: both left out by the data module | Team decision: unscored cannot be ordered; Rejected needs no review |
| `FLAG_TEXT` | `"Does not meet minimum"` | Story text, AC-6 |
| `FIT_SCORE_MIN` / `FIT_SCORE_MAX` | 0 / 100 | §5 (M1) |
| `SKILL_SYNONYMS` | two groups above | D7 |

### 1d. Gap check again

The prompt is in `prompts/s3_gap_check_2_prompt.md`, and the reply and marks are in `docs/design/S-3-gap-check-2.md` (commit e44da99). Of the 37 questions, 30 were real gaps, all settled in §8 (D1, D4, §5 and new D9–D13), and 7 were already answered. All of this was committed before the tests were locked.

## 3b. Answers to the test-writer audit

_TODO (Deliverable 3b)._

## 4a. Changes to the plan

_TODO (Deliverable 4a)._

## 5. Test strength

### 5f. Traceability (updated rows)

_TODO._

### 5b. Integration test

_TODO._

### 5d. Uncovered line or branch

_TODO._

### 5e. Surviving mutants

_TODO._

## 6c. Answers to the headless review

_TODO._

## Reflection

_TODO (300–500 words, written by the team; say if AI polished the wording)._
