# MQAI-0002C — Cray Gate A Execution Approval

DECISION: approve_gate_a_execution_only

APPROVED_BY: Cray
DATE: 2026-07-09
GATE: A (execution — branch-local only)

## Basis
- Scaffold approved (`claude_scaffold_review_v3.md` = approve_scaffold).
- Scripted eval gates pass (`eval_results.json`: risk_tier HIGH, write_scope, secret_scan) —
  noting the V0 write_scope_check audits only the MQAI job folder; product-repo scope is enforced
  by V9.
- Proposed-execution review approved (`claude_proposed_execution_review.md` = approve_for_gate_a).
- PyPI recovery codes already rotated by Cray.

## Scope authorized (Gate A)
- Gate A authorizes **branch-local remediation work only**.
- Allows creating dedicated remediation branches in the approved product repos (`mqengine`,
  `mqnode_cloud`).
- Allows writing ONLY the exact paths listed in `allowed_writes.md`.
- Allows staging and capturing actual diffs for review (`output/staged_diff.md`).
- Allows running V1–V9 validation and capturing evidence to `jobs/active/MQAI-0002C/output/`.

## Still forbidden under Gate A
- NO commit.
- NO push.
- NO git history rewrite.
- NO secret-content inspection.
- NO writes to `mqnode_test2` or `mqchain-console` (confirm-only, zero-write).
- NO product-repo paths outside `allowed_writes.md`.
- NO removal of pre-existing untracked secret/user/product files.

## Gate B remains BLOCKED
- `commit_authorized` MUST remain false.
- Product-repo commits/pushes require ALL of: V1–V9 validation pass + executed-diff review
  (`claude_review_executed.md`) + GPT synthesis (`gpt_synthesis.md`) + Cray final approval
  (`cray_final_approval.md`).
- Gate A completing branch work does NOT imply Gate B.

## job.yaml effect
- execution_authorized: true   (Gate A granted)
- commit_authorized: false     (Gate B pending)
- status: active
