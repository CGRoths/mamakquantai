# MQAI-0002C — Scaffold Fix Notes v3

> Final scaffold-only security correction: **S1 — secret-safe diff capture.**
> Scaffold files only — no remediation, no product repo touched, no `git rm`, no product-repo
> `.gitignore` created, no deletion, no history rewrite, no secret contents inspected, no commit/push.
> Date: 2026-07-09. Applied while `execution_authorized=true` (Gate A) but BEFORE any Gate-A branch work.

## S1 — fixed: secret-safe diff capture
**Problem:** after `git rm --cached -- 'PyPI-Recovery-Codes*.txt'`, an unrestricted
`git diff --cached` would print the DELETED recovery-code contents into MQAI output — violating the
no-secret-content rule.

**Fix (scaffold-only):**
- **Unrestricted staged diff capture is FORBIDDEN when deleted files may contain secrets.**
- **Recovery-code removal evidence must be metadata-only** (`--name-status`, `--stat`, `--summary`).
- Full-content diffs allowed ONLY for newly-created `.gitignore` policy files (no secrets by
  construction), or via a sanitized diff that excludes secret-like paths.

## Changes applied
- `execution_plan.md` — Step 7 rewritten as **secret-safe capture** (7a metadata-only for all staged
  changes; 7b full diff for `.gitignore` only; 7c sanitized full diff excluding secret-like paths);
  `output/staged_diff.md` assembled from 7a+7b+7c only; S1 warning added under Step 3.
- `validation_plan.md` — new **V10 (secret-safe / no-leak scan)**: recovery-code removal evidence is
  metadata-only; no unrestricted `git diff --cached` saved; leak scan of `output/`+`review/`
  (counts/locations only) must find nothing; any hit → FAIL (secret_leak incident).
- `forbidden_actions.md` — added **#1a** (no unrestricted full diff of secret-like deleted files) and
  **#1b** (no writing deleted recovery-code/secret contents into `output/`/`review/`); #6 updated to
  V1–V10 + "sanitized" diff.
- `review_requirements.md` — executed-diff review MUST rely on `--name-status`/`--stat`/`--summary`
  for recovery removal (not a file-content diff), must verify captures are sanitized and V10 passed;
  hard gate now `V1–V10`.
- Chain-range consistency: full-chain references updated `V1–V9 → V1–V10` in `job.yaml` (gate_B
  precondition + gating rule), `forbidden_actions.md` #6, `execution_plan.md` (intro/Step 7/Step 8),
  `review_requirements.md`.

## Note on the already-signed Gate A approval
`review/cray_execution_approval.md` (signed earlier this session, before V10 existed) references
"V1–V9". It was **not** retroactively edited (it is a signed decision record). V10 only ADDS a
secret-safety validation and does not weaken Gate A; **Gate B now requires V1–V10** (this supersedes
the V1–V9 phrasing in that approval). Recommend the eventual `cray_final_approval.md` (Gate B) state
V1–V10 explicitly.

## Status
Scaffold updated; still pre-execution. `execution_authorized=true` (Gate A), `commit_authorized=false`
(Gate B pending), `status: active`. No branch work started; no product repo touched.
