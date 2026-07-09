# Agent Prompt Request — <JOB_ID> / <ROLE>

- objective: <objective>
- state: <state> · tier: <tier> · next gate: <gate>
- next action: <action>

## Read these (do not paste wholesale)
- `jobs/active/<JOB_ID>/job.yaml`
- `jobs/active/<JOB_ID>/output/context_pack.md`
- `jobs/active/<JOB_ID>/output/compact_report.md`

## Hard stops
- no push · no history rewrite · no secret-content inspection · no unrestricted `git diff --cached`
- no product-repo writes unless the job authorizes it · no `git add -A` in product repos

## Your charter
- <role-specific instructions>

## Expected output (compact)
- verdict/result · findings · changed files · blockers · required human decision
