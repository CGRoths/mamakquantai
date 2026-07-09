# MQAI-0002C — Cray Base-Replay Approval (Gate-A continuation)

DECISION: approve_gate_a_base_replay_only

APPROVED_BY: Cray
DATE: 2026-07-09
NATURE: Gate-A continuation (NOT Gate B)

## Scope authorized
- Authorizes **mqengine base-branch replay only**.
- Gate B remains **blocked**; `commit_authorized` remains **false**.
- Replay must use the intended mqengine base branch — **`main`** (default; verified to exist locally
  and to contain the same exposure: recovery file + 11 `.pyc` + 5 `egg-info` tracked, no `.gitignore`).
- Replay applies ONLY the approved idempotent hygiene steps:
  - approved `.gitignore` (execution_plan Step 2 content),
  - `git rm --cached -- 'PyPI-Recovery-Codes*.txt'`,
  - approved generated-artifact untracking (`*.pyc`, `__pycache__/`, `mqengine.egg-info/`, index-only).
- Stage only approved paths. **Never `git add -A`.**
- Secret-safe evidence capture only (metadata for removals; full diff for `.gitignore` only;
  no unrestricted `git diff --cached`).
- Re-run **V1–V10**.
- Refresh output evidence and the executed-diff review if staged evidence changes.

## Still forbidden
- No commit, no push, no history rewrite, no disk deletion of pre-existing/user/product files,
  no secret-content inspection, no touching `mqnode_test2` / `mqchain-console`, no changes to
  `mqnode_cloud` beyond read-only re-verification.

## Base selection note
`origin/HEAD` is not set locally; local `main` selected as the intended integration base. If the
eventual push/PR targets a different default, the Gate-B step must re-confirm the base.

## Effect
- No `job.yaml` flag change: `execution_authorized: true` (Gate A), `commit_authorized: false`
  (Gate B pending). This authorization only permits the mqengine base replay described above.
