# MAMAKQUANTAI — Agent Operating Contract

> STATUS: canonical. `CLAUDE.md` and every agent (Codex, Claude, GPT) defer to this file.
> This is the constitution of MQAI. If anything elsewhere contradicts this file, this file wins.

---

## 0. Read Order

1. This file (`AGENTS.md`).
2. `company_brain/` — mission, non-negotiables, layer boundaries.
3. The active job's `jobs/active/<id>/job.yaml`.
4. The relevant `repo_control/<repo>/` files for every target repo in the job.
5. The relevant `skills/*.md` guide for the work being done.

---

## 1. What MQAI Is / Is Not

**MQAI is the operator / repo-control / engineering workflow layer.** It maps repos, creates jobs, routes work to Codex and Claude, runs eval gates, reviews outputs, preserves memory, and helps build candidate modules safely.

MQAI is **NOT**:
- Not MQBRAIN (future alpha discovery / strategy / capital allocation intelligence).
- Not an autonomous editor of product repos.
- Not a runtime, database, or dashboard.
- Not an authority on trading strategy — it manages engineering, not alpha.

---

## 2. Roles

| Role | Authority | Write scope |
|------|-----------|-------------|
| **Cray** | Sole approver. Only human who authorizes promotion. | Anywhere (human). |
| **MQAI orchestrator** | Job spec, context pack, routing, eval runs, promotion mechanics. | Orchestration + promotion (on approval). |
| **Codex** | Builder / mapper. | `jobs/active/<id>/output/` ONLY. |
| **Claude** | Reviewer. | `jobs/active/<id>/review/` ONLY. |
| **GPT** | High-risk synthesis only. | High-risk job synthesis files ONLY. |

---

## 3. The Flow (canonical 9 steps)

```
Cray objective
 → MQAI creates job spec (job.yaml)
 → MQAI assigns risk tier (path-matched, deterministic)
 → MQAI packs context
 → Codex builds / maps staged output
 → Claude reviews actual output
 → eval gates run
 → Cray manually reviews
 → approved output is promoted / merged
 → memory and lessons are updated
```

---

## 4. Consensus Model by Risk Tier

- **Low:** Codex executes → Claude reviews.
- **Medium:** Codex proposes / builds → Claude reviews the actual output (not just the plan).
- **High:** Codex plan + Claude plan (independent) → GPT synthesis → deterministic gates → Cray approval.

**High-risk areas:** metric formulas, DB schema, ChainIntel canonical registry, live execution logic, risk engine, secrets/auth, lookahead-sensitive research logic.

---

## 5. Hard Boundaries (non-negotiable)

See `company_brain/non_negotiables.md` and `company_brain/separation_of_concerns.md`.

- **Write-scope law:** agents NEVER write outside their assigned job subfolder.
- **Promotion law:** agents NEVER promote to `repo_control/`. Promotion is human-gated only.
- **Protected baseline:** `mqnode_test2` is read-only foundation in V0.
- **No cross-layer writes:** a job scoped to one layer must not write into another layer's owned paths.

---

## 6. Risk Tiering Rule

Risk tier is assigned by **file-path matching against `repo_control/<repo>/critical_files.md`** — NEVER by agent self-assessment. The `risk_tier_assignment` eval runs **first** and configures how strict the other gates are. Default is the stricter tier when a path is ambiguous or unmapped.

---

## 7. Job Lifecycle & Folders

```
jobs/active/<id>/     job.yaml, output/, review/
jobs/completed/<id>/  moved here on Cray approval + promotion
jobs/failed/<id>/     moved here on eval fail or rejection
jobs/TEMPLATE/        canonical job.yaml + folder shape for new jobs
```

Folder contract per job: `job.yaml` (spec), `output/` (Codex only), `review/` (Claude only).

---

## 8. Eval Gates (run order)

1. `risk_tier_assignment` — runs first, sets tier.
2. `write_scope_check` — blocks review + promotion on fail.
3. `secret_scan` — blocks on any hit.
4. `cross_layer_violation_check`
5. `formula_diff_check`
6. `migration_required_check`
7. `lookahead_safety_check`

Gates 5–7 are checklist-driven in V0; gates 1–3 are scripted (`evals/scripts/`).

---

## 9. Handoff Protocol (file-based only)

- Codex writes `output/` + `output/BUILD_NOTES.md` (what it did, assumptions, unverifiable items).
- Orchestrator runs evals → `review/eval_results.json`. Hard fail blocks Claude by default.
- Claude reads `output/` + `eval_results.json` + guards + `rules.md`, writes `review/claude_review.md` with:
  ```
  VERDICT: approve | request_changes | reject
  FINDINGS: [...]
  BOUNDARY_CHECK: pass | fail
  PROMOTE_RECOMMENDATION: yes | no
  ```
- Cray writes `review/cray_decision.md` (explicit signed line). No inferred approval.
- Promotion is a separate step; agents cannot perform it.

---

## 10. Memory Discipline

- `memory/decisions.md` — durable decisions and their rationale.
- `memory/lessons_learned.md` — what worked / what didn't, per job.
- `memory/failure_taxonomy.yaml` — structured failure categories, appended on every failure.

Update memory on every job completion or failure.

---

## 11. Layer Map (glossary)

- **MQNODE** — data truth (`mqnode_test2`, `mqnode_cloud`).
- **MQCHAIN** — entity / label truth (`mamakquantchainintel/mqchain-console`).
- **MQENGINE** — research validation (`mqengine`).
- **MQBOT** — execution (no repo yet).
- **MQDASH** — monitoring / control tower (no repo yet).
- **MQAI** — repo / operator control (this repo).
- **MQBRAIN** — future strategic alpha intelligence (does not exist yet).
