# Lessons Learned

What worked / what didn't, per job. Append-only; newest at top.

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
