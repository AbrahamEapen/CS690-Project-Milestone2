# Contribution Statement: Project Milestone 2

**Name:** Abraham Eapen, QA & DevOps Lead
**Team:** Internal Jobs Board Portal (Ketan Verma, Aditya Pothuri, Abraham Eapen)

## 1. Personal authorship

- **Agent configuration.** I wrote `AGENTS.md`, `CLAUDE.md`, `.claude/settings.json`, `.claude/agents/test-writer.md` and `.claude/agents/reviewer.md` by hand. The agent did not edit them (commit `0bf7f63`, LEDGER entry 28).
- **Test lock.** I decided when to lock the tests and approved the deny rule `Edit(./tests/acceptance/**)`, which the agent added (`9fe0b20`, entry 31); I pushed the `m2-tests-locked` tag.
- **Expected values.** I recomputed all six acceptance-test expected values by hand (LEDGER entry 29).
- **Reflection.** I wrote the content of the reflection in `MILESTONE2.md`; the agent polished the wording (`e880e3a`).
- **Decisions.** I made each of the following decisions; the agent typed them into the docs:
  - open questions OQ-1 to OQ-4 (`a0710e9`, entry 26);
  - the answers to the gap check (`e44da99`, entry 27);
  - D10 two-pass skill validation and D13 `_put` (`3d6a2e9`, entry 33);
  - skills as bare strings (`622086e`, entry 40);
  - test-writer's questions Q1 to Q3 (`30ec446`, entry 43);
  - the demo-empty case (`bafab82`, entry 46);
  - when to tag `m2-green` (entry 48);
  - the coverage and mutation-testing scope (entry 50);
  - the triage of surviving mutants (entry 52).

## 2. AI-assisted authorship

I produced all of the following with Claude Code (Claude Opus 5.5, `claude-opus-5-5`). I reviewed each item and approved it before it was committed.

| Artifact | LEDGER entries |
| --- | --- |
| Milestone 2 repo setup, design-doc decisions, second gap check | 25–27 |
| Fresh-clone check and README test command | 28 |
| Test audit and AC-21 to AC-23 tests (test-writer subagent) | 29 |
| AC-8 test fix (my choice of fix; the agent typed it) | 30 |
| Red run, test lock and permission-denied proof | 31, 32 |
| Build plan and its corrections | 34 |
| Tasks 1–6 (`9223160`, `d569d92`, `8464a89`, `4ac171e`, `d3b2641`, `969ad37`) | 35–39, 42 |
| Review delegated to the reviewer subagent | 41 |
| Validation tests (test-writer subagent) and Task 7b | 44, 45 |
| Task 8 demo; green run and `m2-green` tag | 47, 48 |
| Refactor (`e6270d0`) | 49 |
| Tests 5a–5c (test-writer subagent); coverage and mutation runs; mutant-killing test | 51–54 |
| Headless review script and run | 55 |
| Screenshots | 56 |

## 3. Review

- **AI tool's work.**
  - **AC-8 test.** The test's stage check could never fail. I chose the fix, and it was made before the tests were locked (`e06026b`).
  - **Build plan.** I corrected the plan in two places: validation moved into its own task, and the reviewer step moved to Task 5 (`e7357bb`). I also rejected the plan's claim that `_put` was already a team decision.
  - **test-writer's counts.** test-writer counted 37 "DID NOT RAISE" failures where the run showed 39 (LEDGER entry 44).
  - **Reviewer findings.** Of the reviewer's four findings, I rejected three as work already planned for later tasks and accepted one (LEDGER entry 41).
  - **Headless review.** The headless review reported no findings, so I checked `subagent_stats` rather than accept an empty report (LEDGER entry 55).
  - **Reflection.** I accepted the four factual corrections flagged in the review of my reflection draft.
- **Teammates' work.** I did not review any of Ketan Verma's or Aditya Pothuri's work in Milestone 2.

I confirm that this statement is accurate, and that I can explain any part of the submission I am credited with.

*Wording polished with Claude Code (Claude Opus 5.5); content written by me.*

**Signature:** /s/ Abraham Eapen  **Date:** 2026-11-15
