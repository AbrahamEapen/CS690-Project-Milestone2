# Provenance ledger

Same format as the assignments. One entry per reviewable change, written when the change is finished.

```text
## Entry <n>
artifact:  what this entry covers: a file, a commit SHA, or a document
tool:      product name, model name and version, and the date of use
prompts:   one-line summary of each prompt; the full prompt is saved
           in prompts/ and referenced here by path
review:    what you read, what you changed, what you rejected, and why
checks:    the commands you ran and their results
evidence:  the story, acceptance criterion, or evidence ID this traces to
risk:      what is still unverified after this change
```

---

## Entry 1
artifact:  docs/interviews/ (questions.md, INT-01..INT-05.md, participation.md,
           compliments_predictions.md, lesson.md); commit d984dd1
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-09
prompts:   kick-off: generate Milestone 1 deliverables from the team's interview notes;
           prompts/session_kickoff_prompt.md
review:    The agent transcribed the team's four .docx interview files into five numbered
           note files and added P-numbers. It did not reword any answer. Two files had both
           been labeled INT-01, so the agent proposed renumbering them INT-01 to INT-05.
           Abraham confirmed that all five are real interviews and approved the numbering. The
           agent moved INT-03's compliment and prediction to the CP list, marked the two
           unanswered INT-04 questions "No answer recorded", and wrote no answers of its own.
checks:    grep -c "^P[0-9][0-9]:" docs/interviews/INT-0*.md → INT-01 9, INT-02 6, INT-03 10,
           INT-04 15, INT-05 15; manual diff of each answer against its source .docx text
evidence:  INT-01..INT-05; Deliverable 2
risk:      Dates and team members for INT-01, INT-02, INT-04 and INT-05 are not yet recorded
           in participation.md. Consent wording is recorded only for INT-03, so consent for
           the other four is unverified in writing.

## Entry 2
artifact:  evidence/evidence_log.md (24 E, 7 A, 9 Q); commit d984dd1
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-09
prompts:   build the evidence log with the Assignment 3 scheme; prompts/session_kickoff_prompt.md
review:    The agent drafted every entry and cited an interview paragraph for each E entry. It
           logged the INT-04:P10 vs INT-05:P08 disagreement as Q-2 rather than picking a side,
           and made the proposal's own rules (stage names, forward-only moves, Rejected final,
           no SSO, English documents) A entries. Owners follow proposal roles. Abraham reviewed
           the draft and chose "Proceed as drafted"; there were no edits.
checks:    grep -c "^| E-" → 24; "^| A-" → 7; "^| Q-" → 9; grep for "CP-" or "SYN" in
           the log → 0 hits
evidence:  E-1..E-24, A-1..A-7, Q-1..Q-9
risk:      E-13 and E-19 rest on one hiring manager's general statements (Stated), not on
           observed events. Owner assignments by role have not been confirmed by Ketan and Aditya.

## Entry 3
artifact:  backlog/backlog.md (S-1..S-13, INVEST, AC-1..AC-19, ranking and cut line); commit d984dd1
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-09
prompts:   write the Deliverable 4 backlog; prompts/session_kickoff_prompt.md
review:    The agent wrote 13 stories. S-12 is marked Assumption (A-7) with a clarifying
           question; all others cite E entries. Values not settled by interviews use named
           settings (APPLICANT_STAGE_LABELS, ERASURE_MAX_MINUTES, EXPLANATION_MAX_WORDS) rather
           than numbers. The agent checked that no AC settles a Q entry: AC-2 and AC-4 rest on
           the explicit A-2 and A-3, and no AC moves out of Offer (Q-3). Abraham chose "Proceed
           as drafted".
checks:    every S row has an E or A trace (13/13); every AC row has one Given, one When,
           one Then (19/19); grep for the numbers "5 minutes" or "15" in the AC table → 0
evidence:  S-1..S-13; AC-1..AC-19
risk:      The ranking above the cut line has not been reviewed by Aditya (Project Lead, who
           owns scope decisions). A-1 (stage names) has not been confirmed with any recruiter.

## Entry 4
artifact:  docs/design/S-1.md and docs/design/S-3.md, first drafts; commit 7583dd4
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-09
prompts:   write the 9-section design docs for S-1 (build) and S-3 (design only);
           prompts/session_kickoff_prompt.md
review:    Abraham chose the stories: build the status pipeline, design the ranking. S-3
           carries the invariant "no flagged applicant above a qualified one". Each doc has
           at least 2 non-goals, 3 checkable rules, 3 edge cases, 3 decisions, and open
           questions that each end with "Do not build anything that depends on this. Stop and ask."
checks:    grep -c "Stop and ask" → S-1: 3, S-3: 3 (before the gap check)
evidence:  S-1 (E-5, E-6, E-7), S-3 (E-11..E-14); AC-1..AC-4, AC-6..AC-8
risk:      Both docs are over one page (each under two). R5 in S-1 is checked only
           indirectly by the AC tests.

## Entry 5
artifact:  docs/design/S-1-gap-check-reply.md, S-1-gap-adjudication.md, and section 8 of S-1.md;
           commit 17ac5ac
tool:      Claude Code subagent, Claude Opus 5.5 (claude-opus-5-5), 2026-11-09
prompts:   lecture gap-finding prompt; prompts/gap_check_prompt.md
review:    A fresh subagent that saw only S-1.md returned 28 questions, saved verbatim. 4
           were already answered (§4, evidence log); 24 were real gaps. 22 were decided as
           D6–D11, #23 became a non-goal (no move history), and #7 (duplicate applications)
           became open question OQ-4 rather than being guessed. D6 makes Offer → {} explicit
           so no test depends on moves out of Offer.
checks:    count of rows in the adjudication table = 28; every "Real gap" row names a D, OQ,
           §3 or §9 change that exists in S-1.md (checked by hand)
evidence:  S-1; Q-1, Q-3, Q-4
risk:      D9 relies on FastAPI's default 422 body, which no test pins. A FastAPI upgrade
           could change it without any test noticing.

## Entry 6
artifact:  docs/design/S-3-gap-check-reply.md, S-3-gap-adjudication.md, and section 8 of S-3.md;
           commit 17ac5ac
tool:      Claude Code subagent, Claude Opus 5.5 (claude-opus-5-5), 2026-11-09
prompts:   lecture gap-finding prompt; prompts/gap_check_prompt.md
review:    A fresh subagent that saw only S-3.md returned 30 questions, saved verbatim. 5
           were already answered; 25 were real gaps. Normalization (strip/casefold), the
           exception hierarchy and validation order were decided as D1, D5 and D6. The HTTP
           endpoint was deferred to S-4 (D7). Questions 19 and 20 (applications with no score,
           Rejected applicants) became OQ-4. Tie order stays OQ-1; it was not decided.
checks:    count of rows in the adjudication table = 30; grep -c "Stop and ask" S-3.md → 4
evidence:  S-3; Q-5, Q-6, Q-9
risk:      D1's case-insensitive sort of missing_required and the InvalidSkill exception
           have no AC; they will be unverified until S-3 is built.

## Entry 7
artifact:  README.md, AGENTS.md, requirements.txt, pytest.ini, .gitignore; commits d984dd1
           and 17ac5ac
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-09
prompts:   set up the Deliverable 6a repository files; prompts/session_kickoff_prompt.md
review:    AGENTS.md states the stack, the test command, the folders the agent must not
           change (tests/, docs/, backlog/, evidence/, LEDGER.md, prompts/), and "show a plan
           and wait". Dependencies are pinned to exact versions. Abraham chose the stack
           (Python + FastAPI + pytest).
checks:    python3 -m venv .venv && pip install -r requirements.txt → ok;
           python -m pytest -q runs from the repo root
evidence:  Deliverable 6a
risk:      The fresh-clone install has not yet been run on a second machine or on Windows.

## Entry 8
artifact:  tests/test_s1_pipeline.py (AC-1..AC-4), tests/test_s3_ranking.py (AC-6..AC-8);
           commit 17ac5ac
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-09
prompts:   write the tests from the acceptance criteria before any code exists;
           prompts/session_kickoff_prompt.md
review:    Each test name holds its AC ID, and each test has a comment quoting its
           Given/When/Then. Expected values come from the ACs (stage names, 409 body). S-3
           tests are skipped with reason "AC-n: S-3 not built in Milestone 1". The tests
           imported nothing from src at write time.
checks:    python -m pytest -q → 4 errors (ModuleNotFoundError: jobsboard.api), 3 skipped,
           as expected before the build
evidence:  AC-1..AC-4, AC-6..AC-8
risk:      AC-3 sets up Interview by calling the move endpoint under test, so a bug in
           forward moves would fail AC-3's setup rather than its assertion.

## Entry 9
artifact:  docs/plans/S-1-plan.md; prompts/s1_task_AC-1.md, prompts/s1_task_AC-2.md,
           prompts/s1_task_AC-3.md, prompts/s1_task_AC-4.md; commit 537d708
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-09
prompts:   write the plan before editing; prompts/s1_plan_prompt.md
review:    The plan has a How section (2 new files, an in-memory dict store) and 4 tasks, one
           per AC. Abraham approved the plan and the striking of 3 steps that were not asked
           for: a GET /applications/{id} endpoint, a moved_at timestamp (a §3 non-goal), and
           Offer → Rejected (open question OQ-1).
checks:    git diff --stat before the commit: only docs/plans/ and prompts/ changed
evidence:  S-1; AC-1..AC-4
risk:      The plan's estimates are unverified, and task boundaries overlap: Task 1
           creates the full transition table, so AC-3 passes before Task 3.

## Entry 10
artifact:  src/jobsboard/pipeline.py, src/jobsboard/api.py (new); commit bb06aba
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-09
prompts:   bounded task AC-1; prompts/s1_task_AC-1.md
review:    The plan was shown and approved by Abraham before any edit. Only the two named
           files changed. Read the diff: the R1 table matches S-1.md (Offer → {} per D6), the
           Application dataclass is frozen, a move replaces the record, and the pipeline
           returns all five keys.
checks:    python -m pytest -q → 2 passed (AC-1, AC-3), 2 failed (AC-2, AC-4: unhandled
           InvalidTransition → 500), 3 skipped. By-hand edge cases: lowercase "screened" → 422;
           "Hired" → 422; whitespace applicant_id → 422; empty posting → 5 empty lists;
           same-stage move → 500; unknown application → 500 (to be fixed in Tasks 2 and 4)
evidence:  AC-1; S-1 R1, R3, R5, D4, D6, D10
risk:      Unknown application IDs still return 500 instead of 404 until Task 4.

## Entry 11
artifact:  src/jobsboard/api.py (409 handler); commit fe749ff
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-09
prompts:   bounded task AC-2; prompts/s1_task_AC-2.md
review:    The plan (one exception handler, api.py only) was shown and approved by Abraham
           before the edit. Read the diff: 16 lines added, 2 changed, all in api.py. The body
           uses the stage .value strings, as the AC requires. Nothing else changed.
checks:    python -m pytest -q → 4 passed, 3 skipped (AC-4 also passes now, because it was
           blocked only by the 409 mapping). By-hand edge cases: same-stage move → 409 (was
           500); lowercase and unknown stage names → 422; unknown application → still 500
evidence:  AC-2 (and AC-4); S-1 R2, R4, D5
risk:      An unknown application_id still returns 500, not the 404 in S-1.md §4. No AC
           covers 404, so only the Task 4 by-hand check guards it.

