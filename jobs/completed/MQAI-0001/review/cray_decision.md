# MQAI-0001 — Cray Decision

DECISION: approve

Approved by: Cray (cray.waikit@gmail.com)
Date: 2026-07-09
Basis: Claude review VERDICT=approve, BOUNDARY_CHECK=pass, SECRET_HANDLING_CHECK=pass,
       PROMOTE_RECOMMENDATION=yes; scripted eval gates all pass.

Authorization:
- Promote the four `output/<repo>/map.md` files into `repo_control/<repo>/map.md`
  with per-repo git provenance (review recommendation #B).
- Move MQAI-0001 to jobs/completed/.
- Update memory (decisions, lessons_learned).

Follow-ups acknowledged (tracked separately, NOT part of this read-only job):
- #A reconcile inventory.json schema with repo_mapper.md.
- #C secret-risk files, esp. mqengine PyPI recovery codes — remove + rotate.
- #D narrow each critical_files.md from `**` to verified critical paths.
