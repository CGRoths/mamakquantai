# Handoff — MQAI-0005  (codex -> claude)

- generated: 2026-07-09T15:00:33
- job_id: MQAI-0005
- objective: Build the first production-usable local MQAI orchestrator that reduces manual Cray/GPT/Claude relay by adding job state detection, gate policy, context pack generation, compact reporting, eval runner wrappers, reusable agent prompt generation, and a PowerShell CLI wrapper.

- current_state: execution_authorized  ·  risk_tier: HIGH
- from_agent: codex
- to_agent: claude  (recommended_next_agent)
- stop_reason: context_exhausted

## Progress
- last completed (inferred): reached state `execution_authorized` (evidence: execution approval / execution_authorized flag, plan/scaffold approval, review artifact present, job.yaml present)
- next intended action: NEXT: run validation and write output/validation_results.md.
- gates passed: plan, execution
- gates pending: validation(pending), executed_diff_review(pending), synthesis(pending), final_commit(pending), closeout(pending)

## Repo / change state
- product repos touched: no (product writes not authorized by this job)
- target_repos: (none — MQAI-local job)
- MQAI files changed: see `git status` in the MQAI repo (this job's writes are under `jobs/active/MQAI-0005/` + declared allowed_writes).
- product files changed: none by MQAI control plane (product mutation only in an authorized product execution job).
- current branches / staged files: not captured by V1 handoff for MQAI-local jobs; for product execution jobs see that job's `output/` git-status captures.

## Validation status
- eval_results.json: present
- validation_results.md: absent

## Blockers
- commit of product-repo changes (no final approval)
- push (never inferred; requires explicit push authorization)
- any product-repo mutation (job does not allow product writes)

## Hard stops (do NOT do these)
- push
- history rewrite
- secret-content inspection
- unrestricted `git diff --cached`
- product-repo writes unless the job authorizes it
- `git add -A` in product repos

## Allowed writes
- `orchestrator/**`
- `commands/**`
- `templates/**`
- `skills/**`
- `evals/scripts/**`
- `docs/**`
- `tests/**`
- `jobs/active/MQAI-0005/**`
- `memory/decisions.md`
- `memory/lessons_learned.md`
## Forbidden writes
- `C:/MAMAKQUANT/mqnode_test2/**`
- `C:/MAMAKQUANT/mqnode_cloud/**`
- `C:/MAMAKQUANT/mqengine_lib_full/**`
- `C:/MAMAKQUANT/mamakquantchain/**`

## Files the next agent SHOULD read
- `jobs/active/MQAI-0005/job.yaml`
- `jobs/active/MQAI-0005/output/context_pack.md`
- `jobs/active/MQAI-0005/output/compact_report.md`
- `jobs/active/MQAI-0005/output/handoff/latest_handoff.md`
- `jobs/active/MQAI-0005/output/handoff/resume_prompt.md`

## Files the next agent MUST NOT touch
- any product repo path (see forbidden_writes)
- `repo_control/` canonical truth (promotion is human-gated)
- prior job history under `jobs/completed/`, `jobs/failed/`

## Compact continuation prompt
> Continue MQAI-0005 as `claude`. Read the files listed above (do NOT rely on chat history). Current state `execution_authorized`. Next action: NEXT: run validation and write output/validation_results.md. Respect hard stops. Report compactly: status · next action · gates · changed files · product repos touched · blockers · required human decision.
