# 05 · SQL from zero (with our own tables)
*25 minutes. Then do `practice/sql_practice.md`, where every answer shows its real output.*

SQL is how you ask a database a question. You describe **what** you want; the database figures out **how**.

## Our tables (think of them as Excel sheets)
| Table | One row = | Key columns |
|---|---|---|
| `bids` | one auction iPinYou bid on | bid_id, ts (time), advertiser_id, floor_price, bid_price, exchange |
| `impressions` | one auction it won | bid_id, pay_price, floor_price, clicks, conversion, advertiser_id |
| `advertisers` | one advertiser | advertiser_id, category |
| `campaigns` | one Criteo campaign | campaign, spend, clicks, conversions, spend_w1, spend_w4 |

## 1. SELECT and WHERE: pick columns, filter rows
```sql
SELECT bid_id, pay_price
FROM impressions
WHERE advertiser_id = 2821;
```
"Give me the auction ID and price for every impression of advertiser 2821."
**Toy:** 3 rows in, only rows with advertiser 2821 come out.

## 2. Aggregate: count, sum, avg
```sql
SELECT count(*) AS impressions, sum(clicks) AS clicks
FROM impressions;
```
Many rows become **one** row of totals.

## 3. GROUP BY: totals per group
```sql
SELECT advertiser_id, count(*) AS impressions
FROM impressions
GROUP BY advertiser_id;
```
**Toy:**

| advertiser_id (input rows) |
|---|
| 2821 |
| 2821 |
| 2259 |

→ output: 2821 → 2, 2259 → 1.

Hinglish: *GROUP BY = rows ko dabbon mein daalo, phir har dabbe ka total nikalo.*

## 4. HAVING: filter groups (WHERE filters rows)
```sql
SELECT ts::DATE AS day, count(*) AS impressions
FROM impressions
GROUP BY day
HAVING count(*) > 500000;
```
WHERE runs **before** grouping, HAVING runs **after**. You can't use count(*) in WHERE.

## 5. CASE: turn values into labels
```sql
SELECT CASE WHEN pay_price < 30 THEN 'cheap' ELSE 'normal' END AS bucket, count(*)
FROM impressions
GROUP BY bucket;
```
Like Excel's IF. Used in `sql/05_campaign_segments.sql` to label PROTECT / FIX / GROW / WATCH.

## 6. JOIN: combine two tables on a matching column
```sql
SELECT a.category, sum(i.pay_price) / 100000.0 AS revenue_cny
FROM impressions i
JOIN advertisers a USING (advertiser_id)
GROUP BY a.category;
```
`JOIN` keeps rows that match on both sides. **LEFT JOIN** keeps *every* row from the left table, even with no match
(the right side becomes NULL). That's how win rate works:

```sql
SELECT count(*) AS bids, count(i.bid_id) AS won
FROM bids b
LEFT JOIN impressions i USING (bid_id);
```
**Toy:** 3 bids, 2 won → count(*) = 3, count(i.bid_id) = 2 (NULLs are not counted). Win rate = 2/3.

**Join trap:** if the right table has duplicate keys, a join multiplies rows. That's why I removed duplicate
bid_ids first, and why the checks compare totals before and after.

## 7. CTE (WITH): name a step, then use it
```sql
WITH floored AS (
    SELECT (pay_price <= floor_price)::INT AS floor_binding
    FROM impressions
    WHERE floor_price > 0
)
SELECT avg(floor_binding) FROM floored;
```
A CTE is a temporary named table. It makes long queries readable, step by step. All my SQL files use them.

## 8. Window functions: a calculation across rows, without collapsing them
GROUP BY squashes rows into one per group. A **window** keeps every row and adds a column computed over neighbours.

```sql
-- each advertiser's share of total spend: sum over ALL rows, shown on each row
spend / sum(spend) OVER () AS spend_share

-- rank campaigns by spend inside each segment
ROW_NUMBER() OVER (PARTITION BY segment ORDER BY spend DESC) AS rnk

-- yesterday's revenue on today's row
LAG(revenue) OVER (ORDER BY day) AS prev_day

-- running total
sum(revenue) OVER (ORDER BY day) AS cumulative
```
**Toy running total:** revenue 10, 20, 5 → cumulative 10, 30, 35.

Hinglish: *Window function row ko gayab nahi karta; bas har row ke saath ek extra calculation jodh deta hai.*

## 9. GROUPING SETS and ROLLUP: several totals at once
`GROUP BY GROUPING SETS ((exchange, slot_visibility), (exchange), ())` gives detail rows, a subtotal per exchange,
and a grand total in one query (`sql/03_auction_health.sql`). `ROLLUP (segment)` adds a total row (`sql/06`).

## 10. NULL and safe division
`x / NULLIF(y, 0)` returns NULL instead of an error when y = 0. CTR of a day with 0 impressions is "unknown", not 0%.

## Check yourself
1. What's the difference between WHERE and HAVING?
2. Why does win rate need a LEFT JOIN, not a JOIN?
3. What does `count(i.bid_id)` count that `count(*)` doesn't?
4. Write a query for revenue per day (CNY).
5. What does ROW_NUMBER() OVER (PARTITION BY segment ORDER BY spend DESC) do?

<details><summary>Answers</summary>

1. WHERE filters rows before grouping; HAVING filters groups after aggregation.
2. A JOIN would drop lost bids (they have no impression), so every bid would look won.
3. count(column) skips NULLs, so it counts only won bids; count(*) counts every row.
4. `SELECT ts::DATE AS day, sum(pay_price) / 100000.0 AS revenue_cny FROM impressions GROUP BY day ORDER BY day;`
5. Numbers campaigns 1, 2, 3… inside each segment, biggest spend first.
</details>
