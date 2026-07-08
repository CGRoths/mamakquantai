# mqnode_cloud — Feeder Contract

> STATUS: provisional — pending MQAI-0001 verification.
> This is a governed interface boundary between the cloud feeder and the MQNODE baseline.

## Purpose

Defines the contract for what the cloud feeder delivers into the data-truth layer. Changes to this
contract are high-risk because both `mqnode_cloud` (producer) and `mqnode_test2` (consumer baseline)
depend on it.

## Contract intent (to be verified by MQAI-0001)

1. **Granularity:** primitives are 10m-aligned. The feeder does not emit ad-hoc intervals as
   primitives.
2. **Fact scope:** primitives carry low-level reusable facts only (price, volume, equivalent raw
   observations). No advanced analytics.
3. **Missing data:** absent observations are delivered/stored as NULL, never fabricated zeros.
4. **Ordering & checkpoints:** delivery is checkpoint-safe; a checkpoint advances only after the
   corresponding write succeeds.
5. **API confinement:** exchange-API calls occur only in the feeder ingestion path; consumers read
   stored primitives.
6. **Idempotency / dedupe:** re-delivery of the same 10m bar must not corrupt truth (exact semantics
   TBD by cartography).

## Governance

- Any change to this contract → HIGH consensus mode.
- Contract fields will be pinned to real code paths after MQAI-0001 maps both repos.

## Open questions (for MQAI-0001)

- Exact serialization / schema of delivered primitives.
- Retry / backfill semantics.
- How gaps are signaled vs NULLs.
