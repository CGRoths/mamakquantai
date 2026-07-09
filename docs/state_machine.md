# MQAI Job State Machine (V1)

State is **inferred** from `job.yaml` + files in `review/` and `output/` — generic across job types,
not hardcoded to any job id. Implemented in `orchestrator/job_state.py`.

## States
`drafted → scaffolded → plan_reviewed → plan_approved → execution_ready → execution_authorized →
executed → validation_passed → review_passed → synthesis_required → synthesis_done →
final_approval_required → commit_authorized → committed → post_audit_required → completed`
plus terminal/override states `failed`, `blocked`.

## Evidence signals (examples)
| Signal | Detected from |
|--------|---------------|
| scaffolded | `job.yaml` exists |
| plan_reviewed | `review/*review*.md` |
| plan_approved | `review/cray_decision.md` / `*scaffold*approval*` / `approved_plan.md` |
| execution_authorized | `review/cray_execution_approval*.md` / `approved_execution.md` / flag |
| executed | `output/execution_summary.md` |
| validation_passed | `output/validation_results.md` |
| review_passed | `review/*executed_diff*review*.md` |
| synthesis_done | `review/gpt_synthesis*.md` |
| commit_authorized | `review/cray_final_approval*.md` / `approved_final_commit.md` / flag |
| committed | `output/commit_records.md` |
| completed | job in `jobs/completed/` or `status: completed` |
| failed / blocked | `jobs/failed/`, `status`, or a `*blocked*.md` marker |

## Inference rule
Terminal overrides (failed → blocked → completed) are checked first. Otherwise the engine returns the
**furthest-progressed** state whose evidence exists (a descending ladder from `committed` down to
`scaffolded`, else `drafted`). This is a documented heuristic; it favors honest under-claiming — an
approval artifact alone does not imply the corresponding work product exists.
