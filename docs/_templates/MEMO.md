# Memo: three moves for the ads P&L

**To:** Head of Ads · **From:** Pranay Sarkar · **Data:** public ad data (iPinYou auction logs, {first_day} to {last_day}; Criteo campaign and test data). Not Swiggy data.

## Objective
Find where ad revenue can grow without hurting advertisers or users, and say what to do next.

## What I assumed
- Auction logs from a 2013 ad exchange behave like a marketplace's own ad slots: advertisers bid, the highest bid wins, the winner pays the second price or the floor.
- Criteo's {campaigns} campaigns stand in for our advertisers. Their cost unit is transformed, so I compare campaigns with each other, never in currency.
- The minimum-floor model keeps today's bids fixed. The one thing nobody knows is how many at-risk impressions still sell at a higher floor, so I show the break-even point instead of guessing.

## What I found
1. **Revenue moves with volume, not price.** {revenue} CNY from {impressions} impressions. CPM stayed between {cpm_min} and {cpm_max} CNY every day, while daily revenue swung with how many campaigns were live (peak {peak_revenue} CNY on {peak_day}). One category, {top_adv_category}, brings {top_adv_share} of revenue: a concentration risk.
2. **Competition is thin.** Where a floor exists, it set the price on {floor_binding} of impressions (no rival bid came close). Exchange {no_floor_exchange} sells {no_floor_share} of all impressions with no floor at all.
3. **A minimum floor is a bet on retention, not a free win.** At a minimum floor of 30 fen per 1,000 impressions, {x30_at_risk} of impressions are at risk. Revenue ranges from {x30_lower} (none still sell) to {x30_upper} (all still sell), and it only pays off if at least **{x30_breakeven}** still sell. Across floor levels the break-even sits between {breakeven_min} and {breakeven_max}.
4. **A big advertiser group is overpaying and pulling back.** The top 20% of campaigns hold {top20_share} of spend. The "fix" group ({fix_n} campaigns, {fix_share} of spend) pays **{fix_cpa_ratio}** as much per conversion as the "protect" group, and its week-4 spend is {fix_retention} of week 1. The "grow" group converts {grow_cpa_vs_protect} cheaper than "protect" on just {grow_share} of spend.
5. **Ads do lift conversion.** In a randomised test on {ab_users} users, conversion rose from {conv_c} to {conv_t}: **{conv_rel}** (95% CI {conv_rel_lo} to {conv_rel_hi}). Visits rose {visit_rel}, so the guardrail held. Pre-registered decision: {decision}.

## Recommendation
1. **Fix before we price.** Give the {fix_n} "fix" advertisers targeting and bid help first. They are {fix_share} of spend and already shrinking; losing them costs more than any floor change earns.
2. **Test, don't roll out, a minimum floor.** Run a floor A/B test on the exchange with no floors. Ship only if the share of at-risk impressions that still sell clears the break-even ({x30_breakeven} at 30 fen).
3. **Pitch budget to the "grow" group.** {grow_n} efficient advertisers spend only {grow_share} of the total. More of their budget raises revenue without raising prices.

## Limits
Fill rate and ROAS can't be computed from public data (no unfilled requests, no order values); I used win rate and cost per conversion instead. iPinYou totals after Oct 21 are lower bounds. The A/B data pools several tests, so a single-campaign holdout should confirm the effect.
