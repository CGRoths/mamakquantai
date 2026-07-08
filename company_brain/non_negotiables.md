# Non-Negotiables

> STATUS: canonical. Violation of any item = automatic job failure.

## 1. Write Scope
Agents write only inside their assigned `jobs/active/<id>/` subfolder (Codex → `output/`,
Claude → `review/`). **Zero writes to product repos in V0.**

## 2. Promotion Gate
Nothing enters `repo_control/` without: **eval pass + Claude review + Cray approval.**
Agents cannot self-promote. Ever.

## 3. Protected Baseline
`mqnode_test2` is the read-only foundation in V0. No edits, no refactor, no schema change,
no formula change, no merge.

## 4. Risk Tiering Integrity
Risk tier is path-derived from `critical_files.md`. Agent opinion never sets the tier.
Ambiguous or unmapped paths default to the stricter tier.

## 5. Layer Ownership
No cross-layer writes. A job scoped to one layer must not write into another layer's owned paths.
See `separation_of_concerns.md`.

## 6. Secrets
No secrets captured, logged, or committed. `secret_scan` blocks on any hit.

## 7. Truth Provenance
Provisional canon stays flagged (`STATUS: provisional`) until verified by a job.
No silent hardening of unverified claims.

## 8. Human Authority
Cray is the sole approver. No inferred approval. Approval is an explicit signed line in
`review/cray_decision.md`.

## 9. Scope Discipline
MQAI does not make alpha / strategy / capital allocation decisions. That is MQBRAIN (future).
