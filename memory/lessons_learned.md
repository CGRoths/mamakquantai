# Lessons Learned

What worked / what didn't, per job. Append-only; newest at top.

---

## MQAI-0002B — Security Remediation Plan (planning-only, HIGH-tier)

- **What worked:**
  - The HIGH-tier consensus chain earned its keep: independent review caught a **false-pass
    validation check** (`grep -c recovery` is case-sensitive vs a capital-"R" filename) that would
    have "confirmed" remediation regardless of outcome. Live re-verification (`grep -c`=0 vs
    `grep -ic`=1) proved it before it could mislead an execution job.
  - request_changes → builder fix → v2 approve → GPT synthesis → Cray plan-only approval is a clean,
    auditable loop. Keeping v1 and v2 reviews side-by-side preserved provenance.
  - Firm plan/execution split: approving a plan never authorizes the writes; execution is pushed to a
    named, separately-authorized job (MQAI-0002C).
- **What didn't / friction:**
  - Same class of bug recurred in my own re-verify (`grep -c recovery`) — case sensitivity on Windows
    filenames is an easy trap; standardize case-insensitive/anchored matching in all secret checks.
  - `.gitignore` misconception (that it untracks committed files) had to be explicitly corrected in
    the plan — worth encoding as a standing rule.
- **Change to process:**
  - Add "case-insensitive + anchored matching" and "`.gitignore` does not untrack committed files"
    to the security-hygiene skill/checklist.
  - Execution jobs must always ship rollback notes + before/after `git ls-files` capture.

---

## MQAI-0002 — Security Hygiene Audit (read-only)

- **What worked:**
  - Metadata-only auditing proved you can find a CRITICAL exposure (committed PyPI recovery codes)
    **without ever opening the secret file** — `git ls-files`, `git check-ignore`, `git log -- <path>`,
    and counts-only `git grep` were sufficient. `secret_content_read: false` held for all 8 items.
  - Independent reviewer re-ran the git metadata checks and confirmed every severity claim; the
    counts-only pattern scan kept values out of MQAI output (verified by a second scan).
  - Clean separation of audit vs remediation: approval accepted findings but authorized nothing
    destructive; remediation was pushed to a dedicated HIGH-tier job (MQAI-0002B).
- **What didn't / friction:**
  - Shell delimiter bug: `${entry##*:}` ate the `C:` drive letter on Windows paths. Use `|` (or
    another non-colon delimiter) when packing `name:path` pairs for Windows.
  - Same V0 gap as MQAI-0001: scripted `write_scope_check`/`secret_scan` ran with empty input sets,
    so their pass is weak — manual verification remained necessary.
  - History check is filename-scoped only; a deep-history content scan (gitleaks/trufflehog) is still
    needed and is deferred to a follow-up.
- **Change to process:**
  - Standardize a Windows-safe path-passing convention in orchestrator/audit scripts.
  - Add a reusable read-only "secret hygiene" checklist (tracked-file filename patterns, gitignore
    coverage, history-by-filename, counts-only pattern scan) as an MQAI skill.
  - Wire real touched-path/write-set collection into the gates (carried over from MQAI-0001).

---

## MQAI-0001 — Repo Cartography (read-only)

- **What worked:**
  - File-first handoff held: builder wrote only to `output/`, reviewer only to `review/`,
    promotion gated on explicit `cray_decision.md`. No boundary violations.
  - Independent reviewer verification (path spot-checks, mtime analysis, own secret scan) caught
    that product repos were *pre-existing dirty* — not touched by the job. Trusting the scripted
    gates alone would have missed this, since V0 `write_scope_check`/`secret_scan` ran with empty
    input sets.
  - Builder proactively surfaced 3 secret-risk files (incl. committed PyPI recovery codes) without
    capturing any values.
- **What didn't / friction:**
  - `risk_tier_assignment` returned HIGH for a read-only job because `critical_files.md` is seeded
    `**`. Tier vs `consensus_mode: low` mismatched. Harmless here, but noisy.
  - V0 scripted gates don't actually collect the write-set / touched paths, so their "pass" is weak
    on its own — reviewer had to verify manually.
  - `inventory.json` diverged from the `repo_mapper.md` flat-`files[]` schema (richer, but
    non-conforming).
- **Change to process:**
  - After first cartography, narrow `critical_files.md` to real paths so tiers become meaningful.
  - Wire actual write-set/touched-path collection into the orchestrator before any write-capable job.
  - Record git HEAD + dirty state in every future map (now done for MQAI-0001).
  - Decide whether to bless the richer `inventory.json` schema in `repo_mapper.md` or normalize.

---

## Template

- **Job:** <id>
- **What worked:**
- **What didn't:**
- **Change to process:**
