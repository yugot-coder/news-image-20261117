#!/usr/bin/env python3
"""Build poster.png -- "The Day in Full", Tuesday 17 November 2026.

Design source for the entry image of the make.fun competition
news-image-20261117. It renders a one-page newspaper front page with
Pillow, from the day's wire reports (17 November 2026):

  * Iran fires drones at a U.S. radar site in Bahrain -- its third
    attack in four days, ending a two-month lull; Bahrain says it shot
    them down, a U.S. carrier group (USS Theodore Roosevelt) arrives in
    the region, and mines and missiles batter Strait of Hormuz shipping
    (one crew member missing).
  * A second night of Ukrainian strikes collapses a road span of the
    Kerch Bridge to Crimea; two are killed in Crimea, Russia answers
    against bridges in Kyiv and claims a record drone haul.
  * Trump meets Quad leaders in Manila (critical-minerals pacts) and
    flies on to Shenzhen, where he, Xi Jinping and Vladimir Putin are
    set for a first three-way summit at APEC on Thursday.
  * Nvidia reports a $115.8B quarter, but its board will not reinstate
    Jensen Huang, who resigned over an affair with a suspected spy.
  * Wall Street slides: the S&P 500 falls 1.9% ahead of Nvidia's
    results; oil slips to about $92 despite the Gulf attacks.
  * Two Russian planes breach Japan's airspace off Okinoshima; Tokyo
    scrambles fighter jets and protests.
  * GTA VI's 212 GB pre-load is live; pre-orders pass 15 million
    before Thursday's midnight launch.
  * Briefs: the UK, Australia, Canada and Italy urge Israel to open
    Gaza crossings; settlers kill a Palestinian woman of 72 near
    Jericho; Mongolia's president resigns; Depardieu drops his appeal.

This script is run once, at build time, on the author's machine. The
submitted program (main.py) only copies the rendered poster.png, because
the grading sandbox is standard-library only. Rendering is fully
deterministic: fixed canvas, fixed fonts, no clock, no randomness.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
RIGHT = W - MARGIN
COLW = (RIGHT - MARGIN - 36) // 2  # two-column width
X2 = MARGIN + COLW + 36            # second column x

PAPER = (247, 243, 233)
INK = (23, 29, 45)
SOFT = (62, 60, 54)
ACCENT = (186, 84, 14)
SEA = (18, 47, 74)
SAND = (219, 203, 164)
WHITE = (246, 244, 238)
PALE = (255, 196, 150)
FAINT = (198, 192, 172)
SHIP = (168, 178, 190)

FONTS = "/usr/share/fonts/truetype"
SERIF_BOLD = f"{FONTS}/dejavu/DejaVuSerif-Bold.ttf"
SERIF = f"{FONTS}/dejavu/DejaVuSerif.ttf"
SERIF_IT = f"{FONTS}/liberation/LiberationSerif-Italic.ttf"
SANS_BOLD = f"{FONTS}/liberation/LiberationSans-Bold.ttf"
SANS = f"{FONTS}/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(path, lines, max_width, start):
    """Largest size <= start at which every line fits max_width."""
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    size = start
    while size > 8:
        f = font(path, size)
        if all(probe.textlength(t, font=f) <= max_width for t in lines):
            return f
        size -= 2
    return font(path, size)


def tracked(draw, cx, y, text, fnt, fill, tracking=6):
    """Draw text centred on cx with extra letter tracking."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking
    return total


def wrap(draw, text, fnt, max_width):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def dashed_arc(draw, p0, p1, p2, fill, width=4, dash=14, gap=10):
    """Dashed quadratic Bezier from p0 to p2 with control point p1."""
    pts = []
    steps = 90
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((x, y))
    dist = 0.0
    pen = True
    for a, b in zip(pts, pts[1:]):
        seg = ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
        if pen:
            draw.line([a, b], fill=fill, width=width)
        dist += seg
        if pen and dist >= dash:
            pen, dist = False, 0.0
        elif not pen and dist >= gap:
            pen, dist = True, 0.0


