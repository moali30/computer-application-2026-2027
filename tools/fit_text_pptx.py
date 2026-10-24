#!/usr/bin/env python3
"""Shrink text that would overflow its box when PowerPoint draws an exported deck in Tahoma.

The Slides export sizes every text box for the web fonts (IBM Plex Sans Arabic,
Readex Pro), then writes the text in Tahoma ("basic fonts"). Tahoma is wider, so
in PowerPoint a title that took one line on the web takes two and runs into the
text under it. This lays out every text box and table cell again in the web font,
widened by Tahoma's measured extra width (TAHOMA_BOLD / TAHOMA_REGULAR, from the
Section 4 deck in PowerPoint), and where the text no longer fits the box it
lowers that box's font size and line spacing until it does.

Needs Node with Playwright (the Chromium preinstalled in Claude's cloud
container) and network access to Google Fonts. Run it last, after fix_rtl and
the answer animations, and before make_ppsx:
    python3 tools/fit_text_pptx.py "<deck>.pptx"      (rewrites the file in place)
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

TAHOMA_BOLD = 1.22     # Tahoma Bold width / IBM Plex Sans Arabic Bold width (measured 1.12-1.20), plus a margin
TAHOMA_REGULAR = 1.22  # same for the regular weight (measured 1.11-1.16)
PX = 6350              # EMU per slide pixel (1920 px = 12192000 EMU)
SHAPE = re.compile(r'<p:sp>.*?</p:sp>|<p:graphicFrame>.*?</p:graphicFrame>', re.S)
SLIDE = re.compile(r'ppt/slides/slide\d+\.xml$')

MEASURE_JS = r"""
const {chromium} = require('playwright');
const fs = require('fs');
const [inp, out, rb, rr] = process.argv.slice(2);
const boxes = JSON.parse(fs.readFileSync(inp, 'utf8'));
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.setContent(`<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=block" rel="stylesheet"><body style="margin:0"></body>`, {waitUntil: 'networkidle'});
  await p.evaluate(async () => {
    await document.fonts.load("700 20px 'IBM Plex Sans Arabic'", 'ا');
    await document.fonts.load("400 20px 'IBM Plex Sans Arabic'", 'ا');
    await document.fonts.ready;
    if (!document.fonts.check("700 20px 'IBM Plex Sans Arabic'", 'ا')) throw new Error('IBM Plex Sans Arabic did not load');
  });
  const ks = await p.evaluate(([boxes, rb, rr]) => {
    // height of the text box at k, with Tahoma's width (w = rb/rr) or the web font's (w = 1)
    const height = (box, k, w) => {
      const d = document.createElement('div');
      d.style.cssText = `position:absolute;left:0;top:0;width:${box.w}px;font-family:'IBM Plex Sans Arabic';white-space:pre-wrap`;
      for (const para of box.paras) {
        const e = document.createElement('div');
        e.style.textAlign = para.algn;
        e.style.lineHeight = para.ln ? (para.ln * k) + 'px' : 'normal';
        e.style.minHeight = e.style.lineHeight;
        for (const r of para.runs) {
          const s = document.createElement('span');
          s.textContent = r.t;
          s.style.fontWeight = r.b ? 700 : 400;
          s.style.fontSize = (r.sz * k * (w ? (r.b ? rb : rr) : 1)) + 'px';
          e.appendChild(s);
        }
        d.appendChild(e);
      }
      document.body.appendChild(d);
      const h = d.getBoundingClientRect().height;
      d.remove();
      return h;
    };
    return boxes.map(box => {
      // a table cell the web wrapped to more lines than its exported row height holds may keep them
      const room = Math.max(box.h, height(box, 1, false)) + 2;
      const fits = k => height(box, k, true) <= room;
      if (fits(1)) return 1;
      for (let k = 0.97; k > 0.6; k -= 0.03) if (fits(k)) return +k.toFixed(2);
      return 0.6;
    });
  }, [boxes, +rb, +rr]);
  fs.writeFileSync(out, JSON.stringify(ks));
  await b.close();
})();
"""


def paras(xml):
    out = []
    for p in re.findall(r'<a:p>.*?</a:p>|<a:p\s[^>]*>.*?</a:p>', xml, re.S):
        algn = re.search(r'<a:pPr\b[^>]*\salgn="(\w+)"', p)
        ln = re.search(r'<a:lnSpc><a:spcPts val="(\d+)"', p)
        runs = []
        for r in re.findall(r'<a:r>.*?</a:r>|<a:br\b[^>]*/>', p, re.S):
            if r.startswith('<a:br'):
                runs.append(dict(t='\n', sz=0, b=False))
                continue
            sz = re.search(r'\ssz="(\d+)"', r)
            t = ''.join(re.findall(r'<a:t>(.*?)</a:t>', r, re.S))
            t = t.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&amp;', '&')
            runs.append(dict(t=t, sz=int(sz.group(1)) / 50 if sz else 36, b=bool(re.search(r'\sb="1"', r))))
        out.append(dict(algn={'r': 'right', 'ctr': 'center', 'just': 'justify'}.get(algn and algn.group(1), 'left'),
                        ln=int(ln.group(1)) / 50 if ln else 0, runs=runs))
    return out


def boxes_of(shape):
    """Each text area of a shape as (width px, height px, paragraphs)."""
    if shape.startswith('<p:sp>'):
        ext = re.search(r'<a:ext cx="(\d+)" cy="(\d+)"', shape)
        body = re.search(r'<p:txBody>.*?</p:txBody>', shape, re.S)
        if not ext or not body or '<a:t>' not in body.group(0):
            return []
        bp = re.search(r'<a:bodyPr\b[^>]*>', body.group(0)).group(0)
        ins = {k: int(v) for k, v in re.findall(r'\s([lrtb]Ins)="(\d+)"', bp)}
        w = int(ext[1]) - ins.get('lIns', 91440) - ins.get('rIns', 91440)
        h = int(ext[2]) - ins.get('tIns', 45720) - ins.get('bIns', 45720)
        return [(w / PX, h / PX, paras(body.group(0)))]
    if '<a:tbl>' not in shape:
        return []
    cols = [int(w) for w in re.findall(r'<a:gridCol w="(\d+)"', shape)]
    out = []
    for tr in re.findall(r'<a:tr h="\d+">.*?</a:tr>', shape, re.S):
        h = int(re.match(r'<a:tr h="(\d+)"', tr).group(1))
        for i, tc in enumerate(re.findall(r'<a:tc\b.*?</a:tc>', tr, re.S)):
            if '<a:t>' not in tc or i >= len(cols):
                continue
            span = re.search(r'gridSpan="(\d+)"', tc)
            w = sum(cols[i:i + int(span.group(1))]) if span else cols[i]
            m = re.search(r'<a:tcPr\b[^>]*>', tc).group(0)
            mar = {k: int(v) for k, v in re.findall(r'\s(mar[LRTB])="(\d+)"', m)}
            out.append(((w - mar.get('marL', 91440) - mar.get('marR', 91440)) / PX,
                        (h - mar.get('marT', 45720) - mar.get('marB', 45720)) / PX, paras(tc)))
    return out


def shrink(shape, k):
    def sz(m):
        return '%s="%d"' % (m.group(1), max(100, round(int(m.group(2)) * k / 50) * 50))
    shape = re.sub(r'\b(sz)="(\d+)"', sz, shape)
    return re.sub(r'(<a:spcPts val=")(\d+)"', lambda m: '%s%d"' % (m.group(1), round(int(m.group(2)) * k)), shape)


def main(path):
    with zipfile.ZipFile(path) as z:
        parts = {n: z.read(n).decode('utf-8') for n in z.namelist() if SLIDE.match(n)}
    index, boxes = [], []
    for name, xml in parts.items():
        for i, shape in enumerate(SHAPE.findall(xml)):
            for b in boxes_of(shape):
                index.append((name, i))
                boxes.append(dict(w=b[0], h=b[1], paras=b[2]))
    tmp = tempfile.mkdtemp()
    with open(os.path.join(tmp, 'in.json'), 'w') as f:
        json.dump(boxes, f)
    with open(os.path.join(tmp, 'measure.js'), 'w') as f:
        f.write(MEASURE_JS)
    subprocess.run(['node', os.path.join(tmp, 'measure.js'), os.path.join(tmp, 'in.json'),
                    os.path.join(tmp, 'out.json'), str(TAHOMA_BOLD), str(TAHOMA_REGULAR)], check=True)
    ks = json.load(open(os.path.join(tmp, 'out.json')))
    scale = {}
    for key, k in zip(index, ks):
        scale[key] = min(scale.get(key, 1), k)  # a table shrinks as a whole, by its tightest cell
    for name in parts:
        n = iter(range(10 ** 6))
        parts[name] = SHAPE.sub(lambda m: (lambda i: shrink(m.group(0), scale[(name, i)])
                                           if scale.get((name, i), 1) < 1 else m.group(0))(next(n)), parts[name])
    out = path + '.tmp'
    with zipfile.ZipFile(path) as src, zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as dst:
        for info in src.infolist():
            data = parts[info.filename].encode('utf-8') if info.filename in parts else src.read(info.filename)
            dst.writestr(info, data)
    shutil.copymode(path, out)
    os.replace(out, path)
    shrunk = sorted((int(re.search(r'\d+', n).group()), i, k) for (n, i), k in scale.items() if k < 1)
    for s, i, k in shrunk:
        print(f'slide {s:2d} shape {i:2d}: font x{k}')
    print(f'{path}: {len(shrunk)} text boxes shrunk')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
