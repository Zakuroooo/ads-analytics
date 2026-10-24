# 0005 — Win rate and CPA as labelled stand-ins for fill rate and ROAS
Status: Accepted · Date: 2026-10-24

## Context
The JD's KPI list includes fill rate and ROAS. Fill rate needs ad requests that got no ad; ROAS needs order value. No dataset here has either.

## Options
1. Estimate them anyway (e.g. assume an order value): invents a number.
2. Drop them silently: the interviewer will notice the gap.
3. Show the closest metric the data supports, labelled as a stand-in, and explain the gap.

## Decision
Option 3. Win rate (won impressions / bids) in place of fill rate; CPA (cost / conversion) in place of ROAS. Both marked "stand-in" in the dashboard, METRICS.md and memo.

## Why
- Honest, and it shows I know exactly what each metric needs.
- An interviewer asking "what's your fill rate?" gets a better answer: "this data can't give it because…, here is what I'd need."

## Consequences
- METRICS.md defines fill rate and ROAS fully (formula, data needed), so the definitions are ready for real data.
