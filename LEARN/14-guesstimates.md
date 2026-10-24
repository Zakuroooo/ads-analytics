<!-- Generated from LEARN/_templates/14-guesstimates.md by analysis/render_docs.py. Edit the template, not this file. -->
# 14 · Guesstimates for ads roles
*15 minutes to read, then practise the 3 drills in `practice/guesstimates.md` with a timer.*

## What the interviewer is testing
Not the final number. They want to see: a clear formula, sensible assumptions said out loud, and a sanity check.

## The routine (memorise)
1. **Clarify:** what exactly, which city or country, which time period?
2. **Formula first:** say it before any number.
3. **Assume:** one number per box, with a one-line reason.
4. **Multiply:** round numbers, convert units slowly.
5. **Sanity check:** compare with something you know; question your own inputs.

Hinglish: *Pehle formula bolo, phir numbers. Interviewer ko soch dikhni chahiye, sirf jawab nahi.*

## The ads formula you'll use most
```
Ad revenue = sessions × ad slots seen per session × CTR × CPC
           = impressions × CPM ÷ 1,000            (if sold per 1,000 views)
```
This is exactly the chain in my KPI layer (chapter 7).

## The break-even trick (from my floor model)
For any price change:
```
Revenue stays flat when (1 − share of buyers lost) × (1 + price change) = 1
```
A 10% price rise breaks even if you lose about 9.1% of buyers (1 − 1/1.10). Say: "So the real question is
whether we'd lose more or less than 9%. I'd test it." That's the same logic as my 51% floor break-even.

## Units (where people slip)
- 1 lakh = 100,000 · 1 million = 10 lakh · 1 crore = 100 lakh = 10 million
- Per mille = per 1,000 (CPM)
- I slipped once while writing a drill (₹4.8 million is ₹48 lakh, not ₹4.8 crore). Say the units out loud as you go.

## Three drills (worked in `practice/guesstimates.md`)
1. Monthly revenue of sponsored listings in one city.
2. A new banner on the order-tracking screen: incremental revenue + guardrails.
3. Raising minimum CPC by 10%: break-even and who leaves first.

## Check yourself
1. What are the 5 steps?
2. Write the impressions-to-revenue formula for CPM-priced ads.
3. A 20% price rise: what share of buyers can you lose and still break even?

<details><summary>Answers</summary>

1. Clarify, formula, assume, multiply, sanity check.
2. Revenue = impressions × CPM ÷ 1,000.
3. 1 − 1/1.20 ≈ 16.7%.
</details>
