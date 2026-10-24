-- 06_segment_summary.sql
-- Question: how big is each advertiser group, how efficient, and is its spend growing or shrinking?
-- Grain: one row per segment (PROTECT / FIX / GROW / WATCH) + a total row.
-- "Spend retention" = week-4 spend / week-1 spend for the same campaigns (like net revenue retention).
-- Criteo's sample keeps almost every campaign active all 31 days, so true churn (campaigns that stop)
-- can't be measured here; spend retention is what's left to see.
-- Uses the same segment rule as 05 (repeated here so this file runs on its own).

WITH c AS (
    SELECT *, spend / nullif(conversions, 0) AS cpa FROM campaigns
),
cut AS (
    SELECT median(spend) AS median_spend, median(cpa) AS median_cpa FROM c
),
labelled AS (
    SELECT c.*,
           CASE WHEN c.spend >= cut.median_spend AND c.cpa <= cut.median_cpa THEN 'PROTECT'
                WHEN c.spend >= cut.median_spend                              THEN 'FIX'
                WHEN c.cpa <= cut.median_cpa                                  THEN 'GROW'
                ELSE 'WATCH' END AS segment
    FROM c CROSS JOIN cut
)

SELECT coalesce(segment, 'ALL')                                   AS segment,
       count(*)                                                   AS campaigns,
       round(sum(spend), 2)                                       AS spend,
       round(sum(spend) / (SELECT sum(spend) FROM campaigns), 4)  AS spend_share,
       sum(conversions)                                           AS conversions,
       round(sum(clicks) / sum(impressions), 6)                   AS ctr,
       round(sum(conversions) / sum(clicks), 4)                   AS cvr,
       round(sum(spend) / sum(conversions), 6)                    AS cpa,
       round(sum(spend_w4) / sum(spend_w1), 4)                    AS spend_retention_w4_vs_w1,
       -- campaigns whose week-4 spend fell below half of week 1: the "call them now" list
       count(*) FILTER (WHERE spend_w4 < 0.5 * spend_w1)          AS campaigns_spend_halved
FROM labelled
GROUP BY ROLLUP (segment)
ORDER BY segment IS NULL, spend DESC;
