# Decisions

Durable decisions and their rationale. Append-only; newest at top.

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
