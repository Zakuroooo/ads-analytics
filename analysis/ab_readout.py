"""A/B readout on the Criteo Uplift data, following docs/EXPERIMENT.md exactly.

Steps: count users per group (SQL) -> SRM check -> lift, 95% CI and p-value per metric
-> cross-check with statsmodels -> power/MDE -> effect on exposed users -> decision rule.
Writes outputs/ab_readout.json.
"""
import json
import math
from pathlib import Path

import duckdb
from scipy import stats
from statsmodels.stats.proportion import confint_proportions_2indep, proportions_ztest

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "uplift.parquet"
OUT = ROOT / "outputs" / "ab_readout.json"

ALPHA, POWER = 0.05, 0.80          # fixed in EXPERIMENT.md §6
INTENDED_TREATMENT_SHARE = 0.85    # from Criteo's dataset page (EXPERIMENT.md §8)
Z_ALPHA = stats.norm.ppf(1 - ALPHA / 2)   # 1.96
Z_POWER = stats.norm.ppf(POWER)           # 0.84

con = duckdb.connect()
con.execute("SET memory_limit='3GB'; SET threads=4;")


def group_counts():
    """One row per group: users, visits, conversions, exposed users, conversions among visitors."""
    rows = con.execute(f"""
        SELECT treatment,
               count(*)                         AS users,
               sum(visit)                       AS visits,
               sum(conversion)                  AS conversions,
               sum(exposure)                    AS exposed,
               sum(conversion * visit)          AS conversions_after_visit
        FROM '{DATA}'
        GROUP BY treatment
    """).fetchall()
    keys = ["users", "visits", "conversions", "exposed", "conversions_after_visit"]
    return {("T" if r[0] == 1 else "C"): dict(zip(keys, map(int, r[1:]))) for r in rows}


def srm_check(n_t, n_c):
    """Sample-ratio mismatch: are the group sizes what the 85/15 design promised?"""
    total = n_t + n_c
    expected = [total * INTENDED_TREATMENT_SHARE, total * (1 - INTENDED_TREATMENT_SHARE)]
    chi2, p = stats.chisquare([n_t, n_c], f_exp=expected)
    return {"observed_treatment_share": n_t / total, "intended": INTENDED_TREATMENT_SHARE,
            "chi2": chi2, "p_value": p, "passes": bool(p >= 0.001)}


def compare(x_t, n_t, x_c, n_c):
    """Two-proportion comparison: rates, absolute and relative lift, 95% CI, p-value."""
    p_t, p_c = x_t / n_t, x_c / n_c
    diff = p_t - p_c

    # CI for the difference uses the unpooled standard error (each group keeps its own rate)
    se_unpooled = math.sqrt(p_t * (1 - p_t) / n_t + p_c * (1 - p_c) / n_c)
    ci = (diff - Z_ALPHA * se_unpooled, diff + Z_ALPHA * se_unpooled)

    # The test assumes H0 (no difference), so it uses one pooled rate for both groups
    p_pool = (x_t + x_c) / (n_t + n_c)
    se_pooled = math.sqrt(p_pool * (1 - p_pool) * (1 / n_t + 1 / n_c))
    z = diff / se_pooled
    p_value = 2 * stats.norm.sf(abs(z))

    # Relative lift CI via the log of the ratio (delta method), so it stays sensible for small rates
    se_log_ratio = math.sqrt((1 - p_t) / (p_t * n_t) + (1 - p_c) / (p_c * n_c))
    ratio = p_t / p_c
    rel_ci = (ratio * math.exp(-Z_ALPHA * se_log_ratio) - 1, ratio * math.exp(Z_ALPHA * se_log_ratio) - 1)

    # Cross-check against statsmodels (TESTING.md M3)
    _, sm_p = proportions_ztest([x_t, x_c], [n_t, n_c])
    sm_ci = confint_proportions_2indep(x_t, n_t, x_c, n_c, method="wald", compare="diff")

    return {"rate_treatment": p_t, "rate_control": p_c, "abs_lift": diff, "abs_ci95": ci,
            "rel_lift": ratio - 1, "rel_ci95": rel_ci, "z": z, "p_value": p_value,
            "check_statsmodels": {"p_value": sm_p, "ci95": list(sm_ci),
                                  "matches": bool(abs(sm_p - p_value) < 1e-6
                                                  and abs(sm_ci[0] - ci[0]) < 1e-9
                                                  and abs(sm_ci[1] - ci[1]) < 1e-9)}}


def mde(p_c, n_t, n_c):
    """Smallest true lift this test would detect 80% of the time at alpha 0.05."""
    abs_mde = (Z_ALPHA + Z_POWER) * math.sqrt(p_c * (1 - p_c) * (1 / n_t + 1 / n_c))
    return {"abs": abs_mde, "rel": abs_mde / p_c}


def decide(srm, primary, guardrail):
    """Decision rule fixed in EXPERIMENT.md §7."""
    if not srm["passes"]:
        return "untrustworthy (SRM failed)"
    if primary["abs_ci95"][0] > 0 and guardrail["abs_ci95"][0] >= 0:
        return "ship"
    if primary["abs_ci95"][1] < 0 or guardrail["abs_ci95"][1] < 0:
        return "don't ship"
    return "inconclusive"


def main():
    g = group_counts()
    t, c = g["T"], g["C"]
    srm = srm_check(t["users"], c["users"])
    conversion = compare(t["conversions"], t["users"], c["conversions"], c["users"])
    visit = compare(t["visits"], t["users"], c["visits"], c["users"])
    conv_given_visit = compare(t["conversions_after_visit"], t["visits"],
                               c["conversions_after_visit"], c["visits"])

    # Effect on users who actually saw an ad (CACE): ITT divided by the share of treatment users exposed.
    # Valid because control users could not be exposed (one-sided non-compliance).
    exposure_rate = t["exposed"] / t["users"]
    cace = {"exposure_rate_treatment": exposure_rate,
            "exposed_in_control": c["exposed"],
            "conversion_abs_lift_exposed": conversion["abs_lift"] / exposure_rate,
            "visit_abs_lift_exposed": visit["abs_lift"] / exposure_rate}

    result = {
        "counts": g,
        "srm": srm,
        "primary_conversion": conversion,
        "secondary_visit": visit,
        "secondary_conversion_given_visit": conv_given_visit,
        "guardrail_visit_not_down": {"abs_ci95": visit["abs_ci95"],
                                     "passes": bool(visit["abs_ci95"][0] >= 0)},
        "mde_conversion": mde(conversion["rate_control"], t["users"], c["users"]),
        "mde_visit": mde(visit["rate_control"], t["users"], c["users"]),
        "effect_on_exposed": cace,
        "decision": decide(srm, conversion, visit),
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, default=float))
    print(json.dumps({k: result[k] for k in ("srm", "decision")}, indent=2, default=float))
    print(f"conversion: {conversion['rate_control']:.5f} -> {conversion['rate_treatment']:.5f} "
          f"abs {conversion['abs_lift']:.5f} CI {conversion['abs_ci95'][0]:.5f}..{conversion['abs_ci95'][1]:.5f} "
          f"rel {conversion['rel_lift']:.1%} p={conversion['p_value']:.2e} sm_match={conversion['check_statsmodels']['matches']}")
    print(f"visit:      {visit['rate_control']:.5f} -> {visit['rate_treatment']:.5f} "
          f"abs {visit['abs_lift']:.5f} rel {visit['rel_lift']:.1%} p={visit['p_value']:.2e}")


if __name__ == "__main__":
    main()
