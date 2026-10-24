# 0003 — Static HTML dashboard, not Tableau / Power BI / Streamlit
Status: Accepted · Date: 2026-10-24

## Context
Leadership needs a link they can open on a phone. It must stay up for free, and it must read the same numbers as the Excel file and memo.

## Options
1. Tableau Public / Power BI: standard BA tools, but the free tiers publish raw data publicly and are slow to restyle.
2. Streamlit: easy, but needs a running Python server (free hosts sleep, cold starts of 30 s+).
3. Looker Studio over Google Sheets: free, but tied to Sheets, limited design.
4. Static HTML + one JSON file + a small chart library, on Vercel.

## Decision
Static HTML reading `numbers.json` and small CSVs, deployed on Vercel.

## Why
- Opens instantly, free forever, works on a phone, no server to sleep.
- Full control of design (DESIGN.md), so it doesn't look like a default template.
- Reads the same `numbers.json` as everything else (ADR 0006).

## Consequences
- No drag-and-drop filtering like a BI tool; I pre-compute the cuts leadership needs.
- If asked "do you know Tableau/Power BI?" the honest answer: the Excel/Sheets model covers pivoting; I chose static HTML here for the reasons above.
