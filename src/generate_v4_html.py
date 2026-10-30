import os
import base64

def get_b64(path):
    with open(path, 'rb') as f:
        return 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode('utf-8')

base_dir = os.path.dirname(os.path.abspath(__file__))
hero_b64 = get_b64(os.path.join(base_dir, "assets", "hero_video_frame.jpg"))
white_b64 = get_b64(os.path.join(base_dir, "assets", "demo_white_order.jpg"))
black_b64 = get_b64(os.path.join(base_dir, "assets", "demo_black_frame.jpg"))

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ReturnLens — Pitch Deck (AgentX Hackathon 2026, PS-04)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
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
    --dark-bg: #0D1814;
    --amber: #D88C31;
    --amber-light: #FEF3C7;
    --border-light: #D2CEC4;
    --border-dark: #233830;
    --text-muted: #55605B;
    --text-subtle: #8A9590;
  }}

  body {{
    background-color: #202422;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: var(--dark-green);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 24px 0 60px 0;
  }}

  .deck-container {{
    display: flex;
    flex-direction: column;
    gap: 32px;
  }}

  .slide {{
    width: 1280px;
    height: 720px;
    background-color: var(--cream);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    padding: 44px 56px 36px 56px;
    box-shadow: 0 12px 36px rgba(0,0,0,0.25);
  }}

  .slide.dark {{
    background-color: var(--dark-bg);
    color: #F5F3EF;
  }}

  /* Typography */
  .mono {{
    font-family: 'IBM Plex Mono', monospace;
  }}

  .tag-label {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--primary-teal);
    display: inline-block;
    margin-bottom: 8px;
  }}

  .slide.dark .tag-label {{
    color: #00A382;
  }}

  .slide-title {{
    font-size: 38px;
    font-weight: 800;
    line-height: 1.12;
    letter-spacing: -0.8px;
    color: var(--dark-green);
    margin-bottom: 8px;
  }}

  .slide.dark .slide-title {{
    color: #F5F3EF;
  }}

  .slide-sub {{
    font-size: 20px;
    font-weight: 400;
    line-height: 1.35;
    color: var(--text-muted);
  }}

  .slide.dark .slide-sub {{
    color: #A3B8B0;
  }}

  .slide-footer {{
    position: absolute;
    bottom: 24px;
    left: 56px;
    right: 56px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: var(--text-subtle);
    border-top: 1px solid var(--border-light);
    padding-top: 12px;
  }}

  .slide.dark .slide-footer {{
    border-top: 1px solid var(--border-dark);
    color: #4D665D;
  }}

  /* SLIDE 1 STYLES */
  .hero-layout {{
    display: flex;
    height: 560px;
    margin-top: 16px;
    gap: 40px;
  }}

  .hero-left {{
    width: 38%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding-bottom: 20px;
  }}

  .hero-title {{
    font-size: 48px;
    font-weight: 900;
    letter-spacing: -1.5px;
    color: var(--dark-green);
    margin-bottom: 16px;
    line-height: 1.0;
  }}

  .hero-statement {{
    font-size: 22px;
    font-weight: 700;
    line-height: 1.3;
    color: var(--primary-teal);
    margin-bottom: 14px;
  }}

  .hero-desc {{
    font-size: 18px;
    line-height: 1.45;
    color: var(--text-muted);
  }}

  .hero-meta-box {{
    background: #EBE8E1;
    border-left: 3px solid var(--primary-teal);
    padding: 14px 16px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    line-height: 1.6;
    color: var(--dark-green);
  }}

  .hero-right {{
    width: 62%;
    display: flex;
    flex-direction: column;
  }}

  .console-window {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    height: 100%;
    display: flex;
    flex-direction: column;
    box-shadow: 0 16px 36px rgba(23, 38, 33, 0.08);
  }}

  .console-header {{
    background: var(--dark-green);
    color: var(--cream);
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 16px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.5px;
  }}

  .console-body {{
    display: flex;
    flex: 1;
    overflow: hidden;
  }}

  .console-video {{
    width: 58%;
    position: relative;
    background: #111;
  }}

  .console-video img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }}

  .console-panel {{
    width: 42%;
    background: #FAF9F7;
    border-left: 1px solid var(--border-light);
    padding: 20px 22px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .info-group {{
    margin-bottom: 12px;
  }}

  .info-group .label {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: var(--text-subtle);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 3px;
  }}

  .info-group .val {{
    font-size: 14px;
    font-weight: 600;
    color: var(--dark-green);
    line-height: 1.3;
  }}

  .info-group .val-sub {{
    font-size: 12px;
    color: var(--text-muted);
  }}

  .status-badge {{
    display: inline-block;
    padding: 8px 12px;
    background: var(--teal-light);
    color: var(--primary-teal);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-align: center;
    width: 100%;
    margin-bottom: 10px;
  }}

  .btn-cta {{
    background: var(--primary-teal);
    color: #FFFFFF;
    font-size: 13px;
    font-weight: 700;
    text-align: center;
    padding: 10px;
    letter-spacing: 0.5px;
    cursor: pointer;
    border: none;
    width: 100%;
  }}

  /* SLIDE 2 STYLES */
  .problem-layout {{
    display: flex;
    flex: 1;
    align-items: center;
    justify-content: center;
    position: relative;
    margin: 20px 0;
  }}

  .source-node {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    padding: 16px 20px;
    width: 270px;
    position: absolute;
  }}

  .source-node .s-label {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: var(--primary-teal);
    margin-bottom: 4px;
  }}

  .source-node .s-val {{
    font-size: 15px;
    font-weight: 700;
    color: var(--dark-green);
  }}

  .source-node .s-sub {{
    font-size: 12px;
    color: var(--text-muted);
  }}

  .node-top-left {{ top: 20px; left: 40px; }}
  .node-bottom-left {{ bottom: 20px; left: 40px; }}
  .node-top-right {{ top: 20px; right: 40px; }}
  .node-bottom-right {{ bottom: 20px; right: 40px; }}

  .gap-box {{
    background: #FFFDF7;
    border: 2px dashed var(--amber);
    padding: 28px 36px;
    width: 440px;
    text-align: center;
    z-index: 2;
  }}

  .gap-tag {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: var(--amber);
    margin-bottom: 8px;
  }}

  .gap-title {{
    font-size: 22px;
    font-weight: 800;
    color: var(--dark-green);
    letter-spacing: -0.5px;
    margin-bottom: 8px;
  }}

  .gap-question {{
    font-size: 16px;
    font-style: italic;
    color: var(--text-muted);
  }}

  /* SLIDE 3 STYLES */
  .demo-layout {{
    display: flex;
    flex: 1;
    gap: 24px;
    margin-top: 16px;
  }}

  .demo-evidence {{
    width: 68%;
    display: flex;
    gap: 16px;
    position: relative;
  }}

  .evidence-card {{
    width: 50%;
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}

  .ev-header {{
    background: var(--cream);
    padding: 8px 12px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    color: var(--dark-green);
    border-bottom: 1px solid var(--border-light);
  }}

  .ev-img {{
    flex: 1;
    background: #111;
    position: relative;
    overflow: hidden;
  }}

  .ev-img img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }}

  .ev-footer {{
    padding: 10px 14px;
    background: #FFFFFF;
    border-top: 1px solid var(--border-light);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: var(--text-muted);
    line-height: 1.4;
  }}

  .ev-callout {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: var(--amber);
    color: #FFFFFF;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.5px;
    padding: 10px 20px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.25);
    z-index: 10;
  }}

  .demo-decision {{
    width: 32%;
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    padding: 24px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .decision-finding {{
    margin-top: 12px;
    padding: 12px;
    background: var(--amber-light);
    border-left: 3px solid var(--amber);
  }}

  .decision-finding .status-txt {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    font-weight: 800;
    color: #92400E;
    letter-spacing: 0.5px;
  }}

  .safety-box {{
    background: #F7F7F5;
    border-left: 3px solid var(--primary-teal);
    padding: 14px;
    font-size: 13px;
    line-height: 1.5;
    color: var(--dark-green);
    margin-top: 14px;
  }}

  /* SLIDE 4 STYLES (DARK) */
  .arch-pipeline {{
    display: flex;
    gap: 12px;
    margin-top: 28px;
    align-items: stretch;
  }}

  .pipe-step {{
    flex: 1;
    background: #172621;
    border: 1px solid var(--border-dark);
    padding: 16px 12px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .pipe-step.model-step {{
    border-top: 3px solid #00A382;
  }}

  .pipe-step.code-step {{
    border-top: 3px solid #F5F3EF;
  }}

  .pipe-step.human-step {{
    border-top: 3px solid var(--amber);
  }}

  .pipe-num {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: #6C8279;
    margin-bottom: 6px;
  }}

  .pipe-title {{
    font-size: 13px;
    font-weight: 700;
    color: #F5F3EF;
    line-height: 1.3;
    margin-bottom: 8px;
  }}

  .pipe-role-tag {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    padding: 3px 6px;
    display: inline-block;
    align-self: flex-start;
  }}

  .tag-model {{ background: #00382B; color: #00D1A7; }}
  .tag-code {{ background: #263831; color: #F5F3EF; }}
  .tag-human {{ background: #45260A; color: #FBBF24; }}

  .arch-branches {{
    display: flex;
    gap: 16px;
    margin-top: 24px;
  }}

  .branch-card {{
    flex: 1;
    background: #121F1B;
    border: 1px solid var(--border-dark);
    padding: 16px 18px;
  }}

  .branch-head {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 6px;
  }}

  .head-unclear {{ color: #60A5FA; }}
  .head-contradict {{ color: #F87171; }}
  .head-pass {{ color: #34D399; }}

  .branch-desc {{
    font-size: 13px;
    color: #A3B8B0;
    line-height: 1.4;
  }}

  .arch-legend {{
    display: flex;
    gap: 28px;
    margin-top: 20px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #6C8279;
  }}

  /* SLIDE 5 STYLES */
  .scenarios-grid {{
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 24px;
  }}

  .scenario-lane {{
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    padding: 16px 24px;
    display: flex;
    align-items: center;
    gap: 24px;
  }}

  .sc-badge {{
    width: 120px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    padding: 6px 12px;
    text-align: center;
  }}

  .badge-ready {{ background: var(--teal-light); color: var(--primary-teal); }}
  .badge-mismatch {{ background: var(--amber-light); color: #92400E; }}
  .badge-unclear {{ background: #EFF6FF; color: #1E40AF; }}
  .badge-context {{ background: #F3F4F6; color: #374151; }}

  .sc-evidence {{
    flex: 1;
    font-size: 15px;
    font-weight: 500;
    color: var(--dark-green);
  }}

  .sc-arrow {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 16px;
    color: var(--text-subtle);
  }}

  .sc-action {{
    width: 440px;
    font-size: 15px;
    font-weight: 700;
    color: var(--dark-green);
  }}

  /* SLIDE 6 STYLES */
  .timeline-container {{
    margin-top: 24px;
  }}

  .timeline-bar {{
    display: flex;
    border-bottom: 2px solid var(--primary-teal);
    padding-bottom: 12px;
    margin-bottom: 24px;
  }}

  .t-phase {{
    flex: 1;
    padding-right: 16px;
  }}

  .t-time {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 14px;
    font-weight: 800;
    color: var(--primary-teal);
    margin-bottom: 4px;
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
  }}

  .scope-split {{
    display: flex;
    gap: 24px;
  }}

  .scope-card {{
    flex: 1;
    background: #FFFFFF;
    border: 1px solid var(--border-light);
    padding: 22px 26px;
  }}

  .scope-in {{
    border-left: 4px solid var(--primary-teal);
  }}

  .scope-out {{
    border-left: 4px solid var(--text-subtle);
  }}

  .scope-head {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 8px;
  }}

  .scope-in .scope-head {{ color: var(--primary-teal); }}
  .scope-out .scope-head {{ color: var(--text-subtle); }}

  .scope-text {{
    font-size: 15px;
    color: var(--dark-green);
    line-height: 1.5;
  }}

  /* Print Styles */
  @media print {{
    @page {{
      size: 1280px 720px;
      margin: 0;
    }}
    body {{
      padding: 0;
      background: none;
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

  <!-- SLIDE 1: HERO / PRODUCT IN ONE GLANCE -->
  <section class="slide" id="slide-1">
    <div class="tag-label">AgentX Hackathon 2026 · Track PS-04</div>
    <div class="hero-layout">
      <div class="hero-left">
        <div>
          <h1 class="hero-title">RETURNLENS</h1>
          <div class="hero-statement">“Review returns with cited video evidence.”</div>
          <p class="hero-desc">An evidence-backed return triage agent for small online sellers.</p>
        </div>
        <div class="hero-meta-box">
          Team Rookie · 3 Members · 24h Prototype<br>
          Grounded Video Evidence · Staged Shopify/Shippo APIs
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
                  Illustrative staged evidence
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <span>ReturnLens · Idea Pitch Deck</span>
      <span>Slide 1 / 6</span>
    </div>
  </section>

  <!-- SLIDE 2: THE PROBLEM AS A VISUAL STORY -->
  <section class="slide" id="slide-2">
    <div class="tag-label">The Problem · Solo Seller Bottleneck</div>
    <h2 class="slide-title">One return decision. Four disconnected sources.</h2>
    <p class="slide-sub">Without a cited record connecting video, order truth and policy, the seller is guessing.</p>
    
    <div class="problem-layout">
      <!-- Source Nodes -->
      <div class="source-node node-top-left">
        <div class="s-label">01 Buyer Chat</div>
        <div class="s-val">“Received damaged item”</div>
        <div class="s-sub">Unverified buyer message</div>
      </div>

      <div class="source-node node-top-right">
        <div class="s-label">02 Order Record</div>
        <div class="s-val">White Headphones · ₹1,499</div>
        <div class="s-sub">Store inventory database</div>
      </div>

      <div class="source-node node-bottom-left">
        <div class="s-label">03 Delivery Status</div>
        <div class="s-val">Delivered 4 days ago</div>
        <div class="s-sub">Courier tracking API</div>
      </div>

      <div class="source-node node-bottom-right">
        <div class="s-label">04 Return Policy</div>
        <div class="s-val">7-day return window</div>
        <div class="s-sub">Store terms document</div>
      </div>

      <!-- Center Gap Box -->
      <div class="gap-box">
        <div class="gap-tag">CRITICAL INFORMATION GAP</div>
        <div class="gap-title">NO SHARED EVIDENCE RECORD</div>
        <div class="gap-question">“Approve, deny, or ask for more evidence?”</div>
      </div>
    </div>

    <div class="slide-footer">
      <span>U.S. retail fraud estimates: 9% (NRF) to 15.14% (Appriss/Deloitte); triage takes 15–20 min per return for solo sellers.</span>
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
            SKU: HEAD-WHT-02 · Matte White · ₹1,499<br>
            Delivered 4 days ago · 7-day return window
          </div>
        </div>

        <!-- Video Frame -->
        <div class="evidence-card">
          <div class="ev-header">VIDEO FRAME · INTAKE TIMESTAMP 00:07</div>
          <div class="ev-img">
            <img src="{black_b64}" alt="Black Headphone Video Evidence">
          </div>
          <div class="ev-footer">
            Observed: Midnight Black · SKU: Not verified<br>
            Tag: Not visible in cited keyframe
          </div>
        </div>

        <div class="ev-callout">COLOR MISMATCH</div>
      </div>

      <div class="demo-decision">
        <div>
          <div class="tag-label" style="color: var(--amber);">Deterministic Policy Gate</div>
          <div style="font-size: 18px; font-weight: 800; color: var(--dark-green); margin-top: 4px;">Policy P-03 Check</div>
          <p style="font-size: 13px; color: var(--text-muted); margin-top: 4px;">Specification contradiction flagged against order manifest.</p>

          <div class="decision-finding">
            <div class="status-txt">STATUS: NEEDS SELLER REVIEW</div>
            <div style="font-size: 12px; color: #78350F; margin-top: 4px;">Model proposes; human authorizes.</div>
          </div>

          <div style="margin-top: 16px;">
            <div style="font-family: 'IBM Plex Mono', monospace; font-size: 10px; font-weight: 700; color: var(--text-subtle); text-transform: uppercase;">
              Seller Action Options
            </div>
            <div style="font-size: 13px; color: var(--dark-green); margin-top: 6px; line-height: 1.5;">
              1. Request shipping-label photo<br>
              2. Send to manual physical inspection
            </div>
          </div>
        </div>

        <div class="safety-box">
          <strong>Safety Guarantees:</strong><br>
          • No automatic customer denial<br>
          • No refund or label released without seller click
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <span>Illustrative staged evidence · No real customer PII</span>
      <span>Slide 3 / 6</span>
    </div>
  </section>

  <!-- SLIDE 4: SYSTEM ARCHITECTURE (DARK) -->
  <section class="slide dark" id="slide-4">
    <div class="tag-label">System Architecture · Deterministic Pipeline</div>
    <h2 class="slide-title">Models observe. Code verifies. Seller authorizes.</h2>
    <p class="slide-sub">Deterministic policy gates and human authorization control every action.</p>

    <!-- 6-Step Horizontal Pipeline -->
    <div class="arch-pipeline">
      <div class="pipe-step">
        <div>
          <div class="pipe-num">01</div>
          <div class="pipe-title">Buyer Request</div>
        </div>
        <span class="pipe-role-tag tag-code">INTAKE</span>
      </div>

      <div class="pipe-step">
        <div>
          <div class="pipe-num">02</div>
          <div class="pipe-title">Frame Extraction</div>
        </div>
        <span class="pipe-role-tag tag-code">FFMPEG</span>
      </div>

      <div class="pipe-step model-step">
        <div>
          <div class="pipe-num">03</div>
          <div class="pipe-title">Model Observation</div>
        </div>
        <span class="pipe-role-tag tag-model">GEMINI FLASH</span>
      </div>

      <div class="pipe-step code-step">
        <div>
          <div class="pipe-num">04</div>
          <div class="pipe-title">Policy Engine</div>
        </div>
        <span class="pipe-role-tag tag-code">PYTHON RULES</span>
      </div>

      <div class="pipe-step model-step">
        <div>
          <div class="pipe-num">05</div>
          <div class="pipe-title">Evidence Critic</div>
        </div>
        <span class="pipe-role-tag tag-model">VERIFICATION</span>
      </div>

      <div class="pipe-step human-step">
        <div>
          <div class="pipe-num">06</div>
          <div class="pipe-title">Seller Gate</div>
        </div>
        <span class="pipe-role-tag tag-human">AUTHORIZATION</span>
      </div>
    </div>

    <!-- 3 Branching Outcomes -->
    <div class="arch-branches">
      <div class="branch-card">
        <div class="branch-head head-unclear">UNCLEAR EVIDENCE</div>
        <div class="branch-desc">Ask for specific photo → Resume same case (1 retry limit). Prevents premature rejection.</div>
      </div>

      <div class="branch-card">
        <div class="branch-head head-contradict">CONTRADICTION DETECTED</div>
        <div class="branch-desc">Seller review required. System inhibits automated label generation and flags discrepancy.</div>
      </div>

      <div class="branch-card">
        <div class="branch-head head-pass">ALL CHECKS PASS</div>
        <div class="branch-desc">Seller 1-click approval → releases mock return label and drafts refund.</div>
      </div>
    </div>

    <!-- Legend -->
    <div class="arch-legend">
      <span><strong style="color: #00D1A7;">■ Model:</strong> Proposes observations &amp; timestamps</span>
      <span><strong style="color: #F5F3EF;">■ Code:</strong> Enforces rules P-01 to P-08 &amp; caps</span>
      <span><strong style="color: #FBBF24;">■ Human:</strong> Sole authority to release financial actions</span>
    </div>

    <div class="slide-footer">
      <span>Structured audit log recorded at every state transition · Exactly 3 base LLM calls per case</span>
      <span>Slide 4 / 6</span>
    </div>
  </section>

  <!-- SLIDE 5: FOUR DEMO OUTCOMES -->
  <section class="slide" id="slide-5">
    <div class="tag-label">Demo Scenarios · Bounded Edge Cases</div>
    <h2 class="slide-title">Four scenarios. Four predictable behaviors.</h2>
    <p class="slide-sub">Deliberate, bounded actions across common edge cases.</p>

    <div class="scenarios-grid">
      <div class="scenario-lane">
        <div class="sc-badge badge-ready">READY</div>
        <div class="sc-evidence">Visible casing damage at 00:14 · Serial tag matches order record</div>
        <div class="sc-arrow">→</div>
        <div class="sc-action">Prepare seller approval (Mock label &amp; refund drafted)</div>
      </div>

      <div class="scenario-lane">
        <div class="sc-badge badge-mismatch">MISMATCH</div>
        <div class="sc-evidence">Black headphones received vs White ordered at 00:07</div>
        <div class="sc-arrow">→</div>
        <div class="sc-action">Seller review (Warehouse error check vs physical inspection)</div>
      </div>

      <div class="scenario-lane">
        <div class="sc-badge badge-unclear">UNCLEAR</div>
        <div class="sc-evidence">Blurry shipping barcode at 00:02 · Serial tag unreadable</div>
        <div class="sc-arrow">→</div>
        <div class="sc-action">Ask for specific photo (Auto-prompts buyer for focused still)</div>
      </div>

      <div class="scenario-lane">
        <div class="sc-badge badge-context">CONTEXT</div>
        <div class="sc-evidence">Crushed carton with courier tape intact at 00:11</div>
        <div class="sc-arrow">→</div>
        <div class="sc-action">Check continuity (Approve with transit damage claim note)</div>
      </div>
    </div>

    <div class="slide-footer">
      <span>Expected behavior on staged prototype scenarios — not production metrics.</span>
      <span>Slide 5 / 6</span>
    </div>
  </section>

  <!-- SLIDE 6: 24-HOUR EXECUTION -->
  <section class="slide" id="slide-6">
    <div class="tag-label">Execution Plan · Team Rookie (3 Members)</div>
    <h2 class="slide-title">Built for a 24-hour sprint.</h2>
    <p class="slide-sub">Strict scope discipline and single-threaded execution across 3 owners.</p>

    <div class="timeline-container">
      <div class="timeline-bar">
        <div class="t-phase">
          <div class="t-time">0h – 6h</div>
          <div class="t-title">Mock APIs &amp; Agent Skeleton</div>
          <div class="t-owner">Owner A (Backend)</div>
        </div>

        <div class="t-phase">
          <div class="t-time">6h – 12h</div>
          <div class="t-title">Evidence Pipeline &amp; Policy</div>
          <div class="t-owner">Owner B (Multimodal &amp; UI)</div>
        </div>

        <div class="t-phase">
          <div class="t-time">12h – 18h</div>
          <div class="t-title">Integration &amp; 4 Scenarios</div>
          <div class="t-owner">Owner C (QA &amp; Data)</div>
        </div>

        <div class="t-phase">
          <div class="t-time">18h – 24h</div>
          <div class="t-title">End-to-End Polish &amp; Video</div>
          <div class="t-owner">All 3 Members</div>
        </div>
      </div>

      <div class="scope-split">
        <div class="scope-card scope-in">
          <div class="scope-head">IN SCOPE · 24-HOUR PROTOTYPE</div>
          <div class="scope-text">
            Mock store &amp; shipping APIs · Staged video evidence · One seller review console · Deterministic policy rules · Structured audit log
          </div>
        </div>

        <div class="scope-card scope-out">
          <div class="scope-head">OUT OF SCOPE · DEFERRED CAPABILITIES</div>
          <div class="scope-text">
            Real payment gateways · Multi-seller platform · WhatsApp production webhooks · Voice/audio analysis
          </div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <span>Team Rookie (3 members) · Prototype scope strictly bounded to single-seller staged workflow.</span>
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

out_path = os.path.join(os.path.dirname(base_dir), "deliverables", "ReturnLens_v4.html")
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Generated ReturnLens_v4.html successfully!")

