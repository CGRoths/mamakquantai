# MQAI-0005 — CLI Smoke Results

Entrypoint: `python orchestrator/mqai_runner.py <command> MQAI-0005 [args]`
(PowerShell shim `.\commands\mqai.ps1 ...` is equivalent; if execution policy blocks it, use the
Python form — see docs/cli_usage.md. System policy was NOT changed.)

## Core commands
| Command | Result |
|---------|--------|
| `status` | OK — tier=HIGH, state + next action |
| `next` | OK — next gate + blocked actions |
| `context` | OK — wrote context_pack.md (now with handoff/continuation section) |
| `prompts` | OK — 3 role prompts (reference handoff files when present) |
| `report` | OK — wrote compact_report.md (with Handoff/continuity section) |
| `eval` | OK — risk_tier=pass, write_scope=pass, secret_scan=pass, touched_path=skipped, git_status=skipped |
| `run --until-hard-stop` | OK — stops at gate `plan`, no product mutation |
| `approve --gate plan` | OK — wrote review/approved_plan.md |

## Handoff / resume commands
| Command | Result |
|---------|--------|
| `handoff MQAI-0005 --from codex --to claude --stop-reason context_exhausted` | OK — 4 artifacts (latest_handoff.md, codex_to_claude.md, resume_prompt.md, handoff_state.json) |
| `resume MQAI-0005 --agent claude` | OK — resume_prompt.md (role=Claude) |
| `report` (after handoff) | OK — `handoff_ready: true`, `recommended_next_agent: claude`, `last_stop_reason: context_exhausted` |

Argument names: `--from`, `--to`, `--stop-reason` (handoff); `--agent` (resume). No product repos
touched; no push; no secrets printed.
