# METRICS — definitions the whole project uses
*If a metric's definition changes, it changes here first, then in SQL, with a line in PROGRESS.md.*

| Metric | Formula | Unit | Data | Edge cases |
|---|---|---|---|---|
| **Bids** | count of bid requests iPinYou bid on | count | iPinYou bid log | duplicates by `BidID` removed |
| **Impressions** | count of won auctions where the ad was shown | count | iPinYou imp log | an imp without a matching bid is counted and flagged |
| **Win rate** *(stand-in for fill rate)* | impressions / bids | % | iPinYou | bidder's view, not publisher's (ADR 0005) |
| **Revenue / spend** | Σ price paid per impression ÷ 1,000 | CNY fen (2013) | iPinYou `PayingPrice` is fen per 1,000 imps ✅ | same money: advertiser spend = marketplace revenue |
| **CPM** | revenue / impressions × 1,000 | fen per 1,000 imps | iPinYou | = average `PayingPrice` |
| **Clicks** | count of click log rows joined to an imp | count | iPinYou clk | repeat clicks on one imp counted once |
| **CTR** | clicks / impressions | % | iPinYou, Criteo Attr. | undefined when imps = 0 → NULL, not 0 |
| **Conversions** | count of conversion rows joined to an imp | count | iPinYou conv, Criteo Attr. | one per imp |
| **CVR** | conversions / clicks | % | both | post-click; NULL if clicks = 0 |
| **CPC** | spend / clicks | cost units | both | NULL if clicks = 0 |
| **CPA** *(stand-in for ROAS)* | spend / conversions | cost units | both | NULL if conversions = 0; shown as "no conversions" |
| **Advertiser count** | distinct advertisers (iPinYou) or campaigns (Criteo) with spend > 0 in the period | count | both | Criteo campaign = advertiser proxy |
| **Floor binding rate** | share of imps where paid ≤ floor × 1.05 | % | iPinYou | 5% band because of price rounding ⏳ (check distribution) |
| **Bid-to-pay ratio** | bid / paid, median | ratio | iPinYou | paid = 0 rows excluded and counted |
| **Spend share (top x%)** | spend of top x% campaigns / total spend | % | Criteo Attr. | campaigns ranked by spend |
| **Weekly retention** | campaigns active in week w that were also active in their first week / campaigns in cohort | % | Criteo Attr. | active = spend > 0 that week |
| **Conversion rate (A/B)** | users with conversion / users | % | Criteo Uplift | per user, not per visit |
| **Lift (abs / rel)** | p_T − p_C; (p_T − p_C) / p_C | pp / % | Criteo Uplift | see EXPERIMENT.md |

## Defined, but not computable here (ADR 0005)
| Metric | Formula | Needs |
|---|---|---|
| **Fill rate** | impressions served / ad requests received | ad requests with no ad served (publisher log) |
| **ROAS** | attributed order value / ad spend | order value per conversion |
| **Inventory utilisation** | sold ad slots / available ad slots | count of available slots per page view |
