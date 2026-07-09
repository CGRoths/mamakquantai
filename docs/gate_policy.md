# MQAI Gate Policy (V1)

Implemented in `orchestrator/gate_policy.py`. Required gates per risk tier (ordered):

| Tier | Required gates |
|------|----------------|
| LOW | plan → validation → closeout |
| MEDIUM | plan → validation → executed_diff_review → final_commit → closeout |
| HIGH | plan → execution → validation → executed_diff_review → synthesis → final_commit → closeout |
| CRITICAL | same as HIGH + mandatory human stop before any product-repo mutation |

`push` is always a **separate, explicit, optional** gate. It is NEVER inferred from commit approval
and is never part of the required-to-close set.

## Human-approval gates
`execution`, `final_commit`, `push`, `closeout` require an explicit approval artifact
(`review/cray_*_approval.md` or the generic `review/approved_<gate>.md` written by `mqai approve`).

## Gate status values
`done` · `pending` (evidence not yet produced) · `awaiting_approval` (evidence ready, waiting on Cray)
· `na` · `blocked`.

## Next action
The engine returns the first not-`done` required gate. If it is a human gate and its pre-approval
evidence exists, the action is `AWAIT Cray approval for '<gate>'`; otherwise it is `NEXT: produce
evidence for '<gate>'`.

## Blocked actions (always surfaced)
- product-repo writes without execution approval
- commit without final approval
- push (never inferred)
- any product-repo mutation when the job does not allow product writes

## Risk tiering integrity
Tier comes from `job.yaml risk_tier` (and, for product jobs, from path matching against
`critical_files.md` in the product-repo execution job). Agents do not self-assign tier.
