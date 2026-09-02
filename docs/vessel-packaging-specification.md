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

**Do not read "quoted" as "in stock."** Nothing has been purchased for cards, stickers, or boxes
— only priced. The table below is what the workbook calculates is actually needed to purchase
right now, using the expected full-sellout order count (≈104.35 orders) plus a 5% waste buffer,
regardless of what's been quoted:

| Component | Quoted | Ordered | Required (incl. 5% waste) | Remaining to purchase | Vendor MOQ | Recommended order qty | Cash required |
|---|---|---|---|---|---|---|---|
| Pouches | 500 | 500 | 126 | **0** | N/A (bundled) | 0 | ₪0.00 |
| Cloths | 500 | 500 | 110 | **0** | N/A (bundled) | 0 | ₪0.00 |
| Thank-you cards | 1,000 | 0 | 110 | **110** | UNKNOWN | 110 | ₪27.50 |
| Stickers | 100 | 0 | 110 | **110** | UNKNOWN | 110 | ₪88.00 |
| Shipping boxes (unprinted) | 160 | 0 | 110 | **110** | UNKNOWN | 110 | ₪481.25 |
| Box printing (per box, add-on) | — | — | 110 | 110 | N/A | 110 | **UNKNOWN** |

Pouches and cloths need no new purchase — the 500 already on order comfortably covers the
requirement. **Cards, stickers, and boxes have never actually been ordered**, despite being
quoted, and all three need a real purchase order placed for ~110 units each once vendor MOQs are
confirmed (the recommended quantities above will round up to the vendor's actual lot size once
known — e.g., if stickers can only be bought in batches of some size N, the recommendation
becomes the next multiple of N at or above 110, not 110 itself).

## 6. Sticker Sufficiency — Explicit Finding

**The 100 quoted stickers are NOT sufficient.** Required with the waste buffer: 110. Quoted: 100
— a shortfall even before accounting for the fact that zero stickers have actually been ordered.
This is not a marginal gap; it holds under the workbook's default assumptions and gets worse if
the bundle rate or order count comes in higher than modeled.

## 7. Cash Required

- **Full program value** (all required components at cost, as quoted, excluding printing):
  **₪801.30**.
- **Additional cash required — new purchases only** (cards + stickers + boxes; pouches/cloths
  excluded because any shortfall there is currently ₪0 and their cost already rides on the
  existing, separately-tracked supplier payment): **₪596.75**.
- Box printing add-on, VAT adjustment, and vendor delivery are each genuinely unknown and are
  **not** folded into that ₪596.75 as if they were zero. The workbook's all-in total displays
  **"INCOMPLETE — COST UNKNOWN"** until all three are entered.
- Packaging cost per normal order and per bundle order likewise show **"INCOMPLETE — COST
  UNKNOWN (printing not yet quoted)"** rather than a number that quietly assumes free printing.

**Supplier-order packaging value (informational, not additive to the cash figures above):**
pouches + cloths represent **₪857.04** of value inside the jewelry supplier's invoice.
**₪3,500** of that whole invoice's deposit has been paid, and **₪3,500** remains due before
shipment — but that deposit was **not** allocated to individual invoice lines, so there is no
confirmed "packaging's share of the deposit" figure. The workbook shows one **illustrative,
clearly labeled MODEL ASSUMPTION** only (≈₪428.55, if the deposit were assumed to cover every
invoice line proportionally by value) — this is not a fact and should not be treated as one.

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
- Confirm the minimum order quantity and lead time for an actual order of ~110+ units (the
  1,000-unit quote may have different per-unit economics at a smaller order size — confirm).

**Stickers:**
- Confirm whether the ₪80 quote includes VAT.
- Confirm whether delivery is included or billed separately.
- Confirm the minimum order quantity and lead time — this directly sets the "recommended order
  quantity" once the workbook's placeholder MOQ is replaced with a real number.
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
- Decide whether to place the cards/stickers/boxes orders now at the recommended quantities, or
  wait for real pre-launch order data.
- Approve box artwork/branding before requesting a printed-box quote.
- Decide who chases each vendor question in Section 9 (per the launch command center, this falls
  under "packaging," which is joint between the two founders).
- Decide whether the ₪596.75+ additional packaging cash comes out of the ₪13,000 starting
  investment or is tracked as a separate near-term spend line.

---

*No vendor was contacted, no order was placed, no payment was made, and nothing public changed in
producing this document — see `docs/vessel-packaging-workbook.xlsx` for the full editable model
behind every figure above.*
