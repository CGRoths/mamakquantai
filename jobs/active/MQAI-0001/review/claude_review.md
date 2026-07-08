# MQAI-0001 — Claude Review

> Reviewer: Claude (independent review of builder output). Read-only over `output/`.
> Wrote ONLY this file. Did not edit output/, repo_control/, or product repos. Nothing promoted.
> Date: 2026-07-09.

---

## VERDICT: approve

## FINDINGS

### Scripted eval gates (from `review/eval_results.json`, verified present)
- `risk_tier_assignment`: **pass**, tier **HIGH** (all four repos matched `**` from the conservative
  `critical_files.md` seed).
- `write_scope_check`: **pass** (no offending paths).
- `secret_scan`: **pass** (no hits).

> Caveat: in V0 `write_scope_check` and `secret_scan` were run with the default empty write-set, so
> their "pass" is not by itself a strong guarantee. I therefore verified both independently below.

### Independent verification I performed
1. **Real paths (Q1):** Spot-checked 11 cited paths across all four repos — **11/11 exist**. No
   fabrication detected. Examples confirmed: `mqnode/api/main.py`, `mqnode/metrics/btc/network/nvt.py`,
   `mqengine/risk.py`, `mqengine/metrics.py`, `src/db/schema.ts`,
   `drizzle/0003_audit_trail_immutability.sql`, `src/lib/mqchain/services/registry-service.ts`.
2. **inventory ↔ map (Q2):** All four `inventory.json` are **valid JSON** and are consistent with
   their `map.md` (layers, entry points, deps, secret-risk files, unmapped notes align). See nit #A.
3. **UNVERIFIED discipline (Q3):** Strong. SQL bodies, formula internals, schema definitions,
   checkpoint-after-write ordering, and NextAuth config are all explicitly marked UNVERIFIED rather
   than guessed.
4. **Product repos read-only (Q4):** **Confirmed.** `git status` shows pre-existing uncommitted
   changes in `mqnode_test2` (docker-compose.yml), `mqnode_cloud` (README/feeder, line-ending only),
   and `mqengine` (committed `.pyc` files), but their mtimes are **2026-06-02 / 05-13 / 06-30** — all
   predate the cartography run (output written 2026-07-09 03:17). MQAI-0001 did **not** write to any
   product repo. See finding #B.
5. **Secrets avoided (Q5):** **Confirmed.** Independent regex scan over `output/` found **no secret
   values**. The three secret-risk files are referenced by name/existence only, with `<redacted>` and
   "contents NOT read". Builder proactively surfaced them — good catch (see #C).
6. **mqchain-console-only scope (Q6):** **Respected.** Builder performed a parent-dependency check
   (parent `mamakquantchain` has no shared source imported by the console) and mapped only
   `mqchain-console`. Parent not mapped.
7. **High-risk files / missing critical paths (Q7):** Builder correctly flagged HIGH-risk areas:
   mqnode `metrics/btc/*`, mqengine `metrics.py` + `risk.py`, mqchain canonical registry
   (`registry-*.ts`, `src/db/schema.ts`), auth route, and the audit-immutability / check-constraint
   migrations. No obviously missing critical path given read-only scope; the one gap that matters —
   the exact 10m-primitive storage schema and higher-interval derivation — is honestly left
   UNVERIFIED rather than asserted.
8. **Good enough to promote (Q8):** **Yes**, for V0 cartography. The maps are accurate, honestly
   scoped, and evidence-based. Non-blocking refinements listed below.

## Checklist gates executed
- **cross_layer_violation_check: PASS.** Each map asserts only its own layer's ownership
  (mqnode_*→MQNODE, mqengine→MQENGINE, mamakquantchainintel→MQCHAIN). No foreign-layer authorship;
  no writes to another layer's paths; no writes to `repo_control/`.
- **formula_diff_check: PASS (n/a).** Read-only mapping. No formula added/modified/removed. Builder
  deliberately did not deep-read formula bodies.
- **migration_required_check: PASS (n/a).** No schema change. SQL migration files were listed, not
  modified.
- **lookahead_safety_check: PASS (n/a).** No research logic authored. Builder noted the existence of
  walk-forward/split tests in `mqengine` without modifying or asserting their correctness.

## Non-blocking observations
- **#A — inventory.json schema deviation (minor):** `repo_mapper.md` specifies a flat `files[]` array;
  the builder instead used richer structures (`key_modules`, `package_modules`, `api_route_groups`,
  etc.). This is *more* useful, not less, and all required semantic fields are present. Recommend
  either updating `skills/repo_mapper.md` to bless the richer schema or normalizing on promotion.
- **#B — maps built against a dirty working tree:** Three product repos had pre-existing uncommitted
  changes at map time. It does not corrupt these maps (modified files were only recorded at
  existence/top-level, not content), but future cartography should record the git HEAD/commit and
  dirty state per repo for reproducibility.
- **#C — secret-risk files are a Cray action item (out of scope for this job):** Especially
  `mqengine/PyPI-Recovery-Codes-*.txt` (account recovery codes committed to the repo) — recommend
  removal from the repo and credential rotation. `mqnode_test2/.env` and `mqchain-console/.env.local`
  should be confirmed git-ignored.
- **#D — tier/consensus mismatch (process note):** The job ran `consensus_mode: low` but
  `risk_tier_assignment` returned **HIGH** because `critical_files.md` is seeded `**`. For a
  read-only mapping job this is harmless (no writes → HIGH-consensus machinery is moot), but it
  confirms the conservative seed makes *every* job HIGH. Narrowing `critical_files.md` using these
  now-verified maps is the natural follow-up.

## BOUNDARY_CHECK: pass
Read-only respected; all writes confined to `output/`; no `repo_control/` writes; no cross-layer
authorship; no refactor/schema/formula/merge; nothing promoted.

## SECRET_HANDLING_CHECK: pass
No secret values in `output/`. Secret-bearing files disclosed as findings by name/existence only,
with contents unread and redacted.

## PROMOTE_RECOMMENDATION: yes
Promote the four `map.md` files into `repo_control/<repo>/map.md` (retaining a provenance line noting
MQAI-0001 and the git state caveat #B). Promotion remains a Cray-gated action.

## REQUIRED_CORRECTIONS
None blocking. Recommended (non-blocking) before or at promotion:
1. Record per-repo git commit hash + dirty-state flag in each map (reproducibility) — #B.
2. Reconcile the `inventory.json` schema with `skills/repo_mapper.md` (bless or normalize) — #A.
3. Track the three secret-risk files as a separate Cray action; not part of this read-only job — #C.
4. After promotion, use the verified maps to narrow each `critical_files.md` from `**` to real
   critical paths, resolving the tier/consensus mismatch — #D.
