# Computer Application 2026–2027

SPSS lab sections for Computer Application, Horus University, 2026/2027. Every section has an Arabic deck and an English deck built from the **[Computer Application Sections](https://claude.ai/artifact/VLRrkrryr4GtjK1rRZivek)** design system.

## Sections

| # | Arabic deck | English deck | Source | Files |
| --- | --- | --- | --- | --- |
| 1 | [سكشن 1 — مقدمة في SPSS](https://claude.ai/artifact/DPpuZy1phoURcg819GWUhY) | [Section 1 — Introduction to SPSS](https://claude.ai/artifact/ANxUTh6YSTC7vW3xHRTQBo) | `Section 1 - files/SPSS عربي 1.docx` | `سكشن 1 — مقدمة في SPSS.pptx`, `.ppsx` |
| 2 | [سكشن 2 — القيم المفقودة والإحصاء الوصفي](https://claude.ai/artifact/6XUd3RE5KfiNeb258rk8sV) | [Section 2 — Missing Values and Descriptive Statistics](https://claude.ai/artifact/MVBsPhQFzoAijkU4GrTBxS) | `Section 2 - files/SPSS عربي 2.pptx` | not exported yet |

## Adding a section

1. Upload the section's source, a `.docx` or an older `.pptx`, to a new folder `Section N - files/`, or send it in the chat.
2. Ask Claude Code in this repo: **"اعمل سكشن N"**. It follows `CLAUDE.md` and `.claude/skills/new-section/SKILL.md`, builds both decks from the design system, and adds a row above.
3. Export the Arabic deck as PowerPoint (Share › Export), upload it as `سكشن N — <title>.pptx`, and make the `.ppsx` with `python3 tools/make_ppsx.py "<the .pptx>"`.
