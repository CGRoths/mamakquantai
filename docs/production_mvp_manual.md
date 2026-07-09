# MQAI Production Control Plane — MVP Manual (V1)

MQAI is the AI **engineering** control plane for the MamakQuant stack (repo control, job
orchestration, gates, review workflow, promotion governance). It is **not** MQBRAIN (future alpha
intelligence). This MVP (built under MQAI-0005) is file-first, stdlib-only, local, and honest about
its limits — it reduces manual Cray↔GPT↔Claude prompt relay without pretending to be autonomous.

## What it does
- Loads a job (`jobs/active|completed|failed/<id>/job.yaml`).
- Infers the job's fine-grained **state** from artifacts (see `state_machine.md`).
- Applies **gate policy** by risk tier and computes the next allowed action (see `gate_policy.md`).
- Generates a **context pack** and a **compact report** (link-first, no huge dumps).
- Generates **role-specific agent prompts** (Claude/Codex/GPT) that reference files.
- Runs local **eval gates** (Python-native) into `review/eval_results.json`.
- Records **approval artifacts** and stops at real approval gates / hard stops.

## What it does NOT do (yet)
- No push, no git history rewrite, no product-repo writes from this control plane.
- No Claude/Codex/OpenRouter API calls — prompts are generated for manual/CLI use.
- No DB, no dashboard, no network.

## Quick start
```
python orchestrator/mqai_runner.py status  MQAI-0005
python orchestrator/mqai_runner.py run     MQAI-0005 --until-hard-stop
```
or via PowerShell wrapper: `.\commands\mqai.ps1 status MQAI-0005` (see `cli_usage.md`).

## Layout
- `orchestrator/` — the engine (job_loader, job_state, gate_policy, context_pack, compact_report,
  agent_prompt_builder, eval_runner, path_guard, command_router, mqai_runner, schemas, minimal_yaml).
- `commands/mqai.ps1` — CLI shim.
- `templates/` — job + report + policy templates.
- `skills/` — agent role charters.
- `evals/scripts/` — PowerShell gate scripts (alternative surface).
- `docs/` — this manual + state machine + gate policy + CLI + routing + known limits.
- `tests/` — stdlib unittest + fixtures proving the engine is not hardcoded to one job.

See `known_limits.md` for the honest list of MVP limitations.
