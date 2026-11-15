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
