# Plan: S-3 ranked applicants with a minimum flag

Written by Claude Code (Claude Opus 5.5) in plan mode from `docs/design/S-3.md` and `AGENTS.md`, before any code was edited. Read and corrected by the team (Abraham Eapen) on 2026-11-15 (Deliverable 4a); the corrections are listed at the end, and crossed-out text is what the team removed.

## Context
S-3 acceptance tests are locked (`m2-tests-locked`, red run: 6 S-3 failed, 4 S-1 passed). This plan builds S-3 in eight bounded tasks. Tasks 1 to 6 each make one AC test pass. Task 7 adds input validation (§5, D3, D10, D11), tests first. Task 8 adds the D13 demo seed and the README section "Try the story".

## How

**Files created**
- `src/jobsboard/ranking.py`. Named settings `FLAG_TEXT`, `FIT_SCORE_MIN`, `FIT_SCORE_MAX`, `SKILL_SYNONYMS` (D9). The `Candidate` and `RankedEntry` frozen dataclasses (§4). `InvalidFitScore`, `DuplicateApplication` and `InvalidSkill`, all subclassing `ValueError`, with attributes named after their constructor parameters (D3, D9). Private helpers `_validate_skills` and `_validate_fit_score` (§5, D10). `_normalize`/`_skill_key` (R1, D7). `rank_applicants` (R1 to R5).
- `src/jobsboard/ranking_store.py`. `PostingNotFound(posting_id)` (D9), `RankingStore` (D5, D11), and `seed_demo(store, ranking_store)` (D13).

**Files changed**
- `src/jobsboard/api.py`. Add a module-level `ranking_store = RankingStore()` next to `store` (D12). Add the route `GET /postings/{posting_id}/ranked`. Add a 404 handler that returns `{"detail": {"error": "posting_not_found"}}` (§4). Seed the demo when `os.environ.get("JOBSBOARD_DEMO") == "1"` (D13). The S-1 routes don't change.
- `README.md`: add a "Try the story" section (Task 8 only).
- `tests/unit/test_ranking_validation.py`: new, written by `test-writer` at the start of Task 7.

**Files that must not change:** `src/jobsboard/pipeline.py`, `src/jobsboard/__init__.py`, `tests/` (except the new `tests/unit/test_ranking_validation.py`, written by `test-writer` in Task 7), `docs/design/`, `backlog/`, `evidence/`, `LEDGER.md`, `prompts/`, `AGENTS.md`, `CLAUDE.md`, `.claude/`, `requirements.txt`.

**Data shapes**
- `Candidate(application_id: str, skills: frozenset[str], fit_score: int)`. It has no `__post_init__` check. `rank_applicants` validates all input first, so it can raise the first problem in list order (D3).
- `RankedEntry(application_id: str, fit_score: int, meets_minimum: bool, flag: str | None, missing_required: tuple[str, ...])`.
- Skill key: `n = s.strip().casefold()`. A skill whose `n` is in a `SKILL_SYNONYMS` group uses that group (a `frozenset`) as its key. Otherwise the key is `n` (R1, D1, D7).
- Required skills are grouped by key, so each key counts as one requirement (D1). A missing requirement shows the trimmed posting spelling that sorts first by `(casefold(), spelling)`. `missing_required` is sorted by the same key (§5).
- Sort key: `(not meets_minimum, -fit_score, application_id)`. This covers R3, R4 and D2.
- HTTP JSON: each entry is `dataclasses.asdict(entry)`, so the tuple becomes an array and `None` becomes `null` (D12).

**Validation (§5, D3, D10 as revised in 3d6a2e9; built in Task 7)**
- Order: `required_skills` first, then each candidate in list order. For each candidate, check the duplicate ID, then the fit score, then the skills.
- Skills are checked in two passes. The first pass raises `InvalidSkill(raw)` for the first non-`str` skill in `sorted(key=repr)` order. The second pass raises `InvalidSkill(raw)` for the first skill that is blank after `strip()`, in `sorted()` order.
- A fit score is valid only when `type(x) is int` and 0 ≤ x ≤ 100. Anything else raises `InvalidFitScore(application_id, fit_score)`. A `bool`, a float, a `str` or `None` all fail.
- Any iterable is accepted. A candidate with no skills is valid.

**Data storage (D5, D11).** Everything is in memory, with no database or file I/O.
- `RankingStore._requirements: dict[str, frozenset[str]]` maps `posting_id` to the validated raw spellings.
- `RankingStore._profiles: dict[str, Candidate]` is keyed by `application_id`.
- Both setters validate on set, using the same helpers and errors as `rank_applicants`, and overwrite earlier values.
- `candidates_for_posting(posting_id, applications)` raises `PostingNotFound` when no requirements are set for the posting. Otherwise it returns `(requirements, [profile for each application with this posting_id, a profile, and a stage other than Rejected])`, in the order given.
- The route calls `candidates_for_posting(posting_id, store.list_for_posting(posting_id))`, then `rank_applicants`. It only reads S-1 data (R6).

**Demo seed (D13).** `seed_demo` uses `Application` and the existing `ApplicationStore._put` (team decision, recorded in D13, 3d6a2e9), so its IDs are fixed and easy to read.

