"""S-3 ranking store: the in-memory data module (docs/design/S-3.md D5, D11)."""
from __future__ import annotations

from collections.abc import Iterable

from jobsboard.pipeline import Application, Stage
from jobsboard.ranking import Candidate, _validate_fit_score, _validate_skills


class PostingNotFound(ValueError):
    def __init__(self, posting_id: str) -> None:
        super().__init__(f"posting not found: {posting_id}")
        self.posting_id = posting_id


class RankingStore:
    """Posting requirements and applicant profiles, in memory until S-4 (D5)."""

    def __init__(self) -> None:
        self._requirements: dict[str, frozenset[str]] = {}
        self._profiles: dict[str, Candidate] = {}

    def set_requirements(self, posting_id: str, skills: Iterable[str]) -> None:
        # D11: validate on set with the same errors as rank_applicants, then overwrite.
        # Nothing is written when validation raises, so an earlier value is kept.
        validated = _validate_skills(skills)
        self._requirements[posting_id] = frozenset(validated)

    def set_profile(self, application_id: str, skills: Iterable[str], fit_score: int) -> None:
        # D11: keyed by application_id only; fit_score is checked before skills (D10 order);
        # nothing is written when validation raises, so an earlier profile is kept.
        _validate_fit_score(application_id, fit_score)
        validated = _validate_skills(skills)
        self._profiles[application_id] = Candidate(
            application_id=application_id, skills=frozenset(validated), fit_score=fit_score
        )

    def candidates_for_posting(
        self, posting_id: str, applications: Iterable[Application]
    ) -> tuple[frozenset[str], list[Candidate]]:
        # D12: unknown posting means no requirements set for it.
        if posting_id not in self._requirements:
            raise PostingNotFound(posting_id)
        # R7, D8, D11: keep applications for this posting that have a profile and are not
        # at stage Rejected, in the order given.
        candidates = [
            self._profiles[a.application_id]
            for a in applications
            if a.posting_id == posting_id
            and a.application_id in self._profiles
            and a.stage is not Stage.REJECTED
        ]
        return self._requirements[posting_id], candidates
