# ANALYSIS PLAN — questions, hypotheses, method
*Written before running the queries. Each result later gets a ✅ (supported), ❌ (not supported) or ➖ (can't tell), with the number from `numbers.json`.*

| # | Question | Hypothesis (my guess before looking) | Method | Data |
|---|---|---|---|---|
| Q1 | How do revenue, CPM, CTR move day to day? | weekday/weekend pattern; one advertiser drives most revenue | `sql/01–02` | iPinYou |
| Q2 | Is price set by competition or the floor? | a large share of impressions pay close to the floor → floor matters | floor binding rate = share with pay ≤ floor × 1.05; bid/pay ratio | iPinYou |
| Q3 | Where is the auction weak? | win rate and CPM differ a lot by exchange and slot visibility | group by exchange, visibility, format | iPinYou |
| Q4 | What would raising floors earn? | a modest raise (≤ 1.3×) increases revenue; big raises lose volume faster than price gains | `sql/04`, k = 1.0 → 2.0 step 0.1 | iPinYou |
| Q5 | How concentrated is spend? | top 20% of campaigns ≈ 80% of spend | Pareto curve, share of top decile | Criteo Attr. |
| Q6 | Who to grow, who to fix? | a group with high spend and high CPA exists (fix); low spend, low CPA (grow) | spend tier × CPA vs median → 4 quadrants | Criteo Attr. |
| Q7 | Do campaigns keep spending? | week-over-week retention drops after week 1 | cohort = first active week; active = cost > 0 | Criteo Attr. |
| Q8 | Did the ad treatment work? | small positive lift in visits and conversions | EXPERIMENT.md | Criteo Uplift |

## Opportunity-sizing template (used for Q4 and the guesstimate drills)
```
Impact = base volume × share affected × change per unit × (1 − cannibalisation)
State every assumption, its source, and a low/base/high range.
```

## What I won't claim
Causal effects from non-randomised data (Q1–Q7 are descriptive). Only Q8 is causal.

## Results (2026-10-24)
*Numbers live in [MEMO.md](MEMO.md) and `outputs/numbers.json`; this table only records whether my guess held.*

| # | Verdict | What happened |
|---|---|---|
| Q1 | ➖ | One category does lead revenue (MEMO finding 1). No weekday pattern can be judged from 10 days with advertisers starting and stopping. Revenue followed volume; CPM barely moved. |
| Q2 | ✅ | The floor set the price on a large share of floored impressions (MEMO finding 2). |
| Q3 | ✅ | Win rate, CPM and floor binding differ a lot by exchange; one exchange has no floors (`outputs/auction_health.csv`). |
| Q4 | ➖ | My guess was too simple. Whether a floor raise earns money depends entirely on how many at-risk impressions still sell; the model gives a break-even instead of a yes/no (ADR 0007). |
| Q5 | ✅ | Close to the 80/20 guess (MEMO finding 4). |
| Q6 | ✅ | A large, expensive "fix" group exists, and a small efficient "grow" group (MEMO finding 4). |
| Q7 | ❌ → changed | Churn can't be measured: Criteo's sample keeps almost every campaign active all 31 days. Replaced with spend retention (week 4 / week 1). |
| Q8 | ✅ (bigger than guessed) | Positive and far above the MDE (MEMO finding 5), with caveats in EXPERIMENT.md §8. |
