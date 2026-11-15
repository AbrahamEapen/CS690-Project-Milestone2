"""Unit tests for the S-3 section 7 edge cases and invalid inputs to every section 4 function.

Deliverable 5a, written by test-writer from docs/design/S-3.md sections 4 to 8 and
backlog/backlog.md. Expected values are worked out by hand from the doc, never from the code.

Section 7 edge cases and the test that covers each (before this file):
  1. No required skills, everyone meets the minimum
       unit: test_s5_empty_required_skills_allowed (one candidate). Added here: several candidates.
  2. Every applicant flagged                      none. Added: test_s7_every_applicant_flagged
  3. An empty list                                none. Added: test_s7_empty_candidate_list*
  4. Flagged 100 vs unflagged 0 (R3)              none (AC-6 uses 90 vs 40). Added.
  5. Case / outer spaces (" java " vs "Java")     unit: test_s5_padded_skill_is_not_blank (padded
       candidate skill only). Added: padded required skill and its trimmed missing spelling.
  6. Scores -1 or 101                             unit: test_s5_s7_out_of_range_fit_score_raises
  7. Synonym "postgres" meets "PostgreSQL"        acceptance: test_ac21 uses "Postgres". Added:
       the lowercase "postgres" spelling from section 7.
  8. Synonym "PostgreSQL" meets "Postgres"        none. Added.
  9. Posting requires both "Postgres" and "PostgreSQL" (one requirement, D7)   none. Added.
 10. Equal fit scores within a group (D2)         acceptance: test_ac22 (qualified group only).
       Added: the flagged group.
 11. Unknown posting (404)                        unit: test_d11_failed_first_set_requirements_
       leaves_posting_not_found (indirect). Added: plain unknown posting here; 404 in
       tests/integration/test_ranked_endpoint.py.
 12. Every application Rejected or unscored ([]) acceptance: test_ac23 (X still listed). Added:
       store level here; HTTP in tests/integration/test_ranked_endpoint.py.
 13. Non-int fit scores 50.0, "50", None, True    unit: test_s5_s7_non_int_fit_score_raises
 14. A non-str skill                              unit: test_s5_non_str_*_skill_raises
"""
import dataclasses

import pytest

from jobsboard.pipeline import ApplicationStore, Stage, move_stage
from jobsboard.ranking import (
    Candidate,
    InvalidFitScore,
    InvalidSkill,
    RankedEntry,
    rank_applicants,
)
from jobsboard.ranking_store import PostingNotFound, RankingStore

FLAG = "Does not meet minimum"  # FLAG_TEXT, section 8 named settings


def _c(application_id: str, skills, fit_score: int) -> Candidate:
    return Candidate(application_id=application_id, skills=frozenset(skills), fit_score=fit_score)


def _rows(ranked: list[RankedEntry]) -> list[tuple]:
    return [(e.application_id, e.fit_score, e.meets_minimum, e.flag, e.missing_required) for e in ranked]


# ------------------------------------------------------------------ section 7 edge cases

def test_s7_no_required_skills_everyone_meets_minimum():
    # Edge 1, section 5 (required may be empty), R1, R2, R4.
    # Nothing is required, so nothing is missing: all meet, flag None. One group, so R4
    # orders by fit_score descending: B 20, then A 10.
    ranked = rank_applicants(frozenset(), [_c("A", [], 10), _c("B", ["kdb+"], 20)])
    assert _rows(ranked) == [("B", 20, True, None, ()), ("A", 10, True, None, ())]


def test_s7_every_applicant_flagged_and_d2_tie_in_flagged_group():
    # Edge 2 and edge 10 (D2 within the flagged group), R1, R2, R4.
    # Required {kdb+}; no one has it, so all three are flagged, missing ("kdb+",).
    # Flagged group by fit desc: 80, 80, 30; the 80 tie goes by application_id ascending,
    # "B" < "C". Input order C, A, B so input order cannot produce the answer.
    ranked = rank_applicants(
        frozenset({"kdb+"}),
        [_c("C", [], 80), _c("A", ["Java"], 30), _c("B", ["Java"], 80)],
    )
    assert _rows(ranked) == [
        ("B", 80, False, FLAG, ("kdb+",)),
        ("C", 80, False, FLAG, ("kdb+",)),
        ("A", 30, False, FLAG, ("kdb+",)),
    ]


