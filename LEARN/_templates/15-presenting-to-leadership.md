# 15 · Presenting to leadership
*20 minutes + practice. Spoken English is the part to train hardest, so this chapter is about speaking, not slides.*

## The shape every leadership answer takes
**Objective → assumptions → findings → recommendation.** It's the same shape as `docs/MEMO.md` and the 5 slides
in `docs/READOUT.pptx`.

Rule: **the answer first, then the reason.** Leaders decide fast; don't make them wait for the point.

| Weak | Strong |
|---|---|
| "So I looked at the auction data and there were many exchanges and…" | "Competition is thin. The floor set the price on {floor_binding} of floored auctions." |
| "The A/B test had a p-value of…" | "Ads work: conversion went up {conv_rel}, and I'm confident it's real." |
| "It depends on many factors." | "It pays off only if at least {x30_breakeven} still sell. I'd test it first." |

Hinglish: *Pehle jawab, phir wajah. Leader ko seedha point chahiye.*

## Your materials
- **2-minute script:** `docs/WALKTHROUGH.md`, short sentences, timed sections.
- **5 slides:** `docs/READOUT.pptx` (opens in Google Slides): objective, assumptions, findings, recommendation, next steps.
- **1-page memo:** `docs/MEMO.md`.
- **Live dashboard:** https://slotwise-ads.vercel.app (walk through it top to bottom: KPIs, auction, floor model, advertisers, A/B).

## How to practise speaking (10 minutes a day)
1. Read the walkthrough once aloud, slowly.
2. Record yourself on your phone. Listen once. Note one thing to fix (speed, filler words, a missed number).
3. Say it again without reading, using only the 5 section titles as cues.
4. Use short sentences. One idea per sentence. Pause after each number.
5. If you forget a number, say the idea: "the floor set the price on more than a third of auctions". Ideas matter more than digits.

## Handling interruptions
- **"Is this Swiggy data?"** "No, public ad data. I say that first, every time."
- **"That lift looks too high."** "Agreed, it's large. The data pools several tests, so I'd confirm with a single-campaign holdout."
- **"So what should we do?"** Three moves: fix the expensive advertisers, test a floor before rolling it out, pitch budget to the efficient small ones.
- **"I don't follow."** Slow down, use the toy example (3 bidders, chapter 3; 4 impressions, chapter 8).

## Filler words to drop
"basically", "like", "actually", "so yeah". Replace with a 1-second pause. Silence sounds confident.

## Check yourself (say these aloud)
1. In one sentence: should we raise floor prices?
2. In one sentence: did the ads work?
3. In one sentence: which advertisers should ad sales call first?

<details><summary>Model answers</summary>

1. "Not yet: it only pays off if at least {x30_breakeven} of affected impressions still sell, so I'd A/B test a floor first."
2. "Yes: conversion went up {conv_rel} in a randomised test, with a confidence interval well above zero."
3. "The 'fix' group: {fix_share} of spend, paying {fix_cpa_ratio} more per conversion, and already spending less."
</details>
