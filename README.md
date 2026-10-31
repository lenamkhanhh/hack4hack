# ReturnLens 🔍
### Autonomous Evidence-Backed Return Triage Agent for Solo D2C Merchants
**AgentX Hackathon 2026 · Track PS-04 (Autonomous Support Agent)**  
**Team Rookie (3 Members) · 24-Hour Prototype Feasibility**

---

![ReturnLens Pitch Deck Preview](deliverables/ReturnLens_v7_1_preview.png)

## 📌 Project Overview & Current Stage

> **Submission Scope:** **Idea Round Prototype Proposal (v7.1 Submission Freeze Candidate)**  
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

## 🎨 ReturnLens v7.1 — Final Precision & Submission Freeze Candidate

The ReturnLens v7.1 release builds directly on the acclaimed v7 Swiss editorial presentation architecture, implementing targeted evidentiary hardening, deterministic build reproducibility, offline font resilience, and automated verification:

### Key Precision Refinements in v7.1:
1. **Case B Decision CTA Precision (Slide 1):** The primary console action button is calibrated to **`"Review Evidence & Decide"`** (in place of `"Review & Authorize"`), accurately reflecting that Case B contains a policy contradiction where no refund is authorized and the merchant must choose between three distinct resolution paths.
2. **Exact SKU Grounding Hardening (Slide 1, 3, 5):** Slide 1 features the precise notice:
   > `P-03 COLOR CONTRADICTION: Observed black casing conflicts with ordered Matte White specification. Exact SKU unverified.`  
   Formatted at 7.5pt Consolas with zero boundary clipping.
3. **Case C Policy P-06 & Brightness Standardization (Slides 4 & 5):** Standardized all low-light video re-film triggers to **`Policy P-06`** (Evidence Quality & Illumination) and standardized wording to **`brightness score: 28/255`**.
4. **Fraud Metrics Disambiguation (Slide 2):** Clearly separated industry benchmarks:
   - `• 9.0% — Return Fraud (NRF 2025: criminal only)`: Strict criminal fraud (unboxing swaps, empty boxes).
   - `• 15.14% — Fraud + Policy Abuse (Appriss/Deloitte 2024: criminal + abuse)`: Criminal fraud combined with policy abuse (wardrobing).
5. **Person C Deliverable Alignment (Slide 6):** Synchronized Person C's automated testing deliverable to cite **`10-test smoke suite`**, matching the actual smoke test suite count.
6. **Deterministic & Offline-Resilient Pipeline:**
   - Engineered zip timestamp normalization in `src/build_v7_1_pptx.py` for byte-identical, reproducible PPTX builds.
   - Comprehensive system font fallbacks (`Inter`, `Segoe UI`, `Calibri`, `system-ui` and `IBM Plex Mono`, `Consolas`, `monospace`) for offline judging.
   - Fresh 1920×1080 slide renders in `src/assets/v7_1_pptx_renders/` bound via `render_manifest.json`.

---

## 🎯 Track PS-04 Alignment (Primary & Secondary Routes)

