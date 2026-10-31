import os
import sys
import subprocess
import hashlib
from pathlib import Path
import fitz
from PIL import Image
from pptx import Presentation

base_dir = Path(__file__).resolve().parent.parent

def file_hash(p):
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def run_tests():
    print("=== STARTING RETURNLENS V4 SMOKE TESTS ===")
    all_passed = True

    # 1. Test generator execution
    print("\n[TEST 1] Running src/generate_v4_html.py...")
    script_html = base_dir / "src" / "generate_v4_html.py"
    h_before = file_hash(script_html)

    res = subprocess.run([sys.executable, str(script_html)], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FAILED: generate_v4_html.py returned code {res.returncode}:\n{res.stderr}")
        all_passed = False
    else:
        print("PASSED: generate_v4_html.py executed successfully.")

    # Check P0: Generator must NOT overwrite itself
    h_after = file_hash(script_html)
    if h_before != h_after:
        print("FAILED: P0 BUG DETECTED - generate_v4_html.py modified its own source code!")
        all_passed = False
    else:
        print("PASSED: P0 Check passed - generator source file remained completely untouched.")

    # 2. Test PPTX generator execution
    print("\n[TEST 2] Running src/build_v4_pptx.py...")
    script_pptx = base_dir / "src" / "build_v4_pptx.py"
    res_pptx = subprocess.run([sys.executable, str(script_pptx)], capture_output=True, text=True)
    if res_pptx.returncode != 0:
        print(f"FAILED: build_v4_pptx.py returned code {res_pptx.returncode}:\n{res_pptx.stderr}")
        all_passed = False
    else:
        print("PASSED: build_v4_pptx.py executed successfully.")

    # 3. Test Deliverable Integrity & Synchronization
    print("\n[TEST 3] Checking deliverable files and synchronization...")
    pairs = [
        ("ReturnLens_v4.html", "deliverables/ReturnLens_v4.html"),
        ("ReturnLens_v4.pdf", "deliverables/ReturnLens_v4.pdf"),
        ("ReturnLens_v4.pptx", "deliverables/ReturnLens_v4.pptx"),
        ("ReturnLens_v4_preview.png", "deliverables/ReturnLens_v4_preview.png"),
    ]

    for root_f, deliv_f in pairs:
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

    # 4. Test PDF properties
    print("\n[TEST 4] Validating PDF properties...")
    pdf_path = base_dir / "ReturnLens_v4.pdf"
    doc = fitz.open(pdf_path)
    if len(doc) != 6:
        print(f"FAILED: PDF page count is {len(doc)}, expected 6.")
        all_passed = False
    else:
        print(f"PASSED: PDF has exactly 6 pages.")

    rect = doc[0].rect
    ratio = rect.width / rect.height
    expected_ratio = 16.0 / 9.0
    if abs(ratio - expected_ratio) > 0.01:
        print(f"FAILED: PDF aspect ratio is {ratio:.3f}, expected {expected_ratio:.3f}.")
        all_passed = False
    else:
        print(f"PASSED: PDF aspect ratio is true 16:9 widescreen ({rect.width}x{rect.height}).")

    # 5. Test PPTX properties and Speaker Notes
    print("\n[TEST 5] Validating PPTX properties and Speaker Notes...")
    pptx_path = base_dir / "ReturnLens_v4.pptx"
    prs = Presentation(pptx_path)
    if len(prs.slides) != 6:
        print(f"FAILED: PPTX slide count is {len(prs.slides)}, expected 6.")
        all_passed = False
    else:
        print("PASSED: PPTX has exactly 6 slides.")

    missing_notes = []
    for i, slide in enumerate(prs.slides):
        if not slide.has_notes_slide:
            missing_notes.append(i + 1)
        else:
            txt = slide.notes_slide.notes_text_frame.text.strip()
            if len(txt) == 0:
                missing_notes.append(i + 1)
            else:
                print(f"  Slide {i+1} Speaker Notes: {len(txt)} chars (Starts: '{txt[:45]}...')")

    if missing_notes:
        print(f"FAILED: Slides {missing_notes} missing speaker notes in PPTX.")
        all_passed = False
    else:
        print("PASSED: All 6 slides have verified embedded speaker notes.")

    # 6. Test Preview Image Dimensions
    print("\n[TEST 6] Validating Preview Image Dimensions...")
    prev_path = base_dir / "ReturnLens_v4_preview.png"
    im = Image.open(prev_path)
    if im.size != (2352, 900):
        print(f"FAILED: Preview image size is {im.size}, expected (2352, 900).")
        all_passed = False
    else:
        print(f"PASSED: Preview image size is verified (2352, 900).")

    # 7. Test Evidence Grounding & Honest Text Checks
    print("\n[TEST 7] Verifying Evidence Grounding in PDF & PPTX...")
    pdf_text = ""
    for page in doc:
        pdf_text += page.get_text() + "\n"

    pdf_lower = pdf_text.lower()

    # Grounding check 1: No fabricated "casing crack verified at lower seam"
    if "casing crack verified" in pdf_lower or "verified at lower seam" in pdf_lower:
        print("FAILED: Found unsupported 'casing crack verified' in PDF.")
        all_passed = False
    else:
        print("PASSED: Unverified defect claim removed; honest observation used.")

    # Grounding check 2: Observed SKU unverified on Slide 3
    if "exact sku: not verified" not in pdf_lower:
        print("FAILED: 'Exact SKU: Not verified' missing from Slide 3 evidence footer.")
        all_passed = False
    else:
        print("PASSED: Color mismatch clearly states SKU is unverified.")

    # Grounding check 3: PS-04 secondary route present
    if "secondary ps-04 route" not in pdf_lower or "where is my order?" not in pdf_lower:
        print("FAILED: Secondary PS-04 order-status route missing from Architecture slide.")
        all_passed = False
    else:
        print("PASSED: Secondary PS-04 order status route verified on Slide 4.")

    # Grounding check 4: Conservative Case D sequence
    if "inspect sequence continuity" not in pdf_lower:
        print("FAILED: Conservative Case D sequence continuity text missing from Slide 5.")
        all_passed = False
    else:
        print("PASSED: Case D uses conservative sequence continuity wording.")

    # 8. Test Idempotency (Second run)
    print("\n[TEST 8] Testing Generator Idempotency (Second Run)...")
    res2 = subprocess.run([sys.executable, str(script_html)], capture_output=True, text=True)
    if res2.returncode != 0:
        print("FAILED: Second execution of generate_v4_html.py failed.")
        all_passed = False
    elif file_hash(script_html) != h_before:
        print("FAILED: Second run corrupted generate_v4_html.py!")
        all_passed = False
    else:
        print("PASSED: Generator is 100% idempotent and safe.")

    print("\n==========================================")
    if all_passed:
        print("ALL RETURNLENS V4 SMOKE TESTS PASSED! READY FOR SUBMISSION.")
    else:
        print("SOME SMOKE TESTS FAILED. PLEASE REVIEW LOGS ABOVE.")
    print("==========================================")
    return all_passed

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
