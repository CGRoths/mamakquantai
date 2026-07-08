# MQAI-0002C — Forbidden Actions

> SCAFFOLD. Violation of any item = automatic job failure + rollback + failure_taxonomy entry.

## Absolute (never, at any stage)
1. **No secret-content inspection.** Never open, read, print, copy, or log the contents of any
   secret file (`.env`, `.env.local`, recovery-code, key, token, credential files). Filename +
   git metadata only.
2. **No disk deletion.** Untracking is `git rm --cached` (index only). Files remain on disk; Cray
   relocates/removes the recovery file out-of-band.
3. **No git history rewrite.** No `filter-repo`, no BFG, no rebase, no force-push in this job. The
   optional RP7 history purge is a SEPARATE, separately-authorized action.
4. **No cross-layer edits.** Only the hygiene changes in `allowed_writes.md`. No source/schema/
   formula changes; no writes to another layer's owned paths; no `repo_control/` writes.

## Gated (forbidden UNTIL `execution_authorized == true`)
5. **No product-repo write** of any kind (including `.gitignore` creation and `git rm --cached`)
   before explicit Cray execution approval.
6. **No commit** of product-repo changes before ALL gates pass: eval gates + Claude review +
   GPT synthesis + Cray approval (see `job.yaml` gating order).
7. **No push** of any product repo before authorization and full consensus.
8. **No work on a default/protected branch.** All product-repo changes occur on a dedicated branch
   per repo.

## Process guards
9. **No self-promotion / self-approval.** The builder cannot approve its own execution.
10. **No scope creep.** Only the four MQAI-0002B-approved change classes; `mqnode_test2` and
    `mqchain-console` remain confirm-only (zero writes).
