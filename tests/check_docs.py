"""X2: docs quote only numbers from numbers.json.

1. Each rendered doc (README, MEMO, STORY, WALKTHROUGH) equals a fresh render of its template,
   so nobody hand-edited a number into the output.
2. Templates contain no hand-typed percentages: every % must come from a {placeholder}.
Run: python tests/check_docs.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis"))
import render_docs  # noqa: E402

ok_all = True
for path, text in render_docs.render().items():
    ok = path.exists() and path.read_text() == text
    ok_all &= ok
    print(f"{'PASS' if ok else 'FAIL'}  X2  {path.relative_to(ROOT)} matches its template + numbers.json")

# percentages that are definitions, not results: "95% CI", "top 20% of campaigns", "add to 100%"
DEFINITIONS = {"95%", "20%", "100%"}

for t in sorted(render_docs.TEMPLATES.glob("*.md")):
    stripped = re.sub(r"\{[a-z0-9_]+\}", "", t.read_text())
    typed = [x for x in re.findall(r"\d+(?:\.\d+)?%", stripped) if x not in DEFINITIONS]
    ok = not typed
    ok_all &= ok
    print(f"{'PASS' if ok else 'FAIL'}  X2  {t.name}: no hand-typed percentages" + (f" (found {typed})" if typed else ""))

sys.exit(0 if ok_all else 1)
