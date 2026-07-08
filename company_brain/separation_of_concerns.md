# Separation of Concerns

> STATUS: canonical. Basis for the `cross_layer_violation_check` eval.

## 1. Ownership table

| Layer | Owns | Must NOT touch | Repo(s) |
|-------|------|----------------|---------|
| MQNODE | Data truth: ingestion, storage, primitives, feeder contract | Entity labels, research logic, execution | `mqnode_test2`, `mqnode_cloud` |
| MQCHAIN | Entity / label truth, canonical registry | Data ingestion internals, research logic, execution | `mamakquantchainintel/mqchain-console` |
| MQENGINE | Research validation, lookahead-safe methodology | Data truth, label truth, execution | `mqengine` |
| MQBOT | Execution | Research decisions, data truth, labels | *(no repo yet)* |
| MQDASH | Monitoring / control tower | Any write to truth layers | *(no repo yet)* |
| MQAI | Operator / repo control, routing, review, promotion | Alpha/strategy; direct product-repo writes (V0) | this repo |
| MQBRAIN | *(future)* Strategic alpha intelligence | — | *(does not exist)* |

## 2. Directional rules

- Data truth flows up; labels reference data; research references data + labels; execution consumes
  research; monitoring observes all.
- **No layer writes into another layer's owned paths.**

## 3. Cross-layer violation examples

- A research (MQENGINE) job writing to node schema (MQNODE) → violation.
- A label (MQCHAIN) job editing feeder ingestion logic (MQNODE) → violation.
- Any job writing to `repo_control/` directly → violation (promotion is human-gated).
- Advanced analytics written into MQNODE primitive tables → violation (primitives store low-level
  reusable facts only).

## 4. Undefined layers

MQBOT / MQDASH: named, no repo, out of V0 scope. Placeholder only.

## 5. How this is enforced

- `cross_layer_violation_check` (path ownership).
- `write_scope_check` (job-folder confinement).
- `repo_control/<repo>/rules.md` (per-repo constraints).
