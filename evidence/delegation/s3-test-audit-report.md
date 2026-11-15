## S-3 acceptance test audit: tests/acceptance/test_s3_ranking.py

AC-21, AC-22 and AC-23 had no test, so I added one for each to `/root/CS690/Project/Milestone-2/tests/acceptance/test_s3_ranking.py`. All 6 tests in the file fail, and each one fails because the S-3 code is not built yet, not because of a mistake in a test. I did not edit anything under src/.

**Why I wrote in tests/acceptance/:** that folder is normally read-only. I added tests there because you named the file, and design doc section 9 says the AC-21 to AC-23 tests are to be written by test-writer in Deliverable 3b. The `m2-tests-locked` tag that the file's docstring mentions does not exist yet (`git tag` shows nothing), so the file is not locked. I appended the three tests and did not change any existing line.

### 1. Findings

**Criteria without a test before this pass**
- **AC-21** (D7, synonyms): none. Section 9 says "test to be written by test-writer in Deliverable 3b". Added.
- **AC-22** (D2, tie order): none. Added.
- **AC-23** (D8/D4, HTTP `/ranked` filtering): none. Added.

**Expected values that do not follow from their criterion:** none. I checked each one by hand:
- **AC-6:** order is A then B. A's flag is `None` and B's flag is "Does not meet minimum", which matches the criterion. R3 puts qualified A (40) above flagged B (90).
- **AC-7:** fit scores 80 > 70 > 55 give B, C, A with no flags, which matches.
- **AC-8:** B is listed once, flagged, and still in Applied, which matches. The fit score of 75 is not in the criterion, but no assert depends on it.

**Asserts that only check a type or a length:** none.

**Weak spot, reported only (I did not change it because the file is acceptance-owned):** `test_ac8_flagged_applicant_kept_and_stage_unchanged` checks that B's stage is still Applied (AC-8, R6), but that check can hardly fail.
- The test ranks by calling `rank_applicants` directly with a hand-built `Candidate`.
- That function never sees the S-1 store, so it cannot change any stage.
- The criterion says "the recruiter opens the ranked list for P", which is a request to `GET /postings/{id}/ranked` going through `ranking_store`.
- A stronger version would set requirements and a profile, call that endpoint, and only then check the pipeline. That would catch a `/ranked` route that changes stages.
- A smaller gap: it asserts `app_id in stages["Applied"]` but not that the ID is missing from the other stages.

### 2. Tests written

All three are appended to `/root/CS690/Project/Milestone-2/tests/acceptance/test_s3_ranking.py`.

**`test_ac21_synonym_meets_minimum`** (AC-21; D7, R1, R2, R3, section 5)
- Input: required {"PostgreSQL"}. B has {"MySQL"} with score 90, A has {"Postgres"} with score 60. B is given first.
- Working: "postgres" and "postgresql" are in the same `SKILL_SYNONYMS` group, so A meets the minimum. "mysql" is in no group, so B is missing "PostgreSQL". R3 puts A above B even though 60 < 90.
- Expected: the order is `["A", "B"]`.
- A: flag `None`, `meets_minimum` True, `missing_required == ()`.
- B: flag "Does not meet minimum", `meets_minimum` False, `missing_required == ("PostgreSQL",)`. That value is the posting's own spelling, trimmed, as section 5 requires.

**`test_ac22_equal_fit_scores_ordered_by_application_id`** (AC-22; D2, R4)
- Input: "b" then "a", both with Java and score 70. Giving "b" first means the input order cannot produce the right answer by accident.
- Working: the scores tie, so D2 sorts by application_id ascending, and "a" < "b".
- Expected: `["a", "b"]`, with flags `[None, None]`.

**`test_ac23_ranked_endpoint_lists_only_scored_non_rejected`** (AC-23; D8, R7, D12, section 4 HTTP)
- Setup:
  - Create X, Y and Z through the S-1 HTTP API on a new posting, each checked for 201.
  - Set requirements {"Java"} through `api.ranking_store` (the module-level name D12 gives).
  - Give X the profile (Java, 50) and Y the profile (Java, 80). Z gets no profile.
  - Move Y to Rejected over HTTP and check for 200 with stage "Rejected".
- Working: Y is Rejected and Z has no profile, so D8 leaves both out. X has Java, so it meets the minimum (R1) and gets flag null (R2). D12 says `missing_required` is an array.
- Expected: status 200, and the body is exactly `[{"application_id": X, "fit_score": 50, "meets_minimum": true, "flag": null, "missing_required": []}]`.

### 3. Test command and result

`python` is not on PATH in this shell, so I ran the same command through the venv interpreter:

```
.venv/bin/python -m pytest -q tests/acceptance/test_s3_ranking.py
```

Summary line: `6 failed, 1 warning in 0.40s`

- **AC-6, AC-7, AC-8, AC-21, AC-22:** `ModuleNotFoundError: No module named 'jobsboard.ranking'`. Section 4 names this module and it is not built yet.
- **AC-23:** `AttributeError: module 'jobsboard.api' has no attribute 'ranking_store'`. D12 names this attribute and it is not built yet. The S-1 steps earlier in the test (creating applications and moving one to Rejected) ran without error.
- The 1 warning is a Starlette deprecation warning from `TestClient`.
