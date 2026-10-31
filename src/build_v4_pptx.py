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

    # Colors
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

    tb = s1.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(6.0), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "AGENTX HACKATHON 2026 · TRACK PS-04"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    tb = s1.shapes.add_textbox(Inches(0.8), Inches(1.1), Inches(4.5), Inches(0.9))
    p = tb.text_frame.paragraphs[0]
    p.text = "RETURNLENS"
    p.font.name = FONT_HEAD
    p.font.size = Pt(56)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    tb = s1.shapes.add_textbox(Inches(0.8), Inches(2.1), Inches(4.5), Inches(0.8))
    p = tb.text_frame.paragraphs[0]
    p.text = "“Review returns with cited video evidence.”"
    p.font.name = FONT_HEAD
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    tb = s1.shapes.add_textbox(Inches(0.8), Inches(2.9), Inches(4.5), Inches(0.9))
    p = tb.text_frame.paragraphs[0]
    p.text = "An evidence-backed return triage agent for small direct-to-consumer sellers."
    p.font.name = FONT_HEAD
    p.font.size = Pt(14)
    p.font.color.rgb = C_MUTED

    meta_box = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.3), Inches(4.5), Inches(2.2))
    meta_box.fill.solid()
    meta_box.fill.fore_color.rgb = C_WHITE
    meta_box.line.color.rgb = C_BORDER_LIGHT
    meta_box.line.width = Pt(1)

    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.3), Inches(0.08), Inches(2.2))
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_TEAL
    bar.line.fill.background()

    tf = meta_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Team Rookie · 3 members · PS-04 Track"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    p2 = tf.add_paragraph()
    p2.text = "Target User: Solo D2C merchant managing orders and returns alone."
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = C_MUTED

    p3 = tf.add_paragraph()
    p3.text = "Scope in 24h: Return triage core + 1 zero-vision order status route."
    p3.font.name = FONT_HEAD
    p3.font.size = Pt(10.5)
    p3.font.color.rgb = C_MUTED

    p4 = tf.add_paragraph()
    p4.text = "Guardrails: Fail-closed architecture · No autonomous refunds."
    p4.font.name = FONT_HEAD
    p4.font.size = Pt(10.5)
    p4.font.bold = True
    p4.font.color.rgb = C_DARK

    # Console Window Right
    c_left = Inches(5.6)
    c_top = Inches(1.1)
    c_w = Inches(6.933)
    c_h = Inches(5.4)

    con = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, c_top, c_w, c_h)
    con.fill.solid()
    con.fill.fore_color.rgb = C_WHITE
    con.line.color.rgb = C_BORDER_LIGHT
    con.line.width = Pt(1)

    header = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, c_top, c_w, Inches(0.45))
    header.fill.solid()
    header.fill.fore_color.rgb = C_DARK
    header.line.fill.background()
    p = header.text_frame.paragraphs[0]
    p.text = "RETURNLENS SELLER CONSOLE · CASE #RET-4082          ORDER #ORD-9021"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_CREAM

    hero_img = str(assets_dir / "hero_video_frame.jpg")
    s1.shapes.add_picture(hero_img, c_left, c_top + Inches(0.45), Inches(3.8), c_h - Inches(0.45))

    p_left = c_left + Inches(3.8)
    p_w = c_w - Inches(3.8)
    side_panel = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, p_left, c_top + Inches(0.45), p_w, c_h - Inches(0.45))
    side_panel.fill.solid()
    side_panel.fill.fore_color.rgb = C_WHITE
    side_panel.line.color.rgb = C_BORDER_LIGHT
    side_panel.line.width = Pt(1)

    tb = s1.shapes.add_textbox(p_left + Inches(0.2), c_top + Inches(0.55), p_w - Inches(0.4), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "ORDER TRUTH"
    p.font.name = FONT_MONO
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_SUBTLE

    p2 = tf.add_paragraph()
    p2.text = "HEAD-WHT-02 · White Headphones"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(11.5)
    p2.font.bold = True
    p2.font.color.rgb = C_DARK

    p3 = tf.add_paragraph()
    p3.text = "₹1,499 · Delivered Day 4 (Within 7d window)"
    p3.font.name = FONT_HEAD
    p3.font.size = Pt(9.5)
    p3.font.color.rgb = C_MUTED

    p4 = tf.add_paragraph()
    p4.text = "\nVISUAL OBSERVATION"
    p4.font.name = FONT_MONO
    p4.font.size = Pt(9.5)
    p4.font.bold = True
    p4.font.color.rgb = C_SUBTLE

    p5 = tf.add_paragraph()
    p5.text = "Inspection Frame 00:14"
    p5.font.name = FONT_HEAD
    p5.font.size = Pt(11.5)
    p5.font.bold = True
    p5.font.color.rgb = C_DARK

    p6 = tf.add_paragraph()
    p6.text = "Potential casing damage flagged · Needs manual confirmation"
    p6.font.name = FONT_HEAD
    p6.font.size = Pt(9.5)
    p6.font.color.rgb = C_MUTED

    p7 = tf.add_paragraph()
    p7.text = "\nPOLICY VERIFICATION"
    p7.font.name = FONT_MONO
    p7.font.size = Pt(9.5)
    p7.font.bold = True
    p7.font.color.rgb = C_SUBTLE

    p8 = tf.add_paragraph()
    p8.text = "P-01 Defect Check: FLAGGED FOR REVIEW\nP-04 Return Window: PASS (Day 4 of 7)"
    p8.font.name = FONT_HEAD
    p8.font.size = Pt(10.5)
    p8.font.bold = True
    p8.font.color.rgb = RGBColor(0x92, 0x40, 0x0E)

    # Badge & Button
    badge = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, p_left + Inches(0.2), c_top + Inches(4.0), p_w - Inches(0.4), Inches(0.4))
    badge.fill.solid()
    badge.fill.fore_color.rgb = C_AMBER_LIGHT
    badge.line.fill.background()
    p = badge.text_frame.paragraphs[0]
    p.text = "READY FOR SELLER REVIEW (FLAGGED)"
    p.font.name = FONT_MONO
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x92, 0x40, 0x0E)
    p.alignment = PP_ALIGN.CENTER

    btn = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, p_left + Inches(0.2), c_top + Inches(4.5), p_w - Inches(0.4), Inches(0.45))
    btn.fill.solid()
    btn.fill.fore_color.rgb = C_TEAL
    btn.line.fill.background()
    p = btn.text_frame.paragraphs[0]
    p.text = "Review Evidence & Authorize Draft"
    p.font.name = FONT_HEAD
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.alignment = PP_ALIGN.CENTER

    add_footer(s1, "ReturnLens · Idea Pitch Deck · PS-04 · Team Rookie (3 members)", "Slide 1 / 6")

    set_speaker_notes(s1, """
Slide 1 — Product Hero & Executive Summary:
- Problem Statement fit: PS-04 (Autonomous Support Agent for Online Sellers).
- Target user: Solo direct-to-consumer (D2C) e-commerce merchants managing orders, shipping, and returns without dedicated support staff.
- Core insight: Solo merchants waste 15–20 minutes per return opening fragmented tabs (buyer chat, Shopify, Shippo tracking, return policy). Return decisions are made from memory without unified evidence.
- Differentiator: ReturnLens is not another open-ended conversational bot; it is a fail-closed, evidence-indexed triage agent.
- Visual anchor: The Seller Review Console mockup shows staged inspection frame 00:14. Notice the honest observation: rather than claiming an incontrovertible defect, the agent flags potential damage for seller confirmation.
- 24-hour scope: Return triage core + 1 zero-vision order-status route (reusing Shopify/Shippo mock APIs).
- Guardrail: Financial release strictly requires 1-click human seller authorization. No autonomous refunds.
""")

    # =========================================================================
    # SLIDE 2: THE PROBLEM (RECOMPOSED 3-COLUMN NO-OVERLAP)
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
    p.text = "The return decision is made from memory, before the evidence is checked."
    p.font.name = FONT_HEAD
    p.font.size = Pt(19)
    p.font.color.rgb = C_MUTED

    col_w = Inches(3.6)
    card_h = Inches(1.9)
    gap_w = Inches(3.9)

    # Left Column (Sources 01 & 03)
    c1 = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(2.6), col_w, card_h)
    c1.fill.solid()
    c1.fill.fore_color.rgb = C_WHITE
    c1.line.color.rgb = C_BORDER_LIGHT
    tf = c1.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "01 BUYER CHAT"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p2 = tf.add_paragraph()
    p2.text = "“Received damaged item”"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(13)
    p2.font.bold = True
    p2.font.color.rgb = C_DARK
    p3 = tf.add_paragraph()
    p3.text = "Buyer upload: 30–60s unboxing video + reason in support message"
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
    p2.text = "Delivered 4 days ago"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(13)
    p2.font.bold = True
    p2.font.color.rgb = C_DARK
    p3 = tf.add_paragraph()
    p3.text = "Shippo mock tracking API scan timestamp verification"
    p3.font.name = FONT_HEAD
    p3.font.size = Pt(10)
    p3.font.color.rgb = C_MUTED

    # Center Gap Pillar (NO OVERLAP)
    c_gap = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.7), Inches(2.6), gap_w, Inches(4.0))
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
    p2.text = "NO SHARED EVIDENCE RECORD"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(15)
    p2.font.bold = True
    p2.font.color.rgb = C_CREAM
    p2.alignment = PP_ALIGN.CENTER

    p3 = tf.add_paragraph()
    p3.text = "\nToday the seller opens 4 tabs, then decides alone. A wrong refund loses inventory; an unfair denial loses a customer.\n\nThe gap is that no single record ties order truth, video frames, policy clauses, and decisions together."
    p3.font.name = FONT_HEAD
    p3.font.size = Pt(10.5)
    p3.font.color.rgb = RGBColor(0xD1, 0xD5, 0xDB)
    p3.alignment = PP_ALIGN.CENTER

    # Right Column (Sources 02 & 04)
    c2 = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.9), Inches(2.6), col_w, card_h)
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
    p2.text = "White Headphones · ₹1,499"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(13)
    p2.font.bold = True
    p2.font.color.rgb = C_DARK
    p3 = tf.add_paragraph()
    p3.text = "Shopify mock store API product inventory catalog"
    p3.font.name = FONT_HEAD
    p3.font.size = Pt(10)
    p3.font.color.rgb = C_MUTED

    c4 = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.9), Inches(4.7), col_w, card_h)
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
- Problem: The returns bottleneck is not lack of return policies; it is fragmented, unverified context.
- Sources:
  1. Buyer claim in chat (unverified claims, emotional text).
  2. Order truth in Shopify store (SKU HEAD-WHT-02, price ₹1,499).
  3. Tracking scan in Shippo courier API (delivered 4 days ago).
  4. Store return policy document (7-day defect window, security tag).
