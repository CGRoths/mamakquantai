# MQAI-0005 — Rollback Plan

All changes are MQAI-repo files (new modules + docs + a new job). No product repos, no commits to
product repos, no push.

## To roll back
- The build is additive. To revert, remove the new files under `orchestrator/`, `commands/`,
  `templates/`, `skills/` (the 8 new charters), `evals/scripts/` (the 2 new scripts), `docs/`,
  `tests/`, and `jobs/active/MQAI-0005/` — or `git checkout -- <paths>` / `git clean` for untracked
  additions, once these are under version control.
- No pre-existing MQAI file was destructively overwritten (edits were additive; existing skills/eval
  scripts preserved). `README.md` and prior jobs untouched by this build.

## Not applicable
- No history rewrite, no disk deletion of user/secret files, no product-repo state to revert.
