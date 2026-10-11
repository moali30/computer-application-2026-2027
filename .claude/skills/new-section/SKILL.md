---
name: new-section
description: Build the next Computer Application (SPSS) lab section as two slide decks, Arabic (RTL) and English, from the section's .docx in `Section N - files/`, using the "Computer Application Sections" design system so it matches Section 1. Use when the user says "اعمل سكشن N", "سكشن جديد", "make section N", "build the slides for section N", or adds a new `Section N - files/` folder.
---

# New section

Turns `Section N - files/*.docx` into an Arabic deck and an English deck on claude.ai, built from the design system linked in `CLAUDE.md`.

## 1. Read the source

1. Find `Section N - files/`. No folder or no `.docx` for N: ask the user to upload the section document and stop.
2. Convert it in the scratchpad (never inside the repo):
   `pandoc "Section N - files/<doc>.docx" -t gfm --extract-media=<scratch>/sN -o <scratch>/sN/source.md`
3. Read `source.md` in full. Note, in document order: the parts (headings), each definition, each SPSS step, each screenshot (`<scratch>/sN/media/imageK.png`) and what it shows, and each exercise with its data, questions and answers.

## 2. Read the design system and the reference deck

In one message:

- Design system `https://claude.ai/artifact/VLRrkrryr4GtjK1rRZivek`: read `project/README.md`, `project/slide-layouts.md`, `project/tokens.json`. Use the hex values from `tokens.json` as they are now, not from memory or from Section 1.
- Section 1 Arabic deck `https://claude.ai/artifact/DPpuZy1phoURcg819GWUhY`: read the slide of each layout you will use and copy its markup. Known slides by layout:
  `cover` Cover · `agenda` Agenda · `d1` `d2` `d3` Divider · `type` Screenshot · `ex1data` Exercise data · `ex1q` Exercise questions · `ex1ans` Exercise answers · `summary` Wrap-up.
  The remaining content slides (`variable`, `measures`, `textnum`, `idnote`, `spss`, `windows`, `vview`, `name`, `wdl`, `values`, `missing`, `cam`, `dview`) are Concept, Accent statement, Screenshot and Property-card slides; the section background tells them apart (`paper` = concept or property cards, `paper-alt` = screenshot, `amber` = accent statement).
- For the English deck, read the same slides from `https://claude.ai/artifact/ANxUTh6YSTC7vW3xHRTQBo`.

## 3. Outline

Map the document onto the fixed run: Cover → Agenda → (Divider → content slides) × parts → Exercises divider → per exercise: data, questions, answers → Wrap-up. One idea per slide; split a slide rather than shrink text. Exactly one Accent statement slide (the section's "watch out" idea, taken from the document). Tell the user the outline in a few lines (parts and slide count), then build without waiting unless something in the source is unclear.

## 4. Build both decks

For each language:

1. Create the deck: Artifact publish with `type_url` = `https://claude.ai/artifact/8jTsAFQMFDb2oA8MsPJ2eL`, `title` = `سكشن N — <Arabic title>` / `Section N — <English title>`, `auto_open: "after_first_write"`, no files. Follow the Slides type instructions the reply returns.
2. Upload each screenshot from `<scratch>/sN/media/` to that deck as an asset and use the returned `/_blob/<id>` in `<img src>`. Screenshots use `object-fit:contain` on a `card` mat and are never cropped. The English deck uses translated copies of the screenshots if the user supplied them; otherwise the same images, and say so.
3. Write every `project/slides/<id>.html` and `project/deck.json` under one scratchpad folder. Reuse Section 1's slide ids where the layout matches (`cover`, `agenda`, `d1`…, `ex1data`, `ex1q`, `ex1ans`…, `summary`). In `deck.json`:
   - `faces`: the same three Google Fonts entries as Section 1 (Readex Pro, IBM Plex Sans Arabic, IBM Plex Mono).
   - `sections`: one entry per part, in the deck's language.
   - `designSystems`: `{"title":"Computer Application Sections","namespace":"compapp","artifact":"https://claude.ai/artifact/VLRrkrryr4GtjK1rRZivek","version":null,"copiedAt":"<now>"}`, and install its tokens with `files["project/ds/compapp/tokens.json"] = {"artifact":"https://claude.ai/artifact/VLRrkrryr4GtjK1rRZivek","path":"project/tokens.json"}`.
4. Footer on every content slide: `Computer Application · سكشن N` (Arabic) or `Computer Application · Section N` (English) plus the two-digit page number. Cover eyebrow: the same course · section line.
5. Exercise answers go on the answers slide and in the questions slides' speaker notes.
6. Publish all files in one call per deck.

## 5. Record it in the repo

1. Add the section to the table in `README.md` with both deck links.
2. The `.pptx` comes from the Arabic deck's Share › Export (download as PowerPoint). Ask the user to export it and upload it, named `سكشن N — <Arabic title>.pptx`. When it is in the repo, make the `.ppsx` from it with `python3 tools/make_ppsx.py "<the .pptx>"` (it only changes the presentation's content type, which is the one difference between the two Section 1 files).
3. Commit the source document, README and any exported decks on the working branch and push.

## 6. Report

Give the user both deck links, the slide count per deck, any content you could not place (for example a screenshot the text never references), and anything left for them (exporting the `.pptx`, translated screenshots).
