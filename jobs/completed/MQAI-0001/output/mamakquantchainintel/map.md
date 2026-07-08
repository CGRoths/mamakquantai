# mamakquantchainintel / mqchain-console — Repo Map

> Produced by MQAI-0001 (Repo Cartography, read-only). Staged output — NOT promoted.
> Source path mapped: `C:\MAMAKQUANT\mamakquantchain\mqchain-console`.
> Remote (parent): `github.com/CGRoths/mamakquantchainintel`.
> SCOPE: `mqchain-console` ONLY. All paths below were directly observed. UNVERIFIED where noted.

## Parent-dependency check (scope decision)
Parent repo `C:\MAMAKQUANT\mamakquantchain` contains only `.agents/`, `.codex/`, `.git/`,
`.gitignore`, `README.md`, and the `mqchain-console/` project. **No shared source code in the parent**
that `mqchain-console` imports. Conclusion: mapping `mqchain-console` alone is sufficient; parent was
NOT mapped (consistent with job scope `mqchain-console-only`).

## Repo purpose (as evidenced by code)
Next.js 16 + React 19 + TypeScript web console for the MQCHAIN layer — the ChainIntel entity/label
control plane. Provides UI + API routes for a canonical registry, candidates, dictionaries,
discovery jobs, KV builds, metric groups, review/approval, audit log, and a resolver. Persists via
Drizzle ORM over PostgreSQL. Auth via NextAuth.

## Layer ownership
MQCHAIN (entity / label truth, canonical registry). Consistent with
`repo_control/mamakquantchainintel/label_governance.md` and `registry_truth_boundary.md`.

## Top-level tree (observed)
```
mqchain-console/
├── package.json              # next 16.2.10, react 19, drizzle-orm, next-auth, zod, postgres
├── drizzle.config.ts         # Drizzle config
├── drizzle/                  # SQL migrations + meta
├── next.config.ts, tsconfig.json, eslint.config.mjs, postcss.config.mjs, vitest.config.ts
├── components.json           # shadcn config
├── scripts/                  # seed.ts, compile-kv.ts
├── public/
├── src/
│   ├── app/                  # Next.js app router (pages + api)
│   ├── components/           # auth, mqchain, ui
│   ├── db/                   # client.ts, schema.ts  (Drizzle schema)
│   ├── lib/mqchain/          # domain logic (services, validators, data, kv, address)
│   ├── test/, types/
├── AGENTS.md, CLAUDE.md, README.md
└── .env.example, .env.local  # .env.local SECRET-RISK — contents NOT read
```

## App router surface (observed, `src/app/`)
- **UI pages:** `src/app/mqchain/` — audit-log, batches (+[id]), candidates (+[id]),
  dictionaries (categories, entities, key-prefixes, protocols, roles), discovery/jobs (+[id]),
  intake/new, kv-builds (+[id]), metric-groups, registry (+[id]), resolver, review/groups (+[id]),
  settings, source-jobs (+[id]); plus `src/app/login`.
- **API routes:** `src/app/api/mqchain/` — audit-log, batches (+[id]), candidates (+[id]),
  dictionaries (+versions), discovery/jobs (+[id]/complete), evidence, kv-builds (+[id], +active),
  metric-groups (+[code]/members), registry (+[id]), resolver, review/groups (+[id]), settings,
  source-jobs (+[id]); auth at `src/app/api/auth/[...nextauth]`.

## Domain logic (observed, `src/lib/mqchain/`)
- **services/** — approval, audit, batch, candidate, cex-flow, dashboard, dictionary, discovery,
  evidence, kv-manifest, metric-group, registry, resolver, review, settings, source-job,
  service-utils.
- **validators/** — approval, batch, candidate, dictionary, discovery, evidence, intake,
  kv-manifest, metric-group, registry, resolver-api, settings, source-job (zod-based, UNVERIFIED).
- **kv/** — `schema.ts`; plus `kv-compiler.ts`, `kv-manifest.ts`, `kv-serving-api.ts` at lib root.
- **address/** — `normalize.ts` (address normalization).
- **data/** — `seed-data.ts`.
- Registry surface: `registry-api.ts`, `registry-conflicts.ts`, `registry-detail.ts`,
  `registry-lifecycle.ts` — **canonical registry = HIGH-risk area.**
- Other: audit, trust, flags, discovery, evidence, intake-extraction, csv-upload, metric-rules,
  cex-flow, resolver, review, source-job/url, constants, runtime-env, types.

## Database / schema (observed)
- `src/db/schema.ts` (Drizzle schema), `src/db/client.ts` (postgres client).
- `drizzle/` migrations: `0000_low_maria_hill.sql`, `0001_kv_index_manifest_shards.sql`,
  `0002_freezing_nekra.sql`, `0003_audit_trail_immutability.sql`, `0004_source_verifications.sql`,
  `0005_control_plane_check_constraints.sql`, plus `0000_mqchain_console/` and `meta/`.
- Notable: migration names indicate audit-trail immutability and control-plane check constraints
  (registry-integrity mechanisms) — details UNVERIFIED (SQL not deep-read).

## Entry points (observed)
- Web app: `next dev` / `next build` / `next start` (from `package.json` scripts).
- DB: `db:generate`, `db:migrate` (drizzle-kit), `db:seed` (`scripts/seed.ts`).
- KV: `kv:compile` (`scripts/compile-kv.ts`).
- Tests: `vitest run`.

## External dependencies (from package.json)
next 16.2.10, react/react-dom 19, drizzle-orm, postgres, next-auth, bcryptjs, zod, papaparse,
radix-ui, shadcn, lucide-react, tailwind. Dev: drizzle-kit, vitest, typescript, eslint.

## Detected languages
TypeScript (~170 `.ts`), TSX (~72), SQL (drizzle migrations), plus CSS/config.

## Notable config files
`package.json`, `drizzle.config.ts`, `next.config.ts`, `tsconfig.json`, `eslint.config.mjs`,
`postcss.config.mjs`, `vitest.config.ts`, `components.json`, `.env.example`.
**`.env.local` present — contents NOT read (secret-risk).**

## Open questions / UNVERIFIED
- Exact Drizzle table definitions in `src/db/schema.ts` (not deep-read).
- Registry-integrity enforcement details (audit immutability, check constraints) in SQL.
- Entity ID minting / referential-integrity mechanism.
- NextAuth provider configuration (auth route not deep-read; secret-risk avoided).
- `.next/`, `node_modules/` excluded (build/deps, not product source).
