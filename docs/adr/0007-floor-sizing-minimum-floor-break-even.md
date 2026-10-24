# 0007 — Floor sizing: a minimum floor, sized as a range with a break-even retention rate
Status: Accepted · Date: 2026-10-24 · Supersedes [0004](0004-floor-sizing-assumptions.md)

## Context
ADR 0004 assumed the winning bid is the advertiser's true value. Two facts from the data broke that:
1. The iPinYou README says the campaigns bid "with a fixed relatively high-price bidding strategy". Bids are 277 or 294 fen CPM almost everywhere, far above typical prices (median paid ~67). Using them as valuations would say "raise floors, nobody leaves", which is false for real advertisers.
2. About 35% of impressions have a floor of 0, so "multiply the current floor by k" changes nothing for them.

## Options
1. Keep ADR 0004 (bids = values): inflated upside.
2. Invent a demand elasticity: an invented number.
3. Model a **minimum floor X** (new floor = max(current floor, X)), report a lower and upper bound, and the **break-even retention rate**: the share of affected impressions that must still sell at X for revenue to stay flat.

## Decision
Option 3.

For each impression, with price paid p:
- p ≥ X: nothing changes, revenue p.
- p < X: "at risk". It either still sells at price X (probability r), or is lost.
- Revenue(X, r) = Σ p over not-at-risk + r × X × (number at risk).
- Break-even r* = (revenue currently earned by at-risk impressions) / (X × number at risk).

## Why
- Uses only observed prices; the one unknown (r) is named, not hidden.
- Leadership gets a usable sentence: "a minimum floor of X pays off only if at least r* of affected impressions still sell". The Excel model lets them type their own r.
- It points to the right next step: an A/B test on floors measures r directly.

## Consequences
- The upper bound (r = 1) is an upper bound, never presented as the forecast.
- Ignores long-run effects (advertisers cutting budgets); stated in the memo.
- Check M1 in TESTING.md: at X = 0 the model equals actual revenue for every r.
