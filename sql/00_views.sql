-- 00_views.sql
-- Gives each Parquet dataset a short table name, so every other query reads like plain SQL.
-- A VIEW stores no data; it is a saved query that runs when you select from it.

-- iPinYou: one row per bid request iPinYou bid on (won or lost)
CREATE OR REPLACE VIEW bids AS
SELECT * FROM read_parquet('data/ipinyou/bid/*.parquet');

-- iPinYou: one row per auction iPinYou won and showed an ad (has the price actually paid)
CREATE OR REPLACE VIEW imps AS
SELECT * FROM read_parquet('data/ipinyou/imp/*.parquet');

-- iPinYou: one row per click / conversion event, linked to an impression by bid_id
CREATE OR REPLACE VIEW clicks AS
SELECT * FROM read_parquet('data/ipinyou/clk/*.parquet');

CREATE OR REPLACE VIEW convs AS
SELECT * FROM read_parquet('data/ipinyou/conv/*.parquet');

-- Leaderboard test impressions (Oct 22-28). iPinYou took these out of the training impression
-- log; they carry their own click count and conversion flag instead of separate event logs.
CREATE OR REPLACE VIEW test_imps AS
SELECT * FROM read_parquet('data/ipinyou/test_imp/*.parquet');

-- The impression table every analysis uses: training + test impressions, one row per auction.
-- About 0.3% of bid_ids appear twice with identical values, so ROW_NUMBER keeps the first one.
CREATE OR REPLACE VIEW impressions AS
WITH train AS (
    -- training impressions get clicks/conversions by joining the event logs on bid_id
    SELECT i.*,
           coalesce(c.n_clicks, 0)              AS clicks,
           (v.bid_id IS NOT NULL)::INT          AS conversion,
           'train'                              AS source
    FROM imps i
    LEFT JOIN (SELECT bid_id, count(*) AS n_clicks FROM clicks GROUP BY bid_id) c USING (bid_id)
    LEFT JOIN (SELECT DISTINCT bid_id FROM convs) v USING (bid_id)
),
test AS (
    SELECT * EXCLUDE (click_count, has_conv),
           click_count AS clicks, has_conv AS conversion, 'test' AS source
    FROM test_imps
),
both_sets AS (
    SELECT * FROM train
    UNION ALL BY NAME
    SELECT * FROM test
)
SELECT * EXCLUDE (rn)
FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY bid_id ORDER BY source DESC, ts) AS rn FROM both_sets)
WHERE rn = 1;

-- Advertiser industries, from the iPinYou dataset paper (Zhang et al. 2014, Table 2)
CREATE OR REPLACE VIEW advertisers AS
SELECT * FROM (VALUES
    (2259, 'Milk powder'),
    (2261, 'Telecom'),
    (2821, 'Footwear'),
    (2997, 'Mobile app install')
) AS t(advertiser_id, category);

-- Criteo Attribution: one row per impression, 30 days, many campaigns
CREATE OR REPLACE VIEW attribution AS
SELECT * FROM read_parquet('data/attribution.parquet');

-- One row per Criteo campaign (our stand-in for "advertiser"): spend, outcomes, weekly spend.
-- timestamp is seconds since the start of the 30-day window, so timestamp // 86400 = day 0..30.
-- Conversions = sum(attribution): the impression a conversion was credited to (last touch).
-- Weeks 1-4 = days 0-6, 7-13, 14-20, 21-27; days 28-30 are a partial week and left out of weekly figures.
CREATE OR REPLACE VIEW campaigns AS
SELECT campaign,
       count(*)                                                     AS impressions,
       sum(click)                                                   AS clicks,
       sum(attribution)                                             AS conversions,
       sum(cost)                                                    AS spend,
       count(DISTINCT timestamp // 86400)                           AS active_days,
       sum(cost) FILTER (WHERE timestamp // 86400 BETWEEN 0 AND 6)    AS spend_w1,
       sum(cost) FILTER (WHERE timestamp // 86400 BETWEEN 7 AND 13)   AS spend_w2,
       sum(cost) FILTER (WHERE timestamp // 86400 BETWEEN 14 AND 20)  AS spend_w3,
       sum(cost) FILTER (WHERE timestamp // 86400 BETWEEN 21 AND 27)  AS spend_w4
FROM attribution
GROUP BY campaign;

-- Criteo Uplift: one row per user in the randomised test
CREATE OR REPLACE VIEW uplift AS
SELECT * FROM read_parquet('data/uplift.parquet');
