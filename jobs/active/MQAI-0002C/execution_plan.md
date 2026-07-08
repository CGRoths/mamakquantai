# MQAI-0002C — Execution Plan

> SCAFFOLD. Exact commands proposed for the FUTURE authorized execution. NONE are run at scaffold
> time. All product-repo steps are GATED behind `execution_authorized == true`. Commands are shown
> for Git Bash and/or PowerShell; the execution job picks one consistently.
> No command below reads secret file contents.

## Step 0 — Pre-flight (read-only; safe to run anytime)
```bash
# Per target repo: confirm current state before touching anything.
git -C "<repo>" rev-parse --short HEAD
git -C "<repo>" status --porcelain | head
```
- [ ] Record HEAD + dirty state per repo into `output/preflight.md`.
- [ ] Confirm PyPI codes already rotated (Cray attestation on file).

## Step 1 — Create working branch per repo (gated)
```bash
git -C "<repo>" switch -c chore/mqai-0002c-sechygiene
```
Applies to: `mqengine`, `mqnode_cloud`. (`mqnode_test2`, `mqchain-console` = confirm-only, no branch.)

## Step 2 — mqengine: add `.gitignore` (gated; CREATE new file)
Exact file path: `C:\MAMAKQUANT\mqengine_lib_full\.gitignore`

Narrowed, scoped content (no broad `*recovery*` / `*credential*` / `*_token*`):
```gitignore
# --- Recovery codes (anchored to the known filename shape) ---
/PyPI-Recovery-Codes*.txt
/pypi-recovery-codes*.txt

# --- Secrets / credentials (never commit) ---
.env
.env.*
!.env.example
*.pem
*.key
*.p12
*.pfx
*.secret
*.token

# --- Python build / cache noise ---
__pycache__/
*.pyc
*.egg-info/
.pytest_cache/
.ruff_cache/
build/
dist/
```

## Step 3 — mqengine: untrack the recovery file + already-tracked generated artifacts (gated)
Index-only; NO disk deletion; NO reading contents.
```bash
# 3a. Untrack the recovery-codes file (exact, quoted).
git -C "<mqengine>" rm --cached "PyPI-Recovery-Codes-CrayNg05-2026-04-16T20_23_27.926753.txt"
```
```powershell
# 3b. Untrack already-tracked generated artifacts (pyc / __pycache__ / egg-info).
$generated = git ls-files |
  Select-String -Pattern '(^|/)(__pycache__/|.*\.pyc$|mqengine\.egg-info/)' |
  ForEach-Object { $_.Line }
if ($generated.Count -gt 0) { git rm --cached -r -- $generated }
```
> Rationale: `.gitignore` prevents FUTURE tracking only; it does NOT untrack already-committed files.

## Step 4 — mqnode_cloud: add `.gitignore` (gated; CREATE new file)
Exact file path: `C:\MAMAKQUANT\mqnode_cloud\.gitignore`
```gitignore
# --- Secrets / credentials (never commit) ---
.env
.env.*
!.env.example
*.pem
*.key
*.p12
*.pfx
*.secret
*.token

# --- Python cache noise ---
__pycache__/
*.pyc

# --- Local data ---
data/*
!data/.gitkeep
```

## Step 5 — mqnode_test2: confirm-only (read-only; NO write)
```bash
git -C "<mqnode_test2>" ls-files .env            # expect empty
git -C "<mqnode_test2>" check-ignore .env        # expect ignored
```

## Step 6 — mqchain-console: confirm-only (read-only; NO write)
```bash
git -C "<mqchain-console>" ls-files .env.local       # expect empty
git -C "<mqchain-console>" check-ignore .env.local   # expect ignored
```

## Step 7 — Stage + review BEFORE commit (gated)
```bash
git -C "<repo>" add .gitignore
git -C "<repo>" status
git -C "<repo>" diff --cached --stat
```
- [ ] Produce the staged diff into `output/staged_diff.md` for Claude review of the ACTUAL change.
- [ ] **DO NOT COMMIT YET** — commit only after `validation_plan.md` passes + full consensus.

## Step 8 — Commit (only after ALL gates + Cray approval)
```bash
git -C "<repo>" commit -m "chore(security): add .gitignore; untrack recovery file + generated artifacts (MQAI-0002C)"
```
- [ ] No push in this job unless separately authorized.

## Explicitly NOT in this plan
- No history purge (RP7) — separate authorization required.
- No disk deletion of the recovery file (Cray handles the local copy out-of-band).