- The central gap: No shared evidence record connecting video, store orders, and shipping timestamps into a single auditable artifact.
- Fraud statistics note: Estimates differ fundamentally by methodology. NRF 2025 reports 9% for strictly criminal return fraud, whereas Appriss/Deloitte 2024 reports 15.14% when including policy abuse (wardrobing, unboxing swaps). Never conflate these two metrics.
- Cost to seller: Triage takes 15–20 minutes per ticket. Erroneous approval bleeds gross margins; unfair rejection destroys customer lifetime value (LTV).
""")

    # =========================================================================
    # SLIDE 3: STAR DEMO SLIDE (EVIDENCE BENCHMARK)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_slide_layout)
    set_bg(s3, C_CREAM)

    tb = s3.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(8.0), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "VISUAL EVIDENCE BENCHMARK · CORE DEMONSTRATION"
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
    p.text = "ReturnLens surfaces the contradiction instead of auto-denying."
    p.font.name = FONT_HEAD
    p.font.size = Pt(19)
    p.font.color.rgb = C_MUTED

    card_w = Inches(3.7)
    ev_h = Inches(4.4)

    # White Order Card
    c1 = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(2.35), card_w, ev_h)
    c1.fill.solid()
    c1.fill.fore_color.rgb = C_WHITE
    c1.line.color.rgb = C_BORDER_LIGHT
    c1.line.width = Pt(1)

    s3.shapes.add_picture(str(assets_dir / "demo_white_order.jpg"), Inches(0.8), Inches(2.35), card_w, Inches(3.2))

    tb = s3.shapes.add_textbox(Inches(0.9), Inches(5.6), card_w - Inches(0.2), Inches(1.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "ORDER RECORD · STORE GROUND TRUTH"
    p.font.name = FONT_MONO
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p2 = tf.add_paragraph()
    p2.text = "HEAD-WHT-02 · Matte White · ₹1,499\nDelivered 4 days ago · Original tag present"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(10)
    p2.font.color.rgb = C_MUTED

    # Black Video Card
    c2 = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.7), Inches(2.35), card_w, ev_h)
    c2.fill.solid()
    c2.fill.fore_color.rgb = C_WHITE
    c2.line.color.rgb = C_BORDER_LIGHT
    c2.line.width = Pt(1)

    s3.shapes.add_picture(str(assets_dir / "demo_black_frame.jpg"), Inches(4.7), Inches(2.35), card_w, Inches(3.2))

    tb = s3.shapes.add_textbox(Inches(4.8), Inches(5.6), card_w - Inches(0.2), Inches(1.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "VIDEO FRAME · INTAKE TIMESTAMP 00:07"
    p.font.name = FONT_MONO
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p2 = tf.add_paragraph()
    p2.text = "Observed Color: Midnight Black\nExact SKU: Not verified · Tag: Not visible in cited frame"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(10)
    p2.font.color.rgb = C_MUTED

    # Callout
    callout = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(3.7), Inches(3.8), Inches(1.8), Inches(0.5))
    callout.fill.solid()
    callout.fill.fore_color.rgb = C_CORAL
    callout.line.fill.background()
    p = callout.text_frame.paragraphs[0]
    p.text = "COLOR MISMATCH"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.alignment = PP_ALIGN.CENTER

    # Right Decision Panel
    dp = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.6), Inches(2.35), Inches(3.933), ev_h)
    dp.fill.solid()
    dp.fill.fore_color.rgb = C_WHITE
    dp.line.color.rgb = C_BORDER_LIGHT
    dp.line.width = Pt(1)

    bar = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.6), Inches(2.35), Inches(0.08), ev_h)
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_CORAL
    bar.line.fill.background()

    tb = s3.shapes.add_textbox(Inches(8.8), Inches(2.45), Inches(3.5), Inches(4.1))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "DETERMINISTIC POLICY GATE"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_CORAL

    p2 = tf.add_paragraph()
    p2.text = "P-03 Check: COLOR MISMATCH"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(15)
    p2.font.bold = True
    p2.font.color.rgb = C_DARK

    p3 = tf.add_paragraph()
    p3.text = "Specification contradiction flagged against Shopify order manifest."
    p3.font.name = FONT_HEAD
    p3.font.size = Pt(10)
    p3.font.color.rgb = C_MUTED

    p4 = tf.add_paragraph()
    p4.text = "\ntyped JSON, requires_seller_approval: true"
    p4.font.name = FONT_MONO
    p4.font.size = Pt(9)
    p4.font.bold = True
    p4.font.color.rgb = C_TEAL

    p5 = tf.add_paragraph()
    p5.text = "\nSTATUS: ESCALATE (SELLER REVIEW REQUIRED)"
    p5.font.name = FONT_MONO
    p5.font.size = Pt(9.5)
    p5.font.bold = True
    p5.font.color.rgb = RGBColor(0x99, 0x1B, 0x1B)

    p6 = tf.add_paragraph()
    p6.text = "Color mismatch observed · Exact SKU unconfirmed · No auto-denial."
    p6.font.name = FONT_HEAD
    p6.font.size = Pt(9.5)
    p6.font.color.rgb = RGBColor(0x99, 0x1B, 0x1B)

    p7 = tf.add_paragraph()
    p7.text = "\nSeller Action Options:\n1. Accept as merchant mis-shipment (seller mistake)\n2. Ask customer for outside-box shipping label (buyer mistake)\n3. Hold return for physical inspection at warehouse (potential swap)"
    p7.font.name = FONT_HEAD
    p7.font.size = Pt(9)
    p7.font.color.rgb = C_DARK

    p8 = tf.add_paragraph()
    p8.text = "\nCap: 0 < amount <= min(₹4,999, remaining refundable amount, order paid amount)\nNo auto-denial · No refund released without seller click"
    p8.font.name = FONT_HEAD
    p8.font.size = Pt(8.5)
    p8.font.color.rgb = C_MUTED

    add_footer(s3, "Illustrative staged evidence · Mock Shopify & Shippo APIs", "Slide 3 / 6")

    set_speaker_notes(s3, """
