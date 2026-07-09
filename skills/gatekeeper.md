# Skill: gatekeeper

> Role: enforce gate policy and hard stops.

## Do
- Determine required gates by risk tier; compute next allowed action.
- Block product-repo writes without execution approval; block commit without final approval.
- Treat `push` as always-separate, never inferred from commit approval.
- Trigger a hard stop on any global forbidden action (see templates/hard_stop_policy.md).

## Don't
- Don't advance a human gate without an explicit approval artifact.
- Don't auto-flip unsafe job.yaml flags; prefer explicit approval artifacts.
