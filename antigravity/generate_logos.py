#!/usr/bin/env python3
"""Generate professional placeholder agency logos for the Antigravity system."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os

LOGOS_DIR = Path(__file__).resolve().parent / "assets" / "logos"
LOGOS_DIR.mkdir(parents=True, exist_ok=True)

SIZE = 400

AGENCIES = {
    "spacex":    {"text": "SPACEX",    "bg": "#0B0D17", "fg": "#FFFFFF"},
    "esa":       {"text": "ESA",       "bg": "#003399", "fg": "#FFFFFF"},
    "cern":      {"text": "CERN",      "bg": "#003366", "fg": "#FFFFFF"},
    "darpa":     {"text": "DARPA",     "bg": "#1A1A2E", "fg": "#D4AF37"},
    "lockheed":  {"text": "LM",        "bg": "#1C1C1C", "fg": "#FFFFFF"},
    "blueorigin":{"text": "BLUE\nORIGIN","bg": "#0A1628","fg": "#4FC3F7"},
    "pentagon":  {"text": "DOD",       "bg": "#0D1117", "fg": "#C0C0C0"},
    "boeing":    {"text": "BOEING",    "bg": "#004B87", "fg": "#FFFFFF"},
    "northrop":  {"text": "NGC",       "bg": "#1A1A2E", "fg": "#FFFFFF"},
}

def generate_logos() -> None:
    """Generate simple fallback agency logos used on cards."""
    # We prefer bundled fonts first so renders are consistent in CI and local runs.
    font_path = None
    for fp in [
        str(Path(__file__).resolve().parent / "fonts" / "Oswald-Bold.ttf"),
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]:
        if os.path.exists(fp):
            font_path = fp
            break

    for name, style in AGENCIES.items():
        out_path = LOGOS_DIR / f"{name}.png"
        if out_path.exists():
            print(f"  Skipping {name} (already exists)")
            continue

        img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        margin = 10
        draw.ellipse([margin, margin, SIZE - margin, SIZE - margin], fill=style["bg"])

        font_size = 72 if len(style["text"]) <= 4 else 48
        try:
            font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()
        except OSError:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), style["text"], font=font, align="center")
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = (SIZE - text_w) // 2
        y = (SIZE - text_h) // 2

        draw.text((x, y), style["text"], fill=style["fg"], font=font, align="center")
        img.save(str(out_path), "PNG")
        print(f"  Generated {name}.png")

    print("Done!")


if __name__ == "__main__":
    generate_logos()
