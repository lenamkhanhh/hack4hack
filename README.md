# ReturnLens 🔍
### Autonomous Evidence-Backed Return Triage Agent for Solo D2C Merchants
**AgentX Hackathon 2026 · Track PS-04 (Autonomous Support Agent)**  
**Team Rookie (3 Members) · 24-Hour Prototype Feasibility**

---

![ReturnLens Pitch Deck Preview](deliverables/ReturnLens_v4_preview.png)

## 📌 Project Overview & Current Stage

> **Submission Scope:** **Idea Round Prototype Proposal**  
> This repository contains the official pitch deck, generation engine, staged benchmark evidence, and verified build pipeline. It defines the architecture, deterministic policy rules, and 24-hour execution roadmap for the hackathon prototype. It is not an existing live commercial deployment.

**ReturnLens** is an evidence-backed returns triage agent tailored for solo direct-to-consumer (D2C) online sellers who manage customer support, orders, and returns alone.

When an online customer submits a return request with a short unboxing video (30–60 seconds), ReturnLens:
1. **Intake**: Extracts video keyframes at ~1 fps via FFmpeg alongside customer reason and order ID.
2. **Plan**: Formulates a typed JSON plan schema (`requires_seller_approval: true`).
3. **Evidence**: Pulls store truth (Shopify mock API) and courier tracking scans (Shippo mock API), indexing visual observations against timestamped frames (e.g. Frame 00:07).
4. **Verify**: Runs deterministic code policies (`P-01` to `P-08`) and invokes an independent critic loop to verify cited frames and flag unsupported observations.
5. **Decide & Authorize**: Enforces a strict fail-closed decision function, presenting structured evidence to the merchant console for **one-click human seller authorization**.

> **Core Philosophy:** *Models observe. Code verifies. Seller authorizes.*  
> No automatic customer denials. No mock refund or return label is ever released without explicit merchant approval.

---

## 🎯 Track PS-04 Alignment (Primary & Secondary Routes)

