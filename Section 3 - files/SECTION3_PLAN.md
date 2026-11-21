# Section 3 — Questionnaire reliability (Cronbach's alpha)

Build plan agreed with Mohamed on 2026-10-18. Anyone continuing this section (another Claude account included) starts here, together with the kit workflow (`section-workflow.md`, `sectionkit.py`, `section1.py`).

## Sources
- `spss section 3.docx`: holds one exercise only ("السؤال الثاني"): e-learning attitudes survey, 6 Likert-5 items (q1..q6), 10 students. Tasks: Cronbach's alpha for the whole scale; if low, Item-Total Statistics with "Scale if Item Deleted" to find the item whose deletion raises alpha.
- `data-screenshot.jpeg`: SPSS Data View of the same data (604×302). Not used on the slides: Mohamed wants a typed data table so students enter the data themselves.
- There is no Section 2 in the repo or project; Section 3 does not depend on it.

## Decisions (Mohamed approved all recommendations)
1. The screenshot is the same data as the docx question; no missing "question 1".
2. Write a short theory part (what reliability is, Cronbach's alpha, how to read it, SPSS steps).
3. Keep the e-learning story, framed as: a researcher pilots her questionnaire on 10 students before sending it to a large sample, to check the items measure the same thing.
4. Explain why q4 breaks reliability as a concept (a reverse / negatively worded item). No Recode steps in SPSS.
5. Add 2 applied items: an MCQ concept quiz + one small exercise with new data.
6. Output like Section 1: Arabic and English Slides decks in the same design system, plus a pptx copy in the repo (Arabic pptx fixed with `fix_rtl_pptx.py`).
7. No real SPSS screenshots of menus/output: draw the output tables in SPSS style with the exact numbers below.
8. Keep the section small (about 20 slides per language; Section 1 had 29).

## Update 2026-10-18 (Mohamed's follow-up)
Added a short hook slide [hook] after the cover, and the course case study ([case], [items]) after divider 1, defining the six items (q4 negatively worded). The case is documented in `/CASE_STUDY.md` for later sections. Deck is now 23 slides per language.

## Slide outline (ids in brackets)
1. [cover] Computer Application · Section 3 — ثبات الاستبيان: معامل ألفا كرونباخ / Questionnaire reliability: Cronbach's alpha. Subtitle: هل يمكن الوثوق في إجابات الاستبيان؟
2. [agenda] why reliability; Cronbach's alpha and how to judge it; running it in SPSS and reading the output; two exercises + quiz.
3. [d1] divider 1/3 — لماذا نقيس الثبات؟
4. [why] story + analogy: a bathroom scale that reads 70, 75, 68 for the same person is not reliable; a questionnaire whose items disagree is the same. The researcher pilots 10 students before 400.
5. [alpha] definition: reliability = consistency; Cronbach's alpha measures internal consistency of Likert items, 0 to 1. Judgement table: ≥ 0.90 excellent · 0.80–0.89 good · 0.70–0.79 acceptable · 0.60–0.69 weak · < 0.60 unacceptable. 0.70 is the usual minimum.
6. [d2] divider 2/3 — ألفا كرونباخ في SPSS
7. [steps] Analyze › Scale › Reliability Analysis; move q1..q6 to Items; Model = Alpha; Statistics… › tick "Scale if item deleted" (Descriptives for: Item, Scale optional) › Continue › OK.
8. [read] two output tables: Reliability Statistics (Cronbach's Alpha, N of Items) and Item-Total Statistics. Key columns: Corrected Item-Total Correlation (negative or < 0.30 = weak item) and Cronbach's Alpha if Item Deleted (higher than the current alpha = deleting helps).
9. [d3] divider 3/3 — تمارين تطبيقية
10. [ex1data] shot_slide with the screenshot, the story, the scale labels (1 = لا أوافق بشدة … 5 = أوافق بشدة) and the task card.
11. [ex1q] MCQ: alpha of the whole scale (a .627 b .828 c .368 d .700 → a); is it acceptable (→ no, weak, below 0.70); which item's deletion raises alpha most (→ q4); alpha after deleting it (→ .828). Answers in speaker notes.
12. [ex1out1] Reliability Statistics table: Cronbach's Alpha .627, N of Items 6 → below 0.70, weak, inspect items.
13. [ex1out2] Item-Total Statistics table (below), q4 row highlighted.
14. [reverse] the one amber statement slide: "عبارة واحدة معكوسة تكفي لإسقاط الثبات" — q4 has a negative item-total correlation (−.279): students who agree with the other items disagree with it, so it is probably worded negatively (e.g. "أفضّل المحاضرات التقليدية على التعليم الإلكتروني"). Fix: delete it (alpha .828) or reverse-code it as 6 − value (alpha .787, concept only).
15. [ex1decision] before/after: .627 (weak) → .828 (good) after deleting q4. Report sentence: بلغ معامل ألفا كرونباخ 0.83 بعد حذف العبارة الرابعة، وهو ما يدل على ثبات جيد للمقياس.
16. [ex2data] new data (below).
17. [ex2q] MCQ: alpha (→ .888); judgement (→ good); delete an item? (→ no: alpha is already good and every item correlates above .30).
18. [ex2ans] answers table + Item-Total table.
19. [quiz] 3 concept MCQs: alpha 0.45 means (→ unacceptable, revise items); a negative Corrected Item-Total Correlation means (→ the item runs against the others, maybe reversed); alpha is used for (→ Likert questionnaire items, not ID or gender).
20. [summary] wrap-up: reliability = consistency; alpha ≥ 0.70; read Item-Total to find a weak item; a reverse item shows a negative correlation.

## Exercise 1 numbers (docx data, verified in Python with SPSS formulas)
Data (q1..q6 per student):
```
4 4 5 1 3 4
4 5 4 1 5 4
5 4 5 2 4 4
3 3 4 5 3 2
2 2 1 4 2 2
1 2 1 5 5 5
2 1 2 1 1 3
5 5 4 5 3 3
1 1 2 4 3 2
2 3 2 3 4 2
```
Reliability Statistics: Cronbach's Alpha = .627, N of Items = 6.

Item-Total Statistics:
| Item | Scale Mean if Item Deleted | Scale Variance if Item Deleted | Corrected Item-Total Correlation | Cronbach's Alpha if Item Deleted |
|---|---|---|---|---|
| q1 | 15.50 | 16.278 | .660 | .449 |
| q2 | 15.40 | 14.933 | .829 | .368 |
| q3 | 15.40 | 16.933 | .570 | .489 |
| q4 | 15.30 | 28.900 | −.279 | .828 |
| q5 | 15.10 | 20.322 | .427 | .562 |
| q6 | 15.30 | 22.233 | .315 | .601 |

After deleting q4: alpha = .828 (5 items). q4 reverse-coded (6 − value) instead: alpha = .787.

## Exercise 2 (new data, written for this section)
Story: the department asks 8 students to rate the Computer Application course on 5 Likert-5 items before using the form for all students. Suggested items: q1 الشرح في السكشن واضح · q2 التمارين مرتبطة بالمحاضرة · q3 الوقت كافٍ للتطبيق على SPSS · q4 المعيد يجيب عن الأسئلة · q5 أستطيع تطبيق ما تعلمته وحدي.
```
5 4 4 4 5
4 3 4 3 4
2 3 3 2 1
3 4 2 4 3
5 5 4 3 5
2 2 1 2 3
4 5 3 4 3
1 2 2 3 2
```
Reliability Statistics: Cronbach's Alpha = .888, N of Items = 5 (good).

| Item | Scale Mean if Item Deleted | Scale Variance if Item Deleted | Corrected Item-Total Correlation | Cronbach's Alpha if Item Deleted |
|---|---|---|---|---|
| q1 | 12.75 | 13.357 | .959 | .802 |
| q2 | 12.50 | 17.143 | .751 | .858 |
| q3 | 13.13 | 18.125 | .689 | .872 |
| q4 | 12.88 | 20.982 | .565 | .899 |
| q5 | 12.75 | 15.929 | .735 | .864 |

Lesson: all correlations are positive and above .30, and alpha is already good, so no item is deleted. Deleting q4 would only nudge alpha from .888 to .899, not worth losing an item (teaching point for speaker notes).

## Build status
- Built: 23 slides per language, generated by `section3.py` (needs `sectionkit.py` from the kit beside it). Generated slide files are in `decks/ar` and `decks/en`; contact sheets in `decks/preview-*.png`.
- Arabic deck: https://claude.ai/artifact/TGvyXFyJS92FRpTcqjLnb9
- English deck: https://claude.ai/artifact/RhHxJFmTCrA5LiJYEvdgbv
- Both decks belong to Mohamed's first claude.ai account. From another account, publish new decks from `decks/ar` and `decks/en`.
- Design system: https://claude.ai/artifact/VLRrkrryr4GtjK1rRZivek (namespace `compapp`).
- PowerPoint: `سكشن 3 — ثبات الاستبيان.pptx` / `.ppsx` in the repo root, made from the Slides PPTX export (2026-10-18) with `fix_rtl_pptx.py` (this folder; it now turns LRI-isolated numbers into an LRM prefix so .627 and −.279 keep their order). After the script, slide 13's table was shrunk by hand (cell sz 1263→1150, cell top/bottom margins 31750→12700 EMU) so row 10 clears the task tag; redo that after a fresh export. Then run `add_answer_animations.py` (this folder): on slides 14, 20 and 22 it adds a green highlight on each correct option that fades in on click, one question per click.
