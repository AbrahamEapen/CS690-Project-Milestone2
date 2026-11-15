"""Integration tests for GET /postings/{posting_id}/ranked (S-3, Deliverable 5b).

No mocks: the real api.app with the real module-level api.store (S-1 ApplicationStore) and
api.ranking_store (S-3 data module, D12). Each test uses a unique posting ID (S-1 D3).
Expected values come from docs/design/S-3.md sections 4, 6, 7, 8 and the demo table in
docs/plans/S-3-plan.md.
"""
import json
import os
import subprocess
import sys
import uuid
from pathlib import Path

from fastapi.testclient import TestClient

from jobsboard import api
from jobsboard.pipeline import ApplicationStore, Stage
from jobsboard.ranking import rank_applicants
from jobsboard.ranking_store import RankingStore, seed_demo

FLAG = "Does not meet minimum"
REPO = Path(__file__).resolve().parents[2]
client = TestClient(api.app)


def _pid() -> str:
    return f"posting-{uuid.uuid4().hex}"


def _apply(posting_id: str, applicant_id: str) -> str:
    resp = client.post(f"/postings/{posting_id}/applications", json={"applicant_id": applicant_id})
    assert resp.status_code == 201
    return resp.json()["application_id"]


def _stages(posting_id: str) -> dict:
    return client.get(f"/postings/{posting_id}/pipeline").json()["stages"]


# ------------------------------------------------------------------ 404 (section 4, D12, edge 11)

def test_s7_unknown_posting_returns_404_posting_not_found():
    resp = client.get(f"/postings/{_pid()}/ranked")
    assert resp.status_code == 404
    assert resp.json() == {"detail": {"error": "posting_not_found"}}


def test_d12_posting_with_applications_but_no_requirements_returns_404():
    # D12: 404 exactly when no requirements are set, even if applications and profiles exist.
    pid = _pid()
    app_id = _apply(pid, "applicant-A")
    api.ranking_store.set_profile(app_id, {"Java"}, 50)
    resp = client.get(f"/postings/{pid}/ranked")
    assert resp.status_code == 404
    assert resp.json() == {"detail": {"error": "posting_not_found"}}


# ------------------------------------------------------------------ 200 [] (section 4, edge 12)

def test_s4_requirements_and_no_applications_returns_empty_list():
    pid = _pid()
    api.ranking_store.set_requirements(pid, {"Java"})
    resp = client.get(f"/postings/{pid}/ranked")
    assert resp.status_code == 200
    assert resp.json() == []


def test_d11_empty_requirement_set_and_no_applications_returns_empty_list():
    # D11: an empty requirement set is allowed and counts as "requirements set" (D12), so 200.
    pid = _pid()
    api.ranking_store.set_requirements(pid, [])
    resp = client.get(f"/postings/{pid}/ranked")
    assert resp.status_code == 200
    assert resp.json() == []


def test_s7_r7_every_application_rejected_or_unscored_returns_empty_list():
    # Edge 12, R7, D8: R1 and R2 are scored but Rejected; U has no profile. All left out.
    pid = _pid()
    r1 = _apply(pid, "applicant-R1")
    r2 = _apply(pid, "applicant-R2")
    u = _apply(pid, "applicant-U")
    api.ranking_store.set_requirements(pid, {"Java"})
    api.ranking_store.set_profile(r1, {"Java"}, 90)
    api.ranking_store.set_profile(r2, {"Python"}, 40)
    for app_id in (r1, r2):
        moved = client.post(f"/applications/{app_id}/stage", json={"to_stage": "Rejected"})
        assert moved.status_code == 200

    resp = client.get(f"/postings/{pid}/ranked")

    assert resp.status_code == 200
    assert resp.json() == []
    # R6: the GET changed no stage. R1, R2 under Rejected; U still Applied (S-1 creation order).
    assert _stages(pid) == {"Applied": [u], "Screened": [], "Interview": [], "Offer": [], "Rejected": [r1, r2]}


def test_r7_other_postings_applications_are_not_listed():
    # R7: only this posting's applications. The other posting's application has a profile.
    pid, other = _pid(), _pid()
    mine = _apply(pid, "applicant-A")
    theirs = _apply(other, "applicant-B")
    api.ranking_store.set_requirements(pid, {"Java"})
    api.ranking_store.set_profile(mine, {"Java"}, 10)
    api.ranking_store.set_profile(theirs, {"Java"}, 99)
    resp = client.get(f"/postings/{pid}/ranked")
    assert resp.status_code == 200
    assert [e["application_id"] for e in resp.json()] == [mine]


# ------------------------------------------------------------------ JSON shape and wiring (D12)

