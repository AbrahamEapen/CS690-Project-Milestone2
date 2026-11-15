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

Abraham Eapen led the agent setup, the acceptance tests, the build, and the test-strength work. Everyone works with the agent.

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

The audit report is `evidence/test-audit.md` (test-writer subagent; transcript `evidence/delegation/test-writer-audit.txt`, ledger entry 29). Abraham recomputed every expected value by hand from its criterion and confirmed that each test fails because S-3 is missing (`ModuleNotFoundError: jobsboard.ranking` or no `api.ranking_store`), not because of a mistake in the test.

| # | Finding | Answer |
| --- | --- | --- |
| 1 | AC-21 (D7 synonyms) had no test | Fixed: test-writer added `test_ac21_synonym_meets_minimum`, a5d5f2e. Hand check: postgres ≡ postgresql, so A qualifies; B misses `("PostgreSQL",)`, the posting spelling (§5). |
| 2 | AC-22 (D2 ties) had no test | Fixed: `test_ac22_equal_fit_scores_ordered_by_application_id`, a5d5f2e. Hand check: tie at 70 → "a" before "b"; input given in reverse order. |
| 3 | AC-23 (D8 filtering over HTTP) had no test | Fixed: `test_ac23_ranked_endpoint_lists_only_scored_non_rejected`, a5d5f2e. Hand check: Y Rejected and Z unscored are excluded; X → `{id, 50, true, null, []}` per §4. |
| 4 | AC-8's "stage still Applied" check could not fail, because the test called `rank_applicants` directly and never opened the ranked list | Fixed by the team: the test now calls `GET /postings/P/ranked`, e06026b. |
| 5 | AC-8 checked only that B is in Applied, not that it is absent from the other stages | Fixed in the same team commit: the whole `stages` map is compared, e06026b. |

The report found no expected value that does not follow from its criterion and no type-only or length-only assert; our hand check agrees.

## 4a. Changes to the plan

The agent wrote the plan in plan mode (`prompts/s3_plan_prompt.md`). Abraham read it before any code was written. The corrected plan is `docs/plans/S-3-plan.md`, where the removed text is crossed out.

1. **Validation moved out of Task 1 into its own Task 7, tests first.** Task 1 was meant to make AC-7 pass, but the agent put all the §5/D3/D10 input validation into it. AC-7 asks for none of that and no acceptance test checks it, so Task 1 was not bounded. Validation is now Task 7, and `test-writer` drafts its unit tests before any code.
2. **Reviewer delegation moved from the last task to Task 5.** Task 5 is the first to touch the store, the API and S-1 data (R6, D12). A finding there is cheaper to fix than after the demo task. The headless review in Deliverable 6 still covers every file at the end.
3. **The plan's open points went into the design doc first** (3d6a2e9). D10's "skills in `sorted()` order" fails on mixed types, so the team wrote a two-pass rule, and the plan's two assumptions became decisions in D10. The plan also called the demo's use of `_put` a "team decision" before the team had made one. Abraham then chose it and recorded it in D13.

## 5. Test strength

### 5f. Traceability (updated rows)

The S-3 rows of `traceability/traceability.csv`, updated. The fifth column is the commit that first made the test pass. Design doc §9 lists the same test names.

| Evidence ID | Story | AC | Test | Passing commit |
| --- | --- | --- | --- | --- |
| E-11; E-12; E-13; E-14 | S-3 | AC-6 | `tests/acceptance/test_s3_ranking.py::test_ac6_flagged_never_above_qualified` | d569d92 (task 2) |
| E-11; E-12; E-13; E-14 | S-3 | AC-7 | `tests/acceptance/test_s3_ranking.py::test_ac7_qualified_ordered_by_fit_score` | 9223160 (task 1) |
| E-11; E-12; E-13; E-14 | S-3 | AC-8 | `tests/acceptance/test_s3_ranking.py::test_ac8_flagged_applicant_kept_and_stage_unchanged` | d3b2641 (task 5) |
| E-11; E-12; E-13; E-14; Q-9 (INT-03:P03) | S-3 | AC-21 | `tests/acceptance/test_s3_ranking.py::test_ac21_synonym_meets_minimum` | 4ac171e (task 4) |
| E-11; E-12; E-13; E-14; Q-6 | S-3 | AC-22 | `tests/acceptance/test_s3_ranking.py::test_ac22_equal_fit_scores_ordered_by_application_id` | 8464a89 (task 3) |
| E-11; E-12; E-13; E-14 (D8, team decision) | S-3 | AC-23 | `tests/acceptance/test_s3_ranking.py::test_ac23_ranked_endpoint_lists_only_scored_non_rejected` | 969ad37 (task 6) |

