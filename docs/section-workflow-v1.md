# Computer Application sections: build workflow

How each lab section becomes two matching Slides decks (Arabic RTL and English LTR). Start every new section from here.

## Artifacts
- Design system: **Computer Application Sections** (https://claude.ai/artifact/VLRrkrryr4GtjK1rRZivek). Holds the tokens, brand book, RTL rules and slide layouts. It uses a draft palette until Horus University's logo and colours are supplied.
- Section 1 (Arabic): https://claude.ai/artifact/DPpuZy1phoURcg819GWUhY
- Section 1 (English): https://claude.ai/artifact/ANxUTh6YSTC7vW3xHRTQBo
- Source files live on Mohamed's computer at `E:\02 Work\سكاشن\Computer Application 2026-2027\Section N - files\`

## Steps for Section N
1. Read the section .docx (pandoc to markdown; extract the images).
2. Create two Slides artifacts: "Section N — <topic> (عربي)" and "Section N — <topic> (English)".
3. Upload the screenshots to each deck as assets. In the English deck, replace the Arabic annotations on screenshots with English labels (PIL: white out the label boxes, redraw them in DejaVu Sans Bold in the same colours).
4. Copy `section1.py` to `sectionN.py` and write the content with `L(k, ar, en)` pairs, using only the kit layouts: cover, agenda, divider, content/cards, statement (one per section), shot_slide, mcq, and the exercise data → questions → answers set. The wrap-up uses the same structure.
5. Generate: `python3 sectionN.py ar deck-ar '<ds record json>'` and the same for `en`.
6. Preview locally with `render_preview.py` (fontsource fonts plus Playwright). Fix anything that goes past y 920 or overflows sideways.
7. Publish each deck in two calls: first deck.json, cover and `project/ds/compapp/tokens.json` (copied from the design system artifact), then the remaining slides.

8. PowerPoint copy of the Arabic deck: after the user exports it, run `fix_rtl_pptx.py` on it (the exporter writes every paragraph left-to-right, which scrambles mixed Arabic/English lines). Write the result next to the original as `<name> (RTL).pptx`.

## Rules that must not drift
- Cards stacked vertically in a column must use `flex="none"`. With `flex:1` the slide app collapses them and the text overlaps; the local preview doesn't show this.
- Arabic text: wrap in U+202B…U+202C, align right, `row-reverse` for rows, table columns reversed, no ul/ol, no letter-spacing.
- Blue means concept and SPSS term; amber means practice. Exactly one amber statement slide per section.
- Exercise answers go on the answers slide and in the question slides' speaker notes.
- Content comes only from the section document. Teaching extras go in speaker notes.

## Section log
- Section 1 — Introduction to SPSS (variables and measures, SPSS windows, Variable View properties, Data View, 3 exercises). 29 slides per language.
