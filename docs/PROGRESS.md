# PROGRESS — the build log
*Every finished step, in order: what I built, how, what went wrong, and how I know it works. Newest at the bottom.*

**Latest:** Step 0, design docs (2026-10-24) · **Next:** P0 setup, after Pranay approves the plan

---

## Step 0 — Plan and design docs (2026-10-24)
**What:** researched public ad datasets on Kaggle; wrote BUILD-PLAN, CLAUDE.md, PRD, DATA, ARCHITECTURE,
METRICS, ANALYSIS-PLAN, EXPERIMENT (pre-registration), DESIGN, TESTING, 6 ADRs.
**Why first:** cheaper to change a plan than code; the A/B design must exist before the results do.
**Decisions:** iPinYou season 3 over season 2 (same fields, ~⅓ the download). No ₹ on charts (data isn't in rupees).
Fill rate and ROAS marked not computable (ADR 0005).
**Verified:** dataset file lists and sizes read from the Kaggle API. Licences and row counts still ⏳ until download.