While ReturnLens differentiates itself through **multimodal, video-backed return triage** (solving the solo seller's most expensive problem), it also covers routine customer support inquiries under Problem Statement PS-04:
- **Primary Video Triage Route:** Analyzes customer unboxing footage, checks policies P-01–P-08, extracts timestamp citations, and prepares human-in-the-loop authorization.
- **Secondary Order Status Route (Zero-Vision Fast Path):** When a buyer asks *"Where is my order?"*, the agent bypasses vision models completely:
  $$\text{Buyer Query} \longrightarrow \text{Store API (Shopify)} \longrightarrow \text{Courier API (Shippo)} \longrightarrow \text{Status Reply}$$
  This saves 100% of vision tokens and responds in under 500ms.

---

## 📦 Verified Deliverables & Artifacts (v7.1 Flagship)

All deliverables are generated from source code and maintained in both the repository root and `deliverables/`:

| Deliverable | File Path | Verified Specifications |
| :--- | :--- | :--- |
| **Flagship PowerPoint Deck (v7.1)** | [`ReturnLens_v7_1.pptx`](ReturnLens_v7_1.pptx) / [`deliverables/ReturnLens_v7_1.pptx`](deliverables/ReturnLens_v7_1.pptx) | **Primary Submission Artifact:** Native editable 16:9 presentation (13.333×7.5"), embedded high-res photo assets, vector shapes, deterministic build, and **verified speaker notes on all 6 slides** (~1.2 MB package). |
| **Flagship Vector PDF (v7.1)** | [`ReturnLens_v7_1.pdf`](ReturnLens_v7_1.pdf) / [`deliverables/ReturnLens_v7_1.pdf`](deliverables/ReturnLens_v7_1.pdf) | Exactly 6-page vector PDF (16:9, 960×540 pt) rendered via headless browser with zero box clipping. |
| **Flagship Interactive HTML (v7.1)** | [`ReturnLens_v7_1.html`](ReturnLens_v7_1.html) / [`index.html`](index.html) | Standalone interactive HTML presentation with embedded base64 assets, keyboard shortcuts (`O` Overview, `N` Notes), offline system font fallbacks. |
| **Flagship Preview Sheet (v7.1)** | [`ReturnLens_v7_1_preview.png`](ReturnLens_v7_1_preview.png) | High-resolution 2352×882 master 6-slide contact sheet preview (3×2 grid). |
| **High-Res PPTX Renders (v7.1)** | [`src/assets/v7_1_pptx_renders/`](src/assets/v7_1_pptx_renders/) | 6 high-resolution PNG slides exported directly from PowerPoint COM for visual verification + `render_manifest.json`. |
| **Comprehensive QA Report (v7.1)** | [`V7_1_QA_REPORT.md`](V7_1_QA_REPORT.md) | Slide-by-slide audit, geometric measurements, test results, and historical preservation report. |
| **Canonical Content Spec** | [`content/deck_data.json`](content/deck_data.json) | Single source of truth containing verified copy, metrics, policy rules, and technical speaker notes consumed by both HTML and PPTX generators. |
| **Historical Editions** | `ReturnLens_v7.*` / `ReturnLens_v6.*` / `ReturnLens_v5.*` / `ReturnLens_v4.*` | Complete historical artifacts preserved with 100% byte-identical SHA256 integrity. |

```text
hack4hack/
├── content/                          # Single Source of Truth
│   └── deck_data.json                # Canonical presentation content, prices, and notes
│
├── deliverables/                     # Official submission artifacts
│   ├── ReturnLens_v7_1.pptx          # Flagship native editable PowerPoint deck (16:9) with notes
│   ├── ReturnLens_v7_1.pdf           # Flagship 6-page vector PDF (16:9, 960x540 pt)
│   ├── ReturnLens_v7_1.html          # Flagship standalone interactive HTML deck
│   ├── ReturnLens_v7_1_preview.png   # Flagship 6-slide preview contact-sheet (2352x882)
│   ├── ReturnLens_v7.*               # Historical v7 final competition edition artifacts
│   ├── ReturnLens_v6.*               # Historical v6 visual redesign artifacts
│   ├── ReturnLens_v5.*               # Historical v5 hardened baseline artifacts
│   └── ReturnLens_v4.*               # Historical v4 initial baseline artifacts
│
├── src/                              # Source code, generators, and assets
│   ├── build_v7_1_pptx.py            # Flagship Python script generating native v7.1 PPTX
│   ├── generate_v7_1_html.py         # Flagship Python script compiling v7.1 HTML, PDF & preview
│   ├── build_v7_pptx.py              # Historical v7 PPTX builder
│   ├── generate_v7_html.py           # Historical v7 HTML generator
│   ├── build_v6_pptx.py              # Historical v6 PPTX builder
│   ├── generate_v6_html.py           # Historical v6 HTML generator
│   ├── build_v5_pptx.py              # Historical v5 PPTX builder
│   ├── generate_v5_html.py           # Historical v5 HTML generator
│   └── assets/                       # Staged photos, video frames, and slide renders
│       ├── studio_white_headphones.jpg   # Store catalog ground truth photo (HEAD-WHT-02, Matte White)
│       ├── unboxing_black_headphones.jpg # Customer video unboxing frame at 00:07 (Midnight Black)
│       ├── v7_1_pptx_renders/            # 6 high-res PNGs rendered directly from PPTX + manifest
│       ├── v7_pptx_renders/              # Historical v7 slide PNGs
│       └── slides/                       # Historical rendered slide PNGs
│
├── scripts/                          # Automated testing and verification
│   └── smoke_test.py                 # 10-test QA suite validating v7.1, media, geometry & v5/v6/v7 lock
│
├── V7_1_QA_REPORT.md                 # Detailed visual & technical QA audit report (v7.1)
├── V7_QA_REPORT.md                   # Historical v7 QA report
├── requirements.txt                  # Python build dependencies
├── ReturnLens_v7_1.html              # Flagship root deliverable (matches deliverables/)
├── ReturnLens_v7_1.pdf               # Flagship root deliverable (matches deliverables/)
├── ReturnLens_v7_1.pptx              # Flagship root deliverable (matches deliverables/)
├── ReturnLens_v7_1_preview.png      # Flagship root deliverable (matches deliverables/)
├── index.html                        # GitHub Pages entry point (Flagship v7.1)
└── README.md                         # Project documentation and review guide
```

---

## 🚀 Quickstart: Build & Validate

To build all deliverables and run the comprehensive QA test suite from scratch:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Build native PowerPoint deck (v7.1)
python src/build_v7_1_pptx.py

# 3. Compile interactive HTML, vector PDF, and contact sheet preview (v7.1)
python src/generate_v7_1_html.py

# 4. Run automated QA smoke test suite (10/10)
python scripts/smoke_test.py
```

---

## ⚖️ License & Attribution

ReturnLens is an architectural prototype designed for the **AgentX Hackathon 2026 (Track PS-04)** by **Team Rookie**.  
All rights reserved. Released under the MIT License for competition review.
