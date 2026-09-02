# VESSEL Packaging Specification

Last built: 2 September 2026. Companion to `docs/vessel-packaging-workbook.xlsx` (the numbers
quoted below are that workbook's default-assumption output — change an assumption there and
these figures will move). Also companion to `docs/vessel-qc-workbook.xlsx` and
`docs/vessel-launch-command-center.md`, Section C (Packaging).

Labels used below follow the founders' existing convention: **CONFIRMED**, **PROPOSED**
(direction chosen, not yet final), **MODEL ASSUMPTION** (planning input, not real data), **OPEN**
(unresolved, awaiting a quote or founder decision).

---

## 1. Proposed Packaging Rule — PROPOSED, REQUIRES FOUNDER APPROVAL

This is not a confirmed decision. It is the working rule the workbook is built around, pending
sign-off from both founders:

- One pouch per jewelry item.
- One cleaning cloth per customer order.
- One thank-you card per customer order.
- One sticker per shipping box.
- One cardboard shipping box per order.
- A bundle receives a separate pouch for each jewelry item (to prevent scratching/tangling), but
  only one cloth, card, sticker, and shipping box per order — the same as a single-item order.

## 2. Per-Order Packaging Matrix

| Order type | Pouches | Cloths | Thank-you cards | Stickers | Shipping boxes |
|---|---|---|---|---|---|
| Normal order (1 item) | 1 | 1 | 1 | 1 | 1 |
| Bundle order (2 items — VESSEL LAYER SET or THE DETAIL STACK; THE CONTRAST SET is still
  proposed but expected to keep the same 2-item shape) | 2 | 1 | 1 | 1 | 1 |

## 3. Confirmed Inputs Behind the Numbers Below

- 120 jewelry units: 8 SKUs × 15 units.
- **Pouches** and **cloths**: 500 each, **ordered** as part of the jewelry supplier's invoice
  (10 Aug 2026) — that order is ~50% paid and in production, **not yet received**. US$0.28 and
  US$0.20 per unit respectively.
- **Thank-you cards**: 1,000 **quoted only** at ₪250 total (₪0.25 each). Not ordered, not paid,
  not received.
- **Stickers**: 100 **quoted only** at ₪80 total (₪0.80 each). Not ordered, not paid, not
  received.
- **Cardboard shipping boxes**: 160 **quoted only**, unprinted, at ₪700 total (₪4.375 each). Not
  ordered, not paid, not received. Printing cost not yet quoted.
- Bundles: **VESSEL LAYER SET and THE DETAIL STACK are confirmed.** THE CONTRAST SET is still
  proposed, pending final components/price.
- Genuinely open, not guessed anywhere below: box printing cost, whether VAT/delivery are
  included in any quote, the real bundle take rate, vendor production time for boxes.

## 4. Order-Volume Mathematics (as modeled in the workbook)

Normal order = 1 item; bundle order = 2 items, so:

> Average items per order = 1 + bundle-order %
> Expected orders = Total units to sell ÷ average items per order

With the workbook's default bundle-order rate of **15%** (chosen because it reproduces the
financial model's existing 1.15-items/order and ~104-order planning figures — 120 ÷ 1.15 ≈
104.35 — not a known real rate), this yields:

- Average items per order: **1.15**
- Expected orders: **≈104.35**
- Bundle orders: **≈15.65** — Normal orders: **≈88.70**

The bundle rate, waste buffer, and even the order count itself (via an optional manual override)
are all editable in the workbook; an override that doesn't reconcile to 120 total items trips a
visible warning rather than failing silently.

## 5. Recommended Purchase Quantities (workbook default output)

**Do not read "quoted" as "buyable at that rate in any quantity."** Vendors have priced fixed
lots, not a per-unit rate — you cannot buy 110 cards for 110/1,000 of ₪250. The table below
separates what's actually *needed* from what can actually be *bought* at a known price:

