# mqnode_test2 — Repo Map

> Produced by MQAI-0001 (Repo Cartography, read-only). Staged output — NOT promoted.
> Source path mapped: `C:\MAMAKQUANT\mqnode_test2`. Remote: `github.com/CGRoths/mqnode_test2`.
> All paths below were directly observed. Uncertain items are marked UNVERIFIED.

## Repo purpose (as evidenced by code)
Python data-truth node for the MQNODE layer. Ingests BTC chain data and multi-exchange price data
(REST + WebSocket), composes/normalizes prices, builds primitives, computes BTC metrics, and exposes
them via a FastAPI service. Background work runs on an RQ (Redis Queue) worker system with
checkpointing. Evidence: `mqnode/` package, `docker-compose.yml`, `requirements.txt`.

## Layer ownership
MQNODE (data truth). Consistent with `repo_control/mqnode_test2/rules.md`. Protected baseline.

## Top-level tree (observed)
```
mqnode_test2/
├── Dockerfile
├── docker-compose.yml, docker-compose.dev.yml
├── pyproject.toml            # pytest + ruff config
├── requirements.in / requirements.txt
├── README.md
├── nginx/conf.d/             # reverse proxy config
├── scripts/                  # repo-level scripts (contents UNVERIFIED beyond existence)
└── mqnode/                   # main package
    ├── api/  (main.py, schemas.py, routes/)
    ├── chains/btc/           # BTC chain ingestion
    ├── checkpoints/          # checkpoint_service.py
    ├── config/               # settings.py, logging_config.py
    ├── core/                 # app_context, errors, utils
    ├── db/  (connection, migrations, repositories, sql_versions/)
    ├── market/price/         # exchange price ingestion (REST + WS)
    ├── metrics/btc/          # fee / market / miner / network metrics
    ├── queue/                # jobs, producer, redis_conn
    ├── registry/             # metric registry + dynamic loader + dependency validator
    ├── scripts/              # backfill/compose/ingest/init/reconcile/seed
    ├── tests/                # ~40 pytest modules
    └── workers/              # RQ workers + run_worker.py
```

## Entry points (observed)
- **API:** `mqnode/api/main.py` — FastAPI app "MQNODE API" v0.1.0, mounts routers: health, registry,
  checkpoints, btc_metrics, internal_price_ingest.
- **Workers:** `mqnode/workers/run_worker.py` — RQ worker bootstrap with startup replay handlers for
  primitive/network/miner/market queues.
- **Scripts (CLI):** `mqnode/scripts/` — `init_db.py`, `seed_registry.py`, `backfill_btc.py`,
  `compose_prices.py`, `ingest_price_source.py`, `reconcile_btc.py`.
- **Containers:** `Dockerfile`, `docker-compose.yml` (service topology UNVERIFIED in detail).

## Key modules and responsibilities (observed)
- `mqnode/chains/btc/` — `listener.py`, `ingest.py`, `block_parser.py`, `primitive_builder.py`,
  `reorg.py`, `rpc.py`: BTC block ingestion, primitive construction, reorg handling.
- `mqnode/market/price/` — per-exchange REST + runtime + worker modules (binance, bybit, coinbase,
  kraken, okx, bitstamp) plus `sources/` adapters; `composer.py`, `normalize.py`,
  `remote_ingest.py`, `checkpoints.py`, `registry.py`.
- `mqnode/market/price/ws/` — WebSocket pipeline: `candle_builder.py`, `gap_detector.py`,
  `gap_filler.py`, `reconciler.py`, `remote_push.py`, `repository.py`, `runtime.py`, `state.py`, and
  `ws/sources/` per-exchange adapters.
- `mqnode/market/price/lifecycle/` — `manager.py`, `models.py`, `profiles.py`, `repository.py`,
  `runtime.py`: price-source lifecycle management.
- `mqnode/metrics/btc/` — `fee/fee_metrics.py`, `market/market_cap.py`, `miner/miner_revenue.py`,
  `network/nvt.py`: BTC metric formulas. **HIGH-risk (formulas).**
- `mqnode/registry/` — `metric_registry.py`, `dynamic_loader.py`, `dependency_validator.py`:
  metric registration + dependency resolution.
- `mqnode/db/` — `connection.py`, `repositories.py`, `migrations.py`, `sql_versions/` (6 SQL files).
- `mqnode/checkpoints/checkpoint_service.py` — checkpoint ok/error tracking (used by workers).
- `mqnode/queue/` — `jobs.py` (queue names: BTC_PRIMITIVE/NETWORK/MINER/MARKET), `producer.py`,
  `redis_conn.py`.

## Database / schema (observed)
`mqnode/db/sql_versions/`:
- `0001_price_ws_lifecycle_schema.sql`, `0001_runtime_readiness.sql`,
  `0002_btc_price_lane_expansion.sql`, `0003_price_source_hotplug_registry.sql`,
  `0004_price_ws_quality_lane.sql`, `0005_price_source_lifecycle.sql`.
Migrations orchestrated via `mqnode/db/migrations.py` (mechanism UNVERIFIED beyond filename).

## External dependencies (from requirements.txt)
FastAPI, uvicorn, starlette, pydantic + pydantic-settings, httpx, requests, psycopg2-binary
(PostgreSQL), redis + rq (queue), croniter, python-dotenv, pytest. Runtime Python 3.11.

## Detected languages
Python (primary, ~173 `.py`), SQL (7 files), YAML (compose), Dockerfile, nginx conf, Markdown.

## Notable config files
`pyproject.toml` (pytest/ruff), `requirements.in/.txt`, `docker-compose.yml(.dev)`, `Dockerfile`,
`nginx/conf.d/`, `.env.example`. **`.env` present — contents NOT read (secret-risk).**

## Open questions / UNVERIFIED
- Exact DB table definitions and the 10m-primitive storage schema (SQL contents not deep-read).
- How higher intervals are derived from 10m (invariant in rules.md) — not code-traced.
- NULL-vs-zero handling for missing prices — not code-traced.
- Checkpoint-after-write ordering guarantee — not code-traced.
- `docker-compose.yml` service topology and `scripts/` (repo-root) contents.
- `mqnode/chains`, `metrics`, `market` have no local `__pycache__` excluded content beyond `.py`.
