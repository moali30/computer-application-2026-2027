# Section 5 — The chi-square test of independence

Built on 2026-11-21 from the lecture PDF Mohamed uploaded (`المحاضرة الخامسة SPSS.pdf`, 18 slides). Read with `HANDOFF.md`, `CLAUDE.md`, `CASE_STUDY.md` and `Section 4 - files/SECTION4_PLAN.md` (same build pipeline).

## Source (the lecture)
- Relationship between two qualitative traits; examples: income × education, eye × hair colour, achievement × family income.
- Chi-square of independence: two nominal variables, or one nominal and one ordinal.
- Steps: hypotheses (H0 no significant relationship / independent; H1 a relationship / not independent) → SPSS → compare Sig with α (Sig ≥ α accept H0, Sig < α reject H0).
- SPSS: Analyze › Descriptive Statistics › Crosstabs; one variable in Row(s), the other in Column(s); Statistics › Chi-square; Continue, OK. Three screenshots (`screenshots/ct-*.png`).
- Example 1: gender × major, 10 students → Pearson 2.533, df 2, Sig .282, accept H0.
- Example 2: four MCQs on Example 1's output (valid 10, missing 0, Sig larger than α, accept H0).
- Applications 1 (gender × employment) and 2 (lecture type × achievement): data only, no answers in the lecture.

## Fixes to the source (also in speaker notes)
1. Application 1 codes are labelled "التخصص"; it is the employment variable. Row 8 "لا تعمل" = لا يعمل.
2. Application 2 codes are labelled "النوع"/"التخصص" (lecture type / achievement) and "high" is coded 3; it is 2 here.
3. The hypotheses slide was titled "اختبارات الفروض لعينة واحدة" (left over from Section 4).
4. MCQ numbering repeated "٢"; renumbered 1–4. Typo "رفص" → رفض; the wrong MCQ option is "رفض الفرض العدمي وقبول البديل".

## Computed answers (scipy, SPSS formulas)
- Example 1: Pearson 2.533 (df 2) Sig .282; LR 3.314 .191; Linear-by-Linear .000 1.000 — matches the lecture.
- Application 1 (2×2): counts male 2/2, female 4/2. Pearson .278 (df 1) Sig .598; Continuity Correction .000 1.000; LR .277 .599; Fisher exact 2-sided 1.000, 1-sided .548; Linear-by-Linear .250 .617 → accept H0.
- Application 2: in person low/med/high 1/0/5, online 0/3/1. Pearson 6.528 (df 2) Sig .038; LR 8.053 .018; Linear-by-Linear .833 .361 → reject H0. (Used on the "watch out" slide: the Linear-by-Linear row would give the opposite decision.)

## Additions (Mohamed's standing rules: hook, variables, running case, applied "why")
- Hook: 6 of 7 Business students vs 1 of 7 Dentistry students want some courses fully online: related to faculty, or chance?
- Case application: 20 students; faculty (Part A; 0 Business, 1 Engineering, 2 Dentistry) × q3 grouped (0 not agree = 1–3, 1 agree = 4–5).
  Data (student 1–20): faculty `0 2 1 0 1 2 0 2 1 0 2 1 0 2 1 0 2 1 0 2`, q3 `1 0 1 1 0 0 0 1 1 1 0 0 1 0 1 1 0 0 1 0`.
  Counts: Business 1/6, Engineering 3/3, Dentistry 6/1 (not agree / agree). Pearson 7.143 (df 2) Sig .028; LR 7.925 .019; Linear-by-Linear 6.786 .009 → reject H0: opinion depends on faculty; start online courses in the supporting faculties.
- Statement slide: read Sig from the Pearson Chi-Square row only.

## Slide run (23 per language)
cover · hook · agenda · d1 · case · when · rule · d2 · how · shots · ex1data · ex1ans · casedata · caseans · pearson · d3 · ex2a · ex2b · app1 · app1ans · app2 · app2ans · summary

MCQ answers: ex2a 1 أ (10), 2 ب (صفر) · ex2b 3 أ (أكبر), 4 أ (قبول العدمي).

## Build
- `python3 section5.py ar|en "decks/<lang>" '<ds record>' '<blob map>'` (uses `tools/legacy-kit/sectionkit.py`).
- Decks: Arabic https://claude.ai/artifact/QA94rvus9gBrufBhrLL9GQ · English https://claude.ai/artifact/YQGyDEHLJzk8D4uqmNMUFx.
- PowerPoint: exported locally with the Slides engine (PowerPoint, basic fonts), then `../Section 3 - files/fix_rtl_pptx.py` (Arabic), `add_answer_animations.py <in> <out> ar|en` (MCQ highlights on slides 17–18; headline + decision card on click on 12, 14, 20, 22), `tools/fit_text_pptx.py`, `tools/make_ppsx.py`.
