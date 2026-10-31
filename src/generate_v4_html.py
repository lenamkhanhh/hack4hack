import os
import sys
import json
import base64
import shutil
import subprocess
from pathlib import Path
import fitz
from PIL import Image

# Robust path derivation
base_dir = Path(__file__).resolve().parent.parent
data_path = base_dir / "content" / "deck_data.json"
assets_dir = base_dir / "src" / "assets"

if not data_path.exists():
    raise FileNotFoundError(f"Canonical data file missing: {data_path}")

with open(data_path, "r", encoding="utf-8") as f:
    data = json.load(f)

def get_b64(fname):
    p = assets_dir / fname
    if not p.exists():
        raise FileNotFoundError(f"Required asset not found: {p}")
    with open(p, 'rb') as f:
        mime = "image/jpeg" if fname.endswith(".jpg") else "image/png"
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode('utf-8')

# Ensure required assets exist
white_b64 = get_b64('studio_white_headphones.jpg')
black_b64 = get_b64('unboxing_black_headphones.jpg')

slides_data = {s["slide_number"]: s for s in data["slides"]}
d1 = slides_data[1]
d2 = slides_data[2]
d3 = slides_data[3]
d4 = slides_data[4]
d5 = slides_data[5]
d6 = slides_data[6]

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ReturnLens — Evidence-Backed Returns Triage Agent (AgentX Hackathon 2026, PS-04)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}

  :root {{
    --cream: #F5F3EF;
    --dark-green: #172621;
    --primary-teal: #006B55;
    --teal-light: #E1F2EC;
    --teal-accent: #00D1A7;
    --coral: #D95D39;
    --coral-light: #FCECE8;
    --coral-dark: #991B1B;
    --amber: #D97706;
    --amber-light: #FEF3C7;
    --amber-dark: #92400E;
    --blue-light: #EFF6FF;
    --blue-dark: #1E40AF;
    --text-muted: #596E64;
    --text-subtle: #7A8E85;
    --border-light: #E2DED4;
    --border-dark: #223830;
    --card-dark: #172621;
    --dark-bg: #0F1A16;
  }}

  body {{
    background-color: #2E3A35;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: var(--dark-green);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 0;
    gap: 40px;
    -webkit-font-smoothing: antialiased;
  }}

  @page {{
    size: 1280px 720px;
    margin: 0;
  }}

  @media print {{
    body {{
      background: none;
      padding: 0;
      gap: 0;
    }}
    .slide {{
      box-shadow: none !important;
      page-break-after: always;
      break-after: page;
    }}
  }}

  .slide {{
    width: 1280px;
    height: 720px;
    background-color: var(--cream);
    position: relative;
    padding: 42px 64px 38px 64px;
    box-shadow: 0 16px 48px rgba(0,0,0,0.12);
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }}

  .slide.dark {{
    background-color: var(--dark-bg);
    color: #F5F3EF;
  }}

  .tag-label {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--primary-teal);
    margin-bottom: 6px;
  }}

  .slide.dark .tag-label {{
    color: var(--teal-accent);
  }}

  .slide-title {{
    font-size: 36px;
    font-weight: 800;
    letter-spacing: -0.8px;
    line-height: 1.15;
    color: var(--dark-green);
    margin-bottom: 6px;
  }}

  .slide.dark .slide-title {{
    color: #F5F3EF;
  }}

  .slide-sub {{
    font-size: 17px;
    font-weight: 400;
    line-height: 1.35;
    color: var(--text-muted);
    margin-bottom: 16px;
  }}

  .slide.dark .slide-sub {{
    color: #A3B8B0;
  }}

  .slide-footer {{
    position: absolute;
    bottom: 16px;
    left: 64px;
    right: 64px;
    display: flex;
    justify-content: space-between;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: var(--text-subtle);
    border-top: 1px solid var(--border-light);
    padding-top: 8px;
  }}

  .slide.dark .slide-footer {{
    border-top-color: var(--border-dark);
    color: #5C786E;
  }}

  /* =========================================================================
     SLIDE 1: PRODUCT HERO & CONSOLE
     ========================================================================= */
  .hero-layout {{
    display: grid;
    grid-template-columns: 420px 1fr;
    gap: 40px;
    flex: 1;
    align-items: stretch;
  }}

  .hero-left {{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding-bottom: 16px;
  }}

  .hero-title {{
    font-size: 52px;
    font-weight: 900;
    letter-spacing: -1.5px;
    color: var(--dark-green);
    line-height: 1;
    margin-bottom: 12px;
  }}

  .hero-statement {{
    font-size: 22px;
    font-weight: 700;
    color: var(--dark-green);
    line-height: 1.25;
    margin-bottom: 14px;
  }}

  .hero-summary {{
    font-size: 13.5px;
    line-height: 1.55;
    color: var(--text-muted);
    margin-bottom: 16px;
  }}

  .hero-meta {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    color: var(--text-subtle);
    padding-top: 12px;
    border-top: 1px solid var(--border-light);
  }}

  .console-wrapper {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    display: flex;
    flex-direction: column;
    box-shadow: 0 12px 32px rgba(0,0,0,0.06);
    height: 100%;
  }}

  .console-header {{
    background: #1F302A;
    color: var(--teal-accent);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    padding: 12px 20px;
    letter-spacing: 1px;
    display: flex;
    justify-content: space-between;
  }}

  .console-body {{
    padding: 18px 22px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    flex: 1;
    gap: 12px;
  }}

  .console-images-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }}

  .img-card {{
    display: flex;
    flex-direction: column;
    border: 1px solid var(--border-light);
    background: #FAFAFA;
    overflow: hidden;
  }}

  .img-card img {{
    width: 100%;
    height: 180px;
    object-fit: cover;
  }}

  .img-badge {{
    padding: 6px 8px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    text-align: center;
  }}

  .badge-ordered {{
    background: var(--teal-light);
    color: var(--primary-teal);
  }}

  .badge-observed {{
    background: var(--coral-light);
    color: var(--coral-dark);
  }}

  .c-alert-box {{
    background: var(--coral-light);
    border: 1px solid var(--coral);
    padding: 10px 14px;
    border-radius: 2px;
  }}

  .c-alert-title {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    color: var(--coral-dark);
    margin-bottom: 2px;
  }}

  .c-alert-desc {{
    font-size: 11px;
    color: var(--coral-dark);
  }}

  .c-status-bar {{
    background: var(--amber-light);
    color: var(--amber-dark);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    padding: 9px 12px;
    text-align: center;
    border-radius: 2px;
  }}

  .c-button {{
    background: var(--primary-teal);
    color: #FFFFFF;
    font-family: 'Inter', sans-serif;
    font-size: 13.5px;
    font-weight: 700;
    padding: 11px 16px;
    text-align: center;
    border-radius: 2px;
    letter-spacing: 0.2px;
  }}

  /* =========================================================================
     SLIDE 2: THE PROBLEM (FRAGMENTATION AS A VISUAL STORY)
     ========================================================================= */
  .problem-layout {{
    display: grid;
    grid-template-columns: 520px 40px 1fr;
    gap: 16px;
    flex: 1;
    align-items: center;
  }}

  .sources-stack {{
    display: flex;
    flex-direction: column;
    gap: 12px;
  }}

  .source-strip {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    padding: 14px 18px;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}

  .source-strip-header {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    color: var(--primary-teal);
  }}

  .source-strip-detail {{
    font-size: 13px;
    font-weight: 600;
    color: var(--dark-green);
  }}

  .arrow-connector {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 32px;
    font-weight: 700;
    color: var(--coral);
    text-align: center;
  }}

  .gap-focal-card {{
    background: var(--dark-green);
    border: 2px solid var(--coral);
    padding: 32px 36px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    height: 100%;
    box-shadow: 0 12px 36px rgba(0,0,0,0.1);
  }}

  .gap-tag {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: var(--coral);
    margin-bottom: 8px;
  }}

  .gap-title {{
    font-size: 24px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: var(--cream);
    margin-bottom: 14px;
  }}

  .gap-quote {{
    font-size: 16px;
    font-weight: 700;
    font-style: italic;
    color: #FBBF24;
    line-height: 1.4;
    margin-bottom: 16px;
  }}

  .gap-body {{
    font-size: 13px;
    line-height: 1.6;
    color: #D1D5DB;
  }}

  /* =========================================================================
     SLIDE 3: EVIDENCE ARENA & DECISION PANEL
     ========================================================================= */
  .evidence-layout {{
    display: grid;
    grid-template-columns: 66% 34%;
    gap: 24px;
    flex: 1;
    align-items: stretch;
  }}

  .arena-card {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    padding: 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .arena-pics-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
  }}

  .arena-pic-box {{
    display: flex;
    flex-direction: column;
    border: 1px solid var(--border-light);
    overflow: hidden;
  }}

  .arena-pic-box img {{
    width: 100%;
    height: 250px;
    object-fit: cover;
  }}

  .arena-caption {{
    margin-top: 16px;
    font-size: 12px;
    line-height: 1.5;
    color: var(--text-muted);
    border-top: 1px solid var(--border-light);
    padding-top: 12px;
  }}

  .decision-panel-card {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    padding: 22px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .dec-tag {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10.5px;
    font-weight: 700;
    color: var(--coral);
    margin-bottom: 4px;
  }}

  .dec-title {{
    font-size: 19px;
    font-weight: 800;
    color: var(--coral-dark);
    margin-bottom: 4px;
  }}

  .dec-action {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    color: var(--coral-dark);
    margin-bottom: 12px;
  }}

  .dec-section-head {{
    font-size: 12px;
    font-weight: 700;
    color: var(--dark-green);
    margin-top: 10px;
    margin-bottom: 6px;
  }}

  .dec-list {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 5px;
  }}

  .dec-list li {{
    font-size: 11.5px;
    line-height: 1.4;
    color: var(--text-muted);
    padding-left: 12px;
    position: relative;
  }}

  .dec-list li::before {{
    content: "•";
    position: absolute;
    left: 0;
    color: var(--dark-green);
  }}

  .dec-guardrail-note {{
    margin-top: 14px;
    padding-top: 10px;
    border-top: 1px solid var(--border-light);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    color: var(--text-muted);
    line-height: 1.4;
  }}

  /* =========================================================================
     SLIDE 4: THE AGENTIC SYSTEM (DARK ARCHITECTURE)
     ========================================================================= */
  .arch-container {{
    display: flex;
    flex-direction: column;
    gap: 16px;
    flex: 1;
  }}

  .zones-row {{
    display: grid;
    grid-template-columns: 3.6fr 4.2fr 3.45fr;
    gap: 16px;
  }}

  .zone-card {{
    background: var(--card-dark);
    border: 1px solid var(--border-dark);
    padding: 16px 18px;
    border-top: 4px solid var(--teal-accent);
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}

  .zone-card.code-zone {{
    border-top-color: var(--cream);
  }}

  .zone-card.gate-zone {{
    border-top-color: #FBBF24;
  }}

  .zone-num {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    color: var(--teal-accent);
  }}

  .zone-card.code-zone .zone-num {{ color: var(--cream); }}
  .zone-card.gate-zone .zone-num {{ color: #FBBF24; }}

  .zone-title {{
    font-size: 15px;
    font-weight: 700;
    color: var(--cream);
  }}

  .zone-desc {{
    font-size: 11px;
    line-height: 1.4;
    color: #A3B8B0;
  }}

  .stateful-box {{
    background: #14221D;
    border: 1.5px solid #2563EB;
    padding: 18px 22px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }}

  .stateful-head {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11.5px;
    font-weight: 700;
    color: #93C5FD;
  }}

  .nodes-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
  }}

  .state-node {{
    background: #1F302A;
    border: 1px solid var(--border-dark);
    padding: 10px 12px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    color: var(--cream);
    text-align: center;
    flex: 1;
    border-radius: 2px;
  }}

  .state-node.highlight {{
    background: #1E3A8A;
    border-color: #60A5FA;
    color: #DBEAFE;
  }}

  .state-arrow {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 15px;
    font-weight: 700;
    color: #93C5FD;
  }}

  .stateful-desc {{
    font-size: 12px;
    line-height: 1.45;
    color: #A3B8B0;
  }}

  .bottom-traces {{
    background: #121F1B;
    border: 1px solid var(--border-dark);
    padding: 12px 18px;
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
  }}

  .trace-fast-path {{
    color: #34D399;
    font-weight: 700;
  }}

  .trace-audit {{
    color: #A3B8B0;
  }}

  /* =========================================================================
     SLIDE 5: 4 SCENARIOS MATRIX
     ========================================================================= */
  .scenarios-stack {{
    display: flex;
    flex-direction: column;
    gap: 12px;
    flex: 1;
  }}

  .sc-lane {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    padding: 14px 20px;
    display: grid;
    grid-template-columns: 220px 1fr 30px 1.2fr;
    gap: 16px;
    align-items: center;
  }}

  .sc-badge {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    padding: 8px 12px;
    text-align: center;
    border-radius: 2px;
  }}

  .badge-01 {{ background: var(--teal-light); color: var(--primary-teal); }}
  .badge-02 {{ background: var(--coral-light); color: var(--coral-dark); }}
  .badge-03 {{ background: var(--blue-light); color: var(--blue-dark); }}
  .badge-04 {{ background: #ECFDF5; color: #065F46; }}

  .sc-obs {{
    font-size: 12.5px;
    font-weight: 700;
    color: var(--dark-green);
    line-height: 1.35;
  }}

  .sc-arr {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 18px;
    font-weight: 700;
    color: var(--primary-teal);
    text-align: center;
  }}

  .sc-act {{
    display: flex;
    flex-direction: column;
    gap: 2px;
  }}

  .sc-act-head {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    font-weight: 700;
  }}

  .badge-01 ~ .sc-arr ~ .sc-act .sc-act-head {{ color: var(--primary-teal); }}
  .badge-02 ~ .sc-arr ~ .sc-act .sc-act-head {{ color: var(--coral-dark); }}
  .badge-03 ~ .sc-arr ~ .sc-act .sc-act-head {{ color: var(--blue-dark); }}
  .badge-04 ~ .sc-arr ~ .sc-act .sc-act-head {{ color: #065F46; }}

  .sc-act-desc {{
    font-size: 11px;
    color: var(--text-muted);
    line-height: 1.35;
  }}

  /* =========================================================================
     SLIDE 6: 24-HOUR PROTOTYPE PLAN
     ========================================================================= */
  .plan-container {{
    display: flex;
    flex-direction: column;
    gap: 20px;
    flex: 1;
  }}

  .timeline-flow {{
    position: relative;
    border-top: 4px solid var(--primary-teal);
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    padding-top: 14px;
  }}

  .t-step-box {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    padding: 16px 18px;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}

  .t-time-tag {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    color: var(--primary-teal);
  }}

  .t-title {{
    font-size: 15px;
    font-weight: 700;
    color: var(--dark-green);
  }}

  .t-owner {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    color: var(--primary-teal);
    margin-bottom: 2px;
  }}

  .t-desc {{
    font-size: 11.5px;
    line-height: 1.4;
    color: var(--text-muted);
  }}

  .scope-split {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }}

  .scope-block {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    padding: 18px 22px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}

  .scope-block.must-deliver {{
    border-left: 6px solid var(--primary-teal);
  }}

  .scope-block.cut-first {{
    border-left: 6px solid var(--coral);
  }}

  .scope-head {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.5px;
  }}

  .scope-block.must-deliver .scope-head {{ color: var(--primary-teal); }}
  .scope-block.cut-first .scope-head {{ color: var(--coral); }}

  .scope-items {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 5px;
  }}

  .scope-items li {{
    font-size: 12px;
    line-height: 1.4;
    color: var(--dark-green);
    padding-left: 12px;
    position: relative;
  }}

  .scope-items li::before {{
    content: "•";
    position: absolute;
    left: 0;
    color: var(--dark-green);
  }}
