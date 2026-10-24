# Slotwise: ads analytics for a delivery marketplace
*Built on public ad data. Not Swiggy data, no Swiggy users.*

**Live dashboard:** _link added after deploy_ · **Excel / Google Sheets model:** [`excel/ads_kpi_model.xlsx`](excel/ads_kpi_model.xlsx) · **1-page memo:** [`docs/MEMO.md`](docs/MEMO.md)

I wanted to understand how the ads team of a food-delivery app makes decisions. Which advertisers
should it grow? Is the auction healthy? What would a price change earn? Did a new ad treatment
actually work? Marketplace ad data isn't public, so I used three real public ad datasets and
analysed them the way that team would.

## What I found

| Question | Answer from the data |
|---|---|
| How is the ads business doing? | {revenue} CNY of ad revenue from {impressions} impressions over {first_day} to {last_day}. CPM held between {cpm_min} and {cpm_max} CNY, so revenue moved with volume, not price. |
| Is the auction healthy? | Thin competition. Where a floor exists it set the price on {floor_binding} of impressions; exchange {no_floor_exchange} sells {no_floor_share} of impressions with no floor at all. |
| What would a minimum floor earn? | It's a bet on retention. At 30 fen per 1,000 impressions, {x30_at_risk} of impressions are at risk; revenue ranges {x30_lower} to {x30_upper}, and it pays off only if at least {x30_breakeven} still sell. |
| Which advertisers to grow or fix? | Top 20% of {campaigns} campaigns hold {top20_share} of spend. A "fix" group with {fix_share} of spend pays {fix_cpa_ratio} more per conversion and is pulling back (week 4 = {fix_retention} of week 1). |
| Did the ad treatment work? | Yes. Randomised test on {ab_users} users: conversion {conv_c} → {conv_t}, {conv_rel} (95% CI {conv_rel_lo} to {conv_rel_hi}). Decision rule written before the readout: {decision}. |

## What's inside

| Piece | What it does | Where |
|---|---|---|
| SQL layer (DuckDB over Parquet) | daily KPIs, advertiser KPIs, auction health, floor sizing, campaign segments | [`sql/`](sql/) |
| A/B readout | lift, 95% CI, p-value, sample-ratio check, MDE, decision rule | [`analysis/ab_readout.py`](analysis/ab_readout.py) |
| Excel / Sheets model | SUMIFS, COUNTIFS, XLOOKUP, INDEX/MATCH, NORM.S.INV; floor model with editable inputs | [`excel/`](excel/) |
| Dashboard | static page, every number read from the SQL output | [`dashboard/`](dashboard/) |
| Checks | 29 tie-outs + 21 Excel cells recalculated and matched | [`tests/`](tests/) |
| Docs | PRD, data, metrics, experiment design, decisions, memo | [`docs/00-README.md`](docs/00-README.md) |

## How I know the numbers are right
- Every Parquet file's row count equals the raw file's line count; Criteo counts equal the published counts.
- The same number computed two ways must match: daily totals = overall totals, segments add to 100%, the floor model at today's floor equals today's revenue.
- The A/B maths matches statsmodels, and an independent re-derivation from the raw counts matched to 6 significant figures.
- The Excel file is recalculated by a formula engine and compared with the SQL results.
- Every number in this README, the memo and the story is filled in from `outputs/numbers.json` by a script, not typed by hand.

## What didn't work / limits
- **Fill rate can't be computed.** It needs ad requests that went unfilled; no public log has them. I show win rate instead, labelled as a stand-in.
- **ROAS can't be computed.** No dataset has order value. I use cost per conversion (CPA).
- **iPinYou's bids aren't real valuations.** Its README says the campaigns used a fixed high bid. My first floor model trusted those bids; I replaced it with one that uses only prices paid plus a break-even ([ADR 0007](docs/adr/0007-floor-sizing-minimum-floor-break-even.md)).
- **Some impressions are missing.** iPinYou cut its test set out of the logs. I added the public part back, but a reserved part was never released, so totals after Oct 21 are lower bounds. Ratios are still fair because the split was random.
- **Advertiser churn can't be measured.** Criteo's sample keeps almost every campaign active all month, so I measured shrinking spend instead.
- **Criteo's click-through rate is not a real display CTR.** The sample is heavy in clicked impressions; I only compare campaigns with each other.
- **The "effect on exposed users" in the A/B test is implausible** (only {exposure} of treatment users were exposed), so I report it but don't use it.

## Run it
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/download_data.py && python scripts/to_parquet.py   # needs a Kaggle token
python run_all.py                                                  # rebuilds and checks everything
```
Details: [docs/RUNBOOK.md](docs/RUNBOOK.md).

## Data and licences
iPinYou RTB dataset, season 3 (Zhang et al. 2014, public contest release). Criteo Attribution Modeling and Criteo Uplift v2.1 (Criteo AI Lab, CC BY-NC-SA 4.0). Raw data is not in this repo. Aggregated outputs are derived from CC BY-NC-SA data and shared under the same terms, for non-commercial use. Full notes: [docs/DATA.md](docs/DATA.md).
