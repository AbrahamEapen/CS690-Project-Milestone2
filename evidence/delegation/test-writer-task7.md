## Task 7 validation tests: report

I wrote `/root/CS690/Project/Milestone-2/tests/unit/test_ranking_validation.py`. I did not change anything under `src/` or `tests/acceptance/`, and I did not commit. The file has **67 tests: 46 fail and 21 pass.** Every failure is because validation is not built yet. None comes from a mistake in a test.

### 1. Findings

**Criteria without a test.** None of the items in the brief are left uncovered. Four points are not decided by the doc, so I did not test them:
- **Q1. Order inside `set_profile`.** D11 says the setters raise "the same errors" as `rank_applicants`. It does not say whether `set_profile` checks the fit score before the skills, so I have no test with both a bad score and a bad skill in one call.
- **Q2. Store after a failed set.** Nothing says what the store holds after a set fails, for example whether an earlier value for that posting or application is kept. Not tested.
- **Q3. Skills given as `""` (an empty str).** Under D10 as amended, a single str raises `InvalidSkill("")`. It could also be read as an empty iterable, which would be valid. Not tested.
- **Q4. Other iterables of characters.** D10 names only `str`. It does not say whether `bytes` given as the whole skills argument counts as a "single str"; `bytes` is not a `str`, so its elements would be ints. Not tested. As one skill inside a collection, `b"Java"` is tested as a non-str skill.

**Expected values that do not follow from their criterion:** none. **Asserts that check only a type or a length:** none. Where I check a type (`type(info.value.fit_score) is type(bad)`), it is next to an exact-value check. I added it because `True == 1` and `50.0 == 50`, so the value check alone would not tell the inputs apart.

**Acceptance tests:** I did not change any of them and found none that looks wrong.

### 2. Tests written

