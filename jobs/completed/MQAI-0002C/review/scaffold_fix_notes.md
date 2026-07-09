# MQAI-0002C — Scaffold Fix Notes

> Builder correction pass applied after `claude_scaffold_review.md` (VERDICT: request_changes).
> Scaffold files only — no remediation, no product repo touched, no `git rm`, no product-repo
> `.gitignore` created, no deletion, no history rewrite, no secret contents inspected, no commit/push.
> Date: 2026-07-09.

## W1 — two-gate authorization model (was: contradictory single gate)
Replaced the self-contradictory "no product-repo write until Cray approval" (which made the required
executed-diff review impossible) with an explicit two-gate model:
- **Gate A — `cray_execution_approval`** → `execution_authorized = true`: authorizes BRANCH-LOCAL
  remediation work only (create branch, create `.gitignore`, `git rm --cached`, stage, capture diff).
  Does NOT authorize commit/push.
- **Gate B — `cray_final_approval`** → `commit_authorized = true`: authorizes commit (push only if
  separately authorized), after V1–V9 + executed-diff review + GPT synthesis.
- `execution_authorized=false` = Gate A not yet granted → no product-repo writes at all.
- Files changed: `job.yaml` (scope + gating), `forbidden_actions.md` (#5–#9 restructured),
  `allowed_writes.md` (intro), `execution_plan.md` (intro + Step 7/8), `review/review_requirements.md`
  (artifacts list + hard gate).

## W2 — validation_plan V8 corrected + new V9 product-repo path guard
- V8 now states plainly that the V0 `write_scope_check` audits ONLY the MQAI job folder and CANNOT
  police product-repo writes.
- New **V9**: mandatory per-repo pre/post `git status` + `git diff --cached --name-only` capture,
  compared against the exact `allowed_writes.md` allow-list; confirm-only repos must show an empty
  status; all capture files saved under `jobs/active/MQAI-0002C/output/`. Any out-of-list path → FAIL.
- File changed: `validation_plan.md`.

## W3 — rollback deletion policy clarified
- "No disk deletion" now explicitly protects **pre-existing / user / product files** (and never
  removes pre-existing untracked secret files). **Job-created** files on the remediation branch
  (e.g. a new `.gitignore`) may be removed on rollback, via `git clean -f -- .gitignore`. No history
  rewrite during rollback.
- Files changed: `rollback_plan.md`, and `forbidden_actions.md` #2.

## W4 — anchored glob for recovery-file untracking
- `execution_plan.md` Step 3a now uses `git rm --cached -- 'PyPI-Recovery-Codes*.txt'` (anchored
  glob) instead of a hardcoded exact filename; validation remains case-insensitive/anchored (V1).
  No file contents inspected.
- File changed: `execution_plan.md`.

## Status
Scaffold updated; still **scaffold only**. `execution_authorized=false`, `commit_authorized=false`.
Ready for scaffold re-review. No gate granted; no execution.
