#!/usr/bin/env python3
"""Re-render assets/og-card.png in the website's design language.

The previous card used a serif headline (--font-display = Georgia/Times) which
is inconsistent with the website's sans-serif type (Neue Montreal / Hanken
Grotesk) and its navy+brass palette. This renders the same content in the
website's deep-panel style: navy background, brass accent, sans-serif type.

Matches website/src/styles/tokens.css deep palette:
  --D-paper: #0e1a2b  --D-ink: #ede8dd  --D-ink-2: #a9b2bf
  --D-accent: #c9a866  --D-border: #26384f
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
FONT = "/home/paperclip/scratch/eth-india-og/fonts/HankenGrotesk.ttf"

# palette (deep zone)
BG = (14, 26, 43)          # --D-paper #0e1a2b
INK = (237, 232, 221)      # --D-ink #ede8dd
INK2 = (169, 178, 191)     # --D-ink-2 #a9b2bf
ACCENT = (201, 168, 102)   # --D-accent #c9a866
BORDER = (38, 56, 79)      # --D-border #26384f

def font(size):
    return ImageFont.truetype(FONT, size)

def text_w(draw, txt, f):
    b = draw.textbbox((0, 0), txt, font=f)
    return b[2] - b[0]

def draw_centered(draw, y, txt, f, fill):
    w = text_w(draw, txt, f)
    draw.text(((W - w) / 2, y), txt, font=f, fill=fill)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# subtle vertical grid lines (matches default.png technical feel)
for x in range(0, W, 60):
    draw.line([(x, 0), (x, H)], fill=(255, 255, 255, 0), width=1)
# faint grid via low-alpha overlay
grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grid)
for x in range(0, W, 60):
    gd.line([(x, 0), (x, H)], fill=(237, 232, 221, 8), width=1)
for y in range(0, H, 60):
    gd.line([(0, y), (W, y)], fill=(237, 232, 221, 8), width=1)
img = Image.alpha_composite(img.convert("RGBA"), grid).convert("RGB")
draw = ImageDraw.Draw(img)

# top accent bar
draw.rectangle([0, 0, W, 10], fill=ACCENT)

# eyebrow
eyebrow = "ETHEREUM/INDIA INSTITUTIONAL BRIEFING"
f_eyebrow = font(30)
w = text_w(draw, eyebrow, f_eyebrow)
draw.text((80, 96), eyebrow, font=f_eyebrow, fill=ACCENT)

# headline (sans-serif, consistent with website)
headline = "Tokenised settlement in India"
f_head = font(84)
w = text_w(draw, headline, f_head)
draw.text(((W - w) / 2, 210), headline, font=f_head, fill=INK)

# sub
sub = "What's live, what's legal, where Ethereum fits"
f_sub = font(36)
w = text_w(draw, sub, f_sub)
draw.text(((W - w) / 2, 340), sub, font=f_sub, fill=INK2)

# footer
foot = "Every figure sourced, dated and tiered T1 to T5"
f_foot = font(26)
w = text_w(draw, foot, f_foot)
draw.line([(80, 500), (W - 80, 500)], fill=BORDER, width=1)
draw.text((80, 528), foot, font=f_foot, fill=INK2)

out = "/home/paperclip/scratch/eth-india-og/assets/og-card.png"
img.save(out)
print("saved", out, img.size)