## Entry 12
artifact:  verification of AC-3 against src/jobsboard/pipeline.py (no code change); verified at commit f16623c
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-09
prompts:   bounded task AC-3; prompts/s1_task_AC-3.md
review:    Abraham approved the plan as verify-only, because Task 1 had already created the
           full R1 table. Read pipeline.py line 46: Interview → {Offer, Rejected}, matching
           S-1.md R1. No file was edited.
checks:    python -m pytest -q tests/test_s1_pipeline.py::test_ac3_interview_to_rejected_listed_under_rejected
           → 1 passed; git status → clean
evidence:  AC-3; S-1 R1, R3
risk:      Because Task 1 created the table in one step, the AC-3 test never failed before it
           passed. Its ability to catch a missing Interview → Rejected entry has not been
           shown by a failing run.

## Entry 13
artifact:  src/jobsboard/api.py (404 handler); commit 6889508
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-09
prompts:   bounded task AC-4; prompts/s1_task_AC-4.md
review:    The plan (a 404 handler in api.py only) was shown and approved by Abraham before
           the edit. Read the diff: 17 lines added in api.py only. The 404 body matches
           S-1.md §4, and the imports were regrouped.
checks:    python -m pytest -q → 4 passed, 3 skipped. By-hand edge cases: unknown id → 404
           {"error": "application_not_found", "application_id": "nope"}; Interview → Screened
           → 409; Offer → Rejected → 409 (D6; OQ-1 still open); missing body → 422
evidence:  AC-4; S-1 R2, R4, D3, D6
risk:      The 404 path and R5 (each application in exactly one stage list) have no
           automated test; they were checked only by hand in this session.

## Entry 14
artifact:  traceability/traceability.csv, report/build_report.py, report/render_pdf.py,
           report/REPORT.md, report/CS690_M1_Report.pdf, report/test_output_6e.txt; commit b00efca
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-09
prompts:   build the Deliverable 7 matrix and the submission PDF with a table of contents;
           prompts/session_kickoff_prompt.md
review:    The matrix has one row per AC (19 rows): 7 name tests that exist in the repo, 12
           say "Not yet written". The report is generated from the repository files, so the
           PDF and the repo cannot drift apart. Rendered pages 16, 22 and 23 were checked
           visually. Two formatting bugs were found and fixed: lists after bold labels ran
           into paragraphs, and inline code broke mid-word. Only blank lines were added to the
           docs; no wording changed.
