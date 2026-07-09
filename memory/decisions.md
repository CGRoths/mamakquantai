# Decisions

Durable decisions and their rationale. Append-only; newest at top.

---

## 2026-07-09 — MQAI-0002C committed (local) & closed; MQAI-0002D opened

- **MQAI-0002C security remediation committed locally and closed** to `jobs/completed/`.
  mqengine `62c4243` (untrack recovery file + 5 egg-info + 11 `.pyc`, add `.gitignore`, off `main`),
  mqnode_cloud `4b0e7ae` (add `.gitignore`, off `main`). Closeout re-guard **V9 PASS / V10 PASS**.
- **No push, no history rewrite, no secret inspection.** Local commits sit on
  `chore/mqai-0002c-sechygiene` branches; push/merge is a separate, explicitly-authorized decision.
- **Recovery file** remains on disk (untracked, ignored, rotated/inert); untracked in HEAD.
- **MQAI-0002D** (read-only security re-audit) opened to verify the remediation stuck.

---

## 2026-07-09 — MQAI-0005: handoff / resume protocol added

- **MQAI-0005 handoff/resume protocol added** (additive patch): `orchestrator/handoff.py` + CLI
  `handoff`/`resume` commands + templates + skill + docs + tests.
- **Agents can now resume from files instead of chat memory** — `output/handoff/{latest_handoff,
  <from>_to_<to>,resume_prompt}.md` + `handoff_state.json`; compact report + context pack surface
  handoff state; stop-reason classified (context_exhausted, quota_exhausted, tool_error,
  validation_failed, human_approval_required, hard_stop_triggered, unknown).
- **This is prompt/file-level continuity, NOT automatic agent execution.** Claude/Codex/OpenRouter
  are still not wired; a human (or a future adapter) hands the resume prompt to the agent.
- Core rule reaffirmed: MQAI owns memory/state/rules/gates/handoff; agents are temporary compute;
  Cray is final risk owner. Tests: 23 pass. No product writes, no push.

---

## 2026-07-09 — MQAI-0005: production control-plane MVP created

- **MQAI-0005 created to reduce manual Cray/GPT/Claude prompt relay.** Built a file-first, stdlib-only
  local orchestrator (`orchestrator/` + `commands/mqai.ps1`) with job-state detection, gate policy,
  context-pack + compact-report generation, agent-prompt generation, and a local eval runner.
- **V1 orchestration remains file-first and non-autonomous.** All state is visible in files; no DB,
  no dashboard, no network.
- **Claude/Codex/OpenRouter execution is NOT wired yet** — MQAI generates prompt files for manual/CLI
  use. This is stated honestly in `docs/known_limits.md`; do not claim autonomy.
- **Product-repo writes remain gated by explicit job permissions;** the control-plane runner never
  pushes, rewrites history, inspects secrets, or writes product repos.
- **Compact reporting and generic (non-hardcoded) state detection are now first-class MQAI features**,
  proven by LOW/MEDIUM/HIGH fixtures resolving to distinct states. `push` is always a separate gate,
  never inferred from commit approval.

---

## 2026-07-09 — MQAI-0002B approved (plan-only) & closed

- **MQAI-0002B (Security Remediation Plan) closed with `DECISION: approve_plan_only`.** Moved to
  `jobs/completed/`. The remediation plan, proposed file changes, and validation checklist are
  accepted **as a plan** — **execution is NOT authorized** under this job.
- **Full HIGH-tier consensus recorded:** scripted gates pass; Claude v1 request_changes (F1/F2/F3) →
  builder fixes → Claude v2 approve; GPT synthesis `approve_plan_only`, EXECUTION_ALLOWED_NOW: no;
  Cray decision plan-only.
- **Review caught a real defect:** the v1 validation check `grep -c recovery` was a case-sensitive
  false pass against the capital-"R" filename; fixed to case-insensitive/anchored matching. Also
  added explicit untracking of already-tracked `.pyc`/`__pycache__`/`egg-info` (gitignore alone does
  not untrack committed files), and narrowed broad secret globs.
- **Mandated next job:** **MQAI-0002C — Security Remediation Execution** (separate HIGH-tier). Must
  carry exact write paths, exact commands, validation checks (incl. the case-insensitive recovery
  check), rollback notes, eval gates, Claude review of the executed diff, GPT synthesis, and Cray
  approval before ANY product-repo change is committed. **Not scaffolded yet** (per Cray).
- PyPI recovery codes already rotated by Cray; history purge (RP7) remains optional/post-rotation.

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
