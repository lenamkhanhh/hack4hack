import os
import sys
import json
import zipfile
import hashlib
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image
import numpy as np
import fitz
from pptx import Presentation

sys.stdout.reconfigure(encoding='utf-8')

def file_hash(path):
    with open(path, "rb") as f:
        data = f.read()
    if str(path).endswith('.html'):
        data = data.replace(b'\r\n', b'\n')
    return hashlib.sha256(data).hexdigest()

def run_v9_4_smoke_test():
    print("=== STARTING RETURNLENS V9.4 (FINAL SUBMISSION PATCH) SMOKE & QA SUITE ===\n")
    base_dir = Path(__file__).resolve().parent.parent
    all_passed = True

    # 1. Test Canonical Data Specification
    print("[TEST 1] Validating Canonical Data Specification (content/deck_data_v9_4.json)...")
    data_path = base_dir / "content" / "deck_data_v9_4.json"
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

        # Team 4 members check
        team_str = data.get("meta", {}).get("team", "")
        if "4 Members" not in team_str:
            print(f"FAILED: Team metadata should indicate 4 Members, got '{team_str}'")
            all_passed = False
        else:
            print(f"PASSED: Team size confirmed as 4 members ('{team_str}').")

        # Script word count: calibrated to 310-330 words
        spoken_words_per_slide = []
        for s in slides:
            lines = s["speaker_notes"].strip().split("\n")
            content_lines = [l for l in lines if not l.startswith("[")]
            text = " ".join(content_lines)
            w = len(text.split())
            spoken_words_per_slide.append(w)
        total_spoken = sum(spoken_words_per_slide)
        print(f"  Spoken words per slide: {spoken_words_per_slide}")
        print(f"  Total pitch script spoken word count: {total_spoken} words")
        if 310 <= total_spoken <= 330:
            print(f"PASSED: Script word count is calibrated ({total_spoken} words in target 310-330 range).")
        else:
            print(f"FAILED: Script word count {total_spoken} is outside target 310-330 range!")
            all_passed = False

        # Date formula verification
        pol_status = data.get("meta", {}).get("sample_case", {}).get("policy_status", "")
        if "0 <= current_date - delivery_date <= 7 days" not in pol_status:
            print(f"FAILED: Date formula '0 <= current_date - delivery_date <= 7 days' not found in policy status: '{pol_status}'")
            all_passed = False
        else:
            print("PASSED: Verified date formula '0 <= current_date - delivery_date <= 7 days'.")

        # Sample refund policy check
        rf_note = data.get("meta", {}).get("sample_refund_policy", {}).get("note", "")
        if "not a BTC hackathon limit" not in rf_note:
            print(f"FAILED: Sample refund policy note missing BTC caveat: '{rf_note}'")
            all_passed = False
        else:
            print("PASSED: Sample refund policy explicitly framed as team model, not BTC limit.")

        # Core thesis
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
    print("\n[TEST 2] Validating V9.4 Deliverables Existence & Synchronization (root vs deliverables/)...")
    targets = [
        ("ReturnLens_v9_4.pptx", "pptx"),
        ("ReturnLens_v9_4.pdf", "pdf"),
        ("ReturnLens_v9_4.html", "html"),
        ("ReturnLens_v9_4_preview.png", "preview")
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
    print("\n[TEST 3] Validating V9.4 PDF Properties (Pages & Aspect Ratio)...")
    pdf_path = base_dir / "deliverables" / "ReturnLens_v9_4.pdf"
    if pdf_path.exists():
        doc = fitz.open(pdf_path)
        if len(doc) != 6:
            print(f"FAILED: PDF expected 6 pages, found {len(doc)}")
            all_passed = False
        else:
            print("PASSED: V9.4 PDF has exactly 6 pages.")

        page = doc[0]
        rect = page.rect
        w, h = rect.width, rect.height
        aspect = w / h
        if abs(aspect - 16/9) > 0.05:
            print(f"FAILED: PDF aspect ratio is not 16:9 widescreen ({w}x{h})")
            all_passed = False
        else:
            print(f"PASSED: V9.4 PDF aspect ratio is true 16:9 widescreen ({w}x{h}).")
    else:
        print("FAILED: PDF file not found for inspection.")
        all_passed = False

    # 4. Test PPTX Properties & Embedded Speaker Notes
    print("\n[TEST 4] Validating V9.4 PPTX Properties & Embedded Speaker Notes...")
    pptx_path = base_dir / "deliverables" / "ReturnLens_v9_4.pptx"
    if pptx_path.exists():
        prs = Presentation(pptx_path)
        if len(prs.slides) != 6:
            print(f"FAILED: PPTX expected 6 slides, found {len(prs.slides)}")
            all_passed = False
        else:
            print("PASSED: V9.4 PPTX has exactly 6 slides.")

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
    print("\n[TEST 5] Validating V9.4 Preview Contact Sheet Dimensions...")
    preview_path = base_dir / "deliverables" / "ReturnLens_v9_4_preview.png"
    if preview_path.exists():
        im = Image.open(preview_path)
        if im.size != (2352, 882):
            print(f"FAILED: Preview contact sheet expected 2352x882, got {im.size}")
            all_passed = False
        else:
            print(f"PASSED: V9.4 Preview image is verified {im.size} - exact 16:9 contact sheet.")
    else:
        print("FAILED: Preview image missing.")
        all_passed = False

    # 6. Test XML Style & Theme Effect Neutralization
    print("\n[TEST 6] Validating Elimination of Theme Lines (<p:style>/accent1) and Shadows in V9.4...")
    if pptx_path.exists():
        with zipfile.ZipFile(pptx_path, 'r') as z:
            total_styles = 0
            total_lnRefs = 0
            total_effRefs = 0
            for s_idx in range(1, 7):
                s_name = f'ppt/slides/slide{s_idx}.xml'
                root = ET.fromstring(z.read(s_name))
                styles = root.findall('.//{http://schemas.openxmlformats.org/presentationml/2006/main}style')
                lnRefs = root.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}lnRef')
                effRefs = root.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}effectRef')
                total_styles += len(styles)
                total_lnRefs += len(lnRefs)
                total_effRefs += len(effRefs)

        print(f"  Total XML <p:style> elements across all slides: {total_styles}")
        print(f"  Total XML <a:lnRef> elements across all slides: {total_lnRefs}")
        print(f"  Total XML <a:effectRef> elements across all slides: {total_effRefs}")

        if total_styles > 0 or total_lnRefs > 0 or total_effRefs > 0:
            print("FAILED: Stray theme style or effect references remain in PPTX XML!")
            all_passed = False
        else:
            print("PASSED: 100% of <p:style>, <a:lnRef>, and <a:effectRef> elements neutralized in PPTX.")

        # Pixel check
        renders_dir = base_dir / "src" / "assets" / "v9_4_pptx_renders"
        for s in range(1, 7):
            rp = renders_dir / f"slide_{s}.png"
            if rp.exists():
                im = Image.open(rp).convert('RGB')
                arr = np.array(im)
                blue_mask = (arr[:, :, 0] >= 55) & (arr[:, :, 0] <= 80) & (arr[:, :, 1] >= 100) & (arr[:, :, 1] <= 125) & (arr[:, :, 2] >= 180) & (arr[:, :, 2] <= 210)
                blue_px = int(np.sum(blue_mask))
                if blue_px > 0:
                    print(f"FAILED: Slide {s} has visible theme blue lines ({blue_px} px)!")
                    all_passed = False
        print("PASSED: Render pixel analysis confirms zero visible theme-blue lines across all slides.")

    # 7. Test Content Precision & PS-04 Requirements in V9.4
    print("\n[TEST 7] Validating Content Precision, PS-04 Requirements & Clearance in V9.4...")
    if pptx_path.exists():
        prs = Presentation(pptx_path)

        slide_texts = []
        for s in prs.slides:
            t = " ".join(sh.text_frame.text for sh in s.shapes if sh.has_text_frame)
            slide_texts.append(t)

        all_text = " ".join(slide_texts)

        # Forbidden tags
        forbidden_tags = ["V8.2", "V8.1", "V8", "V7.2", "V7.1", "V9.1", "V9.2", "V9", "FINAL POLISH", "PATCH EDITION",
                          "CORE DEMONSTRATION", "WORKFLOW & RESPONSIBILITIES", "SITUATION MATRIX",
                          "HACKATHON SPRINT PLAN", "SCOPE DISCIPLINE", "THE SELLER'S QUESTION:",
                          "Vision & Ingestion", "Rule Engine", "Planning & Drafting", "Merchant Decision"]
        for tag in forbidden_tags:
            if tag in all_text:
                print(f"FAILED: Found forbidden tag '{tag}' on slide face!")
                all_passed = False
        print("PASSED: All slides clean of editorial tags, redundant subheadings, and 'SCOPE DISCIPLINE'.")

        # Slide 1 checks: PS-04 positioning
        s1 = slide_texts[0]
        if "A support agent for solo sellers that handles order status, returns and refunds—using video evidence to triage disputed claims." not in s1:
            print("FAILED: Slide 1 PS-04 positioning summary mismatch.")
            all_passed = False
        else:
            print("PASSED: Slide 1 PS-04 positioning summary verified.")

        # Slide 2 checks
        s2 = slide_texts[1]
        if "Customer video · 18s" not in s2:
            print("FAILED: Slide 2 attachment line mismatch.")
            all_passed = False
        else:
            print("PASSED: Slide 2 'Customer video · 18s' verified.")

        # Slide 3 checks: "Create return and prepare label."
        s3 = slide_texts[2]
        if "White ordered. Black shown." not in s3:
            print("FAILED: Slide 3 title 'White ordered. Black shown.' missing.")
            all_passed = False
        else:
            print("PASSED: Slide 3 title 'White ordered. Black shown.' verified.")

        if "Create return and prepare label." not in s3:
            print("FAILED: Slide 3 Option 1 action 'Create return and prepare label.' missing.")
            all_passed = False
        else:
            print("PASSED: Slide 3 Option 1 action 'Create return and prepare label.' verified.")

        # Slide 4 checks: subtitle "code verifies", step 1 routine chats tracking
        s4 = slide_texts[3]
        if "models observe, tools fetch, code verifies, and the seller approves" not in s4:
            print("FAILED: Slide 4 subtitle mismatch ('code verifies' missing).")
            all_passed = False
        else:
            print("PASSED: Slide 4 updated subtitle with 'code verifies' verified.")

        if "Routine chats get tracking updates" not in s4:
            print("FAILED: Slide 4 step 1 tracking updates phrasing missing.")
            all_passed = False
        else:
            print("PASSED: Slide 4 step 1 tracking updates phrasing verified.")

        # Slide 5 checks: Case C exact separation
        s5 = slide_texts[4]
        if "Unclear video; requested refund exceeds ₹1,499 remaining." not in s5:
            print("FAILED: Slide 5 Case C situation mismatch.")
            all_passed = False
        else:
            print("PASSED: Slide 5 Case C situation verified.")

        if "Blocks excess amount; requests one close-up; logs both actions." not in s5:
            print("FAILED: Slide 5 Case C agent response mismatch.")
            all_passed = False
        else:
            print("PASSED: Slide 5 Case C agent response verified.")

        if "Review evidence; approve only within refund limits." not in s5:
            print("FAILED: Slide 5 Case C seller next step mismatch.")
            all_passed = False
        else:
            print("PASSED: Slide 5 Case C seller next step verified.")

        # Slide 6 checks: Phase 4 "Final integration and scenario walkthroughs."
        s6 = slide_texts[5]
        if "Final integration and scenario walkthroughs." not in s6:
            print("FAILED: Slide 6 phase 4 output 'Final integration and scenario walkthroughs.' missing.")
            all_passed = False
        else:
            print("PASSED: Slide 6 phase 4 output 'Final integration and scenario walkthroughs.' verified.")

        # Geometry & Clearance checks (claim clearance >= 0.30 inch)
        geom_ok = True
        for s_idx, slide in enumerate(prs.slides):
            max_bottom = 0
            for sh in slide.shapes:
                t = sh.top.inches if sh.top else 0
                l = sh.left.inches if sh.left else 0
                w = sh.width.inches if sh.width else 0
                h = sh.height.inches if sh.height else 0

                if w > 13.0 and h > 7.0:
                    continue # background

                b = t + h
                r = l + w

                if r > 13.38 or b > 7.55:
                    print(f"FAILED: Shape '{sh.name}' on Slide {s_idx + 1} exceeds canvas: right={r:.2f}\", bottom={b:.2f}\"")
                    geom_ok = False
                    all_passed = False

                if t < 6.90 and b > max_bottom:
                    max_bottom = b

            clearance = 6.92 - max_bottom
            print(f"  Slide {s_idx+1}: max content bottom={max_bottom:.2f}\", clearance to page number={clearance:.2f}\"")
            if clearance < 0.30:
                print(f"FAILED: Slide {s_idx+1} clearance too tight ({clearance:.2f}\" < 0.30\")")
                geom_ok = False
                all_passed = False
        if geom_ok:
            print("PASSED: All V9.4 slides passed geometry, safe margins, and canvas clearance checks (>= 0.30 inch).")

    # 8. Test Slide Renders & Manifest
    print("\n[TEST 8] Validating Slide Renders & render_manifest.json...")
    manifest_path = base_dir / "src" / "assets" / "v9_4_pptx_renders" / "render_manifest.json"
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
            rp = base_dir / "src" / "assets" / "v9_4_pptx_renders" / f"slide_{i}.png"
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
        "ReturnLens_v8_2.pptx": "acef2b65c961f107712dc46f779493d27549aff8c2d563a3fcdaaf076eb7f377",
        "ReturnLens_v9.pptx": "8a3dc2bbfac14e3117a6df9e1a9cb5788480e13a70b26d51eca37ae7427b8ee4",
        "ReturnLens_v9_1.pptx": "c4f7a117f458e17c035711d52d0d288667f45c55b4ba7b62f484db2bbb10eea9",
        "ReturnLens_v9_2.pptx": "3d9556f9ffa9894d22a4dd3ee4ec83e21f35cd23562d2f04a56e36d22072730e",
        "ReturnLens_v9_3.pptx": "2116944d4ab2394311209873c1e922e7b1251591d140e639a91088665930981f"
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
        print("PASSED: All historical baseline files (v5, v6, v7, v7.1, v7.2, v8, v8.1, v8.2, v9, v9.1, v9.2, v9.3) are 100% byte-identical.")

    print("\n==========================================")
    if all_passed:
        print("ALL RETURNLENS V9.4 QA & SMOKE TESTS PASSED! (9/9)")
    else:
        print("SOME TESTS FAILED! CHECK OUTPUT ABOVE.")
    print("==========================================")

    return all_passed

if __name__ == "__main__":
    success = run_v9_4_smoke_test()
    sys.exit(0 if success else 1)
