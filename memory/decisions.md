# Decisions

Durable decisions and their rationale. Append-only; newest at top.

---

## 2026-07-09 — MQAI-0002 approved & closed (audit accepted, no remediation)

- **MQAI-0002 (Security Hygiene Audit) Cray-approved and moved to `jobs/completed/`.** Read-only;
  no product-repo writes, no remediation, no secret file opened.
- **Approval accepts findings only** — explicitly does NOT authorize remediation, product-repo
  writes, file deletion, opening secret files, or `repo_control` promotion. Job had
  `promotion.target: none`, so nothing was promoted.
- **Accepted findings:** CRITICAL — `mqengine` tracks `PyPI-Recovery-Codes-*.txt` in HEAD + history;
  HIGH — `mqengine` has no `.gitignore`; MEDIUM — `mqnode_cloud` has no `.gitignore`; LOW —
  `mqnode_test2/.env` and `mqchain-console/.env.local` present but gitignored & untracked; CLEAN —
  tracked-source secret-pattern scan found zero matches.
- **Mandated follow-up:** a separate HIGH-tier job **MQAI-0002B — Security Remediation** must handle
  (1) PyPI recovery-code rotation by Cray, (2) removing the tracked file from `mqengine`,
  (3) adding `.gitignore` coverage, (4) confirming `.env`/`.env.local` stay untracked,
  (5) considering history purge **only after** rotation.
- **Incident note:** PyPI recovery-code rotation is a live account-takeover risk and should be done
  by Cray immediately, independent of any git cleanup.

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
