# MQAI-0002C — Claude Scaffold Re-Review (v2)

> Reviewer: Claude. Read-only over the scaffold. Wrote ONLY this file. No remediation, no product
> repo touched, no scaffold file edited, no git rm, no commit/push, no secret file opened.
> Date: 2026-07-09. Supersedes `claude_scaffold_review.md` (v1, request_changes).

---

## VERDICT: request_changes

The four v1 findings (W1–W4) are **correctly resolved** — this is not a redo. However, the edits left
a set of **internal-consistency nits** (a `V1–V8` vs `V1–V9` mismatch in several files) and one
**substantive validation-logic gap** (the confirm-only check would false-fail against pre-existing
dirty state). These are small, targeted fixes; once applied the scaffold should be approvable.

## Checklist confirmations (all substantively PASS)

1. **W1 two-gate model internally consistent — MOSTLY (see R1).** Gate A / Gate B are cleanly
   defined and the write-window contradiction is gone; only stale `V1–V8` labels mar consistency.
2. **`execution_authorized=false` ⇒ Gate A not granted, product-repo writes blocked — CONFIRMED.**
   `job.yaml` L20/L98, `forbidden_actions` #5.
3. **Gate A = branch-local remediation + staging + diff capture after Cray execution approval —
   CONFIRMED.** `job.yaml` gate_A.grants; `execution_plan` Steps 1–7; `review_requirements` hard gate.
4. **Gate A does NOT allow commit/push — CONFIRMED.** `gate_A.does_not_grant: [commit, push]`;
   `forbidden_actions` #6/#7; `execution_plan` Step 7 "DO NOT COMMIT".
5. **Gate B allows commit/push only after validation + executed-diff review + GPT synthesis + Cray
   final approval — CONFIRMED.** `job.yaml` gate_B preconditions; `review_requirements` hard gate.
6. **V8 honestly states V0 `write_scope_check` cannot police product repos — CONFIRMED.** V8
   IMPORTANT note is explicit.
7. **V9 requires pre/post `git status` + touched-path comparison — CONFIRMED.** V9 baseline + post
   captures + allow-list comparison, evidence saved to `output/`.
8. **`mqnode_test2` & `mqchain-console` confirm-only / zero-write — CONFIRMED** (targets, V9,
   `forbidden_actions` #10) — but the confirm-only *check itself* is flawed; see R3.
9. **Recovery removal uses anchored glob `git rm --cached -- 'PyPI-Recovery-Codes*.txt'` — CONFIRMED.**
   `execution_plan` Step 3a.
10. **Validation remains case-insensitive + anchored — CONFIRMED.** V1 `(?i)` / `grep -Ei`.
11. **No secret-content inspection — CONFIRMED.** `forbidden_actions` #1; `secret_content_inspection:
    false`; metadata-only throughout.
12. **No history rewrite — CONFIRMED.** `forbidden_actions` #3; RP7 excluded.
13. **Rollback does not remove pre-existing untracked secret/user/product files — CONFIRMED.**
    `rollback_plan` "Deletion policy" + R-D; `git clean -f -- .gitignore` scoped to the job-created file.

## Residual findings

### R1 — MINOR (consistency): stale `V1–V8` vs authoritative `V1–V9`
V9 (product-repo path guard) was added, and `validation_plan.md` pass criteria + `review_requirements`
hard gate correctly say **V1–V9**. But several places still say **V1–V8**, which *excludes the very
path guard Gate B depends on*:
- `job.yaml` gate_B precondition 1: "V1-V8 … incl. product-repo path guard" (the guard is V9).
- `forbidden_actions.md` #6: "V1–V8 validation pass".
- `execution_plan.md` intro, Step 7, Step 8 heading: "V1–V8".
→ Fix: change these to **V1–V9**.

### R2 — MEDIUM (validation logic): confirm-only check false-fails on pre-existing dirty state
`validation_plan.md` V9 says: *"`mqnode_test2` and `mqchain-console`: `status_after` MUST be empty
(confirm-only). Any change → FAIL."* But these working trees are **already dirty independent of this
job** — verified earlier this session: `mqnode_test2` has a modified `docker-compose.yml`
(`git status --porcelain` = 1). Requiring an *empty* status would **FALSE-FAIL** on pre-existing dirt
the job never touched. (This is fail-safe, not permissive, but it would wrongly block execution.)
→ Fix: assert **`status_after == status_before` (no NEW change attributable to the job)** using the
captured baseline, rather than requiring empty. Same principle for any confirm-only repo.

### R3 — MINOR (stale cross-ref): `execution_plan.md` Step 7 points to "V8"
Step 7 says "Capture pre/post `git status` + touched-path comparison per repo (see
`validation_plan.md` V8)". That capture guard is **V9**, not V8.
→ Fix: reference V9.

### R4 — COSMETIC: duplicate list numbering in `forbidden_actions.md`
Item **9** appears twice ("Branch work never implies commit" under *Always*, and "No self-promotion"
under *Process guards"). → Renumber to 9/10/11.

### R5 — COSMETIC: recovery glob shape mismatch
`allowed_writes.md` lists `PyPI-Recovery-Codes-*.txt` (hyphen before `*`) while the `.gitignore` /
Step 3a use `PyPI-Recovery-Codes*.txt` (no hyphen). Both match the real filename, but align them for
consistency.

## Boundary / secret-handling (this review)
- BOUNDARY_CHECK: pass — read-only; only this review file written.
- SECRET_HANDLING_CHECK: pass — no secret file opened; recovery filename referenced as metadata only.

## Rollback assessment
Sound: branch-first, index-only, job-created-file-only cleanup via `git clean`, pre-existing secret
files never removed, no history rewrite. No gaps beyond R2's interaction (rollback correctly triggers
on V9 FAIL; just fix V9's confirm-only logic).

## REQUIRED_CORRECTIONS (all minor; no redesign)
1. **R2 (medium):** confirm-only repos must validate `status_after == status_before`, not "empty",
   to tolerate pre-existing dirty state.
2. **R1:** replace stale `V1–V8` with `V1–V9` in `job.yaml`, `forbidden_actions.md`, `execution_plan.md`.
3. **R3:** fix `execution_plan.md` Step 7 cross-reference (V8 → V9).
4. **R4:** renumber duplicate item 9 in `forbidden_actions.md`.
5. **R5:** align the recovery glob shape across `allowed_writes.md` / `.gitignore` / Step 3a.

## EXECUTION_ALLOWED_NOW: no
Scaffold only. No gate granted (`execution_authorized=false`, `commit_authorized=false`). Apply the
corrections, then this scaffold is ready to approve and proceed to the eval-gate + proposed-execution
review stage.
