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

    base_dir = r"D:\Code\Code\AIO\Code\hack4hack\src"

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
    p.text = "Team Rookie · 3 members · PS-04 submission"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    p2 = tf.add_paragraph()
    p2.text = "User: Solo D2C merchant managing orders and returns alone."
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(11)
    p2.font.color.rgb = C_MUTED

    p3 = tf.add_paragraph()
    p3.text = "Scope in 24h: Return triage only, mock store data + 1 order-status route."
    p3.font.name = FONT_HEAD
    p3.font.size = Pt(11)
    p3.font.color.rgb = C_MUTED

    p4 = tf.add_paragraph()
    p4.text = "Not another chatbot; not an autonomous refund gate."
    p4.font.name = FONT_HEAD
    p4.font.size = Pt(11)
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

    hero_img = os.path.join(base_dir, "assets", "hero_video_frame.jpg")
    s1.shapes.add_picture(hero_img, c_left, c_top + Inches(0.45), Inches(3.8), c_h - Inches(0.45))

    p_left = c_left + Inches(3.8)
    p_w = c_w - Inches(3.8)
    side_panel = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, p_left, c_top + Inches(0.45), p_w, c_h - Inches(0.45))
    side_panel.fill.solid()
    side_panel.fill.fore_color.rgb = C_WHITE
    side_panel.line.color.rgb = C_BORDER_LIGHT
    side_panel.line.width = Pt(1)

    tb = s1.shapes.add_textbox(p_left + Inches(0.2), c_top + Inches(0.6), p_w - Inches(0.4), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "ORDER TRUTH"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_SUBTLE

    p2 = tf.add_paragraph()
    p2.text = "HEAD-WHT-02 · White Headphones"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = C_DARK

    p3 = tf.add_paragraph()
    p3.text = "₹1,499 · Delivered Day 4 (Within 7d window)"
    p3.font.name = FONT_HEAD
    p3.font.size = Pt(10)
    p3.font.color.rgb = C_MUTED

    p4 = tf.add_paragraph()
    p4.text = "\nEVIDENCE CITATION"
    p4.font.name = FONT_MONO
    p4.font.size = Pt(10)
    p4.font.bold = True
    p4.font.color.rgb = C_SUBTLE

    p5 = tf.add_paragraph()
    p5.text = "Inspection Frame 00:14"
    p5.font.name = FONT_HEAD
    p5.font.size = Pt(12)
    p5.font.bold = True
    p5.font.color.rgb = C_DARK

    p6 = tf.add_paragraph()
    p6.text = "Casing crack verified at lower seam"
    p6.font.name = FONT_HEAD
    p6.font.size = Pt(10)
    p6.font.color.rgb = C_MUTED

    p7 = tf.add_paragraph()
    p7.text = "\nPOLICY VERIFICATION"
    p7.font.name = FONT_MONO
    p7.font.size = Pt(10)
    p7.font.bold = True
    p7.font.color.rgb = C_SUBTLE

    p8 = tf.add_paragraph()
    p8.text = "P-01 Physical Defect: PASS"
    p8.font.name = FONT_HEAD
    p8.font.size = Pt(12)
    p8.font.bold = True
    p8.font.color.rgb = C_DARK

    # Badge & Button
    badge = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, p_left + Inches(0.2), c_top + Inches(4.0), p_w - Inches(0.4), Inches(0.4))
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

    btn = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, p_left + Inches(0.2), c_top + Inches(4.5), p_w - Inches(0.4), Inches(0.45))
    btn.fill.solid()
    btn.fill.fore_color.rgb = C_TEAL
    btn.line.fill.background()
    p = btn.text_frame.paragraphs[0]
    p.text = "Approve Return & Draft Refund"
    p.font.name = FONT_HEAD
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.alignment = PP_ALIGN.CENTER

    add_footer(s1, "ReturnLens · Idea Pitch Deck · PS-04 · Team Rookie (3 members)", "Slide 1 / 6")

    # =========================================================================
    # SLIDE 2: THE PROBLEM
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
    add_node(Inches(0.8), Inches(2.7), nw, nh, "01 BUYER CHAT", "“Received damaged item”", "Buyer upload: 30–60s unboxing video + reason")
    add_node(Inches(0.8), Inches(4.7), nw, nh, "03 COURIER TRACKING", "Delivered 4 days ago", "Shippo mock tracking API scan")
    add_node(Inches(9.1), Inches(2.7), nw, nh, "02 ORDER RECORD", "White Headphones · ₹1,499", "Shopify mock store API inventory database")
    add_node(Inches(9.1), Inches(4.7), nw, nh, "04 RETURN POLICY", "7-Day Window · Sealed Tag", "Deterministic code rules P-01 to P-08, never prompts")

    gap = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.5), Inches(2.9), Inches(4.3), Inches(2.8))
    gap.fill.solid()
    gap.fill.fore_color.rgb = C_DARK
    gap.line.color.rgb = C_CORAL
    gap.line.width = Pt(2)
    tf = gap.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "CRITICAL INFORMATION GAP"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_CORAL
    p.alignment = PP_ALIGN.CENTER

    p2 = tf.add_paragraph()
    p2.text = "NO SINGLE RECORD TIES ORDER, VIDEO & POLICY TOGETHER"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = C_CREAM
    p2.alignment = PP_ALIGN.CENTER

    p3 = tf.add_paragraph()
    p3.text = "Today the seller opens many tabs, then decides alone. A wrong refund loses money and stock; an unfair denial loses a repeat customer. The gap is not a missing returns portal, it is that no single record ties order, video frame, policy clause, and decision together."
    p3.font.name = FONT_HEAD
    p3.font.size = Pt(10)
    p3.font.color.rgb = RGBColor(0xD1, 0xD5, 0xDB)
    p3.alignment = PP_ALIGN.CENTER

    add_footer(s2, "Fraud estimates differ by definition: 9% (NRF 2025, fraud only) vs 15.14% (Appriss/Deloitte 2024, fraud + abuse).", "Slide 2 / 6")

    # =========================================================================
    # SLIDE 3: STAR DEMO SLIDE
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
    p2.text = "Matte White · ₹1,499 · Delivered 4 days ago · Tag present"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(10)
    p2.font.color.rgb = C_MUTED

    # Black Video Card
    c2 = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.7), Inches(2.35), card_w, ev_h)
    c2.fill.solid()
    c2.fill.fore_color.rgb = C_WHITE
    c2.line.color.rgb = C_BORDER_LIGHT
    c2.line.width = Pt(1)

    s3.shapes.add_picture(os.path.join(base_dir, "assets", "demo_black_frame.jpg"), Inches(4.7), Inches(2.35), card_w, Inches(3.2))

    tb = s3.shapes.add_textbox(Inches(4.8), Inches(5.6), card_w - Inches(0.2), Inches(1.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "VIDEO FRAME · TIME 00:07 / 00:32"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p2 = tf.add_paragraph()
    p2.text = "Observed: HEAD-BLK-09 · Midnight Black · Mock evidence pack"
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
    p2.text = "Policy P-03 Check: FAIL"
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
    p5.text = "\nSTATUS: ESCALATE (NEEDS SELLER REVIEW)"
    p5.font.name = FONT_MONO
    p5.font.size = Pt(10)
    p5.font.bold = True
    p5.font.color.rgb = RGBColor(0x99, 0x1B, 0x1B)

    p6 = tf.add_paragraph()
    p6.text = "\nSeller Action Options:"
    p6.font.name = FONT_MONO
    p6.font.size = Pt(9)
    p6.font.bold = True
    p6.font.color.rgb = C_DARK

    p7 = tf.add_paragraph()
    p7.text = "1. Accept as merchant mis-shipment\n2. Ask customer for outside-box shipping label\n3. Hold return for physical inspection at warehouse"
    p7.font.name = FONT_HEAD
    p7.font.size = Pt(9)
    p7.font.color.rgb = C_DARK

    p8 = tf.add_paragraph()
    p8.text = "\nCap: 0 < amount <= min(₹4,999, remaining refundable amount, order paid amount)\nNo auto-denial · No refund released without seller click"
    p8.font.name = FONT_HEAD
    p8.font.size = Pt(8.5)
    p8.font.color.rgb = C_MUTED

    add_footer(s3, "Illustrative staged evidence · Mock Shopify & Shippo APIs", "Slide 3 / 6")

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

    p_w = Inches(1.85)
    p_gap = Inches(0.12)
    p_top = Inches(2.35)
    p_h = Inches(1.4)

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
        p.font.size = Pt(9)
        p.font.color.rgb = RGBColor(0x6C, 0x82, 0x79)

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.name = FONT_HEAD
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = C_CREAM

        tb_tag = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, px + Inches(0.12), p_top + Inches(0.95), p_w - Inches(0.24), Inches(0.3))
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

    branches = [
        ("1. CONTRADICTION → ESCALATE", RGBColor(0xF8, 0x71, 0x71), "Discrepancy flagged (e.g. Case B). Inhibits automated label and refund draft."),
        ("2. HARD FAIL → ESCALATE", RGBColor(0xFB, 0xBF, 0x24), "Mandatory rule violation (e.g. expired window). Seller reviews; never auto-deny."),
        ("3. UNCLEAR ONLY → ASK MORE", RGBColor(0x60, 0xA5, 0xFA), "Low brightness or blur (e.g. Case C). Prompts exact re-film checklist (1 retry limit)."),
        ("4. ALL PASS → APPROVE REVIEW", RGBColor(0x34, 0xD3, 0x99), "All clauses pass (e.g. Case A). Prepares mock label and drafts refund in pending_return_receipt.")
    ]

    b_w = Inches(2.8)
    b_gap = Inches(0.17)
    b_top = Inches(4.0)
    b_h = Inches(1.3)

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
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = b_col

        p2 = tf.add_paragraph()
        p2.text = b_desc
        p2.font.name = FONT_HEAD
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = RGBColor(0xA3, 0xB8, 0xB0)

    # Legend / Critic line
    leg = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.5), Inches(11.733), Inches(0.9))
    leg.fill.solid()
    leg.fill.fore_color.rgb = RGBColor(0x12, 0x1F, 0x1B)
    leg.line.color.rgb = C_BORDER_DARK
    leg.line.width = Pt(1)

    tf = leg.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "■ Model Calls: Exactly 3 base calls per case (planner, vision, critic) plus retries  |  ■ Policy Clauses: Deterministic Python rules P-01 to P-08, never prompts"
    p.font.name = FONT_MONO
    p.font.size = Pt(9.5)
    p.font.color.rgb = RGBColor(0xA3, 0xB8, 0xB0)

    p2 = tf.add_paragraph()
    p2.text = "■ Critic: The critic reviews cited frames and flags unsupported observations  |  ■ Safety: Prompt injection cannot alter policy code or bypass human gate"
    p2.font.name = FONT_MONO
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = RGBColor(0xA3, 0xB8, 0xB0)

    add_footer(s4, "Structured audit log recorded at every state transition · Decision priority: Contradiction > Hard fail > Unclear only > All pass", "Slide 4 / 6", is_dark=True)

    # =========================================================================
    # SLIDE 5: FOUR DEMO SCENARIOS
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
        ("CASE A · READY", C_TEAL_LIGHT, C_TEAL, "ORD-1042 (₹1,499) · SKU matches manifest, tag present, visible defect within 7-day window.", "Seller approval releases mock return label and refund draft in pending_return_receipt, not executed refund."),
        ("CASE B · ESCALATE", C_CORAL_LIGHT, RGBColor(0x99, 0x1B, 0x1B), "HEAD-WHT-02 vs HEAD-BLK-09 at Frame 00:07 · Policy P-03 SKU mismatch FAIL.", "ESCALATE (no label, no refund, no denial). Seller options: mis-shipment / box label / physical inspection."),
        ("CASE C · ASK MORE", RGBColor(0xEF, 0xF6, 0xFF), RGBColor(0x1E, 0x40, 0xAF), "4-second dark video, brightness 28, only 2 usable frames · Unclear evidence check.", "Case stays open with exact re-film checklist. One retry limit prevents customer lock-out."),
        ("CASE D · CONTINUITY", RGBColor(0xEC, 0xFD, 0xF5), RGBColor(0x06, 0x5F, 0x46), "Unbroken take: opening sealed parcel to showing the label in one continuous sequence.", "Continuity verified: prevents photo-swap fraud before mock return label generation. Proves why video beats photos.")
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

    add_footer(s5, "Staged sample videos, mock store data, no real customer PII · Cap: min(₹4,999, remaining refundable amount, order paid amount)", "Slide 5 / 6")

    # =========================================================================
    # SLIDE 6: 24-HOUR EXECUTION
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

    owners = [
        ("PERSON A", "Backend & Agent Core", "Backend, agent graph, policy, critic, audit log."),
        ("PERSON B", "Video Pipeline & UI", "Video pipeline, video indexer, seller console, evidence pack view."),
        ("PERSON C", "Integration & Verification", "Integration, mock data, 4 demo cases, fallback testing, demo video, README.")
    ]

    t_line = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.1), Inches(11.733), Inches(0.04))
    t_line.fill.solid()
    t_line.fill.fore_color.rgb = C_TEAL
    t_line.line.fill.background()

    phase_w = Inches(3.8)
    for i, (t_time, t_title, t_owner) in enumerate(owners):
        px = Inches(0.8) + i * (phase_w + Inches(0.16))
        tb = s6.shapes.add_textbox(px, Inches(2.25), phase_w, Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = t_time
        p.font.name = FONT_MONO
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_TEAL

        p2 = tf.add_paragraph()
        p2.text = t_title
        p2.font.name = FONT_HEAD
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = C_DARK

        p3 = tf.add_paragraph()
        p3.text = t_owner
        p3.font.name = FONT_HEAD
        p3.font.size = Pt(10.5)
        p3.font.color.rgb = C_MUTED

    sc_w = Inches(5.7)
    sc_h = Inches(2.2)

    sc_in = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.45), sc_w, sc_h)
    sc_in.fill.solid()
    sc_in.fill.fore_color.rgb = C_WHITE
    sc_in.line.color.rgb = C_BORDER_LIGHT
    sc_in.line.width = Pt(1)

    bar = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.45), Inches(0.08), sc_h)
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_TEAL
    bar.line.fill.background()

    tb = s6.shapes.add_textbox(Inches(1.05), Inches(3.55), sc_w - Inches(0.35), sc_h - Inches(0.2))
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
    p2.font.size = Pt(11)
    p2.font.color.rgb = C_DARK

    sc_out = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.833), Inches(3.45), sc_w, sc_h)
    sc_out.fill.solid()
    sc_out.fill.fore_color.rgb = C_WHITE
    sc_out.line.color.rgb = C_BORDER_LIGHT
    sc_out.line.width = Pt(1)

    bar = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.833), Inches(3.45), Inches(0.08), sc_h)
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_CORAL
    bar.line.fill.background()

    tb = s6.shapes.add_textbox(Inches(7.083), Inches(3.55), sc_w - Inches(0.35), sc_h - Inches(0.2))
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
    p2.font.size = Pt(11)
    p2.font.color.rgb = C_DARK

    # Closing quote banner
    q_box = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.8), Inches(11.733), Inches(0.75))
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

    # Save to both deliverables and root
    root_dir = r"D:\Code\Code\AIO\Code\hack4hack"
    out_deliverables = os.path.join(root_dir, "deliverables", "ReturnLens_v4.pptx")
    out_root = os.path.join(root_dir, "ReturnLens_v4.pptx")

    prs.save(out_deliverables)
    prs.save(out_root)
    print("Saved PPTX to:", out_deliverables, "and", out_root)

if __name__ == "__main__":
    create_deck()
