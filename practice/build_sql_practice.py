"""Build practice/sql_practice.md: SQL exercises on this project's own tables.

Every "expected output" is produced by actually running the answer query here, so the practice file
can never show a wrong result. Run: python practice/build_sql_practice.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis"))
from run_sql import connect  # noqa: E402

# (title, skill, question, hint, answer SQL)
EXERCISES = [
    ("Warm-up: count and filter", "SELECT, WHERE, COUNT",
     "How many impressions did the Footwear advertiser (id 2821) win?",
     "Filter `impressions` with WHERE, then count rows.",
     "SELECT count(*) AS impressions\nFROM impressions\nWHERE advertiser_id = 2821;"),

    ("Revenue per advertiser", "GROUP BY, SUM, ORDER BY",
     "Show each advertiser's revenue in CNY, biggest first. (pay_price is fen per 1,000 impressions, so one impression costs pay_price / 100000 CNY.)",
     "GROUP BY advertiser_id, SUM the price, divide once at the end.",
     "SELECT advertiser_id,\n       round(sum(pay_price) / 100000.0, 2) AS revenue_cny\nFROM impressions\nGROUP BY advertiser_id\nORDER BY revenue_cny DESC;"),

    ("CTR the right way", "ratio of totals",
     "What is the CTR of each ad exchange? Use total clicks / total impressions, not an average of anything.",
     "sum(clicks) / count(*) inside GROUP BY. Exchange is NULL for the mobile advertiser.",
     "SELECT exchange,\n       count(*)                          AS impressions,\n       sum(clicks)                       AS clicks,\n       round(sum(clicks) / count(*), 6)  AS ctr\nFROM impressions\nGROUP BY exchange\nORDER BY exchange NULLS LAST;"),

    ("Only the busy days", "HAVING",
     "Which days had more than 500,000 impressions?",
     "WHERE filters rows before grouping; HAVING filters groups after.",
     "SELECT ts::DATE AS day, count(*) AS impressions\nFROM impressions\nGROUP BY day\nHAVING count(*) > 500000\nORDER BY day;"),

    ("Price buckets", "CASE WHEN",
     "Split impressions into price buckets: under 30, 30 to 99, 100 and above (fen CPM). How many impressions and what share in each?",
     "CASE turns a number into a label; a window sum over all rows gives the share.",
     "SELECT CASE WHEN pay_price < 30  THEN '1 under 30'\n            WHEN pay_price < 100 THEN '2 30-99'\n            ELSE '3 100+' END              AS price_bucket,\n       count(*)                             AS impressions,\n       round(count(*) / sum(count(*)) OVER (), 3) AS share\nFROM impressions\nGROUP BY price_bucket\nORDER BY price_bucket;"),

    ("Add the category name", "JOIN",
     "Show revenue per advertiser with its category name (from the `advertisers` table).",
     "JOIN on advertiser_id, then GROUP BY both columns.",
     "SELECT a.category,\n       round(sum(i.pay_price) / 100000.0, 2) AS revenue_cny\nFROM impressions i\nJOIN advertisers a USING (advertiser_id)\nGROUP BY a.category\nORDER BY revenue_cny DESC;"),

    ("Win rate needs a LEFT JOIN", "LEFT JOIN, count(column)",
     "For each advertiser: how many bids, how many were won, and the win rate?",
     "LEFT JOIN keeps lost bids (their impression columns are NULL). count(i.bid_id) skips NULLs; count(*) does not.",
     "SELECT b.advertiser_id,\n       count(*)                          AS bids,\n       count(i.bid_id)                   AS won,\n       round(count(i.bid_id) / count(*), 3) AS win_rate\nFROM bids b\nLEFT JOIN impressions i USING (bid_id)\nGROUP BY b.advertiser_id\nORDER BY b.advertiser_id;"),

    ("Floor-binding rate with a CTE", "WITH (CTE)",
     "Among impressions that had a floor, what share paid exactly the floor or less? Write it as a CTE.",
     "Step 1 (CTE): keep only floor_price > 0 and flag each row. Step 2: average the flag.",
     "WITH floored AS (\n    SELECT (pay_price <= floor_price)::INT AS floor_binding\n    FROM impressions\n    WHERE floor_price > 0\n)\nSELECT count(*)                        AS floored_impressions,\n       round(avg(floor_binding), 4)    AS floor_binding_rate\nFROM floored;"),

    ("Top 3 campaigns", "ROW_NUMBER",
     "List the 3 Criteo campaigns with the highest spend inside each segment.",
     "ROW_NUMBER() OVER (PARTITION BY segment ORDER BY spend DESC), then keep rank <= 3. Read from outputs/campaign_segments.csv.",
     "WITH ranked AS (\n    SELECT segment, campaign, spend,\n           ROW_NUMBER() OVER (PARTITION BY segment ORDER BY spend DESC) AS rnk\n    FROM read_csv('outputs/campaign_segments.csv')\n)\nSELECT segment, rnk, campaign, round(spend, 2) AS spend\nFROM ranked\nWHERE rnk <= 3\nORDER BY segment, rnk;"),

    ("Day-over-day change", "LAG",
     "For each day, show revenue and the % change from the day before.",
     "LAG(revenue) OVER (ORDER BY day) gives yesterday's value on today's row. The first day has no yesterday, so it's NULL.",
     "WITH daily AS (\n    SELECT ts::DATE AS day, sum(pay_price) / 100000.0 AS revenue\n    FROM impressions\n    GROUP BY day\n)\nSELECT day,\n       round(revenue, 2)                                              AS revenue_cny,\n       round(revenue / LAG(revenue) OVER (ORDER BY day) - 1, 3)        AS change_vs_prev_day\nFROM daily\nORDER BY day;"),

    ("Running total", "SUM() OVER (ORDER BY ...)",
     "Show cumulative revenue by day (a running total).",
     "A window SUM with ORDER BY adds up every row up to and including the current one.",
     "WITH daily AS (\n    SELECT ts::DATE AS day, sum(pay_price) / 100000.0 AS revenue\n    FROM impressions\n    GROUP BY day\n)\nSELECT day,\n       round(revenue, 2)                               AS revenue_cny,\n       round(sum(revenue) OVER (ORDER BY day), 2)      AS cumulative_cny\nFROM daily\nORDER BY day;"),

    ("80/20 check", "window over ranked rows",
     "How many Criteo campaigns does it take to reach 50% of all spend?",
     "Sort by spend, running share, then find the first row where it reaches 0.5.",
     "WITH c AS (\n    SELECT spend,\n           sum(spend) OVER (ORDER BY spend DESC) / sum(spend) OVER () AS running_share\n    FROM read_csv('outputs/campaign_segments.csv')\n)\nSELECT count(*) + 1 AS campaigns_to_reach_half\nFROM c\nWHERE running_share < 0.5;"),

    ("Safe division", "NULLIF",
     "Cost per click for each advertiser, without crashing or returning infinity when clicks = 0.",
     "x / NULLIF(y, 0) returns NULL instead of dividing by zero.",
     "SELECT advertiser_id,\n       sum(clicks)                                                AS clicks,\n       round((sum(pay_price) / 100000.0) / NULLIF(sum(clicks), 0), 4) AS cpc_cny\nFROM impressions\nGROUP BY advertiser_id\nORDER BY advertiser_id;"),
]


def table(cur):
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in rows:
        out.append("| " + " | ".join("NULL" if v is None else str(v) for v in r) + " |")
    return "\n".join(out)


def main():
    con = connect()
    md = ["# SQL practice on my own tables",
          "*Generated by `practice/build_sql_practice.py`: every expected output below came from running the answer.*",
          "",
          "**How to use it:** read the question, write your own query first (DuckDB: `python -c \"...\"` or the duckdb CLI),",
          "then open the answer. Say out loud what each line does; that is what the interviewer wants to hear.",
          "",
          "Tables: `bids` (every bid), `impressions` (won auctions: pay_price, floor_price, clicks, conversion, advertiser_id, exchange, ts),",
          "`advertisers` (id → category), and `outputs/campaign_segments.csv` (675 Criteo campaigns with segment).",
          ""]
    for i, (title, skill, q, hint, sql) in enumerate(EXERCISES, start=1):
        cur = con.execute(sql)
        md += [f"## {i}. {title}  ·  *{skill}*", "", q, "", f"<details><summary>Hint</summary>\n\n{hint}\n</details>", "",
               "<details><summary>Answer + expected output</summary>", "", "```sql", sql, "```", "", table(cur), "", "</details>", ""]
    (ROOT / "practice" / "sql_practice.md").write_text("\n".join(md))
    print(f"wrote practice/sql_practice.md ({len(EXERCISES)} exercises)")


if __name__ == "__main__":
    main()
