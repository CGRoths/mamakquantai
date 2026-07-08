# MQAI-0002C — Review Requirements

> SCAFFOLD. Defines what MUST exist in `review/` before any product-repo change is committed/pushed.
> This job is HIGH-tier: the full consensus chain is mandatory. Nothing here is satisfied yet.

## Required review artifacts (in order)
1. `eval_results.json` — scripted gates: `risk_tier_assignment` (HIGH), `write_scope_check`,
   `secret_scan`, `cross_layer_violation_check`. All must pass.
2. `claude_review.md` — Claude review of the PROPOSED execution (this scaffold: allowed_writes,
   execution_plan, validation_plan, rollback_plan). Verdict block required.
3. `claude_review_executed.md` — Claude review of the ACTUAL staged diff (from
   `output/staged_diff.md`) BEFORE commit. Confirms the diff matches the approved plan exactly.
4. `gpt_synthesis.md` — GPT synthesis reconciling the plan review and the executed-diff review.
5. `cray_decision.md` — explicit Cray **execution** approval (separate from the MQAI-0002B plan
   approval). Only this flips `execution_authorized` to true.

## Verdict block format (for Claude reviews)
```
VERDICT: approve | request_changes | reject
FINDINGS:
BOUNDARY_CHECK: pass | fail
SECRET_HANDLING_CHECK: pass | fail
DIFF_MATCHES_APPROVED_PLAN: yes | no    # for the executed-diff review
EXECUTION_ALLOWED_NOW: yes | no
REQUIRED_CORRECTIONS:
```

## Hard gate (mandatory ordering)
```
scaffold reviewed
  → eval_gates pass
    → claude_review (proposed) = approve
      → [AUTHORIZED WINDOW] apply changes on branch, stage diff
        → claude_review_executed (diff matches plan) = approve
          → gpt_synthesis = approve
            → cray_decision = approve (execution)
              → commit on branch  (push only if separately authorized)
```

## Non-negotiables carried into review
- No secret file opened; no secret values in any artifact (filename/metadata only).
- No disk deletion; untracking is index-only.
- No git history rewrite; no force-push.
- `mqnode_test2` and `mqchain-console` remain confirm-only (zero writes).
- Builder cannot approve its own execution; Cray approval is explicit and separate.
