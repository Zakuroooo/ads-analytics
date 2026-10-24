# LEARN — start here

This folder teaches you **everything** about this project, from zero. Simple English, many small
examples, and a Hinglish line when something is hard. The real numbers in these chapters are filled in
from the project's outputs by a script, so what you learn is exactly what you'll say in the interview.
(Small "toy" examples with 3 or 4 made-up rows are marked **toy**.)

## How to read it

- Read in order. Each chapter is 10–20 minutes.
- Every chapter ends with **Check yourself** questions. Answer out loud first (good English practice), then open the answers.
- When a chapter points to a file (e.g. `sql/01_kpi_daily.sql`), open it side by side.
- Live dashboard: https://slotwise-ads.vercel.app · Code: https://github.com/Zakuroooo/ads-analytics

## Chapters

| # | Chapter | You will be able to… |
|---|---|---|
| [01](01-ads-business.md) | The ads business in a delivery app | explain how a food app earns from ads |
| [02](02-ad-metrics.md) | Ad metrics, one by one | compute impressions, CTR, CPM, CVR, CPA, ROAS, fill rate, win rate by hand |
| [03](03-auctions.md) | Auctions: bids, floor price, price paid | explain a second-price auction with 3 bidders, and why the floor matters |
| [04](04-datasets.md) | Our three datasets | say where the data came from, what each column means, and its limits |
| [05](05-sql-from-zero.md) | SQL from zero | read and write SELECT, WHERE, GROUP BY, JOIN, CTE, window functions |
| [06](06-duckdb-parquet.md) | DuckDB and Parquet | explain why we didn't use Excel or pandas for 30M rows |
| [07](07-kpi-layer.md) | The KPI layer | walk through the daily KPI query line by line |
| [08](08-auction-and-floor-sizing.md) | Auction health + floor-price sizing | explain the sizing model and its break-even |
| [09](09-advertiser-segments.md) | Advertiser segments and spend retention | explain who to grow and who to fix, and why |
| [10](10-ab-testing.md) | A/B testing from zero | explain lift, confidence interval, p-value, power, MDE, sample-ratio check |
| [11](11-excel-model.md) | Excel: SUMIFS, XLOOKUP, the floor model | rebuild one formula live in an interview |
| [12](12-how-this-was-built-with-claude-code.md) | How this was built with Claude Code | explain plan → rules → commands → hooks → checks |
| [13](13-interview-questions.md) | Interview questions + answers | answer 30+ likely questions with real numbers |
| [14](14-guesstimates.md) | Guesstimates for ads roles | size "how much could a new ad format earn?" out loud |
| [15](15-presenting-to-leadership.md) | Presenting to leadership | deliver the 2-minute walkthrough and the 5 slides |

Practice material lives in [`../practice/`](../practice/): the SQL set with real outputs, and guesstimate drills.

## The one-minute story (learn this first)

> "I wanted to understand how an ads team in a delivery marketplace thinks. Swiggy's data isn't public,
> so I used real public ad data: auction logs from iPinYou and Criteo's campaign and A/B test data.
> I built the KPI layer in SQL on {bids} bids. I found the floor price set the price on {floor_binding}
> of floored auctions, and showed a higher floor only pays off if at least {x30_breakeven} of the affected
> impressions still sell. I split {campaigns} campaigns into groups and found one with {fix_share} of spend
> paying {fix_cpa_ratio} more per conversion. And I read out a randomised test on {ab_users} users:
> conversion went up {conv_rel}. It all feeds one Excel model and a live dashboard."

Practise it until you can say it in one minute without reading.
