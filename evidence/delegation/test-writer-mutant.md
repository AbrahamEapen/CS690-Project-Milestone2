## Report: kill mutant `jobsboard.ranking_store.x_seed_demo__mutmut_9`

The mutant is now **killed**. I added one test and changed nothing else. `src/` and `tests/acceptance/` are untouched, and nothing is committed.

### 1. Findings
- **Gap behind the survivor:** none of the existing D13 seed tests in `/root/CS690/Project/Milestone-2/tests/integration/test_ranked_endpoint.py` looked at `applicant_id`. They only check application IDs, stages and ranked rows, so changing `applicant_id` to `None` broke none of them.
- **Type check:** the new test checks `isinstance(..., str)`, which is a type check. It is there because neither S-1 §4 nor §5 gives an exact `applicant_id` value. §5 only says "str (non-empty)" and §4 says "all strings". To make it stronger than a type check, the test also checks `applicant_id.strip() != ""` and the exact number of applications.
- **One limit:** a mutant that put in some other non-empty string, such as `"XXapplicant-aXX"`, would still survive this test. Killing that would need the design doc or plan to fix the demo `applicant_id` text, and it does not.
- No other criteria were reviewed in this pass.

### 2. Test written
- **File:** `/root/CS690/Project/Milestone-2/tests/integration/test_ranked_endpoint.py`
- **Test:** `test_d13_seed_demo_applicant_ids_are_non_empty_strings`, placed right after `test_d13_seed_demo_leaves_stages_unchanged_after_ranking`.
- **Covers:** D13 seed data, S-1 §5 (`applicant_id: str`, non-empty) and S-1 §4 (all Application JSON fields are strings).
- **What it does:** seeds a fresh `ApplicationStore` and `RankingStore`, then collects every application across the demo postings.
- **Expected values, worked by hand:**
  - The count is 13, from the plan table, posting by posting:

    | Posting | Applications |
    |---|---|
    | ac6 | 2 |
    | ac7 | 3 |
    | ac8 | 1 |
    | ac21 | 2 |
    | ac22 | 2 |
    | ac23 | 3 (x, y, z) |
    | empty | 0 |
    | **Total** | **13** |

  - Every `applicant_id` must be a `str`, and its stripped value must not equal `""`.

### 3. Commands run and results
```
.venv/bin/python -m pytest --cov=jobsboard.ranking --cov=jobsboard.ranking_store --cov=jobsboard.api --cov-branch --cov-report=term-missing --cov-fail-under=80
```
- `Required test coverage of 80% reached. Total coverage: 97.54%`
- `======================== 154 passed, 1 warning in 4.43s ========================`
- Coverage by file: `api.py` 92% (lines 26, 36, 47 not covered), `ranking.py` 100%, `ranking_store.py` 100%.

```
.venv/bin/mutmut run "jobsboard.ranking_store.x_seed_demo__mutmut_9"
```
- Output: `🎉 jobsboard.ranking_store.x_seed_demo__mutmut_9`
- `.venv/bin/mutmut results --all true` now lists `jobsboard.ranking_store.x_seed_demo__mutmut_9: killed`.
- `mutmut results` still lists 4 other surviving mutants. I did not touch them because they were outside this task.