</style>
</head>
<body>

  <!-- SLIDE 1: PRODUCT HERO & CONSOLE -->
  <section class="slide" id="slide-1">
    <div class="hero-layout">
      <div class="hero-left">
        <div>
          <div class="tag-label">{d1['tag']}</div>
          <h1 class="hero-title">{d1['headline']}</h1>
          <div class="hero-statement">{d1['subheadline']}</div>
          <p class="hero-summary">{d1['summary']}<br><br>When a customer submits an unboxing video, ReturnLens cross-references store truth, verifies deterministic code policies, and gives the solo seller a 1-click decision console.</p>
        </div>
        <div class="hero-meta">{data['meta']['team']} · 24-Hour Prototype Feasibility</div>
      </div>

      <div class="console-wrapper">
        <div class="console-header">
          <span>{d1['console_mockup']['title']}</span>
          <span>{d1['console_mockup']['case_badge']}</span>
        </div>
        <div class="console-body">
          <div class="console-images-grid">
            <div class="img-card">
              <img src="{white_b64}" alt="Ordered White Headphones">
              <div class="img-badge badge-ordered">ORDERED: {d1['console_mockup']['order_info']['sku']} (WHITE)</div>
            </div>
            <div class="img-card">
              <img src="{black_b64}" alt="Observed Black Headphones">
              <div class="img-badge badge-observed">OBSERVED: BLACK ITEM · FRAME 00:07</div>
            </div>
          </div>

          <div class="c-alert-box">
            <div class="c-alert-title">{d1['console_mockup']['evidence_citation']['status_badge']}</div>
            <div class="c-alert-desc">{d1['console_mockup']['policy_check']['window_check']}  |  {d1['console_mockup']['policy_check']['color_check']}</div>
          </div>

          <div class="c-status-bar">{d1['console_mockup']['action_prompt']}</div>
          <div class="c-button">{d1['console_mockup']['button_text']}</div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <span>ReturnLens · Pitch Deck · PS-04 Track · Team Rookie (3 Members)</span>
      <span>Slide 1 / 6</span>
    </div>
  </section>

  <!-- SLIDE 2: THE PROBLEM (FRAGMENTATION) -->
  <section class="slide" id="slide-2">
    <div class="tag-label">{d2['tag']}</div>
    <h2 class="slide-title">{d2['headline']}</h2>
    <p class="slide-sub">{d2['subheadline']}  {d2['supporting_statement']}</p>

    <div class="problem-layout">
      <div class="sources-stack">
        <div class="source-strip">
          <div class="source-strip-header">{d2['sources'][0]['number']}  {d2['sources'][0]['name'].upper()}</div>
          <div class="source-strip-detail">{d2['sources'][0]['detail']}</div>
        </div>
        <div class="source-strip">
          <div class="source-strip-header">{d2['sources'][1]['number']}  {d2['sources'][1]['name'].upper()}</div>
          <div class="source-strip-detail">{d2['sources'][1]['detail']}</div>
        </div>
        <div class="source-strip">
          <div class="source-strip-header">{d2['sources'][2]['number']}  {d2['sources'][2]['name'].upper()}</div>
          <div class="source-strip-detail">{d2['sources'][2]['detail']}</div>
        </div>
        <div class="source-strip">
          <div class="source-strip-header">{d2['sources'][3]['number']}  {d2['sources'][3]['name'].upper()}</div>
          <div class="source-strip-detail">{d2['sources'][3]['detail']}</div>
        </div>
      </div>

      <div class="arrow-connector">→</div>

      <div class="gap-focal-card">
        <div class="gap-tag">{d2['gap_card']['tag']}</div>
        <div class="gap-title">{d2['gap_card']['title']}</div>
        <div class="gap-quote">“{d2['gap_card']['question']}”</div>
        <div class="gap-body">{d2['gap_card']['body']}<br><br><strong>{d2['gap_card']['callout']}</strong></div>
      </div>
    </div>

    <div class="slide-footer">
      <span>Fraud research: 9% strict fraud (NRF 2025) vs 15.14% fraud + abuse (Appriss/Deloitte 2024). Details in notes.</span>
      <span>Slide 2 / 6</span>
    </div>
  </section>

  <!-- SLIDE 3: EVIDENCE ARENA & DECISION PANEL -->
  <section class="slide" id="slide-3">
    <div class="tag-label">{d3['tag']}</div>
    <h2 class="slide-title">{d3['headline']}</h2>
    <p class="slide-sub">{d3['subheadline']}</p>

    <div class="evidence-layout">
      <div class="arena-card">
        <div class="arena-pics-grid">
          <div class="arena-pic-box">
            <img src="{white_b64}" alt="White Headphones Ordered">
            <div class="img-badge badge-ordered">{d3['ordered_evidence']['label']}: {d3['ordered_evidence']['sku']} (WHITE)</div>
          </div>
          <div class="arena-pic-box">
            <img src="{black_b64}" alt="Black Headphones Observed">
            <div class="img-badge badge-observed">{d3['observed_evidence']['label']}: {d3['observed_evidence']['color'].upper()}</div>
          </div>
        </div>
        <div class="arena-caption">
          Visual Grounding Honesty: Keyframe resolution proves black casing. Exact SKU barcode is unreadable in this frame; ReturnLens factually records 'Observed Color: Black · Exact SKU: Not verified' and cites frame 00:07.
        </div>
      </div>

      <div class="decision-panel-card">
        <div>
          <div class="dec-tag">{d3['decision_panel']['tag']}</div>
          <div class="dec-title">{d3['decision_panel']['title']}</div>
          <div class="dec-action">{d3['decision_panel']['next_action']}</div>

          <div class="dec-section-head">Key Findings:</div>
          <ul class="dec-list">
            <li>{d3['decision_panel']['observations'][0]}</li>
            <li>{d3['decision_panel']['observations'][1]}</li>
          </ul>

          <div class="dec-section-head">Seller Resolution Options:</div>
          <ul class="dec-list">
            <li>{d3['decision_panel']['seller_options'][0]}</li>
            <li>{d3['decision_panel']['seller_options'][1]}</li>
            <li>{d3['decision_panel']['seller_options'][2]}</li>
          </ul>
        </div>

        <div class="dec-guardrail-note">
          {d3['decision_panel']['guardrail_note']}
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <span>Illustrative staged evidence · Mock Shopify &amp; Shippo APIs</span>
      <span>Slide 3 / 6</span>
    </div>
  </section>

  <!-- SLIDE 4: ARCHITECTURE (DARK) -->
  <section class="slide dark" id="slide-4">
    <div class="tag-label">{d4['tag']}</div>
    <h2 class="slide-title">{d4['headline']}</h2>
    <p class="slide-sub">{d4['subheadline']}</p>

    <div class="arch-container">
      <div class="zones-row">
        <div class="zone-card">
          <div class="zone-num">01 MODEL ZONE</div>
          <div class="zone-title">Plan &amp; Observe</div>
          <div class="zone-desc">Planner validates JSON schema · Vision extracts keyframes &amp; non-binding visual metadata.</div>
        </div>
        <div class="zone-card code-zone">
          <div class="zone-num">02 CODE ZONE</div>
          <div class="zone-title">Retrieve &amp; Enforce Policy</div>
          <div class="zone-desc">Deterministic Python rules P-01 to P-08 · Shippo &amp; Shopify mock APIs enforce hard rules.</div>
        </div>
        <div class="zone-card gate-zone">
          <div class="zone-num">03 HUMAN SELLER GATE</div>
          <div class="zone-title">Authorize Consequential Action</div>
          <div class="zone-desc">Fail-closed authorization gate · 1-click human merchant confirmation for refund release.</div>
        </div>
      </div>

      <div class="stateful-box">
        <div class="stateful-head">{d4['case_c_flow']['title']}</div>
        <div class="nodes-row">
          <div class="state-node">{d4['case_c_flow']['steps'][0]}</div>
          <div class="state-arrow">→</div>
          <div class="state-node">{d4['case_c_flow']['steps'][1]}</div>
          <div class="state-arrow">→</div>
          <div class="state-node highlight">{d4['case_c_flow']['steps'][2]}</div>
          <div class="state-arrow">→</div>
          <div class="state-node highlight">{d4['case_c_flow']['steps'][3]}</div>
          <div class="state-arrow">→</div>
          <div class="state-node highlight">{d4['case_c_flow']['steps'][4]}</div>
          <div class="state-arrow">→</div>
          <div class="state-node">{d4['case_c_flow']['steps'][5]}</div>
        </div>
        <div class="stateful-desc">{d4['case_c_flow']['desc']}</div>
      </div>

      <div class="bottom-traces">
        <div class="trace-fast-path">{d4['secondary_route']['text']}</div>
        <div class="trace-audit">{d4['audit_output']['text']}</div>
      </div>
    </div>

    <div class="slide-footer">
      <span>Structured audit log recorded at every state transition · Decision priority: Contradiction &gt; Hard fail &gt; Unclear only &gt; All pass</span>
      <span>Slide 4 / 6</span>
    </div>
  </section>

  <!-- SLIDE 5: 4 SCENARIOS MATRIX -->
  <section class="slide" id="slide-5">
    <div class="tag-label">{d5['tag']}</div>
    <h2 class="slide-title">{d5['headline']}</h2>
    <p class="slide-sub">{d5['subheadline']}</p>

    <div class="scenarios-stack">
      <div class="sc-lane">
        <div class="sc-badge badge-01">{d5['cases'][0]['number']} · {d5['cases'][0]['name']}</div>
        <div class="sc-obs">{d5['cases'][0]['observation']}</div>
        <div class="sc-arr">→</div>
        <div class="sc-act">
          <div class="sc-act-head">{d5['cases'][0]['action']}</div>
          <div class="sc-act-desc">{d5['cases'][0]['detail']}</div>
        </div>
      </div>

      <div class="sc-lane">
        <div class="sc-badge badge-02">{d5['cases'][1]['number']} · {d5['cases'][1]['name']}</div>
        <div class="sc-obs">{d5['cases'][1]['observation']}</div>
        <div class="sc-arr">→</div>
        <div class="sc-act">
          <div class="sc-act-head">{d5['cases'][1]['action']}</div>
          <div class="sc-act-desc">{d5['cases'][1]['detail']}</div>
        </div>
      </div>

      <div class="sc-lane">
        <div class="sc-badge badge-03">{d5['cases'][2]['number']} · {d5['cases'][2]['name']}</div>
        <div class="sc-obs">{d5['cases'][2]['observation']}</div>
        <div class="sc-arr">→</div>
        <div class="sc-act">
          <div class="sc-act-head">{d5['cases'][2]['action']}</div>
          <div class="sc-act-desc">{d5['cases'][2]['detail']}</div>
        </div>
      </div>

      <div class="sc-lane">
        <div class="sc-badge badge-04">{d5['cases'][3]['number']} · {d5['cases'][3]['name']}</div>
        <div class="sc-obs">{d5['cases'][3]['observation']}</div>
        <div class="sc-arr">→</div>
        <div class="sc-act">
          <div class="sc-act-head">{d5['cases'][3]['action']}</div>
          <div class="sc-act-desc">{d5['cases'][3]['detail']}</div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <span>Staged prototype scenarios · Expected agent behaviors, not measured production metrics</span>
      <span>Slide 5 / 6</span>
    </div>
  </section>

  <!-- SLIDE 6: 24-HOUR PROTOTYPE PLAN -->
  <section class="slide" id="slide-6">
    <div class="tag-label">{d6['tag']}</div>
    <h2 class="slide-title">{d6['headline']}</h2>
    <p class="slide-sub">{d6['subheadline']}</p>

    <div class="plan-container">
      <div class="timeline-flow">
        <div class="t-step-box">
          <div class="t-time-tag">{d6['timeline'][0]['hours']} · {d6['timeline'][0]['phase']}</div>
          <div class="t-title">{d6['timeline'][0]['title']}</div>
          <div class="t-owner">{d6['timeline'][0]['owner']}</div>
          <div class="t-desc">{d6['timeline'][0]['desc']}</div>
        </div>
        <div class="t-step-box">
          <div class="t-time-tag">{d6['timeline'][1]['hours']} · {d6['timeline'][1]['phase']}</div>
          <div class="t-title">{d6['timeline'][1]['title']}</div>
          <div class="t-owner">{d6['timeline'][1]['owner']}</div>
          <div class="t-desc">{d6['timeline'][1]['desc']}</div>
        </div>
        <div class="t-step-box">
          <div class="t-time-tag">{d6['timeline'][2]['hours']} · {d6['timeline'][2]['phase']}</div>
          <div class="t-title">{d6['timeline'][2]['title']}</div>
          <div class="t-owner">{d6['timeline'][2]['owner']}</div>
          <div class="t-desc">{d6['timeline'][2]['desc']}</div>
        </div>
        <div class="t-step-box">
          <div class="t-time-tag">{d6['timeline'][3]['hours']} · {d6['timeline'][3]['phase']}</div>
          <div class="t-title">{d6['timeline'][3]['title']}</div>
          <div class="t-owner">{d6['timeline'][3]['owner']}</div>
          <div class="t-desc">{d6['timeline'][3]['desc']}</div>
        </div>
      </div>

      <div class="scope-split">
        <div class="scope-block must-deliver">
          <div class="scope-head">MUST DELIVER (CORE PROTOTYPE)</div>
          <ul class="scope-items">
            <li>{d6['scope_boundaries']['must_deliver'][0]}</li>
            <li>{d6['scope_boundaries']['must_deliver'][1]}</li>
            <li>{d6['scope_boundaries']['must_deliver'][2]}</li>
            <li>{d6['scope_boundaries']['must_deliver'][3]}</li>
            <li>{d6['scope_boundaries']['must_deliver'][4]}</li>
            <li>{d6['scope_boundaries']['must_deliver'][5]}</li>
          </ul>
        </div>

        <div class="scope-block cut-first">
          <div class="scope-head">CUT FIRST IF BEHIND (DEFERRED EXPANSION)</div>
          <ul class="scope-items">
            <li>{d6['scope_boundaries']['cut_first'][0]}</li>
            <li>{d6['scope_boundaries']['cut_first'][1]}</li>
            <li>{d6['scope_boundaries']['cut_first'][2]}</li>
            <li>{d6['scope_boundaries']['cut_first'][3]}</li>
            <li>{d6['scope_boundaries']['cut_first'][4]}</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <span>Team Rookie (3 Members) · PS-04 Autonomous Support Agent · 24-Hour Prototype Feasibility</span>
      <span>Slide 6 / 6</span>
    </div>
  </section>

