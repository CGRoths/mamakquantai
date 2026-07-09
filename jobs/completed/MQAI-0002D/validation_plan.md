# MQAI-0002D — Validation Plan

Pass criteria (all must hold; any CRITICAL/HIGH finding → not pass):
- Check 1: recovery untracked in mqengine HEAD (count 0).
- Check 3/5: `.gitignore` present in mqengine + mqnode_cloud.
- Check 4: mqengine tracked generated artifacts = 0.
- Check 6: mqnode_test2 `.env` and mqchain-console `.env.local` ignored + untracked.
- Check 7: tracked-source secret pattern scan = 0 matches in all four repos.
- Secret-handling: no secret values captured; `secret_content_read: false`.

Verdict: `pass | request_changes | fail`. On `pass`, move MQAI-0002D → completed + memory update.
On `request_changes`/`fail`: do NOT remediate; leave active; report blockers.
