#!/usr/bin/env python3
"""THE WORLD TODAY - Thursday 19 November 2026.

A one-page broadsheet front page rendered as a 1024x1024 PNG using only
the Python standard library. The program draws its own 5x7 bitmap font,
a stylised world map, a sunset Vice City skyline, and twelve real
headlines from the wires of 19 November 2026.

Output: exactly one file, entry.png, written to MAKEFUN_OUTPUT_DIR
(the grader mounts the repository read-only at /bot and gives us an
empty writable /output, so we never write to the current directory).
Deterministic: two runs produce byte-identical output.
"""

import os
import struct
import zlib

W, H = 1024, 1024

PAPER = (251, 243, 220)
INK = (18, 18, 18)
RED = (176, 30, 30)
BLUE = (28, 68, 128)
GREY = (112, 106, 94)
LIGHT = (236, 226, 198)
SEA = (216, 230, 238)
LAND = (176, 198, 158)
SUNSET_TOP = (255, 176, 102)
SUNSET_MID = (255, 120, 90)
SUNSET_LOW = (214, 74, 110)
SKYLINE = (48, 32, 48)

# 5x7 bitmap font: each glyph is 7 rows of 5 characters ('#' = ink).
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
}

FONT.update({
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    '-': ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '$': ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '+': ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '@': ("01110", "10001", "10111", "10101", "10110", "10000", "01110"),
    '#': ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    '*': ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
    'v': ("00000", "00000", "00000", "10001", "10001", "01010", "00100"),
    '^': ("00100", "01010", "10001", "00000", "00000", "00000", "00000"),
})


class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.buf = bytearray(bg[0] for _ in range(w * h))
        self.buf = bytearray(w * h * 3)
        for i in range(w * h):
            self.buf[3 * i:3 * i + 3] = bytes(bg)

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = 3 * (y * self.w + x)
            self.buf[i:i + 3] = bytes(c)

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.px(xx, yy, c)

    def hline(self, x, y, w, c):
        self.rect(x, y, w, 1, c)

    def vline(self, x, y, h, c):
        self.rect(x, y, 1, h, c)

    def line(self, x0, y0, x1, y1, c):
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.px(x0, y0, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, c, fill=True):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d = (xx - cx) ** 2 + (yy - cy) ** 2
                if fill and d <= r * r:
                    self.px(xx, yy, c)
                elif not fill and r * r - 2 * r <= d <= r * r:
                    self.px(xx, yy, c)

    def poly(self, pts, c):
        # Scanline fill for a simple (non self-intersecting) polygon.
        ys = [p[1] for p in pts]
        for y in range(min(ys), max(ys) + 1):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for j in range(0, len(xs) - 1, 2):
                for x in range(int(xs[j]), int(xs[j + 1]) + 1):
                    self.px(x, y, c)


def text_width(s, scale):
    return len(s) * 6 * scale - scale


def draw_text(cv, x, y, s, scale, color):
    s = s.upper()
    cx = x
    for ch in s:
        glyph = FONT.get(ch, FONT[' '])
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == '1':
                    cv.rect(cx + col * scale, y + row * scale, scale, scale, color)
        cx += 6 * scale
    return cx


def wrap_text(s, scale, max_w):
    words = s.split(' ')
    lines, cur = [], ''
    for word in words:
        trial = word if not cur else cur + ' ' + word
        if text_width(trial, scale) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(cv, x, y, lines, scale, color, leading=None):
    if leading is None:
        leading = 7 * scale + 3
    for ln in lines:
        draw_text(cv, x, y, ln, scale, color)
        y += leading
    return y


def encode_png(cv):
    raw = bytearray()
    row_len = cv.w * 3
    for y in range(cv.h):
        raw.append(0)
        raw += cv.buf[y * row_len:(y + 1) * row_len]

    def chunk(typ, data):
        out = struct.pack('>I', len(data)) + typ + data
        return out + struct.pack('>I', zlib.crc32(typ + data) & 0xFFFFFFFF)

    ihdr = struct.pack('>IIBBBBB', cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)
            + chunk(b'IDAT', zlib.compress(bytes(raw), 9))
            + chunk(b'IEND', b''))


