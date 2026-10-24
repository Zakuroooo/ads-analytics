# 0004 — Floor sizing: bids stay fixed, lost impressions stay unsold
Status: Accepted · Date: 2026-10-24

## Context
I want to size "what if we raise floor (reserve) prices by k×?". The log shows, for each won impression, the floor f, iPinYou's bid b and the price paid p. It does not show other bidders' bids, or how bidders would react.

## Options
1. Assume bids stay the same; an impression whose bid falls below the new floor is lost and stays unsold.
2. Same, but assume a lost impression is resold at the old price (optimistic).
3. Model bidder reaction with an elasticity guess (adds an invented number).

## Decision
Option 1 as the base case. Option 2 shown as the optimistic bound. No invented elasticity.

## Why
- Option 1 uses only observed numbers, and it's conservative: real other bidders could still buy some lost impressions.
- Base vs optimistic gives leadership a range, not false precision.
- Sanity check built in: at k = 1.0 the model must equal actual revenue exactly.

## Consequences
- New price for a kept impression = max(p, f × k) (second-price logic: the floor can only raise the price).
- Ignores long-run effects (advertisers leaving because prices rose); stated as a limit and as the reason to A/B test any floor change before rollout.
