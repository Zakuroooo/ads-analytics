"""Run every numbered query in sql/ and save each result to outputs/<name>.csv.

Each sql/NN_name.sql file holds exactly one SELECT. sql/00_views.sql is run first to define the tables.
Usage: python analysis/run_sql.py [01 02 ...]   (no arguments = all)
"""
import sys
import time
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
SQL, OUT = ROOT / "sql", ROOT / "outputs"


def connect():
    con = duckdb.connect()
    con.execute("SET memory_limit='3GB'; SET threads=4;")
    con.execute(f"SET temp_directory='{ROOT / '.duckdb_tmp'}'")
    con.execute(f"SET file_search_path='{ROOT}'")   # so 'data/...' paths work from any folder
    con.execute((SQL / "00_views.sql").read_text())
    return con


def main(only):
    con = connect()
    OUT.mkdir(exist_ok=True)
    for path in sorted(SQL.glob("[0-9][0-9]_*.sql")):
        if path.name.startswith("00") or (only and path.name[:2] not in only):
            continue
        start = time.time()
        rel = con.sql(path.read_text())
        out = OUT / f"{path.stem[3:]}.csv"
        rel.write_csv(str(out))
        rows = con.execute(f"SELECT count(*) FROM read_csv('{out}')").fetchall()[0][0]
        print(f"{path.name:28s} -> {out.name:24s} {rows:>5} rows  {time.time() - start:5.1f}s", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
