# DECISIONS — what I chose, what I dropped, and why
*First person, short. The technical "why X over Y" lives in [adr/](adr/README.md); this is the plain list.*

| Date | I decided | Instead of | Because |
|---|---|---|---|
| 10-24 | Use real public ad data | making up Swiggy-like data | every number has to survive "where did this come from?" |
| 10-24 | iPinYou season 3 | season 2 | same fields, a third of the download |
| 10-24 | Show win rate and CPA, labelled as stand-ins | inventing fill rate and ROAS | the data has no unfilled requests and no order value |
| 10-24 | No ₹ on charts | ₹/K/M formatting | the data is 2013 Chinese prices and scaled Criteo units |
| 10-24 | Write the A/B design before the readout | deciding the rule after seeing results | so I can't fool myself |
| 10-24 | Static dashboard | Tableau / Streamlit | instant, free, phone-friendly, my own design |
| 10-24 | Minimum-floor model with a break-even | trusting iPinYou's bids | the README says bids were fixed and high, so they aren't real values (ADR 0007) |
| 10-24 | Add iPinYou's public test impressions back | using training logs only | the training logs had the test set cut out, which halved win rate |
| 10-24 | Spend retention (week 4 / week 1) | campaign churn cohorts | Criteo's sample keeps almost every campaign active all month |
| 10-24 | Report the "effect on exposed users" but not use it | quoting it | an independent check showed it's implausibly large |
| 10-24 | Render README/memo/story from templates | typing numbers into docs | a script fills every number from numbers.json, and a check fails if a % is typed by hand |

## Dropped
- Campaign churn cohorts (data can't show churn).
- Exploratory A/B lift by feature quartile (time; not needed for the decision).
- Weekday/weekend analysis (10 days with advertisers starting and stopping can't support it).
