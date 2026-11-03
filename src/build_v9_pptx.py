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

def build_v9_pptx():
    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / "content" / "deck_data_v9.json"
    deliverables_dir = base_dir / "deliverables"
    assets_dir = base_dir / "src" / "assets"
    deliverables_dir.mkdir(parents=True, exist_ok=True)

    if not data_path.exists():
        raise FileNotFoundError(f"Canonical data file missing: {data_path}")

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    slides_data = {s["slide_number"]: s for s in data["slides"]}

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ReturnLens v9 Minimalist Architectural Palette
    # Light warm gallery white canvas, razor-sharp deep charcoal typography, restrained pine & terracotta accents
    C_BG = RGBColor(0xFA, 0xFA, 0xF9)             # Gallery Warm Off-White (#FAFAF9)
    C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)          # Pure White for mockup containers
    C_TEXT_PRIMARY = RGBColor(0x11, 0x18, 0x15)   # Deep Near-Black Charcoal (#111815)
    C_TEXT_SECONDARY = RGBColor(0x38, 0x44, 0x3E) # Readable Body Charcoal (#38443E)
    C_TEXT_MUTED = RGBColor(0x6E, 0x7B, 0x74)     # Subtle Sage Slate (#6E7B74)
    C_LINE = RGBColor(0xE4, 0xE2, 0xDC)           # Crisp Neutral Hairline (#E4E2DC)
    C_SURFACE_SUBTLE = RGBColor(0xF5, 0xF4, 0xF0) # Minimal subtle surface fill

    # Accents (used with extreme restraint)
    C_PINE = RGBColor(0x0C, 0x5E, 0x4B)           # Brand Pine Green (#0C5E4B)
    C_PINE_DARK = RGBColor(0x08, 0x43, 0x35)      # Deep Pine (#084335)
    C_CORAL = RGBColor(0xC8, 0x4D, 0x33)          # Terracotta Coral (#C84D33)
    C_CORAL_DARK = RGBColor(0x9E, 0x2A, 0x2B)     # Deep Terracotta (#9E2A2B)

    # Typography: Verified Windows system font Arial with deliberate weight hierarchy
    FONT_HEAD = "Arial"
    FONT_BODY = "Arial"

    # Images (1376x768, 16:9 ratio = 1.79167)
    img_white_order = assets_dir / "studio_white_headphones.jpg"
    img_black_unboxing = assets_dir / "unboxing_black_headphones.jpg"

    def set_bg(slide, color=C_BG):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.width = 0
        return bg

    def add_page_number(slide, num_str):
        tb = slide.shapes.add_textbox(Inches(11.50), Inches(6.92), Inches(1.10), Inches(0.30))
        tf = tb.text_frame
        tf.word_wrap = False
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.RIGHT
        p.text = f"{num_str} / 06"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_TEXT_MUTED

    def add_notes(slide, text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = text

    # =========================================================
    # SLIDE 1: PRODUCT INTRODUCTION & FLAT CONSOLE MOCKUP
    # =========================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)
    d1 = slides_data[1]

    # Kicker
    tb = s1.shapes.add_textbox(Inches(0.80), Inches(0.75), Inches(5.00), Inches(0.25))
    tf = tb.text_frame
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = d1.get("kicker", "AgentX Hackathon 2026 · Track PS-04")
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PINE

    # Left Column: Brand, Tagline, Summary, Principle
    col_w1 = Inches(4.70)
    tb_l = s1.shapes.add_textbox(Inches(0.80), Inches(1.15), col_w1, Inches(4.50))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_top = 0

    p = tf_l.paragraphs[0]
    p.text = d1.get("title", "ReturnLens")
    p.font.name = FONT_HEAD
    p.font.size = Pt(50)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY
    p.space_after = Pt(8)

    p = tf_l.add_paragraph()
    p.text = d1.get("tagline", "Every return decision, backed by evidence.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = C_PINE
    p.space_after = Pt(18)

    p = tf_l.add_paragraph()
    p.text = d1.get("summary", "An evidence triage assistant that connects customer claims, unboxing video, order records, and store policy into one clear decision pack for solo merchants.")
    p.font.name = FONT_BODY
    p.font.size = Pt(15)
    p.font.color.rgb = C_TEXT_SECONDARY
    p.space_after = Pt(26)

    # Thin Divider Line
    line_l = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.80), Inches(4.80), Inches(4.70), Inches(0.015))
    line_l.fill.solid()
    line_l.fill.fore_color.rgb = C_LINE
    line_l.line.width = 0

    # Core Principle (Clean text, NOT in a card!)
    tb_pr = s1.shapes.add_textbox(Inches(0.80), Inches(4.95), col_w1, Inches(1.20))
    tf_pr = tb_pr.text_frame
    tf_pr.word_wrap = True
    tf_pr.margin_left = tf_pr.margin_top = 0
    p = tf_pr.paragraphs[0]
    p.text = d1.get("principle", "Models observe. Code verifies. Seller authorizes.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY
    p.space_after = Pt(4)

    p = tf_pr.add_paragraph()
    p.text = "Agent collects info & clarifies · Seller approves returns, labels & refunds"
    p.font.name = FONT_BODY
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_MUTED

    # Right Column: Clean, Flat Seller View Mockup (No macOS 3-dots, no nested rounded cards)
    m_x, m_y, m_w, m_h = Inches(5.90), Inches(0.75), Inches(6.65), Inches(5.75)
    mock = d1["mockup"]

    m_box = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, m_x, m_y, m_w, m_h)
    m_box.fill.solid()
    m_box.fill.fore_color.rgb = C_WHITE
    m_box.line.color.rgb = C_LINE
    m_box.line.width = Pt(1)

    # Mockup Header Bar
    tb_mh = s1.shapes.add_textbox(m_x + Inches(0.30), m_y + Inches(0.18), m_w - Inches(0.60), Inches(0.30))
    tf_mh = tb_mh.text_frame
    tf_mh.margin_left = tf_mh.margin_top = 0
    p = tf_mh.paragraphs[0]
    p.text = mock["case_header"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_PINE

    # Divider below header
    line_m1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, m_x, m_y + Inches(0.55), m_w, Inches(0.015))
    line_m1.fill.solid()
    line_m1.fill.fore_color.rgb = C_LINE
    line_m1.line.width = 0

    # Order Summary Line
    tb_mos = s1.shapes.add_textbox(m_x + Inches(0.30), m_y + Inches(0.65), m_w - Inches(0.60), Inches(0.28))
    tf_mos = tb_mos.text_frame
    tf_mos.margin_left = tf_mos.margin_top = 0
    p = tf_mos.paragraphs[0]
    p.text = mock["order_summary"]
    p.font.name = FONT_BODY
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY

    # Side-by-side Evidence Photos (Aspect ratio strictly locked at 1.79167)
    img_mw = Inches(2.85)
    img_mh = Inches(1.59)
    img_my = m_y + Inches(1.10)

    # Left: Catalog photo
    if img_white_order.exists():
        s1.shapes.add_picture(str(img_white_order), m_x + Inches(0.30), img_my, img_mw, img_mh)
    tb_ms1 = s1.shapes.add_textbox(m_x + Inches(0.30), img_my + img_mh + Inches(0.08), img_mw, Inches(0.45))
    tf_ms1 = tb_ms1.text_frame
    tf_ms1.margin_left = tf_ms1.margin_top = 0
    p = tf_ms1.paragraphs[0]
    p.text = "Ordered: White"
    p.font.name = FONT_HEAD
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY
    p = tf_ms1.add_paragraph()
    p.text = "SKU: HEAD-WHT-02 · Matte White"
    p.font.name = FONT_BODY
    p.font.size = Pt(10.5)
    p.font.color.rgb = C_TEXT_MUTED

    # Right: Unboxing keyframe
    if img_black_unboxing.exists():
        s1.shapes.add_picture(str(img_black_unboxing), m_x + Inches(3.50), img_my, img_mw, img_mh)
    tb_ms2 = s1.shapes.add_textbox(m_x + Inches(3.50), img_my + img_mh + Inches(0.08), img_mw, Inches(0.45))
    tf_ms2 = tb_ms2.text_frame
    tf_ms2.margin_left = tf_ms2.margin_top = 0
    p = tf_ms2.paragraphs[0]
    p.text = "Observed: Black"
    p.font.name = FONT_HEAD
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CORAL
    p = tf_ms2.add_paragraph()
    p.text = "Keyframe 00:07 · Barcode unverified"
    p.font.name = FONT_BODY
    p.font.size = Pt(10.5)
    p.font.color.rgb = C_TEXT_MUTED

    # Discrepancy Callout Strip (Minimal, flat with subtle left accent line)
    dis_y = m_y + Inches(3.40)
    dis_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, m_x + Inches(0.30), dis_y, Inches(0.04), Inches(0.70))
    dis_bar.fill.solid()
    dis_bar.fill.fore_color.rgb = C_CORAL
    dis_bar.line.width = 0

    tb_dis = s1.shapes.add_textbox(m_x + Inches(0.45), dis_y, m_w - Inches(0.75), Inches(0.70))
    tf_dis = tb_dis.text_frame
    tf_dis.word_wrap = True
    tf_dis.margin_left = tf_dis.margin_top = 0
    p = tf_dis.paragraphs[0]
    p.text = mock["discrepancy_note"]
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CORAL_DARK
    p.space_after = Pt(2)
    p = tf_dis.add_paragraph()
    p.text = mock["next_step"]
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.color.rgb = C_TEXT_SECONDARY

    # Divider above action
    line_m2 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, m_x, m_y + Inches(4.35), m_w, Inches(0.015))
    line_m2.fill.solid()
    line_m2.fill.fore_color.rgb = C_LINE
    line_m2.line.width = 0

    # Decision Footer Action Button (1 line, ample width)
    tb_mfa = s1.shapes.add_textbox(m_x + Inches(0.30), m_y + Inches(4.55), Inches(3.60), Inches(0.60))
    tf_mfa = tb_mfa.text_frame
    tf_mfa.word_wrap = True
    tf_mfa.margin_left = tf_mfa.margin_top = 0
    p = tf_mfa.paragraphs[0]
    p.text = "Seller authorizes all consequential actions"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY
    p = tf_mfa.add_paragraph()
    p.text = "No automated refund · No automated rejection"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_TEXT_MUTED

    btn_m = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, m_x + Inches(3.90), m_y + Inches(4.55), Inches(2.45), Inches(0.48))
    btn_m.fill.solid()
    btn_m.fill.fore_color.rgb = C_PINE
    btn_m.line.width = 0
    p = btn_m.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = mock["cta_button"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    add_page_number(s1, "01")
    add_notes(s1, d1["speaker_notes"])

    # =========================================================
    # SLIDE 2: THE PROBLEM (ONE CLAIM. FOUR SOURCES.)
    # =========================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    d2 = slides_data[2]

    # Kicker
    tb = s2.shapes.add_textbox(Inches(0.80), Inches(0.75), Inches(10.0), Inches(0.25))
    p = tb.text_frame.paragraphs[0]
    p.text = d2.get("kicker", "The Merchant's Reality")
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PINE

    # Title (Clear, large, no redundant subtitle!)
    tb = s2.shapes.add_textbox(Inches(0.80), Inches(1.10), Inches(11.70), Inches(0.60))
    tf = tb.text_frame
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = d2.get("title", "One claim. Four disconnected sources.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(34)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY

    # 1. Customer Claim Quote Block (Flat, prominent quote, thin left border)
    quote_y = Inches(1.90)
    quote_h = Inches(1.10)
    q_border = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.80), quote_y, Inches(0.04), quote_h)
    q_border.fill.solid()
    q_border.fill.fore_color.rgb = C_PINE
    q_border.line.width = 0

    tb_q = s2.shapes.add_textbox(Inches(1.00), quote_y + Inches(0.08), Inches(11.50), quote_h - Inches(0.16))
    tf_q = tb_q.text_frame
    tf_q.word_wrap = True
    tf_q.margin_left = tf_q.margin_top = 0
    p = tf_q.paragraphs[0]
    p.text = d2["customer_claim"]["quote"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(21)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY
    p.space_after = Pt(4)

    p = tf_q.add_paragraph()
    p.text = d2["customer_claim"]["attachment"]
    p.font.name = FONT_BODY
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_MUTED

    # 2. Four Disconnected Sources (4 horizontal columns, hairline rules, NO rounded cards!)
    src_y = Inches(3.30)
    src_w = Inches(2.70)
    src_gap = Inches(0.30)
    for i, src in enumerate(d2["sources"]):
        sx = Inches(0.80) + i * (src_w + src_gap)

        # Top hairline rule
        sline = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, sx, src_y, src_w, Inches(0.015))
        sline.fill.solid()
        sline.fill.fore_color.rgb = C_LINE
        sline.line.width = 0

        tb_src = s2.shapes.add_textbox(sx, src_y + Inches(0.12), src_w, Inches(1.40))
        tf_s = tb_src.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_top = 0

        p = tf_s.paragraphs[0]
        p.text = src["num"]
        p.font.name = FONT_HEAD
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_PINE
        p.space_after = Pt(2)

        p = tf_s.add_paragraph()
        p.text = src["name"]
        p.font.name = FONT_HEAD
        p.font.size = Pt(16.5)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_PRIMARY
        p.space_after = Pt(6)

        p = tf_s.add_paragraph()
        p.text = src["detail"]
        p.font.name = FONT_BODY
        p.font.size = Pt(13)
        p.font.color.rgb = C_TEXT_SECONDARY

    # 3. Bottom Decision Question (Prominent concluding line, NO warning card!)
    dil_y = Inches(5.15)
    line_dil = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.80), dil_y, Inches(11.70), Inches(0.015))
    line_dil.fill.solid()
    line_dil.fill.fore_color.rgb = C_LINE
    line_dil.line.width = 0

    tb_dil = s2.shapes.add_textbox(Inches(0.80), dil_y + Inches(0.18), Inches(11.70), Inches(1.10))
    tf_d = tb_dil.text_frame
    tf_d.word_wrap = True
    tf_d.margin_left = tf_d.margin_top = 0

    p = tf_d.paragraphs[0]
    p.text = "THE SELLER'S QUESTION:"
    p.font.name = FONT_HEAD
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PINE
    p.space_after = Pt(4)

    p = tf_d.add_paragraph()
    p.text = d2.get("seller_question", "Packing mistake, delivery error, or unboxing swap? The seller needs verified facts before deciding to refund, replace, or inspect.")
    p.font.name = FONT_BODY
    p.font.size = Pt(17.5)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY

    add_page_number(s2, "02")
    add_notes(s2, d2["speaker_notes"])

    # =========================================================
    # SLIDE 3: THE CORE DEMONSTRATION (WHITE ORDERED. BLACK RECEIVED.)
    # =========================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    d3 = slides_data[3]

    # Kicker
    tb = s3.shapes.add_textbox(Inches(0.80), Inches(0.75), Inches(8.0), Inches(0.25))
    p = tb.text_frame.paragraphs[0]
    p.text = d3.get("kicker", "Core Evidence Comparison")
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PINE

    # Title & Subtitle
    tb = s3.shapes.add_textbox(Inches(0.80), Inches(1.05), Inches(11.70), Inches(0.75))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = d3.get("title", "White ordered. Black received.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(34)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY
    p = tf.add_paragraph()
    p.text = d3.get("subtitle", "ReturnLens highlights the visible discrepancy without jumping to unverified conclusions.")
    p.font.name = FONT_BODY
    p.font.size = Pt(16)
    p.font.color.rgb = C_TEXT_MUTED

    # Two Large Showcase Photos: Flat images, exact 16:9 ratio locked!
    img3_w = Inches(5.20)
    img3_h = Inches(2.90)
    img3_y = Inches(2.05)

    # Left: Studio White
    tb_h_l = s3.shapes.add_textbox(Inches(0.80), img3_y - Inches(0.24), img3_w, Inches(0.22))
    p = tb_h_l.text_frame.paragraphs[0]
    p.text = d3["left_evidence"]["label"]
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_PINE

    if img_white_order.exists():
        s3.shapes.add_picture(str(img_white_order), Inches(0.80), img3_y, img3_w, img3_h)

    tb_c_l = s3.shapes.add_textbox(Inches(0.80), img3_y + img3_h + Inches(0.08), img3_w, Inches(0.50))
    tf_cl = tb_c_l.text_frame
    tf_cl.margin_left = tf_cl.margin_top = 0
    p = tf_cl.paragraphs[0]
    p.text = d3["left_evidence"]["headline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY
    p = tf_cl.add_paragraph()
    p.text = d3["left_evidence"]["meta"]
    p.font.name = FONT_BODY
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_MUTED

    # Center Discrepancy Indicator: Elegant symbol, doesn't obscure photos
    tb_neq = s3.shapes.add_textbox(Inches(6.40), img3_y + Inches(1.15), Inches(0.70), Inches(0.60))
    p_neq = tb_neq.text_frame.paragraphs[0]
    p_neq.alignment = PP_ALIGN.CENTER
    p_neq.text = "≠"
    p_neq.font.name = FONT_HEAD
    p_neq.font.size = Pt(28)
    p_neq.font.bold = True
    p_neq.font.color.rgb = C_CORAL

    # Right: Customer Black Unboxing
    tb_h_r = s3.shapes.add_textbox(Inches(7.30), img3_y - Inches(0.24), img3_w, Inches(0.22))
    p = tb_h_r.text_frame.paragraphs[0]
    p.text = d3["right_evidence"]["label"]
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_CORAL

    if img_black_unboxing.exists():
        s3.shapes.add_picture(str(img_black_unboxing), Inches(7.30), img3_y, img3_w, img3_h)

    tb_c_r = s3.shapes.add_textbox(Inches(7.30), img3_y + img3_h + Inches(0.08), img3_w, Inches(0.50))
    tf_cr = tb_c_r.text_frame
    tf_cr.margin_left = tf_cr.margin_top = 0
    p = tf_cr.paragraphs[0]
    p.text = d3["right_evidence"]["headline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_CORAL
    p = tf_cr.add_paragraph()
    p.text = d3["right_evidence"]["meta"]
    p.font.name = FONT_BODY
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_MUTED

    # Bottom Prepared Options (Clean 3-column row, NO pastel cards!)
    opt_y = Inches(5.50)
    line_opt = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.80), opt_y, Inches(11.70), Inches(0.015))
    line_opt.fill.solid()
    line_opt.fill.fore_color.rgb = C_LINE
    line_opt.line.width = 0

    # Option 1
    tb_o1 = s3.shapes.add_textbox(Inches(0.80), opt_y + Inches(0.08), Inches(3.60), Inches(0.65))
    tf_o1 = tb_o1.text_frame
    tf_o1.word_wrap = True
    tf_o1.margin_left = tf_o1.margin_top = 0
    p = tf_o1.paragraphs[0]
    p.text = "1. Accept mis-pack"
    p.font.name = FONT_HEAD
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY
    p.space_after = Pt(2)
    p = tf_o1.add_paragraph()
    p.text = "Issue replacement return label"
    p.font.name = FONT_BODY
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MUTED

    # Option 2 (Subtly emphasized with a thin pine green left accent line, single-line title!)
    o2_line = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.70), opt_y + Inches(0.08), Inches(0.03), Inches(0.65))
    o2_line.fill.solid()
    o2_line.fill.fore_color.rgb = C_PINE
    o2_line.line.width = 0

    tb_o2 = s3.shapes.add_textbox(Inches(4.85), opt_y + Inches(0.08), Inches(4.00), Inches(0.65))
    tf_o2 = tb_o2.text_frame
    tf_o2.word_wrap = True
    tf_o2.margin_left = tf_o2.margin_top = 0
    p = tf_o2.paragraphs[0]
    p.text = "2. Request label photo"
    p.font.name = FONT_HEAD
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_PINE
    p.space_after = Pt(2)
    p = tf_o2.add_paragraph()
    p.text = "“Please share the outer-box label so we can check your shipment.”"
    p.font.name = FONT_BODY
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_PRIMARY

    # Option 3
    tb_o3 = s3.shapes.add_textbox(Inches(9.10), opt_y + Inches(0.08), Inches(3.40), Inches(0.65))
    tf_o3 = tb_o3.text_frame
    tf_o3.word_wrap = True
    tf_o3.margin_left = tf_o3.margin_top = 0
    p = tf_o3.paragraphs[0]
    p.text = "3. Hold for inspection"
    p.font.name = FONT_HEAD
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY
    p.space_after = Pt(2)
    p = tf_o3.add_paragraph()
    p.text = "Inspect returned parcel before refund"
    p.font.name = FONT_BODY
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MUTED

    # Disclaimer footnote
    tb_disc = s3.shapes.add_textbox(Inches(0.80), Inches(6.35), Inches(11.70), Inches(0.20))
    p = tb_disc.text_frame.paragraphs[0]
    p.text = d3.get("disclaimer", "* Illustrative scenario with staged mock evidence. Barcode and exact model unverified.")
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.color.rgb = C_TEXT_MUTED

    add_page_number(s3, "03")
    add_notes(s3, d3["speaker_notes"])

    # =========================================================
    # SLIDE 4: AGENT WORKFLOW (FROM EVIDENCE TO NEXT STEP)
    # =========================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    d4 = slides_data[4]

    # Kicker
    tb = s4.shapes.add_textbox(Inches(0.80), Inches(0.75), Inches(8.0), Inches(0.25))
    p = tb.text_frame.paragraphs[0]
    p.text = d4.get("kicker", "Agent Architecture")
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PINE

    # Title & Subtitle
    tb = s4.shapes.add_textbox(Inches(0.80), Inches(1.05), Inches(11.70), Inches(0.75))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = d4.get("title", "From evidence to next step.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(34)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY
    p = tf.add_paragraph()
    p.text = d4.get("subtitle", "A structured pipeline where models observe, code verifies, and the seller approves.")
    p.font.name = FONT_BODY
    p.font.size = Pt(16)
    p.font.color.rgb = C_TEXT_MUTED

    # 4 Sequential Steps on a clean flow (NO 4 huge boxes!)
    flow_y = Inches(2.20)
    step_w = Inches(2.65)
    step_gap = Inches(0.36)

    # Clean connecting hairline across flow
    line_flow = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.80), flow_y, Inches(11.70), Inches(0.015))
    line_flow.fill.solid()
    line_flow.fill.fore_color.rgb = C_LINE
    line_flow.line.width = 0

    for i, st in enumerate(d4["steps"]):
        sx = Inches(0.80) + i * (step_w + step_gap)

        # Arrow connector between steps (for i < 3)
        if i < 3:
            tb_arr = s4.shapes.add_textbox(sx + step_w + Inches(0.04), flow_y + Inches(0.14), step_gap - Inches(0.08), Inches(0.30))
            p_a = tb_arr.text_frame.paragraphs[0]
            p_a.alignment = PP_ALIGN.CENTER
            p_a.text = "→"
            p_a.font.name = FONT_HEAD
            p_a.font.size = Pt(13)
            p_a.font.bold = True
            p_a.font.color.rgb = C_PINE

        tb_step = s4.shapes.add_textbox(sx, flow_y + Inches(0.15), step_w, Inches(1.60))
        tf_st = tb_step.text_frame
        tf_st.word_wrap = True
        tf_st.margin_left = tf_st.margin_top = 0

        p = tf_st.paragraphs[0]
        p.text = st["step"]
        p.font.name = FONT_HEAD
        p.font.size = Pt(16.5)
        p.font.bold = True
        p.font.color.rgb = C_PINE if i == 3 else C_TEXT_PRIMARY
        p.space_after = Pt(2)

        p = tf_st.add_paragraph()
        p.text = st["role"]
        p.font.name = FONT_BODY
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_MUTED
        p.space_after = Pt(6)

        p = tf_st.add_paragraph()
        p.text = st["desc"]
        p.font.name = FONT_BODY
        p.font.size = Pt(13)
        p.font.color.rgb = C_TEXT_SECONDARY

    # Case C Clarification Loop (Clean, compact secondary flow, NO giant yellow box!)
    loop_y = Inches(4.25)
    c_flow = d4["clarification_flow"]

    c_box = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.80), loop_y, Inches(11.70), Inches(1.20))
    c_box.fill.solid()
    c_box.fill.fore_color.rgb = C_SURFACE_SUBTLE
    c_box.line.color.rgb = C_LINE
    c_box.line.width = Pt(1)

    tb_cl = s4.shapes.add_textbox(Inches(1.05), loop_y + Inches(0.14), Inches(11.20), Inches(0.92))
    tf_cl = tb_cl.text_frame
    tf_cl.word_wrap = True
    tf_cl.margin_left = tf_cl.margin_top = 0

    p = tf_cl.paragraphs[0]
    p.text = c_flow["label"]
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PINE
    p.space_after = Pt(3)

    p = tf_cl.add_paragraph()
    p.text = c_flow["summary"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(15.5)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY
    p.space_after = Pt(3)

    p = tf_cl.add_paragraph()
    p.text = c_flow["detail"]
    p.font.name = FONT_BODY
    p.font.size = Pt(12.5)
    p.font.color.rgb = C_TEXT_SECONDARY

    # Bottom Responsibility Line (Directly on canvas)
    tb_resp = s4.shapes.add_textbox(Inches(0.80), Inches(5.80), Inches(11.70), Inches(0.50))
    tf_resp = tb_resp.text_frame
    tf_resp.word_wrap = True
    p = tf_resp.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = d4.get("responsibility_summary", "Models observe visual traits · Code checks dates and policy rules · Seller approves returns, labels and refunds.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_PINE

    add_page_number(s4, "04")
    add_notes(s4, d4["speaker_notes"])

    # =========================================================
    # SLIDE 5: SCENARIOS MATRIX (THREE SITUATIONS. CLEAR NEXT STEPS.)
    # =========================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    d5 = slides_data[5]

    # Kicker
    tb = s5.shapes.add_textbox(Inches(0.80), Inches(0.75), Inches(8.0), Inches(0.25))
    p = tb.text_frame.paragraphs[0]
    p.text = d5.get("kicker", "Prototype Scenarios")
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PINE

    # Title & Subtitle
    tb = s5.shapes.add_textbox(Inches(0.80), Inches(1.05), Inches(11.70), Inches(0.75))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = d5.get("title", "Three situations. Clear next steps.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(34)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY
    p = tf.add_paragraph()
    p.text = d5.get("subtitle", "Expected prototype behavior across clean, conflicting, and unclear evidence.")
    p.font.name = FONT_BODY
    p.font.size = Pt(16)
    p.font.color.rgb = C_TEXT_MUTED

    # Clean 3-Row Matrix (Table layout with hairline rules, NO 3 giant cards!)
    mat_y = Inches(2.15)
    mat_w = Inches(11.70)

    c1_x, c1_w = Inches(0.80), Inches(2.20)
    c2_x, c2_w = Inches(3.20), Inches(3.40)
    c3_x, c3_w = Inches(6.80), Inches(3.20)
    c4_x, c4_w = Inches(10.20), Inches(2.30)

    # Table Header Row
    tb_th1 = s5.shapes.add_textbox(c1_x, mat_y, c1_w, Inches(0.25))
    p = tb_th1.text_frame.paragraphs[0]
    p.text = "CASE SCENARIO"
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_MUTED

    tb_th2 = s5.shapes.add_textbox(c2_x, mat_y, c2_w, Inches(0.25))
    p = tb_th2.text_frame.paragraphs[0]
    p.text = "SITUATION"
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_MUTED

    tb_th3 = s5.shapes.add_textbox(c3_x, mat_y, c3_w, Inches(0.25))
    p = tb_th3.text_frame.paragraphs[0]
    p.text = "AGENT RESPONSE"
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_MUTED

    tb_th4 = s5.shapes.add_textbox(c4_x, mat_y, c4_w, Inches(0.25))
    p = tb_th4.text_frame.paragraphs[0]
    p.text = "SELLER'S NEXT STEP"
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_MUTED

    # Hairline below header
    line_th = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.80), mat_y + Inches(0.28), mat_w, Inches(0.015))
    line_th.fill.solid()
    line_th.fill.fore_color.rgb = C_LINE
    line_th.line.width = 0

    # 3 Data Rows
    row_starts = [mat_y + Inches(0.38), mat_y + Inches(1.68), mat_y + Inches(2.98)]
    row_colors = [C_PINE, C_CORAL, C_TEXT_PRIMARY]

    for idx, row in enumerate(d5["matrix_rows"]):
        ry = row_starts[idx]
        acc_col = row_colors[idx]

        # Col 1: Case ID & Label
        tb_r1 = s5.shapes.add_textbox(c1_x, ry, c1_w, Inches(1.05))
        tf_r1 = tb_r1.text_frame
        tf_r1.word_wrap = True
        tf_r1.margin_left = tf_r1.margin_top = 0
        p = tf_r1.paragraphs[0]
        p.text = row["case_id"]
        p.font.name = FONT_HEAD
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = acc_col
        p.space_after = Pt(2)
        p = tf_r1.add_paragraph()
        p.text = row["label"]
        p.font.name = FONT_BODY
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_MUTED

        # Col 2: Situation
        tb_r2 = s5.shapes.add_textbox(c2_x, ry, c2_w, Inches(1.05))
        tf_r2 = tb_r2.text_frame
        tf_r2.word_wrap = True
        tf_r2.margin_left = tf_r2.margin_top = 0
        p = tf_r2.paragraphs[0]
        p.text = row["situation"]
        p.font.name = FONT_BODY
        p.font.size = Pt(12.5)
        p.font.color.rgb = C_TEXT_SECONDARY

        # Col 3: Agent Response
        tb_r3 = s5.shapes.add_textbox(c3_x, ry, c3_w, Inches(1.05))
        tf_r3 = tb_r3.text_frame
        tf_r3.word_wrap = True
        tf_r3.margin_left = tf_r3.margin_top = 0
        p = tf_r3.paragraphs[0]
        p.text = row["agent_response"]
        p.font.name = FONT_BODY
        p.font.size = Pt(12.5)
        p.font.color.rgb = C_TEXT_SECONDARY

        # Col 4: Seller Outcome
        tb_r4 = s5.shapes.add_textbox(c4_x, ry, c4_w, Inches(1.05))
        tf_r4 = tb_r4.text_frame
        tf_r4.word_wrap = True
        tf_r4.margin_left = tf_r4.margin_top = 0
        p = tf_r4.paragraphs[0]
        p.text = row["seller_outcome"]
        p.font.name = FONT_BODY
        p.font.size = Pt(12.5)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_PRIMARY

        # Hairline below row
        line_r = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.80), ry + Inches(1.15), mat_w, Inches(0.015))
        line_r.fill.solid()
        line_r.fill.fore_color.rgb = C_LINE
        line_r.line.width = 0

    # Footnote
    tb_fn = s5.shapes.add_textbox(Inches(0.80), Inches(6.25), mat_w, Inches(0.25))
    p = tb_fn.text_frame.paragraphs[0]
    p.text = d5.get("footnote", "* Planned prototype behavior across core scenarios.")
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.color.rgb = C_TEXT_MUTED

    add_page_number(s5, "05")
    add_notes(s5, d5["speaker_notes"])

    # =========================================================
    # SLIDE 6: 24-HOUR PROTOTYPE SPRINT
    # =========================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    d6 = slides_data[6]

    # Kicker
    tb = s6.shapes.add_textbox(Inches(0.80), Inches(0.75), Inches(8.0), Inches(0.25))
    p = tb.text_frame.paragraphs[0]
    p.text = d6.get("kicker", "24-Hour Prototype Sprint")
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PINE

    # Title
    tb = s6.shapes.add_textbox(Inches(0.80), Inches(1.05), Inches(11.70), Inches(0.50))
    tf = tb.text_frame
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = d6.get("title", "A focused 24-hour prototype.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(34)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY

    # 1. Timeline: 4 Clean Horizontal Intervals (NO pills, NO 4 cards!)
    time_y = Inches(1.80)
    t_line = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.80), time_y, Inches(11.70), Inches(0.015))
    t_line.fill.solid()
    t_line.fill.fore_color.rgb = C_LINE
    t_line.line.width = 0

    tw = Inches(2.70)
    tgap = Inches(0.30)
    for i, ph in enumerate(d6["phases"]):
        tx = Inches(0.80) + i * (tw + tgap)

        tb_ph = s6.shapes.add_textbox(tx, time_y + Inches(0.12), tw, Inches(1.30))
        tf_ph = tb_ph.text_frame
        tf_ph.word_wrap = True
        tf_ph.margin_left = tf_ph.margin_top = 0

        p = tf_ph.paragraphs[0]
        p.text = ph["time"]
        p.font.name = FONT_HEAD
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_PINE
        p.space_after = Pt(2)

        p = tf_ph.add_paragraph()
        p.text = ph["title"]
        p.font.name = FONT_HEAD
        p.font.size = Pt(15.5)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_PRIMARY
        p.space_after = Pt(4)

        p = tf_ph.add_paragraph()
        p.text = ph["output"]
        p.font.name = FONT_BODY
        p.font.size = Pt(12.5)
        p.font.color.rgb = C_TEXT_SECONDARY

    # 2. Bottom Split: Team Responsibilities (Left) vs Scope Discipline (Right) (NO cards!)
    split_y = Inches(3.60)
    col_w6 = Inches(5.60)

    # Left: Team Responsibilities
    line_rl = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.80), split_y, col_w6, Inches(0.015))
    line_rl.fill.solid()
    line_rl.fill.fore_color.rgb = C_LINE
    line_rl.line.width = 0

    tb_rl = s6.shapes.add_textbox(Inches(0.80), split_y + Inches(0.12), col_w6, Inches(1.60))
    tf_rl = tb_rl.text_frame
    tf_rl.word_wrap = True
    tf_rl.margin_left = tf_rl.margin_top = 0

    p = tf_rl.paragraphs[0]
    p.text = "TEAM RESPONSIBILITIES"
    p.font.name = FONT_HEAD
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PINE
    p.space_after = Pt(6)

    for r in d6["roles"]:
        p = tf_rl.add_paragraph()
        p.text = f"• {r['role']}: "
        p.font.name = FONT_BODY
        p.font.size = Pt(12.5)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_PRIMARY
        run = p.add_run()
        run.text = r["deliverables"]
        run.font.bold = False
        run.font.color.rgb = C_TEXT_SECONDARY
        p.space_after = Pt(4)

    # Right: Scope Discipline
    line_sc = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.90), split_y, col_w6, Inches(0.015))
    line_sc.fill.solid()
    line_sc.fill.fore_color.rgb = C_LINE
    line_sc.line.width = 0

    tb_sc = s6.shapes.add_textbox(Inches(6.90), split_y + Inches(0.12), col_w6, Inches(1.60))
    tf_sc = tb_sc.text_frame
    tf_sc.word_wrap = True
    tf_sc.margin_left = tf_sc.margin_top = 0

    p = tf_sc.paragraphs[0]
    p.text = "SCOPE DISCIPLINE"
    p.font.name = FONT_HEAD
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CORAL
    p.space_after = Pt(6)

    p = tf_sc.add_paragraph()
    p.text = "• SPRINT CORE: "
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY
    run = p.add_run()
    run.text = d6["scope_discipline"]["must_deliver"]
    run.font.bold = False
    run.font.color.rgb = C_TEXT_SECONDARY
    p.space_after = Pt(6)

    p = tf_sc.add_paragraph()
    p.text = "• STRETCH GOALS: "
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CORAL
    run = p.add_run()
    run.text = d6["scope_discipline"]["stretch_goals"]
    run.font.bold = False
    run.font.color.rgb = C_TEXT_MUTED

    # 3. Closing Takeaway directly on canvas (NO quote box!)
    take_y = Inches(5.65)
    tb_tk = s6.shapes.add_textbox(Inches(0.80), take_y, Inches(11.70), Inches(0.60))
    tf_tk = tb_tk.text_frame
    tf_tk.word_wrap = True
    p = tf_tk.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = f"“{d6['closing_takeaway']}”"
    p.font.name = FONT_HEAD
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = C_PINE

    add_page_number(s6, "06")
    add_notes(s6, d6["speaker_notes"])

    # =========================================================
    # REPRODUCIBLE DETERMINISTIC PACKAGING (ZIP_STORED)
    # =========================================================
    raw_pptx = deliverables_dir / "temp_raw_v9.pptx"
    prs.save(str(raw_pptx))

    final_deliv_pptx = deliverables_dir / "ReturnLens_v9.pptx"
    root_pptx = base_dir / "ReturnLens_v9.pptx"

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
    print(f"Generated ReturnLens_v9.pptx successfully: {final_deliv_pptx} ({final_deliv_pptx.stat().st_size} bytes)")

if __name__ == "__main__":
    build_v9_pptx()
