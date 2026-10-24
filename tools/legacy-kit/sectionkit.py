"""Section slide kit — builds bilingual (ar/en) slide files that follow the
"Computer Application Sections" design system. Every layout lives here so all
sections share identical markup; a section script only supplies content."""
import json, os, datetime

# ---- tokens -------------------------------------------------------------
INK, INK_SOFT, MUTED = "#14233A", "#46546B", "#5E687C"
PAPER, PAPER_ALT, CARD, RULE = "#F6F4EF", "#ECE8DE", "#FFFDF8", "#D8D2C4"
BLUE, BLUE_TINT = "#1E5AA8", "#DCE7F5"
AMBER, AMBER_INK, AMBER_TINT = "#E9A23B", "#9A5B00", "#FBEBD0"
MIST, INK_LINE = "#B9CCE6", "#2E3C52"
DISPLAY = "'Readex Pro', Tahoma, sans-serif"
SANS = "'IBM Plex Sans Arabic', Tahoma, sans-serif"
MONO = "'IBM Plex Mono', 'Courier New', monospace"
FACES = {
    "readex-pro": {"family": "Readex Pro", "href": "https://fonts.googleapis.com/css2?family=Readex+Pro:wght@400..700&display=swap"},
    "ibm-plex-sans-arabic": {"family": "IBM Plex Sans Arabic", "href": "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap"},
    "ibm-plex-mono": {"family": "IBM Plex Mono", "href": "https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600&display=swap"},
}
RLE, PDF = "‫", "‬"


