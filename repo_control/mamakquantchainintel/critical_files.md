# mamakquantchainintel — Critical Files

> STATUS: provisional — conservative seed pending MQAI-0001 verification.

Until MQAI-0001 completes repo cartography, treat all files in this repo scope as HIGH risk.

Reason:
This repo is MQCHAIN — entity/label truth, including the ChainIntel canonical registry (a declared
HIGH-risk area). The registry is the single source of entity/label truth consumed by every other
layer; corrupted labels, unstable entity IDs, or a shadow registry break referential integrity
system-wide. V0 scope is `mqchain-console` only, but every path in scope is treated as HIGH until
cartography pins the exact critical paths.

```text
**
```

## Known high-risk categories (to be pinned to real paths after mapping)

- Canonical registry storage / schema
- Entity ID minting and references (ID stability)
- Label assignment / relabeling logic
- Label provenance / audit records
- Registry migrations

## Notes

- Ambiguous or unmapped paths → HIGH tier.
- Scope: `mqchain-console` only in V0.
- Single source for tiering `mamakquantchainintel`. Do not tier by agent opinion.
