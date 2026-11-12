# Gap check 2: S-3 (Milestone 2, Deliverable 1d)

Prompt: `prompts/s3_gap_check_2_prompt.md`. The doc checked was `docs/design/S-3.md` at commit a0710e9, after the open questions were settled (1c).
Agent: Claude Code, Claude Opus 5.5 (claude-opus-5-5), fresh general-purpose subagent, 2026-11-11. It was told to read only the design doc.

## Full reply (verbatim)

1. The status line says S-3 is "built in Milestone 2". Does `jobsboard.ranking` or `jobsboard.ranking_store` already exist? If so, am I extending it or writing it from scratch?
2. Which module defines each exception (`InvalidFitScore`, `DuplicateApplication`, `InvalidSkill`, `PostingNotFound`)? Must `ranking_store` import the domain exceptions from `ranking`, or define its own?
3. Exceptions "keep their constructor arguments as attributes". Are the attribute names exactly the parameter names (`application_id`, `fit_score`, `skill`, `posting_id`)? Is there a required message format for `str(exc)`?
4. Which module holds `FLAG_TEXT`, `FIT_SCORE_MIN`, `FIT_SCORE_MAX` and `SKILL_SYNONYMS`? What data type is `SKILL_SYNONYMS` (for example, a tuple of frozensets or a dict mapping each skill to its group)? Is it public API that tests import?
5. D3 says to raise "the first problem in list order". Are `required_skills` validated before `candidates`, or after? `required_skills` is a frozenset with no order, so if several required skills are invalid, which one is reported?
6. Within a single candidate, in what order are the checks done (duplicate ID, then fit score, then skills, or something else)? If one candidate has several invalid skills, which one is reported, given that its skills are also an unordered frozenset?
7. For duplicate IDs, is `DuplicateApplication` raised when the second occurrence is reached, even if the first occurrence also has an invalid score that a full pass would have reported?
8. Does `InvalidSkill.skill` hold the raw value as given (for example `"  "`) or the trimmed value?
9. Besides being empty after trimming, are other skill values invalid? Should non-`str` values raise `InvalidSkill`, `TypeError`, or not be checked at all?
10. Apart from `bool`, which `fit_score` types are rejected? Should a float such as `50.0`, a numeric string, or `None` raise `InvalidFitScore`, or a different error?
11. Is `application_id` validated at all, for example an empty string, whitespace only, or a non-`str` value? If so, which exception does it raise?
12. Must `rank_applicants` accept only a `frozenset` for `required_skills` and a `list` for `candidates`, or any iterable? Should other types be rejected?
13. Is a candidate with an empty `skills` frozenset valid?
14. `missing_required` is "sorted case-insensitively". Is the sort key `casefold()` alone, or `(casefold(), spelling)` as in D1?
15. D1 says to show the "posting spelling", and §5 says the "trimmed spelling". In the `(casefold(), spelling)` tie-break, is `spelling` compared before or after trimming? Is it the trimmed form that gets returned?
16. When a candidate has a skill that is a synonym of a required skill, should its matching use the same "one requirement" merging as D1 (for example, a candidate with only `"postgres"` against a posting that requires both `"Postgres"` and `"PostgreSQL"`)? Or is that already implied?
17. Does `RankingStore.set_requirements` take a `frozenset`, any iterable, or a list? Does it validate skills when called or only at ranking time? Does it overwrite earlier requirements or merge with them? Can it be called with an empty set so that a posting has "requirements" but no skills?
18. Does `set_profile` validate `fit_score` and `skills` when called, or does an invalid value surface only when `rank_applicants` runs? Does calling it again overwrite the profile?
19. Is a profile keyed only by `application_id`, independent of posting? Must the application exist in the S-1 `ApplicationStore` when `set_profile` is called?
20. What exactly is the `applications` argument to `candidates_for_posting`: a list of S-1 `Application` objects, IDs, or something else? What are the attribute names for the ID, posting and stage?
21. Does `candidates_for_posting` filter `applications` by `posting_id` itself, or does it assume the caller has already passed only that posting's applications?
22. How is "stage Rejected" detected: which S-1 enum or member name, and is it compared by identity or by value?
23. In what order does `candidates_for_posting` return candidates? Does it matter, given that D3 errors are reported in list order?
24. The 404 case: is it returned only when the ranking store has no requirements for the posting? What if the posting exists in S-1 but has no requirements, or has requirements but does not exist in S-1?
25. What type is `posting_id` in the path and in the store (`str` or `int`)? How should a malformed ID be handled?
26. What should the HTTP endpoint return if stored data makes `rank_applicants` raise `InvalidFitScore`, `InvalidSkill` or `DuplicateApplication`: 500, 422, or some other status and body?
27. In the JSON response, are the field names exactly the dataclass field names and is `missing_required` a JSON array? Is any field order or response-model or schema declaration required?
28. Where does the FastAPI app live (module or file name, and an app object or a factory)? How are the `RankingStore` and S-1 `ApplicationStore` instances created and shared (module-level singleton, dependency injection, `app.state`)? How do tests swap in a fresh store?
29. What is the S-1 `ApplicationStore` interface: how do I list a posting's applications and read their stages?
30. `JOBSBOARD_DEMO=1` seed: which postings, required skills, applications, profiles and scores should be seeded? Must they also be created in the S-1 store?
31. When is `JOBSBOARD_DEMO` read: at import, at app startup, or at app creation? Does only the exact value `"1"` turn it on? Where does the seeding code live?
32. Should seeding be idempotent if the app is created more than once, for example across tests?
33. Outside the demo, how do requirements and profiles reach the store? Should any HTTP endpoint write them, or only Python calls?
34. AC-21, AC-22 and AC-23 have no tests yet. Should I write them, wait for the test-writer, or build against assumed expectations? What exact assertions will they make?
35. Which test path is current: `tests/test_s3_ranking.py` or `tests/acceptance/test_s3_ranking.py`? Should my code assume one import path or layout?
36. Under R6 / AC-8, what counts as "every S-1 stage unchanged"? Does the endpoint or ranking store have to avoid any reads that have side effects on the S-1 store?
37. Do "A-4", "A-5", "E-11" to "E-14", INT-03 and INT-04 impose any constraints not stated in this doc, given that I cannot see those sources?

