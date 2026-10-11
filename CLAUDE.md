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
| Section 1 deck, Arabic (older RTL technique, see below) | https://claude.ai/artifact/DPpuZy1phoURcg819GWUhY |
| Section 1 deck, English | https://claude.ai/artifact/ANxUTh6YSTC7vW3xHRTQBo |

The design system is the single source of truth for colours, type, layouts and RTL rules. Read it fresh each time (`project/README.md`, `project/slide-layouts.md`, `project/tokens.json`): its palette is a draft that will change to Horus University's colours.

## Repository layout

- `Section N - files/` — the section source for section N: a `.docx` (Section 1) or an older `.pptx` deck (Section 2), with the SPSS screenshots embedded. This is the only content source for the slides.
- `سكشن N — <Arabic title>.pptx` / `.ppsx` — the exported Arabic deck at the repo root.
- `README.md` — table of sections with links to their decks.

## Making a section

When the user asks for a section ("اعمل سكشن 2", "make section 3", or adds a new `Section N - files/` folder), follow the `new-section` skill in `.claude/skills/new-section/SKILL.md`.

Hard rules (from the design system):

- **Never invent content.** Slides carry the document's own definitions, examples and exercises. Anything added for teaching goes in speaker notes.
- SPSS interface words stay in English exactly as SPSS shows them (`Variable View`, `Type`, `Values`, `Scale`), inside Arabic sentences.
- Arabic decks: `text-align:right`, `flex-direction:row-reverse` on rows, no `<ul>`/`<ol>`, no letter-spacing. See "Arabic RTL" below.

## Arabic RTL

The current Slides runtime strips bidi control characters (U+202A–U+202E, U+2066–U+2069, U+200E/F) and supports neither `direction` nor `dir`. Every text box therefore renders with a left-to-right base. The U+202B … U+202C wrapping in the design system's README no longer works on its own. Section 1 was built that way and breaks once its deck moves to the new runtime.

Rules that keep Arabic correct under an LTR base:

- **One language per text box.** A `<p>`/`<h*>` holding Arabic holds only Arabic letters, digits and Arabic punctuation inside the sentence. Digits inside or at the end are fine (`سكشن 2`, `الحالتان 6 و7`).
- **Edges:** an Arabic box starts with an Arabic letter, and ends with an Arabic letter or a digit. Do not end it with a period, colon or `........`, and do not start it with a number or a bullet. Rephrase instead: `القيمة 500 هنا…`, not `500 هنا…`.
- **Mixed sentences** (an SPSS term inside Arabic) become a row of segments: `<div style="display:flex; flex-direction:row-reverse; flex-wrap:wrap; gap:8px">` holding one `<p>` per run (Arabic, English, Arabic…). Set the font size, line height and colour on each `<p>`, not on the div.
- **Mixed titles** use the same row with two `<h2>`s (`‫إدخال البيانات في‬` + `Data View`).
- **Footer and eyebrows:** a row-reverse of `Computer Application` · `·` · `سكشن N`.
- **Fill-in blanks:** a `<div style="width:130px; height:40px; border-bottom:2px dashed #46546B">` segment inside the row, never `........` at a sentence's edge.
- **Table cells** cannot hold a row. Keep each cell in one language. For a short single-line cell that must mix, write the English word first (`IT الذكور في قسم`), so it shows at the reading end.
- Leaving the U+202B … U+202C wrap on Arabic boxes is harmless, and Section 2 keeps it.
- Western digits in both languages; two-digit page numbers in the footer.
- Same slide run every time: Cover → Agenda → (Divider → content) × parts → Exercises divider → per exercise: data, questions, answers → Wrap-up.
