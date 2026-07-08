# Eval Gate: risk_tier_assignment

> Type: deterministic (scripted in V0). Runs FIRST — configures strictness of all other gates.
> Script: `evals/scripts/risk_tier_assignment.ps1`

## 1. Purpose
Assign the job's risk tier by **file-path matching against `critical_files.md`** — never by agent
self-assessment.

## 2. Inputs
- `job.yaml` (`targets`, planned/actual touched paths).
- `repo_control/<repo>/critical_files.md` (glob patterns).

## 3. Method
- For each target repo, match touched paths against `critical_files.md` globs.
- Any match → HIGH. Repo without a `critical_files.md` → default HIGH (conservative).
- Read-only jobs (like MQAI-0001) still receive a tier; scope constraints apply separately.

## 4. Output
```json
{ "gate": "risk_tier_assignment", "status": "pass", "tier": "LOW|MEDIUM|HIGH", "matched": [] }
```
The resulting tier is written back into the job's working state and drives consensus mode.

## 5. Tie-breaking
Ambiguous/unmapped paths → stricter tier (HIGH). Fail-safe by default.

## 6. Notes
V0: conservative seeding means most repos resolve HIGH until cartography narrows `critical_files.md`.
