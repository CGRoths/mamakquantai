# Eval Gate: cross_layer_violation_check

> Type: checklist-driven in V0 (path rules). Executed by Claude during review.
> Basis: `company_brain/separation_of_concerns.md`.

## 1. Purpose
Ensure a job scoped to one layer does not author or claim ownership in another layer's paths.

## 2. Inputs
- `job.yaml` (target layer/repo).
- Staged `output/`.
- Ownership table in `separation_of_concerns.md`.

## 3. Checks
- Output does not write into another layer's owned paths.
- Output does not assert ownership/authority it doesn't have (e.g. research authoring registry
  truth).
- No writes to `repo_control/` (promotion is human-gated).

## 4. Output
```json
{ "gate": "cross_layer_violation_check", "status": "pass|fail", "violations": [] }
```

## 5. Fail behavior
Any violation → FAIL → route to `jobs/failed/`, append `cross_layer_violation` to failure taxonomy.

## 6. Notes
V1: automated ownership graph derived from verified `map.md` files.
