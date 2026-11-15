## Deliverable 5 report (test-writer, S-3)

I wrote all three files. Every test passes: 53 new, and 153 in the full suite with 97.54% coverage. No test failed, so this pass found no bug. I did not edit anything under src/, tests/acceptance/ or tests/unit/test_ranking_validation.py, and I did not commit.

### 1. Findings

**§7 edge cases, and what covered each before this pass** (the list is also in the docstring of the new unit file):

| # | §7 edge case | Test that already covered it | Added in 5a/5b |
|---|---|---|---|
| 1 | No required skills | unit `test_s5_empty_required_skills_allowed` (one candidate only) | yes, several candidates |
| 2 | Every applicant flagged | **none** | yes |
| 3 | Empty list | **none** | yes |
| 4 | Flagged 100 vs unflagged 0 (R3) | **none** (AC-6 uses 90 vs 40) | yes |
| 5 | Case and outer spaces | unit `test_s5_padded_skill_is_not_blank` (padded candidate skill only) | yes, a padded *required* skill and its trimmed missing spelling |
| 6 | Scores -1 and 101 | unit `test_s5_s7_out_of_range_fit_score_raises` | no |
| 7 | `"postgres"` meets `"PostgreSQL"` | acceptance `test_ac21_synonym_meets_minimum` (as "Postgres") | yes, the lowercase spelling |
| 8 | `"PostgreSQL"` meets `"Postgres"` (other direction) | **none** | yes |
| 9 | Posting requires both Postgres and PostgreSQL (one requirement) | **none** | yes |
| 10 | Equal fit scores within a group (D2) | acceptance `test_ac22_...` (qualified group only) | yes, the flagged group |
| 11 | Unknown posting (404) | unit, only indirectly; **no HTTP test** | yes, unit and integration |
| 12 | Every application Rejected or unscored gives `[]` | **none** (AC-23 still lists X) | yes, unit and integration |
| 13 | Non-int scores | unit `test_s5_s7_non_int_fit_score_raises` | no |
| 14 | Non-str skill | unit `test_s5_non_str_*_skill_raises` | no |

**Weak asserts in existing tests:**
- `tests/unit/test_ranking_validation.py::test_d11_failed_set_profile_keeps_earlier_value` (D11) uses `pytest.raises((InvalidFitScore, InvalidSkill))` for every parameter. By D10 and D11, cases `(["Java"], 101)`, `-1` and `50.0` must raise `InvalidFitScore`, and `(["Java", " "], 60)`, `("Java", 60)` and `("", 60)` must raise `InvalidSkill`. Accepting either one would hide a wrong exception type. That file is off-limits to me, so this is for the team.
- I found no expected value that fails to follow from its criterion, and no assert elsewhere that checks only a type, a length or truthiness without the value.

**Doc note (not a test problem):** S-3.md §9 is out of date. It still gives the path `tests/test_s3_ranking.py` and says AC-21 to AC-23 are "to be written".

### 2. Tests written

**`/root/CS690/Project/Milestone-2/tests/unit/test_ranking_edge_cases.py`** (36 passed)

§7 edge cases (`_rows` = (id, fit, meets, flag, missing)):
- `test_s7_no_required_skills_everyone_meets_minimum` (edge 1, R4): required ∅; A 10 and B 20 both meet, so B then A.
- `test_s7_every_applicant_flagged_and_d2_tie_in_flagged_group` (edges 2 and 10): requires {kdb+}; input C 80, A 30, B 80; all missing ("kdb+",). The 80s tie and "B" < "C", so the order is B, C, A.
- `test_s7_empty_candidate_list_returns_empty_list` and `..._and_no_required_skills` (edge 3): result `[]`.
- `test_s7_r3_flagged_100_never_above_unflagged_0` (edge 4): result [U 0, F 100 flagged].
- `test_s7_padded_required_skill_matches_and_missing_shows_trimmed_spelling` (edge 5, §5): required " Java "; "JAVA" meets; the flagged entry shows ("Java",).
- `test_s7_lowercase_postgres_meets_postgresql` (edge 7) and `test_s7_postgresql_meets_postgres_reverse_direction` (edge 8).
- `test_d7_word_group_both_directions` (D7): " word " meets "Microsoft Word", and "MICROSOFT WORD" meets "Word".
- `test_s7_d7_d1_postgres_and_postgresql_required_count_as_one` (edge 9, D1): the flagged entry shows exactly ("Postgres",), because casefold "postgres" < "postgresql" (it is a prefix).
- `test_d1_equal_required_spellings_count_as_one_and_first_spelling_shown`: "Java" and "java" are one requirement; the shown spelling is "Java" because 'J' 0x4A < 'j' 0x6A.
- `test_d1_inner_spaces_not_collapsed`: "Microsoft  Word" (two spaces) does not match, so it is flagged.
- `test_s5_missing_required_sorted_by_casefold_then_spelling`: result ("apple", "Banana", "kdb+"). Plain `sorted()` would give "Banana" first, so this tells the two orders apart.
- `test_s7_store_every_application_rejected_or_unscored_gives_no_candidates` (edge 12, D8, R7): result `(frozenset({"Java"}), [])`.
- `test_d11_candidates_for_posting_keeps_only_this_posting_in_given_order` (D11): given [second, other, first], the result is [second 30, first 10].

Invalid input for each §4 function:
- `rank_applicants`:
  - `test_s4_rank_applicants_invalid_fit_score` with `False, 100.0, 0.0, -100`. A bool and a float each raise, even when the value is in range.
  - `test_s4_rank_applicants_list_valued_skill_raises_invalid_skill`: `skill == ["kdb+"]`.
- `set_requirements`:
  - `test_s4_set_requirements_non_str_in_frozenset_raises` with `None, 1.5, b"kdb+"`.
  - `test_s4_set_requirements_list_valued_skill_raises`.