def test_s7_empty_candidate_list_returns_empty_list():
    # Edge 3: no candidates in, no entries out (R5: output IDs are exactly the input IDs).
    assert rank_applicants(frozenset({"Java"}), []) == []


def test_s7_empty_candidate_list_and_no_required_skills():
    # Edge 3 with edge 1.
    assert rank_applicants(frozenset(), []) == []


def test_s7_r3_flagged_100_never_above_unflagged_0():
    # Edge 4, R3: F scores 100 but lacks Java; U scores 0 and has Java. U first anyway.
    ranked = rank_applicants(frozenset({"Java"}), [_c("F", ["Python"], 100), _c("U", ["Java"], 0)])
    assert _rows(ranked) == [("U", 0, True, None, ()), ("F", 100, False, FLAG, ("Java",))]


def test_s7_padded_required_skill_matches_and_missing_shows_trimmed_spelling():
    # Edge 5, R1, section 5. Required " Java " normalizes to "java"; "JAVA" normalizes to
    # "java" too, so A meets. B lacks it; missing_required holds the trimmed posting
    # spelling "Java" (section 5), not " Java ".
    ranked = rank_applicants(frozenset({" Java "}), [_c("B", ["Python"], 50), _c("A", ["JAVA"], 40)])
    assert _rows(ranked) == [("A", 40, True, None, ()), ("B", 50, False, FLAG, ("Java",))]


def test_s7_lowercase_postgres_meets_postgresql():
    # Edge 7, R1, D7: "postgres" and "postgresql" are one SKILL_SYNONYMS group.
    ranked = rank_applicants(frozenset({"PostgreSQL"}), [_c("A", ["postgres"], 60)])
    assert _rows(ranked) == [("A", 60, True, None, ())]


def test_s7_postgresql_meets_postgres_reverse_direction():
    # Edge 8, R1 ("Matching works in both directions"), D7 (membership is symmetric).
    ranked = rank_applicants(frozenset({"Postgres"}), [_c("A", ["PostgreSQL"], 60)])
    assert _rows(ranked) == [("A", 60, True, None, ())]


def test_d7_word_group_both_directions():
    # D7 second group {word, microsoft word}; R1 both directions, with case and outer spaces.
    ranked = rank_applicants(frozenset({"Microsoft Word"}), [_c("A", [" word "], 70)])
    assert _rows(ranked) == [("A", 70, True, None, ())]
    ranked = rank_applicants(frozenset({"Word"}), [_c("A", ["MICROSOFT WORD"], 70)])
    assert _rows(ranked) == [("A", 70, True, None, ())]


def test_s7_d7_d1_postgres_and_postgresql_required_count_as_one():
    # Edge 9, D1, D7: both required spellings are one requirement.
    # A has "postgresql": meets. B has MySQL: missing exactly one entry. D1 picks the posting
    # spelling first by (casefold(), spelling): "postgres" < "postgresql" (prefix), so
    # "Postgres". Order: A (qualified) then B (flagged, R3) although 50 < 60.
    ranked = rank_applicants(
        frozenset({"Postgres", "PostgreSQL"}),
        [_c("B", ["MySQL"], 60), _c("A", ["postgresql"], 50)],
    )
    assert _rows(ranked) == [("A", 50, True, None, ()), ("B", 60, False, FLAG, ("Postgres",))]


def test_d1_equal_required_spellings_count_as_one_and_first_spelling_shown():
    # D1: "Java" and "java" are equal after normalizing, so one requirement. Both casefold
    # to "java"; tie broken by spelling: "Java" < "java" ('J' 0x4A < 'j' 0x6A).
    ranked = rank_applicants(["Java", "java"], [_c("A", [], 50)])
    assert _rows(ranked) == [("A", 50, False, FLAG, ("Java",))]