class Kit:
    def __init__(self, lang, course, section_label, root):
        self.ar = lang == "ar"
        self.lang = lang
        self.course, self.section_label = course, section_label
        self.root = root
        self.slides = []  # (id, html)
        self.sections = {}
        os.makedirs(os.path.join(root, "project", "slides"), exist_ok=True)

    # ---- direction helpers ------------------------------------------------
    def t(self, s):
        """Wrap Arabic text in a right-to-left embedding (the slide subset has no dir attribute)."""
        return f"{RLE}{s}{PDF}" if self.ar else s

    @property
    def dlh(self):
        return 1.2 if self.ar else 1.05

    @property
    def row(self):
        return "row-reverse" if self.ar else "row"

    @property
    def align(self):
        return "right" if self.ar else "left"

    @property
    def self_start(self):
        return "end" if self.ar else "start"

    def pad_start(self, n):
        return f"0 {n}px 0 0" if self.ar else f"0 0 0 {n}px"

    def pin_start(self, n):
        return f"right:{n}px" if self.ar else f"left:{n}px"

    # ---- atoms --------------------------------------------------------------
    def eyebrow(self, text, kind="concept", dark=False):
        if kind == "term":
            return (f'<p style="align-self:{self.self_start}; font-family:{MONO}; font-size:24px; font-weight:600; '
                    f'color:{BLUE}; background:{BLUE_TINT}; padding:6px 18px; border-radius:999px">{text}</p>')
        color = (AMBER if dark else AMBER_INK) if kind == "practice" else (AMBER if dark else BLUE)
        ls = "" if self.ar else " letter-spacing:3px; text-transform:uppercase;"
        return f'<p style="font-size:24px; font-weight:600;{ls} color:{color}">{self.t(text)}</p>'

    def title(self, text, dark=False):
        c = PAPER if dark else INK
        return f'<h2 style="font-family:{DISPLAY}; font-size:72px; font-weight:600; line-height:1.15; color:{c}">{self.t(text)}</h2>'

    def head(self, eyebrow, title, kind="concept", dark=False):
        return (f'<div style="display:flex; flex-direction:column; gap:16px">'
                f'{self.eyebrow(eyebrow, kind, dark)}{self.title(title, dark)}</div>')

    def h3(self, text, color=INK, size=44):
        return f'<h3 style="font-family:{DISPLAY}; font-size:{size}px; font-weight:600; line-height:1.25; color:{color}">{self.t(text)}</h3>'

    def p(self, text, size=32, color=INK_SOFT, weight=400, extra=""):
        lh = 1.5 if size >= 32 else 1.45
        return f'<p style="font-size:{size}px; line-height:{lh}; font-weight:{weight}; color:{color}{extra}">{self.t(text)}</p>'

    def chip(self, text, dark=False, align=True):
        bg, fg = (INK_LINE, MIST) if dark else (BLUE_TINT, BLUE)
        a = f"align-self:{self.self_start}; " if align else ""
        return (f'<p style="{a}font-family:{MONO}; font-size:28px; font-weight:600; line-height:1.3; color:{fg}; '
                f'background:{bg}; padding:8px 20px; border-radius:999px; white-space:nowrap">{text}</p>')

    def chip_row(self, items, dark=False):
        inner = "".join(self.chip(i, dark, align=False) for i in items)
        return f'<div style="display:flex; flex-direction:{self.row}; flex-wrap:wrap; gap:16px">{inner}</div>'

    def tag(self, text, bg=BLUE_TINT, fg=BLUE):
        """Arabic-capable pill (sans family), e.g. 'اسمي · Nominal'."""
        return (f'<p style="font-size:28px; font-weight:600; line-height:1.3; color:{fg}; background:{bg}; '
                f'padding:8px 22px; border-radius:999px; white-space:nowrap">{self.t(text)}</p>')

    def tag_row(self, items, bg=BLUE_TINT, fg=BLUE):
        inner = "".join(self.tag(i, bg, fg) for i in items)
        return f'<div style="display:flex; flex-direction:{self.row}; flex-wrap:wrap; gap:16px">{inner}</div>'

    def card(self, inner, bg=CARD, flex="1", gap=20, pad=40, border=True, width=None):
        b = f" border:1px solid {RULE};" if border else ""
        w = f"width:{width}px; " if width else ""
        return (f'<div style="{w}flex:{flex}; display:flex; flex-direction:column; gap:{gap}px; background:{bg};{b} '
                f'border-radius:16px; padding:{pad}px">{inner}</div>')

    def cards(self, items, gap=32):
        return f'<div style="display:flex; flex-direction:{self.row}; gap:{gap}px">{"".join(items)}</div>'

    def bullets(self, items, size=32, color=INK_SOFT, gap=12):
        rows = "".join(self.p("•  " + i, size, color) for i in items)
        return f'<div style="display:flex; flex-direction:column; gap:{gap}px">{rows}</div>'

    def num_badge(self, n, size=56, bg=INK, fg=AMBER, font=28):
        return (f'<div style="width:{size}px; height:{size}px; flex:none; border-radius:50%; background:{bg}; '
                f'display:flex; align-items:center; justify-content:center">'
                f'<p style="font-family:{DISPLAY}; font-size:{font}px; font-weight:700; line-height:1; color:{fg}; text-align:center">{n}</p></div>')

    def steps(self, items, size=30, color=INK_SOFT):
        rows = "".join(
            f'<div style="display:flex; flex-direction:{self.row}; gap:20px; align-items:start">'
            f'{self.num_badge(i + 1, 48, BLUE, CARD, 24)}<div style="flex:1">{self.p(s, size, color)}</div></div>'
            for i, s in enumerate(items))
        return f'<div style="display:flex; flex-direction:column; gap:20px">{rows}</div>'

    def shot(self, src, alt, w, h):
        return (f'<div style="flex:none; background:{CARD}; border:1px solid {RULE}; border-radius:16px; padding:16px">'
                f'<img src="{src}" alt="{alt}" style="width:{w}px; height:{h}px; object-fit:contain"></div>')

    def table(self, header, rows, widths, size=28, width=None, center_cols=()):
        if self.ar:
            header, widths = header[::-1], widths[::-1]
            rows = [r[::-1] for r in rows]
            n = len(header)
            center_cols = tuple(n - 1 - c for c in center_cols)
        def al(i):
            return "center" if i in center_cols else self.align
        th = "".join(f'<th style="width:{w}%; padding:14px 20px; text-align:{al(i)}; color:{PAPER}; font-weight:600">{self.t(h)}</th>'
                     for i, (h, w) in enumerate(zip(header, widths)))
        body = ""
        for k, r in enumerate(rows):
            bg = CARD if k % 2 == 0 else PAPER_ALT
            body += f'<tr style="background:{bg}">' + "".join(
                f'<td style="padding:14px 20px; text-align:{al(i)}">{self.t(str(c))}</td>' for i, c in enumerate(r)) + "</tr>"
        wcss = f" width:{width}px;" if width else ""
        return (f'<table style="{wcss} font-size:{size}px; line-height:1.35; color:{INK}; border:1px solid {RULE}; border-radius:8px">'
                f'<tr style="background:{INK}">{th}</tr>{body}</table>')

    def footer(self, n, dark=False, color=None):
        c = color or (MIST if dark else MUTED)
        return (f'<div style="position:absolute; left:128px; bottom:64px; width:1664px; display:flex; flex-direction:{self.row}; '
                f'justify-content:space-between">'
                f'<p style="font-size:24px; color:{c}">{self.t(self.course + " · " + self.section_label)}</p>'
                f'<p style="font-size:24px; font-weight:600; color:{c}; font-variant-numeric:tabular-nums">{n:02d}</p></div>')

    def notes(self, text):
        return f"<aside>{text}</aside>" if text else ""

    # ---- slide shells ---------------------------------------------------------
    def add(self, sid, body, bg=PAPER, notes="", footer=True, dark=False, section=None, justify="start", gap=48, pinned_first=""):
        n = len(self.slides) + 1
        pad = "128px 128px 160px" if footer else "128px"
        color = MIST if dark else INK_SOFT
        html = (f'<section id="{sid}" data-transition="fade" style="background:{bg}; color:{color}; font-family:{SANS}; '
                f'text-align:{self.align}; padding:{pad}; display:flex; flex-direction:column; justify-content:{justify}; gap:{gap}px">'
                f'{pinned_first}{body}{self.footer(n, dark, INK if bg == AMBER else None) if footer else ""}{self.notes(notes)}</section>')
        self.slides.append((sid, html))
        if section:
            self.sections[f"s{len(self.sections) + 1}"] = {"description": section, "start": sid}
        return n

    # ---- motif ----------------------------------------------------------------
    def grid_svg(self, cols=6, rows=6, tile=96, gap=16, sel_col=2):
        W = cols * tile + (cols - 1) * gap
        H = rows * tile + (rows - 1) * gap
        rects = []
        for r in range(rows):
            for c in range(cols):
                x, y = c * (tile + gap), r * (tile + gap)
                if c == sel_col:
                    fill, op = (AMBER, 1) if r == 0 else (BLUE, 1)
                elif r == 0:
                    fill, op = MIST, 0.28
                else:
                    fill, op = INK_LINE, 1
                rects.append(f'<rect x="{x}" y="{y}" width="{tile}" height="{tile}" rx="8" fill="{fill}" fill-opacity="{op}"/>')
        return (f'<svg aria-label="" width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
                + "".join(rects) + "</svg>"), W, H

    def progress_svg(self, total, current):
        tile, gap = 72, 16
        H = total * tile + (total - 1) * gap
        rects = "".join(
            f'<rect x="0" y="{i * (tile + gap)}" width="{tile}" height="{tile}" rx="8" fill="{AMBER if i + 1 == current else INK_LINE}"/>'
            for i in range(total))
        return f'<svg aria-label="" width="{tile}" height="{H}" viewBox="0 0 {tile} {H}" xmlns="http://www.w3.org/2000/svg">{rects}</svg>', tile, H

    # ---- layouts ----------------------------------------------------------------
    def cover(self, sid, eyebrow, title, subtitle, meta, notes="", section=None):
        svg, W, H = self.grid_svg()
        x = 128 if self.ar else 1792 - W
        motif = f'<div style="position:absolute; left:{x}px; top:{(1080 - H) // 2}px; width:{W}px; height:{H}px">{svg}</div>'
        tw = 1664 - W - 96
        text_pin = "left" if not self.ar else "right"
        body = (f'<div style="width:{tw}px; align-self:{self.self_start}; display:flex; flex-direction:column; gap:32px">'
                f'{self.eyebrow(eyebrow, "practice", dark=True)}'
                f'<h1 style="font-family:{DISPLAY}; font-size:120px; font-weight:700; line-height:{self.dlh}; color:{PAPER}">{self.t(title)}</h1>'
                f'<p style="font-size:44px; line-height:1.3; color:{MIST}">{self.t(subtitle)}</p>'
                f'<div style="height:4px; width:120px; background:{AMBER}; align-self:{self.self_start}"></div>'
                f'<p style="font-size:28px; color:{MIST}">{self.t(meta)}</p></div>')
        return self.add(sid, body, bg=INK, notes=notes, footer=False, dark=True, section=section, justify="center", pinned_first=motif)

    def agenda(self, sid, eyebrow, title, items, notes="", section=None):
        rows = ""
        for i, it in enumerate(items):
            bt = "" if i == 0 else f"border-top:1px solid {RULE}; "
            rows += (f'<div style="{bt}display:flex; flex-direction:{self.row}; align-items:center; gap:40px; padding:22px 0">'
                     f'<p style="font-family:{MONO}; font-size:32px; font-weight:600; color:{BLUE}; width:72px; text-align:{self.align}">{i + 1:02d}</p>'
                     f'<p style="flex:1; font-size:36px; line-height:1.3; color:{INK}">{self.t(it)}</p></div>')
        body = self.head(eyebrow, title) + f'<div style="display:flex; flex-direction:column">{rows}</div>'
        return self.add(sid, body, notes=notes, section=section)

    def divider(self, sid, num, total, title, desc, notes="", section=None):
        svg, W, H = self.progress_svg(total, num)
        x = 128 if self.ar else 1792 - W
        motif = f'<div style="position:absolute; left:{x}px; top:{(1080 - H) // 2}px; width:{W}px; height:{H}px">{svg}</div>'
        body = (f'<div style="width:1400px; align-self:{self.self_start}; display:flex; flex-direction:column; gap:24px">'
                f'<p style="font-family:{DISPLAY}; font-size:240px; font-weight:700; line-height:1; color:{AMBER}">{num:02d}</p>'
                f'<h1 style="font-family:{DISPLAY}; font-size:120px; font-weight:700; line-height:{self.dlh}; color:{PAPER}">{self.t(title)}</h1>'
                f'<p style="font-size:36px; line-height:1.4; color:{MIST}">{self.t(desc)}</p></div>')
        return self.add(sid, body, bg=INK, notes=notes, dark=True, section=section, justify="center", pinned_first=motif)

    def statement(self, sid, eyebrow, big, body_text, notes="", section=None):
        body = (f'<div style="width:1500px; align-self:{self.self_start}; display:flex; flex-direction:column; gap:40px">'
                f'<p style="font-size:24px; font-weight:600; color:{INK}{"" if self.ar else "; letter-spacing:3px; text-transform:uppercase"}">{self.t(eyebrow)}</p>'
                f'<h1 style="font-family:{DISPLAY}; font-size:96px; font-weight:700; line-height:1.1; color:{INK}">{self.t(big)}</h1>'
                f'<p style="font-size:40px; line-height:1.45; color:{INK}">{self.t(body_text)}</p></div>')
        n = len(self.slides) + 1
        return self.add(sid, body, bg=AMBER, notes=notes, section=section, justify="center")

    def content(self, sid, eyebrow, title, inner, kind="concept", bg=PAPER, notes="", section=None, gap=48):
        return self.add(sid, self.head(eyebrow, title, kind) + inner, bg=bg, notes=notes, section=section, gap=gap)

    def shot_slide(self, sid, eyebrow, title, src, alt, w, h, side, kind="term", notes="", section=None):
        inner = (f'<div style="display:flex; flex-direction:{self.row}; gap:48px; align-items:start">'
                 f'{self.shot(src, alt, w, h)}<div style="flex:1; display:flex; flex-direction:column; gap:28px">{side}</div></div>')
        return self.content(sid, eyebrow, title, inner, kind=kind, bg=PAPER_ALT, notes=notes, section=section)

    def option(self, letter, text):
        return (f'<div style="display:flex; flex-direction:{self.row}; align-items:center; gap:14px; background:{CARD}; '
                f'border:1px solid {RULE}; border-radius:999px; padding:{"8px 8px 8px 24px" if self.ar else "8px 24px 8px 8px"}">'
                f'{self.num_badge(letter, 44, BLUE_TINT, BLUE, 24)}'
                f'<p style="font-size:28px; line-height:1.3; color:{INK}; white-space:nowrap">{self.t(text)}</p></div>')

    def mcq(self, sid, eyebrow, title, questions, start=1, notes="", section=None):
        blocks = ""
        for i, (stem, opts) in enumerate(questions):
            letters = ["a", "b", "c", "d"]
            ops = "".join(self.option(l, o) for l, o in zip(letters, opts))
            blocks += (f'<div style="display:flex; flex-direction:column; gap:14px">'
                       f'<div style="display:flex; flex-direction:{self.row}; align-items:center; gap:20px">'
                       f'{self.num_badge(start + i, 52, INK, AMBER, 26)}<div style="flex:1">{self.p(stem, 32, INK)}</div></div>'
                       f'<div style="display:flex; flex-direction:{self.row}; flex-wrap:wrap; gap:16px; padding:{self.pad_start(72)}">{ops}</div></div>')
        inner = f'<div style="display:flex; flex-direction:column; gap:28px">{blocks}</div>'
        return self.content(sid, eyebrow, title, inner, kind="practice", notes=notes, section=section, gap=40)

    # ---- output -----------------------------------------------------------------
    def write(self, title, design_system=None):
        for sid, html in self.slides:
            with open(os.path.join(self.root, "project", "slides", f"{sid}.html"), "w", encoding="utf-8") as f:
                f.write(html + "\n")
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        deck = {"v": 4, "createdOnFiles": {"v": 1, "at": now}, "title": title, "cover": self.slides[0][0],
                "order": [s for s, _ in self.slides], "sections": self.sections, "faces": FACES,
                "designSystems": [design_system] if design_system else []}
        with open(os.path.join(self.root, "project", "deck.json"), "w", encoding="utf-8") as f:
            json.dump(deck, f, ensure_ascii=False, indent=1)
        return deck
