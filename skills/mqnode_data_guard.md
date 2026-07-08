# Skill: mqnode_data_guard

> Guard for work touching MQNODE (`mqnode_test2`, `mqnode_cloud`). Data truth.

## When to apply
Any job that targets, reads, or reasons about MQNODE repos.

## Invariants to enforce (from repo_control/mqnode_test2/rules.md)
1. 10m primitive is the canonical base.
2. Higher intervals derive from 10m — never stored as independent primitives.
3. Primitive tables store reusable low-level facts only.
4. Advanced analytics never enter primitive tables.
5. Metrics never call exchange APIs directly (read stored primitives).
6. Missing price is NULL, never fake zero.
7. Schema changes require migrations.
8. Checkpoints advance only after successful writes.

## V0 posture
`mqnode_test2` is the protected baseline: READ-ONLY. Flag any output implying a write, refactor,
schema change, or formula change as a violation.

## Review questions
- Does the output preserve NULL semantics for missing data?
- Does it keep analytics out of primitives?
- Does it avoid direct exchange-API coupling in metric paths?
- Are schema touches accompanied by migrations?
