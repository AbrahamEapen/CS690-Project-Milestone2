"""Integration tests for the S-1 HTTP error paths (docs/design/S-1.md §4, §5 R4, §6, D2).

No mocks: the real api.app and its module-level api.store. Each test uses a unique posting ID
(S-1.md D3). Expected status codes and bodies come from S-1.md §4; the 422 body is FastAPI's
default (D2) and is deliberately not pinned. Added 2026-11-20 (LEDGER entries 61-63).
"""
import uuid

import pytest
from fastapi.testclient import TestClient

from jobsboard import api

client = TestClient(api.app)


def _pid() -> str:
    return f"posting-{uuid.uuid4().hex}"


def _apply(posting_id: str) -> str:
    resp = client.post(f"/postings/{posting_id}/applications", json={"applicant_id": "applicant-1"})
    assert resp.status_code == 201
    return resp.json()["application_id"]


def _stages(posting_id: str) -> dict:
    resp = client.get(f"/postings/{posting_id}/pipeline")
    assert resp.status_code == 200
    return resp.json()["stages"]


# S-1.md §4: 422 if applicant_id is blank; §5: applicant_id is non-empty; R4: a 422 leaves the
# pipeline unchanged, so no application is added.
@pytest.mark.parametrize("blank", ["", "   "])
def test_s1_s4_blank_applicant_id_returns_422_and_adds_nothing(blank: str):
    pid = _pid()
    existing = _apply(pid)
    before = _stages(pid)
    assert before["Applied"] == [existing]

    resp = client.post(f"/postings/{pid}/applications", json={"applicant_id": blank})

    assert resp.status_code == 422
    assert _stages(pid) == before


# S-1.md §4: an unknown application_id returns 404 with this exact body; §6 lists it as an edge
# case; R4: a 404 leaves the pipeline unchanged.
def test_s1_s4_unknown_application_returns_404_and_changes_nothing():
    pid = _pid()
    existing = _apply(pid)
    before = _stages(pid)
    unknown = f"no-such-application-{uuid.uuid4().hex}"

    resp = client.post(f"/applications/{unknown}/stage", json={"to_stage": "Screened"})

    assert resp.status_code == 404
    assert resp.json() == {"detail": {"error": "application_not_found", "application_id": unknown}}
    assert _stages(pid) == before
    assert before["Applied"] == [existing]