Slide 3 — The Star Demo & Technical Honesty in Vision Citation:
- Core benchmark scenario (Case B): Buyer ordered white headphones (HEAD-WHT-02, ₹1,499), but unboxing frame 00:07 shows black headphones.
- Grounding & Honesty: Notice that the agent does NOT claim to read an unreadable SKU barcode from 00:07. It states factually: "Observed Color: Midnight Black · Exact SKU: Not verified".
- Decision logic: Seeing a black item when white was ordered is an undeniable visual contradiction against the manifest. Instead of auto-denying the customer (which might alienate an honest buyer if the warehouse mis-shipped), the policy engine triggers ESCALATE.
- Three clear merchant options are presented:
  1. Accept mis-shipment (warehouse mistake).
  2. Request outside-box label photo (buyer opened wrong family parcel).
  3. Route to warehouse inspection (possible fraud).
- Schema: typed JSON, requires_seller_approval: true.
- Financial cap: 0 < amount <= min(₹4,999, remaining refundable amount, order paid amount).
""")

    # =========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE
    # =========================================================================
    s4 = prs.slides.add_slide(blank_slide_layout)
    set_bg(s4, C_DARK_BG)

    tb = s4.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(8.0), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "SYSTEM ARCHITECTURE · DETERMINISTIC PIPELINE"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x00, 0xD1, 0xA7)

    tb = s4.shapes.add_textbox(Inches(0.8), Inches(0.95), Inches(11.7), Inches(0.8))
    p = tb.text_frame.paragraphs[0]
    p.text = "Models observe. Code verifies. Seller authorizes."
    p.font.name = FONT_HEAD
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_CREAM

    tb = s4.shapes.add_textbox(Inches(0.8), Inches(1.75), Inches(11.7), Inches(0.5))
    p = tb.text_frame.paragraphs[0]
    p.text = "Policy checks and seller approval control actions."
    p.font.name = FONT_HEAD
    p.font.size = Pt(19)
    p.font.color.rgb = RGBColor(0xA3, 0xB8, 0xB0)

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
    p_top = Inches(2.35)
    p_h = Inches(1.3)

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
        p2.font.size = Pt(11.5)
        p2.font.bold = True
        p2.font.color.rgb = C_CREAM

        tb_tag = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, px + Inches(0.1), p_top + Inches(0.88), p_w - Inches(0.2), Inches(0.28))
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

        # Connecting arrow
        if i < len(pipe_steps) - 1:
            arr_box = s4.shapes.add_textbox(px + p_w, p_top + Inches(0.4), p_gap, Inches(0.4))
            p_arr = arr_box.text_frame.paragraphs[0]
            p_arr.text = "→"
            p_arr.font.name = FONT_MONO
            p_arr.font.size = Pt(14)
            p_arr.font.bold = True
            p_arr.font.color.rgb = RGBColor(0x00, 0xD1, 0xA7)
            p_arr.alignment = PP_ALIGN.CENTER

    # Order Status Route Sub-bar (PS-04 Fit)
    sec_bar = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.8), Inches(11.733), Inches(0.4))
    sec_bar.fill.solid()
    sec_bar.fill.fore_color.rgb = RGBColor(0x14, 0x22, 0x1D)
    sec_bar.line.color.rgb = C_BORDER_DARK
    tf = sec_bar.text_frame
    p = tf.paragraphs[0]
    p.text = "SECONDARY PS-04 ROUTE:  Customer: “Where is my order?” → Mock Store API → Courier Scan → Instant Delivery Timestamp (Zero-Vision Fast Path)"
    p.font.name = FONT_MONO
    p.font.size = Pt(9.5)
    p.font.color.rgb = RGBColor(0xA3, 0xB8, 0xB0)

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

    # Legend / Critic line
    leg = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.65), Inches(11.733), Inches(0.95))
    leg.fill.solid()
    leg.fill.fore_color.rgb = RGBColor(0x12, 0x1F, 0x1B)
    leg.line.color.rgb = C_BORDER_DARK
    leg.line.width = Pt(1)

    tf = leg.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "■ Model Calls: Exactly 3 base calls per case (planner, vision, critic) plus retries  |  ■ Policy Clauses: Deterministic Python code rules P-01 to P-08, never prompts"
    p.font.name = FONT_MONO
    p.font.size = Pt(9)
    p.font.color.rgb = RGBColor(0xA3, 0xB8, 0xB0)

    p2 = tf.add_paragraph()
    p2.text = "■ Critic Duty: The critic reviews cited frames and flags unsupported observations  |  ■ Safety: Prompt injection cannot alter policy code or bypass human gate"
    p2.font.name = FONT_MONO
    p2.font.size = Pt(9)
    p2.font.color.rgb = RGBColor(0xA3, 0xB8, 0xB0)

    add_footer(s4, "Structured audit log recorded at every state transition · Decision priority: Contradiction > Hard fail > Unclear only > All pass", "Slide 4 / 6", is_dark=True)

    set_speaker_notes(s4, """
