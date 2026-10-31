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
    --blue-light: #EFF6FF;
    --blue-dark: #1E40AF;
    --text-muted: #596E64;
    --text-subtle: #7A8E85;
    --border-light: #E2DED4;
    --border-dark: #223830;
    --card-dark: #172621;
    --card-dark-alt: #121F1B;
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
    padding: 46px 64px 38px 64px;
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
    margin-bottom: 8px;
  }}

  .slide.dark .tag-label {{
    color: var(--teal-accent);
  }}

  .slide-title {{
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -1px;
    line-height: 1.15;
    color: var(--dark-green);
    margin-bottom: 6px;
  }}

  .slide.dark .slide-title {{
    color: #F5F3EF;
  }}

  .slide-sub {{
    font-size: 18px;
    font-weight: 400;
    line-height: 1.35;
    color: var(--text-muted);
    margin-bottom: 18px;
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

  /* SLIDE 1 STYLES */
  .hero-layout {{
    display: grid;
    grid-template-columns: 38% 62%;
    gap: 36px;
    flex: 1;
    align-items: stretch;
  }}

  .hero-left {{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding-bottom: 20px;
  }}

  .hero-title {{
    font-size: 58px;
    font-weight: 900;
    letter-spacing: -2px;
    color: var(--dark-green);
    line-height: 1;
    margin-bottom: 12px;
  }}

  .hero-statement {{
    font-size: 24px;
    font-weight: 700;
    color: var(--dark-green);
    line-height: 1.25;
    margin-bottom: 14px;
  }}

  .hero-summary {{
    font-size: 13.5px;
    line-height: 1.5;
    color: var(--text-muted);
    margin-bottom: 20px;
  }}

  .hero-metrics-row {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
  }}

  .metric-card {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    padding: 12px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}

  .metric-val {{
    font-size: 22px;
    font-weight: 800;
    color: var(--dark-green);
    line-height: 1.1;
    margin-bottom: 4px;
  }}

  .metric-lbl {{
    font-size: 9.5px;
    color: var(--text-muted);
    line-height: 1.3;
  }}

  .console-wrapper {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    display: flex;
    flex-direction: column;
    box-shadow: 0 12px 32px rgba(0,0,0,0.06);
  }}

  .console-header {{
    background: #1F302A;
    color: var(--teal-accent);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    padding: 12px 18px;
    letter-spacing: 1px;
    display: flex;
    justify-content: space-between;
  }}

  .console-body {{
    padding: 16px 20px;
    display: flex;
    flex-direction: column;
    gap: 14px;
    flex: 1;
    justify-content: space-between;
  }}

  .console-split {{
    display: grid;
    grid-template-columns: 200px 1fr;
    gap: 18px;
    align-items: center;
  }}

  .console-img-box {{
    width: 200px;
    height: 160px;
    border: 1px solid var(--border-light);
    overflow: hidden;
    position: relative;
    background: #FAFAFA;
  }}

  .console-img-box img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
  }}

  .console-data-col {{
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}

  .c-label {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9.5px;
    color: var(--text-subtle);
    font-weight: 700;
    letter-spacing: 0.5px;
  }}

  .c-val {{
    font-size: 12px;
    font-weight: 700;
    color: var(--dark-green);
    line-height: 1.35;
  }}

  .c-alert-box {{
    background: var(--coral-light);
    border: 1px solid var(--coral);
    padding: 10px 14px;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}

  .c-alert-title {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    color: var(--coral-dark);
  }}

  .c-alert-desc {{
    font-size: 11px;
    color: var(--coral-dark);
    line-height: 1.35;
  }}

  .c-status-bar {{
    background: var(--amber-light);
    padding: 8px 12px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9.5px;
    font-weight: 700;
    color: #92400E;
    text-align: center;
  }}

  .c-button {{
    background: var(--primary-teal);
    color: #FFFFFF;
    text-align: center;
    padding: 12px;
    font-weight: 700;
    font-size: 13.5px;
    letter-spacing: 0.5px;
  }}

  /* SLIDE 2 STYLES */
  .problem-layout {{
    display: grid;
    grid-template-columns: 1fr 1.15fr 1fr;
    gap: 18px;
    flex: 1;
    align-items: stretch;
    padding-bottom: 24px;
  }}

  .prob-col {{
    display: flex;
    flex-direction: column;
    gap: 16px;
  }}

  .source-card {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    padding: 18px 20px;
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}

  .s-num {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    color: var(--primary-teal);
    letter-spacing: 1px;
    margin-bottom: 6px;
  }}

  .s-title {{
    font-size: 14px;
    font-weight: 700;
    color: var(--dark-green);
    margin-bottom: 4px;
  }}

  .s-desc {{
    font-size: 11.5px;
    color: var(--text-muted);
    line-height: 1.4;
  }}

  .gap-pillar {{
    background: var(--dark-green);
    color: #F5F3EF;
    border: 2px solid var(--coral);
    padding: 24px 22px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
  }}

  .gap-tag {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: var(--coral);
    margin-bottom: 8px;
  }}

  .gap-title {{
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.3px;
    margin-bottom: 12px;
    line-height: 1.25;
    color: #FFFFFF;
  }}

  .gap-body {{
    font-size: 12px;
    line-height: 1.5;
    color: #D1D5DB;
    margin-bottom: 16px;
  }}

  .gap-stat-box {{
    border-top: 1px solid #2B4239;
    padding-top: 12px;
  }}

  .gap-stat-num {{
    font-size: 17px;
    font-weight: 800;
    color: var(--coral);
    margin-bottom: 4px;
  }}

  .gap-stat-txt {{
    font-size: 9px;
    color: #9CA3AF;
    line-height: 1.35;
  }}

  /* SLIDE 3 STYLES */
  .demo-layout {{
    display: grid;
    grid-template-columns: 66% 34%;
    gap: 24px;
    flex: 1;
    align-items: stretch;
    padding-bottom: 24px;
  }}

  .evidence-arena {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    padding: 16px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .arena-pics {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    flex: 1;
  }}

  .pic-wrapper {{
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}

  .pic-frame {{
    flex: 1;
    border: 1px solid var(--border-light);
    overflow: hidden;
    background: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 250px;
  }}

  .pic-frame img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
  }}

  .pic-badge {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9.5px;
    font-weight: 700;
    padding: 6px 8px;
    text-align: center;
  }}

  .badge-ordered {{ background: var(--teal-light); color: var(--primary-teal); }}
  .badge-observed {{ background: var(--coral-light); color: var(--coral-dark); }}

  .arena-caption {{
    font-size: 11px;
    color: var(--text-muted);
    line-height: 1.45;
    border-top: 1px solid var(--border-light);
    padding-top: 10px;
    margin-top: 10px;
  }}

  .decision-console {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    padding: 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .dec-tag {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9.5px;
    font-weight: 700;
    color: var(--coral);
    margin-bottom: 4px;
  }}

  .dec-title {{
    font-size: 16px;
    font-weight: 800;
    color: var(--coral-dark);
    margin-bottom: 6px;
  }}

  .dec-sub {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9.5px;
    font-weight: 700;
    color: var(--coral-dark);
    margin-bottom: 12px;
    line-height: 1.35;
  }}

  .dec-opt-title {{
    font-size: 11.5px;
    font-weight: 700;
    color: var(--dark-green);
    margin-bottom: 6px;
  }}

  .dec-opt-list {{
    font-size: 10px;
    color: var(--text-muted);
    line-height: 1.4;
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin-bottom: 14px;
  }}

  .dec-guardrail {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    color: var(--text-subtle);
    border-top: 1px solid var(--border-light);
    padding-top: 10px;
    line-height: 1.35;
  }}

  /* SLIDE 4 STYLES (DARK ARCHITECTURE) */
  .arch-layout {{
    display: flex;
    flex-direction: column;
    gap: 16px;
    flex: 1;
    padding-bottom: 24px;
  }}

  .arch-pipeline {{
    display: flex;
    gap: 8px;
    align-items: center;
  }}

  .pipe-step {{
    flex: 1;
    background: var(--card-dark);
    border: 1px solid var(--border-dark);
    padding: 10px 8px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 84px;
  }}

  .pipe-step.model-step {{ border-top: 3px solid var(--teal-accent); }}
  .pipe-step.code-step {{ border-top: 3px solid #E1F2EC; }}
  .pipe-step.human-step {{ border-top: 3px solid #FBBF24; }}

  .pipe-arrow {{
    font-family: 'IBM Plex Mono', monospace;
    color: var(--teal-accent);
    font-size: 13px;
    font-weight: 800;
    flex-shrink: 0;
  }}

  .pipe-num {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 8.5px;
    color: #6C8279;
    margin-bottom: 2px;
  }}

  .pipe-title {{
    font-size: 12px;
    font-weight: 700;
    color: #F5F3EF;
    line-height: 1.2;
    margin-bottom: 3px;
  }}

  .pipe-role-tag {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 8px;
    font-weight: 700;
    padding: 2px 4px;
    display: inline-block;
    align-self: flex-start;
  }}

  .tag-model {{ background: #00382B; color: var(--teal-accent); }}
  .tag-code {{ background: #263831; color: #F5F3EF; }}
  .tag-human {{ background: #45260A; color: #FBBF24; }}

  .agent-paths-grid {{
    display: grid;
    grid-template-columns: 1.5fr 1fr;
    gap: 14px;
  }}

  .agent-path-card {{
    background: #14221D;
    border: 1.5px solid #2563EB;
    padding: 14px 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}

  .agent-path-card.fast {{
    border-color: #059669;
  }}

  .path-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  .path-title {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9.5px;
    font-weight: 700;
    letter-spacing: 0.5px;
  }}

  .path-title.loop {{ color: #93C5FD; }}
  .path-title.fast {{ color: #34D399; }}

  .trace-steps {{
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
  }}

  .trace-node {{
    background: #1F302A;
    border: 1px solid #374151;
    color: #F3F4F6;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 8.5px;
    padding: 4px 6px;
  }}

  .trace-node.wait {{
    background: #1E3A8A;
    border-color: #60A5FA;
    color: #DBEAFE;
    font-weight: 700;
  }}

  .trace-arrow {{
    color: #9CA3AF;
    font-size: 9px;
  }}

  .path-desc {{
    font-size: 10px;
    color: #A3B8B0;
    line-height: 1.35;
  }}

  .arch-legend {{
    background: var(--card-dark-alt);
    border: 1px solid var(--border-dark);
    padding: 10px 14px;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px 16px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    color: #A3B8B0;
    line-height: 1.35;
  }}

  /* SLIDE 5 STYLES */
  .scenarios-grid {{
    display: flex;
    flex-direction: column;
    gap: 10px;
    flex: 1;
    padding-bottom: 24px;
  }}

  .scenario-lane {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    padding: 12px 18px;
    display: grid;
    grid-template-columns: 160px 1fr 24px 1.15fr;
    gap: 16px;
    align-items: center;
    flex: 1;
  }}

  .sc-badge {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    padding: 8px 10px;
    text-align: center;
  }}

  .badge-match {{ background: var(--teal-light); color: var(--primary-teal); }}
  .badge-mismatch {{ background: var(--coral-light); color: var(--coral-dark); }}
  .badge-unclear {{ background: var(--blue-light); color: var(--blue-dark); }}
  .badge-continuity {{ background: #ECFDF5; color: #065F46; }}

  .sc-evidence {{
    font-size: 12px;
    font-weight: 600;
    color: var(--dark-green);
    line-height: 1.35;
  }}

  .sc-arrow {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 16px;
    color: var(--primary-teal);
    text-align: center;
  }}

  .sc-action {{
    font-size: 11.5px;
    color: var(--text-muted);
    line-height: 1.35;
  }}

  /* SLIDE 6 STYLES */
  .timeline-container {{
    display: flex;
    flex-direction: column;
    gap: 16px;
    flex: 1;
    padding-bottom: 24px;
  }}

  .timeline-table-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
  }}

  .t-cell {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    border-top: 4px solid var(--primary-teal);
    padding: 14px;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}

  .t-time {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10.5px;
    font-weight: 700;
    color: var(--primary-teal);
  }}

  .t-title {{
    font-size: 13.5px;
    font-weight: 700;
    color: var(--dark-green);
  }}

  .t-owner {{
    font-size: 11px;
    font-weight: 700;
    color: var(--primary-teal);
    margin-bottom: 2px;
  }}

  .t-desc {{
    font-size: 10px;
    color: var(--text-muted);
    line-height: 1.35;
  }}

  .scope-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    flex: 1;
  }}

  .scope-card {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    padding: 16px 20px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}

  .scope-card.scope-in {{ border-left: 5px solid var(--primary-teal); }}
  .scope-card.scope-out {{ border-left: 5px solid var(--coral); }}

  .scope-head {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11.5px;
    font-weight: 700;
  }}

  .scope-in .scope-head {{ color: var(--primary-teal); }}
  .scope-out .scope-head {{ color: var(--coral); }}

  .scope-text {{
    font-size: 11.5px;
    color: var(--dark-green);
    line-height: 1.5;
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
          <p class="hero-summary">{d1['summary']}<br><br>When a customer submits a return video, ReturnLens extracts keyframes, cross-references order truth and shipping timestamps, verifies deterministic code policies, and gives the solo seller a 1-click decision console.</p>
        </div>

        <div class="hero-metrics-row">
          <div class="metric-card">
            <div class="metric-val" style="color: var(--coral);">15–20m</div>
            <div class="metric-lbl">Manual triage time eliminated</div>
          </div>
          <div class="metric-card">
            <div class="metric-val" style="color: var(--primary-teal);">1-Click</div>
            <div class="metric-lbl">Merchant human verification</div>
          </div>
          <div class="metric-card">
            <div class="metric-val">24h</div>
            <div class="metric-lbl">Prototype build feasibility</div>
          </div>
        </div>
      </div>

      <div class="console-wrapper">
        <div class="console-header">
          <span>{d1['console_mockup']['title']}</span>
          <span>{d1['console_mockup']['case_badge']}</span>
        </div>
        <div class="console-body">
          <div class="console-split">
            <div class="console-img-box">
              <img src="{white_b64}" alt="White Headphones">
            </div>
            <div class="console-data-col">
              <div>
                <div class="c-label">ORDER INFORMATION</div>
                <div class="c-val">{d1['console_mockup']['order_info']['order_id']} · {d1['console_mockup']['order_info']['sku']}<br>{d1['console_mockup']['order_info']['color']} · Price: {d1['console_mockup']['order_info']['price']}<br>{d1['console_mockup']['order_info']['delivery']}</div>
              </div>
              <div>
                <div class="c-label">EVIDENCE CITATION (STAGED)</div>
                <div class="c-val" style="color: var(--text-muted); font-size: 11px;">{d1['console_mockup']['evidence_citation']['timestamp']}<br>{d1['console_mockup']['evidence_citation']['observation']}</div>
              </div>
            </div>
          </div>

          <div class="c-alert-box">
            <div class="c-alert-title">POLICY GATE: {d1['console_mockup']['evidence_citation']['status_badge']}</div>
            <div class="c-alert-desc">{d1['console_mockup']['policy_check']['window_check']} | {d1['console_mockup']['policy_check']['color_check']}</div>
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

  <!-- SLIDE 2: THE PROBLEM -->
  <section class="slide" id="slide-2">
    <div class="tag-label">{d2['tag']}</div>
    <h2 class="slide-title">{d2['headline']}</h2>
    <p class="slide-sub">{d2['subheadline']} · {d2['supporting_statement']}</p>

    <div class="problem-layout">
      <div class="prob-col">
        <div class="source-card">
          <div class="s-num">{d2['sources'][0]['number']} {d2['sources'][0]['name'].upper()}</div>
          <div class="s-title">{d2['sources'][0]['name']}</div>
          <div class="s-desc">{d2['sources'][0]['detail']}</div>
        </div>
        <div class="source-card">
          <div class="s-num">{d2['sources'][2]['number']} {d2['sources'][2]['name'].upper()}</div>
          <div class="s-title">{d2['sources'][2]['name']}</div>
          <div class="s-desc">{d2['sources'][2]['detail']}</div>
        </div>
      </div>

      <div class="gap-pillar">
        <div class="gap-tag">CRITICAL INFORMATION GAP</div>
        <div class="gap-title">{d2['gap_card']['title']}</div>
        <div class="gap-body">{d2['gap_card']['description']}</div>
        <div class="gap-stat-box">
          <div class="gap-stat-num">9.0% vs 15.14%</div>
          <div class="gap-stat-txt">{data['meta']['fraud_metrics']['nrf_2025']} | {data['meta']['fraud_metrics']['deloitte_2024']}<br>{data['meta']['fraud_metrics']['distinction']}</div>
        </div>
      </div>

      <div class="prob-col">
        <div class="source-card">
          <div class="s-num">{d2['sources'][1]['number']} {d2['sources'][1]['name'].upper()}</div>
          <div class="s-title">{d2['sources'][1]['name']}</div>
          <div class="s-desc">{d2['sources'][1]['detail']}</div>
        </div>
        <div class="source-card">
          <div class="s-num">{d2['sources'][3]['number']} {d2['sources'][3]['name'].upper()}</div>
          <div class="s-title">{d2['sources'][3]['name']}</div>
          <div class="s-desc">{d2['sources'][3]['detail']}</div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <span>Fraud statistics note: 9.0% (NRF 2025, fraud only) vs 15.14% (Appriss/Deloitte 2024, fraud + abuse)</span>
      <span>Slide 2 / 6</span>
    </div>
  </section>

  <!-- SLIDE 3: STAR DEMO -->
  <section class="slide" id="slide-3">
    <div class="tag-label">{d3['tag']}</div>
    <h2 class="slide-title">{d3['headline']}</h2>
    <p class="slide-sub">{d3['subheadline']}</p>

    <div class="demo-layout">
      <div class="evidence-arena">
        <div class="arena-pics">
          <div class="pic-wrapper">
            <div class="pic-frame">
              <img src="{white_b64}" alt="White Headphones Ordered">
            </div>
            <div class="pic-badge badge-ordered">{d3['ordered_evidence']['label']}: {d3['ordered_evidence']['sku']} (WHITE)</div>
          </div>
          <div class="pic-wrapper">
            <div class="pic-frame">
              <img src="{black_b64}" alt="Black Headphones Unboxed">
            </div>
            <div class="pic-badge badge-observed">{d3['observed_evidence']['label']}: {d3['observed_evidence']['color'].upper()}</div>
          </div>
        </div>
        <div class="arena-caption">
          Visual Grounding Honesty: Keyframe resolution reveals black casing. Exact SKU barcode is unreadable in this frame; ReturnLens factually records 'Observed Color: Midnight Black · Exact SKU: Not verified' and cites frame 00:07.
        </div>
      </div>

      <div class="decision-console">
        <div>
          <div class="dec-tag">DETERMINISTIC POLICY GATE</div>
          <div class="dec-title">P-03: COLOR CONTRADICTION</div>
          <div class="dec-sub">{d3['decision_panel']['next_action']}<br>Observed: {d3['decision_panel']['observed_color']} · Exact SKU: {d3['decision_panel']['exact_sku']}</div>
          <div class="dec-opt-title">Seller Resolution Options:</div>
          <div class="dec-opt-list">
            <div>• {d3['decision_panel']['seller_options'][0]}</div>
            <div>• {d3['decision_panel']['seller_options'][1]}</div>
            <div>• {d3['decision_panel']['seller_options'][2]}</div>
          </div>
        </div>
        <div class="dec-guardrail">
          Financial Safety Ceiling:<br>
          {data['meta']['refund_guardrail']['formula']}<br>
          No auto-denial · No refund released without seller click
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <span>Illustrative staged evidence · Mock Shopify &amp; Shippo APIs</span>
      <span>Slide 3 / 6</span>
    </div>
  </section>

  <!-- SLIDE 4: ARCHITECTURE -->
  <section class="slide dark" id="slide-4">
    <div class="tag-label">{d4['tag']}</div>
    <h2 class="slide-title">{d4['headline']}</h2>
    <p class="slide-sub">{d4['subheadline']}</p>

    <div class="arch-layout">
      <!-- 6-Step Pipeline -->
      <div class="arch-pipeline">
        <div class="pipe-step model-step">
          <div>
            <div class="pipe-num">01 PLAN</div>
            <div class="pipe-title">Plan</div>
          </div>
          <span class="pipe-role-tag tag-model">MODEL</span>
        </div>
        <span class="pipe-arrow">→</span>

        <div class="pipe-step code-step">
          <div>
            <div class="pipe-num">02 RETRIEVE</div>
            <div class="pipe-title">Retrieve</div>
          </div>
          <span class="pipe-role-tag tag-code">CODE</span>
        </div>
        <span class="pipe-arrow">→</span>

        <div class="pipe-step code-step">
          <div>
            <div class="pipe-num">03 EVALUATE</div>
            <div class="pipe-title">Evaluate</div>
          </div>
          <span class="pipe-role-tag tag-code">CODE</span>
        </div>
        <span class="pipe-arrow">→</span>

        <div class="pipe-step model-step">
          <div>
            <div class="pipe-num">04 AUDIT</div>
            <div class="pipe-title">Audit</div>
          </div>
          <span class="pipe-role-tag tag-model">MODEL</span>
        </div>
        <span class="pipe-arrow">→</span>

        <div class="pipe-step human-step">
          <div>
            <div class="pipe-num">05 AUTHORIZE</div>
            <div class="pipe-title">Authorize</div>
          </div>
          <span class="pipe-role-tag tag-human">HUMAN</span>
        </div>
        <span class="pipe-arrow">→</span>

        <div class="pipe-step code-step">
          <div>
            <div class="pipe-num">06 RECORD</div>
            <div class="pipe-title">Record</div>
          </div>
          <span class="pipe-role-tag tag-code">CODE</span>
        </div>
      </div>

      <!-- Dual Operational Branches -->
      <div class="agent-paths-grid">
        <div class="agent-path-card">
          <div class="path-header">
            <span class="path-title loop">{d4['case_c_flow']['title']}</span>
            <span style="font-size: 8.5px; color: #93C5FD; font-family: 'IBM Plex Mono', monospace;">Observe → Decide → Act → Wait → Resume</span>
          </div>
          <div class="trace-steps">
            <span class="trace-node">Dark Frames</span>
            <span class="trace-arrow">→</span>
            <span class="trace-node">ask_for_evidence()</span>
            <span class="trace-arrow">→</span>
            <span class="trace-node wait">WAITING_FOR_EVIDENCE</span>
            <span class="trace-arrow">→</span>
            <span class="trace-node">Customer Uploads</span>
            <span class="trace-arrow">→</span>
            <span class="trace-node">Resume Case</span>
            <span class="trace-arrow">→</span>
            <span class="trace-node">Seller Review</span>
          </div>
          <div class="path-desc">When lighting is insufficient, the agent halts standard execution, prompts a targeted checklist, pauses state in WAITING_FOR_EVIDENCE, and seamlessly resumes context upon media receipt (1 retry limit protects customer experience).</div>
        </div>

        <div class="agent-path-card fast">
          <div class="path-header">
            <span class="path-title fast">SECONDARY PS-04 ROUTE: ORDER STATUS FAST PATH</span>
            <span style="font-size: 8.5px; color: #34D399; font-family: 'IBM Plex Mono', monospace;">Zero-Vision Direct Route</span>
          </div>
          <div class="trace-steps">
            <span class="trace-node">“Where is my order?”</span>
            <span class="trace-arrow">→</span>
            <span class="trace-node">Query Store &amp; Shippo APIs</span>
            <span class="trace-arrow">→</span>
            <span class="trace-node">Delivery Scan &amp; Time</span>
          </div>
          <div class="path-desc">Routine order queries take a direct tool route without calling heavy multimodal models. Escalates to human seller only if courier scan shows abnormal transit delay.</div>
        </div>
      </div>

      <!-- Governance Pillars -->
      <div class="arch-legend">
        <span><strong style="color: var(--teal-accent);">■ {d4['governance_rules'][0]['label']}:</strong> {d4['governance_rules'][0]['text']}</span>
        <span><strong style="color: #F5F3EF;">■ {d4['governance_rules'][1]['label']}:</strong> {d4['governance_rules'][1]['text']}</span>
        <span><strong style="color: #60A5FA;">■ {d4['governance_rules'][2]['label']}:</strong> {d4['governance_rules'][2]['text']}</span>
        <span><strong style="color: #FBBF24;">■ {d4['governance_rules'][3]['label']}:</strong> {d4['governance_rules'][3]['text']}</span>
      </div>
    </div>

    <div class="slide-footer">
      <span>Structured audit log recorded at every state transition · Decision priority: Contradiction &gt; Hard fail &gt; Unclear only &gt; All pass</span>
      <span>Slide 4 / 6</span>
    </div>
  </section>

  <!-- SLIDE 5: DEMO SCENARIOS -->
  <section class="slide" id="slide-5">
    <div class="tag-label">{d5['tag']}</div>
    <h2 class="slide-title">{d5['headline']}</h2>
    <p class="slide-sub">{d5['subheadline']}</p>

    <div class="scenarios-grid">
      <div class="scenario-lane">
        <div class="sc-badge badge-match">CASE {d5['cases'][0]['number']} · {d5['cases'][0]['name']}</div>
        <div class="sc-evidence">{d5['cases'][0]['observation']}</div>
        <div class="sc-arrow">→</div>
        <div class="sc-action"><strong>{d5['cases'][0]['state_action']}</strong><br>{d5['cases'][0]['action_detail']}</div>
      </div>

      <div class="scenario-lane">
        <div class="sc-badge badge-mismatch">CASE {d5['cases'][1]['number']} · {d5['cases'][1]['name']}</div>
        <div class="sc-evidence">{d5['cases'][1]['observation']}</div>
        <div class="sc-arrow">→</div>
        <div class="sc-action"><strong>{d5['cases'][1]['state_action']}</strong><br>{d5['cases'][1]['action_detail']}</div>
      </div>

      <div class="scenario-lane">
        <div class="sc-badge badge-unclear">CASE {d5['cases'][2]['number']} · {d5['cases'][2]['name']}</div>
        <div class="sc-evidence">{d5['cases'][2]['observation']}</div>
        <div class="sc-arrow">→</div>
        <div class="sc-action"><strong>{d5['cases'][2]['state_action']}</strong><br>{d5['cases'][2]['action_detail']}</div>
      </div>

      <div class="scenario-lane">
        <div class="sc-badge badge-continuity">CASE {d5['cases'][3]['number']} · {d5['cases'][3]['name']}</div>
        <div class="sc-evidence">{d5['cases'][3]['observation']}</div>
        <div class="sc-arrow">→</div>
        <div class="sc-action"><strong>{d5['cases'][3]['state_action']}</strong><br>{d5['cases'][3]['action_detail']}</div>
      </div>
    </div>

    <div class="slide-footer">
      <span>Staged prototype scenarios · Expected agent behaviors, not measured production metrics · Cap: min(₹4,999, remaining, paid)</span>
      <span>Slide 5 / 6</span>
    </div>
  </section>

  <!-- SLIDE 6: 24-HOUR BUILD PLAN -->
  <section class="slide" id="slide-6">
    <div class="tag-label">{d6['tag']}</div>
    <h2 class="slide-title">{d6['headline']}</h2>
    <p class="slide-sub">{d6['subheadline']}</p>

    <div class="timeline-container">
      <div class="timeline-table-grid">
        <div class="t-cell">
          <div class="t-time">{d6['timeline'][0]['hours']} · {d6['timeline'][0]['phase']}</div>
          <div class="t-title">{d6['timeline'][0]['title']}</div>
          <div class="t-owner">{d6['timeline'][0]['owner']}</div>
          <div class="t-desc">{d6['timeline'][0]['deliverables']}</div>
        </div>

        <div class="t-cell">
          <div class="t-time">{d6['timeline'][1]['hours']} · {d6['timeline'][1]['phase']}</div>
          <div class="t-title">{d6['timeline'][1]['title']}</div>
          <div class="t-owner">{d6['timeline'][1]['owner']}</div>
          <div class="t-desc">{d6['timeline'][1]['deliverables']}</div>
        </div>

        <div class="t-cell">
          <div class="t-time">{d6['timeline'][2]['hours']} · {d6['timeline'][2]['phase']}</div>
          <div class="t-title">{d6['timeline'][2]['title']}</div>
          <div class="t-owner">{d6['timeline'][2]['owner']}</div>
          <div class="t-desc">{d6['timeline'][2]['deliverables']}</div>
        </div>

        <div class="t-cell">
          <div class="t-time">{d6['timeline'][3]['hours']} · {d6['timeline'][3]['phase']}</div>
          <div class="t-title">{d6['timeline'][3]['title']}</div>
          <div class="t-owner">{d6['timeline'][3]['owner']}</div>
          <div class="t-desc">{d6['timeline'][3]['deliverables']}</div>
        </div>
      </div>

      <div class="scope-grid">
        <div class="scope-card scope-in">
          <div class="scope-head">MUST DELIVER (CORE PROTOTYPE)</div>
          <div class="scope-text">
            • Deterministic policy engine (P-01 to P-08)<br>
            • Evidence-pack keyframe citations<br>
            • Fail-closed seller authorization gate<br>
            • Structured JSON audit trail log<br>
            • Stateful clarification/resume loop<br>
            • 4 reproducible demo scenarios
          </div>
        </div>

        <div class="scope-card scope-out">
          <div class="scope-head">CUT FIRST IF BEHIND (DEFERRED EXPANSION)</div>
          <div class="scope-text">
            • Live carrier webhooks (keep mock courier)<br>
            • Multi-item return parsing (keep 1 item/return)<br>
            • Video OCR barcode scanner (keep visual color)<br>
            • Live payment gateways (keep draft refunds)<br>
            • Merchant analytics dashboard
          </div>
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
