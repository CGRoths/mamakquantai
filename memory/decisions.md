# Decisions

Durable decisions and their rationale. Append-only; newest at top.

---

## 2026-07-09 — MQAI-0001 approved & promoted

- **MQAI-0001 (Repo Cartography) completed and Cray-approved.** Four `map.md` files promoted into
  `repo_control/<repo>/map.md` with git-provenance banners (HEAD + dirty-state per repo). Job moved
  to `jobs/completed/MQAI-0001/`.
- **Promotion carried provenance** (review rec #B): each promoted map records the product repo's
  HEAD and working-tree state at map time — mqnode_test2 `4207b66` (dirty), mqnode_cloud `aad7187`
  (dirty), mqengine `c2d5d40` (dirty), mamakquantchainintel `e84cd92` (clean).
- **First proof that the file-first control plane works** end-to-end: build → scripted evals →
  independent Claude review → Cray decision → human-gated promotion → memory update.
- **Open follow-ups (tracked, not yet done):** (#A) reconcile `inventory.json` schema with
  `repo_mapper.md`; (#C) remove + rotate mqengine `PyPI-Recovery-Codes-*.txt`, confirm `.env`/
  `.env.local` are git-ignored; (#D) narrow each `critical_files.md` from `**` to verified critical
  paths now that maps exist.

---

## 2026-07-09 — V0 founding decisions

- **MQAI is the operator layer, not MQBRAIN.** No alpha/strategy/capital logic in MQAI.
- **File-first V0.** No SQLite, dashboard, MCP bridge, or quota failover yet.
- **AGENTS.md is canonical; CLAUDE.md is a pure pointer.**
- **Agents stage in `jobs/active/<id>/output/`; promoted truth lives in `repo_control/<repo>/`.**
- **Promotion is human-gated.** Agents never self-promote.
- **Risk tier is path-derived from `critical_files.md`,** never agent self-assessment.
- **`mqnode_test2` is the protected read-only baseline in V0.**
- **`map.md` files are placeholder-only** until produced by MQAI-0001.
- **`critical_files.md` seeded conservatively** (HIGH until cartography verifies exact paths).
- **V0 automation = semi-manual CLI with PowerShell wrappers** (no overbuilding).
- **MQAI-0001 = Repo Cartography, read-only,** across mqnode_test2, mqnode_cloud, mqengine,
  and mamakquantchainintel (`mqchain-console` only).
