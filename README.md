# ReturnLens 🔍
### Autonomous Evidence-Backed Return Triage Agent for Solo D2C Merchants
**AgentX Hackathon 2026 · Track PS-04 (Autonomous Support Agent)**  
**Team Rookie (3 Members) · 24-Hour Prototype Feasibility**

---

![ReturnLens Pitch Deck Preview](deliverables/ReturnLens_v7_preview.png)

## 📌 Project Overview & Current Stage

> **Submission Scope:** **Idea Round Prototype Proposal (v7 Final Competition Edition)**  
> This repository contains the official pitch deck, canonical content specification, generation engine, staged benchmark evidence, and verified build pipeline. It defines the architecture, deterministic policy rules, and 24-hour execution roadmap for the hackathon prototype. It is not an existing live commercial deployment.

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

## 🎨 Design Philosophy: ReturnLens v7 (Final Competition Edition)

The ReturnLens v7 presentation system was designed under the creative direction of a Principal Product Designer and Senior Technical Architect:
> **“Swiss editorial design × premium SaaS product UI × technical information graphics.”**

### Key Improvements over Previous Editions:
1. **Geometric Perfection (Slide 1):** Action buttons sit at $y = 5.34"$ with bottom at $y = 5.72" \le 5.85"$, console padding below buttons is exactly **0.22 inches** (eliminating v6's 0.63" hollow space), and clearance to footer ($y = 7.00"$) is **1.28 inches** ($> 1.10"$). Realistic macOS traffic-light buttons (Red `#FF5F56`, Yellow `#FFBD2E`, Green `#27C93F`) are natively rendered on the window titlebar.
2. **True Information Flow (Slide 2):** Four distinct source cards (`SOURCE 01` to `04`) converge toward a prominent dark evidence-gap region (`“What verifiable evidence justifies moving this money?”`), paired with two distinct, separately sourced editorial callouts:
   - **9.0% Return Fraud** (NRF 2025, criminal fraud only)
   - **15.14% Abuse** (Appriss/Deloitte 2024, criminal fraud + policy abuse)
3. **Exhibition Evidence Comparison (Slide 3):** High-resolution side-by-side catalog truth vs unboxing evidence with a central coral mismatch pill (`≠`), grounded metadata, and three interactive-style action pills: (1) Accept warehouse mis-shipment, (2) Request outside-box shipping label photo, (3) Hold return for physical parcel inspection.
4. **Deep Obsidian Architecture Blueprint (Slide 4):** Premium dark canvas (`#0B1613`) with a 6-stage pipeline (all 3 model calls explicitly badged), three architectural pillars (Call budget, Case C state-transition loop with 1-retry termination rule, and Tiny PS-04 fast path), plus cryptographic approval binding.
5. **Asymmetric Evaluation Suite (Slide 5):** 45% Case B hero card with embedded video frame thumbnail and grounded observations, alongside 3 compact evidence-to-outcome mini-stories for Cases A, C, and D.
6. **24-Hour Horizontal Roadmap (Slide 6):** Four milestone phase badges across a Gantt-style timeline (00–24h), three enriched Person Cards with 4 deliverables each (updated to `Extended smoke runner (10+ tests)` for Person C), and a prominent dual-band scope boundary (`MUST DELIVER` vs `CUT FIRST IF BEHIND`).

---

## 🎯 Track PS-04 Alignment (Primary & Secondary Routes)