</body>
</html>"""

def find_browser():
    candidates = [
        os.environ.get("CHROME_PATH"),
        os.environ.get("EDGE_PATH"),
        shutil.which("msedge"),
        shutil.which("microsoft-edge"),
        shutil.which("google-chrome"),
        shutil.which("chrome"),
        shutil.which("chromium"),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
        "/usr/bin/microsoft-edge"
    ]
    for c in candidates:
        if c and os.path.exists(c):
            return c
    return None

def build():
    # 1. Write HTML deliverables
    deliverable_html = base_dir / "deliverables" / "ReturnLens_v4.html"
    root_html = base_dir / "ReturnLens_v4.html"
    index_html = base_dir / "index.html"

    deliverable_html.parent.mkdir(parents=True, exist_ok=True)
    for p in [deliverable_html, root_html, index_html]:
        with open(p, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Wrote HTML: {p}")

    # 2. Render PDF via discovered browser
    deliverable_pdf = base_dir / "deliverables" / "ReturnLens_v4.pdf"
    root_pdf = base_dir / "ReturnLens_v4.pdf"

    browser_bin = find_browser()
    if not browser_bin:
        raise FileNotFoundError(
            "No headless browser (Edge or Chrome) discovered on system. "
            "Set CHROME_PATH or EDGE_PATH environment variable."
        )

    file_uri = deliverable_html.resolve().as_uri()
    cmd = [
        str(browser_bin),
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={deliverable_pdf}",
        file_uri
    ]

    print(f"Rendering PDF using: {browser_bin}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Browser PDF rendering failed with code {res.returncode}:\n{res.stderr}")

    if not deliverable_pdf.exists() or deliverable_pdf.stat().st_size == 0:
        raise RuntimeError(f"PDF was not generated or is empty: {deliverable_pdf}")

    shutil.copy2(deliverable_pdf, root_pdf)
    print(f"Generated & Synced PDF: {root_pdf} ({root_pdf.stat().st_size} bytes)")

    # 3. Render slide PNGs and preview contact sheet
    doc = fitz.open(deliverable_pdf)
    print(f"Rendered PDF page count: {len(doc)}")
    if len(doc) != 6:
        raise ValueError(f"Expected exactly 6 pages, got {len(doc)}")

    slides_png_dir = assets_dir / "slides"
    slides_png_dir.mkdir(parents=True, exist_ok=True)

    slide_imgs = []
    for i in range(len(doc)):
        page = doc[i]
        pix = page.get_pixmap(dpi=150)
        png_path = slides_png_dir / f"slide_{i+1}.png"
        pix.save(str(png_path))
        slide_imgs.append(Image.open(png_path))

    # Build 3x2 grid preview image: 768*3 + 48 = 2352w, 432*2 + 36 = 900h
    thumb_w = 768
    thumb_h = 432
    grid_w = thumb_w * 3 + 48
    grid_h = thumb_h * 2 + 36

    preview_img = Image.new('RGB', (grid_w, grid_h), color=(15, 26, 22))

    for idx, simg in enumerate(slide_imgs[:6]):
        col = idx % 3
        row = idx // 3
        x = 16 + col * (thumb_w + 8)
        y = 12 + row * (thumb_h + 12)
        resized = simg.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        preview_img.paste(resized, (x, y))

    deliverable_preview = base_dir / "deliverables" / "ReturnLens_v4_preview.png"
    root_preview = base_dir / "ReturnLens_v4_preview.png"

    preview_img.save(deliverable_preview, format="PNG", optimize=True)
    preview_img.save(root_preview, format="PNG", optimize=True)
    print(f"Saved preview: {deliverable_preview} ({deliverable_preview.stat().st_size} bytes, dimensions {preview_img.size})")

if __name__ == "__main__":
    build()
