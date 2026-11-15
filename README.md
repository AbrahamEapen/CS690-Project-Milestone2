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
python -m pytest --cov=jobsboard.ranking --cov=jobsboard.ranking_store --cov=jobsboard.api --cov-branch --cov-report=term-missing --cov-fail-under=80
```

The command fails if coverage of the S-3 story code (`ranking.py`, `ranking_store.py`, `api.py`) drops below 80 percent; the threshold is also set in `pyproject.toml`. `python -m pytest -q` runs the same tests without coverage.

## Run the API locally (optional)

```bash
uvicorn jobsboard.api:app --app-dir src --reload
```

Then open `http://127.0.0.1:8000/docs`.

## Try the story (S-3: ranked applicants with a minimum flag)

Start the app with the demo data (in-memory; it is seeded only when `JOBSBOARD_DEMO` is exactly `1`):

```bash
JOBSBOARD_DEMO=1 uvicorn jobsboard.api:app --app-dir src
```

Then open each URL in a browser (or with `curl`). Each demo posting replays one acceptance criterion. Application IDs are `demo-acN-x`, and every list is in ranked order.

| AC | Open | What it shows |
| --- | --- | --- |
| AC-6 | `http://127.0.0.1:8000/postings/demo-ac6/ranked` | The posting requires Java and kdb+. `demo-ac6-a` (both skills, score 40) is listed above `demo-ac6-b` (Java only, score 90). B is flagged "Does not meet minimum" and missing `["kdb+"]`; A has no flag. |
| AC-7 | `http://127.0.0.1:8000/postings/demo-ac7/ranked` | All three have Java. The order is `demo-ac7-b` (80), `demo-ac7-c` (70), `demo-ac7-a` (55), with no flags. |
| AC-8 | `http://127.0.0.1:8000/postings/demo-ac8/ranked`, then `http://127.0.0.1:8000/postings/demo-ac8/pipeline` | `demo-ac8-b` (Java only) is still listed, flagged "Does not meet minimum". The pipeline still shows it under Applied: ranking never changes a stage. |
| AC-21 | `http://127.0.0.1:8000/postings/demo-ac21/ranked` | The posting requires PostgreSQL. `demo-ac21-a` (Postgres, 60) meets it through the synonym table and is listed first. `demo-ac21-b` (MySQL, 90) is flagged, missing `["PostgreSQL"]`. |
| AC-22 | `http://127.0.0.1:8000/postings/demo-ac22/ranked` | Both score 70 and have Java. `demo-ac22-a` is listed before `demo-ac22-b` (equal scores in ascending application ID order), with no flags. |
| AC-23 | `http://127.0.0.1:8000/postings/demo-ac23/ranked` | Only `demo-ac23-x` (score 50, no flag). `demo-ac23-y` was moved to Rejected and `demo-ac23-z` has no fit score yet, so both are left out. |
| Empty state | `http://127.0.0.1:8000/postings/demo-empty/ranked` | The posting has requirements but no applications, so the response is `200 []`. |
| Error state | `http://127.0.0.1:8000/postings/no-such-posting/ranked` | No requirements are set for this posting, so the response is `404 {"detail": {"error": "posting_not_found"}}`. |

Without `JOBSBOARD_DEMO=1`, nothing is seeded and every `demo-` posting returns 404.

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
