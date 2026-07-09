# MQAI-0002C — Review Requirements

> SCAFFOLD. Defines what MUST exist in `review/` before any product-repo change is committed/pushed.
> This job is HIGH-tier: the full consensus chain is mandatory. Nothing here is satisfied yet.

## Required review artifacts (in order)
1. `claude_scaffold_review.md` — review of this scaffold (W1–W4). Must reach `approve_scaffold`.
2. `eval_results.json` — scripted gates: `risk_tier_assignment` (HIGH), `write_scope_check`
   (MQAI folder only — see V9 caveat), `secret_scan`, `cross_layer_violation_check`. All pass.
3. `claude_review.md` — Claude review of the PROPOSED execution (allowed_writes, execution_plan,
   validation_plan, rollback_plan). Verdict block required.
4. **`cray_execution_approval.md` — Gate A.** Explicit Cray approval authorizing BRANCH-LOCAL
   remediation work + diff capture ONLY. Flips `execution_authorized` → true. Does NOT authorize
   commit/push.
5. `output/staged_diff.md` + V9 capture files — produced during the Gate-A window.
6. `claude_review_executed.md` — Claude review of the ACTUAL staged diff. Confirms the diff matches
   the approved plan exactly and V1–V10 pass. `DIFF_MATCHES_APPROVED_PLAN: yes` required.
   **Secret-safe (S1):** this review MUST rely on metadata-only captures (`--name-status` / `--stat`
   / `--summary`) for the recovery-code removal — NOT a file-content diff. The reviewer must verify
   captures are sanitized (no unrestricted `git diff --cached`; `.gitignore` full diff OK; secret-like
   paths excluded) and that V10's leak scan of `output/`+`review/` passed. If any recovery-code /
   secret content appears in a capture → `DIFF_MATCHES_APPROVED_PLAN: no`, reject, quarantine.
7. `gpt_synthesis.md` — GPT synthesis reconciling the proposed-plan review and the executed-diff
   review.
8. **`cray_final_approval.md` — Gate B.** Explicit Cray approval authorizing COMMIT. Flips
   `commit_authorized` → true. Push only if separately authorized.

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

## Hard gate (mandatory ordering — two Cray gates)
```
scaffold reviewed (approve_scaffold)
  → eval_gates pass
    → claude_review (proposed) = approve
      → [GATE A] cray_execution_approval  (execution_authorized -> true)
        → apply changes on remediation branch; stage; capture staged_diff + V9 evidence  (NO commit)
          → V1–V10 validation pass (incl. V10 secret-safe / no-leak scan)
            → claude_review_executed (sanitized diff matches plan) = approve
              → gpt_synthesis = approve
                → [GATE B] cray_final_approval  (commit_authorized -> true)
                  → commit on branch   (push only if separately authorized)
```
> Gate A opens the branch-local write window ONLY. Gate B is a separate, explicit approval that
> alone authorizes commit. Neither gate is implied by the other.

## Non-negotiables carried into review
- No secret file opened; no secret values in any artifact (filename/metadata only).
- No disk deletion; untracking is index-only.
- No git history rewrite; no force-push.
- `mqnode_test2` and `mqchain-console` remain confirm-only (zero writes).
- Builder cannot approve its own execution; Cray approval is explicit and separate.
