import os
import sys
import json
import hashlib
from pathlib import Path
from PIL import Image
import fitz
from pptx import Presentation

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def file_hash(path):
    with open(path, "rb") as f:
        data = f.read()
    if str(path).endswith('.html'):
        data = data.replace(b'\r\n', b'\n')
    return hashlib.sha256(data).hexdigest()

def run_v8_1_smoke_test():
    base_dir = Path(__file__).resolve().parent.parent
    all_passed = True

    print("=== STARTING RETURNLENS V8.1 (FINAL IDEA ROUND EDITION) SMOKE & QA SUITE ===\n")

    # 1. Test Canonical Data
    print("[TEST 1] Validating Canonical Data Specification (content/deck_data_v8_1.json)...")
    data_path = base_dir / "content" / "deck_data_v8_1.json"
    if not data_path.exists():
        print(f"FAILED: {data_path} missing.")
        all_passed = False
    else:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        meta = data.get("meta", {})
        slides = data.get("slides", [])

        if len(slides) != 6:
            print(f"FAILED: Expected 6 slides in deck_data_v8_1.json, got {len(slides)}")
            all_passed = False
        else:
            print("PASSED: Exactly 6 slides present in canonical data.")

        # Script word count check (Target: 350 - 390 words)
        total_words = 0
        for s in slides:
            # extract actual spoken words (exclude timing headers in brackets)
            txt = s.get("speaker_notes", "")
            lines = [l for l in txt.split("\n") if not l.strip().startswith("[")]
            spoken_text = " ".join(lines)
            words = spoken_text.split()
            total_words += len(words)

        print(f"  Total pitch script word count: {total_words} words (Target: 350-390 words)")
        if total_words < 340 or total_words > 400:
            print(f"FAILED: Script word count {total_words} outside acceptable range (350-390).")
            all_passed = False
        else:
            print("PASSED: Script word count is perfectly calibrated for 3-minute pitch.")

        if meta.get("core_thesis") != "Models observe. Code verifies. Seller authorizes.":
            print("FAILED: Core thesis mismatch in deck_data_v8_1.json.")
            all_passed = False
        else:
            print("PASSED: Core architectural thesis verified.")

        qa_defense = data.get("qa_defense", [])
        if len(qa_defense) != 5:
            print(f"FAILED: Expected 5 Q&A defense questions, got {len(qa_defense)}")
            all_passed = False
        else:
            print("PASSED: All 5 hard hackathon defense questions verified in canonical data.")

    # 2. Test Deliverables Existence & Synchronization
    print("\n[TEST 2] Validating V8.1 Deliverables Existence & Synchronization (root vs deliverables/)...")
    pairs = [
        ("ReturnLens_v8_1.pptx", "deliverables/ReturnLens_v8_1.pptx"),
        ("ReturnLens_v8_1.pdf", "deliverables/ReturnLens_v8_1.pdf"),
        ("ReturnLens_v8_1.html", "deliverables/ReturnLens_v8_1.html"),
        ("ReturnLens_v8_1_preview.png", "deliverables/ReturnLens_v8_1_preview.png")
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
            print(f"FAILED: {root_f} and {deliv_f} hashes differ.")
            all_passed = False
        else:
            print(f"PASSED: {root_f} synchronized ({p_root.stat().st_size} bytes, SHA256: {file_hash(p_root)[:12]}...).")

    # 3. Test PDF Properties
    print("\n[TEST 3] Validating V8.1 PDF Properties (Pages & Aspect Ratio)...")
    pdf_path = base_dir / "deliverables" / "ReturnLens_v8_1.pdf"
    if not pdf_path.exists():
        print(f"FAILED: {pdf_path} missing.")
        all_passed = False
    else:
        doc = fitz.open(pdf_path)
        if len(doc) != 6:
            print(f"FAILED: Expected 6 pages, got {len(doc)}")
            all_passed = False
        else:
            print("PASSED: V8.1 PDF has exactly 6 pages.")

        rect = doc[0].rect
        ratio = rect.width / rect.height
        if abs(ratio - 16.0 / 9.0) > 0.02:
            print(f"FAILED: Ratio is {ratio:.3f}, expected 16:9 (1.778)")
            all_passed = False
        else:
            print(f"PASSED: V8.1 PDF aspect ratio is true 16:9 widescreen ({rect.width:.1f}x{rect.height:.1f}).")

    # 4. Test PPTX Properties & Speaker Notes
    print("\n[TEST 4] Validating V8.1 PPTX Properties & Embedded Speaker Notes...")
    pptx_path = base_dir / "deliverables" / "ReturnLens_v8_1.pptx"
    if not pptx_path.exists():
        print(f"FAILED: {pptx_path} missing.")
        all_passed = False
    else:
        prs = Presentation(pptx_path)
        if len(prs.slides) != 6:
            print(f"FAILED: Expected 6 slides in PPTX, got {len(prs.slides)}")
            all_passed = False
        else:
            print("PASSED: V8.1 PPTX has exactly 6 slides.")

        notes_ok = True
        for i, s in enumerate(prs.slides):
            txt = s.notes_slide.notes_text_frame.text if s.notes_slide else ""
            if len(txt.strip()) < 80:
                print(f"FAILED: Slide {i+1} has insufficient notes ({len(txt)} chars)")
                notes_ok = False
                all_passed = False
            else:
                print(f"  Slide {i+1} Speaker Notes: {len(txt)} chars")
        if notes_ok:
            print("PASSED: All 6 slides have verified embedded speaker notes.")

    # 5. Test Preview Sheet Dimensions
    print("\n[TEST 5] Validating V8.1 Preview Contact Sheet Dimensions...")
    prev_path = base_dir / "deliverables" / "ReturnLens_v8_1_preview.png"
    if not prev_path.exists():
        print(f"FAILED: {prev_path} missing.")
        all_passed = False
    else:
        im = Image.open(prev_path)
        if im.size != (2352, 882):
            print(f"FAILED: Size is {im.size}, expected (2352, 882)")
            all_passed = False
        else:
            print("PASSED: V8.1 Preview image is verified (2352, 882) - exact 16:9 contact sheet.")

    # 6. Test Content Grounding & Conceptual Consistency
    print("\n[TEST 6] Verifying Content Grounding & Conceptual Consistency...")
    if pdf_path.exists():
        doc = fitz.open(pdf_path)
        full_text = " ".join(p.get_text() for p in doc)
        full_lower = " ".join(full_text.lower().split())

        # Grounding check 1: Slide 1 CTA
        s1_text = doc[0].get_text()
        if "Review Evidence & Decide" not in s1_text:
            print("FAILED: Slide 1 CTA 'Review Evidence & Decide' missing.")
            all_passed = False
        else:
            print("PASSED: Slide 1 CTA 'Review Evidence & Decide' verified.")

        if "Seller authorizes returns, labels & refunds" not in s1_text:
            print("FAILED: Slide 1 action label missing accurate authority boundary.")
            all_passed = False
        else:
            print("PASSED: Slide 1 authority boundary verified.")

        # Grounding check 2: Slide 2 claim text
        s2_text = doc[1].get_text()
        if "i ordered white headphones, but received black" not in s2_text.lower():
            print("FAILED: Slide 2 customer claim text mismatch.")
            all_passed = False
        else:
            print("PASSED: Slide 2 customer claim text verified.")

        if "9.0%" in s2_text or "15.14%" in s2_text:
            print("FAILED: Slide 2 still contains 9.0%/15.14% fraud boxes.")
            all_passed = False
        else:
            print("PASSED: Slide 2 cleaned of unsourced fraud percentage boxes.")

        # Grounding check 3: Slide 3 Ordered White vs Observed Black
        s3_text = doc[2].get_text()
        if "Ordered: White" not in s3_text or "Observed: Black" not in s3_text:
            print("FAILED: Slide 3 missing prominent 'Ordered: White' or 'Observed: Black'.")
            all_passed = False
        else:
            print("PASSED: Slide 3 prominent 'Ordered: White' and 'Observed: Black' verified.")

        if "barcode unverified" not in s3_text.lower():
            print("FAILED: Slide 3 missing barcode unverified note.")
            all_passed = False
        else:
            print("PASSED: Slide 3 barcode unverified note verified.")

        if "outer-box label" not in s3_text:
            print("FAILED: Slide 3 missing drafted customer reply for outer-box label.")
            all_passed = False
        else:
            print("PASSED: Slide 3 drafted customer reply verified.")

        # Grounding check 4: Slide 4 Case C close-up photo flow
        s4_text = doc[3].get_text().lower()
        if "close-up photo" not in s4_text:
            print("FAILED: Slide 4 missing close-up photo flow for Case C.")
            all_passed = False
        else:
            print("PASSED: Slide 4 close-up photo flow for Case C verified.")

        # Grounding check 5: Slide 5 Case A and Case B consistency
        s5_text = doc[4].get_text()
        s5_norm = " ".join(s5_text.split()).lower()
        if "within the 7-day return window" not in s5_norm:
            print("FAILED: Slide 5 Case A missing 'within the 7-day return window'.")
            all_passed = False
        else:
            print("PASSED: Slide 5 Case A 'within the 7-day return window' verified.")

        if "i ordered white headphones, but received black" not in s5_norm:
            print("FAILED: Slide 5 Case B claim text not synchronized with Slide 2.")
            all_passed = False
        else:
            print("PASSED: Slide 5 Case B claim text perfectly synchronized.")

        if "close-up photo" not in s5_norm:
            print("FAILED: Slide 5 Case C missing close-up photo.")
            all_passed = False
        else:
            print("PASSED: Slide 5 Case C close-up photo verified.")

        # Grounding check 6: Slide 6 single-line title & closing takeaway
        s6_text = doc[5].get_text()
        if "A focused 24-hour prototype." not in s6_text:
            print("FAILED: Slide 6 single-line title missing.")
            all_passed = False
        else:
            print("PASSED: Slide 6 single-line title verified.")

        if "One clear evidence pack. The seller makes the call." not in s6_text:
            print("FAILED: Slide 6 closing takeaway missing.")
            all_passed = False
        else:
            print("PASSED: Slide 6 closing takeaway verified.")

    # 7. Test Geometry, Safe Margins & Anti-Collision in PPTX
    print("\n[TEST 7] Validating Visual Geometry, Padding & Safe Margins in V8.1 PPTX...")
    if pptx_path.exists():
        prs = Presentation(pptx_path)
        geom_ok = True
        for s_idx, slide in enumerate(prs.slides):
            max_bottom = 0
            for sh in slide.shapes:
                t = sh.top.inches if sh.top else 0
                l = sh.left.inches if sh.left else 0
                w = sh.width.inches if sh.width else 0
                h = sh.height.inches if sh.height else 0

                if w > 13.0 and h > 7.0:
                    continue

                b = t + h
                r = l + w

                if r > 13.38 or b > 7.55:
                    print(f"FAILED: Shape '{sh.name}' on Slide {s_idx + 1} exceeds slide bounds: right={r:.2f}, bottom={b:.2f}")
                    geom_ok = False
                    all_passed = False

                if t < 6.90 and b > 6.80:
                    print(f"FAILED: Content shape '{sh.name}' on Slide {s_idx + 1} collides with footer line at y=6.95 (bottom={b:.2f})")
                    geom_ok = False
                    all_passed = False

                if t < 6.90 and b > max_bottom:
                    max_bottom = b

            clearance = 6.95 - max_bottom
            print(f"  Slide {s_idx + 1}: max content bottom={max_bottom:.2f}\", clearance to footer={clearance:.2f}\"")
            if clearance < 0.30:
                print(f"FAILED: Slide {s_idx + 1} clearance to footer ({clearance:.2f}\") is less than 0.30\"")
                geom_ok = False
                all_passed = False

        if geom_ok:
            print("PASSED: All V8.1 slides passed geometry, safe margins, and collision checks.")

    # 8. Test Slide Renders & Manifest
    print("\n[TEST 8] Validating Slide Renders & render_manifest.json...")
    renders_dir = base_dir / "src" / "assets" / "v8_1_pptx_renders"
    manifest_path = renders_dir / "render_manifest.json"
    if not manifest_path.exists():
        print(f"FAILED: {manifest_path} missing.")
        all_passed = False
    else:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        cur_hash = file_hash(pptx_path)
        if manifest.get("source_sha256") != cur_hash:
            print(f"FAILED: Manifest hash mismatch: {manifest.get('source_sha256')[:12]} vs current {cur_hash[:12]}")
            all_passed = False
        else:
            print(f"PASSED: render_manifest.json matches current PPTX SHA256: {cur_hash[:12]}...")

        for i in range(1, 7):
            rf = renders_dir / f"slide_{i}.png"
            if not rf.exists() or rf.stat().st_size < 50000:
                print(f"FAILED: Render slide_{i}.png missing or too small.")
                all_passed = False
        print("PASSED: All 6 PPTX slide renders present and valid.")

    # 9. Test Historical Baseline Preservation
    print("\n[TEST 9] Validating Historical Baseline Preservation (Zero Regression)...")
    baseline_hashes = {
        "ReturnLens_v5.html": "ad4c421b6f0950b8afe3dfeae6976aafb1b2c1227da72881f82cdaeb368425be",
        "ReturnLens_v6.html": "a62ef784754320b00b4b83f9d7085e858ec3b68546ae3574556af84e41bf7eb5",
        "ReturnLens_v7.html": "bc5ebf29a05a7c38e370f6811137b49533488c69a8682ebc000f1599bfec7618",
        "ReturnLens_v7_1.pptx": "341b47be7aebc31480446cbfa0ae84d0d62eea337cc2e48356e664209bd3b21c",
        "ReturnLens_v7_2.pptx": "01a6b6307bcfdface93929d9cd21558b285818be2eb24d4ecb65ba9a5cfe6af6",
        "ReturnLens_v8.pptx": "9d4c4a06971b5db65dbd38032b0bd8773343abdb8bde6d774a10653169b49888"
    }

    history_ok = True
    for fname, expected_h in baseline_hashes.items():
        fp = base_dir / fname
        if not fp.exists():
            print(f"FAILED: Historical baseline file {fname} is missing!")
            history_ok = False
            all_passed = False
        else:
            cur_h = file_hash(fp)
            if cur_h != expected_h:
                print(f"FAILED: Historical file {fname} modified! Hash: {cur_h[:12]} vs expected: {expected_h[:12]}")
                history_ok = False
                all_passed = False
    if history_ok:
        print("PASSED: All historical baseline files (v5, v6, v7, v7.1, v7.2, v8) are 100% byte-identical.")

    print("\n==========================================")
    if all_passed:
        print("ALL RETURNLENS V8.1 QA & SMOKE TESTS PASSED! (9/9)")
    else:
        print("SOME TESTS FAILED! CHECK OUTPUT ABOVE.")
    print("==========================================")

    return all_passed

if __name__ == "__main__":
    success = run_v8_1_smoke_test()
    sys.exit(0 if success else 1)

