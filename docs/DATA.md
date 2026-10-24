# DATA — sources, licences, schemas, limits
*Every fact marked ✅ is checked against the downloaded files in phase P1; ⏳ means not yet checked.*

## 1. The three datasets

```mermaid
flowchart LR
    I[iPinYou RTB logs<br/>season 3, Oct 2013] -->|bids, imps, clicks, convs| P1[Ads P&L KPIs<br/>auction health<br/>floor sizing]
    CA[Criteo Attribution<br/>30 days, 675 campaigns] -->|cost, clicks, convs per campaign| P2[Advertiser segments<br/>retention, CPA]
    CU[Criteo Uplift v2.1<br/>13.9M users, randomised] -->|treatment, visit, conversion| P3[A/B readout]
```

| | iPinYou RTB (season 3) | Criteo Attribution | Criteo Uplift v2.1 |
|---|---|---|---|
| Publisher | iPinYou (Chinese DSP), for its 2013 bidding contest | Criteo AI Lab | Criteo AI Lab |
| Paper | Zhang et al. 2014, *Real-Time Bidding Benchmarking with iPinYou Dataset* (arXiv:1407.7073) | Diemert et al. 2017, *Attribution Modeling Increases Efficiency of Bidding in Display Advertising* | Diemert et al. 2018, *A Large Scale Benchmark for Uplift Modeling* |
| Where I get it | Kaggle mirror `lastsummer/ipinyou` (`training3rd/`) | Kaggle mirror `sharatsachin/criteo-attribution-modeling` | Kaggle mirror `arashnic/uplift-modeling` |
| Licence | No explicit licence; README says iPinYou "now release[s] all the training datasets" for the public contest ✅ | CC BY-NC-SA 4.0 (Criteo AI Lab page) ✅ | CC BY-NC-SA 4.0 (Criteo AI Lab page) ✅ |
| Download | ~880 MB bz2 (bid ~650 MB, imp ~220 MB, clk/conv small) | ~670 MB zip → 2.6 GB TSV | 324 MB zip → 3.2 GB CSV ✅ |
| Rows | to count ⏳ | "16.5M impressions, 45K conversions, 700 campaigns" (Criteo page) ⏳ | **13,979,592** = published v2.1 count ✅ |

**Notes from the sources (✅ read 2026-10-24):**
- iPinYou README: logs come from campaigns run "with a fixed relatively high-price bidding strategy (with exceptions on some campaigns in the third season)". So iPinYou's bid is **not** a real advertiser valuation; the paying price (set by competitors or the floor) is the more meaningful market signal. In season 3, "conversion" means a landing-page visit, not a purchase.
- Criteo Attribution: `cost` and `cpo` are "not the real price, only a transformed version of it"; data is sub-sampled.
- Criteo Uplift: pooled from several incrementality tests, sub-sampled non-uniformly; treatment ratio 0.85 (observed 0.8500001).

Licence line for the README: *Non-commercial, educational analysis; datasets credited to iPinYou and
Criteo AI Lab under their published terms. No raw data is redistributed in this repo.*

## 2. Schemas (fields I use)

**iPinYou** (tab-separated, no header; season 2/3 format ⏳):

| Field | Meaning | Used for |
|---|---|---|
| `BidID`, `Timestamp` | one auction, time `yyyyMMddHHmmssSSS` | join bids ↔ imps; daily KPIs |
| `AdExchange` | which exchange sent the request (1–3, anonymised) | win rate / CPM by exchange |
| `AdSlotWidth`, `AdSlotHeight`, `AdSlotVisibility`, `AdSlotFormat` | the ad slot | inventory segments |
| `AdSlotFloorPrice` | the floor (reserve) price for this slot | auction health, sizing |
| `BiddingPrice` | what iPinYou bid | bid vs price paid |
| `PayingPrice` (imp log only) | price actually paid when won | revenue, CPM |
| `AdvertiserID` | 4 advertisers in season 3 (industries known, see below) | per-advertiser and per-category KPIs |
| clk / conv logs | one row per click / conversion, keyed by `BidID` | CTR, CVR, CPA |

