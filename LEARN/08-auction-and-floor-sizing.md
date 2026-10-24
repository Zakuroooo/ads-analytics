<!-- Generated from LEARN/_templates/08-auction-and-floor-sizing.md by analysis/render_docs.py. Edit the template, not this file. -->
# 08 · Auction health and floor-price sizing
*20 minutes. This is the "opportunity sizing for a pricing change" part of the JD. Read chapter 3 first.*

## Part A: auction health (`sql/03_auction_health.sql`)
**Question:** is the price set by real competition, or by the floor?

Key metric, **floor-binding rate** = among impressions that have a floor, the share where price paid ≤ floor.

Real results:
- Overall: **37%** of floored impressions paid just the floor.
- Exchange 3: 46%. Exchange 2: 31%. Mobile inventory: 50%.
- Exchange 1 had **no floors at all**, and it carries 25% of all impressions.
- Only 65% of impressions had any floor.

**What it means:** a lot of slots have weak competition. Where nobody bids above the floor, the floor *is* the price.
That makes floors a pricing lever, so the next question is: what if we raise them?

## Part B: sizing a minimum floor (`sql/04_floor_sizing.sql`, ADR 0007)

**The change:** new floor = the higher of (today's floor, X). X goes from 0 to 150 fen per 1,000 impressions.

For every impression we know the price it paid (p):
- **p ≥ X** → nothing changes. Revenue stays p.
- **p < X** → it's **at risk**. Either a buyer still pays X (revenue goes up to X), or nobody does (revenue 0).

We don't know how many at-risk impressions still sell. Call that share **r** (retention).

```
Revenue(X, r) = revenue from safe impressions + r × X × (at-risk impressions that could pay X)
```

**Toy:** 4 impressions paid 10, 20, 60, 80. Today's revenue = 170. Set X = 50.
- Safe (≥ 50): 60 + 80 = 140.
- At risk: the 10 and the 20, earning 30 today.
- If r = 1 (both still sell at 50): 140 + 2 × 50 = 240 (+41%).
- If r = 0 (both lost): 140 (−18%).
- **Break-even r** = 30 / (2 × 50) = **30%**. If at least 30% still sell, the floor pays off.

Hinglish: *Floor badhane se kuch slots mehenge bikenge, kuch bikenge hi nahi. Break-even batata hai kitne bikne chahiye taaki nuksaan na ho.*

## The real answer
At a minimum floor of **30 fen**:
- 24.7% of impressions are at risk
- Revenue range: **−4.2%** (none still sell) to **+4.1%** (all still sell); at r = 50%: −0.1%
- **Break-even: 51%** of at-risk impressions must still sell

At **50 fen**: 39% at risk, range −10.1% to +11.7%, break-even 46%.

Across all floor levels the break-even sits between 36% and 54%.

## Why I didn't give one number
Any single forecast would need me to invent r. Instead the answer is: "this pays off only if at least
51% still sell. We can measure that with an A/B test on floors." That's what a good analyst says.

## The mistake I fixed (tell this story, it's a strength)
My first model (ADR 0004) assumed that if iPinYou's bid was above the new floor, it would still buy. But the README
said its bids were a fixed high price, not real value. So the first model would have said "raise floors, nobody leaves",
which is false. I replaced it with the break-even model, which uses only prices actually paid.

## Built-in sanity checks
- At X = 0 the model must equal today's revenue exactly (it does, for every exchange).
- As X rises, at-risk impressions can only go up and the worst case can only go down (checked).

## Check yourself
1. What does a floor-binding rate of 37% tell the ads team?
2. In the toy, what is revenue at X = 50 and r = 50%?
3. What does break-even retention mean, in one sentence?
4. Why is a range + break-even better than one forecast here?
5. What would you do next?

<details><summary>Answers</summary>

1. On many floored slots no rival bid beat the floor; competition is thin, so floors matter for price.
2. 140 + 0.5 × 2 × 50 = 190.
3. The share of at-risk impressions that must still sell at the higher floor for revenue to stay the same.
4. The key input (how buyers react) is unknown; a single number would hide an invented assumption.
5. Run an A/B test on floors (e.g. on the exchange with no floors), measure the share that still sells, and compare it with the break-even.
</details>
