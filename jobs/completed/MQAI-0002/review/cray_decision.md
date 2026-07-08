# MQAI-0002 — Cray Decision

DECISION: approve

APPROVED_BY: Cray

DATE: 2026-07-09

## Scope Approved

Approve MQAI-0002 Security Hygiene Audit findings as accepted.

This approval does NOT authorize remediation.
This approval does NOT authorize product repo writes.
This approval does NOT authorize deleting files.
This approval does NOT authorize opening or reading secret files.
This approval does NOT authorize repo_control promotion.

## Evidence Reviewed

- Scripted eval gates passed.
- Claude review verdict: approve.
- Boundary check: pass.
- Secret handling check: pass.
- secret_content_read=false for all inventory entries.
- No secret values were copied into MQAI output.
- Product repos were not modified.
- Findings are metadata/filename based only.

## Accepted Findings

- CRITICAL: mqengine contains a tracked PyPI-Recovery-Codes-*.txt file in HEAD and git history.
- HIGH: mqengine has no .gitignore.
- MEDIUM: mqnode_cloud has no .gitignore.
- LOW: mqnode_test2/.env and mqchain-console/.env.local exist locally but are gitignored and not tracked.
- CLEAN: tracked source-file secret pattern scan found zero matches.

## Required Follow-Up

Create a separate HIGH-tier remediation job:

MQAI-0002B — Security Remediation

The remediation job must separately handle:
1. PyPI recovery-code rotation by Cray.
2. Removing the tracked recovery-code file from mqengine.
3. Adding .gitignore coverage.
4. Confirming .env/.env.local files remain untracked.
5. Considering git history purge only after rotation.

## Closeout Authorization

Move MQAI-0002 to jobs/completed/MQAI-0002.
Update job.yaml status to completed.
Update memory/decisions.md.
Update memory/lessons_learned.md.
Update memory/failure_taxonomy.yaml if appropriate.
