# mqengine — Lookahead Rules

> STATUS: provisional — pending MQAI-0001 verification.
> Basis for the `lookahead_safety_check` eval.

## Principle

No future information may influence a computation timestamped at or before its own point in time.
Lookahead bias silently invalidates research; it is treated as a first-class safety hazard.

## Rules (canonical intent)

1. **Point-in-time correctness.** Any feature/metric at time `t` uses only data available at `t`.
2. **No forward-fill from the future.** Fill only from past observations; never backfill from later
   data into an earlier timestamp.
3. **Label timing.** Labels/targets must be shifted so that inputs never overlap the outcome window.
4. **Temporal partition integrity.** Train precedes validation precedes test in time; no shuffling
   across the time boundary.
5. **Derived-interval consistency.** Higher intervals derived from the 10m primitive must close only
   after the interval completes (no partial-bar leakage).
6. **Missing data.** NULL is respected as unknown; never impute using future values.

## Enforcement (V0)

- Checklist-driven during Claude review (`lookahead_safety_check`).
- Any formula/research-logic change flagged HIGH; escalate to full consensus.

## Open questions (for MQAI-0001)

- Exact feature-construction code paths.
- Where partitioning/shifting is implemented.
- Any existing lookahead tests in the repo.
