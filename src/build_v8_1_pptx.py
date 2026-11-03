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

def build_v8_1_pptx():
    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / "content" / "deck_data_v8_1.json"
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

    # ReturnLens v8.1 Palette (Restrained Warm Paper, Forest Ink, Pine Teal, Terracotta Coral, Amber)
    C_PAPER = RGBColor(0xFA, 0xF8, 0xF5)          # Warm Paper canvas (#FAF8F5)
    C_PAPER_TINT = RGBColor(0xF3, 0xEF, 0xE9)     # Subtle Warm Tint
    C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)          # Crisp card surface
    C_INK = RGBColor(0x13, 0x22, 0x1B)            # Forest Ink headline (#13221B)
    C_INK_LIGHT = RGBColor(0x2D, 0x3E, 0x35)      # Charcoal body
    C_MUTED = RGBColor(0x5E, 0x73, 0x68)          # Sage Muted
    C_BORDER = RGBColor(0xE5, 0xE0, 0xD8)         # Soft card border
    C_BORDER_STRONG = RGBColor(0xD0, 0xC8, 0xBD)  # Strong card border

    # Accents
    C_TEAL = RGBColor(0x0C, 0x5E, 0x4B)           # Pine Teal (#0C5E4B)
    C_TEAL_DARK = RGBColor(0x08, 0x43, 0x35)      # Deep Pine
    C_TEAL_TINT = RGBColor(0xEE, 0xF7, 0xF4)     # Soft Mint
    C_TEAL_BORDER = RGBColor(0xBD, 0xE3, 0xD7)   # Mint Border

    C_CORAL = RGBColor(0xC8, 0x4D, 0x33)          # Terracotta Coral (#C84D33)
    C_CORAL_DARK = RGBColor(0x9E, 0x2A, 0x2B)     # Deep Coral
    C_CORAL_TINT = RGBColor(0xFD, 0xF3, 0xF1)    # Blush Coral Tint
    C_CORAL_BORDER = RGBColor(0xF6, 0xC6, 0xBD)   # Coral Border

    C_AMBER = RGBColor(0xD9, 0x77, 0x06)          # Amber Accent
    C_AMBER_DARK = RGBColor(0x92, 0x40, 0x0E)     # Deep Amber
    C_AMBER_TINT = RGBColor(0xFE, 0xF3, 0xC7)    # Amber Tint

    # Typography
    FONT_HEAD = "Segoe UI"
    FONT_BODY = "Segoe UI"
    FONT_MONO = "Consolas"

    # Images (1376x768, 16:9 ratio = 1.79167)
    img_white_order = assets_dir / "studio_white_headphones.jpg"
    img_black_unboxing = assets_dir / "unboxing_black_headphones.jpg"

    def set_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.width = 0
        return bg

    def add_footer(slide, current_num):
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.65), Inches(6.95), Inches(12.03), Inches(0.015))
        line.fill.solid()
        line.fill.fore_color.rgb = C_BORDER
        line.line.width = 0

        tb = slide.shapes.add_textbox(Inches(0.65), Inches(7.02), Inches(8.0), Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = "RETURNLENS V8.1 · AGENTX HACKATHON 2026 PS-04 · IDEA ROUND"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_MUTED

        tb_num = slide.shapes.add_textbox(Inches(11.68), Inches(7.02), Inches(1.0), Inches(0.3))
        tf_num = tb_num.text_frame
        tf_num.margin_left = tf_num.margin_top = tf_num.margin_right = tf_num.margin_bottom = 0
        p_num = tf_num.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.text = f"0{current_num} / 06"
        p_num.font.name = FONT_BODY
        p_num.font.size = Pt(9.5)
        p_num.font.bold = True
        p_num.font.color.rgb = C_TEAL

    def add_notes(slide, text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = text

    # =========================================================
    # SLIDE 1: PRODUCT INTRODUCTION & SELLER CONSOLE
    # =========================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1, C_PAPER)
    d1 = slides_data[1]

    # Category Tag
    tb_tag = s1.shapes.add_textbox(Inches(0.65), Inches(0.40), Inches(4.30), Inches(0.25))
    tf = tb_tag.text_frame
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = d1.get("kicker", "AGENTX HACKATHON 2026 · TRACK PS-04")
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    # Left Column: Brand Story & Trimmed Product Description
    tb_left = s1.shapes.add_textbox(Inches(0.65), Inches(0.70), Inches(4.30), Inches(4.20))
    tf_l = tb_left.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0

    p = tf_l.paragraphs[0]
    p.text = d1.get("title", "ReturnLens")
    p.font.name = FONT_HEAD
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = C_INK
    p.space_after = Pt(6)

    p = tf_l.add_paragraph()
    p.text = d1.get("subtitle", "Every return decision, backed by evidence.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p.space_after = Pt(12)

    p = tf_l.add_paragraph()
    p.text = d1.get("summary", "An evidence-backed triage assistant that connects customer claims, unboxing footage, and store records into a clear decision pack for solo online merchants.")
    p.font.name = FONT_BODY
    p.font.size = Pt(16)
    p.font.color.rgb = C_INK_LIGHT

    # Design Principle Card (Left bottom: reduced height, increased bottom padding, plain merchant language)
    left_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.65), Inches(5.05), Inches(4.30), Inches(1.45))
    left_box.fill.solid()
    left_box.fill.fore_color.rgb = C_TEAL_TINT
    left_box.line.color.rgb = C_TEAL_BORDER
    left_box.line.width = Pt(1.5)

    tb_lb = s1.shapes.add_textbox(Inches(0.85), Inches(5.15), Inches(3.90), Inches(1.25))
    tf_lb = tb_lb.text_frame
    tf_lb.word_wrap = True
    tf_lb.margin_left = tf_lb.margin_top = tf_lb.margin_right = tf_lb.margin_bottom = 0
    p = tf_lb.paragraphs[0]
    p.text = d1["principle_card"]["title"]
    p.font.name = FONT_BODY
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_DARK
    p.space_after = Pt(3)

    p = tf_lb.add_paragraph()
    p.text = d1["principle_card"]["quote"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(16.5)
    p.font.bold = True
    p.font.color.rgb = C_INK
    p.space_after = Pt(4)

    p = tf_lb.add_paragraph()
    p.text = d1["principle_card"]["rule"]
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CORAL_DARK

    # Right Column: Spacious macOS Seller Console Mockup
    c_x, c_y, c_w, c_h = Inches(5.25), Inches(0.65), Inches(7.43), Inches(5.85)

    # Window Container
    win = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x, c_y, c_w, c_h)
    win.fill.solid()
    win.fill.fore_color.rgb = C_WHITE
    win.line.color.rgb = C_BORDER_STRONG
    win.line.width = Pt(1.5)

    # Window Header Bar
    bar_h = Inches(0.42)
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_x, c_y, c_w, bar_h)
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_INK
    bar.line.width = 0

    # Traffic light dots
    for i, col in enumerate([RGBColor(0xFF, 0x5F, 0x56), RGBColor(0xFF, 0xBD, 0x2E), RGBColor(0x27, 0xC9, 0x3F)]):
        dot = s1.shapes.add_shape(MSO_SHAPE.OVAL, c_x + Inches(0.20 + i * 0.18), c_y + Inches(0.14), Inches(0.12), Inches(0.12))
        dot.fill.solid()
        dot.fill.fore_color.rgb = col
        dot.line.width = 0

    tb_bar = s1.shapes.add_textbox(c_x + Inches(0.85), c_y + Inches(0.08), c_w - Inches(1.0), Inches(0.28))
    tf_b = tb_bar.text_frame
    tf_b.margin_left = tf_b.margin_top = 0
    p = tf_b.paragraphs[0]
    p.text = d1.get("console_title", "RETURNLENS SELLER CONSOLE · CASE #RT-8821")
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0xEE, 0xF7, 0xF4)

    # Sub-bar: Order Facts in 1 clean line
    sub_y = c_y + bar_h
    sub_h = Inches(0.36)
    sub = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_x, sub_y, c_w, sub_h)
    sub.fill.solid()
    sub.fill.fore_color.rgb = C_PAPER_TINT
    sub.line.color.rgb = C_BORDER
    sub.line.width = Pt(1)

    tb_sub = s1.shapes.add_textbox(c_x + Inches(0.20), sub_y + Inches(0.06), c_w - Inches(0.40), Inches(0.26))
    tf_s = tb_sub.text_frame
    tf_s.margin_left = tf_s.margin_top = 0
    p = tf_s.paragraphs[0]
    p.text = "Order #ORD-7729 · Studio Wireless · ₹1,499 paid · Delivered 4d ago (Within 7-day window)"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_INK

    # Side-by-side Evidence Cards (Aspect ratio strictly locked: 16:9!)
    card_y = sub_y + sub_h + Inches(0.12)
    card_w = Inches(3.42)
    card_h = Inches(3.00)

    # Left Split Card (Store Truth)
    card_l = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x + Inches(0.20), card_y, card_w, card_h)
    card_l.fill.solid()
    card_l.fill.fore_color.rgb = C_PAPER
    card_l.line.color.rgb = C_BORDER
    card_l.line.width = Pt(1)

    # Image: 16:9 ratio locked (w=3.02, h=1.69)
    if img_white_order.exists():
        s1.shapes.add_picture(str(img_white_order), c_x + Inches(0.40), card_y + Inches(0.12), Inches(3.02), Inches(1.69))

    tb_cl = s1.shapes.add_textbox(c_x + Inches(0.30), card_y + Inches(1.88), card_w - Inches(0.20), Inches(1.05))
    tf_cl = tb_cl.text_frame
    tf_cl.word_wrap = True
    tf_cl.margin_left = tf_cl.margin_top = 0
    p = tf_cl.paragraphs[0]
    p.text = d1["store_truth"]["title"]
    p.font.name = FONT_BODY
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_DARK
    p = tf_cl.add_paragraph()
    p.text = d1["store_truth"]["sku"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_INK
    p = tf_cl.add_paragraph()
    p.text = "Shippo #SH-9012 verified · Security tag required"
    p.font.name = FONT_BODY
    p.font.size = Pt(10.5)
    p.font.color.rgb = C_MUTED

    # Right Split Card (Observed Keyframe)
    card_r = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x + Inches(3.81), card_y, card_w, card_h)
    card_r.fill.solid()
    card_r.fill.fore_color.rgb = C_CORAL_TINT
    card_r.line.color.rgb = C_CORAL_BORDER
    card_r.line.width = Pt(1.5)

    if img_black_unboxing.exists():
        s1.shapes.add_picture(str(img_black_unboxing), c_x + Inches(4.01), card_y + Inches(0.12), Inches(3.02), Inches(1.69))

    tb_cr = s1.shapes.add_textbox(c_x + Inches(3.91), card_y + Inches(1.88), card_w - Inches(0.20), Inches(1.05))
    tf_cr = tb_cr.text_frame
    tf_cr.word_wrap = True
    tf_cr.margin_left = tf_cr.margin_top = 0
    p = tf_cr.paragraphs[0]
    p.text = d1["observed_evidence"]["title"]
    p.font.name = FONT_BODY
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_CORAL_DARK
    p = tf_cr.add_paragraph()
    p.text = d1["observed_evidence"]["observation"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CORAL_DARK
    p = tf_cr.add_paragraph()
    p.text = d1["observed_evidence"]["meta"]
    p.font.name = FONT_BODY
    p.font.size = Pt(10.5)
    p.font.color.rgb = C_INK_LIGHT

    # Discrepancy Notice Strip
    ban_y = card_y + card_h + Inches(0.10)
    ban_h = Inches(0.50)
    ban = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x + Inches(0.20), ban_y, c_w - Inches(0.40), ban_h)
    ban.fill.solid()
    ban.fill.fore_color.rgb = C_INK
    ban.line.color.rgb = C_BORDER
    ban.line.width = Pt(1)

    tb_ban = s1.shapes.add_textbox(c_x + Inches(0.35), ban_y + Inches(0.06), c_w - Inches(0.70), ban_h - Inches(0.12))
    tf_ban = tb_ban.text_frame
    tf_ban.word_wrap = True
    tf_ban.margin_left = tf_ban.margin_top = 0
    p = tf_ban.paragraphs[0]
    p.text = d1.get("discrepancy_notice", "Color discrepancy: Ordered Matte White; video shows Black casing. Barcode unverified.")
    p.font.name = FONT_BODY
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0xFF, 0xD4, 0x85)
    p = tf_ban.add_paragraph()
    p.text = "Prepared 3 resolution choices for merchant authorization."
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.color.rgb = RGBColor(0xDF, 0xEA, 0xE5)

    # Action Bar: Seller authorizes returns, labels & refunds
    act_y = ban_y + ban_h + Inches(0.10)
    tb_act = s1.shapes.add_textbox(c_x + Inches(0.20), act_y + Inches(0.04), Inches(4.00), Inches(0.40))
    tf_a = tb_act.text_frame
    tf_a.margin_left = tf_a.margin_top = 0
    p = tf_a.paragraphs[0]
    p.text = d1.get("action_label", "Seller authorizes returns, labels & refunds")
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_AMBER_DARK
    p = tf_a.add_paragraph()
    p.text = "No automated refund or denial"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_MUTED

    btn_pri = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x + Inches(4.30), act_y, Inches(2.93), Inches(0.44))
    btn_pri.fill.solid()
    btn_pri.fill.fore_color.rgb = C_TEAL
    btn_pri.line.color.rgb = C_TEAL_DARK
    btn_pri.line.width = Pt(1)
    p = btn_pri.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = d1.get("primary_button", "Review Evidence & Decide →")
    p.font.name = FONT_HEAD
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    add_footer(s1, 1)
    add_notes(s1, d1["speaker_notes"])

    # =========================================================
    # SLIDE 2: THE PROBLEM (A SELLER'S DECISION PROBLEM)
    # =========================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2, C_PAPER)
    d2 = slides_data[2]

    # Kicker
    tb = s2.shapes.add_textbox(Inches(0.65), Inches(0.40), Inches(12.0), Inches(0.25))
    p = tb.text_frame.paragraphs[0]
    p.text = d2.get("kicker", "THE SELLER'S DILEMMA · SOLO D2C BOTTLENECK")
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CORAL

    # Title & Subtitle
    tb = s2.shapes.add_textbox(Inches(0.65), Inches(0.70), Inches(12.03), Inches(0.85))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = d2.get("title", "One customer claim. Four disconnected sources.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(34)
    p.font.bold = True
    p.font.color.rgb = C_INK
    p = tf.add_paragraph()
    p.text = d2.get("subtitle", "A solo merchant must piece together fragmented records before deciding how to respond.")
    p.font.name = FONT_BODY
    p.font.size = Pt(20)
    p.font.color.rgb = C_MUTED

    # 1. Incoming Customer Claim Card (Trimmed, generous internal padding)
    claim_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.65), Inches(1.70), Inches(12.03), Inches(1.15))
    claim_box.fill.solid()
    claim_box.fill.fore_color.rgb = C_WHITE
    claim_box.line.color.rgb = C_BORDER_STRONG
    claim_box.line.width = Pt(1.5)

    tb_cl = s2.shapes.add_textbox(Inches(0.90), Inches(1.80), Inches(11.53), Inches(0.95))
    tf_c = tb_cl.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_top = 0
    p = tf_c.paragraphs[0]
    p.text = d2["incoming_claim"]["title"]
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CORAL
    p.space_after = Pt(2)

    p = tf_c.add_paragraph()
    p.text = d2["incoming_claim"]["message"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(19)
    p.font.bold = True
    p.font.color.rgb = C_INK
    p.space_after = Pt(2)

    p = tf_c.add_paragraph()
    p.text = d2["incoming_claim"]["attachment"]
    p.font.name = FONT_BODY
    p.font.size = Pt(12.5)
    p.font.color.rgb = C_MUTED

    # 2. Four Disconnected Sources (4 horizontal cards)
    sources_y = Inches(3.05)
    source_w = Inches(2.85)
    source_gap = Inches(0.21)
    source_h = Inches(1.80)

    for i, src in enumerate(d2["sources"]):
        sx = Inches(0.65) + i * (source_w + source_gap)
        scard = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx, sources_y, source_w, source_h)
        scard.fill.solid()
        scard.fill.fore_color.rgb = C_WHITE
        scard.line.color.rgb = C_BORDER
        scard.line.width = Pt(1)

        tb_s = s2.shapes.add_textbox(sx + Inches(0.18), sources_y + Inches(0.18), source_w - Inches(0.36), source_h - Inches(0.36))
        tf_s = tb_s.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_top = 0
        p = tf_s.paragraphs[0]
        p.text = src["name"]
        p.font.name = FONT_HEAD
        p.font.size = Pt(17)
        p.font.bold = True
        p.font.color.rgb = C_TEAL_DARK
        p.space_after = Pt(8)

        p = tf_s.add_paragraph()
        p.text = src["detail"]
        p.font.name = FONT_BODY
        p.font.size = Pt(14)
        p.font.color.rgb = C_INK_LIGHT

    # 3. Bottom Decision Question Card (Crisp decision question)
    dil_y = Inches(5.05)
    dil_h = Inches(1.40)
    dil = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.65), dil_y, Inches(12.03), dil_h)
    dil.fill.solid()
    dil.fill.fore_color.rgb = C_CORAL_TINT
    dil.line.color.rgb = C_CORAL_BORDER
    dil.line.width = Pt(1.5)

    tb_dil = s2.shapes.add_textbox(Inches(0.90), dil_y + Inches(0.16), Inches(11.53), dil_h - Inches(0.32))
    tf_d = tb_dil.text_frame
    tf_d.word_wrap = True
    tf_d.margin_left = tf_d.margin_top = 0
    p = tf_d.paragraphs[0]
    p.text = "THE SELLER'S QUESTION:"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CORAL_DARK
    p.space_after = Pt(4)

    p = tf_d.add_paragraph()
    p.text = d2.get("decision_question", "Packing mistake, delivery error, or unboxing swap? The seller needs verified facts before deciding to refund, replace, or inspect.")
    p.font.name = FONT_BODY
    p.font.size = Pt(17)
    p.font.color.rgb = C_INK

    add_footer(s2, 2)
    add_notes(s2, d2["speaker_notes"])

    # =========================================================
    # SLIDE 3: THE CORE DEMONSTRATION (NO OVERLAP, 16:9 LOCKED)
    # =========================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3, C_PAPER)
    d3 = slides_data[3]

    # Kicker
    tb = s3.shapes.add_textbox(Inches(0.65), Inches(0.40), Inches(12.0), Inches(0.25))
    p = tb.text_frame.paragraphs[0]
    p.text = d3.get("kicker", "CORE DEMONSTRATION · STAGED CONCEPT SCENARIO")
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    # Title & Subtitle
    tb = s3.shapes.add_textbox(Inches(0.65), Inches(0.70), Inches(12.03), Inches(0.85))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = d3.get("title", "The order says white. The video shows black.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(34)
    p.font.bold = True
    p.font.color.rgb = C_INK
    p = tf.add_paragraph()
    p.text = d3.get("subtitle", "ReturnLens highlights the visible difference without jumping to unverified conclusions.")
    p.font.name = FONT_BODY
    p.font.size = Pt(20)
    p.font.color.rgb = C_MUTED

    # Two Large Showcase Cards: Card ends at y=5.05, perfectly clear of lower strip!
    demo_y = Inches(1.68)
    card_w3 = Inches(5.86)
    card_h3 = Inches(3.35)

    # Left Showcase Card (Shopify Order)
    card_l3 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.65), demo_y, card_w3, card_h3)
    card_l3.fill.solid()
    card_l3.fill.fore_color.rgb = C_WHITE
    card_l3.line.color.rgb = C_BORDER
    card_l3.line.width = Pt(1.5)

    tb_lh = s3.shapes.add_textbox(Inches(0.85), demo_y + Inches(0.10), card_w3 - Inches(0.40), Inches(0.26))
    p = tb_lh.text_frame.paragraphs[0]
    p.text = d3["left_card"]["header"]
    p.font.name = FONT_BODY
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_DARK

    # Image: 16:9 ratio locked (w=4.40", h=2.46")
    img_w3 = Inches(4.40)
    img_h3 = Inches(2.46)
    img_x_l = Inches(0.65) + (card_w3 - img_w3) / 2
    if img_white_order.exists():
        s3.shapes.add_picture(str(img_white_order), img_x_l, demo_y + Inches(0.38), img_w3, img_h3)

    tb_lc = s3.shapes.add_textbox(Inches(0.85), demo_y + Inches(2.88), card_w3 - Inches(0.40), Inches(0.45))
    tf_lc = tb_lc.text_frame
    tf_lc.word_wrap = True
    tf_lc.margin_left = tf_lc.margin_top = 0
    p = tf_lc.paragraphs[0]
    p.text = d3["left_card"]["color_headline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(21)
    p.font.bold = True
    p.font.color.rgb = C_INK
    p.space_after = Pt(1)
    p = tf_lc.add_paragraph()
    p.text = d3["left_card"]["product_line"]
    p.font.name = FONT_BODY
    p.font.size = Pt(12)
    p.font.color.rgb = C_MUTED

    # Right Showcase Card (Unboxing Video)
    card_r3 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.82), demo_y, card_w3, card_h3)
    card_r3.fill.solid()
    card_r3.fill.fore_color.rgb = C_CORAL_TINT
    card_r3.line.color.rgb = C_CORAL_BORDER
    card_r3.line.width = Pt(1.5)

    tb_rh = s3.shapes.add_textbox(Inches(7.02), demo_y + Inches(0.10), card_w3 - Inches(0.40), Inches(0.26))
    p = tb_rh.text_frame.paragraphs[0]
    p.text = d3["right_card"]["header"]
    p.font.name = FONT_BODY
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_CORAL_DARK

    img_x_r = Inches(6.82) + (card_w3 - img_w3) / 2
    if img_black_unboxing.exists():
        s3.shapes.add_picture(str(img_black_unboxing), img_x_r, demo_y + Inches(0.38), img_w3, img_h3)

    tb_rc = s3.shapes.add_textbox(Inches(7.02), demo_y + Inches(2.88), card_w3 - Inches(0.40), Inches(0.45))
    tf_rc = tb_rc.text_frame
    tf_rc.word_wrap = True
    tf_rc.margin_left = tf_rc.margin_top = 0
    p = tf_rc.paragraphs[0]
    p.text = d3["right_card"]["color_headline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(21)
    p.font.bold = True
    p.font.color.rgb = C_CORAL_DARK
    p.space_after = Pt(1)
    p = tf_rc.add_paragraph()
    p.text = d3["right_card"]["note_line"]
    p.font.name = FONT_BODY
    p.font.size = Pt(12)
    p.font.color.rgb = C_INK_LIGHT

    # Center Discrepancy Badge
    badge_w = Inches(2.20)
    badge_h = Inches(0.38)
    badge_x = Inches(0.65) + card_w3 - badge_w / 2 + Inches(0.15)
    badge_y = demo_y + Inches(1.35)
    badge = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, badge_x, badge_y, badge_w, badge_h)
    badge.fill.solid()
    badge.fill.fore_color.rgb = C_CORAL
    badge.line.color.rgb = C_CORAL_DARK
    badge.line.width = Pt(1.5)
    p_b = badge.text_frame.paragraphs[0]
    p_b.alignment = PP_ALIGN.CENTER
    p_b.text = "≠ COLOR DISCREPANCY"
    p_b.font.name = FONT_BODY
    p_b.font.size = Pt(11)
    p_b.font.bold = True
    p_b.font.color.rgb = C_WHITE

    # Bottom Prepared Options Strip: Starts at y=5.20 (0.15" clearance below cards!)
    strip_y = Inches(5.20)
    strip_h = Inches(1.35)
    strip = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.65), strip_y, Inches(12.03), strip_h)
    strip.fill.solid()
    strip.fill.fore_color.rgb = C_WHITE
    strip.line.color.rgb = C_BORDER_STRONG
    strip.line.width = Pt(1.5)

    tb_st = s3.shapes.add_textbox(Inches(0.85), strip_y + Inches(0.08), Inches(6.50), Inches(0.26))
    p = tb_st.text_frame.paragraphs[0]
    p.text = d3.get("prepared_title", "WHAT RETURNLENS PREPARES FOR THE SELLER:")
    p.font.name = FONT_BODY
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_DARK

    tb_disc = s3.shapes.add_textbox(Inches(7.00), strip_y + Inches(0.08), Inches(5.48), Inches(0.26))
    tf_disc = tb_disc.text_frame
    tf_disc.margin_left = tf_disc.margin_top = 0
    p_disc = tf_disc.paragraphs[0]
    p_disc.alignment = PP_ALIGN.RIGHT
    p_disc.text = d3.get("disclaimer", "* Illustrative concept scenario with staged mock evidence.")
    p_disc.font.name = FONT_BODY
    p_disc.font.size = Pt(9.5)
    p_disc.font.color.rgb = C_MUTED

    opt_w = Inches(3.70)
    opt_gap = Inches(0.24)
    for j, opt in enumerate(d3["options"]):
        ox = Inches(0.85) + j * (opt_w + opt_gap)
        
        # Option 2 is highlighted with subtle soft background box
        if j == 1:
            h_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, ox - Inches(0.08), strip_y + Inches(0.32), opt_w + Inches(0.16), Inches(0.92))
            h_box.fill.solid()
            h_box.fill.fore_color.rgb = C_TEAL_TINT
            h_box.line.color.rgb = C_TEAL_BORDER
            h_box.line.width = Pt(1)

        tb_o = s3.shapes.add_textbox(ox, strip_y + Inches(0.36), opt_w, Inches(0.84))
        tf_o = tb_o.text_frame
        tf_o.word_wrap = True
        tf_o.margin_left = tf_o.margin_top = 0
        p = tf_o.paragraphs[0]
        p.text = f"{opt['num']}. {opt['title']}"
        p.font.name = FONT_HEAD
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = C_TEAL_DARK if j == 1 else C_INK
        p.space_after = Pt(2)
        p = tf_o.add_paragraph()
        p.text = opt['desc']
        p.font.name = FONT_BODY
        p.font.size = Pt(11)
        p.font.color.rgb = C_INK if j == 1 else C_MUTED

    add_footer(s3, 3)
    add_notes(s3, d3["speaker_notes"])

    # =========================================================
    # SLIDE 4: HOW THE AGENT MOVES THE CASE FORWARD (SIMPLIFIED)
    # =========================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4, C_PAPER)
    d4 = slides_data[4]

    # Kicker
    tb = s4.shapes.add_textbox(Inches(0.65), Inches(0.40), Inches(12.0), Inches(0.25))
    p = tb.text_frame.paragraphs[0]
    p.text = d4.get("kicker", "AGENT BEHAVIOR · WORKFLOW & RESPONSIBILITIES")
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    # Title & Subtitle
    tb = s4.shapes.add_textbox(Inches(0.65), Inches(0.70), Inches(12.03), Inches(0.85))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = d4.get("title", "Models observe. Code verifies. Seller authorizes.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(34)
    p.font.bold = True
    p.font.color.rgb = C_INK
    p = tf.add_paragraph()
    p.text = d4.get("subtitle", "A structured agent pipeline that investigates, checks policies, and drafts the next step.")
    p.font.name = FONT_BODY
    p.font.size = Pt(20)
    p.font.color.rgb = C_MUTED

    # 1. Four Pipeline Stage Cards (Max 1 short sentence each)
    pipe_y = Inches(1.70)
    pipe_w = Inches(2.85)
    pipe_gap = Inches(0.21)
    pipe_h = Inches(1.95)

    for i, step in enumerate(d4["pipeline_steps"]):
        px = Inches(0.65) + i * (pipe_w + pipe_gap)
        pcard = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, pipe_y, pipe_w, pipe_h)
        pcard.fill.solid()
        pcard.fill.fore_color.rgb = C_WHITE
        pcard.line.color.rgb = C_TEAL_BORDER if i < 3 else C_BORDER_STRONG
        pcard.line.width = Pt(1.5)

        tb_p = s4.shapes.add_textbox(px + Inches(0.18), pipe_y + Inches(0.16), pipe_w - Inches(0.36), pipe_h - Inches(0.32))
        tf_p = tb_p.text_frame
        tf_p.word_wrap = True
        tf_p.margin_left = tf_p.margin_top = 0
        p = tf_p.paragraphs[0]
        p.text = step["step"]
        p.font.name = FONT_HEAD
        p.font.size = Pt(19)
        p.font.bold = True
        p.font.color.rgb = C_TEAL_DARK if i < 3 else C_CORAL_DARK
        p.space_after = Pt(2)

        p = tf_p.add_paragraph()
        p.text = step["role"].upper()
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_MUTED
        p.space_after = Pt(6)

        p = tf_p.add_paragraph()
        p.text = step["desc"]
        p.font.name = FONT_BODY
        p.font.size = Pt(13)
        p.font.color.rgb = C_INK_LIGHT

    # 2. Case C Dynamic Clarification Branch
    loop_y = Inches(3.85)
    loop_h = Inches(1.30)
    loop_box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.65), loop_y, Inches(12.03), loop_h)
    loop_box.fill.solid()
    loop_box.fill.fore_color.rgb = C_AMBER_TINT
    loop_box.line.color.rgb = RGBColor(0xF5, 0x9E, 0x0B)
    loop_box.line.width = Pt(1.5)

    tb_lp = s4.shapes.add_textbox(Inches(0.90), loop_y + Inches(0.14), Inches(11.53), loop_h - Inches(0.28))
    tf_lp = tb_lp.text_frame
    tf_lp.word_wrap = True
    tf_lp.margin_left = tf_lp.margin_top = 0
    p = tf_lp.paragraphs[0]
    p.text = d4["clarification_loop"]["title"]
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_AMBER_DARK
    p.space_after = Pt(3)

    p = tf_lp.add_paragraph()
    p.text = d4["clarification_loop"]["flow"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_INK
    p.space_after = Pt(3)

    p = tf_lp.add_paragraph()
    p.text = d4["clarification_loop"]["desc"]
    p.font.name = FONT_BODY
    p.font.size = Pt(13.5)
    p.font.color.rgb = C_INK_LIGHT

    # 3. Bottom Responsibility Line: Single short line
    resp_y = Inches(5.35)
    resp_h = Inches(0.95)
    resp_box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.65), resp_y, Inches(12.03), resp_h)
    resp_box.fill.solid()
    resp_box.fill.fore_color.rgb = C_WHITE
    resp_box.line.color.rgb = C_BORDER
    resp_box.line.width = Pt(1)

    tb_r = s4.shapes.add_textbox(Inches(0.90), resp_y + Inches(0.24), Inches(11.53), Inches(0.50))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = d4.get("responsibility_line", "Models observe visual traits · Code checks dates and policy rules · Seller authorizes all actions")
    p.font.name = FONT_HEAD
    p.font.size = Pt(16.5)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_DARK

    add_footer(s4, 4)
    add_notes(s4, d4["speaker_notes"])

    # =========================================================
    # SLIDE 5: THREE SITUATIONS, THREE USEFUL NEXT STEPS
    # =========================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5, C_PAPER)
    d5 = slides_data[5]

    # Kicker
    tb = s5.shapes.add_textbox(Inches(0.65), Inches(0.40), Inches(12.0), Inches(0.25))
    p = tb.text_frame.paragraphs[0]
    p.text = d5.get("kicker", "PROTOTYPE SCENARIOS · EXPECTED BEHAVIOR")
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    # Title & Subtitle
    tb = s5.shapes.add_textbox(Inches(0.65), Inches(0.70), Inches(12.03), Inches(0.85))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = d5.get("title", "Three situations. Three useful next steps.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(34)
    p.font.bold = True
    p.font.color.rgb = C_INK
    p = tf.add_paragraph()
    p.text = d5.get("subtitle", "ReturnLens handles clean claims, flags discrepancies, and guides unclear evidence.")
    p.font.name = FONT_BODY
    p.font.size = Pt(20)
    p.font.color.rgb = C_MUTED

    # 3 Scenario Columns (Spacious, trimmed text)
    scen_y = Inches(1.70)
    scen_w = Inches(3.85)
    scen_gap = Inches(0.24)
    scen_h = Inches(4.65)

    scen_colors = [
        (C_TEAL_DARK, C_TEAL_TINT, C_TEAL_BORDER),
        (C_CORAL_DARK, C_CORAL_TINT, C_CORAL_BORDER),
        (C_AMBER_DARK, C_AMBER_TINT, RGBColor(0xFD, 0xBA, 0x74))
    ]

    for i, col_data in enumerate(d5["columns"]):
        cx = Inches(0.65) + i * (scen_w + scen_gap)
        c_title_color, c_tint, c_border = scen_colors[i]

        ccard = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, scen_y, scen_w, scen_h)
        ccard.fill.solid()
        ccard.fill.fore_color.rgb = C_WHITE
        ccard.line.color.rgb = c_border
        ccard.line.width = Pt(1.5)

        pill = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx + Inches(0.20), scen_y + Inches(0.20), Inches(1.80), Inches(0.32))
        pill.fill.solid()
        pill.fill.fore_color.rgb = c_tint
        pill.line.color.rgb = c_border
        pill.line.width = Pt(1)
        p = pill.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = col_data["tag"]
        p.font.name = FONT_BODY
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = c_title_color

        tb_sc = s5.shapes.add_textbox(cx + Inches(0.20), scen_y + Inches(0.60), scen_w - Inches(0.40), scen_h - Inches(0.70))
        tf_sc = tb_sc.text_frame
        tf_sc.word_wrap = True
        tf_sc.margin_left = tf_sc.margin_top = 0

        p = tf_sc.paragraphs[0]
        p.text = col_data["title"]
        p.font.name = FONT_HEAD
        p.font.size = Pt(21)
        p.font.bold = True
        p.font.color.rgb = C_INK
        p.space_after = Pt(10)

        p = tf_sc.add_paragraph()
        p.text = "SITUATION:"
        p.font.name = FONT_BODY
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_MUTED
        p.space_after = Pt(2)

        p = tf_sc.add_paragraph()
        p.text = col_data["situation"]
        p.font.name = FONT_BODY
        p.font.size = Pt(13)
        p.font.color.rgb = C_INK_LIGHT
        p.space_after = Pt(12)

        p = tf_sc.add_paragraph()
        p.text = "AGENT ACTION:"
        p.font.name = FONT_BODY
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_MUTED
        p.space_after = Pt(2)

        p = tf_sc.add_paragraph()
        p.text = col_data["agent_action"]
        p.font.name = FONT_BODY
        p.font.size = Pt(13)
        p.font.color.rgb = C_INK_LIGHT
        p.space_after = Pt(12)

        p = tf_sc.add_paragraph()
        p.text = "SELLER OUTCOME:"
        p.font.name = FONT_BODY
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = c_title_color
        p.space_after = Pt(2)

        p = tf_sc.add_paragraph()
        p.text = col_data["seller_outcome"]
        p.font.name = FONT_BODY
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_INK

    add_footer(s5, 5)
    add_notes(s5, d5["speaker_notes"])

    # =========================================================
    # SLIDE 6: A FOCUSED 24-HOUR PROTOTYPE (NO SUBTITLE, CLEAN TIMELINE)
    # =========================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6, C_PAPER)
    d6 = slides_data[6]

    # Kicker
    tb = s6.shapes.add_textbox(Inches(0.65), Inches(0.40), Inches(12.0), Inches(0.25))
    p = tb.text_frame.paragraphs[0]
    p.text = d6.get("kicker", "24-HOUR PROTOTYPE SPRINT · EXECUTION PLAN")
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    # Title: ONE SINGLE LINE (No subtitle!)
    tb = s6.shapes.add_textbox(Inches(0.65), Inches(0.70), Inches(12.03), Inches(0.55))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = d6.get("title", "A focused 24-hour prototype.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = C_INK

    # 1. Four-Phase Timeline (Clear 0.35" gap below title!)
    phase_y = Inches(1.60)
    phase_w = Inches(2.85)
    phase_gap = Inches(0.21)
    phase_h = Inches(1.30)

    for i, ph in enumerate(d6["phases"]):
        px = Inches(0.65) + i * (phase_w + phase_gap)
        ph_box = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, phase_y, phase_w, phase_h)
        ph_box.fill.solid()
        ph_box.fill.fore_color.rgb = C_WHITE
        ph_box.line.color.rgb = C_BORDER
        ph_box.line.width = Pt(1)

        tb_ph = s6.shapes.add_textbox(px + Inches(0.16), phase_y + Inches(0.12), phase_w - Inches(0.32), phase_h - Inches(0.24))
        tf_ph = tb_ph.text_frame
        tf_ph.word_wrap = True
        tf_ph.margin_left = tf_ph.margin_top = 0
        p = tf_ph.paragraphs[0]
        p.text = ph["time"]
        p.font.name = FONT_BODY
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_TEAL_DARK
        p.space_after = Pt(2)

        p = tf_ph.add_paragraph()
        p.text = ph["title"]
        p.font.name = FONT_HEAD
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = C_INK
        p.space_after = Pt(4)

        p = tf_ph.add_paragraph()
        p.text = ph["output"]
        p.font.name = FONT_BODY
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_INK_LIGHT

    # 2. Bottom Split: Team Roles & Scope Discipline
    split_y = Inches(3.10)
    split_h = Inches(2.15)
    col_w6 = Inches(5.86)

    # Left: Team Roles Card (Clean roles)
    roles_box = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.65), split_y, col_w6, split_h)
    roles_box.fill.solid()
    roles_box.fill.fore_color.rgb = C_WHITE
    roles_box.line.color.rgb = C_BORDER
    roles_box.line.width = Pt(1.5)

    tb_r = s6.shapes.add_textbox(Inches(0.85), split_y + Inches(0.14), col_w6 - Inches(0.40), split_h - Inches(0.28))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_top = 0
    p = tf_r.paragraphs[0]
    p.text = "3 TEAM ROLES"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_DARK
    p.space_after = Pt(6)

    for role_info in d6["roles"]:
        p = tf_r.add_paragraph()
        p.text = f"• {role_info['role']}: "
        p.font.name = FONT_BODY
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_INK
        run = p.add_run()
        run.text = role_info['deliverables']
        run.font.bold = False
        run.font.color.rgb = C_INK_LIGHT
        p.space_after = Pt(5)

    # Right: Scope Discipline (Sprint Core vs Stretch Goals)
    scope_box = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.82), split_y, col_w6, split_h)
    scope_box.fill.solid()
    scope_box.fill.fore_color.rgb = C_WHITE
    scope_box.line.color.rgb = C_CORAL_BORDER
    scope_box.line.width = Pt(1.5)

    tb_sc = s6.shapes.add_textbox(Inches(7.02), split_y + Inches(0.14), col_w6 - Inches(0.40), split_h - Inches(0.28))
    tf_sc = tb_sc.text_frame
    tf_sc.word_wrap = True
    tf_sc.margin_left = tf_sc.margin_top = 0
    p = tf_sc.paragraphs[0]
    p.text = "SCOPE DISCIPLINE: SPRINT CORE VS. STRETCH"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CORAL_DARK
    p.space_after = Pt(6)

    p = tf_sc.add_paragraph()
    p.text = "• SPRINT CORE: "
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_INK
    run = p.add_run()
    run.text = d6["scope_discipline"]["must_deliver"]
    run.font.bold = False
    run.font.color.rgb = C_INK_LIGHT
    p.space_after = Pt(6)

    p = tf_sc.add_paragraph()
    p.text = "• STRETCH GOALS: "
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CORAL_DARK
    run = p.add_run()
    run.text = d6["scope_discipline"]["stretch_goals"]
    run.font.bold = False
    run.font.color.rgb = C_MUTED

    # 3. Closing Takeaway Banner
    take_y = Inches(5.45)
    take_h = Inches(0.95)
    take_box = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.65), take_y, Inches(12.03), take_h)
    take_box.fill.solid()
    take_box.fill.fore_color.rgb = C_TEAL_TINT
    take_box.line.color.rgb = C_TEAL_BORDER
    take_box.line.width = Pt(1.5)

    tb_tk = s6.shapes.add_textbox(Inches(0.90), take_y + Inches(0.22), Inches(11.53), Inches(0.50))
    tf_tk = tb_tk.text_frame
    tf_tk.word_wrap = True
    p = tf_tk.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = f"“{d6['closing_takeaway']}”"
    p.font.name = FONT_HEAD
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_DARK

    add_footer(s6, 6)
    add_notes(s6, d6["speaker_notes"])

    # =========================================================
    # REPRODUCIBLE DETERMINISTIC PACKAGING (ZIP_STORED)
    # =========================================================
    raw_pptx = deliverables_dir / "temp_raw_v8_1.pptx"
    prs.save(str(raw_pptx))

    final_deliv_pptx = deliverables_dir / "ReturnLens_v8_1.pptx"
    root_pptx = base_dir / "ReturnLens_v8_1.pptx"

    fixed_time = (2026, 10, 31, 12, 0, 0)
    with zipfile.ZipFile(raw_pptx, "r") as zin:
        with zipfile.ZipFile(final_deliv_pptx, "w", compression=zipfile.ZIP_STORED) as zout:
            for item in sorted(zin.infolist(), key=lambda x: x.filename):
                data_bytes = zin.read(item.filename)
                new_info = zipfile.ZipInfo(filename=item.filename, date_time=fixed_time)
                new_info.compress_type = zipfile.ZIP_STORED
                new_info.create_system = 0
                new_info.external_attr = 0o644 << 16
                zout.writestr(new_info, data_bytes)

    if raw_pptx.exists():
        raw_pptx.unlink()

    shutil.copy2(final_deliv_pptx, root_pptx)
    print(f"Generated ReturnLens_v8_1.pptx successfully: {final_deliv_pptx} ({final_deliv_pptx.stat().st_size} bytes)")

if __name__ == "__main__":
    build_v8_1_pptx()

