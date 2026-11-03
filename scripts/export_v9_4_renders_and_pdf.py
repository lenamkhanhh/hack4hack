import os
import sys
from pathlib import Path
import win32com.client

sys.stdout.reconfigure(encoding='utf-8')

def export_v9_4():
    base_dir = Path(__file__).resolve().parent.parent
    pptx_path = (base_dir / "deliverables" / "ReturnLens_v9_4.pptx").resolve()
    pdf_path = (base_dir / "deliverables" / "ReturnLens_v9_4.pdf").resolve()
    root_pdf = (base_dir / "ReturnLens_v9_4.pdf").resolve()
    renders_dir = (base_dir / "src" / "assets" / "v9_4_pptx_renders").resolve()
    renders_dir.mkdir(parents=True, exist_ok=True)

    print(f"Opening {pptx_path} with PowerPoint COM...")
    ppt = win32com.client.Dispatch("PowerPoint.Application")
    pres = ppt.Presentations.Open(str(pptx_path), WithWindow=False)

    print(f"Saving vector PDF to {pdf_path}...")
    pres.SaveAs(str(pdf_path), 32) # 32 = ppSaveAsPDF

    import shutil
    shutil.copy2(pdf_path, root_pdf)
    print(f"Copied PDF to root: {root_pdf}")

    print("Exporting slides to 1920x1080 PNGs...")
    for idx, slide in enumerate(pres.Slides):
        out_png = renders_dir / f"slide_{idx + 1}.png"
        slide.Export(str(out_png), "PNG", 1920, 1080)
        print(f"  Exported Slide {idx + 1} -> {out_png.name} ({out_png.stat().st_size} bytes)")

    pres.Close()
    ppt.Quit()
    print("PowerPoint export complete!")

if __name__ == "__main__":
    export_v9_4()
