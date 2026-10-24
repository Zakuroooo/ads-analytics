-- 04_floor_sizing.sql
-- Question: what would a minimum floor price of X earn? (opportunity sizing for a pricing change)
-- Model (ADR 0007): new floor = max(current floor, X). An impression that paid p >= X is unchanged.
-- One that paid p < X is "at risk": it either still sells at X, or is lost. We don't know the share
-- that still sells (r), so we report r = 0 (lower bound), r = 1 (upper bound) and the break-even r.
-- X is in fen per 1,000 impressions (same unit as pay_price); money columns are in CNY.

-- Step 1: the candidate minimum floors to test: 0, 10, 20, ... 150 fen CPM
WITH levels AS (
    SELECT unnest(range(0, 160, 10)) AS min_floor
),

-- Step 2: for each level, split impressions into "unchanged" and "at risk".
-- A CROSS JOIN pairs every impression with every level (16 levels × 4.7M rows, aggregated on the fly).
-- GROUPING SETS gives the all-exchange total and one row per exchange in the same pass.
per_level AS (
    SELECT l.min_floor,
           CASE WHEN GROUPING(i.exchange) = 1 THEN 'ALL'
                ELSE coalesce(i.exchange::VARCHAR, 'mobile/unknown') END  AS exchange,
           count(*)                                                    AS impressions,
           sum(i.pay_price)                                            AS revenue_now_fen,
           count(*) FILTER (WHERE i.pay_price < l.min_floor)           AS at_risk_imps,
           coalesce(sum(i.pay_price) FILTER (WHERE i.pay_price < l.min_floor), 0)  AS at_risk_revenue_fen,
           coalesce(sum(i.pay_price) FILTER (WHERE i.pay_price >= l.min_floor), 0) AS safe_revenue_fen,
           -- the bidder can't pay more than it bid; if X > bid the impression is lost for sure
           count(*) FILTER (WHERE i.pay_price < l.min_floor AND i.bid_price >= l.min_floor) AS can_sell_at_x
    FROM impressions i
    CROSS JOIN levels l
    GROUP BY GROUPING SETS ((l.min_floor), (l.min_floor, i.exchange))
)

-- Step 3: revenue under each assumption, converted to CNY (/1000 per impression, /100 fen per yuan)
SELECT exchange,
       min_floor                                                          AS min_floor_fen_cpm,
       impressions,
       at_risk_imps,
       round(at_risk_imps / impressions, 4)                               AS share_at_risk,
       round(revenue_now_fen / 100000.0, 2)                               AS revenue_now_cny,
       round(safe_revenue_fen / 100000.0, 2)                              AS revenue_lower_cny,   -- r = 0
       round((safe_revenue_fen + min_floor * can_sell_at_x) / 100000.0, 2) AS revenue_upper_cny,  -- r = 1
       round((safe_revenue_fen + 0.5 * min_floor * can_sell_at_x) / 100000.0, 2) AS revenue_r50_cny,
       round((safe_revenue_fen + min_floor * can_sell_at_x) / revenue_now_fen - 1, 4) AS upper_change,
       -- share of at-risk impressions that must still sell at X for revenue to stay flat
       round(at_risk_revenue_fen / nullif(min_floor * can_sell_at_x, 0), 4) AS breakeven_retention
FROM per_level
ORDER BY exchange = 'ALL' DESC, exchange, min_floor;
