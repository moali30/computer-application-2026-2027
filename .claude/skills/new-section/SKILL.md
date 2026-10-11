---
name: new-section
description: Build the next Computer Application (SPSS) lab section as two slide decks, Arabic (RTL) and English, from the section's source (.docx or an older .pptx) in `Section N - files/`, using the "Computer Application Sections" design system so it matches the earlier sections. Use when the user says "اعمل سكشن N", "سكشن جديد", "make section N", "build the slides for section N", uploads a section file, or adds a new `Section N - files/` folder.
---

# New section

Turns the source in `Section N - files/` into an Arabic deck and an English deck on claude.ai, built from the design system linked in `CLAUDE.md`.

## 1. Read the source

1. Find `Section N - files/`. If the user uploaded the file in chat instead, copy it there as `SPSS عربي N.<ext>`. If there is still no source, ask for one and stop.
2. Extract it in the scratchpad (never inside the repo):
   - `.docx`: `pandoc "<doc>.docx" -t gfm --extract-media=<scratch>/sN -o <scratch>/sN/source.md`, then read `source.md` in full.
   - `.pptx`: unzip it to `<scratch>/sN/src` and dump every slide's text, tables and pictures with `python-pptx` (per slide: text frames, table rows, and picture names). Map pictures to slides from `ppt/slides/_rels/slideK.xml.rels`, and view every image in `ppt/media/`.
3. Note, in source order: the parts, each definition, each SPSS step and menu path, each screenshot and what it shows, and each example or exercise with its data, questions and answers.
4. Check the source against itself. Recompute the answers from the data, and compare each screenshot with its data table. Fix plain errors on the slides, put a note in that slide's speaker notes, and list every fix for the user. Section 2 had three: a variance squared from a rounded standard deviation, a task naming a different variable than its solution, and typos in a Data View screenshot.

## 2. Read the design system and the reference deck

In one message:

- Design system `https://claude.ai/artifact/VLRrkrryr4GtjK1rRZivek`: read `project/README.md`, `project/slide-layouts.md`, `project/tokens.json`. Use the hex values from `tokens.json` as they are now, not from memory or from an earlier section.
- Section 2 Arabic deck `https://claude.ai/artifact/6XUd3RE5KfiNeb258rk8sV`: read the slides of the layouts you will use and copy their markup, including the RTL handling (see `CLAUDE.md` → Arabic RTL). Slides by layout:
  `cover` Cover · `agenda` Agenda · `d1`…`d5` Divider · `desc`, `graphs`, `meas` Concept · `mv-note` Accent statement · `mv-vview`, `tb-vview` wide Screenshot (image above callouts) · `mv-dview`, `tb-freq`, `gr-box` Screenshot (image beside callouts) · `gr-histans` stat cards · `mv-data`, `tb-data` Exercise data · `ex1q` Exercise questions with a screenshot and fill-in blanks · `ex1ans` Exercise answers · `summary` Wrap-up.
- For the English deck, read the same slides from `https://claude.ai/artifact/MVBsPhQFzoAijkU4GrTBxS`.
- Section 1 (`https://claude.ai/artifact/DPpuZy1phoURcg819GWUhY`) has multiple-choice question slides (`ex1q`) and property cards (`wdl`), but uses the older RTL technique. Copy its layout, not its text markup.

## 3. Outline

Map the source onto the fixed run: Cover → Agenda → (Divider → content slides) × parts → Exercises divider → per exercise: data, questions, answers → Wrap-up.

- Worked examples, which show how to do something in SPSS, stay inside their part as data slide + solution screenshots.
- Read-the-output questions go to the exercises part.
- One idea per slide. Split a slide rather than shrink text.
- Exactly one Accent statement slide, carrying the section's "watch out" idea from the source.
- Leave out the faculty vision/mission and "Thank you" slides; earlier sections don't have them.

Tell the user the outline in a few lines (parts and slide count), then build without waiting unless something in the source is unclear.

## 4. Build both decks

For each language:

1. Create the deck: Artifact publish with `type_url` = `https://claude.ai/artifact/8jTsAFQMFDb2oA8MsPJ2eL`, `title` = `سكشن N — <Arabic title>` / `Section N — <English title>`, `auto_open: "after_first_write"`, no files. Follow the Slides type instructions the reply returns: write files with the file tool, publish `deck.json` and the cover first, then a few slides per publish.
2. Upload each screenshot to that deck as an asset and use the returned `/_blob/<id>` in `<img src>`. Screenshots use `object-fit:contain` on a `card` mat and are never cropped. Skip clip-art icons; the design system bans stock images. The English deck uses translated copies of the screenshots if the user supplied them. Otherwise it uses the same images, and you say so.
3. In `deck.json`:
   - `faces`: Readex Pro, IBM Plex Sans Arabic, IBM Plex Mono (Google Fonts, as in Section 2).
   - `sections`: one entry per part, in the deck's language.
   - `designSystems`: `{"title":"Computer Application Sections","namespace":"compapp","artifact":"https://claude.ai/artifact/VLRrkrryr4GtjK1rRZivek","version":<the version you read>,"copiedAt":"<now>"}`, and install its tokens with `files["project/ds/compapp/tokens.json"] = {"artifact":"https://claude.ai/artifact/VLRrkrryr4GtjK1rRZivek","path":"project/tokens.json"}`.
4. **Arabic deck: follow `CLAUDE.md` → Arabic RTL on every text box.** Keep one language per box, with no edge punctuation or leading numbers. Mixed sentences go in row-reverse segment rows, the footer and eyebrow are segment rows, and fill-in blanks are dashed boxes. This is the step that broke Section 2's first draft.
5. Footer on every content slide: `Computer Application · سكشن N` (Arabic, as a segment row) or `Computer Application · Section N` (English), plus the two-digit page number.
6. Exercise answers go on the answers slide and in the questions slides' speaker notes.

## 5. Record it in the repo

1. Put the source in `Section N - files/` and add the section to the table in `README.md` with both deck links.
2. The `.pptx` comes from the Arabic deck's Share › Export (download as PowerPoint). Ask the user to export it and upload it, named `سكشن N — <Arabic title>.pptx`. When it is in the repo, make the `.ppsx` from it with `python3 tools/make_ppsx.py "<the .pptx>"`. That script only changes the presentation's content type, which is the one difference between the two Section 1 files.
3. Commit the source, README and any exported decks on the working branch and push.

## 6. Report

Give the user both deck links and the slide count per deck. Also list every source error you fixed, any content you left out, and anything left for them: exporting the `.pptx`, sharing the decks, translated screenshots.
