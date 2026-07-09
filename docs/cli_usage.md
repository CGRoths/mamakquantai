# MQAI CLI Usage (V1)

Two equivalent entrypoints:

- Direct: `python orchestrator/mqai_runner.py <command> <job_id> [args]`
- PowerShell shim: `.\commands\mqai.ps1 <command> <job_id> [args]`

## Commands
| Command | Effect | Mutates? |
|---------|--------|----------|
| `status <id>` | one-line state + next action | read-only |
| `next <id>` | next gate + blocked actions | read-only |
| `context <id>` | writes `output/context_pack.md` | MQAI job output only |
| `report <id>` | writes `output/compact_report.md` | MQAI job output only |
| `prompts <id>` | writes `output/prompts/*.md` | MQAI job output only |
| `eval <id>` | writes `review/eval_results.json` | MQAI job review only |
| `run <id> --until-hard-stop` | context+prompts+eval+report, then stops before any gate/product mutation | MQAI job files only |
| `approve <id> --gate <name>` | writes `review/approved_<gate>.md` | MQAI job review only |
| `close <id> [--commit]` | dry-run close by default | none by default |
| `handoff <id> --from <a> --to <b> [--stop-reason <r>]` | writes `output/handoff/*` + refreshes report | MQAI job output only |
| `resume <id> --agent <codex\|claude\|gpt>` | writes `output/handoff/resume_prompt.md` | MQAI job output only |

## Examples
```
python orchestrator/mqai_runner.py status  MQAI-0005
python orchestrator/mqai_runner.py run     MQAI-0005 --until-hard-stop
python orchestrator/mqai_runner.py approve MQAI-0005 --gate plan
python orchestrator/mqai_runner.py handoff MQAI-0005 --from codex --to claude --stop-reason context_exhausted
python orchestrator/mqai_runner.py resume  MQAI-0005 --agent claude
```

Handoff/resume argument names: `--from`, `--to`, `--stop-reason` (handoff); `--agent` (resume).
Valid agents: `codex`, `claude`, `gpt`. Valid stop reasons: context_exhausted, quota_exhausted,
tool_error, validation_failed, human_approval_required, hard_stop_triggered, unknown.

## PowerShell execution policy
If `.\commands\mqai.ps1` is blocked by execution policy, run the Python entrypoint directly
(shown above). Do **not** change system execution policy automatically. To allow for the current
session only, a user may run (their choice, not automated by MQAI):
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.

## Safety
All commands fail safely and default to read-only / dry-run. No command pushes, rewrites history,
inspects secret contents, or writes product repos.
