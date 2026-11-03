import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
import fitz
from PIL import Image
import base64

def generate_v7_2():
    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / "content" / "deck_data_v7_2.json"
    deliverables_dir = base_dir / "deliverables"
    deliverables_dir.mkdir(parents=True, exist_ok=True)

    if not data_path.exists():
        raise FileNotFoundError(f"Canonical data file missing: {data_path}")

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assets_dir = base_dir / "src" / "assets"
    def b64(p):
        if p.exists():
            with open(p, "rb") as f:
                return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode('utf-8')}"
        return ""

    img_white_b64 = b64(assets_dir / "studio_white_headphones.jpg")
    img_black_b64 = b64(assets_dir / "unboxing_black_headphones.jpg")

    meta = data["meta"]
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
<title>ReturnLens v7.2 — Precision &amp; Honest Grounding Edition (AgentX Hackathon 2026, Track PS-04)</title>
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
    --paper: #FAF8F5;
    --paper-tint: #F3EFE9;
    --paper-card: #FFFFFF;
    --ink: #11201A;
    --ink-light: #283C33;
    --muted: #566B60;
    --subtle: #8A9C93;
    --border: #E2DCD2;
    --border-strong: #CAC2B3;
    
    --teal: #0A5C48;
    --teal-dark: #064032;
    --teal-light: #E8F5F1;
    --teal-border: #99D4C5;
    --teal-accent: #2DD4BF;

    --coral: #C84B31;
    --coral-dark: #9E2A2B;
    --coral-light: #FDF3F1;
    --coral-border: #F7C5BC;

    --amber: #D97706;
    --amber-dark: #92400E;
    --amber-light: #FEF3C7;
    --gold: #FFD485;

    --dark-bg: #0B1613;
    --dark-card: #13231E;
    --dark-border: #223B33;
    --dark-ink: #F8F7F4;
    --dark-muted: #95AFA5;
  }}

  html, body {{
    background-color: #1E2D27;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", "Calibri", Roboto, Helvetica, Arial, sans-serif;
    color: var(--ink);
    -webkit-font-smoothing: antialiased;
    overflow-x: hidden;
  }}

  #deck-container {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 32px;
    padding: 32px 0 80px 0;
  }}

  .slide {{
    width: 1280px;
    height: 720px;
    background: var(--paper);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 36px 44px;
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.35);
    border-radius: 4px;
    page-break-after: always;
  }}

  .slide.dark {{
    background: var(--dark-bg);
    color: var(--dark-ink);
  }}

  .tag-label {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 11px;
    font-weight: 700;
    color: var(--teal);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 4px;
  }}

  .slide.dark .tag-label {{
    color: var(--teal-accent);
  }}

  .headline-wrap {{
    margin-bottom: 16px;
  }}

  .slide-title {{
    font-size: 29px;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--ink);
    line-height: 1.15;
    margin-bottom: 4px;
  }}

  .slide.dark .slide-title {{
    color: var(--dark-ink);
  }}

  .slide-subtitle {{
    font-size: 15px;
    font-weight: 500;
    color: var(--muted);
    line-height: 1.4;
  }}

  .slide.dark .slide-subtitle {{
    color: var(--dark-muted);
  }}

  .slide-footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid var(--border);
    padding-top: 10px;
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9.5px;
    color: var(--muted);
    letter-spacing: 0.04em;
  }}

  .slide.dark .slide-footer {{
    border-color: var(--dark-border);
    color: var(--dark-muted);
  }}

  /* SLIDE 1 */
  .hero-grid {{
    display: grid;
    grid-template-columns: 460px 1fr;
    gap: 32px;
    align-items: stretch;
    height: 100%;
  }}

  .hero-text {{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .hero-wordmark {{
    font-size: 38px;
    font-weight: 900;
    letter-spacing: -0.03em;
    color: var(--ink);
    line-height: 1;
    margin-bottom: 6px;
  }}

  .hero-tagline {{
    font-size: 18px;
    font-weight: 700;
    color: var(--teal);
    line-height: 1.3;
    margin-bottom: 12px;
  }}

  .hero-desc {{
    font-size: 13.5px;
    color: var(--ink-light);
    line-height: 1.55;
    margin-bottom: 16px;
  }}

  .hero-principle-card {{
    background: var(--teal-light);
    border: 1.5px solid var(--teal);
    border-radius: 8px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}

  .hero-principle-tag {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9.5px;
    font-weight: 700;
    color: var(--teal-dark);
    letter-spacing: 0.06em;
  }}

  .hero-principle-thesis {{
    font-size: 17px;
    font-weight: 800;
    color: var(--teal-dark);
    line-height: 1.25;
  }}

  .hero-principle-meta {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9.5px;
    color: var(--coral-dark);
    font-weight: 700;
    line-height: 1.45;
  }}

  .console-window {{
    background: var(--paper-card);
    border: 1.5px solid var(--border-strong);
    border-radius: 8px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}

  .console-titlebar {{
    background: var(--paper-tint);
    border-bottom: 1px solid var(--border);
    padding: 8px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}

  .mac-traffic-lights {{
    display: flex;
    gap: 6px;
  }}

  .mac-dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
  }}

  .mac-dot.red {{ background: #FF5F56; }}
  .mac-dot.yellow {{ background: #FFBD2E; }}
  .mac-dot.green {{ background: #27C93F; }}

  .console-title-text {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 10px;
    font-weight: 700;
    color: var(--ink-light);
  }}

  .console-subbar {{
    background: #FFFFFF;
    border-bottom: 1px solid var(--border);
    padding: 7px 14px;
    display: flex;
    justify-content: space-between;
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9.5px;
    color: var(--muted);
  }}

  .console-subbar strong {{
    color: var(--ink);
  }}

  .console-body {{
    padding: 14px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    flex: 1;
    justify-content: space-between;
  }}

  .console-comparison {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }}

  .comp-card {{
    background: var(--paper);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}

  .comp-card.coral {{
    background: var(--coral-light);
    border-color: var(--coral-border);
  }}

  .comp-img {{
    width: 100%;
    height: 110px;
    object-fit: cover;
    border-radius: 4px;
    margin-bottom: 6px;
  }}

  .comp-label {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 8.5px;
    font-weight: 700;
    color: var(--teal-dark);
  }}

  .comp-card.coral .comp-label {{
    color: var(--coral-dark);
  }}

  .comp-title {{
    font-size: 12px;
    font-weight: 800;
    color: var(--ink);
  }}

  .comp-card.coral .comp-title {{
    color: var(--coral-dark);
  }}

  .comp-meta {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 8.5px;
    color: var(--muted);
    line-height: 1.4;
  }}

  .console-contradiction {{
    background: var(--ink);
    border-radius: 6px;
    padding: 8px 12px;
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 8.5px;
    font-weight: 700;
    color: var(--gold);
    line-height: 1.4;
  }}

  .console-actions {{
    background: var(--paper-tint);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 8px 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  .seller-gate-status {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9.5px;
    font-weight: 700;
    color: var(--coral);
  }}

  .btn-group {{
    display: flex;
    gap: 8px;
  }}

  .btn {{
    padding: 7px 14px;
    border-radius: 4px;
    font-family: 'Inter', -apple-system, sans-serif;
    font-size: 11px;
    font-weight: 700;
    cursor: pointer;
    text-align: center;
  }}

  .btn-sec {{
    background: #FFFFFF;
    border: 1px solid var(--border-strong);
    color: var(--ink);
  }}

  .btn-pri {{
    background: var(--teal);
    color: #FFFFFF;
    border: 1px solid var(--teal-dark);
  }}

  /* SLIDE 2 */
  .problem-layout {{
    display: flex;
    flex-direction: column;
    gap: 16px;
    height: 100%;
    justify-content: space-between;
  }}

  .convergence-wrap {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    align-items: stretch;
  }}

  .sources-list {{
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}

  .source-card {{
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 10px 14px;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }}

  .source-head {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  .source-tag {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9.5px;
    font-weight: 700;
    color: var(--teal);
  }}

  .source-name {{
    font-size: 13px;
    font-weight: 800;
    color: var(--ink);
  }}

  .source-detail {{
    font-size: 11.5px;
    color: var(--muted);
  }}

  .gap-focal-card {{
    background: var(--ink);
    border: 1.5px solid var(--border-strong);
    border-radius: 8px;
    padding: 24px;
    color: #FFFFFF;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .gap-tag {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 10px;
    font-weight: 700;
    color: var(--teal-accent);
    letter-spacing: 0.06em;
  }}

  .gap-lead {{
    font-size: 18px;
    font-weight: 800;
    line-height: 1.35;
    color: #FFFFFF;
  }}

  .gap-body {{
    font-size: 12.5px;
    color: #DFEAE5;
    line-height: 1.5;
  }}

  .bottom-callouts-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }}

  .editorial-callout {{
    background: var(--paper-tint);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 10px 14px;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}

  .callout-title {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9px;
    font-weight: 700;
    color: var(--teal-dark);
  }}

  .callout-desc {{
    font-size: 10.5px;
    line-height: 1.45;
    color: var(--ink);
  }}

  /* SLIDE 3 */
  .star-demo-layout {{
    display: flex;
    flex-direction: column;
    gap: 16px;
    height: 100%;
    justify-content: space-between;
  }}

  .exhibition-wrap {{
    display: grid;
    grid-template-columns: 1fr 60px 1fr;
    align-items: center;
    gap: 16px;
  }}

  .exhibit-board {{
    background: #FFFFFF;
    border: 1.5px solid var(--border);
    border-radius: 8px;
    padding: 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}

  .exhibit-board.coral {{
    background: var(--coral-light);
    border-color: var(--coral-border);
  }}

  .exhibit-head {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9.5px;
    font-weight: 700;
    color: var(--teal-dark);
  }}

  .exhibit-board.coral .exhibit-head {{
    color: var(--coral-dark);
  }}

  .exhibit-img {{
    width: 100%;
    height: 180px;
    object-fit: cover;
    border-radius: 6px;
  }}

  .exhibit-spec {{
    display: flex;
    flex-direction: column;
    gap: 2px;
  }}

  .exhibit-spec-title {{
    font-size: 14.5px;
    font-weight: 800;
    color: var(--ink);
  }}

  .exhibit-board.coral .exhibit-spec-title {{
    color: var(--coral-dark);
  }}

  .exhibit-spec-meta {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9.5px;
    color: var(--muted);
    line-height: 1.4;
  }}

  .mismatch-pill {{
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: var(--coral);
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    font-weight: 900;
    margin: 0 auto;
    box-shadow: 0 4px 12px rgba(200, 75, 49, 0.3);
  }}

  .star-decision-strip {{
    background: #FFFFFF;
    border: 1.5px solid var(--border-strong);
    border-radius: 8px;
    padding: 12px 18px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}

  .decision-head-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
  }}

  .decision-result-tag {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 11px;
    font-weight: 700;
    color: var(--coral);
  }}

  .decision-guardrail-tag {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 10px;
    color: var(--muted);
  }}

  .action-pills-row {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
  }}

  .action-pill-box {{
    background: var(--paper-tint);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 10px;
    font-size: 12px;
    font-weight: 700;
    color: var(--ink);
    text-align: center;
  }}

  /* SLIDE 4 */
  .arch-layout {{
    display: flex;
    flex-direction: column;
    gap: 16px;
    height: 100%;
    justify-content: space-between;
  }}

  .arch-pipeline-strip {{
    background: var(--dark-card);
    border: 1px solid var(--dark-border);
    border-radius: 8px;
    padding: 12px 16px;
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 12px;
  }}

  .pipe-step {{
    display: flex;
    flex-direction: column;
    gap: 2px;
  }}

  .pipe-step-num {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 11.5px;
    font-weight: 700;
    color: var(--teal-accent);
  }}

  .pipe-step-badge {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9px;
    font-weight: 700;
    color: var(--teal-accent);
  }}

  .pipe-step-badge.gold {{ color: var(--gold); }}

  .pipe-step-desc {{
    font-size: 10px;
    color: var(--dark-muted);
  }}

  .arch-pillars-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
  }}

  .arch-pillar-card {{
    background: var(--dark-card);
    border: 1px solid var(--dark-border);
    border-radius: 8px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}

  .arch-pillar-card.featured {{
    background: #142822;
    border-color: var(--teal);
  }}

  .pillar-tag {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9.5px;
    font-weight: 700;
    color: var(--teal-accent);
  }}

  .pillar-title {{
    font-size: 16px;
    font-weight: 800;
    color: var(--dark-ink);
  }}

  .pillar-body {{
    font-size: 11px;
    line-height: 1.5;
    color: var(--dark-muted);
  }}

  .arch-banner-footer {{
    background: #11221D;
    border: 1px solid var(--dark-border);
    border-radius: 8px;
    padding: 10px 16px;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}

  .arch-banner-lead {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 11px;
    font-weight: 700;
    color: var(--gold);
  }}

  .arch-banner-sub {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 10px;
    color: var(--dark-muted);
  }}

  /* SLIDE 5: 4-COLUMN BALANCED BEHAVIORAL MATRIX */
  .scenarios-layout {{
    display: flex;
    flex-direction: column;
    gap: 16px;
    height: 100%;
    justify-content: space-between;
  }}

  .scenarios-grid-4 {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    align-items: stretch;
    height: 480px;
  }}

  .case-col-card {{
    background: #FFFFFF;
    border: 1.5px solid var(--border);
    border-radius: 8px;
    padding: 16px 14px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 10px;
  }}

  .case-col-card.teal {{ border-color: var(--teal); }}
  .case-col-card.coral {{ border-color: var(--coral-border); }}
  .case-col-card.amber {{ border-color: var(--amber); }}
  .case-col-card.slate {{ border-color: var(--border-strong); }}

  .col-pill {{
    border-radius: 4px;
    padding: 6px 10px;
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 10px;
    font-weight: 700;
    text-align: center;
  }}

  .col-pill.teal {{ background: var(--teal-light); color: var(--teal-dark); }}
  .col-pill.coral {{ background: var(--coral-light); color: var(--coral-dark); }}
  .col-pill.amber {{ background: var(--amber-light); color: var(--amber-dark); }}
  .col-pill.slate {{ background: var(--paper-tint); color: var(--ink); }}

  .col-title {{
    font-size: 14px;
    font-weight: 800;
    color: var(--ink);
  }}

  .col-section-tag {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9px;
    font-weight: 700;
    color: var(--teal-dark);
    margin-bottom: 2px;
  }}

  .col-section-tag.coral {{ color: var(--coral-dark); }}
  .col-section-tag.amber {{ color: var(--amber-dark); }}

  .col-desc {{
    font-size: 11px;
    line-height: 1.45;
    color: var(--ink-light);
  }}

  .col-out {{
    font-size: 11px;
    line-height: 1.45;
    color: var(--muted);
  }}

  /* SLIDE 6 */
  .execution-layout {{
    display: flex;
    flex-direction: column;
    gap: 16px;
    height: 100%;
    justify-content: space-between;
  }}

  .timeline-bar-wrap {{
    background: #FFFFFF;
    border: 1px solid var(--border-strong);
    border-radius: 8px;
    padding: 12px 16px;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
  }}

  .timeline-col {{
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}

  .timeline-phase-badge {{
    background: var(--teal-light);
    color: var(--teal-dark);
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 4px;
    width: fit-content;
  }}

  .timeline-col-title {{
    font-size: 13.5px;
    font-weight: 800;
    color: var(--ink);
  }}

  .timeline-col-desc {{
    font-size: 11px;
    color: var(--muted);
    line-height: 1.4;
  }}

  .team-cards-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
  }}

  .team-card {{
    background: var(--paper);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px 16px;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}

  .team-role {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9.5px;
    font-weight: 700;
    color: var(--teal);
  }}

  .team-name {{
    font-size: 14px;
    font-weight: 800;
    color: var(--ink);
  }}

  .team-stack {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9px;
    color: var(--muted);
    margin-bottom: 4px;
  }}

  .team-deliverables {{
    display: flex;
    flex-direction: column;
    gap: 3px;
  }}

  .deliv-item {{
    font-size: 10.5px;
    color: var(--ink-light);
    line-height: 1.35;
  }}

  .scope-discipline-band {{
    background: var(--ink);
    border-radius: 8px;
    padding: 12px 18px;
    display: grid;
    grid-template-columns: 1.1fr 1fr 0.9fr;
    gap: 20px;
    align-items: center;
  }}

  .scope-col {{
    display: flex;
    flex-direction: column;
    gap: 3px;
  }}

  .scope-tag {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 10px;
    font-weight: 700;
  }}

  .scope-tag.gold {{ color: var(--gold); }}
  .scope-tag.coral {{ color: #FF8C69; }}
  .scope-tag.teal {{ color: var(--teal-accent); }}

  .scope-text {{
    font-size: 11px;
    color: #DFEAE5;
    line-height: 1.4;
  }}

  /* CONTROLS */
  #controls {{
    position: fixed;
    bottom: 24px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(17, 32, 26, 0.92);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 30px;
    padding: 8px 18px;
    display: flex;
    align-items: center;
    gap: 14px;
    color: #FFFFFF;
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    z-index: 1000;
  }}

  .nav-btn {{
    background: rgba(255, 255, 255, 0.12);
    border: none;
    color: #FFFFFF;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    cursor: pointer;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  .nav-btn:hover {{
    background: rgba(255, 255, 255, 0.25);
  }}

  .nav-dots {{
    display: flex;
    gap: 6px;
  }}

  .dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    cursor: pointer;
  }}

  .dot.active {{
    background: var(--teal-accent);
    width: 20px;
    border-radius: 4px;
  }}

  #notes-drawer {{
    position: fixed;
    right: 0;
    top: 0;
    width: 440px;
    height: 100vh;
    background: #11201A;
    color: #F8F7F4;
    box-shadow: -8px 0 32px rgba(0, 0, 0, 0.4);
    transform: translateX(100%);
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    z-index: 2000;
    padding: 32px 24px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    overflow-y: auto;
  }}

  #notes-drawer.open {{
    transform: translateX(0);
  }}

  #notes-drawer h3 {{
    font-size: 18px;
    color: var(--teal-accent);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  #close-notes {{
    background: none;
    border: none;
    color: #8A9C93;
    font-size: 20px;
    cursor: pointer;
  }}

  #notes-content {{
    font-size: 13.5px;
    line-height: 1.6;
    color: #DFEAE5;
    white-space: pre-wrap;
  }}

  body.overview-mode #deck-container {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    padding: 40px;
    max-width: 1400px;
    margin: 0 auto;
  }}

  body.overview-mode .slide {{
    transform: scale(0.35);
    transform-origin: top left;
    width: 1280px;
    height: 720px;
    margin-bottom: -440px;
    margin-right: -800px;
    cursor: pointer;
  }}

  @media print {{
    @page {{
      size: 1280px 720px;
      margin: 0;
    }}
    body {{
      background: none;
    }}
    #deck-container {{
      padding: 0;
      gap: 0;
    }}
    .slide {{
      box-shadow: none;
      page-break-after: always;
      break-after: page;
      width: 1280px !important;
      height: 720px !important;
      display: flex !important;
    }}
    #controls, #notes-drawer {{
      display: none !important;
    }}
  }}