def test_d1_inner_spaces_not_collapsed():
    # D1: no collapsing of inner spaces. "microsoft  word" (two spaces) is not
    # "microsoft word", is in no synonym group, and is not equal to it: A is flagged.
    ranked = rank_applicants(frozenset({"Microsoft Word"}), [_c("A", ["Microsoft  Word"], 50)])
    assert _rows(ranked) == [("A", 50, False, FLAG, ("Microsoft Word",))]


def test_s5_missing_required_sorted_by_casefold_then_spelling():
    # Section 5: missing_required sorted by (casefold(), spelling).
    # casefold keys: "apple" < "banana" < "kdb+", so ("apple", "Banana", "kdb+").
    # (Plain sorted() would put "Banana" first, 'B' 0x42 < 'a' 0x61, so this tells them apart.)
    ranked = rank_applicants(frozenset({"kdb+", "Banana", "apple"}), [_c("A", [], 50)])
    assert ranked[0].missing_required == ("apple", "Banana", "kdb+")


def test_s7_store_every_application_rejected_or_unscored_gives_no_candidates():
    # Edge 12, D8, D11, R7. Posting P: R is Rejected (has a profile), U has no profile.
    # Neither is eligible, so candidates_for_posting returns the requirements and [].
    apps = ApplicationStore()
    rejected = apps.create("P", "applicant-R")
    unscored = apps.create("P", "applicant-U")
    move_stage(apps, rejected.application_id, Stage.REJECTED)
    rs = RankingStore()
    rs.set_requirements("P", ["Java"])
    rs.set_profile(rejected.application_id, ["Java"], 90)
    reqs, cands = rs.candidates_for_posting("P", apps.list_for_posting("P"))
    assert (reqs, cands) == (frozenset({"Java"}), [])
    assert rank_applicants(reqs, cands) == []
    assert unscored.application_id not in [c.application_id for c in cands]


def test_d11_candidates_for_posting_keeps_only_this_posting_in_given_order():
    # D11: keeps applications with the given posting_id, a profile, not Rejected, in the
    # order given. Q's application has a profile but another posting, so it is left out.
    apps = ApplicationStore()
    first = apps.create("P", "applicant-1")
    other = apps.create("Q", "applicant-2")
    second = apps.create("P", "applicant-3")
    rs = RankingStore()
    rs.set_requirements("P", ["Java"])
    for app, score in ((first, 10), (other, 20), (second, 30)):
        rs.set_profile(app.application_id, ["Java"], score)
    reqs, cands = rs.candidates_for_posting("P", [second, other, first])
    assert reqs == frozenset({"Java"})
    assert cands == [
        Candidate(second.application_id, frozenset({"Java"}), 30),
        Candidate(first.application_id, frozenset({"Java"}), 10),
    ]


# ------------------------------------------------------------------ invalid input per section 4 function

@pytest.mark.parametrize("bad", [False, 100.0, 0.0, -100])
def test_s4_rank_applicants_invalid_fit_score(bad):
    # Section 5: a bool (False == 0 is in range but is a bool), a float (even 100.0 / 0.0),
    # or an out-of-range int raises InvalidFitScore(application_id, fit_score) (section 4, D3).
    with pytest.raises(InvalidFitScore) as info:
        rank_applicants(frozenset({"Java"}), [Candidate("A", frozenset({"Java"}), bad)])
    assert info.value.application_id == "A"
    assert info.value.fit_score == bad
    assert type(info.value.fit_score) is type(bad)


def test_s4_rank_applicants_list_valued_skill_raises_invalid_skill():
    # Section 5: every skill is a str; anything else (here a list) raises InvalidSkill with the
    # raw value (D10). D10: any iterable is accepted, so a list of skills is fine.
    with pytest.raises(InvalidSkill) as info:
        rank_applicants(["Java"], [Candidate("A", ["Java", ["kdb+"]], 50)])
    assert info.value.skill == ["kdb+"]


@pytest.mark.parametrize("bad", [None, 1.5, b"kdb+"])
def test_s4_set_requirements_non_str_in_frozenset_raises(bad):
    # Section 4, D11: same errors as rank_applicants; InvalidSkill.skill is the raw value.
    with pytest.raises(InvalidSkill) as info:
        RankingStore().set_requirements("P", frozenset({"Java", bad}))
    assert info.value.skill == bad
    assert type(info.value.skill) is type(bad)