Prices: "RMB and the unit of Chinese fen ×1000, corresponding to the ... CPM pricing model" (Zhang et al. 2014) ✅. So a `PayingPrice` of 48 means 48 fen per 1,000 impressions; one impression costs 0.048 fen. Auctions are second price (same paper) ✅.

Season-3 advertisers (paper, Table 2) ✅: **2259 milk powder · 2261 telecom · 2821 footwear · 2997 mobile e-commerce app install**.

**Criteo Attribution** (TSV with header): `timestamp`, `uid`, `campaign`, `conversion`, `conversion_timestamp`,
`conversion_id`, `attribution`, `click`, `click_pos`, `click_nb`, `cost`, `cpo`, `time_since_last_click`, `cat1`–`cat9` ⏳.
`cost` = price paid for the impression (scaled); `cpo` = cost per order for the campaign (scaled).

**Criteo Uplift** (CSV with header): `f0`–`f11` (anonymised user features), `treatment` (1 = in the ad group),
`conversion`, `visit`, `exposure` (1 = actually saw an ad) ⏳.

## 2b. Data quality findings (P1, 2026-10-24) ✅

| Check | Result | What I did |
|---|---|---|
| Row counts raw vs Parquet | all 39 files match exactly; Criteo files match published counts (16,468,027 · 13,979,592) | — |
| iPinYou rows | 11,457,419 bids (all unique) · 3,158,171 training imps · 1,579,086 test imps · 2,716 clicks · 539 conversions | — |
| Duplicate `bid_id` in impressions | 9,914 train + 1,872 test ids appear twice; values identical in all but 4 | keep one row per `bid_id` (`ROW_NUMBER`) |
| **Missing impressions** | README: season-3 test set "is generated from the normal training data". 1,574,644 leaderboard-test imps are in the bid log but not in the training imp log | added the leaderboard test file back (`test_imps`) |
| Still missing | iPinYou also withheld a "reserved" test part (not public) | **totals for Oct 21–28 are lower bounds**; ratios (CPM, CTR, floor binding) stay fair because the split was random |
| Imps with no matching bid | 19,929 (0.4%) | kept in KPIs, excluded from win rate |
| Price sanity | no negative prices; no imp paid more than its bid; 13,237 paid below floor (0.4%) | kept, counted in auction health |
| Advertiser 2997 `exchange` | NULL for all rows (mobile app inventory) | shown as "mobile / unknown" |
| Clicks, conversions | small: ~3.9K clicks, ~780 conversions in total | CTR fine at this volume; CVR/CPA per advertiser reported with counts, not over-read |

After all conversions the deduplicated `impressions` view has 4,724,634 rows.

## 3. Processing
Raw → Parquet once, streamed, then raw deleted (ADR 0001). iPinYou bz2 is decompressed with `bzcat`
in a pipe, one file at a time. No sampling unless a step runs out of memory; if I sample, it's stated here
with the seed and fraction.

## 4. What this data CANNOT tell us
| Wanted (JD) | Why not | What I show instead |
|---|---|---|
| **Fill rate** | needs requests where no ad was served; logs only contain requests iPinYou bid on | **win rate** = won imps / bids (bidder's view), labelled as such |
| **ROAS** | no order value in any dataset | **CPA** (cost per conversion) |
| Advertiser count trends at scale | iPinYou: 4 advertisers | Criteo: 675 campaigns as the advertiser proxy |
| Rupee revenue | 2013 CNY fen; Criteo scaled | real units; ₹ only as "illustrative, assumes X" |
| Other bidders' bids | logs show iPinYou's bid only | sizing assumes a lost impression stays unsold (conservative) — ADR 0004 |
| Categories (food, grocery…) | features are hashed (`cat1`–`cat9`) | "segment" = hashed category value, never renamed to a real category |
