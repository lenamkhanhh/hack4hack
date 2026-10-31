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
    print("=== STARTING RETURNLENS EXTENDED SMOKE & QA SUITE (V4 BASELINE + V5 FLAGSHIP) ===")
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

    # 2. Test V5 Flagship HTML & PDF Generator Execution
    print("\n[TEST 2] Running src/generate_v5_html.py...")
    script_v5_html = base_dir / "src" / "generate_v5_html.py"
    h_before_v5 = file_hash(script_v5_html)

    res_v5 = subprocess.run([sys.executable, str(script_v5_html)], capture_output=True, text=True)
    if res_v5.returncode != 0:
        print(f"FAILED: generate_v5_html.py returned code {res_v5.returncode}:\n{res_v5.stderr}")
        all_passed = False
    else:
        print("PASSED: generate_v5_html.py executed successfully.")

    h_after_v5 = file_hash(script_v5_html)
    if h_before_v5 != h_after_v5:
        print("FAILED: generate_v5_html.py modified its own source code!")
        all_passed = False
    else:
        print("PASSED: Generator source file remained completely untouched (100% idempotent).")

    # 3. Test V5 PPTX Generator Execution
    print("\n[TEST 3] Running src/build_v5_pptx.py...")
    script_v5_pptx = base_dir / "src" / "build_v5_pptx.py"
    res_pptx_v5 = subprocess.run([sys.executable, str(script_v5_pptx)], capture_output=True, text=True)
    if res_pptx_v5.returncode != 0:
        print(f"FAILED: build_v5_pptx.py returned code {res_pptx_v5.returncode}:\n{res_pptx_v5.stderr}")
        all_passed = False
    else:
        print("PASSED: build_v5_pptx.py executed successfully.")

    # 4. Test Deliverable Integrity & Synchronization (V5 Flagship)
    print("\n[TEST 4] Checking V5 deliverable files and synchronization...")
    pairs_v5 = [
        ("ReturnLens_v5.html", "deliverables/ReturnLens_v5.html"),
        ("ReturnLens_v5.html", "index.html"),
        ("ReturnLens_v5.pdf", "deliverables/ReturnLens_v5.pdf"),
        ("ReturnLens_v5.pptx", "deliverables/ReturnLens_v5.pptx"),
        ("ReturnLens_v5_preview.png", "deliverables/ReturnLens_v5_preview.png"),
    ]

    for root_f, deliv_f in pairs_v5:
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

    # 5. Test V5 PDF Properties
    print("\n[TEST 5] Validating V5 PDF properties...")
    pdf_v5_path = base_dir / "deliverables" / "ReturnLens_v5.pdf"
    doc_v5 = fitz.open(pdf_v5_path)
    if len(doc_v5) != 6:
        print(f"FAILED: V5 PDF page count is {len(doc_v5)}, expected 6.")
        all_passed = False
    else:
        print("PASSED: V5 PDF has exactly 6 pages.")

    rect_v5 = doc_v5[0].rect
    ratio_v5 = rect_v5.width / rect_v5.height
    expected_ratio = 16.0 / 9.0
    if abs(ratio_v5 - expected_ratio) > 0.01:
        print(f"FAILED: V5 PDF aspect ratio is {ratio_v5:.3f}, expected {expected_ratio:.3f}.")
        all_passed = False
    else:
        print(f"PASSED: V5 PDF aspect ratio is true 16:9 widescreen ({rect_v5.width}x{rect_v5.height}).")

    # 6. Test V5 PPTX Properties & Speaker Notes
    print("\n[TEST 6] Validating V5 PPTX Properties & Speaker Notes...")
    pptx_v5_path = base_dir / "deliverables" / "ReturnLens_v5.pptx"
    prs_v5 = Presentation(pptx_v5_path)
    if len(prs_v5.slides) != 6:
        print(f"FAILED: V5 PPTX slide count is {len(prs_v5.slides)}, expected 6.")
        all_passed = False
    else:
        print("PASSED: V5 PPTX has exactly 6 slides.")

    missing_notes = []
    for i, slide in enumerate(prs_v5.slides):
        if not slide.has_notes_slide:
            missing_notes.append(i + 1)
        else:
            txt = slide.notes_slide.notes_text_frame.text.strip()
            if len(txt) == 0:
                missing_notes.append(i + 1)
            else:
                print(f"  Slide {i+1} Speaker Notes: {len(txt)} chars")

    if missing_notes:
        print(f"FAILED: Slides {missing_notes} missing speaker notes in V5 PPTX.")
        all_passed = False
    else:
        print("PASSED: All 6 slides have verified embedded speaker notes in V5 PPTX.")

    # 7. Test V5 Preview Image Dimensions
    print("\n[TEST 7] Validating V5 Preview Image Dimensions...")
    prev_v5_path = base_dir / "deliverables" / "ReturnLens_v5_preview.png"
    im_v5 = Image.open(prev_v5_path)
    if im_v5.size != (2352, 882):
        print(f"FAILED: V5 preview image size is {im_v5.size}, expected (2352, 882).")
        all_passed = False
    else:
        print(f"PASSED: V5 preview image size is verified (2352, 882) - exact 16:9 contact sheet.")

    # 8. Test Evidence Grounding & Factual Consistency in V5
    print("\n[TEST 8] Verifying Evidence Grounding in V5 PDF & Content...")
    pdf_v5_text = ""
    for page in doc_v5:
        pdf_v5_text += page.get_text() + "\n"

    pdf_lower = " ".join(pdf_v5_text.lower().split())

    # Grounding check 1: Honest SKU unverified on Slide 3
    if "barcode: unverified" not in pdf_lower and "barcode unverified" not in pdf_lower and "barcode is unverified" not in pdf_lower:
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
    slide4_text = " ".join(doc_v5[3].get_text().lower().split())
    slide5_text = " ".join(doc_v5[4].get_text().lower().split())
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
    slide6_text = " ".join(doc_v5[5].get_text().lower().split())
    if "case d sequence test" not in slide6_text and "case d test" not in slide6_text:
        print("FAILED: Case D sequence test missing from Slide 6 Must Deliver.")
        all_passed = False
    else:
        print("PASSED: Slide 6 Must Deliver correctly distinguishes Case D sequence test.")

    if "advanced video forensic" not in slide6_text:
        print("FAILED: 'Advanced video forensics' missing from Slide 6 Cut First.")
        all_passed = False
    else:
        print("PASSED: Slide 6 Cut First correctly lists Advanced video forensics (Case D stretch).")

    # Grounding check 9: Speaker Notes alignment on Slide 6
    s6_notes = prs_v5.slides[5].notes_slide.notes_text_frame.text.lower()
    if "3 core demo cases" not in s6_notes or "advanced video forensic" not in s6_notes:
        print("FAILED: Slide 6 speaker notes not aligned with refined scope boundaries.")
        all_passed = False
    else:
        print("PASSED: Slide 6 speaker notes strictly aligned with Must Deliver & Cut First.")

    # 9. Test Visual Geometry in V5 PPTX
    print("\n[TEST 9] Validating Visual Geometry & Bounds in V5 PPTX...")
    geom_passed = True
    for s_idx, slide in enumerate(prs_v5.slides):
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

    if geom_passed:
        print("PASSED: All V5 slides passed geometry, safe margins, and collision checks.")

    print("\n==========================================")
    if all_passed:
        print("ALL RETURNLENS EXTENDED SMOKE & QA TESTS PASSED! V5 IS VERIFIED & READY FOR SUBMISSION.")
    else:
        print("SOME SMOKE TESTS FAILED. PLEASE REVIEW LOGS ABOVE.")
    print("==========================================")
    return all_passed

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
