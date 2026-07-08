# MQAI-0002B — Claude Review (planning phase)

> Reviewer: Claude. Read-only over planning files. Wrote ONLY this file.
> No remediation, no product-repo writes, no `git rm`, no `.gitignore` added to any product repo,
> no deletion, no history rewrite, no secret file opened. Date: 2026-07-09.

---

## VERDICT: request_changes

Strategy is sound and boundaries are correctly drawn, but the **validation checklist contains a
verified false-pass bug** on the single most important remediation item (RP1). Because this checklist
is the safety gate for a later destructive execution job, it must be corrected before that job is
authorized. This is a small, precise fix — not a rejection of the approach.

## FINDINGS

### Scripted eval gates (`review/eval_results.json`, verified present)
- `risk_tier_assignment`: **pass**, tier **HIGH** (correct for secrets/auth + history work).
- `write_scope_check`: **pass**.
- `secret_scan`: **pass** (no secret values in output).

### Independent verification I performed
- **Recovery file still tracked in `mqengine`:** `git ls-files | grep -ic recovery` → **1**; exact
  match on `PyPI-Recovery-Codes-...txt` → 1. File remains in HEAD. (Did not open it.)
- **`mqengine` still has no `.gitignore`; tracks 11 `.pyc` + 5 `mqengine.egg-info/` files.**
- **`mqnode_cloud` still has no `.gitignore`.**
- **Confirm-only repos verified:** `mqnode_test2` → `.gitignore` present, `.env` ignored + untracked;
  `mqchain-console` → `.gitignore` present, `.env.local` ignored + untracked. Plan's Change 4 & 5
  ("no change, confirm only") are factually correct.
- **This planning job wrote nothing to any product repo** (only `jobs/active/MQAI-0002B/` in the MQAI
  repo was written).

### F1 — BLOCKING: RP1 validation check is a case-sensitive false pass
`validation_checklist.md` RP1 proposes:
```
git ls-files | grep -c recovery   -> 0 (no longer tracked)
```
The tracked filename is `PyPI-Recovery-Codes-...` (capital **R**). `grep -c recovery` is
case-sensitive and returns **0 even while the file is tracked** (verified live: `grep -c` → 0,
`grep -ic` → 1). This check therefore passes *regardless of whether remediation occurred* — a false
confirmation on the most critical item (removing the exposed secret file).
- **Fix:** use `git ls-files | grep -ic recovery` (case-insensitive) or, better, an exact/anchored
  match: `git ls-files -- '*[Rr]ecovery*'` or `git ls-files -- 'PyPI-Recovery-Codes-*.txt'`, and
  assert the count is 0 only *after* `git rm --cached` runs.

### F2 — Change/validation completeness gap (`mqengine` tracked bytecode)
`validation_checklist.md` RP2 expects `git ls-files '*.pyc'` → 0 "after `git rm --cached` cleanup",
but the proposed changes (RP1 / Change 2) only `git rm --cached` the **recovery file**. A `.gitignore`
does **not** untrack already-tracked files, so the 11 `.pyc` + 5 `egg-info` files would remain
tracked and the RP2 check would fail.
- **Fix:** in `proposed_file_changes.md`, add an explicit step for the execution job:
  `git rm -r --cached __pycache__ '*.pyc' mqengine.egg-info` (index-only; no disk deletion), or scope
  the validation expectation accordingly.

### F3 — Nit: broad ignore globs
`*recovery*`, `*credential*`, `*_token*` are broad and could ignore a legitimately-named future
source file. Acceptable for these repos, but consider anchoring (e.g. `*.recovery`, `*recovery*.txt`)
or a comment noting the intent. Non-blocking.

## Review checklist results
1. **Planning vs execution separation — PASS.** `job.yaml execution_boundary` + plan text state
   approval covers the plan only; execution is a separate HIGH-tier + Cray-authorized job.
2. **Avoids product-repo writes — PASS.** Verified zero product-repo writes by this job.
3. **Avoids reading/printing secret values — PASS.** No secret file opened; filename/metadata only.
4. **PyPI rotation treated as already done — PASS.** Precondition states rotation complete; RP7
   correctly downgraded to optional/LOW because incident response is finished.
5. **`git rm --cached` as untracking not deletion — PASS.** Correctly described; local file retained.
6. **`.gitignore` proposals reasonable — PASS (with F2/F3).** Patterns are correct and sensible;
   see F2 (untracking already-tracked files) and F3 (glob breadth).
7. **`mqnode_test2` & `mqchain-console` confirm-only — PASS.** Verified accurate.
8. **History purge optional & not executed — PASS.** Documented only, not scheduled, correctly
   optional post-rotation, requires separate authorization.
9. **Future execution job HIGH-tier + human-approved — PASS.** Clearly stated and enforced.

## Checklist gates executed
- **cross_layer_violation_check: PASS.** All proposed changes are repo-hygiene only (`.gitignore` +
  index untracking); no cross-layer authorship; no `repo_control/` writes.
- **formula_diff_check: PASS (n/a).** No formulas touched.
- **migration_required_check: PASS (n/a).** No schema touched.
- **lookahead_safety_check: PASS (n/a).** No research logic.

## BOUNDARY_CHECK: pass
Planning-only respected; writes confined to `jobs/active/MQAI-0002B/`; no product-repo edits,
no `git rm`, no `.gitignore` added to product repos, no deletion, no history rewrite.

## SECRET_HANDLING_CHECK: pass
No secret file opened. No secret values in output. Findings are filename/metadata only.

## PLAN_EXECUTION_SEPARATION: pass
Cleanly separated at both the job.yaml and deliverable level.

## REMEDIATION_PLAN_ACCEPTABLE: yes
The remediation strategy (rotate→ignore→untrack→re-audit, history purge optional) is correct and
appropriately staged. Acceptance is conditional on the F1/F2 corrections to the validation checklist
and proposed changes before any execution job relies on them.

## EXECUTION_ALLOWED_NOW: no
No remediation may run now. Execution requires: F1/F2 corrected, a separate HIGH-tier execution job,
its own eval gates, Claude review of the executed diff, and explicit Cray authorization.

## REQUIRED_CORRECTIONS
1. **F1 (blocking):** fix the RP1 validation grep to be case-insensitive / anchored, asserting 0
   only after `git rm --cached`.
2. **F2:** add explicit `git rm --cached` for `mqengine` tracked `.pyc` + `egg-info`, or align the
   RP2 validation expectation.
3. **F3 (optional):** tighten or annotate the broad ignore globs.
