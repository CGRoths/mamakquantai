# Codex — builder / code executor — MQAI-0005

- objective: Build the first production-usable local MQAI orchestrator that reduces manual Cray/GPT/Claude relay by adding job state detection, gate policy, context pack generation, compact reporting, eval runner wrappers, reusable agent prompt generation, and a PowerShell CLI wrapper.

- state: execution_authorized  ·  tier: HIGH  ·  next gate: plan
- next action: NEXT: produce a plan/scaffold review (and Cray plan approval for MEDIUM+).

## Read these (do not paste them wholesale)
- `jobs/active/MQAI-0005/job.yaml`
- `jobs/active/MQAI-0005/output/context_pack.md`
- `jobs/active/MQAI-0005/output/compact_report.md`

## Hard stops
- no push · no history rewrite · no secret-content inspection · no unrestricted `git diff --cached`
- no product-repo writes unless the job authorizes it · no `git add -A` in product repos

## Allowed writes
- `orchestrator/**`
- `commands/**`
- `templates/**`
- `skills/**`
- `evals/scripts/**`
- `docs/**`
- `tests/**`
- `jobs/active/MQAI-0005/**`
- `memory/decisions.md`
- `memory/lessons_learned.md`

## Your charter
- Obey allowed_writes exactly; never `git add -A`; stop at hard stops.
- Write only approved paths; stage only; do not commit/push unless a gate authorizes it.
- Emit an output note describing what changed and any assumptions.

## Expected output (compact)
- verdict/result · findings · changed files · blockers · required human decision
