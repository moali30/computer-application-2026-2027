"""Fix Arabic text direction in a PowerPoint exported from the Arabic Slides deck.

The Slides exporter writes every paragraph as left-to-right, so PowerPoint scrambles
mixed Arabic/English lines. This sets rtl="1" + right alignment + lang ar-EG on every
paragraph that contains Arabic, and strips the U+202B/U+202C embedding marks.

Usage: python3 fix_rtl_pptx.py "<exported>.pptx" "<exported> (RTL).pptx"
"""
import zipfile, re, sys

AR = re.compile(r'[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]')
CTRL = re.compile(r'[‪-‮⁦-⁩]')


def fix_p(m):
    p = m.group(0)
    texts = ''.join(re.findall(r'<a:t>(.*?)</a:t>', p, re.S))
    p = re.sub(r'(<a:t>)(.*?)(</a:t>)', lambda t: t.group(1) + CTRL.sub('', t.group(2)) + t.group(3), p, flags=re.S)
    if not AR.search(texts):
        return p
    if re.search(r'<a:pPr\b', p):
        p = re.sub(r'<a:pPr\b([^>]*?)(/?)>',
                   lambda q: '<a:pPr' + re.sub(r'\s(rtl|algn)="[^"]*"', '', q.group(1)) + ' rtl="1" algn="r"' + q.group(2) + '>',
                   p, count=1)
    else:
        p = p.replace('<a:p>', '<a:p><a:pPr rtl="1" algn="r"/>', 1)
    p = re.sub(r'(<a:(?:rPr|endParaRPr)\b[^>]*?)\slang="[^"]*"', r'\1 lang="ar-EG"', p)
    return p


src, dst = sys.argv[1], sys.argv[2]
zin = zipfile.ZipFile(src)
zout = zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED)
n = 0
for item in zin.infolist():
    data = zin.read(item.filename)
    if re.match(r'ppt/(slides/slide|notesSlides/notesSlide)\d+\.xml$', item.filename):
        x = data.decode('utf-8')
        y = re.sub(r'<a:p>.*?</a:p>', fix_p, x, flags=re.S)
        n += x != y
        data = y.encode('utf-8')
    zout.writestr(item, data)
zout.close()
print('slides changed:', n)
