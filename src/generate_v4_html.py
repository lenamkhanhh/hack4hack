import os
import base64
import subprocess
import fitz
from PIL import Image

base_dir = r"D:\Code\Code\AIO\Code\hack4hack"
assets_dir = os.path.join(base_dir, "src", "assets")

def get_b64(fname):
    p = os.path.join(assets_dir, fname)
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
    padding: 56px 64px 44px 64px;
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
    margin-bottom: 12px;
  }}

  .slide.dark .tag-label {{
    color: #00D1A7;
  }}

  .slide-title {{
    font-size: 36px;
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
    font-size: 17px;
    font-weight: 400;
    line-height: 1.35;
    color: var(--text-muted);
    margin-bottom: 24px;
  }}

  .slide.dark .slide-sub {{
    color: #A3B8B0;
  }}

  .slide-footer {{
    position: absolute;
    bottom: 20px;
    left: 64px;
    right: 64px;
    display: flex;
    justify-content: space-between;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: var(--text-subtle);
    border-top: 1px solid var(--border-light);
    padding-top: 12px;
  }}

  .slide.dark .slide-footer {{
    border-top: 1px solid var(--border-dark);
    color: #5C786E;
  }}

  /* SLIDE 1 STYLES */
  .hero-layout {{
    display: grid;
    grid-template-columns: 1fr 1.35fr;
    gap: 48px;
    height: 100%;
    align-items: stretch;
  }}

  .hero-left {{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding-bottom: 28px;
  }}

  .hero-title {{
    font-size: 64px;
    font-weight: 900;
    letter-spacing: -2px;
    color: var(--dark-green);
    line-height: 1;
    margin-bottom: 12px;
  }}

  .hero-statement {{
    font-size: 20px;
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
    padding: 16px 20px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: var(--dark-green);
    line-height: 1.6;
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
    margin-bottom: 14px;
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
    font-size: 14px;
    font-weight: 700;
    color: var(--dark-green);
  }}

  .info-group .val-sub {{
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 2px;
  }}

  .status-badge {{
    background: var(--teal-light);
    color: var(--primary-teal);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 800;
    padding: 8px 12px;
    text-align: center;
    margin-bottom: 10px;
    letter-spacing: 0.5px;
  }}

  .btn-cta {{
    width: 100%;
    background: var(--primary-teal);
    color: #FFFFFF;
    border: none;
    padding: 12px;
    font-size: 13px;
    font-weight: 700;
    cursor: default;
    text-align: center;
  }}

  /* SLIDE 2 STYLES */
  .problem-layout {{
    position: relative;
    height: 440px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 20px;
    padding: 10px 0;
  }}

  .source-node {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    padding: 24px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}

  .s-label {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    color: var(--primary-teal);
    text-transform: uppercase;
    margin-bottom: 6px;
  }}

  .s-val {{
    font-size: 18px;
    font-weight: 700;
    color: var(--dark-green);
    margin-bottom: 4px;
  }}

  .s-sub {{
    font-size: 12px;
    color: var(--text-muted);
  }}

  .gap-box {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: var(--dark-green);
    color: #F5F3EF;
    border: 2px solid var(--coral);
    padding: 24px 32px;
    text-align: center;
    width: 480px;
    box-shadow: 0 12px 32px rgba(0,0,0,0.18);
    z-index: 10;
  }}

  .gap-tag {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: var(--coral);
    margin-bottom: 6px;
  }}

  .gap-title {{
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.3px;
    margin-bottom: 8px;
    line-height: 1.25;
  }}

  .gap-question {{
    font-size: 12px;
    color: #D1D5DB;
    line-height: 1.45;
  }}

  /* SLIDE 3 STYLES */
  .demo-layout {{
    display: grid;
    grid-template-columns: 2fr 1.05fr;
    gap: 36px;
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
    padding: 24px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .decision-finding {{
    background: var(--coral-light);
    border: 1px solid #F87171;
    padding: 12px 16px;
    margin-top: 14px;
  }}

  .decision-finding .status-txt {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    font-weight: 800;
    color: #991B1B;
  }}

  .safety-box {{
    background: #FAF8F5;
    border: 1px solid var(--border-light);
    padding: 12px 14px;
    font-size: 11px;
    color: var(--text-muted);
    line-height: 1.5;
  }}

  /* SLIDE 4 STYLES (DARK) */
  .arch-pipeline {{
    display: flex;
    gap: 10px;
    margin-top: 16px;
    align-items: stretch;
  }}

  .pipe-step {{
    flex: 1;
    background: #172621;
    border: 1px solid var(--border-dark);
    padding: 14px 10px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .pipe-step.model-step {{ border-top: 3px solid #00D1A7; }}
  .pipe-step.code-step {{ border-top: 3px solid #F5F3EF; }}
  .pipe-step.human-step {{ border-top: 3px solid #FBBF24; }}

  .pipe-num {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: #6C8279;
    margin-bottom: 4px;
  }}

  .pipe-title {{
    font-size: 13px;
    font-weight: 700;
    color: #F5F3EF;
    line-height: 1.25;
    margin-bottom: 6px;
  }}

  .pipe-role-tag {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    font-weight: 700;
    padding: 3px 6px;
    display: inline-block;
    text-align: center;
    letter-spacing: 0.5px;
  }}

  .tag-code {{ background: #223830; color: #F5F3EF; }}
  .tag-model {{ background: rgba(0,209,167,0.18); color: #00D1A7; }}
  .tag-human {{ background: rgba(251,191,36,0.18); color: #FBBF24; }}

  .arch-branches {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-top: 18px;
  }}

  .branch-card {{
    background: #121F1B;
    border: 1px solid var(--border-dark);
    padding: 14px 14px;
  }}

  .branch-head {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-bottom: 6px;
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
    gap: 20px;
    margin-top: 18px;
    padding: 12px 16px;
    background: #121F1B;
    border: 1px solid var(--border-dark);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: #A3B8B0;
    line-height: 1.5;
  }}

  /* SLIDE 5 STYLES */
  .scenarios-grid {{
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 14px;
  }}

  .scenario-lane {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    padding: 14px 20px;
    display: flex;
    align-items: center;
    gap: 20px;
  }}

  .sc-badge {{
    width: 140px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
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
    font-size: 13px;
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

  /* SLIDE 6 STYLES */
  .timeline-container {{
    margin-top: 14px;
  }}

  .timeline-bar {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    border-bottom: 2px solid var(--primary-teal);
    padding-bottom: 14px;
    margin-bottom: 18px;
    gap: 20px;
  }}

  .t-phase {{
    padding-right: 12px;
  }}

  .t-time {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    font-weight: 800;
    color: var(--primary-teal);
    margin-bottom: 4px;
    text-transform: uppercase;
  }}

  .t-title {{
    font-size: 14px;
    font-weight: 700;
    color: var(--dark-green);
    margin-bottom: 4px;
  }}

  .t-owner {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: var(--text-muted);
    line-height: 1.4;
  }}

  .scope-split {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }}

  .scope-card {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    padding: 16px 20px;
  }}

  .scope-in {{ border-left: 4px solid var(--primary-teal); }}
  .scope-out {{ border-left: 4px solid var(--coral); }}

  .scope-head {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.5px;
    margin-bottom: 6px;
  }}

  .scope-in .scope-head {{ color: var(--primary-teal); }}
  .scope-out .scope-head {{ color: var(--coral); }}

  .scope-text {{
    font-size: 12px;
    color: var(--text-muted);
    line-height: 1.5;
  }}

  .closing-quote {{
    margin-top: 16px;
    background: #FAF8F5;
    border: 1px solid var(--border-light);
    padding: 12px 18px;
    font-size: 12px;
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
          <strong>Team Rookie · 3 members · PS-04 submission</strong><br>
          User: Solo D2C merchant managing orders and returns alone.<br>
          Scope in 24h: Return triage only, mock store data + 1 order-status route.<br>
          Not another chatbot; not an autonomous refund gate.
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
                  <div class="label">Evidence Citation</div>
                  <div class="val">Inspection Frame 00:14</div>
                  <div class="val-sub">Casing crack verified at lower seam</div>
                </div>
                <div class="info-group">
                  <div class="label">Policy Verification</div>
                  <div class="val">P-01 Physical Defect: PASS</div>
                  <div class="val-sub">P-04 Return Window: PASS (4 of 7 days)</div>
                </div>
              </div>
              <div>
                <div class="status-badge">READY FOR SELLER REVIEW</div>
                <button class="btn-cta">Approve Return &amp; Draft Refund</button>
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

  <!-- SLIDE 2: THE PROBLEM AS A VISUAL STORY -->
  <section class="slide" id="slide-2">
    <div class="tag-label">The Problem · Solo Seller Bottleneck</div>
    <h2 class="slide-title">One return decision. Four disconnected sources.</h2>
    <p class="slide-sub">The return decision is made from memory, before the evidence is checked.</p>
    
    <div class="problem-layout">
      <!-- Source Nodes -->
      <div class="source-node">
        <div class="s-label">01 Buyer Chat</div>
        <div class="s-val">“Received damaged item”</div>
        <div class="s-sub">Buyer upload: 30–60s unboxing video + reason</div>
      </div>

      <div class="source-node">
        <div class="s-label">02 Order Record</div>
        <div class="s-val">White Headphones · ₹1,499</div>
        <div class="s-sub">Shopify mock store API inventory database</div>
      </div>

      <div class="source-node">
        <div class="s-label">03 Courier Tracking</div>
        <div class="s-val">Delivered 4 days ago</div>
        <div class="s-sub">Shippo mock tracking API timestamp verification</div>
      </div>

      <div class="source-node">
        <div class="s-label">04 Return Policy</div>
        <div class="s-val">7-Day Window · Sealed Tag</div>
        <div class="s-sub">Deterministic code rules P-01 to P-08, never prompts</div>
      </div>

      <!-- Center Gap Box -->
      <div class="gap-box">
        <div class="gap-tag">CRITICAL INFORMATION GAP</div>
        <div class="gap-title">NO SINGLE RECORD TIES ORDER, VIDEO &amp; POLICY TOGETHER</div>
        <div class="gap-question">
          Today the seller opens many tabs, then decides alone. A wrong refund loses money and stock; an unfair denial loses a repeat customer. The gap is not a missing returns portal, it is that no single record ties order, video frame, policy clause, and decision together.
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <span>Fraud estimates differ by definition: 9% (NRF 2025, fraud only) vs 15.14% (Appriss/Deloitte 2024, fraud + abuse).</span>
      <span>Slide 2 / 6</span>
    </div>
  </section>

  <!-- SLIDE 3: THE STAR DEMO SLIDE -->
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
            <strong>Observed: HEAD-BLK-09</strong> · Midnight Black<br>
            Mock evidence pack · Frame 00:07
          </div>
        </div>

        <div class="ev-callout">COLOR MISMATCH</div>
      </div>

      <div class="demo-decision">
        <div>
          <div class="tag-label" style="color: var(--coral);">Deterministic Policy Gate</div>
          <div style="font-size: 18px; font-weight: 800; color: var(--dark-green); margin-top: 4px;">Policy P-03 Check: FAIL</div>
          <p style="font-size: 12px; color: var(--text-muted); margin-top: 4px;">
            Specification contradiction flagged against Shopify order manifest.
          </p>

          <div style="font-family: 'IBM Plex Mono', monospace; font-size: 11px; background: #FAF8F5; border: 1px solid var(--border-light); padding: 8px 10px; margin-top: 10px; color: var(--dark-green);">
            typed JSON, requires_seller_approval: true
          </div>

          <div class="decision-finding">
            <div class="status-txt">STATUS: ESCALATE (NEEDS SELLER REVIEW)</div>
            <div style="font-size: 11px; color: #991B1B; margin-top: 4px;">Model proposes; human authorizes. No label or refund auto-issued.</div>
          </div>

          <div style="margin-top: 12px;">
            <div style="font-family: 'IBM Plex Mono', monospace; font-size: 10px; font-weight: 700; color: var(--text-subtle); text-transform: uppercase;">
              Seller Action Options
            </div>
            <div style="font-size: 12px; color: var(--dark-green); margin-top: 4px; line-height: 1.45;">
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

    <!-- 6-Step Horizontal Pipeline -->
    <div class="arch-pipeline">
      <div class="pipe-step model-step">
        <div>
          <div class="pipe-num">01 PLAN</div>
          <div class="pipe-title">Planner</div>
        </div>
        <span class="pipe-role-tag tag-model">MODEL</span>
      </div>

      <div class="pipe-step code-step">
        <div>
          <div class="pipe-num">02 RETRIEVE</div>
          <div class="pipe-title">Tools &amp; Video</div>
        </div>
        <span class="pipe-role-tag tag-code">CODE</span>
      </div>

      <div class="pipe-step code-step">
        <div>
          <div class="pipe-num">03 EVALUATE</div>
          <div class="pipe-title">Policy Engine</div>
        </div>
        <span class="pipe-role-tag tag-code">CODE</span>
      </div>

      <div class="pipe-step model-step">
        <div>
          <div class="pipe-num">04 AUDIT</div>
          <div class="pipe-title">Critic</div>
        </div>
        <span class="pipe-role-tag tag-model">MODEL</span>
      </div>

      <div class="pipe-step human-step">
        <div>
          <div class="pipe-num">05 AUTHORIZE</div>
          <div class="pipe-title">Seller Gate</div>
        </div>
        <span class="pipe-role-tag tag-human">HUMAN</span>
      </div>

      <div class="pipe-step code-step">
        <div>
          <div class="pipe-num">06 RECORD</div>
          <div class="pipe-title">Audit Log</div>
        </div>
        <span class="pipe-role-tag tag-code">CODE</span>
      </div>
    </div>

    <!-- 4 Decision Function Outcomes (Strict Priority Order) -->
    <div class="arch-branches">
      <div class="branch-card">
        <div class="branch-head head-contradict">1. CONTRADICTION → ESCALATE</div>
        <div class="branch-desc">Discrepancy flagged (e.g. Case B). Inhibits automated label and refund draft. Seller reviews 3 options.</div>
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
      <span><strong style="color: #F5F3EF;">■ Policy Clauses:</strong> Deterministic code rules P-01 to P-08, never prompts</span>
      <span><strong style="color: #60A5FA;">■ Critic:</strong> The critic reviews cited frames and flags unsupported observations</span>
      <span><strong style="color: #FBBF24;">■ Safety Limit:</strong> Injection cannot alter policy code or bypass human gate</span>
    </div>

    <div class="slide-footer">
      <span>Structured audit log recorded at every state transition · Decision priority: Contradiction &gt; Hard fail &gt; Unclear only &gt; All pass</span>
      <span>Slide 4 / 6</span>
    </div>
  </section>

  <!-- SLIDE 5: FOUR DEMO SCENARIOS -->
  <section class="slide" id="slide-5">
    <div class="tag-label">Demo Scenarios · Grounded Verification</div>
    <h2 class="slide-title">Four scenarios. Four predictable behaviors.</h2>
    <p class="slide-sub">Every decision can be clicked back to a frame, a clause, and a log entry.</p>

    <div class="scenarios-grid">
      <!-- Case A -->
      <div class="scenario-lane">
        <div class="sc-badge badge-ready">CASE A · READY</div>
        <div class="sc-evidence">
          <strong>ORD-1042</strong> (₹1,499) · SKU matches manifest, tag present, visible defect within 7-day window.
        </div>
        <div class="sc-arrow">→</div>
        <div class="sc-action">
          Seller approval releases mock return label and refund draft in <strong>pending_return_receipt</strong>, not executed refund.
        </div>
      </div>

      <!-- Case B -->
      <div class="scenario-lane">
        <div class="sc-badge badge-mismatch">CASE B · ESCALATE</div>
        <div class="sc-evidence">
          <strong>HEAD-WHT-02</strong> vs <strong>HEAD-BLK-09</strong> at Frame 00:07 · Policy P-03 SKU mismatch <strong>FAIL</strong>.
        </div>
        <div class="sc-arrow">→</div>
        <div class="sc-action">
          <strong>ESCALATE</strong> (no label, no refund, no denial). Seller options: mis-shipment / box label / physical inspection.
        </div>
      </div>

      <!-- Case C -->
      <div class="scenario-lane">
        <div class="sc-badge badge-unclear">CASE C · ASK MORE</div>
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
        <div class="sc-badge badge-continuity">CASE D · CONTINUITY</div>
        <div class="sc-evidence">
          <strong>Unbroken take</strong>: opening sealed parcel to showing the label in one continuous sequence.
        </div>
        <div class="sc-arrow">→</div>
        <div class="sc-action">
          Continuity verified: prevents photo-swap fraud before mock return label generation. Proves why video beats photos.
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <span>Staged sample videos, mock store data, no real customer PII · Cap: min(₹4,999, remaining refundable amount, order paid amount)</span>
      <span>Slide 5 / 6</span>
    </div>
  </section>

  <!-- SLIDE 6: 24-HOUR EXECUTION -->
  <section class="slide" id="slide-6">
    <div class="tag-label">Execution Plan · Team Rookie (3 Members)</div>
    <h2 class="slide-title">Built for a 24-hour sprint.</h2>
    <p class="slide-sub">Buildable in 24 hours by 3 people, if the scope stays narrow.</p>

    <div class="timeline-container">
      <div class="timeline-bar">
        <div class="t-phase">
          <div class="t-time">Person A</div>
          <div class="t-title">Backend &amp; Agent Core</div>
          <div class="t-owner">Backend, agent graph, policy, critic, audit log.</div>
        </div>

        <div class="t-phase">
          <div class="t-time">Person B</div>
          <div class="t-title">Video Pipeline &amp; UI</div>
          <div class="t-owner">Video pipeline, video indexer, seller console, evidence pack view.</div>
        </div>

        <div class="t-phase">
          <div class="t-time">Person C</div>
          <div class="t-title">Integration &amp; Verification</div>
          <div class="t-owner">Integration, mock data, 4 demo cases, fallback testing, demo video, README.</div>
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

# 1. Write HTML files
deliverable_html = os.path.join(base_dir, "deliverables", "ReturnLens_v4.html")
root_html = os.path.join(base_dir, "ReturnLens_v4.html")
index_html = os.path.join(base_dir, "index.html")

for path in [deliverable_html, root_html, index_html]:
    with open(path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Wrote HTML: {path}")

# Also update src/generate_v4_html.py
src_gen = os.path.join(base_dir, "src", "generate_v4_html.py")
with open(src_gen, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Updated: {src_gen}")

# 2. Render PDF using Edge Headless
deliverable_pdf = os.path.join(base_dir, "deliverables", "ReturnLens_v4.pdf")
root_pdf = os.path.join(base_dir, "ReturnLens_v4.pdf")

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_path):
    edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

file_uri = f"file:///{deliverable_html.replace(os.sep, '/')}"

cmd = [
    edge_path,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    "--print-to-pdf-no-header",
    f"--print-to-pdf={deliverable_pdf}",
    file_uri
]

print("Rendering PDF via headless Edge...")
res = subprocess.run(cmd, capture_output=True, text=True)
print(f"Edge PDF exit: {res.returncode}")

with open(deliverable_pdf, "rb") as f_in, open(root_pdf, "wb") as f_out:
    f_out.write(f_in.read())
print(f"Synced PDF: {root_pdf}")

# 3. Render slide PNGs and preview contact sheet
doc = fitz.open(deliverable_pdf)
print(f"Rendered PDF page count: {len(doc)}")

slides_png_dir = os.path.join(assets_dir, "slides")
os.makedirs(slides_png_dir, exist_ok=True)

slide_imgs = []
for i in range(len(doc)):
    page = doc[i]
    pix = page.get_pixmap(dpi=150)
    png_path = os.path.join(slides_png_dir, f"slide_{i+1}.png")
    pix.save(png_path)
    slide_imgs.append(Image.open(png_path))

# Build 3x2 grid preview image (matching the exact repo preview in Screenshot 2!)
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

deliverable_preview = os.path.join(base_dir, "deliverables", "ReturnLens_v4_preview.png")
root_preview = os.path.join(base_dir, "ReturnLens_v4_preview.png")

preview_img.save(deliverable_preview, format="PNG", optimize=True)
preview_img.save(root_preview, format="PNG", optimize=True)
print(f"Saved preview: {deliverable_preview} and {root_preview}")
