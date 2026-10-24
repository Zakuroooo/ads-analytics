# 07 · The KPI layer, line by line
*20 minutes. Open `sql/01_kpi_daily.sql` next to this.*

## What it answers
"How is the ads business doing each day?" The recurring KPI report from the JD.

## The query in three steps

**Step 1: bids and wins per day**
```sql
WITH bid_day AS (
    SELECT b.ts::DATE              AS day,
           count(*)                AS bids,
           count(i.bid_id)         AS bids_won
    FROM bids b
    LEFT JOIN impressions i USING (bid_id)
    GROUP BY 1
),
```
- `ts::DATE` turns a timestamp like 2013-10-21 14:03:07 into the date 2013-10-21.
- LEFT JOIN keeps lost bids. `count(i.bid_id)` counts only won ones (chapter 5).
- `GROUP BY 1` means "group by the first column" (day).

**Step 2: what the won impressions earned**
```sql
imp_day AS (
    SELECT ts::DATE                         AS day,
           count(*)                         AS impressions,
           sum(pay_price) / 100000.0        AS spend_cny,
           sum(clicks)                      AS clicks,
           ...
    FROM impressions
    GROUP BY 1
)
```
Why divide by 100,000? pay_price is **fen per 1,000 impressions**. One impression costs pay_price / 1,000 fen,
and 100 fen = 1 yuan, so one impression = pay_price / 100,000 CNY.

**Toy:** pay_price 50 → 50 / 100,000 = 0.0005 CNY for that one impression.

**Step 3: put them together and compute ratios from totals**
```sql
SELECT day, bids, bids_won,
       round(bids_won / bids, 4)                AS win_rate,
       impressions,
       round(spend_cny * 1000 / impressions, 4) AS cpm_cny,
       round(clicks / impressions, 6)           AS ctr, ...
FROM bid_day
FULL OUTER JOIN imp_day USING (day)
```
FULL OUTER JOIN keeps a day even if one side is missing (Oct 28 has bids but no impressions in the public logs).

## The real output (`outputs/kpi_daily.csv`)
| Day | Impressions | Revenue (CNY) | CPM (CNY) | Win rate |
|---|---|---|---|---|
{daily_rows}

**How to read it:** CPM stays in a narrow band ({cpm_min}–{cpm_max}) while revenue swings a lot. So revenue
moved with **volume** (how many campaigns were live), not price. Peak: {peak_revenue} CNY on {peak_day}.

## Per advertiser (`sql/02_kpi_advertiser.sql`)
| Category | ID | Revenue (CNY) | Share | CPM | CTR | Win rate |
|---|---|---|---|---|---|---|
{adv_rows}

New SQL idea here: `spend_cny / sum(spend_cny) OVER ()`, a window function that divides each row by the grand total
to get its share.

Insight: {top_adv_category} brings {top_adv_share} of revenue. That's concentration risk: if it stops, revenue drops by almost half.

## How I know it's right (tie-out checks)
`tests/check_numbers.py` computes totals **twice** in different ways and compares:
- sum of daily impressions = overall impressions ({impressions_full})
- sum of advertiser revenue = overall revenue
- CPM, CTR, win rate recomputed from raw counts

Hinglish: *Ek hi number do alag tareeke se nikalo. Match nahi hua toh kahin galti hai.*

## Check yourself
1. Why divide pay_price by 100,000?
2. Why FULL OUTER JOIN in step 3?
3. Revenue peaked but CPM didn't. What does that tell you?
4. How do you know the daily table adds up?

<details><summary>Answers</summary>

1. pay_price is fen per 1,000 impressions: ÷1,000 for one impression, ÷100 to turn fen into yuan.
2. To keep days that exist on only one side (Oct 28 has bids but no impressions).
3. Revenue grew from more volume (more campaigns live), not higher prices.
4. The check script sums the daily rows and compares them with totals computed separately from the raw table; they match exactly.
</details>
