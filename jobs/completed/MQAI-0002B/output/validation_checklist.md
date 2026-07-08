# MQAI-0002B — Validation Checklist

> For use by the FUTURE execution job (after Cray authorizes execution). This job (MQAI-0002B)
> produces the checklist; it does NOT run it against a remediated tree. All checks are read-only
> verifications; none open secret files.

## Pre-execution gate
- [ ] Cray has authorized a separate HIGH-tier **execution** job (this plan approval is not enough).
- [ ] Confirmed: PyPI recovery codes already rotated (done 2026-07-09).
- [ ] Working on a branch, not a protected mainline, in each product repo.

## RP1 — recovery file untracked (`mqengine`)
> The tracked filename has a capital "R" (`PyPI-Recovery-Codes-...`). A case-sensitive
> `grep -c recovery` returns 0 even while the file IS tracked — a false pass. Use a
> CASE-INSENSITIVE / anchored match.
- Check (PowerShell):
  ```powershell
  (git ls-files | Select-String -Pattern '(?i)PyPI-Recovery-Codes.*\.txt').Count
  ```
  - before remediation: **>= 1**
  - after remediation execution: **0**
- Check (Git Bash alternative):
  ```bash
  git ls-files | grep -Ei 'PyPI-Recovery-Codes.*\.txt'   # matches before, empty after
  ```
- [ ] Count is **>= 1 before** and **0 after** the execution job runs `git rm --cached`.
- [ ] Local file, if still present, is inert (codes already rotated) — relocate/remove out-of-band.
- [ ] `git check-ignore "PyPI-Recovery-Codes-2026.txt"` (any sample name) → ignored, matched by the
      anchored pattern `/PyPI-Recovery-Codes*.txt` (NOT a broad `*recovery*`).

## RP2 — `.gitignore` added (`mqengine`)
- [ ] `.gitignore` exists at repo root.
- [ ] `git check-ignore .env` → ignored; `git check-ignore .env.example` → NOT ignored (still tracked).
> Note: `.gitignore` only prevents FUTURE tracking. It does NOT untrack files already committed.
> Already-tracked generated artifacts must be explicitly untracked — see RP2G.

## RP2G — untrack already-tracked generated artifacts (`mqengine`)
`mqengine` currently tracks generated artifacts (verified during review: 11 `.pyc`,
5 `mqengine.egg-info/` entries). `.gitignore` alone will not remove them; the execution job must
untrack them explicitly (index-only; no disk deletion).
- Proposed command (EXECUTION JOB ONLY — do NOT run in a planning job):
  ```powershell
  $generated = git ls-files |
    Select-String -Pattern '(^|/)(__pycache__/|.*\.pyc$|mqengine\.egg-info/)' |
    ForEach-Object { $_.Line }
  if ($generated.Count -gt 0) { git rm --cached -r -- $generated }
  ```
- Validation AFTER execution:
  - [ ] `git ls-files | grep -Ei '\.pyc$'` → empty.
  - [ ] `git ls-files | grep -Ei '__pycache__/'` → empty.
  - [ ] `git ls-files | grep -Ei 'mqengine\.egg-info/'` → empty.

## RP3 — `.gitignore` added (`mqnode_cloud`)
- [ ] `.gitignore` exists at repo root.
- [ ] `git check-ignore .env` → ignored.
- [ ] `data/.gitkeep` still tracked; other `data/*` ignored.

## RP4 — `mqnode_test2/.env` (confirm, no change)
- [ ] `git ls-files .env` → empty.
- [ ] `git check-ignore .env` → ignored.
- [ ] `git log --all --oneline -- .env` → 0 commits.

## RP5 — `mqchain-console/.env.local` (confirm, no change)
- [ ] `git ls-files .env.local` → empty.
- [ ] `git check-ignore .env.local` → ignored.
- [ ] `git log --all --oneline -- .env.local` → 0 commits.

## RP6 — full re-audit (rerun MQAI-0002 checks)
- [ ] Tracked secret-risk filename scan → clean in all four repos.
- [ ] Counts-only secret-pattern scan of tracked source → 0 matches (unchanged).
- [ ] `.gitignore` now present in mqengine + mqnode_cloud.
- [ ] Produce `reaudit.md` summarizing before/after; `secret_content_read: false` maintained.

## RP7 — optional history purge (only if separately authorized)
- [ ] NOT run unless Cray explicitly authorizes in the execution job.
- [ ] If run: verify `git log --all -- "<recovery filename>"` → 0 across all refs; force-push done;
      collaborators notified to re-clone.

## MQAI eval gates (execution job)
- [ ] `risk_tier_assignment` → HIGH (expected).
- [ ] `write_scope_check` → writes confined to authorized product-repo branch(es) + job output.
- [ ] `secret_scan` → no secret values in MQAI output.
- [ ] `cross_layer_violation_check` → changes are hygiene-only, no cross-layer authorship.

## Sign-off
- [ ] Claude review of the executed changes = approve.
- [ ] Cray decision recorded for the execution job.