def test_d12_module_level_stores_drive_the_route_and_json_shape():
    # Applications go straight into api.store (S-1 create), profiles into api.ranking_store.
    # Required {Java, kdb+}. Hand working:
    #   Q (Java, KDB+ ; 30): "kdb+" casefold matches, meets (R1).   -> qualified group
    #   S (Screened, Java ; 95): missing kdb+ -> flagged (R2), still listed (D6, E-14)
    #   T (Interview, nothing ; 95): missing both -> flagged, missing ["Java", "kdb+"]
    #     ("java" < "kdb+" by casefold, section 5)
    # R3: Q first. Flagged group, 95 tie: application_id ascending (D2) - compared below
    # from the server-set IDs, since S-1 sets them.
    pid = _pid()
    q = api.store.create(pid, "applicant-Q").application_id
    s = api.store.create(pid, "applicant-S").application_id
    t = api.store.create(pid, "applicant-T").application_id
    assert client.post(f"/applications/{s}/stage", json={"to_stage": "Screened"}).status_code == 200
    for to in ("Screened", "Interview"):
        assert client.post(f"/applications/{t}/stage", json={"to_stage": to}).status_code == 200
    api.ranking_store.set_requirements(pid, {"Java", "kdb+"})
    api.ranking_store.set_profile(q, {"Java", "KDB+"}, 30)
    api.ranking_store.set_profile(s, {"Java"}, 95)
    api.ranking_store.set_profile(t, set(), 95)

    resp = client.get(f"/postings/{pid}/ranked")

    s_entry = {"application_id": s, "fit_score": 95, "meets_minimum": False, "flag": FLAG,
               "missing_required": ["kdb+"]}
    t_entry = {"application_id": t, "fit_score": 95, "meets_minimum": False, "flag": FLAG,
               "missing_required": ["Java", "kdb+"]}
    flagged = [s_entry, t_entry] if s < t else [t_entry, s_entry]
    assert resp.status_code == 200
    assert resp.json() == [
        {"application_id": q, "fit_score": 30, "meets_minimum": True, "flag": None, "missing_required": []},
        *flagged,
    ]
    # R6: stages unchanged by the GET, read from the real api.store.
    assert {a.application_id: a.stage for a in api.store.list_for_posting(pid)} == {
        q: Stage.APPLIED, s: Stage.SCREENED, t: Stage.INTERVIEW
    }


# ------------------------------------------------------------------ demo seed (D13, plan table)

def _ranked_via_store(store: ApplicationStore, rs: RankingStore, posting_id: str) -> list[tuple]:
    reqs, cands = rs.candidates_for_posting(posting_id, store.list_for_posting(posting_id))
    return [(e.application_id, e.fit_score, e.meets_minimum, e.flag, e.missing_required)
            for e in rank_applicants(reqs, cands)]


# Expected /ranked rows per demo posting, by hand from the docs/plans/S-3-plan.md table.
#   ac6: requires Java, kdb+; a (Java, kdb+; 40) meets; b (Java; 90) misses kdb+. R3: a, b.
#   ac7: all Java, 80 > 70 > 55: b, c, a.
#   ac8: b (Java; 75) misses kdb+, flagged.
#   ac21: a (Postgres; 60) meets PostgreSQL by D7; b (MySQL; 90) misses "PostgreSQL".
#   ac22: a and b both 70: "a" < "b" (D2).
#   ac23: y Rejected and z unscored are left out (D8): only x 50.
#   empty: requires Java, no applications: [].
DEMO_EXPECTED = {
    "demo-ac6": [("demo-ac6-a", 40, True, None, ()), ("demo-ac6-b", 90, False, FLAG, ("kdb+",))],
    "demo-ac7": [("demo-ac7-b", 80, True, None, ()), ("demo-ac7-c", 70, True, None, ()),
                 ("demo-ac7-a", 55, True, None, ())],
    "demo-ac8": [("demo-ac8-b", 75, False, FLAG, ("kdb+",))],
    "demo-ac21": [("demo-ac21-a", 60, True, None, ()), ("demo-ac21-b", 90, False, FLAG, ("PostgreSQL",))],
    "demo-ac22": [("demo-ac22-a", 70, True, None, ()), ("demo-ac22-b", 70, True, None, ())],
    "demo-ac23": [("demo-ac23-x", 50, True, None, ())],
    "demo-empty": [],
}

DEMO_REQUIREMENTS = {
    "demo-ac6": frozenset({"Java", "kdb+"}),
    "demo-ac7": frozenset({"Java"}),
    "demo-ac8": frozenset({"Java", "kdb+"}),
    "demo-ac21": frozenset({"PostgreSQL"}),
    "demo-ac22": frozenset({"Java"}),
    "demo-ac23": frozenset({"Java"}),
    "demo-empty": frozenset({"Java"}),
}


def test_d13_seed_demo_into_fresh_stores_matches_plan_table():
    store, rs = ApplicationStore(), RankingStore()
    seed_demo(store, rs)
    for posting_id, expected in DEMO_EXPECTED.items():
        assert _ranked_via_store(store, rs, posting_id) == expected, posting_id
        assert rs.candidates_for_posting(posting_id, [])[0] == DEMO_REQUIREMENTS[posting_id], posting_id


