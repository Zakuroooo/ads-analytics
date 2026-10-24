# ARCHITECTURE — how the numbers flow

## 1. The pipeline

```mermaid
flowchart LR
    K[Kaggle mirrors] -->|download_data.py| R[raw files<br/>bz2 / zip]
    R -->|to_parquet.py<br/>streamed, then deleted| PQ[(data/*.parquet)]
    PQ -->|DuckDB| SQL[sql/01–06<br/>KPI, auction, sizing,<br/>segments, retention]
    PQ -->|DuckDB + scipy| AB[analysis/ab_readout.py]
    SQL --> EX[analysis/export_numbers.py]
    AB --> EX
    EX --> N[(outputs/numbers.json<br/>+ outputs/*.csv)]
    N --> XL[excel/build_xlsx.py<br/>→ .xlsx, Sheets-safe]
    N --> DB[dashboard/build.py<br/>→ index.html]
    N --> DOC[docs check:<br/>MEMO, README, STORY]
    N --> T[tests/check_numbers.py]
```

**One rule:** `outputs/numbers.json` is the only place numbers come from. Excel, dashboard, memo,
slides and resume bullets all read it. `run_all.py` runs every box above in order.

## 2. Tables (DuckDB views over Parquet)

```mermaid
erDiagram
    IPY_BIDS ||--o| IPY_IMPS : "BidID (won)"
    IPY_IMPS ||--o{ IPY_CLICKS : BidID
    IPY_IMPS ||--o{ IPY_CONVS : BidID
    IPY_BIDS { string bid_id PK; timestamp ts; int exchange; int floor_price; int bid_price; int advertiser_id; string slot_format }
    IPY_IMPS { string bid_id PK; int pay_price }
    CRITEO_ATTR { bigint ts; string uid; int campaign; int click; int conversion; double cost; double cpo }
    CRITEO_UPLIFT { int treatment; int exposure; int visit; int conversion; double f0_f11 }
```

## 3. Query layer

| File | Question | Output |
|---|---|---|
| `sql/01_kpi_daily.sql` | KPIs per day | `kpi_daily.csv` |
| `sql/02_kpi_advertiser.sql` | KPIs per advertiser, exchange, slot | `kpi_advertiser.csv` |
| `sql/03_auction_health.sql` | bid vs pay, floor binding rate, win rate | `auction_health.csv` |
| `sql/04_floor_sizing.sql` | revenue/volume at floor × {1.0…2.0} | `floor_sizing.csv` |
| `sql/05_segments.sql` | campaign spend tiers × CPA quadrant | `segments.csv` |
| `sql/06_retention.sql` | campaign weekly retention cohorts | `retention.csv` |
| `analysis/ab_readout.py` | lift, CI, p, SRM, MDE, CACE | `ab_readout.json` |

## 4. Floor-price sizing logic (detail in ADR 0004)

```mermaid
flowchart TD
    A[Won impression:<br/>floor f, bid b, paid p] --> B{New floor F' = f × k}
    B -->|b < F'| L[Lost: assume unsold<br/>revenue 0]
    B -->|b ≥ F'| W[Still won:<br/>new price = max p, F']
    L --> S[Sum over impressions<br/>→ revenue, volume at k]
    W --> S
    S --> C{k = 1.0 check:<br/>equals actual revenue?}
```

## 5. Runtime limits
DuckDB `memory_limit='3GB'`, `threads=4`; one heavy query at a time; Parquet with ZSTD compression.
Dashboard is static HTML + one JSON file; no server. Deployed on Vercel as static files.
