"""Property tests for S-3 rules R3 to R6 (Deliverable 5c), from docs/design/S-3.md section 6.

Each property checks a relation that must hold for every valid input. None of them sorts or
recomputes the expected order the way the code does.
"""
from collections import Counter

from hypothesis import given, settings
from hypothesis import strategies as st

from jobsboard.pipeline import ApplicationStore, Stage, move_stage
from jobsboard.ranking import Candidate, rank_applicants
from jobsboard.ranking_store import RankingStore

# Small pool with case, outer-space and synonym variants (R1, D1, D7), plus skills in no group.
SKILL_POOL = [
    "Java", "java", " JAVA ", "kdb+", "KDB+",
    "Postgres", "postgres", "PostgreSQL", " postgresql ",
    "Word", "microsoft word", "Microsoft Word ",
    "MySQL", "Python",
]

skill_sets = st.frozensets(st.sampled_from(SKILL_POOL), max_size=5)
fit_scores = st.integers(min_value=0, max_value=100)  # section 5, inclusive
app_ids = st.text(alphabet="abcAB01-", min_size=1, max_size=4)


@st.composite
def ranking_inputs(draw):
    required = draw(skill_sets)
    ids = draw(st.lists(app_ids, unique=True, max_size=12))
    candidates = [Candidate(i, draw(skill_sets), draw(fit_scores)) for i in ids]
    return required, candidates


@given(ranking_inputs())
def test_r3_no_flagged_entry_before_an_unflagged_one(data):
    # R3 (invariant): no entry with meets_minimum False appears before one with it True.
    required, candidates = data
    ranked = rank_applicants(required, candidates)
    seen_flagged = False
    for entry in ranked:
        if not entry.meets_minimum:
            seen_flagged = True
        else:
            assert not seen_flagged, "unflagged entry after a flagged one"


@given(ranking_inputs())
def test_r4_within_group_fit_never_increases_and_ties_ascend_by_id(data):
    # R4 (order) with D2: within a group, adjacent entries never increase in fit_score, and
    # equal fit_score entries are in ascending application_id order (plain string order).
    required, candidates = data
    ranked = rank_applicants(required, candidates)
    for prev, nxt in zip(ranked, ranked[1:]):
        if prev.meets_minimum != nxt.meets_minimum:
            continue  # group boundary; R3 covers it
        assert prev.fit_score >= nxt.fit_score
        if prev.fit_score == nxt.fit_score:
            assert prev.application_id < nxt.application_id


@given(ranking_inputs())
def test_r5_output_ids_are_input_ids_each_exactly_once(data):
    # R5 (no one dropped): every input application_id appears exactly once, and no other ID.
    # Also each entry carries its own candidate's fit_score (nothing swapped or invented).
    required, candidates = data
    ranked = rank_applicants(required, candidates)
    assert Counter(e.application_id for e in ranked) == Counter(c.application_id for c in candidates)
    score_by_id = {c.application_id: c.fit_score for c in candidates}
    assert all(e.fit_score == score_by_id[e.application_id] for e in ranked)


@given(ranking_inputs())
def test_r6_input_list_unchanged(data):
    # R6 (no side effects): the input list keeps the same Candidate objects in the same order,
    # and the required set is unchanged.
    required, candidates = data
    snapshot = list(candidates)
    snapshot_values = [(c.application_id, c.skills, c.fit_score) for c in candidates]
    required_before = frozenset(required)
    rank_applicants(required, candidates)
    assert len(candidates) == len(snapshot)
    assert all(a is b for a, b in zip(candidates, snapshot))
    assert [(c.application_id, c.skills, c.fit_score) for c in candidates] == snapshot_values
    assert required == required_before


# Paths from Applied to each stage along S-1 R1 transitions.
_PATHS = {
    Stage.APPLIED: [],
    Stage.SCREENED: [Stage.SCREENED],
    Stage.INTERVIEW: [Stage.SCREENED, Stage.INTERVIEW],
    Stage.OFFER: [Stage.SCREENED, Stage.INTERVIEW, Stage.OFFER],
    Stage.REJECTED: [Stage.REJECTED],
}


@settings(max_examples=50)
@given(
    required=skill_sets,
    apps=st.lists(
        st.tuples(st.sampled_from(list(Stage)), st.booleans(), skill_sets, fit_scores),
        max_size=8,
    ),
)
def test_r6_ranking_through_store_leaves_every_s1_stage_unchanged(required, apps):
    # R6 (no side effects): fetching candidates (D11) and ranking them changes no S-1 stage,
    # including Rejected and unscored applications that are filtered out (D8).
    store = ApplicationStore()
    rs = RankingStore()
    rs.set_requirements("P", required)
    for n, (stage, has_profile, skills, score) in enumerate(apps):
        app = store.create("P", f"applicant-{n}")
        for to in _PATHS[stage]:
            move_stage(store, app.application_id, to)
        if has_profile:
            rs.set_profile(app.application_id, skills, score)
    before = [(a.application_id, a.stage) for a in store.list_for_posting("P")]

    listed = store.list_for_posting("P")
    listed_copy = list(listed)
    reqs, cands = rs.candidates_for_posting("P", listed)
    rank_applicants(reqs, cands)

    assert [(a.application_id, a.stage) for a in store.list_for_posting("P")] == before
    assert listed == listed_copy
