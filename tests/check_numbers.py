"""Tie-out checks (docs/TESTING.md). The same number computed two ways must match.

Run: python tests/check_numbers.py   -> prints PASS/FAIL per check, exits 1 if any fail.
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs"
results = []


def check(code, name, ok, detail=""):
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {code:3s} {name}" + (f"  ({detail})" if detail else ""))


def close(a, b, tol=1e-6):
    return abs(float(a) - float(b)) <= tol * max(1.0, abs(float(b)))


def rows(name):
    with open(OUT / f"{name}.csv") as f:
        return list(csv.DictReader(f))


def total(rs, col):
    return sum(float(r[col]) for r in rs if r[col] not in ("", None))


n = json.loads((OUT / "numbers.json").read_text())
k = n["ipinyou_kpi"]

# S1: daily rows add up to the overall totals computed separately in export_numbers.py
daily = rows("kpi_daily")
for col, key in [("bids", "bids"), ("impressions", "impressions"), ("clicks", "clicks"),
                 ("conversions", "conversions"), ("bids_won", "bids_won")]:
    check("S1", f"daily {col} sum = overall", close(total(daily, col), k[key]), f"{total(daily, col):,.0f} vs {k[key]:,.0f}")
# spend is rounded to 2 decimals per day, so allow 1 fen per day of rounding
check("S1", "daily spend sum = overall", abs(total(daily, "spend_cny") - k["spend_cny"]) <= 0.01 * len(daily),
      f"{total(daily, 'spend_cny'):,.2f} vs {k['spend_cny']:,.2f}")

# S2: advertisers add up to the overall totals
adv = rows("kpi_advertiser")
check("S2", "advertiser impressions sum = overall", close(total(adv, "impressions"), k["impressions"]))
check("S2", "advertiser spend sum = overall", abs(total(adv, "spend_cny") - k["spend_cny"]) <= 0.01 * len(adv))
check("S2", "advertiser spend shares sum to 1", abs(total(adv, "spend_share") - 1) < 1e-3)

# S3: ratios in numbers.json recomputed from raw counts
check("S3", "CPM = spend*1000/imps", close(k["cpm_cny"], k["spend_cny"] * 1000 / k["impressions"], 1e-9))
check("S3", "CTR = clicks/imps", close(k["ctr"], k["clicks"] / k["impressions"], 1e-9))
check("S3", "win rate = won/bids", close(k["win_rate"], k["bids_won"] / k["bids"], 1e-9))

# Auction totals tie to the KPI layer (two different queries)
auc = n["auction"]["ALL"]
check("S2", "auction-health impressions = KPI impressions", close(auc["impressions"], k["impressions"]))
check("S2", "auction-health spend = KPI spend", abs(float(auc["spend_cny"]) - k["spend_cny"]) <= 0.01)

# M1: floor sizing at minimum floor 0 reproduces actual revenue, for every exchange
sizing = rows("floor_sizing")
zero = [r for r in sizing if r["min_floor_fen_cpm"] == "0"]
check("M1", "sizing at X=0: lower = upper = actual (all exchanges)",
      all(r["revenue_lower_cny"] == r["revenue_upper_cny"] == r["revenue_now_cny"] for r in zero),
      f"{len(zero)} rows")
check("M1", "sizing actual revenue = KPI spend",
      abs(float(next(r for r in zero if r["exchange"] == "ALL")["revenue_now_cny"]) - k["spend_cny"]) <= 0.01)

# M2: as the minimum floor rises, impressions at risk never fall and the lower bound never rises
for ex in sorted({r["exchange"] for r in sizing}):
    s = [r for r in sizing if r["exchange"] == ex]
    risk = [int(r["at_risk_imps"]) for r in s]
    low = [float(r["revenue_lower_cny"]) for r in s]
    check("M2", f"sizing monotonic ({ex})", risk == sorted(risk) and low == sorted(low, reverse=True))

# S4: segments partition the campaigns exactly
seg = [r for r in rows("segment_summary") if r["segment"] != "ALL"]
co = n["criteo_overall"]
check("S4", "segment campaigns sum = all campaigns", total(seg, "campaigns") == co["campaigns"], f"{total(seg, 'campaigns'):.0f}")
check("S4", "segment spend shares sum to 1", abs(total(seg, "spend_share") - 1) < 1e-3)
check("S4", "segment conversions sum = Criteo total", total(seg, "conversions") == co["conversions"])
camp = rows("campaign_segments")
check("S4", "campaign list spend = Criteo total", abs(total(camp, "spend") - co["spend"]) < 1e-2)
check("S4", "last cumulative spend share = 1", abs(float(camp[-1]["cumulative_spend_share"]) - 1) < 1e-4)

# M3: A/B maths matches statsmodels
if "ab" in n:
    for m in ("primary_conversion", "secondary_visit"):
        check("M3", f"A/B {m} matches statsmodels", n["ab"][m]["check_statsmodels"]["matches"])

print(f"\n{sum(results)}/{len(results)} checks passed")
sys.exit(0 if all(results) else 1)
