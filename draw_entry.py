#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news front page (1024x1024 PNG).

Deterministic: fixed text, fixed geometry, no randomness, no network.
Run: python3 draw_entry.py  -> writes entry.png beside this file.
Fonts: DejaVu (present on the build machine and in most Linux images).

Stories (all verified as events of Tuesday 24 November 2026, or first
reported that day; each cross-checked in at least two outlets):
- LEAD: South Korea sounds an air-raid alert on Ulleung Island after
  jets approach; alert lifted within minutes (Reuters, AP, KBS).
- Crimea Platform parliamentary summit opens in Stockholm (Riksdagen,
  Verkhovna Rada, Saeima).
- Trump pardons the Thanksgiving turkeys, then flies to Mar-a-Lago
  (Palm Beach Post, White House schedule).
- Tokyo stock market reopens after the Nikkei's fifth-biggest point
  drop ever on Friday (Asia Daily, Peter Lewis briefing).
- Beaver Supermoon peaks on 24 Nov, first of four supermoons in a row
  (weather.com, Smithsonian, NASA).
- Champions League Matchday 5: nine games on Tuesday (UEFA).
- Odesa's blackout could last weeks after Russian strikes (h.ua,
  Europesays, Forbes/DTEK).
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 238)
NAVY = (20, 33, 61)
NAVY2 = (27, 45, 84)
GOLD = (201, 162, 39)
RED = (180, 35, 24)
INK = (24, 24, 24)
GREY = (90, 90, 90)
CARD = (255, 255, 255)
BORDER = (210, 205, 192)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------- masthead ----------------
d.rectangle([0, 0, W, 122], fill=NAVY)
d.text((W // 2, 14), "THE WORLD IN ONE PICTURE", font=font(SERIF, 52),
       fill=(255, 255, 255), anchor="ma")
d.rectangle([W // 2 - 300, 86, W // 2 + 300, 89], fill=GOLD)
d.text((W // 2, 96), "TUESDAY  ·  24 NOVEMBER 2026",
       font=font(SANS_B, 24), fill=(232, 196, 90), anchor="ma")

# ---------------- lead story ----------------
LX, LY, LW, LH = 28, 138, 968, 300
d.rectangle([LX, LY, LX + LW, LY + LH], fill=CARD, outline=BORDER, width=2)
d.rectangle([LX, LY, LX + LW, LY + 6], fill=RED)
tx = LX + 22
d.text((tx, LY + 20), "LEAD  —  ASIA  ·  SECURITY",
       font=font(SANS_B, 19), fill=RED)
headline = "Seoul sounds alert as jets approach Ulleung Island"
y = draw_lines(d, tx, LY + 50,
               wrap(d, headline, font(SANS_B, 38), 560),
               font(SANS_B, 38), INK, 46)
summary = ("South Korea briefly told residents of Ulleung Island to take "
           "shelter on Tuesday morning after jets approached the island; "
           "the alert was lifted within minutes. The military said the "
           "aircraft entered the air-defence zone but did not breach "
           "airspace, and their origin was later in doubt.")
draw_lines(d, tx, y + 8,
           wrap(d, summary, font(SANS, 18), 560),
           font(SANS, 18), (60, 60, 60), 25)

# lead illustration: radar panel over the East Sea
PX, PY, PW, PH = 648, LY + 20, 326, 238
d.rectangle([PX, PY, PX + PW, PY + PH], fill=(214, 232, 245),
            outline=BORDER, width=1)
# radar rings
cx, cy, r = PX + 163, PY + 108, 82
for rr in (r, r * 2 // 3, r // 3):
    d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
              outline=(46, 111, 173), width=2)
d.line([cx - r, cy, cx + r, cy], fill=(46, 111, 173), width=2)
d.line([cx, cy - r, cx, cy + r], fill=(46, 111, 173), width=2)
# sweep line
d.line([cx, cy, cx + 62, cy - 52], fill=(46, 111, 173), width=3)
# blips
for bx, by in [(cx - 38, cy - 30), (cx + 44, cy + 18), (cx + 8, cy - 52)]:
    d.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=RED)
# island blob bottom centre
d.ellipse([cx - 26, cy + 52, cx + 26, cy + 66], fill=(46, 111, 73))
d.text((cx, cy + 70), "Ulleung Island", font=font(SANS_B, 13),
       fill=NAVY, anchor="ma")
# jet silhouette top right
jx, jy = PX + PW - 52, PY + 26
d.polygon([(jx, jy), (jx + 26, jy + 8), (jx, jy + 16)], fill=NAVY)
d.polygon([(jx + 8, jy + 4), (jx + 22, jy - 6), (jx + 24, jy + 2)],
          fill=NAVY)
d.text((PX + PW // 2, PY + PH - 2), "", font=font(SANS, 10), fill=NAVY)

# ---------------- story cards: 2 cols x 3 rows ----------------
cards = [
    ("EUROPE", (20, 33, 61), "flags",
     "Crimea Platform summit opens in Stockholm",
     "Parliament speakers from about 70 countries gather in Sweden; "
     "Zelenskyy addresses the summit by video as allies press the "
     "case on Crimea."),
    ("USA", (178, 34, 52), "plane",
     "Trump pardons the turkeys, then flies south",
     "The president pardons two birds on the South Lawn on Tuesday "
     "afternoon, then heads to Mar-a-Lago for a five-night "
     "Thanksgiving stay."),
    ("MARKETS", (27, 108, 66), "chart",
     "Tokyo reopens after its worst week in years",
     "The Nikkei plunged 3,007 points on Friday, its fifth-biggest "
     "drop ever; trading resumes on Tuesday after a holiday."),
    ("SCIENCE", (18, 90, 160), "moon",
     "Beaver Supermoon peaks tonight",
     "November's full moon, the first of four supermoons in a row, "
     "reaches peak light at 9:53 a.m. ET and passes near the Pleiades."),
    ("SPORT", (176, 92, 8), "ball",
     "Champions League returns with nine games",
     "Matchday 5: Arsenal host Dortmund, De Bruyne returns to "
     "Manchester with Napoli, and Real Madrid chase a fifth straight "
     "win."),
    ("UKRAINE", (180, 35, 24), "bolt",
     "Odesa's blackout could last weeks",
     "Russian strikes wrecked the port city's grid; schools go remote "
     "for the week as Zelenskyy says Moscow hits power lines again "
     "once repaired."),
]

GX, GY = 28, 454
CW, CH, CGAP, RGAP = 476, 152, 16, 12


def icon(draw, kind, x, y, col):
    """Simple 46x46 pictogram in the card's accent colour."""
    if kind == "flags":
        for i, fcol in enumerate([(178, 34, 52), (0, 56, 168),
                                 (201, 162, 39)]):
            fx0 = x + i * 15
            draw.rectangle([fx0, y + 6, fx0 + 12, y + 34], fill=fcol,
                           outline=(255, 255, 255), width=1)
            draw.line([fx0 + 6, y + 34, fx0 + 6, y + 44], fill=col, width=2)
        draw.line([x, y + 44, x + 46, y + 44], fill=col, width=3)
    elif kind == "plane":
        # fuselage
        d.line([x + 2, y + 23, x + 40, y + 23], fill=col, width=5)
        # nose
        d.polygon([(x + 40, y + 19), (x + 46, y + 23), (x + 40, y + 27)],
                  fill=col)
        # top wing
        d.polygon([(x + 18, y + 23), (x + 26, y + 6), (x + 30, y + 23)],
                  fill=col)
        # bottom wing
        d.polygon([(x + 18, y + 23), (x + 26, y + 40), (x + 30, y + 23)],
                  fill=col)
        # tail
        d.polygon([(x + 2, y + 23), (x + 8, y + 14), (x + 11, y + 23)],
                  fill=col)
        d.polygon([(x + 2, y + 23), (x + 8, y + 32), (x + 11, y + 23)],
                  fill=col)
    elif kind == "chart":
        draw.line([x + 4, y + 40, x + 4, y + 6], fill=col, width=3)
        draw.line([x + 4, y + 40, x + 44, y + 40], fill=col, width=3)
        draw.line([x + 8, y + 30, x + 18, y + 18, x + 28, y + 26,
                   x + 42, y + 8], fill=col, width=3)
        draw.polygon([(x + 42, y + 2), (x + 46, y + 10), (x + 36, y + 10)],
                     fill=col)
    elif kind == "moon":
        draw.ellipse([x + 4, y + 2, x + 42, y + 40], fill=(232, 196, 90),
                     outline=col, width=2)
        for mx, my, mr in [(x + 16, y + 14, 4), (x + 28, y + 24, 5),
                           (x + 18, y + 28, 3)]:
            draw.ellipse([mx - mr, my - mr, mx + mr, my + mr],
                         fill=(201, 162, 39))
    elif kind == "ball":
        draw.ellipse([x + 3, y + 3, x + 43, y + 43], outline=col, width=3)
        draw.polygon([(x + 23, y + 14), (x + 32, y + 21), (x + 29, y + 31),
                      (x + 17, y + 31), (x + 14, y + 21)], fill=col)
        draw.line([x + 23, y + 14, x + 23, y + 4], fill=col, width=2)
        draw.line([x + 32, y + 21, x + 42, y + 16], fill=col, width=2)
        draw.line([x + 29, y + 31, x + 36, y + 40], fill=col, width=2)
        draw.line([x + 17, y + 31, x + 10, y + 40], fill=col, width=2)
        draw.line([x + 14, y + 21, x + 4, y + 16], fill=col, width=2)
    elif kind == "bolt":
        draw.polygon([(x + 26, y + 2), (x + 10, y + 26), (x + 20, y + 26),
                      (x + 16, y + 44), (x + 36, y + 18), (x + 24, y + 18)],
                     fill=col)


for i, (tag, col, kind, head, body) in enumerate(cards):
    cx0 = GX + (i % 2) * (CW + CGAP)
    cy0 = GY + (i // 2) * (CH + RGAP)
    d.rectangle([cx0, cy0, cx0 + CW, cy0 + CH], fill=CARD,
                outline=BORDER, width=2)
    d.rectangle([cx0, cy0, cx0 + 8, cy0 + CH], fill=col)
    icon(d, kind, cx0 + CW - 62, cy0 + 14, col)
    d.text((cx0 + 22, cy0 + 12), tag, font=font(SANS_B, 15), fill=col)
    y = draw_lines(d, cx0 + 22, cy0 + 34,
                   wrap(d, head, font(SANS_B, 20), CW - 100),
                   font(SANS_B, 20), INK, 24)
    draw_lines(d, cx0 + 22, y + 4,
               wrap(d, body, font(SANS, 14), CW - 44),
               font(SANS, 14), (70, 70, 70), 19)

# ---------------- ticker footer ----------------
FY = 948
d.rectangle([0, FY, W, H], fill=NAVY)
ticker = ("ALSO:  Spain votes in five days  ·  US markets shut Thursday  ·  "
          "Beaver Moon nears the Pleiades")
tfs = 16
while d.textlength(ticker, font=font(SANS_B, tfs)) > W - 40 and tfs > 10:
    tfs -= 1
d.text((W // 2, FY + 10), ticker, font=font(SANS_B, tfs),
       fill=(255, 255, 255), anchor="ma")
d.text((W // 2, FY + 38), "Tuesday 24 November 2026  ·  The world in one image",
       font=font(SANS, 14), fill=(200, 205, 220), anchor="ma")

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
