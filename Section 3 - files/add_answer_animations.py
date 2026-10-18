"""Add click-to-reveal answers to the MCQ slides of the exported Section 3 PowerPoint.

For each question, a green highlight is drawn over the correct option's pill and
fades in on the next click (question 1 on the first click, then 2, ...).
Run it after fix_rtl_pptx.py:
    python3 add_answer_animations.py "<in>.pptx" "<out>.pptx"
"""
import re, sys, zipfile

# slide number -> correct option letter per question, in question order
ANSWERS = {14: "accc", 20: "cdc", 22: "bba"}
GREEN = "2E8B57"
PAD = 38100  # highlight grows 3 pt around the pill


def shapes(x):
    out = []
    for sp in re.findall(r'<p:sp>.*?</p:sp>', x, re.S):
        o = re.search(r'<a:off x="(\d+)" y="(\d+)"/><a:ext cx="(\d+)" cy="(\d+)"', sp)
        if not o:
            continue
        g = re.search(r'prst="(\w+)"', sp)
        t = ''.join(re.findall(r'<a:t>(.*?)</a:t>', sp)).strip()
        out.append(dict(t=t, g=g.group(1) if g else '', x=int(o[1]), y=int(o[2]), w=int(o[3]), h=int(o[4])))
    return out


def highlight(sid, s):
    x, y, w, h = s['x'] - PAD, s['y'] - PAD, s['w'] + 2 * PAD, s['h'] + 2 * PAD
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Answer {sid}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>'
            f'<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 50000"/></a:avLst></a:prstGeom>'
            f'<a:solidFill><a:srgbClr val="{GREEN}"><a:alpha val="22000"/></a:srgbClr></a:solidFill>'
            f'<a:ln w="38100"><a:solidFill><a:srgbClr val="{GREEN}"/></a:solidFill></a:ln></p:spPr></p:sp>')


def click_fade(ids, spid):
    a, b, c, d, e = ids
    tgt = f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>'
    return (f'<p:par><p:cTn id="{a}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst><p:childTnLst>'
            f'<p:par><p:cTn id="{b}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
            f'<p:par><p:cTn id="{c}" presetID="10" presetClass="entr" presetSubtype="0" fill="hold" grpId="0" nodeType="clickEffect">'
            f'<p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
            f'<p:set><p:cBhvr><p:cTn id="{d}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>{tgt}'
            f'<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>'
            f'<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{e}" dur="500"/>{tgt}</p:cBhvr></p:animEffect>'
            f'</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>')


def add(x, letters):
    sh = shapes(x)
    badges = sorted([s for s in sh if s['g'] == 'roundRect' and s['t'].isdigit() and s['x'] > 10000000], key=lambda s: s['y'])
    pills = [s for s in sh if s['g'] == 'roundRect' and s['t'] == '']
    nid = max(int(i) for i in re.findall(r'<p:cNvPr id="(\d+)"', x)) + 1
    new, pars, blds, tid = [], [], [], 3
    for qi, letter in enumerate(letters):
        top = badges[qi]['y']
        bottom = badges[qi + 1]['y'] if qi + 1 < len(badges) else 10 ** 9
        chip = [s for s in sh if s['t'] == letter and s['w'] < 400000 and top < s['y'] < bottom]
        assert len(chip) == 1, (qi, letter, chip)
        c = chip[0]
        pill = [p for p in pills if p['x'] <= c['x'] <= p['x'] + p['w'] and p['y'] <= c['y'] <= p['y'] + p['h']]
        assert len(pill) == 1, (qi, letter, pill)
        new.append(highlight(nid, pill[0]))
        pars.append(click_fade(range(tid, tid + 5), nid))
        blds.append(f'<p:bldP spid="{nid}" grpId="0" animBg="1"/>')
        nid += 1
        tid += 5
    x = x.replace('</p:spTree>', ''.join(new) + '</p:spTree>', 1)
    timing = ('<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
              '<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
              + ''.join(pars) +
              '</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
              '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>'
              '</p:childTnLst></p:cTn></p:par></p:tnLst><p:bldLst>' + ''.join(blds) + '</p:bldLst></p:timing>')
    assert '<p:timing' not in x
    m = re.search(r'<p:extLst>(?:(?!<p:extLst>).)*</p:extLst></p:sld>$', x, re.S)
    return x[:m.start()] + timing + x[m.start():] if m else x.replace('</p:sld>', timing + '</p:sld>')


src, dst = sys.argv[1], sys.argv[2]
zin = zipfile.ZipFile(src)
zout = zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED)
for item in zin.infolist():
    data = zin.read(item.filename)
    m = re.match(r'ppt/slides/slide(\d+)\.xml$', item.filename)
    if m and int(m[1]) in ANSWERS:
        data = add(data.decode('utf-8'), ANSWERS[int(m[1])]).encode('utf-8')
        print('slide', m[1], 'answers', ANSWERS[int(m[1])])
    zout.writestr(item, data)
zout.close()
