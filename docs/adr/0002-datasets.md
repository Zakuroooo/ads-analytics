# 0002 — iPinYou + Criteo Attribution + Criteo Uplift
Status: Accepted · Date: 2026-10-24

## Context
I need real ad data covering: auction prices (floor, bid, paid), advertiser-level spend and outcomes, and a real randomised experiment. Marketplace ad data (Swiggy, Zomato, Instacart) is not public.

## Options
1. Synthetic data shaped like Swiggy Ads: looks relevant, but every number is invented.
2. Avazu / Criteo display CTR datasets: clicks only, no prices, no advertisers.
3. iPinYou RTB logs: floor, bid, paid price, exchange, slot, 4 advertisers, clicks, conversions.
4. Criteo Attribution (675 campaigns, cost, conversions) + Criteo Uplift (randomised test, 13.9M users).

## Decision
3 + 4: iPinYou season 3 for the P&L and auction, Criteo Attribution for advertisers, Criteo Uplift for the A/B readout.

## Why
- Real data means every number survives an interviewer's "where did this come from?". Synthetic fails that.
- iPinYou is the only public log I found with **floor price, bid and price paid together**, which auction health and floor sizing need.
- Criteo Uplift is a true randomised test at scale, so the readout is causal, not a correlation dressed up.

## Consequences
- Three datasets means three schemas and more setup time; cut order in BUILD-PLAN.
- Limits I must state: 2013 prices, 4 iPinYou advertisers, hashed categories, no order value (DATA.md §4).
- Season 3 chosen over season 2: same fields, about a third of the download size.
