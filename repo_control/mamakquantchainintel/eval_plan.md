# mamakquantchainintel — Eval Plan

> STATUS: provisional — to be refined once `map.md` exists.
> V0 scope: `mqchain-console` only.

## Gates applied to jobs targeting this repo

| Gate | V0 behavior |
|------|-------------|
| risk_tier_assignment | No `critical_files.md` yet → default HIGH for registry paths. |
| write_scope_check | Assert zero writes to this repo in V0; output stays in job folder. |
| secret_scan | Scan output for keys/tokens/creds. |
| cross_layer_violation_check | Only MQCHAIN may author label/registry truth. |
| formula_diff_check | N/A unless label scoring formulas exist. |
| migration_required_check | Required if registry schema paths touched. |
| lookahead_safety_check | Labels consumed by research must be point-in-time safe. |

## Label/registry-specific checks (future, when writes allowed)

- Single canonical registry; no shadow stores.
- Entity ID stability and referential integrity.
- Auditable provenance on label changes.
