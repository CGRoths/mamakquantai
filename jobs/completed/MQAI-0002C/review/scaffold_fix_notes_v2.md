# MQAI-0002C — Scaffold Fix Notes v2

> Builder correction pass after `claude_scaffold_review_v2.md` (VERDICT: request_changes).
> Scaffold files only — no remediation, no product repo touched, no `git rm`, no product-repo
> `.gitignore` created, no deletion, no history rewrite, no secret contents inspected, no commit/push.
> Date: 2026-07-09.

## R2 — V9 confirm-only validation logic fixed (was: "status_after must be empty")
`validation_plan.md` V9 now proves **no NEW change** instead of requiring an empty tree:
- Confirm-only repos (`mqnode_test2`, `mqchain-console`): require **`status_after == status_before`**
  (byte-identical `diff` of the captured before/after `git status --porcelain`). Tolerates
  pre-existing dirty state (e.g. `mqnode_test2`'s modified `docker-compose.yml`); any new/changed
  path vs baseline → FAIL.
- Change repos (`mqengine`, `mqnode_cloud`): the **delta vs baseline** must be ⊆ the `allowed_writes.md`
  allow-list (not the raw post-state), so pre-existing dirt is not mistaken for job output.
- Both before and after status outputs are captured under `jobs/active/MQAI-0002C/output/`.
- File changed: `validation_plan.md`.

## R1 — stale `V1–V8` → `V1–V9`
Updated everywhere the full validation chain (incl. the V9 path guard) is meant:
- `job.yaml` gate_B precondition 1.
- `forbidden_actions.md` #6.
- `execution_plan.md` intro, Step 7, Step 8 heading.
Files changed: `job.yaml`, `forbidden_actions.md`, `execution_plan.md`.

## R3 — Step 7 cross-reference corrected (V8 → V9)
`execution_plan.md` Step 7 now points to `validation_plan.md` **V9** for the pre/post `git status`
+ touched-path guard. File changed: `execution_plan.md`.

## R4 — duplicate numbering fixed
`forbidden_actions.md` process guards renumbered to **10** and **11** (were a second "9" and "10").
File changed: `forbidden_actions.md`.

## R5 — recovery glob normalized
Canonical glob is now **`PyPI-Recovery-Codes*.txt`** across the scaffold:
- Removal command stays `git rm --cached -- 'PyPI-Recovery-Codes*.txt'` (`execution_plan.md` Step 3a).
- `.gitignore` pattern stays `/PyPI-Recovery-Codes*.txt`.
- `allowed_writes.md` table updated from `PyPI-Recovery-Codes-*.txt` to `PyPI-Recovery-Codes*.txt`.
- Validation remains case-insensitive + anchored (`(?i)PyPI-Recovery-Codes.*\.txt` / `grep -Ei`).
- No file contents inspected. File changed: `allowed_writes.md`.

## Status
Scaffold updated; still **scaffold only**. `execution_authorized=false`, `commit_authorized=false`.
No gate granted; no execution. Ready for scaffold re-review (not performed in this pass).
