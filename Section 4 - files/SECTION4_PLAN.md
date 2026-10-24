# Section 4 — Hypothesis tests for the mean (One Sample and Paired Samples T-Test)

Built on 2026-10-24 from the lecture PDF Mohamed uploaded (`المحاضرة الرابعة SPSS.pdf`, 30 slides). Anyone continuing this section starts here, together with `HANDOFF.md`, `CLAUDE.md` and `CASE_STUDY.md`.

## Source (the lecture)
- Statistical hypothesis: definition, null (no difference, chance), alternative (a difference).
- Steps: state the hypotheses → run in SPSS → compare Sig with the significance level. Sig ≥ α: accept H0; Sig < α: reject H0.
- One-sample t-test: H0: μ = μ0. Analyze › Compare Means › One Sample T-Test, Test Value, Options (confidence level), Continue, OK. Three screenshots.
- Example 1: monthly training hours of 10 employees (18, 22, 15, 20, 14, 25, 21, 16, 23, 30); does the mean differ from 20 at 0.95? Answer Sig = .803 > .05, accept H0.
- Example 2: MCQs on a one-sample output (N 10, mean 407.80, Test Value 300, 99% CI, Sig .064).
- Paired-samples t-test: H0: μ1 = μ2. Analyze › Compare Means › Paired-Samples T Test. Three screenshots.
- Example 3: weekly errors of 6 employees before/after a task-management program, 95%. Answer Sig = .178, accept H0.
- Example 4: MCQs on a paired output (means 15.67 / 19.83, Sig .012).

## Fixes to the source (also in speaker notes)
1. Example 3: the data table has 18 for employee 5 "after", but the lecture's SPSS solution (means 20.17 / 18.67, Sig .178) was run with 24. The slides use 24 so students reproduce the lecture's answer. With 18, Sig = .115 (same decision).
2. Typos: "Parried Sample" → Paired-Samples; "فرض العد" → فرض العدم; "رفص" → رفض; the MCQ option "رفض الفرض العدمي ورفص الفرض البديل" → "رفض الفرض العدمي وقبول البديل".
3. MCQ numbering in examples 2 and 4 repeated "٢"; renumbered 1–7 and 1–5.
4. The One-Sample Effect Sizes and Paired Samples Correlations tables are left off the drawn output (mentioned in notes); they do not affect the decision.

## Additions (from Mohamed's standing rules: hook, define the variables, running case study, applied "why")
- Hook: 12 students average 3.7 out of 5; is that enough to tell management students approve, or chance?
- Case slide: after Section 3 (q4 dropped, alpha .828), each student's **attitude score** = mean of q1, q2, q3, q5, q6 (Scale, 1–5, 3 = neutral). Management's two questions map to the two tests.
- Case application 1 (one sample, 95%), attitude of 12 random respondents vs 3:
  `3.8 4.2 3.4 2.8 4.0 3.6 4.4 3.0 3.8 3.2 4.6 3.4`
  N 12, Mean 3.68, SD .556, SE .160; t 4.260, df 11, Sig .001, Mean Difference .683, 95% CI .33 to 1.04 → reject H0, attitude significantly positive.
- Case application 2 (paired, 99%), 8 students before/after two weeks of one course fully online:
  before `2.6 3.0 2.4 3.4 2.8 3.2 2.2 2.8`, after `3.2 3.6 3.0 3.8 3.4 3.2 3.0 3.6`
  Means 2.80 (SD .400, SE .141) / 3.35 (SD .298, SE .105); difference before − after: Mean −.550, SD .256, SE .091, 99% CI −.867 to −.233, t −6.068, df 7, Sig .001 → reject H0 (α = .01), attitudes improved.
- One amber statement slide: α = 1 − the confidence level in the question (the trap in Example 2, which uses 99%).
- "Why" line on Example 1: the company targets 20 training hours a month.

All numbers recomputed in Python (scipy) with the SPSS formulas. Lecture outputs verified: Example 1 (t .257, Sig .803, CI −3.12 to 3.92), Example 2 (SE 51.090, t 2.110, Sig .064, 99% CI −58.23 to 273.83), Example 4 (t −3.867, Sig .012, CI −6.937 to −1.397).

## Slide run (28 per language, ids)
cover · hook · agenda · d1 · case · hyp · rule · d2 · os-how · os-shots · ex1data · ex1ans · casea · caseaans · d3 · ps-how · ps-shots · ex3data · ex3ans · caseb · casebans · alpha (statement) · d4 · ex2a · ex2b · ex4a · ex4b · summary

MCQ answers (letters أ ب ج د / a b c d): ex2a 1 أ, 2 ج, 3 ب, 4 ج · ex2b 5 ج, 6 أ, 7 أ · ex4a 1 أ, 2 ب, 3 ج · ex4b 4 ب, 5 ب.

## Build
- `section4.py` generates both decks (`python3 section4.py ar|en <out> '<ds record>' '<blob map>'`); it uses `tools/legacy-kit/sectionkit.py`. Generated slides are in `decks/ar` and `decks/en`.
- RTL: `RtlKit.t` keeps formulas (`Sig = 0.803`, `α = 0.05`, `μ = 20`, `H0`) and signed/dot-led numbers in LRI…PDI isolates, and joins multi-word SPSS names with no-break spaces.
- Decks: Arabic https://claude.ai/artifact/AxqRuGr6HA1h1neQcnRtpp · English https://claude.ai/artifact/6ApAwNxuX4GsHDb1topDfR (owned by Mohamed's current account). Screenshots in `screenshots/` are uploaded as assets of each deck.
- PowerPoint: exported from the deck (PowerPoint, basic fonts) by serving the deck locally in Playwright (the HANDOFF skill's step 4.7), then `../Section 3 - files/fix_rtl_pptx.py` (Arabic only) and `add_answer_animations.py <in> <out> ar|en` (green highlight on each correct option, one question per click on slides 24–27), then `tools/make_ppsx.py`.
