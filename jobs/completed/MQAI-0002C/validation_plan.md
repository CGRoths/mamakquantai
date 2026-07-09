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
- [ ] `secret_scan` → no secret values in MQAI output.
- [ ] `cross_layer_violation_check` → hygiene-only, no cross-layer authorship.
- [ ] `write_scope_check` → confirms MQAI writes are confined to `jobs/active/MQAI-0002C/`.
> IMPORTANT (W2): the V0 `write_scope_check` script ONLY audits the MQAI job folder. It does NOT and
> cannot police product-repo writes. Product-repo write scope is enforced separately by V9 (manual
> path guard) — do NOT treat a `write_scope_check` pass as evidence that product-repo writes were
> in-scope.

## V9 — Product-repo write-scope guard (MANDATORY manual/scripted, per target repo)
Enforces that ONLY the paths in `allowed_writes.md` were touched by MQAI-0002C on each remediation
branch. Repos may be dirty BEFORE the job (verified pre-existing state, e.g. `mqnode_test2` has a
modified `docker-compose.yml`), so validation proves **no NEW change was introduced**, not that the
tree is empty.
- Baseline capture (before Gate-A work), per repo, into `output/`:
  ```bash
  git -C "<repo>" rev-parse HEAD                  > output/<repo>_baseline_head.txt
  git -C "<repo>" status --porcelain              > output/<repo>_status_before.txt
  git -C "<repo>" ls-files                        > output/<repo>_lsfiles_before.txt
  ```
- Post-work capture (after staging, before commit), per repo, into `output/`:
  ```bash
  git -C "<repo>" status --porcelain              > output/<repo>_status_after.txt
  git -C "<repo>" diff --cached --name-only       > output/<repo>_touched_paths.txt
  ```
- [ ] **Confirm-only repos (`mqnode_test2`, `mqchain-console`): require
      `status_after == status_before`** (byte-identical). This proves MQAI-0002C introduced NO new
      change even if the repo was already dirty. Do NOT require an empty status. Any new/changed path
      vs baseline → FAIL → rollback.
      ```bash
      diff "output/<repo>_status_before.txt" "output/<repo>_status_after.txt"   # expect no output
      ```
- [ ] **Change repos (`mqengine`, `mqnode_cloud`): the DELTA vs baseline must be ⊆ the allow-list.**
      Compute the set difference (paths present in `status_after`/`touched_paths` but not attributable
      to pre-existing `status_before` state) and compare to `allowed_writes.md`. Any path outside the
      allow-list → FAIL → rollback.
- [ ] `mqengine` allowed delta ⊆ { `.gitignore`, `PyPI-Recovery-Codes*.txt`, `*.pyc`,
      `__pycache__/**`, `mqengine.egg-info/**` }.
- [ ] `mqnode_cloud` allowed delta ⊆ { `.gitignore` }.
- [ ] All V9 capture files (`*_status_before.txt`, `*_status_after.txt`, `*_touched_paths.txt`,
      `*_baseline_head.txt`, `*_lsfiles_before.txt`) saved under `jobs/active/MQAI-0002C/output/`
      (evidence trail).

## V10 — Secret-safe capture / no-leak scan (MANDATORY, S1)
Ensures the remediation evidence never contains recovery-code or deleted secret-file contents.
- [ ] **Recovery-code removal evidence is metadata-only.** For `PyPI-Recovery-Codes*.txt` (and any
      secret-like path), the only captured artifacts are `--name-status`, `--stat`, `--summary`
      (Step 7a). No full-content diff of these paths exists anywhere in `output/` or `review/`.
- [ ] **No unrestricted `git diff --cached` output was saved.** Only 7a (metadata), 7b (`.gitignore`
      full diff), and 7c (sanitized, secret-paths excluded) may appear.
- [ ] **Leak scan of `output/` and `review/`** — after execution, scan both trees for accidental
      secret-like material (counts/locations only; do NOT print matches):
      ```bash
      grep -rIlE -- "-----BEGIN [A-Z ]*PRIVATE KEY-----|AKIA[0-9A-Z]{16}|xox[baprs]-|gh[pousr]_[A-Za-z0-9]{20,}" \
        jobs/active/MQAI-0002C/output jobs/active/MQAI-0002C/review
      # plus: confirm no file under output/ or review/ contains recovery-code line material.
      ```
      Expected: **no matches**. Any hit → FAIL → treat as a secret-handling incident (do NOT commit;
      quarantine/rewrite the offending MQAI artifact; append failure_taxonomy `secret_leak`).
- [ ] `secret_content_read: false` reaffirmed: no secret file was opened at any step.

## Pass criteria
All V1–V10 satisfied AND full consensus complete (Claude review of executed diff + GPT synthesis +
Cray final approval / Gate B) before any commit is finalized/pushed.
