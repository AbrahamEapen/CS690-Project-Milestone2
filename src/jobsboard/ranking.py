"""S-3 ranked applicants with a minimum flag (docs/design/S-3.md)."""
from __future__ import annotations

from collections.abc import Iterable
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


def _validate_fit_score(application_id: str, fit_score: object) -> None:
    # Section 5, D3: a plain int from FIT_SCORE_MIN to FIT_SCORE_MAX inclusive; bool, float,
    # str and None are rejected, and out-of-range scores are rejected, not clamped.
    if type(fit_score) is not int or not FIT_SCORE_MIN <= fit_score <= FIT_SCORE_MAX:
        raise InvalidFitScore(application_id, fit_score)


def _validate_skills(skills: object) -> list[str]:
    # D10: skills given as a single str (including "") are rejected with that str.
    if isinstance(skills, str):
        raise InvalidSkill(skills)
    items = list(skills)  # D10: any iterable is accepted; read it once.
    # D10 pass 1: non-str skills, in sorted(key=repr) order.
    non_str = sorted((s for s in items if not isinstance(s, str)), key=repr)
    if non_str:
        raise InvalidSkill(non_str[0])
    # D10 pass 2 (section 5): str skills blank after strip(), in sorted() order; raw value kept.
    blank = sorted(s for s in items if not s.strip())
    if blank:
        raise InvalidSkill(blank[0])
    return items


def _normalize(skill: str) -> str:
    # R1: skills match when equal after strip() and casefold().
    return skill.strip().casefold()


def _spelling_order(spelling: str) -> tuple[str, str]:
    # Section 5 and D1: sort by (casefold(), spelling).
    return (spelling.casefold(), spelling)


def _skill_key(skill: str) -> str | frozenset[str]:
    # R1, D7: skills match when their normalized forms are equal or in the same
    # SKILL_SYNONYMS group; the group itself is the key, so matching works both ways.
    n = _normalize(skill)
    for group in SKILL_SYNONYMS:
        if n in group:
            return group
    return n


def _missing_required(required_skills: Iterable[str], skills: Iterable[str]) -> tuple[str, ...]:
    have = {_skill_key(s) for s in skills}
    # D1: required skills with the same key count as one requirement.
    requirements: dict[str | frozenset[str], list[str]] = {}
    for r in required_skills:
        requirements.setdefault(_skill_key(r), []).append(r.strip())
    # D1: a missing requirement shows the posting spelling that sorts first;
    # section 5: missing_required is sorted by (casefold(), spelling).
    missing = [min(spellings, key=_spelling_order) for key, spellings in requirements.items() if key not in have]
    return tuple(sorted(missing, key=_spelling_order))


def rank_applicants(required_skills: frozenset[str], candidates: list[Candidate]) -> list[RankedEntry]:
    # D3, D10: validate all input before ranking, raising the first problem in this order:
    # required skills, then each candidate in list order (duplicate ID, fit score, skills).
    required = _validate_skills(required_skills)
    checked: list[tuple[Candidate, list[str]]] = []
    seen: set[str] = set()
    for c in list(candidates):
        if c.application_id in seen:  # D3: exact string match
            raise DuplicateApplication(c.application_id)
        seen.add(c.application_id)
        _validate_fit_score(c.application_id, c.fit_score)
        checked.append((c, _validate_skills(c.skills)))

    entries = []
    for c, skills in checked:
        missing = _missing_required(required, skills)
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
