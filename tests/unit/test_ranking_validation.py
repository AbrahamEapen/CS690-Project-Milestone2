"""Unit tests for S-3 input validation (Task 7; no AC).

Written by test-writer from docs/design/S-3.md §5, §7, D3, D9, D10 (as amended in 622086e and 30ec446)
and D11 (as amended in 30ec446). Each test names the rule, decision or edge case it checks. Expected values come
from the design doc only.
"""
import pytest

from jobsboard.ranking import (
    Candidate,
    DuplicateApplication,
    InvalidFitScore,
    InvalidSkill,
    rank_applicants,
)
from jobsboard.pipeline import ApplicationStore
from jobsboard.ranking_store import PostingNotFound, RankingStore


def _one_app(posting_id: str = "P"):
    # S-1 §4: ApplicationStore.create(posting_id, applicant_id) returns an Application at
    # stage Applied (not Rejected), so D11 keeps it once it has a profile.
    return ApplicationStore().create(posting_id, "applicant-1")


def _ok(application_id: str = "A", skills=("Java",), fit_score: int = 50) -> Candidate:
    return Candidate(application_id=application_id, skills=frozenset(skills), fit_score=fit_score)


# ---------------------------------------------------------------- D3, D9: exception classes

@pytest.mark.parametrize("exc", [InvalidFitScore, DuplicateApplication, InvalidSkill, PostingNotFound])
def test_d3_d10_exceptions_subclass_value_error(exc):
    # D3: exceptions subclass ValueError; D10: PostingNotFound also subclasses ValueError.
    assert issubclass(exc, ValueError)


def test_d3_d9_invalid_fit_score_keeps_constructor_arguments():
    err = InvalidFitScore(application_id="A", fit_score=101)
    assert err.application_id == "A"
    assert err.fit_score == 101


def test_d3_d9_duplicate_application_keeps_constructor_argument():
    err = DuplicateApplication(application_id="A")
    assert err.application_id == "A"


def test_d3_d9_invalid_skill_keeps_constructor_argument():
    err = InvalidSkill(skill="  ")
    assert err.skill == "  "


def test_d3_d9_posting_not_found_keeps_constructor_argument():
    err = PostingNotFound(posting_id="P")
    assert err.posting_id == "P"


# ---------------------------------------------------------------- §5, §7: fit score

@pytest.mark.parametrize("bad", [-1, 101])
def test_s5_s7_out_of_range_fit_score_raises(bad):
    # §5: 0..100 inclusive; §7 edge case: scores of -1 or 101; D3: rejected, not clamped.
    with pytest.raises(InvalidFitScore) as info:
        rank_applicants(frozenset({"Java"}), [_ok("A", fit_score=bad)])
    assert info.value.application_id == "A"
    assert info.value.fit_score == bad
    assert type(info.value.fit_score) is int


@pytest.mark.parametrize("bad", [50.0, "50", None, True])
def test_s5_s7_non_int_fit_score_raises(bad):
    # §5 / §7: a bool, float, str or None raises InvalidFitScore. True == 1 and 50.0 == 50,
    # so the stored value is checked by type as well as by value.
    with pytest.raises(InvalidFitScore) as info:
        rank_applicants(frozenset({"Java"}), [Candidate("A", frozenset({"Java"}), bad)])
    assert info.value.application_id == "A"
    assert type(info.value.fit_score) is type(bad)
    assert info.value.fit_score == bad


def test_s5_fit_score_bounds_0_and_100_accepted():
    # §5: 0 and 100 are inside the inclusive range. Required set is empty, so both meet the
    # minimum (§7); R4 puts 100 before 0.
    ranked = rank_applicants(frozenset(), [_ok("A", fit_score=0), _ok("B", fit_score=100)])
    assert [(e.application_id, e.fit_score) for e in ranked] == [("B", 100), ("A", 0)]


# ---------------------------------------------------------------- §5, D10: skills

@pytest.mark.parametrize("bad", [42, None, b"Java"])
def test_s5_non_str_required_skill_raises(bad):
    # §5: every skill is a str; D10: InvalidSkill.skill is the raw value.
    with pytest.raises(InvalidSkill) as info:
        rank_applicants(frozenset({"Java", bad}), [])
    assert info.value.skill == bad
    assert type(info.value.skill) is type(bad)


