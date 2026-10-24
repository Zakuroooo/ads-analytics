# 03 · Auctions: bids, floor price, price paid
*15 minutes. Needed for chapter 8.*

## Every ad slot is sold in a tiny auction
When you open the app, there's a slot. In a few milliseconds, advertisers "bid" for it. The highest
bid wins and the ad is shown. This happens millions of times a day. That's called **real-time bidding (RTB)**.

## Second-price auction (the type in our data)
**Rule:** the highest bidder wins, but pays the **second-highest** bid (or the floor, if that's higher).

**Toy example:** one slot, three bidders, prices per 1,000 views:

| Bidder | Bid |
|---|---|
| A | ₹100 |
| B | ₹70 |
| C | ₹40 |

A wins (highest). A pays **₹70** (B's bid), not ₹100.

Why? It makes bidding honest: you can bid what the slot is really worth to you, because you only pay
what it takes to beat the next person.

Hinglish: *Sabse bada bid jeet-ta hai, par paisa doosre number ke bid jitna deta hai.*

## The floor price (reserve price)
The seller can say "I won't sell this slot below ₹X". That's the **floor**.

**Toy, same bidders, floor = ₹80:** A still wins, but now pays **max(₹70, ₹80) = ₹80**. The floor raised the price.

**Toy, floor = ₹120:** nobody bid ₹120, so **nobody wins**. The slot stays empty. Revenue = 0.

So a floor can raise revenue (A pays more) or lose revenue (slot unsold). Chapter 8 measures that trade-off.

## "Floor binding": when the floor sets the price
If the price paid equals the floor, it means no rival bid was above the floor. The floor alone set the
price. In our data, among impressions that had a floor, this happened **{floor_binding}** of the time.

That tells the ads team: competition is thin on those slots. Many auctions have only one serious bidder.

## Win rate
From a bidder's view: win rate = auctions won / auctions bid on. Our overall win rate was {win_rate}.
It varied by exchange, e.g. {ex3_win} on exchange 3 vs {ex4_win} on exchange 4.

## A data surprise in our project
The iPinYou README says its campaigns used **"a fixed relatively high-price bidding strategy"**. So iPinYou's
bids weren't what the advertiser truly valued the slot at; they were set high on purpose, to win often.
That's why my floor model doesn't trust the bids. It only uses the **price paid**, which was set by
real rivals or the floor (chapter 8, ADR 0007).

## Check yourself
1. Bids are ₹50, ₹45, ₹20, no floor. Who wins and what do they pay?
2. Same bids, floor ₹48. What happens?
3. Same bids, floor ₹60. What happens?
4. What does "floor binding" tell you about competition?
5. Why didn't I use iPinYou's bids as the advertiser's true value?

<details><summary>Answers</summary>

1. The ₹50 bidder wins and pays ₹45.
2. The ₹50 bidder wins and pays max(₹45, ₹48) = ₹48.
3. No bid reaches ₹60: the slot is unsold, revenue 0.
4. No rival came close: competition is thin, the floor decides the price.
5. The README says the bids were a fixed high price chosen to win, not real valuations.
</details>
