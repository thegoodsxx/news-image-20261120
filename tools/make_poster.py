#!/usr/bin/env python3
"""
tools/make_poster.py - Broadsheet front-page poster generator for news-image-20261120.
Generates entry.png (1024x1024) summing up world news of 20 November 2026.
"""

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
COLOR_MUTED = "#828c99"
COLOR_RULE = "#c8c2b0"

# Fonts
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

def draw_tracked_text(draw, xy, text, font, fill, spacing=6, center_width=None):
    total_w = sum(font.getlength(ch) for ch in text) + spacing * (len(text) - 1)
    x, y = xy
    if center_width is not None:
        x = x + (center_width - total_w) / 2
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += font.getlength(ch) + spacing

def create_poster():
    img = Image.new("RGB", (WIDTH, HEIGHT), COLOR_PAPER)
    draw = ImageDraw.Draw(img)

    # Margins
    margin_x = 38
    content_w = WIDTH - 2 * margin_x  # 948px

    # --- MASTHEAD ---
    # Top rule
    draw.line([(margin_x, 26), (WIDTH - margin_x, 26)], fill=COLOR_INK, width=2)

    # Letter-spaced small caps
    font_mast_top = get_font(13, bold=True)
    draw_tracked_text(draw, (margin_x, 34), "THE WORLD IN ONE DAY", font_mast_top, COLOR_INK, spacing=8, center_width=content_w)

    # Date lines (huge bold type)
    font_date = get_font(78, bold=True)
    friday_str = "FRIDAY"
    date_str = "20 NOVEMBER 2026"

    w_fri = font_date.getlength(friday_str)
    w_date = font_date.getlength(date_str)

    draw.text((margin_x + (content_w - w_fri) / 2, 54), friday_str, font=font_date, fill=COLOR_INK)
    draw.text((margin_x + (content_w - w_date) / 2, 130), date_str, font=font_date, fill=COLOR_INK)

    # Bottom masthead rules
    draw.line([(margin_x, 208), (WIDTH - margin_x, 208)], fill=COLOR_INK, width=2)
    draw.line([(margin_x, 212), (WIDTH - margin_x, 212)], fill=COLOR_INK, width=1)

    # --- LEAD STORY ---
    # y = 224 to 455
    lead_text_w = 600
    lead_panel_x = margin_x + lead_text_w + 24
    lead_panel_w = content_w - (lead_text_w + 24)

    # Kicker
    font_kicker = get_font(14, bold=True)
    draw.text((margin_x, 222), "DIPLOMACY · SUMMIT", font=font_kicker, fill=COLOR_RED)

    # Headline
    font_lead_h = get_font(42, bold=True)
    lead_h_text = "TRUMP, XI AND PUTIN HOLD HISTORIC THREE-WAY MEETING"
    lead_h_lines = wrap_text(lead_h_text, font_lead_h, lead_text_w)
    y_text = 246
    for line in lead_h_lines:
        draw.text((margin_x, y_text), line, font=font_lead_h, fill=COLOR_INK)
        y_text += 46

    # Sub
    font_lead_sub = get_font(19, bold=False)
    lead_sub_text = "First-ever trilateral summit in China ends with a joint peace declaration"
    lead_sub_lines = wrap_text(lead_sub_text, font_lead_sub, lead_text_w)
    y_text += 8
    for line in lead_sub_lines:
        draw.text((margin_x, y_text), line, font=font_lead_sub, fill=COLOR_SUB)
        y_text += 26

    # Beside text: Dark panel with globe and 3 flags
    panel_y0 = 224
    panel_y1 = 456
    draw.rounded_rectangle([(lead_panel_x, panel_y0), (lead_panel_x + lead_panel_w, panel_y1)], radius=8, fill=COLOR_INK)

    # Globe in dark panel
    globe_cx = lead_panel_x + lead_panel_w / 2
    globe_cy = panel_y0 + 95
    globe_r = 54
    draw.ellipse([(globe_cx - globe_r, globe_cy - globe_r), (globe_cx + globe_r, globe_cy + globe_r)], outline="#5a6878", width=2)
    # Equator and meridian arcs
    draw.line([(globe_cx - globe_r, globe_cy), (globe_cx + globe_r, globe_cy)], fill="#5a6878", width=1)
    draw.arc([(globe_cx - globe_r * 0.6, globe_cy - globe_r), (globe_cx + globe_r * 0.6, globe_cy + globe_r)], 0, 360, fill="#5a6878", width=1)
    draw.arc([(globe_cx - globe_r * 0.25, globe_cy - globe_r), (globe_cx + globe_r * 0.25, globe_cy + globe_r)], 0, 360, fill="#5a6878", width=1)
    draw.arc([(globe_cx - globe_r, globe_cy - globe_r * 0.5), (globe_cx + globe_r, globe_cy + globe_r * 0.5)], 0, 360, fill="#404c5a", width=1)

    # Three flags on poles below globe
    # Flag poles
    pole_y_top = panel_y0 + 160
    pole_y_bot = panel_y1 - 18
    flag_w = 42
    flag_h = 24

    flags = [
        (lead_panel_x + 36, "US"),
        (globe_cx - flag_w / 2, "CN"),
        (lead_panel_x + lead_panel_w - 36 - flag_w, "RU"),
    ]

    for fx, ftype in flags:
        # Pole
        draw.line([(fx, pole_y_top), (fx, pole_y_bot)], fill="#c0c8d0", width=2)
        draw.ellipse([(fx - 2, pole_y_top - 3), (fx + 2, pole_y_top + 1)], fill="#f0c040")
        
        # Flag body
        fr = [(fx + 1, pole_y_top + 2), (fx + flag_w, pole_y_top + 2 + flag_h)]
        if ftype == "US":
            # Red and white stripes + canton
            draw.rectangle(fr, fill="#b22234")
            for sy in range(2, flag_h, 4):
                draw.line([(fx + 1, pole_y_top + 2 + sy), (fx + flag_w, pole_y_top + 2 + sy)], fill="#ffffff", width=2)
            # Blue canton
            draw.rectangle([(fx + 1, pole_y_top + 2), (fx + flag_w * 0.45, pole_y_top + 2 + flag_h * 0.55)], fill="#3c3b6e")
        elif ftype == "CN":
            # Red + small gold stars
            draw.rectangle(fr, fill="#de2910")
            draw.ellipse([(fx + 4, pole_y_top + 5), (fx + 10, pole_y_top + 11)], fill="#ffde00")
            draw.rectangle([(fx + 13, pole_y_top + 4), (fx + 15, pole_y_top + 6)], fill="#ffde00")
            draw.rectangle([(fx + 15, pole_y_top + 8), (fx + 17, pole_y_top + 10)], fill="#ffde00")
        elif ftype == "RU":
            # White, blue, red horizontal stripes
            sh = flag_h / 3
            draw.rectangle([(fx + 1, pole_y_top + 2), (fx + flag_w, pole_y_top + 2 + sh)], fill="#ffffff")
            draw.rectangle([(fx + 1, pole_y_top + 2 + sh), (fx + flag_w, pole_y_top + 2 + 2 * sh)], fill="#0039a6")
            draw.rectangle([(fx + 1, pole_y_top + 2 + 2 * sh), (fx + flag_w, pole_y_top + 2 + flag_h)], fill="#d52b1e")

    # Divider below lead story
    draw.line([(margin_x, 470), (WIDTH - margin_x, 470)], fill=COLOR_INK, width=2)

    # --- FOUR PANELS (2x2 GRID) ---
    col_w = (content_w - 24) / 2  # 462px
    col1_x = margin_x
    col2_x = margin_x + col_w + 24
    row1_y = 482
    row2_y = 654
    panel_h = 158

    # Grid dividers
    mid_x = margin_x + col_w + 12
    draw.line([(mid_x, 476), (mid_x, 816)], fill=COLOR_RULE, width=1)
    draw.line([(margin_x, 644), (WIDTH - margin_x, 644)], fill=COLOR_RULE, width=1)

    font_panel_kicker = get_font(13, bold=True)
    font_panel_h = get_font(27, bold=True)
    font_panel_sub = get_font(16, bold=False)

    panels = [
        # (col_x, row_y, kicker, headline, sub, icon_type)
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
        text_max_w = col_w - 68  # reserve 68px for icon on right
        h_lines = wrap_text(headline, font_panel_h, text_max_w)
        cur_y = py + 22
        for l in h_lines:
            draw.text((px, cur_y), l, font=font_panel_h, fill=COLOR_INK)
            cur_y += 31

        # Sub
        s_lines = wrap_text(sub, font_panel_sub, col_w - 10)
        cur_y += 6
        for sl in s_lines:
            draw.text((px, cur_y), sl, font=font_panel_sub, fill=COLOR_SUB)
            cur_y += 20

        # Draw icon
        icon_x = px + col_w - 54
        icon_y = py + 4
        if icon == "hourglass":
            # Hourglass: two triangles and sand dots
            draw.polygon([(icon_x, icon_y), (icon_x + 40, icon_y), (icon_x + 20, icon_y + 24)], outline=COLOR_INK, fill=None, width=2)
            draw.polygon([(icon_x + 20, icon_y + 24), (icon_x, icon_y + 48), (icon_x + 40, icon_y + 48)], outline=COLOR_INK, fill=None, width=2)
            draw.line([(icon_x - 4, icon_y), (icon_x + 44, icon_y)], fill=COLOR_INK, width=2)
            draw.line([(icon_x - 4, icon_y + 48), (icon_x + 44, icon_y + 48)], fill=COLOR_INK, width=2)
            # Sand
            draw.polygon([(icon_x + 12, icon_y + 42), (icon_x + 28, icon_y + 42), (icon_x + 20, icon_y + 30)], fill="#d49b42")
            draw.point([(icon_x + 20, icon_y + 22), (icon_x + 20, icon_y + 26)], fill="#d49b42")
        elif icon == "scales":
            # Scales of justice: post, beam, two pans
            # Post
            draw.line([(icon_x + 20, icon_y + 6), (icon_x + 20, icon_y + 48)], fill=COLOR_INK, width=2)
            draw.line([(icon_x + 8, icon_y + 48), (icon_x + 32, icon_y + 48)], fill=COLOR_INK, width=2)
            # Beam
            draw.line([(icon_x + 2, icon_y + 12), (icon_x + 38, icon_y + 12)], fill=COLOR_INK, width=2)
            # Left pan
            draw.line([(icon_x + 2, icon_y + 12), (icon_x - 2, icon_y + 26)], fill=COLOR_INK, width=1)
            draw.line([(icon_x + 10, icon_y + 12), (icon_x + 10, icon_y + 26)], fill=COLOR_INK, width=1)
            draw.arc([(icon_x - 4, icon_y + 22), (icon_x + 12, icon_y + 30)], 0, 180, fill=COLOR_INK, width=2)
            # Right pan
            draw.line([(icon_x + 30, icon_y + 12), (icon_x + 30, icon_y + 26)], fill=COLOR_INK, width=1)
            draw.line([(icon_x + 38, icon_y + 12), (icon_x + 42, icon_y + 26)], fill=COLOR_INK, width=1)
            draw.arc([(icon_x + 28, icon_y + 22), (icon_x + 44, icon_y + 30)], 0, 180, fill=COLOR_INK, width=2)
        elif icon == "sunset":
            # Neon-noir sunset panel: dark rounded rectangle, setting sun semicircle with scan lines, two palms
            bx0, by0, bx1, by1 = icon_x - 4, icon_y, icon_x + 44, icon_y + 48
            draw.rounded_rectangle([(bx0, by0), (bx1, by1)], radius=4, fill="#1a102e")
            # Setting sun
            draw.chord([(bx0 + 8, by0 + 10), (bx1 - 8, by1 + 10)], 180, 360, fill="#ff5e36")
            # Scanlines
            for sl_y in [by0 + 20, by0 + 25, by0 + 29]:
                draw.line([(bx0 + 6, sl_y), (bx1 - 6, sl_y)], fill="#1a102e", width=1)
            # Two palm tree silhouettes
            draw.line([(bx0 + 10, by1 - 2), (bx0 + 14, by0 + 26)], fill="#0d0818", width=2)
            draw.arc([(bx0 + 8, by0 + 20), (bx0 + 20, by0 + 28)], 160, 340, fill="#0d0818", width=1)
            draw.line([(bx1 - 12, by1 - 2), (bx1 - 15, by0 + 28)], fill="#0d0818", width=2)
            draw.arc([(bx1 - 22, by0 + 22), (bx1 - 10, by0 + 30)], 200, 20, fill="#0d0818", width=1)
        elif icon == "cyclone":
            # Cyclone spiral: concentric arcs
            cx, cy = icon_x + 20, icon_y + 24
            for r in [8, 14, 20]:
                draw.arc([(cx - r, cy - r), (cx + r, cy + r)], 30, 220, fill="#2b5070", width=2)
                draw.arc([(cx - r * 0.8, cy - r * 0.8), (cx + r * 0.8, cy + r * 0.8)], 210, 40, fill="#4a769e", width=2)

    # Divider below grid
    draw.line([(margin_x, 822), (WIDTH - margin_x, 822)], fill=COLOR_INK, width=2)

    # --- FULL-WIDTH STRIP ---
    strip_y = 832
    draw.text((margin_x, strip_y), "EUROPE · WAR & DIPLOMACY", font=font_panel_kicker, fill=COLOR_RED)

    font_strip_h = get_font(24, bold=True)
    draw.text((margin_x, strip_y + 20), "EUROPE READY FOR TALKS WITH RUSSIA TO END UKRAINE WAR", font=font_strip_h, fill=COLOR_INK)

    font_strip_sub = get_font(18, bold=False)
    draw.text((margin_x, strip_y + 52), "Leaders signal negotiations as strikes continue and the Crimean Bridge railway is hit", font=font_strip_sub, fill=COLOR_SUB)

    # --- BOTTOM TICKER ---
    # Black bar
    bar_y0 = 926
    bar_y1 = 998
    draw.rectangle([(margin_x, bar_y0), (WIDTH - margin_x, bar_y1)], fill=COLOR_INK)

    font_ticker = get_font(12, bold=False)
    ticker_line1 = "IN BRIEF — Van Gogh sells for record $190.4m · Hayabusa2 engine trouble ends asteroid landing plan · US and Venezuela sign military cooperation deal"
    ticker_line2 = "South Korea's top court clears ex-PM Han Duck-soo · Fiji declares disaster as drought bites · Anthropic valued at $1.5 trillion"

    draw.text((margin_x + 16, bar_y0 + 16), ticker_line1, font=font_ticker, fill="#ffffff")
    draw.text((margin_x + 16, bar_y0 + 40), ticker_line2, font=font_ticker, fill="#f0f0f0")

    # Save entry.png
    out_path = "entry.png"
    img.save(out_path, format="PNG", optimize=True)
    print(f"Saved {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == "__main__":
    create_poster()
