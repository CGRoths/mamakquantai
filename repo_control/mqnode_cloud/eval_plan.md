# mqnode_cloud — Eval Plan

> STATUS: provisional — to be refined once `map.md` exists.

## Gates applied to jobs targeting this repo

| Gate | V0 behavior |
|------|-------------|
| risk_tier_assignment | No `critical_files.md` yet → default HIGH (conservative). |
| write_scope_check | Assert zero writes to this repo in V0; output stays in job folder. |
| secret_scan | Scan output for keys/tokens/creds (feeder handles API auth → high sensitivity). |
| cross_layer_violation_check | Output must not assert non-MQNODE ownership. |
| formula_diff_check | N/A read-only; required for future formula-touching jobs. |
| migration_required_check | N/A read-only; required if schema/contract paths touched. |
| lookahead_safety_check | Note if delivery timing affects downstream lookahead. |

## Feeder-specific checks (future, when writes allowed)

- Feeder contract preserved (`feeder_contract.md`).
- Missing data as NULL; no fabricated zeros.
- Checkpoint advances only after successful writes.
- Exchange-API access confined to ingestion path.
