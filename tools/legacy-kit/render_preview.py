"""Local preview: renders a deck's slide files to PNGs (approximation of the Slides runtime)."""
import sys, json, os, re, asyncio
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
NM = os.path.join(HERE, "node_modules")
deck_root, out_dir = sys.argv[1], sys.argv[2]
blobmap = json.loads(sys.argv[3])  # blob url -> local file
only = sys.argv[4].split(",") if len(sys.argv) > 4 and sys.argv[4] else None
os.makedirs(out_dir, exist_ok=True)

def ff(family, path, weight="400", rng=None):
    return f"@font-face{{font-family:'{family}';src:url('file://{path}');font-weight:{weight};{('unicode-range:'+rng+';') if rng else ''}}}"

css = []
rp = f"{NM}/@fontsource-variable/readex-pro/files"
css.append(ff("Readex Pro", f"{rp}/readex-pro-arabic-wght-normal.woff2", "160 700", "U+0600-06FF,U+0750-077F,U+08A0-08FF,U+FB50-FDFF,U+FE70-FEFF,U+200C-200E,U+2010-2011,U+204F,U+2E41"))
css.append(ff("Readex Pro", f"{rp}/readex-pro-latin-wght-normal.woff2", "160 700", "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215"))
pa = f"{NM}/@fontsource/ibm-plex-sans-arabic/files"
for w in ["400", "500", "600", "700"]:
    css.append(ff("IBM Plex Sans Arabic", f"{pa}/ibm-plex-sans-arabic-arabic-{w}-normal.woff2", w, "U+0600-06FF,U+0750-077F,U+08A0-08FF,U+FB50-FDFF,U+FE70-FEFF,U+200C-200E"))
    css.append(ff("IBM Plex Sans Arabic", f"{pa}/ibm-plex-sans-arabic-latin-{w}-normal.woff2", w, "U+0000-00FF,U+2000-206F,U+20AC,U+2122,U+2212"))
pm = f"{NM}/@fontsource/ibm-plex-mono/files"
for w in ["500", "600"]:
    css.append(ff("IBM Plex Mono", f"{pm}/ibm-plex-mono-latin-{w}-normal.woff2", w))
css.append("""*{box-sizing:border-box;margin:0}body{background:#888;margin:0}section{width:1920px;height:1080px;position:relative;overflow:hidden}
h1,h2,h3,p{margin:0}table{border-collapse:collapse}td,th{border:1px solid #D8D2C4}aside{display:none}
x-icon{display:inline-block;border-radius:50%;background:currentColor;opacity:.8;transform:scale(.5)}""")

async def main():
    order = json.load(open(os.path.join(deck_root, "project", "deck.json")))["order"]
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium" if os.path.exists("/opt/pw-browsers/chromium") else None)
        pg = await b.new_page(viewport={"width": 1920, "height": 1080})
        for i, sid in enumerate(order):
            if only and sid not in only:
                continue
            html = open(os.path.join(deck_root, "project", "slides", sid + ".html"), encoding="utf-8").read()
            for k, v in blobmap.items():
                html = html.replace(k, "file://" + v)
            doc = f"<!doctype html><html><head><meta charset='utf-8'><style>{''.join(css)}</style></head><body>{html}</body></html>"
            path = os.path.join(out_dir, f"_{sid}.html")
            open(path, "w", encoding="utf-8").write(doc)
            await pg.goto("file://" + path)
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(150)
            # overflow report: any element whose bottom exceeds 920 (content) except pinned footer
            rep = await pg.evaluate("""() => { const s=document.querySelector('section'); const out=[];
              s.querySelectorAll('h1,h2,h3,p,table,img,div').forEach(e=>{ const r=e.getBoundingClientRect();
                if (e.closest('div[style*="bottom:64px"]')) return;
                if (r.bottom>952 || r.right>1800 || r.left<120) out.push(e.tagName+' '+Math.round(r.left)+','+Math.round(r.bottom)+' '+(e.innerText||'').slice(0,40)); });
              s.querySelectorAll('p,h1,h2,h3,td,th').forEach(e=>{ if (e.scrollWidth>e.clientWidth+2) out.push('HOVERFLOW '+(e.innerText||'').slice(0,40)); });
              return out.slice(0,8); }""")
            await pg.screenshot(path=os.path.join(out_dir, f"{i+1:02d}_{sid}.png"))
            if rep:
                print(sid, rep)
        await b.close()

asyncio.run(main())
