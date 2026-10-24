<!-- Generated from docs/_templates/WALKTHROUGH.md by analysis/render_docs.py. Edit the template, not this file. -->
# 2-minute walkthrough (say it out loud)
*Simple sentences. Pause at each line break. About 260 words, so roughly 2 minutes at a calm speed.
Practise with a timer. If you forget a number, say the idea: the idea matters more than the digit.*

---

**Why (15 seconds)**
I wanted to do the real work of an ads analyst, not just say I know SQL.
Swiggy's data isn't public, so I used real public ad data.
Auction logs from iPinYou, and Criteo's campaign data and an A/B test.

**What I built (20 seconds)**
I loaded about 11,457,419 bids and 16.47M campaign impressions into DuckDB.
I wrote the KPI layer in SQL: revenue, CPM, click-through rate, win rate.
Every number feeds one Excel model and a live dashboard, and they all match.

**Finding one: thin competition (25 seconds)**
Where a floor price existed, it set the price 37% of the time.
That means no other bidder came close.
So I sized a minimum floor. The honest answer is: it only pays off
if at least 51% of the affected impressions still sell.
That is a number we should measure with a test, not guess.

**Finding two: advertisers (25 seconds)**
I split 675 campaigns into four groups.
One group pays 4.7× more per conversion and holds 44% of spend.
Their spend is already falling. I would help them first, before changing any price.

**Finding three: the A/B test (20 seconds)**
In a randomised test on 13.98M users, ads raised conversion by +59%.
The confidence interval was +54% to +65%, so it is clearly above zero.
I wrote the decision rule before I looked at the result.

**Close (15 seconds)**
My recommendation: fix the expensive advertisers, test a floor price before rolling it out,
and pitch more budget to the efficient small advertisers.
The main limit: public data has no fill rate or order value, so I used stand-ins and said so.

---

**If they interrupt with "Is this Swiggy data?"** No. It's public data. I say that first, every time.
