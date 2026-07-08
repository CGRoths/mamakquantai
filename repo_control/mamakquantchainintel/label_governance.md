# mamakquantchainintel — Label Governance

> STATUS: provisional — pending MQAI-0001 verification.
> Layer: MQCHAIN (entity / label truth). Scope in V0: `mqchain-console`.

## 1. Access in V0
READ-ONLY. No writes of any kind to this repo in V0.

## 2. Role
MQCHAIN owns **entity / label truth** — the canonical registry of entities and their labels. It does
not own data ingestion (MQNODE), research logic (MQENGINE), or execution (MQBOT).

## 3. Label invariants (canonical intent)

1. **Labels are governed truth.** An entity's label is authoritative; downstream layers consume it,
   they do not redefine it.
2. **Canonical registry is the single source.** No shadow label stores. See
   `registry_truth_boundary.md`.
3. **Label changes are auditable.** Provenance and rationale are recorded for label assignments and
   changes.
4. **No lookahead in labels used by research.** Labels consumed by MQENGINE must respect point-in-
   time semantics (coordinate with `mqengine/lookahead_rules.md`).
5. **Stable identifiers.** Entity IDs are stable; renaming/merging entities is a governed,
   high-risk operation.

## 4. Risk posture
Default **HIGH** for anything touching the canonical registry. Otherwise MEDIUM pending cartography.

## 5. Change protocol (future tiers)
Isolated candidate → registry-integrity checks → Claude review → Cray approval.

## 6. Pointers
`map.md` (placeholder), `registry_truth_boundary.md`, `eval_plan.md`,
`skills/mqchain_label_guard.md`.