@pytest.mark.parametrize("bad", [42, None, b"Java"])
def test_s5_non_str_candidate_skill_raises(bad):
    with pytest.raises(InvalidSkill) as info:
        rank_applicants(frozenset({"Java"}), [Candidate("A", frozenset({"Java", bad}), 50)])
    assert info.value.skill == bad
    assert type(info.value.skill) is type(bad)


@pytest.mark.parametrize("blank", ["", " ", "\t", " \n "])
def test_s5_blank_required_skill_raises_with_raw_value(blank):
    # §5: non-empty after trimming; D10: raises InvalidSkill(raw), not the stripped form.
    with pytest.raises(InvalidSkill) as info:
        rank_applicants(frozenset({"Java", blank}), [])
    assert info.value.skill == blank


@pytest.mark.parametrize("blank", ["", " ", "\t", " \n "])
def test_s5_blank_candidate_skill_raises_with_raw_value(blank):
    with pytest.raises(InvalidSkill) as info:
        rank_applicants(frozenset({"Java"}), [Candidate("A", frozenset({"Java", blank}), 50)])
    assert info.value.skill == blank


def test_d10_required_skills_as_single_str_raise():
    # D10 (622086e): a single str instead of a collection raises InvalidSkill with that str.
    with pytest.raises(InvalidSkill) as info:
        rank_applicants("Java", [])
    assert info.value.skill == "Java"


def test_d10_candidate_skills_as_single_str_raise():
    with pytest.raises(InvalidSkill) as info:
        rank_applicants(frozenset({"Java"}), [Candidate("A", "Java", 50)])
    assert info.value.skill == "Java"


def test_s5_padded_skill_is_not_blank():
    # §5 / §7: " java " is non-empty after strip(), so it is valid and matches "Java" (R1).
    ranked = rank_applicants(frozenset({"Java"}), [Candidate("A", frozenset({" java "}), 50)])
    assert [(e.application_id, e.meets_minimum, e.missing_required) for e in ranked] == [
        ("A", True, ())
    ]


def test_s5_empty_required_skills_allowed():
    # §5: required_skills may be empty; §7: then everyone meets the minimum.
    ranked = rank_applicants(frozenset(), [_ok("A", skills=())])
    assert [(e.application_id, e.meets_minimum, e.flag) for e in ranked] == [("A", True, None)]


def test_d10_candidate_with_no_skills_is_valid():
    # D10: a candidate with no skills is valid; it misses "Java" so it is flagged (R1, R2).
    ranked = rank_applicants(frozenset({"Java"}), [Candidate("A", frozenset(), 50)])
    assert [(e.application_id, e.flag, e.missing_required) for e in ranked] == [
        ("A", "Does not meet minimum", ("Java",))
    ]


def test_d10_any_iterable_accepted():
    # D10: any iterable is accepted for required and candidate skills (list, tuple here).
    ranked = rank_applicants(["Java"], [Candidate("A", ("java",), 50)])
    assert [(e.application_id, e.meets_minimum) for e in ranked] == [("A", True)]


# ---------------------------------------------------------------- D3: duplicate IDs

def test_d3_repeated_application_id_raises():
    with pytest.raises(DuplicateApplication) as info:
        rank_applicants(frozenset({"Java"}), [_ok("A"), _ok("B"), _ok("A")])
    assert info.value.application_id == "A"


@pytest.mark.parametrize("other", ["a", " A", "A "])
def test_d3_duplicate_ids_are_exact_string_matches(other):
    # D3: "A" and "a" / " A" / "A " are different IDs, so no DuplicateApplication;
    # D10: application_id is checked only for duplicates.
    ranked = rank_applicants(frozenset(), [_ok("A", fit_score=60), _ok(other, fit_score=40)])
    assert [e.application_id for e in ranked] == ["A", other]


# ---------------------------------------------------------------- D10: validation order

