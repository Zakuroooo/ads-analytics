# 06 · DuckDB and Parquet: why not Excel or pandas?
*10 minutes. Interviewers ask "why this tool?". Here is the answer.*

## The problem
About 30 million rows across three datasets, several GB as text. The laptop has 8 GB of RAM.
- **Excel** stops at 1,048,576 rows per sheet. Not even close.
- **pandas** (Python) loads the whole table into memory. A 3 GB CSV can need 6–10 GB of RAM: the laptop would freeze.

## What I used
**DuckDB**: a database that runs inside Python, no server. It reads files directly and only loads what a query needs.
**Parquet**: a file format that stores data **by column** and compresses it.

## Why "by column" matters (toy)
A table with 22 columns. My query needs only `pay_price` and `clicks`.
- CSV (row by row): you must read all 22 columns of every row to find those 2.
- Parquet (column by column): read only the 2 columns. Roughly a tenth of the work.

Hinglish: *CSV mein poori line padhni padti hai; Parquet mein sirf woh column uthao jo chahiye.*

## What actually happened in this project
| Step | Result |
|---|---|
| Downloaded raw files | ~1.9 GB compressed |
| Converted each file to Parquet, one at a time, streamed | `scripts/to_parquet.py` |
| Checked row counts | Parquet rows = raw lines for every file |
| Deleted raw files | `data/` ended at about 0.9 GB |
| Set limits | `SET memory_limit='3GB'; SET threads=4;` so the Mac stays usable |
| Queries | most run in 1–3 seconds over millions of rows |

## The honest trade-off
DuckDB's SQL is very close to Postgres/BigQuery, but not identical. Example: `ts::DATE` is a quick
type cast in DuckDB; in BigQuery you'd write `DATE(ts)`. The ideas (GROUP BY, joins, windows) are the same everywhere.

## If they ask "would this scale to Swiggy's data?"
"Not on a laptop. At company scale this SQL would run in a warehouse like BigQuery, Snowflake or Redshift.
The queries would barely change; the engine would." That's an honest, correct answer.

## Check yourself
1. Why not Excel? Why not pandas?
2. What makes Parquet faster for analytics queries?
3. How did you know nothing was lost when converting to Parquet?

<details><summary>Answers</summary>

1. Excel caps at about 1M rows. pandas loads everything into RAM, and 8 GB isn't enough.
2. It stores data by column and compresses it, so a query reads only the columns it needs.
3. I compared row counts: Parquet rows equalled raw line counts for every file, and the Criteo files matched the published counts.
</details>