</style>
</head>
<body>

<div id="deck-container">

  <!-- SLIDE 1: PRODUCT HERO -->
  <section class="slide" id="slide-1">
    <div class="tag-label">AGENTX HACKATHON 2026 · TRACK PS-04 · TEAM ROOKIE (3 MEMBERS)</div>
    <div class="hero-grid">
      <div class="hero-text">
        <div class="hero-wordmark">ReturnLens</div>
        <div class="hero-tagline">{d1.get("subheadline", meta["tagline"])}</div>
        <div class="hero-desc">{d1.get("supporting", meta["one_liner"])}</div>
        <div class="hero-principle-card">
          <div class="hero-principle-tag">CORE ARCHITECTURAL THESIS</div>
          <div class="hero-principle-thesis">“{meta['core_thesis']}”</div>
          <div class="hero-principle-meta">
            Scope: Triage automation · Fail-closed gate · Never auto-refunds<br>
            Guardrail: Server cap ≤ min({meta['refund_guardrail']['ceiling']}, remaining, paid) · Hash-bound
          </div>
        </div>
      </div>

      <div class="console-window">
        <div class="console-titlebar">
          <div class="mac-traffic-lights">
            <div class="mac-dot red"></div>
            <div class="mac-dot yellow"></div>
            <div class="mac-dot green"></div>
          </div>
          <div class="console-title-text">{d1['console_mockup']['title']} — {d1['console_mockup']['case_badge']}</div>
          <div style="font-family:'IBM Plex Mono','Consolas','Courier New',monospace; font-size:9.5px; color:#FDF2D0; font-weight:700;">[ MOCK EVIDENCE PACK ]</div>
        </div>

        <div class="console-subbar">
          <div>CASE: <strong>{meta['sample_order']['case_id']}</strong> · ORDER: <strong>{meta['sample_order']['order_id']}</strong> · SKU: <strong>{meta['sample_order']['sku']}</strong></div>
          <div>DELIVERED: <strong>4d ago</strong> (Window: Day 4/7 PASS)</div>
        </div>

        <div class="console-body">
          <div class="console-comparison">
            <div class="comp-card">
              <img src="{img_white_b64}" class="comp-img" alt="Store Truth White Headphones">
              <div class="comp-label">STORE TRUTH · SHOPIFY</div>
              <div class="comp-title">{meta['sample_order']['sku']} ({meta['sample_order']['ordered_color']})</div>
              <div class="comp-meta">{meta['sample_order']['price']} paid · Studio Spec · Security Tag Required<br>Delivered: 4d ago (Shippo #SH-9012, P-01 verified)<br>Return Window: Day 4/7 (P-04 PASS)</div>
            </div>

            <div class="comp-card coral">
              <img src="{img_black_b64}" class="comp-img" alt="Observed Black Headphones">
              <div class="comp-label">OBSERVED · VIDEO FRAME 00:07</div>
              <div class="comp-title">Black Casing (color-consistent with HEAD-BLK-09)</div>
              <div class="comp-meta">Barcode: Unverified · Exact SKU: Not verified<br>Lighting: Sufficient · Policy P-03 FAIL<br>Contradiction flagged → Route to human seller</div>
            </div>
          </div>

          <div class="console-contradiction">
            P-03 COLOR CONTRADICTION: Observed black casing conflicts with ordered Matte White specification. Exact SKU unverified.
          </div>

          <div class="console-actions">
            <div class="seller-gate-status">● SELLER GATE (FAIL-CLOSED)</div>
            <div class="btn-group">
              <div class="btn btn-sec">Request Box Label</div>
              <div class="btn btn-pri">Review Evidence &amp; Decide</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div>RETURNLENS V7.2 · AGENTX HACKATHON 2026 PS-04 · TEAM ROOKIE (3 MEMBERS)</div>
      <div>01 / 06</div>
    </div>
  </section>

  <!-- SLIDE 2: THE PROBLEM -->
  <section class="slide" id="slide-2">
    <div class="tag-label">THE PROBLEM · SOLO MERCHANT BOTTLENECK · 4 SOURCES</div>
    <div class="headline-wrap">
      <div class="slide-title">One return. Four disconnected systems. Zero shared record.</div>
      <div class="slide-subtitle">{d2.get("supporting_statement", "Solo merchants cross-reference tabs, video footage, and policy rules manually before moving money.")}</div>
    </div>

    <div class="problem-layout">
      <div class="convergence-wrap">
        <div class="sources-list">
          {"".join([f'''
          <div class="source-card">
            <div class="source-head">
              <span class="source-tag">SOURCE 0{i+1}</span>
              <span class="source-name">{src['name'].upper()}</span>
            </div>
            <div class="source-detail">{src['detail']}</div>
          </div>
          ''' for i, src in enumerate(d2["sources"])])}
        </div>

        <div class="gap-focal-card">
          <div class="gap-tag">THE CRITICAL INFORMATION GAP</div>
          <div class="gap-lead">No auditable evidence record. One solo seller making high-stakes financial decisions across browser tabs.</div>
          <div class="gap-body">Without an auditable evidence pack, the merchant either refunds blind (losing COGS and freight) or disputes unfairly (destroying customer trust and merchant ratings).</div>
        </div>
      </div>

      <div class="bottom-callouts-grid">
        <div class="editorial-callout">
          <div class="callout-title">INDUSTRY FRAUD BASELINE (RIGOROUS PROVENANCE · DISTINCT SCOPES)</div>
          <div class="callout-desc">
            • 9.0% — Return Fraud (NRF/Appriss 2024: strict criminal fraud: unboxing swaps, empty boxes).<br>
            • 15.14% — Fraud + Policy Abuse (Appriss/Deloitte 2024: criminal fraud + policy abuse like wardrobing).
          </div>
        </div>

        <div class="editorial-callout">
          <div class="callout-title">SOLO MERCHANT ASYMMETRIC RISK</div>
          <div class="callout-desc">
            • Wrong refund = Lost product COGS + 2-way shipping costs (unrecoverable margin loss).<br>
            • Unfair denial = Ruined customer trust, chargeback penalties &amp; degraded seller account health.
          </div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div>RETURNLENS V7.2 · AGENTX HACKATHON 2026 PS-04 · TEAM ROOKIE (3 MEMBERS)</div>
      <div>02 / 06</div>
    </div>
  </section>

  <!-- SLIDE 3: STAR DEMO -->
  <section class="slide" id="slide-3">
    <div class="tag-label">STAR DEMO · CASE B · CORE BENCHMARK</div>
    <div class="headline-wrap">
      <div class="slide-title">{d3.get("headline", "The order says White. The unboxing video shows Black.")}</div>
      <div class="slide-subtitle">{d3.get("subheadline", "Policy P-03 triggers ESCALATE. No mock label created. No refund draft. No denial without human review.")}</div>
    </div>

    <div class="star-demo-layout">
      <div class="exhibition-wrap">
        <div class="exhibit-board">
          <div class="exhibit-head">ORDER MANIFEST · STORE CATALOG TRUTH (#ORD-7729)</div>
          <img src="{img_white_b64}" class="exhibit-img" alt="Store Truth White Headphones">
          <div class="exhibit-spec">
            <div class="exhibit-spec-title">SKU: {meta['sample_order']['sku']} · Spec: {meta['sample_order']['ordered_color']} Casing</div>
            <div class="exhibit-spec-meta">Price: {meta['sample_order']['price']} paid · Delivered: 4d ago (Shippo #SH-9012)<br>Return Window P-04 (7-Day Policy): PASS (Day 4 of 7)</div>
          </div>
        </div>

        <div class="mismatch-pill">≠</div>

        <div class="exhibit-board coral">
          <div class="exhibit-head">MOCK EVIDENCE PACK · VIDEO CITATION (FRAME 00:07)</div>
          <img src="{img_black_b64}" class="exhibit-img" alt="Observed Black Headphones">
          <div class="exhibit-spec">
            <div class="exhibit-spec-title">Observed: Black Casing (color-consistent with HEAD-BLK-09)</div>
            <div class="exhibit-spec-meta">Exact SKU: Not verified (Barcode unverified) · Policy P-03 FAIL<br>Lighting: Sufficient · REC 00:07 / 00:24 (Mock Keyframe)</div>
          </div>
        </div>
      </div>

      <div class="star-decision-strip">
        <div class="decision-head-row">
          <div class="decision-result-tag">POLICY P-03 RESULT: ESCALATE TO SELLER GATE (FAIL-CLOSED)</div>
          <div class="decision-guardrail-tag">Guardrail: 0 &lt; amt ≤ min({meta['refund_guardrail']['ceiling']}, rem_ref, paid) · Prototype simulation</div>
        </div>
        <div class="action-pills-row">
          <div class="action-pill-box">1. Accept as warehouse mis-shipment</div>
          <div class="action-pill-box">2. Request photo of outside-box shipping label</div>
          <div class="action-pill-box">3. Hold return for physical parcel inspection</div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div>RETURNLENS V7.2 · AGENTX HACKATHON 2026 PS-04 · TEAM ROOKIE (3 MEMBERS)</div>
      <div>03 / 06</div>
    </div>
  </section>

  <!-- SLIDE 4: SYSTEM ARCHITECTURE -->
  <section class="slide dark" id="slide-4">
    <div class="tag-label">SYSTEM ARCHITECTURE · FAIL-CLOSED SAFETY GATES</div>
    <div class="headline-wrap">
      <div class="slide-title">{d4.get("headline", meta["core_thesis"])}</div>
      <div class="slide-subtitle">{d4.get("subheadline", "Exactly 3 model calls per triage pass. Weak evidence triggers stateful clarification. Zero automated refunds.")}</div>
    </div>

    <div class="arch-layout">
      <div class="arch-pipeline-strip">
        <div class="pipe-step">
          <div class="pipe-step-num">1. Planner</div>
          <div class="pipe-step-badge">Model Call 1</div>
          <div class="pipe-step-desc">Proposes typed JSON actions</div>
        </div>
        <div class="pipe-step">
          <div class="pipe-step-num">2. Tools &amp; Vision</div>
          <div class="pipe-step-badge">Model Call 2</div>
          <div class="pipe-step-desc">FFmpeg keyframes + vision (fallible)</div>
        </div>
        <div class="pipe-step">
          <div class="pipe-step-num">3. Policy Engine</div>
          <div class="pipe-step-badge" style="color:var(--dark-muted);">Deterministic Code</div>
          <div class="pipe-step-desc">Evaluates rules P-01–P-08</div>
        </div>
        <div class="pipe-step">
          <div class="pipe-step-num">4. Critic</div>
          <div class="pipe-step-badge">Model Call 3</div>
          <div class="pipe-step-desc">Verifies cited timestamps</div>
        </div>
        <div class="pipe-step">
          <div class="pipe-step-num">5. Seller Gate</div>
          <div class="pipe-step-badge gold">Human Merchant</div>
          <div class="pipe-step-desc">Fail-closed 1-click auth</div>
        </div>
        <div class="pipe-step">
          <div class="pipe-step-num">6. Audit Ledger</div>
          <div class="pipe-step-badge" style="color:var(--dark-muted);">SQLite / JSON</div>
          <div class="pipe-step-desc">Append-only signed audit</div>
        </div>
      </div>

      <div class="arch-pillars-grid">
        <div class="arch-pillar-card">
          <div class="pillar-tag">CALL BUDGET &amp; MODEL RESTRICTION</div>
          <div class="pillar-title">3 Calls Per Triage Pass</div>
          <div class="pillar-body">
            1. Planner proposes typed tool actions.<br>
            2. Vision model inspects keyframes (fallible observation).<br>
            3. Critic evaluates citations against policy.<br><br>
            Case C re-upload triggers Pass 2 (max 6 calls total). Models never access payment APIs directly.
          </div>
        </div>

        <div class="arch-pillar-card featured">
          <div class="pillar-tag">STATEFUL RESUMPTION (CASE C)</div>
          <div class="pillar-title">Clarification &amp; Re-Film Loop</div>
          <div class="pillar-body">
            Low-light video (Policy P-06 FAIL, brightness score: 28/255 &lt; threshold 50/255) triggers ask_for_evidence().<br><br>
            State saves to WAITING_FOR_EVIDENCE → Resumes on upload.<br><br>
            <strong>TERMINATION RULE: After 1 retry, escalates to seller with both attempts logged (never auto-denies).</strong>
          </div>
        </div>

        <div class="arch-pillar-card">
          <div class="pillar-tag">ZERO-LLM FAST PATH</div>
          <div class="pillar-title">Zero-LLM Order Route</div>
          <div class="pillar-body">
            For routine "Where is my order?" inquiries, deterministic code regex routes directly to APIs:<br><br>
            Store API → Courier API → Status Reply<br><br>
            Zero LLM tokens · Zero vision overhead · &lt;500ms response.
          </div>
        </div>
      </div>

      <div class="arch-banner-footer">
        <div class="arch-banner-lead">FAIL-CLOSED FINANCIAL GATE: requires_seller_approval: true · Approval binds case + evidence hash + policy version + nonce.</div>
        <div class="arch-banner-sub">Server Cap: 0 &lt; amount &lt;= min({meta['refund_guardrail']['ceiling']}, remaining_refundable, order_paid) · Idempotency key hash(order_id, return_id, nonce) enforced.</div>
      </div>
    </div>

    <div class="slide-footer">
      <div>RETURNLENS V7.2 · AGENTX HACKATHON 2026 PS-04 · TEAM ROOKIE (3 MEMBERS)</div>
      <div>04 / 06</div>
    </div>
  </section>

  <!-- SLIDE 5: 4-COLUMN BALANCED BEHAVIORAL MATRIX -->
  <section class="slide" id="slide-5">
    <div class="tag-label">DEMO SCENARIOS · BEHAVIORAL MATRIX</div>
    <div class="headline-wrap">
      <div class="slide-title">{d5.get("headline", "Different evidence. Different action.")}</div>
      <div class="slide-subtitle">{d5.get("subheadline", "Four distinct triage behaviors across reproducible test fixtures. Zero automated policy approvals.")}</div>
    </div>

    <div class="scenarios-layout">
      <div class="scenarios-grid-4">
        <div class="case-col-card teal">
          <div class="col-pill teal">01 · PREPARE REVIEW</div>
          <div class="col-title">CASE A · CONSISTENT</div>
          <div>
            <div class="col-section-tag">EVIDENCE PROFILE:</div>
            <div class="col-desc">Manifest matches catalog<br>Packaging tag verified (P-02)<br>Cosmetic defect observed<br>Within 7-day window (P-04)</div>
          </div>
          <div>
            <div class="col-section-tag">POLICY ENGINE ACTION:</div>
            <div class="col-out">Drafts return shipping label &amp; refund draft in pending_return_receipt.<br><br>Funds release only upon physical warehouse parcel receipt.</div>
          </div>
        </div>

        <div class="case-col-card coral">
          <div class="col-pill coral">02 · ESCALATE SELLER</div>
          <div class="col-title">CASE B · CONTRADICTION</div>
          <div>
            <div class="col-section-tag coral">EVIDENCE PROFILE:</div>
            <div class="col-desc">Ordered Matte White<br>Observed Black casing (00:07)<br>Exact SKU unverified<br>Barcode unverified</div>
          </div>
          <div>
            <div class="col-section-tag coral">POLICY ENGINE ACTION:</div>
            <div class="col-out">Policy P-03 FAIL blocks automation. Inhibits label &amp; refund draft.<br><br>Surfaces 3 seller options: mis-shipment / box label / inspection.</div>
          </div>
        </div>

        <div class="case-col-card amber">
          <div class="col-pill amber">03 · CLARIFY LOOP</div>
          <div class="col-title">CASE C · LOW LIGHT</div>
          <div>
            <div class="col-section-tag amber">EVIDENCE PROFILE:</div>
            <div class="col-desc">4s low-light unboxing video<br>Brightness score: 28/255 &lt; 50/255<br>Barcode obscured<br>Only 2 usable frames</div>
          </div>
          <div>
            <div class="col-section-tag amber">POLICY ENGINE ACTION:</div>
            <div class="col-out">Policy P-06 FAIL triggers ask_for_evidence().<br><br>Saves to WAITING_FOR_EVIDENCE; resumes on upload. Max 1 retry.</div>
          </div>
        </div>

        <div class="case-col-card slate">
          <div class="col-pill slate">04 · INSPECT CONTINUITY</div>
          <div class="col-title">CASE D · CONTINUOUS</div>
          <div>
            <div class="col-section-tag">EVIDENCE PROFILE:</div>
            <div class="col-desc">Single unbroken unboxing take<br>Sealed parcel to product display<br>Continuity inspection<br>Flags abrupt transitions</div>
          </div>
          <div>
            <div class="col-section-tag">POLICY ENGINE ACTION:</div>
            <div class="col-out">Inspects sequence continuity and flags abrupt cuts.<br><br>Basic continuity in prototype; advanced forensics is cut first.</div>
          </div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div>RETURNLENS V7.2 · AGENTX HACKATHON 2026 PS-04 · TEAM ROOKIE (3 MEMBERS)</div>
      <div>05 / 06</div>
    </div>
  </section>

  <!-- SLIDE 6: 24-HOUR SPRINT PLAN -->
  <section class="slide" id="slide-6">
    <div class="tag-label">24-HOUR PROTOTYPE PLAN · TEAM ROOKIE (3 MEMBERS)</div>
    <div class="headline-wrap">
      <div class="slide-title">{d6.get("headline", "A credible prototype in 24 hours.")}</div>
      <div class="slide-subtitle">{d6.get("subheadline", "Strict scope boundaries and single-threaded ownership make the prototype buildable in one day.")}</div>
    </div>

    <div class="execution-layout">
      <div class="timeline-bar-wrap">
        <div class="timeline-col">
          <div class="timeline-phase-badge">00 – 06h · PHASE 01</div>
          <div class="timeline-col-title">Foundation</div>
          <div class="timeline-col-desc">Mock Store/Shippo APIs · LangGraph state schema · Zero-LLM fast path</div>
        </div>

        <div class="timeline-col">
          <div class="timeline-phase-badge">06 – 12h · PHASE 02</div>
          <div class="timeline-col-title">Evidence Pipeline</div>
          <div class="timeline-col-desc">FFmpeg ~1fps extractor · Vision observation schema · Seller Console UI</div>
        </div>

        <div class="timeline-col">
          <div class="timeline-phase-badge">12 – 18h · PHASE 03</div>
          <div class="timeline-col-title">Integration</div>
          <div class="timeline-col-desc">Case C pause/resume loop · 4 test fixtures (A–D) · Adversarial critic review</div>
        </div>

        <div class="timeline-col">
          <div class="timeline-phase-badge">18 – 24h · PHASE 04</div>
          <div class="timeline-col-title">Validation &amp; Safety</div>
          <div class="timeline-col-desc">Fail-closed authorization tests · 10-test smoke suite · Video demo recording</div>
        </div>
      </div>

      <div class="team-cards-grid">
        <div class="team-card">
          <div class="team-role">PERSON A · BACKEND, POLICY &amp; AUTH</div>
          <div class="team-name">State Machine &amp; Policy Engine</div>
          <div class="team-stack">Stack: LangGraph · Pydantic · SQLite · SHA256</div>
          <div class="team-deliverables">
            <div class="deliv-item">• Policy P-01 to P-08: Deterministic code rules (window, SKU, tag, refund cap)</div>
            <div class="deliv-item">• Zero-LLM Fast Path: Deterministic regex routing for order status queries</div>
            <div class="deliv-item">• Audit Ledger: Append-only JSON log &amp; signed approval binding</div>
            <div class="deliv-item">• Financial Cap: Server calculation min(₹4,999, remaining, paid)</div>
          </div>
        </div>

        <div class="team-card">
          <div class="team-role">PERSON B · VISION &amp; CONSOLE</div>
          <div class="team-name">Video Pipeline &amp; Seller UI</div>
          <div class="team-stack">Stack: FFmpeg · Hosted vision model (unpinned) · HTML/CSS/SVG</div>
          <div class="team-deliverables">
            <div class="deliv-item">• Keyframe Pipeline: Uniform ~1fps sampling &amp; brightness scoring (threshold 50/255)</div>
            <div class="deliv-item">• Structured Vision: Observation schema with timestamp citation metadata</div>
            <div class="deliv-item">• Adversarial Critic: Cross-checks citations against keyframe timestamps</div>
            <div class="deliv-item">• Seller Console: 1-click decision console with mock evidence pack</div>
          </div>
        </div>

        <div class="team-card">
          <div class="team-role">PERSON C · FIXTURES &amp; QA</div>
          <div class="team-name">Scenarios, Lifecycle &amp; QA</div>
          <div class="team-stack">Stack: Pytest · Mock Fixtures · Automated Smoke QA</div>
          <div class="team-deliverables">
            <div class="deliv-item">• Benchmark Cases: Staged fixtures for 4 demo cases (A–D)</div>
            <div class="deliv-item">• Case C Lifecycle: Re-film loop in WAITING_FOR_EVIDENCE (1 retry max)</div>
            <div class="deliv-item">• Fail-Closed Testing: Verifies zero automated refunds &amp; approval gates</div>
            <div class="deliv-item">• Automated QA: 10-test smoke suite, boundary verification &amp; demo recording</div>
          </div>
        </div>
      </div>

      <div class="scope-discipline-band">
        <div class="scope-col">
          <div class="scope-tag gold">MUST DELIVER (CORE PROTOTYPE)</div>
          <div class="scope-text">Mock APIs · Policy engine · 4 benchmark cases (A–D) · Approval binding · Seller gate · Zero-LLM fast path</div>
        </div>

        <div class="scope-col">
          <div class="scope-tag coral">CUT FIRST IF BEHIND</div>
          <div class="scope-text">Advanced video forensics (Case D stretch) · WhatsApp bot · Exchanges · Multi-seller auth · Audio analysis · Public cloud deployment</div>
        </div>

        <div class="scope-col">
          <div class="scope-tag teal">PROTOTYPE SCOPE LOCKED</div>
          <div class="scope-text">100% reproducible offline build · Zero external network dependencies</div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div>RETURNLENS V7.2 · AGENTX HACKATHON 2026 PS-04 · TEAM ROOKIE (3 MEMBERS)</div>
      <div>06 / 06</div>
    </div>
  </section>

</div>

<div id="controls">
  <button class="nav-btn" id="prev-btn">←</button>
  <span id="slide-num">01 / 06</span>
  <button class="nav-btn" id="next-btn">→</button>
  <div class="nav-dots">
    <div class="dot active" data-target="1"></div>
    <div class="dot" data-target="2"></div>
    <div class="dot" data-target="3"></div>
    <div class="dot" data-target="4"></div>
    <div class="dot" data-target="5"></div>
    <div class="dot" data-target="6"></div>
  </div>
  <button class="nav-btn" id="notes-btn" title="Toggle Speaker Notes (N)" style="border-radius:4px; width:auto; padding:0 8px; font-size:10px;">NOTES (N)</button>
  <button class="nav-btn" id="overview-btn" title="Toggle Grid Overview (O)" style="border-radius:4px; width:auto; padding:0 8px; font-size:10px;">GRID (O)</button>
</div>

<div id="notes-drawer">
  <h3>
    <span>SPEAKER NOTES</span>
    <button id="close-notes">&times;</button>
  </h3>
  <div id="notes-content"></div>
</div>

<script>
  const notes = {{
    1: {json.dumps(d1["speaker_notes"])},
    2: {json.dumps(d2["speaker_notes"])},
    3: {json.dumps(d3["speaker_notes"])},
    4: {json.dumps(d4["speaker_notes"])},
    5: {json.dumps(d5["speaker_notes"])},
    6: {json.dumps(d6["speaker_notes"])}
  }};

  let current = 1;
  const total = 6;
  const slides = document.querySelectorAll('.slide');
  const numDisplay = document.getElementById('slide-num');
  const dots = document.querySelectorAll('.dot');
  const notesContent = document.getElementById('notes-content');
  const notesDrawer = document.getElementById('notes-drawer');

  function updateSlide(n) {{
    if (n < 1) n = 1;
    if (n > total) n = total;
    current = n;
    numDisplay.textContent = `0${{current}} / 0${{total}}`;
    dots.forEach((d, idx) => {{
      if (idx === current - 1) d.classList.add('active');
      else d.classList.remove('active');
    }});
    notesContent.textContent = notes[current] || "No notes available for this slide.";
    if (!document.body.classList.contains('overview-mode')) {{
      slides[current - 1].scrollIntoView({{ behavior: 'smooth', block: 'center' }});
    }}
  }}

  document.getElementById('prev-btn').addEventListener('click', () => updateSlide(current - 1));
  document.getElementById('next-btn').addEventListener('click', () => updateSlide(current + 1));

  window.addEventListener('keydown', (e) => {{
    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
      updateSlide(current + 1);
    }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
      updateSlide(current - 1);
    }} else if (e.key === 'n' || e.key === 'N') {{
      notesDrawer.classList.toggle('open');
    }} else if (e.key === 'o' || e.key === 'O') {{
      document.body.classList.toggle('overview-mode');
    }}
  }});

  document.getElementById('notes-btn').addEventListener('click', () => notesDrawer.classList.toggle('open'));
  document.getElementById('close-notes').addEventListener('click', () => notesDrawer.classList.remove('open'));
  document.getElementById('overview-btn').addEventListener('click', () => document.body.classList.toggle('overview-mode'));

  dots.forEach(dot => {{
    dot.addEventListener('click', () => {{
      const target = parseInt(dot.getAttribute('data-target'));
      updateSlide(target);
    }});
  }});

  slides.forEach((slide, idx) => {{
    slide.addEventListener('click', () => {{
      if (document.body.classList.contains('overview-mode')) {{
        document.body.classList.remove('overview-mode');
        updateSlide(idx + 1);
      }}
    }});
  }});

  updateSlide(1);
