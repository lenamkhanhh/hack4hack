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

    # Required assets validation
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
    C_AMBER_DARK = RGBColor(0x92, 0x40, 0x0E)
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
    # SLIDE 1: PRODUCT HERO & CONSOLE (CLEAR TYPOGRAPHY, ENLARGED CONSOLE COMPARISON)
    # =========================================================================
    d1 = slides_data[1]
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1, C_CREAM)

    left_x = Inches(0.8)
    left_w = Inches(4.7)

    # Tag
    tb = s1.shapes.add_textbox(left_x, Inches(0.75), left_w, Inches(0.35))
    p = tb.text_frame.paragraphs[0]
    p.text = d1["tag"]
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    # Headline
    tb = s1.shapes.add_textbox(left_x, Inches(1.15), left_w, Inches(1.0))
    p = tb.text_frame.paragraphs[0]
    p.text = d1["headline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    # Subheadline
    tb = s1.shapes.add_textbox(left_x, Inches(2.25), left_w, Inches(1.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = f"“{d1['subheadline']}”"
    p.font.name = FONT_HEAD
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    # Body (Concise 2 sentences, 16 pt)
    tb = s1.shapes.add_textbox(left_x, Inches(3.35), left_w, Inches(2.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = d1["summary"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    p2 = tf.add_paragraph()
    p2.text = f"\n{d1['supporting']}"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(14)
    p2.font.color.rgb = C_MUTED

    # Team Metadata (Clear separation at y = 6.0")
    tb_team = s1.shapes.add_textbox(left_x, Inches(6.05), left_w, Inches(0.4))
    p = tb_team.text_frame.paragraphs[0]
    p.text = d1["team_meta"]
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    # Right Column: Dominant Seller Review Console (x = 5.85", w = 6.683", h = 5.85")
    c_left = Inches(5.85)
    c_top = Inches(0.75)
    c_w = Inches(6.683)
    c_h = Inches(5.85)

    con_bg = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, c_top, c_w, c_h)
    con_bg.fill.solid()
    con_bg.fill.fore_color.rgb = C_WHITE
    con_bg.line.color.rgb = C_BORDER_LIGHT
    con_bg.line.width = Pt(1)

    c_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, c_top, c_w, Inches(0.5))
    c_bar.fill.solid()
    c_bar.fill.fore_color.rgb = RGBColor(0x1F, 0x30, 0x2A)
    c_bar.line.fill.background()
    tf = c_bar.text_frame
    p = tf.paragraphs[0]
    p.text = f"{d1['console_mockup']['title']}  ·  {d1['console_mockup']['case_badge']}"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_ACCENT

    # Side-by-side images inside Console
    pic_w = Inches(3.05)
    pic_h = Inches(2.15)
    pic_y = c_top + Inches(0.65)

    # Left: White Ordered
    s1.shapes.add_picture(str(img_white), c_left + Inches(0.2), pic_y, pic_w, pic_h)
    b_wht = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left + Inches(0.2), pic_y + pic_h + Inches(0.05), pic_w, Inches(0.35))
    b_wht.fill.solid()
    b_wht.fill.fore_color.rgb = C_TEAL_LIGHT
    b_wht.line.fill.background()
    b_wht.text_frame.margin_left = Inches(0.02)
    b_wht.text_frame.margin_right = Inches(0.02)
    p = b_wht.text_frame.paragraphs[0]
    p.text = f"ORDERED: {d1['console_mockup']['order_info']['sku']} (WHITE)"
    p.font.name = FONT_MONO
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p.alignment = PP_ALIGN.CENTER

    # Right: Black Observed
    s1.shapes.add_picture(str(img_black), c_left + Inches(3.433), pic_y, pic_w, pic_h)
    b_blk = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left + Inches(3.433), pic_y + pic_h + Inches(0.05), pic_w, Inches(0.35))
    b_blk.fill.solid()
    b_blk.fill.fore_color.rgb = C_CORAL_LIGHT
    b_blk.line.fill.background()
    b_blk.text_frame.margin_left = Inches(0.02)
    b_blk.text_frame.margin_right = Inches(0.02)
    p = b_blk.text_frame.paragraphs[0]
    p.text = "OBSERVED: BLACK ITEM · FRAME 00:07"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_CORAL_DARK
    p.alignment = PP_ALIGN.CENTER

    # Policy Alert Box inside Console
    alert_y = pic_y + pic_h + Inches(0.52)
    alert_box = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left + Inches(0.2), alert_y, c_w - Inches(0.4), Inches(0.72))
    alert_box.fill.solid()
    alert_box.fill.fore_color.rgb = C_CORAL_LIGHT
    alert_box.line.color.rgb = C_CORAL
    alert_box.line.width = Pt(1)
    tf = alert_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = d1['console_mockup']['evidence_citation']['status_badge']
    p.font.name = FONT_MONO
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_CORAL_DARK

    p2 = tf.add_paragraph()
    p2.text = f"{d1['console_mockup']['policy_check']['window_check']}  |  {d1['console_mockup']['policy_check']['color_check']}"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = C_CORAL_DARK

    # Status Pill
    status_y = alert_y + Inches(0.8)
    status_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left + Inches(0.2), status_y, c_w - Inches(0.4), Inches(0.42))
    status_bar.fill.solid()
    status_bar.fill.fore_color.rgb = C_AMBER_LIGHT
    status_bar.line.fill.background()
    p = status_bar.text_frame.paragraphs[0]
    p.text = d1['console_mockup']['action_prompt']
    p.font.name = FONT_MONO
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_AMBER_DARK
    p.alignment = PP_ALIGN.CENTER

    # 1-Click Action Button
    btn_y = status_y + Inches(0.5)
    btn = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left + Inches(0.2), btn_y, c_w - Inches(0.4), Inches(0.55))
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
    # SLIDE 2: THE PROBLEM (CLEAN VISUAL HIERARCHY, FOCAL CENTRAL QUESTION)
    # =========================================================================
    d2 = slides_data[2]
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2, C_CREAM)

    tb = s2.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(8.0), Inches(0.35))
    p = tb.text_frame.paragraphs[0]
    p.text = d2["tag"]
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    tb = s2.shapes.add_textbox(Inches(0.8), Inches(0.95), Inches(11.733), Inches(0.65))
    p = tb.text_frame.paragraphs[0]
    p.text = d2["headline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    tb = s2.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.733), Inches(0.45))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = f"{d2['subheadline']}  {d2['supporting_statement']}"
    p.font.name = FONT_HEAD
    p.font.size = Pt(18)
    p.font.color.rgb = C_MUTED

    # LEFT: 4 Compact Source Strips
    src_top = Inches(2.25)
    src_w = Inches(5.3)
    src_h = Inches(0.95)
    src_gap = Inches(0.12)

    for i, src in enumerate(d2["sources"]):
        sy = src_top + i * (src_h + src_gap)
        box = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), sy, src_w, src_h)
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER_LIGHT
        box.line.width = Pt(1)

        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"{src['number']}  {src['name'].upper()}"
        p.font.name = FONT_MONO
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_TEAL

        p2 = tf.add_paragraph()
        p2.text = src['detail']
        p2.font.name = FONT_HEAD
        p2.font.size = Pt(13)
        p2.font.color.rgb = C_DARK

    # Arrow connector pointing right
    arr_box = s2.shapes.add_textbox(Inches(6.25), Inches(3.8), Inches(0.4), Inches(0.6))
    p_arr = arr_box.text_frame.paragraphs[0]
    p_arr.text = "→"
    p_arr.font.name = FONT_MONO
    p_arr.font.size = Pt(32)
    p_arr.font.bold = True
    p_arr.font.color.rgb = C_CORAL

    # RIGHT: Prominent Focal Card (Clean, Uncluttered, Large Typography)
    gap_box = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), src_top, Inches(5.733), Inches(4.16))
    gap_box.fill.solid()
    gap_box.fill.fore_color.rgb = C_DARK
    gap_box.line.color.rgb = C_CORAL
    gap_box.line.width = Pt(2)
    tf = gap_box.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = d2["gap_card"]["tag"]
    p.font.name = FONT_MONO
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CORAL
    p.alignment = PP_ALIGN.CENTER

    p2 = tf.add_paragraph()
    p2.text = d2["gap_card"]["title"]
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(26)
    p2.font.bold = True
    p2.font.color.rgb = C_CREAM
    p2.alignment = PP_ALIGN.CENTER

    p3 = tf.add_paragraph()
    p3.text = f"\n“{d2['gap_card']['question']}”"
    p3.font.name = FONT_HEAD
    p3.font.size = Pt(18)
    p3.font.bold = True
    p3.font.italic = True
    p3.font.color.rgb = RGBColor(0xFB, 0xBF, 0x24)
    p3.alignment = PP_ALIGN.CENTER

    p4 = tf.add_paragraph()
    p4.text = f"\n{d2['gap_card']['statement']}"
    p4.font.name = FONT_HEAD
    p4.font.size = Pt(15)
    p4.font.bold = True
    p4.font.color.rgb = C_CREAM
    p4.alignment = PP_ALIGN.CENTER

    p5 = tf.add_paragraph()
    p5.text = f"\n{d2['gap_card']['note']}"
    p5.font.name = FONT_HEAD
    p5.font.size = Pt(13)
    p5.font.color.rgb = RGBColor(0xD1, 0xD5, 0xDB)
    p5.alignment = PP_ALIGN.CENTER

    add_footer(s2, "Fraud research: 9% strict fraud (NRF 2025) vs 15.14% fraud + abuse (Appriss/Deloitte 2024). Details in notes.", "Slide 2 / 6")
    set_speaker_notes(s2, d2["speaker_notes"])

    # =========================================================================
    # SLIDE 3: STAR DEMO (EVIDENCE ARENA & CLEAN DECISION PANEL)
    # =========================================================================
    d3 = slides_data[3]
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3, C_CREAM)

    tb = s3.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(8.0), Inches(0.35))
    p = tb.text_frame.paragraphs[0]
    p.text = d3["tag"]
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    tb = s3.shapes.add_textbox(Inches(0.8), Inches(0.9), Inches(11.733), Inches(0.65))
    p = tb.text_frame.paragraphs[0]
    p.text = d3["headline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    tb = s3.shapes.add_textbox(Inches(0.8), Inches(1.55), Inches(11.733), Inches(0.45))
    p = tb.text_frame.paragraphs[0]
    p.text = d3["subheadline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = C_MUTED

    # Primary Visual Area (7.6" width)
    ev_left = Inches(0.8)
    ev_top = Inches(2.15)
    ev_w = Inches(7.6)
    ev_h = Inches(4.45)

    ev_box = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, ev_left, ev_top, ev_w, ev_h)
    ev_box.fill.solid()
    ev_box.fill.fore_color.rgb = C_WHITE
    ev_box.line.color.rgb = C_BORDER_LIGHT
    ev_box.line.width = Pt(1)

    # Photos
    p_w = Inches(3.5)
    p_h = Inches(2.85)
    s3.shapes.add_picture(str(img_white), ev_left + Inches(0.2), ev_top + Inches(0.2), p_w, p_h)
    s3.shapes.add_picture(str(img_black), ev_left + Inches(3.9), ev_top + Inches(0.2), p_w, p_h)

    # Badges below photos
    b1 = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, ev_left + Inches(0.2), ev_top + Inches(3.15), p_w, Inches(0.38))
    b1.fill.solid()
    b1.fill.fore_color.rgb = C_TEAL_LIGHT
    b1.line.fill.background()
    p = b1.text_frame.paragraphs[0]
    p.text = f"{d3['ordered_evidence']['label']}: {d3['ordered_evidence']['sku']} (WHITE)"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p.alignment = PP_ALIGN.CENTER

    b2 = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, ev_left + Inches(3.9), ev_top + Inches(3.15), p_w, Inches(0.38))
    b2.fill.solid()
    b2.fill.fore_color.rgb = C_CORAL_LIGHT
    b2.line.fill.background()
    p = b2.text_frame.paragraphs[0]
    p.text = f"{d3['observed_evidence']['label']}: {d3['observed_evidence']['color'].upper()}"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CORAL_DARK
    p.alignment = PP_ALIGN.CENTER

    # Honest Grounding Caption
    tb_c = s3.shapes.add_textbox(ev_left + Inches(0.2), ev_top + Inches(3.65), ev_w - Inches(0.4), Inches(0.65))
    tf = tb_c.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = d3["grounding_caption"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_MUTED

    p2 = tf.add_paragraph()
    p2.text = "Frame citation provides a traceable timestamped reference, not absolute proof of video authenticity."
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = C_SUBTLE

    # Right Decision Region (3.833" width, clean stopping at y = 6.6")
    dec_left = Inches(8.7)
    dec_w = Inches(3.833)
    dec_box = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, dec_left, ev_top, dec_w, ev_h)
    dec_box.fill.solid()
    dec_box.fill.fore_color.rgb = C_WHITE
    dec_box.line.color.rgb = C_BORDER_LIGHT
    dec_box.line.width = Pt(1)

    tb_dec = s3.shapes.add_textbox(dec_left + Inches(0.25), ev_top + Inches(0.2), dec_w - Inches(0.5), ev_h - Inches(0.4))
    tf = tb_dec.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = d3["decision_panel"]["tag"]
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CORAL

    p2 = tf.add_paragraph()
    p2.text = d3["decision_panel"]["title"]
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = C_CORAL_DARK

    p3 = tf.add_paragraph()
    p3.text = f"\n• {d3['decision_panel']['items'][0]}"
    p3.font.name = FONT_HEAD
    p3.font.size = Pt(15)
    p3.font.bold = True
    p3.font.color.rgb = C_DARK

    p4 = tf.add_paragraph()
    p4.text = f"• {d3['decision_panel']['items'][1]}"
    p4.font.name = FONT_HEAD
    p4.font.size = Pt(15)
    p4.font.bold = True
    p4.font.color.rgb = C_CORAL_DARK

    p5 = tf.add_paragraph()
    p5.text = f"• {d3['decision_panel']['items'][2]}"
    p5.font.name = FONT_HEAD
    p5.font.size = Pt(14)
    p5.font.bold = True
    p5.font.color.rgb = C_MUTED

    # Prominent Action Pill inside decision panel
    act_box = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, dec_left + Inches(0.25), ev_top + Inches(2.7), dec_w - Inches(0.5), Inches(0.6))
    act_box.fill.solid()
    act_box.fill.fore_color.rgb = C_CORAL_LIGHT
    act_box.line.color.rgb = C_CORAL
    act_box.line.width = Pt(1.5)
    p_act = act_box.text_frame.paragraphs[0]
    p_act.text = d3["decision_panel"]["action_badge"]
    p_act.font.name = FONT_MONO
    p_act.font.size = Pt(14)
    p_act.font.bold = True
    p_act.font.color.rgb = C_CORAL_DARK
    p_act.alignment = PP_ALIGN.CENTER

    tb_sup = s3.shapes.add_textbox(dec_left + Inches(0.25), ev_top + Inches(3.45), dec_w - Inches(0.5), Inches(0.8))
    tf_sup = tb_sup.text_frame
    tf_sup.word_wrap = True
    p_sup = tf_sup.paragraphs[0]
    p_sup.text = d3["decision_panel"]["supporting"]
    p_sup.font.name = FONT_HEAD
    p_sup.font.size = Pt(13)
    p_sup.font.bold = True
    p_sup.font.color.rgb = C_DARK

    p_sup2 = tf_sup.add_paragraph()
    p_sup2.text = f"\nFinancial safety ceiling:\n0 < amount <= min(₹4,999, remaining, paid)"
    p_sup2.font.name = FONT_MONO
    p_sup2.font.size = Pt(10)
    p_sup2.font.color.rgb = C_MUTED

    add_footer(s3, "Illustrative staged evidence · Exact SKU: Not verified · Mock Shopify & Shippo APIs", "Slide 3 / 6")
    set_speaker_notes(s3, d3["speaker_notes"])

    # =========================================================================
    # SLIDE 4: THE AGENTIC SYSTEM (ZERO COLLISION, 3 DISTINCT AUTHORITY ZONES)
    # =========================================================================
    d4 = slides_data[4]
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4, C_DARK_BG)

    tb = s4.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(8.0), Inches(0.35))
    p = tb.text_frame.paragraphs[0]
    p.text = d4["tag"]
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_ACCENT

    tb = s4.shapes.add_textbox(Inches(0.8), Inches(0.9), Inches(11.733), Inches(0.65))
    p = tb.text_frame.paragraphs[0]
    p.text = d4["headline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_CREAM

    tb = s4.shapes.add_textbox(Inches(0.8), Inches(1.55), Inches(11.733), Inches(0.45))
    p = tb.text_frame.paragraphs[0]
    p.text = d4["subheadline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(18)
    p.font.color.rgb = RGBColor(0xA3, 0xB8, 0xB0)

    # Level 1: Three Distinct Authority Zones (y = 2.15", h = 1.35")
    z_top = Inches(2.15)
    z_h = Inches(1.35)
    zones = [
        (d4["authority_zones"][0]["name"], d4["authority_zones"][0]["role"], d4["authority_zones"][0]["desc"], C_TEAL_ACCENT, Inches(3.6)),
        (d4["authority_zones"][1]["name"], d4["authority_zones"][1]["role"], d4["authority_zones"][1]["desc"], C_CREAM, Inches(4.3)),
        (d4["authority_zones"][2]["name"], d4["authority_zones"][2]["role"], d4["authority_zones"][2]["desc"], RGBColor(0xFB, 0xBF, 0x24), Inches(3.353))
    ]

    curr_x = Inches(0.8)
    for z_name, z_role, z_desc, z_fg, z_w in zones:
        z_box = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, curr_x, z_top, z_w, z_h)
        z_box.fill.solid()
        z_box.fill.fore_color.rgb = C_CARD_DARK
        z_box.line.color.rgb = C_BORDER_DARK
        z_box.line.width = Pt(1)

        t_bar = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, curr_x, z_top, z_w, Inches(0.04))
        t_bar.fill.solid()
        t_bar.fill.fore_color.rgb = z_fg
        t_bar.line.fill.background()

        tf = z_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = z_name
        p.font.name = FONT_MONO
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = z_fg

        p2 = tf.add_paragraph()
        p2.text = z_role
        p2.font.name = FONT_HEAD
        p2.font.size = Pt(15.5)
        p2.font.bold = True
        p2.font.color.rgb = C_CREAM

        p3 = tf.add_paragraph()
        p3.text = z_desc
        p3.font.name = FONT_HEAD
        p3.font.size = Pt(12)
        p3.font.color.rgb = RGBColor(0xA3, 0xB8, 0xB0)

        curr_x += z_w + Inches(0.24)

    # Level 2: Dominant Technical Diagram — Case C Stateful Clarification Loop
    # (Container without internal text to avoid ANY collision!)
    c_top = Inches(3.72)
    c_h = Inches(2.05)
    c_box = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), c_top, Inches(11.733), c_h)
    c_box.fill.solid()
    c_box.fill.fore_color.rgb = RGBColor(0x14, 0x22, 0x1D)
    c_box.line.color.rgb = RGBColor(0x25, 0x63, 0xEB)
    c_box.line.width = Pt(1.5)

    # Title as standalone shape at top of container (ZERO collision with nodes!)
    tb_title = s4.shapes.add_textbox(Inches(1.0), c_top + Inches(0.12), Inches(11.333), Inches(0.35))
    p_title = tb_title.text_frame.paragraphs[0]
    p_title.text = d4["case_c_flow"]["title"]
    p_title.font.name = FONT_MONO
    p_title.font.size = Pt(13)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)

    # Draw 6 connected state nodes at y = c_top + 0.55"
    nodes = d4["case_c_flow"]["steps"]
    n_w = Inches(1.78)
    n_gap = Inches(0.18)
    n_y = c_top + Inches(0.55)
    n_h = Inches(0.65)

    for i, node_txt in enumerate(nodes):
        nx = Inches(0.95) + i * (n_w + n_gap)
        is_highlight = "WAITING" in node_txt or "RESUME" in node_txt
        n_box = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, nx, n_y, n_w, n_h)
        n_box.fill.solid()
        n_box.fill.fore_color.rgb = RGBColor(0x1E, 0x3A, 0x8A) if is_highlight else RGBColor(0x1F, 0x30, 0x2A)
        n_box.line.color.rgb = RGBColor(0x60, 0xA5, 0xFA) if is_highlight else C_BORDER_DARK
        n_box.line.width = Pt(1.5) if is_highlight else Pt(1)

        tf_n = n_box.text_frame
        tf_n.word_wrap = True
        tf_n.margin_left = Inches(0.03)
        tf_n.margin_right = Inches(0.03)
        p_n = tf_n.paragraphs[0]
        p_n.text = node_txt
        p_n.font.name = FONT_MONO
        p_n.font.size = Pt(10)
        p_n.font.bold = True
        p_n.font.color.rgb = RGBColor(0xDB, 0xEA, 0xFE) if is_highlight else C_CREAM
        p_n.alignment = PP_ALIGN.CENTER

        if i < len(nodes) - 1:
            arr = s4.shapes.add_textbox(nx + n_w - Inches(0.02), n_y + Inches(0.12), n_gap + Inches(0.04), Inches(0.4))
            p_a = arr.text_frame.paragraphs[0]
            p_a.text = "→"
            p_a.font.name = FONT_MONO
            p_a.font.size = Pt(14)
            p_a.font.bold = True
            p_a.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)
            p_a.alignment = PP_ALIGN.CENTER

    # Clean sublabel under nodes inside container
    tb_c_sub = s4.shapes.add_textbox(Inches(1.0), c_top + Inches(1.35), Inches(11.333), Inches(0.55))
    tf_sub = tb_c_sub.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = d4["case_c_flow"]["sublabel"]
    p_sub.font.name = FONT_HEAD
    p_sub.font.size = Pt(12.5)
    p_sub.font.color.rgb = RGBColor(0xA3, 0xB8, 0xB0)

    # Level 3: Secondary Fast Path & Output Trace (y = 5.95", h = 0.78")
    bot_y = Inches(5.95)
    bot_box = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), bot_y, Inches(11.733), Inches(0.78))
    bot_box.fill.solid()
    bot_box.fill.fore_color.rgb = RGBColor(0x12, 0x1F, 0x1B)
    bot_box.line.color.rgb = C_BORDER_DARK
    bot_box.line.width = Pt(1)

    tf_bot = bot_box.text_frame
    tf_bot.word_wrap = True
    p = tf_bot.paragraphs[0]
    p.text = d4["secondary_route"]["text"]
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x34, 0xD3, 0x99)

    p2 = tf_bot.add_paragraph()
    p2.text = d4["audit_output"]["text"]
    p2.font.name = FONT_MONO
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = RGBColor(0xA3, 0xB8, 0xB0)

    add_footer(s4, "Structured JSON Audit Log recorded at every state transition · Decision priority: Contradiction > Hard fail > Unclear only > All pass", "Slide 4 / 6", is_dark=True)
    set_speaker_notes(s4, d4["speaker_notes"])

    # =========================================================================
    # SLIDE 5: AGENT BEHAVIOR MATRIX (CLEAN 4-LANE EDITORIAL MATRIX, NO DASHBOARD FEEL)
    # =========================================================================
    d5 = slides_data[5]
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5, C_CREAM)

    tb = s5.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(8.0), Inches(0.35))
    p = tb.text_frame.paragraphs[0]
    p.text = d5["tag"]
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    tb = s5.shapes.add_textbox(Inches(0.8), Inches(0.9), Inches(11.733), Inches(0.65))
    p = tb.text_frame.paragraphs[0]
    p.text = d5["headline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    tb = s5.shapes.add_textbox(Inches(0.8), Inches(1.55), Inches(11.733), Inches(0.45))
    p = tb.text_frame.paragraphs[0]
    p.text = d5["subheadline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(18)
    p.font.color.rgb = C_MUTED

    # 4 Clean Editorial Scenario Lanes (y = 2.25" to 6.55", h = 0.95", gap = 0.12")
    lane_top = Inches(2.25)
    lane_h = Inches(0.95)
    lane_gap = Inches(0.12)

    case_colors = [
        (C_TEAL_LIGHT, C_TEAL),
        (C_CORAL_LIGHT, C_CORAL_DARK),
        (C_BLUE_LIGHT, C_BLUE_TEXT),
        (RGBColor(0xEC, 0xFD, 0xF5), RGBColor(0x06, 0x5F, 0x46))
    ]

    for i, cs in enumerate(d5["cases"]):
        ly = lane_top + i * (lane_h + lane_gap)
        bg_col, fg_col = case_colors[i]

        lane_box = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), ly, Inches(11.733), lane_h)
        lane_box.fill.solid()
        lane_box.fill.fore_color.rgb = C_WHITE
        lane_box.line.color.rgb = C_BORDER_LIGHT
        lane_box.line.width = Pt(1)

        # Subtle badge
        badge = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), ly + Inches(0.22), Inches(2.2), Inches(0.5))
        badge.fill.solid()
        badge.fill.fore_color.rgb = bg_col
        badge.line.fill.background()
        p = badge.text_frame.paragraphs[0]
        p.text = f"{cs['number']} · {cs['name']}"
        p.font.name = FONT_MONO
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = fg_col
        p.alignment = PP_ALIGN.CENTER

        # Observation
        tb_ob = s5.shapes.add_textbox(Inches(3.35), ly + Inches(0.12), Inches(4.0), Inches(0.7))
        tf = tb_ob.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = cs['observation']
        p.font.name = FONT_HEAD
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_DARK

        # Arrow
        tb_a = s5.shapes.add_textbox(Inches(7.45), ly + Inches(0.2), Inches(0.3), Inches(0.5))
        p = tb_a.text_frame.paragraphs[0]
        p.text = "→"
        p.font.name = FONT_MONO
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = C_TEAL

        # Action (Prominent action header, 14 pt bold!)
        tb_ac = s5.shapes.add_textbox(Inches(7.85), ly + Inches(0.1), Inches(4.5), Inches(0.75))
        tf = tb_ac.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = cs['action']
        p.font.name = FONT_MONO
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = fg_col

        p2 = tf.add_paragraph()
        p2.text = cs['detail']
        p2.font.name = FONT_HEAD
        p2.font.size = Pt(12)
        p2.font.color.rgb = C_MUTED

    add_footer(s5, "Staged prototype scenarios · Expected agent behaviors, not measured production metrics", "Slide 5 / 6")
    set_speaker_notes(s5, d5["speaker_notes"])

    # =========================================================================
    # SLIDE 6: 24-HOUR PROTOTYPE PLAN (CONTINUOUS TIMELINE + DISCIPLINED SCOPE)
    # =========================================================================
    d6 = slides_data[6]
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6, C_CREAM)

    tb = s6.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(8.0), Inches(0.35))
    p = tb.text_frame.paragraphs[0]
    p.text = d6["tag"]
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    tb = s6.shapes.add_textbox(Inches(0.8), Inches(0.9), Inches(11.733), Inches(0.65))
    p = tb.text_frame.paragraphs[0]
    p.text = d6["headline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    tb = s6.shapes.add_textbox(Inches(0.8), Inches(1.55), Inches(11.733), Inches(0.45))
    p = tb.text_frame.paragraphs[0]
    p.text = d6["subheadline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(18)
    p.font.color.rgb = C_MUTED

    # Continuous Horizontal Timeline (y = 2.2", h = 1.9")
    t_top = Inches(2.2)
    t_h = Inches(1.9)
    t_w = Inches(2.8)
    t_gap = Inches(0.17)

    # Continuous accent line across all 4 milestones
    conn_line = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), t_top, Inches(11.733), Inches(0.04))
    conn_line.fill.solid()
    conn_line.fill.fore_color.rgb = C_TEAL
    conn_line.line.fill.background()

    for i, phase in enumerate(d6["timeline"]):
        tx = Inches(0.8) + i * (t_w + t_gap)
        box = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, tx, t_top + Inches(0.04), t_w, t_h - Inches(0.04))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER_LIGHT
        box.line.width = Pt(1)

        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = phase['hours']
        p.font.name = FONT_MONO
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_TEAL

        p2 = tf.add_paragraph()
        p2.text = phase['title']
        p2.font.name = FONT_HEAD
        p2.font.size = Pt(15)
        p2.font.bold = True
        p2.font.color.rgb = C_DARK

        p3 = tf.add_paragraph()
        p3.text = phase['owner']
        p3.font.name = FONT_HEAD
        p3.font.size = Pt(11.5)
        p3.font.bold = True
        p3.font.color.rgb = C_TEAL

        p4 = tf.add_paragraph()
        p4.text = phase['desc']
        p4.font.name = FONT_HEAD
        p4.font.size = Pt(11)
        p4.font.color.rgb = C_MUTED

    # Disciplined Scope Split (Compact, Balanced)
    sc_top = Inches(4.35)
    sc_h = Inches(2.3)
    sc_w = Inches(5.75)

    # Must Deliver
    in_box = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), sc_top, sc_w, sc_h)
    in_box.fill.solid()
    in_box.fill.fore_color.rgb = C_WHITE
    in_box.line.color.rgb = C_BORDER_LIGHT
    in_box.line.width = Pt(1)

    in_bar = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), sc_top, Inches(0.08), sc_h)
    in_bar.fill.solid()
    in_bar.fill.fore_color.rgb = C_TEAL
    in_bar.line.fill.background()

    tb = s6.shapes.add_textbox(Inches(1.05), sc_top + Inches(0.12), sc_w - Inches(0.35), sc_h - Inches(0.24))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "MUST DELIVER (CORE PROTOTYPE)"
    p.font.name = FONT_MONO
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    for item in d6["scope_boundaries"]["must_deliver"]:
        p_item = tf.add_paragraph()
        p_item.text = f"• {item}"
        p_item.font.name = FONT_HEAD
        p_item.font.size = Pt(12)
        p_item.font.color.rgb = C_DARK

    # Cut First If Behind
    out_box = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.783), sc_top, sc_w, sc_h)
    out_box.fill.solid()
    out_box.fill.fore_color.rgb = C_WHITE
    out_box.line.color.rgb = C_BORDER_LIGHT
    out_box.line.width = Pt(1)

    out_bar = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.783), sc_top, Inches(0.08), sc_h)
    out_bar.fill.solid()
    out_bar.fill.fore_color.rgb = C_CORAL
    out_bar.line.fill.background()

    tb = s6.shapes.add_textbox(Inches(7.033), sc_top + Inches(0.12), sc_w - Inches(0.35), sc_h - Inches(0.24))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CUT FIRST IF BEHIND (DEFERRED EXPANSION)"
    p.font.name = FONT_MONO
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CORAL

    for item in d6["scope_boundaries"]["cut_first"]:
        p_item = tf.add_paragraph()
        p_item.text = f"• {item}"
        p_item.font.name = FONT_HEAD
        p_item.font.size = Pt(12)
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
