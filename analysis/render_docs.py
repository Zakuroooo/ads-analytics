"""Render docs from templates so no number in them is typed by hand (ADR 0006).

Templates live in docs/_templates/*.md and use {name} placeholders. This script builds every value
from outputs/numbers.json (and the output CSVs), formats it, and writes the finished file:
  docs/_templates/README.md -> README.md, every other template -> docs/<same name>.
Run: python analysis/render_docs.py        (tests/check_docs.py checks the files are up to date)
"""
import csv
import json
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs"
TEMPLATES = ROOT / "docs" / "_templates"


def read(name):
    with open(OUT / f"{name}.csv") as f:
        return list(csv.DictReader(f))


def half_up(v, d):
    """Round halves up (0.965 -> 0.97), the same way the dashboard's JavaScript formats numbers."""
    return Decimal(repr(float(v))).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP)


def pct(v, d=0):
    return f"{half_up(float(v) * 100, d)}%"


def signed_pct(v, d=0):
    v = float(v) * 100
    return f"{'+' if v >= 0 else '−'}{half_up(abs(v), d)}%"


def compact(v):
    v = float(v)
    return f"{v / 1e6:.2f}M" if v >= 1e6 else f"{v / 1e3:.1f}K" if v >= 1e3 else f"{v:,.0f}"


