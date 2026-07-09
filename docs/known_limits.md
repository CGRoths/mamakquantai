# MQAI MVP — Known Limits (V1, honest)

This is a production-**MVP** spine, not full autonomy. Known limitations:

## Orchestration
- **No agent APIs wired.** Claude/Codex/OpenRouter are NOT connected. `prompts` generates files for
  manual/CLI use only. Do not treat prompt generation as execution.
- **State inference is heuristic**, filename/artifact-based (see `state_machine.md`). It can be
  fooled by unconventional filenames. It deliberately under-claims (approval ≠ work product).
- **`close` is dry-run only.** Real closeout (move to `jobs/completed/` + memory update) is not
  automated to avoid clobbering job history; do it via a governed step.
- **`approve` does not auto-flip `job.yaml` flags** for execution/final_commit/push, to avoid unsafe
  YAML rewrites; it writes an auditable `approved_<gate>.md` artifact instead.

## YAML
- `minimal_yaml` is a **subset** parser (used only if PyYAML is absent): no flow style, no
  anchors/aliases, shallow list-of-maps, naive trailing-`#` comment handling. MQAI job.yaml files
  are authored within this subset. PyYAML is used automatically if installed.

## Evals
- `eval_runner` runs **Python-native** equivalents of the deterministic gates (reliable, no
  subprocess). The PowerShell scripts in `evals/scripts/` are an alternative surface, not the
  primary path in V1. `git_status_capture`/`touched_path_check` report **skipped** (never fake pass)
  when their inputs (target repos / touched_paths.txt) are absent.

## Safety scope
- This control plane never pushes, never rewrites history, never inspects secret contents, and never
  writes product repos. Product-repo mutation happens only inside a separately-authorized product
  execution job (e.g. MQAI-0002C), not from this runner.

## Handoff / resume (added by the handoff patch)
- Handoff/resume is **prompt/file-level continuity only** — it produces `output/handoff/*` artifacts
  so a new agent/session can resume from files. It does NOT execute agents; Claude/Codex/OpenRouter
  remain unwired. A human (or a future adapter) still hands the resume prompt to the agent.
- `branches`/`staged files` fields are not auto-captured for MQAI-local jobs (marked not-captured);
  product-execution jobs rely on their own git-status captures.
- Handoff detection is artifact-based (`handoff_state.json` + `latest_handoff.md`).

## Next improvements (candidate jobs)
- Optional PyYAML dependency detection + richer parser.
- Live (guarded) git status capture for product-execution jobs.
- Safe, governed `close` automation with history-preserving move.
- Optional agent API adapters (behind explicit config + gates).
