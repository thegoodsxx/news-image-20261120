#!/usr/bin/env python3
"""
tools/make_poster.py - Broadsheet front-page poster generator for news-image-20261120.
Draws a 1024x1024 newspaper front-page poster summing up world news of 20 November 2026.
Uses only PIL primitives (rectangles, polygons, ellipses, lines, arcs).
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions
WIDTH = 1024
HEIGHT = 1024

# Palette
COLOR_PAPER = "#f8f4e8"
COLOR_INK = "#14181d"
COLOR_RED = "#b3231b"
COLOR_SUB = "#3d4652"
COLOR_MUTED = "#7a8594"
COLOR_RULE = "#c8c2b0"
COLOR_RULE_DARK = "#14181d"

# Font paths
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def get_font(size, bold=False):
    path = FONT_BOLD_PATH if bold else FONT_REG_PATH
    return ImageFont.truetype(path, size)

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        candidate = " ".join(current_line + [word])
        if font.getlength(candidate) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def draw_tracked_text(draw, xy, text, font, fill, spacing=7, center_width=None):
    total_w = sum(font.getlength(ch) for ch in text) + spacing * (len(text) - 1)
    x, y = xy
    if center_width is not None:
        x = x + (center_width - total_w) / 2
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += font.getlength(ch) + spacing

def draw_star(draw, cx, cy, r, fill):
    points = []
    for i in range(10):
        radius = r if i % 2 == 0 else r * 0.45
        angle = i * math.pi / 5 - math.pi / 2
        points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    draw.polygon(points, fill=fill)

def draw_lead_panel(draw, px, py, pw, ph):
    """Draws the dark visual panel beside the lead story: globe & 3 flags."""
    # Dark panel container
    draw.rounded_rectangle([(px, py), (px + pw, py + ph)], radius=8, fill=COLOR_INK)
    draw.rounded_rectangle([(px, py), (px + pw, py + ph)], radius=8, outline="#2b333e", width=1)

    # Globe in upper half
    globe_cx = px + pw / 2
    globe_cy = py + 84
    globe_r = 46

    # Globe sphere backing
    draw.ellipse([(globe_cx - globe_r, globe_cy - globe_r), (globe_cx + globe_r, globe_cy + globe_r)], fill="#182230", outline="#6e829a", width=2)
    # Equator
    draw.line([(globe_cx - globe_r, globe_cy), (globe_cx + globe_r, globe_cy)], fill="#6e829a", width=1)
    # Longitude meridians
    for factor in [0.72, 0.42, 0.16]:
        draw.arc([(globe_cx - globe_r * factor, globe_cy - globe_r), (globe_cx + globe_r * factor, globe_cy + globe_r)], 0, 360, fill="#506276", width=1)
    # Latitudes
    for y_off in [-23, 23]:
        w_at_y = math.sqrt(max(0, globe_r * globe_r - y_off * y_off))
        draw.line([(globe_cx - w_at_y, globe_cy + y_off), (globe_cx + w_at_y, globe_cy + y_off)], fill="#3c4d60", width=1)

    # Pedestal divider bar
    div_y = py + 148
    draw.line([(px + 16, div_y), (px + pw - 16, div_y)], fill="#2d3642", width=1)

    # Three flags on poles
    pole_y_top = div_y + 10
    pole_y_bot = py + ph - 14
    flag_w = 46
    flag_h = 26

    spacing = (pw - 32 - 3 * flag_w) / 4
    flags = [
        (px + 16 + spacing, "US"),
        (px + 16 + 2 * spacing + flag_w, "CN"),
        (px + 16 + 3 * spacing + 2 * flag_w, "RU"),
    ]

    for fx, ftype in flags:
        pole_x = fx
        # Pole line
        draw.line([(pole_x, pole_y_top), (pole_x, pole_y_bot)], fill="#c0c8d4", width=2)
        # Gold finial
        draw.ellipse([(pole_x - 3, pole_y_top - 4), (pole_x + 3, pole_y_top + 2)], fill="#e8b838")

        flag_x = pole_x + 2
        flag_y = pole_y_top + 2
        fr = [(flag_x, flag_y), (flag_x + flag_w, flag_y + flag_h)]

        if ftype == "US":
            # 7 alternating red and white stripes
            draw.rectangle(fr, fill="#ffffff")
            sh = flag_h / 7
            for i in range(0, 7, 2):
                draw.rectangle([(flag_x, flag_y + i * sh), (flag_x + flag_w, flag_y + (i + 1) * sh)], fill="#b22234")
            # Blue canton
            canton_w = flag_w * 0.45
            canton_h = 4 * sh
            draw.rectangle([(flag_x, flag_y), (flag_x + canton_w, flag_y + canton_h)], fill="#3c3b6e")
            # Star dots in canton
            for dot_x in [flag_x + 5, flag_x + 10, flag_x + 15]:
                for dot_y in [flag_y + 4, flag_y + 9, flag_y + 13]:
                    draw.point([(dot_x, dot_y)], fill="#ffffff")
        elif ftype == "CN":
            # Crimson field
            draw.rectangle(fr, fill="#de2910")
            # Main gold star
            draw_star(draw, flag_x + 7, flag_y + 8, 4.5, "#ffde00")
            # 4 small stars
            for sx, sy in [(flag_x + 15, flag_y + 4), (flag_x + 18, flag_y + 7), (flag_x + 18, flag_y + 11), (flag_x + 15, flag_y + 14)]:
                draw_star(draw, sx, sy, 1.8, "#ffde00")
        elif ftype == "RU":
            # White, blue, red tricolor
            sh = flag_h / 3
            draw.rectangle([(flag_x, flag_y), (flag_x + flag_w, flag_y + sh)], fill="#ffffff")
            draw.rectangle([(flag_x, flag_y + sh), (flag_x + flag_w, flag_y + 2 * sh)], fill="#0039a6")
            draw.rectangle([(flag_x, flag_y + 2 * sh), (flag_x + flag_w, flag_y + flag_h)], fill="#d52b1e")

def draw_hourglass(draw, ix, iy):
    """Draws an hourglass: two triangles and sand dots."""
    # Top and bottom base plates
    draw.line([(ix, iy), (ix + 40, iy)], fill=COLOR_INK, width=2)
    draw.line([(ix, iy + 44), (ix + 40, iy + 44)], fill=COLOR_INK, width=2)

    # Upper glass bulb
    draw.polygon([(ix + 4, iy + 2), (ix + 36, iy + 2), (ix + 20, iy + 22)], outline=COLOR_INK, width=2)
    # Lower glass bulb
    draw.polygon([(ix + 20, iy + 22), (ix + 4, iy + 42), (ix + 36, iy + 42)], outline=COLOR_INK, width=2)

    # Golden sand
    # Upper bulb draining sand
    draw.polygon([(ix + 10, iy + 12), (ix + 30, iy + 12), (ix + 20, iy + 21)], fill="#c8963e")
    # Falling stream and dots
    draw.line([(ix + 20, iy + 21), (ix + 20, iy + 32)], fill="#c8963e", width=1)
    draw.point([(ix + 20, iy + 25), (ix + 20, iy + 29)], fill="#c8963e")
    # Lower bulb accumulated sand mound
    draw.polygon([(ix + 8, iy + 42), (ix + 32, iy + 42), (ix + 20, iy + 33)], fill="#c8963e")

def draw_scales_of_justice(draw, ix, iy):
    """Draws scales of justice: a post, a beam, two pans."""
    # Central vertical post
    draw.line([(ix + 20, iy + 6), (ix + 20, iy + 44)], fill=COLOR_INK, width=2)
    # Sturdy base
    draw.line([(ix + 7, iy + 44), (ix + 33, iy + 44)], fill=COLOR_INK, width=2)
    # Top finial ball
    draw.ellipse([(ix + 18, iy + 4), (ix + 22, iy + 8)], fill=COLOR_INK)
    # Balanced cross beam
    draw.line([(ix + 2, iy + 12), (ix + 38, iy + 12)], fill=COLOR_INK, width=2)

    # Left pan
    draw.line([(ix + 4, iy + 12), (ix, iy + 25)], fill=COLOR_INK, width=1)
    draw.line([(ix + 12, iy + 12), (ix + 12, iy + 25)], fill=COLOR_INK, width=1)
    draw.arc([(ix - 2, iy + 21), (ix + 14, iy + 29)], 0, 180, fill=COLOR_INK, width=2)

    # Right pan
    draw.line([(ix + 28, iy + 12), (ix + 28, iy + 25)], fill=COLOR_INK, width=1)
    draw.line([(ix + 36, iy + 12), (ix + 40, iy + 25)], fill=COLOR_INK, width=1)
    draw.arc([(ix + 26, iy + 21), (ix + 42, iy + 29)], 0, 180, fill=COLOR_INK, width=2)

def draw_neon_sunset(draw, ix, iy):
    """Draws small neon-noir sunset panel: dark rounded rect, setting sun with scan lines, two palm silhouettes."""
    bx0, by0 = ix - 2, iy
    bx1, by1 = ix + 42, iy + 44
    draw.rounded_rectangle([(bx0, by0), (bx1, by1)], radius=6, fill="#120c24")

    # Setting sun semicircle
    draw.chord([(bx0 + 6, by0 + 11), (bx1 - 6, by1 + 11)], 180, 360, fill="#ff5a36")

    # Scan lines cutting across sun
    for sy in [by0 + 20, by0 + 24, by0 + 27]:
        draw.line([(bx0 + 5, sy), (bx1 - 5, sy)], fill="#120c24", width=1)

    # Left palm tree
    draw.line([(bx0 + 8, by1 - 2), (bx0 + 13, by0 + 22)], fill="#05030a", width=2)
    draw.arc([(bx0 + 6, by0 + 16), (bx0 + 18, by0 + 24)], 160, 350, fill="#05030a", width=1)
    draw.arc([(bx0 + 4, by0 + 18), (bx0 + 14, by0 + 26)], 180, 360, fill="#05030a", width=1)

    # Right palm tree
    draw.line([(bx1 - 10, by1 - 2), (bx1 - 14, by0 + 23)], fill="#05030a", width=2)
    draw.arc([(bx1 - 22, by0 + 17), (bx1 - 10, by0 + 25)], 190, 20, fill="#05030a", width=1)
    draw.arc([(bx1 - 20, by0 + 19), (bx1 - 8, by0 + 27)], 180, 10, fill="#05030a", width=1)

    # Cyan horizon glow
    draw.line([(bx0 + 4, by1 - 3), (bx1 - 4, by1 - 3)], fill="#00e5ff", width=1)

def draw_cyclone(draw, ix, iy):
    """Draws a cyclone spiral: concentric arcs."""
    cx, cy = ix + 20, iy + 22
    # Central storm eye
    draw.ellipse([(cx - 3, cy - 3), (cx + 3, cy + 3)], fill="#0f385c")
    # Swirling concentric arcs
    arc_layers = [
        (6, 30, 220, "#1d6996"),
        (10, 150, 340, "#2f80ed"),
        (14, 270, 100, "#1d6996"),
        (18, 30, 210, "#56ccf2"),
        (21, 160, 320, "#2f80ed"),
    ]
    for r, a0, a1, c in arc_layers:
        draw.arc([(cx - r, cy - r), (cx + r, cy + r)], a0, a1, fill=c, width=2)

def create_poster():
    img = Image.new("RGB", (WIDTH, HEIGHT), COLOR_PAPER)
    draw = ImageDraw.Draw(img)

    margin_x = 38
    content_w = WIDTH - 2 * margin_x  # 948px

    # --- 1. MASTHEAD ---
    # Top double rules
    draw.line([(margin_x, 26), (WIDTH - margin_x, 26)], fill=COLOR_INK, width=2)
    draw.line([(margin_x, 30), (WIDTH - margin_x, 30)], fill=COLOR_INK, width=1)

    # Letter-spaced small caps line
    font_mast_top = get_font(13, bold=True)
    draw_tracked_text(draw, (margin_x, 37), "THE WORLD IN ONE DAY", font_mast_top, COLOR_INK, spacing=8, center_width=content_w)

    # Huge bold date lines
    font_friday = get_font(84, bold=True)
    font_date = get_font(80, bold=True)
    friday_str = "FRIDAY"
    date_str = "20 NOVEMBER 2026"

    w_fri = font_friday.getlength(friday_str)
    w_date = font_date.getlength(date_str)

    draw.text((margin_x + (content_w - w_fri) / 2, 54), friday_str, font=font_friday, fill=COLOR_INK)
    draw.text((margin_x + (content_w - w_date) / 2, 132), date_str, font=font_date, fill=COLOR_INK)

    # Bottom masthead rules
    draw.line([(margin_x, 210), (WIDTH - margin_x, 210)], fill=COLOR_INK, width=2)
    draw.line([(margin_x, 214), (WIDTH - margin_x, 214)], fill=COLOR_INK, width=1)

    # --- 2. LEAD STORY ---
    lead_text_w = 600
    lead_panel_x = margin_x + lead_text_w + 22
    lead_panel_w = content_w - (lead_text_w + 22)

    # Red kicker
    font_kicker = get_font(14, bold=True)
    draw.text((margin_x, 224), "DIPLOMACY · SUMMIT", font=font_kicker, fill=COLOR_RED)

    # Headline bold ~52px
    font_lead_h = get_font(44, bold=True)
    lead_h_text = "TRUMP, XI AND PUTIN HOLD HISTORIC THREE-WAY MEETING"
    lead_h_lines = wrap_text(lead_h_text, font_lead_h, lead_text_w)
    cur_y = 248
    for line in lead_h_lines:
        draw.text((margin_x, cur_y), line, font=font_lead_h, fill=COLOR_INK)
        cur_y += 48

    # Sub ~25px
    font_lead_sub = get_font(20, bold=False)
    lead_sub_text = "First-ever trilateral summit in China ends with a joint peace declaration"
    lead_sub_lines = wrap_text(lead_sub_text, font_lead_sub, lead_text_w)
    cur_y += 6
    for line in lead_sub_lines:
        draw.text((margin_x, cur_y), line, font=font_lead_sub, fill=COLOR_SUB)
        cur_y += 26

    # Beside text: Dark visual panel (globe + 3 flags)
    draw_lead_panel(draw, lead_panel_x, 224, lead_panel_w, 228)

    # Divider below lead story
    draw.line([(margin_x, 462), (WIDTH - margin_x, 462)], fill=COLOR_INK, width=2)

    # --- 3. FOUR PANELS (2x2 GRID) ---
    col_w = (content_w - 24) / 2  # 462px
    col1_x = margin_x
    col2_x = margin_x + col_w + 24
    row1_y = 472
    row2_y = 646

    # Dividers
    mid_x = margin_x + col_w + 12
    draw.line([(mid_x, 468), (mid_x, 810)], fill=COLOR_RULE, width=1)
    draw.line([(margin_x, 638), (WIDTH - margin_x, 638)], fill=COLOR_RULE, width=1)

    font_panel_kicker = get_font(13, bold=True)
    font_panel_h = get_font(25, bold=True)
    font_panel_sub = get_font(16, bold=False)

    panels = [
        (
            col1_x, row1_y,
            "MIDDLE EAST · WAR",
            "TRUMP PUSHES IRAN WAR DECISION TO 2027",
            "President says he'll 'see what happens' after January 1; no rush on decision",
            "hourglass"
        ),
        (
            col2_x, row1_y,
            "JUSTICE · HUMAN RIGHTS",
            "ICJ: MYANMAR COMMITTED GENOCIDE AGAINST ROHINGYA",
            "Top UN court rules the 2017 crackdown aimed to destroy the minority",
            "scales"
        ),
        (
            col1_x, row2_y,
            "GAMING · CULTURE",
            "GTA 6 SALES PASS $1.80BN, TOP THE ODYSSEY",
            "Rockstar's blockbuster overtakes the biggest film opening in a day",
            "sunset"
        ),
        (
            col2_x, row2_y,
            "ASIA · WEATHER",
            "CYCLONE AKVAN: 300,000 EVACUATED IN ODISHA",
            "Rescue teams deploy as the severe storm nears India's east coast",
            "cyclone"
        ),
    ]

    for px, py, kicker, headline, sub, icon in panels:
        # Kicker
        draw.text((px, py), kicker, font=font_panel_kicker, fill=COLOR_RED)

        # Headline
        text_max_w = 410
        h_lines = wrap_text(headline, font_panel_h, text_max_w)
        y_text = py + 20
        for l in h_lines:
            draw.text((px, y_text), l, font=font_panel_h, fill=COLOR_INK)
            y_text += 29

        # Sub
        s_lines = wrap_text(sub, font_panel_sub, col_w - 12)
        y_text += 5
        for sl in s_lines:
            draw.text((px, y_text), sl, font=font_panel_sub, fill=COLOR_SUB)
            y_text += 20

        # Icon in top-right of panel
        icon_x = px + col_w - 44
        icon_y = py + 4
        if icon == "hourglass":
            draw_hourglass(draw, icon_x, icon_y)
        elif icon == "scales":
            draw_scales_of_justice(draw, icon_x, icon_y)
        elif icon == "sunset":
            draw_neon_sunset(draw, icon_x, icon_y)
        elif icon == "cyclone":
            draw_cyclone(draw, icon_x, icon_y)

    # Divider below grid
    draw.line([(margin_x, 814), (WIDTH - margin_x, 814)], fill=COLOR_INK, width=2)

    # --- 4. FULL-WIDTH STRIP ---
    strip_y = 824
    draw.text((margin_x, strip_y), "EUROPE · WAR & DIPLOMACY", font=font_panel_kicker, fill=COLOR_RED)

    font_strip_h = get_font(24, bold=True)
    draw.text((margin_x, strip_y + 22), "EUROPE READY FOR TALKS WITH RUSSIA TO END UKRAINE WAR", font=font_strip_h, fill=COLOR_INK)

    font_strip_sub = get_font(17.5, bold=False)
    draw.text((margin_x, strip_y + 54), "Leaders signal negotiations as strikes continue and the Crimean Bridge railway is hit", font=font_strip_sub, fill=COLOR_SUB)

    # Divider below strip
    draw.line([(margin_x, 916), (WIDTH - margin_x, 916)], fill=COLOR_RULE, width=1)

    # --- 5. BOTTOM TICKER ---
    bar_y0 = 926
    bar_y1 = 998
    draw.rectangle([(margin_x - 2, bar_y0), (WIDTH - margin_x + 2, bar_y1)], fill=COLOR_INK)

    font_ticker_bold = get_font(12, bold=True)
    font_ticker_reg = get_font(12, bold=False)

    prefix = "IN BRIEF — "
    ticker_line1_rest = "Van Gogh sells for record $190.4m · Hayabusa2 engine trouble ends asteroid landing plan · US and Venezuela sign military cooperation deal ·"
    ticker_line2 = "South Korea's top court clears ex-PM Han Duck-soo · Fiji declares disaster as drought bites · Anthropic valued at $1.5 trillion"

    ty1 = bar_y0 + 16
    draw.text((margin_x + 10, ty1), prefix, font=font_ticker_bold, fill="#ff4d4d")
    w_pref = font_ticker_bold.getlength(prefix)
    draw.text((margin_x + 10 + w_pref, ty1), ticker_line1_rest, font=font_ticker_reg, fill="#ffffff")

    ty2 = bar_y0 + 40
    draw.text((margin_x + 10, ty2), ticker_line2, font=font_ticker_reg, fill="#e6edf3")

    # Save output
    out_path = "entry.png"
    img.save(out_path, format="PNG", optimize=True)
    print(f"Saved {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == "__main__":
    create_poster()
