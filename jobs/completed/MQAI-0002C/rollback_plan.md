# MQAI-0002C — Rollback Plan

> SCAFFOLD. How to safely undo each step if a gate fails or a problem is found. All rollback is
> index/branch-level; no disk deletion, no history rewrite. No secret file is opened during rollback.

## Guiding principle
All product-repo work happens on a dedicated branch (`chore/mqai-0002c-sechygiene`) and is NOT
committed until full consensus (Gate B). Therefore the primary rollback is simply "do not commit /
discard the branch." Nothing reaches the default branch or remote until authorized.

## Deletion policy during rollback (W3)
- **"No disk deletion" protects pre-existing / user / product files.** Those are NEVER deleted.
  In particular, **pre-existing untracked secret files are never removed** (e.g. the local
  recovery-codes file, `.env`, `.env.local`) — Cray relocates/removes those out-of-band.
- **Files THIS job created on the remediation branch** (e.g. a new `.gitignore`) MAY be removed
  during rollback if needed, since they did not exist before Gate-A work.
- **No git history rewrite** occurs during rollback (nothing was rewritten to begin with).

## R-A — Before any commit (staged/working changes only)
- Unstage `.gitignore` / untracking:
  ```bash
  git -C "<repo>" restore --staged .gitignore
  git -C "<repo>" restore --staged .    # unstage index changes (re-tracks previously untracked)
  ```
- Remove the not-yet-committed working `.gitignore` — permitted because it is a JOB-CREATED file
  (did not exist before Gate-A work). No pre-existing/user/product file is removed:
  ```bash
  git -C "<repo>" clean -f -- .gitignore   # removes only the job-created, untracked .gitignore
  ```
- Re-track anything unstaged by `git rm --cached` (the index restore above re-adds them).

## R-B — Abandon the working branch entirely
```bash
git -C "<repo>" switch -   # back to prior branch
git -C "<repo>" branch -D chore/mqai-0002c-sechygiene
```
- Leaves the default branch untouched. Product repo returns to pre-job state (minus the local
  recovery file, which was never deleted by this job).

## R-C — After a local commit (not yet pushed)
```bash
git -C "<repo>" reset --soft HEAD~1   # undo commit, keep changes staged
# or hard-abandon the branch via R-B
```
- Still nothing on the remote (no push in this job).

## R-D — Recovery file safety
- The recovery file is only `git rm --cached` (untracked), never deleted from disk. If untracking
  must be reverted: `git -C "<mqengine>" restore --staged -- "<recovery filename>"` re-tracks it.
- Codes are already rotated, so the file is inert regardless of tracking state.

## What rollback does NOT do
- Does not touch git history (nothing was rewritten).
- Does not delete any user file from disk.
- Does not affect remotes (nothing pushed).

## On rollback
- Record cause + action in `output/rollback_log.md` and append a `failure_taxonomy.yaml` entry
  (category depends on the failing gate). Then return the job to `review` or `failed` per outcome.
