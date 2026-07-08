# System Layers

> STATUS: canonical.

## Layer map

| Layer | Owns | Repo(s) | State |
|-------|------|---------|-------|
| **MQNODE** | Data truth (ingestion, storage, feeder contract) | `mqnode_test2` (baseline), `mqnode_cloud` (feeder) | active |
| **MQCHAIN** | Entity / label truth, canonical registry | `mamakquantchainintel` (`mqchain-console`) | active |
| **MQENGINE** | Research validation, lookahead-safe methodology | `mqengine` | active |
| **MQBOT** | Execution | *(no repo yet)* | defined, out of V0 scope |
| **MQDASH** | Monitoring / control tower (read-only view) | *(no repo yet)* | defined, out of V0 scope |
| **MQAI** | Repo / operator control | this repo | active |
| **MQBRAIN** | Future strategic alpha intelligence | *(does not exist)* | future |

## Directional flow

```
Data truth (MQNODE)
   → referenced by labels (MQCHAIN)
      → validated by research (MQENGINE)
         → consumed by execution (MQBOT)
            → observed by monitoring (MQDASH)
```

MQAI sits beside all layers as the operator; MQBRAIN (future) sits above research/execution as
strategic intelligence.

## Undefined layers

MQBOT and MQDASH are named in the boundary model but have no repo yet. They are **out of V0 scope**
and appear here only for completeness. Do not create `repo_control/` entries for them in V0.
