import os
import sys
import json
import zipfile
import shutil
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml

sys.stdout.reconfigure(encoding='utf-8')

def build_v9_3_pptx():
    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / "content" / "deck_data_v9_3.json"
    deliverables_dir = base_dir / "deliverables"
    assets_dir = base_dir / "src" / "assets"
    deliverables_dir.mkdir(parents=True, exist_ok=True)

    if not data_path.exists():
        raise FileNotFoundError(f"Missing canonical data: {data_path}")

    with open(data_path, "r", encoding="utf-8") as f:
        deck_data = json.load(f)

    slides_data = {s["slide_number"]: s for s in deck_data["slides"]}

    # Initialize 16:9 Widescreen Presentation (13.333 x 7.50 inches)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.50)
    blank_layout = prs.slide_layouts[6]

    # ReturnLens Minimalist Architectural Palette
    C_BG = RGBColor(0xFA, 0xFA, 0xF9)             # Gallery Warm Off-White (#FAFAF9)
    C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)          # Pure White (#FFFFFF)
    C_TEXT_PRIMARY = RGBColor(0x11, 0x18, 0x15)   # Deep Near-Black Charcoal (#111815)
    C_TEXT_SECONDARY = RGBColor(0x38, 0x44, 0x3E) # Readable Body Charcoal (#38443E)
    C_TEXT_MUTED = RGBColor(0x6E, 0x7B, 0x74)     # Subtle Sage Slate (#6E7B74)
    C_LINE = RGBColor(0xE4, 0xE2, 0xDC)           # Crisp Neutral Hairline (#E4E2DC)

    # Restrained Accents
    C_PINE = RGBColor(0x0C, 0x5E, 0x4B)           # Brand Pine Green (#0C5E4B)
    C_CORAL = RGBColor(0xC8, 0x4D, 0x33)          # Terracotta Coral (#C84D33)
    C_CORAL_DARK = RGBColor(0x9E, 0x2A, 0x2B)     # Deep Terracotta (#9E2A2B)

    # Typography: Arial with strict hierarchy
    FONT_HEAD = "Arial"
    FONT_BODY = "Arial"

    # Images (1376x768, 16:9 ratio locked)
    img_white_order = assets_dir / "studio_white_headphones.jpg"
    img_black_unboxing = assets_dir / "unboxing_black_headphones.jpg"

    def add_flat_rect(slide, left, top, width, height, fill_rgb=None, line_rgb=None, line_width_pt=0.5, no_line=False):
        """
        Creates a truly flat rectangle without theme line (accent1 blue) or theme effects (shadow/bevel).
        Explicitly removes <p:style>, clears <a:effectLst/>, and specifies fills and strokes.
        """
        sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        sp = sh._element

        style = sp.find('{http://schemas.openxmlformats.org/presentationml/2006/main}style')
        if style is not None:
            sp.remove(style)

        spPr = sp.spPr

        for tag in ['solidFill', 'noFill', 'gradFill', 'blipFill', 'pattFill', 'grpFill']:
            el = spPr.find(f'{{http://schemas.openxmlformats.org/drawingml/2006/main}}{tag}')
            if el is not None:
                spPr.remove(el)

        if fill_rgb is not None:
            hex_val = f"{fill_rgb[0]:02X}{fill_rgb[1]:02X}{fill_rgb[2]:02X}"
            spPr.append(parse_xml(f'<a:solidFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:srgbClr val="{hex_val}"/></a:solidFill>'))
        else:
            spPr.append(parse_xml('<a:noFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'))

        existing_ln = spPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}ln')
        if existing_ln is not None:
            spPr.remove(existing_ln)

        if no_line or line_rgb is None:
            spPr.append(parse_xml('<a:ln xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:noFill/></a:ln>'))
        else:
            hex_line = f"{line_rgb[0]:02X}{line_rgb[1]:02X}{line_rgb[2]:02X}"
            w_emu = int(line_width_pt * 12700)
            spPr.append(parse_xml(f'<a:ln xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" w="{w_emu}"><a:solidFill><a:srgbClr val="{hex_line}"/></a:solidFill><a:prstDash val="solid"/></a:ln>'))

        existing_eff = spPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
        if existing_eff is not None:
            spPr.remove(existing_eff)
        spPr.append(parse_xml('<a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'))

        return sh

    def set_bg(slide, color=C_BG):
        return add_flat_rect(slide, 0, 0, prs.slide_width, prs.slide_height, fill_rgb=color, no_line=True)

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

    # Left Column: Brand, Tagline, Support Agent Summary, Principle
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
    p.text = d1.get("summary", "A support agent for solo sellers that handles order status, returns and refunds—using video evidence to triage disputed claims.")
    p.font.name = FONT_BODY
    p.font.size = Pt(15)
    p.font.color.rgb = C_TEXT_SECONDARY
    p.space_after = Pt(26)

    # Thin Flat Divider Line (0.5 pt, no shadow)
    add_flat_rect(s1, Inches(0.80), Inches(4.85), Inches(4.70), Inches(0.015), fill_rgb=C_LINE, no_line=True)

    # Core Principle
    tb_pr = s1.shapes.add_textbox(Inches(0.80), Inches(5.05), col_w1, Inches(0.80))
    tf_pr = tb_pr.text_frame
    tf_pr.word_wrap = True
    tf_pr.margin_left = tf_pr.margin_top = 0
    p = tf_pr.paragraphs[0]
    p.text = d1.get("principle", "Models observe. Code verifies. Seller authorizes.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY

    # Right Column: Clean, Flat Seller View Mockup
    m_x, m_y, m_w, m_h = Inches(5.90), Inches(0.75), Inches(6.65), Inches(5.75)
    mock = d1["mockup"]

    add_flat_rect(s1, m_x, m_y, m_w, m_h, fill_rgb=C_WHITE, line_rgb=C_LINE, line_width_pt=0.5)

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

    # Flat divider below header
    add_flat_rect(s1, m_x, m_y + Inches(0.55), m_w, Inches(0.015), fill_rgb=C_LINE, no_line=True)

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

    # Side-by-side Evidence Photos (Aspect ratio locked at 1.79167)
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

    # Discrepancy Callout Strip
    dis_y = m_y + Inches(3.40)
    add_flat_rect(s1, m_x + Inches(0.30), dis_y, Inches(0.035), Inches(0.70), fill_rgb=C_CORAL, no_line=True)

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

    # Flat divider above action
    add_flat_rect(s1, m_x, m_y + Inches(4.35), m_w, Inches(0.015), fill_rgb=C_LINE, no_line=True)

    # Decision Footer
    tb_mfa = s1.shapes.add_textbox(m_x + Inches(0.30), m_y + Inches(4.55), Inches(3.55), Inches(0.60))
    tf_mfa = tb_mfa.text_frame
    tf_mfa.word_wrap = True
    tf_mfa.margin_left = tf_mfa.margin_top = 0
    p = tf_mfa.paragraphs[0]
    p.text = mock["authority_note"]
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY
    p = tf_mfa.add_paragraph()
    p.text = mock["safety_note"]
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.color.rgb = C_TEXT_MUTED

    btn_m = add_flat_rect(s1, m_x + Inches(3.90), m_y + Inches(4.55), Inches(2.45), Inches(0.48), fill_rgb=C_PINE, no_line=True)
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

    # Title
    tb = s2.shapes.add_textbox(Inches(0.80), Inches(1.10), Inches(11.70), Inches(0.60))
    tf = tb.text_frame
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = d2.get("title", "One claim. Four disconnected sources.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(34)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY

    # 1. Customer Claim Quote Block (Flat left accent bar, concise attachment)
    quote_y = Inches(1.90)
    quote_h = Inches(1.10)
    add_flat_rect(s2, Inches(0.80), quote_y, Inches(0.035), quote_h, fill_rgb=C_PINE, no_line=True)

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

    # 2. Four Disconnected Sources
    src_y = Inches(3.30)
    src_w = Inches(2.70)
    src_gap = Inches(0.30)
    for i, src in enumerate(d2["sources"]):
        sx = Inches(0.80) + i * (src_w + src_gap)

        add_flat_rect(s2, sx, src_y, src_w, Inches(0.015), fill_rgb=C_LINE, no_line=True)

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

    # 3. Bottom Decision Question
    dil_y = Inches(5.15)
    add_flat_rect(s2, Inches(0.80), dil_y, Inches(11.73), Inches(0.015), fill_rgb=C_LINE, no_line=True)

    tb_dil = s2.shapes.add_textbox(Inches(0.80), dil_y + Inches(0.25), Inches(11.73), Inches(0.95))
    tf_d = tb_dil.text_frame
    tf_d.word_wrap = True
    tf_d.margin_left = tf_d.margin_top = 0

    p = tf_d.paragraphs[0]
    p.text = d2.get("seller_question", "Should I request more evidence, approve a return, or inspect the parcel?")
    p.font.name = FONT_BODY
    p.font.size = Pt(17)
    p.font.bold = False
    p.font.color.rgb = C_TEXT_PRIMARY

    add_page_number(s2, "02")
    add_notes(s2, d2["speaker_notes"])

    # =========================================================
    # SLIDE 3: THE CORE DEMONSTRATION (WHITE ORDERED. BLACK SHOWN.)
    # =========================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    d3 = slides_data[3]

    # Kicker
    tb = s3.shapes.add_textbox(Inches(0.80), Inches(0.70), Inches(8.0), Inches(0.22))
    p = tb.text_frame.paragraphs[0]
    p.text = d3.get("kicker", "Core Evidence Comparison")
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PINE

    # Title & Subtitle ("White ordered. Black shown.")
    tb = s3.shapes.add_textbox(Inches(0.80), Inches(0.95), Inches(11.73), Inches(0.70))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = d3.get("title", "White ordered. Black shown.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY
    p.space_after = Pt(2)
    p = tf.add_paragraph()
    p.text = d3.get("subtitle", "Order details, video evidence and the next step—in one view.")
    p.font.name = FONT_BODY
    p.font.size = Pt(15)
    p.font.color.rgb = C_TEXT_MUTED

    # Two Large Showcase Photos: Flat images, exact 16:9 ratio locked!
    img3_w = Inches(4.60)
    img3_h = Inches(2.57)
    img3_y = Inches(2.20)

    # Left: Studio White
    tb_h_l = s3.shapes.add_textbox(Inches(0.80), Inches(1.95), img3_w, Inches(0.20))
    tf_hl = tb_h_l.text_frame
    tf_hl.margin_left = tf_hl.margin_top = 0
    p = tf_hl.paragraphs[0]
    p.text = d3["left_evidence"]["label"]
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_PINE

    if img_white_order.exists():
        s3.shapes.add_picture(str(img_white_order), Inches(0.80), img3_y, img3_w, img3_h)

    tb_c_l = s3.shapes.add_textbox(Inches(0.80), Inches(4.85), img3_w, Inches(0.48))
    tf_cl = tb_c_l.text_frame
    tf_cl.margin_left = tf_cl.margin_top = 0
    p = tf_cl.paragraphs[0]
    p.text = d3["left_evidence"]["headline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY
    p.space_after = Pt(1)
    p = tf_cl.add_paragraph()
    p.text = d3["left_evidence"]["meta"]
    p.font.name = FONT_BODY
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MUTED

    # Center Discrepancy Indicator
    tb_neq = s3.shapes.add_textbox(Inches(5.40), img3_y + Inches(1.00), Inches(2.53), Inches(0.50))
    p_neq = tb_neq.text_frame.paragraphs[0]
    p_neq.alignment = PP_ALIGN.CENTER
    p_neq.text = "≠"
    p_neq.font.name = FONT_HEAD
    p_neq.font.size = Pt(28)
    p_neq.font.bold = True
    p_neq.font.color.rgb = C_CORAL

    # Right: Customer Black Unboxing
    tb_h_r = s3.shapes.add_textbox(Inches(7.93), Inches(1.95), img3_w, Inches(0.20))
    tf_hr = tb_h_r.text_frame
    tf_hr.margin_left = tf_hr.margin_top = 0
    p = tf_hr.paragraphs[0]
    p.text = d3["right_evidence"]["label"]
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_CORAL

    if img_black_unboxing.exists():
        s3.shapes.add_picture(str(img_black_unboxing), Inches(7.93), img3_y, img3_w, img3_h)

    tb_c_r = s3.shapes.add_textbox(Inches(7.93), Inches(4.85), img3_w, Inches(0.48))
    tf_cr = tb_c_r.text_frame
    tf_cr.margin_left = tf_cr.margin_top = 0
    p = tf_cr.paragraphs[0]
    p.text = d3["right_evidence"]["headline"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_CORAL
    p.space_after = Pt(1)
    p = tf_cr.add_paragraph()
    p.text = d3["right_evidence"]["meta"]
    p.font.name = FONT_BODY
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MUTED

    # Divider below photos: placed at y=5.50"
    opt_y = Inches(5.50)
    add_flat_rect(s3, Inches(0.80), opt_y, Inches(11.73), Inches(0.015), fill_rgb=C_LINE, no_line=True)

    # Bottom Prepared Options
    # Option 1: Approve return ("1. Approve return")
    tb_o1 = s3.shapes.add_textbox(Inches(0.80), opt_y + Inches(0.12), Inches(3.60), Inches(0.65))
    tf_o1 = tb_o1.text_frame
    tf_o1.word_wrap = True
    tf_o1.margin_left = tf_o1.margin_top = 0
    p = tf_o1.paragraphs[0]
    p.text = d3["options"][0]["title"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY
    p.space_after = Pt(2)
    p = tf_o1.add_paragraph()
    p.text = d3["options"][0]["action"]
    p.font.name = FONT_BODY
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MUTED

    # Option 2: Request label photo (emphasized with flat pine green vertical bar)
    add_flat_rect(s3, Inches(4.55), opt_y + Inches(0.12), Inches(0.03), Inches(0.65), fill_rgb=C_PINE, no_line=True)

    tb_o2 = s3.shapes.add_textbox(Inches(4.70), opt_y + Inches(0.12), Inches(4.10), Inches(0.65))
    tf_o2 = tb_o2.text_frame
    tf_o2.word_wrap = True
    tf_o2.margin_left = tf_o2.margin_top = 0
    p = tf_o2.paragraphs[0]
    p.text = d3["options"][1]["title"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_PINE
    p.space_after = Pt(2)
    p = tf_o2.add_paragraph()
    p.text = d3["options"][1]["action"]
    p.font.name = FONT_BODY
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_PRIMARY

    # Option 3: Hold for inspection
    tb_o3 = s3.shapes.add_textbox(Inches(9.10), opt_y + Inches(0.12), Inches(3.43), Inches(0.65))
    tf_o3 = tb_o3.text_frame
    tf_o3.word_wrap = True
    tf_o3.margin_left = tf_o3.margin_top = 0
    p = tf_o3.paragraphs[0]
    p.text = d3["options"][2]["title"]
    p.font.name = FONT_HEAD
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY
    p.space_after = Pt(2)
    p = tf_o3.add_paragraph()
    p.text = d3["options"][2]["action"]
    p.font.name = FONT_BODY
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_MUTED

    # Clean Footnote
    tb_disc = s3.shapes.add_textbox(Inches(0.80), Inches(6.36), Inches(11.73), Inches(0.20))
    p = tb_disc.text_frame.paragraphs[0]
    p.text = d3.get("disclaimer", "* Staged example.")
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.color.rgb = C_TEXT_MUTED

    add_page_number(s3, "03")
    add_notes(s3, d3["speaker_notes"])

    # =========================================================
    # SLIDE 4: AGENT ARCHITECTURE & TOOL EXECUTION (PLANNED PROTOTYPE)
    # =========================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    d4 = slides_data[4]

    # Kicker
    tb = s4.shapes.add_textbox(Inches(0.80), Inches(0.75), Inches(8.0), Inches(0.25))
    p = tb.text_frame.paragraphs[0]
    p.text = d4.get("kicker", "Agent Architecture (Planned Prototype)")
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PINE

    # Title & Subtitle
    tb = s4.shapes.add_textbox(Inches(0.80), Inches(1.05), Inches(11.73), Inches(0.75))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = d4.get("title", "Tool-assisted triage and safety guardrails.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY
    p = tf.add_paragraph()
    p.text = d4.get("subtitle", "A structured pipeline where models observe, tools fetch and verify, and the seller approves.")
    p.font.name = FONT_BODY
    p.font.size = Pt(15)
    p.font.color.rgb = C_TEXT_MUTED

    # 4 Steps with Tool Execution
    flow_y = Inches(2.15)
    step_w = Inches(2.65)
    step_gap = Inches(0.36)

    add_flat_rect(s4, Inches(0.80), flow_y, Inches(11.73), Inches(0.015), fill_rgb=C_LINE, no_line=True)

    for i, st in enumerate(d4["steps"]):
        sx = Inches(0.80) + i * (step_w + step_gap)

        if i < 3:
            tb_arr = s4.shapes.add_textbox(sx + step_w + Inches(0.04), flow_y + Inches(0.14), step_gap - Inches(0.08), Inches(0.30))
            p_a = tb_arr.text_frame.paragraphs[0]
            p_a.alignment = PP_ALIGN.CENTER
            p_a.text = "→"
            p_a.font.name = FONT_HEAD
            p_a.font.size = Pt(13)
            p_a.font.bold = True
            p_a.font.color.rgb = C_PINE

        tb_step = s4.shapes.add_textbox(sx, flow_y + Inches(0.15), step_w, Inches(1.65))
        tf_st = tb_step.text_frame
        tf_st.word_wrap = True
        tf_st.margin_left = tf_st.margin_top = 0

        p = tf_st.paragraphs[0]
        p.text = st["step"]
        p.font.name = FONT_HEAD
        p.font.size = Pt(16.5)
        p.font.bold = True
        p.font.color.rgb = C_PINE if i == 3 else C_TEXT_PRIMARY
        p.space_after = Pt(6)

        p = tf_st.add_paragraph()
        p.text = st["desc"]
        p.font.name = FONT_BODY
        p.font.size = Pt(12.5)
        p.font.color.rgb = C_TEXT_SECONDARY

    # Lower Section: Refund Guardrails & Full Audit Log
    gr_y = Inches(4.30)
    add_flat_rect(s4, Inches(0.80), gr_y, Inches(11.73), Inches(0.015), fill_rgb=C_LINE, no_line=True)

    # Kicker for guardrails
    tb_gk = s4.shapes.add_textbox(Inches(0.80), gr_y + Inches(0.15), Inches(8.0), Inches(0.20))
    p = tb_gk.text_frame.paragraphs[0]
    p.text = "PROTOTYPE SAFETY GUARDRAILS & AUDIT LOG"
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_PINE

    # Left: Refund Guardrail
    tb_gr1 = s4.shapes.add_textbox(Inches(0.80), gr_y + Inches(0.40), Inches(5.60), Inches(1.05))
    tf_gr1 = tb_gr1.text_frame
    tf_gr1.word_wrap = True
    tf_gr1.margin_left = tf_gr1.margin_top = 0
    p = tf_gr1.paragraphs[0]
    p.text = "Refund Guardrails"
    p.font.name = FONT_HEAD
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY
    p.space_after = Pt(3)
    p = tf_gr1.add_paragraph()
    p.text = d4["guardrails"]["refund_cap"]
    p.font.name = FONT_BODY
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_SECONDARY

    # Right: Full Audit Log
    tb_gr2 = s4.shapes.add_textbox(Inches(6.80), gr_y + Inches(0.40), Inches(5.73), Inches(1.05))
    tf_gr2 = tb_gr2.text_frame
    tf_gr2.word_wrap = True
    tf_gr2.margin_left = tf_gr2.margin_top = 0
    p = tf_gr2.paragraphs[0]
    p.text = "Full Audit Log"
    p.font.name = FONT_HEAD
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY
    p.space_after = Pt(3)
    p = tf_gr2.add_paragraph()
    p.text = d4["guardrails"]["audit_logging"]
    p.font.name = FONT_BODY
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_SECONDARY

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
    p.text = d5.get("kicker", "Planned scenarios")
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PINE

    # Title
    tb = s5.shapes.add_textbox(Inches(0.80), Inches(1.05), Inches(11.73), Inches(0.60))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = d5.get("title", "Three situations. Clear next steps.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(34)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY

    # Table Layout
    mat_y = Inches(1.95)
    mat_w = Inches(11.73)

    c1_x, c1_w = Inches(0.80), Inches(2.50)
    c2_x, c2_w = Inches(3.50), Inches(3.10)
    c3_x, c3_w = Inches(6.80), Inches(3.20)
    c4_x, c4_w = Inches(10.20), Inches(2.33)

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

    add_flat_rect(s5, Inches(0.80), mat_y + Inches(0.28), mat_w, Inches(0.015), fill_rgb=C_LINE, no_line=True)

    # 3 Data Rows
    row_starts = [mat_y + Inches(0.42), mat_y + Inches(1.82), mat_y + Inches(3.22)]
    row_colors = [C_PINE, C_CORAL, C_TEXT_PRIMARY]

    for idx, row in enumerate(d5["matrix_rows"]):
        ry = row_starts[idx]
        acc_col = row_colors[idx]

        # Col 1: Case ID & Concise Label
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
        p.font.size = Pt(12.5)
        p.font.color.rgb = C_TEXT_MUTED

        # Col 2: Situation (Regular font)
        tb_r2 = s5.shapes.add_textbox(c2_x, ry, c2_w, Inches(1.05))
        tf_r2 = tb_r2.text_frame
        tf_r2.word_wrap = True
        tf_r2.margin_left = tf_r2.margin_top = 0
        p = tf_r2.paragraphs[0]
        p.text = row["situation"]
        p.font.name = FONT_BODY
        p.font.size = Pt(12.5)
        p.font.bold = False
        p.font.color.rgb = C_TEXT_SECONDARY

        # Col 3: Agent Response (Regular font)
        tb_r3 = s5.shapes.add_textbox(c3_x, ry, c3_w, Inches(1.05))
        tf_r3 = tb_r3.text_frame
        tf_r3.word_wrap = True
        tf_r3.margin_left = tf_r3.margin_top = 0
        p = tf_r3.paragraphs[0]
        p.text = row["agent_response"]
        p.font.name = FONT_BODY
        p.font.size = Pt(12.5)
        p.font.bold = False
        p.font.color.rgb = C_TEXT_SECONDARY

        # Col 4: Seller's Next Step (Regular font)
        tb_r4 = s5.shapes.add_textbox(c4_x, ry, c4_w, Inches(1.05))
        tf_r4 = tb_r4.text_frame
        tf_r4.word_wrap = True
        tf_r4.margin_left = tf_r4.margin_top = 0
        p = tf_r4.paragraphs[0]
        p.text = row["seller_outcome"]
        p.font.name = FONT_BODY
        p.font.size = Pt(12.5)
        p.font.bold = False
        p.font.color.rgb = C_TEXT_PRIMARY

        add_flat_rect(s5, Inches(0.80), ry + Inches(1.15), mat_w, Inches(0.015), fill_rgb=C_LINE, no_line=True)

    add_page_number(s5, "05")
    add_notes(s5, d5["speaker_notes"])

    # =========================================================
    # SLIDE 6: 24-HOUR PROTOTYPE SPRINT (4-PERSON TEAM)
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
    tb = s6.shapes.add_textbox(Inches(0.80), Inches(1.05), Inches(11.73), Inches(0.50))
    tf = tb.text_frame
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = d6.get("title", "A focused 24-hour prototype.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(34)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_PRIMARY

    # 1. Timeline: 4 Clean Horizontal Intervals
    time_y = Inches(1.75)
    add_flat_rect(s6, Inches(0.80), time_y, Inches(11.73), Inches(0.015), fill_rgb=C_LINE, no_line=True)

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
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT_SECONDARY

    # 2. Bottom Split: Team (4 Roles Parallel) vs Scope (Build first & Later)
    split_y = Inches(3.45)
    left_w = Inches(5.30)
    right_x = Inches(6.70)
    right_w = Inches(5.83)

    # Left Column: Team (4 Members: A, B, C, D)
    add_flat_rect(s6, Inches(0.80), split_y, left_w, Inches(0.015), fill_rgb=C_LINE, no_line=True)

    tb_team = s6.shapes.add_textbox(Inches(0.80), split_y + Inches(0.12), left_w, Inches(2.15))
    tf_team = tb_team.text_frame
    tf_team.word_wrap = True
    tf_team.margin_left = tf_team.margin_top = 0

    p = tf_team.paragraphs[0]
    p.text = d6.get("team_label", "Team (Parallel Execution to Shared Schema)")
    p.font.name = FONT_HEAD
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PINE
    p.space_after = Pt(6)

    for role_str in d6.get("roles_simple", [
        "A — Tool execution, policy engine and refund caps.",
        "B — Video frame extraction and visual observations.",
        "C — Seller console, drafted replies and audit view.",
        "D — Mock data fixtures, scenario walkthroughs and QA."
    ]):
        p = tf_team.add_paragraph()
        p.text = role_str
        p.font.name = FONT_BODY
        p.font.size = Pt(12)
        p.font.bold = False
        p.font.color.rgb = C_TEXT_PRIMARY
        p.space_after = Pt(4)

    # Right Column: Scope (Build first & Later)
    add_flat_rect(s6, right_x, split_y, right_w, Inches(0.015), fill_rgb=C_LINE, no_line=True)

    tb_scope = s6.shapes.add_textbox(right_x, split_y + Inches(0.12), right_w, Inches(2.15))
    tf_scope = tb_scope.text_frame
    tf_scope.word_wrap = True
    tf_scope.margin_left = tf_scope.margin_top = 0

    p = tf_scope.paragraphs[0]
    p.text = d6.get("build_first_label", "Build first")
    p.font.name = FONT_HEAD
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PINE
    p.space_after = Pt(4)

    p = tf_scope.add_paragraph()
    p.text = d6.get("build_first_items", "Real tool calls on mock data · 3 scenario branches · Refund caps & audit log · Seller approval gate")
    p.font.name = FONT_BODY
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_PRIMARY
    p.space_after = Pt(10)

    p = tf_scope.add_paragraph()
    p.text = d6.get("later_label", "Later")
    p.font.name = FONT_HEAD
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_MUTED
    p.space_after = Pt(4)

    p = tf_scope.add_paragraph()
    p.text = d6.get("later_items", "Live store and courier integrations.")
    p.font.name = FONT_BODY
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_MUTED

    # 3. Closing Takeaway directly on canvas
    take_y = Inches(5.85)
    tb_tk = s6.shapes.add_textbox(Inches(0.80), take_y, Inches(11.73), Inches(0.50))
    tf_tk = tb_tk.text_frame
    tf_tk.word_wrap = True
    p = tf_tk.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = d6.get("closing_takeaway", "One clear evidence pack. The seller makes the call.")
    p.font.name = FONT_HEAD
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = C_PINE

    add_page_number(s6, "06")
    add_notes(s6, d6["speaker_notes"])

    # =========================================================
    # GLOBAL NEUTRALIZATION PASS: GUARANTEE ZERO THEME LEAKAGE
    # =========================================================
    for slide in prs.slides:
        for sh in slide.shapes:
            sp = sh._element
            st = sp.find('{http://schemas.openxmlformats.org/presentationml/2006/main}style')
            if st is not None:
                sp.remove(st)
            if hasattr(sp, 'spPr'):
                eff = sp.spPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
                if eff is None:
                    sp.spPr.append(parse_xml('<a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'))
                else:
                    for child in list(eff):
                        eff.remove(child)

    # =========================================================
    # REPRODUCIBLE DETERMINISTIC PACKAGING (ZIP_STORED)
    # =========================================================
    raw_pptx = deliverables_dir / "temp_raw_v9_3.pptx"
    prs.save(str(raw_pptx))

    final_deliv_pptx = deliverables_dir / "ReturnLens_v9_3.pptx"
    root_pptx = base_dir / "ReturnLens_v9_3.pptx"

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
    print(f"Generated ReturnLens_v9_3.pptx successfully: {final_deliv_pptx} ({final_deliv_pptx.stat().st_size} bytes)")

if __name__ == "__main__":
    build_v9_3_pptx()
