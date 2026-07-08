# Eval Gate: lookahead_safety_check

> Type: checklist-driven in V0. Executed by Claude during review.
> Basis: `repo_control/mqengine/lookahead_rules.md`.

## 1. Purpose
Ensure research logic contains no lookahead bias — no future information influences a point-in-time
computation.

## 2. Inputs
- Staged `output/` (research logic / features / labels).
- `lookahead_rules.md`.

## 3. Checks
- Feature at time `t` uses only data available at `t`.
- No forward-fill from future; NULL never imputed from future values.
- Label timing avoids input/outcome overlap.
- Temporal partition integrity (train < validation < test).
- Derived intervals close only after the interval completes.

## 4. Output
```json
{ "gate": "lookahead_safety_check", "status": "pass|fail|n/a", "concerns": [] }
```

## 5. V0 applicability
`n/a` for read-only mapping jobs. Mandatory for any MQENGINE research-logic job.

## 6. Notes
V1: automated temporal-leakage detection on research code.
