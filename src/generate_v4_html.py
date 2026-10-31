import os

html_code = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ReturnLens — Evidence-Checked Returns Agent (AgentX PS-04)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  :root {
    --bg-paper: #F5F3EF;
    --bg-dark: #0D1814;
    --ink: #172621;
    --text-muted: #55605B;
    --text-subtle: #8A9590;
    --border-light: #D2CEC4;
    --border-dark: #233830;
    --teal: #006B55;
    --teal-light: #E1F2EC;
    --amber: #D88C31;
    --amber-light: #FEF3C7;
    --white: #FFFFFF;
    --panel-bg: #FAF9F7;
    --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    --font-mono: 'IBM Plex Mono', SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', monospace;
  }

  html, body {
    width: 100%;
    height: 100%;
    overflow: hidden;
    background-color: #1A1F1D;
    font-family: var(--font-sans);
    color: var(--ink);
  }

  /* TOP PROGRESS BAR */
  #top-progress-bar {
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    background: var(--teal);
    width: 16.666%;
    z-index: 1000;
    transition: width 0.25s ease;
  }

  /* VIEWPORT & PROPORTIONAL SCALING */
  #viewport {
    width: 100vw;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
  }

  #presentation {
    width: 1280px;
    height: 720px;
    position: relative;
    transform-origin: center center;
    box-shadow: 0 24px 64px rgba(0, 0, 0, 0.45);
    background: var(--bg-paper);
  }

  /* BASE SLIDE (1280x720) */
  .slide {
    width: 1280px;
    height: 720px;
    position: absolute;
    top: 0;
    left: 0;
    padding: 44px 56px 36px 56px;
    display: none;
    flex-direction: column;
    justify-content: space-between;
    background-color: var(--bg-paper);
    overflow: hidden;
  }

  .slide.active {
    display: flex;
  }

  .slide.dark-theme {
    background-color: var(--bg-dark);
    color: var(--bg-paper);
  }

  /* TYPOGRAPHY */
  .mono {
    font-family: var(--font-mono);
  }

  .kicker {
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--teal);
    margin-bottom: 6px;
    display: inline-block;
  }

  .dark-theme .kicker {
    color: #00A382;
  }

  .slide-title {
    font-size: 40px;
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.8px;
    color: var(--ink);
    margin-bottom: 6px;
  }

  .dark-theme .slide-title {
    color: var(--bg-paper);
  }

  .slide-subtitle {
    font-size: 18px;
    line-height: 1.35;
    color: var(--text-muted);
    font-weight: 400;
  }

  .dark-theme .slide-subtitle {
    color: #A3B8B0;
  }

  /* EDITORIAL FOOTER */
  .slide-footer {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid var(--border-light);
    padding-top: 12px;
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--text-subtle);
  }

  .dark-theme .slide-footer {
    border-top-color: var(--border-dark);
    color: #6C8279;
  }

  /* =========================================================================
     SLIDE 1 — HERO
     ========================================================================= */
  .hero-container {
    display: flex;
    gap: 36px;
    height: 480px;
    align-items: stretch;
  }

  .hero-left {
    width: 38%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .hero-headline-group h1 {
    font-size: 44px;
    font-weight: 900;
    line-height: 1.05;
    letter-spacing: -1.2px;
    color: var(--ink);
    margin: 4px 0 10px 0;
  }

  .hero-value-prop {
    font-size: 18px;
    font-weight: 600;
    line-height: 1.35;
    color: var(--teal);
    margin-bottom: 16px;
  }

  .hero-facts-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 16px;
  }

  .hero-fact-row {
    font-size: 14px;
    line-height: 1.4;
    color: var(--text-muted);
  }

  .hero-fact-row strong {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--ink);
    letter-spacing: 0.5px;
    text-transform: uppercase;
    display: inline-block;
    width: 140px;
  }

  .hero-meta-card {
    background: #EBE8E1;
    border-left: 3px solid var(--teal);
    padding: 10px 14px;
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--ink);
    line-height: 1.45;
  }

  /* SELLER CONSOLE MOCK (Hero Right) */
  .hero-right {
    width: 62%;
    display: flex;
    flex-direction: column;
  }

  .console-window {
    background: var(--white);
    border: 1px solid var(--border-light);
    border-radius: 12px;
    box-shadow: 0 16px 36px rgba(23, 38, 33, 0.08);
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
  }

  .console-header-bar {
    background: var(--ink);
    color: var(--bg-paper);
    height: 38px;
    padding: 0 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.5px;
  }

  .console-split {
    display: flex;
    flex: 1;
    overflow: hidden;
  }

  /* Video area on Left of Console */
  .console-video-panel {
    width: 54%;
    background: #111815;
    padding: 16px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    border-right: 1px solid var(--border-light);
  }

  .video-top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: var(--font-mono);
    font-size: 11px;
    color: #F5F3EF;
  }

  .rec-indicator {
    color: #EF4444;
    font-weight: 700;
  }

  .video-frame-display {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: #17221E;
    border: 1px dashed #344C43;
    margin: 12px 0;
    padding: 16px;
    text-align: center;
    position: relative;
  }

  .css-headset-box {
    width: 140px;
    height: 120px;
    border: 2px solid var(--amber);
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: rgba(216, 140, 49, 0.08);
  }

  .css-headset-silhouette {
    width: 80px;
    height: 70px;
    border: 6px solid #283631;
    border-bottom: none;
    border-radius: 40px 40px 0 0;
    position: relative;
  }

  .css-headset-cup {
    position: absolute;
    bottom: -10px;
    width: 20px;
    height: 32px;
    background: #0A0D0C;
    border: 1px solid #3E524A;
  }

  .css-headset-cup.left { left: -12px; }
  .css-headset-cup.right { right: -12px; }

  .bbox-label {
    position: absolute;
    top: -12px;
    left: 4px;
    background: var(--amber);
    color: #FFFFFF;
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 700;
    padding: 2px 6px;
  }

  .video-bottom-caption {
    font-family: var(--font-mono);
    font-size: 10px;
    color: #7D948B;
    text-align: center;
  }

  /* Side panel on Right of Console */
  .console-data-panel {
    width: 46%;
    background: var(--panel-bg);
    padding: 18px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .data-field-group {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .df-item .df-label {
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 700;
    color: var(--text-subtle);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .df-item .df-val {
    font-size: 13px;
    font-weight: 700;
    color: var(--ink);
    line-height: 1.3;
  }

  .df-item .df-sub {
    font-size: 11px;
    color: var(--text-muted);
  }

  .status-badge-amber {
    background: var(--amber-light);
    color: #92400E;
    border: 1px solid var(--amber);
    padding: 6px;
    text-align: center;
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
  }

  .console-actions-row {
    display: flex;
    gap: 8px;
  }

  .btn-approve {
    flex: 1;
    background: var(--teal);
    color: #FFFFFF;
    font-family: var(--font-sans);
    font-size: 12px;
    font-weight: 700;
    text-align: center;
    padding: 8px;
    border: none;
    cursor: default;
  }

  .btn-escalate-outline {
    flex: 1;
    background: transparent;
    color: var(--amber);
    border: 1px solid var(--amber);
    font-family: var(--font-sans);
    font-size: 12px;
    font-weight: 700;
    text-align: center;
    padding: 8px;
    cursor: default;
  }

  /* STATS STRIP AT BOTTOM OF SLIDE 1 */
  .hero-stats-strip {
    display: flex;
    border-top: 1px solid var(--border-light);
    border-bottom: 1px solid var(--border-light);
    background: var(--white);
    padding: 10px 0;
  }

  .stat-col {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-right: 1px solid var(--border-light);
  }

  .stat-col:last-child {
    border-right: none;
  }

  .stat-num {
    font-size: 20px;
    font-weight: 800;
    color: var(--teal);
    line-height: 1.1;
  }

  .stat-lbl {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--text-subtle);
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 2px;
  }

  /* =========================================================================
     SLIDE 2 — PROBLEM AS A CONVERGENCE DIAGRAM
     ========================================================================= */
  .problem-stage {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 520px;
  }

  .convergence-diagram {
    display: grid;
    grid-template-columns: 310px 1fr 310px;
    grid-template-rows: 1fr 1fr;
    gap: 16px 20px;
    height: 330px;
    align-items: center;
    position: relative;
    margin-top: 8px;
  }

  .source-box {
    background: var(--white);
    border: 1px solid var(--border-light);
    padding: 14px 16px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .source-box .src-num {
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 700;
    color: var(--teal);
    letter-spacing: 1px;
    margin-bottom: 4px;
    text-transform: uppercase;
  }

  .source-box .src-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 2px;
  }

  .source-box .src-sub {
    font-size: 12px;
    color: var(--text-muted);
    line-height: 1.35;
  }

  /* Central Dashed Amber Box */
  .center-gap-card {
    grid-column: 2;
    grid-row: 1 / span 2;
    background: #FFFDF7;
    border: 2px dashed var(--amber);
    padding: 24px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    height: 100%;
    position: relative;
  }

  .gap-tag {
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 800;
    color: var(--amber);
    letter-spacing: 1px;
    margin-bottom: 8px;
  }

  .gap-header {
    font-size: 20px;
    font-weight: 800;
    color: var(--ink);
    margin-bottom: 8px;
    letter-spacing: -0.3px;
  }

  .gap-prompt {
    font-size: 15px;
    font-style: italic;
    color: var(--text-muted);
    line-height: 1.4;
  }

  /* Bottom 3-Column Band */
  .problem-bottom-band {
    display: flex;
    gap: 20px;
    border-top: 1px solid var(--border-light);
    padding-top: 14px;
    background: transparent;
  }

  .band-col {
    flex: 1;
    font-size: 13px;
    line-height: 1.45;
    color: var(--text-muted);
  }

  .band-col strong {
    color: var(--ink);
    display: block;
    margin-bottom: 3px;
    font-size: 13px;
  }

  .band-col.fraud-col {
    background: #EBE8E1;
    padding: 10px 14px;
    border-left: 3px solid var(--amber);
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--ink);
    line-height: 1.4;
  }

  /* =========================================================================
     SLIDE 3 — STAR DEMO (EVIDENCE COMPARISON)
     ========================================================================= */
  .demo-stage {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 520px;
  }

  .comparison-row {
    display: flex;
    align-items: center;
    gap: 20px;
    height: 380px;
  }

  .cmp-card {
    flex: 1;
    height: 100%;
    background: var(--white);
    border: 1px solid var(--border-light);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .cmp-card.video-side {
    border: 2px solid var(--amber);
    background: #FFFDF7;
  }

  .cmp-card-header {
    background: var(--bg-paper);
    padding: 10px 14px;
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 700;
    color: var(--ink);
    border-bottom: 1px solid var(--border-light);
    display: flex;
    justify-content: space-between;
  }

  .cmp-card.video-side .cmp-card-header {
    background: var(--amber-light);
    border-bottom-color: var(--amber);
    color: #92400E;
  }

  .cmp-card-visual {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 16px;
    position: relative;
    background: #FAF9F7;
  }

  .cmp-card.video-side .cmp-card-visual {
    background: #111815;
  }

  /* Product Spec Diagram (Store Truth) */
  .store-truth-badge {
    border: 2px solid var(--teal);
    padding: 20px;
    text-align: center;
    width: 220px;
    background: var(--white);
  }

  .st-sku {
    font-family: var(--font-mono);
    font-size: 16px;
    font-weight: 800;
    color: var(--teal);
    margin-bottom: 4px;
  }

  .st-color {
    font-size: 16px;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 6px;
  }

  .st-meta {
    font-size: 12px;
    color: var(--text-muted);
    line-height: 1.4;
  }

  /* Video Evidence Frame (CSS Mock) */
  .video-frame-wireframe {
    width: 240px;
    height: 160px;
    border: 2px solid var(--amber);
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: #17221E;
  }

  .vf-timecode {
    position: absolute;
    top: 8px;
    left: 8px;
    font-family: var(--font-mono);
    font-size: 10px;
    color: #F5F3EF;
    background: rgba(0,0,0,0.6);
    padding: 2px 6px;
  }

  .vf-sku-badge {
    position: absolute;
    bottom: 8px;
    right: 8px;
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 700;
    color: var(--amber);
    background: rgba(0,0,0,0.7);
    padding: 2px 6px;
  }

  .cmp-card-footer {
    padding: 12px 14px;
    background: var(--white);
    border-top: 1px solid var(--border-light);
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--ink);
    line-height: 1.4;
  }

  .cmp-vs-node {
    width: 48px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-family: var(--font-mono);
    font-size: 18px;
    font-weight: 800;
    color: var(--amber);
  }

  .cmp-vs-arrow {
    font-size: 24px;
    margin-top: 4px;
    color: var(--text-subtle);
  }

  /* Bottom Decision Bar */
  .decision-gate-bar {
    background: var(--amber-light);
    border: 1px solid var(--amber);
    padding: 14px 20px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .dgb-headline {
    font-family: var(--font-mono);
    font-size: 14px;
    font-weight: 800;
    color: #92400E;
    letter-spacing: 0.5px;
  }

  .dgb-options {
    font-size: 13px;
    color: var(--ink);
  }

  .dgb-safety {
    font-size: 13px;
    font-weight: 800;
    color: #92400E;
  }

  /* =========================================================================
     SLIDE 4 — ARCHITECTURE (DARK THEME)
     ========================================================================= */
  .arch-stage {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 520px;
  }

  .pipeline-strip {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #13221C;
    border: 1px solid var(--border-dark);
    padding: 12px 14px;
  }

  .pipe-node {
    flex: 1;
    background: #1A2C25;
    border: 1px solid var(--border-dark);
    padding: 10px 8px;
    text-align: center;
  }

  .pipe-node .pn-role {
    font-family: var(--font-mono);
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 4px;
    display: block;
  }

  .pipe-node.role-model { border-top: 3px solid #00D1A7; }
  .pipe-node.role-model .pn-role { color: #00D1A7; }

  .pipe-node.role-code { border-top: 3px solid #F5F3EF; }
  .pipe-node.role-code .pn-role { color: #F5F3EF; }

  .pipe-node.role-human { border-top: 3px solid #FBBF24; }
  .pipe-node.role-human .pn-role { color: #FBBF24; }

  .pipe-node .pn-name {
    font-size: 12px;
    font-weight: 700;
    color: #F5F3EF;
  }

  .pipe-arrow {
    color: #4D665D;
    font-family: var(--font-mono);
    font-size: 14px;
  }

  .arch-columns-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    margin: 8px 0;
  }

  .arch-col-box {
    background: #13221C;
    border: 1px solid var(--border-dark);
    padding: 16px 20px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .arch-spec-item {
    font-size: 13px;
    line-height: 1.45;
    color: #A3B8B0;
  }

  .arch-spec-item strong {
    font-family: var(--font-mono);
    font-size: 11px;
    color: #F5F3EF;
    text-transform: uppercase;
    display: inline-block;
    width: 120px;
  }

  .decision-strip-full {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
  }

  .ds-segment {
    background: #172A22;
    border: 1px solid var(--border-dark);
    padding: 10px 12px;
    text-align: center;
  }

  .ds-cond {
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 700;
    color: #6C8279;
    text-transform: uppercase;
    margin-bottom: 2px;
  }

  .ds-act {
    font-size: 12px;
    font-weight: 700;
    color: #F5F3EF;
  }

  .ds-segment.warn { border-top: 2px solid #F87171; }
  .ds-segment.warn .ds-act { color: #FCA5A5; }

  .ds-segment.retry { border-top: 2px solid #60A5FA; }
  .ds-segment.retry .ds-act { color: #93C5FD; }

  .ds-segment.pass { border-top: 2px solid #34D399; }
  .ds-segment.pass .ds-act { color: #6EE7B7; }

  /* =========================================================================
     SLIDE 5 — EVIDENCE CASES
     ========================================================================= */
  .evidence-stage {
    display: flex;
    gap: 24px;
    height: 480px;
    align-items: stretch;
  }

  .case-b-table-card {
    width: 52%;
    background: var(--white);
    border: 1px solid var(--border-light);
    display: flex;
    flex-direction: column;
  }

  .cbt-header {
    background: var(--bg-paper);
    padding: 10px 16px;
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 800;
    color: var(--ink);
    border-bottom: 1px solid var(--border-light);
  }

  .cbt-table {
    width: 100%;
    border-collapse: collapse;
    flex: 1;
  }

  .cbt-table td {
    padding: 12px 16px;
    border-bottom: 1px solid var(--border-light);
    font-size: 13px;
    line-height: 1.4;
  }

  .cbt-table tr:last-child td {
    border-bottom: none;
  }

  .cbt-table td.col-lbl {
    width: 130px;
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 700;
    color: var(--text-subtle);
    text-transform: uppercase;
    background: #FAF9F7;
  }

  .cbt-table td.col-val {
    color: var(--ink);
  }

  .escalate-badge {
    background: var(--amber-light);
    color: #92400E;
    font-family: var(--font-mono);
    font-weight: 800;
    padding: 2px 8px;
    border: 1px solid var(--amber);
    display: inline-block;
  }

  .stacked-cases-col {
    width: 48%;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .compact-case-card {
    flex: 1;
    background: var(--white);
    border: 1px solid var(--border-light);
    padding: 14px 16px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .ccc-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
  }

  .case-id-tag {
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 700;
    color: var(--ink);
  }

  .badge-approved {
    background: var(--teal-light);
    color: var(--teal);
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 700;
    padding: 3px 8px;
  }

  .badge-unclear {
    background: #EFF6FF;
    color: #1E40AF;
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 700;
    padding: 3px 8px;
  }

  .badge-continuity {
    background: #F3F4F6;
    color: #374151;
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 700;
    padding: 3px 8px;
  }

  .ccc-evidence {
    font-size: 13px;
    font-weight: 600;
    color: var(--ink);
    margin-bottom: 2px;
  }

  .ccc-result {
    font-size: 12px;
    color: var(--text-muted);
    line-height: 1.35;
  }

  .evidence-disclaimer {
    font-family: var(--font-mono);
    font-size: 10.5px;
    color: var(--text-subtle);
    margin-top: 6px;
  }

  /* =========================================================================
     SLIDE 6 — EXECUTION & 24H SPRINT
     ========================================================================= */
  .exec-stage {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 520px;
  }

  .timeline-strip {
    display: flex;
    border-top: 3px solid var(--teal);
    background: var(--white);
    border: 1px solid var(--border-light);
    border-top: 3px solid var(--teal);
    padding: 12px 0;
  }

  .t-segment {
    flex: 1;
    padding: 0 16px;
    border-right: 1px solid var(--border-light);
  }

  .t-segment:last-child {
    border-right: none;
  }

  .t-seg-hours {
    font-family: var(--font-mono);
    font-size: 13px;
    font-weight: 800;
    color: var(--teal);
    margin-bottom: 2px;
  }

  .t-seg-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 2px;
  }

  .t-seg-desc {
    font-size: 11px;
    color: var(--text-muted);
  }

  .people-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin: 8px 0;
  }

  .person-card {
    background: var(--white);
    border: 1px solid var(--border-light);
    padding: 14px 16px;
  }

  .pc-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
  }

  .pc-role-mono {
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 800;
    color: var(--teal);
  }

  .pc-duties {
    font-size: 12.5px;
    color: var(--text-muted);
    line-height: 1.45;
  }

  .exec-bottom-row {
    display: grid;
    grid-template-columns: 1fr 1fr 1.3fr;
    gap: 16px;
    align-items: stretch;
  }

  .scope-box {
    background: var(--white);
    border: 1px solid var(--border-light);
    padding: 12px 14px;
    font-size: 12px;
    line-height: 1.4;
    color: var(--text-muted);
  }

  .scope-box strong {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    display: block;
    margin-bottom: 4px;
  }

  .scope-box.cut strong { color: var(--text-subtle); }
  .scope-box.keep strong { color: var(--teal); }

  .refund-cap-card {
    background: #172621;
    color: #F5F3EF;
    padding: 12px 14px;
    font-family: var(--font-mono);
    font-size: 11px;
    line-height: 1.4;
  }

  .rcc-header {
    font-size: 10px;
    color: #00D1A7;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
    text-transform: uppercase;
  }

  .rcc-code {
    background: #0E1815;
    padding: 6px 8px;
    border-left: 2px solid #00D1A7;
    margin: 4px 0;
    color: #A3E6D8;
    font-size: 11px;
  }

  .exec-guarantee-line {
    font-size: 11.5px;
    color: var(--text-subtle);
    margin-top: 6px;
    line-height: 1.35;
  }

  /* =========================================================================
     NAVIGATION CHROME & CONTROLS
     ========================================================================= */
  #nav-controls {
    position: fixed;
    bottom: 20px;
    right: 24px;
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(23, 38, 33, 0.85);
    backdrop-filter: blur(8px);
    padding: 6px 12px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    z-index: 999;
  }

  .nav-btn {
    background: transparent;
    color: #F5F3EF;
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 6px 12px;
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .nav-btn:hover, .nav-btn:focus-visible {
    background: var(--teal);
    border-color: var(--teal);
    outline: none;
  }

  #slide-counter-disp {
    font-family: var(--font-mono);
    font-size: 11px;
    color: #F5F3EF;
    padding: 0 8px;
  }

  /* SPEAKER NOTES DRAWER */
  #notes-drawer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #172621;
    color: #F5F3EF;
    border-top: 2px solid var(--teal);
    padding: 16px 32px;
    font-size: 13px;
    line-height: 1.5;
    z-index: 1001;
    transform: translateY(100%);
    transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    box-shadow: 0 -12px 32px rgba(0,0,0,0.5);
  }

  #notes-drawer.open {
    transform: translateY(0);
  }

  .notes-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
    font-family: var(--font-mono);
    font-size: 11px;
    color: #00D1A7;
    letter-spacing: 1px;
  }

  .notes-close-btn {
    background: transparent;
    border: none;
    color: #F5F3EF;
    cursor: pointer;
    font-family: var(--font-mono);
    font-size: 12px;
  }

  /* OVERVIEW GRID MODAL */
  #overview-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(13, 24, 20, 0.95);
    backdrop-filter: blur(12px);
    z-index: 2000;
    display: none;
    flex-direction: column;
    padding: 32px;
  }

  #overview-modal.open {
    display: flex;
  }

  .overview-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    color: #F5F3EF;
  }

  .overview-header h2 {
    font-size: 20px;
    font-weight: 800;
    font-family: var(--font-mono);
    letter-spacing: 1px;
  }

  .overview-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(2, 1fr);
    gap: 20px;
    flex: 1;
  }

  .overview-thumb {
    background: var(--bg-paper);
    border: 2px solid rgba(255, 255, 255, 0.15);
    padding: 16px;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.15s ease;
  }

  .overview-thumb:hover, .overview-thumb:focus-visible {
    border-color: var(--teal);
    transform: translateY(-2px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.5);
    outline: none;
  }

  .overview-thumb.dark-thumb {
    background: var(--bg-dark);
    color: #F5F3EF;
  }

  .ot-num {
    font-family: var(--font-mono);
    font-size: 12px;
    font-weight: 800;
    color: var(--teal);
    margin-bottom: 4px;
  }

  .overview-thumb.dark-thumb .ot-num {
    color: #00D1A7;
  }

  .ot-title {
    font-size: 14px;
    font-weight: 700;
    line-height: 1.25;
  }

  /* =========================================================================
     PRINT CSS FOR PIXEL-PERFECT PDF GENERATION
     ========================================================================= */
  @media print {
    @page {
      size: 1280px 720px;
      margin: 0;
    }

    html, body {
      width: 1280px !important;
      height: auto !important;
      background: transparent !important;
      overflow: visible !important;
      padding: 0 !important;
      margin: 0 !important;
    }

    #viewport {
      width: auto !important;
      height: auto !important;
      display: block !important;
      background: transparent !important;
      overflow: visible !important;
      position: static !important;
    }

    #presentation {
      width: auto !important;
      height: auto !important;
      transform: none !important;
      box-shadow: none !important;
      position: static !important;
    }

    .slide {
      width: 1280px !important;
      height: 720px !important;
      position: relative !important;
      display: flex !important;
      page-break-after: always !important;
      break-after: page !important;
      box-shadow: none !important;
      overflow: hidden !important;
      margin: 0 !important;
      top: auto !important;
      left: auto !important;
    }

    #top-progress-bar, #nav-controls, #notes-drawer, #overview-modal {
      display: none !important;
    }
  }
</style>
</head>
<body>

<div id="top-progress-bar"></div>

<div id="viewport">
  <div id="presentation">

    <!-- =====================================================================
         SLIDE 1 — HERO
         ===================================================================== -->
    <section class="slide active" id="slide-1" data-index="1">
      <div class="kicker">PS-04 · TEAM ROOKIE · AGENTX HACKATHON 2026</div>

      <div class="hero-container">
        <!-- Left Column (38%) -->
        <div class="hero-left">
          <div class="hero-headline-group">
            <h1>ReturnLens</h1>
            <div class="hero-value-prop">An evidence-checked returns agent for small direct-to-consumer sellers.</div>
          </div>

          <div class="hero-facts-list">
            <div class="hero-fact-row">
              <strong>USER</strong>
              Solo D2C merchant managing orders and returns alone.
            </div>
            <div class="hero-fact-row">
              <strong>SCOPE IN 24H</strong>
              Return triage only, mock store data + 1 order-status route.
            </div>
            <div class="hero-fact-row">
              <strong>WHAT IT IS NOT</strong>
              Not another chatbot; not an autonomous refund gate.
            </div>
          </div>

          <div class="hero-meta-card">
            Team Rookie · 3 members · PS-04 submission<br>
            <span style="color: var(--text-muted); font-size: 10px;">Deterministic Policy Engine · Grounded Video Proof · 24h Build</span>
          </div>
        </div>

        <!-- Right Column (62%): Seller Review Console Mock -->
        <div class="hero-right">
          <div class="console-window">
            <div class="console-header-bar">
              <span>SELLER REVIEW CONSOLE · CASE B</span>
              <span>ORDER #ORD-9021</span>
            </div>

            <div class="console-split">
              <!-- Video Panel -->
              <div class="console-video-panel">
                <div class="video-top-bar">
                  <span class="rec-indicator">● REC 00:07 / 00:32</span>
                  <span>720p HD</span>
                </div>

                <div class="video-frame-display">
                  <div class="css-headset-box">
                    <span class="bbox-label">FRAME 00:07</span>
                    <div class="css-headset-silhouette">
                      <div class="css-headset-cup left"></div>
                      <div class="css-headset-cup right"></div>
                    </div>
                  </div>
                  <div style="margin-top: 10px; font-family: var(--font-mono); font-size: 11px; color: #F5F3EF; font-weight: 700;">
                    Observed: HEAD-BLK-09, Black
                  </div>
                </div>

                <div class="video-bottom-caption">
                  Mock evidence pack · Frame 00:07
                </div>
              </div>

              <!-- Data Panel -->
              <div class="console-data-panel">
                <div class="data-field-group">
                  <div class="df-item">
                    <div class="df-label">Order Manifest</div>
                    <div class="df-val">HEAD-WHT-02, White</div>
                    <div class="df-sub">₹1,499 · Delivered Day 4 (within 7d window)</div>
                  </div>

                  <div class="df-item">
                    <div class="df-label">Video Observation</div>
                    <div class="df-val">HEAD-BLK-09, Black</div>
                    <div class="df-sub">Timestamp 00:07 · Server hash verified</div>
                  </div>

                  <div class="df-item">
                    <div class="df-label">Policy Evaluation</div>
                    <div class="df-val" style="color: #92400E;">P-03 SKU mismatch, FAIL</div>
                    <div class="df-sub">Critic veto: Contradiction flagged</div>
                  </div>
                </div>

                <div>
                  <div class="status-badge-amber">NEEDS SELLER REVIEW</div>
                  <div class="console-actions-row">
                    <button class="btn-approve">Approve (Draft)</button>
                    <button class="btn-escalate-outline">Escalate</button>
                  </div>
                  <div style="font-family: var(--font-mono); font-size: 9.5px; color: var(--text-subtle); text-align: center; margin-top: 6px;">
                    Pending seller authorization · No auto-refund
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Strip -->
      <div class="hero-stats-strip">
        <div class="stat-col">
          <div class="stat-num">3</div>
          <div class="stat-lbl">Members</div>
        </div>
        <div class="stat-col">
          <div class="stat-num">P-01 to P-08</div>
          <div class="stat-lbl">Policy Engine</div>
        </div>
        <div class="stat-col">
          <div class="stat-num">4</div>
          <div class="stat-lbl">Demo Cases</div>
        </div>
        <div class="stat-col">
          <div class="stat-num">1-Click</div>
          <div class="stat-lbl">Seller Approval</div>
        </div>
      </div>

      <div class="slide-footer">
        <span>ReturnLens · PS-04</span>
        <span>1 / 6</span>
      </div>
    </section>

    <!-- =====================================================================
         SLIDE 2 — PROBLEM AS A CONVERGENCE DIAGRAM
         ========================================================================= -->
    <section class="slide" id="slide-2" data-index="2">
      <div class="kicker">Problem Statement · Solo Seller Bottleneck</div>
      <h2 class="slide-title">The return decision is made from memory, before the evidence is checked.</h2>
      <p class="slide-subtitle">Today the seller opens many tabs, then decides alone.</p>

      <div class="problem-stage">
        <!-- Convergence Diagram -->
        <div class="convergence-diagram">
          <!-- Top Left Node -->
          <div class="source-box">
            <span class="src-num">01 Buyer Chat</span>
            <div class="src-title">“Received damaged item”</div>
            <div class="src-sub">Unverified text in support inbox.</div>
          </div>

          <!-- Top Right Node -->
          <div class="source-box">
            <span class="src-num">02 Order Record</span>
            <div class="src-title">HEAD-WHT-02 · ₹1,499</div>
            <div class="src-sub">Database manifest &amp; SKU truth.</div>
          </div>

          <!-- Centre Gap Card -->
          <div class="center-gap-card">
            <div class="gap-tag">⚠ CRITICAL INFORMATION GAP</div>
            <div class="gap-header">NO SHARED EVIDENCE RECORD</div>
            <div class="gap-prompt">“Approve, deny, or ask for more evidence?”</div>
          </div>

          <!-- Bottom Left Node -->
          <div class="source-box">
            <span class="src-num">03 Delivery Tracking</span>
            <div class="src-title">Delivered 4 days ago</div>
            <div class="src-sub">Carrier tracking portal status.</div>
          </div>

          <!-- Bottom Right Node -->
          <div class="source-box">
            <span class="src-num">04 Return Policy</span>
            <div class="src-title">7-day window, intact tag</div>
            <div class="src-sub">Store PDF terms &amp; conditions.</div>
          </div>
        </div>

        <!-- Bottom 3-Column Band -->
        <div class="problem-bottom-band">
          <div class="band-col">
            <strong>A wrong decision costs both ways</strong>
            A wrong refund loses money and stock, an unfair denial loses a repeat customer.
          </div>
          <div class="band-col">
            <strong>The gap is not a missing portal</strong>
            It is that no single record ties order, video frame, policy clause, and decision together.
          </div>
          <div class="band-col fraud-col">
            Fraud estimates differ by definition:<br>
            <strong>9%</strong> (NRF 2025, fraud only) vs <strong>15.14%</strong> (Appriss/Deloitte 2024, fraud + abuse).
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <span>ReturnLens · PS-04</span>
        <span>2 / 6</span>
      </div>
    </section>

    <!-- =====================================================================
         SLIDE 3 — STAR DEMO (EVIDENCE COMPARISON)
         ========================================================================= -->
    <section class="slide" id="slide-3" data-index="3">
      <div class="kicker">Core Demonstration · Audit Proof</div>
      <h2 class="slide-title">One frame changes the verdict.</h2>
      <p class="slide-subtitle">ReturnLens surfaces the contradiction instead of auto-denying.</p>

      <div class="demo-stage">
        <!-- Comparison Row -->
        <div class="comparison-row">
          <!-- Left: Order Truth -->
          <div class="cmp-card">
            <div class="cmp-card-header">
              <span>ORDER TRUTH</span>
              <span>SHOPIFY MANIFEST</span>
            </div>
            <div class="cmp-card-visual">
              <div class="store-truth-badge">
                <div class="st-sku">HEAD-WHT-02</div>
                <div class="st-color">Matte White</div>
                <div class="st-meta">₹1,499 · Delivered 4 days ago<br>Original retail tag present</div>
              </div>
            </div>
            <div class="cmp-card-footer">
              Order record specifies White Wireless Over-Ear headset.
            </div>
          </div>

          <!-- Centre VS Node -->
          <div class="cmp-vs-node">
            <span>VS</span>
            <span class="cmp-vs-arrow">→</span>
          </div>

          <!-- Right: Customer Video -->
          <div class="cmp-card video-side">
            <div class="cmp-card-header">
              <span>CUSTOMER VIDEO · FRAME 00:07</span>
              <span>UNBOXING TAKE</span>
            </div>
            <div class="cmp-card-visual">
              <div class="video-frame-wireframe">
                <span class="vf-timecode">● 00:07 / 00:32</span>
                <div class="css-headset-box" style="width: 120px; height: 100px; border-color: var(--amber);">
                  <div class="css-headset-silhouette" style="border-color: #384C44; width: 64px; height: 56px;">
                    <div class="css-headset-cup left" style="background: #000;"></div>
                    <div class="css-headset-cup right" style="background: #000;"></div>
                  </div>
                </div>
                <span class="vf-sku-badge">HEAD-BLK-09 · Black</span>
              </div>
            </div>
            <div class="cmp-card-footer">
              <span style="font-weight: 700; color: #92400E;">Observed: HEAD-BLK-09, Midnight Black</span><br>
              <span style="color: var(--text-subtle);">Mock evidence pack</span>
            </div>
          </div>
        </div>

        <!-- Full-Width Decision Gate Bar -->
        <div class="decision-gate-bar">
          <div class="dgb-headline">P-03 SKU mismatch, FAIL → NEEDS SELLER REVIEW</div>
          <div class="dgb-options">
            <strong>Seller options:</strong> Accept as mis-shipment / Ask for outside-box label / Hold for inspection
          </div>
          <div class="dgb-safety">
            No label, no refund draft, no denial.
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <span>ReturnLens · PS-04</span>
        <span>3 / 6</span>
      </div>
    </section>

    <!-- =====================================================================
         SLIDE 4 — ARCHITECTURE (DARK THEME)
         ========================================================================= -->
    <section class="slide dark-theme" id="slide-4" data-index="4">
      <div class="kicker">System Architecture · Deterministic Governance</div>
      <h2 class="slide-title">Policy checks and seller approval control actions</h2>
      <p class="slide-subtitle">Deterministic policy in code and human authorization govern every state transition.</p>

      <div class="arch-stage">
        <!-- 6-Step Horizontal Pipeline -->
        <div class="pipeline-strip">
          <div class="pipe-node role-model">
            <span class="pn-role">MODEL</span>
            <div class="pn-name">Planner</div>
          </div>
          <span class="pipe-arrow">→</span>
          <div class="pipe-node role-code">
            <span class="pn-role">CODE</span>
            <div class="pn-name">Tools</div>
          </div>
          <span class="pipe-arrow">→</span>
          <div class="pipe-node role-code">
            <span class="pn-role">CODE</span>
            <div class="pn-name">Policy Engine</div>
          </div>
          <span class="pipe-arrow">→</span>
          <div class="pipe-node role-model">
            <span class="pn-role">MODEL</span>
            <div class="pn-name">Critic</div>
          </div>
          <span class="pipe-arrow">→</span>
          <div class="pipe-node role-human">
            <span class="pn-role">HUMAN</span>
            <div class="pn-name">Seller Gate</div>
          </div>
          <span class="pipe-arrow">→</span>
          <div class="pipe-node role-code">
            <span class="pn-role">CODE</span>
            <div class="pn-name">Audit Log</div>
          </div>
        </div>

        <!-- Middle 2-Column Grid -->
        <div class="arch-columns-grid">
          <!-- Left Spec Column -->
          <div class="arch-col-box">
            <div class="arch-spec-item">
              <strong>Tools</strong>
              Mock store &amp; shipping APIs + FFmpeg keyframe indexer.
            </div>
            <div class="arch-spec-item">
              <strong>Policy Clauses</strong>
              Deterministic code rules P-01 to P-08, never prompts.
            </div>
            <div class="arch-spec-item">
              <strong>Model Calls</strong>
              Exactly 3 base model calls per case: planner, vision, critic, plus retries.
            </div>
            <div class="arch-spec-item">
              <strong>Frames</strong>
              Server-generated with frame_id, timestamp, video hash, and frame hash. The model may only cite frames it was given.
            </div>
          </div>

          <!-- Right Spec Column -->
          <div class="arch-col-box">
            <div class="arch-spec-item">
              <strong>Critic</strong>
              The critic reviews cited frames and flags unsupported observations.
            </div>
            <div class="arch-spec-item">
              <strong>Fail-Closed</strong>
              Weak evidence escalates; never auto-deny, never auto-refund.
            </div>
            <div class="arch-spec-item">
              <strong>Injection Limit</strong>
              Injection cannot change the law, exceed the server cap, or execute an action alone, but it can change an observation field, so the seller must check the frames in the evidence pack.
            </div>
          </div>
        </div>

        <!-- Full-Width Decision Strip -->
        <div class="decision-strip-full">
          <div class="ds-segment warn">
            <div class="ds-cond">Contradiction</div>
            <div class="ds-act">→ Escalate</div>
          </div>
          <div class="ds-segment warn">
            <div class="ds-cond">Hard Fail</div>
            <div class="ds-act">→ Escalate</div>
          </div>
          <div class="ds-segment retry">
            <div class="ds-cond">Unclear Only</div>
            <div class="ds-act">→ Ask More</div>
          </div>
          <div class="ds-segment pass">
            <div class="ds-cond">All Pass</div>
            <div class="ds-act">→ Approve for Review</div>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <span>ReturnLens · PS-04</span>
        <span>4 / 6</span>
      </div>
    </section>

    <!-- =====================================================================
         SLIDE 5 — EVIDENCE CASES
         ========================================================================= -->
    <section class="slide" id="slide-5" data-index="5">
      <div class="kicker">Demo Scenarios · Grounded Verification</div>
      <h2 class="slide-title">Every decision can be clicked back to a frame, a clause, and a log entry.</h2>
      <p class="slide-subtitle">Four reproducible benchmark cases prove deterministic safety.</p>

      <div class="evidence-stage">
        <!-- Left: Large Case B Table Card -->
        <div class="case-b-table-card">
          <div class="cbt-header">CASE B · AUDIT PROOF (THE CORE BENCHMARK)</div>
          <table class="cbt-table">
            <tr>
              <td class="col-lbl">Order</td>
              <td class="col-val"><strong>HEAD-WHT-02</strong>, White, ₹1,499, delivered, tag present</td>
            </tr>
            <tr>
              <td class="col-lbl">Frame</td>
              <td class="col-val"><strong>Frame 00:07</strong>: <strong>HEAD-BLK-09</strong>, Black</td>
            </tr>
            <tr>
              <td class="col-lbl">Policy</td>
              <td class="col-val"><strong>P-03 SKU mismatch</strong>, <strong>FAIL</strong></td>
            </tr>
            <tr>
              <td class="col-lbl">Result</td>
              <td class="col-val"><span class="escalate-badge">ESCALATE</span> (no label, no refund draft, no denial)</td>
            </tr>
            <tr>
              <td class="col-lbl">Seller Options</td>
              <td class="col-val">Accept as mis-shipment / Ask for outside-box label / Hold for inspection</td>
            </tr>
          </table>
        </div>

        <!-- Right: 3 Stacked Compact Cases -->
        <div class="stacked-cases-col">
          <!-- Case A -->
          <div class="compact-case-card">
            <div class="ccc-top">
              <span class="case-id-tag">CASE A · ORD-1042</span>
              <span class="badge-approved">READY FOR REVIEW</span>
            </div>
            <div class="ccc-evidence">ORD-1042, ₹1,499, SKU matches, tag present, within window.</div>
            <div class="ccc-result">Seller approval creates a mock return label and a refund draft in <strong>pending_return_receipt</strong>, not an executed refund.</div>
          </div>

          <!-- Case C -->
          <div class="compact-case-card">
            <div class="ccc-top">
              <span class="case-id-tag">CASE C · POOR LIGHTING</span>
              <span class="badge-unclear">ASK FOR MORE EVIDENCE</span>
            </div>
            <div class="ccc-evidence">4-second dark video, brightness 28, only 2 usable frames.</div>
            <div class="ccc-result">Case stays open with an exact re-film checklist.</div>
          </div>

          <!-- Case D -->
          <div class="compact-case-card">
            <div class="ccc-top">
              <span class="case-id-tag">CASE D · UNBROKEN TAKE</span>
              <span class="badge-continuity">WHY VIDEO BEATS PHOTOS</span>
            </div>
            <div class="ccc-evidence">One continuous take from opening a sealed parcel to showing the label in one continuous sequence.</div>
            <div class="ccc-result">Prevents photo-swap fraud before mock return label generation.</div>
          </div>
        </div>
      </div>

      <div class="evidence-disclaimer">
        Staged sample videos, mock data, no real customer data. If the model fails or the quota runs out, escalate. Do not approve without evidence.
      </div>

      <div class="slide-footer">
        <span>ReturnLens · PS-04</span>
        <span>5 / 6</span>
      </div>
    </section>

    <!-- =====================================================================
         SLIDE 6 — EXECUTION & 24H SPRINT
         ========================================================================= -->
    <section class="slide" id="slide-6" data-index="6">
      <div class="kicker">Execution Plan · Hackathon Feasibility</div>
      <h2 class="slide-title">Buildable in 24 hours by 3 people, if the scope stays narrow.</h2>
      <p class="slide-subtitle">Project logic is written inside the 24 hours. Before that, only research, design, accounts, and library choice.</p>

      <div class="exec-stage">
        <!-- Top Timeline Strip -->
        <div class="timeline-strip">
          <div class="t-segment">
            <div class="t-seg-hours">0–6h</div>
            <div class="t-seg-title">Skeleton</div>
            <div class="t-seg-desc">Mock store &amp; shipping APIs + agent skeleton.</div>
          </div>
          <div class="t-segment">
            <div class="t-seg-hours">6–12h</div>
            <div class="t-seg-title">Pipeline &amp; Policy</div>
            <div class="t-seg-desc">FFmpeg video indexer + P-01 to P-08 code engine.</div>
          </div>
          <div class="t-segment">
            <div class="t-seg-hours">12–18h</div>
            <div class="t-seg-title">Integration</div>
            <div class="t-seg-desc">4 demo cases + independent critic verification.</div>
          </div>
          <div class="t-segment">
            <div class="t-seg-hours">18–24h</div>
            <div class="t-seg-title">Demo &amp; Polish</div>
            <div class="t-seg-desc">Seller console view, fallback tests, video &amp; README.</div>
          </div>
        </div>

        <!-- Middle 3-Person Grid -->
        <div class="people-grid">
          <div class="person-card">
            <div class="pc-head">
              <span style="font-weight: 800; font-size: 14px;">Person A</span>
              <span class="pc-role-mono">BACKEND</span>
            </div>
            <div class="pc-duties">Backend, agent graph, policy, critic, audit log.</div>
          </div>

          <div class="person-card">
            <div class="pc-head">
              <span style="font-weight: 800; font-size: 14px;">Person B</span>
              <span class="pc-role-mono">VIDEO &amp; UI</span>
            </div>
            <div class="pc-duties">Video pipeline, video indexer, seller console, evidence pack view.</div>
          </div>

          <div class="person-card">
            <div class="pc-head">
              <span style="font-weight: 800; font-size: 14px;">Person C</span>
              <span class="pc-role-mono">INTEGRATION</span>
            </div>
            <div class="pc-duties">Integration, mock data, 4 demo cases, fallback testing, demo video, README.</div>
          </div>
        </div>

        <!-- Bottom 3-Column Scope & Cap -->
        <div class="exec-bottom-row">
          <div class="scope-box cut">
            <strong>Cut First</strong>
            WhatsApp, exchanges, multi-seller, audio, public deployment.
          </div>

          <div class="scope-box keep">
            <strong>Never Cut</strong>
            Policy engine, critic, seller gate, audit log, 4 demo cases.
          </div>

          <div class="refund-cap-card">
            <div class="rcc-header">SERVER-COMPUTED REFUND CAP</div>
            <div class="rcc-code">0 &lt; amount &lt;= min(₹4,999, remaining refundable amount, order paid amount)</div>
            <div style="font-size: 10px; color: #8A9590;">Idempotent single transaction per order.</div>
          </div>
        </div>

        <!-- Final Checklist & Closing Line -->
        <div class="exec-guarantee-line">
          <strong>PS-04 checklist:</strong> mock tool calls, refund-limit guardrails, action log, human confirmation before refund.<br>
          <em>No idea can guarantee top-100 selection. This deck claims a checkable, buildable agent, not a guaranteed result.</em>
        </div>
      </div>

      <div class="slide-footer">
        <span>ReturnLens · PS-04</span>
        <span>6 / 6</span>
      </div>
    </section>

  </div>
</div>

<!-- =========================================================================
     NAVIGATION BAR & ON-SCREEN CONTROLS
     ========================================================================= -->
<div id="nav-controls" class="chrome-ui">
  <button class="nav-btn" id="btn-prev" title="Previous Slide (← / Up)">Prev</button>
  <span id="slide-counter-disp">1 / 6</span>
  <button class="nav-btn" id="btn-next" title="Next Slide (→ / Space / Down)">Next</button>
  <button class="nav-btn" id="btn-overview" title="Toggle 6-Slide Grid (G)">Overview</button>
  <button class="nav-btn" id="btn-notes" title="Toggle Speaker Notes (N)">Notes</button>
  <button class="nav-btn" id="btn-print" title="Print / Export to PDF (P)">Print / PDF</button>
</div>

<!-- =========================================================================
     SPEAKER NOTES DRAWER
     ========================================================================= -->
<div id="notes-drawer" class="chrome-ui">
  <div class="notes-header">
    <span id="notes-slide-tag">SPEAKER NOTES · SLIDE 1</span>
    <button class="notes-close-btn" id="btn-close-notes">[Close ✕]</button>
  </div>
  <div id="notes-body-text">
    ReturnLens is a dedicated returns triage agent for solo direct-to-consumer merchants. In 24 hours we build the return triage flow with mock store and shipping APIs, plus one order status route to satisfy PS-04. Every return requires seller confirmation; no refund is ever issued autonomously.
  </div>
</div>

<!-- =========================================================================
     OVERVIEW GRID MODAL (G KEY)
     ========================================================================= -->
<div id="overview-modal" class="chrome-ui">
  <div class="overview-header">
    <h2>SLIDE OVERVIEW · RETURNLENS (6 SLIDES)</h2>
    <button class="nav-btn" id="btn-close-overview">ESC to Close</button>
  </div>
  <div class="overview-grid">
    <div class="overview-thumb" data-jump="1" tabindex="0">
      <div>
        <div class="ot-num">SLIDE 1</div>
        <div class="ot-title">ReturnLens · Product Hero &amp; Value Proposition</div>
      </div>
      <div style="font-size: 11px; color: var(--text-muted); font-family: var(--font-mono);">Console Mock · Case B</div>
    </div>

    <div class="overview-thumb" data-jump="2" tabindex="0">
      <div>
        <div class="ot-num">SLIDE 2</div>
        <div class="ot-title">The return decision is made from memory, before the evidence is checked.</div>
      </div>
      <div style="font-size: 11px; color: var(--text-muted); font-family: var(--font-mono);">Convergence Diagram · 4 Sources</div>
    </div>

    <div class="overview-thumb" data-jump="3" tabindex="0">
      <div>
        <div class="ot-num">SLIDE 3</div>
        <div class="ot-title">One frame changes the verdict.</div>
      </div>
      <div style="font-size: 11px; color: var(--text-muted); font-family: var(--font-mono);">Store Truth vs Frame 00:07</div>
    </div>

    <div class="overview-thumb dark-thumb" data-jump="4" tabindex="0">
      <div>
        <div class="ot-num">SLIDE 4</div>
        <div class="ot-title">Policy checks and seller approval control actions</div>
      </div>
      <div style="font-size: 11px; color: #A3B8B0; font-family: var(--font-mono);">6-Step Pipeline · Decision Strip</div>
    </div>

    <div class="overview-thumb" data-jump="5" tabindex="0">
      <div>
        <div class="ot-num">SLIDE 5</div>
        <div class="ot-title">Every decision can be clicked back to a frame, a clause, and a log entry.</div>
      </div>
      <div style="font-size: 11px; color: var(--text-muted); font-family: var(--font-mono);">Case B Table + Cases A, C, D</div>
    </div>

    <div class="overview-thumb" data-jump="6" tabindex="0">
      <div>
        <div class="ot-num">SLIDE 6</div>
        <div class="ot-title">Buildable in 24 hours by 3 people, if the scope stays narrow.</div>
      </div>
      <div style="font-size: 11px; color: var(--text-muted); font-family: var(--font-mono);">24h Timeline · Team Scope</div>
    </div>
  </div>
</div>

<script>
  (function() {
    let currentSlide = 1;
    const totalSlides = 6;
    const presentation = document.getElementById('presentation');
    const progressBar = document.getElementById('top-progress-bar');
    const counterDisp = document.getElementById('slide-counter-disp');
    const notesDrawer = document.getElementById('notes-drawer');
    const notesTag = document.getElementById('notes-slide-tag');
    const notesBody = document.getElementById('notes-body-text');
    const overviewModal = document.getElementById('overview-modal');

    const speakerNotes = {
      1: "ReturnLens is a dedicated returns triage agent for solo direct-to-consumer merchants. In 24 hours we build the return triage flow with mock store and shipping APIs, plus one order status route to satisfy PS-04. Every return requires seller confirmation; no refund is ever issued autonomously.",
      2: "Today solo sellers juggle chat, order databases, delivery tracking, and policy PDFs in separate tabs, deciding from memory. Fraud and abuse account for 9% to 15.14% of returns depending on definition. The gap isn't a missing customer portal, but the lack of an objective record linking video proof, order truth, and policy rules.",
      3: "In our core benchmark case, the customer ordered white headphones but unboxed black ones. Instead of auto-denying the claim, ReturnLens cites frame 00:07, flags P-03 SKU mismatch, and escalates to the seller with three actionable choices: accept warehouse mis-shipment, request outer box label, or hold for physical inspection.",
      4: "Our architecture enforces strict boundaries: exactly three base LLM calls per case (planner, vision, critic). Models only observe and extract timestamps; deterministic Python code evaluates policy rules P-01 through P-08; and only the human seller can release mock shipping labels and refund drafts. Weak or contradictory evidence always fails closed.",
      5: "We test four concrete cases: Case A drafts approval for valid damage; Case B escalates the white vs black mismatch; Case C asks for clearer video when lighting is below threshold; and Case D leverages a continuous video take from sealed parcel to barcode to prove unbroken chain of custody. Every decision links back to an exact frame and log entry.",
      6: "Three engineers can build this prototype in 24 hours by cutting non-core features like WhatsApp, voice reasoning, and live gateways. We strictly enforce human seller confirmation, structured action logging, and a deterministic refund cap formula min(4999, remaining, paid). We deliver a checkable, buildable agent."
    };

    function updateScale() {
      if (window.matchMedia && window.matchMedia('print').matches) return;
      const targetW = 1280;
      const targetH = 720;
      const margin = 20; // safety viewport margin
      const scaleW = (window.innerWidth - margin) / targetW;
      const scaleH = (window.innerHeight - margin) / targetH;
      const scale = Math.min(scaleW, scaleH, 1.25); // cap max scale at 1.25 for large screens
      presentation.style.transform = `scale(${scale})`;
    }

    function showSlide(index) {
      if (index < 1) index = 1;
      if (index > totalSlides) index = totalSlides;
      currentSlide = index;

      document.querySelectorAll('.slide').forEach(s => s.classList.remove('active'));
      const target = document.getElementById(`slide-${index}`);
      if (target) target.classList.add('active');

      // Update chrome
      counterDisp.textContent = `${index} / ${totalSlides}`;
      progressBar.style.width = `${(index / totalSlides) * 100}%`;

      // Update notes
      notesTag.textContent = `SPEAKER NOTES · SLIDE ${index}`;
      notesBody.textContent = speakerNotes[index] || "";
    }

    function toggleNotes() {
      notesDrawer.classList.toggle('open');
    }

    function toggleOverview() {
      overviewModal.classList.toggle('open');
      if (overviewModal.classList.contains('open')) {
        const firstThumb = overviewModal.querySelector('.overview-thumb');
        if (firstThumb) firstThumb.focus();
      }
    }

    // Keyboard navigation
    window.addEventListener('keydown', (e) => {
      if (overviewModal.classList.contains('open')) {
        if (e.key === 'Escape' || e.key === 'g' || e.key === 'G') {
          toggleOverview();
        }
        return;
      }

      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown' || e.key === 'ArrowDown') {
        showSlide(currentSlide + 1);
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp' || e.key === 'ArrowUp') {
        showSlide(currentSlide - 1);
      } else if (e.key === 'Home') {
        showSlide(1);
      } else if (e.key === 'End') {
        showSlide(totalSlides);
      } else if (e.key === 'g' || e.key === 'G') {
        toggleOverview();
      } else if (e.key === 'n' || e.key === 'N') {
        toggleNotes();
      } else if (e.key === 'p' || e.key === 'P') {
        window.print();
      } else if (e.key === 'Escape') {
        notesDrawer.classList.remove('open');
        overviewModal.classList.remove('open');
      }
    });

    // Control buttons
    document.getElementById('btn-prev').addEventListener('click', () => showSlide(currentSlide - 1));
    document.getElementById('btn-next').addEventListener('click', () => showSlide(currentSlide + 1));
    document.getElementById('btn-overview').addEventListener('click', toggleOverview);
    document.getElementById('btn-close-overview').addEventListener('click', toggleOverview);
    document.getElementById('btn-notes').addEventListener('click', toggleNotes);
    document.getElementById('btn-close-notes').addEventListener('click', () => notesDrawer.classList.remove('open'));
    document.getElementById('btn-print').addEventListener('click', () => window.print());

    // Overview click to jump
    document.querySelectorAll('.overview-thumb').forEach(thumb => {
      thumb.addEventListener('click', () => {
        const jumpIdx = parseInt(thumb.getAttribute('data-jump'), 10);
        showSlide(jumpIdx);
        overviewModal.classList.remove('open');
      });
      thumb.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          const jumpIdx = parseInt(thumb.getAttribute('data-jump'), 10);
          showSlide(jumpIdx);
          overviewModal.classList.remove('open');
        }
      });
    });

    // Window events
    window.addEventListener('resize', updateScale);
    window.addEventListener('load', () => {
      updateScale();
      showSlide(1);
    });
  })();
</script>
</body>
</html>
"""

dest_path = r"D:\Code\Code\AIO\Code\hack4hack\deliverables\ReturnLens_v4.html"
with open(dest_path, "w", encoding="utf-8") as f:
    f.write(html_code)

print("Saved HTML successfully to:", dest_path, f"({len(html_code)} bytes)")

