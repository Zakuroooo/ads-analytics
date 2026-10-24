<!-- Generated from docs/_templates/MEMO.md by analysis/render_docs.py. Edit the template, not this file. -->
# Memo: three moves for the ads P&L

**To:** Head of Ads · **From:** Pranay Sarkar · **Data:** public ad data (iPinYou auction logs, 2013-10-19 to 2013-10-28; Criteo campaign and test data). Not Swiggy data.

## Objective
Find where ad revenue can grow without hurting advertisers or users, and say what to do next.

## What I assumed
- Auction logs from a 2013 ad exchange behave like a marketplace's own ad slots: advertisers bid, the highest bid wins, the winner pays the second price or the floor.
- Criteo's 675 campaigns stand in for our advertisers. Their cost unit is transformed, so I compare campaigns with each other, never in currency.
- The minimum-floor model keeps today's bids fixed. The one thing nobody knows is how many at-risk impressions still sell at a higher floor, so I show the break-even point instead of guessing.

## What I found
1. **Revenue moves with volume, not price.** 4,254 CNY from 4.72M impressions. CPM stayed between 0.72 and 0.97 CNY every day, while daily revenue swung with how many campaigns were live (peak 762 CNY on 2013-10-21). One category, footwear, brings 44% of revenue: a concentration risk.
2. **Competition is thin.** Where a floor exists, it set the price on 37% of impressions (no rival bid came close). Exchange 1 sells 25% of all impressions with no floor at all.
3. **A minimum floor is a bet on retention, not a free win.** At a minimum floor of 30 fen per 1,000 impressions, 24.7% of impressions are at risk. Revenue ranges from −4.2% (none still sell) to +4.1% (all still sell), and it only pays off if at least **51%** still sell. Across floor levels the break-even sits between 36% and 54%.
4. **A big advertiser group is overpaying and pulling back.** The top 20% of campaigns hold 73% of spend. The "fix" group (195 campaigns, 44% of spend) pays **4.7×** as much per conversion as the "protect" group, and its week-4 spend is 97% of week 1. The "grow" group converts 31% cheaper than "protect" on just 4% of spend.
5. **Ads do lift conversion.** In a randomised test on 13.98M users, conversion rose from 0.194% to 0.309%: **+59%** (95% CI +54% to +65%). Visits rose +27%, so the guardrail held. Pre-registered decision: SHIP.

## Recommendation
1. **Fix before we price.** Give the 195 "fix" advertisers targeting and bid help first. They are 44% of spend and already shrinking; losing them costs more than any floor change earns.
2. **Test, don't roll out, a minimum floor.** Run a floor A/B test on the exchange with no floors. Ship only if the share of at-risk impressions that still sell clears the break-even (51% at 30 fen).
3. **Pitch budget to the "grow" group.** 195 efficient advertisers spend only 4% of the total. More of their budget raises revenue without raising prices.

## Limits
Fill rate and ROAS can't be computed from public data (no unfilled requests, no order values); I used win rate and cost per conversion instead. iPinYou totals after Oct 21 are lower bounds. The A/B data pools several tests, so a single-campaign holdout should confirm the effect.
