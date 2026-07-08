# MQAI-0002C — Allowed Writes

> SCAFFOLD. These are the ONLY writes this job may ever make, and ONLY after
> `execution_authorized == true` (see `job.yaml` gating). Until then, this job writes nothing to any
> product repo. MQAI-side job artifacts under `jobs/active/MQAI-0002C/` are always writable.

## A. MQAI repo (always allowed)
```
jobs/active/MQAI-0002C/output/**      # execution logs, reaudit.md, before/after captures
jobs/active/MQAI-0002C/review/**      # review + synthesis + decision artifacts
```

## B. Product repos (GATED — only after Cray execution approval)

All product-repo work happens on a dedicated branch per repo (e.g. `chore/mqai-0002c-sechygiene`),
never directly on the default branch. Exact allowed paths:

### mqengine  (`C:\MAMAKQUANT\mqengine_lib_full`)
| Path | Operation | Notes |
|------|-----------|-------|
| `.gitignore` | CREATE (new file) | narrowed patterns (see execution_plan.md Step 2) |
| `PyPI-Recovery-Codes-*.txt` | `git rm --cached` (index only) | untrack; file stays on disk |
| `**/*.pyc` | `git rm --cached` (index only) | untrack already-tracked bytecode |
| `**/__pycache__/**` | `git rm --cached -r` (index only) | untrack cache dirs |
| `mqengine.egg-info/**` | `git rm --cached -r` (index only) | untrack build metadata |

### mqnode_cloud  (`C:\MAMAKQUANT\mqnode_cloud`)
| Path | Operation | Notes |
|------|-----------|-------|
| `.gitignore` | CREATE (new file) | narrowed patterns (see execution_plan.md Step 4) |

### mqnode_test2  (`C:\MAMAKQUANT\mqnode_test2`)
- **NO WRITES.** Confirm-only (read-only verification of `.env` ignored+untracked).

### mamakquantchainintel / mqchain-console  (`C:\MAMAKQUANT\mamakquantchain\mqchain-console`)
- **NO WRITES.** Confirm-only (read-only verification of `.env.local` ignored+untracked).

## C. Explicitly NOT allowed as writes
- No edits to any source/config file other than creating the two `.gitignore` files.
- No disk deletion of any file (index-only `git rm --cached`).
- No git history rewrite / force-push (RP7 is a separate, separately-authorized action).
- No push of any product repo until authorization + full consensus complete.
