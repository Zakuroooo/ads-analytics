# RUNBOOK — rebuild, refresh, deploy
*Skeleton now; commands are confirmed as each phase lands. ⏳ = not yet tested.*

## 1. Rebuild from scratch
```bash
git clone https://github.com/Zakuroooo/ads-analytics && cd ads-analytics
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/download_data.py     # Kaggle token in ~/.kaggle; ~1.9 GB download, ~6 GB peak disk
python scripts/to_parquet.py        # streamed; deletes raw files after row-count check
python run_all.py                   # SQL → numbers.json → Excel → dashboard → checks
```
Expected time on an M2 8 GB: ⏳ (measured in P1–P2).

## 2. Refresh after changing a query
`python run_all.py` → check output → commit query + regenerated outputs (not data).

## 3. Excel → Google Sheets ⏳
Google Drive → New → File upload → `excel/ads_kpi_model.xlsx` → right-click → Open with Google Sheets.
Then check: `KPI_Summary!B7` (total revenue) equals `ipinyou_kpi.spend_cny` in `outputs/numbers.json`, and `AB_Test!B32` shows SHIP. Not yet done (needs a Google account).

## 4. Deploy the dashboard ✅
Vercel project `slotwise-ads` (team zakuroooo's projects), linked to GitHub `Zakuroooo/ads-analytics`, root directory `dashboard/`,
no framework, no build command. **Every push to `main` redeploys automatically.**
Live: https://slotwise-ads.vercel.app (public). The team-scoped aliases are behind Vercel login; share only the URL above.
After changing data: `python run_all.py` → commit `dashboard/` + `outputs/` → push.

## 5. Troubleshooting
| Symptom | Fix |
|---|---|
| DuckDB "out of memory" | lower `memory_limit`, check `temp_directory` has disk space, run one job at a time |
| Kaggle 401 | token expired: new one from kaggle.com → Settings → API |
| bz2 decode slow | expected (single-threaded); run in background, one file at a time |
