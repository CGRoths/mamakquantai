# COMMANDS

V0 is semi-manual CLI with PowerShell wrappers. Commands below are the intended operating loop.
Paths assume you run from the MQAI root: `C:\MAMAKQUANT\mamakquantai`.

> Prerequisite: fill `LOCAL_ENV.md` with local clone paths before running any job that touches repos.

## Run a Codex build/map job

```powershell
.\orchestrator\run_codex_job.ps1 -JobId MQAI-0001
```

What it does (V0):
- Loads `jobs/active/<JobId>/job.yaml`.
- Packs context (repo_control + skill guide) and prints the Codex briefing.
- After Codex writes to `output/`, validates write scope.

## Run the eval gates

```powershell
.\orchestrator\run_codex_job.ps1 -JobId MQAI-0001 -EvalsOnly
```

Runs scripted gates (`risk_tier_assignment`, `write_scope_check`, `secret_scan`) and records
`review/eval_results.json`. Checklist gates are executed by Claude during review.

## Run a Claude review

```powershell
.\orchestrator\run_claude_review.ps1 -JobId MQAI-0001
```

Prepares the review context and validates that review writes stay in `review/`.

## Cray decision

Manually inspect `output/` and `review/`, then record your decision in:
```
jobs/active/<JobId>/review/cray_decision.md
```
Use an explicit line: `DECISION: approve` or `DECISION: reject`.

## Promotion (human-gated)

Only after evals pass + Claude approves + Cray approves. Promotion copies approved output into
`repo_control/<repo>/`. Agents may never run this step.

## Job status transitions

- `jobs/active/` → `jobs/completed/` on approval + promotion.
- `jobs/active/` → `jobs/failed/` on eval fail or rejection (append to `memory/failure_taxonomy.yaml`).