| Component | Required (incl. 5% waste) | Economic usage value (analytical only) | Available quoted lot | Lot adequate? | Already ordered | Actual cash required |
|---|---|---|---|---|---|---|
| Pouches | 126 | ₪125.98 | 500 for ₪499.94 | Yes | 500 | **₪0** — already covered |
| Cloths | 110 | ₪78.56 | 500 for ₪357.10 | Yes | 500 | **₪0** — already covered |
| Thank-you cards | 110 | ₪27.50 | 1,000 for ₪250 | Yes | 0 | **₪250** — must buy the full 1,000-lot |
| Stickers | 110 | ₪88.00 | 100 for ₪80 | **NO** | 0 | **UNKNOWN** — the only quote is too small |
| Shipping boxes (unprinted) | 110 | ₪481.25 | 160 for ₪700 | Yes | 0 | **₪700** — must buy the full 160-lot |
| Box printing (per box, add-on) | 110 | — | no quote exists | — | — | **UNKNOWN** |

"Economic usage value" is what the required quantity would be worth at the quoted per-unit rate
— a planning metric, **not a real purchase option**, since none of these vendors will sell you an
arbitrary fraction of their quoted lot. Pouches and cloths need no new purchase — the 500 already
on order comfortably covers the requirement, at no incremental cost. **Cards and boxes have never
actually been ordered**, and since their only quoted lot is large enough to cover what's needed,
the real purchasing decision is binary: buy the full 1,000-card lot for ₪250, and the full
160-box lot for ₪700 — there is no smaller purchase option on record. **Stickers are different:**
the only quote (100 for ₪80) does not cover the 110 required, so there is currently no known way
to buy enough — a new, larger quote is needed before a sticker order can even be sized.

## 6. Sticker Sufficiency — Explicit Finding

**The 100 quoted stickers are NOT sufficient**, and this isn't just a shortfall you can top up at
the same rate: the only sticker quote on file is for 100 units, required is 110, and **no vendor
quote exists yet for any quantity that actually covers the requirement.** Both the price and the
available order quantity for an adequate sticker purchase are unknown. This holds under the
workbook's default assumptions and gets worse if the bundle rate or order count comes in higher
than modeled.

## 7. Cash Required

- **Full program economic value** (all required components valued at their quoted per-unit rate,
  excluding printing — an analytical figure, not a purchase price): **₪801.30**.
- **Known quoted cash required — cards + boxes** (the only two components with an adequate,
  purchasable quote, at their full lot price): **₪250 + ₪700 = ₪950.** This is the minimum real
  cash need identified so far; do **not** read the earlier ₪596.75 figure — it incorrectly
  scaled bulk quotes down to a smaller quantity, which is not something either vendor has offered.
- Stickers, box printing, VAT, and vendor delivery are all genuinely unknown and are **not**
  folded into that ₪950 as if they were zero or estimable. The workbook's all-in total displays
  **"INCOMPLETE — COST UNKNOWN"** until all four are resolved.
- Packaging cost per normal order and per bundle order (a separate, economic-allocation metric —
  not a claim about what's purchasable) likewise show **"INCOMPLETE — COST UNKNOWN (printing not
  yet quoted)"** rather than a number that quietly assumes free printing.

**Supplier-order packaging value (informational, not additive to the cash figures above):**
pouches + cloths represent **₪857.04** of value inside the jewelry supplier's invoice. Approximately
**₪3,500** of that whole invoice's deposit has been paid, and approximately **₪3,500** remains due
before shipment — that deposit was **not** allocated to individual invoice lines, so there is no
confirmed, and no illustrative, "packaging's share of the deposit" figure to report.

## 8. Physical Packing Test Checklist

Run this once sample packaging materials and at least a few real units are on hand — before
committing to final packaging quantities or box artwork:

- [ ] Does one jewelry item (in its pouch) fit correctly in the box, with room for the cloth and
      card?
- [ ] Does a 2-item bundle (2 pouches) fit in the same box without forcing or crushing?
- [ ] Are items protected from scratching each other (pouch-to-pouch, and against the box
      interior)?
- [ ] Are chains/pearls protected from tangling, both within one pouch and between two pouches in
      a bundle order?
- [ ] Does the box close securely without needing excess tape or force?
- [ ] Where does the sticker sit, and does it hold on the box surface/material?
- [ ] What does the box look like when the customer opens it — does the presentation match the
      premium brand guardrails (handoff §4)?
