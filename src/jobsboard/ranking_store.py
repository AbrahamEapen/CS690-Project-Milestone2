"""S-3 ranking store: the in-memory data module (docs/design/S-3.md D5, D11)."""
from __future__ import annotations

from collections.abc import Iterable

from jobsboard.pipeline import Application
from jobsboard.ranking import Candidate


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
        # D11: overwrites earlier values. Validation on set comes in Task 7.
        self._requirements[posting_id] = frozenset(skills)

    def set_profile(self, application_id: str, skills: Iterable[str], fit_score: int) -> None:
        # D11: keyed by application_id only; overwrites earlier values. Validation comes in Task 7.
        self._profiles[application_id] = Candidate(
            application_id=application_id, skills=frozenset(skills), fit_score=fit_score
        )

    def candidates_for_posting(
        self, posting_id: str, applications: Iterable[Application]
    ) -> tuple[frozenset[str], list[Candidate]]:
        # D12: unknown posting means no requirements set for it.
        if posting_id not in self._requirements:
            raise PostingNotFound(posting_id)
        # D8, D11: keep applications for this posting that have a profile, in the order given.
        # The Rejected filter comes in Task 6.
        candidates = [
            self._profiles[a.application_id]
            for a in applications
            if a.posting_id == posting_id and a.application_id in self._profiles
        ]
        return self._requirements[posting_id], candidates
