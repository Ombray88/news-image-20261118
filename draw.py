#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions
WIDTH, HEIGHT = 1024, 1024

# Colors
BG_PAPER = "#F7F3EA"
NAVY = "#1B2A4A"
TEXT_DARK = "#1E293B"
TEXT_MUTED = "#64748B"
BORDER_COLOR = "#E2D9C8"
WHITE = "#FFFFFF"

# Continent colors
CONTINENT_COLORS = {
    "Europe": "#C0392B",
    "Asia": "#0E7C7B",
    "Africa": "#D98E00",
    "North America": "#2E5FA3",
    "South America": "#3E8E41",
    "Oceania": "#7A4FA3",
}

# Fonts
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def get_font(size, bold=False):
    path = FONT_BOLD_PATH if bold else FONT_REG_PATH
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

# 35 Stories Data
STORIES = [
    # Heroes 1-3
    {
        "id": 1, "continent": "Asia", "category": "WAR",
        "headline": "Gulf strikes spread to Kuwait and Bahrain",
        "deck": "US jets hit a missile site on Iran's Qeshm Island. Iran says it fired at US sites in Kuwait and Bahrain; both report interception.",
        "lat": 26.2, "lon": 50.6, "badge": "3RD CARRIER · GULF"
    },
    {
        "id": 2, "continent": "Asia", "category": "DIPLOMACY",
        "headline": "Xi and Putin meet before Trump trilateral",
        "deck": "China's Xi and Russia's Putin meet in Shenzhen ahead of their three-way summit with US President Trump, who arrives from the Quad.",
        "lat": 22.5, "lon": 114.0, "badge": "SHENZHEN · APEC"
    },
    {
        "id": 3, "continent": "Europe", "category": "WAR",
        "headline": "Ukraine hits Crimea bridge a second day",
        "deck": "Ukraine says a strike collapsed part of the Kerch Bridge road span; Russia confirms damage and agrees to a major prisoner swap.",
        "lat": 45.3, "lon": 36.5, "badge": "2ND DAY · CRIMEA"
    },
    # Grid 4-15
    {
        "id": 4, "continent": "North America", "category": "POLITICS",
        "headline": "Peltola wins Alaska; Democrats take Senate",
        "deck": "Democrat Mary Peltola defeats Dan Sullivan in Alaska, securing a projected 56-44 Senate majority.",
        "lat": 61.2, "lon": -149.9
    },
    {
        "id": 5, "continent": "North America", "category": "TECH",
        "headline": "Nvidia rules out Huang return; revenue doubles",
        "deck": "Nvidia board will not reinstate Jensen Huang. Revenue surges 103% to $115.8B as inquiries continue.",
        "lat": 37.35, "lon": -121.95
    },
    {
        "id": 6, "continent": "Asia", "category": "DISASTER",
        "headline": "Cyclone Akvan bears down on India's east coast",
        "deck": "Severe storm heads for Andhra Pradesh; South Odisha begins large-scale evacuations.",
        "lat": 17.7, "lon": 83.3
    },
    {
        "id": 7, "continent": "Asia", "category": "CLIMATE",
        "headline": "COP31 opens in Antalya amid fossil-fuel rift",
        "deck": "Climate talks push 2035 electrification pledge; draft fossil-fuel phaseout divides nations.",
        "lat": 36.9, "lon": 30.7
    },
    {
        "id": 8, "continent": "Europe", "category": "POLITICS",
        "headline": "Latvia's new government takes office",
        "deck": "Andris Kulbergs' coalition takes office on Independence Day; defence gets 5% of GDP.",
        "lat": 56.95, "lon": 24.1
    },
    {
        "id": 9, "continent": "Africa", "category": "HEALTH",
        "headline": "Ebola in DR Congo passes 11,000 cases",
        "deck": "Outbreak passes 11,000 cases, largest toll of current epidemic, as health teams race.",
        "lat": -4.3, "lon": 15.3
    },
    {
        "id": 10, "continent": "North America", "category": "HEALTH",
        "headline": "US loses measles-free status after 26 years",
        "deck": "US loses measles-free status as cases spread; 13 babies born with measles this year.",
        "lat": 38.9, "lon": -77.0
    },
    {
        "id": 11, "continent": "Asia", "category": "SPORT",
        "headline": "Dhoni retires from the IPL",
        "deck": "MS Dhoni retires from Indian Premier League, ending one of cricket's most storied careers.",
        "lat": 13.08, "lon": 80.27
    },
    {
        "id": 12, "continent": "North America", "category": "OBITUARY",
        "headline": "Jesse Jackson dies at 84",
        "deck": "US civil rights leader Jesse Jackson dies at 84, closing a six-decade career for equality.",
        "lat": 41.88, "lon": -87.6
    },
    {
        "id": 13, "continent": "Asia", "category": "WAR",
        "headline": "Debris damages Aramco tower in Riyadh",
        "deck": "Attempted attack damages Aramco tower; no casualties reported as Gulf tensions spread.",
        "lat": 24.7, "lon": 46.7
    },
    {
        "id": 14, "continent": "Europe", "category": "SPORT",
        "headline": "Alcaraz beats Medvedev at ATP Finals",
        "deck": "Carlos Alcaraz beats Daniil Medvedev 6-2, 6-4 at the ATP Finals in Turin.",
        "lat": 45.07, "lon": 7.69
    },
    {
        "id": 15, "continent": "Oceania", "category": "SPORT",
        "headline": "England win ODI series in Hobart",
        "deck": "Ben Duckett's 133 takes England to a 97-run win over Australia and 2-1 series victory.",
        "lat": -42.88, "lon": 147.32
    },
    # Also list 16-35
    { "id": 16, "continent": "Asia", "category": "DIPLOMACY", "headline": "Quad agrees joint patrol flights and minerals deals", "lat": 14.6, "lon": 121.0 },
    { "id": 17, "continent": "North America", "category": "COURTS", "headline": "Merchant gets 27.5 years over Trump plot", "lat": 40.7, "lon": -74.0 },
    { "id": 18, "continent": "Asia", "category": "DIPLOMACY", "headline": "Herzog taps Eisenkot to form Israel's government", "lat": 31.8, "lon": 35.2 },
    { "id": 19, "continent": "Asia", "category": "DIPLOMACY", "headline": "ASEAN sets terms for Myanmar's return", "lat": -6.2, "lon": 106.8 },
    { "id": 20, "continent": "Europe", "category": "DIPLOMACY", "headline": "Iran and US to hold nuclear talks in Geneva", "lat": 46.2, "lon": 6.14 },
    { "id": 21, "continent": "Africa", "category": "DIPLOMACY", "headline": "Chad closes its border with Sudan", "lat": 12.1, "lon": 15.0 },
    { "id": 22, "continent": "Africa", "category": "DIPLOMACY", "headline": "Nigeria bids for UN Human Rights Council seat", "lat": 9.06, "lon": 7.49 },
    { "id": 23, "continent": "North America", "category": "WEATHER", "headline": "New York orders travel ban as major storm hits", "lat": 40.7, "lon": -74.0 },
    { "id": 24, "continent": "Asia", "category": "DISASTER", "headline": "Death toll rises to 16 in Pakistan building blast", "lat": 24.86, "lon": 67.0 },
    { "id": 25, "continent": "Asia", "category": "DISASTER", "headline": "Over 600 die in Afghan earthquake", "lat": 34.5, "lon": 69.2 },
    { "id": 26, "continent": "North America", "category": "SECURITY", "headline": "Cartel violence grips Mexico after El Mencho's death", "lat": 19.43, "lon": -99.13 },
    { "id": 27, "continent": "Asia", "category": "DIPLOMACY", "headline": "India urges its citizens to leave Iran", "lat": 28.6, "lon": 77.2 },
    { "id": 28, "continent": "Europe", "category": "DIPLOMACY", "headline": "Australia & UK sanction Israeli settlement expansion", "lat": 51.5, "lon": -0.12 },
    { "id": 29, "continent": "Asia", "category": "WAR", "headline": "Gaza ceasefire strains as Board faults both sides", "lat": 31.5, "lon": 34.47 },
    { "id": 30, "continent": "North America", "category": "TECH", "headline": "OpenAI launches GPT-6.2 Astra and Sol", "lat": 37.77, "lon": -122.42 },
    { "id": 31, "continent": "North America", "category": "DIPLOMACY", "headline": "Carney meets Trump at APEC in Shenzhen", "lat": 45.42, "lon": -75.69 },
    { "id": 32, "continent": "Europe", "category": "POLITICS", "headline": "Le Pen proposes lower French retirement age", "lat": 48.85, "lon": 2.35 },
    { "id": 33, "continent": "Europe", "category": "WAR", "headline": "France rejects Russian claims on secret Ukraine mission", "lat": 48.85, "lon": 2.6 },
    { "id": 34, "continent": "South America", "category": "SPORT", "headline": "Argentina rout Costa Rica 7-0 in friendly", "lat": -34.6, "lon": -58.38 },
    { "id": 35, "continent": "Africa", "category": "SPORT", "headline": "South Africa beat Kenya 2-1 in AFCON qualifier", "lat": -1.29, "lon": 36.82 },
]