| Posting | Requires | Applications (skills, fit) | `/ranked` shows |
| --- | --- | --- | --- |
| `demo-ac6` | Java, kdb+ | `demo-ac6-a` (Java, kdb+; 40), `demo-ac6-b` (Java; 90) | a, then b flagged |
| `demo-ac7` | Java | `demo-ac7-a` (55), `demo-ac7-b` (80), `demo-ac7-c` (70), all Java | b, c, a, no flags |
| `demo-ac8` | Java, kdb+ | `demo-ac8-b` (Java; 75), stage Applied | b flagged; the pipeline still shows b under Applied |
| `demo-ac21` | PostgreSQL | `demo-ac21-a` (Postgres; 60), `demo-ac21-b` (MySQL; 90) | a, then b flagged, missing `["PostgreSQL"]` |
| `demo-ac22` | Java | `demo-ac22-b` (Java; 70) inserted first, then `demo-ac22-a` (Java; 70) | a, b, no flags |
| `demo-ac23` | Java | `demo-ac23-x` (50); `demo-ac23-y` (80) moved to Rejected; `demo-ac23-z` with no profile | only x, unflagged |

## Tasks
Each task gets one commit (`task N: … (AC-x)`). The team saves each prompt to `prompts/s3_task_AC-x.md` and writes the ledger entry. The full test command runs after every task.

1. **AC-7: qualified applicants are ordered by fit score.** Create `ranking.py` with ~~everything in How~~ the named settings, `Candidate`, `RankedEntry`, the three exception classes and `rank_applicants` (team correction: ~~validation helpers~~ move to Task 7). Matching is exact on `strip`/`casefold` only, with no synonyms yet. R1 and R2 are flag logic. Sort by `-fit_score` only, with no grouping and no tie-break. Check: `test_ac7_qualified_ordered_by_fit_score` passes.
2. **AC-6: a flagged applicant is never above a qualified one.** Add `not meets_minimum` as the first sort key (R3). Check: `test_ac6_flagged_never_above_qualified` passes.
3. **AC-22: equal fit scores are ordered by application_id.** Add `application_id` ascending as the last sort key (D2, R4). Check: `test_ac22_equal_fit_scores_ordered_by_application_id` passes.
4. **AC-21: synonyms meet the minimum.** Add `SKILL_SYNONYMS` keys to matching, group the required skills (D1), and pick the posting spelling for `missing_required`. Check: `test_ac21_synonym_meets_minimum` passes.
5. **AC-8: a flagged applicant is kept, and their stage is unchanged.** Create `ranking_store.py`: `PostingNotFound`, and `RankingStore` with validate-on-set setters. `candidates_for_posting` filters by posting and by having a profile. In `api.py`, add `ranking_store`, the `/ranked` route and the 404 handler. Check: `test_ac8_flagged_applicant_kept_and_stage_unchanged` passes. **Then the main agent hands Task 5 to the `reviewer` subagent** (team correction; report saved in `evidence/delegation/`).
6. **AC-23: `/ranked` lists only scored applications that aren't Rejected.** Add the `stage is not Stage.REJECTED` filter (D8, R7). Unscored applications are already left out by Task 5. Check: `test_ac23_ranked_endpoint_lists_only_scored_non_rejected` passes, and all 10 tests pass.
7. **Input validation (§5, D3, D10, D11; no AC, edge cases in §7).** First the main agent has `test-writer` draft `tests/unit/test_ranking_validation.py` from §5, §7, D3, D10 and D11 (scores −1, 101, `50.0`, `"50"`, `None`, `True`; non-`str` and blank skills; duplicate IDs; validation order; store validate-on-set). The team reviews and commits those tests, then the agent adds `_validate_skills`, `_validate_fit_score` and the duplicate check to `ranking.py`, and calls them from the `RankingStore` setters. Check: the new unit tests and all 10 acceptance tests pass.
8. **Demo seed and "Try the story" (D13; no AC).** Add `seed_demo` with the table above, the `JOBSBOARD_DEMO == "1"` hook in `api.py`, and the README section. Check: `JOBSBOARD_DEMO=1 uvicorn jobsboard.api:app --app-dir src` starts, and `GET /postings/demo-acN/ranked` matches the table for every row. All 10 tests still pass.

## Before Task 1 (team, by hand) — done
- D10 and D13 in `docs/design/S-3.md` were updated by the team in commit 3d6a2e9.

## Assumptions — settled by the team in D10 (3d6a2e9)
- A skill that is blank after trimming raises `InvalidSkill(raw)`.
- `PostingNotFound` also subclasses `ValueError` (D3).

## Verification
- After each task, run `python -m pytest --cov=jobsboard --cov-branch --cov-report=term-missing --cov-fail-under=80`. Report the exact output. Only the AC the task targets turns green.
- After Task 6, the result is 10 passed, saved later as `evidence/green.txt`.
- After Task 8, run the demo command and do a manual `curl` or `/docs` check of all six demo postings.
- ~~Run the `reviewer` subagent on `ranking.py`, `ranking_store.py` and `api.py` against S-3.md after Task 7.~~ Moved to after Task 5 (team correction 2). The headless review (Deliverable 6) covers all story files at the end.

## Team corrections (Deliverable 4a)
1. **Validation moved out of Task 1 into its own Task 7, tests first.** The plan put all §5/D3/D10 validation into Task 1, but AC-7 asks for none of it and no acceptance test checks it, so Task 1 was not bounded. As its own task, the validation gets unit tests from `test-writer` first, and each part of the build can be reviewed against its own check.
2. **Reviewer delegation moved from after the last task to after Task 5.** Task 5 is the first to touch the store, the API and S-1 data (the R6 and D12 risks), so a finding there costs least to fix. The headless review in Deliverable 6 covers everything again.
3. **The plan's open points were settled in the design doc first** (commit 3d6a2e9): D10's two-pass skill order, blank skill → `InvalidSkill`, `PostingNotFound` is a `ValueError`, and the D13 demo uses `_put`. The plan had called `_put` a "team decision" before the team had made it.