### 5b. Integration test

`tests/integration/test_ranked_endpoint.py` (13 tests, ledger entries 51 and 53). It joins **the S-3 data module, `RankingStore` (`api.ranking_store`)**, and **the `/ranked` route in `api.py` reading S-1's `ApplicationStore` (`api.store`)**, with no mock between them. Requests go through FastAPI's `TestClient` into the real module-level stores. The tests cover the 404, the two `200 []` cases, the R7 posting filter, the JSON shape (D12), and `seed_demo` against the plan's demo table, both in-process and with `JOBSBOARD_DEMO=1` in a fresh interpreter. This closes the Task 5 reviewer's finding 4 (ledger entry 41).

### 5d. Uncovered line or branch

`evidence/coverage.txt`: 154 passed, 97.54% over the story files (`ranking.py` and `ranking_store.py` 100%; `api.py` 92%, missing 26, 36, 47). Line 26 of `api.py`, `seed_demo(store, ranking_store)` under `if os.environ.get("JOBSBOARD_DEMO") == "1"`, is not covered. That is acceptable. `test_d13_demo_env_1_serves_plan_table_over_http` does run it, but in a subprocess (it has to import `api.py` with the variable set), and pytest-cov does not measure subprocesses. Turning on coverage's subprocess measurement (`COVERAGE_PROCESS_START`) would count it. Lines 36 and 47 are S-1 error paths (blank `applicant_id`, unknown application).

### 5e. Surviving mutants

mutmut 3.8.1 mutates `ranking.py` and `ranking_store.py` (`[tool.mutmut]` in `pyproject.toml`). First run (`evidence/mutation-before.txt`): 158 mutants, 153 killed, 5 survived. After (`evidence/mutation-after.txt`): 154 killed, 4 survived. All 5 survivors were triaged; there were fewer than 20.

| Mutant | What it changed | Outcome |
| --- | --- | --- |
| `jobsboard.ranking_store.x_seed_demo__mutmut_9` | demo `applicant_id=f"applicant-{letter}"` → `None` | Killed by `test_d13_seed_demo_applicant_ids_are_non_empty_strings` (test-writer, from S-1 §4/§5), 3e151a1 |
| `jobsboard.ranking_store.xǁPostingNotFoundǁ__init____mutmut_1` | exception message → `None` | Not killed: equivalent under D9 ("no message format is required"). A test would have to take its expected text from the code. |
| `jobsboard.ranking.xǁInvalidFitScoreǁ__init____mutmut_1` | exception message → `None` | Not killed: same reason (D9) |
| `jobsboard.ranking.xǁDuplicateApplicationǁ__init____mutmut_1` | exception message → `None` | Not killed: same reason (D9) |
| `jobsboard.ranking.xǁInvalidSkillǁ__init____mutmut_1` | exception message → `None` | Not killed: same reason (D9) |

_TODO (team, one sentence): what the mutation score told you that coverage did not._

## 6c. Answers to the headless review

`scripts/review_story.sh` was run at commit 27b1c80, after `m2-green`, under the normal permission rules. It reviewed the files changed since `m2-tests-locked`: `src/jobsboard/api.py`, `ranking.py` and `ranking_store.py`. The report in `evidence/headless-review.json` is committed exactly as the tool wrote it. Its `structured_output` is `{"verdict": "pass", "findings": []}`, so there are no findings to answer.

We checked that the main agent did not review the files itself: `subagent_stats.by_type` is `{"reviewer": 1}` (1 spawned, 1 completed, no permission denials), so the `--agent reviewer` fallback was not needed. The first attempt failed before any review ran: the CLI's schema validator rejected the `$schema` draft-2020-12 meta-reference. The fix is in 27b1c80, and `stdin` is now read from `/dev/null`. The reviewer's earlier findings on the same code were answered in ledger entry 41 and closed by Tasks 6 and 7 and the 5b integration test, which may be why this pass found nothing.

## Reflection

_TODO (300–500 words, written by the team; say if AI polished the wording)._