def draw_map(draw, y0, height=102):
    """Schematic panel: the Strait of Hormuz and the Gulf."""
    y1 = y0 + height
    draw.rectangle([MARGIN, y0, RIGHT, y1], fill=SEA)
    # North shore: Iran.
    draw.polygon(
        [(MARGIN, y0), (RIGHT, y0), (RIGHT, y0 + 24), (770, y0 + 32),
         (648, y0 + 20), (520, y0 + 34), (398, y0 + 24), (238, y0 + 32),
         (118, y0 + 22), (MARGIN, y0 + 30)],
        fill=SAND,
    )
    # South shore: Arabia.
    draw.polygon(
        [(MARGIN, y1), (MARGIN, y0 + 82), (220, y0 + 76), (420, y0 + 88),
         (560, y0 + 78), (700, y0 + 90), (862, y0 + 80), (RIGHT, y0 + 88),
         (RIGHT, y1)],
        fill=SAND,
    )
    f_land = font(SANS_BOLD, 19)
    draw.text((MARGIN + 16, y0 + 4), "I R A N", font=f_land, fill=INK)
    draw.text((MARGIN + 16, y1 - 24), "A R A B I A", font=f_land, fill=INK)
    draw.text((MARGIN + 250, y0 + 46), "Strait of Hormuz",
              font=font(SERIF_IT, 23), fill=WHITE)
    f_lab = font(SANS_BOLD, 20)

    # Launch point on the Iranian shore; dashed arcs to Bahrain.
    lx, ly = 640, y0 + 34
    draw.ellipse([lx - 6, ly - 6, lx + 6, ly + 6], fill=ACCENT)
    draw.text((lx + 14, ly - 12), "IRANIAN DRONES", font=f_lab, fill=PALE)

    tx, ty = 452, y0 + 70
    dashed_arc(draw, (lx - 8, ly + 4), ((lx + tx) / 2, y0 + 10), (tx, ty - 8),
               (255, 110, 70), width=4)
    draw.ellipse([tx - 7, ty - 7, tx + 7, ty + 7], fill=ACCENT, outline=WHITE, width=2)
    draw.text((tx - 14, ty - 11), "BAHRAIN", font=f_lab, fill=WHITE, anchor="ra")

    # A merchant ship hit in the strait.
    sx, sy = 724, y0 + 54
    draw.polygon([(sx - 20, sy), (sx + 20, sy), (sx + 13, sy + 9), (sx - 13, sy + 9)],
                 fill=SHIP)
    draw.rectangle([sx - 5, sy - 7, sx + 7, sy - 1], fill=SHIP)
    draw.ellipse([sx - 24, sy + 13, sx - 16, sy + 21], fill=(255, 110, 70))
    draw.ellipse([sx + 16, sy + 13, sx + 24, sy + 21], fill=(255, 110, 70))
    draw.text((sx, y1 - 21), "SHIPPING ATTACKED", font=font(SANS_BOLD, 15),
              fill=INK, anchor="ma")

    # The arriving U.S. carrier group, far right (Gulf of Oman side).
    kx, ky = 916, y0 + 40
    draw.polygon([(kx - 26, ky), (kx + 26, ky), (kx + 18, ky + 8), (kx - 18, ky + 8)],
                 fill=SHIP)
    draw.rectangle([kx - 3, ky - 6, kx + 9, ky - 1], fill=SHIP)
    draw.text((RIGHT - 10, ky + 12), "U.S. CARRIER GROUP", font=font(SANS_BOLD, 15),
              fill=WHITE, anchor="ra")
    draw.text((RIGHT - 10, ky + 30), "ARRIVES", font=font(SANS_BOLD, 15),
              fill=WHITE, anchor="ra")


