"""Generate a simple app icon (PNG) for the Strava API application.

Fitness-data themed: a white heartbeat/pulse line on a warm orange gradient
with rounded corners. 512x512, transparent outside the rounded square.

Usage: python scripts/generate_strava_icon.py [output.png]
"""

from PIL import Image, ImageDraw
import sys

SIZE = 512
RADIUS = 96
TOP = (255, 107, 53)     # warm orange
BOTTOM = (247, 147, 30)  # amber


def build(output_path):
    # Vertical gradient
    grad = Image.new("RGB", (SIZE, SIZE))
    px = grad.load()
    for y in range(SIZE):
        t = y / (SIZE - 1)
        r = round(TOP[0] + (BOTTOM[0] - TOP[0]) * t)
        g = round(TOP[1] + (BOTTOM[1] - TOP[1]) * t)
        b = round(TOP[2] + (BOTTOM[2] - TOP[2]) * t)
        for x in range(SIZE):
            px[x, y] = (r, g, b)

    # Rounded-rectangle mask
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, SIZE - 1, SIZE - 1], radius=RADIUS, fill=255)

    icon = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    icon.paste(grad, (0, 0), mask)

    # Heartbeat / ECG pulse line
    draw = ImageDraw.Draw(icon)
    base = 280
    pulse = [
        (48, base), (150, base), (186, base), (206, 214), (226, base),
        (250, base), (268, 96), (298, 416), (322, base), (356, base),
        (384, 246), (404, base), (464, base),
    ]
    white = (255, 255, 255, 255)
    draw.line(pulse, fill=white, width=20, joint="curve")
    # Rounded caps on the ends
    for (cx, cy) in (pulse[0], pulse[-1]):
        draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=white)

    icon.save(output_path)
    print(f"Icon generated: {output_path} ({SIZE}x{SIZE})")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "fitness_fetch/assets/app_icon.png"
    build(out)
