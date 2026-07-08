# mqengine — Repo Map

> Produced by MQAI-0001 (Repo Cartography, read-only). Staged output — NOT promoted.
> Source path mapped: `C:\MAMAKQUANT\mqengine_lib_full`. Remote: `github.com/CGRoths/mqengine`.
> All paths below were directly observed. Uncertain items are marked UNVERIFIED.
> NOTE: local folder is `mqengine_lib_full`; canonical repo name is `mqengine`.

## Repo purpose (as evidenced by code)
Installable Python library for the MQENGINE layer: a backtest runtime + sweep dashboard "inspired by
NVT workflow" (from `pyproject.toml` description). Provides research/backtest engine, validation
(walk-forward, splits), Monte Carlo, portfolio/risk analytics, metrics, and a Flask dashboard.

## Layer ownership
MQENGINE (research validation). Consistent with `repo_control/mqengine/research_protocol.md` and
`lookahead_rules.md`.

## Top-level tree (observed)
```
mqengine_lib_full/
├── pyproject.toml            # name=mqengine, version=0.3.0; deps flask/numpy/pandas
├── README.md
├── mqengine/                 # the library package
├── mqengine.egg-info/        # build metadata
├── examples/                 # nvt_sql_pattern_example.py, nvt_sweep_dashboard_example.py
├── tests/                    # 11 pytest modules
├── .agents/ .codex/ .qodo/ .vscode/   # tooling (not product)
└── PyPI-Recovery-Codes-*.txt # SECRET-RISK — contents NOT read (see BUILD_NOTES)
```

## Package modules (observed, `mqengine/*.py`)
- `engine.py` — backtest engine (core runtime).
- `research.py` — research workflow.
- `validation.py` — validation logic (signal validation per tests).
- `sweep.py` — parameter sweep.
- `montecarlo.py` — Monte Carlo simulation.
- `portfolio.py` — portfolio construction/analytics.
- `risk.py` — risk analytics. **HIGH-risk area (risk engine).**
- `metrics.py` — metric computations. **HIGH-risk area (formulas).**
- `transforms.py` — data transforms.
- `alignment.py` — series alignment (time alignment).
- `conditions.py` — signal conditions.
- `stability.py` — stability analysis.
- `vectorized.py` — vectorized signal/backtest paths.
- `oms_analytics.py` — order-management-system analytics.
- `io_sql.py` — SQL input/output (reads data; MQENGINE consumes truth, does not own it).
- `facade.py` — public facade / API surface.
- `dashboard.py` — Flask dashboard (template `mqengine/templates/basic.html`).
- `result.py`, `schemas.py`, `types.py` — result objects, schemas, type definitions.

## Entry points (observed)
- Library import surface via `mqengine/__init__.py` + `facade.py` (exact exports UNVERIFIED).
- Dashboard: `dashboard.py` (Flask).
- Examples: `examples/nvt_sql_pattern_example.py`, `examples/nvt_sweep_dashboard_example.py`.

## Lookahead-relevant surface (observed via tests)
- `tests/test_walkforward.py`, `tests/test_research_split.py`,
  `tests/test_research_protocol_splits.py`, `tests/test_validation_signal.py`,
  `tests/test_vectorized_signal_backtest.py`, `tests/test_alignment.py`,
  `tests/test_metric_keys.py`, `tests/test_metrics.py`, `tests/test_portfolio.py`,
  `tests/test_engine_backward_compat.py`, `tests/test_adrs_compat_metrics.py`.
  Presence of walk-forward / split tests indicates temporal-partitioning logic exists (point-in-time
  correctness NOT code-verified here).

## External dependencies (from pyproject.toml)
`flask>=3.0.0`, `numpy>=1.24.0`, `pandas>=2.0.0`. Python `>=3.11`.

## Detected languages
Python (~34 `.py`), HTML (1 template), TOML, Markdown.

## Notable config files
`pyproject.toml` (setuptools build; project metadata), `mqengine.egg-info/PKG-INFO`.

## Open questions / UNVERIFIED
- Public export list from `mqengine/__init__.py` / `facade.py`.
- Which metric/formula definitions live in `metrics.py` vs `nvt`-specific code (HIGH-risk; not
  deep-read to avoid formula exposure/assumptions).
- Point-in-time correctness of splits/walk-forward (tests exist; logic not traced).
- `io_sql.py` data source expectations (what truth it reads and from where).
