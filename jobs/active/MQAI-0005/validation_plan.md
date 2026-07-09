# MQAI-0005 — Validation Plan

## Automated
- `python -m unittest discover tests` — loader, state, gate policy, context pack, compact report,
  eval runner. Must pass with no network.
- Fixtures LOW/MEDIUM/HIGH resolve to **distinct** states + next gates (anti-hardcoding proof).

## CLI smoke (MQAI-0005)
- `status`, `next`, `context`, `report`, `prompts`, `eval`, `run --until-hard-stop`, `approve --gate plan`.
- Expect: context_pack.md, compact_report.md, prompts/*.md, eval_results.json produced; run stops at
  the next gate without product mutation.

## Safety assertions
- No product-repo working tree changed by this build (compare pre-existing status).
- `eval secret_scan` = pass (no secret-shape values in MQAI output).
- No push; no history rewrite; no writes outside C:/MAMAKQUANT/mamakquantai.

## Evidence
Captured in `output/build_report.md`, `output/test_results.md`, `output/cli_smoke_results.md`,
`output/known_limits.md`.