def test_d10_required_skills_checked_before_candidates():
    # Required has a blank skill; the only candidate has a bad score. Required comes first.
    with pytest.raises(InvalidSkill) as info:
        rank_applicants(frozenset({" "}), [_ok("A", fit_score=101)])
    assert info.value.skill == " "


def test_d10_candidates_checked_in_list_order():
    # First candidate has a blank skill, second a bad score: the first problem in list order.
    with pytest.raises(InvalidSkill) as info:
        rank_applicants(
            frozenset({"Java"}),
            [Candidate("B", frozenset({""}), 50), Candidate("A", frozenset({"Java"}), 101)],
        )
    assert info.value.skill == ""


def test_d10_duplicate_id_checked_before_fit_score():
    # Second "A" has score 101: the duplicate ID is found first for that candidate.
    with pytest.raises(DuplicateApplication) as info:
        rank_applicants(frozenset({"Java"}), [_ok("A"), _ok("A", fit_score=101)])
    assert info.value.application_id == "A"


def test_d10_first_occurrence_bad_score_raised_before_later_duplicate():
    # First "A" has score 101 and is not yet a duplicate, so InvalidFitScore comes first.
    with pytest.raises(InvalidFitScore) as info:
        rank_applicants(frozenset({"Java"}), [_ok("A", fit_score=101), _ok("A")])
    assert (info.value.application_id, info.value.fit_score) == ("A", 101)


def test_d10_fit_score_checked_before_skills():
    with pytest.raises(InvalidFitScore) as info:
        rank_applicants(frozenset({"Java"}), [Candidate("A", frozenset({"", 7}), -1)])
    assert (info.value.application_id, info.value.fit_score) == ("A", -1)


def test_d10_fit_score_checked_before_single_str_skills():
    # The single-str rule is a skills check, so it comes after the fit score check.
    with pytest.raises(InvalidFitScore) as info:
        rank_applicants(frozenset({"Java"}), [Candidate("A", "Java", 101)])
    assert (info.value.application_id, info.value.fit_score) == ("A", 101)


def test_d10_required_non_str_before_blank():
    # Pass 1 (non-str) runs before pass 2 (blank), whatever the list order.
    with pytest.raises(InvalidSkill) as info:
        rank_applicants(["", "Java", 7], [])
    assert info.value.skill == 7


def test_d10_candidate_non_str_before_blank():
    with pytest.raises(InvalidSkill) as info:
        rank_applicants(frozenset({"Java"}), [Candidate("A", ["", "Java", 7], 50)])
    assert info.value.skill == 7


def test_d10_non_str_skills_sorted_by_repr():
    # repr(None) == "None", repr(5) == "5"; "5" < "None" ('5' is 0x35, 'N' is 0x4E),
    # so 5 is raised although None comes first in the list.
    with pytest.raises(InvalidSkill) as info:
        rank_applicants([None, 5], [])
    assert info.value.skill == 5
    with pytest.raises(InvalidSkill) as info:
        rank_applicants(frozenset({"Java"}), [Candidate("A", [None, 5], 50)])
    assert info.value.skill == 5


def test_d10_blank_skills_in_sorted_order():
    # sorted([" ", "\t"]) == ["\t", " "] because "\t" is 0x09 and " " is 0x20,
    # so "\t" is raised although " " comes first in the list.
    with pytest.raises(InvalidSkill) as info:
        rank_applicants([" ", "\t"], [])
    assert info.value.skill == "\t"
    with pytest.raises(InvalidSkill) as info:
        rank_applicants(frozenset({"Java"}), [Candidate("A", [" ", "\t"], 50)])
    assert info.value.skill == "\t"


# ---------------------------------------------------------------- D11: store validates on set

def test_d11_set_requirements_blank_skill_raises():
    with pytest.raises(InvalidSkill) as info:
        RankingStore().set_requirements("P", ["Java", "  "])
    assert info.value.skill == "  "


def test_d11_set_requirements_non_str_skill_raises():
    with pytest.raises(InvalidSkill) as info:
        RankingStore().set_requirements("P", ["Java", 42])
    assert info.value.skill == 42


def test_d11_d10_set_requirements_single_str_raises():
    with pytest.raises(InvalidSkill) as info:
        RankingStore().set_requirements("P", "Java")
    assert info.value.skill == "Java"


