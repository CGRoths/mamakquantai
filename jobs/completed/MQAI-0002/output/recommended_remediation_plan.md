# MQAI-0002 — Recommended Remediation Plan

> PROPOSAL ONLY. No remediation was performed in this job (per scope). Each item below is a future
> work package requiring its own risk tier, review, and Cray approval. Product-repo writes are a
> HIGH-risk area (secrets/auth) and require the full consensus path.

## Priority 0 — CRITICAL (do first, treat as incident)

### R1. Rotate the exposed PyPI recovery codes (`mqengine`)
- **Why:** account-takeover credential committed to git and in history.
- **Steps (human-driven, outside MQAI):**
  1. **Rotate now:** log into PyPI, invalidate/regenerate recovery codes and confirm 2FA. Do this
     **before** touching git — history purge does not un-expose already-pushed codes.
  2. Verify whether `github.com/CGRoths/mqengine` ever received a push containing the file; if yes,
     assume disclosure and keep the rotated state.
- **Owner:** Cray. **MQAI role:** none (cannot rotate external credentials).

### R2. Remove the recovery-codes file from `mqengine` git (after rotation)
- **Steps:** `git rm --cached "PyPI-Recovery-Codes-*.txt"` → add `.gitignore` (R3) → commit.
- **History purge:** use `git filter-repo` (preferred) or BFG to strip the blob from all history,
  then coordinate a force-push per policy and have collaborators re-clone.
- **Risk tier:** HIGH (history rewrite + force-push). Full consensus + Cray approval required.

## Priority 1 — HIGH / MEDIUM (prevent recurrence)

### R3. Add `.gitignore` to `mqengine`
Cover at minimum:
```
.env
.env.*
!.env.example
*.pem
*.key
*.p12
*.pfx
*_token*
*credential*
*recovery*
__pycache__/
*.pyc
*.egg-info/
```
- Also `git rm --cached` the currently-tracked `.pyc` / `egg-info` bytecode (hygiene, non-secret).

### R4. Add `.gitignore` to `mqnode_cloud`
- Same `.env*` / keys / tokens / credentials coverage as R3 (preventive; no secret present today).

## Priority 2 — LOW (confirm, no urgent change)

### R5. Confirm `.env.example` files are placeholder-only
- `mqnode_test2`, `mqnode_cloud`, `mqchain-console` each track a `.env.example`. A human should
  eyeball that they contain only placeholder values (not opened in this read-only audit).

### R6. Keep correctly-ignored local env files as-is
- `mqnode_test2/.env` and `mqchain-console/.env.local` are properly ignored and unhistoried.
  No change; never force-add.

## Priority 3 — Follow-up capability

### R7. Deep-history secret scan (tool-assisted)
- This audit checked history **by filename** only. Recommend a dedicated job running `gitleaks` or
  `trufflehog` across **all refs/history** of all four repos for content-level leakage.
- This also aligns with the V1 upgrade of the MQAI `secret_scan` eval gate.

## Sequencing
```
R1 (rotate)  →  R3 (.gitignore mqengine)  →  R2 (rm cached + history purge + force-push)
R4 (.gitignore mqnode_cloud)   [independent, anytime]
R5, R6 (confirm)               [independent, low priority]
R7 (deep scan)                 [independent follow-up job]
```

## MQAI boundary reminder
Every remediation touching a product repo is a **product-repo write** — forbidden in V0 and gated by
`AGENTS.md` (HIGH consensus + Cray approval). MQAI can prepare the change packages and review them,
but cannot execute product-repo writes or rotate external credentials.
