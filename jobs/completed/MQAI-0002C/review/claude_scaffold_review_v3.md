# MQAI-0002C — Claude Scaffold Re-Review (v3)

> Reviewer: Claude. Read-only over the scaffold. Wrote ONLY this file. No remediation, no product
> repo touched, no scaffold file edited, no git rm, no commit/push, no secret file opened.
> Date: 2026-07-09. Supersedes v1 (request_changes) and v2 (request_changes).

---

## VERDICT: approve_scaffold

All prior findings are resolved. W1–W4 (v1) and R1–R5 (v2) are fixed; no new substantive issue.
The scaffold is internally consistent and safe to advance to the next stage (eval gates →
proposed-execution review → Gate A). Approving the **scaffold** does NOT authorize execution.

## W1–W4 — remain fixed
- **W1 two-gate model:** `job.yaml` scope (`execution_authorized:false`, `commit_authorized:false`)
  + `gating.gate_A`/`gate_B`; `forbidden_actions` #5–#7; `review_requirements` hard gate. Consistent.
- **W2 write-scope honesty + V9:** `validation_plan` V8 IMPORTANT note disclaims the V0 gate; V9 is
  the real product-repo guard.
- **W3 rollback deletion scope:** `rollback_plan` "Deletion policy" + `forbidden_actions` #2 protect
  pre-existing/user/product files; only job-created `.gitignore` removable via `git clean`.
- **W4 anchored glob:** `execution_plan` Step 3a `git rm --cached -- 'PyPI-Recovery-Codes*.txt'`.

## R1–R5 — fixed
- **R1 (V1–V8 → V1–V9):** corrected in `job.yaml` gate_B, `forbidden_actions` #6, `execution_plan`
  intro/Step 7/Step 8. Repo-wide grep shows no stray `V1–V8` in spec files; the only remaining `V8`
  is the legitimate `## V8` section header (a distinct eval-gate check, correctly not renamed).
- **R2 (V9 confirm-only logic):** now requires `status_after == status_before` (byte-identical
  `diff`), explicitly tolerating pre-existing dirt and failing on any new job-introduced change.
- **R3 (Step 7 cross-ref):** now points to `validation_plan.md` **V9**.
- **R4 (duplicate numbering):** `forbidden_actions` renumbered to 10/11.
- **R5 (canonical glob):** `PyPI-Recovery-Codes*.txt` across spec files; the old `-*` form survives
  only in historical review/notes documents (acceptable).

## Checklist confirmations (all PASS)
1. W1–W4 remain fixed — CONFIRMED.
2. R1–R5 fixed — CONFIRMED.
3. All full validation-chain references say **V1–V9** — CONFIRMED (`## V8` header is a distinct
   check, not the chain range).
4. V9 confirm-only uses `status_after == status_before` — CONFIRMED (V9, lines 73–79).
5. V9 compares changed/touched paths vs `allowed_writes.md` for change repos — CONFIRMED (V9,
   lines 80–86).
6. Confirm-only tolerate pre-existing dirt but fail on any new MQAI-0002C change — CONFIRMED
   (byte-identical diff; "any new/changed path vs baseline → FAIL").
7. Canonical recovery glob `PyPI-Recovery-Codes*.txt` — CONFIRMED.
8. Removal command `git rm --cached -- 'PyPI-Recovery-Codes*.txt'` — CONFIRMED (execution_plan Step
   3a; allowed_writes table).
9. Validation case-insensitive + anchored — CONFIRMED (V1 `(?i)` / `grep -Ei`).
10. `execution_authorized=false` ⇒ Gate A not granted, product-repo writes blocked — CONFIRMED.
11. Gate A = branch-local remediation + staging + diff capture only after Cray execution approval —
    CONFIRMED.
12. Gate A does NOT allow commit/push — CONFIRMED (`does_not_grant: [commit, push]`; forbidden #6/#7).
13. Gate B allows commit/push only after V1–V9 + executed-diff review + GPT synthesis + Cray final
    approval — CONFIRMED (`gating.gate_B`; hard gate).
14. No secret-content inspection — CONFIRMED (forbidden #1; `secret_content_inspection: false`).
15. No history rewrite — CONFIRMED (forbidden #3; RP7 excluded).
16. Rollback does not remove pre-existing untracked secret/user/product files — CONFIRMED
    (rollback "Deletion policy"; forbidden #2).

## Optional (non-blocking) refinement
- V9 change-repo wording ("compute the set difference … not attributable to pre-existing state") is
  slightly informal. In practice `output/<repo>_touched_paths.txt` (`git diff --cached --name-only`)
  IS the authoritative job-delta (only what the job staged), so the execution job can compare that
  file directly to the allow-list. Consider stating that explicitly. Not required for approval.

## Boundary / secret-handling (this review)
- BOUNDARY_CHECK: pass — read-only; only this review file written.
- SECRET_HANDLING_CHECK: pass — no secret file opened; recovery filename referenced as metadata only.

## EXECUTION_ALLOWED_NOW: no
Scaffold approved, but no gate is granted (`execution_authorized=false`, `commit_authorized=false`).
Next stage: run scripted eval gates → produce `claude_review.md` of the proposed execution → obtain
**Gate A** (Cray execution approval) before ANY branch-local product-repo work. Execution remains
fully blocked until then.

## Recommended next steps
1. Run scripted eval gates for MQAI-0002C (`run_codex_job.ps1 -JobId MQAI-0002C -EvalsOnly`).
2. Claude review of the proposed execution (distinct from this scaffold review).
3. Cray Gate-A decision (`review/cray_execution_approval.md`) — only then does branch-local work begin.
