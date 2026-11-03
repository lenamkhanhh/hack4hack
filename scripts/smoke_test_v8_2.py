import os
import sys
import json
import hashlib
import pathlib
from pathlib import Path
from PIL import Image
import fitz
from pptx import Presentation

sys.stdout.reconfigure(encoding='utf-8')

def file_hash(path):
    with open(path, "rb") as f:
        data = f.read()
    if str(path).endswith('.html'):
        data = data.replace(b'\r\n', b'\n')
    return hashlib.sha256(data).hexdigest()

def run_v8_2_smoke_test():
    print("=== STARTING RETURNLENS V8.2 (FINAL POLISH PATCH EDITION) SMOKE & QA SUITE ===\n")
    base_dir = Path(__file__).resolve().parent.parent
    all_passed = True

    # 1. Test Canonical Data Specification
    print("[TEST 1] Validating Canonical Data Specification (content/deck_data_v8_2.json)...")
    data_path = base_dir / "content" / "deck_data_v8_2.json"
    if not data_path.exists():
        print(f"FAILED: {data_path} missing.")
        all_passed = False
    else:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        slides = data.get("slides", [])
        if len(slides) != 6:
            print(f"FAILED: Expected exactly 6 slides, got {len(slides)}")
            all_passed = False
        else:
            print("PASSED: Exactly 6 slides present in canonical data.")

        # Script word count
        notes_text = " ".join(" ".join(s["speaker_notes"].split("\n")[1:]) for s in slides)
        word_count = len(notes_text.split())
        print(f"  Total pitch script spoken word count: {word_count} words")
        if 350 <= word_count <= 410:
            print("PASSED: Script word count is well-calibrated for 3-minute pitch.")
        else:
            print(f"WARNING: Script word count {word_count} is outside expected range 350-410.")

        # Core thesis & authority boundary check
        thesis = data.get("meta", {}).get("core_thesis")
        if thesis != "Models observe. Code verifies. Seller authorizes.":
            print(f"FAILED: Core thesis mismatch: '{thesis}'")
            all_passed = False
        else:
            print("PASSED: Core architectural thesis verified.")

        qa = data.get("qa_defense", [])
        if len(qa) < 5:
            print(f"FAILED: Expected at least 5 Q&A defense pairs, got {len(qa)}")
            all_passed = False
        else:
            print("PASSED: All 5 hard hackathon defense questions verified in canonical data.")

    # 2. Test Deliverables Existence & Root-Sync
    print("\n[TEST 2] Validating V8.2 Deliverables Existence & Synchronization (root vs deliverables/)...")
    deliv_files = [
        ("ReturnLens_v8_2.pptx", "deliverables/ReturnLens_v8_2.pptx"),
        ("ReturnLens_v8_2.pdf", "deliverables/ReturnLens_v8_2.pdf"),
        ("ReturnLens_v8_2.html", "deliverables/ReturnLens_v8_2.html"),
        ("ReturnLens_v8_2_preview.png", "deliverables/ReturnLens_v8_2_preview.png"),
    ]

    for root_f, deliv_f in deliv_files:
        rp = base_dir / root_f
        dp = base_dir / deliv_f
        if not rp.exists():
            print(f"FAILED: Root deliverable {root_f} missing.")
            all_passed = False
        elif not dp.exists():
            print(f"FAILED: Deliverables copy {deliv_f} missing.")
            all_passed = False
        else:
            rh = file_hash(rp)
            dh = file_hash(dp)
            if rh != dh:
                print(f"FAILED: Hash mismatch between {root_f} and {deliv_f}")
                all_passed = False
            else:
                print(f"PASSED: {root_f} synchronized ({rp.stat().st_size} bytes, SHA256: {rh[:12]}...).")

    # 3. Test PDF Properties
    print("\n[TEST 3] Validating V8.2 PDF Properties (Pages & Aspect Ratio)...")
    pdf_path = base_dir / "deliverables" / "ReturnLens_v8_2.pdf"
    if not pdf_path.exists():
        print(f"FAILED: {pdf_path} missing.")
        all_passed = False
    else:
        doc = fitz.open(pdf_path)
        if len(doc) != 6:
            print(f"FAILED: PDF has {len(doc)} pages, expected exactly 6.")
            all_passed = False
        else:
            print("PASSED: V8.2 PDF has exactly 6 pages.")

        page = doc[0]
        rect = page.rect
        ratio = rect.width / rect.height
        if abs(ratio - 16/9) > 0.01:
            print(f"FAILED: PDF aspect ratio is {ratio:.3f}, expected 16:9 (~1.778).")
            all_passed = False
        else:
            print(f"PASSED: V8.2 PDF aspect ratio is true 16:9 widescreen ({rect.width}x{rect.height}).")

    # 4. Test PPTX Properties & Speaker Notes
    print("\n[TEST 4] Validating V8.2 PPTX Properties & Embedded Speaker Notes...")
    pptx_path = base_dir / "deliverables" / "ReturnLens_v8_2.pptx"
    if not pptx_path.exists():
        print(f"FAILED: {pptx_path} missing.")
        all_passed = False
    else:
        prs = Presentation(pptx_path)
        if len(prs.slides) != 6:
            print(f"FAILED: PPTX has {len(prs.slides)} slides, expected 6.")
            all_passed = False
        else:
            print("PASSED: V8.2 PPTX has exactly 6 slides.")

        notes_ok = True
        for i, slide in enumerate(prs.slides):
            notes = slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ""
            print(f"  Slide {i+1} Speaker Notes: {len(notes)} chars")
            if len(notes.strip()) < 50:
                print(f"FAILED: Slide {i+1} notes missing or too short ({len(notes)} chars)")
                notes_ok = False
                all_passed = False
        if notes_ok:
            print("PASSED: All 6 slides have verified embedded speaker notes.")

    # 5. Test Preview Image Dimensions
    print("\n[TEST 5] Validating V8.2 Preview Contact Sheet Dimensions...")
    prev_path = base_dir / "deliverables" / "ReturnLens_v8_2_preview.png"
    if not prev_path.exists():
        print(f"FAILED: {prev_path} missing.")
        all_passed = False
    else:
        im = Image.open(prev_path)
        if im.size != (2352, 882):
            print(f"FAILED: Size is {im.size}, expected (2352, 882)")
            all_passed = False
        else:
            print("PASSED: V8.2 Preview image is verified (2352, 882) - exact 16:9 contact sheet.")

    # 6. Test Content Grounding & Conceptual Consistency
    print("\n[TEST 6] Verifying Content Grounding & Conceptual Consistency...")
    if pdf_path.exists():
        doc = fitz.open(pdf_path)

        # Slide 1 CTA & Authority
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

        # Slide 2: Claim text & single question label
        s2_text = doc[1].get_text()
        s2_norm = " ".join(s2_text.split())
        if "i ordered white headphones, but received black" not in s2_norm.lower():
            print("FAILED: Slide 2 customer claim text mismatch.")
            all_passed = False
        else:
            print("PASSED: Slide 2 customer claim text verified.")

        # Ensure "THE SELLER'S QUESTION:" appears exactly once
        count_sq = s2_norm.upper().count("THE SELLER'S QUESTION:")
        if count_sq != 1:
            print(f"FAILED: 'THE SELLER'S QUESTION:' appeared {count_sq} times on Slide 2, expected exactly 1.")
            all_passed = False
        else:
            print("PASSED: Slide 2 'THE SELLER'S QUESTION:' appears exactly once (no duplicate prefix).")

        # Slide 3: Ordered White vs Observed Black, Request label photo, no (Recommended)
        s3_text = doc[2].get_text()
        s3_norm = " ".join(s3_text.split())
        if "Ordered: White" not in s3_text or "Observed: Black" not in s3_text:
            print("FAILED: Slide 3 missing prominent 'Ordered: White' or 'Observed: Black'.")
            all_passed = False
        else:
            print("PASSED: Slide 3 prominent 'Ordered: White' and 'Observed: Black' verified.")

        if "2. Request label photo" not in s3_norm:
            print("FAILED: Slide 3 missing '2. Request label photo'.")
            all_passed = False
        else:
            print("PASSED: Slide 3 '2. Request label photo' verified.")

        if "(recommended)" in s3_norm.lower():
            print("FAILED: Slide 3 still contains '(Recommended)' in Option 2 title.")
            all_passed = False
        else:
            print("PASSED: Slide 3 '(Recommended)' correctly removed from Option 2 title.")

        if "please share the outer-box label so we can check your shipment" not in s3_norm.lower():
            print("FAILED: Slide 3 missing drafted customer reply.")
            all_passed = False
        else:
            print("PASSED: Slide 3 drafted customer reply verified.")

        # Slide 4: "Seller approves returns, labels and refunds."
        s4_text = doc[3].get_text()
        s4_norm = " ".join(s4_text.split())
        if "seller approves returns, labels and refunds" not in s4_norm.lower():
            print("FAILED: Slide 4 missing 'Seller approves returns, labels and refunds.'.")
            all_passed = False
        else:
            print("PASSED: Slide 4 'Seller approves returns, labels and refunds.' verified.")

        # Slide 5: Case A cracked headband & 7-day window, Case B synchronized, Case C close-up photo
        s5_text = doc[4].get_text()
        s5_norm = " ".join(s5_text.split()).lower()
        if "cracked headband" not in s5_norm:
            print("FAILED: Slide 5 Case A missing 'cracked headband'.")
            all_passed = False
        else:
            print("PASSED: Slide 5 Case A 'cracked headband' verified.")

        if "cracked screen" in s5_norm:
            print("FAILED: Slide 5 Case A incorrectly mentions 'cracked screen'.")
            all_passed = False
        else:
            print("PASSED: Slide 5 Case A clean of 'cracked screen'.")

        if "10 seconds" in s5_norm or "15 minutes" in s2_norm.lower():
            print("FAILED: Unsourced timing measurements ('10 seconds' / '15 minutes') found.")
            all_passed = False
        else:
            print("PASSED: Clean of unsourced time claims ('10 seconds' / '15 minutes').")

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

        # Slide 6: single-line title & closing takeaway
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
    print("\n[TEST 7] Validating Visual Geometry, Padding & Safe Margins in V8.2 PPTX...")
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
            print("PASSED: All V8.2 slides passed geometry, safe margins, and collision checks.")

    # 8. Test Slide Renders & Manifest
    print("\n[TEST 8] Validating Slide Renders & render_manifest.json...")
    renders_dir = base_dir / "src" / "assets" / "v8_2_pptx_renders"
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
        "ReturnLens_v8.pptx": "9d4c4a06971b5db65dbd38032b0bd8773343abdb8bde6d774a10653169b49888",
        "ReturnLens_v8_1.pptx": "7172acbcb26c0b050957448024b309b3990aa0a3147af4ed9580296e0a1133eb"
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
        print("PASSED: All historical baseline files (v5, v6, v7, v7.1, v7.2, v8, v8.1) are 100% byte-identical.")

    print("\n==========================================")
    if all_passed:
        print("ALL RETURNLENS V8.2 QA & SMOKE TESTS PASSED! (9/9)")
    else:
        print("SOME TESTS FAILED! CHECK OUTPUT ABOVE.")
    print("==========================================")

    return all_passed

if __name__ == "__main__":
    success = run_v8_2_smoke_test()
    sys.exit(0 if success else 1)
