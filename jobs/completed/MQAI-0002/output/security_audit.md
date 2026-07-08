# MQAI-0002 — Security Hygiene Audit

> Read-only audit. No product-repo writes. No remediation performed.
> **No secret file was opened, read, printed, or copied.** Findings reference paths/filenames and
> git metadata only. `secret_content_read = false` for every item.
> Date: 2026-07-09. Builder stage output — NOT promoted.

## Method (all read-only)
- `git ls-files` — enumerate tracked files, filter by secret-risk filename patterns.
- `git check-ignore` — confirm whether secret-risk paths are ignored.
- `git log --all -- <path>` — detect secret-risk files in history **by filename only**.
- `git grep -cE` — scan tracked NON-secret files for secret-like patterns, reporting **file + match
  count only** (never the matching line or value).
- `.gitignore` files were read (not secret). `.env` / `.env.local` / recovery-code files were
  **never opened**; only their existence and git status were checked.

## Result summary

| Repo | .gitignore | Secret-risk file | Tracked? | Ignored? | In history? | Risk |
|------|-----------|------------------|----------|----------|-------------|------|
| mqengine | **MISSING** | `PyPI-Recovery-Codes-*.txt` | **YES** | no | **YES (1 commit)** | **CRITICAL** |
| mqnode_cloud | **MISSING** | none present | — | — | — | **MEDIUM** (preventive) |
| mqnode_test2 | yes (40 ln) | `.env` | no | **yes** | no | LOW |
| mamakquantchainintel | yes (42 ln) | `.env.local` | no | **yes** | no | LOW |

## Findings

### F1 — CRITICAL: PyPI recovery codes committed to `mqengine`
- `PyPI-Recovery-Codes-CrayNg05-2026-04-16T20_23_27.926753.txt` is **git-tracked**, present in
  `HEAD`, and appears in git history (1 commit touching the path). It is **not** gitignored (the repo
  has no `.gitignore`).
- Impact: PyPI account recovery codes are account-takeover credentials. If this repo was ever pushed
  to `github.com/CGRoths/mqengine` (remote confirmed in MQAI-0001), the codes must be treated as
  **compromised**.
- Contents were **not** read. Finding is based on filename + git tracking/history metadata only.

### F2 — HIGH: `mqengine` has no `.gitignore`
- No ignore rules exist, which is the root cause of F1 (and of committed `.pyc` bytecode observed in
  MQAI-0001). Any `.env`/key/token created here would be committable by default.

### F3 — MEDIUM: `mqnode_cloud` has no `.gitignore`
- No secret file is present today, but there is no protection against a future `.env`/key being
  committed. Preventive gap.

### F4 — LOW: `mqnode_test2` `.env`
- `.env` exists locally but is **correctly gitignored** and has **never** been committed
  (0 commits touch the path). No action required beyond keeping it ignored.

### F5 — LOW: `mamakquantchainintel/mqchain-console` `.env.local`
- `.env.local` exists locally but is **correctly gitignored** and has **never** been committed.
  No action required.

## Secret-pattern scan (tracked source files)
Scanned all tracked files (excluding `.env.example`, lockfiles) in all four repos for:
private-key blocks, AWS access keys, GitHub/Slack tokens, and `key/secret/token/password = <long
value>` assignments. **Zero matches** in every repo. (Counts-only scan; no values inspected.)

## Notes / limitations
- `.env.example` files (tracked, expected) were **excluded** from the pattern scan and **not** opened;
  a manual eyeball that they contain only placeholders is recommended but out of this read-only scope.
- History check is **filename-scoped** per instructions; a full deep-history content scan
  (e.g. gitleaks over all refs) is recommended as a follow-up in a dedicated tool-assisted job.
- This audit did not push, fetch, or mutate any repo.

## Cross-layer / boundary note
Findings are hygiene/security only and assert no layer ownership. No writes outside
`jobs/active/MQAI-0002/output/`.
