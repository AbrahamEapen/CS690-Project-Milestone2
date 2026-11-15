"""Acceptance tests for S-3, ranked applicants (docs/design/S-3.md).

Written from the S-3 acceptance criteria in backlog/backlog.md before any code existed
(AC-6 to AC-8 in Milestone 1). Moved here and un-skipped in Milestone 2; locked at the tag
m2-tests-locked. Do not delete, skip or weaken these tests.
"""
import uuid

FLAG = "Does not meet minimum"


# AC-6: Given posting P requires {Java, kdb+}; applicant A has both with fit score 40;
# applicant B has only Java with fit score 90. When the recruiter opens the ranked list for P,
# Then A is listed above B, and B shows the flag "Does not meet minimum" while A shows no flag.
def test_ac6_flagged_never_above_qualified():
    from jobsboard.ranking import Candidate, rank_applicants

    ranked = rank_applicants(
        frozenset({"Java", "kdb+"}),
        [
            Candidate(application_id="B", skills=frozenset({"Java"}), fit_score=90),
            Candidate(application_id="A", skills=frozenset({"Java", "kdb+"}), fit_score=40),
        ],
    )

    assert [e.application_id for e in ranked] == ["A", "B"]
    assert ranked[0].flag is None
    assert ranked[1].flag == FLAG


# AC-7: Given posting P requires {Java}; applicants A, B, C all have Java, with fit scores
# 55, 80, 70. When the recruiter opens the ranked list for P, Then the list shows B, C, A
# in that order, with no flags.
def test_ac7_qualified_ordered_by_fit_score():
    from jobsboard.ranking import Candidate, rank_applicants

    ranked = rank_applicants(
        frozenset({"Java"}),
        [
            Candidate(application_id="A", skills=frozenset({"Java"}), fit_score=55),
            Candidate(application_id="B", skills=frozenset({"Java"}), fit_score=80),
            Candidate(application_id="C", skills=frozenset({"Java"}), fit_score=70),
        ],
    )

    assert [e.application_id for e in ranked] == ["B", "C", "A"]
    assert all(e.flag is None for e in ranked)


# AC-8: Given posting P requires {Java, kdb+}; applicant B (stage Applied) has only Java.
# When the recruiter opens the ranked list for P, Then B still appears in the list, flagged
# "Does not meet minimum", and B's stage is still Applied.
def test_ac8_flagged_applicant_kept_and_stage_unchanged():
    from fastapi.testclient import TestClient

    from jobsboard.api import app
    from jobsboard.ranking import Candidate, rank_applicants

    client = TestClient(app)
    posting_id = f"posting-{uuid.uuid4().hex}"
    created = client.post(f"/postings/{posting_id}/applications", json={"applicant_id": "applicant-B"})
    app_id = created.json()["application_id"]

    ranked = rank_applicants(
        frozenset({"Java", "kdb+"}),
        [Candidate(application_id=app_id, skills=frozenset({"Java"}), fit_score=75)],
    )

    assert [e.application_id for e in ranked] == [app_id]
    assert ranked[0].flag == FLAG
    stages = client.get(f"/postings/{posting_id}/pipeline").json()["stages"]
    assert app_id in stages["Applied"]


# AC-21 (S-3 D7, R1, R2): Given posting P requires {PostgreSQL}; applicant A has {Postgres}
# with fit score 60; applicant B has {MySQL} with fit score 90. When the recruiter opens the
# ranked list for P, Then A is listed above B; A shows no flag, and B shows the flag
# "Does not meet minimum".
# Hand working: "postgres" and "postgresql" are one SKILL_SYNONYMS group (D7), so A meets the
# minimum; "mysql" is in no group and differs from "postgresql", so B is missing "PostgreSQL"
# (the posting spelling, trimmed, per section 5). R3 puts A (qualified) above B despite 60 < 90.
def test_ac21_synonym_meets_minimum():
    from jobsboard.ranking import Candidate, rank_applicants

    ranked = rank_applicants(
        frozenset({"PostgreSQL"}),
        [
            Candidate(application_id="B", skills=frozenset({"MySQL"}), fit_score=90),
            Candidate(application_id="A", skills=frozenset({"Postgres"}), fit_score=60),
        ],
    )

    assert [e.application_id for e in ranked] == ["A", "B"]
    assert ranked[0].flag is None
    assert ranked[0].meets_minimum is True  # R1
    assert ranked[0].missing_required == ()  # R1: meets_minimum exactly when nothing missing
    assert ranked[1].flag == FLAG
    assert ranked[1].meets_minimum is False  # R2
    assert ranked[1].missing_required == ("PostgreSQL",)  # section 5: posting spelling


# AC-22 (S-3 D2, R4): Given posting P requires {Java}; applications "b" and "a" both have Java
# with fit score 70. When the recruiter opens the ranked list for P, Then the list shows "a"
# then "b", with no flags.
# Hand working: both qualified, equal fit_score 70, so D2 breaks the tie by application_id
# ascending: "a" < "b". Input is given as "b" then "a" so input order cannot produce the answer.
def test_ac22_equal_fit_scores_ordered_by_application_id():
    from jobsboard.ranking import Candidate, rank_applicants

    ranked = rank_applicants(
        frozenset({"Java"}),
        [
            Candidate(application_id="b", skills=frozenset({"Java"}), fit_score=70),
            Candidate(application_id="a", skills=frozenset({"Java"}), fit_score=70),
        ],
    )

    assert [e.application_id for e in ranked] == ["a", "b"]
    assert [e.flag for e in ranked] == [None, None]


# AC-23 (S-3 D8, D4, R7, section 4 HTTP): Given posting P requires {Java}; application X has
# Java with fit score 50 at stage Applied; application Y has Java with fit score 80 and has been
# moved to Rejected; application Z has no fit score yet. When the recruiter requests
# GET /postings/P/ranked, Then the response is 200 and lists only X, unflagged.
# Hand working: Y is Rejected and Z has no profile, so D8/R7 leave both out; X has Java, so it
# meets the minimum (R1), flag null (R2, section 4 JSON), missing_required [] (D12: an array).
def test_ac23_ranked_endpoint_lists_only_scored_non_rejected():
    from fastapi.testclient import TestClient

    from jobsboard import api

    client = TestClient(api.app)
    posting_id = f"posting-{uuid.uuid4().hex}"

    def _apply(applicant_id: str) -> str:
        resp = client.post(f"/postings/{posting_id}/applications", json={"applicant_id": applicant_id})
        assert resp.status_code == 201
        return resp.json()["application_id"]

    x_id = _apply("applicant-X")
    y_id = _apply("applicant-Y")
    z_id = _apply("applicant-Z")  # no profile set: no fit score yet

    api.ranking_store.set_requirements(posting_id, {"Java"})
    api.ranking_store.set_profile(x_id, {"Java"}, 50)
    api.ranking_store.set_profile(y_id, {"Java"}, 80)

    moved = client.post(f"/applications/{y_id}/stage", json={"to_stage": "Rejected"})
    assert moved.status_code == 200
    assert moved.json()["stage"] == "Rejected"

    resp = client.get(f"/postings/{posting_id}/ranked")

    assert resp.status_code == 200
    assert resp.json() == [
        {
            "application_id": x_id,
            "fit_score": 50,
            "meets_minimum": True,
            "flag": None,
            "missing_required": [],
        }
    ]
    assert z_id not in [e["application_id"] for e in resp.json()]
