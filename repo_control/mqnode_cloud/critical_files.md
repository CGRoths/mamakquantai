# mqnode_cloud — Critical Files

> STATUS: provisional — conservative seed pending MQAI-0001 verification.

Until MQAI-0001 completes repo cartography, treat all files in this repo scope as HIGH risk.

Reason:
This repo is the MQNODE cloud feeder — the entry point for data truth. It holds exchange-API access
(secrets/auth surface) and enforces the feeder contract consumed by the protected baseline
(`mqnode_test2`). A defect here corrupts primitives at the source and propagates system-wide, so
every path is treated as HIGH until cartography pins the exact critical paths.

```text
**
```

## Known high-risk categories (to be pinned to real paths after mapping)

- Exchange-API access / ingestion path
- Feeder contract (delivery shape/semantics — see `feeder_contract.md`)
- Checkpoint advancement logic
- 10m primitive production/relay
- Secrets / auth / config

## Notes

- Ambiguous or unmapped paths → HIGH tier.
- Single source for tiering `mqnode_cloud`. Do not tier by agent opinion.
