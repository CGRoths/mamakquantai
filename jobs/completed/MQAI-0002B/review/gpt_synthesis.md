# MQAI-0002B — GPT Synthesis

SYNTHESIZER: GPT manual synthesis

DATE: 2026-07-09

## Verdict

SYNTHESIS_VERDICT: approve_plan_only

EXECUTION_ALLOWED_NOW: no

NEXT_REQUIRED_JOB: MQAI-0002C — Security Remediation Execution

## Basis Reviewed

- MQAI-0002B is a HIGH-tier planning job.
- Claude review v1 returned request_changes due to validation false-pass risk.
- Builder corrected F1, F2, and F3.
- Claude review v2 returned approve.
- PyPI recovery-code rotation has already been completed manually by Cray.
- Current MQAI-0002B scope is planning and patch proposal only.

## Synthesis

The remediation plan is now acceptable as a plan.

F1 is fixed because recovery-code tracking validation now uses case-insensitive anchored matching instead of the false-passing case-sensitive `grep -c recovery`.

F2 is fixed because the plan now explicitly handles already-tracked generated artifacts in mqengine, including `.pyc`, `__pycache__`, and `mqengine.egg-info`. The plan correctly states that `.gitignore` prevents future tracking but does not untrack files already committed.

F3 is fixed because broad secret globs were narrowed to scoped patterns. This reduces false positives and avoids accidentally ignoring legitimate source files.

The planning/execution separation is valid. MQAI-0002B must not modify product repos. Actual remediation must be a separate HIGH-tier execution job with explicit Cray approval.

## Approved Plan Scope

The following actions are approved only as a future execution plan:

1. Remove the tracked PyPI recovery-code file from mqengine index/current tree without reading or printing its contents.
2. Add .gitignore coverage to mqengine.
3. Untrack already-tracked generated artifacts in mqengine.
4. Add .gitignore coverage to mqnode_cloud.
5. Confirm mqnode_test2 `.env` remains untracked and gitignored.
6. Confirm mqchain-console `.env.local` remains untracked and gitignored.
7. Re-audit after remediation.
8. Keep history purge optional and post-rotation only.

## Explicit Non-Approval

This synthesis does NOT approve immediate execution.

This synthesis does NOT approve product repo writes inside MQAI-0002B.

This synthesis does NOT approve reading, printing, copying, or opening secret values.

This synthesis does NOT approve git history rewrite.

## Recommendation

Cray may approve and close MQAI-0002B as an accepted remediation plan.

After closeout, create a separate HIGH-tier job:

MQAI-0002C — Security Remediation Execution

That job must contain exact allowed write paths, exact commands, validation checks, rollback notes, eval gates, review, GPT synthesis, and Cray approval before any product repo change is committed.
