# LEARN — start here

This folder teaches you **everything** about this project, from zero. Simple English, many small
examples, and a Hinglish line when something is hard. Every example uses the project's **real
outputs** (filled in as each phase finishes) — so what you learn is exactly what you'll say in the interview.

## How to read it

- Read in order. Each chapter is 10–20 minutes.
- Every chapter ends with **Check yourself** questions. Answer out loud (good English practice), then open the answers.
- When a chapter points to a file (e.g. `sql/01_kpi_daily.sql`), open it side by side.

## Chapters

| # | Chapter | You will be able to… |
|---|---|---|
| 01 | The ads business in a delivery app | explain how a food app earns from ads (restaurant pays to show on top) |
| 02 | Ad metrics, one by one | compute impressions, CTR, CPM, CVR, CPA, ROAS, fill rate, win rate by hand |
| 03 | Auctions: bids, floor price, price paid | explain a second-price auction with 3 bidders, and why floor price matters |
| 04 | Our three datasets | say what each column means, where data came from, and its limits |
| 05 | SQL from zero (with our tables) | read and write SELECT, WHERE, GROUP BY, JOIN, CTE, window functions |
| 06 | DuckDB and Parquet | explain why we didn't use Excel/pandas for 30M rows |
| 07 | The KPI layer | walk through the daily KPI query line by line |
| 08 | Auction health + floor-price sizing | explain the sizing model and its assumptions |
| 09 | Advertiser segments and retention | explain who to grow and who to fix, and why |
| 10 | A/B testing from zero | explain lift, confidence interval, p-value, power, MDE, sample-ratio check |
| 11 | Excel: SUMIFS, XLOOKUP, pivot, the sizing model | rebuild one formula live in an interview |
| 12 | How this was built with Claude Code | explain plan → CLAUDE.md → commands → hooks → checks |
| 13 | Interview questions + answers | answer 30+ likely questions with real numbers |
| 14 | Guesstimates for ads roles | size "how much could a new ad format earn?" step by step, out loud |
| 15 | Presenting to leadership | deliver the 2-minute walkthrough and the 5 slides in simple spoken English |

Practice material lives in `practice/` (SQL set with expected outputs, guesstimate drills).

## The one-minute story (learn this first)

> "I wanted to understand how an ads team in a delivery marketplace thinks. Swiggy data isn't public,
> so I used real public ad data — 2013 auction logs from iPinYou and Criteo's campaign and A/B test data.
> I built the KPI layer in SQL, checked auction health and sized a floor-price change, segmented 675
> campaigns, read out a real randomised test of 13.9 million users, and put it into an Excel model and
> a live dashboard with a one-page memo."

(Numbers like revenue gain and lift get added here once the analysis runs.)
