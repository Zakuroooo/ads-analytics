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

## Dropped
_Added as the build forces choices (e.g. if retention cohorts get cut for time)._
