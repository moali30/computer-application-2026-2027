"""Make a .ppsx (opens straight into the slide show) from a .pptx.

The two formats differ only in the content type of ppt/presentation.xml.

Usage: python3 tools/make_ppsx.py "سكشن 2 — <title>.pptx"
Writes the .ppsx next to the .pptx.
"""
import sys
import zipfile
from pathlib import Path

PPTX_MAIN = b"presentationml.presentation.main+xml"
PPSX_MAIN = b"presentationml.slideshow.main+xml"


def make_ppsx(src: Path) -> Path:
    dst = src.with_suffix(".ppsx")
    with zipfile.ZipFile(src) as zin:
        # Check before opening dst, so a bad input never truncates an existing .ppsx.
        if PPTX_MAIN not in zin.read("[Content_Types].xml"):
            raise SystemExit(f"{src}: not a .pptx presentation")
        with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "[Content_Types].xml":
                    data = data.replace(PPTX_MAIN, PPSX_MAIN)
                zout.writestr(item, data)
    return dst


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    print(make_ppsx(Path(sys.argv[1])))
