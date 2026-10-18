# Handoff: continuing this project from a new Claude account

This repository is the complete record of the Computer Application (SPSS) sections project, moved here on 2026-10-18 so the work can continue from a different Claude account. Everything a fresh Claude needs is in this repo; nothing depends on the old account's chats or memory.

## Start here (fresh account)

1. Sign in to claude.ai with the new account and connect GitHub: https://claude.ai/connect-github
2. Open Claude Code on the web (claude.ai/code) or create a Project, and add the repo `moali30/computer-application-2026-2027`.
3. Tell Claude: **"اقرا HANDOFF.md و CLAUDE.md وخلّص ملف PowerPoint بتاع سكشن 3"**, then **"اعمل سكشن 4"** for the next one.

Claude Code reads `CLAUDE.md` automatically; the `new-section` skill in `.claude/skills/new-section/SKILL.md` is the step-by-step recipe.

## Where things stand

| Section | Topic | State | Where |
| --- | --- | --- | --- |
| 1 | Introduction to SPSS | Done: Arabic + English decks, `.pptx` / `.ppsx` | repo root, `Section 1 - files/` |
| 2 | Missing values and descriptive statistics | Done: Arabic + English decks, `.pptx` / `.ppsx` | repo root, `Section 2 - files/` |
| 3 | Questionnaire reliability (Cronbach's alpha) | Decks done: 20 Arabic + 20 English slides ([Arabic](https://claude.ai/artifact/TGvyXFyJS92FRpTcqjLnb9), [English](https://claude.ai/artifact/RhHxJFmTCrA5LiJYEvdgbv)). **Left:** the `.pptx` / `.ppsx` | PR #2 (branch `claude/section-3-rkdy8z`): source, slide code, plan. Approved decisions also in [`docs/section-3-plan.md`](docs/section-3-plan.md) |

### Merge order

1. Merge PR #3 (this handoff; it also carries PR #1 with Section 2).
2. Merge PR #2 (Section 3 source, slide code and plan). Mark it ready for review first if it is still a draft.

### The one step left for Section 3

Export the Arabic deck (Share › Export › PowerPoint, basic fonts), save it at the repo root as `سكشن 3 — <Arabic title>.pptx`, run `python3 tools/fix_rtl.py "<the .pptx>"` and then `python3 tools/make_ppsx.py "<the .pptx>"`, fill in the Files column of the Section 3 row in `README.md`, and commit. The export has to happen from an account that can open the deck, so share it first (below).

## The claude.ai artifacts (important)

The slide decks and the design system are claude.ai artifacts owned by the **old** account (links in `README.md` and `CLAUDE.md`). A new account can only open or copy them if they were shared with it. Before the old account's access ends, open each link from the old account and share it, including the Section 3 decks above, (Share › anyone with the link, or invite the new email). If that isn't possible:

- The exported `.pptx` / `.ppsx` files in this repo are the durable copies of Sections 1 and 2. Section 3's slide HTML is also stored in the repo under `Section 3 - files/decks/` (after PR #2 is merged).
- The design system's colours, fonts and layout rules are written down in `CLAUDE.md`, `.claude/skills/new-section/SKILL.md`, and the token values at the top of `tools/legacy-kit/sectionkit.py`. A new account can recreate the design system from those.

## How Mohamed wants sections made

See [`docs/preferences.md`](docs/preferences.md). In short: one Arabic deck (RTL) and the same deck in English, Horus University colours, cover and footer show only the course and section (no instructor name), content comes only from the section file, and extra application questions should explain *why* we do each analysis with a real-life scenario.

## Repository map

- `README.md`: section table with deck links.
- `CLAUDE.md`: rules Claude follows in this repo (design system, Arabic RTL technique).
- `.claude/skills/new-section/SKILL.md`: the recipe for building a section.
- `Section N - files/`: source material for each section (the only content source).
- `سكشن N — ….pptx` / `.ppsx`: exported Arabic decks (after `tools/fix_rtl.py`).
- `tools/fix_rtl.py`, `tools/make_ppsx.py`: fix Arabic direction in an exported PowerPoint; make the `.ppsx`.
- `tools/legacy-kit/`: the older Python kit used for Section 1 (layout generator, local preview renderer, first RTL fixer). Kept for reference and for its token values; the skill above is the current method.
- `docs/section-workflow-v1.md`: the original workflow notes from the first project.
- `docs/preferences.md`: Mohamed's stated preferences.
- `docs/section-3-plan.md`: the approved decisions and computed answers for Section 3.
