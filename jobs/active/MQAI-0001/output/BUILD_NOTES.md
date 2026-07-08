# MQAI-0001 — BUILD_NOTES

> Builder: Claude Code (semi-manual builder mode, standing in for the Codex role).
> Job: Repo Cartography (read-only). Consensus: low. Date: 2026-07-09.
> Output staged in `jobs/active/MQAI-0001/output/` ONLY. Nothing promoted.

## What was done
Read-only cartography of four targets at the locked paths in `LOCAL_ENV.md`:

| Repo (canonical) | Local path | Layer | Scope |
|------------------|-----------|-------|-------|
| mqnode_test2 | `C:\MAMAKQUANT\mqnode_test2` | MQNODE | full |
| mqnode_cloud | `C:\MAMAKQUANT\mqnode_cloud` | MQNODE | full |
| mqengine | `C:\MAMAKQUANT\mqengine_lib_full` | MQENGINE | full |
| mamakquantchainintel | `C:\MAMAKQUANT\mamakquantchain\mqchain-console` | MQCHAIN | mqchain-console only |

For each: produced `output/<repo>/map.md` + `output/<repo>/inventory.json`. Output folder names use
the **canonical repo names** from `job.yaml` (so `mqengine`, not `mqengine_lib_full`).

## Method
- Directory walks and targeted reads (top-level trees, package layouts, dependency manifests,
  entry-point signatures). Excluded `.git/`, `__pycache__/`, caches, `node_modules/`, `.next/`.
- Cited only observed paths. Anything not confirmed is marked `UNVERIFIED` in the maps.
- No files in any product repo were created, edited, moved, or deleted. Read-only throughout.

## Scope decision — mqchain-console parent dependency (job blocker resolved)
Parent repo `C:\MAMAKQUANT\mamakquantchain` contains no shared source code that `mqchain-console`
imports (only `.git/`, `.agents/`, `.codex/`, `.gitignore`, `README.md`, and the project folder).
**Decision:** mapped `mqchain-console` only; parent NOT mapped. Consistent with `mqchain-console-only`.

## SECRET-RISK findings (contents NOT read, NOT captured)
The following credential/secret-bearing files exist in target repos. I recorded existence only and
did **not** open or transcribe their contents. Flagged for `secret_scan` and Cray attention:

1. `C:\MAMAKQUANT\mqnode_test2\.env` — real `.env` present in working tree (not just `.env.example`).
2. `C:\MAMAKQUANT\mqengine_lib_full\PyPI-Recovery-Codes-<redacted>.txt` — PyPI account recovery
   codes committed into the repo working tree. **Recommend Cray remove from repo and rotate.**
3. `C:\MAMAKQUANT\mamakquantchain\mqchain-console\.env.local` — local env with likely secrets.

> These are findings about the product repos, not MQAI output. `secret_scan` over `output/` should
> pass because no secret values were copied into any deliverable. Verify during eval.

## Assumptions / limitations
- SQL migration files were listed but NOT deep-read (schema/table definitions UNVERIFIED). This
  keeps the map honest and avoids asserting schema truth the cartography did not confirm.
- Metric/formula internals (mqnode `metrics/btc/*`, mqengine `metrics.py`/`risk.py`) were identified
  as HIGH-risk and located, but NOT deep-read — cartography does not need formula bodies, and reading
  them risks unverified assertions.
- Data-truth invariants (10m canonical, higher intervals derived, NULL-not-zero, checkpoint-after-
  write) were partially corroborated for `mqnode_cloud` (10m bucket aggregation confirmed) but NOT
  code-traced end-to-end in `mqnode_test2`. Left as open questions in that map.
- Per-file enumeration of every React component / test was summarized at the group level for
  `mqchain-console`; `inventory.json` `unmapped` notes this.

## Boundary / compliance self-check (for Claude review)
- **Write scope:** all writes under `jobs/active/MQAI-0001/output/`. No product-repo writes. No
  writes to `repo_control/`. No review files written.
- **Cross-layer:** each map asserts only the repo's own layer ownership; no foreign-layer claims.
- **No refactor / schema change / formula change / merge.** Read-only respected.
- **No promotion.** Maps remain staged; `repo_control/<repo>/map.md` untouched.

## Deliverables written
- `output/mqnode_test2/map.md`, `output/mqnode_test2/inventory.json`
- `output/mqnode_cloud/map.md`, `output/mqnode_cloud/inventory.json`
- `output/mqengine/map.md`, `output/mqengine/inventory.json`
- `output/mamakquantchainintel/map.md`, `output/mamakquantchainintel/inventory.json`
- `output/BUILD_NOTES.md` (this file)

## Recommended next steps (not executed)
1. Run eval gates (`run_codex_job.ps1 -JobId MQAI-0001 -EvalsOnly`).
2. Claude review → `review/claude_review.md`.
3. Cray decision → `review/cray_decision.md`.
4. On approval, promote maps into `repo_control/<repo>/map.md`.
5. Address the three secret-risk files above (out-of-band; not part of this read-only job).
