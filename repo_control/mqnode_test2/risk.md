# mqnode_test2 — Risk

> STATUS: provisional — pending MQAI-0001 verification.

## Overall posture

**HIGH.** This is the protected baseline / current foundation and owns data truth. Default to the
strictest handling until cartography verifies exact critical paths (`critical_files.md`).

## Why high

- Data truth: corruption here propagates to labels, research, and execution.
- 10m primitive is the canonical base; damage to primitives is systemic.
- Missing-data and checkpoint invariants must not be violated (see `rules.md`).

## Tiering in V0

- Any job targeting this repo defaults to HIGH tier via `critical_files.md` (`**`).
- MQAI-0001 is read-only and therefore does not modify anything here, but still runs under the
  read-only constraint set.

## Escalation

Any proposed future write to this repo → HIGH consensus mode (Codex plan + Claude plan + GPT
synthesis + deterministic gates + Cray approval).
