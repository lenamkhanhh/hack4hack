# ReturnLens 🔍
### Autonomous Evidence-Backed Return Triage Agent for Solo D2C Merchants
**AgentX Hackathon 2026 · Track PS-04 (Autonomous Support Agent)**  
**Team Rookie (3 Members) · 24-Hour Prototype Feasibility**

---

![ReturnLens Pitch Deck Preview](deliverables/ReturnLens_v4_preview.png)

## 📌 Executive Summary

**ReturnLens** is an evidence-backed returns triage agent tailored for solo direct-to-consumer (D2C) online sellers. 

When a customer submits a return request with a short unboxing video, ReturnLens:
1. Samples keyframes from the customer's video at ~1 fps via FFmpeg.
2. Extracts visual observations (color, visible cracks, barcode, packaging integrity) via multimodal vision.
3. Cross-references visual observations against store ground truth (Shopify/Shippo order manifests) and store policy rules (`P-01` to `P-08`).
4. Verifies timestamp citations via an independent critic loop to eliminate hallucinations.
5. Surfaces discrepancies to the merchant console and drafts a mock return shipping label or refund draft for **one-click human seller authorization**.

> **Core Philosophy:** *Models observe. Code verifies. Seller authorizes.*  
> No automatic customer denials. No mock refund or label is ever released without explicit merchant approval.

---

## 🏆 Pitch Deck Deliverables (Version 4 — Ground-up Redesign)

The pitch deck has been designed from scratch according to top-tier hackathon / YC demo standards: restrained, editorial Swiss typography (Inter + IBM Plex Mono), 16:9 widescreen, no generic AI cards, and photorealistic staged evidence.

| Format | File Path | Description |
| :--- | :--- | :--- |
| **PowerPoint** | [`deliverables/ReturnLens_v4.pptx`](deliverables/ReturnLens_v4.pptx) | Editable 16:9 widescreen presentation with native PowerPoint vector shapes, high-res photos, and comprehensive speaker notes on every slide. |
| **PDF Document** | [`deliverables/ReturnLens_v4.pdf`](deliverables/ReturnLens_v4.pdf) | Exactly 6-page submission PDF rendered directly from headless Edge engine with vector typography. |
| **Interactive HTML** | [`deliverables/ReturnLens_v4.html`](deliverables/ReturnLens_v4.html) | Standalone interactive 16:9 presentation with keyboard navigation (`←` / `→` / `Space`) and embedded base64 imagery. |
| **Contact Sheet** | [`deliverables/ReturnLens_v4_preview.png`](deliverables/ReturnLens_v4_preview.png) | High-resolution master overview image of all 6 slides (2304×1008px). |

---

## 🖼 Slide-by-Slide Overview

- **Slide 1 — Product Hero (One Glance):**
  - Left: Product name, value proposition, hackathon metadata (`Team Rookie · 3 Members · 24h Prototype`).
  - Right: Dominant **Seller Review Console Mockup** showing Frame `00:14`, order truth (`HEAD-WHT-02`, ₹1,499), defect bounding box, and one-click approval button.
- **Slide 2 — The Problem (Visual Convergence):**
  - Shows 4 disconnected sources (Buyer Chat, Order Record, Delivery Tracking, Return Policy) converging toward the central question: *"Approve, deny, or ask for more evidence?"*
  - Highlights the critical missing link: **`NO SHARED EVIDENCE RECORD`**.
- **Slide 3 — The Star Demo (Visual Evidence Benchmark):**
  - Direct visual contrast: Order Record (`Matte White, SKU HEAD-WHT-02`) vs. Customer Video Frame (`Midnight Black at 00:07`).
  - Prominent callout: **`COLOR MISMATCH`**.
  - Decision Gate: Flags `NEEDS SELLER REVIEW` with 2 seller actions (Check warehouse mis-shipment vs. Request label photo). **No automated denial.**
- **Slide 4 — System Architecture (Deterministic Pipeline):**
  - High-contrast dark theme (`#0D1814`) with a 6-step horizontal pipeline: `Buyer Request` → `Frame Extraction` → `Model Observation` → `Policy Engine` → `Evidence Critic` → `Seller Gate`.
  - Color-coded governance: **Model (Teal)**, **Code (White)**, **Human (Amber)**.
  - 3 decision branches: Unclear Evidence (retry), Contradiction (seller review), All Checks Pass (1-click approval).
