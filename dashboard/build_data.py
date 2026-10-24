"""Write dashboard/data.json for the static dashboard, using only outputs/ (ADR 0006).
The page renders every number from this file; nothing is typed into the HTML.
"""
import csv
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs"


def read(name):
    with open(OUT / f"{name}.csv") as f:
        return list(csv.DictReader(f))


def f(v):
    return None if v in ("", None) else float(v)


n = json.loads((OUT / "numbers.json").read_text())
ab = n["ab"]

data = {
    "kpi": n["ipinyou_kpi"],
    "daily": [{"day": r["day"], "spend": f(r["spend_cny"]), "cpm": f(r["cpm_cny"]), "win_rate": f(r["win_rate"]),
               "impressions": f(r["impressions"]), "ctr": f(r["ctr"])} for r in read("kpi_daily")],
    "advertisers": [{"id": r["advertiser_id"], "category": r["category"], "spend": f(r["spend_cny"]),
                     "share": f(r["spend_share"]), "cpm": f(r["cpm_cny"]), "ctr": f(r["ctr"]),
                     "win_rate": f(r["win_rate"])} for r in read("kpi_advertiser")],
    "auction": [{"exchange": r["exchange"], "impressions": f(r["impressions"]), "cpm": f(r["cpm_cny"]),
                 "share_with_floor": f(r["share_with_floor"]), "floor_binding": f(r["floor_binding_rate"]),
                 "win_rate": f(r["win_rate"])}
                for r in read("auction_health") if r["slot_visibility"] == "ALL"],
    "floor": [{"exchange": r["exchange"], "x": int(r["min_floor_fen_cpm"]), "now": f(r["revenue_now_cny"]),
               "lower": f(r["revenue_lower_cny"]), "can_sell": f(r["can_sell_at_x"]),
               "at_risk_share": f(r["share_at_risk"]), "breakeven": f(r["breakeven_retention"])}
              for r in read("floor_sizing")],
    "campaigns": [{"id": r["campaign"], "spend": f(r["spend"]), "cpa": f(r["cpa"]), "segment": r["segment"],
                   "retention": f(r["spend_retention_w4_vs_w1"])} for r in read("campaign_segments")],
    "segments": n["segments"],
    "concentration": n["criteo_concentration"],
    "criteo": n["criteo_overall"],
    "ab": {
        "users": ab["counts"]["T"]["users"] + ab["counts"]["C"]["users"],
        "treatment_share": ab["srm"]["observed_treatment_share"], "srm_p": ab["srm"]["p_value"],
        "conversion": {k: ab["primary_conversion"][k] for k in ("rate_treatment", "rate_control", "abs_lift", "abs_ci95", "rel_lift", "rel_ci95", "p_value")},
        "visit": {k: ab["secondary_visit"][k] for k in ("rate_treatment", "rate_control", "abs_lift", "abs_ci95", "rel_lift", "rel_ci95", "p_value")},
        "mde_conversion_rel": ab["mde_conversion"]["rel"], "mde_visit_rel": ab["mde_visit"]["rel"],
        "exposure_rate": ab["effect_on_exposed"]["exposure_rate_treatment"],
        "decision": ab["decision"],
    },
}
payload = json.dumps(data, separators=(",", ":"))
(ROOT / "dashboard" / "data.json").write_text(payload)
# data.js lets the page load its data with a plain <script> tag, so it also works opened from disk
(ROOT / "dashboard" / "data.js").write_text("window.DASHBOARD_DATA = " + payload + ";\n")
# the page offers the Excel model as a download
shutil.copy(ROOT / "excel" / "ads_kpi_model.xlsx", ROOT / "dashboard" / "ads_kpi_model.xlsx")
print(f"wrote dashboard/data.json + data.js ({len(data['campaigns'])} campaigns, {len(data['floor'])} sizing rows)")
