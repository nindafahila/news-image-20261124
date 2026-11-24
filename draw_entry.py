#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news front page (1024x1024 PNG).

One-page newspaper: navy masthead, a lead story with a radar panel,
six story cards in a 2x3 grid, and a navy ticker footer.

Deterministic on purpose: fixed text, fixed geometry, no randomness,
no network access, no clock reads. Running this script twice produces
the same bytes. Fonts are the DejaVu family shipped with the system.
Run from the repository root:  python3 draw_entry.py

Stories (each verified as an event of Tuesday 24 November 2026, or
first reported that day, cross-checked in at least two outlets):
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
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# Palette
PAPER = (250, 246, 238)      # page background
NAVY = (20, 33, 61)          # masthead / footer / EUROPE tag
GOLD = (201, 162, 39)        # masthead rule
GOLD_TEXT = (232, 196, 90)   # masthead date
RED = (180, 35, 24)          # lead bar / UKRAINE tag
INK = (24, 24, 24)           # headlines
BODY_GREY = (60, 60, 60)     # lead summary
CARD_GREY = (70, 70, 70)     # card body text
CARD = (255, 255, 255)       # card fill
BORDER = (210, 205, 192)     # card outline
FOOTER_SUB = (200, 205, 220)  # footer second line

# Tag colours per card
TAG_NAVY = (20, 33, 61)
TAG_RED = (178, 34, 52)
TAG_GREEN = (27, 108, 66)
TAG_BLUE = (18, 90, 160)
TAG_BROWN = (176, 92, 8)

