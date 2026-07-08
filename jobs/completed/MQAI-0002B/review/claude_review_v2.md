# MQAI-0002B — Claude Re-Review (v2, planning phase)

> Reviewer: Claude. Read-only over planning files. Wrote ONLY this file (`claude_review_v2.md`).
> No remediation, no product-repo writes, no `git rm`, no `.gitignore` added to product repos, no
> deletion, no history rewrite, no secret file opened, no output file edited. Date: 2026-07-09.
> Supersedes: `claude_review.md` (v1, VERDICT=request_changes). v1 left intact for provenance.

---

## VERDICT: approve

All three v1 findings (F1, F2, F3) are fixed. The planning/execution separation still holds. The
plan set is internally consistent and safe to accept **as a plan**; execution remains a separate,
Cray-authorized HIGH-tier job.

## F1_STATUS: fixed
`validation_checklist.md` RP1 now:
- Uses a **case-insensitive / anchored** match — PowerShell
  `(git ls-files | Select-String -Pattern '(?i)PyPI-Recovery-Codes.*\.txt').Count` and Git Bash
  `git ls-files | grep -Ei 'PyPI-Recovery-Codes.*\.txt'`.
- **No `grep -c recovery`** anywhere (the false-pass pattern is gone; an explanatory note documents
  why it was wrong).
- States expected behavior clearly: **≥ 1 before**, **0 after** the execution job's `git rm --cached`.
- `check-ignore` note references the anchored `/PyPI-Recovery-Codes*.txt` pattern, not `*recovery*`.

## F2_STATUS: fixed
Already-tracked generated artifacts are now explicitly handled:
- New **RP2G** (`validation_checklist.md`) and **Change 2b** (`proposed_file_changes.md`) target
  tracked `__pycache__/`, `*.pyc`, and `mqengine.egg-info/` via `git rm --cached -r` (index-only, no
  disk deletion). This matches the counts I verified live in v1 (11 `.pyc`, 5 `egg-info`).
- Both files (and RP2's note) state plainly that **`.gitignore` only prevents future tracking and
  does not untrack already-committed files**.
- The untracking command is marked **EXECUTION JOB ONLY — do NOT run now**; execution stays future-only.
- Post-execution validation added: `git ls-files | grep -Ei` for `\.pyc$`, `__pycache__/`,
  `mqengine\.egg-info/` → empty.

## F3_STATUS: fixed
Broad globs removed from both proposed `.gitignore` files:
- Dropped `*recovery*`, `*credential*`, `*_token*`, `*.keystore`, `id_rsa`, `id_dsa`.
- Recovery coverage is now **anchored**: `/PyPI-Recovery-Codes*.txt` + `/pypi-recovery-codes*.txt`.
- Secret coverage is **scoped to concrete extensions**: `.env`, `.env.*`, `!.env.example`, `*.pem`,
  `*.key`, `*.p12`, `*.pfx`, `*.secret`, `*.token`. Reasonable and low-risk of ignoring legit source.

## Planning/execution separation — holds
- `job.yaml` remains planning-only (`product_repo_writes: false`, `remediation_execution: false`).
- `remediation_plan.md` Rev-2 note + Precondition + Consensus sections all state execution (RP1, RP2,
  RP2G, RP3, RP6, and any RP7) is a **separate HIGH-tier execution job** requiring its own eval gates,
  Claude review of the executed diff, and explicit Cray authorization.
- RP7 (history purge) remains **documented only, optional, post-rotation, LOW priority** — not scheduled.

## Checklist gates executed
- **cross_layer_violation_check: PASS** — hygiene-only (`.gitignore` + index untracking); no
  cross-layer authorship; no `repo_control/` writes.
- **formula_diff_check: PASS (n/a)** · **migration_required_check: PASS (n/a)** ·
  **lookahead_safety_check: PASS (n/a)**.

## Scripted eval gates
Per `review/eval_results.json`: `risk_tier_assignment` pass (HIGH), `write_scope_check` pass,
`secret_scan` pass. (No re-run needed; output files only edited within `output/`.)

## BOUNDARY_CHECK: pass
Re-review was read-only; only `claude_review_v2.md` written. Plan asserts no product-repo writes; no
forbidden action taken.

## SECRET_HANDLING_CHECK: pass
No secret file opened. No secret values in output. The recovery **filename** appears (metadata only,
consistent with MQAI-0002 handling); no contents.

## PLAN_EXECUTION_SEPARATION: pass
Cleanly separated at job.yaml and deliverable level; execution gated behind a separate authorized job.

## REMEDIATION_PLAN_ACCEPTABLE: yes
Strategy is correct and now internally consistent (rotate→ignore→untrack file→untrack generated
artifacts→confirm→re-audit; history purge optional). Validation checks are sound and will actually
distinguish remediated from non-remediated state.

## EXECUTION_ALLOWED_NOW: no
No remediation may run now. Execution requires a separate HIGH-tier execution job with its own eval
gates, Claude review of the executed diff, and explicit Cray authorization.

## REQUIRED_CORRECTIONS
None. Plan is approved as a plan and is execution-ready pending a separately-authorized execution job.
(Optional, non-blocking: when the execution job runs, prefer creating a working branch per repo and
capture before/after `git ls-files` counts into `reaudit.md`.)
