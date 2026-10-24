# Architecture Decision Records (ADRs)

An ADR is a one-page note: **what I decided, what else I considered, and why.** Interviewers ask
"why X over Y?" These are the written answers.

Rules: one decision per file · never edit an accepted decision; write a new ADR that supersedes it ·
status is `Proposed`, `Accepted` or `Superseded by NNNN`.

| # | Decision | Status |
|---|---|---|
| [0001](0001-duckdb-parquet-over-pandas.md) | DuckDB SQL over Parquet, not pandas or a database server | Accepted |
| [0002](0002-datasets.md) | iPinYou + Criteo Attribution + Criteo Uplift, not synthetic or Avazu | Accepted |
| [0003](0003-static-dashboard-over-bi-tool.md) | Static HTML dashboard, not Tableau/Power BI/Streamlit | Accepted |
| [0004](0004-floor-sizing-assumptions.md) | Floor sizing: bids fixed, lost impressions unsold | Accepted |
| [0005](0005-honest-stand-ins.md) | Win rate and CPA as labelled stand-ins for fill rate and ROAS | Accepted |
| [0006](0006-numbers-json-single-source.md) | All numbers flow from one `numbers.json` | Accepted |

## Template
```markdown
# NNNN — Title
Status: Proposed | Accepted | Superseded by NNNN · Date: YYYY-MM-DD

## Context        — what problem forces a decision
## Options        — 2–4 real alternatives, one line each
## Decision       — what I picked
## Why            — the 2–3 reasons that actually decided it
## Consequences   — what gets easier, what gets harder, what to watch
```
