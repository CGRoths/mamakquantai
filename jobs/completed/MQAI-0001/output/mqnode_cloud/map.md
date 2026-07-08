# mqnode_cloud — Repo Map

> Produced by MQAI-0001 (Repo Cartography, read-only). Staged output — NOT promoted.
> Source path mapped: `C:\MAMAKQUANT\mqnode_cloud`. Remote: `github.com/CGRoths/mqnode_cloud`.
> All paths below were directly observed. Uncertain items are marked UNVERIFIED.

## Repo purpose (as evidenced by code)
Lightweight single-purpose cloud feeder for the MQNODE layer. Fetches Binance 5-minute klines,
aggregates them into 10-minute buckets, and POSTs rows to the MQNODE node. Evidence: the sole module
`binance_cloud_price_feeder.py` and its functions.

## Layer ownership
MQNODE (data truth) — cloud feeder role. Consistent with `repo_control/mqnode_cloud/rules.md` and
`feeder_contract.md`.

## Top-level tree (observed)
```
mqnode_cloud/
├── binance_cloud_price_feeder.py   # the entire feeder (337 lines)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt                # requests>=2.31.0,<3
├── README.md
├── data/                           # empty (.gitkeep only)
└── .env.example
```

## Entry points (observed)
- `binance_cloud_price_feeder.py` — `main()` at module bottom; `run_loop()` and `run_once()` drive
  execution. Containerized via `Dockerfile` / `docker-compose.yml`.

## Key functions and responsibilities (observed, by signature)
- **Time helpers:** `utc_now`, `parse_utc_datetime`, `to_iso_z`, `to_bucket_start_10m`
  — 10m bucket alignment.
- **Config (env):** `getenv_str`, `getenv_float`, `getenv_int`, `configure_logging` — configuration
  read from environment (values NOT captured).
- **Checkpointing:** `load_checkpoint`, `save_checkpoint` — persist last processed 10m bucket.
- **Fetch (Binance):** `binance_klines_url`, `request_binance_5m_klines_once`,
  `fetch_binance_5m_klines` (with `MAX_FETCH_RETRIES=5`), `kline_open_time_utc`,
  `kline_close_time_utc`.
- **Aggregation:** `aggregate_5m_to_10m` — combines two 5m klines into one 10m bucket.
- **Delivery:** `post_rows_to_mqnode` — POSTs aggregated rows to the MQNODE ingest endpoint.
- **Orchestration:** `resolve_start_utc`, `run_once`, `run_loop`, `main`.
- **Constants:** `SOURCE_NAME="binance"`, `TEN_MINUTES`, `FIVE_MINUTES`, `BINANCE_LIMIT=1000`.

## Observed alignment with feeder invariants
- **10m primitive is canonical:** confirmed — `to_bucket_start_10m` + `aggregate_5m_to_10m` produce
  10m buckets from 5m source data.
- **Exchange-API access confined to ingestion:** confirmed — Binance REST calls live only in the
  fetch functions; delivery is via HTTP POST to MQNODE.
- **Checkpointing present:** `load_checkpoint`/`save_checkpoint` exist; "advance only after
  successful write" ordering is UNVERIFIED (not code-traced).

## External dependencies
`requests` (only). Runtime is a standalone Python script; Python version UNVERIFIED
(Dockerfile not deep-read).

## Detected languages
Python (1 file), YAML (compose), Dockerfile, Markdown.

## Notable config files
`requirements.txt`, `docker-compose.yml`, `Dockerfile`, `.env.example`.
No `.env` present in the working tree at map time (only `.env.example`).

## Open questions / UNVERIFIED
- Exact target MQNODE endpoint / payload schema in `post_rows_to_mqnode` (not deep-read).
- Whether checkpoint advances strictly after a confirmed successful POST.
- Dockerfile base image / Python version and compose service config.
- `.qodo/` agent/workflow files (present, not mapped — tooling, not product).
