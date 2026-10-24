# EXPERIMENT — A/B design, written before the readout
*Pre-registration. Written 2026-10-24, before I ran any analysis on the uplift data. Honest caveat: the
dataset is public and its paper reports headline numbers; I have not used them to set anything below.
Changes after seeing results go in §8 with a date, never by editing §1–7.*

## 1. The test (as Criteo ran it)
Users were randomly split. **Treatment** users were eligible to see Criteo ads; **control** users were not.
Some treatment users never actually saw an ad (`exposure = 0`).

Marketplace translation: *"Does showing a new sponsored ad format make users visit and order more?"*

## 2. Hypotheses
- H0: conversion rate (treatment) = conversion rate (control)
- H1: they differ (two-sided test, even though we expect an increase)

## 3. Metrics
| Role | Metric | Unit |
|---|---|---|
| **Primary** | conversion rate = users with `conversion=1` / users | per user |
| Secondary | visit rate = users with `visit=1` / users | per user |
| Secondary | conversion given visit | per visiting user |
| Guardrail | visit rate must not fall in treatment (ads annoying users) | per user |
| Validity | sample-ratio mismatch (SRM) check | — |

Limit: real marketplace guardrails (order cancellations, session length, organic restaurant clicks)
are not in this data. Stated in the readout.

## 4. Analysis
- **Intent-to-treat (ITT)** is the main answer: compare everyone assigned, exposed or not. It is what a
  launch decision would actually get.
- Absolute lift = p_T − p_C; relative lift = (p_T − p_C) / p_C.
- 95% CI for the difference: two-proportion z-interval (unpooled SE). Cross-checked with scipy.
- p-value: two-proportion z-test (pooled SE).
- **Effect on exposed users (CACE)** = ITT / exposure rate in treatment (control cannot be exposed),
  reported as secondary with its assumption stated.
- Exploratory (labelled exploratory, not used for the decision): lift by quartile of 2 features.

## 5. Validity checks (run first)
- **SRM:** chi-square test of observed treatment/control counts vs the intended split. The intended split
  is taken from the dataset paper/README ⏳. If p < 0.001, stop and report the test as untrustworthy.
- Rates are 0/1 only; no missing values.

## 6. Power and MDE
- α = 0.05 (two-sided), power = 80%.
- MDE (absolute) = (z₀.₉₇₅ + z₀.₈) × √(p_C(1−p_C)(1/n_T + 1/n_C)), using the observed control rate.
- Reported as both absolute and relative MDE, so leadership sees "the smallest lift this test could detect".

## 7. Decision rule (fixed now)
- **Ship** if: SRM passes AND primary CI lower bound > 0 AND visit-rate guardrail CI lower bound ≥ 0.
- **Don't ship** if the primary CI upper bound < 0, or the guardrail CI is entirely below 0.
- **Inconclusive** otherwise → recommend a longer test, with the sample size needed.

## 8. Deviations and notes after loading data
- **2026-10-24 (before looking at any outcome column):** Criteo's dataset page gives the intended
  treatment ratio as **0.85**, and says the data comes from *several* incrementality tests, sub-sampled
  non-uniformly for privacy. Observed treatment share in the file: 0.8500001. So the SRM check will
  pass almost by construction; it is still run and reported, but it can't detect real assignment bugs
  here. Also: absolute visit/conversion rates are not representative of any one live campaign; the
  readout reports them, but the decision rests on the treatment-vs-control difference.
  No change to metrics, alpha or decision rule.
- **2026-10-24 (after the readout, from an independent re-derivation of the statistics):** all numbers
  matched to 6 significant figures; the rule gives **SHIP**. Caveats added, not changes to the rule:
  1. The effect-on-exposed (CACE) estimate is implausibly large (+28.7 pp visit rate for exposed users vs
     a 3.8% control rate; exposure is only 3.6% of treatment users). Likely exposure is logged in a way
     that breaks the IV assumption (e.g. recorded around a visit). **CACE is reported but not used.**
  2. The data pools several tests; SRM and lift could differ inside each test (Simpson's paradox).
     Per-test IDs aren't in the data, so this can't be checked here. Recommendation becomes
     "ship, and confirm with a single-campaign holdout".
  3. Conversion-per-visit conditions on a post-treatment variable, so it is **descriptive only**.
  4. Three metrics, no multiplicity correction: irrelevant at these z-values (z ≥ 14), stated anyway.
