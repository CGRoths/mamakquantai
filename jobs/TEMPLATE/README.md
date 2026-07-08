# Job Template

Copy this folder to `jobs/active/<MQAI-XXXX>/` to start a new job.

## Folder shape
```
jobs/active/<MQAI-XXXX>/
├── job.yaml     # spec (see this template's job.yaml)
├── output/      # Codex writes here ONLY
└── review/      # Claude writes here ONLY (+ cray_decision.md)
```

## Rules
- Fill `job.yaml` fully before running.
- Risk tier is set by `risk_tier_assignment` (path-derived), not by hand.
- Agents never write outside their allowed folder; agents never promote.
- On approval: move to `jobs/completed/`. On failure/rejection: move to `jobs/failed/`
  and append to `memory/failure_taxonomy.yaml`.
