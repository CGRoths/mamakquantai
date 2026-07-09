# MQAI-0002D — Audit Plan (read-only)

Verifies MQAI-0002C remediation on the branches where it was committed
(`chore/mqai-0002c-sechygiene`, not yet merged to `main`). Metadata/counts/paths only; no secret
contents; no writes; no remediation.

## Checks
1. `mqengine`: `PyPI-Recovery-Codes*.txt` NOT tracked in HEAD (`git ls-files`, case-insensitive).
2. `mqengine`: recovery file if on disk is ignored/untracked (`git check-ignore`) — contents NOT read.
3. `mqengine`: `.gitignore` exists and covers approved patterns (recovery glob, `.env*`, keys, `*.pyc`,
   `__pycache__/`, `*.egg-info/`).
4. `mqengine`: tracked `.pyc` / `__pycache__/` / `mqengine.egg-info/` removed from HEAD (count 0).
5. `mqnode_cloud`: `.gitignore` exists.
6. `mqnode_test2` `.env` and `mqchain-console` `.env.local` remain ignored + untracked.
7. Tracked-source secret pattern scan (`git grep -I -c`, counts only) across all four repos.
8. Capture metadata/counts/paths only — never secret values.

## Method
Read-only git commands (`ls-files`, `check-ignore`, `grep`), no `git rm`, no diff of secret files.
