# mqnode_cloud — Rules

> STATUS: provisional — pending MQAI-0001 verification.
> Layer: MQNODE (data truth). Role: cloud feeder.

## 1. Access in V0
READ-ONLY. No writes of any kind to this repo in V0.

## 2. Forbidden actions
No refactor, no schema change, no formula change, no merge, no file move.

## 3. Feeder invariants (canonical intent)

1. **Feeds data truth, does not own analytics.** The cloud feeder supplies primitives to MQNODE; it
   does not compute advanced analytics.
2. **10m primitive is canonical.** The feeder produces/relays 10m-aligned primitives; higher
   intervals are derived downstream, not fabricated here.
3. **Missing price is NULL, never fake zero.** The feeder must never invent 0 for absent data.
4. **Checkpoints advance only after successful writes.** No optimistic checkpoint advancement.
5. **Exchange-API access is confined to the ingestion path.** Downstream consumers read stored
   primitives, not exchange APIs.
6. **Feeder contract is a boundary.** See `feeder_contract.md` — the shape/semantics of what the
   feeder delivers is a governed interface.

## 4. Risk posture
Default **HIGH** until cartography verifies exact critical paths (`feeder_contract.md`).

## 5. Change protocol (future tiers)
Isolated candidate → tests → data checks → Claude review → Cray approval.

## 6. Pointers
`map.md` (placeholder), `feeder_contract.md`, `eval_plan.md`, `skills/mqcloud_feeder_guard.md`.
