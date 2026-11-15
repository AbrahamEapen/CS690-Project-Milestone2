# Internal Jobs Board Portal — CS 690 Project, Milestone 2

An internal jobs board for mid-size companies. HR recruiters post roles, employees apply, and recruiters move each applicant through a status pipeline (Applied → Screened → Interview → Offer, or Rejected). Recruiters will later see applicants ranked by fit against the job description.

Team: Ketan Verma, Aditya Pothuri, Abraham Eapen.

Milestone 1 built S-1 (status pipeline). **Milestone 2 builds S-3 (ranked applicants with a minimum flag)**; see `MILESTONE2.md`. Agent instructions are in `AGENTS.md` (Claude Code reads it through `CLAUDE.md`).

## Requirements

- Python 3.11 or later (developed on 3.12)
- Dependencies pinned in `requirements.txt` (FastAPI, httpx, pytest, uvicorn, pytest-cov, Hypothesis, mutmut)
- Mutation testing (mutmut) runs on Linux and macOS; on Windows use WSL

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run all the tests (one command, with the coverage gate)

```bash
python -m pytest --cov=jobsboard --cov-branch --cov-report=term-missing --cov-fail-under=80
```

The command fails if line coverage of `src/jobsboard` drops below 80 percent. `python -m pytest -q` runs the same tests without coverage.

## Run the API locally (optional)

```bash
uvicorn jobsboard.api:app --app-dir src --reload
```

Then open `http://127.0.0.1:8000/docs`.

## Repository map

| Path | What it holds | Deliverable |
| --- | --- | --- |
| `docs/proposal_followup.md` | Approval items and scope changes since the proposal | 1 |
| `docs/interviews/` | Interview questions, raw notes INT-01 to INT-05, participation table, compliments and predictions, lesson learned | 2 |
| `evidence/evidence_log.md` | E, A, and Q evidence log | 3 |
| `backlog/backlog.md` | Stories S-1 to S-14, evidence trace, INVEST, AC-1 to AC-20, ranking and cut line | 4 |
| `docs/design/` | Design docs `S-1.md` and `S-3.md`, gap-check replies and adjudication | 5 |
| `docs/plans/S-1-plan.md` | Agent-written build plan for S-1 | 6c |
| `src/jobsboard/` | Application code | 6d |
| `tests/` | Acceptance tests (AC ID in each test name) | 6b |
| `traceability/traceability.csv` | Evidence → story → AC → test | 7 |
| `LEDGER.md`, `prompts/` | Provenance ledger and every prompt it references | 8 |
| `report/REPORT.md` | Source for the submitted PDF | all |
| `AGENTS.md` | Standing instructions for the AI coding tool | 6a |