# Radar panel colours
RADAR_FILL = (214, 232, 245)
RADAR_LINE = (46, 111, 173)
ISLAND_GREEN = (46, 111, 73)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, font, max_width):
    """Greedy word wrap by rendered pixel width."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, x, y, lines, font, fill, leading):
    """Draw lines top to bottom, return the y below the last line."""
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


canvas = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(canvas)

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 122], fill=NAVY)
d.text((W // 2, 14), "THE WORLD IN ONE PICTURE",
       font=load(SERIF_B, 52), fill=(255, 255, 255), anchor="ma")
d.rectangle([W // 2 - 300, 86, W // 2 + 300, 89], fill=GOLD)
d.text((W // 2, 96), "TUESDAY  ·  24 NOVEMBER 2026",
       font=load(SANS_B, 24), fill=GOLD_TEXT, anchor="ma")

# ---------------------------------------------------------------- lead story
LX, LY, LW, LH = 28, 138, 968, 300
d.rectangle([LX, LY, LX + LW, LY + LH], fill=CARD, outline=BORDER, width=2)
d.rectangle([LX, LY, LX + LW, LY + 6], fill=RED)
tx = LX + 22
d.text((tx, LY + 20), "LEAD  —  ASIA  ·  SECURITY",
       font=load(SANS_B, 19), fill=RED)
headline = "Seoul sounds alert as jets approach Ulleung Island"
y = draw_wrapped(d, tx, LY + 50,
                 wrap_text(d, headline, load(SANS_B, 38), 560),
                 load(SANS_B, 38), INK, 46)
summary = ("South Korea briefly told residents of Ulleung Island to take "
           "shelter on Tuesday morning after jets approached the island; "
           "the alert was lifted within minutes. The military said the "
           "aircraft entered the air-defence zone but did not breach "
           "airspace, and their origin was later in doubt.")
draw_wrapped(d, tx, y + 8,
             wrap_text(d, summary, load(SANS, 18), 560),
             load(SANS, 18), BODY_GREY, 25)

# Radar panel over the East Sea, right of the lead text.
PX, PY, PW, PH = 648, LY + 20, 326, 238
d.rectangle([PX, PY, PX + PW, PY + PH], fill=RADAR_FILL,
            outline=BORDER, width=1)
cx, cy, r = PX + 163, PY + 108, 82
for rr in (r, r * 2 // 3, r // 3):
    d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
              outline=RADAR_LINE, width=2)
d.line([cx - r, cy, cx + r, cy], fill=RADAR_LINE, width=2)
d.line([cx, cy - r, cx, cy + r], fill=RADAR_LINE, width=2)
d.line([cx, cy, cx + 62, cy - 52], fill=RADAR_LINE, width=3)
for bx, by in [(cx - 38, cy - 30), (cx + 44, cy + 18), (cx + 8, cy - 52)]:
    d.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=RED)
d.ellipse([cx - 26, cy + 52, cx + 26, cy + 66], fill=ISLAND_GREEN)
d.text((cx, cy + 70), "Ulleung Island", font=load(SANS_B, 13),
       fill=NAVY, anchor="ma")
# Jet silhouette, top right of the panel.
jx, jy = PX + PW - 52, PY + 26
d.polygon([(jx, jy), (jx + 26, jy + 8), (jx, jy + 16)], fill=NAVY)
d.polygon([(jx + 8, jy + 4), (jx + 22, jy - 6), (jx + 24, jy + 2)],
          fill=NAVY)

# ---------------------------------------------------------------- story cards
CARDS = [
    ("EUROPE", TAG_NAVY, "flags",
     "Crimea Platform summit opens in Stockholm",
     "Parliament speakers from about 70 countries gather in Sweden; "
     "Zelenskyy addresses the summit by video as allies press the "
     "case on Crimea."),
    ("USA", TAG_RED, "plane",
     "Trump pardons the turkeys, then flies south",
     "The president pardons two birds on the South Lawn on Tuesday "
     "afternoon, then heads to Mar-a-Lago for a five-night "
     "Thanksgiving stay."),
    ("MARKETS", TAG_GREEN, "chart",
     "Tokyo reopens after its worst week in years",
     "The Nikkei plunged 3,007 points on Friday, its fifth-biggest "
     "drop ever; trading resumes on Tuesday after a holiday."),
    ("SCIENCE", TAG_BLUE, "moon",
     "Beaver Supermoon peaks tonight",
     "November's full moon, the first of four supermoons in a row, "
     "reaches peak light at 9:53 a.m. ET and passes near the Pleiades."),
    ("SPORT", TAG_BROWN, "ball",
     "Champions League returns with nine games",
     "Matchday 5: Arsenal host Dortmund, De Bruyne returns to "
     "Manchester with Napoli, and Real Madrid chase a fifth straight "
     "win."),
    ("UKRAINE", RED, "bolt",
     "Odesa's blackout could last weeks",
     "Russian strikes wrecked the port city's grid; schools go remote "
     "for the week as Zelenskyy says Moscow hits power lines again "
     "once repaired."),
]

GX, GY = 28, 454
CW, CH, CGAP, RGAP = 476, 152, 16, 12


def draw_icon(kind, x, y, col):
    """A simple 46x46 pictogram in the card's accent colour."""
    if kind == "flags":
        for i, fcol in enumerate([(178, 34, 52), (0, 56, 168),
                                 (201, 162, 39)]):
            fx0 = x + i * 15
            d.rectangle([fx0, y + 6, fx0 + 12, y + 34], fill=fcol,
                        outline=(255, 255, 255), width=1)
            d.line([fx0 + 6, y + 34, fx0 + 6, y + 44], fill=col, width=2)
        d.line([x, y + 44, x + 46, y + 44], fill=col, width=3)
    elif kind == "plane":
        d.line([x + 2, y + 23, x + 40, y + 23], fill=col, width=5)
        d.polygon([(x + 40, y + 19), (x + 46, y + 23), (x + 40, y + 27)],
                  fill=col)
        d.polygon([(x + 18, y + 23), (x + 26, y + 6), (x + 30, y + 23)],
                  fill=col)
        d.polygon([(x + 18, y + 23), (x + 26, y + 40), (x + 30, y + 23)],
                  fill=col)
        d.polygon([(x + 2, y + 23), (x + 8, y + 14), (x + 11, y + 23)],
                  fill=col)
        d.polygon([(x + 2, y + 23), (x + 8, y + 32), (x + 11, y + 23)],
                  fill=col)
    elif kind == "chart":
        d.line([x + 4, y + 40, x + 4, y + 6], fill=col, width=3)
        d.line([x + 4, y + 40, x + 44, y + 40], fill=col, width=3)
        d.line([x + 8, y + 30, x + 18, y + 18, x + 28, y + 26,
                x + 42, y + 8], fill=col, width=3)
        d.polygon([(x + 42, y + 2), (x + 46, y + 10), (x + 36, y + 10)],
                  fill=col)
    elif kind == "moon":
        d.ellipse([x + 4, y + 2, x + 42, y + 40], fill=GOLD_TEXT,
                  outline=col, width=2)
        for mx, my, mr in [(x + 16, y + 14, 4), (x + 28, y + 24, 5),
                           (x + 18, y + 28, 3)]:
            d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=GOLD)
    elif kind == "ball":
        d.ellipse([x + 3, y + 3, x + 43, y + 43], outline=col, width=3)
        d.polygon([(x + 23, y + 14), (x + 32, y + 21), (x + 29, y + 31),
                   (x + 17, y + 31), (x + 14, y + 21)], fill=col)
        d.line([x + 23, y + 14, x + 23, y + 4], fill=col, width=2)
        d.line([x + 32, y + 21, x + 42, y + 16], fill=col, width=2)
        d.line([x + 29, y + 31, x + 36, y + 40], fill=col, width=2)
        d.line([x + 17, y + 31, x + 10, y + 40], fill=col, width=2)
        d.line([x + 14, y + 21, x + 4, y + 16], fill=col, width=2)
    elif kind == "bolt":
        d.polygon([(x + 26, y + 2), (x + 10, y + 26), (x + 20, y + 26),
                   (x + 16, y + 44), (x + 36, y + 18), (x + 24, y + 18)],
                  fill=col)


