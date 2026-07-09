# MQAI-0005 — Production MVP Scope

## In scope (V1)
- Job loader (active/completed/failed) with stdlib YAML fallback.
- Generic, artifact-driven job state machine (not hardcoded to one job).
- Gate policy by risk tier; next-action + blocked-actions computation.
- Context pack + compact report generators (link-first).
- Role-specific agent prompt generation (Claude/Codex/GPT) — files only.
- Local eval runner (Python-native gates) → review/eval_results.json (honest skips).
- Path guard (write-scope + product-path detection).
- PowerShell CLI wrapper + Python entrypoint.
- Fixtures (LOW/MEDIUM/HIGH) + stdlib unittest smoke suite.
- Docs: manual, state machine, gate policy, CLI, routing, known limits.

## Out of scope (V1)
- Claude/Codex/OpenRouter API execution.
- DB, dashboard, network.
- Product-repo writes from the runner; push; history rewrite.
- Automated `close` (dry-run only).

## Success criteria
See `job.yaml success_criteria`. All must hold with no product writes, no secrets printed, no push.
