# Ads Analytics — End-to-End Plan

**One line:** ads analytics for a delivery marketplace, built on public ad data — KPI reporting,
auction health, advertiser segments, an A/B test readout and a pricing (floor-price) sizing model.

**Why:** Swiggy Ads Business Analyst Intern application. Deadline to apply: **26 Oct 2026**.
**Honest framing:** this is NOT Swiggy data and has no real Swiggy users. It is real public ad data
(2013 Chinese ad exchange + Criteo), analysed the way a marketplace ads team would.

---

## 0. What "done" looks like (the finish line)

| # | Deliverable | Proves which JD line |
|---|---|---|
| 1 | `sql/` — DuckDB queries over the full datasets (millions of rows) | "Strong SQL on large datasets" |
| 2 | KPI layer: revenue, impressions, CPM, CTR, CVR, CPA, win rate, advertiser count — daily + per advertiser | "Recurring KPI reporting for the ads P&L" |
| 3 | Auction health: bid vs price paid, floor binding rate, win rate by exchange/slot | "Auction health, inventory utilisation" |
| 4 | Floor-price sizing model with stated assumptions | "Opportunity sizing for pricing changes" |
| 5 | Advertiser/campaign segments + retention cohorts (675 campaigns) | "Advertiser insights: spend, ROI, retention, grow or fix" |
| 6 | A/B readout on a real randomised test (13.9M users): lift, CI, p-value, power, guardrails | "A/B test design and readouts" |
| 7 | `excel/ads_kpi_model.xlsx` — live SUMIFS/XLOOKUP formulas, pivot-style summary, editable sizing inputs; imports cleanly into **Google Sheets** (tested, steps in README) | "Advanced Excel or Google Sheets" |
| 8 | Live dashboard (static HTML on Vercel), hand-designed — see section 4b | KPI reporting, communication |
| 9 | `docs/METRICS.md` (metric definitions), `docs/MEMO.md` (1-page leadership memo, first person) | "Maintained metric definitions", "communicate to senior stakeholders" |
| 10 | `docs/DECISIONS.md` — what I chose, why, what I dropped; README "What didn't work / limits" | Judgement, honesty |
| 11 | `docs/READOUT.pptx` — 5 slides (objective → assumptions → findings → recommendation → next steps), opens in Google Slides, + `docs/WALKTHROUGH.md` 2-minute spoken script | "Interpret for leadership", spoken communication |
| 12 | `practice/` — SQL practice set on his own tables (JOIN, GROUP BY/HAVING, CASE, CTE, ROW_NUMBER, LAG, running total), each with expected output; 3 ads guesstimate drills with worked answers | BA interview rounds |
| 13 | `LEARN/` — full teaching course on this project, in simple English | So Pranay can explain every line |
| 14 | 4 resume bullets + GitHub + live links | Hand-back to the Resume chat |

**Rule for every number:** it comes from a script output in `outputs/numbers.json`. No number is typed by
hand into the memo, dashboard, Excel or bullets. If the data changes, one command rebuilds all of them.

---

## 1. Data (real, public, cited)

| Dataset | What it has | Size | Used for | Licence |
|---|---|---|---|---|
| **iPinYou RTB, season 3** (Oct 19–28, 2013) | every bid: floor price, bid price, price paid, ad exchange, slot size; impressions, clicks, conversions; 4 advertisers | ~880 MB (bz2) | ads P&L KPIs, auction health, floor sizing | released for research (Zhang et al. 2014) — exact terms checked from its README |
| **Criteo Attribution** | 16.5M impressions, 675 campaigns, 30 days, cost, click, conversion, cost-per-order | ~670 MB zip | advertiser segments, retention, CPA | CC BY-NC-SA 4.0 (Criteo AI Lab) — verify |
| **Criteo Uplift v2.1** | 13.9M users, random treatment/control, visit, conversion, exposure | ~340 MB zip | A/B test readout | CC BY-NC-SA 4.0 (Criteo AI Lab) — verify |

**What the data cannot do (said openly in README + memo):**
- **Fill rate** — needs unfilled ad requests; no public log has them → shown as "not computable", win rate used instead.
- **ROAS** — needs order value; none of the datasets has it → CPA (cost per conversion) used instead.
- iPinYou has only 4 advertisers → advertiser *segmentation* uses Criteo's 675 campaigns.
- Prices are 2013 Chinese CPM units (iPinYou) and scaled cost units (Criteo) — not rupees.

