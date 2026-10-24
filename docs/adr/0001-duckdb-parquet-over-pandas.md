# 0001 — DuckDB SQL over Parquet, not pandas or a database server
Status: Accepted · Date: 2026-10-24

## Context
About 30M+ rows across three datasets (several GB as text) on a MacBook with 8 GB RAM. The JD asks for "strong SQL on large datasets".

## Options
1. pandas: load CSVs into memory.
2. Postgres / Supabase: load into a database server.
3. DuckDB querying Parquet files directly.

## Decision
DuckDB over Parquet (ZSTD), with `memory_limit='3GB'`.

## Why
- pandas needs the whole table in RAM; a 3 GB CSV becomes 6–10 GB in memory and the Mac swaps or crashes. DuckDB streams and spills to disk.
- It's plain SQL, the same skill the JD tests, with window functions and CTEs, and no server to run.
- Parquet is columnar and compressed: a query that needs 3 of 22 columns reads only those 3.

## Consequences
- Easier: one file per question, fast re-runs, runs on any laptop.
- Harder: DuckDB SQL has small dialect differences from Postgres/BigQuery/Snowflake (I note them in LEARN ch. 05).
- Watch: run one heavy query at a time.
