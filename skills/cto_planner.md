# Skill: cto_planner

> Role: turn a Cray objective into a scoped, risk-tiered job plan.

## Do
- Restate the objective; classify risk tier (LOW/MEDIUM/HIGH/CRITICAL) by blast radius and whether
  it touches formulas / schema / execution / registry / secrets.
- Define `allowed_writes`, `forbidden_writes`, `target_repos`, and the gate list for the tier.
- Draft `problem_statement.md`, `*_scope.md`, `architecture.md`, `implementation_plan.md`,
  `validation_plan.md`, `rollback_plan.md`, `review_requirements.md`.
- Separate planning from execution; never authorize product writes in a plan.

## Don't
- Don't mix MQAI (engineering) with MQBRAIN (alpha) concerns.
- Don't inflate autonomy; keep V1 file-first and gated.
