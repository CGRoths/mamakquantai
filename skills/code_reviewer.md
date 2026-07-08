# Skill: code_reviewer

> Used by: Claude (reviewer). Reviews staged output in `jobs/active/<id>/output/`.

## Objective
Independently verify that staged output is correct, in-scope, boundary-safe, and promotable —
before Cray inspects it.

## Hard constraints
- Write ONLY to `jobs/active/<id>/review/`.
- Review the ACTUAL output, not just the plan (especially for medium/high tiers).
- Do not promote. Recommendation only; Cray decides.

## Inputs
- `output/` (all staged deliverables) + `output/BUILD_NOTES.md`.
- `review/eval_results.json` (scripted gate results).
- Relevant `skills/*_guard.md` and `repo_control/<repo>/rules.md`.

## Checklist gates Claude executes (V0)
- `cross_layer_violation_check` — no foreign-layer authorship.
- `formula_diff_check` — flag any metric/formula change (HIGH).
- `migration_required_check` — schema touch requires migration.
- `lookahead_safety_check` — research point-in-time safety.

## Verdict block (write to review/claude_review.md)
```
VERDICT: approve | request_changes | reject
FINDINGS: [ ... ]
BOUNDARY_CHECK: pass | fail
PROMOTE_RECOMMENDATION: yes | no
```

## Quality bar
No fabrication, evidence-based findings, explicit boundary verdict, clear promote recommendation.
