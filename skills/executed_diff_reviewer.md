# Skill: executed_diff_reviewer

> Role: Claude — review the ACTUAL staged diff before commit.

## Do
- Verify staged paths ⊆ allowed_writes; confirm-only repos unchanged (status_after == status_before).
- Confirm no commit/push occurred yet (HEAD == base tip); confirm base branch is the intended one.
- Rely on metadata-only evidence for secret-like removals; verify captures are sanitized (V10).
- Emit: VERDICT · DIFF_MATCHES_APPROVED_PLAN (yes/no) · BOUNDARY_CHECK · SECRET_HANDLING_CHECK.

## Don't
- Never run unrestricted `git diff --cached`; never open secret files.
- Never approve push; push is a separate explicit gate.
