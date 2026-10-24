"""Convert raw downloads to Parquet, check row counts, then delete the raw files.

Why: Parquet is compressed and columnar, so DuckDB reads only the columns a query needs (ADR 0001).
Usage: python scripts/to_parquet.py [uplift|attribution|ipinyou ...] [--keep-raw]
"""
import subprocess
import sys
import zipfile
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
RAW, DATA = ROOT / "raw", ROOT / "data"
KEEP_RAW = "--keep-raw" in sys.argv

con = duckdb.connect()
con.execute("SET memory_limit='3GB'; SET threads=4; SET preserve_insertion_order=false;")
con.execute(f"SET temp_directory='{ROOT / '.duckdb_tmp'}'")


def count_lines(path):
    # wc -l counts newline characters; a CSV with a header has rows = lines - 1
    return int(subprocess.run(["wc", "-l", str(path)], capture_output=True, text=True).stdout.split()[0])


def write_parquet(select_sql, out):
    out.parent.mkdir(parents=True, exist_ok=True)
    con.execute(f"COPY ({select_sql}) TO '{out}' (FORMAT parquet, COMPRESSION zstd)")
    return con.execute(f"SELECT count(*) FROM '{out}'").fetchone()[0]


def unzip_single(zip_path):
    with zipfile.ZipFile(zip_path) as z:
        name = z.namelist()[0]
        z.extract(name, zip_path.parent)
    return zip_path.parent / name


def check(label, raw_rows, parquet_rows):
    status = "OK" if raw_rows == parquet_rows else "MISMATCH"
    print(f"{label}: raw={raw_rows:,} parquet={parquet_rows:,} {status}", flush=True)
    if status != "OK":
        sys.exit(f"row count mismatch for {label}; raw files kept")


def uplift():
    src = unzip_single(RAW / "uplift" / "uplift-modeling.zip")
    rows = write_parquet(f"SELECT * FROM read_csv('{src}', header=true)", DATA / "uplift.parquet")
    check("uplift", count_lines(src) - 1, rows)
    if not KEEP_RAW:
        src.unlink()


def attribution():
    src = unzip_single(RAW / "attribution" / "criteo-attribution-modeling.zip")
    rows = write_parquet(f"SELECT * FROM read_csv('{src}', header=true, delim='\\t')", DATA / "attribution.parquet")
    check("attribution", count_lines(src) - 1, rows)
    if not KEEP_RAW:
        src.unlink()


# iPinYou season 2/3 log columns (tab-separated, no header). The bid log has 21 columns;
# impression/click/conversion logs add LogType, PayingPrice and KeyPageURL (24 columns).
BID_COLS = ["bid_id", "ts", "ipinyou_id", "user_agent", "ip", "region", "city", "exchange", "domain",
            "url", "anon_url_id", "slot_id", "slot_width", "slot_height", "slot_visibility", "slot_format",
            "floor_price", "creative_id", "bid_price", "advertiser_id", "user_tags"]
EVENT_COLS = ["bid_id", "ts", "log_type", "ipinyou_id", "user_agent", "ip", "region", "city", "exchange",
              "domain", "url", "anon_url_id", "slot_id", "slot_width", "slot_height", "slot_visibility",
              "slot_format", "floor_price", "creative_id", "bid_price", "pay_price", "key_page_url",
              "advertiser_id", "user_tags"]
# Only the columns the analysis needs are kept (user agent, IP, URLs and user tags are dropped).
KEEP = """bid_id, strptime(substr(ts, 1, 14), '%Y%m%d%H%M%S') AS ts,
          CAST(exchange AS INT) AS exchange, region, city, slot_id,
          CAST(slot_width AS INT) AS slot_width, CAST(slot_height AS INT) AS slot_height,
          slot_visibility, slot_format, CAST(floor_price AS INT) AS floor_price,
          creative_id, CAST(bid_price AS INT) AS bid_price, CAST(advertiser_id AS INT) AS advertiser_id"""


def ipinyou():
    src_dir = RAW / "ipinyou" / "ipinyou.contest.dataset" / "training3rd"
    for bz in sorted(src_dir.glob("*.txt.bz2")):
        kind, day = bz.name.split(".")[:2]
        out = DATA / "ipinyou" / kind / f"{day}.parquet"
        if out.exists():
            continue
        txt = bz.with_suffix("")  # strip .bz2
        with open(txt, "wb") as f:
            subprocess.run(["bzcat", str(bz)], stdout=f, check=True)
        cols = BID_COLS if kind == "bid" else EVENT_COLS
        extra = "" if kind == "bid" else ", CAST(pay_price AS INT) AS pay_price"
        col_spec = "{" + ", ".join(f"'{c}': 'VARCHAR'" for c in cols) + "}"
        select = f"""SELECT {KEEP}{extra} FROM read_csv('{txt}', delim='\\t', header=false,
                     quote='', escape='', nullstr='null', columns={col_spec})"""
        rows = write_parquet(select, out)
        check(f"ipinyou {kind} {day}", count_lines(txt), rows)
        txt.unlink()
        if not KEEP_RAW:
            bz.unlink()


if __name__ == "__main__":
    jobs = {"uplift": uplift, "attribution": attribution, "ipinyou": ipinyou}
    for name in [a for a in sys.argv[1:] if not a.startswith("--")] or jobs:
        jobs[name]()
