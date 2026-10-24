<!-- Generated from LEARN/_templates/11-excel-model.md by analysis/render_docs.py. Edit the template, not this file. -->
# 11 · Excel: SUMIFS, XLOOKUP and the floor model
*20 minutes. Open `excel/ads_kpi_model.xlsx` (or upload it to Google Sheets) while reading.*

## Why an Excel model at all?
The JD asks for "advanced Excel or Google Sheets". Leaders like to change an assumption and see the answer move.
SQL does the heavy lifting; Excel is where people play with it.

## The sheets
| Sheet | What it shows | Key formulas |
|---|---|---|
| README | what's inside, units, caveats | none |
| KPI_Summary | totals and ratios + per-advertiser table | SUM, XLOOKUP, INDEX/MATCH |
| Segments | pivot-style summary of 675 campaigns | COUNTIFS, SUMIFS |
| Campaign_Lookup | type a campaign id, see its numbers | XLOOKUP, MEDIAN, IFERROR |
| Floor_Model | pick exchange, floor, retention → revenue | SUMIFS with 2 conditions, data validation dropdowns |
| AB_Test | the whole readout as formulas | SQRT, NORM.S.INV, NORM.S.DIST, IF/AND |
| Daily, Advertisers, Campaigns, FloorData | data exported from SQL | values |

Yellow cells are inputs. Everything else is a formula.

## SUMIFS: "add up where conditions are true"
```
=SUMIFS(sum_range, criteria_range1, criteria1, criteria_range2, criteria2, ...)
```
**Toy:** sheet with Segment in column O and Spend in column F.
`=SUMIFS(F:F, O:O, "FIX")` → total spend of FIX campaigns.

Real (Segments sheet, row FIX): `=SUMIFS(Campaigns!$F$2:$F$676, Campaigns!$O$2:$O$676, A6)`.
Result: the FIX group's spend, 44% of the total.

COUNTIFS works the same way but counts rows:
`=COUNTIFS(segment_range, "FIX", retention_range, "<0.5")` = FIX campaigns whose spend halved.

Hinglish: *SUMIFS = sirf woh rows jodo jo saari shartein poori karein.*

## XLOOKUP: "find this, return that"
```
=XLOOKUP(lookup_value, lookup_array, return_array, "if not found")
```
**Toy:** `=XLOOKUP(2821, A:A, B:B, "not found")` → finds 2821 in column A, returns the matching value from column B ("Footwear").

Real (Campaign_Lookup): `=XLOOKUP($B$3, Campaigns!$A$2:$A$676, Campaigns!$O$2:$O$676, "no such campaign")`
→ type any campaign id in B3, get its segment.

Older equivalent you should also know: `=INDEX(B:B, MATCH(2821, A:A, 0))`. MATCH finds the row number, INDEX returns
the value in that row. Used for "Best day by spend" on KPI_Summary.

## The floor model (Floor_Model sheet)
Inputs: Exchange (dropdown), Minimum floor X (dropdown 0–150), Retention r (0–100%).

```
Revenue today     = SUMIFS(FloorData revenue_now, exchange = B4, floor = B5)
Revenue at your r = safe revenue + r × X × sellable at-risk impressions ÷ 100,000
Break-even r      = (revenue today − safe revenue) ÷ (X × sellable at-risk ÷ 100,000)
```
There's also a sensitivity grid: rows = floor X, columns = r (0, 25, 50, 75, 100%), each cell = revenue change.
That's what leaders love: they see at a glance where it turns positive.

## The A/B sheet
The same maths as chapter 10, as formulas:
- `=NORM.S.INV(1 - alpha/2)` → 1.96
- `=SQRT(pT*(1-pT)/nT + pC*(1-pC)/nC)` → standard error
- `=2*(1-NORM.S.DIST(ABS(z), TRUE))` → p-value
- `=IF(AND(CI_low>0, guardrail_low>=0), "SHIP", ...)` → the pre-registered decision

## How I know the Excel file is right
Python can write formulas but can't calculate them. So `tests/check_excel.py` uses a formula engine to recalculate the
whole workbook and compares 21 key cells with the SQL results. All match.

## Google Sheets
Upload the .xlsx to Google Drive → Open with Google Sheets. All functions used (SUMIFS, COUNTIFS, XLOOKUP, INDEX/MATCH,
NORM.S.INV, NORM.S.DIST) exist in Sheets. No macros, no Excel-only pivot objects. (Do this once yourself before the interview.)

## Live-interview drill
Be ready to type, from memory:
1. `=SUMIFS(...)` for total spend of one segment
2. `=XLOOKUP(...)` to fetch a campaign's CPA
3. `=C6/E6` style ratio, and explain why it's a ratio of totals

## Check yourself
1. Write a formula for the number of GROW campaigns.
2. What's the difference between SUMIFS and COUNTIFS?
3. Write the INDEX/MATCH version of an XLOOKUP.
4. In the floor model, what happens to the answer when you raise r?

<details><summary>Answers</summary>

1. `=COUNTIFS(Campaigns!$O$2:$O$676, "GROW")`
2. SUMIFS adds a column's values for matching rows; COUNTIFS counts matching rows.
3. `=INDEX(return_range, MATCH(lookup_value, lookup_range, 0))`
4. Revenue at your scenario goes up (more at-risk impressions still sell at the higher price); the break-even itself doesn't change.
</details>
