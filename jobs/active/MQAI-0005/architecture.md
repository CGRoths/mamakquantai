# MQAI-0005 — Architecture

File-first, stdlib-only. Data flows: `job.yaml` + artifacts → JobSpec → StateResult → GateEvaluation
→ generators (context pack / compact report / prompts / evals).

```
commands/mqai.ps1  ──►  orchestrator/mqai_runner.py (argparse)
                                     │
                                     ▼
                        orchestrator/command_router.py
             ┌───────────────┬───────────────┬───────────────┐
             ▼               ▼               ▼               ▼
        job_loader     job_state       gate_policy      eval_runner
        (+minimal_yaml)  (infer)       (tier→gates)   (native gates)
             │               │               │               │
             └──────► schemas.JobSpec / StateResult / GateEvaluation ◄──────┘
                                     │
             ┌───────────────┬───────┴────────┬────────────────┐
             ▼               ▼                ▼                ▼
        context_pack    compact_report   agent_prompt_builder  path_guard
```

## Modules
- `minimal_yaml` — YAML-subset parser (PyYAML used if present).
- `schemas` — dataclasses (JobSpec, StateResult, GateStatus, GateEvaluation, EvalGateResult, CommandResult).
- `job_loader` — find + parse jobs.
- `job_state` — evidence-driven state inference.
- `gate_policy` — tier→required gates, next action, blocked actions.
- `path_guard` — write-scope + product-path checks.
- `context_pack` / `compact_report` / `agent_prompt_builder` — generators.
- `eval_runner` — Python-native gate execution → JSON.
- `command_router` / `mqai_runner` — dispatch + CLI.

## Principles
Default read-only/dry-run; fail safe; no network; no product writes; honest skips; no fake pass.
