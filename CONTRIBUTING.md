# Contributing

## Setup
Prereqs: Python 3.12+, ~6 GB free disk during data download (deleted after conversion).

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/download_data.py      # needs a Kaggle token in ~/.kaggle (never commit it)
python run_all.py                    # SQL → outputs/numbers.json → Excel → dashboard → checks
python tests/check_numbers.py        # tie-out checks only
```

## Commits
- **Small commits, every working step.** One idea per commit, plain message: `add floor sizing query`.
- No `Co-Authored-By` or tool-attribution lines.
- A commit must leave `python tests/check_numbers.py` passing.
- Never commit data (`data/`, `*.parquet`, `*.csv`, `*.bz2`, `*.zip`), secrets, `CLAUDE.md` or `.claude/`. The pre-commit hook blocks these.

## Changing a number
Numbers live in `outputs/numbers.json` and are written only by `analysis/export_numbers.py`.
To change what a doc or chart shows, change the SQL or script, re-run `run_all.py`, never the doc.

## Changing a metric definition
Edit `docs/METRICS.md` first, then the SQL, then add a line to `docs/PROGRESS.md` saying what changed and why.

## Definition of done
- [ ] The query answers a question listed in `docs/ANALYSIS-PLAN.md`
- [ ] Tie-out checks pass (`docs/TESTING.md`), real output pasted in PROGRESS
- [ ] No number typed by hand anywhere
- [ ] Limits stated where the data can't support a claim
- [ ] I can explain the change in one minute without notes
