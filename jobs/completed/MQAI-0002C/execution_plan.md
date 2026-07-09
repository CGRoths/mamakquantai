# MQAI-0002C — Execution Plan

> SCAFFOLD. Exact commands proposed for the FUTURE authorized execution. NONE are run at scaffold
> time. Two-gate authorization (see `job.yaml`):
> - Steps 1–7 (branch, `.gitignore`, `git rm --cached`, stage, diff) require **Gate A**
>   (`execution_authorized == true`) — branch-local only, NO commit/push.
> - Step 8 (commit) requires **Gate B** (`commit_authorized == true`) after V1–V10 + executed-diff
>   review + GPT synthesis + Cray final approval.
> Commands are shown for Git Bash and/or PowerShell; the execution job picks one consistently.
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
# 3a. Untrack the recovery-codes file via ANCHORED GLOB (not a hardcoded exact name).
#     Consistent with the case-insensitive/anchored detection in validation_plan.md V1.
git -C "<mqengine>" rm --cached -- 'PyPI-Recovery-Codes*.txt'
```
```powershell
# 3b. Untrack already-tracked generated artifacts (pyc / __pycache__ / egg-info).
$generated = git ls-files |
  Select-String -Pattern '(^|/)(__pycache__/|.*\.pyc$|mqengine\.egg-info/)' |
  ForEach-Object { $_.Line }
if ($generated.Count -gt 0) { git rm --cached -r -- $generated }
```
> Rationale: `.gitignore` prevents FUTURE tracking only; it does NOT untrack already-committed files.
> S1 WARNING: after this `git rm --cached`, do NOT run/save an unrestricted `git diff --cached` — it
> would print the deleted recovery-code contents. Capture removal evidence metadata-only (Step 7a).

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

## Step 7 — Stage + capture SECRET-SAFE diff BEFORE commit (Gate A)
> S1 (secret-safe diff capture): a `git rm --cached` of a secret file makes an unrestricted
> `git diff --cached` print the DELETED file's contents. That would leak recovery-code / secret
> material into MQAI output. **Never run or save an unrestricted `git diff --cached`.**

```bash
git -C "<repo>" add .gitignore
git -C "<repo>" status --porcelain
```

### 7a. Metadata-only capture for ALL staged changes (always safe)
```bash
git -C "<repo>" diff --cached --name-status   > output/<repo>_staged_name_status.txt
git -C "<repo>" diff --cached --stat          > output/<repo>_staged_stat.txt
git -C "<repo>" diff --cached --summary       > output/<repo>_staged_summary.txt
```
These show WHICH paths changed and how (A/M/D + line counts) without printing file contents. This is
the authoritative capture for recovery-code / secret-like removals (e.g. `PyPI-Recovery-Codes*.txt`,
`*.pyc`, `mqengine.egg-info/`).

### 7b. Full-content diff — ONLY for newly-created `.gitignore` policy files
`.gitignore` files are newly created here and must contain no secrets, so a full diff is safe:
```bash
git -C "<repo>" diff --cached -- .gitignore   > output/<repo>_gitignore_diff.txt
```

### 7c. If a broader full diff is ever needed — EXCLUDE secret-like paths
```bash
git -C "<repo>" diff --cached -- . \
  ':(exclude)PyPI-Recovery-Codes*.txt' ':(exclude)*.pem' ':(exclude)*.key' \
  ':(exclude)*.p12' ':(exclude)*.pfx' ':(exclude)*.secret' ':(exclude)*.token' \
  ':(exclude).env' ':(exclude).env.*'   > output/<repo>_staged_diff_sanitized.txt
```

- [ ] `output/staged_diff.md` (for executed-diff review) is assembled from 7a + 7b + 7c ONLY.
      It MUST NOT contain any unrestricted `git diff --cached` output.
- [ ] Capture pre/post `git status` + touched-path comparison per repo (see `validation_plan.md` V9).
- [ ] Run the leak scan (`validation_plan.md` V10) over `output/` and `review/` after capture.
- [ ] **DO NOT COMMIT** — Step 8 is blocked until Gate B (V1–V10 + executed-diff review + GPT
      synthesis + Cray final approval). Gate A ends here.

## Step 8 — Commit (Gate B only: after V1–V10 + executed-diff review + GPT synthesis + Cray final approval)
```bash
git -C "<repo>" commit -m "chore(security): add .gitignore; untrack recovery file + generated artifacts (MQAI-0002C)"
```
- [ ] No push in this job unless separately authorized.

## Explicitly NOT in this plan
- No history purge (RP7) — separate authorization required.
- No disk deletion of the recovery file (Cray handles the local copy out-of-band).
