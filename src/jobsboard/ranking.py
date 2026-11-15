"""S-3 ranked applicants with a minimum flag (docs/design/S-3.md)."""
from __future__ import annotations

from dataclasses import dataclass

# Named settings (S-3.md section 8 table, D9).
FLAG_TEXT = "Does not meet minimum"
FIT_SCORE_MIN = 0
FIT_SCORE_MAX = 100
SKILL_SYNONYMS: tuple[frozenset[str], ...] = (
    frozenset({"postgres", "postgresql"}),
    frozenset({"word", "microsoft word"}),
)


@dataclass(frozen=True)
class Candidate:
    application_id: str
    skills: frozenset[str]
    fit_score: int


@dataclass(frozen=True)
class RankedEntry:
    application_id: str
    fit_score: int
    meets_minimum: bool
    flag: str | None
    missing_required: tuple[str, ...]


class InvalidFitScore(ValueError):
    def __init__(self, application_id: str, fit_score: object) -> None:
        super().__init__(f"invalid fit score for {application_id}: {fit_score!r}")
        self.application_id = application_id
        self.fit_score = fit_score


class DuplicateApplication(ValueError):
    def __init__(self, application_id: str) -> None:
        super().__init__(f"duplicate application: {application_id}")
        self.application_id = application_id


class InvalidSkill(ValueError):
    def __init__(self, skill: object) -> None:
        super().__init__(f"invalid skill: {skill!r}")
        self.skill = skill


def _normalize(skill: str) -> str:
    # R1: skills match when equal after strip() and casefold().
    return skill.strip().casefold()


def _missing_required(required_skills: frozenset[str], skills: frozenset[str]) -> tuple[str, ...]:
    # Section 5: each unmatched required skill's trimmed spelling, sorted by (casefold(), spelling).
    have = {_normalize(s) for s in skills}
    missing = {r.strip() for r in required_skills if _normalize(r) not in have}
    return tuple(sorted(missing, key=lambda s: (s.casefold(), s)))


def rank_applicants(required_skills: frozenset[str], candidates: list[Candidate]) -> list[RankedEntry]:
    entries = []
    for c in candidates:
        missing = _missing_required(required_skills, c.skills)
        meets = not missing  # R1
        entries.append(
            RankedEntry(
                application_id=c.application_id,
                fit_score=c.fit_score,
                meets_minimum=meets,
                flag=None if meets else FLAG_TEXT,  # R2
                missing_required=missing,
            )
        )
    # R3: qualified entries first; R4: fit_score descending within each group;
    # D2: equal fit_score in ascending application_id order (plain string order).
    return sorted(entries, key=lambda e: (not e.meets_minimum, -e.fit_score, e.application_id))
