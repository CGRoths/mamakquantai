# MQAI-0002C — Claude Scaffold Review

> Reviewer: Claude. Read-only over the scaffold. Wrote ONLY this file. No remediation, no product
> repo touched, no scaffold file edited. Date: 2026-07-09.

---

## VERDICT: request_changes

The scaffold is thorough and 8 of the 9 confirmation items pass outright. However, there is a
**material internal contradiction in the write-authorization model** that touches the two most
important guarantees (when writes are allowed, and how the executed-diff review is produced). It
must be reconciled before this HIGH-tier execution job runs. The fixes are structural clarifications,
not a redesign.

## Confirmation checklist

1. **`execution_authorized` is false — CONFIRMED.** `job.yaml`: `execution_authorized: false`,
   `writes_gated: true`.
2. **Product-repo writes blocked until separate Cray approval — CONFIRMED (with contradiction, see
   W1).** Stated in `job.yaml` gating + `forbidden_actions` #5/#6/#7, but conflicts with the
   apply-before-Cray ordering in `review_requirements.md` / `validation_plan.md`.
3. **Exact write paths enumerated — CONFIRMED.** `allowed_writes.md` gives per-repo path tables.
4. **`mqnode_test2` & `mqchain-console` confirm-only / zero-write — CONFIRMED.** Both marked
   "NO WRITES" in `allowed_writes.md` and `changes: [confirm_only]` in `job.yaml`.
5. **PyPI-Recovery-Codes validation case-insensitive + anchored — CONFIRMED.** `validation_plan.md`
   V1 uses `(?i)PyPI-Recovery-Codes.*\.txt` / `grep -Ei`; ignore pattern `/PyPI-Recovery-Codes*.txt`.
