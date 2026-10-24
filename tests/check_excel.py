"""X1: recalculate every formula in the Excel model and compare key cells with numbers.json.

openpyxl writes formulas but can't calculate them, so the `formulas` package (a Python Excel engine)
recalculates the workbook here. Run: python tests/check_excel.py
"""
import json
import sys
from pathlib import Path

import formulas

ROOT = Path(__file__).resolve().parent.parent
XLSX = ROOT / "excel" / "ads_kpi_model.xlsx"
n = json.loads((ROOT / "outputs" / "numbers.json").read_text())

model = formulas.ExcelModel().loads(str(XLSX)).finish()
solution = model.calculate()


def cell(sheet, ref):
    key = f"'[{XLSX.name}]{sheet.upper()}'!{ref}"
    value = solution[key].value
    return value[0][0] if hasattr(value, "__getitem__") else value


k, ab, seg = n["ipinyou_kpi"], n["ab"], n["segments"]
fix_row = n["floor_sizing_all"][3]   # minimum floor 30, the model's default input
expected = [
    ("KPI_Summary", "B3", k["bids"]), ("KPI_Summary", "B6", k["impressions"]),
    ("KPI_Summary", "B7", k["spend_cny"]), ("KPI_Summary", "B8", k["cpm_cny"]),
    ("KPI_Summary", "B10", k["ctr"]), ("KPI_Summary", "B5", k["win_rate"]),
    ("Segments", "B9", 675), ("Segments", "C6", float(seg["FIX"]["spend"])),
    ("Segments", "G5", float(seg["PROTECT"]["cpa"])), ("Segments", "H6", float(seg["FIX"]["spend_retention_w4_vs_w1"])),
    ("Segments", "B12", n["criteo_concentration"]["top20pct_spend_share"]),
    ("Floor_Model", "B9", float(fix_row["revenue_now_cny"])), ("Floor_Model", "B12", float(fix_row["revenue_lower_cny"])),
    ("Floor_Model", "B13", float(fix_row["revenue_r50_cny"])), ("Floor_Model", "B15", float(fix_row["breakeven_retention"])),
    ("AB_Test", "B15", ab["primary_conversion"]["rate_treatment"]), ("AB_Test", "B17", ab["primary_conversion"]["abs_lift"]),
    ("AB_Test", "B21", ab["primary_conversion"]["abs_ci95"][0]), ("AB_Test", "B22", ab["primary_conversion"]["abs_ci95"][1]),
    ("AB_Test", "B29", ab["mde_conversion"]["abs"]), ("AB_Test", "B32", "SHIP"),
]

ok_all = True
for sheet, ref, want in expected:
    got = cell(sheet, ref)
    if isinstance(want, str):
        ok = got == want
    else:
        # 2-decimal CSV rounding in the floor data allows a 0.01 CNY gap; ratios must match tightly
        ok = abs(float(got) - float(want)) <= max(0.011, 1e-6 * abs(float(want))) if abs(float(want)) > 1 \
            else abs(float(got) - float(want)) <= 5e-4 * max(1e-9, abs(float(want))) + 1e-9
    ok_all &= ok
    print(f"{'PASS' if ok else 'FAIL'}  X1  {sheet}!{ref}: excel={got} expected={want}")
print("\nall Excel cells match" if ok_all else "\nEXCEL MISMATCH")
sys.exit(0 if ok_all else 1)
