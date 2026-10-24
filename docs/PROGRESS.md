# PROGRESS — the build log
*Every finished step, in order: what I built, how, what went wrong, and how I know it works. Newest at the bottom.*

**Latest:** Step 13, LEARN course (2026-10-24) · **Next:** Pranay uploads the Excel file to Google Sheets once; reads LEARN 01–10 before applying

---

## Step 0 — Plan and design docs (2026-10-24)
**What:** researched public ad datasets on Kaggle; wrote BUILD-PLAN, CLAUDE.md, PRD, DATA, ARCHITECTURE,
METRICS, ANALYSIS-PLAN, EXPERIMENT (pre-registration), DESIGN, TESTING, 6 ADRs.
**Why first:** cheaper to change a plan than code; the A/B design must exist before the results do.
**Decisions:** iPinYou season 3 over season 2 (same fields, ~⅓ the download). No ₹ on charts (data isn't in rupees).
Fill rate and ROAS marked not computable (ADR 0005).
**Verified:** dataset file lists and sizes read from the Kaggle API. Licences and row counts still ⏳ until download.

## Step 1 — P0 setup + P1 data (2026-10-24)
**What:** git repo, `.gitignore`, venv (`requirements.txt`, prebuilt wheels only), git hooks
(`scripts/githooks/`: block data/secrets/CLAUDE.md, block attribution lines), local Claude Code setup
(`/rebuild`, `/check`, `/explain` commands; a PreToolUse hook that blocks `--no-verify`).
Downloaded all three datasets with the Kaggle CLI, converted to Parquet (`scripts/to_parquet.py`), deleted raw files. `data/` = 910 MB.

**How I know it works:**
- Hook test: committing `data/t.csv` → `pre-commit: blocked`; `git commit --no-verify` → guard exits 2.
- Every Parquet file's row count = raw line count (39/39 OK). Uplift 13,979,592 and attribution 16,468,027 = published counts.

**What went wrong:**
- First `pip install` started compiling packages from source on Python 3.14 (no wheels for the pinned versions). Killed it, reinstalled with `--only-binary=:all:` and pinned what installed.
- iPinYou win rate dropped from 65% to 11% after Oct 21. Cause: the README says the season-3 test set was cut out of the training logs. Added the leaderboard test impressions back (+1.58M imps). A second "reserved" test part is not public, so Oct 21–28 totals are lower bounds (DATA.md §2b).
- The iPinYou README says bids came from a fixed high-price strategy, so iPinYou's bid isn't a real valuation. ADR 0004 (floor sizing) needs revisiting in P3.

**Facts confirmed from sources:** licences (Criteo CC BY-NC-SA 4.0; iPinYou public release, no explicit licence), price unit (RMB fen per 1,000 imps), second-price auction, season-3 advertiser industries.

## Step 2 — P2 KPI layer (2026-10-24)
`sql/00_views.sql` (tables; `impressions` = training + test imps, deduped), `sql/01_kpi_daily.sql`, `sql/02_kpi_advertiser.sql`,
`analysis/run_sql.py` (runs each query → `outputs/*.csv`), `analysis/export_numbers.py` (→ `outputs/numbers.json`), `tests/check_numbers.py`.
**Checked:** daily and advertiser totals equal overall totals computed separately (S1, S2); ratios recomputed (S3).
**Went wrong:** DuckDB 2.0 removed `fetchone()` on relations and refuses a new query while a result is open; switched to `execute().fetchall()`.
CVR showed 0% for advertisers that never had conversion tracking; now NULL.

## Step 3 — P3 auction health + floor sizing (2026-10-24)
`sql/03_auction_health.sql` (GROUPING SETS by exchange × visibility), `sql/04_floor_sizing.sql` (minimum floor 0–150, per exchange).
**Changed the model:** ADR 0004 → 0007 after reading that iPinYou's bids were fixed; the new model uses prices paid and a break-even retention.
**Checked:** at X = 0 every exchange reproduces actual revenue (M1); monotonic (M2); auction totals = KPI totals.

## Step 4 — P4 advertiser segments (2026-10-24)
`campaigns` view, `sql/05_campaign_segments.sql` (675 rows, running spend share, segment), `sql/06_segment_summary.sql` (ROLLUP).
**Changed the plan:** churn cohorts dropped (98% of campaigns active all month in the sample); spend retention instead.
**Checked:** segments partition all campaigns, spend and conversions exactly (S4).

## Step 5 — P5 A/B readout (2026-10-24)
`analysis/ab_readout.py` following EXPERIMENT.md: SRM, lift, CI, p-value, MDE, CACE, decision rule. Cross-checked with statsmodels (M3).
**Independent review (M4):** a fresh agent re-derived everything from raw counts: all matched to 6 significant figures. It flagged the
CACE as implausible, the pooled-tests risk, and the post-treatment ratio; written into EXPERIMENT.md §8. Decision unchanged: SHIP.

## Step 6 — P6 Excel / Sheets model (2026-10-24)
`excel/build_xlsx.py` → `excel/ads_kpi_model.xlsx`: KPI_Summary (SUM, XLOOKUP, INDEX/MATCH), Segments (COUNTIFS/SUMIFS pivot-style),
Campaign_Lookup (XLOOKUP), Floor_Model (dropdown inputs, sensitivity grid), AB_Test (NORM.S.INV / NORM.S.DIST). Only Sheets-compatible functions.
**Checked:** `tests/check_excel.py` recalculates the workbook with the `formulas` engine: 21/21 cells = numbers.json (X1).
Not yet checked: an actual upload to Google Sheets (needs Pranay's Google account).

## Step 7 — P7 dashboard (2026-10-24)
`dashboard/index.html` + `build_data.py` (→ `data.js`, `data.json`, Excel copy). Hand-written SVG charts, own palette validated for
colour-blind separation; FIX/GROW coloured, other segments grey (4 colours failed the all-pairs check for a scatter).
**Checked:** headless Chrome renders all sections; screenshots at 1440 px and inside a 390 px frame (headless Chrome's minimum window is 500 px,
which first looked like a mobile overflow bug). Fixed: tables widening grid columns (`min-width: 0`), charts now size to their container.

## Step 8 — P8 docs (2026-10-24)
README, MEMO, STORY, WALKTHROUGH rendered from `docs/_templates/` by `analysis/render_docs.py`; `tests/check_docs.py` (X2) fails if a
rendered file was hand-edited or a template has a hand-typed percentage. Updated METRICS, DATA, TESTING, PLAYBOOK, DECISIONS, ANALYSIS-PLAN results.
Rounding: docs use round-half-up so they match the dashboard's JavaScript (24.65% → 24.7% in both).

## Step 9 — P9 slides (2026-10-24)
`analysis/build_readout.py` → `docs/READOUT.pptx` (5 slides, Georgia/Arial so Google Slides renders them). Numbers from the same values as the memo.
Checked: slide 1 rendered with Quick Look; slides 2–5 checked by layout arithmetic only.

## Step 10 — P10 ship (2026-10-24, Pranay approved)
Public repo https://github.com/Zakuroooo/ads-analytics (created with the GitHub connector, pushed over HTTPS).
Vercel project `slotwise-ads`, linked to the repo, root `dashboard/`: https://slotwise-ads.vercel.app (public, 200).
**Went wrong:** in a hidden browser tab the scroll-fade never fired, leaving sections at opacity 0. Fixed: content is visible by default,
animation only after JS confirms it can reveal, plus a 2.5 s fallback. Verified live: no console errors; floor slider recalculates (X=50, exchange 1 → break-even 52%, matches SQL).

## Step 11 — P11 hand-back (2026-10-24)
4 resume bullets + links written to the shared notes folder (`ads-analytics-handover.md`) for the Resume chat.

## Step 12 — P12 practice (2026-10-24)
`practice/build_sql_practice.py` → `practice/sql_practice.md`: 13 exercises on our tables; every expected output comes from running the answer.
`practice/guesstimates.md`: 3 ads drills. **Went wrong:** drill 1 said ₹4.8 crore; re-running the arithmetic showed ₹48 lakh. Fixed, and kept as a teaching note.

## Step 13 — P13 LEARN (2026-10-24)
16 chapters in `LEARN/`, rendered from `LEARN/_templates/` so real numbers match `numbers.json`. Each ends with check questions + answers.
