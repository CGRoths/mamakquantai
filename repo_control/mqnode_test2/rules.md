# mqnode_test2 — Rules

> STATUS: provisional — pending MQAI-0001 verification.
> Layer: MQNODE (data truth). Classification: **protected baseline / current foundation.**

## 1. Access in V0
READ-ONLY. No writes of any kind to this repo in V0.

## 2. Forbidden actions
No refactor, no schema change, no formula change, no merge, no file move.

## 3. Data-truth invariants (canonical intent)

1. **The 10m primitive is the canonical base.** All time-series truth is anchored to the 10-minute
   interval.
2. **Higher intervals derive from 10m.** 1h, 4h, 1d, etc. are computed from the 10m primitive —
   never fetched or stored as independent primitives.
3. **Primitive tables store reusable low-level facts only.** Prices, volumes, and equivalent raw
   facts — nothing else.
4. **Advanced analytics do NOT go into primitive tables.** Derived metrics, indicators, and
   analytics live in their own layer, never mixed into primitives.
5. **Metrics do not call exchange APIs directly.** Metrics read from stored primitives. Only the
   ingestion/feeder path touches exchange APIs.
6. **Missing price is NULL, never a fake zero.** Absence of data must be represented as NULL.
   Never fabricate 0 for a missing observation.
7. **Schema changes require migrations.** No ad-hoc schema mutation. Every schema change ships with
   a migration.
8. **Checkpoints advance only after successful writes.** An ingestion checkpoint moves forward only
   once the corresponding write has succeeded — never optimistically.

## 4. Risk posture
Default **HIGH** until cartography verifies exact critical paths. See `critical_files.md`, `risk.md`.

## 5. Change protocol (future tiers)
Any future write requires: isolated candidate → tests → data checks → Claude review → Cray approval.

## 6. Pointers
`map.md` (placeholder), `critical_files.md`, `risk.md`, `eval_plan.md`,
`skills/mqnode_data_guard.md`.
