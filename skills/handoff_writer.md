# Skill: handoff_writer

> Role: produce a complete, file-based handoff so any agent/session can resume without chat history.

## Do
- Capture: job_id, current state, objective, from/to agent, stop_reason, last completed + next
  intended action, gates passed/pending, product-repos-touched, changed files, branches/staged (if
  known), validation status, blockers, hard stops, allowed/forbidden writes, exact files to read,
  files not to touch, and a compact continuation prompt.
- Classify stop_reason: context_exhausted | quota_exhausted | tool_error | validation_failed |
  human_approval_required | hard_stop_triggered | unknown (default unknown).
- Write `output/handoff/latest_handoff.md`, `<from>_to_<to>.md`, `resume_prompt.md`, and a
  machine-readable `handoff_state.json`.

## Don't
- Don't rely on chat memory; everything must be reconstructable from files.
- Don't claim agent APIs are wired — V1 is prompt/file continuity only.
- Don't inspect secret contents or include product-repo writes.

## Core rule
MQAI owns memory/state/rules/gates/handoff. Agents are temporary compute. Cray is final risk owner.
