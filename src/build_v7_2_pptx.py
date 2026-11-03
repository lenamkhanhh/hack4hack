import os
import sys
import json
import shutil
import zipfile
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_v7_2_pptx():
    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / "content" / "deck_data_v7_2.json"
    deliverables_dir = base_dir / "deliverables"
    assets_dir = base_dir / "src" / "assets"
    deliverables_dir.mkdir(parents=True, exist_ok=True)

    if not data_path.exists():
        raise FileNotFoundError(f"Canonical data file missing: {data_path}")

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    meta = data["meta"]
    slides_data = {s["slide_number"]: s for s in data["slides"]}

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ReturnLens V7.2 Palette (Warm Paper, Forest Ink, Pine Teal, Terracotta Coral, Obsidian)
    C_PAPER = RGBColor(0xFA, 0xF8, 0xF5)          # Warm Paper canvas (#FAF8F5)
    C_PAPER_TINT = RGBColor(0xF3, 0xEF, 0xE9)     # Warm Paper Tint
    C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)          # Crisp card white
    C_INK = RGBColor(0x11, 0x20, 0x1A)            # Forest Ink (#11201A)
    C_INK_LIGHT = RGBColor(0x28, 0x3C, 0x33)      # Charcoal slate
    C_MUTED = RGBColor(0x56, 0x6B, 0x60)          # Sage Muted
    C_SUBTLE = RGBColor(0x8A, 0x9C, 0x93)         # Hairline gray
    C_BORDER = RGBColor(0xE2, 0xDC, 0xD2)         # Soft Border (#E2DCD2)
    C_BORDER_STRONG = RGBColor(0xCA, 0xC2, 0xB3)  # Strong Divider

    # Accents
    C_TEAL = RGBColor(0x0A, 0x5C, 0x48)           # Pine Teal (#0A5C48)
    C_TEAL_DARK = RGBColor(0x06, 0x40, 0x32)      # Dark Pine
    C_TEAL_LIGHT = RGBColor(0xE8, 0xF5, 0xF1)     # Soft Mint
    C_TEAL_ACCENT = RGBColor(0x2D, 0xD4, 0xBF)    # Mint Accent for dark surfaces

    C_CORAL = RGBColor(0xC8, 0x4B, 0x31)          # Terracotta Coral (#C84B31)
    C_CORAL_DARK = RGBColor(0x9E, 0x2A, 0x2B)     # Deep Coral
    C_CORAL_LIGHT = RGBColor(0xFD, 0xF3, 0xF1)    # Blush Coral Tint
    C_CORAL_BORDER = RGBColor(0xF7, 0xC5, 0xBC)   # Coral Border

    C_AMBER = RGBColor(0xD9, 0x77, 0x06)          # Amber
    C_AMBER_DARK = RGBColor(0x92, 0x40, 0x0E)     # Deep Amber
    C_AMBER_LIGHT = RGBColor(0xFE, 0xF3, 0xC7)    # Amber Cream
    C_GOLD_TEXT = RGBColor(0xFF, 0xD4, 0x85)      # Gold Highlight for dark cards

    # macOS Window Buttons
    C_MAC_RED = RGBColor(0xFF, 0x5F, 0x56)
    C_MAC_YELLOW = RGBColor(0xFF, 0xBD, 0x2E)
    C_MAC_GREEN = RGBColor(0x27, 0xC9, 0x3F)

    # Dark Obsidian Architecture Palette (Slide 4)
    C_DARK_BG = RGBColor(0x0B, 0x16, 0x13)        # Obsidian Canvas (#0B1613)
    C_DARK_CARD = RGBColor(0x13, 0x23, 0x1E)      # Obsidian Card
    C_DARK_BORDER = RGBColor(0x22, 0x3B, 0x33)    # Obsidian Border
    C_DARK_INK = RGBColor(0xF8, 0xF7, 0xF4)       # Pure Warm White text
    C_DARK_MUTED = RGBColor(0x95, 0xAF, 0xA5)     # Sage Muted text

    FONT_HEAD = "Calibri"
    FONT_MONO = "Consolas"

    # Image assets
    img_white_order = assets_dir / "studio_white_headphones.jpg"
    img_black_unboxing = assets_dir / "unboxing_black_headphones.jpg"

    def set_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.color.rgb = color
        bg.line.width = 0

    def add_footer(slide, current_num, dark=False):
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.46), Inches(7.0), Inches(12.41), Inches(0.015))
        line.fill.solid()
        line.fill.fore_color.rgb = C_DARK_BORDER if dark else C_BORDER
        line.line.width = 0

        tb = slide.shapes.add_textbox(Inches(0.46), Inches(7.05), Inches(10.0), Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = "RETURNLENS V7.2 · AGENTX HACKATHON 2026 PS-04 · TEAM ROOKIE (3 MEMBERS)"
        p.font.name = FONT_MONO
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_DARK_MUTED if dark else C_MUTED

        tb_num = slide.shapes.add_textbox(Inches(11.87), Inches(7.05), Inches(1.0), Inches(0.3))
        tf_num = tb_num.text_frame
        tf_num.margin_left = tf_num.margin_top = tf_num.margin_right = tf_num.margin_bottom = 0
        p_num = tf_num.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.text = f"0{current_num} / 06"
        p_num.font.name = FONT_MONO
        p_num.font.size = Pt(9.5)
        p_num.font.bold = True
        p_num.font.color.rgb = C_TEAL_ACCENT if dark else C_TEAL

    def add_notes(slide, text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = text

    # =========================================================
    # SLIDE 1: PRODUCT HERO & REFINED SELLER DECISION CONSOLE
    # =========================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1, C_PAPER)
    d1 = slides_data[1]

    # Category Tag
    tb = s1.shapes.add_textbox(Inches(0.46), Inches(0.36), Inches(12.0), Inches(0.28))
    tf = tb.text_frame
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = "AGENTX HACKATHON 2026 · TRACK PS-04 · TEAM ROOKIE (3 MEMBERS)"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    # Left Column: Brand Story, Value Prop & Architectural Principle
    tb_title = s1.shapes.add_textbox(Inches(0.46), Inches(0.85), Inches(4.5), Inches(4.1))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0

    p = tf_t.paragraphs[0]
    p.text = d1.get("headline", meta["project_name"])
    p.font.name = FONT_HEAD
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = C_INK
    p.space_after = Pt(12)

    p = tf_t.add_paragraph()
    p.text = d1.get("subheadline", meta["tagline"])
    p.font.name = FONT_HEAD
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p.space_after = Pt(14)

    p = tf_t.add_paragraph()
    p.text = d1.get("supporting", meta["one_liner"])
    p.font.name = FONT_HEAD
    p.font.size = Pt(15.5)
    p.font.color.rgb = C_MUTED
    p.space_after = Pt(16)

    # Core Architectural Principle Card (Left Column bottom)
    left_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.46), Inches(5.12), Inches(4.5), Inches(1.58))
    left_box.fill.solid()
    left_box.fill.fore_color.rgb = C_PAPER_TINT
    left_box.line.color.rgb = C_BORDER
    left_box.line.width = Pt(1)

    tb_lb = s1.shapes.add_textbox(Inches(0.62), Inches(5.24), Inches(4.18), Inches(1.34))
    tf_lb = tb_lb.text_frame
    tf_lb.word_wrap = True
    p = tf_lb.paragraphs[0]
    p.text = "CORE ARCHITECTURAL PRINCIPLE"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_DARK
    p = tf_lb.add_paragraph()
    p.text = f"“{meta['core_thesis']}”"
    p.font.name = FONT_HEAD
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = C_INK
    p = tf_lb.add_paragraph()
    p.text = f"Scope: Return triage + order status · Mock fixtures · Never auto-refunds\nGuardrail: Server cap ≤ min({meta['refund_guardrail']['ceiling']}, remaining, paid) · Hash-bound"
    p.font.name = FONT_MONO
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_INK_LIGHT

    # Right Column: Refined macOS Seller Console
    c_x, c_y, c_w = Inches(5.22), Inches(0.85), Inches(7.65)
    c_btn_top = Inches(5.34)
    c_btn_h = Inches(0.38)
    c_btn_bottom = c_btn_top + c_btn_h
    c_pad_bottom = Inches(0.22)
    c_bottom = c_btn_bottom + c_pad_bottom
    c_h = c_bottom - c_y

    c_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x, c_y, c_w, c_h)
    c_card.fill.solid()
    c_card.fill.fore_color.rgb = C_WHITE
    c_card.line.color.rgb = C_BORDER_STRONG
    c_card.line.width = Pt(1)

    # 1. macOS Window Title Bar with Realistic Traffic-Light Controls
    bar_h = Inches(0.42)
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_x, c_y, c_w, bar_h)
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_INK
    bar.line.width = 0

    dot_d = Inches(0.13)
    dot_y = c_y + Inches(0.145)
    dot_colors = [C_MAC_RED, C_MAC_YELLOW, C_MAC_GREEN]
    for i, col in enumerate(dot_colors):
        dot = s1.shapes.add_shape(MSO_SHAPE.OVAL, c_x + Inches(0.20 + i * 0.18), dot_y, dot_d, dot_d)
        dot.fill.solid()
        dot.fill.fore_color.rgb = col
        dot.line.width = 0

    tb_bar = s1.shapes.add_textbox(c_x + Inches(0.80), c_y + Inches(0.06), c_w - Inches(0.95), Inches(0.32))
    tf_b = tb_bar.text_frame
    tf_b.margin_left = tf_b.margin_top = 0
    p = tf_b.paragraphs[0]
    p.text = f"{d1['console_mockup']['title']} — {d1['console_mockup']['case_badge']}       [ MOCK EVIDENCE PACK ]"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0xFD, 0xF2, 0xD0)

    # 2. Metadata Sub-bar
    sub_y = c_y + bar_h
    sub_h = Inches(0.34)
    subbar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_x, sub_y, c_w, sub_h)
    subbar.fill.solid()
    subbar.fill.fore_color.rgb = C_PAPER_TINT
    subbar.line.color.rgb = C_BORDER
    subbar.line.width = Pt(1)

    tb_sub = s1.shapes.add_textbox(c_x + Inches(0.2), sub_y + Inches(0.04), c_w - Inches(0.4), Inches(0.28))
    tf_s = tb_sub.text_frame
    tf_s.margin_left = tf_s.margin_top = 0
    p = tf_s.paragraphs[0]
    p.text = f"CASE: {meta['sample_order']['case_id']} · ORDER: {meta['sample_order']['order_id']} · SKU: {meta['sample_order']['sku']}      DELIVERED: 4d ago (Window: Day 4/7 PASS)"
    p.font.name = FONT_MONO
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_INK

    # 3. Side-by-side Visual Comparison
    b_y = sub_y + sub_h + Inches(0.12)
    bx_w = Inches(3.55)
    b_h = Inches(2.55)

    # Left Box - Store Truth
    box_l = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x + Inches(0.20), b_y, bx_w, b_h)
    box_l.fill.solid()
    box_l.fill.fore_color.rgb = C_PAPER
    box_l.line.color.rgb = C_BORDER
    box_l.line.width = Pt(1)

    if img_white_order.exists():
        s1.shapes.add_picture(str(img_white_order), c_x + Inches(0.30), b_y + Inches(0.10), bx_w - Inches(0.20), Inches(1.18))

    tb_l = s1.shapes.add_textbox(c_x + Inches(0.30), b_y + Inches(1.32), bx_w - Inches(0.20), Inches(1.15))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0
    p = tf_l.paragraphs[0]
    p.text = "STORE TRUTH · SHOPIFY"
    p.font.name = FONT_MONO
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = C_MUTED
    p = tf_l.add_paragraph()
    p.text = f"{meta['sample_order']['sku']} ({meta['sample_order']['ordered_color']})"
    p.font.name = FONT_HEAD
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_INK
    p = tf_l.add_paragraph()
    p.text = f"{meta['sample_order']['price']} paid · Studio Spec · Security Tag Required\nDelivered: 4d ago (Shippo #SH-9012)\nReturn Window: Day 4/7 (P-04 PASS)"
    p.font.name = FONT_HEAD
    p.font.size = Pt(10)
    p.font.color.rgb = C_MUTED

    # Right Box - Grounded Observation: Black casing, color-consistent with HEAD-BLK-09, SKU not verified
    box_r = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x + Inches(3.90), b_y, bx_w, b_h)
    box_r.fill.solid()
    box_r.fill.fore_color.rgb = C_CORAL_LIGHT
    box_r.line.color.rgb = C_CORAL_BORDER
    box_r.line.width = Pt(1.5)

    if img_black_unboxing.exists():
        s1.shapes.add_picture(str(img_black_unboxing), c_x + Inches(4.00), b_y + Inches(0.10), bx_w - Inches(0.20), Inches(1.18))

    tb_r = s1.shapes.add_textbox(c_x + Inches(4.00), b_y + Inches(1.32), bx_w - Inches(0.20), Inches(1.15))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0
    p = tf_r.paragraphs[0]
    p.text = "OBSERVED · VIDEO FRAME 00:07"
    p.font.name = FONT_MONO
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = C_CORAL
    p = tf_r.add_paragraph()
    p.text = "Black Casing (color-consistent with HEAD-BLK-09)"
    p.font.name = FONT_HEAD
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CORAL_DARK
    p = tf_r.add_paragraph()
    p.text = "Barcode: Unverified · Exact SKU: Not verified\nLighting: Sufficient · Policy P-03 FAIL\nContradiction flagged → Route to human seller"
    p.font.name = FONT_HEAD
    p.font.size = Pt(10)
    p.font.color.rgb = C_INK_LIGHT

    # 4. FIX A: Precise P-03 Color Contradiction Notice Strip (Eliminate exact SKU overclaim)
    conf_y = b_y + b_h + Inches(0.10)
    conf_h = Inches(0.44)
    conf = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x + Inches(0.20), conf_y, c_w - Inches(0.40), conf_h)
    conf.fill.solid()
    conf.fill.fore_color.rgb = C_CORAL_LIGHT
    conf.line.color.rgb = C_CORAL_BORDER
    conf.line.width = Pt(1)

    tb_c = s1.shapes.add_textbox(c_x + Inches(0.24), conf_y + Inches(0.06), c_w - Inches(0.48), conf_h - Inches(0.10))
    tf_c = tb_c.text_frame
    tf_c.margin_left = Inches(0.04)
    tf_c.margin_right = Inches(0.04)
    tf_c.margin_top = Inches(0.02)
    tf_c.margin_bottom = Inches(0.02)
    p = tf_c.paragraphs[0]
    p.text = "P-03 COLOR CONTRADICTION: Observed black casing conflicts with ordered Matte White specification. Exact SKU unverified."
    p.font.name = FONT_MONO
    p.font.size = Pt(7.5)
    p.font.bold = True
    p.font.color.rgb = C_CORAL_DARK

    # 5. Audit & Ledger Strip
    aud_y = conf_y + conf_h + Inches(0.08)
    aud_h = Inches(0.34)
    aud_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x + Inches(0.20), aud_y, c_w - Inches(0.40), aud_h)
    aud_box.fill.solid()
    aud_box.fill.fore_color.rgb = C_PAPER_TINT
    aud_box.line.color.rgb = C_BORDER
    aud_box.line.width = Pt(1)

    tb_aud = s1.shapes.add_textbox(c_x + Inches(0.32), aud_y + Inches(0.05), c_w - Inches(0.64), aud_h - Inches(0.08))
    tf_aud = tb_aud.text_frame
    tf_aud.margin_left = tf_aud.margin_top = tf_aud.margin_right = tf_aud.margin_bottom = 0
    p = tf_aud.paragraphs[0]
    p.text = f"AUDIT LEDGER: Logged to SQLite · SHA256 evidence hash · Server refund cap: ≤ min({meta['refund_guardrail']['ceiling']}, rem, paid)"
    p.font.name = FONT_MONO
    p.font.size = Pt(8.5)
    p.font.color.rgb = C_MUTED

    # 6. Bottom Decision & Action Bar (FIX A: "Review Evidence & Decide")
    tb_act = s1.shapes.add_textbox(c_x + Inches(0.20), c_btn_top + Inches(0.04), Inches(3.2), Inches(0.32))
    tf_a = tb_act.text_frame
    p = tf_a.paragraphs[0]
    p.text = "● SELLER GATE (FAIL-CLOSED)"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_AMBER_DARK

    btn_sec = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x + Inches(3.45), c_btn_top, Inches(1.85), c_btn_h)
    btn_sec.fill.solid()
    btn_sec.fill.fore_color.rgb = C_PAPER_TINT
    btn_sec.line.color.rgb = C_BORDER_STRONG
    btn_sec.line.width = Pt(1)
    p = btn_sec.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "Request Box Label"
    p.font.name = FONT_HEAD
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_INK

    primary_cta_text = d1['console_mockup'].get('button_text', 'Review Evidence & Decide')
    btn_pri = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x + Inches(5.40), c_btn_top, Inches(2.05), c_btn_h)
    btn_pri.fill.solid()
    btn_pri.fill.fore_color.rgb = C_TEAL
    btn_pri.line.width = 0
    p = btn_pri.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = primary_cta_text
    p.font.name = FONT_HEAD
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    add_footer(s1, 1)
    add_notes(s1, d1["speaker_notes"])

    # =========================================================
    # SLIDE 2: THE PROBLEM (4 DISCONNECTED SOURCES CONVERGENCE)
    # =========================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2, C_PAPER)
    d2 = slides_data[2]

    tb = s2.shapes.add_textbox(Inches(0.46), Inches(0.36), Inches(12.0), Inches(0.25))
    p = tb.text_frame.paragraphs[0]
    p.text = d2.get("tag", "THE PROBLEM · SOLO SELLER BOTTLENECK")
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CORAL

    tb = s2.shapes.add_textbox(Inches(0.46), Inches(0.65), Inches(12.4), Inches(0.85))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = d2.get("headline", "One return. Four disconnected sources.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = C_INK
    p = tf.add_paragraph()
    p.text = d2.get("subheadline", "Four systems. No traceable decision.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(16)
    p.font.color.rgb = C_MUTED

    # 4 Source Cards on Left
    src_x = Inches(0.46)
    src_w = Inches(5.80)
    card_h = Inches(1.10)
    gap_y = Inches(0.18)
    start_y = Inches(1.68)

    sources = [
        ("01", "Buyer Message", "Unstructured text & unverified unboxing video in chat", C_CORAL),
        ("02", "Order Record", f"Shopify manifest: {meta['sample_order']['sku']}, {meta['sample_order']['ordered_color']}, {meta['sample_order']['price']}", C_TEAL),
        ("03", "Courier Status", "Shippo scan: delivered 4 days ago (P-01 verified, Day 4 of 7)", C_MUTED),
        ("04", "Return Policy", "Store rules: 7-day window (P-04), packaging tag required (P-02)", C_INK_LIGHT)
    ]

    for idx, (num, title, detail, accent) in enumerate(sources):
        cy = start_y + Inches(idx * 1.28)
        sc = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, src_x, cy, src_w, card_h)
        sc.fill.solid()
        sc.fill.fore_color.rgb = C_WHITE
        sc.line.color.rgb = C_BORDER
        sc.line.width = Pt(1)

        # Number pill
        pill = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, src_x + Inches(0.16), cy + Inches(0.18), Inches(0.52), Inches(0.48))
        pill.fill.solid()
        pill.fill.fore_color.rgb = C_PAPER_TINT
        pill.line.width = 0
        p_pill = pill.text_frame.paragraphs[0]
        p_pill.alignment = PP_ALIGN.CENTER
        p_pill.text = num
        p_pill.font.name = FONT_MONO
        p_pill.font.size = Pt(12)
        p_pill.font.bold = True
        p_pill.font.color.rgb = accent

        tb_text = s2.shapes.add_textbox(src_x + Inches(0.85), cy + Inches(0.14), src_w - Inches(1.05), Inches(0.82))
        tf_t = tb_text.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p = tf_t.paragraphs[0]
        p.text = title
        p.font.name = FONT_HEAD
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = C_INK
        p = tf_t.add_paragraph()
        p.text = detail
        p.font.name = FONT_HEAD
        p.font.size = Pt(11)
        p.font.color.rgb = C_MUTED

    # Center Convergence Arrows & Right Focal Area
    foc_x = Inches(6.65)
    foc_w = Inches(6.22)
    foc_h = Inches(5.00)

    # Focal Dark Card: The Missing Link
    fc = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, foc_x, start_y, foc_w, Inches(3.60))
    fc.fill.solid()
    fc.fill.fore_color.rgb = C_INK
    fc.line.color.rgb = C_BORDER_STRONG
    fc.line.width = Pt(1.5)

    tb_fc = s2.shapes.add_textbox(foc_x + Inches(0.35), start_y + Inches(0.30), foc_w - Inches(0.70), Inches(3.00))
    tf_fc = tb_fc.text_frame
    tf_fc.word_wrap = True
    tf_fc.margin_left = tf_fc.margin_top = tf_fc.margin_right = tf_fc.margin_bottom = 0

    p = tf_fc.paragraphs[0]
    p.text = "THE MISSING LINK"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_ACCENT
    p.space_after = Pt(6)

    p = tf_fc.add_paragraph()
    p.text = "NO AUDITABLE EVIDENCE RECORD"
    p.font.name = FONT_HEAD
    p.font.size = Pt(21)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.space_after = Pt(12)

    p = tf_fc.add_paragraph()
    p.text = "No auditable evidence record. One solo seller making high-stakes financial decisions across browser tabs."
    p.font.name = FONT_HEAD
    p.font.size = Pt(14.5)
    p.font.color.rgb = RGBColor(0xDF, 0xEA, 0xE5)
    p.space_after = Pt(12)

    p = tf_fc.add_paragraph()
    p.text = "• Wrong Refund: Loses inventory and gross margin.\n• Unfair Denial: Destroys customer lifetime value (LTV).\n• Manual Triage: Wastes 15–30 minutes per dispute."
    p.font.name = FONT_HEAD
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(0xBA, 0xD4, 0xCA)

    # Sourced Fraud Context Box (NRF 9% vs Deloitte 15.14%)
    fb = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, foc_x, start_y + Inches(3.72), foc_w, Inches(1.28))
    fb.fill.solid()
    fb.fill.fore_color.rgb = C_PAPER_TINT
    fb.line.color.rgb = C_BORDER
    fb.line.width = Pt(1)

    tb_fb = s2.shapes.add_textbox(foc_x + Inches(0.25), start_y + Inches(3.80), foc_w - Inches(0.50), Inches(1.12))
    tf_fb = tb_fb.text_frame
    tf_fb.word_wrap = True
    tf_fb.margin_left = tf_fb.margin_top = tf_fb.margin_right = tf_fb.margin_bottom = 0
    p = tf_fb.paragraphs[0]
    p.text = "INDUSTRY BASELINE & FRAUD CONTEXT (RIGOROUS PROVENANCE):"
    p.font.name = FONT_MONO
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_DARK
    p = tf_fb.add_paragraph()
    p.text = "• 9.0% — Return Fraud (NRF/Appriss 2024: strict criminal fraud: unboxing swaps, empty boxes)"
    p.font.name = FONT_HEAD
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_INK
    p = tf_fb.add_paragraph()
    p.text = "• 15.14% — Fraud + Policy Abuse (Appriss/Deloitte 2024: criminal fraud + policy abuse like wardrobing)"
    p.font.name = FONT_HEAD
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_INK
    p = tf_fb.add_paragraph()
    p.text = "Sources: NRF/Appriss 2024 ($101B US retail); Appriss/Deloitte 2024. Measured scopes are distinct."
    p.font.name = FONT_MONO
    p.font.size = Pt(8.0)
    p.font.color.rgb = C_MUTED

    add_footer(s2, 2)
    add_notes(s2, d2["speaker_notes"])

    # =========================================================
    # SLIDE 3: STAR DEMO (CASE B EVIDENCE COMPARISON)
    # =========================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3, C_PAPER)
    d3 = slides_data[3]

    tb = s3.shapes.add_textbox(Inches(0.46), Inches(0.36), Inches(12.0), Inches(0.25))
    p = tb.text_frame.paragraphs[0]
    p.text = d3.get("tag", "STAR DEMO · CORE BENCHMARK SCENARIO")
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CORAL

    tb = s3.shapes.add_textbox(Inches(0.46), Inches(0.65), Inches(12.4), Inches(0.85))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = d3.get("headline", "The order says white. The video shows black.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = C_INK
    p = tf.add_paragraph()
    p.text = d3.get("subheadline", "ReturnLens flags the contradiction — the seller decides.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(16)
    p.font.color.rgb = C_MUTED

    # Side-by-Side Comparison Columns
    col_w = Inches(5.90)
    col_h = Inches(3.40)
    col_y = Inches(1.68)

    # Left Column: Store Truth
    cl = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.46), col_y, col_w, col_h)
    cl.fill.solid()
    cl.fill.fore_color.rgb = C_WHITE
    cl.line.color.rgb = C_BORDER
    cl.line.width = Pt(1)

    if img_white_order.exists():
        s3.shapes.add_picture(str(img_white_order), Inches(0.70), col_y + Inches(0.20), Inches(2.20), Inches(2.20))

    tb_cl = s3.shapes.add_textbox(Inches(3.10), col_y + Inches(0.20), Inches(3.10), Inches(2.20))
    tf = tb_cl.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "STORE CATALOG TRUTH"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_DARK
    p = tf.add_paragraph()
    p.text = f"{meta['sample_order']['sku']}\n{meta['sample_order']['ordered_color']}"
    p.font.name = FONT_HEAD
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_INK
    p.space_after = Pt(4)
    p = tf.add_paragraph()
    p.text = f"Price: {meta['sample_order']['price']} paid\nProduct: {meta['sample_order']['product_name']}\nCarrier: Shippo #SH-9012\nDelivered: 4d ago (Day 4/7, P-04 PASS)"
    p.font.name = FONT_HEAD
    p.font.size = Pt(11)
    p.font.color.rgb = C_MUTED

    # Bottom caption on Left Card
    tb_cl_bot = s3.shapes.add_textbox(Inches(0.70), col_y + Inches(2.55), Inches(5.40), Inches(0.70))
    tf = tb_cl_bot.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "GROUND TRUTH: Verified Shopify order record & delivery timestamp."
    p.font.name = FONT_MONO
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_DARK

    # Right Column: Observed Unboxing Video Keyframe
    cr = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.97), col_y, col_w, col_h)
    cr.fill.solid()
    cr.fill.fore_color.rgb = C_CORAL_LIGHT
    cr.line.color.rgb = C_CORAL_BORDER
    cr.line.width = Pt(1.5)

    if img_black_unboxing.exists():
        s3.shapes.add_picture(str(img_black_unboxing), Inches(7.21), col_y + Inches(0.20), Inches(2.20), Inches(2.20))

    tb_cr = s3.shapes.add_textbox(Inches(9.61), col_y + Inches(0.20), Inches(3.10), Inches(2.20))
    tf = tb_cr.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "UNBOXING KEYFRAME (STAGED MOCK)"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_CORAL_DARK
    p = tf.add_paragraph()
    p.text = "Black Casing\n(Color-consistent)"
    p.font.name = FONT_HEAD
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_CORAL_DARK
    p.space_after = Pt(4)
    p = tf.add_paragraph()
    p.text = "Exact SKU: Not verified (Barcode unverified) · Policy P-03 FAIL\nLighting: Sufficient · REC 00:07 / 00:24 (Mock Keyframe)"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.color.rgb = C_CORAL_DARK

    # Bottom caption on Right Card
    tb_cr_bot = s3.shapes.add_textbox(Inches(7.21), col_y + Inches(2.55), Inches(5.40), Inches(0.70))
    tf = tb_cr_bot.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "VISUAL GROUNDING: Frame 00:07 confirms black casing. Barcode is unverified; citation does not prove video authenticity."
    p.font.name = FONT_MONO
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_CORAL_DARK

    # Central Mismatch Badge (≠)
    mm = s3.shapes.add_shape(MSO_SHAPE.OVAL, Inches(6.36), col_y + Inches(1.30), Inches(0.70), Inches(0.70))
    mm.fill.solid()
    mm.fill.fore_color.rgb = C_CORAL
    mm.line.color.rgb = C_WHITE
    mm.line.width = Pt(2)
    p_mm = mm.text_frame.paragraphs[0]
    p_mm.alignment = PP_ALIGN.CENTER
    p_mm.text = "≠"
    p_mm.font.name = FONT_HEAD
    p_mm.font.size = Pt(24)
    p_mm.font.bold = True
    p_mm.font.color.rgb = C_WHITE

    # Bottom Wide Decision Strip (Full Width)
    dec_y = Inches(5.24)
    dec_h = Inches(1.58)
    dec_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.46), dec_y, Inches(12.41), dec_h)
    dec_box.fill.solid()
    dec_box.fill.fore_color.rgb = C_WHITE
    dec_box.line.color.rgb = C_BORDER_STRONG
    dec_box.line.width = Pt(1.5)

    # Left Section of Decision Strip
    tb_ds_l = s3.shapes.add_textbox(Inches(0.65), dec_y + Inches(0.12), Inches(4.50), Inches(1.35))
    tf = tb_ds_l.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "POLICY P-03 RESULT: COLOR CONTRADICTION"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_CORAL
    p = tf.add_paragraph()
    p.text = "Ordered White ≠ Observed Black"
    p.font.name = FONT_HEAD
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_INK
    p = tf.add_paragraph()
    p.text = f"Guardrail: 0 < amt <= min({meta['refund_guardrail']['ceiling']}, rem_ref, paid) · Prototype simulation"
    p.font.name = FONT_MONO
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_MUTED
    p = tf.add_paragraph()
    p.text = "No automatic policy approvals. Financial release requires seller click."
    p.font.name = FONT_MONO
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_CORAL_DARK

    # Vertical divider in decision strip
    div = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.30), dec_y + Inches(0.15), Inches(0.015), Inches(1.28))
    div.fill.solid()
    div.fill.fore_color.rgb = C_BORDER
    div.line.width = 0

    # Right Section: Preserved 3 Seller Choices
    tb_ds_r = s3.shapes.add_textbox(Inches(5.50), dec_y + Inches(0.12), Inches(7.15), Inches(1.35))
    tf = tb_ds_r.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "FAIL-CLOSED GATE · THREE PRESERVED SELLER OPTIONS:"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_DARK

    # 3 Seller Action Cards
    act_y = dec_y + Inches(0.42)
    act_w = Inches(2.25)
    act_h = Inches(0.95)

    opts = [
        ("Option 1", "Accept as warehouse mis-shipment", C_TEAL_LIGHT, C_TEAL_DARK),
        ("Option 2", "Request photo of outside-box label", C_PAPER_TINT, C_INK),
        ("Option 3", "Hold return for parcel inspection", C_CORAL_LIGHT, C_CORAL_DARK)
    ]

    for idx, (lbl, text, bg_c, txt_c) in enumerate(opts):
        ax = Inches(5.50 + idx * 2.45)
        ab = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, ax, act_y, act_w, act_h)
        ab.fill.solid()
        ab.fill.fore_color.rgb = bg_c
        ab.line.color.rgb = C_BORDER
        ab.line.width = Pt(1)

        tb_a = s3.shapes.add_textbox(ax + Inches(0.12), act_y + Inches(0.10), act_w - Inches(0.24), act_h - Inches(0.20))
        tf_a = tb_a.text_frame
        tf_a.word_wrap = True
        tf_a.margin_left = tf_a.margin_top = tf_a.margin_right = tf_a.margin_bottom = 0
        p = tf_a.paragraphs[0]
        p.text = lbl
        p.font.name = FONT_MONO
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = txt_c
        p = tf_a.add_paragraph()
        p.text = text
        p.font.name = FONT_HEAD
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_INK

    add_footer(s3, 3)
    add_notes(s3, d3["speaker_notes"])

    # =========================================================
    # SLIDE 4: SYSTEM ARCHITECTURE (OBSIDIAN DARK THEME)
    # =========================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4, C_DARK_BG)
    d4 = slides_data[4]

    tb = s4.shapes.add_textbox(Inches(0.46), Inches(0.36), Inches(12.0), Inches(0.25))
    p = tb.text_frame.paragraphs[0]
    p.text = d4.get("tag", "SYSTEM ARCHITECTURE · FAIL-CLOSED SAFETY GATES")
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_ACCENT

    tb = s4.shapes.add_textbox(Inches(0.46), Inches(0.65), Inches(12.4), Inches(0.85))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = d4.get("headline", meta["core_thesis"])
    p.font.name = FONT_HEAD
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = C_DARK_INK
    p = tf.add_paragraph()
    p.text = d4.get("subheadline", "Exactly 3 model calls per triage pass. Weak evidence triggers stateful clarification. Zero automated refunds.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(15.5)
    p.font.color.rgb = C_DARK_MUTED

    # 6-Stage Visual Architecture Pipeline with Distinct Authority Types & Directional Flow
    pip_y = Inches(1.65)
    pip_h = Inches(1.10)
    pip = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.46), pip_y, Inches(12.41), pip_h)
    pip.fill.solid()
    pip.fill.fore_color.rgb = C_DARK_CARD
    pip.line.color.rgb = C_DARK_BORDER
    pip.line.width = Pt(1)

    steps = [
        ("1", "Planner", "Model Call 1", "Proposes typed JSON actions"),
        ("2", "Tools & Vision", "Model Call 2", "FFmpeg keyframes + vision (fallible)"),
        ("3", "Policy Engine", "Deterministic Code", "Evaluates rules P-01–P-08"),
        ("4", "Critic", "Model Call 3", "Verifies cited timestamps"),
        ("5", "Seller Gate", "Human Merchant", "Fail-closed 1-click auth"),
        ("6", "Audit Ledger", "SQLite / JSON", "Append-only signed audit")
    ]
    for idx, (num, name, role_badge, desc) in enumerate(steps):
        step_x = Inches(0.65 + idx * 2.05)
        tb_step = s4.shapes.add_textbox(step_x, pip_y + Inches(0.10), Inches(1.90), Inches(0.90))
        tf = tb_step.text_frame
        p = tf.paragraphs[0]
        p.text = f"{num}. {name}"
        p.font.name = FONT_MONO
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = C_TEAL_ACCENT if "Model" in role_badge else C_DARK_INK
        p = tf.add_paragraph()
        p.text = role_badge
        p.font.name = FONT_MONO
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = C_GOLD_TEXT if "Human" in role_badge else (C_TEAL_ACCENT if "Model" in role_badge else C_DARK_MUTED)
        p = tf.add_paragraph()
        p.text = desc
        p.font.name = FONT_HEAD
        p.font.size = Pt(10)
        p.font.color.rgb = C_DARK_MUTED

    # 3 Floating Architectural Pillars
    g_y = Inches(2.92)
    g_w = Inches(3.95)
    g_h = Inches(2.72)

    # Pillar 1: Call Budget & Zero Payment Access
    gc1 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.46), g_y, g_w, g_h)
    gc1.fill.solid()
    gc1.fill.fore_color.rgb = C_DARK_CARD
    gc1.line.color.rgb = C_DARK_BORDER
    gc1.line.width = Pt(1)

    tb = s4.shapes.add_textbox(Inches(0.65), g_y + Inches(0.18), g_w - Inches(0.40), g_h - Inches(0.36))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "CALL BUDGET & MODEL RESTRICTION"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_ACCENT
    p = tf.add_paragraph()
    p.text = "3 Calls Per Triage Pass"
    p.font.name = FONT_HEAD
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = C_DARK_INK
    p.space_after = Pt(8)
    p = tf.add_paragraph()
    p.text = "1. Planner proposes typed tool actions.\n2. Vision model inspects keyframes (fallible observation).\n3. Critic evaluates citations against policy.\n\nCase C re-upload triggers Pass 2 (max 6 calls total). Models never access payment APIs directly."
    p.font.name = FONT_HEAD
    p.font.size = Pt(11)
    p.font.color.rgb = C_DARK_MUTED

    # Pillar 2: Case C Stateful Resumption Diagram & P-06 Failure
    gc2 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.69), g_y, g_w, g_h)
    gc2.fill.solid()
    gc2.fill.fore_color.rgb = RGBColor(0x14, 0x28, 0x22)
    gc2.line.color.rgb = C_TEAL
    gc2.line.width = Pt(1.5)

    tb = s4.shapes.add_textbox(Inches(4.88), g_y + Inches(0.18), g_w - Inches(0.40), g_h - Inches(0.36))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "STATEFUL RESUMPTION (CASE C)"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_ACCENT
    p = tf.add_paragraph()
    p.text = "Clarification & Re-Film Loop"
    p.font.name = FONT_HEAD
    p.font.size = Pt(16.5)
    p.font.bold = True
    p.font.color.rgb = C_DARK_INK
    p.space_after = Pt(6)
    p = tf.add_paragraph()
    p.text = "Low-light video (Policy P-06 FAIL, brightness score: 28/255 < threshold 50/255) triggers ask_for_evidence().\n\nState saves to WAITING_FOR_EVIDENCE → Resumes on upload.\n\nTERMINATION RULE: After 1 retry, escalates to seller with both attempts logged (never auto-denies)."
    p.font.name = FONT_HEAD
    p.font.size = Pt(10.5)
    p.font.color.rgb = RGBColor(0xD2, 0xE5, 0xDC)

    # Pillar 3: Secondary Fast Path (Zero-LLM Order Route)
    gc3 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.92), g_y, g_w, g_h)
    gc3.fill.solid()
    gc3.fill.fore_color.rgb = C_DARK_CARD
    gc3.line.color.rgb = C_DARK_BORDER
    gc3.line.width = Pt(1)

    tb = s4.shapes.add_textbox(Inches(9.11), g_y + Inches(0.18), g_w - Inches(0.40), g_h - Inches(0.36))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "ZERO-LLM FAST PATH"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_ACCENT
    p = tf.add_paragraph()
    p.text = "Zero-LLM Order Route"
    p.font.name = FONT_HEAD
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = C_DARK_INK
    p.space_after = Pt(8)
    p = tf.add_paragraph()
    p.text = "For routine \"Where is my order?\" inquiries, deterministic code regex routes directly to APIs:\n\nStore API → Courier API → Status Reply\n\nZero LLM tokens · Zero vision overhead · <500ms response."
    p.font.name = FONT_HEAD
    p.font.size = Pt(11)
    p.font.color.rgb = C_DARK_MUTED

    # Bottom Technical Banner
    ban_y = g_y + g_h + Inches(0.16)
    ban = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.46), ban_y, Inches(12.41), Inches(0.80))
    ban.fill.solid()
    ban.fill.fore_color.rgb = RGBColor(0x11, 0x22, 0x1D)
    ban.line.color.rgb = C_DARK_BORDER
    ban.line.width = Pt(1)

    tb_ban = s4.shapes.add_textbox(Inches(0.65), ban_y + Inches(0.10), Inches(12.0), Inches(0.60))
    tf_ban = tb_ban.text_frame
    p = tf_ban.paragraphs[0]
    p.text = "FAIL-CLOSED FINANCIAL GATE: requires_seller_approval: true · Approval binds case + evidence hash + policy version + nonce."
    p.font.name = FONT_MONO
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_GOLD_TEXT
    p = tf_ban.add_paragraph()
    p.text = f"Server Cap: 0 < amount <= min({meta['refund_guardrail']['ceiling']}, remaining_refundable, order_paid) · Idempotency key enforced."
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.color.rgb = C_DARK_MUTED

    add_footer(s4, 4, dark=True)
    add_notes(s4, d4["speaker_notes"])

    # =========================================================
    # SLIDE 5: 4 EVALUATION SCENARIOS (EVALUATIVE BEHAVIORAL MATRIX)
    # =========================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5, C_PAPER)
    d5 = slides_data[5]

    tb = s5.shapes.add_textbox(Inches(0.46), Inches(0.36), Inches(12.0), Inches(0.25))
    p = tb.text_frame.paragraphs[0]
    p.text = d5.get("tag", "DEMO SCENARIOS · BEHAVIORAL MATRIX")
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    tb = s5.shapes.add_textbox(Inches(0.46), Inches(0.65), Inches(12.4), Inches(0.85))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = d5.get("headline", "Different evidence. Different action.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = C_INK
    p = tf.add_paragraph()
    p.text = d5.get("subheadline", "Four distinct triage behaviors across reproducible test fixtures. Zero automated policy approvals.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(15.5)
    p.font.color.rgb = C_MUTED

    # 4-Column Balanced Behavioral Matrix
    card_y = Inches(1.68)
    card_w = Inches(2.95)
    card_h = Inches(5.08)

    matrix_cases = [
        ("01", "CASE A · CONSISTENT", "PREPARE REVIEW", C_TEAL_LIGHT, C_TEAL_DARK, C_TEAL,
         "Manifest matches catalog\nPackaging tag verified (P-02)\nCosmetic defect observed\nWithin 7-day window (P-04)",
         "Drafts return shipping label & refund draft in pending_return_receipt.\n\nMoney releases only upon physical warehouse parcel receipt."),
        ("02", "CASE B · CONTRADICTION", "ESCALATE SELLER", C_CORAL_LIGHT, C_CORAL_DARK, C_CORAL,
         "Ordered Matte White\nObserved Black casing (Frame 00:07)\nExact SKU unverified\nBarcode unverified",
         "Policy P-03 FAIL blocks automation. Inhibits label and refund draft.\n\nSurfaces 3 seller options: mis-shipment / box label / physical inspection."),
        ("03", "CASE C · LOW LIGHT", "CLARIFY LOOP", C_AMBER_LIGHT, C_AMBER_DARK, C_AMBER,
         "4s low-light unboxing video\nBrightness score: 28/255 < 50/255\nBarcode obscured\nOnly 2 usable frames",
         "Policy P-06 FAIL triggers ask_for_evidence().\n\nState saves to WAITING_FOR_EVIDENCE; resumes on upload. Max 1 retry; 2nd failure escalates (never auto-denies)."),
        ("04", "CASE D · CONTINUOUS", "INSPECT SEQUENCE", C_PAPER_TINT, C_INK_LIGHT, C_MUTED,
         "Single unbroken unboxing take\nSealed parcel to product display\nContinuity inspection\nFlags abrupt transitions",
         "Inspects sequence continuity and flags abrupt cuts.\n\nBasic continuity in prototype; advanced forensics is cut first. Does not claim proof of item authenticity.")
    ]

    for idx, (num, title, badge, bg_col, txt_col, border_col, ev_text, out_text) in enumerate(matrix_cases):
        cx = Inches(0.46 + idx * 3.15)
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, card_y, card_w, card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = border_col
        card.line.width = Pt(1.5)

        # Header Pill
        hpill = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx + Inches(0.15), card_y + Inches(0.15), card_w - Inches(0.30), Inches(0.42))
        hpill.fill.solid()
        hpill.fill.fore_color.rgb = bg_col
        hpill.line.width = 0
        p_hp = hpill.text_frame.paragraphs[0]
        p_hp.alignment = PP_ALIGN.CENTER
        p_hp.text = f"{num} · {badge}"
        p_hp.font.name = FONT_MONO
        p_hp.font.size = Pt(10)
        p_hp.font.bold = True
        p_hp.font.color.rgb = txt_col

        tb_c = s5.shapes.add_textbox(cx + Inches(0.18), card_y + Inches(0.68), card_w - Inches(0.36), card_h - Inches(0.80))
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0

        p = tf_c.paragraphs[0]
        p.text = title
        p.font.name = FONT_HEAD
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_INK
        p.space_after = Pt(8)

        p = tf_c.add_paragraph()
        p.text = "EVIDENCE PROFILE:"
        p.font.name = FONT_MONO
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = C_TEAL_DARK
        p.space_after = Pt(2)

        p = tf_c.add_paragraph()
        p.text = ev_text
        p.font.name = FONT_HEAD
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_INK_LIGHT
        p.space_after = Pt(10)

        p = tf_c.add_paragraph()
        p.text = "POLICY ENGINE ACTION:"
        p.font.name = FONT_MONO
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = txt_col
        p.space_after = Pt(2)

        p = tf_c.add_paragraph()
        p.text = out_text
        p.font.name = FONT_HEAD
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_MUTED

    add_footer(s5, 5)
    add_notes(s5, d5["speaker_notes"])

    # =========================================================
    # SLIDE 6: 24-HOUR PROTOTYPE PLAN & SCOPE
    # =========================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6, C_PAPER)
    d6 = slides_data[6]

    tb = s6.shapes.add_textbox(Inches(0.46), Inches(0.36), Inches(12.0), Inches(0.25))
    p = tb.text_frame.paragraphs[0]
    p.text = "24-HOUR PROTOTYPE PLAN · TEAM ROOKIE (3 MEMBERS)"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    tb = s6.shapes.add_textbox(Inches(0.46), Inches(0.65), Inches(12.4), Inches(0.85))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = d6.get("headline", "A credible prototype in 24 hours.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = C_INK
    p = tf.add_paragraph()
    p.text = d6.get("subheadline", "Strict scope boundaries and single-threaded ownership make the prototype buildable in one day.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(15.5)
    p.font.color.rgb = C_MUTED

    # High-Quality Horizontal Roadmap Timeline (00-24h)
    t_y = Inches(1.65)
    t_h = Inches(1.22)
    t_bar = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.46), t_y, Inches(12.41), t_h)
    t_bar.fill.solid()
    t_bar.fill.fore_color.rgb = C_WHITE
    t_bar.line.color.rgb = C_BORDER_STRONG
    t_bar.line.width = Pt(1)

    t_slots = [
        ("00 – 06h", "Foundation", "Mock Store/Shippo APIs · LangGraph state schema · Zero-LLM fast path"),
        ("06 – 12h", "Evidence Pipeline", "FFmpeg ~1fps extractor · Vision observation schema · Seller Console UI"),
        ("12 – 18h", "Integration", "Case C pause/resume loop · 4 test fixtures (A–D) · Adversarial critic review"),
        ("18 – 24h", "Validation & Safety", "Fail-closed authorization tests · 10-test smoke suite · Video demo recording")
    ]
    for idx, (hrs, phase, desc) in enumerate(t_slots):
        tx = Inches(0.65 + idx * 3.08)

        mbadge = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, tx, t_y + Inches(0.12), Inches(1.65), Inches(0.24))
        mbadge.fill.solid()
        mbadge.fill.fore_color.rgb = C_TEAL_LIGHT
        mbadge.line.width = 0
        p = mbadge.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = f"{hrs} · PHASE 0{idx+1}"
        p.font.name = FONT_MONO
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = C_TEAL_DARK

        tb = s6.shapes.add_textbox(tx, t_y + Inches(0.38), Inches(2.95), Inches(0.76))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = phase
        p.font.name = FONT_HEAD
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_INK
        p = tf.add_paragraph()
        p.text = desc
        p.font.name = FONT_HEAD
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_MUTED

        if idx < 3:
            div = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.65 + (idx + 1) * 3.08 - 0.15), t_y + Inches(0.18), Inches(0.015), Inches(0.86))
            div.fill.solid()
            div.fill.fore_color.rgb = C_BORDER
            div.line.width = 0

    # 3 Enriched Person Cards: Exactly 4 Concrete Deliverables Each & Clear Tech Stacks
    p_y = Inches(3.05)
    p_w = Inches(3.95)
    p_h = Inches(2.48)

    people = [
        ("PERSON A · BACKEND, POLICY & AUTH", "State Machine & Policy Engine",
         "Stack: LangGraph · Pydantic · SQLite · SHA256",
         [
             "• Policy P-01 to P-08: Deterministic code rules (window, SKU, tag, refund cap)",
             "• Zero-LLM Fast Path: Deterministic regex routing for order status queries",
             "• Audit Ledger: Append-only JSON log & signed approval binding",
             "• Financial Cap: Server calculation min(₹4,999, remaining, paid)"
         ]),
        ("PERSON B · VISION & CONSOLE", "Video Pipeline & Seller UI",
         "Stack: FFmpeg · Hosted vision model (unpinned) · HTML/CSS/SVG",
         [
             "• Keyframe Pipeline: Uniform ~1fps sampling & brightness scoring (threshold 50/255)",
             "• Structured Vision: Observation schema with timestamp citation metadata",
             "• Adversarial Critic: Cross-checks citations against keyframe timestamps",
             "• Seller Console: 1-click decision console with mock evidence pack"
         ]),
        ("PERSON C · FIXTURES & QA", "Scenarios, Lifecycle & QA",
         "Stack: Pytest · Mock Fixtures · Automated Smoke QA",
         [
             "• Benchmark Cases: Staged fixtures for 4 demo cases (A–D)",
             "• Case C Lifecycle: Re-film loop in WAITING_FOR_EVIDENCE (1 retry max)",
             "• Fail-Closed Testing: Verifies zero automated refunds & approval gates",
             "• Automated QA: 10-test smoke suite, boundary verification & demo recording"
         ])
    ]

    for idx, (role, name, stack, deliverables) in enumerate(people):
        px = Inches(0.46 + idx * 4.23)
        pc = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, p_y, p_w, p_h)
        pc.fill.solid()
        pc.fill.fore_color.rgb = C_PAPER
        pc.line.color.rgb = C_BORDER
        pc.line.width = Pt(1)

        tb = s6.shapes.add_textbox(px + Inches(0.18), p_y + Inches(0.12), p_w - Inches(0.36), p_h - Inches(0.20))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = role
        p.font.name = FONT_MONO
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = C_TEAL
        p = tf.add_paragraph()
        p.text = name
        p.font.name = FONT_HEAD
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = C_INK
        p = tf.add_paragraph()
        p.text = stack
        p.font.name = FONT_MONO
        p.font.size = Pt(8.5)
        p.font.color.rgb = C_MUTED
        p.space_after = Pt(2)
        for item in deliverables:
            p = tf.add_paragraph()
            p.text = item
            p.font.name = FONT_HEAD
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_INK_LIGHT
            p.space_after = Pt(1.5)

    # Bottom Scope Discipline Band
    sc_y = Inches(5.58)
    sc_h = Inches(1.22)
    sc = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.46), sc_y, Inches(12.41), sc_h)
    sc.fill.solid()
    sc.fill.fore_color.rgb = C_INK
    sc.line.width = 0

    tb_sc1 = s6.shapes.add_textbox(Inches(0.65), sc_y + Inches(0.10), Inches(4.50), Inches(1.02))
    tf1 = tb_sc1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0
    p = tf1.paragraphs[0]
    p.text = "MUST DELIVER (CORE PROTOTYPE)"
    p.font.name = FONT_MONO
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_GOLD_TEXT
    p = tf1.add_paragraph()
    p.text = "Mock APIs · Policy engine · 4 benchmark cases (A–D) · Approval binding · Seller gate · Zero-LLM fast path"
    p.font.name = FONT_HEAD
    p.font.size = Pt(11.5)
    p.font.color.rgb = RGBColor(0xDF, 0xEA, 0xE5)

    tb_sc2 = s6.shapes.add_textbox(Inches(5.40), sc_y + Inches(0.10), Inches(4.20), Inches(1.02))
    tf2 = tb_sc2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0
    p = tf2.paragraphs[0]
    p.text = "CUT FIRST IF BEHIND"
    p.font.name = FONT_MONO
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0xFF, 0x8C, 0x69)
    p = tf2.add_paragraph()
    p.text = "Advanced video forensics (Case D stretch) · WhatsApp bot · Exchanges · Multi-seller auth · Audio analysis · Public cloud deployment"
    p.font.name = FONT_HEAD
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(0xDF, 0xEA, 0xE5)

    tb_sc3 = s6.shapes.add_textbox(Inches(9.80), sc_y + Inches(0.10), Inches(2.90), Inches(1.02))
    tf3 = tb_sc3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = tf3.margin_top = tf3.margin_right = tf3.margin_bottom = 0
    p = tf3.paragraphs[0]
    p.text = "PROTOTYPE SCOPE LOCKED"
    p.font.name = FONT_MONO
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_ACCENT
    p = tf3.add_paragraph()
    p.text = "100% reproducible offline build · Zero external network dependencies"
    p.font.name = FONT_HEAD
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(0xDF, 0xEA, 0xE5)

    add_footer(s6, 6)
    add_notes(s6, d6["speaker_notes"])

    # Save PPTX initially to temporary location
    temp_pptx = deliverables_dir / "temp_build_v7_2.pptx"
    prs.save(temp_pptx)

    # Deterministic Packaging Pipeline (ZIP_STORED Packaging)
    pptx_deliv = deliverables_dir / "ReturnLens_v7_2.pptx"
    pptx_root = base_dir / "ReturnLens_v7_2.pptx"

    fixed_time = (2026, 10, 31, 12, 0, 0)
    with zipfile.ZipFile(temp_pptx, 'r') as zin:
        with zipfile.ZipFile(pptx_deliv, 'w') as zout:
            for item in sorted(zin.infolist(), key=lambda x: x.filename):
                data = zin.read(item.filename)
                new_info = zipfile.ZipInfo(item.filename, date_time=fixed_time)
                new_info.compress_type = zipfile.ZIP_STORED
                new_info.create_system = 0
                new_info.external_attr = 0o644 << 16
                zout.writestr(new_info, data)

    if temp_pptx.exists():
        temp_pptx.unlink()

    shutil.copy2(pptx_deliv, pptx_root)
    print(f"Generated ReturnLens_v7_2.pptx successfully: {pptx_deliv} ({os.path.getsize(pptx_deliv)} bytes)")

if __name__ == "__main__":
    build_v7_2_pptx()
