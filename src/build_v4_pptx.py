import os
import sys
import json
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_pptx():
    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / "content" / "deck_data.json"
    assets_dir = base_dir / "src" / "assets"

    if not data_path.exists():
        raise FileNotFoundError(f"Canonical data file missing: {data_path}")

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Required assets validation: Must fail build if missing!
    img_white = assets_dir / "studio_white_headphones.jpg"
    img_black = assets_dir / "unboxing_black_headphones.jpg"

    if not img_white.exists():
        raise FileNotFoundError(f"CRITICAL ASSET MISSING: {img_white}")
    if not img_black.exists():
        raise FileNotFoundError(f"CRITICAL ASSET MISSING: {img_black}")

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Design Tokens & Palette
    C_CREAM = RGBColor(0xF5, 0xF3, 0xEF)
    C_DARK = RGBColor(0x17, 0x26, 0x21)
    C_DARK_BG = RGBColor(0x0F, 0x1A, 0x16)
    C_CARD_DARK = RGBColor(0x17, 0x26, 0x21)
    C_TEAL = RGBColor(0x00, 0x6B, 0x55)
    C_TEAL_LIGHT = RGBColor(0xE1, 0xF2, 0xEC)
    C_TEAL_ACCENT = RGBColor(0x00, 0xD1, 0xA7)
    C_CORAL = RGBColor(0xD9, 0x5D, 0x39)
    C_CORAL_LIGHT = RGBColor(0xFC, 0xEC, 0xE8)
    C_CORAL_DARK = RGBColor(0x99, 0x1B, 0x1B)
    C_AMBER = RGBColor(0xD9, 0x77, 0x06)
    C_AMBER_LIGHT = RGBColor(0xFE, 0xF3, 0xC7)
    C_BLUE_LIGHT = RGBColor(0xEF, 0xF6, 0xFF)
    C_BLUE_TEXT = RGBColor(0x1E, 0x40, 0xAF)
    C_MUTED = RGBColor(0x59, 0x6E, 0x64)
    C_SUBTLE = RGBColor(0x7A, 0x8E, 0x85)
    C_BORDER_LIGHT = RGBColor(0xE2, 0xDE, 0xD4)
    C_BORDER_DARK = RGBColor(0x22, 0x38, 0x30)
    C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)

    FONT_HEAD = "Inter"
    FONT_MONO = "IBM Plex Mono"

    def set_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_footer(slide, left_text, right_text, is_dark=False):
        y = Inches(6.92)
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y, Inches(11.733), Inches(0.015))
        line.fill.solid()
        line.fill.fore_color.rgb = C_BORDER_DARK if is_dark else C_BORDER_LIGHT
        line.line.fill.background()

        tb_l = slide.shapes.add_textbox(Inches(0.8), y + Inches(0.06), Inches(9.0), Inches(0.4))
        p = tb_l.text_frame.paragraphs[0]
        p.text = left_text
        p.font.name = FONT_MONO
        p.font.size = Pt(9.5)
        p.font.color.rgb = RGBColor(0x5C, 0x78, 0x6E) if is_dark else C_SUBTLE

        tb_r = slide.shapes.add_textbox(Inches(10.0), y + Inches(0.06), Inches(2.533), Inches(0.4))
        p = tb_r.text_frame.paragraphs[0]
        p.text = right_text
        p.font.name = FONT_MONO
        p.font.size = Pt(9.5)
        p.font.color.rgb = RGBColor(0x5C, 0x78, 0x6E) if is_dark else C_SUBTLE
        p.alignment = PP_ALIGN.RIGHT

    def set_speaker_notes(slide, notes_text):
        tf = slide.notes_slide.notes_text_frame
        tf.text = notes_text.strip()

    slides_data = {s["slide_number"]: s for s in data["slides"]}

    # =========================================================================
    # SLIDE 1: PRODUCT HERO & CONSOLE (EDITORIAL SWISS)
    # =========================================================================
    d1 = slides_data[1]
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1, C_CREAM)

    # Left Column (38% width)
    tb = s1.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(4.5), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = d1["tag"]
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    tb = s1.shapes.add_textbox(Inches(0.8), Inches(1.15), Inches(4.5), Inches(1.1))
    p = tb.text_frame.paragraphs[0]
    p.text = d1["headline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(56)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    tb = s1.shapes.add_textbox(Inches(0.8), Inches(2.35), Inches(4.5), Inches(0.85))
    p = tb.text_frame.paragraphs[0]
    p.text = d1["subheadline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    tb = s1.shapes.add_textbox(Inches(0.8), Inches(3.3), Inches(4.5), Inches(1.2))
    p = tb.text_frame.paragraphs[0]
    p.text = d1["summary"] + "\n\nWhen a buyer submits an unboxing video, ReturnLens links video keyframes to store truth and courier scans, evaluates deterministic policy rules, and presents a 1-click decision console to the solo merchant."
    p.font.name = FONT_HEAD
    p.font.size = Pt(13)
    p.font.color.rgb = C_MUTED

    # Metrics row
    metrics = [
        ("15–20m", "Manual triage eliminated"),
        ("1-Click", "Merchant verification"),
        ("24h", "Prototype feasibility")
    ]
    for i, (m_val, m_lbl) in enumerate(metrics):
        mx = Inches(0.8) + i * Inches(1.5)
        m_box = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, mx, Inches(5.1), Inches(1.4), Inches(1.4))
        m_box.fill.solid()
        m_box.fill.fore_color.rgb = C_WHITE
        m_box.line.color.rgb = C_BORDER_LIGHT
        m_box.line.width = Pt(1)
        tf = m_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = m_val
        p.font.name = FONT_HEAD
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = C_TEAL if i == 1 else (C_CORAL if i == 0 else C_DARK)
        p2 = tf.add_paragraph()
        p2.text = m_lbl
        p2.font.name = FONT_HEAD
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_MUTED

    # Right Column: Dominant Seller Review Console (60% width)
    c_left = Inches(5.6)
    c_top = Inches(0.75)
    c_w = Inches(6.933)
    c_h = Inches(5.9)

    con_bg = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, c_top, c_w, c_h)
    con_bg.fill.solid()
    con_bg.fill.fore_color.rgb = C_WHITE
    con_bg.line.color.rgb = C_BORDER_LIGHT
    con_bg.line.width = Pt(1)

    c_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, c_top, c_w, Inches(0.55))
    c_bar.fill.solid()
    c_bar.fill.fore_color.rgb = RGBColor(0x1F, 0x30, 0x2A)
    c_bar.line.fill.background()
    tf = c_bar.text_frame
    p = tf.paragraphs[0]
    p.text = f"{d1['console_mockup']['title']}  ·  {d1['console_mockup']['case_badge']}"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_ACCENT

    # Embedded product image inside Console!
    s1.shapes.add_picture(str(img_white), c_left + Inches(0.3), c_top + Inches(0.8), Inches(2.7), Inches(2.3))

    # Console Details (Right side of console)
    det_left = c_left + Inches(3.2)
    det_w = c_w - Inches(3.5)
    tb_det = s1.shapes.add_textbox(det_left, c_top + Inches(0.75), det_w, Inches(2.4))
    tf = tb_det.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "ORDER INFORMATION"
    p.font.name = FONT_MONO
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_SUBTLE

    p2 = tf.add_paragraph()
    p2.text = f"{d1['console_mockup']['order_info']['order_id']}  ·  {d1['console_mockup']['order_info']['sku']}\n{d1['console_mockup']['order_info']['color']}  ·  Price: {d1['console_mockup']['order_info']['price']}\n{d1['console_mockup']['order_info']['delivery']}"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = C_DARK

    p3 = tf.add_paragraph()
    p3.text = "\nEVIDENCE CITATION (STAGED)"
    p3.font.name = FONT_MONO
    p3.font.size = Pt(9.5)
    p3.font.bold = True
    p3.font.color.rgb = C_SUBTLE

    p4 = tf.add_paragraph()
    p4.text = f"{d1['console_mockup']['evidence_citation']['timestamp']}\n{d1['console_mockup']['evidence_citation']['observation']}"
    p4.font.name = FONT_HEAD
    p4.font.size = Pt(10.5)
    p4.font.color.rgb = C_MUTED

    # Contradiction Alert Box inside Console
    alert_box = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left + Inches(0.3), c_top + Inches(3.3), c_w - Inches(0.6), Inches(0.85))
    alert_box.fill.solid()
    alert_box.fill.fore_color.rgb = C_CORAL_LIGHT
    alert_box.line.color.rgb = C_CORAL
    alert_box.line.width = Pt(1)
    tf = alert_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = f"POLICY GATE: {d1['console_mockup']['evidence_citation']['status_badge']}"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_CORAL_DARK
    p2 = tf.add_paragraph()
    p2.text = f"{d1['console_mockup']['policy_check']['window_check']}  |  {d1['console_mockup']['policy_check']['color_check']}"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = C_CORAL_DARK

    # Status & 1-Click Action Button
    status_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left + Inches(0.3), c_top + Inches(4.35), c_w - Inches(0.6), Inches(0.45))
    status_bar.fill.solid()
    status_bar.fill.fore_color.rgb = C_AMBER_LIGHT
    status_bar.line.fill.background()
    p = status_bar.text_frame.paragraphs[0]
    p.text = d1['console_mockup']['action_prompt']
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x92, 0x40, 0x0E)
    p.alignment = PP_ALIGN.CENTER

    btn = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left + Inches(0.3), c_top + Inches(4.95), c_w - Inches(0.6), Inches(0.65))
    btn.fill.solid()
    btn.fill.fore_color.rgb = C_TEAL
    btn.line.fill.background()
    p = btn.text_frame.paragraphs[0]
    p.text = d1['console_mockup']['button_text']
    p.font.name = FONT_HEAD
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.alignment = PP_ALIGN.CENTER

    add_footer(s1, "ReturnLens · Pitch Deck · PS-04 Track · Team Rookie (3 Members)", "Slide 1 / 6")
    set_speaker_notes(s1, d1["speaker_notes"])

    # =========================================================================
    # SLIDE 2: THE PROBLEM (FOUR DISCONNECTED SOURCES & MISSING RECORD)
    # =========================================================================
    d2 = slides_data[2]
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2, C_CREAM)

    tb = s2.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(8.0), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = d2["tag"]
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    tb = s2.shapes.add_textbox(Inches(0.8), Inches(1.0), Inches(11.7), Inches(0.75))
    p = tb.text_frame.paragraphs[0]
    p.text = d2["headline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    tb = s2.shapes.add_textbox(Inches(0.8), Inches(1.75), Inches(11.7), Inches(0.5))
    p = tb.text_frame.paragraphs[0]
    p.text = d2["subheadline"] + "  ·  " + d2["supporting_statement"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(18)
    p.font.color.rgb = C_MUTED

    # 3-Column Layout without overlap:
    # Left: Sources 01 & 03 (Buyer Claim, Courier Tracking)
    # Center: Giant Critical Gap Card (NO SHARED EVIDENCE RECORD)
    # Right: Sources 02 & 04 (Store Truth, Return Policy)
    col_w = Inches(3.5)
    gap_w = Inches(4.333)
    card_h = Inches(1.95)

    # Source 01
    s1_box = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(2.45), col_w, card_h)
    s1_box.fill.solid()
    s1_box.fill.fore_color.rgb = C_WHITE
    s1_box.line.color.rgb = C_BORDER_LIGHT
    s1_box.line.width = Pt(1)
    tf = s1_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = f"{d2['sources'][0]['number']} {d2['sources'][0]['name'].upper()}"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p2 = tf.add_paragraph()
    p2.text = d2['sources'][0]['name']
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = C_DARK
    p3 = tf.add_paragraph()
    p3.text = d2['sources'][0]['detail']
    p3.font.name = FONT_HEAD
    p3.font.size = Pt(11)
    p3.font.color.rgb = C_MUTED

    # Source 03
    s3_box = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.6), col_w, card_h)
    s3_box.fill.solid()
    s3_box.fill.fore_color.rgb = C_WHITE
    s3_box.line.color.rgb = C_BORDER_LIGHT
    s3_box.line.width = Pt(1)
    tf = s3_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = f"{d2['sources'][2]['number']} {d2['sources'][2]['name'].upper()}"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p2 = tf.add_paragraph()
    p2.text = d2['sources'][2]['name']
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = C_DARK
    p3 = tf.add_paragraph()
    p3.text = d2['sources'][2]['detail']
    p3.font.name = FONT_HEAD
    p3.font.size = Pt(11)
    p3.font.color.rgb = C_MUTED

    # Center Gap Anchor
    c_gap = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.5), Inches(2.45), gap_w, Inches(4.1))
    c_gap.fill.solid()
    c_gap.fill.fore_color.rgb = C_DARK
    c_gap.line.color.rgb = C_CORAL
    c_gap.line.width = Pt(2)
    tf = c_gap.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "CRITICAL INFORMATION GAP"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_CORAL
    p.alignment = PP_ALIGN.CENTER

    p2 = tf.add_paragraph()
    p2.text = d2["gap_card"]["title"]
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = C_CREAM
    p2.alignment = PP_ALIGN.CENTER

    p3 = tf.add_paragraph()
    p3.text = "\n" + d2["gap_card"]["description"]
    p3.font.name = FONT_HEAD
    p3.font.size = Pt(11.5)
    p3.font.color.rgb = RGBColor(0xD1, 0xD5, 0xDB)
    p3.alignment = PP_ALIGN.CENTER

    p4 = tf.add_paragraph()
    p4.text = "\n9.0% vs 15.14%"
    p4.font.name = FONT_HEAD
    p4.font.size = Pt(16)
    p4.font.bold = True
    p4.font.color.rgb = C_CORAL
    p4.alignment = PP_ALIGN.CENTER

    p5 = tf.add_paragraph()
    p5.text = f"{data['meta']['fraud_metrics']['nrf_2025']}  |  {data['meta']['fraud_metrics']['deloitte_2024']}\n{data['meta']['fraud_metrics']['distinction']}"
    p5.font.name = FONT_HEAD
    p5.font.size = Pt(9)
    p5.font.color.rgb = RGBColor(0x9C, 0xA3, 0xAF)
    p5.alignment = PP_ALIGN.CENTER

    # Right: Sources 02 & 04
    s2_box = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.033), Inches(2.45), col_w, card_h)
    s2_box.fill.solid()
    s2_box.fill.fore_color.rgb = C_WHITE
    s2_box.line.color.rgb = C_BORDER_LIGHT
    s2_box.line.width = Pt(1)
    tf = s2_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = f"{d2['sources'][1]['number']} {d2['sources'][1]['name'].upper()}"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p2 = tf.add_paragraph()
    p2.text = d2['sources'][1]['name']
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = C_DARK
    p3 = tf.add_paragraph()
    p3.text = d2['sources'][1]['detail']
    p3.font.name = FONT_HEAD
    p3.font.size = Pt(11)
    p3.font.color.rgb = C_MUTED

    s4_box = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.033), Inches(4.6), col_w, card_h)
    s4_box.fill.solid()
    s4_box.fill.fore_color.rgb = C_WHITE
    s4_box.line.color.rgb = C_BORDER_LIGHT
    s4_box.line.width = Pt(1)
    tf = s4_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = f"{d2['sources'][3]['number']} {d2['sources'][3]['name'].upper()}"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p2 = tf.add_paragraph()
    p2.text = d2['sources'][3]['name']
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = C_DARK
    p3 = tf.add_paragraph()
    p3.text = d2['sources'][3]['detail']
    p3.font.name = FONT_HEAD
    p3.font.size = Pt(11)
    p3.font.color.rgb = C_MUTED

    add_footer(s2, "Fraud statistics note: 9.0% (NRF 2025, fraud only) vs 15.14% (Appriss/Deloitte 2024, fraud + abuse)", "Slide 2 / 6")
    set_speaker_notes(s2, d2["speaker_notes"])

    # =========================================================================
    # SLIDE 3: STAR DEMO / EVIDENCE CONTRADICTION (LARGE PRODUCT PHOTOS)
    # =========================================================================
    d3 = slides_data[3]
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3, C_CREAM)

    tb = s3.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(8.0), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = d3["tag"]
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    tb = s3.shapes.add_textbox(Inches(0.8), Inches(0.95), Inches(11.7), Inches(0.75))
    p = tb.text_frame.paragraphs[0]
    p.text = d3["headline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    tb = s3.shapes.add_textbox(Inches(0.8), Inches(1.7), Inches(11.7), Inches(0.45))
    p = tb.text_frame.paragraphs[0]
    p.text = d3["subheadline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(19)
    p.font.color.rgb = C_MUTED

    # Left: Visual Evidence Arena (66% width = 7.7 inches)
    ev_left = Inches(0.8)
    ev_top = Inches(2.25)
    ev_w = Inches(7.7)
    ev_h = Inches(4.45)

    ev_box = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, ev_left, ev_top, ev_w, ev_h)
    ev_box.fill.solid()
    ev_box.fill.fore_color.rgb = C_WHITE
    ev_box.line.color.rgb = C_BORDER_LIGHT
    ev_box.line.width = Pt(1)

    # Two large pictures: White vs Black
    pic_w = Inches(3.55)
    pic_h = Inches(2.8)

    s3.shapes.add_picture(str(img_white), ev_left + Inches(0.2), ev_top + Inches(0.2), pic_w, pic_h)
    s3.shapes.add_picture(str(img_black), ev_left + Inches(3.95), ev_top + Inches(0.2), pic_w, pic_h)

    # Badges below pictures
    b1 = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, ev_left + Inches(0.2), ev_top + Inches(3.1), pic_w, Inches(0.35))
    b1.fill.solid()
    b1.fill.fore_color.rgb = C_TEAL_LIGHT
    b1.line.fill.background()
    p = b1.text_frame.paragraphs[0]
    p.text = f"{d3['ordered_evidence']['label']}: {d3['ordered_evidence']['sku']} (WHITE)"
    p.font.name = FONT_MONO
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p.alignment = PP_ALIGN.CENTER

    b2 = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, ev_left + Inches(3.95), ev_top + Inches(3.1), pic_w, Inches(0.35))
    b2.fill.solid()
    b2.fill.fore_color.rgb = C_CORAL_LIGHT
    b2.line.fill.background()
    p = b2.text_frame.paragraphs[0]
    p.text = f"{d3['observed_evidence']['label']}: {d3['observed_evidence']['color'].upper()}"
    p.font.name = FONT_MONO
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = C_CORAL_DARK
    p.alignment = PP_ALIGN.CENTER

    # Caption / Footnote on Grounding
    tb_c = s3.shapes.add_textbox(ev_left + Inches(0.2), ev_top + Inches(3.55), ev_w - Inches(0.4), Inches(0.8))
    tf = tb_c.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Visual Grounding Honesty: Keyframe resolution reveals black casing. Exact SKU barcode is unreadable in this frame; ReturnLens factually records 'Observed Color: Midnight Black · Exact SKU: Not verified' and cites frame 00:07."
    p.font.name = FONT_HEAD
    p.font.size = Pt(10)
    p.font.color.rgb = C_MUTED

    # Right: Decision & Action Console (33% width = 3.8 inches)
    dec_left = Inches(8.75)
    dec_w = Inches(3.783)
    dec_box = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, dec_left, ev_top, dec_w, ev_h)
    dec_box.fill.solid()
    dec_box.fill.fore_color.rgb = C_WHITE
    dec_box.line.color.rgb = C_BORDER_LIGHT
    dec_box.line.width = Pt(1)

    tb = s3.shapes.add_textbox(dec_left + Inches(0.2), ev_top + Inches(0.15), dec_w - Inches(0.4), ev_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "DETERMINISTIC POLICY GATE"
    p.font.name = FONT_MONO
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_CORAL

    p2 = tf.add_paragraph()
    p2.text = "P-03: COLOR CONTRADICTION"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = C_CORAL_DARK

    p3 = tf.add_paragraph()
    p3.text = f"{d3['decision_panel']['next_action']}\nObserved: {d3['decision_panel']['observed_color']} · Exact SKU: {d3['decision_panel']['exact_sku']}"
    p3.font.name = FONT_MONO
    p3.font.size = Pt(9)
    p3.font.bold = True
    p3.font.color.rgb = C_CORAL_DARK

    p4 = tf.add_paragraph()
    p4.text = "\nSeller Resolution Options:"
    p4.font.name = FONT_HEAD
    p4.font.size = Pt(11)
    p4.font.bold = True
    p4.font.color.rgb = C_DARK

    for opt in d3['decision_panel']['seller_options']:
        p_opt = tf.add_paragraph()
        p_opt.text = opt
        p_opt.font.name = FONT_HEAD
        p_opt.font.size = Pt(9.5)
        p_opt.font.color.rgb = C_MUTED

    p5 = tf.add_paragraph()
    p5.text = f"\nFinancial Safety Ceiling:\n{data['meta']['refund_guardrail']['formula']}\nNo auto-denial · No refund released without seller click"
    p5.font.name = FONT_MONO
    p5.font.size = Pt(8.5)
    p5.font.color.rgb = C_MUTED

    add_footer(s3, "Illustrative staged evidence · Mock Shopify & Shippo APIs", "Slide 3 / 6")
    set_speaker_notes(s3, d3["speaker_notes"])

    # =========================================================================
    # SLIDE 4: THE AGENTIC SYSTEM (DARK ARCHITECTURE & STATEFUL LOOP)
    # =========================================================================
    d4 = slides_data[4]
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4, C_DARK_BG)

    tb = s4.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(8.0), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = d4["tag"]
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_ACCENT

    tb = s4.shapes.add_textbox(Inches(0.8), Inches(0.95), Inches(11.7), Inches(0.75))
    p = tb.text_frame.paragraphs[0]
    p.text = d4["headline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_CREAM

    tb = s4.shapes.add_textbox(Inches(0.8), Inches(1.65), Inches(11.7), Inches(0.45))
    p = tb.text_frame.paragraphs[0]
    p.text = d4["subheadline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(18)
    p.font.color.rgb = RGBColor(0xA3, 0xB8, 0xB0)

    # 1. Main Horizontal Pipeline (6 Steps with Arrows) - y = 2.25", h = 1.35"
    p_w = Inches(1.75)
    p_gap = Inches(0.24)
    p_top = Inches(2.25)
    p_h = Inches(1.35)

    pipe_colors = {
        "MODEL": (RGBColor(0x00, 0x38, 0x2B), C_TEAL_ACCENT),
        "CODE": (RGBColor(0x26, 0x38, 0x31), C_CREAM),
        "HUMAN": (RGBColor(0x45, 0x26, 0x0A), RGBColor(0xFB, 0xBF, 0x24))
    }

    for i, step in enumerate(d4["pipeline_steps"]):
        px = Inches(0.8) + i * (p_w + p_gap)
        tag_bg, tag_fg = pipe_colors.get(step["role"], (C_DARK, C_WHITE))

        box = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, px, p_top, p_w, p_h)
        box.fill.solid()
        box.fill.fore_color.rgb = C_CARD_DARK
        box.line.color.rgb = C_BORDER_DARK
        box.line.width = Pt(1)

        top_bar = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, px, p_top, p_w, Inches(0.04))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = tag_fg
        top_bar.line.fill.background()

        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"{step['num']} {step['name'].upper()}"
        p.font.name = FONT_MONO
        p.font.size = Pt(9)
        p.font.color.rgb = RGBColor(0x6C, 0x82, 0x79)

        p2 = tf.add_paragraph()
        p2.text = step['name']
        p2.font.name = FONT_HEAD
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = C_CREAM

        p3 = tf.add_paragraph()
        p3.text = step['desc']
        p3.font.name = FONT_HEAD
        p3.font.size = Pt(9)
        p3.font.color.rgb = RGBColor(0xA3, 0xB8, 0xB0)

        tb_tag = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, px + Inches(0.1), p_top + Inches(0.95), p_w - Inches(0.2), Inches(0.26))
        tb_tag.fill.solid()
        tb_tag.fill.fore_color.rgb = tag_bg
        tb_tag.line.fill.background()
        p = tb_tag.text_frame.paragraphs[0]
        p.text = step['role']
        p.font.name = FONT_MONO
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = tag_fg
        p.alignment = PP_ALIGN.CENTER

        if i < len(d4["pipeline_steps"]) - 1:
            arr_box = s4.shapes.add_textbox(px + p_w, p_top + Inches(0.4), p_gap, Inches(0.4))
            p_arr = arr_box.text_frame.paragraphs[0]
            p_arr.text = "→"
            p_arr.font.name = FONT_MONO
            p_arr.font.size = Pt(14)
            p_arr.font.bold = True
            p_arr.font.color.rgb = C_TEAL_ACCENT
            p_arr.alignment = PP_ALIGN.CENTER

    # 2. Dominant Center Section: Dual Operational Branches (y = 3.8", h = 1.7")
    br_top = Inches(3.8)
    br_h = Inches(1.7)

    # Left: Case C Dynamic Stateful Clarification Loop (7.1" width)
    c_box = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), br_top, Inches(7.1), br_h)
    c_box.fill.solid()
    c_box.fill.fore_color.rgb = RGBColor(0x14, 0x22, 0x1D)
    c_box.line.color.rgb = RGBColor(0x25, 0x63, 0xEB)
    c_box.line.width = Pt(1.5)
    tf = c_box.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = d4["case_c_flow"]["title"]
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)

    p2 = tf.add_paragraph()
    p2.text = "Dark Frames → ask_for_evidence() → WAITING_FOR_EVIDENCE → Customer Uploads → Resume Case"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = C_CREAM

    p3 = tf.add_paragraph()
    p3.text = "Agentic State Machine: When lighting is insufficient, the agent halts standard execution, prompts a targeted checklist, pauses state in WAITING_FOR_EVIDENCE, and seamlessly resumes context upon media receipt (1 retry limit protects customer experience)."
    p3.font.name = FONT_HEAD
    p3.font.size = Pt(9.5)
    p3.font.color.rgb = RGBColor(0xA3, 0xB8, 0xB0)

    # Right: Secondary Fast Path (4.4" width)
    f_box = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.133), br_top, Inches(4.4), br_h)
    f_box.fill.solid()
    f_box.fill.fore_color.rgb = RGBColor(0x14, 0x22, 0x1D)
    f_box.line.color.rgb = RGBColor(0x05, 0x96, 0x69)
    f_box.line.width = Pt(1.5)
    tf = f_box.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = d4["fast_path"]["title"]
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_ACCENT

    p2 = tf.add_paragraph()
    p2.text = f"{d4['fast_path']['query']} → Direct Mock Store & Courier Scan"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = C_CREAM

    p3 = tf.add_paragraph()
    p3.text = f"{d4['fast_path']['outcome']}\nRoutine order queries take a direct tool route without calling heavy multimodal models. Escalates to human seller only if courier scan shows abnormal transit delay."
    p3.font.name = FONT_HEAD
    p3.font.size = Pt(9.5)
    p3.font.color.rgb = RGBColor(0xA3, 0xB8, 0xB0)

    # 3. Bottom Governance Bar: Fill Space (y = 5.7", h = 1.05")
    gov_box = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.7), Inches(11.733), Inches(1.05))
    gov_box.fill.solid()
    gov_box.fill.fore_color.rgb = RGBColor(0x12, 0x1F, 0x1B)
    gov_box.line.color.rgb = C_BORDER_DARK
    gov_box.line.width = Pt(1)
    tf = gov_box.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = f"■ {d4['governance_rules'][0]['label']}: {d4['governance_rules'][0]['text']}   |   ■ {d4['governance_rules'][1]['label']}: {d4['governance_rules'][1]['text']}"
    p.font.name = FONT_MONO
    p.font.size = Pt(9)
    p.font.color.rgb = RGBColor(0xA3, 0xB8, 0xB0)

    p2 = tf.add_paragraph()
    p2.text = f"■ {d4['governance_rules'][2]['label']}: {d4['governance_rules'][2]['text']}   |   ■ {d4['governance_rules'][3]['label']}: {d4['governance_rules'][3]['text']}"
    p2.font.name = FONT_MONO
    p2.font.size = Pt(9)
    p2.font.color.rgb = RGBColor(0xA3, 0xB8, 0xB0)

    add_footer(s4, "Structured audit log recorded at every state transition · Decision priority: Contradiction > Hard fail > Unclear only > All pass", "Slide 4 / 6", is_dark=True)
    set_speaker_notes(s4, d4["speaker_notes"])

    # =========================================================================
    # SLIDE 5: FOUR DEMO BENCHMARK SCENARIOS (EXPANDED TO FILL CANVAS)
    # =========================================================================
    d5 = slides_data[5]
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5, C_CREAM)

    tb = s5.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(8.0), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = d5["tag"]
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    tb = s5.shapes.add_textbox(Inches(0.8), Inches(0.95), Inches(11.7), Inches(0.75))
    p = tb.text_frame.paragraphs[0]
    p.text = d5["headline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    tb = s5.shapes.add_textbox(Inches(0.8), Inches(1.65), Inches(11.7), Inches(0.45))
    p = tb.text_frame.paragraphs[0]
    p.text = d5["subheadline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(18)
    p.font.color.rgb = C_MUTED

    # 4 Expanded Scenario Rows: Fills from y = 2.25" to 6.8" (h = 1.05", gap = 0.12")
    row_top = Inches(2.25)
    row_h = Inches(1.02)
    row_gap = Inches(0.12)

    case_styles = [
        (C_TEAL_LIGHT, C_TEAL),
        (C_CORAL_LIGHT, C_CORAL_DARK),
        (C_BLUE_LIGHT, C_BLUE_TEXT),
        (RGBColor(0xEC, 0xFD, 0xF5), RGBColor(0x06, 0x5F, 0x46))
    ]

    for i, cs in enumerate(d5["cases"]):
        ry = row_top + i * (row_h + row_gap)
        bg_col, fg_col = case_styles[i]

        row_box = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), ry, Inches(11.733), row_h)
        row_box.fill.solid()
        row_box.fill.fore_color.rgb = C_WHITE
        row_box.line.color.rgb = C_BORDER_LIGHT
        row_box.line.width = Pt(1)

        # Badge
        badge = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), ry + Inches(0.22), Inches(2.2), Inches(0.55))
        badge.fill.solid()
        badge.fill.fore_color.rgb = bg_col
        badge.line.fill.background()
        tf = badge.text_frame
        p = tf.paragraphs[0]
        p.text = f"CASE {cs['number']} · {cs['name']}"
        p.font.name = FONT_MONO
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = fg_col
        p.alignment = PP_ALIGN.CENTER
        p2 = tf.add_paragraph()
        p2.text = cs['subtitle']
        p2.font.name = FONT_HEAD
        p2.font.size = Pt(9)
        p2.font.color.rgb = fg_col
        p2.alignment = PP_ALIGN.CENTER

        # Observation
        tb_ob = s5.shapes.add_textbox(Inches(3.35), ry + Inches(0.12), Inches(3.9), Inches(0.8))
        tf = tb_ob.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = cs['observation']
        p.font.name = FONT_HEAD
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_DARK

        # Arrow
        tb_arr = s5.shapes.add_textbox(Inches(7.35), ry + Inches(0.24), Inches(0.3), Inches(0.5))
        p = tb_arr.text_frame.paragraphs[0]
        p.text = "→"
        p.font.name = FONT_MONO
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = C_TEAL

        # Action & Outcome
        tb_act = s5.shapes.add_textbox(Inches(7.75), ry + Inches(0.12), Inches(4.6), Inches(0.8))
        tf = tb_act.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = cs['state_action']
        p.font.name = FONT_MONO
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = fg_col
        p2 = tf.add_paragraph()
        p2.text = cs['action_detail']
        p2.font.name = FONT_HEAD
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_MUTED

    add_footer(s5, "Staged prototype scenarios · Expected agent behaviors, not measured production metrics · Cap: min(₹4,999, remaining, paid)", "Slide 5 / 6")
    set_speaker_notes(s5, d5["speaker_notes"])

    # =========================================================================
    # SLIDE 6: 24-HOUR BUILD PLAN & STRICT SCOPE (RECOMPOSED & EXPANDED)
    # =========================================================================
    d6 = slides_data[6]
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6, C_CREAM)

    tb = s6.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(8.0), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = d6["tag"]
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    tb = s6.shapes.add_textbox(Inches(0.8), Inches(0.95), Inches(11.7), Inches(0.75))
    p = tb.text_frame.paragraphs[0]
    p.text = d6["headline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    tb = s6.shapes.add_textbox(Inches(0.8), Inches(1.65), Inches(11.7), Inches(0.45))
    p = tb.text_frame.paragraphs[0]
    p.text = d6["subheadline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(18)
    p.font.color.rgb = C_MUTED

    # 4-Phase Timeline Grid (y = 2.25", h = 1.8")
    t_top = Inches(2.25)
    t_h = Inches(1.8)
    t_w = Inches(2.8)
    t_gap = Inches(0.17)

    for i, phase in enumerate(d6["timeline"]):
        tx = Inches(0.8) + i * (t_w + t_gap)
        box = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, tx, t_top, t_w, t_h)
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER_LIGHT
        box.line.width = Pt(1)

        top_bar = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, tx, t_top, t_w, Inches(0.04))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = C_TEAL
        top_bar.line.fill.background()

        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"{phase['hours']} · {phase['phase']}"
        p.font.name = FONT_MONO
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_TEAL

        p2 = tf.add_paragraph()
        p2.text = phase['title']
        p2.font.name = FONT_HEAD
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = C_DARK

        p3 = tf.add_paragraph()
        p3.text = phase['owner']
        p3.font.name = FONT_HEAD
        p3.font.size = Pt(10)
        p3.font.bold = True
        p3.font.color.rgb = C_TEAL

        p4 = tf.add_paragraph()
        p4.text = phase['deliverables']
        p4.font.name = FONT_HEAD
        p4.font.size = Pt(9.5)
        p4.font.color.rgb = C_MUTED

    # Bottom Scope Grid: Generously filling y = 4.25" to 6.8" (h = 2.45")
    sc_top = Inches(4.25)
    sc_h = Inches(2.45)
    sc_w = Inches(5.75)

    # In Scope: MUST DELIVER
    in_box = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), sc_top, sc_w, sc_h)
    in_box.fill.solid()
    in_box.fill.fore_color.rgb = C_WHITE
    in_box.line.color.rgb = C_BORDER_LIGHT
    in_box.line.width = Pt(1)

    in_bar = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), sc_top, Inches(0.08), sc_h)
    in_bar.fill.solid()
    in_bar.fill.fore_color.rgb = C_TEAL
    in_bar.line.fill.background()

    tb = s6.shapes.add_textbox(Inches(1.05), sc_top + Inches(0.15), sc_w - Inches(0.35), sc_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "MUST DELIVER (CORE PROTOTYPE)"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    for item in d6["scope_boundaries"]["must_deliver"]:
        p_item = tf.add_paragraph()
        p_item.text = f"• {item}"
        p_item.font.name = FONT_HEAD
        p_item.font.size = Pt(10.5)
        p_item.font.color.rgb = C_DARK

    # Out of Scope: CUT FIRST IF BEHIND
    out_box = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.783), sc_top, sc_w, sc_h)
    out_box.fill.solid()
    out_box.fill.fore_color.rgb = C_WHITE
    out_box.line.color.rgb = C_BORDER_LIGHT
    out_box.line.width = Pt(1)

    out_bar = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.783), sc_top, Inches(0.08), sc_h)
    out_bar.fill.solid()
    out_bar.fill.fore_color.rgb = C_CORAL
    out_bar.line.fill.background()

    tb = s6.shapes.add_textbox(Inches(7.033), sc_top + Inches(0.15), sc_w - Inches(0.35), sc_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CUT FIRST IF BEHIND (DEFERRED EXPANSION)"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CORAL

    for item in d6["scope_boundaries"]["cut_first"]:
        p_item = tf.add_paragraph()
        p_item.text = f"• {item}"
        p_item.font.name = FONT_HEAD
        p_item.font.size = Pt(10.5)
        p_item.font.color.rgb = C_DARK

    add_footer(s6, "Team Rookie (3 Members) · PS-04 Autonomous Support Agent · 24-Hour Prototype Feasibility", "Slide 6 / 6")
    set_speaker_notes(s6, d6["speaker_notes"])

    # Output Saving
    out_deliv = base_dir / "deliverables" / "ReturnLens_v4.pptx"
    out_root = base_dir / "ReturnLens_v4.pptx"
    out_deliv.parent.mkdir(parents=True, exist_ok=True)

    prs.save(str(out_deliv))
    prs.save(str(out_root))
    print(f"Generated PPTX successfully:\n  -> {out_deliv} ({out_deliv.stat().st_size} bytes)\n  -> {out_root} ({out_root.stat().st_size} bytes)")

if __name__ == "__main__":
    build_pptx()