Slide 4 — System Architecture & Deterministic Governance:
- Philosophy: "Models observe. Code verifies. Seller authorizes."
- Pipeline (6 steps):
  1. Planner [MODEL]: Validates incoming JSON payload against strict schema.
  2. Tools & Video [CODE]: Extracts keyframes with FFmpeg; calls mock Shopify/Shippo endpoints.
  3. Policy Engine [CODE]: Evaluates deterministic Python rules P-01 through P-08 (window, SKU match, tags).
  4. Evidence Critic [MODEL]: Secondary auditor verifying cited timestamps against extracted observations to catch hallucinated damage.
  5. Seller Gate [HUMAN]: Merchant console where human authorizes mock label or draft refund.
  6. Audit Log [CODE]: Immutable append-only structured JSON log for every state transition.
- Broad PS-04 alignment: A fast zero-vision route handles routine "Where is my order?" inquiries by querying the courier tracking tool directly, answering customer queries in sub-second time.
- Strict priority order for decision function:
  Contradiction > Hard fail > Unclear only > All pass.
- Bounded calls: Exactly 3 base LLM calls per triage case.
""")

    # =========================================================================
    # SLIDE 5: FOUR DEMO BENCHMARK SCENARIOS
    # =========================================================================
    s5 = prs.slides.add_slide(blank_slide_layout)
    set_bg(s5, C_CREAM)

    tb = s5.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(8.0), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "DEMO SCENARIOS · GROUNDED VERIFICATION"
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
    p.text = "Every decision can be clicked back to a frame, a clause, and a log entry."
    p.font.name = FONT_HEAD
    p.font.size = Pt(19)
    p.font.color.rgb = C_MUTED

    scenarios = [
        ("CASE A · READY", C_TEAL_LIGHT, C_TEAL, "ORD-1042 (₹1,499) · SKU matches manifest, tag visible, defect confirmed within 7-day window.", "Seller approval releases mock return label and refund draft in pending_return_receipt, not executed refund."),
        ("CASE B · MISMATCH", C_CORAL_LIGHT, RGBColor(0x99, 0x1B, 0x1B), "HEAD-WHT-02 (White) ordered vs Frame 00:07 showing Black item · SKU unverified.", "ESCALATE (no label, no refund, no denial). Seller options: mis-shipment / box label / physical inspection."),
        ("CASE C · UNCLEAR", RGBColor(0xEF, 0xF6, 0xFF), RGBColor(0x1E, 0x40, 0xAF), "4-second dark video, brightness 28, only 2 usable frames · Unclear evidence check.", "Case stays open with exact re-film checklist. One retry limit prevents customer lock-out."),
        ("CASE D · CONTEXT", RGBColor(0xEC, 0xFD, 0xF5), RGBColor(0x06, 0x5F, 0x46), "Parcel-to-product take: opening sealed parcel to product reveal in one continuous take.", "Expected behavior: inspect sequence continuity and flag missing transitions for seller review.")
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

        badge = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), ly + Inches(0.24), Inches(1.7), Inches(0.46))
        badge.fill.solid()
        badge.fill.fore_color.rgb = b_bg
        badge.line.fill.background()
        p = badge.text_frame.paragraphs[0]
        p.text = badge_txt
        p.font.name = FONT_MONO
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = b_fg
        p.alignment = PP_ALIGN.CENTER

        tb_ev = s5.shapes.add_textbox(Inches(2.9), ly + Inches(0.12), Inches(4.4), Inches(0.7))
        tf = tb_ev.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = ev_txt
        p.font.name = FONT_HEAD
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_DARK

        tb_arr = s5.shapes.add_textbox(Inches(7.3), ly + Inches(0.16), Inches(0.3), Inches(0.5))
        p = tb_arr.text_frame.paragraphs[0]
        p.text = "→"
        p.font.name = FONT_MONO
        p.font.size = Pt(14)
        p.font.color.rgb = C_TEAL

        tb_act = s5.shapes.add_textbox(Inches(7.7), ly + Inches(0.12), Inches(4.7), Inches(0.7))
        tf = tb_act.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = act_txt
        p.font.name = FONT_HEAD
        p.font.size = Pt(11)
        p.font.color.rgb = C_MUTED

    add_footer(s5, "Staged benchmark scenarios · Expected prototype behaviors, not measured production metrics · Cap: min(₹4,999, remaining refundable amount, order paid amount)", "Slide 5 / 6")

    set_speaker_notes(s5, """
