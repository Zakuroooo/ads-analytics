# The story
*The whole project in simple words, in my voice. Updated when each phase ends. This is also what I say in interviews.*

> **Where we are (2026-10-24):** plan and design docs done. No data downloaded yet. Numbers appear here only after the build produces them.

## 1. Why I built it
I'm applying to the Swiggy Ads team as a business analyst intern. I didn't want to just say "I know SQL
and A/B testing". I wanted to do the actual work an ads analyst does, on real data, and be able to show it.

## 2. The problem in one line
An ads team has to know, every week, how ads are earning, whether the auction is healthy, what a price
change would earn, which advertisers to grow, and whether an experiment really worked.

## 3. What I did (filled in as phases finish)
1. KPI layer: _⏳_
2. Auction health: _⏳_
3. Floor-price sizing: _⏳_
4. Advertisers: _⏳_
5. A/B readout: _⏳_

## 4. The 2-minute version (draft, numbers added later)
> "Swiggy's ad data isn't public, so I used real public ad data: auction logs from iPinYou, and Criteo's
> campaign data and a randomised test on 13.9 million users. I wrote the KPI layer in SQL on DuckDB,
> checked whether prices were set by competition or by the floor price, and sized what a floor-price
> change would earn, with the assumptions written down. I split 675 campaigns into grow and fix groups,
> and read out the A/B test with confidence intervals and a decision rule I wrote before looking at the
> results. It all feeds one Excel model and a live dashboard, and every number reconciles."

## 5. Mistakes and what they taught
_Added as they happen._
