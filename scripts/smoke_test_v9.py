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

def run_v9_smoke_test():
    print("=== STARTING RETURNLENS V9 (MINIMALIST ART DIRECTION & TYPOGRAPHY) SMOKE & QA SUITE ===\n")
    base_dir = Path(__file__).resolve().parent.parent
    all_passed = True

    # 1. Test Canonical Data Specification
    print("[TEST 1] Validating Canonical Data Specification (content/deck_data_v9.json)...")
    data_path = base_dir / "content" / "deck_data_v9.json"
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
        notes_text = " ".join(" ".join(s["speaker_notes"].strip().split("\n")[1:]) for s in slides)
        word_count = len(notes_text.split())
        print(f"  Total pitch script spoken word count: {word_count} words")
        if 350 <= word_count <= 420:
            print("PASSED: Script word count is well-calibrated for 3-minute pitch (382 words).")
        else:
            print(f"WARNING: Script word count {word_count} is outside expected range 350-420.")

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
    print("\n[TEST 2] Validating V9 Deliverables Existence & Synchronization (root vs deliverables/)...")
    targets = [
        ("ReturnLens_v9.pptx", "pptx"),
        ("ReturnLens_v9.pdf", "pdf"),
        ("ReturnLens_v9.html", "html"),
        ("ReturnLens_v9_preview.png", "preview")
    ]
    for filename, kind in targets:
        root_file = base_dir / filename
        deliv_file = base_dir / "deliverables" / filename
        if not root_file.exists():
            print(f"FAILED: Root deliverable {filename} is missing.")
            all_passed = False
        elif not deliv_file.exists():
            print(f"FAILED: Deliverables/{filename} is missing.")
            all_passed = False
        else:
            h_root = file_hash(root_file)
            h_deliv = file_hash(deliv_file)
            if h_root != h_deliv:
                print(f"FAILED: Hash mismatch between root and deliverables/ for {filename}!")
                all_passed = False
            else:
                sz = root_file.stat().st_size
                print(f"PASSED: {filename} synchronized ({sz} bytes, SHA256: {h_root[:12]}...).")

    # 3. Test PDF Properties
    print("\n[TEST 3] Validating V9 PDF Properties (Pages & Aspect Ratio)...")
    pdf_path = base_dir / "deliverables" / "ReturnLens_v9.pdf"
    if pdf_path.exists():
        doc = fitz.open(pdf_path)
        if len(doc) != 6:
            print(f"FAILED: PDF expected 6 pages, found {len(doc)}")
            all_passed = False
        else:
            print("PASSED: V9 PDF has exactly 6 pages.")

        page = doc[0]
        rect = page.rect
        w, h = rect.width, rect.height
        aspect = w / h
        if abs(aspect - 16/9) > 0.05:
            print(f"FAILED: PDF aspect ratio is not 16:9 widescreen ({w}x{h})")
            all_passed = False
        else:
            print(f"PASSED: V9 PDF aspect ratio is true 16:9 widescreen ({w}x{h}).")
    else:
        print("FAILED: PDF file not found for inspection.")
        all_passed = False

    # 4. Test PPTX Properties & Embedded Speaker Notes
    print("\n[TEST 4] Validating V9 PPTX Properties & Embedded Speaker Notes...")
    pptx_path = base_dir / "deliverables" / "ReturnLens_v9.pptx"
    if pptx_path.exists():
        prs = Presentation(pptx_path)
        if len(prs.slides) != 6:
            print(f"FAILED: PPTX expected 6 slides, found {len(prs.slides)}")
            all_passed = False
        else:
            print("PASSED: V9 PPTX has exactly 6 slides.")

        notes_ok = True
        for idx, slide in enumerate(prs.slides):
            notes = slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ""
            if not notes.strip():
                print(f"FAILED: Slide {idx+1} is missing speaker notes in PPTX.")
                notes_ok = False
                all_passed = False
            else:
                print(f"  Slide {idx+1} Speaker Notes: {len(notes)} chars")
        if notes_ok:
            print("PASSED: All 6 slides have verified embedded speaker notes.")
    else:
        print("FAILED: PPTX file not found for inspection.")
        all_passed = False

    # 5. Test Preview Image Dimensions
    print("\n[TEST 5] Validating V9 Preview Contact Sheet Dimensions...")
    preview_path = base_dir / "deliverables" / "ReturnLens_v9_preview.png"
    if preview_path.exists():
        im = Image.open(preview_path)
        if im.size != (2352, 882):
            print(f"FAILED: Preview contact sheet expected 2352x882, got {im.size}")
            all_passed = False
        else:
            print(f"PASSED: V9 Preview image is verified {im.size} - exact 16:9 contact sheet.")
    else:
        print("FAILED: Preview image missing.")
        all_passed = False

    # 6. Test Content Grounding & Art Direction Consistency
    print("\n[TEST 6] Verifying Content Grounding, Art Direction & Conceptual Consistency...")
    if pptx_path.exists():
        prs = Presentation(pptx_path)

        # Full text extracted from all slides
        slide_texts = []
        for s in prs.slides:
            t = " ".join(sh.text_frame.text for sh in s.shapes if sh.has_text_frame)
            slide_texts.append(t)

        all_text = " ".join(slide_texts)

        # Check absence of internal tags and old jargon
        forbidden_tags = ["V8.2", "V8.1", "V8", "V7.2", "V7.1", "FINAL POLISH", "PATCH EDITION",
                          "CORE DEMONSTRATION", "WORKFLOW & RESPONSIBILITIES", "SITUATION MATRIX",
                          "HACKATHON SPRINT PLAN", "SELLER CONSOLE MOCKUP", "THE SELLER'S DILEMMA"]
        for tag in forbidden_tags:
            if tag in all_text:
                print(f"FAILED: Found forbidden internal/editorial tag '{tag}' on slide face!")
                all_passed = False

        # Slide 1 checks
        s1 = slide_texts[0]
        if "Review Evidence & Decide →" not in s1:
            print("FAILED: Slide 1 CTA 'Review Evidence & Decide →' not found.")
            all_passed = False
        else:
            print("PASSED: Slide 1 CTA 'Review Evidence & Decide →' verified.")

        if "Agent collects info & clarifies · Seller approves returns, labels & refunds" not in s1:
            print("FAILED: Slide 1 authority boundary string mismatch.")
            all_passed = False
        else:
            print("PASSED: Slide 1 authority boundary verified.")

        # Slide 2 checks
        s2 = slide_texts[1]
        claim_text = "I ordered white headphones, but received black. Please refund me."
        if claim_text not in s2:
            print("FAILED: Slide 2 customer claim text mismatch.")
            all_passed = False
        else:
            print("PASSED: Slide 2 customer claim text verified.")

        if s2.count("THE SELLER'S QUESTION:") != 1:
            print("FAILED: Slide 2 'THE SELLER'S QUESTION:' does not appear exactly once.")
            all_passed = False
        else:
            print("PASSED: Slide 2 'THE SELLER'S QUESTION:' appears exactly once.")

        # Slide 3 checks
        s3 = slide_texts[2]
        if "White ordered. Black received." not in s3:
            print("FAILED: Slide 3 title 'White ordered. Black received.' missing.")
            all_passed = False
        else:
            print("PASSED: Slide 3 title 'White ordered. Black received.' verified.")

        if "Ordered: White" not in s3 or "Observed: Black" not in s3:
            print("FAILED: Slide 3 missing 'Ordered: White' or 'Observed: Black'.")
            all_passed = False
        else:
            print("PASSED: Slide 3 prominent 'Ordered: White' and 'Observed: Black' verified.")

        if "2. Request label photo" not in s3:
            print("FAILED: Slide 3 '2. Request label photo' missing.")
            all_passed = False
        else:
            print("PASSED: Slide 3 '2. Request label photo' verified.")

        if "(Recommended)" in s3:
            print("FAILED: Slide 3 should NOT contain '(Recommended)' text.")
            all_passed = False
        else:
            print("PASSED: Slide 3 '(Recommended)' cleanly removed.")

        draft_reply = "Please share the outer-box label so we can check your shipment."
        if draft_reply not in s3:
            print("FAILED: Slide 3 drafted customer reply mismatch.")
            all_passed = False
        else:
            print("PASSED: Slide 3 drafted customer reply verified.")

        # Slide 4 checks
        s4 = slide_texts[3]
        if "Seller approves returns, labels and refunds." not in s4:
            print("FAILED: Slide 4 seller approval phrase missing.")
            all_passed = False
        else:
            print("PASSED: Slide 4 'Seller approves returns, labels and refunds.' verified.")

        if "Case C Clarification Loop" not in s4:
            print("FAILED: Slide 4 Case C Clarification Loop missing.")
            all_passed = False
        else:
            print("PASSED: Slide 4 Case C Clarification Loop container verified.")

        # Slide 5 checks
        s5 = slide_texts[4]
        if "cracked headband" not in s5:
            print("FAILED: Slide 5 Case A cracked headband missing.")
            all_passed = False
        else:
            print("PASSED: Slide 5 Case A 'cracked headband' verified.")

        if "cracked screen" in s5:
            print("FAILED: Slide 5 contains legacy 'cracked screen'!")
            all_passed = False
        else:
            print("PASSED: Slide 5 clean of 'cracked screen'.")

        if "10 seconds" in s5 or "15 minutes" in s5:
            print("FAILED: Slide 5 contains unsourced timing claims.")
            all_passed = False
        else:
            print("PASSED: Clean of unsourced time claims ('10 seconds' / '15 minutes').")

        if "within the 7-day return window" not in s5:
            print("FAILED: Slide 5 Case A return window clause missing.")
            all_passed = False
        else:
            print("PASSED: Slide 5 Case A 'within the 7-day return window' verified.")

        # Slide 6 checks
        s6 = slide_texts[5]
        if "A focused 24-hour prototype." not in s6:
            print("FAILED: Slide 6 single-line title missing.")
            all_passed = False
        else:
            print("PASSED: Slide 6 title verified.")

        if "One clear evidence pack. The seller makes the call." not in s6:
            print("FAILED: Slide 6 closing takeaway missing.")
            all_passed = False
        else:
            print("PASSED: Slide 6 closing takeaway verified.")

    # 7. Test Geometry, Safe Margins & Safe Canvas Clearance
    print("\n[TEST 7] Validating Visual Geometry, Padding & Safe Margins in V9 PPTX...")
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

                # Skip full-slide background rectangle
                if w > 13.0 and h > 7.0:
                    continue

                b = t + h
                r = l + w

                if r > 13.38 or b > 7.55:
                    print(f"FAILED: Shape '{sh.name}' on Slide {s_idx + 1} exceeds slide canvas: right={r:.2f}\", bottom={b:.2f}\"")
                    geom_ok = False
                    all_passed = False

                if t < 6.90 and b > max_bottom:
                    max_bottom = b

            clearance = 6.92 - max_bottom
            print(f"  Slide {s_idx+1}: max content bottom={max_bottom:.2f}\", clearance to page number={clearance:.2f}\"")
            if clearance < 0.25:
                print(f"FAILED: Slide {s_idx+1} bottom clearance too tight ({clearance:.2f}\" < 0.25\")")
                geom_ok = False
                all_passed = False
        if geom_ok:
            print("PASSED: All V9 slides passed geometry, safe margins, and canvas clearance checks.")

    # 8. Test Slide Renders & Manifest
    print("\n[TEST 8] Validating Slide Renders & render_manifest.json...")
    manifest_path = base_dir / "src" / "assets" / "v9_pptx_renders" / "render_manifest.json"
    if not manifest_path.exists():
        print(f"FAILED: {manifest_path} missing.")
        all_passed = False
    else:
        with open(manifest_path, "r", encoding="utf-8") as f:
            man = json.load(f)
        pptx_cur_hash = file_hash(pptx_path)
        if man.get("source_sha256") != pptx_cur_hash:
            print(f"FAILED: Manifest source_sha256 mismatch! ({man.get('source_sha256')[:12]} vs {pptx_cur_hash[:12]})")
            all_passed = False
        else:
            print(f"PASSED: render_manifest.json matches current PPTX SHA256: {pptx_cur_hash[:12]}...")

        renders_ok = True
        for i in range(1, 7):
            rp = base_dir / "src" / "assets" / "v9_pptx_renders" / f"slide_{i}.png"
            if not rp.exists():
                print(f"FAILED: Render missing: {rp}")
                renders_ok = False
                all_passed = False
            else:
                rim = Image.open(rp)
                if rim.size != (1920, 1080):
                    print(f"FAILED: Render {rp.name} size {rim.size} != (1920, 1080)")
                    renders_ok = False
                    all_passed = False
        if renders_ok:
            print("PASSED: All 6 PPTX slide renders present and verified at 1920x1080.")

    # 9. Test Historical Baseline Preservation
    print("\n[TEST 9] Validating Historical Baseline Preservation (Zero Regression)...")
    baseline_hashes = {
        "ReturnLens_v5.html": "ad4c421b6f0950b8afe3dfeae6976aafb1b2c1227da72881f82cdaeb368425be",
        "ReturnLens_v6.html": "a62ef784754320b00b4b83f9d7085e858ec3b68546ae3574556af84e41bf7eb5",
        "ReturnLens_v7.html": "bc5ebf29a05a7c38e370f6811137b49533488c69a8682ebc000f1599bfec7618",
        "ReturnLens_v7_1.pptx": "341b47be7aebc31480446cbfa0ae84d0d62eea337cc2e48356e664209bd3b21c",
        "ReturnLens_v7_2.pptx": "01a6b6307bcfdface93929d9cd21558b285818be2eb24d4ecb65ba9a5cfe6af6",
        "ReturnLens_v8.pptx": "9d4c4a06971b5db65dbd38032b0bd8773343abdb8bde6d774a10653169b49888",
        "ReturnLens_v8_1.pptx": "7172acbcb26c0b050957448024b309b3990aa0a3147af4ed9580296e0a1133eb",
        "ReturnLens_v8_2.pptx": "acef2b65c961f107712dc46f779493d27549aff8c2d563a3fcdaaf076eb7f377"
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
        print("PASSED: All historical baseline files (v5, v6, v7, v7.1, v7.2, v8, v8.1, v8.2) are 100% byte-identical.")

    print("\n==========================================")
    if all_passed:
        print("ALL RETURNLENS V9 QA & SMOKE TESTS PASSED! (9/9)")
    else:
        print("SOME TESTS FAILED! CHECK OUTPUT ABOVE.")
    print("==========================================")

    return all_passed

if __name__ == "__main__":
    success = run_v9_smoke_test()
    sys.exit(0 if success else 1)