def wrap_text(text, font, max_width, draw):
    """Helper to wrap text into lines fitting max_width."""
    words = text.split()
    if not words:
        return []
    lines = []
    current_line = words[0]
    for word in words[1:]:
        test_line = current_line + " " + word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if (bbox[2] - bbox[0]) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return lines

def main():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_PAPER)
    draw = ImageDraw.Draw(img)

    # 1. MASTHEAD (y = 0 to 92)
    draw.rectangle([0, 0, WIDTH, 92], fill=NAVY)
    
    # Kicker & Date
    f_kicker = get_font(10, bold=True)
    f_date = get_font(22, bold=True)
    f_meta = get_font(10, bold=False)
    
    draw.text((24, 12), "THE DAY IN WORLD NEWS", fill="#D4AF37", font=f_kicker)
    draw.text((24, 28), "WEDNESDAY 18 NOVEMBER 2026", fill=WHITE, font=f_date)
    
    # Right side meta & legend
    draw.text((WIDTH - 24, 16), "35 STORIES · 6 CONTINENTS", fill=WHITE, font=f_meta, anchor="rt")
    
    # Legend row
    continents = ["Europe", "Asia", "Africa", "North America", "South America", "Oceania"]
    lx = WIDTH - 24
    ly = 64
    for cont in reversed(continents):
        color = CONTINENT_COLORS[cont]
        tbox = draw.textbbox((0, 0), cont, font=f_meta)
        t_w = tbox[2] - tbox[0]
        lx -= t_w
        draw.text((lx, ly - 4), cont, fill="#CBD5E1", font=f_meta)
        lx -= 12
        draw.ellipse([lx, ly, lx + 8, ly + 8], fill=color)
        lx -= 16

    # 2. HERO ROW (y = 104 to 348, height 244)
    hero_y = 104
    hero_h = 244
    hero_w = 312
    hero_gap = 24
    hero_x_start = 20

    f_hero_head = get_font(15, bold=True)
    f_hero_deck = get_font(11, bold=False)
    f_badge = get_font(9, bold=True)

    for i in range(3):
        h_data = STORIES[i]
        hx = hero_x_start + i * (hero_w + hero_gap)
        hy = hero_y
        
        # Card background
        draw.rectangle([hx, hy, hx + hero_w, hy + hero_h], fill=WHITE, outline=BORDER_COLOR, width=1)
        
        # Accent top border
        c_color = CONTINENT_COLORS[h_data["continent"]]
        draw.rectangle([hx, hy, hx + hero_w, hy + 4], fill=c_color)

        # Illustration box on top
        ill_box_h = 75
        draw.rectangle([hx + 12, hy + 14, hx + hero_w - 12, hy + 14 + ill_box_h], fill="#F1ECE1")
        
        # Enhanced recognisable flat pictograms
        if i == 0:
            # Gulf War: Ship hull, radar waves & missile trajectory
            draw.arc([hx + 30, hy + 35, hx + 80, hy + 85], 180, 360, fill=c_color, width=3)
            draw.line([hx + 25, hy + 75, hx + 85, hy + 75], fill=c_color, width=3)
            draw.arc([hx + 90, hy + 30, hx + 140, hy + 80], 225, 315, fill=TEXT_MUTED, width=2)
            draw.arc([hx + 100, hy + 20, hx + 150, hy + 70], 225, 315, fill=TEXT_MUTED, width=2)
            draw.line([hx + 130, hy + 65, hx + 180, hy + 35], fill=c_color, width=2)
        elif i == 1:
            # Shenzhen / APEC: Skyline towers & flag
            # Buildings
            draw.rectangle([hx + 35, hy + 45, hx + 65, hy + 85], fill=c_color)
            draw.rectangle([hx + 70, hy + 30, hx + 105, hy + 85], fill=NAVY)
            draw.rectangle([hx + 110, hy + 40, hx + 140, hy + 85], fill=c_color)
            draw.rectangle([hx + 145, hy + 50, hx + 175, hy + 85], fill=TEXT_MUTED)
            # Flag pole and pennant
            draw.line([hx + 185, hy + 25, hx + 185, hy + 85], fill=TEXT_DARK, width=2)
            draw.polygon([(hx + 185, hy + 25), (hx + 205, hy + 33), (hx + 185, hy + 41)], fill=c_color)
        else:
            # Crimea Bridge: Bridge span, piers and suspension cables
            draw.line([hx + 30, hy + 65, hx + 180, hy + 65], fill=TEXT_DARK, width=4) # deck
            draw.rectangle([hx + 55, hy + 65, hx + 63, hy + 85], fill=c_color) # pier 1
            draw.rectangle([hx + 115, hy + 65, hx + 123, hy + 85], fill=c_color) # pier 2
            draw.line([hx + 59, hy + 65, hx + 59, hy + 35], fill=c_color, width=2) # tower 1
            draw.line([hx + 119, hy + 65, hx + 119, hy + 35], fill=c_color, width=2) # tower 2
            draw.line([hx + 30, hy + 65, hx + 59, hy + 35], fill=TEXT_MUTED, width=1)
            draw.line([hx + 59, hy + 35, hx + 119, hy + 35], fill=TEXT_MUTED, width=1)
            draw.line([hx + 119, hy + 35, hx + 180, hy + 65], fill=TEXT_MUTED, width=1)

        # Data badge pill inside illustration
        if "badge" in h_data:
            badge_text = h_data["badge"]
            bbox = draw.textbbox((0, 0), badge_text, font=f_badge)
            bw = bbox[2] - bbox[0] + 12
            bh = 18
            bx_pill = hx + hero_w - 18 - bw
            by_pill = hy + 20
            draw.rounded_rectangle([bx_pill, by_pill, bx_pill + bw, by_pill + bh], radius=4, fill=NAVY)
            draw.text((bx_pill + 6, by_pill + 3), badge_text, fill=WHITE, font=f_badge)

        # Number badge
        num_r = 12
        num_cx = hx + 24
        num_cy = hy + 26
        draw.ellipse([num_cx - num_r, num_cy - num_r, num_cx + num_r, num_cy + num_r], fill=c_color)
        f_num = get_font(11, bold=True)
        draw.text((num_cx, num_cy - 1), str(h_data["id"]), fill=WHITE, font=f_num, anchor="mm")

        # Headline
        text_y = hy + 98
        head_lines = wrap_text(h_data["headline"], f_hero_head, hero_w - 24, draw)
        for hl in head_lines[:2]:
            draw.text((hx + 12, text_y), hl, fill=TEXT_DARK, font=f_hero_head)
            text_y += 18

        # Deck
        text_y += 4
        deck_lines = wrap_text(h_data["deck"], f_hero_deck, hero_w - 24, draw)
        for dl in deck_lines[:3]:
            draw.text((hx + 12, text_y), dl, fill=TEXT_MUTED, font=f_hero_deck)
            text_y += 14


    # 3. GRID 4-15 (y = 360 to 710, 3 rows x 4 cols)
    grid_y = 360
    cols = 4
    gw = 234
    gh = 108
    g_gap_x = 16
    g_gap_y = 10
    g_x_start = 20
    g_y_start = grid_y

    f_grid_head = get_font(12, bold=True)
    f_grid_deck = get_font(9, bold=False)
    f_cat = get_font(8, bold=True)
    f_num_small = get_font(9, bold=True)

    for idx, story in enumerate(STORIES[3:15]):
        r = idx // cols
        c = idx % cols
        gx = g_x_start + c * (gw + g_gap_x)
        gy = g_y_start + r * (gh + g_gap_y)

        draw.rectangle([gx, gy, gx + gw, gy + gh], fill=WHITE, outline=BORDER_COLOR, width=1)
        c_color = CONTINENT_COLORS[story["continent"]]
        draw.rectangle([gx, gy, gx + 3, gy + gh], fill=c_color)

        # Number badge & Category pill
        draw.ellipse([gx + 12, gy + 10, gx + 28, gy + 26], fill=c_color)
        draw.text((gx + 20, gy + 18), str(story["id"]), fill=WHITE, font=f_num_small, anchor="mm")

        cat_text = story["category"]
        cbox = draw.textbbox((0, 0), cat_text, font=f_cat)
        cw = cbox[2] - cbox[0] + 8
        draw.rounded_rectangle([gx + 34, gy + 10, gx + 34 + cw, gy + 24], radius=3, fill="#F1ECE1")
        draw.text((gx + 38, gy + 12), cat_text, fill=TEXT_MUTED, font=f_cat)

        # Headline
        text_y = gy + 32
        head_lines = wrap_text(story["headline"], f_grid_head, gw - 24, draw)
        for hl in head_lines[:2]:
            draw.text((gx + 12, text_y), hl, fill=TEXT_DARK, font=f_grid_head)
            text_y += 15

        # Deck
        text_y += 2
        deck_lines = wrap_text(story["deck"], f_grid_deck, gw - 24, draw)
        for dl in deck_lines[:2]:
            draw.text((gx + 12, text_y), dl, fill=TEXT_MUTED, font=f_grid_deck)
            text_y += 12


    # 4. BOTTOM SECTION (y = 722 to 980)
    bot_y = 722
    bot_h = 252
    
    # Left Box: WHERE IT HAPPENED (width 430)
    lw = 430
    draw.rectangle([20, bot_y, 20 + lw, bot_y + bot_h], fill=WHITE, outline=BORDER_COLOR, width=1)
    
    f_sec_title = get_font(11, bold=True)
    draw.text((36, bot_y + 12), "WHERE IT HAPPENED · MAP & PINS 1–35", fill=NAVY, font=f_sec_title)

    # Load worldmap.txt and render dot matrix map
    with open("worldmap.txt") as f:
        map_lines = [line.strip() for line in f if line.strip()]
    
    map_x0 = 40
    map_y0 = bot_y + 36
    map_w = lw - 40
    map_h = 160

    rows_m = len(map_lines)
    cols_m = len(map_lines[0]) if rows_m > 0 else 96

    # Draw dot matrix map background (clipped to map area)
    for r_idx, r_line in enumerate(map_lines):
        for c_idx, ch in enumerate(r_line):
            if ch == '#':
                px = map_x0 + (c_idx / cols_m) * map_w
                py = map_y0 + (r_idx / rows_m) * map_h
                if py <= map_y0 + map_h:
                    draw.rectangle([px, py, px + 1.8, py + 1.8], fill="#4A5568")

    # Plot pins for 1-15 and dots for 16-35 (clipped to map area)
    for story in STORIES:
        lat = story["lat"]
        lon = story["lon"]
        px = map_x0 + ((lon + 180) / 360.0) * map_w
        py = map_y0 + ((90.0 - lat) / 180.0) * map_h
        c_color = CONTINENT_COLORS[story["continent"]]
        
        if map_y0 <= py <= map_y0 + map_h:
            if story["id"] <= 15:
                pr = 7
                draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=c_color, outline=WHITE, width=2)
                f_ppin = get_font(8, bold=True)
                draw.text((px, py - 0.5), str(story["id"]), fill=WHITE, font=f_ppin, anchor="mm")
            else:
                pr = 2.5
                draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=c_color, outline=WHITE, width=1)

    # Right Box: ALSO ON WEDNESDAY 18 NOVEMBER (width 550, x = 462 to 1004)
    rx = 462
    rw = WIDTH - 24 - rx
    draw.rectangle([rx, bot_y, rx + rw, bot_y + bot_h], fill=WHITE, outline=BORDER_COLOR, width=1)
    
    draw.text((rx + 16, bot_y + 12), "ALSO ON WEDNESDAY 18 NOVEMBER (16–35)", fill=NAVY, font=f_sec_title)

    # Render list 16-35 in two columns with font size 9 so everything fits on one line without truncation
    f_also = get_font(9, bold=False)
    f_also_num = get_font(9, bold=True)
    
    col1_items = STORIES[15:25] # 16-25
    col2_items = STORIES[25:35] # 26-35

    def draw_also_column(items, start_x, start_y):
        sy = start_y
        for item in items:
            num_str = f"{item['id']:2d}."
            draw.text((start_x, sy), num_str, fill=CONTINENT_COLORS[item['continent']], font=f_also_num)
            headline = item['headline']
            draw.text((start_x + 24, sy), headline, fill=TEXT_DARK, font=f_also)
            sy += 21

    draw_also_column(col1_items, rx + 16, bot_y + 36)
    draw_also_column(col2_items, rx + (rw / 2) + 8, bot_y + 36)


    # 5. FOOTER (y = 984 to 1024)
    draw.rectangle([0, 984, WIDTH, HEIGHT], fill=NAVY)
    f_footer = get_font(10, bold=False)
    footer_text = "Every story happened or was first reported on Wednesday 18 November 2026. Disputed claims are attributed. Sources: AP · Reuters · AFP · BBC · Al Jazeera · UN News · Original drawings"
    draw.text((WIDTH / 2, 1004), footer_text, fill="#CBD5E1", font=f_footer, anchor="mm")

    # Save output
    output_path = "entry.png"
    img.save(output_path, "PNG", optimize=True)
    size_kb = os.path.getsize(output_path) / 1024
    print(f"Saved {output_path} ({size_kb:.1f} KB)")

if __name__ == "__main__":
    main()
