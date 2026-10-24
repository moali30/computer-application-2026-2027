"""Section 4 — Hypothesis tests for the mean (One Sample and Paired Samples T-Test). Content for the Arabic and English decks.

Usage: python3 section4.py <ar|en> <out root> '<design-system record json>' '<blob map json>'
The blob map gives each screenshot's /_blob/<id> url in that deck: {"os-menu": "/_blob/…", …}.
"""
import sys, os, json, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools", "legacy-kit"))
from sectionkit import *

AR_CHARS = re.compile(r"[؀-ۿ]")
# Kept left-to-right inside Arabic text: formulas such as "Sig = 0.803", "α = 0.05", "μ = 20", and numbers whose
# sign or leading dot the RTL embedding would move (.627 → 627. , −.279 → .279−).
LTR_RUN = re.compile(r"(?:Sig|α|μ\d?|H[01])(?:\s?[=≠<>≥≤]\s?(?:[−-]?\d*\.?\d+%?|μ\d?))?"
                     r"|[−-]?\d*\.\d+|[−-]\d+(?:\.\d+)?|\d+(?:\.\d+)?\s?[−–-]\s?\d+(?:\.\d+)?")
# SPSS names of two or more words ("One Sample", "Mean Difference") never break across lines.
LATIN_PHRASE = re.compile(r"[A-Za-z][\w.()-]*(?: [A-Za-z][\w.()-]*)+")
LRI, PDI, NBSP = "⁦", "⁩", " "
GREEN, GREEN_TINT = "#2E7D4F", "#DDEFE3"


class RtlKit(Kit):
    """Kit.t with fixes for Arabic slides (Section 3's, plus formulas and no-break SPSS names): text with
    no Arabic letters stays left-to-right; formulas and signed or dot-led numbers are isolated."""
    def t(self, s):
        if not self.ar or not isinstance(s, str):
            return s
        if not AR_CHARS.search(s):
            return s
        s = LATIN_PHRASE.sub(lambda m: m.group(0).replace(" ", NBSP), s)
        return super().t(LTR_RUN.sub(lambda m: f"{LRI}{m.group(0)}{PDI}", s))


L = lambda k, ar, en: ar if k.ar else en

# ---- data and SPSS output (computed in Python with the SPSS formulas; see SECTION4_PLAN.md) -------------
EX1_HOURS = [18, 22, 15, 20, 14, 25, 21, 16, 23, 30]                 # lecture example 1, test value 20
EX3_BEFORE, EX3_AFTER = [20, 18, 25, 15, 25, 18], [19, 17, 24, 16, 24, 12]   # lecture example 3 (employee 5 after = 24, see plan)
CASE_A = [3.8, 4.2, 3.4, 2.8, 4.0, 3.6, 4.4, 3.0, 3.8, 3.2, 4.6, 3.4]  # attitude score of 12 students, test value 3
CASE_B_BEFORE = [2.6, 3.0, 2.4, 3.4, 2.8, 3.2, 2.2, 2.8]               # attitude before / after a two-week online trial
CASE_B_AFTER = [3.2, 3.6, 3.0, 3.8, 3.4, 3.2, 3.0, 3.6]


