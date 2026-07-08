# MQAI-0002B — Cray Decision

DECISION: approve_plan_only

APPROVED_BY: Cray

DATE: 2026-07-09

## Scope Approved

MQAI-0002B is approved **as a remediation plan only**.

- This approval accepts the remediation plan, proposed file changes, and validation checklist as a
  sound, internally-consistent plan.
- **Execution is NOT authorized inside MQAI-0002B.** No product-repo write, no `git rm`, no
  `.gitignore` addition to any product repo, no file deletion, no git history rewrite, and no
  reading/printing of secret values may occur under this job.

## Basis

- Scripted eval gates: pass (risk_tier HIGH, write_scope, secret_scan).
- Claude review v1: request_changes (F1/F2/F3).
- Builder corrected F1, F2, F3 (planning files only).
- Claude review v2: approve.
- GPT synthesis: approve_plan_only; EXECUTION_ALLOWED_NOW: no.
- PyPI recovery codes already rotated manually by Cray.

## Execution Boundary (mandatory)

Any product-repo remediation must happen ONLY through a separate HIGH-tier job:

**MQAI-0002C — Security Remediation Execution**

MQAI-0002C must contain, before any product-repo change is committed:
- exact allowed write paths,
- exact commands,
- validation checks (including the case-insensitive recovery-file check),
- rollback notes,
- eval gates,
- Claude review of the executed diff,
- GPT synthesis,
- explicit Cray approval.

## Closeout Authorization

- Move MQAI-0002B to jobs/completed/MQAI-0002B.
- Update job.yaml status to completed.
- Do NOT scaffold MQAI-0002C yet.
- Update memory/decisions.md and memory/lessons_learned.md.