**Mac limits (M2, 8 GB RAM):** never load the raw files into pandas. Convert each file once to Parquet
(streamed), let DuckDB query Parquet with `memory_limit = '3GB'`, run one heavy job at a time,
delete raw downloads after conversion. `data/` is never committed.

---

## 2. Phases (in order, each ends with a check)

| Phase | Work | Check before moving on | Time |
|---|---|---|---|
| **P0 Setup** | git init, `.gitignore`, Python venv (duckdb, pandas, scipy, openpyxl, kaggle), CLAUDE.md, slash commands, hook | `git status` shows no data/secrets; hook blocks a test bad commit | 30 min |
| **P1 Data** | download → convert to Parquet → row counts → delete raw | row counts match published counts (13,979,592 uplift; 16,468,027 attribution) | 1.5 h |
| **P2 KPI layer** | `sql/01_kpi_daily.sql`, `02_kpi_advertiser.sql` | totals tie out: sum of daily = overall; CTR = clicks/imps recomputed in Python | 1.5 h |
| **P3 Auction + sizing** | `03_auction_health.sql`, `04_floor_sizing.sql` | sizing at today's floor = today's revenue exactly (sanity check) | 1.5 h |
| **P4 Advertisers** | `05_segments.sql`, `06_retention.sql` (Criteo) | segment shares add to 100%; cohort week-0 = 100% | 1 h |
| **P5 A/B readout** | `analysis/ab_readout.py` | sample-ratio check passes; CI method cross-checked with scipy; a fresh reviewer agent re-derives the stats | 1.5 h |
| **P6 Excel + Sheets** | `excel/build_xlsx.py` → `.xlsx` (only functions Sheets supports: SUMIFS, XLOOKUP, IFERROR, INDEX/MATCH; no macros, no Excel pivot objects, no Power Query) | open in Excel: formulas recalc; change a sizing input → output changes; upload to Google Sheets → same totals | 1.25 h |
| **P7 Dashboard** | `dashboard/index.html` from `numbers.json`, design rules in 4b | browser: no console errors, phone width OK, light + dark sections readable, screenshot | 2 h |
| **P8 Docs** | METRICS.md, MEMO.md, DECISIONS.md, README.md (first person, plain English) | every number in docs matches `numbers.json` (script check) | 1.25 h |
| **P9 Readout** | 5-slide READOUT.pptx + 2-minute WALKTHROUGH.md | opens in Google Slides; script read aloud in ≤ 2 min | 1 h |
| **P10 Ship** | ask Pranay → GitHub repo (public) → push → Vercel deploy | live link opens; README links work | 30 min |
| **P11 Hand-back** | 4 resume bullets with real numbers + links → Resume chat | bullets ≤ ~110 chars, 1–3 bold phrases, numbers in `numbers.json` | 15 min |
| **P12 Practice** | `practice/sql_practice.md` (+ answers run against his tables), `practice/guesstimates.md` | every expected output produced by actually running the query | 1.5 h |
| **P13 LEARN** | chapters written from real outputs (can finish after 26 Oct) | each chapter ends with check questions + answers | 3–4 h |

**Cut order if time runs short (agreed):** ship first = A/B readout, Excel model, dashboard, memo
(+ the SQL/KPI work they depend on). Then: slides + walkthrough, practice set. Retention cohorts are the
first analysis to drop. LEARN chapters can finish after he applies on 26 Oct.

**One command rebuilds everything:** `python run_all.py` → SQL → numbers.json → Excel → dashboard → docs check.

---

## 3. Folder layout

```
ads-analytics/
├── README.md, CONTRIBUTING.md
├── docs/                   ← full doc set; map in docs/00-README.md (this file = docs/BUILD-PLAN.md)
├── run_all.py              ← one command, whole pipeline
├── data/                   ← Parquet files (git-ignored)
├── sql/                    ← 01..06 numbered queries, each with plain-English comments
├── analysis/               ← ab_readout.py, sizing.py, export_numbers.py
├── outputs/numbers.json    ← single source of truth for every number
├── excel/                  ← build_xlsx.py + ads_kpi_model.xlsx
├── dashboard/index.html    ← static, deployable to Vercel
│   (after build: MEMO.md, READOUT.pptx, WALKTHROUGH.md)
├── practice/               ← sql_practice.md (with expected outputs), guesstimates.md
├── LEARN/                  ← the teaching course (see LEARN/00-START-HERE.md)
├── CLAUDE.md, .claude/     ← Claude Code setup (git-ignored, never committed)
└── tests/check_numbers.py  ← ties out totals, checks docs vs numbers.json
```

