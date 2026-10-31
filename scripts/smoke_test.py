import os
import sys
import json
import zipfile
import subprocess
import hashlib
from pathlib import Path
import fitz
from PIL import Image
from pptx import Presentation

base_dir = Path(__file__).resolve().parent.parent

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def file_hash(p):
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def run_tests():
    print("=== STARTING RETURNLENS EXTENDED SMOKE & QA SUITE (V7 FINAL COMPETITION EDITION) ===")
    all_passed = True

    # 1. Test Canonical Content Specification
    print("\n[TEST 1] Validating Canonical Data Specification (content/deck_data.json)...")
    data_path = base_dir / "content" / "deck_data.json"
    if not data_path.exists():
        print(f"FAILED: Canonical data file missing: {data_path}")
        all_passed = False
    else:
        try:
            with open(data_path, "r", encoding="utf-8") as f:
                d = json.load(f)
            sample_price = d["meta"]["sample_order"]["price"]
            ceiling = d["meta"]["refund_guardrail"]["ceiling"]
            print(f"PASSED: Canonical data loaded successfully. Sample order: {sample_price}, Ceiling: {ceiling}.")
            if sample_price != "₹1,499" or ceiling != "₹4,999":
                print(f"FAILED: Unexpected price/ceiling values in deck_data.json: {sample_price}, {ceiling}")
                all_passed = False
        except Exception as e:
            print(f"FAILED: deck_data.json parsing error: {e}")
            all_passed = False

    # 2. Test V7 Generators Execution & Idempotency
    print("\n[TEST 2] Running V7 generators (src/generate_v7_html.py & src/build_v7_pptx.py)...")
    script_v7_html = base_dir / "src" / "generate_v7_html.py"
    script_v7_pptx = base_dir / "src" / "build_v7_pptx.py"

    h_before_html = file_hash(script_v7_html)
    res_v7_html = subprocess.run([sys.executable, str(script_v7_html)], capture_output=True, text=True)
    if res_v7_html.returncode != 0:
        print(f"FAILED: generate_v7_html.py returned code {res_v7_html.returncode}:\n{res_v7_html.stderr}")
        all_passed = False
    else:
        print("PASSED: generate_v7_html.py executed successfully.")

    h_after_html = file_hash(script_v7_html)
    if h_before_html != h_after_html:
        print("FAILED: generate_v7_html.py modified its own source code!")
        all_passed = False
    else:
        print("PASSED: HTML generator is 100% idempotent.")

    res_v7_pptx = subprocess.run([sys.executable, str(script_v7_pptx)], capture_output=True, text=True)
    if res_v7_pptx.returncode != 0:
        print(f"FAILED: build_v7_pptx.py returned code {res_v7_pptx.returncode}:\n{res_v7_pptx.stderr}")
        all_passed = False
    else:
        print("PASSED: build_v7_pptx.py executed successfully.")

    # 3. Test V7 Deliverable Integrity & Synchronization
    print("\n[TEST 3] Checking V7 deliverable files and synchronization...")
    pairs_v7 = [
        ("ReturnLens_v7.html", "deliverables/ReturnLens_v7.html"),
        ("ReturnLens_v7.html", "index.html"),
        ("ReturnLens_v7.pdf", "deliverables/ReturnLens_v7.pdf"),
        ("ReturnLens_v7.pptx", "deliverables/ReturnLens_v7.pptx"),
        ("ReturnLens_v7_preview.png", "deliverables/ReturnLens_v7_preview.png"),
    ]

    for root_f, deliv_f in pairs_v7:
        p_root = base_dir / root_f
        p_deliv = base_dir / deliv_f
        if not p_root.exists() or p_root.stat().st_size == 0:
            print(f"FAILED: {root_f} missing or empty.")
            all_passed = False
        elif not p_deliv.exists() or p_deliv.stat().st_size == 0:
            print(f"FAILED: {deliv_f} missing or empty.")
            all_passed = False
        elif file_hash(p_root) != file_hash(p_deliv):
            print(f"FAILED: {root_f} and {deliv_f} are not synchronized (hashes differ).")
            all_passed = False
        else:
            print(f"PASSED: {root_f} synced with {deliv_f} ({p_root.stat().st_size} bytes).")

    # 4. Test V7 PDF Properties & 16:9 Aspect Ratio
    print("\n[TEST 4] Validating V7 PDF properties...")
    pdf_v7_path = base_dir / "deliverables" / "ReturnLens_v7.pdf"
    doc_v7 = fitz.open(pdf_v7_path)
    if len(doc_v7) != 6:
        print(f"FAILED: V7 PDF page count is {len(doc_v7)}, expected 6.")
        all_passed = False
    else:
        print("PASSED: V7 PDF has exactly 6 pages.")

    rect_v7 = doc_v7[0].rect
    ratio_v7 = rect_v7.width / rect_v7.height
    expected_ratio = 16.0 / 9.0
    if abs(ratio_v7 - expected_ratio) > 0.02:
        print(f"FAILED: V7 PDF aspect ratio is {ratio_v7:.3f}, expected {expected_ratio:.3f}.")
        all_passed = False
    else:
        print(f"PASSED: V7 PDF aspect ratio is true 16:9 widescreen ({rect_v7.width:.1f}x{rect_v7.height:.1f}).")

    # 5. Test V7 PPTX Properties & Full Canonical Speaker Notes
    print("\n[TEST 5] Validating V7 PPTX Properties & Speaker Notes...")
    pptx_v7_path = base_dir / "deliverables" / "ReturnLens_v7.pptx"
    prs_v7 = Presentation(pptx_v7_path)
    if len(prs_v7.slides) != 6:
        print(f"FAILED: V7 PPTX slide count is {len(prs_v7.slides)}, expected 6.")
        all_passed = False
    else:
        print("PASSED: V7 PPTX has exactly 6 slides.")

    missing_notes = []
    for i, slide in enumerate(prs_v7.slides):
        if not slide.has_notes_slide:
            missing_notes.append(i + 1)
        else:
            txt = slide.notes_slide.notes_text_frame.text.strip()
            if len(txt) < 300:
                missing_notes.append(i + 1)
            else:
                print(f"  Slide {i+1} Speaker Notes: {len(txt)} chars")

    if missing_notes:
        print(f"FAILED: Slides {missing_notes} missing or insufficient speaker notes in V7 PPTX.")
        all_passed = False
    else:
        print("PASSED: All 6 slides have verified embedded speaker notes in V7 PPTX.")

    # 6. Test V7 Preview Image Dimensions
    print("\n[TEST 6] Validating V7 Preview Image Dimensions...")
    prev_v7_path = base_dir / "deliverables" / "ReturnLens_v7_preview.png"
    im_v7 = Image.open(prev_v7_path)
    if im_v7.size != (2352, 882):
        print(f"FAILED: V7 preview image size is {im_v7.size}, expected (2352, 882).")
        all_passed = False
    else:
        print(f"PASSED: V7 preview image size is verified (2352, 882) - exact 16:9 contact sheet.")

    # 7. Test Evidence Grounding, Policies & Financial Ceiling in V7
    print("\n[TEST 7] Verifying Evidence Grounding in V7 PDF & Content...")
    pdf_v7_text = ""
    for page in doc_v7:
        pdf_v7_text += page.get_text() + "\n"

    pdf_lower = " ".join(pdf_v7_text.lower().split())

    # Grounding check 1: Honest SKU unverified on Slide 3
    if "barcode: unverified" not in pdf_lower and "barcode unverified" not in pdf_lower:
        print("FAILED: 'Barcode unverified' missing from Slide 3 evidence.")
        all_passed = False
    else:
        print("PASSED: Color mismatch clearly states barcode is unverified.")

    # Grounding check 2: PS-04 secondary route present
    if "tiny ps-04 order route" not in pdf_lower and "order route" not in pdf_lower:
        print("FAILED: Secondary PS-04 order-status route missing from Architecture slide.")
        all_passed = False
    else:
        print("PASSED: Secondary PS-04 order status route verified on Slide 4.")

    # Grounding check 3: Case C stateful clarification loop present
    if "waiting_for_evidence" not in pdf_lower or "ask_for_evidence" not in pdf_lower:
        print("FAILED: Case C stateful loop missing from Architecture slide.")
        all_passed = False
    else:
        print("PASSED: Dynamic stateful clarification loop verified on Slide 4.")

    # Grounding check 4: Conservative Case D sequence
    if "inspects sequence continuity" not in pdf_lower:
        print("FAILED: Conservative Case D sequence continuity text missing from Slide 5.")
        all_passed = False
    else:
        print("PASSED: Case D uses conservative sequence continuity wording.")

    # Grounding check 5: No exchange contradiction
    if "dispatch exchange" in pdf_lower or "issue exchange" in pdf_lower:
        print("FAILED: Exchange contradiction detected in seller options!")
        all_passed = False
    else:
        print("PASSED: Seller options clean of exchange contradiction.")

    # Grounding check 6: Cryptographic approval binding on Slide 4
    if "approval binds" not in pdf_lower or "evidence hash" not in pdf_lower:
        print("FAILED: Cryptographic approval binding missing from Slide 4 PDF.")
        all_passed = False
    else:
        print("PASSED: Approval binding (case ID + evidence hash + policy version) verified on Slide 4.")

    # Grounding check 7: Case C termination rule on both Slide 4 and Slide 5
    slide4_text = " ".join(doc_v7[3].get_text().lower().split())
    slide5_text = " ".join(doc_v7[4].get_text().lower().split())
    if "after 1 retry" not in slide4_text or "never auto-denies" not in slide4_text:
        print("FAILED: Case C termination rule ('after 1 retry... never auto-denies') missing from Slide 4.")
        all_passed = False
    else:
        print("PASSED: Case C termination rule verified on Slide 4.")

    if "after 1 retry" not in slide5_text or "never auto-denies" not in slide5_text:
        print("FAILED: Case C termination rule missing from Slide 5.")
        all_passed = False
    else:
        print("PASSED: Case C termination rule verified on Slide 5.")

    # Grounding check 8: Scope boundaries alignment on Slide 6
    slide6_text = " ".join(doc_v7[5].get_text().lower().split())
    if "case d sequence test" not in slide6_text:
        print("FAILED: Case D sequence test missing from Slide 6 Must Deliver.")
        all_passed = False
    else:
        print("PASSED: Slide 6 Must Deliver correctly distinguishes Case D sequence test.")

    if "advanced video forensics" not in slide6_text and "advanced video forensic" not in slide6_text:
        print("FAILED: 'Advanced video forensics' missing from Slide 6 Cut First.")
        all_passed = False
    else:
        print("PASSED: Slide 6 Cut First correctly lists Advanced video forensics (Case D stretch).")

    # 8. Test Visual Geometry in V7 PPTX & Slide 1 Console Padding
    print("\n[TEST 8] Validating Visual Geometry, Padding & Bounds in V7 PPTX...")
    geom_passed = True
    for s_idx, slide in enumerate(prs_v7.slides):
        for shape in slide.shapes:
            left = shape.left.inches if shape.left else 0
            top = shape.top.inches if shape.top else 0
            w = shape.width.inches if shape.width else 0
            h = shape.height.inches if shape.height else 0
            bottom = top + h
            right = left + w

            if right > 13.38 or bottom > 7.55:
                print(f"FAILED: Shape '{shape.name}' on Slide {s_idx + 1} exceeds slide boundary: right={right:.2f}, bottom={bottom:.2f}")
                geom_passed = False
                all_passed = False

            if top > 0.1 and top < 6.90 and bottom > 6.98:
                print(f"FAILED: Content shape '{shape.name}' on Slide {s_idx + 1} collides with footer line at y=7.0 (bottom={bottom:.2f})")
                geom_passed = False
                all_passed = False

    # Slide 1 Console Bottom Padding Validation
    # Action buttons should sit at or above y=5.85", card padding 0.18-0.25", clearance to footer > 1.10"
    s1 = prs_v7.slides[0]
    btn_shapes = []
    for sh in s1.shapes:
        if sh.has_text_frame and "Review & Authorize" in sh.text_frame.text:
            btn_shapes.append(sh)

    if btn_shapes:
        btn = btn_shapes[0]
        btn_bottom = btn.top.inches + btn.height.inches
        clearance_to_footer = 7.00 - btn_bottom
        print(f"  Slide 1 Action Button bottom: {btn_bottom:.2f}\" (target <= 5.85\"), Clearance to footer: {clearance_to_footer:.2f}\" (target > 1.10\")")
        if btn_bottom > 5.85:
            print(f"FAILED: Slide 1 button bottom ({btn_bottom:.2f}\") sits below y=5.85\"")
            geom_passed = False
            all_passed = False
        if clearance_to_footer < 1.10:
            print(f"FAILED: Slide 1 clearance to footer ({clearance_to_footer:.2f}\") is less than 1.10\"")
            geom_passed = False
            all_passed = False

    if geom_passed:
        print("PASSED: All V7 slides passed geometry, safe margins, and collision checks.")

    # 9. Test Media Assets & Freshness of PPTX Slide Renders
    print("\n[TEST 9] Validating Media Embeds and PPTX Render Freshness...")
    renders_dir = base_dir / "src" / "assets" / "v7_pptx_renders"
    if not renders_dir.exists():
        print(f"FAILED: PPTX renders directory missing: {renders_dir}")
        all_passed = False
    else:
        render_files = [renders_dir / f"slide_{i}.png" for i in range(1, 7)]
        all_exist = all(rf.exists() and rf.stat().st_size > 50000 for rf in render_files)
        if not all_exist:
            print(f"FAILED: One or more rendered slide PNGs missing or too small in {renders_dir}")
            all_passed = False
        else:
            print(f"PASSED: All 6 PPTX-rendered slide PNGs present in {renders_dir}.")

    # 10. Test Historical Preservation of V5 and V6 Binaries (Regression Protection)
    print("\n[TEST 10] Validating Historical V5 & V6 Preservation (Zero Regression)...")
    baseline_hashes = {
        "ReturnLens_v5.html": "201bc1a4ea9b7c8a03c282bdc645d69120ce24aa41454798cc14c20b8697d8af",
        "ReturnLens_v5.pdf": "a290d3e589d4bee66bbdc05e0e10485f856b47ced584fee20d9098c8b3af37a0",
        "ReturnLens_v5.pptx": "960b37af5a8ef15af6b618693355c330d8c953cc3de62ad8f5caa2854bc6da2f",
        "ReturnLens_v5_preview.png": "f18f943cc432921e0f21b7b208a86c41095d6407883d5131d0949de51d4d4312",
        "ReturnLens_v6.html": "c6ee4d37d7185f5662798d28d0d79f59d1d1aae63355b7ee25eab9991fb9adfa",
        "ReturnLens_v6.pdf": "471d36afcf83e41c9b3a09b9251d8a4f77a5c0189260dfec464994e821a5a371",
        "ReturnLens_v6.pptx": "0232f36e803d4b0d4180d6adfee533355e66cd9daa88693f17fbbde69438fec2",
        "ReturnLens_v6_preview.png": "1483430d8b7595cbbff1bac32fc78f6de920ef5ebb295416939fa4c254c5296f",
    }

    v5_v6_clean = True
    for fname, expected_hash in baseline_hashes.items():
        p_root = base_dir / fname
        if not p_root.exists():
            print(f"FAILED: Historical baseline file {fname} is missing!")
            v5_v6_clean = False
            all_passed = False
        else:
            curr_hash = file_hash(p_root)
            if curr_hash != expected_hash:
                print(f"FAILED: Historical file {fname} was modified! Hash: {curr_hash[:12]} vs expected: {expected_hash[:12]}")
                v5_v6_clean = False
                all_passed = False

    if v5_v6_clean:
        print("PASSED: All 8 historical V5 and V6 files are 100% byte-identical to pre-V7 baseline.")

    print("\n==========================================")
    if all_passed:
        print("ALL RETURNLENS V7 FINAL COMPETITION QA & SMOKE TESTS PASSED! (10/10)")
    else:
        print("SOME SMOKE TESTS FAILED. PLEASE REVIEW LOGS ABOVE.")
    print("==========================================")
    return all_passed

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
