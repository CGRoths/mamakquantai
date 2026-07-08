# mqengine — Critical Files

> STATUS: provisional — conservative seed pending MQAI-0001 verification.

Until MQAI-0001 completes repo cartography, treat all files in this repo scope as HIGH risk.

Reason:
This repo is MQENGINE — research validation. It contains metric/formula definitions and
lookahead-sensitive research logic, both of which are declared HIGH-risk areas. Formula drift or
lookahead leakage silently invalidates research and any downstream decision, and the failure is not
visible at runtime. Every path is treated as HIGH until cartography pins the exact critical paths.

```text
**
```

## Known high-risk categories (to be pinned to real paths after mapping)

- Metric / formula definitions
- Feature construction (point-in-time correctness)
- Label timing / target shifting
- Train/validation/test partitioning
- Derived-interval computation from the 10m primitive

## Notes

- Ambiguous or unmapped paths → HIGH tier.
- Single source for tiering `mqengine`. Do not tier by agent opinion.
