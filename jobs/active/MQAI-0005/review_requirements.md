# MQAI-0005 — Review Requirements

Since this job is MQAI-local (no product writes), the review is lighter than a product-execution job.

## Required review artifacts
1. `review/builder_self_review.md` — what was built, what works, what doesn't, tests, CLI smoke,
   changed files, risks, known limits, product-touched (no), push (no). Verdict:
   `built_mvp_ready_for_review | partial_build_request_review | blocked`.
2. (Optional, recommended) Claude independent review of the orchestrator modules + docs.
3. Cray review before promoting any of this into standing MQAI convention / closing the job.

## Gate expectations (HIGH tier, MQAI-local)
- `plan`: this planning set + Cray plan acknowledgement.
- `validation`: `output/test_results.md` + `output/cli_smoke_results.md` present and green.
- `executed_diff_review`: builder self-review (+ optional Claude review) over the changed files.
- `synthesis`: optional for an MQAI-local job (no product mutation); may be marked N/A by Cray.
- `final_commit`: Cray decision to commit the MVP into the MQAI repo (MQAI repo commit is allowed;
  product repos remain untouched). **push remains separately authorized.**
