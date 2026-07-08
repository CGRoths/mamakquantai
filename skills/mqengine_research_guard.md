# Skill: mqengine_research_guard

> Guard for work touching MQENGINE (`mqengine`). Research validation.

## When to apply
Any job that targets, reads, or reasons about `mqengine`.

## Invariants to enforce (from research_protocol.md + lookahead_rules.md)
1. Research reads truth; it does not redefine data or labels.
2. Lookahead safety is mandatory — no future info at time `t`.
3. Deterministic, reproducible validation (seeds recorded).
4. Metric formulas are HIGH-risk — any change gated by formula_diff_check + HIGH consensus.
5. No direct exchange-API calls; read stored primitives.
6. Temporal partition integrity (train < validation < test in time).

## V0 posture
READ-ONLY. Treat any formula or lookahead-sensitive path as HIGH.

## Review questions
- Any lookahead leakage (forward-fill, label overlap, shuffled partitions)?
- Any metric/formula change? → escalate HIGH.
- Is the run reproducible?
- Any direct exchange-API coupling?
