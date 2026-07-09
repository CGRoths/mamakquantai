# MQAI-0002C — Forbidden Actions

> SCAFFOLD. Violation of any item = automatic job failure + rollback + failure_taxonomy entry.

## Absolute (never, at any stage)
1. **No secret-content inspection.** Never open, read, print, copy, or log the contents of any
   secret file (`.env`, `.env.local`, recovery-code, key, token, credential files). Filename +
   git metadata only.
1a. **No unrestricted full diff of secret-like deleted files (S1).** After `git rm --cached` of a
   secret-like path, an unrestricted `git diff --cached` prints the DELETED contents. Never run or
   save unrestricted `git diff --cached`. Capture recovery-code / secret-like removals metadata-only
   (`--name-status` / `--stat` / `--summary`); full-content diffs are allowed ONLY for newly-created
   `.gitignore` files, or via a sanitized diff that excludes secret-like paths (execution_plan Step 7).
1b. **No writing deleted recovery-code / secret contents into MQAI output or review files.** Nothing
   under `jobs/active/MQAI-0002C/output/` or `review/` may contain recovery-code lines or the
   contents of any deleted secret file. Enforced by validation V10 leak scan.
2. **No disk deletion of pre-existing / user / product files.** Untracking is `git rm --cached`
   (index only); those files remain on disk. Cray relocates/removes the recovery file out-of-band.
   (Exception — narrow: a file THIS job created on the remediation branch, e.g. a new `.gitignore`,
   may be removed during rollback; see `rollback_plan.md`. Pre-existing untracked secret files are
   NEVER removed.)
3. **No git history rewrite.** No `filter-repo`, no BFG, no rebase, no force-push in this job. The
   optional RP7 history purge is a SEPARATE, separately-authorized action.
4. **No cross-layer edits.** Only the hygiene changes in `allowed_writes.md`. No source/schema/
   formula changes; no writes to another layer's owned paths; no `repo_control/` writes.

## Two-gate authorization (W1)

### Gated — forbidden UNTIL Gate A (`execution_authorized == true`)
5. **No branch-local product-repo write** of any kind (creating a remediation branch, creating
   `.gitignore`, `git rm --cached`, staging) before **Gate A** = explicit Cray *execution* approval.
   Gate A authorizes branch-local remediation work + diff capture ONLY. It does NOT authorize commit
   or push.

### Gated — forbidden UNTIL Gate B (`commit_authorized == true`)
6. **No commit** of product-repo changes before **Gate B**, which requires: V1–V10 validation pass +
   Claude review of the ACTUAL (sanitized) staged diff (matches approved plan) + GPT synthesis +
   Cray *final* approval.
7. **No push** of any product repo before Gate B (and push only if separately authorized even then).

### Always
8. **No work on a default/protected branch.** All product-repo changes occur on a dedicated
   remediation branch per repo.
9. **Branch work never implies commit.** Completing Gate-A branch work does not authorize Gate B;
   the two approvals are explicit and separate.

## Process guards
10. **No self-promotion / self-approval.** The builder cannot approve its own execution.
11. **No scope creep.** Only the four MQAI-0002B-approved change classes; `mqnode_test2` and
    `mqchain-console` remain confirm-only (zero writes).
