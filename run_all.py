"""One command rebuilds everything from the Parquet data:
SQL -> A/B readout -> numbers.json -> Excel -> dashboard data -> checks.
Run: python run_all.py   (data/ must exist: see docs/RUNBOOK.md)
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STEPS = [
    ("SQL layer", ["analysis/run_sql.py"]),
    ("A/B readout", ["analysis/ab_readout.py"]),
    ("numbers.json", ["analysis/export_numbers.py"]),
    ("Excel model", ["excel/build_xlsx.py"]),
    ("Dashboard data", ["dashboard/build_data.py"]),
    ("Docs from templates", ["analysis/render_docs.py"]),
    ("Tie-out checks", ["tests/check_numbers.py"]),
    ("Excel recalculation check", ["tests/check_excel.py"]),
    ("Docs check", ["tests/check_docs.py"]),
]

for name, args in STEPS:
    if not (ROOT / args[0]).exists():
        print(f"-- skip {name} ({args[0]} not built yet)")
        continue
    print(f"\n== {name}", flush=True)
    result = subprocess.run([sys.executable, *args], cwd=ROOT)
    if result.returncode != 0:
        sys.exit(f"stopped: {name} failed")
print("\nall steps passed")
