# MQAI Handoff / Resume Protocol (V1)

Lets Codex, Claude, GPT, or a new session continue a job from **files**, not chat memory.

**Core rule:** MQAI owns memory, state, rules, gates, and handoff. Agents are temporary compute.
Cray is the final risk owner. **Agents do not share memory** — a resuming agent reads the files.

## Artifacts (under `jobs/active/<JOB_ID>/output/handoff/`)
- `latest_handoff.md` — full handoff note (see fields below).
- `<from_agent>_to_<to_agent>.md` — the same note, named by direction (e.g. `codex_to_claude.md`).
- `resume_prompt.md` — role-specific resume prompt for the incoming agent.
- `handoff_state.json` — machine-readable {from, to, recommended_next_agent, stop_reason, state}.

## Handoff note fields
job_id · current state · objective · from/to agent · stop_reason · last completed action · next
intended action · gates passed/pending · product repos touched · MQAI files changed · product files
changed · branches/staged (if known) · validation status · blockers · hard stops · allowed/forbidden
writes · files to read · files not to touch · compact continuation prompt.

## Stop reasons
`context_exhausted · quota_exhausted · tool_error · validation_failed · human_approval_required ·
hard_stop_triggered · unknown` (default `unknown`).

## Commands
```
mqai handoff <JOB_ID> --from <agent> --to <agent> [--stop-reason <reason>]
mqai resume  <JOB_ID> --agent <codex|claude|gpt>
```
`handoff` also refreshes the compact report so `handoff_ready` surfaces immediately. `resume`
regenerates `resume_prompt.md` targeted at the chosen agent.

## Reporting surfaces
- Compact report adds: `handoff_ready`, `latest_handoff_path`, `resume_prompt_path`,
  `recommended_next_agent`, `last_stop_reason`.
- Context pack adds: handoff state, resume path, continuation policy, and the "agents do not share
  memory" statement.
- Generated agent prompts reference the handoff + resume files when they exist.

## Limit (honest)
This is **prompt/file-level continuity**, not automatic agent execution. Claude/Codex/OpenRouter are
NOT wired; a human (or a future adapter) still hands the resume prompt to the agent.
