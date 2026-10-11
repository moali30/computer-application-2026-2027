#!/usr/bin/env python3
"""Make the Arabic paragraphs of an exported deck right-to-left in PowerPoint.

The Slides export (Share > Export > PowerPoint) writes every paragraph
left-to-right and keeps the RLE/PDF characters that the slide HTML uses for
bidi. PowerPoint ignores those characters, so a line that mixes Arabic and
English (`إدخال البيانات في Data View`) comes out in the wrong order.

This marks every paragraph that contains Arabic -- on slides, in tables and in
speaker notes -- as rtl="1" with lang="ar-EG", the way the Section 1 file is,
and removes the bidi control characters. Running it twice changes nothing.

Usage: python3 tools/fix_rtl.py "<deck>.pptx"     (rewrites the file in place)
"""
import os
import re
import shutil
import sys
import tempfile
import zipfile

ARABIC = re.compile('[؀-ۿݐ-ݿﭐ-﷿ﹰ-ﻼ]')
CONTROLS = re.compile('[‪-‮⁦-⁩]')
PARA = re.compile(r'<a:p(?:\s[^>/]*)?>.*?</a:p>', re.S)  # not <a:p/>, not <a:pPr>
RUN = re.compile(r'<a:r>.*?</a:r>', re.S)
TEXT = re.compile(r'<a:t>([^<]*)</a:t>')
RTL_PARTS = re.compile(r'ppt/(slides|notesSlides)/[^/]+\.xml$')


def set_attr(tag, name, value):
    """Set name="value" on an XML start tag such as '<a:pPr algn="r">'."""
    tag = re.sub(r'\s%s="[^"]*"' % name, '', tag)
    end = '/>' if tag.endswith('/>') else '>'
    return tag[:-len(end)].rstrip() + ' %s="%s"%s' % (name, value, end)


def fix_run(m):
    run = m.group(0)
    if not ARABIC.search(''.join(TEXT.findall(run))):
        return run
    tag = re.search(r'<a:rPr\b[^>]*>', run)
    if tag:
        return run.replace(tag.group(0), set_attr(tag.group(0), 'lang', 'ar-EG'), 1)
    return run.replace('<a:r>', '<a:r><a:rPr lang="ar-EG"/>', 1)


def fix_para(m):
    para = m.group(0)
    if not ARABIC.search(''.join(TEXT.findall(para))):
        return para
    start = re.match(r'<a:p\b[^>]*>', para).group(0)
    ppr = re.match(r'<a:pPr\b[^>]*>', para[len(start):])
    if ppr:
        para = start + set_attr(ppr.group(0), 'rtl', '1') + para[len(start) + ppr.end():]
    else:
        para = start + '<a:pPr rtl="1"/>' + para[len(start):]
    para = RUN.sub(fix_run, para)
    end = re.search(r'<a:endParaRPr\b[^>]*>', para)
    if end:
        para = para.replace(end.group(0), set_attr(end.group(0), 'lang', 'ar-EG'), 1)
    return para


def fix_xml(name, xml):
    xml = CONTROLS.sub('', xml)
    if RTL_PARTS.match(name):
        xml = PARA.sub(fix_para, xml)
    return xml


def main(path):
    tmp = tempfile.NamedTemporaryFile(delete=False, dir=os.path.dirname(os.path.abspath(path)), suffix='.pptx')
    tmp.close()
    paras = 0
    with zipfile.ZipFile(path) as src, zipfile.ZipFile(tmp.name, 'w') as dst:
        for info in src.infolist():
            data = src.read(info.filename)
            if info.filename.endswith('.xml'):
                xml = data.decode('utf-8')
                new = fix_xml(info.filename, xml)
                paras += new.count('rtl="1"') - xml.count('rtl="1"')
                data = new.encode('utf-8')
            dst.writestr(info, data)
    shutil.copymode(path, tmp.name)
    os.replace(tmp.name, path)
    print(f'{path}: {paras} paragraphs set right-to-left')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