# Stylised world map: continents as polygons in a 672 x 200 box.
CONTINENTS = [
    # North America
    [(30, 28), (88, 16), (150, 24), (172, 44), (150, 60), (122, 54),
     (112, 80), (82, 96), (56, 80), (34, 54)],
    # Greenland
    [(186, 8), (206, 6), (212, 20), (196, 26)],
    # South America
    [(150, 104), (186, 100), (206, 114), (196, 150), (176, 186),
     (160, 160), (146, 124)],
    # Europe
    [(330, 34), (360, 24), (386, 30), (376, 50), (350, 56), (334, 50)],
    # Africa
    [(330, 70), (370, 64), (400, 76), (396, 110), (370, 142),
     (344, 130), (330, 100)],
    # Asia
    [(400, 24), (470, 14), (540, 20), (582, 34), (562, 60), (522, 54),
     (502, 80), (460, 86), (430, 70), (404, 50)],
    # South-East Asia islands
    [(520, 94), (536, 100), (530, 112), (516, 106)],
    # Australia
    [(540, 130), (590, 124), (612, 140), (586, 160), (550, 156)],
]
# (x, y) in map-box space -> (number, place) for the legend.
MARKERS = [
    (545, 52, '1'), (456, 62, '2'), (494, 78, '3'),
    (372, 34, '4'), (108, 46, '5'), (338, 40, '6'),
]
LEGEND = [
    ('1', 'SHENZHEN - TRUMP, XI AND PUTIN MEET AT APEC'),
    ('2', 'THE GULF - US AND IRAN TRADE FIRE AGAIN'),
    ('3', 'INDIA - CYCLONE AKVAN NEARS EAST COAST'),
    ('4', 'KYIV - EU PROPOSES 45BN EURO UKRAINE LOAN'),
    ('5', 'WASHINGTON - JEFFRIES NOMINATED FOR SPEAKER'),
    ('6', 'LONDON - VAN GOGH SELLS FOR RECORD $190.4M'),
]

STORIES = [
    ('WORLD', 'TRUMP, XI AND PUTIN SHAKE HANDS IN SHENZHEN',
     'The three leaders meet on Thursday at the APEC summit, with a trilateral session on trade and security.'),
    ('WORLD', 'US AND IRAN TRADE FIRE AGAIN',
     'US forces hit a missile site on Qeshm Island. Iran widens its attacks to a US base in Kuwait and Bahrain.'),
    ('POLITICS', 'JEFFRIES NOMINATED FOR SPEAKER',
     'Democrats nominate Hakeem Jeffries, who could become the first Black Speaker of the House.'),
    ('MARKETS', 'FED MINUTES POINT TO MORE RATE HIKES',
     'Nearly all officials see further hikes ahead if inflation and jobs stay hot, minutes from October show.'),
    ('TECH', 'NVIDIA HALTS H-CHIP SHIPMENTS TO CHINA',
     'Acting chief Colette Kress also promises earlier pay rises and more stock grants to staff.'),
    ('EUROPE', 'EU PROPOSES 45BN EURO UKRAINE LOAN',
     'Brussels wants the loan repaid once Russia pays reparations. Sanctions extended for three years.'),
    ('CULTURE', 'VAN GOGH SELLS FOR RECORD $190.4M',
     'Chataigniers en fleurs, painted in 1890, fetches a record sum after a row over its Nazi history.'),
    ('SCIENCE', 'VOYAGER 1 REACHES ONE LIGHT-DAY',
     'After almost 50 years in space, the probe is one light-day from Earth. NASA confirms it today.'),
    ('MARKETS', 'ANTHROPIC EYES $1.4TN DEBUT',
     'The Claude-maker is poised for one of the largest stock market debuts ever.'),
]


