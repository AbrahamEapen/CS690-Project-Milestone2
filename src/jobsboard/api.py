"""S-1 HTTP API (docs/design/S-1.md §4)."""
from __future__ import annotations

from dataclasses import asdict

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, StrictStr, field_validator

from jobsboard.pipeline import (
    Application,
    ApplicationNotFound,
    ApplicationStore,
    InvalidTransition,
    Stage,
    move_stage,
)
from jobsboard.ranking import rank_applicants
from jobsboard.ranking_store import PostingNotFound, RankingStore

app = FastAPI(title="Internal Jobs Board")
store = ApplicationStore()  # module-level, in-memory (S-1.md D3)
ranking_store = RankingStore()  # module-level, in-memory (S-3.md D5, D12)


class CreateApplicationBody(BaseModel):
    applicant_id: StrictStr

    @field_validator("applicant_id")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("applicant_id must not be empty")  # S-1.md §4, §5
        return v


class MoveStageBody(BaseModel):
    to_stage: Stage


@app.exception_handler(ApplicationNotFound)
def _not_found(_: Request, exc: ApplicationNotFound) -> JSONResponse:
    # S-1.md §4: unknown application id returns 404 and changes nothing (R4).
    return JSONResponse(
        status_code=404,
        content={"detail": {"error": "application_not_found", "application_id": exc.application_id}},
    )


@app.exception_handler(InvalidTransition)
def _invalid_transition(_: Request, exc: InvalidTransition) -> JSONResponse:
    # S-1.md R2 and §4: a refused move returns 409 naming both stages.
    return JSONResponse(
        status_code=409,
        content={"detail": {
            "error": "invalid_transition",
            "from_stage": exc.from_stage.value,
            "to_stage": exc.to_stage.value,
        }},
    )


@app.exception_handler(PostingNotFound)
def _posting_not_found(_: Request, exc: PostingNotFound) -> JSONResponse:
    # S-3.md section 4 and D12: 404 exactly when no requirements are set for the posting.
    return JSONResponse(status_code=404, content={"detail": {"error": "posting_not_found"}})


def _to_json(a: Application) -> dict:
    d = asdict(a)
    d["stage"] = a.stage.value
    return d


@app.post("/postings/{posting_id}/applications", status_code=201)
def create_application(posting_id: str, body: CreateApplicationBody) -> dict:
    return _to_json(store.create(posting_id, body.applicant_id))


@app.post("/applications/{application_id}/stage")
def change_stage(application_id: str, body: MoveStageBody) -> dict:
    return _to_json(move_stage(store, application_id, body.to_stage))


@app.get("/postings/{posting_id}/pipeline")
def pipeline(posting_id: str) -> dict:
    stages: dict[str, list[str]] = {s.value: [] for s in Stage}
    for a in store.list_for_posting(posting_id):
        stages[a.stage.value].append(a.application_id)
    return {"posting_id": posting_id, "stages": stages}


@app.get("/postings/{posting_id}/ranked")
def ranked(posting_id: str) -> list[dict]:
    # S-3.md section 4, D12: reads the ranking store and S-1 data only, so no stage changes (R6).
    required, candidates = ranking_store.candidates_for_posting(posting_id, store.list_for_posting(posting_id))
    return [asdict(e) for e in rank_applicants(required, candidates)]
