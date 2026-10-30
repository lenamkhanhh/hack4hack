import base64
import os

with open(r"D:\Code\Code\AIO\Code\ZaloAIC\assets_v3\product_white_headphones.png", "rb") as f:
    b64_white = base64.b64encode(f.read()).decode("utf-8")

with open(r"D:\Code\Code\AIO\Code\ZaloAIC\assets_v3\video_frame_black_headphones.png", "rb") as f:
    b64_black = base64.b64encode(f.read()).decode("utf-8")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ReturnLens — AgentX Hackathon 2026 (PS-04)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    :root {{
      --bg-light: #F5F3EF;
      --bg-white: #FFFFFF;
      --bg-dark: #0D1814;
      --bg-dark-card: #14221D;
      --bg-dark-line: #1F342C;
      --text-dark: #172621;
      --text-muted: #5A6661;
      --text-light: #EDEBE6;
      --text-light-muted: #95A39D;
      --accent-teal: #006B55;
      --accent-teal-soft: #E6F3EE;
      --accent-amber: #D88C31;
      --accent-amber-soft: #FBF2E6;
      --accent-red: #C53929;
      --border-line: #E2DFD8;
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-mono: 'IBM Plex Mono', ui-monospace, Menlo, Consolas, monospace;
    }}

    body {{
      background-color: #242726;
      font-family: var(--font-sans);
      color: var(--text-dark);
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 32px;
      padding: 40px 20px;
      -webkit-font-smoothing: antialiased;
    }}

    /* 16:9 Presentation Canvas: 1280px x 720px */
    .slide {{
      width: 1280px;
      height: 720px;
      position: relative;
      background-color: var(--bg-light);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 50px 64px 38px 64px;
      box-shadow: 0 12px 36px rgba(0, 0, 0, 0.4);
      border-radius: 0px; /* Sharp corners */
    }}

    .slide.dark-theme {{
      background-color: var(--bg-dark);
      color: var(--text-light);
    }}

    /* Header & Tag Typography */
    .slide-header {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}

    .label-tag {{
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--accent-teal);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .slide.dark-theme .label-tag {{
      color: #3EC9B6;
    }}

    h1.slide-title {{
      font-size: 38px;
      font-weight: 700;
      line-height: 1.15;
      letter-spacing: -0.025em;
      color: var(--text-dark);
    }}

    .slide.dark-theme h1.slide-title {{
      color: #FFFFFF;
    }}

    p.slide-sub {{
      font-size: 16px;
      color: var(--text-muted);
      line-height: 1.35;
      margin-top: 2px;
    }}

    .slide.dark-theme p.slide-sub {{
      color: var(--text-light-muted);
    }}

    /* Footer */
    .slide-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 14px;
      border-top: 1px solid var(--border-line);
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--text-muted);
      letter-spacing: 0.04em;
    }}

    .slide.dark-theme .slide-footer {{
      border-top-color: var(--bg-dark-line);
      color: var(--text-light-muted);
    }}

    .mono {{
      font-family: var(--font-mono);
    }}

    /* Print Styles for Perfect 16:9 PDF Export */
    @page {{
      size: 1280px 720px;
      margin: 0;
    }}
    @media print {{
      body {{
        background: transparent !important;
        padding: 0 !important;
        gap: 0 !important;
      }}
      .slide {{
        box-shadow: none !important;
        page-break-after: always;
        break-after: page;
      }}
      .nav-controls {{
        display: none !important;
      }}
    }}

    .nav-controls {{
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: rgba(17, 17, 17, 0.85);
      backdrop-filter: blur(8px);
      padding: 8px 16px;
      border-radius: 4px;
      color: #FFF;
      font-family: var(--font-mono);
      font-size: 12px;
      display: flex;
      gap: 12px;
      z-index: 9999;
    }}
    .nav-controls button {{
      background: var(--accent-teal);
      border: none;
      color: #FFF;
      padding: 4px 10px;
      border-radius: 2px;
      cursor: pointer;
      font-family: inherit;
    }}

    /* =========================================
       SLIDE 1: PRODUCT INTRODUCTION
    ========================================= */
    .s1-grid {{
      display: grid;
      grid-template-columns: 1.15fr 1fr;
      gap: 48px;
      align-items: center;
      flex: 1;
    }}

    .s1-left {{
      display: flex;
      flex-direction: column;
      gap: 18px;
    }}

    .brand-title {{
      font-size: 64px;
      font-weight: 700;
      letter-spacing: -0.04em;
      color: var(--text-dark);
      line-height: 1;
    }}

    .brand-lead {{
      font-size: 26px;
      font-weight: 600;
      line-height: 1.25;
      color: var(--accent-teal);
      letter-spacing: -0.015em;
    }}

    .brand-desc {{
      font-size: 15.5px;
      line-height: 1.5;
      color: var(--text-muted);
      max-width: 500px;
    }}

    .meta-badges {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 6px;
    }}

    .badge {{
      display: inline-block;
      font-family: var(--font-mono);
      font-size: 11px;
      padding: 5px 12px;
      background: var(--bg-white);
      border: 1px solid var(--border-line);
      color: var(--text-dark);
      font-weight: 500;
    }}

    .hero-evidence-card {{
      background: var(--bg-white);
      border: 1px solid var(--border-line);
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}

    .card-header-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border-line);
      padding-bottom: 12px;
    }}

    .card-tag {{
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 600;
      background: var(--accent-amber-soft);
      color: var(--accent-amber);
      padding: 4px 10px;
    }}

    .card-item-row {{
      display: grid;
      grid-template-columns: 80px 1fr;
      gap: 16px;
      align-items: center;
    }}

    .item-thumbnail {{
      width: 80px;
      height: 80px;
      background: #F0ECE1;
      border: 1px solid var(--border-line);
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }}

    .item-specs h4 {{
      font-size: 14.5px;
      font-weight: 600;
      color: var(--text-dark);
    }}

    .item-specs p {{
      font-size: 12px;
      color: var(--text-muted);
      font-family: var(--font-mono);
      margin-top: 2px;
    }}

    .video-proof-box {{
      background: #171A1E;
      color: #FFF;
      padding: 14px;
      font-size: 12px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}

    .video-proof-box .time-badge {{
      font-family: var(--font-mono);
      font-size: 10.5px;
      background: rgba(255, 255, 255, 0.2);
      padding: 2px 6px;
      width: fit-content;
    }}

    .action-gate-bar {{
      border-top: 1px solid var(--border-line);
      padding-top: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .btn-approve {{
      background: var(--accent-teal);
      color: #FFF;
      border: none;
      padding: 8px 18px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
    }}

    /* =========================================
       SLIDE 2: THE SELLER'S PROBLEM
    ========================================= */
    .s2-body {{
      display: flex;
      flex-direction: column;
      gap: 20px;
      flex: 1;
      justify-content: center;
    }}

    .tabs-visual-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
    }}

    .tab-card {{
      background: var(--bg-white);
      border: 1px solid var(--border-line);
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}

    .tab-card .t-head {{
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 600;
      color: var(--accent-teal);
      text-transform: uppercase;
      border-bottom: 1px solid var(--border-line);
      padding-bottom: 6px;
    }}

    .tab-card .t-body {{
      font-size: 13.5px;
      color: var(--text-dark);
      line-height: 1.45;
    }}

    .s2-bottom-row {{
      display: grid;
      grid-template-columns: 1.5fr 1fr;
      gap: 20px;
      align-items: stretch;
    }}

    .cost-box {{
      background: var(--bg-white);
      border: 1px solid var(--border-line);
      border-left: 4px solid var(--accent-amber);
      padding: 16px 20px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}

    .cost-title {{
      font-size: 14px;
      font-weight: 700;
      color: var(--text-dark);
    }}

    .cost-desc {{
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.45;
    }}

    .stat-callout {{
      background: var(--accent-teal-soft);
      border: 1px solid #C4E2D7;
      padding: 16px 20px;
      display: flex;
      flex-direction: column;
      gap: 4px;
      justify-content: center;
    }}

    .stat-title {{
      font-size: 13px;
      font-weight: 600;
      color: var(--accent-teal);
    }}

    .stat-note {{
      font-size: 10.5px;
      color: var(--text-muted);
    }}

    /* =========================================
       SLIDE 3: PRODUCT DEMONSTRATION (STAR SLIDE)
    ========================================= */
    .s3-container {{
      display: flex;
      flex-direction: column;
      gap: 16px;
      flex: 1;
      justify-content: center;
    }}

    .s3-compare-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr 1.15fr;
      gap: 20px;
    }}

    .evidence-box {{
      background: var(--bg-white);
      border: 1px solid var(--border-line);
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .evidence-box.highlight-mismatch {{
      border: 2px solid var(--accent-amber);
    }}

    .ev-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border-line);
      padding-bottom: 8px;
    }}

    .ev-title {{
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
    }}

    .ev-img-wrap {{
      height: 150px;
      background: #ECEEE9;
      border: 1px solid var(--border-line);
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      overflow: hidden;
    }}

    .ev-img-wrap img {{
      max-width: 100%;
      max-height: 100%;
      object-fit: cover;
    }}

    .verdict-action-panel {{
      background: var(--bg-white);
      border: 1px solid var(--border-line);
      border-left: 4px solid var(--accent-amber);
      padding: 18px 20px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}

    .verdict-status-pill {{
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 700;
      background: var(--accent-amber);
      color: #FFF;
      padding: 5px 12px;
      width: fit-content;
    }}

    .seller-options-list {{
      display: flex;
      flex-direction: column;
      gap: 6px;
      font-size: 12.5px;
      color: var(--text-dark);
      padding-left: 18px;
    }}

    /* =========================================
       SLIDE 4: WORKFLOW & DECISION AUTHORITY (DARK)
    ========================================= */
    .s4-diagram-wrap {{
      display: flex;
      flex-direction: column;
      gap: 20px;
      flex: 1;
      justify-content: center;
    }}

    .node-flow-row {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 16px;
      position: relative;
    }}

    .flow-node {{
      background: var(--bg-dark-card);
      border: 1px solid var(--bg-dark-line);
      padding: 18px 16px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}

    .flow-node.key-node {{
      border: 2px solid #3EC9B6;
    }}

    .n-tag {{
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 600;
      color: #3EC9B6;
    }}

    .n-title {{
      font-size: 15px;
      font-weight: 700;
      color: #FFF;
    }}

    .n-desc {{
      font-size: 12px;
      color: var(--text-light-muted);
      line-height: 1.4;
    }}

    .branches-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 16px;
    }}

    .branch-card {{
      background: var(--bg-dark-card);
      border: 1px solid var(--bg-dark-line);
      padding: 14px 18px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .b-tag {{
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
    }}

    .b-text {{
      font-size: 12px;
      color: var(--text-light);
    }}

    .authority-summary-strip {{
      background: var(--bg-dark-card);
      border: 1px solid var(--bg-dark-line);
      padding: 12px 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
      font-family: var(--font-mono);
      color: var(--text-light);
    }}

    /* =========================================
       SLIDE 5: DEMO SCENARIOS TABLE
    ========================================= */
    .s5-table-wrap {{
      display: flex;
      flex-direction: column;
      gap: 14px;
      flex: 1;
      justify-content: center;
    }}

    .scenario-table {{
      width: 100%;
      border-collapse: collapse;
      background: var(--bg-white);
      border: 1px solid var(--border-line);
    }}

    .scenario-table th, .scenario-table td {{
      padding: 14px 18px;
      text-align: left;
      font-size: 13.5px;
      border-bottom: 1px solid var(--border-line);
      vertical-align: middle;
    }}

    .scenario-table th {{
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--accent-teal);
      background: #ECEEE9;
    }}

    .scenario-table tr:last-child td {{
      border-bottom: none;
    }}

    .badge-scenario {{
      display: inline-block;
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 600;
      padding: 3px 8px;
    }}

    .badge-scenario.ready {{ background: var(--accent-teal-soft); color: var(--accent-teal); }}
    .badge-scenario.mismatch {{ background: var(--accent-amber-soft); color: var(--accent-amber); }}
    .badge-scenario.unclear {{ background: #ECEEE9; color: var(--text-dark); }}
    .badge-scenario.context {{ background: #E9ECEF; color: var(--text-dark); }}

    /* =========================================
       SLIDE 6: 24-HOUR DELIVERY PLAN
    ========================================= */
    .s6-grid {{
      display: grid;
      grid-template-columns: 1.3fr 1fr;
      gap: 36px;
      flex: 1;
      align-items: center;
    }}

    .timeline-phases {{
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .phase-row {{
      background: var(--bg-white);
      border: 1px solid var(--border-line);
      padding: 14px 18px;
      display: grid;
      grid-template-columns: 90px 1fr;
      gap: 16px;
      align-items: center;
    }}

    .phase-time {{
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 700;
      color: var(--accent-teal);
    }}

    .phase-details h4 {{
      font-size: 14.5px;
      font-weight: 700;
      color: var(--text-dark);
    }}

    .phase-details p {{
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 2px;
    }}

    .team-cards-stack {{
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}

    .person-card {{
      background: var(--bg-white);
      border: 1px solid var(--border-line);
      padding: 12px 16px;
      display: flex;
      flex-direction: column;
      gap: 3px;
    }}

    .person-card .p-name {{
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 700;
      color: var(--accent-teal);
    }}

    .person-card .p-roles {{
      font-size: 12px;
      color: var(--text-dark);
      line-height: 1.4;
    }}

    .scope-guard-box {{
      background: var(--accent-teal-soft);
      border: 1px solid #C4E2D7;
      padding: 12px 16px;
      font-size: 12px;
      color: var(--accent-teal);
      line-height: 1.4;
    }}
  </style>
</head>
<body>

  <div class="nav-controls">
    <span id="slide-num-indicator">Slide 1 / 6</span>
    <button onclick="prevSlide()">◀ Prev</button>
    <button onclick="nextSlide()">Next ▶</button>
    <button onclick="window.print()">Print / PDF</button>
  </div>

  <!-- SLIDE 1 -->
  <section class="slide" id="slide-1">
    <div class="label-tag">
      <span>AgentX Hackathon 2026</span>
      <span>·</span>
      <span>PS-04 Track</span>
    </div>

    <div class="s1-grid">
      <div class="s1-left">
        <h1 class="brand-title">ReturnLens</h1>
        <h2 class="brand-lead">Review returns with cited video evidence.</h2>
        <p class="brand-desc">
          A focused return triage agent for solo direct-to-consumer sellers. It links buyer unboxing clips to store records and policy rules for 1-click decision making.
        </p>

        <div class="meta-badges">
          <span class="badge">Team Rookie</span>
          <span class="badge">3 Members</span>
          <span class="badge">24-Hour Prototype</span>
          <span class="badge">Mock Data & Staged Evidence</span>
        </div>
      </div>

      <div class="hero-evidence-card">
        <div class="card-header-row">
          <div>
            <span class="mono" style="font-size: 13px; font-weight: 700; color: var(--text-dark);">CASE #RET-2026-084</span>
            <div class="mono" style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">Order #ORD-1042 · Customer: Anita S.</div>
          </div>
          <span class="card-tag">PENDING REVIEW</span>
        </div>

        <div class="card-item-row">
          <div class="item-thumbnail">
            <img src="data:image/png;base64,{b64_white}" alt="White Headphones" style="width: 100%; height: 100%; object-fit: contain;">
          </div>
          <div class="item-specs">
            <h4>Wireless Over-Ear Headphones (White)</h4>
            <p>SKU: HEAD-WHT-02 · Paid: ₹1,499</p>
            <p style="color: var(--accent-teal);">Delivered 4 days ago (Within 7d window)</p>
          </div>
        </div>

        <div class="video-proof-box">
          <div class="time-badge">CITED FRAME: 00:14 / 00:45</div>
          <div style="font-family: var(--font-mono); font-size: 11.5px; opacity: 0.9;">
            "Seam tear on left casing verified. Brand tag matches store SKU."
          </div>
        </div>

        <div class="action-gate-bar">
          <span class="mono" style="font-size: 11px; color: var(--text-muted);">Seller approval mandatory</span>
          <button class="btn-approve">Approve Return (1-Click)</button>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <span>ReturnLens · Evidence-Backed Return Triage</span>
      <span>Slide 1 / 6</span>
    </div>
  </section>

  <!-- SLIDE 2 -->
  <section class="slide" id="slide-2">
    <div class="slide-header">
      <div class="label-tag">
        <span>The Problem</span>
        <span>·</span>
        <span>Solo Seller Bottleneck</span>
      </div>
      <h1 class="slide-title">Return evidence is scattered across four sources</h1>
      <p class="slide-sub">Sellers make high-stakes return decisions from memory while toggling between fragmented tabs.</p>
    </div>

    <div class="s2-body">
      <div class="tabs-visual-grid">
        <div class="tab-card">
          <div class="t-head">1. Buyer Chat / Video</div>
          <div class="t-body">
            "Received damaged unit. Need full refund."<br>
            <span class="mono" style="font-size: 11.5px; color: var(--accent-teal);">📎 unboxing_clip_32s.mp4</span>
          </div>
        </div>
        <div class="tab-card">
          <div class="t-head">2. Order Record</div>
          <div class="t-body">
            <span class="mono">ORD-8492 · ₹1,499</span><br>
            SKU: HEAD-WHT-02<br>
            Customer: Rohit K.
          </div>
        </div>
        <div class="tab-card">
          <div class="t-head">3. Delivery Status</div>
          <div class="t-body">
            Delivered: 26 Oct (4d ago)<br>
            Tracking: TRK-98214-DEL<br>
            Carrier: MockPost
          </div>
        </div>
        <div class="tab-card">
          <div class="t-head">4. Return Policy</div>
          <div class="t-body">
            7-day limit from delivery.<br>
            Tags intact. Original packaging.<br>
            Refund cap: ₹4,999.
          </div>
        </div>
      </div>

      <div class="s2-bottom-row">
        <div class="cost-box">
          <div class="cost-title">The Cost of Guesswork</div>
          <div class="cost-desc">
            • <strong>Wrong Approval:</strong> Unrecoverable cash, shipping fees, and inventory lost to fraud or abuse.<br>
            • <strong>Unfair Denial:</strong> Permanent loss of customer goodwill, chargebacks, and marketplace penalties.
          </div>
        </div>

        <div class="stat-callout">
          <div class="stat-title">Sourced Industry Benchmark</div>
          <div style="font-size: 12.5px; color: var(--text-dark); line-height: 1.4;">
            Fraud estimates differ by definition: <strong>9%</strong> (NRF 2025, fraud only) vs <strong>15.14%</strong> (Appriss/Deloitte 2024, fraud & abuse).
          </div>
          <div class="stat-note">*U.S. retail estimates; not measured on our target sellers.</div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <span>ReturnLens · Problem Context</span>
      <span>Slide 2 / 6</span>
    </div>
  </section>

  <!-- SLIDE 3 (STAR SLIDE) -->
  <section class="slide" id="slide-3">
    <div class="slide-header">
      <div class="label-tag">
        <span>Product Demonstration</span>
        <span>·</span>
        <span>Visual Evidence Benchmark</span>
      </div>
      <h1 class="slide-title">A color mismatch needs seller review</h1>
      <p class="slide-sub">When video evidence contradicts store truth, ReturnLens surfaces the discrepancy without auto-denying.</p>
    </div>

    <div class="s3-container">
      <div class="s3-compare-grid">
        <!-- Store Truth -->
        <div class="evidence-box">
          <div class="ev-header">
            <span class="ev-title">Store API Record</span>
            <span class="mono" style="font-size: 11px; color: var(--accent-teal); font-weight: 700;">ORDER TRUTH</span>
          </div>
          <div class="ev-img-wrap">
            <img src="data:image/png;base64,{b64_white}" alt="Ordered White Headphones">
          </div>
          <div class="mono" style="font-size: 12.5px; line-height: 1.45;">
            <strong>SKU: HEAD-WHT-02</strong><br>
            Product: Wireless Headset<br>
            Ordered Color: <span style="background: #E5E5E5; padding: 1px 5px;">White</span><br>
            Price: ₹1,499 · Delivered 4d ago
          </div>
        </div>

        <!-- Video Evidence -->
        <div class="evidence-box highlight-mismatch">
          <div class="ev-header">
            <span class="ev-title">Video Evidence</span>
            <span class="mono" style="font-size: 11px; color: var(--accent-amber); font-weight: 700;">STAGED FRAME [00:07]</span>
          </div>
          <div class="ev-img-wrap">
            <img src="data:image/png;base64,{b64_black}" alt="Observed Black Headphones">
          </div>
          <div class="mono" style="font-size: 12.5px; line-height: 1.45;">
            <strong>Observed color: Black</strong><br>
            SKU: Not verified (unreadable)<br>
            Tag: Tag not visible in this frame<br>
            Discrepancy: Color divergence detected
          </div>
        </div>

        <!-- Verdict & Resolution Options -->
        <div class="verdict-action-panel">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="mono" style="font-size: 12px; font-weight: 700; color: var(--text-dark);">Policy P-03 Check:</span>
            <span class="mono" style="font-weight: 700; color: var(--accent-red);">FAIL (MISMATCH)</span>
          </div>
          <span class="verdict-status-pill">STATUS: NEEDS SELLER REVIEW</span>
          <p style="font-size: 12px; color: var(--text-muted); line-height: 1.4;">
            No automatic denial. No return label or refund draft issued at this stage.
          </p>

          <div style="font-size: 12px; font-weight: 700; color: var(--text-dark); margin-top: 2px;">
            Seller Resolution Options:
          </div>
          <ul class="seller-options-list">
            <li>Review possible warehouse mis-shipment</li>
            <li>Request outside-box shipping label photo</li>
            <li>Hold for physical inspection upon return</li>
          </ul>

          <div class="mono" style="font-size: 10px; color: var(--text-muted); margin-top: auto; border-top: 1px solid var(--border-line); padding-top: 6px;">
            Illustrative prototype · Staged mock evidence
          </div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <span>Illustrative Prototype · Staged Mock Evidence · No Real Customer PII</span>
      <span>Slide 3 / 6</span>
    </div>
  </section>

  <!-- SLIDE 4 (DARK THEME) -->
  <section class="slide dark-theme" id="slide-4">
    <div class="slide-header">
      <div class="label-tag">
        <span>Workflow & Decision Authority</span>
        <span>·</span>
        <span>Deterministic Architecture</span>
      </div>
      <h1 class="slide-title">Evidence checks and seller approval</h1>
      <p class="slide-sub">A deterministic pipeline where models observe, code verifies, and the seller authorizes.</p>
    </div>

    <div class="s4-diagram-wrap">
      <div class="node-flow-row">
        <div class="flow-node">
          <span class="n-tag">01 · INGEST</span>
          <span class="n-title">Receive & Retrieve</span>
          <span class="n-desc">Buyer video & message via mock chat; queries order and courier APIs.</span>
        </div>
        <div class="flow-node">
          <span class="n-tag">02 · OBSERVE</span>
          <span class="n-title">Model Observation</span>
          <span class="n-desc">Models inspect frames and generate structured observations with timestamps.</span>
        </div>
        <div class="flow-node key-node">
          <span class="n-tag">03 · CHECK</span>
          <span class="n-title">Policy Engine (Code)</span>
          <span class="n-desc">Pure code evaluates 7-day window, delivery date, SKU match, and refund cap.</span>
        </div>
        <div class="flow-node">
          <span class="n-tag">04 · VERIFY</span>
          <span class="n-title">Independent Critic</span>
          <span class="n-desc">Audits cited frames to confirm observations are supported by actual visual data.</span>
        </div>
        <div class="flow-node">
          <span class="n-tag">05 · AUTHORIZE</span>
          <span class="n-title">Seller Gate</span>
          <span class="n-desc">Seller 1-click approval permits mock return label & refund draft.</span>
        </div>
      </div>

      <div class="branches-grid">
        <div class="branch-card" style="border-left: 3px solid var(--accent-amber);">
          <span class="b-tag" style="color: var(--accent-amber);">UNCLEAR EVIDENCE</span>
          <span class="b-text">Asks for specific photo (e.g. tag/serial) and resumes the exact same case.</span>
        </div>
        <div class="branch-card" style="border-left: 3px solid #FF8A7A;">
          <span class="b-tag" style="color: #FF8A7A;">MISMATCH / CONTRADICTION</span>
          <span class="b-text">Escalates directly to seller review with proof pack; never auto-denies.</span>
        </div>
        <div class="branch-card" style="border-left: 3px solid #3EC9B6;">
          <span class="b-tag" style="color: #3EC9B6;">ALL POLICY CHECKS PASS</span>
          <span class="b-text">Prepares 1-click approval package for seller; draft in <span class="mono">pending_return_receipt</span>.</span>
        </div>
      </div>

      <div class="authority-summary-strip">
        <span style="color: #3EC9B6; font-weight: 700;">AUTHORITY MODEL:</span>
        <span>Server-enforced limits</span>
        <span>·</span>
        <span>Models observe; pure code evaluates policy</span>
        <span>·</span>
        <span>Seller approval required for all actions</span>
      </div>
    </div>

    <div class="slide-footer">
      <span>ReturnLens · System Architecture & Decision Flow</span>
      <span>Slide 4 / 6</span>
    </div>
  </section>

  <!-- SLIDE 5 -->
  <section class="slide" id="slide-5">
    <div class="slide-header">
      <div class="label-tag">
        <span>Demo Scenarios</span>
        <span>·</span>
        <span>Benchmark Matrix</span>
      </div>
      <h1 class="slide-title">Four return scenarios</h1>
      <p class="slide-sub">Expected prototype behavior across diverse real-world return situations.</p>
    </div>

    <div class="s5-table-wrap">
      <table class="scenario-table">
        <thead>
          <tr>
            <th style="width: 140px;">Scenario</th>
            <th style="width: 170px;">Case Identifier</th>
            <th>Evidence Situation</th>
            <th>Expected Prototype Behavior</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><span class="badge-scenario ready">Ready</span></td>
            <td class="mono">Case A · ORD-1042<br><span style="color: var(--text-muted); font-size: 11.5px;">₹1,499</span></td>
            <td>Seam tear verified at 00:14; inside 7-day window; brand tag matches.</td>
            <td><strong>Prepare for seller approval</strong> → Generates mock label & refund draft in <span class="mono">pending_return_receipt</span>.</td>
          </tr>
          <tr>
            <td><span class="badge-scenario mismatch">Mismatch</span></td>
            <td class="mono">Case B · ORD-8492<br><span style="color: var(--text-muted); font-size: 11.5px;">₹1,499</span></td>
            <td>White ordered vs Black observed in frame 00:07; tag missing.</td>
            <td><strong>Needs seller review</strong> → Flagged with proof pack for manual decision; no auto-denial, no label created.</td>
          </tr>
          <tr>
            <td><span class="badge-scenario unclear">Unclear</span></td>
            <td class="mono">Case C · ORD-5120<br><span style="color: var(--text-muted); font-size: 11.5px;">₹850</span></td>
            <td>4-second dark video (brightness 28); only 2 usable frames.</td>
            <td><strong>Request specific evidence</strong> → Prompts buyer for well-lit tag photo; preserves active case session.</td>
          </tr>
          <tr>
            <td><span class="badge-scenario context">Context</span></td>
            <td class="mono">Case D · ORD-3391<br><span style="color: var(--text-muted); font-size: 11.5px;">₹2,199</span></td>
            <td>Continuous take tracking parcel from sealed label to unboxing.</td>
            <td><strong>Check sequence continuity</strong> → Verifies chronological context; asks for missing angles if needed.</td>
          </tr>
        </tbody>
      </table>

      <div class="mono" style="font-size: 11px; color: var(--text-muted);">
        *Expected prototype behavior on staged benchmark cases; not a measurement of live production metrics.
      </div>
    </div>

    <div class="slide-footer">
      <span>Consistent Demo Benchmark Suite · 4 Scenarios</span>
      <span>Slide 5 / 6</span>
    </div>
  </section>

  <!-- SLIDE 6 -->
  <section class="slide" id="slide-6">
    <div class="slide-header">
      <div class="label-tag">
        <span>Delivery Plan</span>
        <span>·</span>
        <span>Team Rookie</span>
      </div>
      <h1 class="slide-title">A focused 24-hour prototype</h1>
      <p class="slide-sub">Realistic scope and role allocation for a 3-person sprint during the hackathon.</p>
    </div>

    <div class="s6-grid">
      <!-- 4 Phases -->
      <div class="timeline-phases">
        <div class="phase-row">
          <div class="phase-time">00h – 06h</div>
          <div class="phase-details">
            <h4>Mock APIs & Core Flow</h4>
            <p>FastAPI mock store and shipping services, SQLite seed data, core StateGraph.</p>
          </div>
        </div>
        <div class="phase-row">
          <div class="phase-time">06h – 12h</div>
          <div class="phase-details">
            <h4>Evidence Pipeline & Policy Checks</h4>
            <p>ffmpeg CPU frame extraction (~1 fps), multimodal prompt grounding, deterministic code policy rules.</p>
          </div>
        </div>
        <div class="phase-row">
          <div class="phase-time">12h – 18h</div>
          <div class="phase-details">
            <h4>Integration & 4 Demo Scenarios</h4>
            <p>End-to-end testing across Cases A, B, C, D; critic checks; fallback error handling.</p>
          </div>
        </div>
        <div class="phase-row">
          <div class="phase-time">18h – 24h</div>
          <div class="phase-details">
            <h4>Demo Polish & Packaging</h4>
            <p>Seller review console polish, 3-minute video walk-through, GitHub README, submission package.</p>
          </div>
        </div>
      </div>

      <!-- Team Allocation -->
      <div class="team-cards-stack">
        <div class="person-card">
          <div class="p-name">Person A (Backend & Logic)</div>
          <div class="p-roles">Agent flow, state graph, deterministic policy engine, critic, audit log.</div>
        </div>
        <div class="person-card">
          <div class="p-name">Person B (Multimodal & UI)</div>
          <div class="p-roles">Video pipeline, frame indexer, seller console, evidence pack view.</div>
        </div>
        <div class="person-card">
          <div class="p-name">Person C (QA & Integration)</div>
          <div class="p-roles">Integration, mock store data, 4 demo cases, fallback testing, demo video.</div>
        </div>

        <div class="scope-guard-box">
          <strong>Strict 24-Hour Scope Guardrails:</strong><br>
          Mock services · Staged evidence · Single seller return workflow · No production payments.
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <span>Project-specific logic written inside the 24 hours · Checkable, buildable agent prototype</span>
      <span>Slide 6 / 6</span>
    </div>
  </section>

  <script>
    let currentSlide = 1;
    const totalSlides = 6;

    function updateNav() {{
      document.getElementById('slide-num-indicator').innerText = `Slide ${{currentSlide}} / ${{totalSlides}}`;
      const target = document.getElementById(`slide-${{currentSlide}}`);
      if (target) {{
        target.scrollIntoView({{ behavior: 'smooth' }});
      }}
    }}

    function nextSlide() {{
      if (currentSlide < totalSlides) {{
        currentSlide++;
        updateNav();
      }}
    }}

    function prevSlide() {{
      if (currentSlide > 1) {{
        currentSlide--;
        updateNav();
      }}
    }}

    window.addEventListener('keydown', (e) => {{
      if (e.key === 'ArrowRight' || e.key === 'Space' || e.key === 'PageDown') {{
        nextSlide();
      }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
        prevSlide();
      }}
    }});
  </script>
</body>
</html>
"""

with open(r"D:\Code\Code\AIO\Code\ZaloAIC\ReturnLens_v3.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("ReturnLens_v3.html generated successfully!")

