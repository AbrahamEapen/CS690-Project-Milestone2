# AGENTS.md — standing instructions for AI coding tools

These rules apply to every AI coding session in this repository. Claude Code reads them through `CLAUDE.md`.

## Stack
- Python 3.12 (3.11+ supported). FastAPI for HTTP; dataclasses and Enums for the domain.
- Tests: pytest with FastAPI `TestClient`; Hypothesis for properties; pytest-cov; mutmut.
- Story data stays in memory behind one data module (`src/jobsboard/ranking_store.py` for S-3). No database, network or LLM calls.

## Commands (each checked on a fresh clone)
```bash
python3 -m venv .venv && source .venv/bin/activate      # install
python -m pip install -r requirements.txt
JOBSBOARD_DEMO=1 uvicorn jobsboard.api:app --app-dir src # run the app (http://127.0.0.1:8000/docs)
python -m pytest --cov=jobsboard --cov-branch --cov-report=term-missing --cov-fail-under=80   # test + coverage gate
mutmut run && mutmut results                             # mutation testing (Linux/WSL)
```
`python -m pytest -q` runs the tests without the coverage gate. Run the full test command before reporting any task as done, and report its exact output.

## Folder layout
- `src/jobsboard/` — application code. S-1: `pipeline.py`, `api.py`. S-3: `ranking.py`, `ranking_store.py`, and the `/ranked` route in `api.py`.
- `tests/acceptance/` — locked acceptance tests, one per AC. **Read only.**
- `tests/unit/`, `tests/integration/`, `tests/property/` — tests you may add, through the `test-writer` subagent.
- `docs/design/` — design docs (`S-1.md`, `S-3.md`); the source of truth for behavior.
- `docs/plans/` — build plans (`S-3-plan.md`). `backlog/backlog.md` — stories and AC IDs.
- `evidence/` — tool output and interview evidence. `prompts/` — every prompt the ledger cites.
- `agent/`, `scripts/` — headless review schema and script. `.claude/agents/` — subagents.

## Workflow rules
1. **Show a plan and wait.** Before editing any file, list the files you will change and what changes in each, then stop until a human team member approves.
2. One bounded task at a time; a task implements one acceptance criterion from `docs/design/S-3.md`.
3. Change only the files the task prompt names. Stop when the check it names passes.
4. If the design doc does not answer something, **stop and ask**. Never invent a value for a named setting or a decision in section 8.

## Testing rules
- Tests come from the acceptance criteria and the design doc, never from the code. Expected values are worked out from the criterion, not from running the code.
- Every test names its AC ID (or the rule or edge case it checks) in its name or a comment.
- Never edit, delete, skip or weaken a test in `tests/acceptance/` to make it pass. If you think one is wrong, stop and say why; the team changes design doc, then criterion, then test, by hand.
- Run the test command before you report a task as done.

## Git and ledger rules
- One task per commit. The message names the task number and AC ID, e.g. `task 3: tie order (AC-22)`.
- Never push. Never use `rm -rf`. Never read `.env`.
- Every agent task gets one entry in `LEDGER.md` (seven fields; name the subagent in `tool`), and its prompt is saved in `prompts/`.

## Files and folders you must not change
- `tests/acceptance/` (also blocked by the permission rules in `.claude/settings.json`).
- `docs/design/`, `backlog/`, `evidence/`, `docs/interviews/` — owned by the team.
- `LEDGER.md`, `prompts/`, `AGENTS.md`, `CLAUDE.md`, `.claude/` — the team writes these.
- `requirements.txt` — ask before adding a dependency.

## Code conventions
- Type hints on every parameter and return value.
- Domain errors are exception classes in the domain module; the API maps them to the status codes and JSON bodies in the design doc.
