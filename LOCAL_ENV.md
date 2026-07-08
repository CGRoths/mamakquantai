# LOCAL_ENV

Local machine configuration for MQAI. **Cray must fill the TBD paths before running any job.**

## MQAI root

```
C:\MAMAKQUANT\mamakquantai
```

## Target repo local clone paths

> TBD — Cray to confirm. GitHub references are under `CGRoths/` (confirm vs `MAMAKQUANT`).

| Repo | Layer | GitHub | Local clone path |
|------|-------|--------|------------------|
| mqnode_test2 | MQNODE (data truth, protected baseline) | github.com/CGRoths/mqnode_test2 | C:\MAMAKQUANT\mqnode_test2 |
| mqnode_cloud | MQNODE (cloud feeder) | github.com/CGRoths/mqnode_cloud | C:\MAMAKQUANT\mqnode_cloud |
| mqengine | MQENGINE (research validation) | github.com/CGRoths/mqengine | C:\MAMAKQUANT\mqengine_lib_full |
| mamakquantchainintel | MQCHAIN (label truth) | github.com/CGRoths/mamakquantchainintel | C:\MAMAKQUANT\mamakquantchain|

### MQAI-0001 scope note

- `mamakquantchainintel` is scoped to **`mqchain-console` only** for MQAI-0001.
  Do not map the whole repo unless `mqchain-console` depends on parent files.

## Tooling prerequisites

- PowerShell (Windows) — primary orchestrator shell.
- Git — for read-only repo access.
- Codex CLI — `TBD` (invocation command / auth).
- Claude CLI — `TBD` (invocation command / auth).
- Secret scanner — V0 uses regex/entropy via `evals/scripts/secret_scan.ps1`
  (gitleaks/trufflehog optional, V1).

## Notes

- Product repos are opened **read-only** in V0.
- No secrets belong in this file. Store credentials outside the repo.
