import os
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
    C_DARK_BG = RGBColor(0x0D, 0x18, 0x14)
    C_AMBER = RGBColor(0xD8, 0x8C, 0x31)
    C_AMBER_LIGHT = RGBColor(0xFE, 0xF3, 0xC7)
    C_BORDER_LIGHT = RGBColor(0xD2, 0xCE, 0xC4)
    C_BORDER_DARK = RGBColor(0x23, 0x38, 0x30)
    C_MUTED = RGBColor(0x55, 0x60, 0x5B)
    C_SUBTLE = RGBColor(0x8A, 0x95, 0x90)
    C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)

    FONT_HEAD = "Inter"
    FONT_MONO = "IBM Plex Mono"

    def set_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_footer(slide, left_text, right_text, is_dark=False):
        y = Inches(6.85)
        # Line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y, Inches(11.733), Inches(0.015))
        line.fill.solid()
        line.fill.fore_color.rgb = C_BORDER_DARK if is_dark else C_BORDER_LIGHT
        line.line.fill.background()

        # Left text
        tb_left = slide.shapes.add_textbox(Inches(0.8), y + Inches(0.08), Inches(9.0), Inches(0.4))
        p = tb_left.text_frame.paragraphs[0]
        p.text = left_text
        p.font.name = FONT_MONO
        p.font.size = Pt(10)
        p.font.color.rgb = RGBColor(0x6C, 0x82, 0x79) if is_dark else C_SUBTLE

        # Right text
        tb_right = slide.shapes.add_textbox(Inches(10.0), y + Inches(0.08), Inches(2.533), Inches(0.4))
        p = tb_right.text_frame.paragraphs[0]
        p.text = right_text
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_MONO
        p.font.size = Pt(10)
        p.font.color.rgb = RGBColor(0x6C, 0x82, 0x79) if is_dark else C_SUBTLE

    # =========================================================================
    # SLIDE 1: HERO / PRODUCT IN ONE GLANCE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_slide_layout)
    set_bg(s1, C_CREAM)

    # Left Meta
    tb = s1.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(4.5), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "AGENTX HACKATHON 2026 · TRACK PS-04"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    # Left Title
    tb = s1.shapes.add_textbox(Inches(0.8), Inches(1.1), Inches(4.3), Inches(0.9))
    p = tb.text_frame.paragraphs[0]
    p.text = "RETURNLENS"
    p.font.name = FONT_HEAD
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    # Left Statement
    tb = s1.shapes.add_textbox(Inches(0.8), Inches(2.05), Inches(4.2), Inches(0.8))
    p = tb.text_frame.paragraphs[0]
    p.text = "“Review returns with cited video evidence.”"
    p.font.name = FONT_HEAD
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    # Left Desc
    tb = s1.shapes.add_textbox(Inches(0.8), Inches(2.95), Inches(4.2), Inches(0.9))
    p = tb.text_frame.paragraphs[0]
    p.text = "An evidence-backed return triage agent for small online sellers."
    p.font.name = FONT_HEAD
    p.font.size = Pt(17)
    p.font.color.rgb = C_MUTED

    # Left Meta Box
    box = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.1), Inches(4.2), Inches(1.3))
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(0xEB, 0xE8, 0xE1)
    box.line.color.rgb = C_TEAL
    box.line.width = Pt(2.5)
    tf = box.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "Team Rookie · 3 Members · 24h Prototype"
    p1.font.name = FONT_MONO
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = C_DARK
    p2 = tf.add_paragraph()
    p2.text = "Grounded Video Evidence · Staged Shopify/Shippo APIs"
    p2.font.name = FONT_MONO
    p2.font.size = Pt(10)
    p2.font.color.rgb = C_MUTED

    # Right Side: Product Console Mockup
    c_left = Inches(5.3)
    c_top = Inches(0.8)
    c_w = Inches(7.2)
    c_h = Inches(5.6)

    # Window Container
    win = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, c_top, c_w, c_h)
    win.fill.solid()
    win.fill.fore_color.rgb = C_WHITE
    win.line.color.rgb = C_BORDER_LIGHT
    win.line.width = Pt(1)

    # Header Bar
    hb = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, c_top, c_w, Inches(0.45))
    hb.fill.solid()
    hb.fill.fore_color.rgb = C_DARK
    hb.line.fill.background()
    p = hb.text_frame.paragraphs[0]
    p.text = "RETURNLENS SELLER CONSOLE · CASE #RET-4082          ORDER #ORD-9021"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.color.rgb = C_CREAM

    # Video Frame on Left
    base_dir = os.path.dirname(os.path.abspath(__file__))
    hero_img = os.path.join(base_dir, "assets", "hero_video_frame.jpg")
    s1.shapes.add_picture(hero_img, c_left, c_top + Inches(0.45), Inches(4.3), c_h - Inches(0.45))

    # Triage Panel on Right
    p_left = c_left + Inches(4.3)
    p_w = c_w - Inches(4.3)
    p_h = c_h - Inches(0.45)
    panel = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, p_left, c_top + Inches(0.45), p_w, p_h)
    panel.fill.solid()
    panel.fill.fore_color.rgb = RGBColor(0xFA, 0xF9, 0xF7)
    panel.line.color.rgb = C_BORDER_LIGHT
    panel.line.width = Pt(1)

    # Inside Panel Info
    tb = s1.shapes.add_textbox(p_left + Inches(0.15), c_top + Inches(0.55), p_w - Inches(0.3), Inches(3.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "ORDER TRUTH"
    p.font.name = FONT_MONO
    p.font.size = Pt(9)
    p.font.color.rgb = C_SUBTLE
    p.font.bold = True

    p = tf.add_paragraph()
    p.text = "HEAD-WHT-02 · White Headphones\n₹1,499 · Delivered Day 4 (In 7d window)"
    p.font.name = FONT_HEAD
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    p = tf.add_paragraph()
    p.text = "\nEVIDENCE CITATION"
    p.font.name = FONT_MONO
    p.font.size = Pt(9)
    p.font.color.rgb = C_SUBTLE
    p.font.bold = True

    p = tf.add_paragraph()
    p.text = "Frame 00:14: Casing seam fracture"
    p.font.name = FONT_HEAD
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    p = tf.add_paragraph()
    p.text = "\nPOLICY VERIFICATION"
    p.font.name = FONT_MONO
    p.font.size = Pt(9)
    p.font.color.rgb = C_SUBTLE
    p.font.bold = True

    p = tf.add_paragraph()
    p.text = "P-01 Physical Defect: PASS\nP-04 Return Window: PASS (4 of 7d)"
    p.font.name = FONT_HEAD
    p.font.size = Pt(12)
    p.font.color.rgb = C_DARK

    # Status Badge
    badge = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, p_left + Inches(0.15), c_top + Inches(4.35), p_w - Inches(0.3), Inches(0.42))
    badge.fill.solid()
    badge.fill.fore_color.rgb = C_TEAL_LIGHT
    badge.line.fill.background()
    p = badge.text_frame.paragraphs[0]
    p.text = "READY FOR SELLER REVIEW"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p.alignment = PP_ALIGN.CENTER

    # CTA Button
    btn = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, p_left + Inches(0.15), c_top + Inches(4.85), p_w - Inches(0.3), Inches(0.45))
    btn.fill.solid()
    btn.fill.fore_color.rgb = C_TEAL
    btn.line.fill.background()
    p = btn.text_frame.paragraphs[0]
    p.text = "Approve Return & Draft Refund"
    p.font.name = FONT_HEAD
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.alignment = PP_ALIGN.CENTER

    # Watermark
    tb = s1.shapes.add_textbox(p_left + Inches(0.15), c_top + Inches(5.32), p_w - Inches(0.3), Inches(0.25))
    p = tb.text_frame.paragraphs[0]
    p.text = "Illustrative staged evidence"
    p.font.name = FONT_MONO
    p.font.size = Pt(8)
    p.font.color.rgb = C_SUBTLE
    p.alignment = PP_ALIGN.CENTER

    add_footer(s1, "ReturnLens · Idea Pitch Deck", "Slide 1 / 6")

    s1.notes_slide.notes_text_frame.text = (
        "ReturnLens is an evidence-backed returns triage agent built for small D2C merchants.\n"
        "Solo merchants process 100% of returns manually, spending 15-20 minutes scrubbing videos and matching orders.\n"
        "ReturnLens connects unboxing video evidence to store records, applies deterministic policy checks, and prepares 1-click approvals."
    )

    # =========================================================================
    # SLIDE 2: THE PROBLEM AS A VISUAL STORY
    # =========================================================================
    s2 = prs.slides.add_slide(blank_slide_layout)
    set_bg(s2, C_CREAM)

    # Meta
    tb = s2.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(6.0), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "THE PROBLEM · SOLO SELLER BOTTLENECK"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    # Title
    tb = s2.shapes.add_textbox(Inches(0.8), Inches(1.05), Inches(11.7), Inches(0.8))
    p = tb.text_frame.paragraphs[0]
    p.text = "One return decision. Four disconnected sources."
    p.font.name = FONT_HEAD
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    # Subhead
    tb = s2.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(11.7), Inches(0.6))
    p = tb.text_frame.paragraphs[0]
    p.text = "Without a cited record connecting video, order truth and policy, the seller is guessing."
    p.font.name = FONT_HEAD
    p.font.size = Pt(19)
    p.font.color.rgb = C_MUTED

    # 4 Source Nodes
    def add_node(x, y, w, h, tag, title, sub):
        box = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER_LIGHT
        box.line.width = Pt(1)
        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = tag
        p.font.name = FONT_MONO
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_TEAL
        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.name = FONT_HEAD
        p2.font.size = Pt(14)
        p2.font.bold = True
        p2.font.color.rgb = C_DARK
        p3 = tf.add_paragraph()
        p3.text = sub
        p3.font.name = FONT_HEAD
        p3.font.size = Pt(11)
        p3.font.color.rgb = C_MUTED

    nw, nh = Inches(3.4), Inches(1.35)
    # Top Left
    add_node(Inches(0.8), Inches(2.7), nw, nh, "01 BUYER CHAT", "“Received damaged item”", "Unverified claim in customer message inbox")
    # Bottom Left
    add_node(Inches(0.8), Inches(4.7), nw, nh, "03 DELIVERY STATUS", "Delivered 4 days ago", "Courier shipping API tracking scan")
    # Top Right
    add_node(Inches(9.1), Inches(2.7), nw, nh, "02 ORDER RECORD", "White Headphones · ₹1,499", "E-commerce store inventory database")
    # Bottom Right
    add_node(Inches(9.1), Inches(4.7), nw, nh, "04 RETURN POLICY", "7-day return window", "Store terms & conditions PDF document")

    # Center Gap Box
    gap = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.6), Inches(3.1), Inches(4.1), Inches(2.4))
    gap.fill.solid()
    gap.fill.fore_color.rgb = RGBColor(0xFF, 0xFD, 0xF7)
    gap.line.color.rgb = C_AMBER
    gap.line.width = Pt(2)
    tf = gap.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CRITICAL INFORMATION GAP"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p.alignment = PP_ALIGN.CENTER

    p2 = tf.add_paragraph()
    p2.text = "NO SHARED EVIDENCE RECORD"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = C_DARK
    p2.alignment = PP_ALIGN.CENTER

    p3 = tf.add_paragraph()
    p3.text = "“Approve, deny, or ask for more evidence?”"
    p3.font.name = FONT_HEAD
    p3.font.size = Pt(14)
    p3.font.italic = True
    p3.font.color.rgb = C_MUTED
    p3.alignment = PP_ALIGN.CENTER

    add_footer(s2, "*U.S. retail fraud estimates: 9% (NRF) to 15.14% (Appriss/Deloitte); triage takes 15–20 min per return for solo sellers.", "Slide 2 / 6")

    s2.notes_slide.notes_text_frame.text = (
        "The core friction is not the policy rules themselves, but the lack of an evidence bridge connecting video, store orders, and shipping APIs.\n"
        "Solo merchants spend 15-20 minutes opening four different browser tabs per return.\n"
        "Without an objective evidence record, merchants either auto-approve (losing 9-15% in fraud/leakage) or reject confrontational claims (ruining customer trust)."
    )

    # =========================================================================
    # SLIDE 3: THE STAR DEMO SLIDE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_slide_layout)
    set_bg(s3, C_CREAM)

    # Meta
    tb = s3.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(8.0), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "VISUAL EVIDENCE BENCHMARK · CORE DEMONSTRATION"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    # Title
    tb = s3.shapes.add_textbox(Inches(0.8), Inches(0.95), Inches(11.7), Inches(0.8))
    p = tb.text_frame.paragraphs[0]
    p.text = "The order says white. The video shows black."
    p.font.name = FONT_HEAD
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    # Subhead
    tb = s3.shapes.add_textbox(Inches(0.8), Inches(1.75), Inches(11.7), Inches(0.5))
    p = tb.text_frame.paragraphs[0]
    p.text = "ReturnLens surfaces the contradiction instead of auto-denying."
    p.font.name = FONT_HEAD
    p.font.size = Pt(19)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    # Left Evidence Visuals
    ev_w = Inches(7.8)
    ev_h = Inches(4.3)
    card_w = Inches(3.8)

    # White Order Card
    c1 = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(2.35), card_w, ev_h)
    c1.fill.solid()
    c1.fill.fore_color.rgb = C_WHITE
    c1.line.color.rgb = C_BORDER_LIGHT
    c1.line.width = Pt(1)

    s3.shapes.add_picture(os.path.join(base_dir, "assets", "demo_white_order.jpg"), Inches(0.8), Inches(2.35), card_w, Inches(3.2))

    tb = s3.shapes.add_textbox(Inches(0.9), Inches(5.6), card_w - Inches(0.2), Inches(1.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "ORDER RECORD · SKU: HEAD-WHT-02"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p2 = tf.add_paragraph()
    p2.text = "Matte White · ₹1,499 · Delivered 4 days ago"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(11)
    p2.font.color.rgb = C_MUTED

    # Black Video Card
    c2 = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.8), Inches(2.35), card_w, ev_h)
    c2.fill.solid()
    c2.fill.fore_color.rgb = C_WHITE
    c2.line.color.rgb = C_BORDER_LIGHT
    c2.line.width = Pt(1)

    s3.shapes.add_picture(os.path.join(base_dir, "assets", "demo_black_frame.jpg"), Inches(4.8), Inches(2.35), card_w, Inches(3.2))

    tb = s3.shapes.add_textbox(Inches(4.9), Inches(5.6), card_w - Inches(0.2), Inches(1.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "VIDEO FRAME · TIME 00:07 / 00:32"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p2 = tf.add_paragraph()
    p2.text = "Observed: Midnight Black · SKU: Unverified"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(11)
    p2.font.color.rgb = C_MUTED

    # Connecting Callout
    callout = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(3.6), Inches(3.8), Inches(2.2), Inches(0.55))
    callout.fill.solid()
    callout.fill.fore_color.rgb = C_AMBER
    callout.line.fill.background()
    p = callout.text_frame.paragraphs[0]
    p.text = "COLOR MISMATCH"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.alignment = PP_ALIGN.CENTER

    # Right Decision Panel
    dp = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.9), Inches(2.35), Inches(3.6), ev_h)
    dp.fill.solid()
    dp.fill.fore_color.rgb = C_WHITE
    dp.line.color.rgb = C_BORDER_LIGHT
    dp.line.width = Pt(1)

    tb = s3.shapes.add_textbox(Inches(9.1), Inches(2.5), Inches(3.2), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "DETERMINISTIC POLICY GATE"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_AMBER

    p = tf.add_paragraph()
    p.text = "Policy P-03 Check"
    p.font.name = FONT_HEAD
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    p = tf.add_paragraph()
    p.text = "Specification contradiction detected."
    p.font.name = FONT_HEAD
    p.font.size = Pt(12)
    p.font.color.rgb = C_MUTED

    # Status Box
    s_box = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.1), Inches(3.55), Inches(3.2), Inches(0.48))
    s_box.fill.solid()
    s_box.fill.fore_color.rgb = C_AMBER_LIGHT
    s_box.line.color.rgb = C_AMBER
    s_box.line.width = Pt(1)
    p = s_box.text_frame.paragraphs[0]
    p.text = "STATUS: NEEDS SELLER REVIEW"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x92, 0x40, 0x0E)
    p.alignment = PP_ALIGN.CENTER

    tb2 = s3.shapes.add_textbox(Inches(9.1), Inches(4.15), Inches(3.2), Inches(1.1))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "SELLER ACTION OPTIONS"
    p.font.name = FONT_MONO
    p.font.size = Pt(9)
    p.font.color.rgb = C_SUBTLE
    p.font.bold = True
    p2 = tf2.add_paragraph()
    p2.text = "1. Request shipping-label photo\n2. Send to manual physical inspection"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(12)
    p2.font.color.rgb = C_DARK

    # Safety Guarantee
    safe = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.1), Inches(5.35), Inches(3.2), Inches(1.15))
    safe.fill.solid()
    safe.fill.fore_color.rgb = RGBColor(0xF7, 0xF7, 0xF5)
    safe.line.color.rgb = C_TEAL
    safe.line.width = Pt(2)
    tf = safe.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Safety Guarantees:"
    p.font.name = FONT_HEAD
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p2 = tf.add_paragraph()
    p2.text = "• No automatic customer denial\n• No refund or label released without seller click"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(10)
    p2.font.color.rgb = C_MUTED

    add_footer(s3, "Illustrative staged evidence · No real customer PII", "Slide 3 / 6")

    s3.notes_slide.notes_text_frame.text = (
        "Why no automatic denial is crucial:\n"
        "A color mismatch can indicate either buyer fraud OR a merchant mis-shipment (warehouse packing error).\n"
        "If the agent auto-denies, an innocent buyer gets alienated. If it auto-approves, the seller loses inventory.\n"
        "ReturnLens flags the exact timestamp (00:07) and offers 2 clear paths to resolve."
    )

    # =========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE (DARK)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_slide_layout)
    set_bg(s4, C_DARK_BG)

    # Meta
    tb = s4.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(8.0), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "SYSTEM ARCHITECTURE · DETERMINISTIC PIPELINE"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x00, 0xA3, 0x82)

    # Title
    tb = s4.shapes.add_textbox(Inches(0.8), Inches(0.95), Inches(11.7), Inches(0.8))
    p = tb.text_frame.paragraphs[0]
    p.text = "Models observe. Code verifies. Seller authorizes."
    p.font.name = FONT_HEAD
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_CREAM

    # Subhead
    tb = s4.shapes.add_textbox(Inches(0.8), Inches(1.75), Inches(11.7), Inches(0.5))
    p = tb.text_frame.paragraphs[0]
    p.text = "Deterministic policy gates and human authorization control every action."
    p.font.name = FONT_HEAD
    p.font.size = Pt(19)
    p.font.color.rgb = RGBColor(0xA3, 0xB8, 0xB0)

    # 6-Step Pipeline Nodes
    pipe_steps = [
        ("01", "Buyer Request", "INTAKE", RGBColor(0x26, 0x38, 0x31), C_CREAM),
        ("02", "Frame Extraction", "FFMPEG", RGBColor(0x26, 0x38, 0x31), C_CREAM),
        ("03", "Model Observation", "GEMINI FLASH", RGBColor(0x00, 0x38, 0x2B), RGBColor(0x00, 0xD1, 0xA7)),
        ("04", "Policy Engine", "PYTHON RULES", RGBColor(0x26, 0x38, 0x31), C_CREAM),
        ("05", "Evidence Critic", "VERIFICATION", RGBColor(0x00, 0x38, 0x2B), RGBColor(0x00, 0xD1, 0xA7)),
        ("06", "Seller Gate", "AUTHORIZATION", RGBColor(0x45, 0x26, 0x0A), RGBColor(0xFB, 0xBF, 0x24))
    ]

    p_w = Inches(1.85)
    p_gap = Inches(0.12)
    p_top = Inches(2.4)
    p_h = Inches(1.5)

    for i, (num, title, tag, tag_bg, tag_fg) in enumerate(pipe_steps):
        px = Inches(0.8) + i * (p_w + p_gap)
        box = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, px, p_top, p_w, p_h)
        box.fill.solid()
        box.fill.fore_color.rgb = RGBColor(0x17, 0x26, 0x21)
        box.line.color.rgb = C_BORDER_DARK
        box.line.width = Pt(1)

        # Accent top bar
        top_bar = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, px, p_top, p_w, Inches(0.04))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = tag_fg
        top_bar.line.fill.background()

        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = num
        p.font.name = FONT_MONO
        p.font.size = Pt(10)
        p.font.color.rgb = RGBColor(0x6C, 0x82, 0x79)

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.name = FONT_HEAD
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = C_CREAM

        # Tag
        tb_tag = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, px + Inches(0.12), p_top + Inches(1.05), p_w - Inches(0.24), Inches(0.32))
        tb_tag.fill.solid()
        tb_tag.fill.fore_color.rgb = tag_bg
        tb_tag.line.fill.background()
        p = tb_tag.text_frame.paragraphs[0]
        p.text = tag
        p.font.name = FONT_MONO
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = tag_fg
        p.alignment = PP_ALIGN.CENTER

    # 3 Branching Outcomes
    branches = [
        ("UNCLEAR EVIDENCE", RGBColor(0x60, 0xA5, 0xFA), "Ask for specific photo → Resume same case (1 retry limit). Prevents premature customer rejection."),
        ("CONTRADICTION DETECTED", RGBColor(0xF8, 0x71, 0x71), "Seller review required. System inhibits automated label generation and flags exact discrepancy."),
        ("ALL CHECKS PASS", RGBColor(0x34, 0xD3, 0x99), "Seller 1-click approval → Releases mock return label and drafts refund amount.")
    ]

    b_w = Inches(3.75)
    b_gap = Inches(0.24)
    b_top = Inches(4.2)
    b_h = Inches(1.6)

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
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = b_col

        p2 = tf.add_paragraph()
        p2.text = b_desc
        p2.font.name = FONT_HEAD
        p2.font.size = Pt(12)
        p2.font.color.rgb = RGBColor(0xA3, 0xB8, 0xB0)

    # Legend
    tb = s4.shapes.add_textbox(Inches(0.8), Inches(6.05), Inches(11.7), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "■ Model: Proposes observations & timestamps   |   ■ Code: Enforces rules P-01 to P-08 & caps   |   ■ Human: Sole authority to release financial actions"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(0x6C, 0x82, 0x79)

    add_footer(s4, "Structured audit log recorded at every state transition · Exactly 3 base LLM calls per case", "Slide 4 / 6", is_dark=True)

    s4.notes_slide.notes_text_frame.text = (
        "Technical Architecture Notes:\n"
        "- FFmpeg extracts keyframes at 1 fps; Gemini Flash inspects packaging, defect areas, and serial numbers.\n"
        "- LangGraph controls the state machine.\n"
        "- Policy rules P-01 to P-08 are deterministic Python functions (not model prompts).\n"
        "- Exactly 3 base calls: Planner, Vision, Critic. Cap formula: min(₹4,999, remaining refundable amount, order paid amount)."
    )

    # =========================================================================
    # SLIDE 5: FOUR DEMO OUTCOMES
    # =========================================================================
    s5 = prs.slides.add_slide(blank_slide_layout)
    set_bg(s5, C_CREAM)

    # Meta
    tb = s5.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(8.0), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "DEMO SCENARIOS · BENCHMARK MATRIX"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    # Title
    tb = s5.shapes.add_textbox(Inches(0.8), Inches(0.95), Inches(11.7), Inches(0.8))
    p = tb.text_frame.paragraphs[0]
    p.text = "Four scenarios. Four predictable behaviors."
    p.font.name = FONT_HEAD
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    # Subhead
    tb = s5.shapes.add_textbox(Inches(0.8), Inches(1.75), Inches(11.7), Inches(0.5))
    p = tb.text_frame.paragraphs[0]
    p.text = "Deliberate, bounded actions across common edge cases."
    p.font.name = FONT_HEAD
    p.font.size = Pt(19)
    p.font.color.rgb = C_MUTED

    scenarios = [
        ("READY", C_TEAL_LIGHT, C_TEAL, "Visible casing damage at 00:14 · Serial tag matches order record", "Prepare seller approval (Mock label & refund drafted)"),
        ("MISMATCH", C_AMBER_LIGHT, RGBColor(0x92, 0x40, 0x0E), "Black headphones received vs White ordered at 00:07", "Seller review (Warehouse error check vs physical inspection)"),
        ("UNCLEAR", RGBColor(0xEF, 0xF6, 0xFF), RGBColor(0x1E, 0x40, 0xAF), "Blurry shipping barcode at 00:02 · Serial tag unreadable", "Ask for specific photo (Auto-prompts buyer for focused still)"),
        ("CONTEXT", RGBColor(0xF3, 0xF4, 0xF6), RGBColor(0x37, 0x41, 0x51), "Crushed carton with courier tape intact at 00:11", "Check continuity (Approve with transit damage claim note)")
    ]

    lane_top = Inches(2.4)
    lane_h = Inches(0.95)
    lane_gap = Inches(0.18)

    for i, (badge_txt, b_bg, b_fg, ev_txt, act_txt) in enumerate(scenarios):
        ly = lane_top + i * (lane_h + lane_gap)
        box = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), ly, Inches(11.733), lane_h)
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER_LIGHT
        box.line.width = Pt(1)

        # Badge
        badge = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), ly + Inches(0.24), Inches(1.3), Inches(0.46))
        badge.fill.solid()
        badge.fill.fore_color.rgb = b_bg
        badge.line.fill.background()
        p = badge.text_frame.paragraphs[0]
        p.text = badge_txt
        p.font.name = FONT_MONO
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = b_fg
        p.alignment = PP_ALIGN.CENTER

        # Evidence
        tb_ev = s5.shapes.add_textbox(Inches(2.5), ly + Inches(0.15), Inches(5.0), Inches(0.65))
        p = tb_ev.text_frame.paragraphs[0]
        p.text = ev_txt
        p.font.name = FONT_HEAD
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_DARK

        # Arrow
        tb_arr = s5.shapes.add_textbox(Inches(7.6), ly + Inches(0.18), Inches(0.4), Inches(0.5))
        p = tb_arr.text_frame.paragraphs[0]
        p.text = "→"
        p.font.name = FONT_MONO
        p.font.size = Pt(16)
        p.font.color.rgb = C_SUBTLE

        # Action
        tb_act = s5.shapes.add_textbox(Inches(8.1), ly + Inches(0.15), Inches(4.2), Inches(0.65))
        p = tb_act.text_frame.paragraphs[0]
        p.text = act_txt
        p.font.name = FONT_HEAD
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_DARK

    add_footer(s5, "Expected behavior on staged prototype scenarios — not production metrics.", "Slide 5 / 6")

    s5.notes_slide.notes_text_frame.text = (
        "Four Staged Benchmark Cases:\n"
        "1. Case A (Ready): Damage visible, SKU matches -> prepares approval.\n"
        "2. Case B (Mismatch): Color discrepancy detected -> stops auto-approval, escalates.\n"
        "3. Case C (Unclear): Barcode out of focus -> triggers targeted retry for clean barcode photo.\n"
        "4. Case D (Context): Crushed carton with courier tape intact -> marks for carrier transit damage compensation."
    )

    # =========================================================================
    # SLIDE 6: 24-HOUR EXECUTION
    # =========================================================================
    s6 = prs.slides.add_slide(blank_slide_layout)
    set_bg(s6, C_CREAM)

    # Meta
    tb = s6.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(8.0), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "EXECUTION PLAN · TEAM ROOKIE (3 MEMBERS)"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    # Title
    tb = s6.shapes.add_textbox(Inches(0.8), Inches(0.95), Inches(11.7), Inches(0.8))
    p = tb.text_frame.paragraphs[0]
    p.text = "Built for a 24-hour sprint."
    p.font.name = FONT_HEAD
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    # Subhead
    tb = s6.shapes.add_textbox(Inches(0.8), Inches(1.75), Inches(11.7), Inches(0.5))
    p = tb.text_frame.paragraphs[0]
    p.text = "Strict scope discipline and single-threaded execution across 3 owners."
    p.font.name = FONT_HEAD
    p.font.size = Pt(19)
    p.font.color.rgb = C_MUTED

    # Timeline Phases
    phases = [
        ("0h – 6h", "Mock APIs & Agent Skeleton", "Owner A (Backend)"),
        ("6h – 12h", "Evidence Pipeline & Policy", "Owner B (Multimodal & UI)"),
        ("12h – 18h", "Integration & 4 Scenarios", "Owner C (QA & Data)"),
        ("18h – 24h", "End-to-End Polish & Video", "All 3 Members")
    ]

    # Timeline Bar Line
    t_line = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.1), Inches(11.733), Inches(0.04))
    t_line.fill.solid()
    t_line.fill.fore_color.rgb = C_TEAL
    t_line.line.fill.background()

    phase_w = Inches(2.9)
    for i, (t_time, t_title, t_owner) in enumerate(phases):
        px = Inches(0.8) + i * phase_w
        tb = s6.shapes.add_textbox(px, Inches(2.35), phase_w, Inches(0.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = t_time
        p.font.name = FONT_MONO
        p.font.size = Pt(14)
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
        p3.font.name = FONT_MONO
        p3.font.size = Pt(10)
        p3.font.color.rgb = C_MUTED

    # Scope Boundary Boxes
    sc_w = Inches(5.7)
    sc_h = Inches(2.6)

    # In Scope
    sc_in = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.6), sc_w, sc_h)
    sc_in.fill.solid()
    sc_in.fill.fore_color.rgb = C_WHITE
    sc_in.line.color.rgb = C_BORDER_LIGHT
    sc_in.line.width = Pt(1)

    # Teal left accent
    bar = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.6), Inches(0.08), sc_h)
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_TEAL
    bar.line.fill.background()

    tb = s6.shapes.add_textbox(Inches(1.05), Inches(3.75), sc_w - Inches(0.35), sc_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "IN SCOPE · 24-HOUR PROTOTYPE"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    p2 = tf.add_paragraph()
    p2.text = "• Mock store & shipping APIs\n• Staged video evidence keyframe pipeline\n• One seller review console with 1-click approval\n• Deterministic policy rules P-01 to P-08\n• Structured JSON audit log"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(13)
    p2.font.color.rgb = C_DARK

    # Out of Scope
    sc_out = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.833), Inches(3.6), sc_w, sc_h)
    sc_out.fill.solid()
    sc_out.fill.fore_color.rgb = C_WHITE
    sc_out.line.color.rgb = C_BORDER_LIGHT
    sc_out.line.width = Pt(1)

    # Grey left accent
    bar = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.833), Inches(3.6), Inches(0.08), sc_h)
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_SUBTLE
    bar.line.fill.background()

    tb = s6.shapes.add_textbox(Inches(7.083), Inches(3.75), sc_w - Inches(0.35), sc_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "OUT OF SCOPE · DEFERRED CAPABILITIES"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_SUBTLE

    p2 = tf.add_paragraph()
    p2.text = "• Real payment gateways / live banking APIs\n• Multi-seller platform / multi-tenancy\n• WhatsApp production webhooks\n• Voice / audio reasoning\n• Public cloud deployment"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(13)
    p2.font.color.rgb = C_DARK

    add_footer(s6, "Team Rookie (3 members) · Prototype scope strictly bounded to single-seller staged workflow.", "Slide 6 / 6")

    s6.notes_slide.notes_text_frame.text = (
        "Team Ownership & Scope Boundaries:\n"
        "- Person A: LangGraph agent graph, deterministic policy logic P-01 to P-08, and JSON audit logging.\n"
        "- Person B: FFmpeg frame extraction, visual indexer, and Streamlit/web seller console.\n"
        "- Person C: Staged mock datasets (Cases A-D), boundary testing, fallback test cases, demo video, and documentation.\n"
        "- Strict financial cap formula: min(₹4,999, remaining refundable amount, order paid amount)."
    )

    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(os.path.dirname(base_dir), "deliverables", "ReturnLens_v4.pptx")
    prs.save(out_path)
    print("Saved PPTX successfully:", out_path)

if __name__ == "__main__":
    create_deck()

