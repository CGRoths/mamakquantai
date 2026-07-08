# MQAI-0002B — Validation Checklist

> For use by the FUTURE execution job (after Cray authorizes execution). This job (MQAI-0002B)
> produces the checklist; it does NOT run it against a remediated tree. All checks are read-only
> verifications; none open secret files.

## Pre-execution gate
- [ ] Cray has authorized a separate HIGH-tier **execution** job (this plan approval is not enough).
- [ ] Confirmed: PyPI recovery codes already rotated (done 2026-07-09).
- [ ] Working on a branch, not a protected mainline, in each product repo.

## RP1 — recovery file untracked (`mqengine`)
- [ ] `git ls-files | grep -c recovery` → **0** (no longer tracked).
- [ ] Local file, if still present, is inert (codes rotated) — relocate/remove out-of-band.
- [ ] `git check-ignore "<recovery filename>"` → ignored (matched by `*recovery*`).

## RP2 — `.gitignore` added (`mqengine`)
- [ ] `.gitignore` exists at repo root.
- [ ] `git check-ignore .env` → ignored; `git check-ignore .env.example` → NOT ignored (still tracked).
- [ ] `git ls-files '*.pyc' | wc -l` → 0 after `git rm --cached` cleanup (bytecode untracked).

## RP3 — `.gitignore` added (`mqnode_cloud`)
- [ ] `.gitignore` exists at repo root.
- [ ] `git check-ignore .env` → ignored.
- [ ] `data/.gitkeep` still tracked; other `data/*` ignored.

## RP4 — `mqnode_test2/.env` (confirm, no change)
- [ ] `git ls-files .env` → empty.
- [ ] `git check-ignore .env` → ignored.
- [ ] `git log --all --oneline -- .env` → 0 commits.

## RP5 — `mqchain-console/.env.local` (confirm, no change)
- [ ] `git ls-files .env.local` → empty.
- [ ] `git check-ignore .env.local` → ignored.
- [ ] `git log --all --oneline -- .env.local` → 0 commits.

## RP6 — full re-audit (rerun MQAI-0002 checks)
- [ ] Tracked secret-risk filename scan → clean in all four repos.
- [ ] Counts-only secret-pattern scan of tracked source → 0 matches (unchanged).
- [ ] `.gitignore` now present in mqengine + mqnode_cloud.
- [ ] Produce `reaudit.md` summarizing before/after; `secret_content_read: false` maintained.

## RP7 — optional history purge (only if separately authorized)
- [ ] NOT run unless Cray explicitly authorizes in the execution job.
- [ ] If run: verify `git log --all -- "<recovery filename>"` → 0 across all refs; force-push done;
      collaborators notified to re-clone.

## MQAI eval gates (execution job)
- [ ] `risk_tier_assignment` → HIGH (expected).
- [ ] `write_scope_check` → writes confined to authorized product-repo branch(es) + job output.
- [ ] `secret_scan` → no secret values in MQAI output.
- [ ] `cross_layer_violation_check` → changes are hygiene-only, no cross-layer authorship.

## Sign-off
- [ ] Claude review of the executed changes = approve.
- [ ] Cray decision recorded for the execution job.