def values():
    n = json.loads((OUT / "numbers.json").read_text())
    k, ab, seg = n["ipinyou_kpi"], n["ab"], n["segments"]
    auction = n["auction"]
    sizing = {int(r["min_floor_fen_cpm"]): r for r in n["floor_sizing_all"]}
    daily = [r for r in read("kpi_daily") if r["spend_cny"]]
    peak = max(daily, key=lambda r: float(r["spend_cny"]))
    cpms = [float(r["cpm_cny"]) for r in daily]
    adv = n["ipinyou_advertisers"]
    top_adv = max(adv, key=lambda r: float(r["spend_share"]))
    no_floor = next(e for e, r in auction.items() if e != "ALL" and float(r["share_with_floor"]) == 0)
    breakevens = [float(r["breakeven_retention"]) for x, r in sizing.items() if x > 0]
    conv, visit = ab["primary_conversion"], ab["secondary_visit"]
    s30, s50 = sizing[30], sizing[50]

    return {
        # iPinYou P&L
        "bids": f"{k['bids']:,}", "impressions": compact(k["impressions"]), "impressions_full": f"{k['impressions']:,}",
        "revenue": f"{k['spend_cny']:,.0f}", "cpm": f"{k['cpm_cny']:.2f}", "ctr": pct(k["ctr"], 3),
        "win_rate": pct(k["win_rate"]), "first_day": k["first_day"], "last_day": k["last_day"],
        "peak_day": peak["day"], "peak_revenue": f"{float(peak['spend_cny']):,.0f}",
        "cpm_min": str(half_up(min(cpms), 2)), "cpm_max": str(half_up(max(cpms), 2)),
        "top_adv_category": top_adv["category"].lower(), "top_adv_share": pct(top_adv["spend_share"]),
        "clicks": f"{k['clicks']:,}",
        # auction
        "floor_binding": pct(auction["ALL"]["floor_binding_rate"]),
        "share_with_floor": pct(auction["ALL"]["share_with_floor"]),
        "no_floor_exchange": no_floor,
        "no_floor_share": pct(float(auction[no_floor]["impressions"]) / k["impressions"]),
        "ex3_binding": pct(auction["3"]["floor_binding_rate"]), "ex3_win": pct(auction["3"]["win_rate"]),
        "mobile_binding": pct(auction["mobile/unknown"]["floor_binding_rate"]),
        # floor sizing
        "x30_at_risk": pct(s30["share_at_risk"], 1), "x30_upper": signed_pct(s30["upper_change"], 1),
        "x30_lower": signed_pct(float(s30["revenue_lower_cny"]) / float(s30["revenue_now_cny"]) - 1, 1),
        "x30_breakeven": pct(s30["breakeven_retention"]),
        "x30_r50": signed_pct(float(s30["revenue_r50_cny"]) / float(s30["revenue_now_cny"]) - 1, 1),
        "x50_at_risk": pct(s50["share_at_risk"]), "x50_upper": signed_pct(s50["upper_change"], 1),
        "x50_breakeven": pct(s50["breakeven_retention"]),
        "x50_r50": signed_pct(float(s50["revenue_r50_cny"]) / float(s50["revenue_now_cny"]) - 1, 1),
        "breakeven_min": pct(min(breakevens)), "breakeven_max": pct(max(breakevens)),
        # Criteo advertisers
        "criteo_impressions": compact(n["criteo_overall"]["impressions"]), "campaigns": n["criteo_overall"]["campaigns"],
        "top20_share": pct(n["criteo_concentration"]["top20pct_spend_share"]),
        "top10_share": pct(n["criteo_concentration"]["top10pct_spend_share"]),
        "fix_n": seg["FIX"]["campaigns"], "fix_share": pct(seg["FIX"]["spend_share"]),
        "fix_cpa_ratio": f"{float(seg['FIX']['cpa']) / float(seg['PROTECT']['cpa']):.1f}×",
        "fix_retention": pct(seg["FIX"]["spend_retention_w4_vs_w1"]), "fix_halved": seg["FIX"]["campaigns_spend_halved"],
        "protect_n": seg["PROTECT"]["campaigns"], "protect_share": pct(seg["PROTECT"]["spend_share"]),
        "protect_retention": pct(seg["PROTECT"]["spend_retention_w4_vs_w1"]),
        "grow_n": seg["GROW"]["campaigns"], "grow_share": pct(seg["GROW"]["spend_share"]),
        "grow_cpa_vs_protect": pct(1 - float(seg["GROW"]["cpa"]) / float(seg["PROTECT"]["cpa"])),
        "watch_n": seg["WATCH"]["campaigns"],
        "halved_all": seg["ALL"]["campaigns_spend_halved"],
        # A/B
        "ab_users": compact(ab["counts"]["T"]["users"] + ab["counts"]["C"]["users"]),
        "ab_users_full": f"{ab['counts']['T']['users'] + ab['counts']['C']['users']:,}",
        "conv_c": pct(conv["rate_control"], 3), "conv_t": pct(conv["rate_treatment"], 3),
        "conv_abs": f"{conv['abs_lift'] * 100:.3f} pp",
        "conv_abs_lo": f"{conv['abs_ci95'][0] * 100:.3f}", "conv_abs_hi": f"{conv['abs_ci95'][1] * 100:.3f}",
        "conv_rel": signed_pct(conv["rel_lift"]), "conv_rel_lo": signed_pct(conv["rel_ci95"][0]),
        "conv_rel_hi": signed_pct(conv["rel_ci95"][1]),
        "visit_c": pct(visit["rate_control"], 2), "visit_t": pct(visit["rate_treatment"], 2),
        "visit_rel": signed_pct(visit["rel_lift"]),
        "mde_conv": signed_pct(ab["mde_conversion"]["rel"], 1),
        "exposure": pct(ab["effect_on_exposed"]["exposure_rate_treatment"], 1),
        "srm_share": pct(ab["srm"]["observed_treatment_share"], 4),
        "decision": ab["decision"].upper(),
        # extra detail used by the LEARN chapters
        "users_t": f"{ab['counts']['T']['users']:,}", "users_c": f"{ab['counts']['C']['users']:,}",
        "conv_n_t": f"{ab['counts']['T']['conversions']:,}", "conv_n_c": f"{ab['counts']['C']['conversions']:,}",
        "visit_n_t": f"{ab['counts']['T']['visits']:,}", "visit_n_c": f"{ab['counts']['C']['visits']:,}",
        "srm_p": f"{ab['srm']['p_value']:.2f}", "mde_visit": signed_pct(ab["mde_visit"]["rel"], 1),
        "conv_p": f"{conv['p_value']:.1e}",
        "fix_cpa": f"{float(seg['FIX']['cpa']):.4f}", "protect_cpa": f"{float(seg['PROTECT']['cpa']):.4f}",
        "grow_cpa": f"{float(seg['GROW']['cpa']):.4f}", "watch_cpa": f"{float(seg['WATCH']['cpa']):.4f}",
        "spend_cny_exact": f"{k['spend_cny']:,.2f}", "bids_won": f"{k['bids_won']:,}",
        "ex1_win": pct(auction["1"]["win_rate"]), "ex4_win": pct(auction["4"]["win_rate"]),
        "ex2_binding": pct(auction["2"]["floor_binding_rate"]),
        "x50_lower": signed_pct(float(s50["revenue_lower_cny"]) / float(s50["revenue_now_cny"]) - 1, 1),
        "adv_rows": "\n".join(f"| {a['category']} | {a['advertiser_id']} | {float(a['spend_cny']):,.0f} | {pct(a['spend_share'])} | {float(a['cpm_cny']):.2f} | {pct(a['ctr'], 3)} | {pct(a['win_rate'])} |" for a in adv),
        "daily_rows": "\n".join(f"| {r['day']} | {int(r['impressions']):,} | {float(r['spend_cny']):,.2f} | {float(r['cpm_cny']):.2f} | {pct(r['win_rate'])} |" for r in daily),
    }


LEARN_TEMPLATES = ROOT / "LEARN" / "_templates"


def render():
    v = values()
    out = {}
    for t in sorted(TEMPLATES.glob("*.md")) + sorted(LEARN_TEMPLATES.glob("*.md")):
        if t.parent == LEARN_TEMPLATES:
            target = ROOT / "LEARN" / t.name
        else:
            target = ROOT / "README.md" if t.name == "README.md" else ROOT / "docs" / t.name
        header = f"<!-- Generated from {t.relative_to(ROOT)} by analysis/render_docs.py. Edit the template, not this file. -->\n"
        out[target] = header + t.read_text().format_map(v)
    return out


if __name__ == "__main__":
    files = render()
    for path, text in files.items():
        path.write_text(text)
        print(f"rendered {path.relative_to(ROOT)}")
    sys.exit(0)