6. **Avoids secret-content inspection — CONFIRMED.** `forbidden_actions` #1; `secret_content_inspection:
   false`; filename/metadata only throughout.
7. **No history rewrite — CONFIRMED.** `forbidden_actions` #3; RP7 excluded and left to a separate
   authorization.
8. **Commit blocked until eval gates + actual-diff review + GPT synthesis + Cray approval —
   CONFIRMED.** `review_requirements.md` hard gate encodes exactly this ordering.
9. **Missing rollback/validation/scope weaknesses — see below (W1–W4).**

## Findings

### W1 — BLOCKING: contradictory write-authorization model (stage vs commit)
The scaffold conflates "apply changes on a branch / stage the diff" with "commit," and forbids ALL
product-repo writes until Cray approval — yet its own required flow needs a write before Cray:
- `forbidden_actions` #5: *"No product-repo write of any kind (including `.gitignore` creation and
  `git rm --cached`) before explicit Cray execution approval."*
- `job.yaml`: `execution_authorized` flips true *only after* step 5 (Cray); writes forbidden until
  then.
- BUT `review_requirements.md` hard gate: `claude_review (proposed) → [AUTHORIZED WINDOW] apply
  changes on branch, stage diff → claude_review_executed (diff matches plan) → gpt_synthesis →
  cray_decision → commit`. And `validation_plan.md` V1 expects a *before/after* comparison and a
  `staged_diff.md` — all of which require applying changes (a product-repo write) **before** Cray
  approval.

**Impact:** as written, you cannot produce the executed-diff review (item 8's prerequisite) without
violating `forbidden_actions` #5 / `job.yaml`. The two guarantees are mutually exclusive.

**Recommended fix (two-phase authorization):**
- **Phase 1 — preview (branch-local):** after `scaffold_reviewed` + `eval_gates_pass` +
  `claude_review (proposed) = approve`, allow applying changes **on an isolated branch only**
  (create `.gitignore`, `git rm --cached`), **stage, and diff — NO commit, NO push.** This is the
  window that produces `staged_diff.md`.
- **Phase 2 — commit (gated):** blocked until `claude_review_executed = approve` + `gpt_synthesis =
  approve` + `cray_decision = approve`. Only then commit (push still separately authorized).
- Update `forbidden_actions` #5 to forbid **commit/push** before Cray (not all writes), keep
  disk-deletion/history-rewrite absolute, and split `execution_authorized` into
  `preview_authorized` (Phase 1) and `commit_authorized` (Phase 2) — or rename to make the
  stage/commit boundary explicit.

### W2 — SHOULD-FIX: `write_scope_check` cannot enforce product-repo write scope in V0
`validation_plan.md` V8 states `write_scope_check` will confine product-repo writes to the authorized
branch + allowed paths. The current scripted gate (`evals/scripts/write_scope_check.ps1`) only audits
`jobs/active/<id>/output|review` and has no knowledge of product-repo paths. So its "pass" says
nothing about the mqengine/mqnode_cloud writes.
- **Fix:** add an explicit product-repo path guard for this job (compare `git -C <repo> status
  --porcelain` against `allowed_writes.md`), or a mandatory manual verification step, before commit.
  Do not rely on the V0 stub for product-repo scoping.

### W3 — MINOR: rollback deletes a file from disk, conflicting with "no disk deletion"
`rollback_plan.md` R-A includes `rm "<repo>/.gitignore"`, but `forbidden_actions` #2 says "No disk
deletion." These need reconciliation.
- **Fix:** clarify that the no-deletion rule protects **pre-existing / user files**, and that a
  **job-created** file (the new `.gitignore`) may be removed on rollback — or avoid `rm` entirely and
  leave the untracked `.gitignore` in place / use `git clean -f -- .gitignore` with an explicit note.

### W4 — MINOR: exact hardcoded recovery filename in `git rm --cached`
`execution_plan.md` Step 3a removes the file by its exact name. If the filename differs at execution
time, the step silently no-ops while V1 still expects untracking.
- **Fix:** use an anchored glob consistent with detection, e.g.
  `git rm --cached -- 'PyPI-Recovery-Codes*.txt'`, and assert V1 count == 0 afterward.

## Scope-control assessment
Scope is otherwise well-bounded: four repos, two with `.gitignore` + untracking, two strictly
confirm-only; no source/schema/formula edits; no cross-layer writes; no push; builder cannot
self-approve. The only scope weakness is enforcement (W2), not intent.

## Rollback assessment
Branch-first strategy is sound (primary rollback = discard branch, nothing reaches default/remote).
Covered: pre-commit unstage, branch abandon, soft reset, recovery-file re-track. Gaps: W3 wording,
and it should also state rollback for the mqnode_cloud `.gitignore` (same branch-discard applies,
but make it explicit).

## Validation assessment
V1–V8 are strong and the case-insensitive recovery check is correct. Gaps: V8 over-claims
`write_scope_check` (W2); add an explicit "before" capture step (baseline HEAD + `git ls-files`
counts) so the before/after comparison in V1/V2 is anchored to a recorded baseline.

## Boundary / secret-handling (this review)
- BOUNDARY_CHECK: pass — read-only; only this review file written.
- SECRET_HANDLING_CHECK: pass — no secret file opened; recovery filename referenced as metadata only.

## REQUIRED_CORRECTIONS (before execution)
1. **W1 (blocking):** reconcile the stage-vs-commit authorization; introduce the two-phase model so
   the executed-diff review can exist without violating the "no write before Cray" rule. Make clear
   that **commit/push** (not branch-local staging) is what Cray gates.
2. **W2:** add a real product-repo write-scope guard (or mandatory manual check); stop relying on the
   V0 `write_scope_check` stub for product paths.
3. **W3:** reconcile rollback disk-`rm` with the no-deletion rule.
4. **W4:** use an anchored glob for the recovery-file `git rm --cached`.

## EXECUTION_ALLOWED_NOW: no
Scaffold only. No execution regardless of this verdict; corrections required before the execution
consensus chain proceeds.
