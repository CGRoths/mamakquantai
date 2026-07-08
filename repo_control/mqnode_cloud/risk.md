# mqnode_cloud — Risk

> STATUS: provisional — pending MQAI-0001 verification.

## Overall posture

**HIGH.** Owns the feeder path into data truth. A defective feeder corrupts primitives at the source,
which propagates system-wide.

## Why high

- Feeder is the entry point for data truth; errors are systemic.
- Exchange-API access lives here; secrets/auth exposure risk.
- Feeder contract is a cross-repo boundary (`feeder_contract.md`).

## Tiering in V0

- Any job targeting this repo defaults to HIGH via `critical_files` policy (conservative).
- MQAI-0001 is read-only; no writes occur here.

## Escalation

Any future feeder or contract change → HIGH consensus mode + deterministic gates + Cray approval.