def test_d11_set_requirements_order_non_str_before_blank():
    # Same two-pass order as rank_applicants (D10, D11).
    with pytest.raises(InvalidSkill) as info:
        RankingStore().set_requirements("P", ["", None])
    assert info.value.skill is None


def test_d11_empty_requirement_set_allowed():
    # D11: an empty requirement set is allowed; the posting then has requirements set (so no
    # PostingNotFound, D12) and the returned requirement set is empty.
    rs = RankingStore()
    rs.set_requirements("P", [])
    assert rs.candidates_for_posting("P", []) == (frozenset(), [])


def test_d11_set_requirements_accepts_any_iterable():
    rs = RankingStore()
    rs.set_requirements("P", (s for s in ["Java"]))
    assert rs.candidates_for_posting("P", []) == (frozenset({"Java"}), [])


@pytest.mark.parametrize("bad", [-1, 101, 50.0, "50", None, True])
def test_d11_set_profile_bad_fit_score_raises(bad):
    with pytest.raises(InvalidFitScore) as info:
        RankingStore().set_profile("A", ["Java"], bad)
    assert info.value.application_id == "A"
    assert type(info.value.fit_score) is type(bad)
    assert info.value.fit_score == bad


@pytest.mark.parametrize("ok", [0, 100])
def test_d11_set_profile_fit_score_bounds_accepted(ok):
    # §5: 0 and 100 are inside 0..100 inclusive, so the profile is stored as given and
    # candidates_for_posting returns it (D11: posting matches, has a profile, stage Applied).
    app = _one_app()
    rs = RankingStore()
    rs.set_requirements("P", ["Java"])
    rs.set_profile(app.application_id, ["Java"], ok)
    assert rs.candidates_for_posting("P", [app]) == (
        frozenset({"Java"}),
        [Candidate(app.application_id, frozenset({"Java"}), ok)],
    )


def test_d11_set_profile_blank_skill_raises():
    with pytest.raises(InvalidSkill) as info:
        RankingStore().set_profile("A", ["Java", " "], 50)
    assert info.value.skill == " "


def test_d11_set_profile_non_str_skill_raises():
    with pytest.raises(InvalidSkill) as info:
        RankingStore().set_profile("A", ["Java", 3.5], 50)
    assert info.value.skill == 3.5


def test_d11_d10_set_profile_single_str_raises():
    # D10 example verbatim: set_profile(id, "Java", 50).
    with pytest.raises(InvalidSkill) as info:
        RankingStore().set_profile("A", "Java", 50)
    assert info.value.skill == "Java"


def test_d11_set_profile_overwrite_is_not_a_duplicate():
    # D11: setters overwrite earlier values; profiles are keyed by application_id, so setting
    # the same ID twice is not a DuplicateApplication.
    # The second set overwrites the first, so the stored fit_score is 60, not 50.
    app = _one_app()
    rs = RankingStore()
    rs.set_requirements("P", ["Java"])
    rs.set_profile(app.application_id, ["Java"], 50)
    rs.set_profile(app.application_id, ["Java"], 60)
    assert rs.candidates_for_posting("P", [app]) == (
        frozenset({"Java"}),
        [Candidate(app.application_id, frozenset({"Java"}), 60)],
    )


# ---------------------------------------------------------------- Q1: D11 set_profile order

@pytest.mark.parametrize("bad_skill", [" ", "", 7])
def test_d11_set_profile_fit_score_checked_before_skills(bad_skill):
    # D11 (30ec446): set_profile checks fit_score before skills (D10 per-candidate order), so
    # a call with fit_score 101 and a bad skill raises InvalidFitScore("A", 101).
    with pytest.raises(InvalidFitScore) as info:
        RankingStore().set_profile("A", ["Java", bad_skill], 101)
    assert (info.value.application_id, info.value.fit_score) == ("A", 101)


def test_d11_set_profile_fit_score_checked_before_single_str_skills():
    # The single-str rule (D10) is a skills check, so fit_score -1 is raised first.
    with pytest.raises(InvalidFitScore) as info:
        RankingStore().set_profile("A", "Java", -1)
    assert (info.value.application_id, info.value.fit_score) == ("A", -1)


