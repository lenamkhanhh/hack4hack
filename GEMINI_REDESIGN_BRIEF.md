# ReturnLens v5 — Gemini redesign brief (visual only)

## Task
Redesign the visual presentation of the existing 6-slide ReturnLens deck so it looks beautiful and is easy to read. Do NOT change the content, facts, numbers, or decisions. The user judges the visual result; do not remove content just to make a slide look emptier.

## Source of truth
- `content/deck_data.json` — canonical content and speaker notes.
- `src/build_v5_pptx.py` — current PPTX generator (after the typography pass: Calibri / Consolas, larger body text). Regenerate the PPTX from the generator after any redesign, so the file and the generator stay in sync.
- Note: the committed `deliverables/ReturnLens_v5.pptx` binary is still the older 0fe65b5 build. Treat the generator + `deck_data.json` as the source, not the old binary.

## Format (hard)
- Exactly 6 slides, 16:9, 13.333 x 7.5 inch.
- Native editable PPTX with speaker notes on all 6 slides. Hack4Hack requires a PPT / Google Slides link; HTML alone is not a submission.
- Save the redesign as a NEW version (for example `deliverables/ReturnLens_v6.pptx` + generator `src/build_v6_pptx.py`). Do not overwrite v5, so the user can compare.

## Content that must stay exactly
- Thesis: "Models observe. Code verifies. Seller authorizes."
- User: a solo direct-to-consumer merchant managing orders/returns alone.
- Architecture: 3 base model calls per case (planner, vision, critic); policy P-01 to P-08 as deterministic code; seller gate, fail-closed; no automatic refunds, labels, or denials.
- Refund cap, server-computed, LLM never sets the amount: `0 < amount <= min(₹4,999, remaining_refundable_amount, order_paid_amount)`.
- Approval binding: approval binds case + evidence hash + policy version, with revalidation before any draft is released.
- Case A (ORD-1042, ₹1,499): valid return, prepared for seller review, label + refund draft in `pending_return_receipt`, not executed.
- Case B, star demo (case RT-8821, order ORD-7729, SKU HEAD-WHT-02 White, ₹1,499, frame 00:07): video shows black casing. Wording must stay: "Black casing (color-consistent with HEAD-BLK-09) · Barcode unverified · SKU not verified". Outcome: ESCALATE to seller, P-03 FAIL, no label, no refund draft, no denial.
- Case B seller options, only these three: Accept mis-shipment / Request box-label photo / Hold for physical inspection. Exchanges are NOT a seller option (exchanges are only under "Cut First").
- Case C: dark 4-second video, brightness 28/255, 2 usable frames, P-06 FAIL, REQUEST_MORE_EVIDENCE, state WAITING_FOR_EVIDENCE. Termination: "After 1 retry, escalates to seller with both attempts logged (never auto-denies)".
- Case D: continuous unboxing sequence test only. It inspects sequence continuity and flags abrupt transitions. It does NOT prove item authenticity.
- Slide 6 scope: "3 core demo cases (A–C) + Case D sequence test", plus approval binding. Cut First: "Advanced video forensic splice analysis (Case D stretch)", plus WhatsApp, exchanges, multi-seller auth, real carriers, audio, public deployment.
- Fraud figures, only with definitions separated: NRF 2025 strict fraud 9% vs Appriss/Deloitte 2024 fraud + abuse 15.14%.

## Do NOT invent
- No invented people, metrics, or hashes. No "SHA256:xxxx" value, no "1080p" claim, no pinned vision-model name (the model is deliberately unpinned, to be verified at build hour 0), no "average brightness" — 28/255 is the Case C sample only.
- No staged photo labelled as a video frame. Mock evidence must stay labelled "Mock evidence pack".
- No prototype code claims: this is an idea-round deck, not a built product.

## Visual goal
- Clean, readable typography, larger body text than the old 9–11pt, clear hierarchy, no text overflowing its card, no text touching a card border, footer at 7.0 inch kept clear.
- Keep the dark slide 4 and the light slides recognisable; improve fonts, spacing, and card fill, not the story.
- Check every slide at full size after regenerating, and fix any overflow before handing back.