- [ ] Where does the shipping label go, and does it leave room for the sticker and branding to
      still be visible?
- [ ] Does anything shift or rattle when the box is gently shaken (both single-item and bundle
      configurations)?
- [ ] What is the total packed weight for a normal order and for a bundle order (relevant to
      delivery-provider pricing, which may be weight-tiered)?

## 9. Vendor Questions — Exact List, By Vendor

**Pouches & cloths (via the jewelry supplier — already ordered):**
- Confirm whether the US$140 (pouches) and US$100 (cloths) already include VAT and international
  shipping, or are billed separately.
- Confirm reorder cost, minimum order quantity, and lead time if more than 500 of either are
  ever needed.

**Thank-you cards:**
- Confirm whether the ₪250 quote includes VAT.
- Confirm whether delivery is included or billed separately.
- Confirm whether a smaller lot than 1,000 is available and its price — only ~110 are actually
  needed, and the ₪250 quote is specifically for the full 1,000-unit lot. If no smaller lot
  exists, ₪250 for the full 1,000 is the real cash requirement regardless.

**Stickers:**
- **Priority: get a new quote for a quantity that actually covers ~110+ units.** The only quote
  on file (100 for ₪80) is too small, and its per-unit rate cannot be assumed to hold at a larger
  volume — both the price and the available order quantity for an adequate purchase are unknown.
- Confirm whether that new quote includes VAT.
- Confirm whether delivery is included or billed separately.
- Confirm sticker material/adhesive suitability for the box surface (relevant to the packing
  test's "sticker placement" check).

**Cardboard shipping boxes:**
- Confirm the **printed** box price — only the ₪700/160 **unprinted** price is on file.
- Confirm whether VAT and delivery are included in both the unprinted quote and any printed
  quote.
- Confirm the vendor's production/turnaround time for printing — this is the missing input for
  the box-order deadline formula below.
- Confirm the minimum order quantity for a reprint or reorder.
- Confirm exact box interior dimensions (needed to run the physical packing test).
- Confirm proof/artwork requirements and turnaround time for approval.

**General:**
- Confirm with an accountant whether VAT applies to these purchases at all under the osek-patur
  structure, separate from the question of whether it's already included in a given quote
  (handoff §20 flags the osek-patur threshold itself as still needing professional verification).

## 10. Box-Order Deadline — Formula, Not a Date

Neither the launch date nor the box vendor's production time is confirmed yet, so a specific
calendar date here would be invented. The rule, to apply the moment both are known:

> **Box order deadline = Launch date − (receipt buffer) − (vendor production time) − (artwork
> proof turnaround)**

This mirrors the placeholders already in `docs/vessel-launch-command-center.md` (artwork proof
approval targeted at Launch −21d pending vendor lead time; box receipt targeted at Launch −7d).
Once the vendor states a real production time, substitute it into this formula against whatever
launch date gets set, and the actual order deadline falls out directly.

## 11. Open Founder Decisions

- Approve, reject, or modify the proposed packaging rule in Section 1.
- Decide the bundle-order % to plan around (currently a 15% model assumption, not a known rate).
- Decide the spare/waste buffer % to hold (currently 5%, editable).
- Decide whether to place the full-lot cards order (₪250) and boxes order (₪700) now, or wait for
  real pre-launch order data — there's no smaller purchase option for either, so this is a binary
  buy-now-or-wait call, not a "how many" call.
- Get a new sticker quote covering the real requirement before any sticker purchase decision can
  even be framed.
- Approve box artwork/branding before requesting a printed-box quote.
- Decide who chases each vendor question in Section 9 (per the launch command center, this falls
  under "packaging," which is joint between the two founders).
- Decide whether the ₪950+ additional packaging cash (cards + boxes, before stickers/printing/
  VAT/delivery are resolved) comes out of the ₪13,000 starting investment or is tracked as a
  separate near-term spend line.

---

*No vendor was contacted, no order was placed, no payment was made, and nothing public changed in
producing this document — see `docs/vessel-packaging-workbook.xlsx` for the full editable model
behind every figure above.*
