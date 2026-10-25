# The story
*The whole project in simple words, in my voice. This is also what I say in interviews.*

> **Where we are (2026-10-24):** everything is built, checked and live: https://slotwise-ads.vercel.app · code: https://github.com/Zakuroooo/ads-analytics.

## 1. Why I built it
I'm applying to the Swiggy Ads team as a business analyst intern. I didn't want to just say "I know SQL
and A/B testing". I wanted to do the real work of an ads analyst, on real data, and be able to show it.

## 2. The problem in one line
Every week an ads team has to know how ads are earning, whether the auction is healthy, what a price
change would earn, which advertisers to grow, and whether an experiment really worked.

## 3. What I did, step by step

```mermaid
flowchart LR
    A[Plan + design docs] --> B[Download 3 public datasets]
    B --> C[Convert to Parquet,<br/>check row counts]
    C --> D[SQL: KPIs, auction,<br/>floor sizing, segments]
    D --> E[A/B readout +<br/>independent re-check]
    E --> F[numbers.json]
    F --> G[Excel model]
    F --> H[Dashboard]
    F --> I[Memo + docs]
```

1. **Plan first.** I wrote the problem, the data plan, the metric definitions and the A/B decision rule before touching data.
2. **Data.** {bids} auction bids and {impressions_full} impressions from iPinYou (2013), {criteo_impressions} impressions across {campaigns} Criteo campaigns, and a randomised test on {ab_users_full} users. Every file's row count was checked.
3. **KPI layer.** Revenue {revenue} CNY, CPM {cpm} CNY, CTR {ctr}, win rate {win_rate}. Daily and per-advertiser totals add up to the overall totals exactly.
4. **Auction health.** Where a floor exists it decided the price {floor_binding} of the time. One exchange had no floors at all.
5. **Floor sizing.** A minimum floor of 30 fen only pays off if at least {x30_breakeven} of at-risk impressions still sell.
6. **Advertisers.** Four groups by spend and cost per conversion. The "fix" group pays {fix_cpa_ratio} more per conversion on {fix_share} of spend.
7. **A/B readout.** Conversion {conv_rel} (95% CI {conv_rel_lo} to {conv_rel_hi}), decision {decision}, checked by an independent re-derivation.

## 4. Five ideas I must be able to explain
1. **CPM** = revenue for 1,000 impressions. Ours: {cpm} CNY.
2. **Floor price** = the lowest price the seller accepts. In a second-price auction, if no rival bids above the floor, the floor *is* the price.
3. **Break-even retention** = the share of at-risk impressions that must still sell for a higher floor to pay off. It turns an unknown into a clear test target.
4. **Confidence interval** = the range the true lift probably sits in. Ours, {conv_rel_lo} to {conv_rel_hi}, is far from zero, so the lift is real.
5. **Ratio of totals, not average of ratios.** Overall CTR = total clicks / total impressions. Averaging daily CTRs gives the wrong answer when days differ in size.

## 5. Mistakes and what they taught
- **Trusting the bids.** My first floor model treated iPinYou's bids as advertiser value. The README said the bids were fixed and high. I replaced the model with a break-even version. Lesson: read the data's documentation before modelling.
- **Missing impressions.** Win rate roughly halved halfway through the logs. It wasn't the market; iPinYou had removed its test set. Lesson: when a metric jumps, suspect the data first.
- **An effect that was too good.** The "effect on exposed users" came out implausibly big. An independent re-check flagged it, so I kept it out of the decision. Lesson: get a second pair of eyes on the riskiest maths.