# ---------------------------------------------------------------- Q2: D11 failed set keeps store

@pytest.mark.parametrize("bad_skills", [["Java", " "], ["Java", 42], "Java", ""])
def test_d11_failed_set_requirements_keeps_earlier_value(bad_skills):
    # D11 (30ec446): a set that raises leaves the store unchanged, so the earlier
    # requirement set {"kdb+"} is still returned.
    app = _one_app()
    rs = RankingStore()
    rs.set_requirements("P", ["kdb+"])
    rs.set_profile(app.application_id, ["Java"], 70)
    with pytest.raises(InvalidSkill):
        rs.set_requirements("P", bad_skills)
    assert rs.candidates_for_posting("P", [app]) == (
        frozenset({"kdb+"}),
        [Candidate(app.application_id, frozenset({"Java"}), 70)],
    )


@pytest.mark.parametrize("bad_skills", [["Java", " "], ["Java", 42], "Java", ""])
def test_d11_failed_first_set_requirements_leaves_posting_not_found(bad_skills):
    # D11: no earlier value existed, and the failed set must not create one, so the posting
    # still has no requirements and candidates_for_posting raises PostingNotFound("P") (§4).
    rs = RankingStore()
    with pytest.raises(InvalidSkill):
        rs.set_requirements("P", bad_skills)
    with pytest.raises(PostingNotFound) as info:
        rs.candidates_for_posting("P", [])
    assert info.value.posting_id == "P"


@pytest.mark.parametrize(
    "bad_skills, bad_score",
    [(["Java"], 101), (["Java"], -1), (["Java"], 50.0), (["Java", " "], 60), ("Java", 60), ("", 60)],
)
def test_d11_failed_set_profile_keeps_earlier_value(bad_skills, bad_score):
    # D11 (30ec446): the earlier profile ({"Java"}, 50) is kept after a set that raises.
    app = _one_app()
    rs = RankingStore()
    rs.set_requirements("P", ["Java"])
    rs.set_profile(app.application_id, ["Java"], 50)
    with pytest.raises((InvalidFitScore, InvalidSkill)):
        rs.set_profile(app.application_id, bad_skills, bad_score)
    assert rs.candidates_for_posting("P", [app]) == (
        frozenset({"Java"}),
        [Candidate(app.application_id, frozenset({"Java"}), 50)],
    )


def test_d11_failed_first_set_profile_leaves_application_unprofiled():
    # D11: no earlier profile existed and the failed set adds none, so D8/D11 leave the
    # application out: the candidate list is empty.
    app = _one_app()
    rs = RankingStore()
    rs.set_requirements("P", ["Java"])
    with pytest.raises(InvalidFitScore):
        rs.set_profile(app.application_id, ["Java"], 101)
    assert rs.candidates_for_posting("P", [app]) == (frozenset({"Java"}), [])


# ---------------------------------------------------------------- Q3: D10 skills given as ""

def test_d10_required_skills_as_empty_str_raise():
    # D10 (30ec446): a single str, including "", raises InvalidSkill with that str.
    with pytest.raises(InvalidSkill) as info:
        rank_applicants("", [])
    assert info.value.skill == ""
    assert type(info.value.skill) is str


def test_d10_candidate_skills_as_empty_str_raise():
    with pytest.raises(InvalidSkill) as info:
        rank_applicants(frozenset({"Java"}), [Candidate("A", "", 50)])
    assert info.value.skill == ""
    assert type(info.value.skill) is str


def test_d11_d10_set_requirements_empty_str_raises():
    # "" is a str, not an empty requirement set, so the D11 empty-set allowance does not apply.
    with pytest.raises(InvalidSkill) as info:
        RankingStore().set_requirements("P", "")
    assert info.value.skill == ""
    assert type(info.value.skill) is str


def test_d11_d10_set_profile_empty_str_raises():
    with pytest.raises(InvalidSkill) as info:
        RankingStore().set_profile("A", "", 50)
    assert info.value.skill == ""
    assert type(info.value.skill) is str
