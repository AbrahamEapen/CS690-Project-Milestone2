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
