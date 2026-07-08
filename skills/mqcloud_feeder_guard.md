# Skill: mqcloud_feeder_guard

> Guard for work touching the MQNODE cloud feeder (`mqnode_cloud`).

## When to apply
Any job that targets, reads, or reasons about `mqnode_cloud`.

## Invariants to enforce (from feeder_contract.md + rules.md)
1. Feeder supplies primitives; it does not own advanced analytics.
2. 10m primitive is canonical; higher intervals derived downstream.
3. Missing price is NULL, never fake zero.
4. Checkpoints advance only after successful writes.
5. Exchange-API access confined to the ingestion path.
6. The feeder contract is a governed cross-repo boundary.

## V0 posture
READ-ONLY. Feeder handles API auth → high secret sensitivity; any credential in output = fail.

## Review questions
- Would this change break the feeder contract consumed by the baseline?
- Are exchange-API calls confined to ingestion?
- Is checkpoint-safety preserved?
- Any secrets/tokens present?