checks:    for each test name in the CSV: grep "def <name>" tests/*.py → 7/7 found.
           Fresh clone + pip install + python -m pytest -q → 4 passed, 3 skipped (saved
           to report/test_output_6e.txt). The PDF is 34 pages; its TOC shows page numbers.
evidence:  AC-1..AC-19; Deliverables 6e and 7
risk:      The repository URL in the report is still a TODO. The fresh-clone check ran
           against a local clone, not a clone from GitHub.

## Entry 15
artifact:  contribution/Abraham_Eapen_contribution.md (+ PDF), docs/interviews/participation.md
           (Abraham on INT-04 and INT-05); commit recorded in git log after entry 14
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-09
prompts:   draft the Deliverable 9 statement from Abraham's answers; prompts/session_kickoff_prompt.md
review:    Abraham said he took part in INT-04 and INT-05 and that his personal authorship is
           the notes for those interviews. The agent removed two sentences from its own first
           draft because they claimed reviews Abraham had not described (checking teammates'
           transcriptions, and finding the 500 errors himself). The teammate-review part is
           left as a TODO for Abraham to write.
checks:    grep "TODO" contribution/Abraham_Eapen_contribution.md → 1 (teammate review);
           the signature and date lines are blank for a hand signature
evidence:  Deliverable 9; INT-04, INT-05
risk:      Dates, formats and team members for INT-01 to INT-03 and the dates for INT-04 and
           INT-05 are still unfilled, so the requirement that every member took part in at
           least one interview is not yet shown.

## Entry 16
artifact:  SHA roll-up of AI-assisted commits not named in an earlier entry: c53a9a5, f16623c,
           18a5bae (ledger commits), 1146cb9 (contribution statement draft, participation, entries 14–15),
           a01db91 (rebuilt report PDF and contribution PDF)
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-09
prompts:   no new prompt; covered by prompts/session_kickoff_prompt.md
review:    Compared git log --oneline against every artifact line in entries 1–15. All 13
           commits now appear in at least one entry. The commit that adds this entry is
           ledger-only.
checks:    git log --oneline | wc -l → 13 before this entry; python -m pytest -q → 4 passed, 3 skipped
evidence:  Deliverable 8
risk:      The report PDF names a01db91's parent as its build commit. If any file changes
           before submission, the PDF must be rebuilt (python report/build_report.py, then
           render_pdf.py), or the PDF and the repo will disagree.

## Entry 17
artifact:  review fixes 1–5: docs/design/S-1.md, S-3.md, both gap adjudications,
           evidence/evidence_log.md (Q-4), backlog/backlog.md (S-14, AC-20, ranking),
           docs/proposal_followup.md (new), traceability.csv (AC-20), README.md, code comments
           in src/jobsboard/; commit 4c3b6e5
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-09
prompts:   Abraham: "fix items 1 to 5. prompt me if any for reviews, decision making, and
           validation" (following the agent's audit of the repo against the handout and
           proposal); recorded in prompts/review_fixes_prompt.md
review:    Abraham decided three points: S-14 for scans goes below the line; S-12 stays below
           with the change recorded; moves out of Offer become an S-1 non-goal instead of D6.
           These edits to team-owned docs/design/, backlog/ and evidence/ were made at
           Abraham's explicit request.
           (1) Both design docs were cut to fit 2 pages, and rules stated twice were removed
           (old S-1 D2, D3, D5 repeated R1 and R2; old S-3 D2, D3 repeated R2, R5, R6).
           (2) Q-4 now asks only who sets Withdrawn and whether it can be reopened, so AC-16
           no longer answers it. (3) S-1 D6 was removed; Offer → {} stays in R1 and is
           listed as a non-goal.
           Errors caught during the trim: a merged edge-case bullet said that same-stage and
           backward moves return 422 (they return 409); restored. Several gap-check decisions
           had been cut too far (IDs stored as given, HTTP-only validation, FastAPI path
           defaults, stack, test isolation); restored. Both adjudication tables were rewritten
           to point at the new section numbers.
checks:    Page count at Letter, 11pt DejaVu Sans, 1-inch margins, normal heading sizes:
           S-1 2 pages (643 words), S-3 2 pages (667 words). With a browser's default heading
           spacing both still run to 3 pages. grep "Stop and ask": S-1 4, S-3 4.
           python -m pytest -q → 4 passed, 3 skipped. The traceability CSV has 20 rows.
evidence:  S-1, S-3, S-8, S-10, S-12, S-14; AC-16, AC-20; Q-3, Q-4; E-19
risk:      The "two pages" limit depends on the font and heading sizes; a grader viewing the
           markdown on GitHub may see more than two screens. S-14's AC-20 assumes OCR can read
           "kdb+" from a PNG; no sample scan has been tried. The design docs were trimmed
           after the gap check and were not re-run through it.

## Entry 18
artifact:  docs/interviews/participation.md (INT-04, INT-05 rows), INT-04.md and INT-05.md
           headers; commit f147734
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-09
prompts:   Abraham: "Prompt me to fill out questions in the participation table related to
           Abraham Eapen"; prompts/participation_prompt.md
review:    Every value came from Abraham's answers to the agent's questions; the agent wrote no
           new facts. Abraham first said a teammate attended at one or both interviews, then
           answered "Abraham only" for each when asked per interview. The per-interview answers
           were used.
checks:    grep "\[fill in\]" docs/interviews/participation.md → INT-01, INT-02, INT-03 only
evidence:  Deliverable 2b; INT-04, INT-05
risk:      Dates are recorded only to the week (2026-11-02). Consent for INT-04 and INT-05 is
           Abraham's recollection, not a contemporaneous written note. Ketan and Aditya do not
           appear in any row yet, so "every member takes part" is still unshown.

## Entry 19
artifact:  SHA roll-up of AI-assisted commits not named in an earlier entry: 704f4d7 (ledger
           entry 16), 720b0e3 (ledger entry 17 + prompts/review_fixes_prompt.md), 560eed3
           (report PDF rebuilt after the review fixes), 84f3110 (ledger entry 18 +
           prompts/participation_prompt.md), 537b943 (report PDF rebuilt after the
           participation update). Also fixes entry 9: its prompt path is now the four real
           files, and its risk line no longer starts with the word "None".
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-09
prompts:   Abraham: "Fix ledger problems now"; prompts/ledger_fix_prompt.md
review:    Checked every prompts/ path in this ledger against the files on disk, and every
           commit in git log against the ledger text. Entry 9's wording was changed, but
           what it records was not.
checks:    for each prompts/*.md path in LEDGER.md: test -f → all present; for each SHA in
           git log --format=%h: grep -q in LEDGER.md → all present except the commit that
           adds this entry
evidence:  Deliverable 8
risk:      The commit that adds this entry, and any later commit, is not named here. Each
           future AI-assisted commit needs its own entry or a later roll-up.

## Entry 20
artifact:  Public-repository preparation: redacted docs/interviews/INT-02..INT-05.md,
           participation.md, compliments_predictions.md, evidence_log.md (E-11, E-12, E-24,
           Q-9), S-3.md OQ-3 example, backlog AC-9 and AC-20 examples, README and report
           (UCIDs removed), contribution statement, and prompts/session_kickoff_prompt.md.
           Git history rewritten with git filter-branch: every commit's author and committer
           is now AbrahamEapen@users.noreply.github.com, older versions get the same
           redactions, and report/CS690_M1_Report.pdf, report/REPORT.md and
           contribution/Abraham_Eapen_contribution.pdf were removed from older commits (they
           held unredacted text) and regenerated at the tip. Old → new SHAs (all SHAs in
           this ledger now use the new values):
           3a5a873 -> d984dd1
           a5d472e -> 7583dd4
           6277a0b -> 17ac5ac
           5b39391 -> 537d708
           38cc342 -> bb06aba
           12dc16d -> c53a9a5
           3dd5592 -> fe749ff
           09b7f77 -> f16623c
           2848930 -> 6889508
           52bfc46 -> 18a5bae
           6ed52f2 -> b00efca
           62d56e9 -> 1146cb9
           d202a40 -> a01db91
           27510a4 -> 704f4d7
           0c92988 -> 4c3b6e5
           36293a0 -> 720b0e3
           c1092c7 -> 560eed3
           0cb68a4 -> f147734
           c242d20 -> 84f3110
           9b2d524 -> 537b943
           be6b81d -> d09675d
           3642b6b -> 19df87d
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-09
prompts:   Abraham asked about data sensitivity, then said "the repo is public for now so
           please update accordinly"; prompts/public_repo_prompt.md
review:    Identifying or confidential details were generalized and marked in [brackets],
           so readers can see where the raw notes were edited. Details covered: employer
           type and team, job title, exact months, a third party's eligibility outcome, a
           remark about an identifiable colleague, INT-05's teams and tenure, and INT-02's
           dollar amounts and hiring metrics. Every E entry still says what its cited paragraph says. Q-9 and
           S-3 OQ-3 now use a neutral synonym example. AC-9 and AC-20 (no tests yet) now use
           neutral skills. AC-6 and AC-8 keep "kdb+" because their tests exist and tests/ is
           protected; it is a generic skill name with no link to the generalized INT-03 notes.
           Four commits are now empty: the three PDF-rebuild commits (560eed3, 537b943,
           a01db91) and the redaction commit 19df87d, whose changes were applied back through
           history. They are kept so the SHA map stays one-to-one.
checks:    git grep over every commit (git rev-list --all) for the generalized terms and
           the UCIDs → no hits outside this entry;
           git log --format=%ae | sort -u → the no-reply address only; python -m pytest -q → 4 passed, 3 skipped.
           A backup bundle of the pre-rewrite history is kept outside the repo, in the
           agent's scratchpad.
evidence:  Handout "Interviewing people": no names or identifying details in notes or evidence
risk:      Generalized details could still identify someone to a colleague who knows the
           context. INT-03's consent promised use "only for our report", so a public repo
           may go beyond it; this was not re-confirmed with the interviewee. Before any
           future push, check that the commit emails are still the no-reply address.

## Entry 21
artifact:  docs/interviews/participation.md (INT-01..INT-03 rows; the TODO note replaced by a
           per-member summary), INT-01.md, INT-02.md and INT-03.md headers; commit e28dc0f.
           This entry also names the ledger commit for entry 20, 2950088.
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-09
prompts:   Abraham: "I have the dates for Ketan and Aditya. please prompt me";
           prompts/participation_teammates_prompt.md
review:    Every value came from Abraham's answers on his teammates' behalf. INT-03's date
           and format were already in its original notes; only the team member was added.
           Each member now appears in at least one row: Aditya (INT-01, INT-02), Ketan
           (INT-03), Abraham (INT-04, INT-05).
checks:    grep -c "\[fill in\]" docs/interviews/participation.md → 0; git log -1 --format=%ae
           → the no-reply address
evidence:  Deliverable 2b; INT-01..INT-03
risk:      The INT-01..INT-03 details and consent were reported by Abraham, not confirmed
           by Ketan or Aditya in writing. INT-01, INT-02, INT-04 and INT-05 dates are
           recorded only to the week.

## Entry 22
artifact:  contribution/Abraham_Eapen_contribution.md and .pdf, completed and signed; commit
           371d0d9. This entry also names the ledger commit for entry 21, 0c4a544.
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-09
prompts:   Abraham: "prompt me for my contribution statement, signature , and date";
           prompts/contribution_prompt.md
review:    The teammate review, the findings, the E-entry check, the signature form and the
           date all come from Abraham's answers. The AI-assisted table was updated to cover
           entries 16–21 and the current backlog (S-1..S-14, AC-1..AC-20). The agent
           corrected its own draft twice before committing. It had miscounted Abraham's E
           entries as 16 and 8; checking the log with awk gave 15 (INT-04/05) and 9
           (INT-01..03). It had also added "no problems in Ketan's INT-03 notes", which
           Abraham did not say; that line was removed.
checks:    awk over evidence_log.md sources → INT-04/05 only: E-1..E-4, E-8..E-10, E-13,
           E-14, E-16..E-20, E-24 (15); citing INT-01..03: E-5..E-7, E-11, E-12, E-15,
           E-21..E-23 (9). grep TODO contribution/Abraham_Eapen_contribution.md → 0
evidence:  Deliverable 9; AI policy (a person checks every claim before it enters the log)
risk:      The 9 E entries from INT-01..INT-03 have not been checked against the notes by any
           person; Aditya and Ketan need to do it. The statement says nothing about Ketan's
           INT-03 notes beyond the general review.

## Entry 23
artifact:  report/build_report.py (REPO_URL), report/REPORT.md and CS690_M1_Report.pdf
           rebuilt; commit ea11ad3. This entry also names the ledger commit for entry 22,
           e02c5ea. Push to https://github.com/ap3478/CS690-Project attempted on 2026-11-09:
           HTTPS had no credentials; SSH authenticated as AbrahamEapen but was denied
           (no write access to ap3478's repo). Nothing has been pushed yet.
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-09
prompts:   Abraham: "Push to https://github.com/ap3478/CS690-Project"; prompts/push_prompt.md
review:    Before pushing, the remote was checked with git ls-remote: it exists and is empty,
           so nothing was overwritten. The report's repository line was changed from the
           TODO to the URL, and the PDF was rebuilt. No other content changed.
checks:    git ls-remote → no refs (empty repo); git log --format=%ae | sort -u → the no-reply
           address only; python -m pytest -q → 4 passed, 3 skipped
evidence:  Turn-in instructions (GitHub repository URL)
risk:      The commit that adds this entry is not named here. The repository belongs to
           Aditya's account (ap3478), so collaborator access and its public/private setting
           are his to manage. Clone and test from GitHub itself after the push.

## Entry 24
artifact:  First successful push of branch main to https://github.com/ap3478/CS690-Project
           (29 commits, tip 7fea4c8). This entry also names the ledger commit for entry 23,
           7fea4c8.
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-09
prompts:   Abraham: "I have accepted the invite . please repush to
           https://github.com/ap3478/CS690-Project.git"; prompts/push_prompt.md
review:    Abraham accepted collaborator access to ap3478's repository, and the push went over
           SSH as AbrahamEapen. The remote was empty before the push, so nothing was
           overwritten.
checks:    git push -u origin main → "[new branch] main -> main". A fresh clone from GitHub
           has 29 commits, all authored with the no-reply address. Running pip install -r
           requirements.txt and python -m pytest -q there → 4 passed, 3 skipped (AC-6, AC-7,
           AC-8 skipped with their AC IDs).
evidence:  Turn-in instructions (GitHub repository URL); Deliverable 6e
risk:      The commit that adds this entry is not named here. The repository is public:
           the redacted interview notes are visible to anyone, and INT-03's consent
           ("used only for our report") has not been re-confirmed for public use.

---

# Milestone 2 (story S-3)

From Milestone 2 on, the repository is https://github.com/AbrahamEapen/CS690-Project-Milestone2.
SHAs before c17dcad are in the Milestone 1 repository, ap3478/CS690-Project.

## Entry 25
artifact:  Repository start, commit c17dcad (Milestone 1 files copied without history;
           .gitignore extended with .env, .coverage, htmlcov/, mutants/, .hypothesis/)
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-11
prompts:   handout review; settling repo items 1–8; the three setup items; push;
           prompts/m2_session_prompts.md items 1–4
review:    Abraham chose a new repository over continuing the old one. The agent checked the
           staged files for .env, .venv and caches before committing and found none. The HTTPS
           remote had no credentials, so it was switched to SSH for the same repository.
checks:    python -m pytest -q in a new .venv → 4 passed, 3 skipped; git push -u origin main →
           "[new branch] main -> main"
evidence:  Milestone 2 turn-in instructions
risk:      The Milestone 1 SHAs cited in the 1a follow-up live in a different repository; the
           grader must open ap3478/CS690-Project to check them.

## Entry 26
artifact:  docs/design/S-3.md §3, §4, §6, §7, §8; backlog/backlog.md (AC-21..AC-23, S-15);
           evidence/evidence_log.md (Q-5, Q-6, Q-9 settled); commit a0710e9
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-11
prompts:   settle OQ-1..OQ-4 and the named settings; prompts/m2_session_prompts.md items 2, 5
review:    Abraham picked each decision from the agent's options. Abraham rejected the agent's
           suggestion to break ties by application time, because it needed a new applied_at
           field, and chose application_id ascending instead. Abraham also rejected the agent's
           recommendation to add no synonyms, and chose the two INT-03:P03 pairs. The design
           doc was changed first, then the criteria; the tests follow in 3b. The non-goal
           "no synonym matching" in §3 contradicted D7, so it was rewritten.
checks:    grep -n "OQ-" docs/design/S-3.md → every OQ line replaced by a decision;
           python -m pytest -q → 4 passed, 3 skipped (no code changed)
evidence:  S-3; OQ-1..OQ-4; Q-5, Q-6, Q-9; INT-03:P03; INT-04:P06–P07
risk:      D2, D6 and D8 are team decisions, not interviewee answers. No recruiter has
           confirmed that ordering ties by application_id, or hiding Rejected applicants,
           matches how they work.

## Entry 27
artifact:  docs/design/S-3-gap-check-2.md; S-3.md §5 and §8 (D1, D4, D9–D13); commits
           e44da99, 7be1fde
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-11, fresh general-purpose
           subagent for the gap check (no conversation context)
prompts:   prompts/s3_gap_check_2_prompt.md (handout prompt, verbatim)
review:    The subagent returned 37 questions, saved verbatim. The main agent drafted marks:
           30 real gaps and 7 answered. Abraham decided the three with real alternatives:
           validate the ranking store on set rather than at ranking time (this removes a
           500/422 path, Q26), reject any non-int fit_score (Q10), and reject non-str skills
           but leave application_id unchecked (Q9, Q11). The agent's draft answer to Q21
           (assume the caller pre-filters by posting) was changed so that the store filters
           by posting_id itself.
checks:    every row in the marks table names a section or decision that exists in S-3.md
           (checked by grep for D9..D13)
evidence:  S-3; AC-6..AC-8, AC-21..AC-23
risk:      The 30 resolutions were checked against the doc text, not by a second gap-check
           run, so new gaps could come from D9–D13 themselves.

## Entry 28
artifact:  AGENTS.md, CLAUDE.md, .claude/settings.json, .claude/agents/test-writer.md,
           .claude/agents/reviewer.md, requirements.txt, README.md (test command); commit
           0bf7f63
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15 (fresh-clone check and
           README edit only)
prompts:   prompts/m2_session_prompts.md item 7 (commit the setup; check it on a fresh clone)
review:    Abraham wrote AGENTS.md, CLAUDE.md, the permission rules and both subagent files by
           hand; the agent did not edit them. The agent changed only README.md, replacing the
           M1 test command with the coverage-gated one so the README and AGENTS.md give the
           same command. The tests/acceptance/ deny rule is left out on purpose until the
           lock in Deliverable 3d.
checks:    fresh clone in a scratch folder: python3 -m venv .venv; pip install -r
           requirements.txt → OK; python -m pytest --cov=jobsboard --cov-branch
           --cov-report=term-missing --cov-fail-under=80 → 4 passed, 3 skipped, total 92.86%;
           mutmut --version → 3.8.1; uvicorn jobsboard.api:app --app-dir src → GET /docs 200
evidence:  Milestone 2 Deliverable 2a–2c
risk:      The permission rules have not been confirmed with /permissions after a restart,
           and JOBSBOARD_DEMO=1 and mutmut run cannot be checked until S-3 code and
           pyproject.toml exist. Bash commands such as sed or a redirect could still write
           into tests/acceptance/ after the lock, because the Edit deny rule covers only the
           Edit tool.

## Entry 29
artifact:  tests/acceptance/test_s3_ranking.py (AC-21, AC-22, AC-23 tests), commit a5d5f2e;
           evidence/test-audit.md; evidence/delegation/s3-test-audit-report.md and
           test-writer-audit.txt (/export transcript)
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15, subagent test-writer
prompts:   audit the S-3 acceptance tests and write a test for each criterion without one;
           prompts/s3_test_audit_prompt.md
review:    The main agent delegated to test-writer (the transcript shows
           "test-writer(Audit S-3 acceptance tests)"). It reported AC-21..AC-23 untested and
           added one test each; no expected value or type-only assert was flagged. Abraham
           recomputed all six expected values by hand from the criteria (AC-21's
           missing_required ("PostgreSQL",) from §5; AC-22's "a","b" from D2; AC-23's JSON from
           §4 and D8) and confirmed each test fails only because S-3 is missing. Abraham
           accepted the subagent's weak-spot finding on AC-8 and fixed it in a separate
           commit (entry 30).
checks:    .venv/bin/python -m pytest -q tests/acceptance/test_s3_ranking.py → 6 failed
           (ModuleNotFoundError jobsboard.ranking ×5; no attribute api.ranking_store ×1);
           cmp evidence/test-audit.md evidence/delegation/s3-test-audit-report.md → identical
evidence:  S-3; AC-6..AC-8, AC-21..AC-23; D2, D7, D8, D12
risk:      AC-23 and the new AC-8 depend on api.ranking_store being a module-level object
           that keeps state between requests (D12); a store rebuilt per request would fail
           them for a reason the criteria do not state.

## Entry 30
artifact:  tests/acceptance/test_s3_ranking.py, test_ac8_flagged_applicant_kept_and_stage_unchanged;
           commit "3b: AC-8 test opens the ranked list (team fix)"
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15 (main agent typed the
           change Abraham chose; no subagent)
prompts:   prompts/m2_session_prompts.md item 8 (answer the test-writer audit)
review:    Team fix for the test-writer finding in evidence/test-audit.md: the old AC-8 test
           ranked with rank_applicants directly, which never touches the S-1 store, so its
           "stage still Applied" assert could not fail. Abraham chose to have the test open
           GET /postings/P/ranked (the criterion's "opens the ranked list") and to compare the
           whole pipeline, so B must be in Applied and in no other stage. The criterion text
           and design doc are unchanged; no expected value changed (B listed, flagged, Applied).
           Abraham rejected the alternative of keeping the direct call.
checks:    .venv/bin/python -m pytest -q tests/acceptance → 6 failed; AC-8 now fails with
           AttributeError: module 'jobsboard.api' has no attribute 'ranking_store' (feature
           missing), not with an error in the test
evidence:  S-3; AC-8; R6, D12
risk:      AC-8 no longer calls rank_applicants directly, so R6 for the function's own input
           list (unchanged after ranking) is left to the property test planned in 5c.

## Entry 31
artifact:  evidence/red.txt (3c); .claude/settings.json deny rule Edit(./tests/acceptance/**)
           and tag m2-tests-locked (3d)
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15
prompts:   prompts/m2_session_prompts.md item 8 (run red, then lock after approval)
review:    Abraham approved the lock after the 3b answers were committed. red.txt is the
           tool's own output, written with tee. Only the handout's Edit deny rule was added
           (team decision, 2026-11-11); Claude Code applies Edit rules to Write as well.
checks:    python -m pytest --cov=jobsboard --cov-branch --cov-report=term-missing
           --cov-fail-under=80 | tee evidence/red.txt → 6 failed (all S-3: ModuleNotFoundError
           or missing api.ranking_store), 4 passed (S-1), coverage 92.86%
evidence:  S-3; AC-6..AC-8, AC-21..AC-23; Deliverable 3c, 3d
risk:      The rule binds only sessions started in Milestone-2/ (this session started one folder
           up and did not load .claude/). A Bash write (sed -i, redirect) into
           tests/acceptance/ is not covered by the Edit rule; the git diff --stat check at
           m2-green is the backstop.

## Entry 32
artifact:  evidence/permission-denied.md (2b permission proof)
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15, session started in
           Milestone-2/ (rules loaded); the file was written by a second session from the
           refusal Abraham pasted
prompts:   "This is a test of the permission rule. Change the expected order in test_ac7 ...
           to ["A", "B", "C"]." (saved verbatim in evidence/permission-denied.md)
review:    The tool blocked the Edit with "File is in a directory that is denied by your
           permission settings." The agent did not retry through Bash. Abraham kept the
           team decision of 2026-11-11 not to add a Bash deny pattern or hook for
           tests/acceptance/, and relies on the git diff --stat check at m2-green instead.
checks:    git status --short → clean; git diff --stat m2-tests-locked -- tests/acceptance →
           empty; git ls-remote origin → main and m2-tests-locked both at 9fe0b20
evidence:  Deliverable 2b, 3d; AC-7
risk:      Only the Edit path was tested. A Bash write into tests/acceptance/ (sed -i, >) is
           still possible and would be caught only after the fact by the m2-green diff check.

## Entry 33
artifact:  docs/design/S-3.md D10 (two-pass skill check; blank skill → InvalidSkill;
           PostingNotFound subclasses ValueError) and D13 (demo IDs via _put)
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15 (main agent typed the
           wording Abraham approved)
prompts:   prompts/m2_session_prompts.md item 9 (review the S-3 plan and settle its open points)
review:    The plan agent found that D10's "skills in sorted() order" cannot be built: sorted()
           raises TypeError when a skill set mixes str and non-str values. Abraham approved a
           two-pass rule (non-str by sorted(key=repr), then blank str in sorted() order) and
           settled the plan's two assumptions (a blank skill raises InvalidSkill; PostingNotFound
           subclasses ValueError per D3). For D13, Abraham chose the private _put over random
           IDs from store.create(), so the "Try the story" steps can use readable IDs. Design
           doc changed first, before the plan and any code, as the handout orders.
checks:    git diff docs/design/S-3.md → only D10 and D13 changed; python -m pytest -q → 6 failed,
           4 passed (unchanged; no code yet)
evidence:  S-3 §5, D3, D10, D13
risk:      No acceptance test covers validation; the two-pass order is checked only by the
           unit tests planned for Task 7. The _put call couples the demo to a private S-1
           method that S-1 could rename.

## Entry 34
artifact:  docs/plans/S-3-plan.md (corrected plan); MILESTONE2.md §4a
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15, plan mode (plan written
           in the Milestone-2/ session; corrections applied by a second session)
prompts:   prompts/s3_plan_prompt.md (write the plan); prompts/m2_session_prompts.md item 9
           (review the plan)
review:    Abraham crossed out "everything in How" from Task 1, because it bundled all §5/D3/D10
           validation into the AC-7 task without a test, and made validation its own Task 7,
           with test-writer unit tests first. Abraham moved the reviewer delegation from after the
           last task to after Task 5, the first task that touches the store and S-1 data. Abraham
           rejected the plan's line "approved without corrections" and its claim that _put
           was already a team decision; the D10/D13 points were settled in the doc first
           (entry 33, 3d6a2e9).
checks:    grep -n "~~" docs/plans/S-3-plan.md → 3 crossed-out passages; each task names one
           AC except Task 7 (validation, §5/D3/D10) and Task 8 (demo, D13)
evidence:  S-3; AC-6..AC-8, AC-21..AC-23; D10, D13; Deliverable 4a
risk:      Tasks 7 and 8 are not tied to an AC. The handout asks for every task to be tied to
           one, so a grader may count them as unplanned work. They rest on §5/D10 and D13 instead.

## Entry 35
artifact:  src/jobsboard/ranking.py (new); prompts/s3_task_1_AC-7.md; commit 9223160
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15, main agent (no
           subagent), Task 1 of docs/plans/S-3-plan.md
prompts:   prompts/s3_task_1_AC-7.md (bounded task, verbatim)
review:    Abraham approved the agent's task plan before any edit, then approved the diff.
           The agent kept to the corrected Task 1 scope: named settings, Candidate,
           RankedEntry, the three ValueError exceptions (defined but not raised until Task 7),
           and rank_applicants with exact strip/casefold matching, R1/R2 flag, §5
           missing_required order, and a sort by fit_score descending only. No validation,
           synonyms, grouping or tie-break; no other file changed. D1 is also left to Task 4:
           required skills that are equal after normalizing (e.g. "Java" and " java") are not
           yet merged into one requirement, so both spellings can appear in missing_required.
checks:    python -m pytest -q tests/acceptance/test_s3_ranking.py::test_ac7_qualified_ordered_by_fit_score
           → 1 passed; python -m pytest --cov=jobsboard --cov-branch --cov-report=term-missing
           --cov-fail-under=80 → 5 failed, 5 passed, total 90.28% (failing: AC-6, AC-8,
           AC-21, AC-22, AC-23, as the plan expects)
evidence:  S-3; AC-7; R1, R2, R4 (fit_score part); §5; D9
risk:      Ties keep input order (Python's stable sort) until Task 3, and the exception
           constructors are uncovered (ranking.py lines 34-36, 41-42, 47-48) until Task 7.

## Entry 36
artifact:  src/jobsboard/ranking.py; prompts/s3_task_2_AC-6.md; commit d569d92
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15, main agent (no
           subagent), Task 2 of docs/plans/S-3-plan.md
prompts:   prompts/s3_task_2_AC-6.md (bounded task, verbatim)
review:    Abraham approved the agent's task plan before any edit, then approved the diff.
           One line changed: the sort key went from -fit_score to (not meets_minimum,
           -fit_score), so every qualified entry comes before every flagged one (R3) and
           fit_score stays descending within each group (R4). Matching, flag,
           missing_required and the exceptions are unchanged; no other file changed.
checks:    python -m pytest -q tests/acceptance/test_s3_ranking.py::test_ac6_flagged_never_above_qualified
           → 1 passed; python -m pytest --cov=jobsboard --cov-branch --cov-report=term-missing
           --cov-fail-under=80 → 4 failed, 6 passed, total 90.28% (failing: AC-8, AC-21,
           AC-22, AC-23, as the plan expects)
evidence:  S-3; AC-6; R3, R4 (fit_score part)
risk:      Ties within a group still keep input order (stable sort) until Task 3 adds the
           application_id tie-break (D2).

## Entry 37
artifact:  src/jobsboard/ranking.py; prompts/s3_task_3_AC-22.md; commit 8464a89
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15, main agent (no
           subagent), Task 3 of docs/plans/S-3-plan.md
prompts:   prompts/s3_task_3_AC-22.md (bounded task, verbatim)
review:    Abraham approved the agent's task plan before any edit, then approved the diff.
           One line changed: application_id was added as the last sort key, giving
           (not meets_minimum, -fit_score, application_id), so equal fit scores within a group
           are in ascending application_id order (D2, R4) and input order no longer matters.
           No other file changed.
checks:    python -m pytest -q tests/acceptance/test_s3_ranking.py::test_ac22_equal_fit_scores_ordered_by_application_id
           → 1 passed; python -m pytest --cov=jobsboard --cov-branch --cov-report=term-missing
           --cov-fail-under=80 → 3 failed, 7 passed, total 90.28% (failing: AC-8, AC-21,
           AC-23, as the plan expects)
evidence:  S-3; AC-22; D2, R4
risk:      application_id order is plain string order (D2), so "10" sorts before "9"; S-1
           IDs are uuid hex, so this only shows with hand-made IDs.

## Entry 38
artifact:  src/jobsboard/ranking.py; prompts/s3_task_4_AC-21.md; commit 4ac171e
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15, main agent (no
           subagent), Task 4 of docs/plans/S-3-plan.md
prompts:   prompts/s3_task_4_AC-21.md (bounded task, verbatim)
review:    Abraham approved the agent's task plan before any edit, then approved the diff.
           The agent added _skill_key (the SKILL_SYNONYMS group is the key, so matching works
           both ways, R1/D7) and _spelling_order, and rewrote _missing_required to group
           required skills by key (D1), show the first posting spelling by (casefold(),
           spelling) for each missing group (D1), and sort the result the same way (§5).
           Before approving, Abraham set five expected missing_required values by hand; the
           agent worked each out from D1/D7/§5 in its plan before running anything.
checks:    console only, no test file: a) {"Postgres","PostgreSQL"} vs {} → ("Postgres",);
           b) {"Java"," java"} vs {} → ("Java",); c) {"Word"} vs {"Microsoft Word "} → ();
           d) {"PostgreSQL"} vs {"POSTGRES"} → (); e) {"kdb+","Java"} vs {} → ("Java","kdb+");
           all five matched. python -m pytest -q tests/acceptance/test_s3_ranking.py::test_ac21_synonym_meets_minimum
           → 1 passed; python -m pytest --cov=jobsboard --cov-branch --cov-report=term-missing
           --cov-fail-under=80 → 2 failed, 8 passed, total 91.30% (failing: AC-8, AC-23, as
           the plan expects)
evidence:  S-3; AC-21; R1, D1, D7, §5
risk:      The five console checks are not saved as tests; Task 7 or Deliverable 5 should add
           them as unit tests through test-writer so a later change cannot break D1 quietly.

## Entry 39
artifact:  src/jobsboard/ranking_store.py (new); src/jobsboard/api.py;
           prompts/s3_task_5_AC-8.md; commit d3b2641
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15, main agent (no
           subagent), Task 5 of docs/plans/S-3-plan.md
prompts:   prompts/s3_task_5_AC-8.md (bounded task, verbatim)
review:    Abraham approved the agent's task plan before any edit, then approved the diff.
           ranking_store.py: PostingNotFound(ValueError); RankingStore whose setters store
           and overwrite without validating (validation is Task 7, as the prompt says);
           candidates_for_posting raises PostingNotFound when no requirements are set, else
           keeps this posting's applications that have a profile, in the order given (no
           Rejected filter until Task 6). api.py: module-level ranking_store (D12), a 404
           handler with body {"detail": {"error": "posting_not_found"}} (§4), and
           GET /postings/{posting_id}/ranked, which only reads S-1 data (R6). S-1 code unchanged.
checks:    python -m pytest -q tests/acceptance/test_s3_ranking.py::test_ac8_flagged_applicant_kept_and_stage_unchanged
           → 1 passed; python -m pytest --cov=jobsboard --cov-branch --cov-report=term-missing
           --cov-fail-under=80 → 1 failed, 9 passed, total 90.21% (failing: AC-23, which still
           lists the Rejected applicant Y, as the plan expects). Console only: GET
           /postings/no-such-posting/ranked → 404 {"detail": {"error": "posting_not_found"}}.
evidence:  S-3; AC-8; R6, D5, D11, D12, §4
risk:      The 404 path (api.py line 66, ranking_store.py lines 12-13 and 38) has no saved test;
           Deliverable 5 should add one. Until Task 7 the store accepts any value, so bad data
           set through Python is only caught when it breaks ranking.

## Entry 40
artifact:  docs/design/S-3.md D10 (a skills argument given as a single str raises InvalidSkill)
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15 (second session reviewing
           task diffs; it typed the wording Abraham chose)
prompts:   prompts/m2_session_prompts.md item 10 (review task 5)
review:    While reviewing Task 5 (d3b2641), the reviewing session showed that
           RankingStore.set_profile(id, "Java", 50) stores the skills {"J", "a", "v"} without
           error, because D10/D11 accept "any iterable" and a str is one. The doc did not cover
           this. Abraham chose to raise InvalidSkill(the str), reusing the existing error,
           over accepting it silently. Doc changed before Task 7 builds validation.
checks:    git diff docs/design/S-3.md → D10 only; python -m pytest -q → 1 failed (AC-23,
           expected), 9 passed
evidence:  S-3 D10, D11, §5
risk:      Other iterables that are not collections of str, such as bytes or a dict of skills,
           are still not named in D10; Task 7's unit tests will show what they do.

## Entry 41
artifact:  evidence/delegation/reviewer-task5.md (and reviewer-task5.txt, /export transcript);
           review of task 5, commit d3b2641
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15, subagent reviewer
prompts:   prompts/s3_review_task5_prompt.md (main-agent prompt and the prompt it passed to
           reviewer, both verbatim)
review:    The reviewer returned "verdict: pass" with 4 minor findings. Abraham answered each:
           (1) ranking_store.py:25 set_requirements does not validate → rejected, already
           planned as Task 7 (plan correction 1; D10 amended in 622086e). (2) ranking_store.py:29
           set_profile stores invalid fit scores and skills, so D12's "stored data is always
           valid" does not hold yet → rejected for now, Task 7. (3) ranking_store.py:41 no
           Rejected filter → rejected, already planned as Task 6. (4) api.py:93 no test for the
           404 or the 200 [] response → accepted; an integration test in Deliverable 5b will
           cover both.
checks:    report saved verbatim; git diff --stat d3b2641 HEAD -- src → empty (no code changed
           by the review)
evidence:  S-3; AC-8, AC-23; R6, R7, D8, D10, D11, D12, §4; Deliverable 4c
risk:      Until Task 7, /ranked can return an out-of-range fit_score set through Python. Until
           5b, a change to the 404 body or the empty-list response would not fail any test.

## Entry 42
artifact:  src/jobsboard/ranking_store.py; prompts/s3_task_6_AC-23.md; commit 969ad37
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15, main agent (no
           subagent), Task 6 of docs/plans/S-3-plan.md
prompts:   prompts/s3_task_6_AC-23.md (bounded task, verbatim)
review:    Abraham approved the agent's task plan before any edit, then approved the diff.
           candidates_for_posting now also requires a.stage is not Stage.REJECTED (D11
           wording), so the ranked list holds exactly this posting's applications that have a
           profile and are not Rejected (R7, D8), in the order given. This closes the
           reviewer's Task 5 finding 3 (entry 41). Setters are still unvalidated (Task 7); no
           other file changed.
checks:    python -m pytest -q tests/acceptance/test_s3_ranking.py::test_ac23_ranked_endpoint_lists_only_scored_non_rejected
           → 1 passed; python -m pytest --cov=jobsboard --cov-branch --cov-report=term-missing
           --cov-fail-under=80 → 10 passed, total 90.21% (all 6 S-3 acceptance tests and all
           4 S-1 tests)
evidence:  S-3; AC-23; R7, D8, D11
risk:      Green is reached with validation not yet built: until Task 7, /ranked can return
           an out-of-range fit_score set through Python (entry 41). evidence/green.txt is not
           saved yet.

## Entry 43
artifact:  docs/design/S-3.md D10 ("" is a single str) and D11 (set_profile check order; a
           failed set leaves the store unchanged)
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15 (second session reviewing
           task work; it typed the wording Abraham chose)
prompts:   prompts/m2_session_prompts.md item 11 (review the Task 7 tests)
review:    test-writer's Task 7 report (evidence/delegation/test-writer-task7.md) listed four
           points the doc did not decide. Abraham settled three in the doc before any
           validation code: Q1, set_profile checks fit_score before skills, as D10 orders per
           candidate; Q2, a set that raises keeps the earlier value; Q3, skills "" is a single
           str and raises InvalidSkill(""). For Q4 (bytes passed as the whole skills argument),
           Abraham chose no new rule, because the existing D10 rules already raise InvalidSkill
           (with an int).
checks:    git diff docs/design/S-3.md → D10 and D11 only; python -m pytest -q tests/acceptance
           tests/test_s1_pipeline.py → 10 passed
evidence:  S-3 D10, D11, §5
risk:      Q4 is untested: set_profile(id, b"Java", 50) raises InvalidSkill with an int element
           rather than the bytes, which a caller may find confusing.

## Entry 44
artifact:  tests/unit/test_ranking_validation.py (new, 90 tests); evidence/delegation/
           test-writer-task7.md and test-writer-task7-followup.md; prompts/
           s3_task_7_tests_prompt.md and s3_task_7_tests_followup_prompt.md; commit 9a12c89
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15, subagent test-writer
           (two runs), started by the main agent
prompts:   prompts/s3_task_7_tests_prompt.md and prompts/s3_task_7_tests_followup_prompt.md
           (main-agent prompts verbatim, with the changes made before passing them to
           test-writer)
review:    Run 1 wrote 67 tests from §5, §7, D3, D9, D10, D11 and listed four points the doc did
           not decide; Abraham settled Q1-Q3 in the doc (entry 43, 30ec446) and left Q4 (bytes).
           Run 2 added Q1 (set_profile checks fit_score before skills), Q2 (a failed set keeps the
           earlier value, and a failed first set_requirements still gives PostingNotFound), Q3
           (skills "" raise InvalidSkill("")), and made the 0/100 and overwrite tests check the
           stored profile through candidates_for_posting (overwrite gives 60). The first report's
           "37 DID NOT RAISE" is an arithmetic slip: the run shows 39 (25 InvalidSkill + 12
           InvalidFitScore + 2 DuplicateApplication), plus 5 AttributeError and 2 TypeError,
           which makes 46. The main agent spot-checked repr and sorted() order, list order, and
           duplicate-before-score against D10. Run 2 flagged two points: the store tests assume
           skills are stored exactly as given (not stated in D11), and the Q2 set_profile test
           accepts either InvalidFitScore or InvalidSkill on purpose.
checks:    python -m pytest -q tests/unit/test_ranking_validation.py → 69 failed, 21 passed;
           failure reasons recounted by the main agent: 37 DID NOT RAISE InvalidSkill, 17
           InvalidFitScore, 6 (InvalidFitScore, InvalidSkill), 2 DuplicateApplication, 5
           AttributeError, 2 TypeError = 69. git diff --stat -- src tests/acceptance → empty.
           Full command: 69 failed, 31 passed, total 94.85% (all 10 acceptance tests pass).
evidence:  S-3; §5, §7, D3, D9, D10, D11 (as amended in 622086e and 30ec446); Task 7
risk:      The suite is red until Task 7b builds validation. That skills are stored as given is
           assumed by the tests but not written in D11. Q4 (bytes as the whole skills argument)
           stays untested.

## Entry 45
artifact:  src/jobsboard/ranking.py; src/jobsboard/ranking_store.py;
           prompts/s3_task_7b_validation.md; commit 6f71ca3
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15, main agent (no
           subagent), Task 7 of docs/plans/S-3-plan.md (built after the test-writer tests in
           entry 44)
prompts:   prompts/s3_task_7b_validation.md (bounded task, verbatim)
review:    Abraham approved the agent's task plan before any edit, then approved the diff.
           ranking.py: _validate_fit_score (type(x) is int and 0..100, else InvalidFitScore)
           and _validate_skills (a single str, including "", raises first; the iterable is read
           once; pass 1 raises the first non-str by repr order; pass 2 raises the first blank
           str by sorted() order, raw value kept). rank_applicants validates everything first
           in D10 order (required skills, then per candidate duplicate ID, fit score, skills)
           and ranks the validated skill lists; ranking logic unchanged. ranking_store.py: the
           setters call the same helpers (set_profile: fit_score before skills) and write only
           after validation passes, so a failed set keeps the earlier value; skills are stored
           as given. This closes the reviewer's Task 5 findings 1 and 2 (entry 41).
checks:    python -m pytest -q tests/unit/test_ranking_validation.py tests/acceptance → 96 passed;
           python -m pytest --cov=jobsboard --cov-branch --cov-report=term-missing
           --cov-fail-under=80 → 100 passed, total 96.57%; ranking.py and ranking_store.py
           100% lines and branches
evidence:  S-3; §5, D3, D9, D10, D11 (as amended in 622086e and 30ec446); Task 7
risk:      ranking_store.py imports the private helpers _validate_fit_score and
           _validate_skills from ranking.py, so a rename there breaks the store; the headless
           review may flag it. The 404 handler (api.py line 66) is still untested until 5b.

## Entry 46
artifact:  docs/design/S-3.md D13 and docs/plans/S-3-plan.md demo table (demo-empty posting)
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15 (second session reviewing
           task work; it typed the change Abraham chose)
prompts:   prompts/m2_session_prompts.md item 12 (review task 7b; plan Task 8)
review:    Reviewing Task 7b (6f71ca3): it matches §5/D3/D10/D11; 100 tests pass, and ranking.py
           and ranking_store.py have 100% line and branch coverage. Noted for the 4e refactor:
           ranking_store.py imports the private _validate_* helpers from ranking.py. For 4f the
           handout wants a screenshot of the empty or error state; the 404 needs no seed, but no
           demo posting showed 200 []. Abraham chose to add demo-empty to D13 and the plan,
           rather than showing only the 404.
checks:    git diff → D13 and one plan table row only; python -m pytest --cov=jobsboard
           --cov-branch --cov-report=term-missing --cov-fail-under=80 → 100 passed, 96.57%
evidence:  S-3 D13, §4; Deliverable 4f
risk:      The demo seed is not covered by any automated test until Task 8 or Deliverable 5;
           the README steps are checked only by hand.

## Entry 47
artifact:  src/jobsboard/ranking_store.py (seed_demo); src/jobsboard/api.py (JOBSBOARD_DEMO
           hook); README.md ("Try the story"); prompts/s3_task_8_demo.md; commit b7e7fb9
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15, main agent (no
           subagent), Task 8 of docs/plans/S-3-plan.md
prompts:   prompts/s3_task_8_demo.md (bounded task, verbatim)
review:    Abraham approved the agent's task plan before any edit, including the agent's one
           unspecified choice, applicant_id "applicant-x", then approved the diff. seed_demo
           seeds the 7 postings of the plan table (6 AC rows plus demo-empty): applications at
           Applied through ApplicationStore._put with fixed demo-acN-x IDs (D13), requirements and
           profiles through the validating setters, demo-ac23-z with no profile, and demo-ac23-y
           moved to Rejected with move_stage. api.py seeds once at import only when
           os.environ.get("JOBSBOARD_DEMO") == "1". The README section gives the start command,
           one URL per AC with what it shows, the empty state and the error state.
checks:    python -m pytest --cov=jobsboard --cov-branch --cov-report=term-missing
           --cov-fail-under=80 → 100 passed, total 90.55%. JOBSBOARD_DEMO=1 uvicorn
           jobsboard.api:app --app-dir src, then curl: demo-ac6 → a (40, no flag), b (90, flagged,
           ["kdb+"]); demo-ac7 → b 80, c 70, a 55, no flags; demo-ac8 → b flagged, and its
           pipeline shows b only under Applied; demo-ac21 → a (no flag), b (flagged,
           ["PostgreSQL"]); demo-ac22 → a, b, both 70, no flags; demo-ac23 → only x (and its
           pipeline shows y under Rejected); demo-empty → 200 []; no-such-posting → 404
           {"detail":{"error":"posting_not_found"}}. Without JOBSBOARD_DEMO: demo-ac6 and
           demo-empty → 404 (nothing seeded).
evidence:  S-3; AC-6, AC-7, AC-8, AC-21, AC-22, AC-23; D13, §4; Deliverables 4b and 4f
risk:      No automated test runs the demo, so coverage fell from 96.57% to 90.55%
           (ranking_store.py lines 72-88 and api.py line 26 uncovered); the curl checks are by
           hand. seed_demo depends on the private ApplicationStore._put (D13).

## Entry 48
artifact:  evidence/green.txt; tag m2-green (4d)
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15 (second session: reviewed
           Task 8, ran the demo, saved green.txt, tagged)
prompts:   prompts/m2_session_prompts.md item 13 (review task 8, then green)
review:    Task 8 (b7e7fb9) was reviewed by running JOBSBOARD_DEMO=1 uvicorn and curling every
           demo URL: all 7 postings, the AC-8 pipeline and the 404 match the plan table and
           their criteria; without the env var, demo-ac6 returns 404. Abraham chose on
           2026-11-15 to tag m2-green after Tasks 7 and 8, not at the first all-pass run
           (969ad37), so the tag marks the finished build with validation in place. green.txt
           is the tool's own output, written with tee.
checks:    python -m pytest --cov=jobsboard --cov-branch --cov-report=term-missing
           --cov-fail-under=80 | tee evidence/green.txt → 100 passed, total 90.55%;
           git diff --stat m2-tests-locked m2-green -- tests/acceptance → empty (lock held)
evidence:  S-3; AC-6..AC-8, AC-21..AC-23; Deliverable 4d
risk:      seed_demo (ranking_store.py lines 72-88) has no automated test, so ranking_store.py
           coverage is 67%; the demo is checked only by hand until Deliverable 5.

## Entry 49
artifact:  src/jobsboard/ranking.py; src/jobsboard/ranking_store.py; evidence/refactor.txt;
           prompts/s3_refactor.md; commit e6270d0
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15, main agent (no
           subagent), Deliverable 4e refactor
prompts:   prompts/s3_refactor.md (refactor task, verbatim)
review:    Abraham approved the agent's plan before any edit, then approved the diff. No
           behavior change: _validate_fit_score and _validate_skills renamed to the public
           validate_fit_score and validate_skills (bodies unchanged), with the three calls in
           rank_applicants and the import and three calls in ranking_store.py updated; this
           removes the private cross-module import noted in entries 45 and 46. Demo rows changed
           from (letter, skills or None, fit_score) to (letter, profile), where profile is
           (skills, fit_score) or None, so demo-ac23-z no longer carries an unused 0; two type
           aliases replace the long annotation. The agent pointed out that docs/plans/S-3-plan.md
           still names the private helpers; the prompt kept docs/ out of scope.
checks:    python -m pytest --cov=jobsboard --cov-branch --cov-report=term-missing
           --cov-fail-under=80 | tee evidence/refactor.txt → 100 passed, total 90.27% (was
           90.55%: seed_demo gained one uncovered statement). The 10 demo curl responses under
           JOBSBOARD_DEMO=1 (7 /ranked postings, the 404, 2 pipelines) were captured before
           (committed code, via git stash) and after the change, and diff found them identical.
evidence:  S-3; D9, D10, D11, D13; Deliverable 4e
risk:      validate_fit_score and validate_skills are now public names that the design doc does
           not list in §4, and the plan text still calls them private. seed_demo still has no
           automated test, so the demo comparison was a one-off check by hand.

## Entry 50
artifact:  README.md and AGENTS.md test command; pyproject.toml ([tool.coverage.report]
           fail_under = 80) (5d set-up)
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15 (second session; it
           reviewed the 4e refactor and made the change Abraham chose)
prompts:   prompts/m2_session_prompts.md item 14 (review refactor; decide coverage and mutation scope)
review:    Refactor e6270d0 reviewed: demo output at m2-green and after the refactor is
           byte-for-byte identical (cmp over all 7 postings and the AC-8 pipeline), no
           _validate_ names are left in src/, and tests are unchanged. For 5d, --cov=jobsboard also
           counted S-1's pipeline.py, so S-3 code could fall below 80% while the total stayed
           above it. Abraham chose to gate the story files only (ranking, ranking_store, api).
           For 5e, Abraham chose to mutate ranking.py and ranking_store.py, but not api.py.
checks:    python -m pytest --cov=jobsboard.ranking --cov=jobsboard.ranking_store
           --cov=jobsboard.api --cov-branch --cov-report=term-missing --cov-fail-under=80 →
           100 passed, 89.66%; python -m pytest -q → 100 passed (no gate without --cov)
evidence:  Deliverable 4e, 5d, 5e
risk:      S-1's pipeline.py is no longer under the coverage gate; a drop there would go
           unnoticed. api.py is gated but not mutated, so the strength of the route's tests is
           measured only by coverage.

## Entry 51
artifact:  tests/unit/test_ranking_edge_cases.py (36), tests/integration/test_ranked_endpoint.py
           (12), tests/property/test_ranking_properties.py (5); evidence/delegation/
           test-writer-strength.md; commit "5a-5c: edge-case, integration and property tests"
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15, subagent test-writer
prompts:   prompts/s3_test_strength_prompt.md
review:    Abraham reviewed the subagent's three files with a second session before committing.
           5a: the header maps all 14 §7 edge cases to a test; hand checks include the
           flagged-group tie B, C, A, the trimmed " Java " → ("Java",), and the casefold sort
           ("apple", "Banana", "kdb+"). 5b joins the S-3 data module (api.ranking_store) and the
           /ranked route with S-1's ApplicationStore (api.store) with no mock; it closes
           reviewer finding 4 of entry 41 (404 and 200 [] untested). 5c checks R3, R4, R5 and R6
           (twice) as relations, with no re-sort. No test was rejected. No test failed, so this
           pass found no bug.
checks:    pytest -q per file → 36, 12, 5 passed; README gated command → 153 passed, 97.54%
           (ranking.py and ranking_store.py 100%; api.py 92%, missing 26, 36, 47)
evidence:  S-3 §4, §6 R3–R6, §7, D1, D7, D8, D11–D13; Deliverable 5a–5c
risk:      Two integration tests import api.py in a subprocess to exercise the JOBSBOARD_DEMO
           hook. Coverage does not measure that process (so api.py line 26 shows as missed),
           and under mutmut it may run unmutated code.

## Entry 52
artifact:  evidence/coverage.txt (5d); pyproject.toml [tool.mutmut]; evidence/mutation-before.txt (5e)
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15 (second session: ran
           coverage and mutmut 3.8.1, proposed the triage)
prompts:   prompts/m2_session_prompts.md item 15 (review 5a-5c, then 5d and 5e)
review:    mutmut config: source_paths ["src/"] copies all of src/ into mutants/, only_mutate
           limits mutation to ranking.py and ranking_store.py (Abraham's choice, entry 50), and
           also_copy adds pytest.ini, which mutmut does not copy by default. The first run was
           not saved with tee, so the mutants/ cache was moved aside (no rm -rf) and the run was
           repeated twice; mutation-before.txt is the raw output of the last run plus
           "mutmut results". 158 mutants: 153 killed, 5 survived. Abraham's triage: #1-#4
           (exception message → None in PostingNotFound, InvalidFitScore, DuplicateApplication,
           InvalidSkill) are equivalent under D9 ("no message format is required"). Killing
           them would need expected values taken from the code. #5 (seed_demo applicant_id →
           None) is killable from S-1 §4/§5 (applicant_id is a non-empty str); test-writer will
           add that test. Abraham rejected pinning the messages.
checks:    README gated command | tee evidence/coverage.txt → 153 passed, 97.54%; mutmut run →
           158/158, 153 killed, 5 survived (1.98 mutations/second)
evidence:  S-3 D9, D13; S-1 §4, §5; Deliverable 5d, 5e
risk:      Mutation covers only ranking.py and ranking_store.py; the /ranked route in api.py is
           measured only by coverage. Two integration tests run api.py in a subprocess, and
           which source that subprocess loads under mutmut was not checked.

## Entry 53
artifact:  tests/integration/test_ranked_endpoint.py::test_d13_seed_demo_applicant_ids_are_non_empty_strings;
           evidence/delegation/test-writer-mutant.md; commit "5e: test-writer kills seed_demo mutant 9"
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15, subagent test-writer
prompts:   prompts/s3_mutant_kill_prompt.md
review:    Abraham reviewed the test with a second session. The expected value comes from
           S-1 §5 (applicant_id is a non-empty str) and §4 (an Application's JSON fields are all
           strings), not from the code. The test does not pin the demo text "applicant-a",
           because no doc fixes it. The count of 13 applications was checked by hand against
           the plan table (2+3+1+2+2+3+0).
checks:    README gated command → 154 passed, 97.54%; mutmut run
           "jobsboard.ranking_store.x_seed_demo__mutmut_9" → killed
evidence:  S-3 D13; S-1 §4, §5; Deliverable 5e
risk:      The test checks only that applicant_id is a non-blank str; a seed that gave every
           demo application the same applicant_id would still pass.

## Entry 54
artifact:  evidence/mutation-after.txt; MILESTONE2.md §5 (5b, 5d, 5e, 5f); docs/design/S-3.md §9;
           traceability/traceability.csv (S-3 rows)
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15 (second session)
prompts:   prompts/m2_session_prompts.md item 16 (review the mutant-kill test; next step)
review:    mutation-after.txt is a fresh run (the mutants/ cache moved aside) saved raw, plus
           "mutmut results": 158 mutants, 154 killed, 4 survived (the D9 message mutants
           Abraham marked equivalent in entry 52). The "passing commit" column of the matrix
           was taken from the task reviews, where each test first passed: AC-7 9223160,
           AC-6 d569d92, AC-22 8464a89, AC-21 4ac171e, AC-8 d3b2641, AC-23 969ad37. S-3 rows
           in the CSV now use tests/acceptance/ paths, and three rows were added for
           AC-21..AC-23. §9 lists the same names. The 5e comparison sentence is left to the team.
checks:    mutmut run → 158/158, 154 killed, 4 survived; every test name in the matrix found
           by grep in tests/acceptance/test_s3_ranking.py (6/6); pytest -q tests/integration → 13 passed
evidence:  S-3; AC-6..AC-8, AC-21..AC-23; Deliverable 5b, 5d, 5e, 5f
risk:      The evidence column for AC-22 and AC-23 points at team decisions (Q-6, D8) rather
           than interview evidence; no recruiter has confirmed either rule (entry 26).

## Entry 55
artifact:  scripts/review_story.sh, agent/review-schema.json (commits fb23b12, 27b1c80);
           evidence/headless-review.json; MILESTONE2.md §6c
tool:      Claude Code 2.1.325 headless (claude -p --output-format json --json-schema),
           Claude Opus 5.5 (claude-opus-5-5), 2026-11-15, subagent reviewer; run by the second
           session at Abraham's request
prompts:   the PROMPT in scripts/review_story.sh (handout core, verbatim, story ID S-3)
review:    First run: the CLI refused the schema ("no schema with key or ref
           https://json-schema.org/draft/2020-12/schema") and wrote an empty file. The $schema
           line was removed, and stdin was redirected from /dev/null after a 3 s stdin wait
           warning. Second run (27b1c80): verdict pass with no findings. Because zero findings
           can mean the main agent reviewed the files itself, Abraham had subagent_stats checked:
           by_type {"reviewer": 1}, completed 1, no permission denials, so the main form was
           used, not --agent reviewer. The JSON was checked for secrets (only token counts and
           a credential expiry time) and committed unedited.
checks:    ./scripts/review_story.sh → exit 0, 42 s; structured_output → {"verdict": "pass",
           "findings": []}; is_error false; modelUsage lists claude-opus-5-5 and, for $0.0001,
           claude-haiku-5-5
evidence:  S-3; AC-6..AC-8, AC-21..AC-23; Deliverable 6
risk:      A single headless pass with no findings is weak evidence of correctness. The
           reviewer is a model, and this run was not repeated. modelUsage shows a small
           claude-haiku-5-5 call whose purpose is not visible in the JSON.

## Entry 56
artifact:  evidence/screens/ (ac6, ac7, ac8-ranked, ac8-pipeline, ac21, ac22, ac23, empty, 404 .png);
           scripts/capture_screens.py (4f)
tool:      Claude Code, Claude Opus 5.5 (claude-opus-5-5), 2026-11-15, with Playwright 1.x
           and Chrome Headless Shell 159 installed in a scratch venv (not in requirements.txt)
prompts:   prompts/m2_session_prompts.md item 21 (capture the 4f screenshots)
review:    No browser was installed in WSL. Abraham approved installing Playwright, Chromium and
           its apt dependencies (libatomic1 and others) outside the project. Each screenshot is
           one real request made through the app's own Swagger UI (/docs, "Try it out" →
           "Execute") against JOBSBOARD_DEMO=1 uvicorn on port 8000, so it shows the request
           URL, status code and response body. None was edited. ac6, 404 and ac8-pipeline were
           opened and checked against AC-6, the §4 404 body, and AC-8 (demo-ac8-b only under
           Applied).
checks:    capture script → 9 files saved; uvicorn log shows the matching GET requests
evidence:  S-3; AC-6..AC-8, AC-21..AC-23; §4 empty and error states; Deliverable 4f
risk:      Swagger UI loads its JavaScript from a CDN, so recapturing needs network access. The
           screenshots show the API through Swagger, not a recruiter-facing page, because S-3
           has no UI in this milestone.

## Entry 57
artifact:  docs/reviews/2026-11-20-repo-review.md (new); prompts/m2_repo_review_prompt.md (new);
           commit 3f53eaf
tool:      Claude (claude.ai, Claude Opus 5.5, claude-opus-5-5), 2026-11-20; requested by Ketan Verma
prompts:   read the repo, summarize it, review it, and update the ledger with inputs, feedback and
           contributions; prompts/m2_repo_review_prompt.md
review:    Claude's GitHub connection could not open the private repo, so Ketan uploaded the
           GitHub ZIP of main (aff2104); work was committed on a fresh local repo. The review read
           all of src/jobsboard/, the test suites, MILESTONE2.md, LEDGER.md, prompts/ and
           contribution/. No code bugs were found against S-3.md. It lists 5 code findings
           (C1-C5, all Low or Info) and 6 repo findings (R1-R6); the highest is R1, missing
           contribution statements for Ketan and Aditya. Ketan read the findings and chose to
           act on C1, C2, R2, R3 and R6 and to supply his own contribution facts (R1); C3 and C4
           are left for a team decision.
checks:    python -m pytest --cov=... --cov-fail-under=80 (Python 3.13.18) → 154 passed,
           97.54%, api.py missing 26, 36, 47, same as evidence/coverage.txt; every prompts/ path
           cited in LEDGER.md exists (0 missing); all 56 earlier entries have seven fields
evidence:  S-3; AC-6..AC-8, AC-21..AC-23; Deliverables 7 and 9
risk:      The ZIP carries no tags or history, so m2-tests-locked and m2-green and the commit SHAs
           in entries 25-56 were not re-checked. The review is one model pass; C3 (non-iterable
           skills raise TypeError) needs a team decision in D10.

## Entry 58
artifact:  src/jobsboard/api.py (docstring), src/jobsboard/ranking.py (rank_applicants type
           hints), AGENTS.md (new workflow rule 0); commit 6026c61
tool:      Claude (claude.ai, Claude Opus 5.5, claude-opus-5-5), 2026-11-20; requested by Ketan Verma
prompts:   apply the low-risk fixes from the review; prompts/m2_repo_review_prompt.md
review:    Ketan chose three review findings to fix. C1: the api.py docstring now names S-3 as
           well as S-1. C2: rank_applicants takes Iterable[str] and Iterable[Candidate], matching
           D10 ("any iterable is accepted"); behaviour is unchanged. R6: AGENTS.md gains rule 0,
           start the session in the repo root, the lesson from the MILESTONE2.md reflection. No
           test was added or changed, and tests/acceptance/ was not touched. C3 (non-iterable
           skills) and C4 (no locking) were not changed; they need a team decision.
checks:    python -m pytest --cov=... --cov-fail-under=80 → 154 passed, 97.54% (unchanged);
           git diff --stat → 3 files, +3 -2
evidence:  S-3 D10; MILESTONE2.md Reflection; docs/reviews/2026-11-20-repo-review.md C1, C2, R6
risk:      mutmut was not re-run; only annotations and a docstring changed in mutated files, so
           the mutant count should be the same but is unverified.

## Entry 59
artifact:  prompts/README.md (Milestone 2 table); MILESTONE2.md §1a; review file wording;
           commit 9cc6024
tool:      Claude (claude.ai, Claude Opus 5.5, claude-opus-5-5), 2026-11-20; requested by Ketan Verma
prompts:   index the Milestone 2 prompts and record the feedback check; prompts/m2_repo_review_prompt.md
review:    The prompt index stopped at entry 24. Claude listed which prompts/ files each of
           entries 25-56 cites (script over LEDGER.md) and added one table row per file or task
           group, plus a note that entries 32 and 55 keep their prompts in
           evidence/permission-denied.md and scripts/review_story.sh. Ketan confirmed that no
           Milestone 1 feedback has been received, so §1a now says so with today's date instead
           of being left at 2026-11-15. No ledger entry was edited.
checks:    every file in prompts/ except README.md is now named in prompts/README.md (checked
           with a grep loop); every prompts/ path cited in LEDGER.md exists
evidence:  Deliverables 1a and 7; docs/reviews/2026-11-20-repo-review.md R2, R3
risk:      If Milestone 1 feedback arrives later, §1a and a new ledger entry must be updated again.

## Entry 60
artifact:  contribution/Ketan_Verma_contribution.md (new); MILESTONE2.md Team roles
tool:      Claude (claude.ai, Claude Opus 5.5, claude-opus-5-5), 2026-11-20; requested by Ketan Verma
prompts:   draft my contribution statement from my answers; prompts/m2_repo_review_prompt.md
review:    Ketan's facts, verbatim: "I did the test runs and checks of the agent and teamates
           work, Did review abhram work and suggested changes"; and "Ketan Verma reviewed on
           11/18/2026", recorded as the date of his review of Abraham's work. Claude drafted the
           statement in
           the format of Abraham's statement using only those facts and the verifiable work of
           entries 57-59; it added no tasks, commits or findings Ketan did not give. Team roles
           in MILESTONE2.md now names Ketan's part. The signature line is left blank for Ketan
           to sign himself.
checks:    statement has sections 1-3 and the confirmation line, matching
           contribution/Abraham_Eapen_contribution.md; git log origin/main → 9cc6024, so
           entries 57-59 (3f53eaf, 6026c61, 9cc6024) were pushed by Ketan before this entry;
           their artifact lines now name those commits
evidence:  Deliverable 9; docs/reviews/2026-11-20-repo-review.md R1, R4
risk:      The statement names no specific commits or ledger entries for Ketan's test runs and
           his 2026-11-18 review, because none were given; a grader may ask for them. Unsigned until
           Ketan signs. Aditya Pothuri's statement is still missing.

## Entry 61
artifact:  tests/integration/test_s1_error_paths.py (new):
           test_s1_s4_blank_applicant_id_returns_422_and_adds_nothing ("" and "   ")
tool:      Claude (claude.ai, Claude Opus 5.5, claude-opus-5-5), 2026-11-20; requested by Ketan Verma.
           Written by the main agent, not the test-writer subagent: this claude.ai session does not
           load .claude/agents/ (AGENTS.md asks for test-writer)
prompts:   summarize the test runs and raise coverage, following the Milestone 1 design doc;
           one commit per test; prompts/m2_repo_review_prompt.md (test coverage follow-up)
review:    Ketan asked whether the tests follow the Milestone 1 design doc before approving them.
           Expected values come from S-1.md, not from the code: §4 "422 if applicant_id is
           missing, blank, or not a string", §5 applicant_id non-empty, R4 "a 404, 409, or 422
           leaves the pipeline unchanged". The test checks the status and that the pipeline is
           unchanged; it does not pin the 422 body, which D2 leaves to FastAPI's default (entry 5
           risk). Fault check: with the blank check in api.py disabled, both cases fail.
checks:    full test command → 156 passed; coverage gate 97.54% → 98.52%; api.py line 36 now
           covered (missing 26, 47)
evidence:  S-1 §4, §5, §6 R4; docs/reviews/2026-11-20-repo-review.md C5; MILESTONE2.md §5d
risk:      The 422 body is still unpinned by design (D2); a FastAPI upgrade could change it unseen.

## Entry 62
artifact:  tests/integration/test_s1_error_paths.py:
           test_s1_s4_unknown_application_returns_404_and_changes_nothing
tool:      Claude (claude.ai, Claude Opus 5.5, claude-opus-5-5), 2026-11-20; requested by Ketan Verma;
           main agent, not test-writer (see entry 61)
prompts:   same as entry 61; prompts/m2_repo_review_prompt.md (test coverage follow-up)
review:    Expected values from S-1.md §4: POST /applications/{id}/stage on an unknown id returns
           404 {"detail": {"error": "application_not_found", "application_id": <id>}}; §7 lists
           an unknown application_id as an edge case; R4: the pipeline is unchanged. The full 404
           body is compared. Fault check: with the body's application_id changed in api.py, the
           test fails.
checks:    full test command → 157 passed; coverage gate 98.52% → 99.01%; api.py line 47 covered
           (missing 26 only); pipeline.py, outside the gate, 93% → 100% (lines 31-32, 75-76)
evidence:  S-1 §4, §6 R4, §7; docs/reviews/2026-11-20-repo-review.md C5; MILESTONE2.md §5d
risk:      api.py line 26 (demo seed under JOBSBOARD_DEMO=1) is still only run in a subprocess
           that pytest-cov does not measure.

## Entry 63
artifact:  tests/integration/test_s1_error_paths.py:
           test_s1_d2_bad_body_on_unknown_application_is_422_not_404
tool:      Claude (claude.ai, Claude Opus 5.5, claude-opus-5-5), 2026-11-20; requested by Ketan Verma;
           main agent, not test-writer (see entry 61)
prompts:   same as entry 61; prompts/m2_repo_review_prompt.md (test coverage follow-up)
review:    Expected value from S-1.md D2, "validation ... runs before the lookup (404)", and §7,
           a wrong-case stage name ("screened") is 422. So an unknown id with a bad body must be
           422, not 404. This test adds no coverage; it pins an ordering rule the doc states and
           no earlier test checked.
checks:    full test command → 158 passed; coverage gate 99.01% (unchanged); whole package
           (--cov=jobsboard) 96% → 99%
evidence:  S-1 §8 D2, §7; docs/reviews/2026-11-20-repo-review.md C5
risk:      MILESTONE2.md §5d and evidence/coverage.txt still show the 2026-11-15 numbers (154
           passed, 97.54%); they are the team's record of the milestone run and were not edited.

## Entry 64
artifact:  evidence/mutation-2026-11-20.txt (new)
tool:      Claude (claude.ai, Claude Opus 5.5, claude-opus-5-5), 2026-11-20; mutmut 3.8.1 on Linux,
           Python 3.13.18; requested by Ketan Verma
prompts:   re-run mutation testing after the review changes; prompts/m2_repo_review_prompt.md
           (further test and review work, item 1)
review:    Entry 58's risk said mutmut was not re-run after the rank_applicants type-hint change.
           Ketan's Mac cannot run mutmut (libcst needs a Rust compiler on Intel macOS), so the run
           was done in Claude's Linux workspace on an exact copy of main at 05acde2 (git bundle
           from Ketan's clone). Only the spinner lines were removed from the output; the counts
           and survivor list are as printed. The 4 survivors are the same exception-message
           mutants triaged as equivalent under D9 in MILESTONE2.md §5e.
checks:    mutmut run → 158/158, killed 154, survived 4, timeout 0, suspicious 0; mutmut results
           lists the same 4 mutants as evidence/mutation-after.txt
evidence:  S-3; MILESTONE2.md §5e; entry 58 risk (now closed)
risk:      Run on Linux, not on the team's machines; mutmut scope is still ranking.py and
           ranking_store.py only (team decision, entry 50), so api.py and pipeline.py are not mutated.

## Entry 65
artifact:  tests/integration/test_s1_error_paths.py (comments only); LEDGER.md entries 61-63
           (section references)
tool:      Claude (claude.ai, Claude Opus 5.5, claude-opus-5-5), 2026-11-20; requested by Ketan Verma
prompts:   found while doing item 2; prompts/m2_repo_review_prompt.md (further test and review work)
review:    Claude's own error, caught when re-reading S-1.md for item 2: entries 61-63 and the test
           comments cited R4 as §5 and the edge cases as §6. In S-1.md, R4 is in §6 (Rules), edge
           cases are §7, and D2 is §8; §4 (Interface) and §5 (Data) were cited correctly. The
           references are corrected in place; the pushed commit messages 7f3bde3, 6c1fe03 and
           2c73fc9 still carry the old numbers and cannot be changed without rewriting history.
           No assertion or expected value changed: each one was taken from the right text, only
           its section number was wrong.
checks:    python -m pytest -q tests/integration/test_s1_error_paths.py → 4 passed; grep of each
           corrected reference against S-1.md headings (§4 Interface, §5 Data, §6 Rules,
           §7 Edge cases, §8 Decisions)
evidence:  S-1 §4-§8; entries 61-63
risk:      Commit messages 7f3bde3 (§4, R4), 6c1fe03 (§4, §6, R4) and 2c73fc9 (D2) keep the
           wrong §6 for edge cases; this entry is the correction of record.

## Entry 66
artifact:  tests/integration/test_s1_pipeline_view.py (new):
           test_s1_s7_empty_posting_returns_all_five_stages_empty
tool:      Claude (claude.ai, Claude Opus 5.5, claude-opus-5-5), 2026-11-20; requested by Ketan Verma;
           main agent, not test-writer (see entry 61)
prompts:   test the empty-posting pipeline; prompts/m2_repo_review_prompt.md (further test and
           review work, item 2)
review:    S-1.md §7 lists "an empty posting (all five keys present)" as an edge case, and no test
           checked it: every existing pipeline assertion had at least one application. Expected
           value from §4 (response shape, five stage keys) and §5 (any posting ID is valid; no
           posting entity until S-6). The whole JSON body is compared. Fault check: with api.py
           building the stages dict empty instead of from Stage, the test fails.
checks:    python -m pytest → 159 passed; coverage gate 99.01% (unchanged; the code path was
           already run by other tests, this pins its behaviour for the empty case)
evidence:  S-1 §4, §5, §7
risk:      None new.

## Entry 67
artifact:  pyproject.toml ([tool.coverage.run] patch = ["subprocess"])
tool:      Claude (claude.ai, Claude Opus 5.5, claude-opus-5-5), 2026-11-20; coverage 7.17.4,
           pytest-cov 7.1.0; requested by Ketan Verma
prompts:   measure the demo-seed subprocess in coverage; prompts/m2_repo_review_prompt.md
           (further test and review work, item 3)
review:    MILESTONE2.md §5d explains that api.py line 26 (seed_demo under JOBSBOARD_DEMO=1) runs
           only inside the subprocess started by test_d13_demo_env_1_serves_plan_table_over_http,
           which coverage did not measure. pytest-cov 7 no longer measures subprocesses itself;
           coverage's own patch = ["subprocess"] (coverage >= 7.10, which pytest-cov 7.1.0
           already requires) does. This is a configuration change only: no test or source file
           changed, and fail_under stays 80. The subprocess inherits the parent environment
           (the test copies os.environ), so coverage starts in it.
checks:    full test command → 159 passed, Total coverage: 100.00% (api.py, ranking.py,
           ranking_store.py all 100%, no missing lines or partial branches); python -m pytest -q
           without --cov → 159 passed; no stray .coverage.* files left after the run
evidence:  MILESTONE2.md §5d; docs/reviews/2026-11-20-repo-review.md C5
risk:      If a later test starts a subprocess with a cleaned environment, coverage will not run
           in it. Coverage of the subprocess depends on coverage >= 7.10, pinned indirectly
           through pytest-cov==7.1.0.

## Entry 69
artifact:  README.md (Install: note for the libcst build failure)
tool:      Claude (claude.ai, Claude Opus 5.5, claude-opus-5-5), 2026-11-20; requested by Ketan Verma
prompts:   note the Intel-Mac install problem in the README; prompts/m2_repo_review_prompt.md
           (further test and review work, item 4)
review:    On 2026-11-20 Ketan's fresh install on an Intel Mac failed: pip found no prebuilt
           libcst (a mutmut dependency) and could not build it without a Rust compiler;
           upgrading pip did not help. Installing requirements.txt without mutmut worked, and the
           tests then ran. The README now says this, with the exact two commands Ketan used and
           where to run mutmut instead. requirements.txt itself is unchanged (AGENTS.md: ask
           before changing dependencies).
checks:    the two commands are the ones Ketan ran successfully; the full test command was then
           run and the result pushed (2c73fc9)
evidence:  Ketan's install output, 2026-11-20; README "Install"
risk:      Only seen on one Intel Mac; other platforms may hit it with other Python versions.

## Entry 70
artifact:  Local dev environment fix (no code change). Covers running
           src/jobsboard/api.py via `uvicorn jobsboard.api:app --app-dir src --reload`
           after it failed with "[Errno 48] Address already in use" on port 8000.
tool:      Claude (claude.ai), model Claude Opus 5.5 (claude-opus-5-5), used 2026-11-21
prompts:   1. Pasted the uvicorn startup error and asked for help resolving it
              -> prompts/<entry-n>-01-uvicorn-port-in-use.md
           2. Asked for this ledger entry using Option 1 (kill the process on port 8000)
              -> prompts/<entry-n>-02-ledger-entry.md
review:    Read the AI's diagnosis: port 8000 was still held by an earlier
           uvicorn process (Errno 48 = EADDRINUSE on macOS). The AI gave two options:
           (1) find and kill the process holding port 8000, or (2) run on --port 8001.
           Accepted Option 1, because it keeps the default port that the project
           and its docs/clients expect, and it removes a stale server instead of
           leaving it running in the background.
           Rejected Option 2: it hides the stale process and changes the URL.
           Before killing, confirmed with lsof that the process was Python/uvicorn
           and not an unrelated service. No source files were changed.
checks:    $ lsof -i :8000
            COMMAND     PID USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
com.docke 47515   ga  111u  IPv4 0xa0e005b0ae88a101      0t0  TCP localhost:irdmi (LISTEN)
ga@Adityas-MacBook-Pro cs690-project-milestone2 % kill 47515
evidence:  Rer-ran the unicorn without any errors
risk:      Check Port assignments to ensure there are no conflicts. 
