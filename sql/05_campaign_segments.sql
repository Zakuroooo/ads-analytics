-- 05_campaign_segments.sql
-- Question: which advertisers should ad sales grow, protect, fix or watch?
-- Grain: one row per Criteo campaign (675). Cost is Criteo's transformed unit, not real money,
-- so compare campaigns with each other, never read the values as currency.
--
-- Two cuts, each at the median, give four groups:
--   spend: high / low        efficiency (CPA = cost per conversion): low CPA is good
--   high spend + low CPA  -> PROTECT  (big and efficient: keep them happy, upsell)
--   high spend + high CPA -> FIX      (big but paying a lot per conversion: churn risk)
--   low spend  + low CPA  -> GROW     (efficient but small: room to spend more)
--   low spend  + high CPA -> WATCH    (small and expensive)

-- Step 1: per-campaign ratios, plus each campaign's rank by spend (window function)
WITH c AS (
    SELECT campaign,
           impressions, clicks, conversions, spend,
           clicks / impressions                              AS ctr,
           conversions / nullif(clicks, 0)                   AS cvr,
           spend / nullif(conversions, 0)                    AS cpa,
           spend_w1, spend_w4,
           spend_w4 / nullif(spend_w1, 0)                    AS spend_retention_w4_vs_w1,
           ROW_NUMBER() OVER (ORDER BY spend DESC)           AS spend_rank
    FROM campaigns
),

-- Step 2: the two medians that split campaigns into halves
cut AS (
    SELECT median(spend) AS median_spend, median(cpa) AS median_cpa FROM c
)

-- Step 3: label each campaign and add its running share of total spend (a running total)
SELECT c.campaign,
       c.spend_rank,
       c.impressions, c.clicks, c.conversions,
       round(c.spend, 4)                                     AS spend,
       round(c.spend / sum(c.spend) OVER (), 6)              AS spend_share,
       round(sum(c.spend) OVER (ORDER BY c.spend_rank) / sum(c.spend) OVER (), 4) AS cumulative_spend_share,
       round(c.ctr, 6)                                       AS ctr,
       round(c.cvr, 4)                                       AS cvr,
       round(c.cpa, 6)                                       AS cpa,
       round(c.spend_retention_w4_vs_w1, 4)                  AS spend_retention_w4_vs_w1,
       CASE WHEN c.spend >= cut.median_spend AND c.cpa <= cut.median_cpa THEN 'PROTECT'
            WHEN c.spend >= cut.median_spend                              THEN 'FIX'
            WHEN c.cpa <= cut.median_cpa                                  THEN 'GROW'
            ELSE 'WATCH' END                                 AS segment
FROM c CROSS JOIN cut
ORDER BY c.spend_rank;
