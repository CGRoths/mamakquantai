# Handoff — <JOB_ID>  (<from_agent> -> <to_agent>)

- generated: <iso timestamp>
- job_id: <JOB_ID>
- objective: <objective>
- current_state: <state> · risk_tier: <tier>
- from_agent: <from> · to_agent: <to> (recommended_next_agent)
- stop_reason: <context_exhausted|quota_exhausted|tool_error|validation_failed|human_approval_required|hard_stop_triggered|unknown>

## Progress
- last completed (inferred): <state + evidence>
- next intended action: <action>
- gates passed: <list>
- gates pending: <list>

## Repo / change state
- product repos touched: <yes/no>
- target_repos: <list or none>
- MQAI files changed: <see git status / job output>
- product files changed: <none by control plane>
- current branches / staged files: <if known, else not captured in V1>

## Validation status
- eval_results.json: <present/not run>
- validation_results.md: <present/absent>

## Blockers
- <blocker>

## Hard stops (do NOT do)
- push · history rewrite · secret-content inspection · unrestricted `git diff --cached`
- product-repo writes unless authorized · `git add -A` in product repos

## Allowed writes / Forbidden writes
- (from job.yaml)

## Files next agent SHOULD read
- job.yaml · context_pack.md · compact_report.md · handoff/latest_handoff.md · handoff/resume_prompt.md

## Files next agent MUST NOT touch
- product repo paths · repo_control/ canonical truth · jobs/completed|failed history

## Compact continuation prompt
> Continue <JOB_ID> as <to_agent>. Read the files above (NOT chat history). Respect hard stops.
> Report compactly.
