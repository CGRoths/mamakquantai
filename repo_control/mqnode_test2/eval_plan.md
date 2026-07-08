# mqnode_test2 — Eval Plan

> STATUS: provisional — to be refined once `map.md` exists.

## Gates applied to jobs targeting this repo

| Gate | V0 behavior |
|------|-------------|
| risk_tier_assignment | Path match vs `critical_files.md` → HIGH (provisional `**`). |
| write_scope_check | Assert zero writes to this repo in V0; all output in job folder. |
| secret_scan | Scan output for keys/tokens/creds. |
| cross_layer_violation_check | Assert output does not assert non-MQNODE ownership. |
| formula_diff_check | N/A for read-only; required for any future formula-touching job. |
| migration_required_check | N/A for read-only; required if schema paths are touched. |
| lookahead_safety_check | N/A (MQENGINE concern); note if data semantics affect lookahead. |

## Data-specific checks (future, when writes are allowed)

- Missing price represented as NULL (never 0).
- 10m primitive integrity; higher intervals derived, not stored as primitives.
- Primitive tables contain low-level facts only (no advanced analytics).
- Checkpoints advance only after successful writes.
- Schema changes accompanied by migrations.
