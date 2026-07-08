# Skill: repo_mapper

> Used by: Codex (builder) for cartography jobs. Read-only.

## Objective
Produce an accurate, verifiable map of a target repo WITHOUT modifying it.

## Hard constraints
- Read-only. Write ONLY to `jobs/active/<id>/output/<repo>/`.
- No refactor suggestions applied. No secrets captured (redact any encountered).
- Do not assert cross-layer ownership. Describe only what the repo actually contains.

## Deliverables (per repo)
- `map.md` — human-readable map.
- `inventory.json` — machine-readable inventory.

## map.md structure
- Repo purpose (as evidenced by code, not assumed).
- Layer ownership.
- Top-level tree.
- Entry points.
- Key modules and responsibilities.
- External dependencies.
- Detected languages.
- Notable config files.
- **Open questions / unverified** — anything not confidently determined.

## inventory.json schema
```json
{
  "repo": "string",
  "scope": "string (e.g. mqchain-console only)",
  "layer": "MQNODE | MQCHAIN | MQENGINE",
  "files": ["path", "..."],
  "entry_points": ["path", "..."],
  "languages": ["string", "..."],
  "deps": ["string", "..."],
  "config_files": ["path", "..."],
  "unmapped": ["path or note", "..."]
}
```

## Method
Walk the tree, classify, record. Do not infer beyond evidence. Flag every uncertainty in
"open questions" / `unmapped`.

## Quality bar (what Claude will check)
Completeness, no fabrication, no secrets, scope compliance, provenance of every claim.