## Marks

**Real gap** questions are settled in `S-3.md` §8 at the decision named. **Answered** questions name the section that already answers them. Decisions on Q9, Q10 and Q17/18/26 were made by the team (Abraham) on 2026-11-11; the others are team decisions recorded in D9–D13.

| # | Mark | Resolution |
| --- | --- | --- |
| 1 | Real gap | D4: neither module exists at the start of M2; both are new files. |
| 2 | Real gap | D9: the three ranking errors are in `ranking.py`; `PostingNotFound` is in `ranking_store.py`, which imports the ranking errors. |
| 3 | Real gap | D9: attribute names equal parameter names; no message format is required. |
| 4 | Real gap | D9: all named settings are in `ranking.py`; `SKILL_SYNONYMS: tuple[frozenset[str], ...]`, public. |
| 5 | Real gap | D10: `required_skills` first, in `sorted()` order, then candidates in list order. |
| 6 | Real gap | D10: per candidate, duplicate ID, then fit score, then skills in `sorted()` order. |
| 7 | Real gap | D10: checks run candidate by candidate, so an earlier candidate's invalid score is raised before a later duplicate. |
| 8 | Real gap | D10: the raw value as given. |
| 9 | Real gap | §5 / D10: a skill must be a `str` that is non-empty after trimming; otherwise `InvalidSkill`. |
| 10 | Real gap | §5 / D10: any `fit_score` that is not a plain `int` (`bool`, float, str, `None`) raises `InvalidFitScore`. |
| 11 | Real gap | D10: `application_id` is checked only for duplicates (S-1 creates IDs). |
| 12 | Real gap | D10: any iterable is accepted; container types are not checked. |
| 13 | Real gap | D10: yes; it meets the minimum only when there are no requirements. |
| 14 | Real gap | §5: sort key `(casefold(), spelling)`, the same as D1. |
| 15 | Real gap | §5 / D1: compared and returned after trimming. |
| 16 | Answered | D1 (synonym requirements count as one) and R1 (either direction). |
| 17 | Real gap | D11: any iterable of str, stored as a frozenset; validated on set; overwrites; an empty set is allowed. |
| 18 | Real gap | D11: validated on set; overwrites. |
| 19 | Real gap | D11: keyed by `application_id` only; the S-1 application need not exist yet. |
| 20 | Real gap | D11: S-1 `Application` objects (`application_id`, `posting_id`, `stage`). |
| 21 | Real gap | D11: it filters by `posting_id` itself. |
| 22 | Real gap | D11: `application.stage is Stage.REJECTED`. |
| 23 | Real gap | D11: the order of the given list (S-1 creation order); the output order comes from R3/R4 only. |
| 24 | Real gap | D12: 404 exactly when the ranking store has no requirements for the posting; S-1 has no posting entity to check. |
| 25 | Real gap | D12: `str`, any value; no malformed case. |
| 26 | Real gap | D11/D12: the store validates on set, so ranking cannot raise from stored data; no extra HTTP error. |
| 27 | Real gap | D12: field names are the dataclass names; `missing_required` is a JSON array; no field order. |
| 28 | Real gap | D12: `api.py` holds module-level `store` (S-1) and `ranking_store`; tests use unique posting IDs, as AC-8 does. |
| 29 | Answered | `S-1.md` §4 and `pipeline.ApplicationStore.list_for_posting` (outside this doc by design). |
| 30 | Real gap | D13: one demo posting per S-3 AC, in both stores; exact rows in `docs/plans/S-3-plan.md`. |
| 31 | Real gap | D13: read once when `api.py` is imported; only `"1"`; code in `ranking_store.seed_demo`. |
| 32 | Real gap | D13: runs once per process; fixed `demo-` posting IDs, so tests never collide with it. |
| 33 | Real gap | D13: Python calls only; S-4 adds the real writer. |
| 34 | Answered | §9: test-writer writes them in Deliverable 3b, before the build. |
| 35 | Answered | §9: moved to `tests/acceptance/` in Deliverable 3. |
| 36 | Answered | R6, plus `S-1.md`: listing applications has no side effects. |
| 37 | Answered | §6 R1 restates A-5 and D4 restates A-4; E-11 to E-14 are motivation only (§1). |

Totals: 30 real gaps (all settled in §8, D1 and D4 updated, D9–D13 added) and 7 already answered.
