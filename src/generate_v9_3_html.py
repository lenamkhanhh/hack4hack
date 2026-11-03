import os
import sys
import json
import shutil
import base64
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image

def file_hash(path):
    with open(path, "rb") as f:
        data = f.read()
    if str(path).endswith('.html'):
        data = data.replace(b'\r\n', b'\n')
    return hashlib.sha256(data).hexdigest()

def generate_v9_3():
    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / "content" / "deck_data_v9_3.json"
    deliverables_dir = base_dir / "deliverables"
    renders_dir = base_dir / "src" / "assets" / "v9_3_pptx_renders"
    pptx_path = deliverables_dir / "ReturnLens_v9_3.pptx"
    pdf_path = deliverables_dir / "ReturnLens_v9_3.pdf"
    deliverables_dir.mkdir(parents=True, exist_ok=True)

    if not data_path.exists():
        raise FileNotFoundError(f"Canonical data file missing: {data_path}")

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    meta = data["meta"]
    slides = data["slides"]

    # 1. Verify and read 6 slide PNG renders
    slide_b64s = []
    render_info = []
    slide_images = []
    for i in range(1, 7):
        p = renders_dir / f"slide_{i}.png"
        if not p.exists():
            raise FileNotFoundError(f"Slide render missing: {p}")
        im = Image.open(p)
        slide_images.append(im)
        render_info.append({
            "slide": i,
            "file": f"slide_{i}.png",
            "size": p.stat().st_size
        })
        with open(p, "rb") as f:
            b64_str = base64.b64encode(f.read()).decode("utf-8")
            slide_b64s.append(f"data:image/png;base64,{b64_str}")

    # 2. Write render_manifest.json
    manifest = {
        "source_pptx": "ReturnLens_v9_3.pptx",
        "source_sha256": file_hash(pptx_path),
        "tool": "Microsoft PowerPoint COM (win32com.client)",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dimensions": {
            "width": 1920,
            "height": 1080
        },
        "slides": render_info
    }
    manifest_path = renders_dir / "render_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Generated {manifest_path} (SHA256: {manifest['source_sha256'][:12]}...)")

    # 3. Generate Contact Sheet Preview (2352x882, exact 16:9 ratio, 3 cols x 2 rows)
    thumb_w = 784
    thumb_h = 441
    grid = Image.new("RGB", (thumb_w * 3, thumb_h * 2), (250, 250, 249))
    for idx, simg in enumerate(slide_images):
        row = idx // 3
        col = idx % 3
        resized = simg.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        grid.paste(resized, (col * thumb_w, row * thumb_h))

    preview_deliv = deliverables_dir / "ReturnLens_v9_3_preview.png"
    preview_root = base_dir / "ReturnLens_v9_3_preview.png"
    grid.save(preview_deliv, quality=95)
    shutil.copy2(preview_deliv, preview_root)
    print(f"Generated Preview Contact Sheet: {preview_deliv} ({grid.size})")

    # 4. Copy PDF and PPTX to root
    shutil.copy2(pptx_path, base_dir / "ReturnLens_v9_3.pptx")
    shutil.copy2(pdf_path, base_dir / "ReturnLens_v9_3.pdf")
    print(f"Copied ReturnLens_v9_3.pptx and ReturnLens_v9_3.pdf to root")

    # 5. Generate Interactive HTML Deck (Clean architectural design, Arial typography)
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ReturnLens v9.3 — Pitch Deck (AgentX Hackathon 2026, Track PS-04)</title>
<style>
  :root {{
    --bg-canvas: #121A16;
    --paper: #FAFAF9;
    --ink: #111815;
    --ink-light: #38443E;
    --muted: #6E7B74;
    --border: #E4E2DC;
    --pine: #0C5E4B;
    --pine-dark: #084335;
    --coral: #C84D33;
  }}

  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}

  body {{
    font-family: Arial, -apple-system, BlinkMacSystemFont, sans-serif;
    background: var(--bg-canvas);
    color: #F3EFE9;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
  }}

  header {{
    width: 100%;
    max-width: 1200px;
    padding: 16px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }}

  .brand {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}

  .brand h1 {{
    font-size: 20px;
    font-weight: 700;
    color: #FAF8F5;
    letter-spacing: -0.5px;
  }}

  .badge {{
    font-size: 11px;
    font-weight: 700;
    padding: 4px 8px;
    background: rgba(12, 94, 75, 0.4);
    color: #5EEAD4;
    border: 1px solid rgba(94, 234, 212, 0.3);
    border-radius: 2px;
  }}

  .nav-controls {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}

  .btn {{
    background: rgba(255, 255, 255, 0.08);
    color: #FAF8F5;
    border: 1px solid rgba(255, 255, 255, 0.15);
    padding: 8px 16px;
    border-radius: 4px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
  }}

  .btn:hover {{
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.3);
  }}

  main {{
    width: 100%;
    max-width: 1200px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}

  .slide-container {{
    width: 100%;
    aspect-ratio: 16 / 9;
    background: #000;
    border-radius: 4px;
    overflow: hidden;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
    position: relative;
    border: 1px solid rgba(255, 255, 255, 0.12);
  }}

  .slide {{
    display: none;
    width: 100%;
    height: 100%;
  }}

  .slide.active {{
    display: block;
  }}

  .slide img {{
    width: 100%;
    height: 100%;
    object-fit: contain;
    display: block;
  }}

  .dots-container {{
    display: flex;
    gap: 8px;
    margin-top: 16px;
  }}

  .dot {{
    width: 10px;
    height: 10px;
    background: rgba(255, 255, 255, 0.2);
    cursor: pointer;
    transition: all 0.2s;
  }}

  .dot.active {{
    background: #5EEAD4;
    width: 24px;
  }}

  .notes-panel {{
    width: 100%;
    margin-top: 24px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 4px;
    padding: 20px;
  }}

  .notes-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }}

  .notes-header h2 {{
    font-size: 14px;
    font-weight: 700;
    color: #5EEAD4;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}

  .notes-content {{
    font-size: 15px;
    line-height: 1.6;
    color: #E2E8F0;
    white-space: pre-line;
  }}

  .hint {{
    margin-top: 12px;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.4);
  }}
</style>
</head>
<body>

<header>
  <div class="brand">
    <h1>ReturnLens</h1>
    <span class="badge">AGENTX PS-04 · v9.3</span>
  </div>
  <div class="nav-controls">
    <button class="btn" onclick="prevSlide()">← Prev</button>
    <span id="counter" style="font-weight: 700; font-size: 14px; min-width: 60px; text-align: center;">01 / 06</span>
    <button class="btn" onclick="nextSlide()">Next →</button>
  </div>
</header>

<main>
  <div class="slide-container">
"""

    for i in range(6):
        active_cls = " active" if i == 0 else ""
        s_data = slides[i]
        html_content += f"""    <div class="slide{active_cls}" id="slide-{i+1}">
      <img src="{slide_b64s[i]}" alt="Slide {i+1}: {s_data['title']}">
    </div>
"""

    html_content += """  </div>

  <div class="dots-container">
    <div class="dot active" onclick="goToSlide(1)"></div>
    <div class="dot" onclick="goToSlide(2)"></div>
    <div class="dot" onclick="goToSlide(3)"></div>
    <div class="dot" onclick="goToSlide(4)"></div>
    <div class="dot" onclick="goToSlide(5)"></div>
    <div class="dot" onclick="goToSlide(6)"></div>
  </div>

  <div class="notes-panel">
    <div class="notes-header">
      <h2 id="notes-title">SPEAKER SCRIPT · SLIDE 01</h2>
      <span style="font-size: 12px; color: rgba(255,255,255,0.5);">Total 311 spoken words · ~3 minutes</span>
    </div>
    <div class="notes-content" id="notes-body"></div>
  </div>

  <div class="hint">
    Use Keyboard: ← Left Arrow / → Right Arrow / Space / Keys 1–6 to navigate.
  </div>
</main>

<script>
  const slidesData = """ + json.dumps(slides) + """;
  let currentSlide = 1;
  const totalSlides = 6;

  function updateSlide(n) {
    if (n < 1) n = 1;
    if (n > totalSlides) n = totalSlides;
    currentSlide = n;

    document.querySelectorAll('.slide').forEach((el, idx) => {
      el.classList.toggle('active', idx === currentSlide - 1);
    });

    document.querySelectorAll('.dot').forEach((el, idx) => {
      el.classList.toggle('active', idx === currentSlide - 1);
    });

    document.getElementById('counter').innerText = `0${currentSlide} / 06`;
    document.getElementById('notes-title').innerText = `SPEAKER SCRIPT · SLIDE 0${currentSlide} (${slidesData[currentSlide - 1].title})`;
    document.getElementById('notes-body').innerText = slidesData[currentSlide - 1].speaker_notes;
  }

  function nextSlide() { updateSlide(currentSlide + 1); }
  function prevSlide() { updateSlide(currentSlide - 1); }
  function goToSlide(n) { updateSlide(n); }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
      nextSlide();
    } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
      prevSlide();
    } else if (e.key >= '1' && e.key <= '6') {
      goToSlide(parseInt(e.key));
    }
  });

  updateSlide(1);
</script>

</body>
</html>
"""

    html_deliv = deliverables_dir / "ReturnLens_v9_3.html"
    html_root = base_dir / "ReturnLens_v9_3.html"

    with open(html_deliv, "w", encoding="utf-8", newline="\n") as f:
        f.write(html_content)
    shutil.copy2(html_deliv, html_root)
    print(f"Generated ReturnLens_v9_3.html successfully ({html_deliv.stat().st_size} bytes)")

if __name__ == "__main__":
    generate_v9_3()
