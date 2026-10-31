import os
import shutil
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]

    # Color Palette: ReturnLens Warm Editorial Swiss
    C_CREAM = RGBColor(0xF5, 0xF3, 0xEF)
    C_DARK = RGBColor(0x17, 0x26, 0x21)
    C_TEAL = RGBColor(0x00, 0x6B, 0x55)
    C_TEAL_LIGHT = RGBColor(0xE1, 0xF2, 0xEC)
    C_CORAL = RGBColor(0xD9, 0x5D, 0x39)
    C_CORAL_LIGHT = RGBColor(0xFC, 0xEC, 0xE8)
    C_AMBER = RGBColor(0xD9, 0x77, 0x06)
    C_AMBER_LIGHT = RGBColor(0xFE, 0xF3, 0xC7)
    C_BORDER_LIGHT = RGBColor(0xE2, 0xDE, 0xD4)
    C_MUTED = RGBColor(0x59, 0x6E, 0x64)
    C_SUBTLE = RGBColor(0x7A, 0x8E, 0x85)
    C_DARK_BG = RGBColor(0x0F, 0x1A, 0x16)
    C_BORDER_DARK = RGBColor(0x22, 0x38, 0x30)
    C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)

    FONT_HEAD = "Inter"
    FONT_MONO = "IBM Plex Mono"

    base_dir = Path(__file__).resolve().parent.parent
    assets_dir = base_dir / "src" / "assets"

    def set_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_footer(slide, left_text, right_text, is_dark=False):
        y = Inches(6.85)
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y, Inches(11.733), Inches(0.015))
        line.fill.solid()
        line.fill.fore_color.rgb = C_BORDER_DARK if is_dark else C_BORDER_LIGHT
        line.line.fill.background()

        tb_left = slide.shapes.add_textbox(Inches(0.8), y + Inches(0.08), Inches(9.0), Inches(0.4))
        p = tb_left.text_frame.paragraphs[0]
        p.text = left_text
        p.font.name = FONT_MONO
        p.font.size = Pt(10)
        p.font.color.rgb = RGBColor(0x5C, 0x78, 0x6E) if is_dark else C_SUBTLE

        tb_right = slide.shapes.add_textbox(Inches(10.0), y + Inches(0.08), Inches(2.533), Inches(0.4))
        p = tb_right.text_frame.paragraphs[0]
        p.text = right_text
        p.font.name = FONT_MONO
        p.font.size = Pt(10)
        p.font.color.rgb = RGBColor(0x5C, 0x78, 0x6E) if is_dark else C_SUBTLE
        p.alignment = PP_ALIGN.RIGHT

    def set_speaker_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text.strip()

    # =========================================================================
    # SLIDE 1: PRODUCT LAUNCH & EXECUTIVE SUMMARY
    # =========================================================================
    s1 = prs.slides.add_slide(blank_slide_layout)
    set_bg(s1, C_CREAM)

    tb = s1.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(6.2), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "RETURNLENS · PRODUCT LAUNCH"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    tb = s1.shapes.add_textbox(Inches(0.8), Inches(1.05), Inches(6.2), Inches(1.1))
    p = tb.text_frame.paragraphs[0]
    p.text = "RETURNLENS"
    p.font.name = FONT_HEAD
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    tb = s1.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(6.2), Inches(0.8))
    p = tb.text_frame.paragraphs[0]
    p.text = "Every return decision, backed by evidence."
    p.font.name = FONT_HEAD
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    tb = s1.shapes.add_textbox(Inches(0.8), Inches(3.1), Inches(6.2), Inches(1.2))
    p = tb.text_frame.paragraphs[0]
    p.text = "Solo online sellers lose 15–20 minutes per return deciding from memory across disconnected tabs.\n\nReturnLens indexes unboxing video keyframes, matches store orders, applies deterministic policy rules, and presents a 1-click decision console to the merchant."
    p.font.name = FONT_HEAD
    p.font.size = Pt(12)
    p.font.color.rgb = C_MUTED

    badge_meta = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.5), Inches(6.2), Inches(0.65))
    badge_meta.fill.solid()
    badge_meta.fill.fore_color.rgb = C_WHITE
    badge_meta.line.color.rgb = C_BORDER_LIGHT
    badge_meta.line.width = Pt(1)
    tf = badge_meta.text_frame
    p = tf.paragraphs[0]
    p.text = "AgentX Hackathon 2026 · PS-04 Track · Team Rookie (3 Members)"
    p.font.name = FONT_MONO
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p2 = tf.add_paragraph()
    p2.text = "Thesis: Models observe. Code verifies. Seller authorizes."
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(10)
    p2.font.color.rgb = C_DARK

    # Metrics row
    m_box1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.3), Inches(1.9), Inches(1.25))
    m_box1.fill.solid()
    m_box1.fill.fore_color.rgb = C_WHITE
    m_box1.line.color.rgb = C_BORDER_LIGHT
    m_box1.line.width = Pt(1)
    tf = m_box1.text_frame
    p = tf.paragraphs[0]
    p.text = "15–20m"
    p.font.name = FONT_HEAD
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = C_CORAL
    p2 = tf.add_paragraph()
    p2.text = "Current manual triage time per return ticket"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(9)
    p2.font.color.rgb = C_MUTED

    m_box2 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(2.95), Inches(5.3), Inches(1.9), Inches(1.25))
    m_box2.fill.solid()
    m_box2.fill.fore_color.rgb = C_WHITE
    m_box2.line.color.rgb = C_BORDER_LIGHT
    m_box2.line.width = Pt(1)
    tf = m_box2.text_frame
    p = tf.paragraphs[0]
    p.text = "1-Click"
    p.font.name = FONT_HEAD
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p2 = tf.add_paragraph()
    p2.text = "Merchant decision with cited keyframe evidence"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(9)
    p2.font.color.rgb = C_MUTED

    m_box3 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.1), Inches(5.3), Inches(1.9), Inches(1.25))
    m_box3.fill.solid()
    m_box3.fill.fore_color.rgb = C_WHITE
    m_box3.line.color.rgb = C_BORDER_LIGHT
    m_box3.line.width = Pt(1)
    tf = m_box3.text_frame
    p = tf.paragraphs[0]
    p.text = "24h"
    p.font.name = FONT_HEAD
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p2 = tf.add_paragraph()
    p2.text = "Prototype feasibility for 3-member team"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(9)
    p2.font.color.rgb = C_MUTED

    # Right Console Mockup
    c_left = Inches(7.4)
    c_top = Inches(0.85)
    c_w = Inches(5.133)
    c_h = Inches(5.7)

    console_bg = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, c_top, c_w, c_h)
    console_bg.fill.solid()
    console_bg.fill.fore_color.rgb = C_WHITE
    console_bg.line.color.rgb = C_BORDER_LIGHT
    console_bg.line.width = Pt(1)

    c_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, c_top, c_w, Inches(0.55))
    c_bar.fill.solid()
    c_bar.fill.fore_color.rgb = RGBColor(0x1F, 0x30, 0x2A)
    c_bar.line.fill.background()
    tf = c_bar.text_frame
    p = tf.paragraphs[0]
    p.text = "RETURNLENS SELLER CONSOLE  ·  CASE #RT-1042"
    p.font.name = FONT_MONO
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x00, 0xD1, 0xA7)

    # Console Body
    hero_img_path = assets_dir / "studio_white_headphones.png"
    if hero_img_path.exists():
        s1.shapes.add_picture(str(hero_img_path), c_left + Inches(0.2), c_top + Inches(0.7), Inches(2.2), Inches(2.2))

    p_left = c_left + Inches(2.55)
    p_w = c_w - Inches(2.75)
    tb_c_info = s1.shapes.add_textbox(p_left, c_top + Inches(0.7), p_w, Inches(4.3))
    tf = tb_c_info.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "ORDER INFORMATION"
    p.font.name = FONT_MONO
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = C_SUBTLE

    p2 = tf.add_paragraph()
    p2.text = "Order #ORD-8821\nSKU: HEAD-WHT-02 (White)\nPrice: ₹4,999 · Delivered 4d ago"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(10.5)
    p2.font.bold = True
    p2.font.color.rgb = C_DARK

    p3 = tf.add_paragraph()
    p3.text = "\nVIDEO EVIDENCE CITATION"
    p3.font.name = FONT_MONO
    p3.font.size = Pt(9)
    p3.font.bold = True
    p3.font.color.rgb = C_SUBTLE

    p4 = tf.add_paragraph()
    p4.text = "Inspection Frame 00:14"
    p4.font.name = FONT_HEAD
    p4.font.size = Pt(11)
    p4.font.bold = True
    p4.font.color.rgb = C_DARK

    p5 = tf.add_paragraph()
    p5.text = "Potential casing damage flagged · Requires manual confirmation"
    p5.font.name = FONT_HEAD
    p5.font.size = Pt(9.5)
    p5.font.color.rgb = C_MUTED

    p6 = tf.add_paragraph()
    p6.text = "\nPOLICY VERIFICATION"
    p6.font.name = FONT_MONO
    p6.font.size = Pt(9)
    p6.font.bold = True
    p6.font.color.rgb = C_SUBTLE

    p7 = tf.add_paragraph()
    p7.text = "P-01 Defect Check: FLAGGED FOR REVIEW\nP-04 Return Window: PASS (Day 4 of 7)"
    p7.font.name = FONT_HEAD
    p7.font.size = Pt(10)
    p7.font.bold = True
    p7.font.color.rgb = RGBColor(0x92, 0x40, 0x0E)

    # Console Badge & Button
    badge = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left + Inches(0.2), c_top + Inches(4.3), c_w - Inches(0.4), Inches(0.4))
    badge.fill.solid()
    badge.fill.fore_color.rgb = C_AMBER_LIGHT
    badge.line.fill.background()
    p = badge.text_frame.paragraphs[0]
    p.text = "STATUS: READY FOR SELLER REVIEW (FLAGGED)"
    p.font.name = FONT_MONO
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x92, 0x40, 0x0E)
    p.alignment = PP_ALIGN.CENTER

    btn = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left + Inches(0.2), c_top + Inches(4.85), c_w - Inches(0.4), Inches(0.55))
    btn.fill.solid()
    btn.fill.fore_color.rgb = C_TEAL
    btn.line.fill.background()
    p = btn.text_frame.paragraphs[0]
    p.text = "Review Evidence & Authorize Draft"
    p.font.name = FONT_HEAD
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.alignment = PP_ALIGN.CENTER

    add_footer(s1, "ReturnLens · Idea Pitch Deck · PS-04 · Team Rookie (3 members)", "Slide 1 / 6")

    set_speaker_notes(s1, """
Slide 1 — Product Hero & Executive Summary:
- Track & Fit: AgentX Hackathon 2026, Track PS-04 (Autonomous Support Agent for Online Sellers), Team Rookie (3 members).
- Target Merchant: Solo direct-to-consumer (D2C) e-commerce sellers managing orders, shipping, and returns without dedicated support staff.
- Core Friction: Solo sellers spend 15–20 minutes per return opening fragmented tabs (buyer chat, Shopify, Shippo tracking, store return policy). Return decisions are currently made from memory without unified evidence.
- Our Thesis: "Models observe. Code verifies. Seller authorizes."
- Technical Honesty: In the console mockup, observe the conservative metadata: "Potential casing damage flagged · Requires manual confirmation" rather than an ungrounded claim of incontrovertible defect.
- Fail-Closed Safety: The system never autonomously transfers money. Return labels and refund drafts remain strictly in pending status until the human merchant reviews evidence and clicks authorization.
- 24-Hour Hackathon Scope: Focused exclusively on return triage plus one zero-vision order status fast path (reusing store and courier APIs).
""")

    # =========================================================================
    # SLIDE 2: THE PROBLEM (3-COLUMN ZERO-OVERLAP LAYOUT)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_slide_layout)
    set_bg(s2, C_CREAM)

    tb = s2.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(6.0), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "THE PROBLEM · SOLO SELLER BOTTLENECK"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    tb = s2.shapes.add_textbox(Inches(0.8), Inches(1.05), Inches(11.7), Inches(0.8))
    p = tb.text_frame.paragraphs[0]
    p.text = "One return decision. Four disconnected sources."
    p.font.name = FONT_HEAD
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    tb = s2.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(11.7), Inches(0.6))
    p = tb.text_frame.paragraphs[0]
    p.text = "Sellers decide returns from memory today. ReturnLens assembles one trace before money moves."
    p.font.name = FONT_HEAD
    p.font.size = Pt(19)
    p.font.color.rgb = C_MUTED

    col_w = Inches(3.6)
    gap_w = Inches(4.133)
    card_h = Inches(1.9)

    # Left Column: Today's Friction (Sources 01 & 03)
    c1 = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(2.6), col_w, card_h)
    c1.fill.solid()
    c1.fill.fore_color.rgb = C_WHITE
    c1.line.color.rgb = C_BORDER_LIGHT
    tf = c1.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "01 BUYER VIDEO & CLAIM"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p2 = tf.add_paragraph()
    p2.text = "Unverified Customer Claims"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(13)
    p2.font.bold = True
    p2.font.color.rgb = C_DARK
    p3 = tf.add_paragraph()
    p3.text = "Subjective descriptions in chat; videos are unindexed and skipped"
    p3.font.name = FONT_HEAD
    p3.font.size = Pt(10)
    p3.font.color.rgb = C_MUTED

    c3 = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.7), col_w, card_h)
    c3.fill.solid()
    c3.fill.fore_color.rgb = C_WHITE
    c3.line.color.rgb = C_BORDER_LIGHT
    tf = c3.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "03 COURIER TRACKING"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p2 = tf.add_paragraph()
    p2.text = "Delivered 4 Days Ago"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(13)
    p2.font.bold = True
    p2.font.color.rgb = C_DARK
    p3 = tf.add_paragraph()
    p3.text = "Shippo mock tracking API scan timestamp verification"
    p3.font.name = FONT_HEAD
    p3.font.size = Pt(10)
    p3.font.color.rgb = C_MUTED

    # Center Gap Card: Forceful Editorial Anchor (NO OVERLAP)
    c_gap = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.6), Inches(2.6), gap_w, Inches(4.0))
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
    p2.text = "Four systems. No traceable decision."
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = C_CREAM
    p2.alignment = PP_ALIGN.CENTER

    p3 = tf.add_paragraph()
    p3.text = "NO SHARED EVIDENCE RECORD"
    p3.font.name = FONT_MONO
    p3.font.size = Pt(11)
    p3.font.bold = True
    p3.font.color.rgb = RGBColor(0x00, 0xD1, 0xA7)
    p3.alignment = PP_ALIGN.CENTER

    p4 = tf.add_paragraph()
    p4.text = "\nToday the seller opens 4 tabs, then decides alone. A wrong refund loses inventory; an unfair denial loses a repeat customer.\n\nThe gap is not a missing returns portal, but the absence of a unified record connecting order, video frames, courier scans, and policy terms."
    p4.font.name = FONT_HEAD
    p4.font.size = Pt(10)
    p4.font.color.rgb = RGBColor(0xD1, 0xD5, 0xDB)
    p4.alignment = PP_ALIGN.CENTER

    p5 = tf.add_paragraph()
    p5.text = "\n9.0% vs 15.14%"
    p5.font.name = FONT_HEAD
    p5.font.size = Pt(14)
    p5.font.bold = True
    p5.font.color.rgb = C_CORAL
    p5.alignment = PP_ALIGN.CENTER

    p6 = tf.add_paragraph()
    p6.text = "9% Return Fraud (NRF 2025, fraud only)  |  15.14% (Appriss/Deloitte 2024, fraud + abuse)\nDefinitions differ: strict fraud vs fraud combined with policy abuse."
    p6.font.name = FONT_HEAD
    p6.font.size = Pt(8.5)
    p6.font.color.rgb = RGBColor(0x9C, 0xA3, 0xAF)
    p6.alignment = PP_ALIGN.CENTER

    # Right Column: Order Truth & Policy (Sources 02 & 04)
    c2 = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.933), Inches(2.6), col_w, card_h)
    c2.fill.solid()
    c2.fill.fore_color.rgb = C_WHITE
    c2.line.color.rgb = C_BORDER_LIGHT
    tf = c2.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "02 ORDER RECORD"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p2 = tf.add_paragraph()
    p2.text = "White Headphones · ₹4,999"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(13)
    p2.font.bold = True
    p2.font.color.rgb = C_DARK
    p3 = tf.add_paragraph()
    p3.text = "Shopify mock store API product inventory catalog"
    p3.font.name = FONT_HEAD
    p3.font.size = Pt(10)
    p3.font.color.rgb = C_MUTED

    c4 = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.933), Inches(4.7), col_w, card_h)
    c4.fill.solid()
    c4.fill.fore_color.rgb = C_WHITE
    c4.line.color.rgb = C_BORDER_LIGHT
    tf = c4.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "04 RETURN POLICY"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p2 = tf.add_paragraph()
    p2.text = "7-Day Window · Sealed Tag"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(13)
    p2.font.bold = True
    p2.font.color.rgb = C_DARK
    p3 = tf.add_paragraph()
    p3.text = "Deterministic code rules P-01 to P-08, never prompts"
    p3.font.name = FONT_HEAD
    p3.font.size = Pt(10)
    p3.font.color.rgb = C_MUTED

    add_footer(s2, "Fraud estimates differ by definition: 9% (NRF 2025, fraud only) vs 15.14% (Appriss/Deloitte 2024, fraud + abuse).", "Slide 2 / 6")

    set_speaker_notes(s2, """
Slide 2 — Problem Space & The Four Disconnected Sources:
- Problem: The return decision bottleneck is not an absent return policy; it is fragmented, unverified context.
- Sources:
  1. Customer Claim in chat (unverified claims, emotional text).
  2. Order Truth in Shopify store (SKU HEAD-WHT-02, price ₹4,999).
  3. Tracking Scan in Shippo courier API (delivered 4 days ago).
  4. Store Return Policy document (7-day defect window, security tag required).
- Central Gap: "Four systems. No traceable decision." Sellers decide returns from memory today. No single record ties video frames, store orders, and shipping status into an immutable decision trace.
- Fraud Metrics Defense: Strict fraud is 9% (NRF 2025, fraud only), while fraud + abuse is 15.14% (Appriss/Deloitte 2024). They represent fundamentally different measurement scopes and must never be merged.
- Asymmetric Merchant Risk: Wrong refund loses inventory and gross margin; unfair denial destroys customer lifetime value (LTV).
""")

    # =========================================================================
    # SLIDE 3: STAR DEMO SLIDE (VISUAL EVIDENCE BENCHMARK)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_slide_layout)
    set_bg(s3, C_CREAM)

    tb = s3.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(8.0), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "STAR DEMO · VISUAL GROUNDING & COLOR CONTRADICTION"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    tb = s3.shapes.add_textbox(Inches(0.8), Inches(0.95), Inches(11.7), Inches(0.8))
    p = tb.text_frame.paragraphs[0]
    p.text = "The order says white. The video shows black."
    p.font.name = FONT_HEAD
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    tb = s3.shapes.add_textbox(Inches(0.8), Inches(1.75), Inches(11.7), Inches(0.5))
    p = tb.text_frame.paragraphs[0]
    p.text = "ReturnLens extracts keyframes, flags color discrepancies, and halts auto-payout for seller approval."
    p.font.name = FONT_HEAD
    p.font.size = Pt(19)
    p.font.color.rgb = C_MUTED

    # Left: Evidence Image Comparison (White Ordered vs Black Observed)
    panel_left = Inches(0.8)
    panel_top = Inches(2.35)
    panel_w = Inches(7.4)
    panel_h = Inches(4.35)

    ev_bg = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, panel_left, panel_top, panel_w, panel_h)
    ev_bg.fill.solid()
    ev_bg.fill.fore_color.rgb = C_WHITE
    ev_bg.line.color.rgb = C_BORDER_LIGHT
    ev_bg.line.width = Pt(1)

    # Images
    img_w = Inches(3.4)
    img_h = Inches(2.8)

    w_img_path = assets_dir / "studio_white_headphones.png"
    if w_img_path.exists():
        s3.shapes.add_picture(str(w_img_path), panel_left + Inches(0.2), panel_top + Inches(0.2), img_w, img_h)

    b_img_path = assets_dir / "unboxing_black_headphones.png"
    if b_img_path.exists():
        s3.shapes.add_picture(str(b_img_path), panel_left + Inches(3.8), panel_top + Inches(0.2), img_w, img_h)

    # Badges below images
    b_order = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, panel_left + Inches(0.2), panel_top + Inches(3.1), img_w, Inches(0.35))
    b_order.fill.solid()
    b_order.fill.fore_color.rgb = C_TEAL_LIGHT
    b_order.line.fill.background()
    p = b_order.text_frame.paragraphs[0]
    p.text = "ORDER MANIFEST: WHITE HEADPHONES"
    p.font.name = FONT_MONO
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p.alignment = PP_ALIGN.CENTER

    b_obs = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, panel_left + Inches(3.8), panel_top + Inches(3.1), img_w, Inches(0.35))
    b_obs.fill.solid()
    b_obs.fill.fore_color.rgb = C_CORAL_LIGHT
    b_obs.line.fill.background()
    p = b_obs.text_frame.paragraphs[0]
    p.text = "UNBOXING KEYFRAME 00:07: BLACK ITEM"
    p.font.name = FONT_MONO
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_CORAL
    p.alignment = PP_ALIGN.CENTER

    # Caption / Footnote on Grounding
    tb_foot = s3.shapes.add_textbox(panel_left + Inches(0.2), panel_top + Inches(3.55), panel_w - Inches(0.4), Inches(0.7))
    tf = tb_foot.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Visual Grounding Honesty: Keyframe resolution reveals black casing. Exact SKU barcode is unreadable in this frame; ReturnLens factually records 'Observed Color: Black · Exact SKU: Not verified' and cites frame 00:07."
    p.font.name = FONT_HEAD
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_MUTED

    # Right: Deterministic Policy Gate & Seller Decision Console
    con_left = Inches(8.45)
    con_top = Inches(2.35)
    con_w = Inches(4.083)
    con_h = Inches(4.35)

    con_bg = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, con_left, con_top, con_w, con_h)
    con_bg.fill.solid()
    con_bg.fill.fore_color.rgb = C_WHITE
    con_bg.line.color.rgb = C_BORDER_LIGHT
    con_bg.line.width = Pt(1)

    tb = s3.shapes.add_textbox(con_left + Inches(0.2), con_top + Inches(0.15), con_w - Inches(0.4), Inches(4.1))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "DETERMINISTIC POLICY GATE"
    p.font.name = FONT_MONO
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_CORAL

    p2 = tf.add_paragraph()
    p2.text = "P-03 Check: COLOR CONTRADICTION"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(0x99, 0x1B, 0x1B)

    p3 = tf.add_paragraph()
    p3.text = "STATUS: ESCALATE (SELLER REVIEW REQUIRED)\nObserved Color: Midnight Black · Exact SKU: Not verified"
    p3.font.name = FONT_MONO
    p3.font.size = Pt(8.5)
    p3.font.bold = True
    p3.font.color.rgb = RGBColor(0x99, 0x1B, 0x1B)

    p4 = tf.add_paragraph()
    p4.text = "Customer claim contradicts visual evidence. Automated return label and refund payout are inhibited."
    p4.font.name = FONT_HEAD
    p4.font.size = Pt(9.5)
    p4.font.color.rgb = C_MUTED

    p5 = tf.add_paragraph()
    p5.text = "\nSeller Resolution Options:\n1. Request unboxing video with packaging label / serial visible\n2. Reject return under Clause 4.2 (Item does not match order)\n3. Override & approve if seller acknowledges warehouse error"
    p5.font.name = FONT_HEAD
    p5.font.size = Pt(9)
    p5.font.color.rgb = C_DARK

    p6 = tf.add_paragraph()
    p6.text = "\nFinancial Safety Ceiling:\nmax_refund = min(₹4,999, remaining refundable, order paid amount)\nNo automatic customer denial · No refund released without seller click"
    p6.font.name = FONT_MONO
    p6.font.size = Pt(8.5)
    p6.font.color.rgb = C_MUTED

    add_footer(s3, "Illustrative staged evidence · Mock Shopify & Shippo APIs", "Slide 3 / 6")

    set_speaker_notes(s3, """
Slide 3 — The Star Demo & Technical Honesty in Vision Citation:
- Core Benchmark Scenario (Case B): Buyer ordered white headphones (HEAD-WHT-02, ₹4,999), but unboxing frame 00:07 shows black headphones.
- Grounding & Honesty: The agent does NOT claim to read an unreadable SKU barcode from frame 00:07. It states factually: "Observed Color: Midnight Black · Exact SKU: Not verified · Tag: Not visible in cited frame".
- Decision Logic: Seeing a black item when white was ordered is an undeniable visual contradiction against the manifest. Instead of auto-denying the customer (which might alienate an honest buyer if the warehouse mis-shipped), the policy engine triggers ESCALATE.
- Three Merchant Decision Options:
  1. Request unboxing video with packaging label / serial number visible.
  2. Reject return under Clause 4.2 (Item does not match order record).
  3. Override & approve if seller acknowledges known warehouse fulfillment error.
- Fail-Closed Financial Gate:
  max_refund = min(₹4,999, remaining refundable amount, order paid amount).
  No refund money is released without explicit seller click.
""")

    # =========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE (DARK + AGENTIC GOVERNANCE)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_slide_layout)
    set_bg(s4, C_DARK_BG)

    tb = s4.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(8.0), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "SYSTEM ARCHITECTURE · DYNAMIC AGENTIC GOVERNANCE"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x00, 0xD1, 0xA7)

    tb = s4.shapes.add_textbox(Inches(0.8), Inches(0.9), Inches(11.7), Inches(0.7))
    p = tb.text_frame.paragraphs[0]
    p.text = "Models observe. Code verifies. Seller authorizes."
    p.font.name = FONT_HEAD
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_CREAM

    tb = s4.shapes.add_textbox(Inches(0.8), Inches(1.55), Inches(11.7), Inches(0.45))
    p = tb.text_frame.paragraphs[0]
    p.text = "Dynamic action selection and stateful resumption under deterministic human authorization."
    p.font.name = FONT_HEAD
    p.font.size = Pt(18)
    p.font.color.rgb = RGBColor(0xA3, 0xB8, 0xB0)

    # 6-Step Horizontal Pipeline with Arrows
    pipe_steps = [
        ("01 PLAN", "Planner", "MODEL", RGBColor(0x00, 0x38, 0x2B), RGBColor(0x00, 0xD1, 0xA7)),
        ("02 RETRIEVE", "Tools & Video", "CODE", RGBColor(0x26, 0x38, 0x31), C_CREAM),
        ("03 EVALUATE", "Policy Engine", "CODE", RGBColor(0x26, 0x38, 0x31), C_CREAM),
        ("04 AUDIT", "Critic", "MODEL", RGBColor(0x00, 0x38, 0x2B), RGBColor(0x00, 0xD1, 0xA7)),
        ("05 AUTHORIZE", "Seller Gate", "HUMAN", RGBColor(0x45, 0x26, 0x0A), RGBColor(0xFB, 0xBF, 0x24)),
        ("06 RECORD", "Audit Log", "CODE", RGBColor(0x26, 0x38, 0x31), C_CREAM)
    ]

    p_w = Inches(1.75)
    p_gap = Inches(0.24)
    p_top = Inches(2.05)
    p_h = Inches(1.15)

    for i, (num, title, tag, tag_bg, tag_fg) in enumerate(pipe_steps):
        px = Inches(0.8) + i * (p_w + p_gap)
        box = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, px, p_top, p_w, p_h)
        box.fill.solid()
        box.fill.fore_color.rgb = RGBColor(0x17, 0x26, 0x21)
        box.line.color.rgb = C_BORDER_DARK
        box.line.width = Pt(1)

        top_bar = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, px, p_top, p_w, Inches(0.04))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = tag_fg
        top_bar.line.fill.background()

        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = num
        p.font.name = FONT_MONO
        p.font.size = Pt(8.5)
        p.font.color.rgb = RGBColor(0x6C, 0x82, 0x79)

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.name = FONT_HEAD
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = C_CREAM

        tb_tag = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, px + Inches(0.1), p_top + Inches(0.78), p_w - Inches(0.2), Inches(0.26))
        tb_tag.fill.solid()
        tb_tag.fill.fore_color.rgb = tag_bg
        tb_tag.line.fill.background()
        p = tb_tag.text_frame.paragraphs[0]
        p.text = tag
        p.font.name = FONT_MONO
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = tag_fg
        p.alignment = PP_ALIGN.CENTER

        if i < len(pipe_steps) - 1:
            arr_box = s4.shapes.add_textbox(px + p_w, p_top + Inches(0.35), p_gap, Inches(0.4))
            p_arr = arr_box.text_frame.paragraphs[0]
            p_arr.text = "→"
            p_arr.font.name = FONT_MONO
            p_arr.font.size = Pt(14)
            p_arr.font.bold = True
            p_arr.font.color.rgb = RGBColor(0x00, 0xD1, 0xA7)
            p_arr.alignment = PP_ALIGN.CENTER

    # Dual Operational Branches (Agentic Loop vs Order Status Fast Path)
    path_top = Inches(3.35)
    path_h = Inches(0.85)

    # Path 1: Case C Stateful Clarification Loop
    p1_box = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), path_top, Inches(6.5), path_h)
    p1_box.fill.solid()
    p1_box.fill.fore_color.rgb = RGBColor(0x14, 0x22, 0x1D)
    p1_box.line.color.rgb = RGBColor(0x25, 0x63, 0xEB)
    p1_box.line.width = Pt(1)
    tf = p1_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "DYNAMIC STATEFUL CLARIFICATION LOOP (CASE C) · Observe → Decide → Act → Wait → Resume"
    p.font.name = FONT_MONO
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)
    p2 = tf.add_paragraph()
    p2.text = "Dark Frames → ask_for_evidence() → WAITING_FOR_EVIDENCE → Customer Uploads → Resume Case"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(9.5)
    p2.font.bold = True
    p2.font.color.rgb = C_CREAM

    # Path 2: Order Status Fast Path
    p2_box = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.45), path_top, Inches(5.083), path_h)
    p2_box.fill.solid()
    p2_box.fill.fore_color.rgb = RGBColor(0x14, 0x22, 0x1D)
    p2_box.line.color.rgb = RGBColor(0x05, 0x96, 0x69)
    p2_box.line.width = Pt(1)
    tf = p2_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "ORDER STATUS FAST PATH (PS-04 FIT) · Zero-Vision Direct Route"
    p.font.name = FONT_MONO
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x34, 0xD3, 0x99)
    p2 = tf.add_paragraph()
    p2.text = "“Where is my order?” → Query Store & Shippo APIs → Delivery Scan & Time"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(9.5)
    p2.font.bold = True
    p2.font.color.rgb = C_CREAM

    # 4 Decision Branches
    branches = [
        ("1. CONTRADICTION → ESCALATE", RGBColor(0xF8, 0x71, 0x71), "Discrepancy flagged (e.g. Case B). Inhibits automated label/refund. Seller reviews 3 options."),
        ("2. HARD FAIL → ESCALATE", RGBColor(0xFB, 0xBF, 0x24), "Mandatory rule violation (e.g. expired return window). Seller makes final decision; never auto-deny."),
        ("3. UNCLEAR ONLY → ASK MORE", RGBColor(0x60, 0xA5, 0xFA), "Low brightness or blurry barcode (e.g. Case C). Prompts exact re-film checklist (1 retry limit)."),
        ("4. ALL PASS → APPROVE REVIEW", RGBColor(0x34, 0xD3, 0x99), "All clauses pass (e.g. Case A). Prepares mock label and drafts refund in pending_return_receipt.")
    ]

    b_w = Inches(2.8)
    b_gap = Inches(0.17)
    b_top = Inches(4.35)
    b_h = Inches(1.15)

    for i, (b_title, b_col, b_desc) in enumerate(branches):
        bx = Inches(0.8) + i * (b_w + b_gap)
        box = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, bx, b_top, b_w, b_h)
        box.fill.solid()
        box.fill.fore_color.rgb = RGBColor(0x12, 0x1F, 0x1B)
        box.line.color.rgb = C_BORDER_DARK
        box.line.width = Pt(1)

        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = b_title
        p.font.name = FONT_MONO
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = b_col

        p2 = tf.add_paragraph()
        p2.text = b_desc
        p2.font.name = FONT_HEAD
        p2.font.size = Pt(9)
        p2.font.color.rgb = RGBColor(0xA3, 0xB8, 0xB0)

    # Architecture Guarantees & Critic Bar
    leg = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.65), Inches(11.733), Inches(0.95))
    leg.fill.solid()
    leg.fill.fore_color.rgb = RGBColor(0x12, 0x1F, 0x1B)
    leg.line.color.rgb = C_BORDER_DARK
    leg.line.width = Pt(1)

    tf = leg.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "■ Model Calls: Bounded design estimate (3 base calls: planner, vision, critic + retries)  |  ■ Policy Rules: Deterministic Python code rules P-01 to P-08, never prompts"
    p.font.name = FONT_MONO
    p.font.size = Pt(8.5)
    p.font.color.rgb = RGBColor(0xA3, 0xB8, 0xB0)

    p2 = tf.add_paragraph()
    p2.text = "■ Critic Duty: Reviews cited frames, flags unsupported observations (correlated error limits noted)  |  ■ Safety Boundary: Backend authorization check — LLMs cannot execute financial refunds"
    p2.font.name = FONT_MONO
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = RGBColor(0xA3, 0xB8, 0xB0)

    add_footer(s4, "Structured audit log recorded at every state transition · Decision priority: Contradiction > Hard fail > Unclear only > All pass", "Slide 4 / 6", is_dark=True)

    set_speaker_notes(s4, """
Slide 4 — System Architecture, Agentic Governance & Technical Q&A Defense:
- Philosophy: "Models observe. Code verifies. Seller authorizes."

- DEFENSE QUESTION 1: Why is this an agent rather than a hardcoded workflow?
  ReturnLens is an autonomous state machine with dynamic action selection, multi-modal observation, and stateful lifecycle management.
  In Case C, when a customer submits a dark/blurry video (average brightness 28), the agent does NOT simply fail or run a static linear chain. It inspects the frames, determines evidence is insufficient under Policy P-05, dynamically decides to invoke ask_for_evidence() with specific re-filming guidance, transitions the ticket to WAITING_FOR_EVIDENCE, pauses execution while retaining state and order context, and resumes the exact triage session when new media arrives.
  Conversely, for routine "Where is my order?" requests, the agent selects the zero-vision fast path, querying mock Shopify and Shippo APIs directly without invoking heavy vision models.

- DEFENSE QUESTION 2: What happens if vision or critic models hallucinate?
  Vision models produce non-binding observation metadata, never authoritative decisions. Hard business rules (return windows from carrier delivery timestamps, SKU comparisons) are executed in deterministic Python code (P-01 to P-08), which cannot be jailbroken by customer prompts.
  The critic provides an adversarial sanity check against cited timestamps. If both vision and critic experience correlated hallucinations, the fail-closed human seller gate guarantees that no refund or return label can ever be issued without seller review.

- DEFENSE QUESTION 3: How do you prevent duplicate or incorrect refunds?
  Refund transactions are enforced at the backend policy layer:
  1. Idempotency keys (hash(order_id, return_id, transaction_type)) prevent double-execution.
  2. Ledgers track cumulative refunded amounts against total order value: 0 < amount <= min(₹4,999, remaining_refundable_amount, order_paid_amount).
  3. LLMs possess zero capability to call payment gateways directly; all actions produce draft state objects awaiting merchant authorization.

- Bounded Execution: Exactly 3 base model calls per triage case (Planner, Vision, Critic) plus retries.
""")

    # =========================================================================
    # SLIDE 5: FOUR DEMO BENCHMARK SCENARIOS
    # =========================================================================
    s5 = prs.slides.add_slide(blank_slide_layout)
    set_bg(s5, C_CREAM)

    tb = s5.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(8.0), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "DEMO SCENARIOS · CONTROLLED PROTOTYPE BEHAVIORS"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    tb = s5.shapes.add_textbox(Inches(0.8), Inches(0.95), Inches(11.7), Inches(0.8))
    p = tb.text_frame.paragraphs[0]
    p.text = "Four scenarios. Four predictable behaviors."
    p.font.name = FONT_HEAD
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    tb = s5.shapes.add_textbox(Inches(0.8), Inches(1.75), Inches(11.7), Inches(0.5))
    p = tb.text_frame.paragraphs[0]
    p.text = "Expected prototype behaviors across staged benchmark cases. Not measured production metrics."
    p.font.name = FONT_HEAD
    p.font.size = Pt(19)
    p.font.color.rgb = C_MUTED

    scenarios = [
        ("CASE A · READY", C_TEAL_LIGHT, C_TEAL, "Verified Damage · Staged cosmetic crack, timestamp 00:04 · Defect verified.", "Agent prepares mock label & draft refund in pending_return_receipt; seller one-click confirms."),
        ("CASE B · MISMATCH", C_CORAL_LIGHT, RGBColor(0x99, 0x1B, 0x1B), "Color Contradiction · HEAD-WHT-02 (White) ordered vs Frame 00:07 Black item · SKU unverified.", "P-03 contradiction blocks automation; seller selects 1 of 3 options: mis-shipment / box label / warehouse inspection."),
        ("CASE C · UNCLEAR", RGBColor(0xEF, 0xF6, 0xFF), RGBColor(0x1E, 0x40, 0xAF), "Insufficient Visibility · 4-second dark video, brightness 28, only 2 usable frames.", "Agent requests targeted photo; enters WAITING_FOR_EVIDENCE; resumes case on upload (1 retry limit)."),
        ("CASE D · CONTEXT", RGBColor(0xEC, 0xFD, 0xF5), RGBColor(0x06, 0x5F, 0x46), "Sequence Continuity · Staged parcel-to-product take: opening sealed parcel to product reveal.", "Expected behavior: inspect sequence continuity and flag missing transitions for seller review.")
    ]

    lane_top = Inches(2.35)
    lane_h = Inches(0.95)
    lane_gap = Inches(0.14)

    for i, (badge_txt, b_bg, b_fg, ev_txt, act_txt) in enumerate(scenarios):
        ly = lane_top + i * (lane_h + lane_gap)
        box = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), ly, Inches(11.733), lane_h)
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER_LIGHT
        box.line.width = Pt(1)

        badge = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), ly + Inches(0.24), Inches(1.8), Inches(0.46))
        badge.fill.solid()
        badge.fill.fore_color.rgb = b_bg
        badge.line.fill.background()
        p = badge.text_frame.paragraphs[0]
        p.text = badge_txt
        p.font.name = FONT_MONO
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = b_fg
        p.alignment = PP_ALIGN.CENTER

        tb_ev = s5.shapes.add_textbox(Inches(3.0), ly + Inches(0.12), Inches(4.3), Inches(0.7))
        tf = tb_ev.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = ev_txt
        p.font.name = FONT_HEAD
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_DARK

        tb_arr = s5.shapes.add_textbox(Inches(7.35), ly + Inches(0.16), Inches(0.3), Inches(0.5))
        p = tb_arr.text_frame.paragraphs[0]
        p.text = "→"
        p.font.name = FONT_MONO
        p.font.size = Pt(14)
        p.font.color.rgb = C_TEAL

        tb_act = s5.shapes.add_textbox(Inches(7.75), ly + Inches(0.12), Inches(4.6), Inches(0.7))
        tf = tb_act.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = act_txt
        p.font.name = FONT_HEAD
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_MUTED

    add_footer(s5, "Staged prototype scenarios · Expected agent behaviors, not measured production metrics · Cap: min(₹4,999, remaining refundable amount, order paid amount)", "Slide 5 / 6")

    set_speaker_notes(s5, """
Slide 5 — Four Reproducible Benchmark Scenarios:
- Note on Grounding: These four scenarios represent staged prototype test suites and deterministic expected behaviors, NOT ungrounded production field metrics.
- Case A (Clean Claim): All rules pass (within 7d, SKU matches manifest, tag visible, physical crack observed). System drafts return shipping label and refund draft in 'pending_return_receipt' state. No refund money is transferred until physical warehouse receipt.
- Case B (Contradiction): Color mismatch detected (ordered white, unboxed black). System prevents auto-rejection and routes to seller review with 3 concrete resolution options.
- Case C (Unclear / Agentic Loop): Dark video (28/255 avg brightness). Instead of auto-denying, the agent provides a clear checklist, transitions to WAITING_FOR_EVIDENCE, and resumes on upload (1 retry limit protects customers from infinite loops).
- Case D (Continuity): Expected prototype behavior: inspect parcel-to-product sequence to flag suspicious cut-aways or missing transitions.
- Financial Cap Formula: min(₹4,999, remaining refundable amount, order paid amount) strictly prevents over-refunding.
""")

    # =========================================================================
    # SLIDE 6: 24-HOUR EXECUTION (TIMELINE GRID & STRICT SCOPE)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_slide_layout)
    set_bg(s6, C_CREAM)

    tb = s6.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(8.0), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "24-HOUR PROTOTYPE PLAN · FEASIBILITY & SCOPE GUARDRAILS"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    tb = s6.shapes.add_textbox(Inches(0.8), Inches(0.95), Inches(11.7), Inches(0.8))
    p = tb.text_frame.paragraphs[0]
    p.text = "Built for a 24-hour sprint."
    p.font.name = FONT_HEAD
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    tb = s6.shapes.add_textbox(Inches(0.8), Inches(1.75), Inches(11.7), Inches(0.5))
    p = tb.text_frame.paragraphs[0]
    p.text = "Strict scope boundaries and clear division of labor make the prototype fully buildable in one day."
    p.font.name = FONT_HEAD
    p.font.size = Pt(19)
    p.font.color.rgb = C_MUTED

    # 4-Phase Timeline Grid (00h-06h, 06h-12h, 12h-18h, 18h-24h)
    phases = [
        ("00h – 06h · Foundation", "Mock APIs & Agent Core", "Person A (Backend), supported by C\nLangGraph skeleton, mock store/courier fixtures, order status route"),
        ("06h – 12h · Evidence", "Evidence Pipeline & Policy", "Person B (Video & UI)\nFFmpeg keyframe indexer, Python rules P-01 to P-08, critic prompt"),
        ("12h – 18h · Integration", "State Flow & Scenarios", "Person C (Integration), supported by A/B\nEnd-to-end wiring, clarification/resume loop, seller console UI"),
        ("18h – 24h · Validation", "Testing & Submission", "All 3 Members\nFallback testing, authorization tests, demo video recording, README")
    ]

    p_w = Inches(2.8)
    p_gap = Inches(0.17)
    p_top = Inches(2.35)
    p_h = Inches(1.35)

    for i, (t_time, t_title, t_owner) in enumerate(phases):
        px = Inches(0.8) + i * (p_w + p_gap)
        box = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, px, p_top, p_w, p_h)
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER_LIGHT
        box.line.width = Pt(1)

        top_bar = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, px, p_top, p_w, Inches(0.04))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = C_TEAL
        top_bar.line.fill.background()

        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = t_time
        p.font.name = FONT_MONO
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_TEAL

        p2 = tf.add_paragraph()
        p2.text = t_title
        p2.font.name = FONT_HEAD
        p2.font.size = Pt(11.5)
        p2.font.bold = True
        p2.font.color.rgb = C_DARK

        p3 = tf.add_paragraph()
        p3.text = t_owner
        p3.font.name = FONT_HEAD
        p3.font.size = Pt(9)
        p3.font.color.rgb = C_MUTED

    sc_w = Inches(5.7)
    sc_h = Inches(1.95)

    # In Scope
    sc_in = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.9), sc_w, sc_h)
    sc_in.fill.solid()
    sc_in.fill.fore_color.rgb = C_WHITE
    sc_in.line.color.rgb = C_BORDER_LIGHT
    sc_in.line.width = Pt(1)

    bar = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.9), Inches(0.08), sc_h)
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_TEAL
    bar.line.fill.background()

    tb = s6.shapes.add_textbox(Inches(1.05), Inches(4.0), sc_w - Inches(0.35), sc_h - Inches(0.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "NEVER CUT (CORE ENGINE)"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    p2 = tf.add_paragraph()
    p2.text = "• Deterministic policy engine (P-01 to P-08)\n• Evidence-pack frame citation\n• Fail-closed seller approval gate\n• Structured JSON audit log\n• Clarification/resume loop\n• 4 reproducible demo cases"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(10)
    p2.font.color.rgb = C_DARK

    # Out of Scope
    sc_out = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.833), Inches(3.9), sc_w, sc_h)
    sc_out.fill.solid()
    sc_out.fill.fore_color.rgb = C_WHITE
    sc_out.line.color.rgb = C_BORDER_LIGHT
    sc_out.line.width = Pt(1)

    bar = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.833), Inches(3.9), Inches(0.08), sc_h)
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_CORAL
    bar.line.fill.background()

    tb = s6.shapes.add_textbox(Inches(7.083), Inches(4.0), sc_w - Inches(0.35), sc_h - Inches(0.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CUT FIRST IF BEHIND (DEFERRED EXPANSION)"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CORAL

    p2 = tf.add_paragraph()
    p2.text = "• Real carrier webhook integration (keep mock courier)\n• Multi-product order parsing (keep 1 item/return)\n• Custom video encoding (keep standard 1 fps FFmpeg extraction)\n• Production payment gateways / live WhatsApp webhooks\n• Seller analytics dashboard"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(10)
    p2.font.color.rgb = C_DARK

    # Closing quote banner
    q_box = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.0), Inches(11.733), Inches(0.65))
    q_box.fill.solid()
    q_box.fill.fore_color.rgb = RGBColor(0xFA, 0xF8, 0xF5)
    q_box.line.color.rgb = C_BORDER_LIGHT
    q_box.line.width = Pt(1)
    p = q_box.text_frame.paragraphs[0]
    p.text = "“The winning hackathon agent is not the one with the most tool definitions. It is the one where every action is held to evidence, and the seller stays in control.”"
    p.font.name = FONT_HEAD
    p.font.size = Pt(11)
    p.font.italic = True
    p.font.color.rgb = C_DARK
    p.alignment = PP_ALIGN.CENTER

    add_footer(s6, "Team Rookie (3 members) · PS-04 Autonomous Support Agent · 24-Hour Prototype Feasibility", "Slide 6 / 6")

    set_speaker_notes(s6, """
Slide 6 — 24-Hour Sprint Feasibility, Ownership & Strict Scope Guardrails:
- Feasibility Argument: Why is ReturnLens realistically buildable in 24 hours by 3 engineers?
  1. No live external production dependencies: deterministic mock APIs for Shopify & Shippo eliminate external latency and flakiness.
  2. Clear division of labor with single-threaded ownership across 3 teammates:
     - Person A (Backend): LangGraph state graph, mock store/courier fixtures, order-status route, state serialization.
     - Person B (Video & UI): FFmpeg keyframe extraction, deterministic rules P-01 to P-08, critic prompt, seller console.
     - Person C (Integration & Validation): Clarification/resume loop, 4 staged demo cases (A-D), authorization boundary tests, demo video recording, README.
  3. Strict Scope Discipline:
     - NEVER CUT: Core policy engine, frame citations, seller authorization gate, structured audit log, clarification/resume loop, 4 demo cases.
     - CUT FIRST IF BEHIND: Real carrier webhooks, multi-product order parsing, video OCR barcode scanning, production payment gateways, seller analytics dashboards.
- Winning Philosophy: "The winning hackathon agent is not the one with the most tool definitions. It is the one where every action is held to evidence, and the seller stays in control."
""")

    out_deliverables = base_dir / "deliverables" / "ReturnLens_v4.pptx"
    out_root = base_dir / "ReturnLens_v4.pptx"

    out_deliverables.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out_deliverables))
    prs.save(str(out_root))
    print(f"Saved PPTX to: {out_deliverables} and {out_root}")

if __name__ == "__main__":
    create_deck()