def build(lang, root, ds_record=None, blobs=None):
    k = RtlKit(lang, "Computer Application", "سكشن 4" if lang == "ar" else "Section 4", root)
    blobs = blobs or {}

    # ---- building blocks --------------------------------------------------------------------
    def spss_table(header, rows, widths, size=24, width=None, title=None, sub=None, hl=None, pad="8px 14px"):
        """An SPSS output table. SPSS prints in English left-to-right, so columns are never reversed.
        hl = (row, col) of the cell to colour (the value the decision uses)."""
        th = "".join(f'<th style="width:{w}%; padding:{pad}; text-align:{"left" if i == 0 else "center"}; color:{PAPER}; font-weight:600">{h}</th>'
                     for i, (h, w) in enumerate(zip(header, widths)))
        body = ""
        for r_i, r in enumerate(rows):
            bg = CARD if r_i % 2 == 0 else PAPER_ALT
            cells = ""
            for i, c in enumerate(r):
                col = f" color:{AMBER_INK}; font-weight:700;" if hl == (r_i, i) else ""
                cells += f'<td style="padding:{pad}; text-align:{"left" if i == 0 else "center"};{col}">{c}</td>'
            body += f'<tr style="background:{bg}">{cells}</tr>'
        wcss = f" width:{width}px;" if width else ""
        cap = ""
        if title:
            s = f' <span style="color:{MUTED}">· {sub}</span>' if sub else ""
            cap = f'<p style="font-family:{MONO}; font-size:24px; font-weight:600; color:{INK}; text-align:left; white-space:nowrap">{title}{s}</p>'
        return (f'<div style="display:flex; flex-direction:column; gap:8px; align-self:{k.self_start}">{cap}'
                f'<table style="{wcss} font-size:{size}px; line-height:1.25; color:{INK}; border:1px solid {RULE}; border-radius:8px; font-variant-numeric:tabular-nums">'
                f'<tr style="background:{INK}">{th}</tr>{body}</table></div>')

    def os_out(var, n, mean, sd, se, tv, t, df, sig, md, lo, hi, cl=95, stack=False):
        """One-Sample Statistics + One-Sample Test, side by side (or stacked)."""
        a = spss_table(["", "N", "Mean", "Std. Deviation", "Std. Error Mean"], [[var, n, mean, sd, se]],
                       [22, 10, 20, 24, 24], width=640 if not stack else 760, title="One-Sample Statistics")
        b = spss_table(["", "t", "df", "Sig. (2-tailed)", "Mean Difference", f"{cl}% CI Lower", f"{cl}% CI Upper"],
                       [[var, t, df, sig, md, lo, hi]], [17, 10, 8, 17, 17, 15.5, 15.5], width=992 if not stack else 1300,
                       title="One-Sample Test", sub=f"Test Value = {tv}", hl=(0, 3))
        if stack:
            return f'<div style="display:flex; flex-direction:column; gap:20px">{a}{b}</div>'
        return f'<div style="display:flex; flex-direction:row; gap:32px; align-items:end; align-self:{k.self_start}">{a}{b}</div>'

    def ps_out(v1, v2, s1, s2, diff, cl=95):
        """Paired Samples Statistics + Paired Samples Test. s1/s2 = (mean, n, sd, se); diff = (mean, sd, se, lo, hi, t, df, sig)."""
        a = spss_table(["Pair 1", "Mean", "N", "Std. Deviation", "Std. Error Mean"],
                       [[v1, *s1], [v2, *s2]], [28, 14, 10, 24, 24], width=760, title="Paired Samples Statistics")
        b = spss_table(["Pair 1", "Mean", "Std. Deviation", "Std. Error Mean", f"{cl}% CI Lower", f"{cl}% CI Upper", "t", "df", "Sig. (2-tailed)"],
                       [[f"{v1} - {v2}", *diff]], [17, 9, 12, 11, 11, 11, 9, 6, 14], width=1664,
                       title="Paired Samples Test", sub="Paired Differences", hl=(0, 8))
        return f'<div style="display:flex; flex-direction:column; gap:20px">{a}{b}</div>'

    def hyp_row(h0, h1):
        """H0 / H1 chips with their meaning."""
        def one(label, f, d):
            return (f'<div style="display:flex; flex-direction:{k.row}; gap:16px; align-items:center">'
                    f'{k.chip(f, align=False)}{k.p(label + ": " + d if not k.ar else label + ": " + d, 26, INK_SOFT)}</div>')
        return (f'<div style="display:flex; flex-direction:{k.row}; gap:48px; flex-wrap:wrap">'
                + one(L(k, "الفرض العدمي", "Null"), h0[0], h0[1]) + one(L(k, "الفرض البديل", "Alternative"), h1[0], h1[1]) + "</div>")

    def decision(lines, reject):
        fg = GREEN if reject else AMBER_INK
        bg = GREEN_TINT if reject else AMBER_TINT
        inner = k.h3(lines[0], fg, 34) + "".join(k.p(l, 28, INK) for l in lines[1:])
        return k.card(inner, bg=bg, border=False, flex="none", pad=32, gap=12)

    def task_card(title, steps, width=None):
        return k.card(k.h3(title, AMBER_INK, 34) + k.steps(steps, 28), bg=AMBER_TINT, border=False, flex="none", pad=32, gap=18, width=width)

    def hdata(label_col, row_label, values, size=26):
        """A one-variable data set as a wide table: one header row (respondent numbers) and one data row."""
        hdr = [label_col] + [str(i + 1) for i in range(len(values))]
        n = len(values)
        first = 30
        widths = [first] + [(100 - first) / n] * n
        rows = [[row_label] + [f"{v:.1f}" if isinstance(v, float) else str(v) for v in values]]
        if k.ar:
            hdr, widths, rows = hdr[::-1], widths[::-1], [r[::-1] for r in rows]
        th = "".join(f'<th style="width:{w:.2f}%; padding:10px 12px; text-align:center; color:{PAPER}; font-weight:600">{k.t(h)}</th>' for h, w in zip(hdr, widths))
        body = "".join(f'<tr style="background:{CARD}">' + "".join(f'<td style="padding:10px 12px; text-align:center">{k.t(c)}</td>' for c in r) + "</tr>" for r in rows)
        return (f'<table style="width:1664px; font-size:{size}px; line-height:1.3; color:{INK}; border:1px solid {RULE}; border-radius:8px; '
                f'font-variant-numeric:tabular-nums"><tr style="background:{INK}">{th}</tr>{body}</table>')

    def vdata(headers, rows, widths, width, size=26):
        """Data as typed rows (one row per person), the way it is entered in Data View."""
        if k.ar:
            headers, widths, rows = headers[::-1], widths[::-1], [r[::-1] for r in rows]
        th = "".join(f'<th style="width:{w}%; padding:8px 14px; text-align:center; color:{PAPER}; font-weight:600; line-height:1.3">{k.t(h)}</th>' for h, w in zip(headers, widths))
        body = "".join(f'<tr style="background:{CARD if i % 2 == 0 else PAPER_ALT}">'
                       + "".join(f'<td style="padding:8px 14px; text-align:center">{c}</td>' for c in r) + "</tr>" for i, r in enumerate(rows))
        return (f'<table style="width:{width}px; flex:none; font-size:{size}px; line-height:1.25; color:{INK}; border:1px solid {RULE}; border-radius:8px; '
                f'font-variant-numeric:tabular-nums"><tr style="background:{INK}">{th}</tr>{body}</table>')

    def shots(items):
        """Three numbered SPSS screenshots in a row: (blob key, alt, caption)."""
        cards = ""
        for i, (key, alt, cap) in enumerate(items):
            cards += (f'<div style="flex:1; display:flex; flex-direction:column; gap:20px">'
                      f'<div style="background:{CARD}; border:1px solid {RULE}; border-radius:16px; padding:16px; display:flex; justify-content:center">'
                      f'<img src="{blobs.get(key, "")}" alt="{alt}" style="width:480px; height:340px; object-fit:contain"></div>'
                      f'<div style="display:flex; flex-direction:{k.row}; gap:16px; align-items:start">{k.num_badge(i + 1, 48, BLUE, CARD, 24)}'
                      f'<div style="flex:1">{k.p(cap, 28, INK)}</div></div></div>')
        return f'<div style="display:flex; flex-direction:{k.row}; gap:32px">{cards}</div>'

    letters = ["أ", "ب", "ج", "د"] if k.ar else ["a", "b", "c", "d"]

    def qrow(n, stem, opts, stem_w=600):
        """A compact multiple-choice row: number, stem, options, all on one line."""
        ops = "".join(k.option(l, o) for l, o in zip(letters, opts))
        return (f'<div style="display:flex; flex-direction:{k.row}; align-items:center; gap:24px">'
                f'{k.num_badge(n, 52, INK, AMBER, 26)}'
                f'<div style="width:{stem_w}px; flex:none">{k.p(stem, 28, INK)}</div>'
                f'<div style="flex:1; display:flex; flex-direction:{k.row}; flex-wrap:wrap; gap:14px">{ops}</div></div>')

    def quiz_slide(sid, eyebrow, title, output, questions, start, answers, notes_extra="", section=None, stem_w=600):
        rows = "".join(qrow(start + i, s, o, stem_w) for i, (s, o) in enumerate(questions))
        ans = " | ".join(f"{start + i}: {letters[a]}" for i, a in enumerate(answers))
        k.content(sid, eyebrow, title,
                  output + f'<div style="display:flex; flex-direction:column; gap:20px">{rows}</div>',
                  kind="practice", gap=32, section=section,
                  notes=L(k, f"الإجابات: {ans}. {notes_extra}", f"Answers: {ans}. {notes_extra}"))

    # ================================================================================================
    # 1 cover
    k.cover("cover", L(k, "Computer Application · سكشن 4", "Computer Application · Section 4"),
            L(k, "اختبارات الفروض للمتوسط", "Hypothesis tests for the mean"),
            L(k, "هل الفرق حقيقي أم مجرد صدفة؟", "Is the difference real, or just chance?"),
            "Horus University · 2026/2027",
            section=L(k, "الافتتاح وخطة السكشن", "Opening and plan"))

    # 2 hook
    k.add("hook", f'<div style="width:1500px; align-self:{k.self_start}; display:flex; flex-direction:column; gap:40px">'
          + k.eyebrow(L(k, "قبل أن نبدأ", "Before we start"), "practice", dark=True)
          + f'<h1 style="font-family:{DISPLAY}; font-size:96px; font-weight:700; line-height:1.15; color:{PAPER}">'
          + k.t(L(k, "3.7 من 5: هل الطلاب مؤيدون فعلًا؟", "3.7 out of 5: do students really approve?")) + '</h1>'
          + k.p(L(k, "سألنا 12 طالبًا عن التعليم الإلكتروني فكان متوسط اتجاههم 3.7، أعلى من المحايد 3. لكن لو سألنا 12 طالبًا غيرهم قد نحصل على 2.9.",
                  "We asked 12 students about e-learning and their average attitude was 3.7, above the neutral 3. Ask 12 other students and we might get 2.9."), 40, MIST)
          + k.p(L(k, "قبل أن نقول للإدارة «الطلاب مؤيدون» نحتاج اختبارًا يجيب: هل الفرق حقيقي أم صدفة؟",
                  "Before telling management “students approve”, we need a test that answers: is the difference real, or chance?"), 40, PAPER, 600)
          + '</div>', bg=INK, dark=True, justify="center",
          notes=L(k, "اسأل الطلاب: هل متوسط 3.7 من عينة صغيرة كافٍ لنبني عليه قرار تحويل مواد كاملة إلى أونلاين؟ اسمع الإجابات ثم قل: اختبار الفروض هو الأداة التي تحسم ذلك.",
                  "Ask: is an average of 3.7 from a small sample enough to move whole courses online? Take a few answers, then say: a hypothesis test is the tool that settles it."))

    # 3 agenda
    k.agenda("agenda", L(k, "خطة السكشن", "Today"), L(k, "ماذا سنتعلم اليوم؟", "What we cover today"), [
        L(k, "الفرض الإحصائي: الفرض العدمي والفرض البديل وقاعدة القرار", "Statistical hypotheses: null, alternative, and the decision rule"),
        L(k, "اختبار عينة واحدة One Sample T-Test", "The one-sample t-test"),
        L(k, "اختبار عينتين مترابطتين Paired Samples T-Test", "The paired-samples t-test"),
        L(k, "تطبيق على دراسة الحالة: اتجاه الطلاب نحو التعليم الإلكتروني", "Applying both to the case: students’ attitude to e-learning"),
        L(k, "قراءة المخرجات: أسئلة اختيار من متعدد", "Reading the output: multiple-choice questions"),
    ])

    # 4 divider 1
    k.divider("d1", 1, 4, L(k, "الفرض الإحصائي", "Statistical hypotheses"),
              L(k, "ادعاء نختبره، وقاعدة واحدة للحكم عليه", "A claim we test, and one rule to judge it"),
              section=L(k, "الفرض الإحصائي وقاعدة القرار", "Hypotheses and the decision rule"))

    # 5 case study: where we are, the variable we measure, the questions
    def ccard(tag, h, d):
        return k.card(k.tag_row([tag]) + k.h3(h, size=36) + k.p(d, 28), gap=14, pad=32)
    k.content("case", L(k, "دراسة الحالة", "Case study"), L(k, "من الثبات إلى القرار", "From reliability to a decision"),
              k.cards([
                  ccard(L(k, "ما وصلنا إليه", "Where we are"), L(k, "استبيان ثابت", "A reliable questionnaire"),
                        L(k, "في سكشن 3 حذفنا q4 فأصبح ثبات العبارات الخمس جيدًا (ألفا = .828)، ثم وُزّع الاستبيان على الطلاب.",
                          "In Section 3 we dropped q4, so the five items became reliable (alpha = .828); then the questionnaire went out to students.")),
                  ccard(L(k, "المتغير", "The variable"), L(k, "درجة الاتجاه", "Attitude score"),
                        L(k, "متوسط إجابات الطالب على العبارات الخمس، من 1 إلى 5. متغير كمي (Scale)، و3 تعني محايد.",
                          "The student’s average over the five items, from 1 to 5. A quantitative (Scale) variable; 3 means neutral.")),
                  ccard(L(k, "أسئلة الإدارة", "Management asks"), L(k, "سؤالان اليوم", "Two questions today"),
                        L(k, "هل اتجاه الطلاب يختلف عن المحايد؟ وهل تجربة الدراسة أونلاين غيّرت رأيهم؟",
                          "Do students’ attitudes differ from neutral? Did trying online study change their minds?")),
              ], 28) + k.tag(L(k, "نجيب عن السؤالين باختبار T: عينة واحدة، ثم عينتان مترابطتان", "We answer both with a t-test: one sample, then paired samples"), AMBER_TINT, AMBER_INK),
              gap=40,
              notes=L(k, "درجة الاتجاه تُحسب في SPSS من Transform ثم Compute Variable بمتوسط q1 و q2 و q3 و q5 و q6. في التمارين اليوم نعطي الدرجة جاهزة حتى نركز على الاختبار. الجزء (أ) من الاستبيان (النوع، الكلية) نحتفظ به لسكشن المقارنة بين مجموعتين مستقلتين.",
                      "The attitude score is made in SPSS with Transform › Compute Variable as the mean of q1, q2, q3, q5 and q6. Today the score is given ready so we can focus on the test. Part A (gender, faculty) is kept for the independent-groups section."))

    # 6 hypotheses
    def hcard(code, h, d, ex):
        return k.card(k.chip(code) + k.h3(h, size=40) + k.p(d, 28) + '<div style="flex:1"></div>'
                      + k.tag(ex, AMBER_TINT, AMBER_INK), gap=16, pad=36)
    k.content("hyp", L(k, "التعريف", "Definition"), L(k, "ما هو الفرض الإحصائي؟", "What is a statistical hypothesis?"),
              k.p(L(k, "ادعاء أو تخمين حول معلمة من معالم المجتمع (مثل المتوسط μ)، والمطلوب اختبار صحة هذا الادعاء.",
                    "A claim or guess about a population parameter (such as the mean μ) whose truth we want to test."), 32, INK)
              + k.cards([
                  hcard("H0", L(k, "الفرض العدمي", "The null hypothesis"),
                        L(k, "لا يوجد فرق أو تغيّر. الفرق بين العينة والمجتمع ناتج عن الصدفة، ولا فرق حقيقي.",
                          "No difference or change. Any gap between sample and population is due to chance."),
                        L(k, "في حالتنا: متوسط الاتجاه = 3", "Our case: mean attitude = 3")),
                  hcard("H1", L(k, "الفرض البديل", "The alternative hypothesis"),
                        L(k, "يوجد فرق أو تغيّر حقيقي. هو عكس الفرض العدمي.",
                          "There is a real difference or change. It is the opposite of the null."),
                        L(k, "في حالتنا: متوسط الاتجاه ≠ 3", "Our case: mean attitude ≠ 3")),
              ]), gap=40,
              notes=L(k, "الفرض العدمي دائمًا فيه علامة يساوي، والبديل فيه لا يساوي. نبدأ دائمًا بافتراض أنه لا يوجد فرق، والبيانات هي التي تقنعنا بالعكس.",
                      "The null always has the equals sign; the alternative has not-equal. We start by assuming no difference, and the data has to convince us otherwise."))

    # 7 steps and decision rule
    def rule(f, h, d, reject):
        fg, bg = (GREEN, GREEN_TINT) if reject else (AMBER_INK, AMBER_TINT)
        return k.card(k.chip(f) + k.h3(h, fg, 34) + k.p(d, 28, INK), bg=bg, border=False, gap=14, pad=32)
    left = (f'<div style="flex:1; display:flex; flex-direction:column; gap:24px">'
            + k.steps([L(k, "تعريف الفروض (H0 و H1)", "State the hypotheses (H0 and H1)"),
                       L(k, "التطبيق على برنامج SPSS", "Run the test in SPSS"),
                       L(k, "مقارنة قيمة Sig مع مستوى المعنوية α", "Compare Sig with the significance level α")], 32, INK)
            + k.card(k.p(L(k, "مستوى المعنوية α = 1 − مستوى الثقة. ثقة 95% تعني α = 0.05، وثقة 99% تعني α = 0.01.",
                           "Significance level α = 1 − confidence level. 95% confidence means α = 0.05; 99% means α = 0.01."), 28, INK),
                     bg=BLUE_TINT, border=False, flex="none", pad=28)
            + '</div>')
    right = (f'<div style="width:760px; flex:none; display:flex; flex-direction:column; gap:24px">'
             + rule("Sig ≥ α", L(k, "قبول الفرض العدمي ورفض البديل", "Accept H0, reject H1"),
                    L(k, "الفرق الذي نراه في العينة يمكن أن يكون صدفة.", "The difference in the sample could be chance."), False)
             + rule("Sig < α", L(k, "رفض الفرض العدمي وقبول البديل", "Reject H0, accept H1"),
                    L(k, "الفرق حقيقي (معنوي)، وليس صدفة.", "The difference is real (significant), not chance."), True)
             + '</div>')
    k.content("rule", L(k, "خطوات الاختبار", "The procedure"), L(k, "ثلاث خطوات وقاعدة قرار واحدة", "Three steps and one decision rule"),
              f'<div style="display:flex; flex-direction:{k.row}; gap:56px; align-items:start">{left}{right}</div>', gap=48,
              notes=L(k, "Sig هي احتمال أن نرى فرقًا بهذا الحجم لو كان الفرض العدمي صحيحًا. كلما صغرت، قلّ احتمال أن يكون الفرق صدفة. ملاحظة للمعيد: إحصائيًا الأدق أن نقول «لا نرفض الفرض العدمي» بدل «نقبله»، لكننا نلتزم بصياغة المحاضرة.",
                      "Sig is the chance of seeing a difference this big if the null were true; the smaller it is, the less likely the difference is chance. Note: strictly we “fail to reject” H0 rather than “accept” it, but we keep the lecture’s wording."))

    # 8 divider 2
    k.divider("d2", 2, 4, L(k, "اختبار عينة واحدة", "One-sample t-test"),
              L(k, "هل متوسط المجتمع يساوي قيمة معينة؟", "Does the population mean equal a given value?"),
              section=L(k, "اختبار عينة واحدة One Sample T-Test", "One-sample t-test"))

    # 9 one-sample: when + steps
    when = k.card(k.h3(L(k, "متى نستخدمه؟", "When?"), size=36)
                  + k.p(L(k, "عندما نقارن متوسط متغير كمي واحد بقيمة افتراضية μ0 مذكورة في السؤال.",
                          "When we compare the mean of one quantitative variable with a hypothesised value μ0 given in the question."), 28)
                  + k.chip("H0: μ = μ0") + k.chip("H1: μ ≠ μ0"), flex="none", width=560, pad=36, gap=20)
    how = (f'<div style="flex:1; display:flex; flex-direction:column; gap:24px">'
           + k.chip_row(["Analyze", "›", "Compare Means", "›", "One Sample T-Test"])
           + k.steps([L(k, "أدخل البيانات في SPSS ثم اختر المسار أعلاه.", "Enter the data, then follow the menu path above."),
                      L(k, "انقل المتغير إلى خانة Test Variable(s).", "Move the variable into Test Variable(s)."),
                      L(k, "اكتب القيمة الافتراضية الموجودة في السؤال في خانة Test Value.", "Type the hypothesised value from the question in Test Value."),
                      L(k, "لتحديد مستوى الثقة اضغط Options واكتب قيمته.", "To set the confidence level, click Options and type it."),
                      L(k, "اضغط Continue ثم OK.", "Click Continue, then OK.")], 28) + '</div>')
    k.content("os-how", "One Sample T-Test", L(k, "متى نستخدمه؟ وكيف؟", "When and how"),
              f'<div style="display:flex; flex-direction:{k.row}; gap:56px; align-items:start">{when}{how}</div>', kind="term", gap=48,
              notes=L(k, "Test Value هي أهم خانة: لو نسيتها يقارن SPSS المتوسط بالصفر. مستوى الثقة في Options يغيّر فترة الثقة فقط، ونحن نستخدمه لنعرف α.",
                      "Test Value is the key box: leave it empty and SPSS compares the mean with zero. The confidence level in Options only changes the confidence interval; we use it to know α."))

    # 10 one-sample screenshots
    k.content("os-shots", L(k, "التطبيق على SPSS", "In SPSS"), L(k, "اختبار عينة واحدة خطوة بخطوة", "One-sample t-test step by step"),
              shots([("os-menu", "Analyze menu, Compare Means, One-Sample T Test", "Analyze › Compare Means › One-Sample T Test"),
                     ("os-dialog", "One-Sample T Test dialog with Test Value 20",
                      L(k, "انقل المتغير إلى Test Variable(s) واكتب Test Value", "Move the variable to Test Variable(s) and type the Test Value")),
                     ("os-options", "Options dialog with Confidence Interval Percentage 95",
                      L(k, "من Options اكتب مستوى الثقة ثم Continue", "In Options, type the confidence level, then Continue"))]),
              bg=PAPER_ALT, gap=48)

    # 11 example 1 data (lecture)
    k.content("ex1data", L(k, "مثال 1", "Example 1"), L(k, "ساعات التدريب الشهرية", "Monthly training hours"),
              k.p(L(k, "الشركة تستهدف 20 ساعة تدريب شهريًا لكل موظف. البيانات التالية هي ساعات التدريب الشهرية لعينة من 10 موظفين تم اختيارهم عشوائيًا.",
                    "The company aims for 20 training hours a month per employee. These are the monthly training hours of 10 randomly chosen employees."), 30, INK)
              + hdata(L(k, "الموظف", "Employee"), L(k, "ساعات التدريب (hours)", "Training hours (hours)"), EX1_HOURS)
              + task_card(L(k, "المطلوب", "Your task"), [
                  L(k, "أدخل البيانات في SPSS في متغير واحد اسمه hours.", "Enter the data in SPSS as one variable, hours."),
                  L(k, "هل يختلف متوسط ساعات التدريب الشهرية معنويًا عن 20 ساعة عند مستوى ثقة 0.95؟", "Does the mean monthly training differ significantly from 20 hours at 0.95 confidence?")]),
              kind="practice", gap=36, section=L(k, "مثال 1", "Example 1"),
              notes=L(k, "Test Value = 20، ومستوى الثقة 95% يعني α = 0.05. اطلب من الطلاب كتابة الفروض قبل تشغيل SPSS.",
                      "Test Value = 20; 95% confidence means α = 0.05. Have students write the hypotheses before running SPSS."))

    # 12 example 1 answer
    k.content("ex1ans", L(k, "مثال 1 · الحل", "Example 1 · Answer"), L(k, "الفرق صدفة: الهدف متحقق", "The gap is chance: target met"),
              hyp_row(("H0: μ = 20", L(k, "لا توجد فروق معنوية", "no significant difference")),
                      ("H1: μ ≠ 20", L(k, "توجد فروق معنوية", "a significant difference")))
              + os_out("hours", "10", "20.40", "4.926", "1.558", "20", ".257", "9", ".803", ".400", "-3.12", "3.92")
              + decision([L(k, "Sig = 0.803 أكبر من α = 0.05: قبول الفرض العدمي ورفض الفرض البديل", "Sig = 0.803 > α = 0.05: accept H0, reject H1"),
                          L(k, "متوسط ساعات التدريب (20.4) لا يختلف معنويًا عن 20 ساعة؛ الفرق 0.4 ساعة يمكن أن يكون صدفة.",
                            "Mean training (20.4 h) does not differ significantly from 20 hours; the 0.4-hour gap could be chance.")], False),
              kind="practice", gap=32,
              notes=L(k, "اقرأ مع الطلاب عمود Sig. (2-tailed) فقط للقرار. SPSS الحديث يضيف أيضًا جدول One-Sample Effect Sizes (يظهر في المحاضرة) ولا نحتاجه هنا.",
                      "Only the Sig. (2-tailed) column decides. Newer SPSS also prints a One-Sample Effect Sizes table (shown in the lecture); we do not need it here."))

    # 13 case A data
    k.content("casea", L(k, "تطبيق على الحالة", "Case study"), L(k, "هل الطلاب محايدون تجاه التعليم الإلكتروني؟", "Are students neutral about e-learning?"),
              k.p(L(k, "الإدارة تسأل: هل اتجاه الطلاب يختلف عن المحايد (3)؟ اخترنا عشوائيًا 12 طالبًا ممن أجابوا الاستبيان، وهذه درجة اتجاه كل منهم.",
                    "Management asks: does students’ attitude differ from neutral (3)? We picked 12 respondents at random; here is each one’s attitude score."), 30, INK)
              + hdata(L(k, "الطالب", "Student"), L(k, "درجة الاتجاه نحو التعليم الإلكتروني (attitude)", "Attitude to e-learning (attitude)"), CASE_A, 26)
              + task_card(L(k, "المطلوب", "Your task"), [
                  L(k, "عرّف المتغير attitude في Variable View (Scale، Decimals = 1) وأدخل الدرجات.", "Define attitude in Variable View (Scale, Decimals = 1) and enter the scores."),
                  L(k, "اختبر عند مستوى ثقة 95%: هل متوسط الاتجاه يختلف عن 3؟ وماذا نقول للإدارة؟", "Test at 95% confidence whether the mean attitude differs from 3. What do we tell management?")]),
              kind="practice", gap=36, section=L(k, "تطبيق 1 على الحالة", "Case application 1"),
              notes=L(k, "لماذا 3؟ لأنها منتصف مقياس ليكرت (محايد). لو المتوسط أعلى من 3 معنويًا فالطلاب مؤيدون، ولو أقل معنويًا فهم معارضون.",
                      "Why 3? It is the midpoint of the Likert scale (neutral). Significantly above 3 means students approve; significantly below means they oppose."))

    # 14 case A answer
    k.content("caseaans", L(k, "تطبيق 1 · الحل", "Case 1 · Answer"), L(k, "الطلاب ليسوا محايدين: اتجاههم إيجابي", "Students are not neutral: they lean positive"),
              hyp_row(("H0: μ = 3", L(k, "الاتجاه محايد", "attitude is neutral")),
                      ("H1: μ ≠ 3", L(k, "الاتجاه يختلف عن المحايد", "attitude differs from neutral")))
              + os_out("attitude", "12", "3.68", ".556", ".160", "3", "4.260", "11", ".001", ".683", ".33", "1.04")
              + decision([L(k, "Sig = 0.001 أصغر من α = 0.05: رفض الفرض العدمي وقبول الفرض البديل", "Sig = 0.001 < α = 0.05: reject H0, accept H1"),
                          L(k, "Mean Difference موجب (3.68 أعلى من 3)، إذن الاتجاه إيجابي. للإدارة: «اتجاه الطلاب نحو التعليم الإلكتروني إيجابي بشكل معنوي».",
                            "Mean Difference is positive (3.68 is above 3), so the attitude is positive. For management: “Students’ attitude to e-learning is significantly positive.”")], True),
              kind="practice", gap=32,
              notes=L(k, "الاختبار يقول هل يوجد فرق، وإشارة Mean Difference تقول اتجاهه. فترة الثقة (.33 إلى 1.04) كلها موجبة ولا تحتوي الصفر، وهذا يتفق مع رفض الفرض العدمي.",
                      "The test says whether there is a difference; the sign of Mean Difference says which way. The confidence interval (.33 to 1.04) is all positive and excludes zero, which agrees with rejecting H0."))

    # 15 divider 3
    k.divider("d3", 3, 4, L(k, "عينتان مترابطتان", "Paired samples"),
              L(k, "نفس الأفراد قبل وبعد: هل حدث تغيّر؟", "The same people before and after: did anything change?"),
              section=L(k, "اختبار عينتين مترابطتين Paired Samples T-Test", "Paired-samples t-test"))

    # 16 paired: when + steps
    when = k.card(k.h3(L(k, "متى نستخدمه؟", "When?"), size=36)
                  + k.p(L(k, "عندما نقيس نفس الأفراد مرتين (قبل وبعد) ونريد أن نعرف هل تغيّر المتوسط.",
                          "When we measure the same people twice (before and after) and want to know whether the mean changed."), 28)
                  + k.chip("H0: μ1 = μ2") + k.chip("H1: μ1 ≠ μ2"), flex="none", width=560, pad=36, gap=20)
    how = (f'<div style="flex:1; display:flex; flex-direction:column; gap:24px">'
           + k.chip_row(["Analyze", "›", "Compare Means", "›", "Paired-Samples T Test"])
           + k.steps([L(k, "أدخل البيانات في عمودين (قبل، بعد): كل صف شخص واحد.", "Enter the data in two columns (before, after): one row per person."),
                      L(k, "اختر المسار أعلاه وانقل المتغيرين إلى Paired Variables.", "Follow the path above and move both variables into Paired Variables."),
                      L(k, "لتحديد مستوى الثقة اضغط Options واكتب قيمته.", "To set the confidence level, click Options and type it."),
                      L(k, "اضغط Continue ثم OK.", "Click Continue, then OK.")], 28) + '</div>')
    k.content("ps-how", "Paired Samples T-Test", L(k, "متى نستخدمه؟ وكيف؟", "When and how"),
              f'<div style="display:flex; flex-direction:{k.row}; gap:56px; align-items:start">{when}{how}</div>', kind="term", gap=48,
              notes=L(k, "الفكرة: SPSS يحسب الفرق لكل شخص (قبل − بعد) ثم يختبر هل متوسط هذه الفروق يساوي صفرًا. لذلك يجب أن يكون الشخص نفسه في الصف نفسه.",
                      "The idea: SPSS takes each person’s difference (before − after) and tests whether the mean difference is zero, so each person must stay on one row."))

    # 17 paired screenshots
    k.content("ps-shots", L(k, "التطبيق على SPSS", "In SPSS"), L(k, "عينتان مترابطتان خطوة بخطوة", "Paired-samples t-test step by step"),
              shots([("ps-menu", "Analyze menu, Compare Means, Paired-Samples T Test", "Analyze › Compare Means › Paired-Samples T Test"),
                     ("ps-dialog", "Paired-Samples T Test dialog with before as Variable1 and after as Variable2",
                      L(k, "انقل «قبل» إلى Variable1 و«بعد» إلى Variable2", "Put before in Variable1 and after in Variable2")),
                     ("ps-options", "Options dialog with Confidence Interval Percentage 95",
                      L(k, "من Options اكتب مستوى الثقة ثم Continue", "In Options, type the confidence level, then Continue"))]),
              bg=PAPER_ALT, gap=48)

    # 18 example 3 data (lecture)
    rows3 = [[i + 1, b, a] for i, (b, a) in enumerate(zip(EX3_BEFORE, EX3_AFTER))]
    k.content("ex3data", L(k, "مثال 3", "Example 3"), L(k, "برنامج جديد لإدارة المهام", "A new task-management program"),
              f'<div style="display:flex; flex-direction:{k.row}; gap:56px; align-items:start">'
              + vdata([L(k, "الموظف", "Employee"), L(k, "قبل (before)", "Before (before)"), L(k, "بعد (after)", "After (after)")], rows3, [30, 35, 35], 560)
              + f'<div style="flex:1; display:flex; flex-direction:column; gap:28px">'
              + k.p(L(k, "تريد إدارة إحدى الشركات معرفة هل يقلل برنامج تنظيمي جديد لإدارة المهام عدد الأخطاء الأسبوعية لموظفي خدمة العملاء. اختارت 6 موظفين وسجلت أخطاء كل منهم قبل البرنامج وبعده.",
                      "A company wants to know whether a new task-management program cuts the weekly errors of its customer-service staff. It picked 6 employees and recorded each one’s weekly errors before and after."), 30, INK)
              + task_card(L(k, "المطلوب", "Your task"), [
                  L(k, "هل للنظام الجديد تأثير معنوي على متوسط عدد الأخطاء الأسبوعية؟ (المجتمع يتبع التوزيع الطبيعي)", "Does the new system have a significant effect on mean weekly errors? (Assume a normal population.)"),
                  L(k, "استخدم مستوى ثقة 95%.", "Use 95% confidence.")])
              + '</div></div>',
              kind="practice", gap=40, section=L(k, "مثال 3", "Example 3"),
              notes=L(k, "تصحيح: في جدول المحاضرة رقم «بعد» للموظف الخامس 18، لكن مخرجات SPSS في الحل (Sig = 0.178) محسوبة على 24. كتبنا 24 هنا حتى يحصل الطلاب على نفس الحل. بالرقم 18 تكون Sig = 0.115 والقرار نفسه.",
                      "Correction: the lecture’s table has 18 for employee 5 after, but its SPSS solution (Sig = 0.178) was run with 24. We use 24 so students reproduce the lecture’s answer. With 18, Sig = 0.115 and the decision is the same."))

    # 19 example 3 answer
    k.content("ex3ans", L(k, "مثال 3 · الحل", "Example 3 · Answer"), L(k, "لا تأثير معنوي للبرنامج", "No significant effect"),
              hyp_row(("H0: μ1 = μ2", L(k, "لا فرق بين قبل وبعد", "no change")), ("H1: μ1 ≠ μ2", L(k, "يوجد فرق", "a change")))
              + ps_out("before", "after", ("20.17", "6", "4.070", "1.662"), ("18.67", "6", "4.719", "1.926"),
                       ("1.500", "2.345", ".957", "-.961", "3.961", "1.567", "5", ".178"))
              + decision([L(k, "Sig = 0.178 أكبر من α = 0.05: قبول الفرض العدمي ورفض الفرض البديل", "Sig = 0.178 > α = 0.05: accept H0, reject H1"),
                          L(k, "الأخطاء انخفضت في العينة بـ 1.5 خطأ في المتوسط، لكن الانخفاض ليس معنويًا: قد يكون صدفة.",
                            "Errors fell by 1.5 on average in the sample, but the drop is not significant: it could be chance.")], False),
              kind="practice", gap=28,
              notes=L(k, "SPSS يطبع أيضًا جدول Paired Samples Correlations (الارتباط بين قبل وبعد = .868) ولا نستخدمه في القرار. Mean = قبل − بعد = 1.5 موجب، أي أن الأخطاء قلّت.",
                      "SPSS also prints Paired Samples Correlations (r = .868 between before and after); it is not used for the decision. Mean = before − after = 1.5, positive, so errors went down."))

    # 20 case B data
    rowsb = [[i + 1, f"{b:.1f}", f"{a:.1f}"] for i, (b, a) in enumerate(zip(CASE_B_BEFORE, CASE_B_AFTER))]
    k.content("caseb", L(k, "تطبيق على الحالة", "Case study"), L(k, "هل غيّرت تجربة الأونلاين رأي الطلاب؟", "Did trying online change students’ minds?"),
              f'<div style="display:flex; flex-direction:{k.row}; gap:56px; align-items:start">'
              + vdata([L(k, "الطالب", "Student"), L(k, "الاتجاه قبل التجربة (att_before)", "Attitude before (att_before)"),
                       L(k, "الاتجاه بعد التجربة (att_after)", "Attitude after (att_after)")], rowsb, [22, 39, 39], 700, 26)
              + f'<div style="flex:1; display:flex; flex-direction:column; gap:28px">'
              + k.p(L(k, "قبل أن تقرر الإدارة، درّست مادة واحدة أونلاين بالكامل لمدة أسبوعين لـ 8 طلاب، وقاست درجة اتجاههم قبل التجربة وبعدها.",
                      "Before deciding, the university taught one course fully online for two weeks to 8 students and measured their attitude score before and after."), 30, INK)
              + task_card(L(k, "المطلوب", "Your task"), [
                  L(k, "أدخل البيانات في عمودين واختبر الفرق عند مستوى ثقة 99%.", "Enter the two columns and test the difference at 99% confidence."),
                  L(k, "ما القرار؟ وهل تحسّن الاتجاه أم ساء؟", "What is the decision? Did attitudes improve or worsen?")])
              + '</div></div>',
              kind="practice", gap=40, section=L(k, "تطبيق 2 على الحالة", "Case application 2"),
              notes=L(k, "لماذا مترابطتان؟ لأنهم نفس الطلاب الثمانية في القياسين. لاحظ أن مستوى الثقة هنا 99%، أي α = 0.01.",
                      "Why paired? The same eight students are measured twice. Note the confidence level is 99% here, so α = 0.01."))

    # 21 case B answer
    k.content("casebans", L(k, "تطبيق 2 · الحل", "Case 2 · Answer"), L(k, "التجربة حسّنت اتجاه الطلاب", "The trial improved attitudes"),
              hyp_row(("H0: μ1 = μ2", L(k, "التجربة لم تغيّر الاتجاه", "no change")), ("H1: μ1 ≠ μ2", L(k, "التجربة غيّرت الاتجاه", "a change")))
              + ps_out("att_before", "att_after", ("2.80", "8", ".400", ".141"), ("3.35", "8", ".298", ".105"),
                       ("-.550", ".256", ".091", "-.867", "-.233", "-6.068", "7", ".001"), cl=99)
              + decision([L(k, "Sig = 0.001 أصغر من α = 0.01: رفض الفرض العدمي وقبول الفرض البديل", "Sig = 0.001 < α = 0.01: reject H0, accept H1"),
                          L(k, "متوسط الفروق (قبل − بعد) سالب: −0.55، أي أن الاتجاه بعد التجربة أعلى؛ ارتفع من 2.80 إلى 3.35.",
                            "Mean = before − after = −0.55 (negative), so attitudes are higher after the trial: from 2.80 to 3.35.")], True),
              kind="practice", gap=28,
              notes=L(k, "SPSS يطرح Variable1 − Variable2 بالترتيب الذي أدخلناه. لو وضعنا att_after أولًا تصبح الإشارة موجبة والقرار نفسه. للإدارة: «تجربة الدراسة أونلاين لمدة أسبوعين حسّنت اتجاه الطلاب بشكل معنوي».",
                      "SPSS subtracts Variable1 − Variable2 in the order entered. Put att_after first and the sign flips; the decision stays. For management: “Two weeks of online study significantly improved students’ attitude.”"))

    # 22 statement: alpha comes from the question
    k.statement("alpha", L(k, "انتبه", "Watch out"), L(k, "اعرف α قبل أن تقارن", "Know α before you compare"),
                L(k, "α = 1 − مستوى الثقة المذكور في السؤال. عند ثقة 95% نقارن Sig بـ 0.05، وعند ثقة 99% نقارنها بـ 0.01. Sig = 0.03 تعني رفض الفرض العدمي في الأولى وقبوله في الثانية.",
                  "α = 1 − the confidence level in the question. At 95% we compare Sig with 0.05; at 99%, with 0.01. Sig = 0.03 rejects H0 in the first case and accepts it in the second."),
                notes=L(k, "هذا أكثر خطأ شائع في الامتحان: الطالب يقارن دائمًا بـ 0.05. في مثال 2 القادم مستوى الثقة 99%.",
                        "The most common exam mistake: always comparing with 0.05. Example 2, next, uses 99% confidence."))

    # 23 divider 4
    k.divider("d4", 4, 4, L(k, "اقرأ المخرجات", "Read the output"),
              L(k, "أسئلة اختيار من متعدد على مخرجات جاهزة", "Multiple-choice questions on ready-made output"),
              section=L(k, "قراءة المخرجات: أمثلة 2 و 4", "Reading output: examples 2 and 4"))

    # 24–25 example 2 (lecture): one-sample output, 99% confidence
    out2 = os_out("wage", "10", "407.80", "161.560", "51.090", "300", "2.110", "9", ".064", "107.800", "-58.23", "273.83", cl=99)
    quiz_slide("ex2a", L(k, "مثال 2", "Example 2"), L(k, "أجب من المخرجات", "Answer from the output"), out2, [
        (L(k, "نوع المتغير ومقياسه:", "Variable type and measure:"),
         [L(k, "كمي، Scale", "Quantitative, Scale"), L(k, "وصفي، Nominal", "Qualitative, Nominal"),
          L(k, "وصفي، Ordinal", "Qualitative, Ordinal"), L(k, "كمي، Nominal", "Quantitative, Nominal")]),
        (L(k, "القيمة الافتراضية μ0 تساوي:", "The hypothesised value μ0 is:"), ["500", "0.64", "300", "10"]),
        (L(k, "مستوى الثقة:", "The confidence level:"), ["0.05", "99%", "1%", "10%"]),
        (L(k, "مستوى المعنوية:", "The significance level:"), ["0.05", "99%", "1%", "10%"]),
    ], 1, [0, 2, 1, 2], L(k, "مستوى الثقة نقرؤه من عنوان فترة الثقة (99%)، إذن α = 1%.", "Read the confidence level from the interval heading (99%), so α = 1%."),
        section=L(k, "مثال 2", "Example 2"), stem_w=480)
    quiz_slide("ex2b", L(k, "مثال 2", "Example 2"), L(k, "أجب من المخرجات", "Answer from the output"), out2, [
        (L(k, "حجم العينة المستخدم:", "The sample size:"), ["300", "9", "10", "10%"]),
        (L(k, "عند مقارنة Sig مع مستوى المعنوية، تكون Sig:", "Compared with the significance level, Sig is:"),
         [L(k, "أكبر", "Larger"), L(k, "أصغر", "Smaller")]),
        (L(k, "في هذا الاختبار يتم:", "In this test we:"),
         [L(k, "قبول الفرض العدمي ورفض البديل", "Accept H0, reject H1"), L(k, "رفض الفرض العدمي وقبول البديل", "Reject H0, accept H1")]),
    ], 5, [2, 0, 0], L(k, "Sig = 0.064 أكبر من α = 0.01، إذن نقبل الفرض العدمي. لاحظ: لو كانت الثقة 95% لكانت 0.064 أيضًا أكبر من 0.05.",
                         "Sig = 0.064 > α = 0.01, so accept H0. Even at 95% confidence, 0.064 would still be above 0.05."), stem_w=600)

    # 26–27 example 4 (lecture): paired output, 95% confidence
    out4 = ps_out("before", "after", ("15.67", "6", "5.538", "2.261"), ("19.83", "6", "3.817", "1.558"),
                  ("-4.167", "2.639", "1.078", "-6.937", "-1.397", "-3.867", "5", ".012"))
    quiz_slide("ex4a", L(k, "مثال 4", "Example 4"), L(k, "أجب من المخرجات", "Answer from the output"), out4, [
        (L(k, "مستوى الثقة يساوي:", "The confidence level is:"), ["95%", "5%", "6", "2.693"]),
        (L(k, "مستوى المعنوية يساوي:", "The significance level is:"), ["95%", "5%", "6", "2.693"]),
        (L(k, "قيمة Sig لهذا الاختبار:", "Sig for this test:"), ["95%", "5%", "0.012", "2.693"]),
    ], 1, [0, 1, 2], L(k, "في المحاضرة يظهر أيضًا جدول Paired Samples Correlations (r = .905، Sig = .013): لا تخلط بين Sig الارتباط و Sig الاختبار.",
                         "The lecture’s output also shows Paired Samples Correlations (r = .905, Sig = .013): do not confuse that Sig with the test’s Sig."),
        section=L(k, "مثال 4", "Example 4"), stem_w=480)
    quiz_slide("ex4b", L(k, "مثال 4", "Example 4"), L(k, "أجب من المخرجات", "Answer from the output"), out4, [
        (L(k, "عند مقارنة Sig مع مستوى المعنوية، تكون Sig:", "Compared with the significance level, Sig is:"),
         [L(k, "أكبر", "Larger"), L(k, "أصغر", "Smaller")]),
        (L(k, "في هذا الاختبار يتم:", "In this test we:"),
         [L(k, "قبول الفرض العدمي ورفض البديل", "Accept H0, reject H1"), L(k, "رفض الفرض العدمي وقبول البديل", "Reject H0, accept H1")]),
    ], 4, [1, 1], L(k, "Sig = 0.012 أصغر من α = 0.05، إذن نرفض الفرض العدمي: يوجد فرق معنوي بين قبل وبعد.",
                      "Sig = 0.012 < α = 0.05, so reject H0: there is a significant before/after difference."), stem_w=600)

    # 28 summary
    def sc(n, h, d):
        return k.card(k.num_badge(n, 56, AMBER, INK, 28).replace("flex:none;", f"flex:none; align-self:{k.self_start};", 1) +
                      k.h3(h, PAPER, 40) + k.p(d, 30, MIST), bg=INK_LINE, border=False, gap=20)
    k.add("summary", k.head(L(k, "الخلاصة", "Wrap-up"), L(k, "ما الذي يجب أن تتذكره؟", "What to remember"), "practice", dark=True) + k.cards([
        sc(1, L(k, "الفروض أولًا", "Hypotheses first"), L(k, "H0: لا يوجد فرق. H1: يوجد فرق. نكتبهما قبل تشغيل SPSS.",
                                                       "H0: no difference. H1: a difference. Write both before running SPSS.")),
        sc(2, L(k, "أي اختبار؟", "Which test?"), L(k, "متوسط مقابل قيمة ثابتة: One Sample. نفس الأفراد قبل وبعد: Paired Samples.",
                                                  "A mean against a fixed value: One Sample. The same people before and after: Paired Samples.")),
        sc(3, L(k, "قاعدة القرار", "The decision rule"), L(k, "α = 1 − مستوى الثقة. Sig أصغر من α: نرفض H0. Sig أكبر من أو تساوي α: نقبل H0.",
                                                         "α = 1 − confidence. Sig < α: reject H0. Sig ≥ α: accept H0.")),
    ]), bg=INK, dark=True, section=L(k, "الخلاصة", "Wrap-up"))

    title = L(k, "سكشن 4 — اختبارات الفروض للمتوسط", "Section 4 — Hypothesis tests for the mean")
    return k.write(title, ds_record)


if __name__ == "__main__":
    lang, root = sys.argv[1], sys.argv[2]
    rec = json.loads(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3] else None
    blobs = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {}
    d = build(lang, root, rec, blobs)
    print(lang, len(d["order"]), "slides")
