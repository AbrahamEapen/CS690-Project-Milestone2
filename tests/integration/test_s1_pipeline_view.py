"""Integration tests for the S-1 pipeline view (docs/design/S-1.md §4, §7).

No mocks: the real api.app and its module-level api.store. Each test uses a unique posting ID
(S-1.md D3). Expected values come from S-1.md, not from the code. Added 2026-11-20 (LEDGER
entry 66).
"""
import uuid

from fastapi.testclient import TestClient

from jobsboard import api

client = TestClient(api.app)


# S-1.md §7 edge case: an empty posting (all five keys present). §4: GET /postings/{posting_id}/
# pipeline returns 200 {"posting_id", "stages": {"Applied", "Screened", "Interview", "Offer",
# "Rejected"}}; a posting with no applications has every stage list empty (§5: no posting entity
# until S-6, so any posting ID is valid).
def test_s1_s7_empty_posting_returns_all_five_stages_empty():
    pid = f"posting-{uuid.uuid4().hex}"

    resp = client.get(f"/postings/{pid}/pipeline")

    assert resp.status_code == 200
    assert resp.json() == {
        "posting_id": pid,
        "stages": {"Applied": [], "Screened": [], "Interview": [], "Offer": [], "Rejected": []},
    }
