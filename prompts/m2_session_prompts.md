# Milestone 2 session prompts (Abraham, Claude Code)

The team's own requests to the main Claude Code agent, verbatim, in order. Decisions given
through the agent's multiple-choice questions are listed after each request.

1. "Review CS690_Milestone2_handout"
2. "Prompt me to settle in repo first from items 1 - 8 before working on Handout 2. Use Milestone-2 folder to work with."
   - Repo: copy without git into a new repo. Demo: FastAPI + in-memory store. Lock: handout Edit rule only.
   - OQ-1: application_id ascending. OQ-2: no override in S-3. OQ-3: fixed synonym table. OQ-4: exclude unscored and Rejected.
   - Property tests: R3, R4, R5, R6.
3. "Prompt me for the three items"
   - Remote https://github.com/AbrahamEapen/CS690-Project-Milestone2.git; synonyms only the INT-03 pairs, both directions; first commit approved.
4. "Push inital to https://github.com/AbrahamEapen/CS690-Project-Milestone2.git"
5. "Review CS690_Milestone2_Handout. Lets complete delieverables 1-9 for story S-3. Prompt me for any decision, validation, or question. adhere to guidelines in Milestone2 handout. ensure updates to md files as we go thru delieverables"
   - 1a: M1 feedback not received yet. New ACs AC-21..AC-23 approved. Synonym requirements count as one. Seeded in-memory ranking store.
   - Gap check 2: validate on set; any non-int fit_score rejected; non-str skill raises InvalidSkill, ids unchecked.
6. "Review Milestone-2 Repo and CS690_Milestone2_Handout. I want to complete Story S3. How long would that take with Claude help ?"
7. "I would like to complete story 3 following instructions from CS690 Milestone 2 in the Milestone 2 repo. Prompt me for any questions or validation."
   - Deliverable 2 setup: commit as drafted (AGENTS.md, CLAUDE.md, .claude/ written by Abraham). Fresh-clone check in a scratch folder: approved.
   - Checkpoints: stop at each review the handout requires. Team roles: Abraham led all four areas.
8. "I have completed step. review and lets proceed to next step" (after the test-writer audit ran in a session started from Milestone-2/)
   - AC-8 finding: fix the test to go through GET /postings/P/ranked and check the whole pipeline (team commit). Hand recomputation of all six expected values: confirmed by Abraham.
9. "The S-3 plan is saved to docs/plans/S-3-plan.md. It isn't committed yet. Review and prompt me for next steps"
   - Validation: own task (Task 7), test-writer drafts unit tests first. Reviewer: after Task 5. Demo seed: store._put, recorded in D13. D10 two-pass wording: approved.
10. Task reviews: "Task N is committed, please review and prompt for any question or validation. Then move to next step" (tasks 1-5)
   - Task 5 review: a bare str for skills raises InvalidSkill(the str) (D10 amended before Task 7).
