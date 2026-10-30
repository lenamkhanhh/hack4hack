import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs(r"D:\Code\Code\AIO\Code\ZaloAIC\assets_v3", exist_ok=True)

# 1. White Headphone Product Graphic (for Store API Order Truth)
def generate_white_headphone():
    w, h = 600, 420
    im = Image.new("RGBA", (w, h), (245, 243, 239, 255))
    d = ImageDraw.Draw(im)

    # Soft subtle pedestal
    d.ellipse([140, 340, 460, 390], fill=(225, 222, 215, 255))

    # Headband arc (White / Silver with subtle outline)
    d.arc([160, 70, 440, 310], start=180, end=0, fill=(210, 210, 210, 255), width=28)
    d.arc([162, 72, 438, 308], start=180, end=0, fill=(255, 255, 255, 255), width=24)

    # Left Ear Cup (White)
    d.rounded_rectangle([130, 180, 210, 330], radius=38, fill=(255, 255, 255, 255), outline=(190, 190, 190, 255), width=3)
    d.rounded_rectangle([145, 195, 195, 315], radius=24, fill=(240, 240, 240, 255))

    # Right Ear Cup (White)
    d.rounded_rectangle([390, 180, 470, 330], radius=38, fill=(255, 255, 255, 255), outline=(190, 190, 190, 255), width=3)
    d.rounded_rectangle([405, 195, 455, 315], radius=24, fill=(240, 240, 240, 255))

    # Label text overlay
    d.text((20, 20), "SKU: HEAD-WHT-02 (White)", fill=(100, 110, 105, 255))
    
    im.save(r"D:\Code\Code\AIO\Code\ZaloAIC\assets_v3\product_white_headphones.png", "PNG")
    print("Saved product_white_headphones.png")

# 2. Black Headphone Video Frame Graphic (for Video Evidence Frame 00:07)
def generate_black_headphone_frame():
    w, h = 600, 420
    im = Image.new("RGBA", (w, h), (20, 24, 22, 255))
    d = ImageDraw.Draw(im)

    # Video noise / background subtle table
    d.rectangle([0, 280, 600, 420], fill=(28, 32, 30, 255))

    # Headband arc (Matte Black with dark silver highlight)
    d.arc([160, 70, 440, 310], start=180, end=0, fill=(70, 75, 72, 255), width=28)
    d.arc([162, 72, 438, 308], start=180, end=0, fill=(35, 38, 36, 255), width=24)

    # Left Ear Cup (Matte Charcoal Black)
    d.rounded_rectangle([130, 180, 210, 330], radius=38, fill=(30, 33, 31, 255), outline=(60, 65, 62, 255), width=3)
    d.rounded_rectangle([145, 195, 195, 315], radius=24, fill=(22, 24, 23, 255))

    # Right Ear Cup (Matte Charcoal Black)
    d.rounded_rectangle([390, 180, 470, 330], radius=38, fill=(30, 33, 31, 255), outline=(60, 65, 62, 255), width=3)
    d.rounded_rectangle([405, 195, 455, 315], radius=24, fill=(22, 24, 23, 255))

    # Red/Amber discrepancy indicator box over ear cup
    d.rectangle([115, 165, 225, 345], outline=(216, 140, 49, 255), width=2)

    # Video timecode overlay
    d.rectangle([16, 16, 175, 44], fill=(0, 0, 0, 200))
    d.text((24, 22), "REC [00:07 / 00:32]", fill=(240, 240, 240, 255))

    d.rectangle([16, h - 44, 220, h - 16], fill=(0, 0, 0, 200))
    d.text((24, h - 38), "OBSERVED COLOR: BLACK", fill=(216, 140, 49, 255))

    im.save(r"D:\Code\Code\AIO\Code\ZaloAIC\assets_v3\video_frame_black_headphones.png", "PNG")
    print("Saved video_frame_black_headphones.png")

generate_white_headphone()
generate_black_headphone_frame()

