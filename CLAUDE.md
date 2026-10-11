# Computer Application 2026–2027

Source material for the **Computer Application (SPSS) lab sections**, Horus University, 2026/2027.
Every section becomes two slide decks — Arabic (right-to-left) and English — built from one design system, so every section in the series looks the same.

## Linked artifacts (claude.ai)

| What | Link |
| --- | --- |
| Design system — *Computer Application Sections* (namespace `compapp`) | https://claude.ai/artifact/VLRrkrryr4GtjK1rRZivek |
| Slides artifact type (new decks are created from it) | https://claude.ai/artifact/8jTsAFQMFDb2oA8MsPJ2eL |
| Section 1 deck, Arabic — reference for every layout's markup | https://claude.ai/artifact/DPpuZy1phoURcg819GWUhY |
| Section 1 deck, English | https://claude.ai/artifact/ANxUTh6YSTC7vW3xHRTQBo |

The design system is the single source of truth for colours, type, layouts and RTL rules. Read it fresh each time (`project/README.md`, `project/slide-layouts.md`, `project/tokens.json`): its palette is a draft that will change to Horus University's colours.

## Repository layout

- `Section N - files/` — the section document(s) for section N (`.docx` with the SPSS screenshots embedded). This is the only content source for the slides.
- `سكشن N — <Arabic title>.pptx` / `.ppsx` — the exported Arabic deck at the repo root.
- `README.md` — table of sections with links to their decks.

## Making a section

When the user asks for a section ("اعمل سكشن 2", "make section 3", or adds a new `Section N - files/` folder), follow the `new-section` skill in `.claude/skills/new-section/SKILL.md`.

Hard rules (from the design system):

- **Never invent content.** Slides carry the document's own definitions, examples and exercises. Anything added for teaching goes in speaker notes.
- SPSS interface words stay in English exactly as SPSS shows them (`Variable View`, `Type`, `Values`, `Scale`), inside Arabic sentences.
- Arabic decks: wrap every Arabic text node in U+202B … U+202C, `text-align:right`, `flex-direction:row-reverse` on rows, no `<ul>`/`<ol>`, no letter-spacing.
- Western digits in both languages; two-digit page numbers in the footer.
- Same slide run every time: Cover → Agenda → (Divider → content) × parts → Exercises divider → per exercise: data, questions, answers → Wrap-up.
