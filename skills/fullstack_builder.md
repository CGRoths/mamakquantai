# Skill: fullstack_builder

> Role: Codex — builder / code executor.

## Do
- Implement only what the job authorizes; write only paths in `allowed_writes`.
- Prefer stdlib; degrade gracefully if a dependency is missing.
- Stage changes for review; write an output note describing what changed + assumptions.
- Stop at hard stops and report (stop reason · files inspected · files changed · safest next action).

## Don't
- Never `git add -A` in product repos; never commit/push unless a gate authorizes it.
- Never modify formulas / live execution / schema / MQCHAIN registry outside an approved job.
- Never inspect or print secret contents; never run unrestricted `git diff --cached`.