def cell(draw, x, y, kicker, big, body):
    draw.text((x, y), kicker, font=font(SANS_BOLD, 20), fill=ACCENT)
    f_big = fit_font(SERIF_BOLD, [big], COLW, 42)
    draw.text((x, y + 25), big, font=f_big, fill=INK)
    f_body = font(SERIF, 22)
    ly = y + 25 + 44 + 5
    for line in wrap(draw, body, f_body, COLW):
        draw.text((x, ly), line, font=f_body, fill=SOFT)
        ly += 27
    return ly


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    cx = W / 2

    # --- Masthead -------------------------------------------------------
    draw.rectangle([MARGIN, 22, RIGHT, 27], fill=INK)
    draw.rectangle([MARGIN, 30, RIGHT, 32], fill=ACCENT)
    tracked(draw, cx, 38, "TUESDAY · 17 NOVEMBER 2026", font(SANS_BOLD, 25), INK, tracking=5)
    f_mast = fit_font(SERIF_BOLD, ["THE DAY IN FULL"], RIGHT - MARGIN, 96)
    draw.text((cx, 66), "THE DAY IN FULL", font=f_mast, fill=INK, anchor="ma")
    draw.rectangle([MARGIN, 163, RIGHT, 166], fill=ACCENT)
    draw.rectangle([MARGIN, 169, RIGHT, 170], fill=INK)

    # --- Lead story -----------------------------------------------------
    y = 174
    draw.text((MARGIN, y), "GULF WAR", font=font(SANS_BOLD, 25), fill=ACCENT)
    draw.text((MARGIN + 148, y + 2), "— THE DAY'S TOP STORY", font=font(SANS, 22), fill=SOFT)
    y += 33
    lead = ["IRAN'S DRONES STRIKE BAHRAIN AGAIN", "AS U.S. CARRIER GROUP ARRIVES"]
    f_h1 = fit_font(SERIF_BOLD, lead, RIGHT - MARGIN, 56)
    draw.text((MARGIN, y), lead[0], font=f_h1, fill=INK)
    draw.text((MARGIN, y + 56), lead[1], font=f_h1, fill=INK)
    y += 116
    f_sub = font(SERIF, 25)
    sub = ("Iran fires drones at a U.S. radar site in Bahrain -- a third "
           "attack in four days. Bahrain says it downed them all.")
    for line in wrap(draw, sub, f_sub, RIGHT - MARGIN):
        draw.text((MARGIN, y), line, font=f_sub, fill=SOFT)
        y += 30
    y += 2
    draw_map(draw, y, height=102)
    y += 102 + 8
    draw.rectangle([MARGIN, y, RIGHT, y + 2], fill=INK)
    y += 12

    # --- Middle band: summitry and the Kerch Bridge ---------------------
    top = y
    draw.text((MARGIN, y), "SUMMITRY · MANILA & SHENZHEN", font=font(SANS_BOLD, 21), fill=ACCENT)
    draw.text((X2, y), "WAR IN EUROPE · CRIMEA", font=font(SANS_BOLD, 21), fill=ACCENT)
    y += 26
    left_h = ["TRUMP MEETS THE QUAD,", "THREE-WAY SUMMIT NEXT"]
    right_h = ["UKRAINE DROPS A SPAN", "OF THE KERCH BRIDGE"]
    f_h2 = fit_font(SERIF_BOLD, left_h + right_h, COLW, 36)
    for i, line in enumerate(left_h):
        draw.text((MARGIN, y + i * 38), line, font=f_h2, fill=INK)
    for i, line in enumerate(right_h):
        draw.text((X2, y + i * 38), line, font=f_h2, fill=INK)
    y += 2 * 38 + 4
    f_b = font(SERIF, 23)
    left_b = ("Quad leaders unveil minerals pacts in Manila; "
              "Trump flies to Shenzhen.")
    right_b = ("A second night of strikes fells the road span; "
               "two die in Crimea.")
    ly = y
    for line in wrap(draw, left_b, f_b, COLW):
        draw.text((MARGIN, ly), line, font=f_b, fill=SOFT)
        ly += 28
    ry = y
    for line in wrap(draw, right_b, f_b, COLW):
        draw.text((X2, ry), line, font=f_b, fill=SOFT)
        ry += 28
    y = max(ly, ry) + 4
    draw.line([MARGIN + COLW + 18, top, MARGIN + COLW + 18, y], fill=INK, width=1)
    draw.rectangle([MARGIN, y, RIGHT, y + 2], fill=INK)
    y += 9

    # --- Bottom grid: four stories with big numbers ---------------------
    gy = y
    cell(draw, MARGIN, gy, "TECH · NVIDIA", "$115.8B",
         "Nvidia's quarter; board bars Huang's return amid spy scandal.")
    cell(draw, X2, gy, "MARKETS · WALL STREET", "-1.9%",
         "S&P 500 slides before Nvidia's results; oil slips to $92.")
    gy2 = gy + 131
    draw.line([MARGIN, gy + 123, RIGHT, gy + 123], fill=FAINT, width=1)
    cell(draw, MARGIN, gy2, "ASIA · JAPAN", "2 PLANES",
         "Russian jets breach airspace off Okinoshima; Tokyo scrambles.")
    cell(draw, X2, gy2, "GAMES · GTA VI", "212 GB",
         "Pre-load is live; 15M+ pre-orders before Thursday's launch.")
    draw.line([MARGIN + COLW + 18, gy, MARGIN + COLW + 18, gy2 + 117], fill=INK, width=1)

    # --- Footer briefs ---------------------------------------------------
    fy = gy2 + 131
    draw.rectangle([MARGIN, fy, RIGHT, fy + 3], fill=ACCENT)
    f_brief = font(SANS_BOLD, 19)
    briefs = ("ALSO TODAY -- UK, Australia, Canada & Italy urge Israel to open Gaza "
              "crossings · Settlers kill a Palestinian woman, 72, near Jericho · "
              "Mongolia's president resigns")
    lines = wrap(draw, briefs, f_brief, RIGHT - MARGIN)
    for i, line in enumerate(lines):
        draw.text((cx, fy + 7 + i * 25), line, font=f_brief, fill=INK, anchor="ma")
    end = fy + 7 + len(lines) * 25
    assert end <= H - 10, f"layout overflows: {end}"

    out = Path(__file__).resolve().parent / "poster.png"
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
