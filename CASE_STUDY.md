# Course case study: Should the university expand e-learning?

One running case that every section from Section 3 onward builds on, so students always know why they run each analysis.

## The story
University management wants to know students' attitudes to e-learning before moving some courses fully online. A research team builds a two-part questionnaire, pilots it on 10 students to check its reliability, then sends it to 400 students.

## The questionnaire
**Part A: student details** (for later sections: comparing groups, cross-tabs)
- Gender (male / female) · Nominal
- Faculty · Nominal
- Year of study · Ordinal

**Part B: attitude items**, 5-point Likert (1 = strongly disagree … 5 = strongly agree)

| Code | Item (Arabic) | Item (English) |
|---|---|---|
| q1 | التعليم الإلكتروني يوفر وقتي ومجهودي | E-learning saves me time and effort |
| q2 | أفهم المحاضرة المسجلة كما أفهمها في القاعة | I understand a recorded lecture as well as one in class |
| q3 | أفضّل أن تُدرَّس بعض المواد أونلاين بالكامل | I would like some courses taught fully online |
| q4 | أفضّل المحاضرات التقليدية على التعليم الإلكتروني (عبارة سلبية) | I prefer traditional lectures to e-learning (negative item) |
| q5 | منصة الجامعة الإلكترونية سهلة الاستخدام | The university's e-learning platform is easy to use |
| q6 | أنصح زملائي بالمواد الإلكترونية | I recommend online courses to my classmates |

q4 is worded negatively on purpose: in the pilot data it correlates −.279 with the rest and drops alpha to .627 (.828 without it, .787 if reverse-coded as 6 − value).

## Sections so far
- Section 3: reliability of Part B on the 10-student pilot (data in `Section 3 - files/SECTION3_PLAN.md`).
- Section 4: hypothesis tests for the mean on the **attitude score** (each student's mean of the five reliable items q1, q2, q3, q5, q6; Scale, 1 to 5, 3 = neutral).
  - One-sample t-test: 12 randomly chosen respondents, test value 3. Mean 3.68, Sig = .001, so students' attitude is significantly positive.
  - Paired-samples t-test: 8 students before and after two weeks of one course taught fully online, 99% confidence. Mean 2.80 → 3.35, Sig = .001 < .01, so the trial improved attitudes.
  - Data and SPSS output in `Section 4 - files/SECTION4_PLAN.md`.

## Ideas for later sections (not yet agreed with Mohamed)
Comparing attitudes by gender or faculty (independent-samples t-test, ANOVA) using Part A; correlation between items; descriptive statistics of the attitude score. Each would need the 400-student data, which does not exist yet and would have to be written for the section.
