# MQAI-0005 — Implementation Plan

1. Package skeleton: `orchestrator/__init__.py`, `minimal_yaml`, `schemas`.
2. `job_loader` (find + parse; stdlib fallback).
3. `job_state` (generic evidence-driven inference).
4. `gate_policy` (tier→gates, next action, blocked).
5. `path_guard` (write-scope, product paths).
6. Generators: `context_pack`, `compact_report`, `agent_prompt_builder`.
7. `eval_runner` (native gates → JSON, honest skips).
8. `command_router` + `mqai_runner` (argparse) + `commands/mqai.ps1`.
9. Templates, skills (8), eval scripts (touched_path_check, git_status_capture), docs (6).
10. Fixtures (LOW/MEDIUM/HIGH) + unittest suite (loader/state/gate/context/report).
11. Validate: `python -m unittest discover tests`; CLI smoke on MQAI-0005.
12. Output reports + builder self-review + memory updates.

All writes MQAI-local (per `allowed_writes`). No product writes, no push.
