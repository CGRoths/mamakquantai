# MQAI-0005 — Problem Statement

The current MQAI workflow relays prompts manually: Cray → GPT (writes prompt) → Claude (executes/
reports) → back to GPT → Claude → ... This burns tokens/context and is slow and error-prone.

MQAI is file-first and governance-strong (jobs, gates, reviews, approvals) but has **no local runner**
to detect job state, compute the next allowed action, pack context compactly, run local eval gates,
and generate reusable agent prompts. Every step is hand-driven.

**Problem:** compress the manual relay into a small, auditable, local control-plane CLI —
`mqai status/next/context/report/prompts/eval/run/approve` — without pretending to be autonomous and
without weakening safety (no push, no product-repo writes from the runner, no secret exposure).
