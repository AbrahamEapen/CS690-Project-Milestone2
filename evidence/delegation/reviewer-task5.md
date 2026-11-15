/root/CS690/Project/Milestone-2/src/jobsboard/ranking_store.py:25 | none | minor | `set_requirements` stores `frozenset(skills)` without checking anything. D11 says the setters validate on set with the same errors as `rank_applicants`, and plan Task 5 says "validate-on-set setters", but the code comment puts this off to Task 7. Until then, a call like `set_requirements(p, "Java")` silently stores {"J","a","v"} instead of raising `InvalidSkill("Java")` (D10 as revised in 622086e). Non-`str` and blank skills are also accepted. Not blocking for AC-8, as long as Task 7 adds this.
/root/CS690/Project/Milestone-2/src/jobsboard/ranking_store.py:29 | none | minor | `set_profile` has the same gap (D11, D10, §5). A single `str` skill is split into characters, and an invalid `fit_score` (−1, 101, 50.0, "50", None, True) is stored. That breaks D12's premise that "stored data is always valid", so `/ranked` can return out-of-range scores now, or a 500 once `rank_applicants` validates. Planned for Task 7.
/root/CS690/Project/Milestone-2/src/jobsboard/ranking_store.py:41 | AC-23 | minor | `candidates_for_posting` does not yet drop applications whose stage is Rejected. R7, D8 and D11 require `stage is not Stage.REJECTED`, so for now a Rejected application with a profile appears in `/ranked`. The plan schedules this for Task 6 (the comment at line 40 says so). It does not affect AC-8, which passes.
/root/CS690/Project/Milestone-2/src/jobsboard/api.py:93 | none | minor | No unit or integration test covers the 404 `{"detail": {"error": "posting_not_found"}}` path (§4, D12, edge case "an unknown posting (404)"). None covers a posting that has requirements but no eligible applications returning 200 `[]` (§4). The code looks correct (lines 63-66 and 96-97), but nothing checks it.

Checked and found consistent with the docs:
- `PostingNotFound` subclasses `ValueError` and keeps `posting_id` (D3, D9, D10).
- The 404 is raised only when no requirements are set (D12).
- An empty requirement set is allowed (D11).
- Profiles are keyed by `application_id` only.
- Input order is kept.
- `api.py` has module-level `store` and `ranking_store` (D12).
- JSON field names come from `RankedEntry`, with `flag` as null and `missing_required` as an array (§4, D12).
- The route only reads S-1 data, so stages are unchanged (R6, AC-8).

verdict: pass
