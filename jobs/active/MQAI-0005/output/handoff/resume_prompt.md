# Resume Prompt — MQAI-0005  (agent: claude)

> **Do NOT rely on chat history.** All continuity is in the files below. MQAI owns memory,
> state, rules, gates, and handoff. Agents are temporary compute; Cray is final risk owner.
> Agents do not share memory with each other — read the files.

## Your role
- You are Claude (reviewer/auditor OR builder-continuation). Review artifacts/diffs and identify contradictions; if continuing a build, obey allowed_writes and hard stops.

## Read these job files (do not paste them wholesale)
- `jobs/active/MQAI-0005/job.yaml`
- `jobs/active/MQAI-0005/output/context_pack.md`
- `jobs/active/MQAI-0005/output/compact_report.md`
- `jobs/active/MQAI-0005/output/handoff/latest_handoff.md`

## Current state summary
- state: `execution_authorized`  ·  tier: HIGH  ·  next gate: validation
- next allowed action: NEXT: run validation and write output/validation_results.md.
- blocked: commit of product-repo changes (no final approval), push (never inferred; requires explicit push authorization), any product-repo mutation (job does not allow product writes)

## Hard stops
- no push · no history rewrite · no secret-content inspection · no unrestricted `git diff --cached` · no product-repo writes unless authorized · no `git add -A` in product repos

## Reporting format (compact)
- status · next action · gates passed/pending · changed files · product repos touched · blockers · required human decision