While ReturnLens differentiates itself through **multimodal, video-backed return triage** (solving the solo seller's most expensive problem), it also covers routine customer support inquiries under Problem Statement PS-04:
- **Primary Video Triage Route:** Analyzes customer unboxing footage, checks policies P-01–P-08, extracts timestamp citations, and prepares human-in-the-loop authorization.
- **Secondary Order Status Route (Zero-Vision Fast Path):** When a buyer asks *"Where is my order?"*, the agent directly reuses the mock Shopify and Shippo APIs to return real-time delivery timestamps and courier status scans in sub-second time, escalating to the seller only if courier delay thresholds are exceeded.

---

## 📦 Verified Deliverables & Repository Map

All deliverables are generated from source code and maintained in both the repository root and `deliverables/`:

| Deliverable | File Path | Verified Specifications |
| :--- | :--- | :--- |
| **Interactive HTML Deck** | [`ReturnLens_v4.html`](ReturnLens_v4.html) / [`index.html`](index.html) | Standalone, self-contained 16:9 widescreen presentation (1280×720) with embedded base64 photorealistic assets and keyboard navigation (`←`/`→`/`Space`). |
| **Submission PDF** | [`ReturnLens_v4.pdf`](ReturnLens_v4.pdf) | Exactly 6-page 16:9 widescreen PDF rendered via headless browser engine with vector typography and zero margin clipping. |
| **PowerPoint Deck** | [`ReturnLens_v4.pptx`](ReturnLens_v4.pptx) | Native, editable 16:9 presentation with embedded high-resolution photos, vector shapes, and **verified speaker notes on all 6 slides**. |
| **Master Preview** | [`ReturnLens_v4_preview.png`](ReturnLens_v4_preview.png) | High-resolution 2352×900 master 6-slide contact sheet preview (3×2 grid). |
| **HTML & PDF Generator** | [`src/generate_v4_html.py`](src/generate_v4_html.py) | Python master build script with automatic cross-platform browser discovery (Chrome/Edge) and 100% idempotent execution. |
| **PowerPoint Generator** | [`src/build_v4_pptx.py`](src/build_v4_pptx.py) | Python script generating native PPTX via `python-pptx` with embedded technical speaker notes. |
| **Smoke Test Suite** | [`scripts/smoke_test.py`](scripts/smoke_test.py) | Automated test suite validating deliverable synchronization, PDF page counts, PPTX speaker notes, preview dimensions, and generator idempotency. |

```text
hack4hack/
├── deliverables/                     # Official v4 submission artifacts
│   ├── ReturnLens_v4.pptx            # Native editable PowerPoint deck (16:9) with speaker notes
│   ├── ReturnLens_v4.pdf             # 6-page presentation PDF (16:9)
│   ├── ReturnLens_v4.html            # Standalone interactive HTML deck
│   └── ReturnLens_v4_preview.png     # Full 6-slide preview contact-sheet (2352x900)
│
├── src/                              # Source code, generators, and assets
│   ├── build_v4_pptx.py              # Python script generating native PPTX with notes
│   ├── generate_v4_html.py           # Python script compiling HTML, PDF & preview
│   └── assets/                       # Staged photos, video frames, and slide renders
│       ├── demo_white_order.jpg      # Store catalog ground truth photo (HEAD-WHT-02, Matte White)
│       ├── demo_black_frame.jpg      # Customer video unboxing frame at 00:07 (Midnight Black)
│       ├── hero_video_frame.jpg      # Inspection frame at 00:14
│       └── slides/                   # High-resolution rendered PNG images of slides 1 to 6
│
├── scripts/                          # Automated testing and verification
│   └── smoke_test.py                 # 8-step smoke test verifying build & deliverable integrity
│
├── research/                         # Background research & problem statement analysis
│   └── AgentX_Idea_Research.html     # Deep dive on 7 AgentX problem statements & market friction
│
├── archive/                          # Historical iterations (v0, v1 Swiss, v2, v3)
├── requirements.txt                  # Python build dependencies
├── ReturnLens_v4.html                # Root deliverable (matches deliverables/)
├── ReturnLens_v4.pdf                 # Root deliverable (matches deliverables/)
├── ReturnLens_v4.pptx                # Root deliverable (matches deliverables/)
├── ReturnLens_v4_preview.png         # Root deliverable (matches deliverables/)
├── index.html                        # GitHub Pages entry point
└── README.md                         # Project documentation and review guide
```

---

## 🎯 6-Slide Pitch Deck Architecture

### Slide 1: Product Launch & Executive Summary
- **Tag**: `AgentX Hackathon 2026 · Track PS-04`
- **Headline**: `RETURNLENS` — *“Review returns with cited video evidence.”*
- **Value Proposition**: Evidence-backed returns triage agent for solo direct-to-consumer online sellers.
- **Scope Guardrails**: Return triage core + 1 zero-vision order-status route. Fail-closed architecture; no autonomous refunds.
- **Visual Anchor**: Seller Review Console mockup featuring Case RET-4082 / ORD-9021 with inspection frame 00:14, store truth (`HEAD-WHT-02`, ₹1,499), honest visual observation (*“Potential casing damage flagged · Requires manual confirmation”*), policy verification (`P-01 FLAGGED FOR REVIEW`, `P-04 PASS`), status `READY FOR SELLER REVIEW (FLAGGED)`, and 1-click draft authorization.

### Slide 2: The Problem as a Visual Story (3-Column Zero-Overlap Layout)
- **Tag**: `The Problem · Solo Seller Bottleneck`
- **Headline**: `One return decision. Four disconnected sources.`
- **Subtitle**: *The return decision is made from memory, before the evidence is checked.*
- **Visual Layout**: 3-column composition without overlap:
  - *Left Column*: Source 01 (Buyer Chat: “Received damaged item”, 30–60s video) & Source 03 (Courier Tracking: Delivered 4 days ago, Shippo mock API scan).
  - *Center Pillar (Critical Gap)*: **`NO SHARED EVIDENCE RECORD`** — *Today the seller opens 4 tabs, then decides alone. A wrong refund loses inventory; an unfair denial loses a customer. The gap is that no single record ties order truth, video frames, policy clauses, and decisions together.*
  - *Right Column*: Source 02 (Order Record: White Headphones, ₹1,499, Shopify mock API) & Source 04 (Return Policy: 7-day window, sealed tag, code rules P-01 to P-08).
- **Sourced Signal**: Fraud estimates differ by definition: **9%** (*NRF 2025, fraud only*) vs **15.14%** (*Appriss/Deloitte 2024, fraud + abuse*).

### Slide 3: The Star Demo (Visual Evidence Benchmark)
- **Tag**: `Visual Evidence Benchmark · Core Demonstration`
- **Headline**: `The order says white. The video shows black.`
- **Subtitle**: *ReturnLens surfaces the contradiction instead of auto-denying.*
- **Visual Contrast**:
  - *Left Card (Order Ground Truth)*: Studio photo of `HEAD-WHT-02` (Matte White, ₹1,499, delivered 4 days ago, tag present).
  - *Center Badge*: `COLOR MISMATCH`.
  - *Right Card (Video Keyframe)*: Customer unboxing frame at `00:07` showing Midnight Black item. Grounded citation explicitly notes: *“Observed Color: Midnight Black · Exact SKU: Not verified · Tag: Not visible in cited frame”*.
- **Deterministic Policy Gate**:
  - Rule `P-03 Check: COLOR MISMATCH`.
  - Plan Schema: `typed JSON, requires_seller_approval: true`.
  - Status: `STATUS: ESCALATE (SELLER REVIEW REQUIRED)` — Color mismatch observed; exact SKU unconfirmed; no automatic customer denial.
  - **3 Seller Options**:
    1. Accept as merchant mis-shipment (seller mistake).
    2. Ask customer for outside-box shipping label (buyer mistake).
    3. Hold return for physical inspection at warehouse (potential swap).
  - **Financial Cap**: $0 < \text{amount} \le \min(₹4,999, \text{remaining refundable amount}, \text{order paid amount})$.

### Slide 4: System Architecture (Deterministic Pipeline)
- **Tag**: `System Architecture · Deterministic Pipeline`
- **Headline**: `Models observe. Code verifies. Seller authorizes.`
- **Subtitle**: *Policy checks and seller approval control actions.*
- **6-Step Pipeline**:
  $$\text{01 PLAN [MODEL]} \longrightarrow \text{02 RETRIEVE [CODE]} \longrightarrow \text{03 EVALUATE [CODE]} \longrightarrow \text{04 AUDIT [MODEL]} \longrightarrow \text{05 AUTHORIZE [HUMAN]} \longrightarrow \text{06 RECORD [CODE]}$$
- **Secondary PS-04 Order Status Route**:
  $$\text{Query: “Where is my order?”} \longrightarrow \text{Mock Store API} \longrightarrow \text{Courier Scan} \longrightarrow \text{Instant Delivery Timestamp (Zero-Vision Fast Path)}$$
- **4 Decision Function Outcomes (Strict Priority Order)**:
  1. `Contradiction → Escalate`: Discrepancy flagged (e.g. Case B); inhibits automated label and refund draft.
  2. `Hard Fail → Escalate`: Mandatory rule violation (e.g. expired return window); seller decides; never auto-deny.
  3. `Unclear Only → Ask More`: Low brightness or blurry barcode (e.g. Case C); exact re-film checklist (1 retry limit).
  4. `All Pass → Approve Review`: All clauses pass (e.g. Case A); prepares mock label and drafts refund in `pending_return_receipt`.
- **Core Architecture Rules**:
  - *Model Calls*: Exactly 3 base LLM calls per triage case (planner, vision, critic) plus retries.
  - *Policy Clauses*: Deterministic Python code rules `P-01` to `P-08`, never prompts.
  - *Critic Duty*: The critic reviews cited frames and flags unsupported observations.
  - *Safety Boundary*: Prompt injection cannot modify policy code, exceed server caps, or bypass human gate.

### Slide 5: Four Demo Benchmark Scenarios
- **Tag**: `Demo Scenarios · Grounded Verification`
- **Headline**: `Four scenarios. Four predictable behaviors.`
- **Subtitle**: *Every decision can be clicked back to a frame, a clause, and a log entry.*
- **4 Reproducible Benchmark Cases**:
  - **Case A · Ready for Review (`ORD-1042`, ₹1,499)**:
    - *Evidence*: SKU matches manifest, tag visible, defect confirmed within 7-day window.
    - *Expected Action*: Seller approval releases mock return label and refund draft in `pending_return_receipt`, not executed refund.
  - **Case B · Mismatch (Color Discrepancy - Core Benchmark)**:
    - *Evidence*: Ordered `HEAD-WHT-02` (White) vs Video Frame 00:07 showing Black item (SKU unverified).
    - *Expected Action*: `ESCALATE` (no label, no refund, no denial). Seller chooses mis-shipment / box label / physical inspection.
  - **Case C · Unclear (Low Lighting)**:
    - *Evidence*: 4-second dark video, brightness 28, only 2 usable frames.
    - *Expected Action*: `ASK MORE EVIDENCE` (case stays open with exact re-film checklist; 1 retry limit).
  - **Case D · Context (Sequence Continuity)**:
    - *Evidence*: Staged parcel-to-product take: opening sealed parcel to product reveal in one continuous take.
    - *Expected Action*: *Expected prototype behavior: inspect sequence continuity and flag missing transitions for seller review.*

### Slide 6: 24-Hour Execution & Feasibility
- **Tag**: `Execution Plan · Team Rookie (3 Members)`
- **Headline**: `Built for a 24-hour sprint.`
- **Subtitle**: *Buildable in 24 hours by 3 people, if the scope stays narrow.*
- **24-Hour Timeline Grid**:
  - `00h – 06h`: **Mock APIs & Agent Core** · LangGraph skeleton, mock store/courier fixtures, order status route · *Owner: Person A (Backend)*
  - `06h – 12h`: **Evidence Pipeline & Policy** · FFmpeg keyframe indexer, Python rules P-01 to P-08, critic prompt · *Owner: Person B (Video & UI)*
  - `12h – 18h`: **Integration & Four Scenarios** · End-to-end wiring, 4 staged demo cases (A–D), seller console UI · *Owner: Person C (Integration)*
  - `18h – 24h`: **Testing, Polish & Submission** · Fallback testing, edge cases, video walkthrough recording, README · *All 3 Members*
- **Scope Discipline**:
  - **Never Cut (Core Engine)**: Deterministic policy engine (`P-01` to `P-08`), evidence-pack frame citation, fail-closed seller approval gate, structured JSON audit log, 4 reproducible demo cases.
  - **Cut First (Deferred Expansion)**: Video OCR barcode scanner, auto-drafted customer email reply, seller analytics dashboard, production payment gateways / live WhatsApp webhooks.
- **Closing Motto**:
  > *“The winning hackathon agent is not the one with the most tool definitions. It is the one where every action is held to evidence, and the seller stays in control.”*

---

## 🛠️ How to Reproduce & Verify All Deliverables

### Prerequisites
- Python 3.10+
- An installed headless browser (Microsoft Edge or Google Chrome)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Automated Smoke Test Suite
```bash
python scripts/smoke_test.py
```
This script will:
- Run `src/generate_v4_html.py` to compile HTML and invoke Edge/Chrome headless PDF rendering.
- Verify that `generate_v4_html.py` does not modify its own source code (idempotency check).
- Run `src/build_v4_pptx.py` to generate the native PowerPoint presentation.
- Verify byte synchronization across root and `deliverables/`.
- Validate that the PDF has exactly 6 pages in 16:9 widescreen.
- Validate that all 6 slides in the PPTX contain embedded technical speaker notes.
- Check that preview dimensions are exactly 2352×900.
- Check that all evidence grounding rules are satisfied.

### 3. Rebuild Individual Outputs
- To rebuild HTML, PDF, and slide PNG preview:
  ```bash
  python src/generate_v4_html.py
  ```
- To rebuild native PowerPoint presentation:
  ```bash
  python src/build_v4_pptx.py
  ```

---

## 🛡️ Technical & Ethical Guardrails

1. **Fail-Closed Architecture**: The model is purely observational. All state transitions, policy checks, and refund drafts run through deterministic Python code.
2. **Cap on Draft Refunds**: Hard ceiling enforced at code level: $\min(₹4,999, \text{remaining balance}, \text{order amount})$.
3. **Audit Trail**: Every evaluation outputs an immutable structured JSON log recording frame citations, rule evaluations, and timestamps.
4. **No Real PII / Mock Data**: All customer identities, shipping tracking scans, and store orders are staged mock fixtures for hackathon evaluation.
