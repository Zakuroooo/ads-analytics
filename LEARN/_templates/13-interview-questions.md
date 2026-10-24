# 13 · Interview questions and answers
*Practise out loud. Short answers first; add detail only if they ask. Each answer uses the project's real numbers.*

## About the project
**1. Walk me through this project.**
Use the one-minute story in `00-START-HERE.md`. End with the recommendation: fix the expensive advertisers, test a floor, grow the efficient ones.

**2. Is this Swiggy data?**
No. It's public ad data: iPinYou auction logs and Criteo's campaign and test data. I analysed it the way a delivery app's ads team would.

**3. Why these datasets?**
iPinYou is the only public log I found with floor price, bid and price paid together, which auction health needs. Criteo Uplift is a real randomised test. Criteo Attribution has {campaigns} campaigns for advertiser analysis.

**4. What was the hardest part?**
Data problems, not code. Win rate halved mid-week because iPinYou had cut its test set out of the logs. I found it by checking row counts against the README and added the public part back.

**5. What would you do differently with real Swiggy data?**
Compute fill rate and ROAS properly (needs request logs and order values), run the floor A/B test, and build the KPI report on the warehouse with the same metric definitions.

## Metrics
**6. Define CTR, CPM, CPC, CPA, ROAS.** See chapter 2. Our CTR {ctr}, CPM {cpm} CNY.

**7. Why didn't you report fill rate?**
It needs ad requests that got no ad, and the logs don't have them. I showed win rate, labelled as a stand-in.

**8. Why is averaging daily CTRs wrong?**
Small days count as much as big days. Use total clicks / total impressions.

**9. What is win rate here and how is it different from fill rate?**
Win rate = auctions iPinYou won / auctions it bid on ({win_rate}). Fill rate is the seller's view: slots filled / slots available.

**10. Revenue rose but CPM didn't. What does that mean?**
Growth came from volume (more impressions), not price. In our data CPM stayed between {cpm_min} and {cpm_max} CNY.

## Auction and pricing
**11. Explain a second-price auction.** Highest bid wins, pays the second-highest bid or the floor, whichever is higher.

**12. What does a floor-binding rate of {floor_binding} mean?**
On those floored impressions no rival bid beat the floor, so the floor set the price. Competition is thin.

**13. Should we raise floor prices?**
"It depends on how many affected impressions still sell. At a 30-fen floor, it pays off only if at least {x30_breakeven} do. I'd A/B test it rather than roll it out."

**14. Why not give a single revenue forecast?**
The key input (buyer reaction) is unknown. A single number would hide an invented assumption. A range plus break-even is honest and decision-ready.

**15. What was wrong with your first floor model?**
It treated iPinYou's bids as true value, but the README says bids were fixed and high. I replaced it with a model that uses only prices paid.

## Advertisers
**16. How did you segment advertisers?**
Two median cuts: spend and cost per conversion. Four groups: protect, fix, grow, watch.

**17. Which group matters most?**
FIX: {fix_share} of spend, {fix_cpa_ratio} the cost per conversion of PROTECT, spend already at {fix_retention} of week 1.

**18. Why not measure churn?**
Criteo's sample keeps almost every campaign active all month. I measured spend retention (week 4 / week 1) instead.

**19. How concentrated is spend?** Top 20% of campaigns = {top20_share} of spend.

## A/B testing
**20. What was the result?**
Conversion {conv_c} → {conv_t}, relative lift {conv_rel}, 95% CI {conv_rel_lo} to {conv_rel_hi}. Decision: {decision}.

**21. A {conv_rel} lift sounds huge. Is it believable?** *(Expect this one.)*
"It's large, and I treat it carefully. The data pools several Criteo tests, so I'd confirm it with a single-campaign holdout before
rolling anything out. The randomised comparison itself is solid: the CI is far above zero and the maths was independently re-checked."

**22. What is a p-value?** If there were no real effect, the chance of seeing a result at least this extreme.

**23. What is a confidence interval?** The range the true effect is very likely in; ours excludes zero.

**24. What is MDE?** Smallest effect the test could reliably detect. Ours was {mde_conv}, far below the observed lift.

**25. What is SRM?** Sample-ratio mismatch: group sizes far from the plan. Ours: {srm_share} vs 85% intended, fine.

**26. What guardrail did you use?** Visit rate must not fall. It rose {visit_rel}.

**27. Why did you write the decision rule before seeing results?** So I couldn't bend the rule to fit the result.

**28. What's the "effect on exposed users" and why didn't you use it?**
Only {exposure} of treatment users actually saw an ad. Dividing the lift by that gives an implausibly big effect, which suggests exposure isn't recorded cleanly. I report it, but the decision rests on the randomised comparison.

## SQL and tools
**29. Why DuckDB?** 30M rows on an 8 GB laptop: Excel can't hold it, pandas would run out of memory. DuckDB reads Parquet column by column.

**30. LEFT JOIN vs JOIN?** LEFT JOIN keeps every row from the left even without a match. Needed for win rate (lost bids have no impression).

**31. What's a window function? Give an example from your project.**
A calculation across rows that keeps every row. `sum(spend) OVER (ORDER BY spend_rank)` for the running share of spend.

**32. How do you know your numbers are right?**
Each number is computed two ways and must match: 29 tie-out checks, the Excel file recalculated and compared, and an independent re-check of the A/B maths.

**33. Which Excel functions did you use?** SUMIFS, COUNTIFS, XLOOKUP, INDEX/MATCH, NORM.S.INV, NORM.S.DIST, data-validation dropdowns.

## Behavioural (from the project)
**34. Tell me about a time you were wrong.** The floor-model story (Q15). Say what you assumed, what showed you were wrong, and what you changed.

**35. Tell me about communicating to leadership.** The 1-page memo: objective, assumptions, findings, recommendation. Three moves, each tied to a number.
