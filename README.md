# Slotwise — ads analytics for a delivery marketplace
*Working name. Built on public ad data. Not Swiggy data, no Swiggy users.*

I wanted to understand how the ads team of a food-delivery app decides things: which advertisers
to grow, whether an auction is healthy, what a price change would earn, and whether a new ad format
actually works. Marketplace ad data isn't public, so I used three real public ad datasets and
analysed them the way that team would.

> **Status (2026-10-24):** design docs written, build not started. Every number below appears only
> after `python run_all.py` produces it.

## What I built

| Question an ads team asks | What I did | Where |
|---|---|---|
| How is the ads business doing this week? | KPI layer in SQL: revenue, impressions, CPM, CTR, CVR, CPA, win rate, advertiser count | `sql/01–02`, dashboard |
| Is the auction healthy? | bid vs price paid, how often the floor price decides the price, win rate by exchange and slot | `sql/03` |
| What would a floor-price change earn? | sizing model with editable assumptions | `sql/04`, Excel |
| Which advertisers should we grow or fix? | spend tiers, CPA, retention cohorts across 675 campaigns | `sql/05–06` |
| Did the new ad treatment work? | readout of a real randomised test on 13.9M users | `analysis/ab_readout.py` |

Results: _filled from `outputs/numbers.json` after the build._

## Data
iPinYou RTB logs (season 3, 2013), Criteo Attribution Modeling dataset, Criteo Uplift v2.1.
Sources, licences, schemas and limits: [docs/DATA.md](docs/DATA.md).

## What didn't work / limits
- **Fill rate can't be computed.** It needs ad requests that went unfilled, and no public log has them. I show win rate instead and say so.
- **ROAS can't be computed.** None of the datasets has order value. I use cost per conversion (CPA).
- iPinYou has only 4 advertisers, so advertiser segmentation uses Criteo's campaigns instead.
- Prices are 2013 Chinese ad-exchange units and Criteo's scaled cost units, not rupees.
- _More added here as the build finds them._

## Run it
See [CONTRIBUTING.md](CONTRIBUTING.md). One command: `python run_all.py`.

## Docs
Start at [docs/00-README.md](docs/00-README.md). The project as a story: [docs/STORY.md](docs/STORY.md).
