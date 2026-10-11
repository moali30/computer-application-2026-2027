# Computer Application 2026–2027

Source material for the **Computer Application (SPSS) lab sections**, Horus University, 2026/2027.
Every section becomes two slide decks — Arabic (right-to-left) and English — built from one design system, so every section in the series looks the same.

## Linked artifacts (claude.ai)

| What | Link |
| --- | --- |
| Design system — *Computer Application Sections* (namespace `compapp`) | https://claude.ai/artifact/VLRrkrryr4GtjK1rRZivek |
| Slides artifact type (new decks are created from it) | https://claude.ai/artifact/8jTsAFQMFDb2oA8MsPJ2eL |
| Section 2 deck, Arabic — reference for layout markup and RTL handling | https://claude.ai/artifact/6XUd3RE5KfiNeb258rk8sV |
| Section 2 deck, English | https://claude.ai/artifact/MVBsPhQFzoAijkU4GrTBxS |
| Section 1 deck, Arabic (uses `row-reverse`, see below) | https://claude.ai/artifact/DPpuZy1phoURcg819GWUhY |
| Section 1 deck, English | https://claude.ai/artifact/ANxUTh6YSTC7vW3xHRTQBo |

The design system is the single source of truth for colours, type, layouts and RTL rules. Read it fresh each time (`project/README.md`, `project/slide-layouts.md`, `project/tokens.json`): its palette is a draft that will change to Horus University's colours.

## Repository layout

- `Section N - files/` — the section source for section N: a `.docx` (Section 1) or an older `.pptx` deck (Section 2), with the SPSS screenshots embedded. This is the only content source for the slides.
- `سكشن N — <Arabic title>.pptx` / `.ppsx` — the exported Arabic deck at the repo root, after `tools/fix_rtl.py` (see Arabic RTL).
- `tools/` — `fix_rtl.py` makes an exported deck's Arabic paragraphs right-to-left; `make_ppsx.py` turns the `.pptx` into the `.ppsx`.
- `README.md` — table of sections with links to their decks.

## Making a section

When the user asks for a section ("اعمل سكشن 2", "make section 3", or adds a new `Section N - files/` folder), follow the `new-section` skill in `.claude/skills/new-section/SKILL.md`.

Hard rules (from the design system):

- **Never invent content.** Slides carry the document's own definitions, examples and exercises. Anything added for teaching goes in speaker notes.
- SPSS interface words stay in English exactly as SPSS shows them (`Variable View`, `Type`, `Values`, `Scale`), inside Arabic sentences.
- Arabic decks: `text-align:right`, rows in visual order (never `row-reverse`), no `<ul>`/`<ol>`, no letter-spacing. See "Arabic RTL" below.

## Arabic RTL

An Arabic deck is seen in two places, and each needs its own fix:

1. **The claude.ai page** (and the export's layout, which comes from the same engine). Every text box has a left-to-right base, and neither `direction` nor `dir` is supported. The browser does honour U+202B … U+202C (RLE … PDF) inside a box.
2. **PowerPoint** ignores RLE … PDF. It follows each paragraph's `rtl` attribute, which the export never sets. Without it, a mixed line comes out as `Data View إدخال البيانات في`.

Rules for the slide HTML:

- **One sentence, one text box, wrapped in U+202B … U+202C.** This includes sentences with SPSS terms in them: `<h2>‫إدخال البيانات في Data View‬</h2>`, `<p>‫… لذلك نعرّفها في خانة Missing في نافذة Variable View‬</p>`, and the footer `<p>‫Computer Application · سكشن 2‬</p>`. Never split a sentence into several boxes laid out in a row.
- **Never use `flex-direction:row-reverse`.** The engine does not store it. It reorders the children and keeps `justify-content` as written, so the row hugs the left edge, and when it wraps, the end of the sentence moves up to the first line. Section 2's second draft broke this way. Write every row as `flex-direction:row; justify-content:flex-end`, with the children in visual order, left to right: the first thing read is the last child. A row with `space-between` keeps it. The design system's README and the Section 1 deck still use `row-reverse`; this rule overrides them.
- **SPSS names of two or more words** get a no-break space (U+00A0) between the words inside Arabic text, so a line never splits `Data View` or `Case Processing Summary`.
- **Fill-in blanks:** a row with `justify-content:flex-end; align-items:end` and no wrap. It holds, left to right, the unit `<p>` (if any), the blank `<div style="width:130px; height:40px; border-bottom:2px dashed #46546B">`, and the Arabic `<p>`. Keep it short enough for one line.
- **Tables:** columns are written in visual order, left to right, so the first column read is the last cell. A cell that mixes languages is written Arabic-first and wrapped in RLE … PDF (`‫الذكور في قسم IT‬`).
- Avoid starting an Arabic box with a number or ending it with `........`. Use a badge for numbering and a dashed box for a blank.

Rules for the exported file:

- Export the Arabic deck with **Share › Export › PowerPoint, basic fonts (.pptx)**, which uses Tahoma, as in Section 1. Then run `python3 tools/fix_rtl.py "<deck>.pptx"` before `tools/make_ppsx.py`. It sets `rtl="1"` and `lang="ar-EG"` on every Arabic paragraph (slides, tables, speaker notes) and removes the bidi control characters, matching how the Section 1 file is written.

General:

- Western digits in both languages; two-digit page numbers in the footer.
- Same slide run every time: Cover → Agenda → (Divider → content) × parts → Exercises divider → per exercise: data, questions, answers → Wrap-up.
