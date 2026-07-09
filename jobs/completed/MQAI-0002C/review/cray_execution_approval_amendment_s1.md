# MQAI-0002C — Cray Gate A Amendment (S1 / V10 acknowledged)

DECISION: gate_a_amended_s1_v10_acknowledged

APPROVED_BY: Cray
DATE: 2026-07-09
AMENDS: review/cray_execution_approval.md (Gate A — execution, branch-local only)

## Statement
- The prior Gate A approval **remains valid**.
- S1/V10 **strengthens** the execution constraints by requiring secret-safe diff capture.
- Gate A execution must now follow **V1–V10**, not V1–V9.
- **Unrestricted `git diff --cached` capture is forbidden.**
- **Recovery-code removal evidence must be metadata-only** (`--name-status` / `--stat` / `--summary`;
  full-content diff allowed ONLY for newly-created `.gitignore`, or a sanitized diff excluding
  secret-like paths).
- **MQAI `output/` and `review/` files must NOT contain deleted recovery-code contents** (or any
  deleted secret-file contents).
- **V10 failure blocks Gate B** and must be treated as a **secret_leak incident** (do NOT commit;
  quarantine the offending artifact; append `failure_taxonomy.yaml` `secret_leak`).

## Unchanged scope (reaffirmed)
- Gate A still authorizes only **branch-local remediation, staging, diff capture, and validation**.
- Gate A still does **NOT** authorize commit or push.
- `commit_authorized` remains **false**.
- Gate B still requires: V1–V10 validation pass + executed-diff review (`claude_review_executed.md`)
  + GPT synthesis (`gpt_synthesis.md`) + Cray final approval (`cray_final_approval.md`).

## Effect
- No change to `job.yaml` flags: `execution_authorized: true` (Gate A), `commit_authorized: false`
  (Gate B pending). This amendment only acknowledges and binds the S1/V10 constraints into the
  active Gate A authorization.
