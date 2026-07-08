# MQAI-0002B — Security Remediation Plan

> PLANNING / PATCH PROPOSAL ONLY. Nothing in this document has been executed. No product repo was
> edited, no file deleted, no git history rewritten, no commit/push. No secret file was opened.
> Source of findings: MQAI-0002 (approved, closed). Date: 2026-07-09.

## Precondition status
- **PyPI recovery codes: ROTATED by Cray (done).** The account-takeover incident action is complete,
  so the git-side cleanup below is no longer time-critical — but the exposed file must still be
  removed and prevented from recurring.

## Remediation items (proposed — execution deferred to a separate HIGH-tier job)

### RP1 — Remove tracked recovery-codes file from `mqengine` current tree
- **Action (proposed):** `git rm --cached "PyPI-Recovery-Codes-*.txt"` (untrack, keep local copy),
  then commit. Local file is left on disk for Cray to relocate/delete manually (this job does not
  delete files).
- **Effect:** removes the file from the working tree index / future commits. Does **not** remove it
  from existing history (see RP7).
- **Boundary:** product-repo write → out of scope here; belongs to the execution job.

### RP2 — Add `.gitignore` to `mqengine`
- **Action (proposed):** create `.gitignore` with coverage below (see `proposed_file_changes.md`).
- **Effect:** prevents recurrence of committed secrets and cleans up tracked bytecode noise.

### RP3 — Add `.gitignore` to `mqnode_cloud`
- **Action (proposed):** create `.gitignore` with the same secret/keys/env coverage (preventive; no
  secret present today).

### RP4 — Confirm `mqnode_test2/.env` remains untracked + gitignored
- **Action (proposed, read-only verification):** re-run `git ls-files .env` (expect empty) and
  `git check-ignore .env` (expect ignored). No change expected; confirm only.

### RP5 — Confirm `mqchain-console/.env.local` remains untracked + gitignored
- **Action (proposed, read-only verification):** re-run `git ls-files .env.local` (expect empty) and
  `git check-ignore .env.local` (expect ignored). Confirm only.

### RP6 — Re-audit after remediation
- **Action (proposed):** re-run the MQAI-0002 read-only hygiene checks against all four repos and
  confirm: recovery file no longer tracked, `.gitignore` present in `mqengine` + `mqnode_cloud`,
  env files still untracked, pattern scan still clean. Produce a short `reaudit.md` in the execution
  job's output.

### RP7 — OPTIONAL history purge (DOCUMENT ONLY — DO NOT EXECUTE)
- **Rationale:** codes are already rotated, so purging history is now hygiene, not incident response.
  Only worth doing if policy requires the blob gone from all refs.
- **Proposed approach (if ever authorized):** `git filter-repo --path "<recovery file>" --invert-paths`
  (preferred) or BFG; then force-push and require all clones to re-clone.
- **Risks:** rewrites SHAs for all downstream history; breaks existing clones/forks/PRs; force-push.
- **Status:** NOT scheduled. Requires its own explicit Cray authorization in the execution job.
  Given rotation is done, RP7 is **recommended LOW priority / optional**.

## Sequencing (for the future execution job)
```
RP2 (.gitignore mqengine)  →  RP1 (git rm --cached recovery file)  →  commit
RP3 (.gitignore mqnode_cloud)            [independent]
RP4, RP5 (confirm env files)             [read-only, anytime]
RP6 (re-audit)                           [after RP1–RP3]
RP7 (optional history purge)             [only if separately authorized]
```

## Consensus & authorization
- This is a HIGH-tier job (`consensus_mode: high`): Codex plan + Claude plan + GPT synthesis +
  deterministic gates + Cray approval.
- **Approving this job approves the PLAN only.** Execution (RP1–RP3, RP6, and any RP7) is a
  **separate** HIGH-tier execution job requiring its own Cray authorization, because every step is a
  product-repo write.