Slide 5 — Four Reproducible Benchmark Scenarios:
- Note on Grounding: These four scenarios represent staged prototype test suites and deterministic expected behaviors, NOT ungrounded production field metrics.
- Case A (Clean Claim): All rules pass (within 7d, SKU matches manifest, tag visible, physical crack observed). System drafts return shipping label and refund draft in 'pending_return_receipt' state. No refund money is transferred until physical warehouse receipt.
- Case B (Contradiction): Color mismatch detected (ordered white, unboxed black). System prevents auto-rejection and routes to seller review with 3 concrete resolution options.
- Case C (Unclear / Low Light): Dark video (28/255 avg brightness). Instead of auto-denying, the agent provides a clear checklist and allows 1 retry to protect legitimate customers.
- Case D (Continuity): Expected prototype behavior: inspect parcel-to-product sequence to flag suspicious cut-aways or missing transitions.
- Financial cap formula: min(₹4,999, remaining refundable amount, order paid amount) prevents catastrophic loss.
""")

    # =========================================================================
    # SLIDE 6: 24-HOUR EXECUTION (TIMELINE GRID)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_slide_layout)
    set_bg(s6, C_CREAM)

    tb = s6.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(8.0), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "EXECUTION PLAN · TEAM ROOKIE (3 MEMBERS)"
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
    p.text = "Buildable in 24 hours by 3 people, if the scope stays narrow."
    p.font.name = FONT_HEAD
    p.font.size = Pt(19)
    p.font.color.rgb = C_MUTED

    # 4-Phase Timeline Grid (00h-06h, 06h-12h, 12h-18h, 18h-24h)
    phases = [
        ("00h – 06h", "Mock APIs & Agent Core", "Person A (Backend)\nLangGraph skeleton, mock store/courier fixtures, order status route"),
        ("06h – 12h", "Evidence Pipeline & Policy", "Person B (Video & UI)\nFFmpeg keyframe indexer, Python rules P-01 to P-08, critic prompt"),
        ("12h – 18h", "Integration & 4 Scenarios", "Person C (Integration)\nEnd-to-end wiring, 4 staged demo cases (A–D), seller console UI"),
        ("18h – 24h", "Testing, Polish & Submission", "All 3 Members\nFallback testing, edge cases, video walkthrough recording, README")
    ]

    p_w = Inches(2.8)
    p_gap = Inches(0.17)
    p_top = Inches(2.35)
    p_h = Inches(1.3)

    for i, (t_time, t_title, t_owner) in enumerate(phases):
        px = Inches(0.8) + i * (p_w + p_gap)
        box = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, px, p_top, p_w, p_h)
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER_LIGHT
        box.line.width = Pt(1)

        # Teal top accent
        top_bar = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, px, p_top, p_w, Inches(0.04))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = C_TEAL
        top_bar.line.fill.background()

        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = t_time
        p.font.name = FONT_MONO
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_TEAL

        p2 = tf.add_paragraph()
        p2.text = t_title
        p2.font.name = FONT_HEAD
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = C_DARK

        p3 = tf.add_paragraph()
        p3.text = t_owner
        p3.font.name = FONT_HEAD
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = C_MUTED

    sc_w = Inches(5.7)
    sc_h = Inches(2.0)

    # In Scope
    sc_in = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.85), sc_w, sc_h)
    sc_in.fill.solid()
    sc_in.fill.fore_color.rgb = C_WHITE
    sc_in.line.color.rgb = C_BORDER_LIGHT
    sc_in.line.width = Pt(1)

    bar = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.85), Inches(0.08), sc_h)
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_TEAL
    bar.line.fill.background()

    tb = s6.shapes.add_textbox(Inches(1.05), Inches(3.95), sc_w - Inches(0.35), sc_h - Inches(0.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "NEVER CUT (CORE ENGINE)"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    p2 = tf.add_paragraph()
    p2.text = "• Deterministic policy engine (P-01 to P-08)\n• Evidence-pack frame citation\n• Fail-closed seller approval gate\n• Structured JSON audit log\n• 4 reproducible demo cases"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = C_DARK

    # Out of Scope
    sc_out = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.833), Inches(3.85), sc_w, sc_h)
    sc_out.fill.solid()
    sc_out.fill.fore_color.rgb = C_WHITE
    sc_out.line.color.rgb = C_BORDER_LIGHT
    sc_out.line.width = Pt(1)

    bar = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.833), Inches(3.85), Inches(0.08), sc_h)
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_CORAL
    bar.line.fill.background()

    tb = s6.shapes.add_textbox(Inches(7.083), Inches(3.95), sc_w - Inches(0.35), sc_h - Inches(0.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CUT FIRST (DEFERRED EXPANSION)"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CORAL

    p2 = tf.add_paragraph()
    p2.text = "• Video OCR barcode scanner\n• Auto-drafted customer email reply\n• Seller analytics dashboard\n• Production payment gateways / live WhatsApp webhooks\n• Public cloud deployment"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(10.5)
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
- Feasibility argument: Why is ReturnLens realistically buildable in 24 hours by 3 engineers?
  1. No live external production dependencies (we use deterministic mock APIs for Shopify & Shippo).
  2. Clear division of labor with single-threaded ownership across 3 teammates:
     - Person A (Backend): LangGraph state graph, policy logic P-01 to P-08, JSON audit logger, order-status route.
     - Person B (Video/UI): FFmpeg keyframe extraction script, Streamlit seller review console, frame citation display.
     - Person C (Integration/QA): 4 staged test datasets (Cases A-D), boundary testing, fallback test cases, demo recording, and submission docs.
  3. Scope discipline:
     - NEVER CUT: Core policy engine, frame citations, seller authorization gate, structured audit log.
     - CUT FIRST: Video OCR barcode scanning, automated customer email replying, seller analytics dashboards, production payment gateways.
- Winning philosophy: "The winning hackathon agent is not the one with the most tool definitions. It is the one where every action is held to evidence, and the seller stays in control."
""")

    out_deliverables = base_dir / "deliverables" / "ReturnLens_v4.pptx"
    out_root = base_dir / "ReturnLens_v4.pptx"

    out_deliverables.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out_deliverables))
    prs.save(str(out_root))
    print(f"Saved PPTX to: {out_deliverables} and {out_root}")

if __name__ == "__main__":
    create_deck()
