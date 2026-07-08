# Eval Gate: formula_diff_check

> Type: checklist-driven in V0. Executed by Claude during review.
> High-risk gate: metric/formula changes trigger HIGH consensus.

## 1. Purpose
Detect any change to a metric or formula definition. Formula drift silently corrupts research and
downstream decisions.

## 2. Inputs
- Staged `output/` (proposed changes).
- Known formula/metric locations (from `map.md` once verified; provisional until then).

## 3. Checks
- Does the output add/modify/remove a metric or formula?
- If yes: is it justified, documented, and escalated to HIGH consensus?
- Are before/after formula definitions explicitly shown?

## 4. Output
```json
{ "gate": "formula_diff_check", "status": "pass|fail|n/a", "changed_formulas": [] }
```

## 5. V0 applicability
`n/a` for read-only jobs (e.g. MQAI-0001). Mandatory for any code job touching MQENGINE metrics or
MQNODE derived-metric paths.

## 6. Notes
V1: AST/diff-based automated detection of formula changes.
