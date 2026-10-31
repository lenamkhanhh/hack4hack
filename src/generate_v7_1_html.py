import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
import fitz
from PIL import Image
import base64

def generate_v7_1():
    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / "content" / "deck_data.json"
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
<title>ReturnLens v7.1 — Evidence-Checked Returns Triage Agent (AgentX Hackathon 2026, Track PS-04)</title>
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
    padding: 32px 0 80px 0;
    gap: 36px;
  }}

  .slide {{
    width: 1280px;
    height: 720px;
    background-color: var(--paper);
    position: relative;
    padding: 34px 44px 26px 44px;
    box-shadow: 0 20px 48px rgba(0, 0, 0, 0.25);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
    flex-shrink: 0;
  }}

  .slide.dark {{
    background-color: var(--dark-bg);
    color: var(--dark-ink);
  }}

  .tag-label {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    color: var(--teal);
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  .slide.dark .tag-label {{
    color: var(--teal-accent);
  }}

  .headline-wrap {{
    margin-top: 4px;
    margin-bottom: 12px;
  }}

  .slide-title {{
    font-size: 36px;
    font-weight: 800;
    letter-spacing: -1.2px;
    line-height: 1.1;
    color: var(--ink);
  }}

  .slide.dark .slide-title {{
    color: var(--dark-ink);
  }}

  .slide-subtitle {{
    font-size: 15.5px;
    font-weight: 500;
    color: var(--muted);
    margin-top: 6px;
    line-height: 1.35;
  }}

  .slide.dark .slide-subtitle {{
    color: var(--dark-muted);
  }}

  .slide-footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 10px;
    border-top: 1px solid var(--border);
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 10px;
    color: var(--subtle);
  }}

  .slide.dark .slide-footer {{
    border-top-color: var(--dark-border);
    color: var(--dark-muted);
  }}

  /* SLIDE 1 */
  .hero-grid {{
    display: grid;
    grid-template-columns: 410px 1fr;
    gap: 32px;
    align-items: center;
    height: 100%;
    margin-bottom: 6px;
  }}

  .hero-text {{
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 16px;
  }}

  .hero-wordmark {{
    font-size: 52px;
    font-weight: 900;
    letter-spacing: -2px;
    line-height: 1;
    color: var(--ink);
  }}

  .hero-tagline {{
    font-size: 23px;
    font-weight: 800;
    line-height: 1.25;
    letter-spacing: -0.6px;
    color: var(--teal);
  }}

  .hero-desc {{
    font-size: 15px;
    line-height: 1.45;
    color: var(--muted);
  }}

  .hero-principle-card {{
    background: var(--paper-tint);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px 16px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}

  .hero-principle-tag {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9.5px;
    font-weight: 700;
    letter-spacing: 1px;
    color: var(--teal-dark);
  }}

  .hero-principle-thesis {{
    font-size: 14.5px;
    font-weight: 800;
    color: var(--ink);
  }}

  .hero-principle-meta {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9.5px;
    line-height: 1.4;
    color: var(--ink-light);
  }}

  /* CONSOLE WINDOW */
  .console-window {{
    background: #FFFFFF;
    border: 1px solid var(--border-strong);
    border-radius: 8px;
    box-shadow: 0 14px 36px rgba(17, 32, 26, 0.12);
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }}

  .console-titlebar {{
    background: var(--ink);
    padding: 8px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: #FFFFFF;
  }}

  .mac-traffic-lights {{
    display: flex;
    gap: 6px;
    align-items: center;
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
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.6px;
    color: #FDF2D0;
  }}

  .console-subbar {{
    background: var(--paper-tint);
    border-bottom: 1px solid var(--border);
    padding: 8px 16px;
    display: flex;
    justify-content: space-between;
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 10px;
    color: var(--ink);
  }}

  .console-body {{
    padding: 14px 16px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}

  .console-comparison {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
  }}

  .comp-card {{
    background: var(--paper);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}

  .comp-card.coral {{
    background: var(--coral-light);
    border-color: var(--coral-border);
    border-width: 1.5px;
  }}

  .comp-img {{
    width: 100%;
    height: 120px;
    object-fit: cover;
    border-radius: 4px;
  }}

  .comp-label {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9px;
    font-weight: 700;
    color: var(--muted);
  }}

  .comp-card.coral .comp-label {{
    color: var(--coral);
  }}

  .comp-title {{
    font-size: 13.5px;
    font-weight: 800;
    color: var(--ink);
  }}

  .comp-card.coral .comp-title {{
    color: var(--coral-dark);
  }}

  .comp-meta {{
    font-size: 11px;
    line-height: 1.35;
    color: var(--muted);
  }}

  .comp-card.coral .comp-meta {{
    color: var(--ink-light);
  }}

  .console-contradiction {{
    background: var(--coral-light);
    border: 1px solid var(--coral-border);
    border-radius: 6px;
    padding: 8px 12px;
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 10px;
    font-weight: 700;
    color: var(--coral-dark);
  }}

  .console-ledger {{
    background: var(--paper-tint);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 7px 12px;
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9.5px;
    color: var(--muted);
  }}

  .console-actions {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 4px;
  }}

  .seller-gate-status {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 10px;
    font-weight: 700;
    color: var(--amber-dark);
  }}

  .btn-group {{
    display: flex;
    gap: 8px;
  }}

  .btn {{
    font-size: 11.5px;
    font-weight: 700;
    padding: 7px 14px;
    border-radius: 5px;
    border: 1px solid transparent;
  }}

  .btn-sec {{
    background: var(--paper-tint);
    border-color: var(--border-strong);
    color: var(--ink);
  }}

  .btn-pri {{
    background: var(--teal);
    color: #FFFFFF;
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
    grid-template-columns: 460px 1fr;
    gap: 24px;
    align-items: stretch;
  }}

  .sources-list {{
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}

  .source-card {{
    background: #FFFFFF;
    border: 1px solid var(--border-strong);
    border-radius: 6px;
    padding: 10px 14px;
    display: flex;
    flex-direction: column;
    gap: 3px;
    position: relative;
  }}

  .source-head {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  .source-tag {{
    background: var(--teal-light);
    color: var(--teal-dark);
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9px;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 3px;
  }}

  .source-name {{
    font-size: 12px;
    font-weight: 800;
    color: var(--ink);
  }}

  .source-detail {{
    font-size: 12px;
    color: var(--muted);
  }}

  .gap-focal-card {{
    background: var(--ink);
    border-radius: 8px;
    padding: 24px 28px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 12px;
    color: #FFFFFF;
  }}

  .gap-tag {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 11px;
    font-weight: 700;
    color: var(--gold);
    letter-spacing: 0.8px;
  }}

  .gap-quote {{
    font-size: 24px;
    font-weight: 800;
    line-height: 1.25;
    color: #FFFFFF;
  }}

  .gap-lead {{
    font-size: 14.5px;
    line-height: 1.4;
    color: #DFEAE5;
  }}

  .gap-body {{
    font-size: 13.5px;
    line-height: 1.4;
    color: #A5C0B6;
  }}

  .bottom-callouts-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
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
    font-size: 9.5px;
    font-weight: 700;
    color: var(--teal-dark);
  }}

  .callout-desc {{
    font-size: 11.5px;
    line-height: 1.35;
    color: var(--ink-light);
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
    grid-template-columns: 1fr 80px 1fr;
    align-items: center;
    gap: 16px;
  }}

  .exhibit-board {{
    background: #FFFFFF;
    border: 1px solid var(--border-strong);
    border-radius: 8px;
    padding: 14px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}

  .exhibit-board.coral {{
    background: #FFFCFC;
    border-color: var(--coral-border);
    border-width: 1.5px;
  }}

  .exhibit-head {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 11px;
    font-weight: 700;
    color: var(--teal);
  }}

  .exhibit-board.coral .exhibit-head {{
    color: var(--coral);
  }}

  .exhibit-img {{
    width: 100%;
    height: 220px;
    object-fit: cover;
    border-radius: 4px;
  }}

  .exhibit-spec {{
    display: flex;
    flex-direction: column;
    gap: 4px;
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
    font-size: 11.5px;
    line-height: 1.35;
    color: var(--ink-light);
  }}

  .exhibit-board.coral .exhibit-spec-meta {{
    color: var(--coral-dark);
  }}

  .mismatch-pill {{
    width: 68px;
    height: 68px;
    border-radius: 50%;
    background: var(--coral);
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    font-weight: 900;
    margin: 0 auto;
    box-shadow: 0 4px 14px rgba(200, 75, 49, 0.35);
  }}

  .star-decision-strip {{
    background: #FFFFFF;
    border: 1px solid var(--border-strong);
    border-radius: 8px;
    padding: 12px 18px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}

  .decision-head-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  .decision-result-tag {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    font-weight: 700;
    color: var(--coral-dark);
  }}

  .decision-guardrail-tag {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 10.5px;
    color: var(--muted);
  }}

  .action-pills-row {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 12px;
  }}

  .action-pill-box {{
    background: var(--paper-tint);
    border: 1px solid var(--border-strong);
    border-radius: 6px;
    padding: 8px 12px;
    text-align: center;
    font-size: 11.5px;
    font-weight: 700;
    color: var(--ink);
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
    gap: 3px;
  }}

  .pipe-step-num {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    font-weight: 700;
    color: var(--dark-ink);
  }}

  .pipe-step-badge {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9px;
    font-weight: 700;
    color: var(--teal-accent);
  }}

  .pipe-step-badge.gold {{
    color: var(--gold);
  }}

  .pipe-step-desc {{
    font-size: 10.5px;
    color: var(--dark-muted);
    line-height: 1.3;
  }}

  .arch-pillars-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 16px;
  }}

  .arch-pillar-card {{
    background: var(--dark-card);
    border: 1px solid var(--dark-border);
    border-radius: 8px;
    padding: 16px 18px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}

  .arch-pillar-card.featured {{
    background: #142822;
    border-color: var(--teal);
    border-width: 1.5px;
  }}

  .pillar-tag {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 10px;
    font-weight: 700;
    color: var(--teal-accent);
  }}

  .pillar-title {{
    font-size: 17.5px;
    font-weight: 800;
    color: var(--dark-ink);
  }}

  .pillar-body {{
    font-size: 12.5px;
    line-height: 1.45;
    color: var(--dark-muted);
  }}

  .arch-pillar-card.featured .pillar-body {{
    color: #D2E5DC;
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
    font-size: 11.5px;
    font-weight: 700;
    color: var(--gold);
  }}

  .arch-banner-sub {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 10.5px;
    color: var(--dark-muted);
  }}

  /* SLIDE 5 */
  .scenarios-layout {{
    display: flex;
    flex-direction: column;
    gap: 16px;
    height: 100%;
    justify-content: space-between;
  }}

  .scenarios-grid {{
    display: grid;
    grid-template-columns: 460px 1fr;
    gap: 20px;
    align-items: stretch;
  }}

  .case-b-hero-card {{
    background: #FFFFFF;
    border: 2px solid var(--coral-border);
    border-radius: 8px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}

  .case-b-tag {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9.5px;
    font-weight: 700;
    color: var(--coral);
  }}

  .case-b-title {{
    font-size: 20px;
    font-weight: 800;
    color: var(--ink);
  }}

  .case-b-sub {{
    font-size: 12px;
    color: var(--muted);
  }}

  .case-b-cite-box {{
    background: var(--coral-light);
    border: 1px solid var(--coral-border);
    border-radius: 6px;
    padding: 10px;
    display: grid;
    grid-template-columns: 1fr 110px;
    gap: 10px;
    align-items: center;
  }}

  .cite-text {{
    display: flex;
    flex-direction: column;
    gap: 3px;
    font-size: 11px;
  }}

  .cite-title {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9px;
    font-weight: 700;
    color: var(--coral);
  }}

  .cite-img {{
    width: 110px;
    height: 80px;
    object-fit: cover;
    border-radius: 4px;
  }}

  .case-b-action-bar {{
    background: var(--ink);
    border-radius: 4px;
    padding: 7px 12px;
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 10px;
    font-weight: 700;
    color: var(--gold);
    text-align: center;
  }}

  .case-b-options-box {{
    background: var(--paper-tint);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 10px 12px;
    display: flex;
    flex-direction: column;
    gap: 5px;
  }}

  .options-label {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9.5px;
    font-weight: 700;
    color: var(--teal-dark);
  }}

  .option-line {{
    font-size: 11.5px;
    font-weight: 600;
    color: var(--ink);
  }}

  .option-guard {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9px;
    color: var(--muted);
    margin-top: 2px;
  }}

  .cases-stack {{
    display: flex;
    flex-direction: column;
    gap: 12px;
  }}

  .case-row-card {{
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 14px 16px;
    display: flex;
    flex-direction: column;
    gap: 5px;
  }}

  .case-row-head {{
    display: flex;
    align-items: center;
    gap: 10px;
  }}

  .case-row-title {{
    font-size: 14.5px;
    font-weight: 800;
    color: var(--ink);
  }}

  .case-row-badge {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 10px;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 3px;
  }}

  .case-row-badge.teal {{ background: var(--teal-light); color: var(--teal-dark); }}
  .case-row-badge.amber {{ background: var(--amber-light); color: var(--amber-dark); }}
  .case-row-badge.ink {{ background: var(--paper-tint); color: var(--ink); }}

  .case-row-ev {{
    font-size: 12px;
    color: var(--muted);
  }}

  .case-row-out {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 10.5px;
    font-weight: 700;
    color: var(--teal-dark);
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
    padding: 12px 18px;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
  }}

  .timeline-col {{
    display: flex;
    flex-direction: column;
    gap: 4px;
    position: relative;
  }}

  .timeline-phase-badge {{
    background: var(--teal-light);
    color: var(--teal-dark);
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9px;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 3px;
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
    line-height: 1.35;
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
    gap: 6px;
  }}

  .team-role {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9.5px;
    font-weight: 700;
    color: var(--teal);
  }}

  .team-name {{
    font-size: 15px;
    font-weight: 800;
    color: var(--ink);
  }}

  .team-stack {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9.5px;
    color: var(--muted);
    margin-bottom: 2px;
  }}

  .team-deliverables {{
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}

  .deliv-item {{
    font-size: 11px;
    line-height: 1.35;
    color: var(--ink-light);
  }}

  .scope-discipline-band {{
    background: var(--ink);
    border-radius: 8px;
    padding: 14px 20px;
    display: grid;
    grid-template-columns: 1.2fr 1fr 0.8fr;
    gap: 20px;
    color: #FFFFFF;
  }}

  .scope-col {{
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}

  .scope-tag {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.6px;
  }}

  .scope-tag.gold {{ color: var(--gold); }}
  .scope-tag.coral {{ color: #FF8C69; }}
  .scope-tag.teal {{ color: var(--teal-accent); }}

  .scope-text {{
    font-size: 12px;
    line-height: 1.35;
    color: #DFEAE5;
  }}

  .scope-text.mono {{
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    color: #FFFFFF;
  }}

  /* OVERVIEW & NOTES UI */
  #controls {{
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(17, 32, 26, 0.9);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 30px;
    padding: 8px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    z-index: 1000;
    color: #FFFFFF;
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-size: 12px;
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
          <div class="hero-principle-tag">CORE ARCHITECTURAL PRINCIPLE</div>
          <div class="hero-principle-thesis">“{meta['core_thesis']}”</div>
          <div class="hero-principle-meta">
            Scope: Return triage + order status · Mock fixtures · Never auto-refunds<br>
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
              <div class="comp-meta">{meta['sample_order']['price']} paid · Studio Spec · Tag present<br>Delivered: 4d ago (Shippo #SH-9012)<br>Return Window: Day 4/7 (P-04 PASS)</div>
            </div>

            <div class="comp-card coral">
              <img src="{img_black_b64}" class="comp-img" alt="Observed Black Headphones">
              <div class="comp-label">OBSERVED · VIDEO FRAME 00:07</div>
              <div class="comp-title">Black Casing (color-consistent with HEAD-BLK-09)</div>
              <div class="comp-meta">Barcode: Unverified · Exact SKU: Not verified<br>Lighting: Optimal (142/255) · Policy P-03 FAIL<br>Contradiction flagged → Route to human seller</div>
            </div>
          </div>

          <div class="console-contradiction">
            P-03 COLOR CONTRADICTION: Observed black casing conflicts with ordered Matte White specification. Exact SKU unverified.
          </div>

          <div class="console-ledger">
            AUDIT LEDGER: Logged to SQLite · SHA256 evidence hash · Server refund cap: ≤ min({meta['refund_guardrail']['ceiling']}, rem, paid)
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
      <div>RETURNLENS V7.1 · AGENTX HACKATHON 2026 PS-04 · TEAM ROOKIE (3 MEMBERS)</div>
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
          <div class="gap-quote">“What verifiable evidence justifies moving this money?”</div>
          <div class="gap-lead">Four disconnected systems. One solo seller making high-stakes financial decisions across browser tabs.</div>
          <div class="gap-body">Without an auditable evidence pack, the merchant either refunds blind (losing COGS and 2-way freight) or disputes unfairly (destroying customer trust and merchant ratings).</div>
        </div>
      </div>

      <div class="bottom-callouts-grid">
        <div class="editorial-callout">
          <div class="callout-title">INDUSTRY FRAUD BASELINE (DEFINITIONS DIFFER · NOT DIRECTLY COMPARABLE)</div>
          <div class="callout-desc">
            • 9.0% — Return Fraud (NRF 2025: criminal only): Strict criminal fraud (unboxing swaps, empty boxes).<br>
            • 15.14% — Fraud + Policy Abuse (Appriss/Deloitte 2024: criminal + abuse): Criminal fraud combined with policy abuse (wardrobing).
          </div>
        </div>

        <div class="editorial-callout">
          <div class="callout-title">SOLO MERCHANT ASYMMETRIC RISK</div>
          <div class="callout-desc">
            • Wrong refund = Lost product COGS + 2-way shipping costs (unrecoverable margin loss).<br>
            • Unfair denial = Ruined customer trust, chargeback penalties & degraded seller account health.
          </div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div>RETURNLENS V7.1 · AGENTX HACKATHON 2026 PS-04 · TEAM ROOKIE (3 MEMBERS)</div>
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
            <div class="exhibit-spec-meta">Exact SKU: Not verified (Barcode unverified) · Policy P-03 FAIL<br>Lighting: Optimal (142/255) · REC 00:07 / 00:24 (Mock Keyframe)</div>
          </div>
        </div>
      </div>

      <div class="star-decision-strip">
        <div class="decision-head-row">
          <div class="decision-result-tag">POLICY P-03 RESULT: ESCALATE TO SELLER GATE (FAIL-CLOSED)</div>
          <div class="decision-guardrail-tag">Guardrail: 0 &lt; amt ≤ min({meta['refund_guardrail']['ceiling']}, rem_ref, paid) · Never auto-refunds</div>
        </div>
        <div class="action-pills-row">
          <div class="action-pill-box">1. Accept as warehouse mis-shipment</div>
          <div class="action-pill-box">2. Request photo of outside-box shipping label</div>
          <div class="action-pill-box">3. Hold return for physical parcel inspection</div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div>RETURNLENS V7.1 · AGENTX HACKATHON 2026 PS-04 · TEAM ROOKIE (3 MEMBERS)</div>
      <div>03 / 06</div>
    </div>
  </section>

  <!-- SLIDE 4: SYSTEM ARCHITECTURE -->
  <section class="slide dark" id="slide-4">
    <div class="tag-label">SYSTEM ARCHITECTURE · FAIL-CLOSED GOVERNANCE</div>
    <div class="headline-wrap">
      <div class="slide-title">{d4.get("headline", meta["core_thesis"])}</div>
      <div class="slide-subtitle">Exactly 3 base model calls per triage case. Weak evidence escalates. Never releases automated refunds.</div>
    </div>

    <div class="arch-layout">
      <div class="arch-pipeline-strip">
        <div class="pipe-step">
          <div class="pipe-step-num">1. Planner</div>
          <div class="pipe-step-badge">Model Call 1</div>
          <div class="pipe-step-desc">Proposes typed JSON actions</div>
        </div>
        <div class="pipe-step">
          <div class="pipe-step-num">2. Tools & Vision</div>
          <div class="pipe-step-badge">Model Call 2</div>
          <div class="pipe-step-desc">FFmpeg keyframes + vision</div>
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
          <div class="pillar-tag">CALL BUDGET & MODEL RESTRICTION</div>
          <div class="pillar-title">Exactly 3 Model Calls</div>
          <div class="pillar-body">
            1. Planner proposes typed tool actions.<br>
            2. Vision model inspects server-extracted keyframes.<br>
            3. Critic evaluates citations against policy.<br><br>
            <strong>MODELS NEVER ACCESS PAYMENT APIS DIRECTLY.</strong>
          </div>
        </div>

        <div class="arch-pillar-card featured">
          <div class="pillar-tag">STATEFUL RESUMPTION (CASE C)</div>
          <div class="pillar-title">Clarification & Re-Film Loop</div>
          <div class="pillar-body">
            Low-light video (Policy P-06 FAIL, brightness score: 28/255) triggers ask_for_evidence().<br><br>
            State saves to WAITING_FOR_EVIDENCE → Resumes on upload.<br><br>
            <strong>TERMINATION RULE: After 1 retry, escalates to seller with both attempts logged (never auto-denies).</strong>
          </div>
        </div>

        <div class="arch-pillar-card">
          <div class="pillar-tag">SECONDARY PS-04 ROUTE</div>
          <div class="pillar-title">Tiny PS-04 Order Route</div>
          <div class="pillar-body">
            For routine "Where is my order?" inquiries, the agent bypasses vision models entirely:<br><br>
            Store API → Courier API → Status Reply<br><br>
            Zero vision token waste · Instant response.
          </div>
        </div>
      </div>

      <div class="arch-banner-footer">
        <div class="arch-banner-lead">FAIL-CLOSED FINANCIAL GATE: requires_seller_approval: true · Approval binds case + evidence hash + policy version.</div>
        <div class="arch-banner-sub">Server Cap: 0 &lt; amount &lt;= min({meta['refund_guardrail']['ceiling']}, remaining_refundable, order_paid) · Revalidation check before draft release.</div>
      </div>
    </div>

    <div class="slide-footer">
      <div>RETURNLENS V7.1 · AGENTX HACKATHON 2026 PS-04 · TEAM ROOKIE (3 MEMBERS)</div>
      <div>04 / 06</div>
    </div>
  </section>

  <!-- SLIDE 5: 4 BENCHMARK CASES -->
  <section class="slide" id="slide-5">
    <div class="tag-label">EVALUATION SUITE · 4 CONTROLLED SCENARIOS</div>
    <div class="headline-wrap">
      <div class="slide-title">{d5.get("headline", "Different evidence. Controlled, predictable action.")}</div>
      <div class="slide-subtitle">{d5.get("subheadline", "Every case produces an auditable mock evidence pack. No automatic policy approvals.")}</div>
    </div>

    <div class="scenarios-layout">
      <div class="scenarios-grid">
        <div class="case-b-hero-card">
          <div class="case-b-tag">CORE BENCHMARK SCENARIO · P-03 CONTRADICTION</div>
          <div class="case-b-title">Case B: Color Contradiction</div>
          <div class="case-b-sub">The order says White. Unboxing video frame 00:07 shows Black.</div>

          <div class="case-b-cite-box">
            <div class="cite-text">
              <div class="cite-title">MOCK EVIDENCE PACK · FRAME 00:07</div>
              <div>Manifest: {meta['sample_order']['sku']} White ({meta['sample_order']['price']})</div>
              <div style="font-weight:700; color:var(--coral-dark);">Observed: Black casing (color-consistent)</div>
              <div style="font-family:'IBM Plex Mono','Consolas','Courier New',monospace; font-size:9.5px; color:var(--muted);">Barcode: Unverified · Exact SKU: Not verified</div>
              <div style="font-weight:700; color:var(--coral-dark);">P-03 FAIL → No label, no refund draft</div>
            </div>
            <img src="{img_black_b64}" class="cite-img" alt="Case B unboxing frame thumbnail">
          </div>

          <div class="case-b-action-bar">
            POLICY ACTION: ESCALATE TO SELLER GATE (FAIL-CLOSED)
          </div>

          <div class="case-b-options-box">
            <div class="options-label">PRESERVED SELLER OPTIONS IN DECISION CONSOLE:</div>
            <div class="option-line">① Accept warehouse mis-shipment</div>
            <div class="option-line">② Request photo of outside-box shipping label</div>
            <div class="option-line">③ Hold return for physical parcel inspection</div>
            <div class="option-guard">Financial Guardrail: 0 &lt; amount ≤ min({meta['refund_guardrail']['ceiling']}, rem, paid) · Binds evidence hash</div>
          </div>
        </div>

        <div class="cases-stack">
          <div class="case-row-card">
            <div class="case-row-head">
              <div class="case-row-title">Case A: Valid Return (ORD-1042)</div>
              <div class="case-row-badge teal">PREPARE SELLER REVIEW</div>
            </div>
            <div class="case-row-ev">Evidence: ORD-1042 · ₹1,499 · SKU matches catalog · Packaging tag present · Within 7-day return window.</div>
            <div class="case-row-out">Outcome: Mock shipping label created · Refund draft placed in pending_return_receipt (not executed).</div>
          </div>

          <div class="case-row-card">
            <div class="case-row-head">
              <div class="case-row-title">Case C: Low-Light Video (Re-Film Loop)</div>
              <div class="case-row-badge amber">ASK &amp; RESUME</div>
            </div>
            <div class="case-row-ev">Evidence: 4-second dark unboxing video · Brightness score: 28/255 · Only 2 usable keyframes extracted.</div>
            <div class="case-row-out">Outcome: Agent issues re-film checklist under Policy P-06 · State saved to WAITING_FOR_EVIDENCE · Resumes on upload (after 1 retry, escalates with both attempts logged; never auto-denies).</div>
          </div>

          <div class="case-row-card">
            <div class="case-row-head">
              <div class="case-row-title">Case D: Continuous Unboxing Sequence</div>
              <div class="case-row-badge ink">INSPECT SEQUENCE</div>
            </div>
            <div class="case-row-ev">Evidence: Single continuous take from opening sealed parcel to displaying label in one sequence.</div>
            <div class="case-row-out">Outcome: Inspects sequence continuity and flags abrupt transitions. Does not claim proof of identical item.</div>
          </div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div>RETURNLENS V7.1 · AGENTX HACKATHON 2026 PS-04 · TEAM ROOKIE (3 MEMBERS)</div>
      <div>05 / 06</div>
    </div>
  </section>

  <!-- SLIDE 6: 24-HOUR SPRINT PLAN -->
  <section class="slide" id="slide-6">
    <div class="tag-label">24-HOUR PROTOTYPE PLAN · TEAM ROOKIE (3 MEMBERS)</div>
    <div class="headline-wrap">
      <div class="slide-title">{d6.get("headline", "A credible, buildable prototype in 24 hours.")}</div>
      <div class="slide-subtitle">{d6.get("subheadline", "Strict scope discipline, mock data fixtures, and single-threaded ownership ensure on-time delivery.")}</div>
    </div>

    <div class="execution-layout">
      <div class="timeline-bar-wrap">
        <div class="timeline-col">
          <div class="timeline-phase-badge">00 – 06h · PHASE 01</div>
          <div class="timeline-col-title">Foundation</div>
          <div class="timeline-col-desc">Mock Store/Shippo APIs · LangGraph state schema · Policy P-01 to P-08</div>
        </div>

        <div class="timeline-col">
          <div class="timeline-phase-badge">06 – 12h · PHASE 02</div>
          <div class="timeline-col-title">Evidence Pipeline</div>
          <div class="timeline-col-desc">FFmpeg ~1fps extractor · Vision prompt schemas · Seller Console UI mock</div>
        </div>

        <div class="timeline-col">
          <div class="timeline-phase-badge">12 – 18h · PHASE 03</div>
          <div class="timeline-col-title">Integration</div>
          <div class="timeline-col-desc">Case C pause/resume loop · 3 core cases (A–C) + Case D sequence test · Critic review</div>
        </div>

        <div class="timeline-col">
          <div class="timeline-phase-badge">18 – 24h · PHASE 04</div>
          <div class="timeline-col-title">Validation &amp; Safety</div>
          <div class="timeline-col-desc">Fail-closed authorization tests · Boundary QA · Video demo recording</div>
        </div>
      </div>

      <div class="team-cards-grid">
        <div class="team-card">
          <div class="team-role">PERSON A · BACKEND, POLICY &amp; AUDIT</div>
          <div class="team-name">State Machine &amp; Policy Engine</div>
          <div class="team-stack">Stack: LangGraph · Pydantic · SQLite · SHA256</div>
          <div class="team-deliverables">
            <div class="deliv-item">• Policy P-01 to P-08: Deterministic code rules (window, SKU, tag, refund cap)</div>
            <div class="deliv-item">• Critic Agent: Adversarial check against cited keyframe timestamps</div>
            <div class="deliv-item">• Audit Ledger: Append-only JSON log &amp; cryptographic approval binding</div>
            <div class="deliv-item">• Financial Cap: Server calculation min(₹4,999, remaining, paid)</div>
          </div>
        </div>

        <div class="team-card">
          <div class="team-role">PERSON B · VISION &amp; CONSOLE</div>
          <div class="team-name">Video Pipeline &amp; Seller UI</div>
          <div class="team-stack">Stack: FFmpeg · Hosted vision model (unpinned) · HTML/CSS/SVG</div>
          <div class="team-deliverables">
            <div class="deliv-item">• Keyframe Pipeline: Uniform ~1fps sampling &amp; brightness scoring (Case C sample: 28/255)</div>
            <div class="deliv-item">• Structured Vision: Observation schema with timestamp citation metadata</div>
            <div class="deliv-item">• Seller Console: 1-click decision console with mock evidence pack</div>
            <div class="deliv-item">• Grounding Guard: Enforces unverified barcode vs color distinction</div>
          </div>
        </div>

        <div class="team-card">
          <div class="team-role">PERSON C · INTEGRATION &amp; QA</div>
          <div class="team-name">Scenarios, Lifecycle &amp; QA</div>
          <div class="team-stack">Stack: Pytest · Mock Fixtures · Automated Smoke QA</div>
          <div class="team-deliverables">
            <div class="deliv-item">• Benchmark Cases: Staged data for Cases A–C + Case D sequence test</div>
            <div class="deliv-item">• Case C Lifecycle: Re-film loop in WAITING_FOR_EVIDENCE (1 retry)</div>
            <div class="deliv-item">• Fail-Closed Testing: Verifies zero automated refunds &amp; approval gates</div>
            <div class="deliv-item">• Automated QA: 10-test smoke suite, end-to-end event bus &amp; demo recording</div>
          </div>
        </div>
      </div>

      <div class="scope-discipline-band">
        <div class="scope-col">
          <div class="scope-tag gold">MUST DELIVER (CORE PROTOTYPE)</div>
          <div class="scope-text">Mock APIs · Policy engine · Cases A–C + Case D sequence test · Approval binding · Seller gate · Tiny order route</div>
        </div>

        <div class="scope-col">
          <div class="scope-tag coral">CUT FIRST IF BEHIND</div>
          <div class="scope-text">Advanced video forensics (Case D stretch) · WhatsApp bot · Exchanges · Multi-seller auth · Audio analysis · Public cloud deployment</div>
        </div>

        <div class="scope-col">
          <div class="scope-tag teal">FINANCIAL CEILING FORMULA</div>
          <div class="scope-text mono">0 &lt; amt &lt;= min({meta['refund_guardrail']['ceiling']}, rem_ref, paid)</div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div>RETURNLENS V7.1 · AGENTX HACKATHON 2026 PS-04 · TEAM ROOKIE (3 MEMBERS)</div>
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
  const dots = document.querySelectorAll('.dot');
  const numDisplay = document.getElementById('slide-num');
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
    html_target = deliverables_dir / "ReturnLens_v7_1.html"
    root_target = base_dir / "ReturnLens_v7_1.html"
    index_target = base_dir / "index.html"

    with open(html_target, "w", encoding="utf-8", newline="\n") as f:
        f.write(html_content)
    shutil.copy2(html_target, root_target)
    shutil.copy2(html_target, index_target)
    print(f"Compiled ReturnLens_v7_1.html successfully: {html_target} ({os.path.getsize(html_target)} bytes)")

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

    pdf_deliverable = deliverables_dir / "ReturnLens_v7_1.pdf"
    pdf_root = base_dir / "ReturnLens_v7_1.pdf"

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

                preview_deliv = deliverables_dir / "ReturnLens_v7_1_preview.png"
                preview_root = base_dir / "ReturnLens_v7_1_preview.png"
                grid.save(preview_deliv, quality=95)
                shutil.copy2(preview_deliv, preview_root)
                print(f"Exported preview contact sheet: {preview_deliv} ({grid.size})")

if __name__ == "__main__":
    generate_v7_1()
