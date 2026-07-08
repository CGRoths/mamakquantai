# mqnode_test2 — Critical Files

> STATUS: provisional — conservative seed. Pending MQAI-0001 verification.
> Used by `risk_tier_assignment` to set risk tier via path matching (NOT agent self-assessment).

## Seeding policy (conservative)

Until repo cartography verifies exact paths, **treat the entire repo as HIGH risk.** This is the
protected baseline; the fail-safe default is stricter. Narrow this list only after MQAI-0001
produces a verified `map.md`.

## Critical path globs (provisional)

```
**            # ALL paths — HIGH until verified (protected baseline)
```

## Known high-risk categories (to be pinned to real paths after mapping)

- Schema / migrations
- Metric / formula definitions
- Ingestion checkpoints
- Feeder / exchange-API access
- Primitive table definitions (10m base)
- Secrets / auth / config

## Notes

- Ambiguous or unmapped paths → HIGH tier.
- This file is the single source for tiering `mqnode_test2`. Do not tier by agent opinion.
