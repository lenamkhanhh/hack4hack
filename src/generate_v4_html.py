import os
import sys
import shutil
import base64
import subprocess
from pathlib import Path
import fitz
from PIL import Image

# Robust path derivation (works anywhere, cross-platform)
base_dir = Path(__file__).resolve().parent.parent
assets_dir = base_dir / "src" / "assets"

def get_b64(fname):
    p = assets_dir / fname
    if not p.exists():
        raise FileNotFoundError(f"Required asset not found: {p}")
    with open(p, 'rb') as f:
        return 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode('utf-8')

hero_b64 = get_b64('hero_video_frame.jpg')
white_b64 = get_b64('demo_white_order.jpg')
black_b64 = get_b64('demo_black_frame.jpg')

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
    -webkit-font-smoothing: antialiased;
    border-radius: 0 !important;
  }}

  :root {{
    --cream: #F5F3EF;
    --dark-green: #172621;
    --primary-teal: #006B55;
    --teal-light: #E1F2EC;
    --coral: #D95D39;
    --coral-light: #FCECE8;
    --amber: #D97706;
    --amber-light: #FEF3C7;
    --border-light: #E2DED4;
    --text-muted: #596E64;
    --text-subtle: #7A8E85;
    --dark-bg: #0F1A16;
    --border-dark: #223830;
  }}

  body {{
    background-color: #E5E1D8;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--dark-green);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 0;
    gap: 40px;
  }}

  .deck-container {{
    display: flex;
    flex-direction: column;
    gap: 40px;
  }}

  .slide {{
    width: 1280px;
    height: 720px;
    background-color: var(--cream);
    position: relative;
    padding: 50px 64px 40px 64px;
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
    margin-bottom: 10px;
  }}

  .slide.dark .tag-label {{
    color: #00D1A7;
  }}

  .slide-title {{
    font-size: 34px;
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: -0.5px;
    color: var(--dark-green);
    margin-bottom: 6px;
  }}

  .slide.dark .slide-title {{
    color: #F5F3EF;
  }}

  .slide-sub {{
    font-size: 16px;
    font-weight: 400;
    line-height: 1.35;
    color: var(--text-muted);
    margin-bottom: 20px;
  }}

  .slide.dark .slide-sub {{
    color: #A3B8B0;
  }}

  .slide-footer {{
    position: absolute;
    bottom: 18px;
    left: 64px;
    right: 64px;
    display: flex;
    justify-content: space-between;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: var(--text-subtle);
    border-top: 1px solid var(--border-light);
    padding-top: 10px;
  }}

  .slide.dark .slide-footer {{
    border-top: 1px solid var(--border-dark);
    color: #5C786E;
  }}

  /* SLIDE 1 STYLES */
  .hero-layout {{
    display: grid;
    grid-template-columns: 1fr 1.35fr;
    gap: 44px;
    height: 100%;
    align-items: stretch;
  }}

  .hero-left {{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding-bottom: 24px;
  }}

  .hero-title {{
    font-size: 60px;
    font-weight: 900;
    letter-spacing: -2px;
    color: var(--dark-green);
    line-height: 1;
    margin-bottom: 12px;
  }}

  .hero-statement {{
    font-size: 19px;
    font-weight: 700;
    color: var(--primary-teal);
    line-height: 1.3;
    margin-bottom: 8px;
  }}

  .hero-desc {{
    font-size: 15px;
    color: var(--text-muted);
    line-height: 1.45;
  }}

  .hero-meta-box {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    border-left: 4px solid var(--primary-teal);
    padding: 14px 18px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: var(--dark-green);
    line-height: 1.55;
  }}

  .console-window {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    display: flex;
    flex-direction: column;
    height: 520px;
    overflow: hidden;
  }}

  .console-header {{
    background: var(--dark-green);
    color: #F5F3EF;
    padding: 12px 18px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  .console-body {{
    display: grid;
    grid-template-columns: 1.15fr 1fr;
    flex: 1;
    background: #FAFAFA;
  }}

  .console-video {{
    background: #000000;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }}

  .console-video img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
  }}

  .console-panel {{
    padding: 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    border-left: 1px solid var(--border-light);
    background: #FFFFFF;
  }}

  .info-group {{
    margin-bottom: 12px;
  }}

  .info-group .label {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    color: var(--text-subtle);
    text-transform: uppercase;
    margin-bottom: 3px;
  }}

  .info-group .val {{
    font-size: 13px;
    font-weight: 700;
    color: var(--dark-green);
  }}

  .info-group .val-sub {{
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 2px;
  }}

  .status-badge {{
    background: var(--amber-light);
    color: #92400E;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 800;
    padding: 8px 10px;
    text-align: center;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
  }}

  .btn-cta {{
    width: 100%;
    background: var(--primary-teal);
    color: #FFFFFF;
    border: none;
    padding: 11px;
    font-size: 12px;
    font-weight: 700;
    cursor: default;
    text-align: center;
  }}

  /* SLIDE 2 STYLES (RECOMPOSED 3-COLUMN LAYOUT: NO OVERLAP) */
  .problem-layout-3col {{
    display: grid;
    grid-template-columns: 1fr 1.05fr 1fr;
    gap: 20px;
    height: 450px;
    align-items: stretch;
  }}

  .source-col {{
    display: flex;
    flex-direction: column;
    gap: 16px;
    justify-content: space-between;
  }}

  .source-card {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    padding: 20px;
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}

  .s-label {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    color: var(--primary-teal);
    text-transform: uppercase;
    margin-bottom: 6px;
  }}

  .s-val {{
    font-size: 16px;
    font-weight: 700;
    color: var(--dark-green);
    margin-bottom: 4px;
    line-height: 1.3;
  }}

  .s-sub {{
    font-size: 11px;
    color: var(--text-muted);
    line-height: 1.4;
  }}

  .gap-pillar {{
    background: var(--dark-green);
    color: #F5F3EF;
    border: 2px solid var(--coral);
    padding: 28px 24px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.14);
  }}

  .gap-tag {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: var(--coral);
    margin-bottom: 12px;
  }}

  .gap-title {{
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.3px;
    margin-bottom: 14px;
    line-height: 1.25;
    color: #FFFFFF;
  }}

  .gap-text {{
    font-size: 12px;
    color: #D1D5DB;
    line-height: 1.55;
  }}

  /* SLIDE 3 STYLES */
  .demo-layout {{
    display: grid;
    grid-template-columns: 2fr 1.05fr;
    gap: 32px;
    height: 480px;
  }}

  .demo-evidence {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    position: relative;
  }}

  .evidence-card {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}

  .ev-header {{
    background: #FAF8F5;
    padding: 10px 14px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    color: var(--text-muted);
    border-bottom: 1px solid var(--border-light);
  }}

  .ev-img {{
    flex: 1;
    background: #000000;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    max-height: 330px;
  }}

  .ev-img img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
  }}

  .ev-footer {{
    padding: 12px 14px;
    font-size: 11px;
    font-family: 'IBM Plex Mono', monospace;
    color: var(--dark-green);
    background: #FFFFFF;
    border-top: 1px solid var(--border-light);
    line-height: 1.5;
  }}

  .ev-callout {{
    position: absolute;
    top: 42%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: var(--coral);
    color: #FFFFFF;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 800;
    padding: 6px 14px;
    letter-spacing: 1px;
    box-shadow: 0 4px 14px rgba(217,93,57,0.4);
    z-index: 10;
  }}

  .demo-decision {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    border-left: 4px solid var(--coral);
    padding: 22px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .decision-finding {{
    background: var(--coral-light);
    border: 1px solid #F87171;
    padding: 10px 14px;
    margin-top: 10px;
  }}

  .decision-finding .status-txt {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 800;
    color: #991B1B;
  }}

  .safety-box {{
    background: #FAF8F5;
    border: 1px solid var(--border-light);
    padding: 10px 12px;
    font-size: 11px;
    color: var(--text-muted);
    line-height: 1.45;
  }}

  /* SLIDE 4 STYLES (DARK) */
  .arch-pipeline {{
    display: flex;
    gap: 8px;
    margin-top: 12px;
    align-items: center;
  }}

  .pipe-step {{
    flex: 1;
    background: #172621;
    border: 1px solid var(--border-dark);
    padding: 12px 10px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 98px;
  }}

  .pipe-step.model-step {{ border-top: 3px solid #00D1A7; }}
  .pipe-step.code-step {{ border-top: 3px solid #F5F3EF; }}
  .pipe-step.human-step {{ border-top: 3px solid #FBBF24; }}

  .pipe-arrow {{
    font-family: 'IBM Plex Mono', monospace;
    color: #00D1A7;
    font-size: 14px;
    font-weight: 800;
    flex-shrink: 0;
  }}

  .pipe-num {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    color: #6C8279;
    margin-bottom: 2px;
  }}

  .pipe-title {{
    font-size: 12px;
    font-weight: 700;
    color: #F5F3EF;
    line-height: 1.2;
    margin-bottom: 4px;
  }}

  .pipe-role-tag {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 8.5px;
    font-weight: 700;
    padding: 2px 5px;
    display: inline-block;
    text-align: center;
    letter-spacing: 0.5px;
  }}

  .tag-code {{ background: #223830; color: #F5F3EF; }}
  .tag-model {{ background: rgba(0,209,167,0.18); color: #00D1A7; }}
  .tag-human {{ background: rgba(251,191,36,0.18); color: #FBBF24; }}

  /* Order status sub-bar */
  .ps04-route-strip {{
    margin-top: 12px;
    background: #14221D;
    border: 1px solid var(--border-dark);
    padding: 8px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
  }}

  .ps04-pill {{
    background: var(--primary-teal);
    color: #FFFFFF;
    padding: 3px 8px;
    font-weight: 700;
    font-size: 9px;
  }}

  .arch-branches {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-top: 14px;
  }}

  .branch-card {{
    background: #121F1B;
    border: 1px solid var(--border-dark);
    padding: 12px 14px;
  }}

  .branch-head {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
  }}

  .head-unclear {{ color: #60A5FA; }}
  .head-contradict {{ color: #F87171; }}
  .head-hardfail {{ color: #FBBF24; }}
  .head-pass {{ color: #34D399; }}

  .branch-desc {{
    font-size: 11px;
    color: #A3B8B0;
    line-height: 1.4;
  }}

  .arch-legend {{
    display: flex;
    flex-wrap: wrap;
    gap: 18px;
    margin-top: 14px;
    padding: 10px 14px;
    background: #121F1B;
    border: 1px solid var(--border-dark);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: #A3B8B0;
    line-height: 1.4;
  }}

  /* SLIDE 5 STYLES */
  .scenarios-grid {{
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 12px;
  }}

  .scenario-lane {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    padding: 12px 18px;
    display: flex;
    align-items: center;
    gap: 18px;
  }}

  .sc-badge {{
    width: 140px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10.5px;
    font-weight: 800;
    letter-spacing: 0.5px;
    padding: 6px 8px;
    text-align: center;
    flex-shrink: 0;
  }}

  .badge-ready {{ background: var(--teal-light); color: var(--primary-teal); }}
  .badge-mismatch {{ background: var(--coral-light); color: #991B1B; }}
  .badge-unclear {{ background: #EFF6FF; color: #1E40AF; }}
  .badge-continuity {{ background: #ECFDF5; color: #065F46; }}

  .sc-evidence {{
    flex: 1.1;
    font-size: 12.5px;
    color: var(--dark-green);
    line-height: 1.4;
  }}

  .sc-evidence strong {{
    color: var(--dark-green);
    font-weight: 700;
  }}

  .sc-arrow {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 16px;
    font-weight: 800;
    color: var(--primary-teal);
    flex-shrink: 0;
  }}

  .sc-action {{
    flex: 1.1;
    font-size: 12px;
    color: var(--text-muted);
    line-height: 1.4;
  }}

  .sc-action strong {{
    color: var(--dark-green);
  }}

  /* SLIDE 6 STYLES (TIMELINE TABLE + SCOPE DISCIPLINE) */
  .timeline-container {{
    margin-top: 12px;
  }}

  .timeline-table-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    border-bottom: 2px solid var(--primary-teal);
    padding-bottom: 14px;
    margin-bottom: 16px;
  }}

  .t-cell {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    padding: 12px 14px;
  }}

  .t-time {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 800;
    color: var(--primary-teal);
    margin-bottom: 4px;
    text-transform: uppercase;
  }}

  .t-title {{
    font-size: 13px;
    font-weight: 700;
    color: var(--dark-green);
    margin-bottom: 4px;
    line-height: 1.25;
  }}

  .t-owner {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: var(--text-muted);
    line-height: 1.35;
  }}

  .scope-split {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
  }}

  .scope-card {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    padding: 14px 18px;
  }}

  .scope-in {{ border-left: 4px solid var(--primary-teal); }}
  .scope-out {{ border-left: 4px solid var(--coral); }}

  .scope-head {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10.5px;
    font-weight: 800;
    letter-spacing: 0.5px;
    margin-bottom: 6px;
  }}

  .scope-in .scope-head {{ color: var(--primary-teal); }}
  .scope-out .scope-head {{ color: var(--coral); }}

  .scope-text {{
    font-size: 11.5px;
    color: var(--text-muted);
    line-height: 1.45;
  }}

  .closing-quote {{
    margin-top: 14px;
    background: #FAF8F5;
    border: 1px solid var(--border-light);
    padding: 10px 16px;
    font-size: 11.5px;
    font-style: italic;
    color: var(--dark-green);
    text-align: center;
  }}

  @page {{
    size: 1280px 720px;
    margin: 0;
  }}

  @media print {{
    body {{
      padding: 0;
      background: none;
      gap: 0;
    }}
    .deck-container {{
      gap: 0;
    }}
    .slide {{
      page-break-after: always;
      box-shadow: none;
      margin: 0;
      width: 1280px;
      height: 720px;
    }}
  }}
</style>
</head>
<body>

<div class="deck-container">

  <!-- SLIDE 1: PRODUCT LAUNCH & EXECUTIVE SUMMARY -->
  <section class="slide" id="slide-1">
    <div class="tag-label">AgentX Hackathon 2026 · Track PS-04</div>
    <div class="hero-layout">
      <div class="hero-left">
        <div>
          <h1 class="hero-title">RETURNLENS</h1>
          <div class="hero-statement">“Review returns with cited video evidence.”</div>
          <p class="hero-desc">An evidence-backed return triage agent for small direct-to-consumer sellers.</p>
        </div>
        <div class="hero-meta-box">
          <strong>Team Rookie · 3 members · PS-04 Track</strong><br>
          Target User: Solo D2C merchant managing orders and returns alone.<br>
          Scope in 24h: Return triage core + 1 zero-vision order-status route.<br>
          Guardrails: Fail-closed architecture · No autonomous refunds.
        </div>
      </div>

      <div class="hero-right">
        <div class="console-window">
          <div class="console-header">
            <span>RETURNLENS SELLER CONSOLE · CASE #RET-4082</span>
            <span>ORDER #ORD-9021</span>
          </div>
          <div class="console-body">
            <div class="console-video">
              <img src="{hero_b64}" alt="Inspection Frame">
            </div>
            <div class="console-panel">
              <div>
                <div class="info-group">
                  <div class="label">Order Truth</div>
                  <div class="val">HEAD-WHT-02 · White Headphones</div>
                  <div class="val-sub">₹1,499 · Delivered Day 4 (Within 7d window)</div>
                </div>
                <div class="info-group">
                  <div class="label">Visual Observation</div>
                  <div class="val">Inspection Frame 00:14</div>
                  <div class="val-sub">Potential casing damage flagged · Requires manual confirmation</div>
                </div>
                <div class="info-group">
                  <div class="label">Policy Verification</div>
                  <div class="val" style="color: #92400E;">P-01 Defect Check: FLAGGED FOR REVIEW</div>
                  <div class="val-sub">P-04 Return Window: PASS (Day 4 of 7)</div>
                </div>
              </div>
              <div>
                <div class="status-badge">READY FOR SELLER REVIEW (FLAGGED)</div>
                <button class="btn-cta">Review Evidence &amp; Authorize Draft</button>
                <div style="font-size: 10px; color: var(--text-subtle); text-align: center; margin-top: 6px; font-family: 'IBM Plex Mono', monospace;">
                  Illustrative staged evidence · Mock store data
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <span>ReturnLens · Idea Pitch Deck · PS-04 · Team Rookie (3 members)</span>
      <span>Slide 1 / 6</span>
    </div>
  </section>

  <!-- SLIDE 2: THE PROBLEM (RECOMPOSED 3-COLUMN NO-OVERLAP) -->
  <section class="slide" id="slide-2">
    <div class="tag-label">The Problem · Solo Seller Bottleneck</div>
    <h2 class="slide-title">One return decision. Four disconnected sources.</h2>
    <p class="slide-sub">The return decision is made from memory, before the evidence is checked.</p>
    
    <div class="problem-layout-3col">
      <!-- Left Column: Sources 01 & 03 -->
      <div class="source-col">
        <div class="source-card">
          <div class="s-label">01 Buyer Chat</div>
          <div class="s-val">“Received damaged item”</div>
          <div class="s-sub">Buyer upload: 30–60s unboxing video + reason in support message</div>
        </div>
        <div class="source-card">
          <div class="s-label">03 Courier Tracking</div>
          <div class="s-val">Delivered 4 days ago</div>
          <div class="s-sub">Shippo mock tracking API scan timestamp verification</div>
        </div>
      </div>

      <!-- Center Pillar: Critical Gap (Zero Overlap) -->
      <div class="gap-pillar">
        <div class="gap-tag">CRITICAL INFORMATION GAP</div>
        <div class="gap-title">NO SHARED EVIDENCE RECORD</div>
        <div class="gap-text">
          Today the seller opens 4 tabs, then decides alone. A wrong refund loses inventory; an unfair denial loses a customer.<br><br>
          The gap is that no single record ties order truth, video frames, policy clauses, and decisions together.
        </div>
      </div>

      <!-- Right Column: Sources 02 & 04 -->
      <div class="source-col">
        <div class="source-card">
          <div class="s-label">02 Order Record</div>
          <div class="s-val">White Headphones · ₹1,499</div>
          <div class="s-sub">Shopify mock store API product inventory catalog</div>
        </div>
        <div class="source-card">
          <div class="s-label">04 Return Policy</div>
          <div class="s-val">7-Day Window · Sealed Tag</div>
          <div class="s-sub">Deterministic code rules P-01 to P-08, never prompts</div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <span>Fraud estimates differ by definition: 9% (NRF 2025, fraud only) vs 15.14% (Appriss/Deloitte 2024, fraud + abuse).</span>
      <span>Slide 2 / 6</span>
    </div>
  </section>

  <!-- SLIDE 3: THE STAR DEMO (EVIDENCE BENCHMARK) -->
  <section class="slide" id="slide-3">
    <div class="tag-label">Visual Evidence Benchmark · Core Demonstration</div>
    <h2 class="slide-title">The order says white. The video shows black.</h2>
    <p class="slide-sub">ReturnLens surfaces the contradiction instead of auto-denying.</p>

    <div class="demo-layout">
      <div class="demo-evidence">
        <!-- Order Record -->
        <div class="evidence-card">
          <div class="ev-header">ORDER RECORD · STORE GROUND TRUTH</div>
          <div class="ev-img">
            <img src="{white_b64}" alt="White Headphone Store Truth">
          </div>
          <div class="ev-footer">
            <strong>HEAD-WHT-02</strong> · Matte White · ₹1,499<br>
            Delivered 4 days ago · Original tag present
          </div>
        </div>

        <!-- Video Frame -->
        <div class="evidence-card">
          <div class="ev-header">VIDEO FRAME · INTAKE TIMESTAMP 00:07</div>
          <div class="ev-img">
            <img src="{black_b64}" alt="Black Headphone Video Evidence">
          </div>
          <div class="ev-footer">
            <strong>Observed Color: Midnight Black</strong><br>
            Exact SKU: Not verified · Tag: Not visible in cited frame
          </div>
        </div>

        <div class="ev-callout">COLOR MISMATCH</div>
      </div>

      <div class="demo-decision">
        <div>
          <div class="tag-label" style="color: var(--coral);">Deterministic Policy Gate</div>
          <div style="font-size: 17px; font-weight: 800; color: var(--dark-green); margin-top: 4px;">P-03 Check: COLOR MISMATCH</div>
          <p style="font-size: 11.5px; color: var(--text-muted); margin-top: 3px;">
            Specification contradiction flagged against Shopify order manifest.
          </p>

          <div style="font-family: 'IBM Plex Mono', monospace; font-size: 10.5px; background: #FAF8F5; border: 1px solid var(--border-light); padding: 6px 10px; margin-top: 8px; color: var(--dark-green);">
            typed JSON, requires_seller_approval: true
          </div>

          <div class="decision-finding">
            <div class="status-txt">STATUS: ESCALATE (SELLER REVIEW REQUIRED)</div>
            <div style="font-size: 10.5px; color: #991B1B; margin-top: 3px;">Color mismatch observed · Exact SKU unconfirmed · No auto-denial.</div>
          </div>

          <div style="margin-top: 10px;">
            <div style="font-family: 'IBM Plex Mono', monospace; font-size: 10px; font-weight: 700; color: var(--text-subtle); text-transform: uppercase;">
              Seller Action Options
            </div>
            <div style="font-size: 11.5px; color: var(--dark-green); margin-top: 3px; line-height: 1.4;">
              1. Accept as merchant mis-shipment (seller mistake)<br>
              2. Ask customer for outside-box shipping label (buyer mistake)<br>
              3. Hold return for physical inspection at warehouse (potential swap)
            </div>
          </div>
        </div>

        <div class="safety-box">
          <strong>Deterministic Guardrails:</strong><br>
          • Cap: 0 &lt; amount &le; min(₹4,999, remaining refundable amount, order paid amount)<br>
          • No automatic customer denial · No refund released without seller click
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <span>Illustrative staged evidence · Mock Shopify &amp; Shippo APIs</span>
      <span>Slide 3 / 6</span>
    </div>
  </section>

  <!-- SLIDE 4: SYSTEM ARCHITECTURE (DARK) -->
  <section class="slide dark" id="slide-4">
    <div class="tag-label">System Architecture · Deterministic Pipeline</div>
    <h2 class="slide-title">Models observe. Code verifies. Seller authorizes.</h2>
    <p class="slide-sub">Policy checks and seller approval control actions.</p>

    <!-- 6-Step Horizontal Pipeline with Directional Arrows -->
    <div class="arch-pipeline">
      <div class="pipe-step model-step">
        <div>
          <div class="pipe-num">01 PLAN</div>
          <div class="pipe-title">Planner</div>
        </div>
        <span class="pipe-role-tag tag-model">MODEL</span>
      </div>
      <span class="pipe-arrow">→</span>

      <div class="pipe-step code-step">
        <div>
          <div class="pipe-num">02 RETRIEVE</div>
          <div class="pipe-title">Tools &amp; Video</div>
        </div>
        <span class="pipe-role-tag tag-code">CODE</span>
      </div>
      <span class="pipe-arrow">→</span>

      <div class="pipe-step code-step">
        <div>
          <div class="pipe-num">03 EVALUATE</div>
          <div class="pipe-title">Policy Engine</div>
        </div>
        <span class="pipe-role-tag tag-code">CODE</span>
      </div>
      <span class="pipe-arrow">→</span>

      <div class="pipe-step model-step">
        <div>
          <div class="pipe-num">04 AUDIT</div>
          <div class="pipe-title">Critic</div>
        </div>
        <span class="pipe-role-tag tag-model">MODEL</span>
      </div>
      <span class="pipe-arrow">→</span>

      <div class="pipe-step human-step">
        <div>
          <div class="pipe-num">05 AUTHORIZE</div>
          <div class="pipe-title">Seller Gate</div>
        </div>
        <span class="pipe-role-tag tag-human">HUMAN</span>
      </div>
      <span class="pipe-arrow">→</span>

      <div class="pipe-step code-step">
        <div>
          <div class="pipe-num">06 RECORD</div>
          <div class="pipe-title">Audit Log</div>
        </div>
        <span class="pipe-role-tag tag-code">CODE</span>
      </div>
    </div>

    <!-- Secondary PS-04 Order Status Route -->
    <div class="ps04-route-strip">
      <div style="display: flex; align-items: center; gap: 10px;">
        <span class="ps04-pill">SECONDARY PS-04 ROUTE</span>
        <span style="color: #F5F3EF; font-weight: 600;">Order Status Inquiry:</span>
        <span style="color: #A3B8B0;">Customer: “Where is my order?” → Mock Store API → Courier Scan → Instant Delivery Timestamp</span>
      </div>
      <span style="color: #00D1A7;">Zero-Vision Fast Path</span>
    </div>

    <!-- 4 Decision Function Outcomes (Strict Priority Order) -->
    <div class="arch-branches">
      <div class="branch-card">
        <div class="branch-head head-contradict">1. CONTRADICTION → ESCALATE</div>
        <div class="branch-desc">Discrepancy flagged (e.g. Case B). Inhibits automated label/refund. Seller reviews 3 options.</div>
      </div>

      <div class="branch-card">
        <div class="branch-head head-hardfail">2. HARD FAIL → ESCALATE</div>
        <div class="branch-desc">Mandatory rule violation (e.g. expired return window). Seller makes final decision; never auto-deny.</div>
      </div>

      <div class="branch-card">
        <div class="branch-head head-unclear">3. UNCLEAR ONLY → ASK MORE</div>
        <div class="branch-desc">Low brightness or blurry barcode (e.g. Case C). Prompts exact re-film checklist (1 retry limit).</div>
      </div>

      <div class="branch-card">
        <div class="branch-head head-pass">4. ALL PASS → APPROVE REVIEW</div>
        <div class="branch-desc">All clauses pass (e.g. Case A). Prepares mock label and drafts refund in pending_return_receipt.</div>
      </div>
    </div>

    <!-- Architecture Guarantees & Critic -->
    <div class="arch-legend">
      <span><strong style="color: #00D1A7;">■ Model Calls:</strong> Exactly 3 base calls per case: planner, vision, critic, plus retries</span>
      <span><strong style="color: #F5F3EF;">■ Policy Clauses:</strong> Deterministic Python code rules P-01 to P-08, never prompts</span>
      <span><strong style="color: #60A5FA;">■ Critic Duty:</strong> The critic reviews cited frames and flags unsupported observations</span>
      <span><strong style="color: #FBBF24;">■ Safety Boundary:</strong> Prompt injection cannot alter policy code or bypass human gate</span>
    </div>

    <div class="slide-footer">
      <span>Structured audit log recorded at every state transition · Decision priority: Contradiction &gt; Hard fail &gt; Unclear only &gt; All pass</span>
      <span>Slide 4 / 6</span>
    </div>
  </section>

  <!-- SLIDE 5: FOUR DEMO BENCHMARK SCENARIOS -->
  <section class="slide" id="slide-5">
    <div class="tag-label">Demo Scenarios · Grounded Verification</div>
    <h2 class="slide-title">Four scenarios. Four predictable behaviors.</h2>
    <p class="slide-sub">Every decision can be clicked back to a frame, a clause, and a log entry.</p>

    <div class="scenarios-grid">
      <!-- Case A -->
      <div class="scenario-lane">
        <div class="sc-badge badge-ready">CASE A · READY</div>
        <div class="sc-evidence">
          <strong>ORD-1042</strong> (₹1,499) · SKU matches manifest, tag visible, defect confirmed within 7-day window.
        </div>
        <div class="sc-arrow">→</div>
        <div class="sc-action">
          Seller approval releases mock return label and refund draft in <strong>pending_return_receipt</strong>, not executed refund.
        </div>
      </div>

      <!-- Case B -->
      <div class="scenario-lane">
        <div class="sc-badge badge-mismatch">CASE B · MISMATCH</div>
        <div class="sc-evidence">
          <strong>HEAD-WHT-02</strong> (White) ordered vs Frame 00:07 showing Black item · SKU unverified.
        </div>
        <div class="sc-arrow">→</div>
        <div class="sc-action">
          <strong>ESCALATE</strong> (no label, no refund, no denial). Seller options: mis-shipment / box label / physical inspection.
        </div>
      </div>

      <!-- Case C -->
      <div class="scenario-lane">
        <div class="sc-badge badge-unclear">CASE C · UNCLEAR</div>
        <div class="sc-evidence">
          <strong>4-second dark video</strong>, brightness 28, only 2 usable frames · Unclear evidence check.
        </div>
        <div class="sc-arrow">→</div>
        <div class="sc-action">
          Case stays open with exact re-film checklist. One retry limit prevents customer lock-out.
        </div>
      </div>

      <!-- Case D -->
      <div class="scenario-lane">
        <div class="sc-badge badge-continuity">CASE D · CONTEXT</div>
        <div class="sc-evidence">
          <strong>Parcel-to-product take</strong>: opening sealed parcel to product reveal in one continuous take.
        </div>
        <div class="sc-arrow">→</div>
        <div class="sc-action">
          Expected behavior: inspect sequence continuity and flag missing transitions for seller review.
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <span>Staged benchmark scenarios · Expected prototype behaviors, not measured production metrics · Cap: min(₹4,999, remaining refundable amount, order paid amount)</span>
      <span>Slide 5 / 6</span>
    </div>
  </section>

  <!-- SLIDE 6: 24-HOUR EXECUTION (TIMELINE GRID) -->
  <section class="slide" id="slide-6">
    <div class="tag-label">Execution Plan · Team Rookie (3 Members)</div>
    <h2 class="slide-title">Built for a 24-hour sprint.</h2>
    <p class="slide-sub">Buildable in 24 hours by 3 people, if the scope stays narrow.</p>

    <div class="timeline-container">
      <div class="timeline-table-grid">
        <div class="t-cell">
          <div class="t-time">00h – 06h</div>
          <div class="t-title">Mock APIs &amp; Agent Core</div>
          <div class="t-owner">Person A (Backend)<br>LangGraph skeleton, mock store/courier fixtures, order status route</div>
        </div>

        <div class="t-cell">
          <div class="t-time">06h – 12h</div>
          <div class="t-title">Evidence Pipeline &amp; Policy</div>
          <div class="t-owner">Person B (Video &amp; UI)<br>FFmpeg keyframe indexer, Python rules P-01 to P-08, critic prompt</div>
        </div>

        <div class="t-cell">
          <div class="t-time">12h – 18h</div>
          <div class="t-title">Integration &amp; 4 Scenarios</div>
          <div class="t-owner">Person C (Integration)<br>End-to-end wiring, 4 staged demo cases (A–D), seller console UI</div>
        </div>

        <div class="t-cell">
          <div class="t-time">18h – 24h</div>
          <div class="t-title">Testing, Polish &amp; Submission</div>
          <div class="t-owner">All 3 Members<br>Fallback testing, edge cases, video walkthrough recording, README</div>
        </div>
      </div>

      <div class="scope-split">
        <div class="scope-card scope-in">
          <div class="scope-head">NEVER CUT (CORE ENGINE)</div>
          <div class="scope-text">
            Deterministic policy engine (P-01 to P-08) · Evidence-pack frame citation · Fail-closed seller approval gate · Structured JSON audit log · 4 reproducible demo cases.
          </div>
        </div>

        <div class="scope-card scope-out">
          <div class="scope-head">CUT FIRST (DEFERRED EXPANSION)</div>
          <div class="scope-text">
            Video OCR barcode scanner · Auto-drafted customer email reply · Seller analytics dashboard · Production payment gateways / live WhatsApp webhooks.
          </div>
        </div>
      </div>

      <div class="closing-quote">
        “The winning hackathon agent is not the one with the most tool definitions. It is the one where every action is held to evidence, and the seller stays in control.”
      </div>
    </div>

    <div class="slide-footer">
      <span>Team Rookie (3 members) · PS-04 Autonomous Support Agent · 24-Hour Prototype Feasibility</span>
      <span>Slide 6 / 6</span>
    </div>
  </section>

</div>

<script>
  let currentSlide = 1;
  const totalSlides = 6;
  function showSlide(n) {{
    const el = document.getElementById('slide-' + n);
    if (el) {{
      el.scrollIntoView({{ behavior: 'smooth' }});
      currentSlide = n;
    }}
  }}
  window.addEventListener('keydown', (e) => {{
    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
      if (currentSlide < totalSlides) showSlide(currentSlide + 1);
    }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
      if (currentSlide > 1) showSlide(currentSlide - 1);
    }}
  }});
</script>
</body>
</html>
"""

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
    # 1. Write HTML outputs (NEVER write to src/generate_v4_html.py)
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
