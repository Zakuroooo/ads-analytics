-- 02_kpi_advertiser.sql
-- Question: which advertisers (and categories) drive the ads business, and how well do their ads work?
-- Grain: one row per advertiser. Money in CNY.
-- Conversions exist only for 2 of the 4 advertisers (iPinYou logged landing-page visits for them),
-- so CPA is NULL for the others rather than 0.

-- Step 1: bids and wins per advertiser
WITH bid_adv AS (
    SELECT b.advertiser_id,
           count(*)          AS bids,
           count(i.bid_id)   AS bids_won
    FROM bids b
    LEFT JOIN impressions i USING (bid_id)
    GROUP BY 1
),

-- Step 2: outcomes of won impressions per advertiser
imp_adv AS (
    SELECT advertiser_id,
           count(*)                     AS impressions,
           sum(pay_price) / 100000.0    AS spend_cny,
           sum(clicks)                  AS clicks,
           sum(conversion)              AS conversions,
           count(DISTINCT ts::DATE)     AS active_days
    FROM impressions
    GROUP BY 1
)

-- Step 3: ratios + each advertiser's share of total spend (window function over all rows)
SELECT a.advertiser_id,
       adv.category,
       a.active_days,
       b.bids,
       round(b.bids_won / b.bids, 4)                              AS win_rate,
       a.impressions,
       round(a.spend_cny, 2)                                      AS spend_cny,
       round(a.spend_cny / sum(a.spend_cny) OVER (), 4)           AS spend_share,
       round(a.spend_cny * 1000 / a.impressions, 4)               AS cpm_cny,
       a.clicks,
       round(a.clicks / a.impressions, 6)                         AS ctr,
       round(a.spend_cny / nullif(a.clicks, 0), 4)                AS cpc_cny,
       a.conversions,
       -- no conversions logged = conversions not tracked for this advertiser, so NULL not 0%
       CASE WHEN a.conversions > 0 THEN round(a.conversions / a.clicks, 4) END AS cvr,
       round(a.spend_cny / nullif(a.conversions, 0), 4)           AS cpa_cny
FROM imp_adv a
JOIN bid_adv b USING (advertiser_id)
JOIN advertisers adv USING (advertiser_id)
ORDER BY spend_cny DESC;
