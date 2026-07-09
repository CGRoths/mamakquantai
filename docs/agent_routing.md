# MQAI Agent Routing (V1)

MQAI routes work to three agent roles via generated prompt files (manual/CLI use in V1; no APIs
wired). Prompts are compact and reference files rather than pasting context.

| Role | Skill charter | When | Output |
|------|---------------|------|--------|
| **Codex** — builder/executor | `skills/fullstack_builder.md` | build/patch/execute behind gates | code + `output/*` notes; obeys allowed_writes; no `git add -A`; stops at hard stops |
| **Claude** — reviewer/auditor | `skills/security_reviewer.md`, `skills/executed_diff_reviewer.md` | review artifacts + staged diffs | verdict block; contradictions; boundary + secret-handling checks |
| **GPT** — synthesis/judge | `skills/gpt_synthesis_judge.md` | HIGH/CRITICAL consensus | consensus + unresolved risk; gate conditions |

Supporting skills: `cto_planner.md` (plan/scope), `compact_reporter.md` (status compression),
`gatekeeper.md` (gate enforcement), `incident_diagnoser.md` (failure triage).

## Consensus by tier
- LOW: Codex builds → Claude compact review.
- MEDIUM: Codex builds → Claude reviews actual output.
- HIGH/CRITICAL: Codex plan + Claude plan → GPT synthesis → deterministic gates → Cray approval.

## Routing flow
`mqai run <id> --until-hard-stop` produces the context pack + role prompts + evals + compact report,
then stops. Cray hands the relevant prompt to the agent, pastes back the artifact, and re-runs
`mqai status`/`next`. This compresses the previous manual relay loop.

## Not wired yet
Real Claude/Codex/OpenRouter execution is intentionally not connected (see `known_limits.md`).
