<!-- Generated from LEARN/_templates/10-ab-testing.md by analysis/render_docs.py. Edit the template, not this file. -->
# 10 · A/B testing from zero
*25 minutes. The most important statistics chapter. Go slowly.*

## The idea
You want to know if showing ads makes people convert more. You can't just compare people who saw ads with
people who didn't: they might be different people (keener shoppers see more ads). So you **randomly** split users:
- **Treatment:** can see the ads
- **Control:** can't

Because the split is random, the two groups are alike in everything except the ads. Any difference in outcome
is caused by the ads. That's why A/B tests give *causal* answers.

Hinglish: *Random baantne se dono group ek jaise ho jaate hain. Phir jo farak dikhe, woh ads ki wajah se hai.*

## Our test (Criteo Uplift)
| | Treatment | Control |
|---|---|---|
| Users | 11,882,655 | 2,096,937 |
| Visits | 576,824 | 80,105 |
| Conversions | 36,711 | 4,063 |
| Conversion rate | 0.309% | 0.194% |

## Step 0: write the plan BEFORE looking (pre-registration)
In `docs/EXPERIMENT.md`, before running anything, I fixed:
- **Primary metric:** conversion rate per user
- **Guardrail:** visit rate must not fall (ads shouldn't push people away)
- **α = 0.05**, power 80%
- **Decision rule:** ship if the conversion lift's 95% CI is above 0 and the visit guardrail holds

Why first? If you decide the rule after seeing results, you can (without meaning to) pick whatever looks good.

## Step 1: sample-ratio check (SRM)
The design said 85% treatment / 15% control. Observed: 85.0000% treatment. A chi-square test gives p = 1.00, so the
split is fine. (Honest note: Criteo built the file at exactly 85%, so this check passes almost by design.)

**Toy:** you planned 50/50 with 10,000 users but got 5,400 / 4,600. That's too far off to be chance: something broke
(e.g. a bug sending some users to one group). Stop and fix before reading results.

## Step 2: lift
- Absolute lift = 0.309% − 0.194% = **0.115 pp** (percentage points)
- Relative lift = 0.309% / 0.194% − 1 = **+59%**

"Percentage points" vs "percent": going from 2% to 3% is +1 percentage point, but +50% relative. Always say which.

## Step 3: confidence interval (CI)
The 95% CI for the relative lift is **+54% to +65%**. Meaning: if we ran this test many times, 95% of such
intervals would contain the true lift. Plain version: "the true lift is very likely between +54% and +65%".
It's far from 0, so the lift is real.

How it's computed (absolute difference):
```
SE = sqrt( pT(1−pT)/nT + pC(1−pC)/nC )
CI = (pT − pC) ± 1.96 × SE
```
SE (standard error) = how much the difference would wobble from sample to sample. Bigger samples → smaller SE → narrower CI.

## Step 4: p-value
p = 7.3e-179. The p-value is: *if ads truly did nothing*, the chance of seeing a difference this big or bigger.
It's astronomically small, so "ads did nothing" is not believable.

**Don't say:** "p-value is the probability the result is wrong". It isn't.

## Step 5: power and MDE
**MDE (minimum detectable effect)** = the smallest true lift this test could reliably catch (80% of the time at α 0.05).
Ours: +4.8% relative for conversion. The real lift (+59%) is far bigger, so the test was easily big enough.
If the lift had been smaller than the MDE, a "no effect" result would mean "too small to see", not "no effect".

## Step 6: guardrail and decision
Visits rose +27% (from 3.82% to 4.85%), so the guardrail held. **Decision by the pre-written rule: SHIP.**

## Step 7: the caveats (this is where you sound senior)
1. **Effect on exposed users:** only 3.6% of treatment users actually saw an ad. Dividing the lift by that gives an
   implausibly large effect, so I report it but don't use it. An independent re-check of my maths flagged this.
2. **Pooled tests:** the file mixes several Criteo campaigns' tests. Effects could differ inside each. Next step: a single-campaign holdout.
3. **Conversion per visit** is only descriptive: the ads changed *who* visits, so that comparison isn't randomised anymore.

## How I checked the maths
- My formulas vs the statsmodels library: same p-value and CI.
- A separate agent got only the raw counts and re-derived everything: matched to 6 significant figures.
- The Excel sheet `AB_Test` recomputes it with NORM.S.INV / NORM.S.DIST: same answer.

## Check yourself
1. Why must the split be random?
2. Conversion goes from 4% to 5%. Absolute and relative lift?
3. What does a 95% CI of +54% to +65% mean, in plain words?
4. What is a p-value? What is it NOT?
5. What is an MDE, and why does it matter when a test shows "no effect"?
6. What is SRM and what do you do if it fails?

<details><summary>Answers</summary>

1. So the groups are alike in everything except the treatment; then any difference is caused by it.
2. Absolute +1 percentage point; relative +25%.
3. The true lift is very likely in that range; since it's well above 0, ads really increased conversion.
4. If there were no real effect, the chance of a result at least this extreme. It is NOT the chance the result is wrong.
5. The smallest effect the test can reliably detect. If the true effect is below it, "no effect" just means "too small to see".
6. Sample-ratio mismatch: group sizes far from the plan. Stop, find the assignment bug, don't trust the results.
</details>