While ReturnLens differentiates itself through **multimodal, video-backed return triage** (solving the solo seller's most expensive problem), it also covers routine customer support inquiries under Problem Statement PS-04:
- **Primary Video Triage Route:** Analyzes customer unboxing footage, checks policies P-01–P-08, extracts timestamp citations, and prepares human-in-the-loop authorization.
- **Secondary Order Status Route (Zero-Vision Fast Path):** When a buyer asks *"Where is my order?"*, the agent directly reuses the mock Shopify and Shippo APIs to return real-time delivery timestamps and courier status scans, escalating to the seller only if courier delay thresholds are exceeded.

---

## 🧠 Technical Defensibility & Judge Q&A Defense

| Question / Concern | Technical Mechanism in ReturnLens | Architecture Guarantee |
| :--- | :--- | :--- |
| **Q1: Why is this an agent rather than a hardcoded workflow?** | **Dynamic state machine with conditional branching & pause/resume.**<br>In Case C, upon detecting low-light video (brightness 28/255), the agent dynamically halts normal execution, calls `ask_for_evidence()` with specific re-filming guidance, transitions the state machine to `WAITING_FOR_EVIDENCE`, pauses execution, and resumes the exact ticket context when new evidence arrives (1 retry limit). Conversely, routine order queries take a zero-vision fast path directly querying mock store and courier APIs. | **Stateful resumption & adaptive tool selection** rather than static linear scripting. |
| **Q2: What happens if vision or critic models hallucinate?** | **Observations are non-binding; code enforces business truth.**<br>Vision model outputs (`observed_color`, `damage_flag`) are treated strictly as observation metadata. Hard constraints (7-day delivery window from courier scans, SKU comparisons) are verified in deterministic Python (`P-01` to `P-08`). The critic provides an adversarial sanity check against cited timestamps. If both models suffer correlated errors, the **fail-closed human gate** ensures no refund or label is ever issued without seller review. | **Zero autonomous execution.** LLMs propose; deterministic code verifies; human authorizes. |
| **Q3: How do you prevent duplicate or incorrect refunds?** | **Code-level financial guardrails & idempotency keys.**<br>1. Idempotency keys (`hash(order_id, return_id, transaction_type)`) block duplicate execution at the mock API layer.<br>2. Ledgers enforce: $\text{amount} \le \min(₹4,999, \text{remaining refundable amount}, \text{order paid amount})$.<br>3. LLMs possess **zero access** to financial release tools; refunds are created in draft state `pending_return_receipt` awaiting merchant cryptographic/UI authorization. | **Mathematical refund ceiling** and backend-enforced transaction idempotency. |

---

## 📦 Verified Deliverables & Repository Map

All deliverables are generated from source code and maintained in both the repository root and `deliverables/`:

| Deliverable | File Path | Verified Specifications |
| :--- | :--- | :--- |
| **Flagship PowerPoint Deck (v7)** | [`ReturnLens_v7.pptx`](ReturnLens_v7.pptx) / [`deliverables/ReturnLens_v7.pptx`](deliverables/ReturnLens_v7.pptx) | **Primary Submission Artifact:** Native editable 16:9 presentation (13.333×7.5"), embedded high-res photo assets, vector shapes, and **verified speaker notes on all 6 slides** (~1.2 MB package). |
| **Flagship Vector PDF (v7)** | [`ReturnLens_v7.pdf`](ReturnLens_v7.pdf) / [`deliverables/ReturnLens_v7.pdf`](deliverables/ReturnLens_v7.pdf) | Exactly 6-page vector PDF (16:9, 960×540 pt) rendered via headless browser with zero box clipping. |
| **Flagship Interactive HTML (v7)** | [`ReturnLens_v7.html`](ReturnLens_v7.html) / [`index.html`](index.html) | Standalone interactive HTML presentation with embedded base64 assets, keyboard shortcuts (`O` Overview, `N` Notes). |
| **Flagship Preview Sheet (v7)** | [`ReturnLens_v7_preview.png`](ReturnLens_v7_preview.png) | High-resolution 2352×882 master 6-slide contact sheet preview (3×2 grid). |
| **High-Res PPTX Renders (v7)** | [`src/assets/v7_pptx_renders/`](src/assets/v7_pptx_renders/) | 6 high-resolution PNG slides exported directly from PowerPoint COM for visual verification. |
| **Comprehensive QA Report (v7)** | [`V7_QA_REPORT.md`](V7_QA_REPORT.md) | Slide-by-slide audit, geometric measurements, test results, and historical preservation report. |
| **Canonical Content Spec** | [`content/deck_data.json`](content/deck_data.json) | Single source of truth containing verified copy, metrics, policy rules, and technical speaker notes consumed by both HTML and PPTX generators. |
| **Historical Editions** | `ReturnLens_v6.*` / `ReturnLens_v5.*` / `ReturnLens_v4.*` | Complete historical artifacts preserved with 100% byte-identical SHA256 integrity. |

```text
hack4hack/
├── content/                          # Single Source of Truth
│   └── deck_data.json                # Canonical presentation content, prices, and notes
│
├── deliverables/                     # Official submission artifacts
│   ├── ReturnLens_v7.pptx            # Flagship native editable PowerPoint deck (16:9) with notes
│   ├── ReturnLens_v7.pdf             # Flagship 6-page vector PDF (16:9, 960x540 pt)
│   ├── ReturnLens_v7.html            # Flagship standalone interactive HTML deck
│   ├── ReturnLens_v7_preview.png     # Flagship 6-slide preview contact-sheet (2352x882)
│   ├── ReturnLens_v6.*               # Historical v6 visual redesign artifacts
│   ├── ReturnLens_v5.*               # Historical v5 hardened baseline artifacts
│   └── ReturnLens_v4.*               # Historical v4 initial baseline artifacts
│
├── src/                              # Source code, generators, and assets
│   ├── build_v7_pptx.py              # Flagship Python script generating native v7 PPTX
│   ├── generate_v7_html.py           # Flagship Python script compiling v7 HTML, PDF & preview
│   ├── build_v6_pptx.py              # Historical v6 PPTX builder
│   ├── generate_v6_html.py           # Historical v6 HTML generator
│   ├── build_v5_pptx.py              # Historical v5 PPTX builder
│   ├── generate_v5_html.py           # Historical v5 HTML generator
│   └── assets/                       # Staged photos, video frames, and slide renders
│       ├── studio_white_headphones.jpg   # Store catalog ground truth photo (HEAD-WHT-02, Matte White)
│       ├── unboxing_black_headphones.jpg # Customer video unboxing frame at 00:07 (Midnight Black)
│       ├── v7_pptx_renders/              # 6 high-res PNGs rendered directly from PPTX
│       └── slides/                       # Historical rendered slide PNGs
│
├── scripts/                          # Automated testing and verification
│   └── smoke_test.py                 # Extended QA suite validating v7, media, geometry & v5/v6 lock
│
├── V7_QA_REPORT.md                   # Detailed visual & technical QA audit report
├── requirements.txt                  # Python build dependencies
├── ReturnLens_v7.html                # Flagship root deliverable (matches deliverables/)
├── ReturnLens_v7.pdf                 # Flagship root deliverable (matches deliverables/)
├── ReturnLens_v7.pptx                # Flagship root deliverable (matches deliverables/)
├── ReturnLens_v7_preview.png         # Flagship root deliverable (matches deliverables/)
├── index.html                        # GitHub Pages entry point (Flagship v7)
└── README.md                         # Project documentation and review guide
```

---

## 🚀 Quickstart: Build & Validate

To build all deliverables and run the comprehensive QA test suite from scratch:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Build native PowerPoint deck (v7)
python src/build_v7_pptx.py

# 3. Compile interactive HTML, vector PDF, and contact sheet preview (v7)
python src/generate_v7_html.py

# 4. Run automated QA smoke test suite (10/10)
python scripts/smoke_test.py
```
