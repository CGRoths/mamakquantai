# Resume Prompt — <JOB_ID>  (agent: <agent>)

> **Do NOT rely on chat history.** All continuity is in the files below. MQAI owns memory, state,
> rules, gates, and handoff. Agents are temporary compute; Cray is final risk owner.
> Agents do not share memory — read the files.

## Your role
- <role-specific instruction for codex | claude | gpt>

## Read these job files
- `jobs/active/<JOB_ID>/job.yaml`
- `jobs/active/<JOB_ID>/output/context_pack.md`
- `jobs/active/<JOB_ID>/output/compact_report.md`
- `jobs/active/<JOB_ID>/output/handoff/latest_handoff.md`

## Current state summary
- state: <state> · tier: <tier> · next gate: <gate>
- next allowed action: <action>
- blocked: <list>

## Hard stops
- no push · no history rewrite · no secret-content inspection · no unrestricted `git diff --cached`
- no product-repo writes unless authorized · no `git add -A` in product repos

## Reporting format (compact)
- status · next action · gates passed/pending · changed files · product repos touched · blockers ·
  required human decision
