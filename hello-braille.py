#!/usr/bin/env python3
"""
Generate compact Braille-art representations of various shapes:
- United States flag
- Sine wave curve
- Circle outline
- Filled circle
Each shape is drawn as a monochrome PIL image, converted to Braille Unicode art, and printed.
"""
import math
from PIL import Image, ImageDraw

# Braille dot mapping (2×4 pixels)
BRAILLE_BASE = 0x2800
BRAILLE_DOTS = [
    (0, 0), (0, 1), (0, 2),
    (1, 0), (1, 1), (1, 2),
    (0, 3), (1, 3)
]


def image_to_braille(img: Image.Image, threshold: int = 128) -> str:
    """
    Convert a monochrome PIL Image to Braille Unicode art.
    Each 2x4 pixel block maps to one Braille character.
    """
    w, h = img.size
    lines = []
    for y in range(0, h, 4):
        line = ''
        for x in range(0, w, 2):
            pattern = 0
            for i, (dx, dy) in enumerate(BRAILLE_DOTS):
                px, py = x + dx, y + dy
                if px < w and py < h and img.getpixel((px, py)) < threshold:
                    pattern |= (1 << i)
            line += chr(BRAILLE_BASE + pattern)
        lines.append(line)
    return '\n'.join(lines)


def generate_us_flag(width: int = 40, height: int = 26) -> Image.Image:
    """Create a monochrome PIL Image of the US flag (13 stripes, blue canton)."""
    img = Image.new('L', (width, height), 255)
    draw = ImageDraw.Draw(img)
    stripe_h = height / 13
    # 13 stripes: black for red, white for white
    for i in range(13):
        y0 = int(i * stripe_h)
        y1 = int((i + 1) * stripe_h)
        color = 0 if i % 2 == 0 else 255
        draw.rectangle([0, y0, width, y1], fill=color)
    # Blue canton as gray
    canton_h = int(stripe_h * 7)
    canton_w = int(width * 0.4)
    draw.rectangle([0, 0, canton_w, canton_h], fill=128)
    return img


def generate_sine(width: int = 40, height: int = 16) -> Image.Image:
    """Create a monochrome PIL Image of a sine wave curve."""
    img = Image.new('L', (width, height), 255)
    draw = ImageDraw.Draw(img)
    amplitude = height / 2 - 1
    freq = 2 * math.pi / width * 2
    for x in range(width):
        y = int(height / 2 + amplitude * math.sin(freq * x))
        draw.point((x, y), fill=0)
    return img


def generate_circle_outline(diameter: int = 32) -> Image.Image:
    """Create a monochrome PIL Image of a circle outline."""
    img = Image.new('L', (diameter, diameter), 255)
    draw = ImageDraw.Draw(img)
    r = diameter // 2 - 1
    cx, cy = diameter // 2, diameter // 2
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=0)
    return img


def generate_filled_circle(diameter: int = 32) -> Image.Image:
    """Create a monochrome PIL Image of a filled circle."""
    img = Image.new('L', (diameter, diameter), 255)
    draw = ImageDraw.Draw(img)
    r = diameter // 2 - 1
    cx, cy = diameter // 2, diameter // 2
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=0)
    return img


if __name__ == '__main__':
    # Test: blank 2x4 block => one empty braille cell
    blank = Image.new('L', (2, 4), 255)
    assert image_to_braille(blank) == chr(BRAILLE_BASE), 'Blank cell test failed'

    shapes = [
        ('US Flag', generate_us_flag()),
        ('Sine Curve', generate_sine()),
        ('Circle Outline', generate_circle_outline()),
        ('Filled Circle', generate_filled_circle()),
    ]
    for title, img in shapes:
        print(f'--- {title} ---')
        print(image_to_braille(img))
        print()