- **Slide 5 — Four Benchmark Scenarios:**
  - `READY`: Visible defect at `00:14`, matching SKU $\rightarrow$ Prepare seller approval.
  - `MISMATCH`: Black received vs White ordered at `00:07` $\rightarrow$ Seller review.
  - `UNCLEAR`: Blurry barcode at `00:02` $\rightarrow$ Targeted automated prompt for clear photo.
  - `CONTEXT`: Crushed outer carton with intact tape at `00:11` $\rightarrow$ Approve with carrier transit claim note.
- **Slide 6 — 24-Hour Execution & Scope:**
  - Horizontal timeline (`0h`–`6h` Skeleton, `6h`–`12h` Pipeline & Policy, `12h`–`18h` Integration & Scenarios, `18h`–`24h` Demo & Polish).
  - Explicit scope boundaries: **IN SCOPE** (Mock APIs, Staged Video, 1-Click Console, Deterministic Rules, Audit Log) vs. **OUT OF SCOPE** (Real payments, multi-seller, WhatsApp webhooks).

---

## 📂 Repository Structure

```text
hack4hack/
├── deliverables/                     # Official v4 submission artifacts
│   ├── ReturnLens_v4.pptx            # Native editable PowerPoint deck (16:9)
│   ├── ReturnLens_v4.pdf             # 6-page presentation PDF
│   ├── ReturnLens_v4.html            # Standalone interactive HTML deck
│   └── ReturnLens_v4_preview.png     # Full 6-slide preview contact-sheet
│
├── src/                              # Source code, generators, and assets
│   ├── build_v4_pptx.py              # Python script generating native PPTX with python-pptx
│   ├── generate_v4_html.py           # Python script compiling HTML deck with embedded base64 assets
│   └── assets/                       # Staged photos, video frames, and slide renders
│       ├── demo_white_order.jpg      # Store ground truth catalog photo (Matte White)
│       ├── demo_black_frame.jpg      # Customer video unboxing frame at 00:07 (Midnight Black)
│       ├── hero_video_frame.jpg      # Defect inspection frame at 00:14 with bounding box
│       ├── studio_white_headphones.jpg
│       ├── unboxing_black_headphones.jpg
│       └── slides/                   # High-resolution (2000x1125) renders of slides 1 to 6
│
├── research/                         # Background research & problem analysis
│   └── AgentX_Idea_Research.html     # Deep dive on 7 AgentX problem statements & market friction
│
├── archive/                          # Iteration history preserved for reference
│   ├── v3/                           # Version 3 deck, scripts, and initial graphics
│   ├── v2_redesigned/                # Version 2 redesign
│   ├── v1_swiss/                     # Version 1 Swiss typographic prototype
│   └── v0_initial/                   # Initial brainstorming drafts
│
├── .gitignore
└── README.md
```

---

## 👥 Team Rookie (AgentX Hackathon 2026)

- **Person A (Backend & Agent Graph):** LangGraph state machine, deterministic policy logic (`P-01` to `P-08`), critic verification loop, structured JSON audit log.
- **Person B (Multimodal Vision & UI):** FFmpeg keyframe pipeline, image indexer, Streamlit/Web seller review console, bounding box overlay renderer.
- **Person C (Integration & Benchmark Data):** Staged Shopify/Shippo mock APIs, 4 demo test datasets (Cases A–D), boundary testing, demo video recording, and submission documentation.

---

## 📜 Disclosure on Staged Data & Financial Guardrails

- All product SKUs (`HEAD-WHT-02`), order numbers (`#ORD-9021`), customer video clips, and carrier shipping labels are **staged prototype assets / mock data** created for demonstration purposes without real customer PII.
- Refund releases in the prototype environment are constrained by a deterministic code-level cap:  
  $$\text{Cap} = \min(₹4,999, \text{remaining refundable amount}, \text{order paid amount})$$
- No live banking or production payment gateways are connected.