def test_d13_seed_demo_s1_applications_and_stages():
    # Plan table: the S-1 store holds these demo applications. ac22 inserts b before a,
    # and S-1 D3 keeps creation order. ac8 b is at Applied ("the pipeline still shows b under
    # Applied"); ac23 y is Rejected. demo-empty has no applications.
    store, rs = ApplicationStore(), RankingStore()
    seed_demo(store, rs)
    ids = {p: [a.application_id for a in store.list_for_posting(p)] for p in DEMO_EXPECTED}
    assert sorted(ids["demo-ac6"]) == ["demo-ac6-a", "demo-ac6-b"]
    assert sorted(ids["demo-ac7"]) == ["demo-ac7-a", "demo-ac7-b", "demo-ac7-c"]
    assert ids["demo-ac8"] == ["demo-ac8-b"]
    assert sorted(ids["demo-ac21"]) == ["demo-ac21-a", "demo-ac21-b"]
    assert ids["demo-ac22"] == ["demo-ac22-b", "demo-ac22-a"]
    assert sorted(ids["demo-ac23"]) == ["demo-ac23-x", "demo-ac23-y", "demo-ac23-z"]
    assert ids["demo-empty"] == []
    assert store.get("demo-ac8-b").stage is Stage.APPLIED
    assert store.get("demo-ac23-y").stage is Stage.REJECTED
    assert store.get("demo-ac23-x").stage is Stage.APPLIED


def test_d13_seed_demo_leaves_stages_unchanged_after_ranking():
    # R6 on the demo data: ranking every demo posting changes no S-1 stage.
    store, rs = ApplicationStore(), RankingStore()
    seed_demo(store, rs)
    before = {p: [(a.application_id, a.stage) for a in store.list_for_posting(p)] for p in DEMO_EXPECTED}
    for p in DEMO_EXPECTED:
        _ranked_via_store(store, rs, p)
    after = {p: [(a.application_id, a.stage) for a in store.list_for_posting(p)] for p in DEMO_EXPECTED}
    assert after == before


def test_d13_seed_demo_applicant_ids_are_non_empty_strings():
    # D13 seed must hold valid S-1 Applications. S-1 §5: applicant_id is a str, non-empty;
    # S-1 §4: an Application's JSON fields (application_id, posting_id, applicant_id, stage)
    # are all strings. Neither section fixes the demo applicant_id text, so the strongest
    # requirement-backed check is: a str whose stripped value is not "".
    store, rs = ApplicationStore(), RankingStore()
    seed_demo(store, rs)
    apps = [a for p in DEMO_EXPECTED for a in store.list_for_posting(p)]
    assert len(apps) == 13  # plan table: 2 + 3 + 1 + 2 + 2 + 3 + 0 applications
    for a in apps:
        assert isinstance(a.applicant_id, str), a.application_id
        assert a.applicant_id.strip() != "", a.application_id


_DEMO_SCRIPT = """
import json
from fastapi.testclient import TestClient
from jobsboard import api
c = TestClient(api.app)
out = {}
for p in %r:
    r = c.get(f"/postings/{p}/ranked")
    out[p] = [r.status_code, r.json()]
out["pipeline-ac8"] = c.get("/postings/demo-ac8/pipeline").json()["stages"]
print(json.dumps(out))
"""


def _run_demo_app(env_value: str | None) -> dict:
    # Imports api.py in a fresh interpreter so the JOBSBOARD_DEMO hook (D13) runs for real.
    env = {k: v for k, v in os.environ.items() if k != "JOBSBOARD_DEMO"}
    if env_value is not None:
        env["JOBSBOARD_DEMO"] = env_value
    env["PYTHONPATH"] = str(REPO / "src")
    proc = subprocess.run(
        [sys.executable, "-c", _DEMO_SCRIPT % list(DEMO_EXPECTED)],
        capture_output=True, text=True, env=env, cwd=REPO, timeout=60,
    )
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout.strip().splitlines()[-1])


def test_d13_demo_env_1_serves_plan_table_over_http():
    out = _run_demo_app("1")
    for posting_id, rows in DEMO_EXPECTED.items():
        expected_json = [
            {"application_id": a, "fit_score": f, "meets_minimum": m, "flag": fl, "missing_required": list(mr)}
            for a, f, m, fl, mr in rows
        ]
        assert out[posting_id] == [200, expected_json], posting_id
    assert out["pipeline-ac8"] == {"Applied": ["demo-ac8-b"], "Screened": [], "Interview": [], "Offer": [],
                                   "Rejected": []}


def test_d13_demo_env_not_exactly_1_does_not_seed():
    # D13: the seed runs only when JOBSBOARD_DEMO is exactly "1"; "true" seeds nothing,
    # so every demo posting has no requirements and returns 404.
    out = _run_demo_app("true")
    for posting_id in DEMO_EXPECTED:
        assert out[posting_id] == [404, {"detail": {"error": "posting_not_found"}}], posting_id
