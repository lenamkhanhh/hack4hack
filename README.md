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

## 🧠 Technical Defensibility & Judge Q&A Defense

| Question / Concern | Technical Mechanism in ReturnLens | Architecture Guarantee |
| :--- | :--- | :--- |
| **Q1: Why is this an agent rather than a hardcoded workflow?** | **Dynamic state machine with conditional branching & pause/resume.**<br>In Case C, upon detecting low-light video (brightness 28), the agent dynamically halts normal execution, calls `ask_for_evidence()` with specific re-filming guidance, transitions the state machine to `WAITING_FOR_EVIDENCE`, pauses execution, and resumes the exact ticket context when new evidence arrives (1 retry limit). Conversely, routine order queries take a zero-vision fast path directly querying mock store and courier APIs. | **Stateful resumption & adaptive tool selection** rather than static linear scripting. |
| **Q2: What happens if vision or critic models hallucinate?** | **Observations are non-binding; code enforces business truth.**<br>Vision model outputs (`observed_color`, `damage_flag`) are treated strictly as observation metadata. Hard constraints (7-day delivery window from courier scans, SKU comparisons) are verified in deterministic Python (`P-01` to `P-08`). The critic provides an adversarial sanity check against cited timestamps. If both models suffer correlated errors, the **fail-closed human gate** ensures no refund or label is ever issued without seller review. | **Zero autonomous execution.** LLMs propose; deterministic code verifies; human authorizes. |
| **Q3: How do you prevent duplicate or incorrect refunds?** | **Code-level financial guardrails & idempotency keys.**<br>1. Idempotency keys (`hash(order_id, return_id, transaction_type)`) block duplicate execution at the mock API layer.<br>2. Ledgers enforce: $\text{amount} \le \min(₹4,999, \text{remaining refundable amount}, \text{order paid amount})$.<br>3. LLMs possess **zero access** to financial release tools; refunds are created in draft state `pending_return_receipt` awaiting merchant cryptographic/UI authorization. | **Mathematical refund ceiling** and backend-enforced transaction idempotency. |

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
│       ├── studio_white_headphones.png  # Store catalog ground truth photo (HEAD-WHT-02, Matte White)
│       ├── unboxing_black_headphones.png # Customer video unboxing frame at 00:07 (Midnight Black)
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
- **Headline**: `RETURNLENS` — *“Every return decision, backed by evidence.”*
- **Value Proposition**: Evidence-backed returns triage agent for solo direct-to-consumer online sellers.
- **Scope Guardrails**: Return triage core + 1 zero-vision order-status route. Fail-closed architecture; no autonomous refunds.
- **Visual Anchor**: Seller Review Console mockup featuring Case RT-1042 / ORD-8821 with inspection frame 00:14, store truth (`HEAD-WHT-02`, ₹4,999), honest visual observation (*“Potential casing damage flagged · Requires manual confirmation”*), policy verification (`P-01 FLAGGED FOR REVIEW`, `P-04 PASS`), status `READY FOR SELLER REVIEW (FLAGGED)`, and 1-click draft authorization.

### Slide 2: The Problem as a Visual Story (3-Column Zero-Overlap Layout)
- **Tag**: `The Problem · Solo Seller Bottleneck`
- **Headline**: `One return decision. Four disconnected sources.`
- **Subtitle**: *Sellers decide returns from memory today. ReturnLens assembles one trace before money moves.*
- **Visual Layout**: 3-column composition without overlap:
  - *Left Column*: Source 01 (Buyer Chat: “Received damaged item”, 30–60s video) & Source 03 (Courier Tracking: Delivered 4 days ago, Shippo mock API scan).
  - *Center Pillar (Critical Gap)*: **`Four systems. No traceable decision.`** · **`NO SHARED EVIDENCE RECORD`** — *Today the seller opens 4 tabs, then decides alone. A wrong refund loses inventory; an unfair denial loses a customer. The gap is that no single record ties order truth, video frames, policy clauses, and decisions together.*
  - *Right Column*: Source 02 (Order Record: White Headphones, ₹4,999, Shopify mock API) & Source 04 (Return Policy: 7-day window, sealed tag, code rules P-01 to P-08).
- **Sourced Signal**: Fraud estimates differ by definition: **9%** (*NRF 2025, fraud only*) vs **15.14%** (*Appriss/Deloitte 2024, fraud + abuse*).

### Slide 3: The Star Demo (Visual Evidence Benchmark)
- **Tag**: `Star Demo · Visual Grounding & Color Contradiction`
- **Headline**: `The order says white. The video shows black.`
- **Subtitle**: *ReturnLens extracts keyframes, flags color discrepancies, and halts auto-payout for seller approval.*
- **Visual Contrast**:
  - *Left Card (Order Ground Truth)*: Studio photo of `HEAD-WHT-02` (Matte White, ₹4,999, delivered 4 days ago, tag present).
  - *Center Badge*: `COLOR CONTRADICTION`.
  - *Right Card (Video Keyframe)*: Customer unboxing frame at `00:07` showing Midnight Black item. Grounded citation explicitly notes: *“Observed Color: Midnight Black · Exact SKU: Not verified · Tag: Not visible in cited frame”*.
- **Deterministic Policy Gate**:
  - Rule `P-03 Check: COLOR CONTRADICTION`.
  - Plan Schema: `typed JSON, requires_seller_approval: true`.
  - Status: `STATUS: ESCALATE (SELLER REVIEW REQUIRED)` — Color contradiction observed; exact SKU unverified; automated return label and refund payout inhibited.
  - **3 Seller Options**:
    1. Request unboxing video with packaging label / serial number visible.
    2. Reject return under Clause 4.2 (Item does not match order record).
    3. Override & approve if seller acknowledges known warehouse fulfillment error.
  - **Financial Cap**: $0 < \text{amount} \le \min(₹4,999, \text{remaining refundable amount}, \text{order paid amount})$.

