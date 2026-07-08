# Eval Gate: secret_scan

> Type: deterministic (scripted in V0). Blocks: Claude review + promotion on any hit.
> Script: `evals/scripts/secret_scan.ps1`

## 1. Purpose
Ensure no secrets (keys, tokens, credentials, private keys, `.env` contents) appear in staged output.

## 2. Inputs
Everything under `jobs/active/<id>/output/`.

## 3. Method (V0)
Regex + entropy scan for:
- API keys / bearer tokens.
- AWS/GCP/exchange credential patterns.
- PEM / private key blocks (`-----BEGIN ... PRIVATE KEY-----`).
- `.env`-style `KEY=secret` assignments.
- High-entropy strings above threshold.

## 4. Output
```json
{ "gate": "secret_scan", "status": "pass|fail", "hits": [ { "file": "", "pattern": "" } ] }
```

## 5. Fail behavior
Any hit → FAIL → job halts. Never log the secret value itself; log location + pattern name only.

## 6. Notes
V0 = regex/entropy. V1 = gitleaks/trufflehog integration + pre-commit hook.
