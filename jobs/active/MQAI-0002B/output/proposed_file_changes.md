# MQAI-0002B — Proposed File Changes

> PROPOSAL ONLY. These changes are NOT applied. They are patch proposals for a future execution job.
> No product repo was edited. No file deleted. No commit/push. No secret file opened.

---

## Change 1 — `mqengine`: new `.gitignore` (NEW FILE)

Path: `C:\MAMAKQUANT\mqengine_lib_full\.gitignore` (does not exist today)

Proposed content:
```gitignore
# --- Secrets / credentials (never commit) ---
.env
.env.*
!.env.example
*.pem
*.key
*.p12
*.pfx
*.keystore
id_rsa
id_dsa
*_token*
*credential*
*recovery*

# --- Python build / cache noise ---
__pycache__/
*.pyc
*.egg-info/
.pytest_cache/
.ruff_cache/
build/
dist/
```

Notes:
- `*recovery*` ensures the rotated recovery-codes filename pattern can never be re-committed.
- The Python cache/egg-info lines also address the tracked `.pyc` bytecode noted in MQAI-0001.

---

## Change 2 — `mqengine`: untrack the recovery-codes file (INDEX CHANGE, not deletion)

Proposed command (execution job only):
```bash
git rm --cached "PyPI-Recovery-Codes-CrayNg05-2026-04-16T20_23_27.926753.txt"
```
- `--cached` removes it from the index only; the local file stays on disk (this job never deletes).
- Cray to relocate/remove the local copy manually out-of-band.
- Codes already rotated → the local copy is inert, but should not live inside a repo working tree.

---

## Change 3 — `mqnode_cloud`: new `.gitignore` (NEW FILE)

Path: `C:\MAMAKQUANT\mqnode_cloud\.gitignore` (does not exist today)

Proposed content:
```gitignore
# --- Secrets / credentials (never commit) ---
.env
.env.*
!.env.example
*.pem
*.key
*.p12
*.pfx
*.keystore
id_rsa
id_dsa
*_token*
*credential*
*recovery*

# --- Python cache noise ---
__pycache__/
*.pyc

# --- Local data ---
data/*
!data/.gitkeep
```

Notes:
- Preventive only — no secret present today. `data/` kept as an empty tracked dir via `.gitkeep`.

---

## Change 4 — `mqnode_test2`: NO CHANGE (confirm only)

- `.env` is already gitignored and untracked. `.gitignore` already exists (40 lines).
- Proposed: read-only confirmation in the execution job; **no file change**.

---

## Change 5 — `mqchain-console`: NO CHANGE (confirm only)

- `.env.local` is already gitignored and untracked. `.gitignore` already exists (42 lines).
- Proposed: read-only confirmation in the execution job; **no file change**.

---

## Explicitly NOT proposed here
- No history rewrite / `filter-repo` / BFG execution (RP7 is documented in `remediation_plan.md`
  only, and is optional now that rotation is complete).
- No deletion of any local file.
- No edits to formulas, schema, or any source logic — these are `.gitignore` + index changes only.

## Layer / boundary note
All proposed changes are repository-hygiene only (`.gitignore` + index untracking). They touch no
data-truth, label-truth, or research logic, and assert no cross-layer ownership. Every change is a
product-repo write and therefore reserved for a separately-authorized HIGH-tier execution job.
