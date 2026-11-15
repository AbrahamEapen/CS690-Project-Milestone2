## Report: tests/unit/test_ranking_validation.py (Task 7, D10/D11 as amended in 30ec446)

All three additions and both strengthened tests are in. The file now has **90 tests: 21 pass, 69 fail**. Every failure comes from validation that isn't built yet; none comes from a mistake in a test. I did not edit `src/` or `tests/acceptance/`, and I did not commit.

File: `/root/CS690/Project/Milestone-2/tests/unit/test_ranking_validation.py`

### 1. Findings
- **No criterion is left without a test.** Q1, Q2 and Q3 from your task are all covered now.
- **Skills stored exactly as given (assumption, not a doc rule).** Several store tests expect the stored skills to come back exactly as passed in, for example `frozenset({"Java"})`. The doc never says whether the store keeps raw or normalized skills. The earlier `test_d11_set_requirements_accepts_any_iterable` already assumed this, and the new store tests do too. The two strengthened tests pass against the current code, so the current store keeps skills as given. The team may want to add one sentence to D11 so this is a stated rule.
- **One assert accepts either exception class.** `test_d11_failed_set_profile_keeps_earlier_value` uses `pytest.raises((InvalidFitScore, InvalidSkill))`. That test checks that the store is left unchanged, so I kept it loose on purpose. The exact exception and its attributes for each input are checked by other tests.
- I found no assert that checks only a type or a length, and no expected value that does not follow from the doc.

### 2. Tests written or changed
I added a helper, `_one_app()`. It calls S-1 `ApplicationStore().create("P", "applicant-1")`, which gives an application at stage Applied, so D11 keeps it once it has a profile.

**Strengthened (both pass now):**
- `test_d11_set_profile_fit_score_bounds_accepted[0|100]` (§5, D11): requirements are {"Java"}, then `set_profile(id, ["Java"], ok)`. Expected `candidates_for_posting("P", [app]) == (frozenset({"Java"}), [Candidate(id, frozenset({"Java"}), ok)])`, because 0 and 100 are inside the inclusive range 0..100.
- `test_d11_set_profile_overwrite_is_not_a_duplicate` (D11): set 50, then set 60. The later set overwrites the earlier one, so the expected fit_score is **60**.

**Q1, fit score checked before skills (D11 order):**
- `test_d11_set_profile_fit_score_checked_before_skills[" " | "" | 7]`: `set_profile("A", ["Java", bad], 101)` should raise `InvalidFitScore`, with `(application_id, fit_score) == ("A", 101)`.
- `test_d11_set_profile_fit_score_checked_before_single_str_skills`: `set_profile("A", "Java", -1)` should raise `InvalidFitScore("A", -1)`. The single-str rule is a skills check, so the fit score is checked first.

**Q2, a set that raises leaves the store unchanged (D11):**
- `test_d11_failed_set_requirements_keeps_earlier_value[["Java"," "] | ["Java",42] | "Java" | ""]`: start with requirements {"kdb+"} and profile ({"Java"}, 70). After the failed set, expected `(frozenset({"kdb+"}), [Candidate(id, frozenset({"Java"}), 70)])`.
- `test_d11_failed_first_set_requirements_leaves_posting_not_found[same 4 inputs]`: no earlier value existed. After the failed set, `candidates_for_posting("P", [])` should raise `PostingNotFound` with `posting_id == "P"`.
- `test_d11_failed_set_profile_keeps_earlier_value`, six cases: (["Java"],101), (["Java"],-1), (["Java"],50.0), (["Java"," "],60), ("Java",60), ("",60). The earlier profile ({"Java"}, 50) should still be returned.
- `test_d11_failed_first_set_profile_leaves_application_unprofiled`: the failed set gives the application no profile, so D8/D11 leave it out. Expected `(frozenset({"Java"}), [])`.

**Q3, skills given as "" (D10):**
- `test_d10_required_skills_as_empty_str_raise`: `rank_applicants("", [])`
- `test_d10_candidate_skills_as_empty_str_raise`: a `Candidate("A", "", 50)`
- `test_d11_d10_set_requirements_empty_str_raises`: `set_requirements("P", "")`. This is a str, not an empty requirement set, so the empty-set allowance does not apply.
- `test_d11_d10_set_profile_empty_str_raises`: `set_profile("A", "", 50)`

All four expect `InvalidSkill` with `skill == ""` and `type(skill) is str`.

I also updated the module docstring to cite 30ec446.

### 3. Command and result
`python` is not on PATH in this shell, so I used the venv interpreter:
```
cd /root/CS690/Project/Milestone-2 && .venv/bin/python -m pytest -q tests/unit/test_ranking_validation.py
69 failed, 21 passed in 0.72s
```
Failure reasons, counted from the `E` lines:
- 37: `DID NOT RAISE InvalidSkill`
- 17: `DID NOT RAISE InvalidFitScore`
- 6: `DID NOT RAISE (InvalidFitScore, InvalidSkill)` (the Q2 set_profile cases)
- 2: `DID NOT RAISE DuplicateApplication`
- 7: crashes from the current code meeting unvalidated input: `AttributeError` x5 (`'int'/'NoneType' has no attribute 'strip'`, `'bytes' has no attribute 'casefold'`) and `TypeError` x2 (`bad operand type for unary -` on a str or None fit_score)

In every case the validation is missing from `src/jobsboard/ranking.py` and `ranking_store.py`. There were no import errors and no fixture or setup errors. All the new Q2 tests reach the step that is supposed to raise, so the helper and the `candidates_for_posting` calls work.
