# PROGRESS — the build log
*Every finished step, in order: what I built, how, what went wrong, and how I know it works. Newest at the bottom.*

**Latest:** Step 1, setup + data (2026-10-24) · **Next:** P2 KPI layer

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