| Test | Rule | Expected value and working |
|---|---|---|
| `test_d3_d10_exceptions_subclass_value_error[x4]` | D3, D10 | All four exceptions, including `PostingNotFound`, subclass `ValueError` |
| `test_d3_d9_*_keeps_constructor_argument(s)` (x4) | D3, D9 | Built with keyword arguments; attributes `application_id`, `fit_score`, `skill`, `posting_id` equal what was passed in |
| `test_s5_s7_out_of_range_fit_score_raises[-1,101]` | §5, §7, D3 | `InvalidFitScore("A", -1 or 101)`, rejected rather than clamped |
| `test_s5_s7_non_int_fit_score_raises[50.0,"50",None,True]` | §5, §7 | `InvalidFitScore("A", raw)`, with the raw value's type kept |
| `test_s5_fit_score_bounds_0_and_100_accepted` | §5 | No required skills, so both candidates meet the minimum; R4 gives `[("B",100),("A",0)]` |
| `test_s5_non_str_{required,candidate}_skill_raises[42,None,b"Java"]` | §5, D10 | `InvalidSkill(raw)` |
| `test_s5_blank_{required,candidate}_skill_raises_with_raw_value["", " ", "\t", " \n "]` | §5, D10 | `InvalidSkill(raw)`, the value before stripping |
| `test_d10_{required,candidate}_skills_as_single_str_raise` | D10 (622086e) | `InvalidSkill("Java")` |
| `test_s5_padded_skill_is_not_blank` | §5, §7, R1 | `" java "` meets `"Java"`, giving `("A", True, ())` |
| `test_s5_empty_required_skills_allowed` | §5, §7 | `("A", True, None)` |
| `test_d10_candidate_with_no_skills_is_valid` | D10, R1, R2 | `("A", "Does not meet minimum", ("Java",))` |
| `test_d10_any_iterable_accepted` | D10 | A list for required skills and a tuple for candidate skills give `[("A", True)]` |
| `test_d3_repeated_application_id_raises` | D3 | For the list [A, B, A]: `DuplicateApplication("A")` |
| `test_d3_duplicate_ids_are_exact_string_matches["a"," A","A "]` | D3, D10 | No error; scores 60 and 40 give the order `["A", other]` |
| `test_d10_required_skills_checked_before_candidates` | D10 | Required `{" "}` with candidate score 101 raises `InvalidSkill(" ")` |
| `test_d10_candidates_checked_in_list_order` | D3, D10 | The first candidate's blank skill wins over the second candidate's bad score: `InvalidSkill("")` |
| `test_d10_duplicate_id_checked_before_fit_score` | D10 | For [A, A with 101]: `DuplicateApplication("A")` |
| `test_d10_first_occurrence_bad_score_raised_before_later_duplicate` | D10 | For [A with 101, A]: `InvalidFitScore("A", 101)` |
| `test_d10_fit_score_checked_before_skills` | D10 | Skills `{"", 7}` with score -1 raise `InvalidFitScore("A", -1)` |
| `test_d10_fit_score_checked_before_single_str_skills` | D10 | Skills `"Java"` with score 101 raise `InvalidFitScore("A", 101)`. The single-str rule is a skills check, so it runs after the fit score |
| `test_d10_{required,candidate}_non_str_before_blank` | D10 | `["", "Java", 7]` raises `InvalidSkill(7)`, because pass 1 runs before pass 2 |
| `test_d10_non_str_skills_sorted_by_repr` | D10 | `[None, 5]`: `repr` gives `"5"` and `"None"`, and `'5'` (0x35) < `'N'` (0x4E), so the result is `InvalidSkill(5)` even though None comes first in the list. Checked for required and candidate skills |
| `test_d10_blank_skills_in_sorted_order` | D10 | `[" ", "\t"]`: `"\t"` (0x09) < `" "` (0x20), so the result is `InvalidSkill("\t")`. Checked for required and candidate skills |
| `test_d11_set_requirements_{blank,non_str}_skill_raises`, `..._single_str_raises`, `..._order_non_str_before_blank` | D11, D10 | `InvalidSkill("  ")`, `InvalidSkill(42)`, `InvalidSkill("Java")`; `["", None]` raises `InvalidSkill(None)` |
| `test_d11_empty_requirement_set_allowed` | D11, D12 | `candidates_for_posting("P", []) == (frozenset(), [])` with no `PostingNotFound` |
| `test_d11_set_requirements_accepts_any_iterable` | D11 | A generator gives `(frozenset({"Java"}), [])` |
| `test_d11_set_profile_bad_fit_score_raises[-1,101,50.0,"50",None,True]` | D11, §5 | `InvalidFitScore("A", raw)` |
| `test_d11_set_profile_fit_score_bounds_accepted[0,100]` | D11, §5 | Does not raise |
| `test_d11_set_profile_{blank,non_str}_skill_raises`, `test_d11_d10_set_profile_single_str_raises` | D11, D10 | `InvalidSkill(" ")`, `InvalidSkill(3.5)`, `InvalidSkill("Java")`, using the D10 example as written |
| `test_d11_set_profile_overwrite_is_not_a_duplicate` | D11 | Setting the same ID twice does not raise |

### 3. Test run

Command: `.venv/bin/python -m pytest -q tests/unit/test_ranking_validation.py`

Summary line: `46 failed, 21 passed in 0.51s`

**Which fail and why.** All 46 failures are tests that expect an exception that has not been built:
- **37 "DID NOT RAISE":** 25 for `InvalidSkill`, 12 for `InvalidFitScore`, and 2 for `DuplicateApplication`.
- **5 `AttributeError`:** the existing ranking code calls `.strip()` or `.casefold()` on a non-str skill (int, None, bytes).
- **2 `TypeError`:** the sort key negates `None` or a `str` fit score.
- **2 not listed above:** the full run shows 46 failures, but these failure-reason counts add up to 44.

There are no ImportErrors and no errors from the tests themselves.

**Already passing (21).** These are the tests the brief expected might already pass:
- the exception-class and attribute tests (8);
- the valid-input tests: scores 0 and 100, padded skill, empty requirements, candidate with no skills, any iterable, exact-match IDs (8);
- the store tests: empty requirement set, generator for requirements, `set_profile` with 0 and 100, overwrite (5).
