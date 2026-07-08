# Skill: mqchain_label_guard

> Guard for work touching MQCHAIN (`mamakquantchainintel` / `mqchain-console`). Label truth.

## When to apply
Any job that targets, reads, or reasons about `mqchain-console`.

## Invariants to enforce (from label_governance.md + registry_truth_boundary.md)
1. Labels are governed truth; consumers do not redefine them.
2. Canonical registry is the single source — no shadow stores.
3. Label changes are auditable (provenance recorded).
4. Labels consumed by research must be point-in-time safe.
5. Entity IDs are stable; rename/merge is HIGH-risk.

## V0 posture
READ-ONLY. Registry is HIGH-risk; any registry-authoring output from a non-MQCHAIN job = violation.

## Review questions
- Does output respect the single canonical registry?
- Any cross-layer authorship of labels/registry?
- Is entity ID stability preserved?
- Any lookahead exposure in labels used downstream?
