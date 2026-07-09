# MQAI-0002C — Claude Scaffold Re-Review (v4): S1 / V10 secret-safe diff capture

> Reviewer: Claude. Read-only over the scaffold. Wrote ONLY this file. No remediation, no product
> repo touched, no scaffold file edited, no git rm, no commit/push, no secret file opened.
> Date: 2026-07-09. Follows scaffold reviews v1–v3 (v3 = approve_scaffold) + proposed-execution review
> (approve_for_gate_a) + Gate A approval. (This review avoids pasting raw secret-detection regexes so
> it will not self-trip the V10 leak scan of `review/`.)

---

## VERDICT: approve_s1_v10

The S1 secret-safe diff-capture correction is correctly and completely implemented. No residual leak
vector, contradiction, or stale full-chain reference in the spec files. Two minor, non-blocking
observations noted. Execution posture unchanged: Gate A branch-local only; commit/push still blocked.

## Checklist confirmations (all PASS)
1. **S1 secret-safe diff capture correctly implemented** — CONFIRMED. `execution_plan.md` Step 7 is
   restructured into 7a (metadata-only for all staged changes), 7b (`.gitignore` full diff only),
   7c (sanitized full diff excluding secret-like paths). `output/staged_diff.md` is assembled from
   7a+7b+7c only.
2. **Unrestricted `git diff --cached` forbidden** — CONFIRMED. `forbidden_actions` #1a; Step 7 header;
   Step 3 S1 warning; Step 7 checkbox "MUST NOT contain any unrestricted `git diff --cached`".
3. **Recovery-code removal evidence metadata-only** — CONFIRMED. Only `--name-status` / `--stat` /
   `--summary` for `PyPI-Recovery-Codes*.txt` (7a; V10; #1a). Verified these git modes emit paths /
   line-counts / mode changes only — never file content.
4. **Full-content diff only for new `.gitignore` or sanitized** — CONFIRMED. 7b limited to
   `-- .gitignore`; 7c uses `:(exclude)` pathspecs for recovery/`.env`/key/token/secret paths.
5. **V10 scans `output/` and `review/` after execution** — CONFIRMED. V10 leak scan runs over both
   trees (files-with-matches / counts only; does not print matches).
6. **V10 failure blocks Gate B + treated as `secret_leak` incident** — CONFIRMED. V10: "any hit →
   FAIL → secret-handling incident (do NOT commit; quarantine; append failure_taxonomy `secret_leak`)";
   pass criteria require V1–V10 before Gate B; `forbidden_actions` #1b enforced by V10.
7. **All full validation-chain references say V1–V10** — CONFIRMED in spec files: `job.yaml` (gate_B
   precondition + gating rule), `forbidden_actions` #6, `execution_plan` (intro/Step 7/Step 8),
   `validation_plan` pass criteria, `review_requirements` (artifact #6 + hard gate). No stray `V1–V9`
   remains in any spec file.
8. **Gate B requires V1–V10 + executed-diff review + GPT synthesis + Cray final approval** —
   CONFIRMED (`job.yaml` gate_B; `review_requirements` hard gate).
9. **Older Gate A approval's `V1–V9` is not expanded by S1; S1 only strengthens** — CONFIRMED.
   `cray_execution_approval.md` (signed) was correctly left unedited; `scaffold_fix_notes_v3.md`
   documents that V10 only ADDS a secret-safety validation (does not authorize anything new) and that
   Gate B now requires V1–V10, superseding the V1–V9 phrasing. Gate A scope is unchanged.
10. **`execution_authorized=true` still authorizes only Gate-A branch-local work** — CONFIRMED
    (`job.yaml` scope + gating; `forbidden_actions` #5/#6 keep commit/push behind Gate B).
11. **`commit_authorized=false` still blocks commit/push** — CONFIRMED.
12. **No secret-content inspection** — CONFIRMED (`forbidden_actions` #1/#1a/#1b; capture is
    metadata-only; `secret_content_inspection: false`).
13. **No history rewrite** — CONFIRMED (`forbidden_actions` #3; RP7 excluded).

## Leak-vector sweep (independent)
Reviewed every capture command in the plan for content exposure:
- Step 0 / Step 7 `git status --porcelain`, V9 `--name-only`, 7a `--name-status`/`--stat`/`--summary`
  → path + counts + mode only. **No content.**
- 7b restricted to `.gitignore`; 7c excludes secret-like paths. **No secret content.**
- No unrestricted `git diff --cached` anywhere; `staged_diff.md` constrained to 7a+7b+7c.
Conclusion: no residual leak vector in the documented commands.

## Minor observations (non-blocking)
- **N1 — V10 scan shape:** the leak-scan patterns target key/token shapes, not the PyPI recovery-code
  string shape specifically. That's acceptable because the PRIMARY control is prevention
  (metadata-only capture, never diffing the file); the scan is defense-in-depth plus a manual
  "confirm no recovery-code line material" step. Optionally add a recovery-code-shape check for
  completeness. Not required.
- **N2 — V10 self-match risk:** scanning `review/` could raise a benign false positive if a future
  artifact quotes a secret-detection pattern literally. This is fail-safe (a hit blocks Gate B and
  forces human triage, never auto-passes), so it is safe; consider excluding known
  pattern-definition artifacts or annotating expected-benign matches to reduce noise. Not required.

## Boundary / secret-handling (this review)
- BOUNDARY_CHECK: pass — read-only; only this file written.
- SECRET_HANDLING_CHECK: pass — no secret file opened; recovery filename referenced as metadata only;
  no raw secret-detection regexes reproduced here.

## EXECUTION_ALLOWED_NOW: gate_a_only
Gate A is granted (`execution_authorized=true`) → branch-local remediation + secret-safe capture +
V1–V10 validation are now permitted. Commit/push remain blocked (`commit_authorized=false`) until
Gate B (V1–V10 + executed-diff review + GPT synthesis + Cray final approval). The scaffold is ready
for the Gate-A execution run.
