# mqengine — Research Protocol

> STATUS: provisional — pending MQAI-0001 verification.
> Layer: MQENGINE (research validation).

## 1. Access in V0
READ-ONLY. No writes of any kind to this repo in V0.

## 2. Role
MQENGINE owns **research validation** — the methodology by which candidate signals/strategies are
tested. It does not own data truth (MQNODE), label truth (MQCHAIN), or execution (MQBOT).

## 3. Research invariants (canonical intent)

1. **Reads truth, does not redefine it.** Research consumes MQNODE data and MQCHAIN labels; it does
   not mutate them.
2. **Lookahead safety is mandatory.** No future information may leak into any point-in-time
   computation. See `lookahead_rules.md`.
3. **Deterministic, reproducible validation.** Same inputs → same result. Random seeds fixed and
   recorded.
4. **Metric formulas are high-risk.** Any change to a metric/formula requires HIGH consensus and
   `formula_diff_check`.
5. **No direct exchange-API calls.** Research reads stored primitives, never live exchange APIs.
6. **Separation of train/validation/test.** Data partitions must respect temporal ordering.

## 4. Risk posture
Default **HIGH** for anything touching formulas or lookahead-sensitive logic. Otherwise MEDIUM
pending cartography.

## 5. Change protocol (future tiers)
Isolated candidate → tests → lookahead check → Claude review → Cray approval.

## 6. Pointers
`map.md` (placeholder), `lookahead_rules.md`, `eval_plan.md`, `skills/mqengine_research_guard.md`.