def test_s4_set_requirements_list_valued_skill_raises():
    with pytest.raises(InvalidSkill) as info:
        RankingStore().set_requirements("P", ["Java", ["kdb+"]])
    assert info.value.skill == ["kdb+"]


@pytest.mark.parametrize("bad", [False, 100.5, 102])
def test_s4_set_profile_invalid_fit_score(bad):
    # Section 5: bool False, float, or out of range raises InvalidFitScore (D11).
    with pytest.raises(InvalidFitScore) as info:
        RankingStore().set_profile("A", ["Java"], bad)
    assert (info.value.application_id, info.value.fit_score) == ("A", bad)
    assert type(info.value.fit_score) is type(bad)


def test_s4_set_profile_non_str_skill_in_frozenset_raises():
    with pytest.raises(InvalidSkill) as info:
        RankingStore().set_profile("A", frozenset({"Java", 7}), 50)
    assert info.value.skill == 7


def test_s4_candidates_for_posting_unknown_posting_raises():
    # Edge 11, section 4: PostingNotFound(posting_id) when the posting has no requirements set.
    with pytest.raises(PostingNotFound) as info:
        RankingStore().candidates_for_posting("unknown-posting", [])
    assert info.value.posting_id == "unknown-posting"


def test_s4_candidates_for_posting_other_case_posting_is_unknown():
    # D12: posting_id is any str, 404 exactly when no requirements are set for it. Setting
    # requirements for "P" sets none for "p".
    rs = RankingStore()
    rs.set_requirements("P", ["Java"])
    with pytest.raises(PostingNotFound) as info:
        rs.candidates_for_posting("p", [])
    assert info.value.posting_id == "p"


def test_s4_candidates_for_posting_with_applications_but_no_requirements_raises():
    # Section 4: PostingNotFound depends only on requirements, not on applications or profiles.
    apps = ApplicationStore()
    app = apps.create("P", "applicant-1")
    rs = RankingStore()
    rs.set_profile(app.application_id, ["Java"], 50)
    with pytest.raises(PostingNotFound) as info:
        rs.candidates_for_posting("P", [app])
    assert info.value.posting_id == "P"


def test_s4_candidate_is_frozen():
    # Section 4: Candidate is a frozen dataclass, so assigning a field raises.
    c = Candidate("A", frozenset({"Java"}), 50)
    with pytest.raises(dataclasses.FrozenInstanceError):
        c.fit_score = 99
    with pytest.raises(dataclasses.FrozenInstanceError):
        c.application_id = "B"
    assert (c.application_id, c.skills, c.fit_score) == ("A", frozenset({"Java"}), 50)


def test_s4_ranked_entry_is_frozen():
    # Section 4: RankedEntry is a frozen dataclass; a recruiter-side flag change (no override,
    # D6) cannot be made by assigning to the entry.
    e = RankedEntry("A", 50, False, FLAG, ("Java",))
    with pytest.raises(dataclasses.FrozenInstanceError):
        e.flag = None
    with pytest.raises(dataclasses.FrozenInstanceError):
        e.meets_minimum = True
    assert (e.application_id, e.fit_score, e.meets_minimum, e.flag, e.missing_required) == (
        "A", 50, False, FLAG, ("Java",)
    )


def test_s4_ranked_entries_from_rank_applicants_are_frozen():
    ranked = rank_applicants(frozenset({"Java"}), [_c("A", ["Java"], 50)])
    with pytest.raises(dataclasses.FrozenInstanceError):
        ranked[0].fit_score = 0


def test_s4_dataclass_field_names():
    # Section 4 field names and order; D12 uses them as the JSON field names.
    assert [f.name for f in dataclasses.fields(Candidate)] == ["application_id", "skills", "fit_score"]
    assert [f.name for f in dataclasses.fields(RankedEntry)] == [
        "application_id", "fit_score", "meets_minimum", "flag", "missing_required"
    ]


def test_s4_candidate_missing_argument_raises_type_error():
    # Section 4: all three Candidate fields are required (no defaults are given).
    with pytest.raises(TypeError):
        Candidate("A", frozenset({"Java"}))
