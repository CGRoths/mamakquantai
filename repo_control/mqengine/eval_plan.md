# mqengine — Eval Plan

> STATUS: provisional — to be refined once `map.md` exists.

## Gates applied to jobs targeting this repo

| Gate | V0 behavior |
|------|-------------|
| risk_tier_assignment | No `critical_files.md` yet → default HIGH for formula/lookahead paths. |
| write_scope_check | Assert zero writes to this repo in V0; output stays in job folder. |
| secret_scan | Scan output for keys/tokens/creds. |
| cross_layer_violation_check | Output must not assert MQNODE/MQCHAIN ownership. |
| formula_diff_check | Required for any metric/formula change (HIGH). |
| migration_required_check | N/A unless research persists to schema. |
| lookahead_safety_check | Primary gate for this repo (`lookahead_rules.md`). |

## Research-specific checks (future, when writes allowed)

- Point-in-time correctness; no future leakage.
- Deterministic, reproducible runs (seeds recorded).
- Metric formula changes gated by `formula_diff_check` + HIGH consensus.
- Temporal partition integrity.