### Slide 4: System Architecture (Dynamic Agentic Governance)
- **Tag**: `System Architecture · Dynamic Agentic Governance`
- **Headline**: `Models observe. Code verifies. Seller authorizes.`
- **Subtitle**: *Dynamic action selection and stateful resumption under deterministic human authorization.*
- **6-Step Pipeline**:
  $$\text{01 PLAN [MODEL]} \longrightarrow \text{02 RETRIEVE [CODE]} \longrightarrow \text{03 EVALUATE [CODE]} \longrightarrow \text{04 AUDIT [MODEL]} \longrightarrow \text{05 AUTHORIZE [HUMAN]} \longrightarrow \text{06 RECORD [CODE]}$$
- **Dual Operational Branches**:
  - *Dynamic Stateful Clarification Loop (Case C)*: $\text{Dark Frames} \longrightarrow \text{ask\_for\_evidence()} \longrightarrow \text{WAITING\_FOR\_EVIDENCE} \longrightarrow \text{Customer Uploads} \longrightarrow \text{Resume Case}$
  - *Secondary PS-04 Order Status Fast Path*: $\text{Query: “Where is my order?”} \longrightarrow \text{Mock Store API} \longrightarrow \text{Courier Scan} \longrightarrow \text{Instant Delivery Timestamp}$
- **4 Decision Function Outcomes (Strict Priority Order)**:
  1. `Contradiction → Escalate`: Discrepancy flagged (e.g. Case B); inhibits automated label and refund draft.
  2. `Hard Fail → Escalate`: Mandatory rule violation (e.g. expired return window); seller decides; never auto-deny.
  3. `Unclear Only → Ask More`: Low brightness or blurry barcode (e.g. Case C); exact re-film checklist (1 retry limit).
  4. `All Pass → Approve Review`: All clauses pass (e.g. Case A); prepares mock label and drafts refund in `pending_return_receipt`.
- **Core Architecture Guarantees**:
  - *Model Calls*: Bounded design estimate (3 base calls: planner, vision, critic + retries).
  - *Policy Rules*: Deterministic Python code rules `P-01` to `P-08`, never prompts.
  - *Critic Duty*: Reviews cited frames and flags unsupported observations (correlated error limits noted).
  - *Safety Boundary*: Backend authorization boundary — LLMs cannot execute financial refund tools.

### Slide 5: Four Demo Benchmark Scenarios
- **Tag**: `Demo Scenarios · Controlled Prototype Behaviors`
- **Headline**: `Four scenarios. Four predictable behaviors.`
- **Subtitle**: *Expected prototype behaviors across staged benchmark cases. Not measured production metrics.*
- **4 Reproducible Benchmark Cases**:
  - **Case A · Ready (`ORD-1042`, ₹4,999)**:
    - *Evidence*: Verified Damage · Staged cosmetic crack, timestamp 00:04 · Defect verified.
    - *Expected Action*: Agent prepares mock label & draft refund in `pending_return_receipt`; seller one-click confirms.
  - **Case B · Mismatch (Color Contradiction - Core Benchmark)**:
    - *Evidence*: Color Contradiction · `HEAD-WHT-02` (White) ordered vs Frame 00:07 Black item · SKU unverified.
    - *Expected Action*: `P-03` contradiction blocks automation; seller selects 1 of 3 options: mis-shipment / box label / warehouse inspection.
  - **Case C · Unclear (Agentic Clarification Loop)**:
    - *Evidence*: Insufficient Visibility · 4-second dark video, brightness 28, only 2 usable frames.
    - *Expected Action*: Agent requests targeted photo; enters `WAITING_FOR_EVIDENCE`; resumes case on upload (1 retry limit).
  - **Case D · Context (Sequence Continuity)**:
    - *Evidence*: Sequence Continuity · Staged parcel-to-product take: opening sealed parcel to product reveal.
    - *Expected Action*: *Expected prototype behavior: inspect sequence continuity and flag missing transitions for seller review.*

### Slide 6: 24-Hour Execution & Feasibility
- **Tag**: `24-Hour Prototype Plan · Feasibility & Scope Guardrails`
- **Headline**: `Built for a 24-hour sprint.`
- **Subtitle**: *Strict scope boundaries and clear division of labor make the prototype fully buildable in one day.*
- **24-Hour Timeline Grid**:
  - `00h – 06h · Foundation`: **Mock APIs & Agent Core** · LangGraph skeleton, mock store/courier fixtures, order status route · *Owner: Person A (Backend), supported by C*
  - `06h – 12h`: **Evidence Pipeline & Policy** · FFmpeg keyframe indexer, Python rules P-01 to P-08, critic prompt · *Owner: Person B (Video & UI)*
  - `12h – 18h`: **State Flow & Scenarios** · End-to-end wiring, clarification/resume loop, seller console UI · *Owner: Person C (Integration), supported by A/B*
  - `18h – 24h`: **Testing & Submission** · Fallback testing, authorization tests, demo video recording, README · *All 3 Members*
- **Scope Discipline**:
  - **Never Cut (Core Engine)**: Deterministic policy engine (`P-01` to `P-08`), evidence-pack frame citation, fail-closed seller approval gate, structured JSON audit log, clarification/resume loop, 4 reproducible demo cases.
  - **Cut First If Behind (Deferred Expansion)**: Real carrier webhook integration (keep mock courier), multi-product order parsing (keep 1 item/return), custom video encoding (keep standard 1 fps FFmpeg extraction), production payment gateways / live WhatsApp webhooks, seller analytics dashboard.
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
