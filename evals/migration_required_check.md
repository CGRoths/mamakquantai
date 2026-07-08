# Eval Gate: migration_required_check

> Type: checklist-driven in V0. Executed by Claude during review.

## 1. Purpose
Ensure any schema change ships with a corresponding migration. No ad-hoc schema mutation.

## 2. Inputs
- Staged `output/`.
- Known schema locations (from verified `map.md`; provisional until then).

## 3. Checks
- Does the output touch a schema/DDL/table definition?
- If yes: is there a matching migration file?
- Does the change respect data-truth invariants (NULL semantics, primitive scope)?

## 4. Output
```json
{ "gate": "migration_required_check", "status": "pass|fail|n/a", "schema_touches": [] }
```

## 5. V0 applicability
`n/a` for read-only jobs. Mandatory for any job touching MQNODE/MQCHAIN schema paths.

## 6. Notes
V1: auto-detect schema deltas and require a migration artifact before promotion.