- `set_profile`:
  - `test_s4_set_profile_invalid_fit_score` with `False, 100.5, 102`.
  - `test_s4_set_profile_non_str_skill_in_frozenset_raises`.
- `candidates_for_posting`:
  - `test_s4_candidates_for_posting_unknown_posting_raises`: `posting_id == "unknown-posting"`.
  - `..._other_case_posting_is_unknown`: "p" after setting "P" (D12).
  - `..._with_applications_but_no_requirements_raises`.
- Frozen dataclasses:
  - `test_s4_candidate_is_frozen`, `test_s4_ranked_entry_is_frozen` and `test_s4_ranked_entries_from_rank_applicants_are_frozen` expect `FrozenInstanceError`.
  - `test_s4_dataclass_field_names` checks the field names and order from §4.
  - `test_s4_candidate_missing_argument_raises_type_error`.

**`/root/CS690/Project/Milestone-2/tests/integration/test_ranked_endpoint.py`** (12 passed; no mocks; real `api.app`, `api.store` and `api.ranking_store`; a uuid posting ID per test)
- `test_s7_unknown_posting_returns_404_posting_not_found`: exact body `{"detail": {"error": "posting_not_found"}}`.
- `test_d12_posting_with_applications_but_no_requirements_returns_404`.
- `test_s4_requirements_and_no_applications_returns_empty_list`: 200 `[]`.
- `test_d11_empty_requirement_set_and_no_applications_returns_empty_list`: 200 `[]`.
- `test_s7_r7_every_application_rejected_or_unscored_returns_empty_list`: 200 `[]`. The pipeline afterwards is exactly `{"Applied": [u], ..., "Rejected": [r1, r2]}` (R6).
- `test_r7_other_postings_applications_are_not_listed`.
- `test_d12_module_level_stores_drive_the_route_and_json_shape`: requires {Java, kdb+}.
  - Q (Java, KDB+; 30) meets.
  - S (Screened, Java; 95) shows missing ["kdb+"].
  - T (Interview, no skills; 95) shows missing ["Java", "kdb+"].
  - The order is Q, then the two flagged entries by ascending ID. S-1 sets the IDs, so the test compares the real IDs.
  - Stages are read back from `api.store`.
- `test_d13_seed_demo_into_fresh_stores_matches_plan_table`: seeds a fresh `ApplicationStore()` and `RankingStore()`. Every row of the plan table is checked through `candidates_for_posting` and `rank_applicants`, along with each posting's requirement set. Expected rows: ac6 a, b(flag, kdb+); ac7 b, c, a; ac8 b(flag); ac21 a, b(flag, PostgreSQL); ac22 a, b; ac23 x only; empty [].
- `test_d13_seed_demo_s1_applications_and_stages`: checks each demo posting's application IDs, that ac22 keeps insertion order [b, a], that ac8-b is Applied, ac23-y is Rejected and ac23-x is Applied.
- `test_d13_seed_demo_leaves_stages_unchanged_after_ranking` (R6).
- `test_d13_demo_env_1_serves_plan_table_over_http`: starts a fresh interpreter with `JOBSBOARD_DEMO=1` and checks the same table as JSON over HTTP, plus the ac8 pipeline.
- `test_d13_demo_env_not_exactly_1_does_not_seed`: `JOBSBOARD_DEMO=true` gives 404 for every demo posting.

**`/root/CS690/Project/Milestone-2/tests/property/test_ranking_properties.py`** (5 passed)

The generators make unique IDs, scores 0 to 100, and skills from a pool with case, padding and synonym variants. No property sorts or recomputes the expected order.
- `test_r3_no_flagged_entry_before_an_unflagged_one` (R3): once a flagged entry is seen, no unflagged entry follows.
- `test_r4_within_group_fit_never_increases_and_ties_ascend_by_id` (R4, D2): adjacent entries in the same group have `prev.fit >= next.fit`, and on equal scores `prev.id < next.id`.
- `test_r5_output_ids_are_input_ids_each_exactly_once` (R5): the ID counts in equal the ID counts out, and each entry keeps its own candidate's fit_score.
- `test_r6_input_list_unchanged` (R6): the same Candidate objects in the same order with the same values, and the required set unchanged.
- `test_r6_ranking_through_store_leaves_every_s1_stage_unchanged` (R6): each application is put at a random stage by legal moves, with or without a profile. After `candidates_for_posting` and `rank_applicants`, the S-1 stages and the given list are unchanged.

### 3. Commands run and summary lines
- `.venv/bin/python -m pytest -q tests/unit/test_ranking_edge_cases.py tests/integration/test_ranked_endpoint.py tests/property/test_ranking_properties.py` gave `53 passed, 1 warning in 2.18s`.
  - `tests/unit/test_ranking_edge_cases.py`: `36 passed in 0.11s`
  - `tests/integration/test_ranked_endpoint.py`: `12 passed in 1.27s`
  - `tests/property/test_ranking_properties.py`: `5 passed in 0.85s`
- `.venv/bin/python -m pytest --cov=jobsboard.ranking --cov=jobsboard.ranking_store --cov=jobsboard.api --cov-branch --cov-report=term-missing --cov-fail-under=80` gave `Required test coverage of 80% reached. Total coverage: 97.54%` and `153 passed, 1 warning in 4.37s`. By file: api.py 92% (lines 26, 36 and 47 not run), ranking.py 100%, ranking_store.py 100%.
- Bare `python` is not on PATH here, so I ran both commands with `.venv/bin/python`.
- The one warning is a Starlette/anyio deprecation notice.
- The two `JOBSBOARD_DEMO` tests import `api.py` in a separate interpreter, and coverage does not track that process.
