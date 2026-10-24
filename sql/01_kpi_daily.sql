-- 01_kpi_daily.sql
-- Question: how is the ads business doing each day? (the recurring KPI report)
-- Grain: one row per day. Money in CNY (iPinYou pay_price is fen per 1,000 impressions,
-- so one impression costs pay_price / 1000 fen = pay_price / 100000 CNY).
-- Caveat: Oct 21-28 totals are lower bounds (iPinYou withheld a test set); ratios are fair.

-- Step 1: bids per day, and how many of them we won (win rate = stand-in for fill rate)
WITH bid_day AS (
    SELECT b.ts::DATE              AS day,
           count(*)                AS bids,
           count(i.bid_id)         AS bids_won          -- LEFT JOIN: NULL when the bid lost
    FROM bids b
    LEFT JOIN impressions i USING (bid_id)
    GROUP BY 1
),

-- Step 2: what the won impressions earned and produced, per day
imp_day AS (
    SELECT ts::DATE                         AS day,
           count(*)                         AS impressions,
           sum(pay_price) / 100000.0        AS spend_cny,
           sum(clicks)                      AS clicks,
           sum(conversion)                  AS conversions,
           count(DISTINCT advertiser_id)    AS active_advertisers
    FROM impressions
    GROUP BY 1
)

-- Step 3: put them side by side and compute the ratios from totals (never average daily ratios)
SELECT day,
       bids,
       bids_won,
       round(bids_won / bids, 4)                          AS win_rate,
       impressions,
       round(spend_cny, 2)                                AS spend_cny,
       round(spend_cny * 1000 / impressions, 4)           AS cpm_cny,
       clicks,
       round(clicks / impressions, 6)                     AS ctr,
       round(spend_cny / nullif(clicks, 0), 4)            AS cpc_cny,
       conversions,
       active_advertisers
FROM bid_day
FULL OUTER JOIN imp_day USING (day)   -- keeps a day that has bids but no impressions (Oct 28)
ORDER BY day;
