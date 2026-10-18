# Section 3 — Questionnaire reliability (Cronbach's alpha): approved plan

Status on 2026-10-18: questions asked and all recommendations approved by Mohamed; numbers computed; decks not built yet. Deck work happens on branch `claude/section-3`.

## Source

- `Section 3 - files/spss section 3.docx`: a single exercise titled "السؤال الثاني". An e-learning attitudes survey, 6 five-point Likert items (q1–q6), 10 students. Tasks: compute Cronbach's alpha for the whole scale; if it is low, use Item-Total Statistics ("Cronbach's Alpha if Item Deleted") to decide which item to drop. No theory text, no images.
- `Section 3 - files/data-screenshot.jpeg`: SPSS Data View of the same data.

Data (q1..q6 per student):

```
1: 4 4 5 1 3 4     6:  1 2 1 5 5 5
2: 4 5 4 1 5 4     7:  2 1 2 1 1 3
3: 5 4 5 2 4 4     8:  5 5 4 5 3 3
4: 3 3 4 5 3 2     9:  1 1 2 4 3 2
5: 2 2 1 4 2 2    10:  2 3 2 3 4 2
```

## Decisions Mohamed approved (all recommended options)

1. The screenshot is the same exercise as the docx, not a missing first question. (If a "first question" turns up, add it.)
2. Claude writes a **short** theory part: what reliability is, what Cronbach's alpha means, rule-of-thumb thresholds, and the SPSS steps (Analyze › Scale › Reliability Analysis, Statistics › "Scale if item deleted").
3. Scenario: keep the e-learning survey and frame it as **a researcher who wants to make sure her questionnaire works before sending it to a large sample** (a pilot test).
4. Why q4 hurts reliability: explain it as a **reverse-worded item**, as an idea only, no Recode steps.
5. Add **2** applied questions: one comprehension MCQ, and one small exercise with new data and a real-life scenario.
6. Same format as Sections 1–2: Arabic and English decks in the same design, and the Arabic `.pptx` / `.ppsx` in the repo.
7. Claude cannot run SPSS, so the SPSS output tables (Reliability Statistics, Item-Total Statistics) are **drawn as SPSS-style tables with the correct numbers**.

## Computed answers for the given exercise

- Cronbach's alpha (6 items) = **0.627**, below the usual 0.70.
- Corrected item-total correlation: q1 .660, q2 .829, q3 .570, **q4 −.279**, q5 .427, q6 .315.
- Alpha if item deleted: q1 .449, q2 .368, q3 .489, **q4 .828**, q5 .562, q6 .601.
- Conclusion: q4 correlates negatively with the rest (it runs opposite to the other items, likely a negatively worded statement). Deleting it raises alpha to about 0.83. Reverse-coding it instead would give about 0.79.

Recompute everything from the data before putting it on slides.
