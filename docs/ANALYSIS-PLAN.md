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
