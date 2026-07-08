# MQAI-0002C — Validation Plan

> SCAFFOLD. Read-only verifications the execution job runs. None open secret files. Recovery-file
> detection is CASE-INSENSITIVE + ANCHORED (a case-sensitive `grep -c recovery` is a false pass
> against the capital-"R" filename).

## V1 — Recovery file untracked (mqengine)
- Check (PowerShell):
  ```powershell
  (git ls-files | Select-String -Pattern '(?i)PyPI-Recovery-Codes.*\.txt').Count
  ```
- Check (Git Bash):
  ```bash
  git ls-files | grep -Ei 'PyPI-Recovery-Codes.*\.txt'
  ```
- [ ] BEFORE execution: count **>= 1** (file currently tracked).
- [ ] AFTER execution: count **0** (untracked).
- [ ] `git check-ignore` on a sample `PyPI-Recovery-Codes-<x>.txt` → ignored via `/PyPI-Recovery-Codes*.txt`.

## V2 — Generated artifacts untracked (mqengine)
- [ ] `git ls-files | grep -Ei '\.pyc$'` → empty.
- [ ] `git ls-files | grep -Ei '__pycache__/'` → empty.
- [ ] `git ls-files | grep -Ei 'mqengine\.egg-info/'` → empty.
- [ ] Before/after counts captured to `output/reaudit.md` (expected before: 11 `.pyc`, 5 `egg-info`).

## V3 — mqengine `.gitignore` effective
- [ ] `.gitignore` exists at repo root.
- [ ] `git check-ignore .env` → ignored; `git check-ignore .env.example` → NOT ignored (stays tracked).

## V4 — mqnode_cloud `.gitignore` effective
- [ ] `.gitignore` exists at repo root.
- [ ] `git check-ignore .env` → ignored.
- [ ] `data/.gitkeep` still tracked; other `data/*` ignored.

## V5 — mqnode_test2 confirm-only (no change)
- [ ] `git ls-files .env` → empty; `git check-ignore .env` → ignored; `git log --all -- .env` → 0.

## V6 — mqchain-console confirm-only (no change)
- [ ] `git ls-files .env.local` → empty; `git check-ignore .env.local` → ignored;
      `git log --all -- .env.local` → 0.

## V7 — Full re-audit (rerun MQAI-0002 hygiene checks)
- [ ] Tracked secret-risk filename scan → clean in all four repos.
- [ ] Counts-only secret-pattern scan of tracked source → 0 matches.
- [ ] `secret_content_read: false` maintained throughout; no secret values in any MQAI output.

## V8 — MQAI eval gates (on this job's output)
- [ ] `risk_tier_assignment` → HIGH.
- [ ] `write_scope_check` → product-repo writes confined to the authorized branch + allowed paths;
      MQAI writes confined to `jobs/active/MQAI-0002C/`.
- [ ] `secret_scan` → no secret values in MQAI output.
- [ ] `cross_layer_violation_check` → hygiene-only, no cross-layer authorship.

## Pass criteria
All V1–V8 satisfied AND full consensus complete (Claude review of executed diff + GPT synthesis +
Cray approval) before any commit is finalized/pushed.
