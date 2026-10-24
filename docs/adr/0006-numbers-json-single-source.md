# 0006 — All numbers flow from one `outputs/numbers.json`
Status: Accepted · Date: 2026-10-24

## Context
The same numbers appear in the Excel model, dashboard, memo, slides, README and resume bullets. Hand-copying invites drift; one mismatch kills trust in an interview.

## Options
1. Copy numbers by hand into each place.
2. Each output runs its own queries.
3. One export script writes `numbers.json`; every output reads it; a test checks the docs against it.

## Decision
Option 3.

## Why
- One place to change; re-run `run_all.py` and everything updates.
- `tests/check_numbers.py` fails if a doc quotes a number that isn't in `numbers.json`.

## Consequences
- Every new number needs a line in `analysis/export_numbers.py` first. A little slower, much safer.
