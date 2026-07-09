# Skill: incident_diagnoser

> Role: triage a failed/blocked job or a failing gate.

## Do
- Read `review/eval_results.json`, `output/*`, and the latest review artifacts.
- Identify the failing gate, the evidence gap, and the safest recovery per `rollback_plan.md`.
- Classify the failure (secret_leak / write_scope_violation / cross_layer / missing_migration /
  lookahead_bias / scope_creep / fabrication) and propose a `failure_taxonomy.yaml` entry.

## Don't
- Don't attempt recovery that requires product-repo mutation without an authorized job.
- Don't inspect secret contents while diagnosing; metadata only.
