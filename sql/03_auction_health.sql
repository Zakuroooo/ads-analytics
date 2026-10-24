-- 03_auction_health.sql
-- Question: is the price set by real competition, or by the floor (reserve) price? Where is the auction weak?
-- In a second-price auction the winner pays max(second-highest bid, floor). So when the price paid
-- equals the floor, no other bidder came close: the floor alone set the price ("floor binding").
-- Grain: one row per ad exchange × slot visibility, one total row per exchange, one grand total.
-- Advertiser 2997 (mobile app) has no exchange recorded; it shows as 'mobile/unknown'.

-- Step 1: bids and wins per exchange (win rate is only shown on exchange-total rows)
WITH bid_ex AS (
    SELECT b.exchange,
           count(*)          AS bids,
           count(i.bid_id)   AS bids_won
    FROM bids b
    LEFT JOIN impressions i USING (bid_id)
    GROUP BY 1
),

-- Step 2: price signals for every won impression
imp AS (
    SELECT exchange,
           slot_visibility,
           pay_price,
           floor_price,
           (floor_price > 0)::INT                                   AS has_floor,
           (floor_price > 0 AND pay_price <= floor_price)::INT      AS floor_binding,
           (pay_price < floor_price)::INT                           AS paid_below_floor,
           clicks
    FROM impressions
),

-- Step 3: aggregate at three levels in one pass. GROUPING SETS = several GROUP BYs at once.
-- GROUPING(col) is 1 when that column was rolled up (so the row is a total), else 0.
agg AS (
    SELECT exchange,
           slot_visibility,
           GROUPING(exchange)                                        AS is_grand_total,
           GROUPING(slot_visibility)                                 AS is_exchange_total,
           count(*)                                                  AS impressions,
           sum(pay_price) / 100000.0                                 AS spend_cny,
           avg(pay_price) / 100.0                                    AS cpm_cny,
           median(pay_price) / 100.0                                 AS median_cpm_cny,
           avg(has_floor)                                            AS share_with_floor,
           avg(floor_price) / 100.0                                  AS avg_floor_cpm_cny,
           -- among impressions that have a floor: how often did the floor set the price?
           sum(floor_binding) / nullif(sum(has_floor), 0)            AS floor_binding_rate,
           sum(paid_below_floor)                                     AS paid_below_floor,
           sum(clicks) / count(*)                                    AS ctr
    FROM imp
    GROUP BY GROUPING SETS ((exchange, slot_visibility), (exchange), ())
)

SELECT CASE WHEN a.is_grand_total = 1 THEN 'ALL'
            ELSE coalesce(a.exchange::VARCHAR, 'mobile/unknown') END        AS exchange,
       CASE WHEN a.is_exchange_total = 1 THEN 'ALL' ELSE a.slot_visibility END AS slot_visibility,
       a.impressions,
       round(a.spend_cny, 2)                     AS spend_cny,
       round(a.cpm_cny, 4)                       AS cpm_cny,
       round(a.median_cpm_cny, 4)                AS median_cpm_cny,
       round(a.share_with_floor, 4)              AS share_with_floor,
       round(a.avg_floor_cpm_cny, 4)             AS avg_floor_cpm_cny,
       round(a.floor_binding_rate, 4)            AS floor_binding_rate,
       a.paid_below_floor,
       round(a.ctr, 6)                           AS ctr,
       -- win rate: only meaningful on exchange-level rows (bids have no slot breakdown after losing)
       CASE WHEN a.is_exchange_total = 1 AND a.is_grand_total = 0
            THEN round(b.bids_won / b.bids, 4) END AS win_rate
FROM agg a
LEFT JOIN bid_ex b ON a.exchange IS NOT DISTINCT FROM b.exchange
ORDER BY a.is_grand_total, a.exchange NULLS LAST, a.is_exchange_total DESC, a.impressions DESC;
