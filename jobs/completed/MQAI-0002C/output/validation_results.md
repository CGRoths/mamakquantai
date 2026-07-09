# MQAI-0002C — Validation Results (Gate-A + base-replay)

> Gate A only. Branch-local, staged, NOT committed, NOT pushed. No secret file opened.
> Updated 2026-07-09 after the mqengine base-branch REPLAY onto `main`. Supersedes the wrong-base
> run; wrong-base evidence preserved under `output/mqengine_wrongbase_evidence/`.

## Base state (post-replay)
- `mqengine`: remediation branch `chore/mqai-0002c-sechygiene` now created **from `main`**
  (HEAD `f56f790`). `main` verified to contain the same exposure (recovery file + 11 `.pyc` +
  5 `egg-info` tracked, no `.gitignore`), so the untracking steps are valid against `main`.
- `mqnode_cloud`: remediation branch `chore/mqai-0002c-sechygiene`, merge-base == `main` tip
  (`aad7187`) → already based on `main`. Staged delta = `.gitignore` only. No replay needed.
- Recovery file preserved on disk during the base switch (tracked in `main` → not removed).
- Recovery codes already rotated by Cray; removal is index-only.

## Results (post-replay)
| Check | Result | Evidence |
|-------|--------|----------|
| **V1** recovery untracked (mqengine, case-insensitive) | **PASS** | `ls-files | grep -Eic 'PyPI-Recovery-Codes.*\.txt'` = 0 |
| **V2** generated artifacts untracked (mqengine) | **PASS** | tracked `.pyc`/`__pycache__/`/`egg-info` = 0 (16 staged for removal) |
| **V3** mqengine `.gitignore` effective | **PASS** | `.env`→ignored; `.env.example`→NOT ignored |
| **V4** mqnode_cloud `.gitignore` effective | **PASS** | staged; `.env`→ignored; `data/.gitkeep` tracked |
| **V5** mqnode_test2 confirm-only | **PASS** | untouched; status_after == status_before |
| **V6** mqchain-console confirm-only | **PASS** | untouched; status_after == status_before |
| **V7** full re-audit | **PASS** | recovery untracked; `.gitignore` present in both; env files untracked; pattern scan clean |
| **V8** MQAI scripted gates | **PASS** | risk HIGH, write_scope (MQAI folder), secret_scan clean (V0 caveat: MQAI-folder only) |
| **V9** product-repo write-scope guard | **PASS** | see below |
| **V10** secret-safe / no-leak scan | **PASS (triaged)** | see below |

## V9 — product-repo write-scope guard (post-replay)
- **Confirm-only:** `mqnode_test2`, `mqchain-console` untouched; `status_after == status_before`. PASS.
- **Change repos — touched ⊆ allow-list:**
  - `mqengine` (off `main`): `.gitignore` (A); `PyPI-Recovery-Codes-*.txt` (D); 5× `mqengine.egg-info/*`
    (D); 11× `mqengine/__pycache__/*.cpython-311.pyc` (D). ⊆ { `.gitignore`, `PyPI-Recovery-Codes*.txt`,
    `*.pyc`, `__pycache__/**`, `mqengine.egg-info/**` }. PASS.
  - `mqnode_cloud` (off `main`): `.gitignore` (A) only. ⊆ { `.gitignore` }. PASS.

## V10 — secret-safe / no-leak scan (post-replay)
- Only `diff --git` artifacts are the two `.gitignore` diffs (each `a/.gitignore b/.gitignore`).
- No recovery-code CONTENTS in any `+`/`-` line (only the benign `.gitignore` glob add-line).
- Secret-shape scan of `output/` + `review/` → **no matches**.
- Recovery file on disk (not deleted), untracked, ignored.
- **PASS** (benign filename/glob references only; no secret material leaked).

## Gate B pre-commit guard (2026-07-09)
Re-ran immediately before commit:
- **V9: PASS** — mqengine staged ⊆ allow-list; mqnode_cloud staged = `.gitignore`; confirm-only
  repos unchanged.
- **V10: PASS** — only `.gitignore` content diffs; no recovery-code contents; secret-shape scan clean.
Commits: mqengine `62c4243`, mqnode_cloud `4b0e7ae` (local only; **no push**). See `commit_records.md`.

## Overall
**V1–V10: PASS** on the main-based staged state, and **re-passed as the Gate-B pre-commit guard**.
Committed locally (no push). Remaining: push/merge decision + closeout.

## Closeout re-guard (2026-07-09)
V9 PASS + V10 PASS (triaged benign) re-run at closeout against committed diffs. See review/closeout_review.md.