</script>
</body>
</html>"""

    # Write HTML files
    html_target = deliverables_dir / "ReturnLens_v7_2.html"
    root_target = base_dir / "ReturnLens_v7_2.html"

    with open(html_target, "w", encoding="utf-8", newline="\n") as f:
        f.write(html_content)
    shutil.copy2(html_target, root_target)
    print(f"Compiled ReturnLens_v7_2.html successfully: {html_target} ({os.path.getsize(html_target)} bytes)")

    # Export PDF via headless browser
    username = os.environ.get("USERNAME", "")
    browser_candidates = [
        os.environ.get("CHROME_PATH"),
        os.environ.get("EDGE_PATH"),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        rf"C:\Users\{username}\AppData\Local\Google\Chrome\Application\chrome.exe",
        rf"C:\Users\{username}\AppData\Local\Microsoft\Edge\Application\msedge.exe",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/bin/microsoft-edge",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
    ]
    browser = None
    for p in browser_candidates:
        if p and os.path.exists(p):
            browser = p
            break

    pdf_deliverable = deliverables_dir / "ReturnLens_v7_2.pdf"
    pdf_root = base_dir / "ReturnLens_v7_2.pdf"

    if browser:
        cmd = [
            browser,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_deliverable}",
            str(html_target)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0 and pdf_deliverable.exists():
            shutil.copy2(pdf_deliverable, pdf_root)
            print(f"Exported vector PDF: {pdf_deliverable} ({os.path.getsize(pdf_deliverable)} bytes)")

            # Render Preview Sheet (2352x882, exact 16:9 contact sheet, 3 columns x 2 rows)
            doc = fitz.open(str(pdf_deliverable))
            images = []
            for page in doc:
                pix = page.get_pixmap(dpi=150)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                images.append(img)

            if len(images) == 6:
                thumb_w = 784
                thumb_h = int(thumb_w * images[0].size[1] / images[0].size[0])
                resized = [img.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS) for img in images]
                grid = Image.new("RGB", (thumb_w * 3, thumb_h * 2), (20, 32, 28))
                for idx, img in enumerate(resized):
                    row = idx // 3
                    col = idx % 3
                    grid.paste(img, (col * thumb_w, row * thumb_h))

                preview_deliv = deliverables_dir / "ReturnLens_v7_2_preview.png"
                preview_root = base_dir / "ReturnLens_v7_2_preview.png"
                grid.save(preview_deliv, quality=95)
                shutil.copy2(preview_deliv, preview_root)
                print(f"Exported preview contact sheet: {preview_deliv} ({grid.size})")

if __name__ == "__main__":
    generate_v7_2()