def draw_masthead(cv):
    cv.hline(28, 18, 968, INK)
    cv.hline(28, 22, 968, INK)
    title = 'THE WORLD TODAY'
    tw = text_width(title, 6)
    draw_text(cv, (W - tw) // 2, 34, title, 6, INK)
    date = 'THURSDAY, 19 NOVEMBER 2026'
    dw = text_width(date, 2)
    draw_text(cv, (W - dw) // 2, 96, date, 2, RED)
    draw_text(cv, 28, 96, 'VOL. I - NO. 323', 1, GREY)
    right = 'ONE DAY - ONE PAGE'
    draw_text(cv, W - 28 - text_width(right, 1), 96, right, 1, GREY)
    cv.rect(28, 122, 968, 4, INK)
    cv.hline(28, 130, 968, INK)


def draw_lead(cv):
    y = 146
    draw_text(cv, 28, y, 'CULTURE - GAMING', 1, RED)
    draw_text(cv, 28, y + 16, 'VICE CITY OPENS ITS GATES', 3, INK)
    sub = ('After a 13-year wait, Grand Theft Auto VI begins its global '
           'rollout - and millions of gamers are already heading back '
           'to Vice City.')
    draw_lines(cv, 28, y + 52, wrap_text(sub, 1, 560), 1, INK)
    # Sunset "photo" panel, right of the lead text.
    px, py, pw, ph = 620, 146, 376, 148
    bands = [(SUNSET_TOP, 0, 44), (SUNSET_MID, 44, 48), (SUNSET_LOW, 92, 56)]
    for col, off, hh in bands:
        cv.rect(px, py + off, pw, hh, col)
    cv.circle(px + 288, py + 52, 22, (255, 236, 170))
    skyline = [(0, 96, 34, 52), (40, 78, 30, 70), (76, 104, 26, 44),
               (108, 66, 36, 82), (150, 92, 30, 56), (186, 74, 34, 74),
               (226, 100, 28, 48), (260, 84, 32, 64), (298, 108, 30, 40),
               (334, 90, 42, 58)]
    for ox, oy, ww, hh in skyline:
        cv.rect(px + ox, py + oy, ww, hh, SKYLINE)
    for tx in (60, 250):
        cv.line(px + tx, py + 148, px + tx + 6, py + 96, SKYLINE)
        for dx, dy in ((-22, -16), (-12, -24), (0, -26), (12, -22), (22, -14)):
            cv.line(px + tx + 6, py + 96, px + tx + 6 + dx, py + 96 + dy, SKYLINE)
    cv.rect(px, py, pw, 2, INK)
    cv.rect(px, py + ph - 2, pw, 2, INK)
    cv.rect(px, py, 2, ph, INK)
    cv.rect(px + pw - 2, py, 2, ph, INK)
    draw_text(cv, 28, 306,
              'GAMERS ENTER VICE CITY AS GTA VI ROLLS OUT WORLDWIDE.',
              1, GREY)


def draw_map(cv):
    y = 336
    draw_text(cv, 28, y, 'THE WORLD IN ONE GLANCE', 2, INK)
    cv.hline(28, y + 22, 968, INK)
    mx, my, mw, mh = 28, y + 32, 672, 200
    cv.rect(mx, my, mw, mh, SEA)
    cv.rect(mx, my, mw, 2, INK)
    cv.rect(mx, my + mh - 2, mw, 2, INK)
    cv.rect(mx, my, 2, mh, INK)
    cv.rect(mx + mw - 2, my, 2, mh, INK)
    for poly in CONTINENTS:
        cv.poly([(mx + x, my + yy) for x, yy in poly], LAND)
    for x, yy, num in MARKERS:
        cv.circle(mx + x, my + yy, 9, RED)
        draw_text(cv, mx + x - 3, my + yy - 3, num, 1, (255, 255, 255))
    lx = 724
    draw_text(cv, lx, my + 4, 'WHERE THE NEWS IS', 1, RED)
    yy = my + 26
    for num, text in LEGEND:
        cv.circle(lx + 8, yy + 4, 8, RED)
        draw_text(cv, lx + 5, yy + 1, num, 1, (255, 255, 255))
        yy = draw_lines(cv, lx + 24, yy, wrap_text(text, 1, 248), 1, INK)
        yy += 8


def draw_columns(cv):
    y = 592
    cv.hline(28, y, 968, INK)
    col_w, gap = 300, 34
    for ci in range(3):
        x = 28 + ci * (col_w + gap)
        yy = y + 14
        for kicker, head, deck in STORIES[ci * 3:(ci + 1) * 3]:
            draw_text(cv, x, yy, kicker, 1, RED)
            yy += 12
            yy = draw_lines(cv, x, yy, wrap_text(head, 2, col_w), 2, INK)
            yy += 2
            yy = draw_lines(cv, x, yy, wrap_text(deck, 1, col_w), 1, GREY)
            yy += 8
            cv.hline(x, yy, col_w, GREY)
            yy += 12


def draw_footer(cv):
    cv.rect(28, 946, 968, 30, INK)
    tick = ('GOLD $3,730 v 5%  -  OIL FALLS ON MIDDLE EAST TENSIONS  -  '
            'CYCLONE AKVAN TO CROSS MACHILIPATNAM-PURI  -  CRIMEAN BRIDGE HIT AGAIN')
    draw_text(cv, 40, 955, tick, 1, (255, 255, 255))
    foot = 'THE WORLD TODAY - PRINTED 19 NOVEMBER 2026 - EVERY STORY FROM THE DAY\'S WIRES'
    fw = text_width(foot, 1)
    draw_text(cv, (W - fw) // 2, 990, foot, 1, GREY)


def main():
    cv = Canvas(W, H, PAPER)
    draw_masthead(cv)
    draw_lead(cv)
    draw_map(cv)
    draw_columns(cv)
    draw_footer(cv)
    outdir = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, 'entry.png')
    with open(path, 'wb') as f:
        f.write(encode_png(cv))


if __name__ == '__main__':
    main()