for i, (tag, col, kind, head, body) in enumerate(CARDS):
    cx0 = GX + (i % 2) * (CW + CGAP)
    cy0 = GY + (i // 2) * (CH + RGAP)
    d.rectangle([cx0, cy0, cx0 + CW, cy0 + CH], fill=CARD,
                outline=BORDER, width=2)
    d.rectangle([cx0, cy0, cx0 + 8, cy0 + CH], fill=col)
    draw_icon(kind, cx0 + CW - 62, cy0 + 14, col)
    d.text((cx0 + 22, cy0 + 12), tag, font=load(SANS_B, 15), fill=col)
    y = draw_wrapped(d, cx0 + 22, cy0 + 34,
                     wrap_text(d, head, load(SANS_B, 20), CW - 100),
                     load(SANS_B, 20), INK, 24)
    draw_wrapped(d, cx0 + 22, y + 4,
                 wrap_text(d, body, load(SANS, 14), CW - 44),
                 load(SANS, 14), CARD_GREY, 19)

# ---------------------------------------------------------------- ticker footer
FY = 948
d.rectangle([0, FY, W, H], fill=NAVY)
ticker = ("ALSO:  Spain votes in five days  ·  US markets shut Thursday  ·  "
          "Beaver Moon nears the Pleiades")
tfs = 16
while d.textlength(ticker, font=load(SANS_B, tfs)) > W - 40 and tfs > 10:
    tfs -= 1
d.text((W // 2, FY + 10), ticker, font=load(SANS_B, tfs),
       fill=(255, 255, 255), anchor="ma")
d.text((W // 2, FY + 38), "Tuesday 24 November 2026  ·  The world in one image",
       font=load(SANS, 14), fill=FOOTER_SUB, anchor="ma")

canvas.save("entry.png", optimize=True)
print("saved entry.png", canvas.size)