---

## 4. How this is built like a pro Claude Code user

You will learn these in `LEARN/12-how-this-was-built-with-claude-code.md`. The point: an expert doesn't
just "ask the AI to build it" — they set up rules, checks and repeatable commands, so the AI's work
can be trusted and re-run.

| Pro habit | What we do here | Why it matters |
|---|---|---|
| **Plan before code** | this PLAN.md, approved by you before any download | cheap to change a plan, costly to change code |
| **Project memory (`CLAUDE.md`)** | rules every session reads: no fake numbers, no Swiggy claims, 8 GB RAM limits, commit rules | a new session behaves the same without re-explaining |
| **Custom slash commands** (`.claude/commands/`) | `/rebuild` (run whole pipeline), `/check` (tie-out tests), `/explain <file>` (teach a file in simple English) | repeat work becomes one word |
| **Hooks** (`.claude/settings.json`) | before any `git commit`: block data files, secrets, `Co-Authored-By` lines | rules enforced by code, not memory |
| **Single source of truth** | all numbers flow from `outputs/numbers.json` | no number can drift between memo, Excel and resume |
| **Verify, don't trust** | each phase has a check (table above); dashboard checked in a browser | AI can be confidently wrong; checks catch it |
| **Independent review (subagent)** | a fresh agent re-derives the A/B statistics without seeing my answer | a second pair of eyes on the riskiest maths |
| **Small commits** | one commit per finished step, plain messages | easy to see history, easy to undo |
| **Context hygiene** | heavy downloads run in background; big outputs saved to files, not pasted into chat | keeps the session fast and focused |

---

## 4b. Design and voice (so it doesn't look AI-generated)

**Dashboard**
- Own brand name and colours (working name picked in P7). **No Swiggy logo, no Swiggy orange**, nothing that reads as an official Swiggy page.
- Dark premium base with inverted light sections, strong type (one display font + one text font from Google Fonts), clear hierarchy: the headline number first, then the chart that explains it.
- Subtle scroll motion only (fade/rise on enter, respects `prefers-reduced-motion`).
- Avoid: default Tailwind/shadcn card grids, purple gradients, glassmorphism, emoji.
- Charts: one consistent palette across all charts, labelled axes with units, numbers as K/M.
- **Currency: no ₹ sign.** The data is not in rupees (iPinYou = Chinese fen per 1,000 impressions in 2013; Criteo = scaled cost units). Putting ₹ on it would be a false claim an interviewer can catch. Each chart labels its real unit; the memo can convert to an illustrative ₹ figure only where it says "illustrative, assumes X".

**Writing (README, MEMO, DECISIONS)**
- First person ("I chose…", "I dropped…"), plain English, short sentences.
- No buzzwords ("leverage", "synergy", "data-driven insights", "actionable"), no em-dash-heavy prose.
- README has a **"What didn't work / limits"** section: fill rate and ROAS not computable, 4-advertiser limit, 2013 prices, anything that failed during the build.

---

## 5. Risks and what I'll do

| Risk | Plan |
|---|---|
| Time — total is now ~19 h of work for ~1.5 days | follow the cut order in section 2; apply on 26 Oct with what's shipped, never delay the application for LEARN or practice |
| iPinYou bz2 files are slow to decompress | stream `bzcat` → DuckDB → Parquet in background, one file at a time |
| Kaggle download fails | Kaggle CLI with your token; fallback: original Criteo / iPinYou mirrors |
| Interviewer: "Is this Swiggy data?" | No — public data, said in line one of README and memo |
| Interviewer asks about a line you can't explain | LEARN folder + TEACH questions; every SQL file commented in plain English |

---

## 6. Rules (from your instructions)

- Real data only; no made-up numbers, users or metrics.
- Commits: small, plain messages, **no Co-Authored-By / Claude lines**; never commit CLAUDE.md, `.claude/`, data, secrets.
- Ask you before: creating the public GitHub repo, pushing, deploying.
- Resume bullets: no AI-tool names.
