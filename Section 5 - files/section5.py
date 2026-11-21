"""Section 5 — Chi-square test of independence (relationship between two qualitative variables).

Usage: python3 section5.py <ar|en> <out root> '<design-system record json>' '<blob map json>'
The blob map gives each screenshot's /_blob/<id> url in that deck: {"ct-menu": "/_blob/…", …}.
All SPSS numbers were computed in Python (scipy) with the SPSS formulas; see SECTION5_PLAN.md.
"""
import sys, os, json, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools", "legacy-kit"))
from sectionkit import *

AR_CHARS = re.compile(r"[؀-ۿ]")
LTR_RUN = re.compile(r"(?:Sig|α|H[01])(?:\s?[=≠<>≥≤]\s?(?:[−-]?\d*\.?\d+%?))?"
                     r"|[−-]?\d*\.\d+|[−-]\d+(?:\.\d+)?|\d+(?:\.\d+)?\s?[−–-]\s?\d+(?:\.\d+)?")
LATIN_PHRASE = re.compile(r"[A-Za-z][\w.()-]*(?: [A-Za-z][\w.()-]*)+")
LRI, PDI, NBSP = "⁦", "⁩", " "
GREEN, GREEN_TINT = "#2E7D4F", "#DDEFE3"


class RtlKit(Kit):
    def t(self, s):
        if not self.ar or not isinstance(s, str):
            return s
        if not AR_CHARS.search(s):
            return s
        s = LATIN_PHRASE.sub(lambda m: m.group(0).replace(" ", NBSP), s)
        return super().t(LTR_RUN.sub(lambda m: f"{LRI}{m.group(0)}{PDI}", s))


L = lambda k, ar, en: ar if k.ar else en

# ---- data (codes as in the lecture; typos fixed, see SECTION5_PLAN.md) -----------------------------
EX1 = [(0, 0), (1, 0), (0, 2), (1, 0), (0, 1), (1, 2), (0, 2), (1, 2), (0, 1), (1, 2)]   # gender, major
APP1 = [(1, 0), (1, 1), (0, 0), (1, 0), (0, 1), (1, 0), (0, 0), (1, 1), (0, 1), (1, 0)]  # gender, work
APP2 = [(0, 2), (1, 2), (1, 1), (0, 2), (0, 2), (1, 1), (0, 0), (1, 1), (0, 2), (0, 2)]  # lecture type, achievement
CASE = [0, 2, 1, 0, 1, 2, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2]                     # faculty
CASE_Q3 = [1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0]                  # q3: 1 agree, 0 not


def build(lang, root, ds_record=None, blobs=None):
    k = RtlKit(lang, "Computer Application", "سكشن 5" if lang == "ar" else "Section 5", root)
    blobs = blobs or {}

    # ---- building blocks --------------------------------------------------------------------
    def spss_table(header, rows, widths, size=22, width=None, title=None, sub=None, hl=None, pad="7px 12px", foot=None, bold_rows=()):
        th = "".join(f'<th style="width:{w}%; padding:{pad}; text-align:{"left" if i == 0 else "center"}; color:{PAPER}; font-weight:600; line-height:1.2">{h}</th>'
                     for i, (h, w) in enumerate(zip(header, widths)))
        body = ""
        for r_i, r in enumerate(rows):
            bg = CARD if r_i % 2 == 0 else PAPER_ALT
            cells = ""
            for i, c in enumerate(r):
                col = f" color:{AMBER_INK}; font-weight:700;" if hl == (r_i, i) else ""
                fw = " font-weight:600;" if r_i in bold_rows and not col else ""
                cells += f'<td style="padding:{pad}; text-align:{"left" if i == 0 else "center"};{col}{fw}">{k.t(str(c))}</td>'
            body += f'<tr style="background:{bg}">{cells}</tr>'
        wcss = f" width:{width}px;" if width else ""
        cap = ""
        if title:
            s = f' <span style="color:{MUTED}">· {sub}</span>' if sub else ""
            cap = f'<p style="font-family:{MONO}; font-size:22px; font-weight:600; color:{INK}; text-align:left; white-space:nowrap">{title}{s}</p>'
        ft = f'<p style="font-size:18px; line-height:1.3; color:{MUTED}; text-align:left">{foot}</p>' if foot else ""
        return (f'<div style="display:flex; flex-direction:column; gap:8px; flex:none">{cap}'
                f'<table style="{wcss} font-size:{size}px; line-height:1.25; color:{INK}; border:1px solid {RULE}; border-radius:8px; font-variant-numeric:tabular-nums">'
                f'<tr style="background:{INK}">{th}</tr>{body}</table>{ft}</div>')

    def cps(label, n, width=760):
        return spss_table(["", "Valid N", "Valid %", "Missing N", "Missing %", "Total N", "Total %"],
                          [[label, n, "100.0%", "0", "0.0%", n, "100.0%"]], [22, 13, 13, 13, 13, 13, 13],
                          width=width, title="Case Processing Summary", size=20)

    def xtab(rv, cv, cols, rows, width=640):
        """rows: [(label, [counts])]; totals are added."""
        n = len(cols)
        tot = [sum(r[1][i] for r in rows) for i in range(n)]
        body = [[lab, *c, sum(c)] for lab, c in rows] + [["Total", *tot, sum(tot)]]
        first = 24
        return spss_table([rv + " \\ " + cv, *cols, "Total"], body, [first] + [(100 - first - 13) / n] * n + [13],
                          width=width, title=f"{rv} * {cv} Crosstabulation", sub="Count", bold_rows=(len(body) - 1,))

    def chi_tests(rows, n, foot, exact=False, width=1000):
        """rows: [(label, value, df, asymp)] (+ exact 2s, 1s when exact)."""
        hdr = ["", "Value", "df", "Asymp. Sig. (2-sided)"]
        w = [36, 16, 10, 38]
        if exact:
            hdr += ["Exact Sig. (2-sided)", "Exact Sig. (1-sided)"]
            w = [30, 11, 7, 18, 17, 17]
        body = [list(r) for r in rows] + [["N of Valid Cases", n] + [""] * (len(hdr) - 2)]
        return spss_table(hdr, body, w, width=width, title="Chi-Square Tests", hl=(0, 3), foot=foot)

    def hyp_row(h0, h1):
        def one(label, d):
            return (f'<div style="display:flex; flex-direction:{k.row}; gap:16px; align-items:center">'
                    f'{k.chip(label, align=False)}{k.p(d, 26, INK_SOFT)}</div>')
        return (f'<div style="display:flex; flex-direction:{k.row}; gap:48px; flex-wrap:wrap">' + one("H0", h0) + one("H1", h1) + "</div>")

    def decision(lines, reject):
        fg, bg = (GREEN, GREEN_TINT) if reject else (AMBER_INK, AMBER_TINT)
        inner = k.h3(lines[0], fg, 32) + "".join(k.p(l, 26, INK) for l in lines[1:])
        return k.card(inner, bg=bg, border=False, flex="none", pad=28, gap=10)

    def task_card(title, steps, width=None):
        return k.card(k.h3(title, AMBER_INK, 32) + k.steps(steps, 26), bg=AMBER_TINT, border=False, flex="none", pad=28, gap=16, width=width)

    def codes_card(lines):
        return k.card(k.h3(L(k, "استخدم الأكواد في Values", "Codes for Values"), BLUE, 30) + "".join(k.p(l, 26, INK) for l in lines),
                      bg=BLUE_TINT, border=False, flex="none", pad=28, gap=10)

    def vdata(headers, rows, widths, width, size=24, pad="7px 12px"):
        if k.ar:
            headers, widths, rows = headers[::-1], widths[::-1], [r[::-1] for r in rows]
        th = "".join(f'<th style="width:{w}%; padding:8px 12px; text-align:center; color:{PAPER}; font-weight:600; line-height:1.25">{k.t(h)}</th>' for h, w in zip(headers, widths))
        body = "".join(f'<tr style="background:{CARD if i % 2 == 0 else PAPER_ALT}">'
                       + "".join(f'<td style="padding:{pad}; text-align:center">{k.t(str(c))}</td>' for c in r) + "</tr>" for i, r in enumerate(rows))
        return (f'<table style="width:{width}px; flex:none; font-size:{size}px; line-height:1.2; color:{INK}; border:1px solid {RULE}; border-radius:8px; '
                f'font-variant-numeric:tabular-nums"><tr style="background:{INK}">{th}</tr>{body}</table>')

    def shots(items):
        cards = ""
        for i, (key, alt, cap) in enumerate(items):
            cards += (f'<div style="flex:1; display:flex; flex-direction:column; gap:20px">'
                      f'<div style="background:{CARD}; border:1px solid {RULE}; border-radius:16px; padding:16px; display:flex; justify-content:center">'
                      f'<img src="{blobs.get(key, "")}" alt="{alt}" style="width:480px; height:360px; object-fit:contain"></div>'
                      f'<div style="display:flex; flex-direction:{k.row}; gap:16px; align-items:start">{k.num_badge(i + 1, 48, BLUE, CARD, 24)}'
                      f'<div style="flex:1">{k.p(cap, 28, INK)}</div></div></div>')
        return f'<div style="display:flex; flex-direction:{k.row}; gap:32px">{cards}</div>'

    def row2(a, b, gap=40, align="start"):
        return f'<div style="display:flex; flex-direction:{k.row}; gap:{gap}px; align-items:{align}">{a}{b}</div>'

    def col(inner, gap=24, flex="1", width=None):
        w = f"width:{width}px; flex:none;" if width else f"flex:{flex};"
        return f'<div style="{w} display:flex; flex-direction:column; gap:{gap}px">{inner}</div>'

    letters = ["أ", "ب", "ج", "د"] if k.ar else ["a", "b", "c", "d"]

    def qrow(n, stem, opts, stem_w=560):
        ops = "".join(k.option(l, o) for l, o in zip(letters, opts))
        return (f'<div style="display:flex; flex-direction:{k.row}; align-items:center; gap:24px">'
                f'{k.num_badge(n, 52, INK, AMBER, 26)}'
                f'<div style="width:{stem_w}px; flex:none">{k.p(stem, 28, INK)}</div>'
                f'<div style="flex:1; display:flex; flex-direction:{k.row}; flex-wrap:wrap; gap:14px">{ops}</div></div>')

    def quiz_slide(sid, eyebrow, title, output, questions, start, answers, notes_extra="", section=None, stem_w=560):
        rows = "".join(qrow(start + i, s, o, stem_w) for i, (s, o) in enumerate(questions))
        ans = " | ".join(f"{start + i}: {letters[a]}" for i, a in enumerate(answers))
        k.content(sid, eyebrow, title,
                  output + f'<div style="display:flex; flex-direction:column; gap:20px">{rows}</div>',
                  kind="practice", gap=28, section=section,
                  notes=L(k, f"الإجابات: {ans}. {notes_extra}", f"Answers: {ans}. {notes_extra}"))

    # labels
    G = [L(k, "ذكر", "Male"), L(k, "أنثى", "Female")]
    MAJ = [L(k, "محاسبة", "Accounting"), L(k, "إدارة أعمال", "Business"), L(k, "تسويق", "Marketing")]
    WORK = [L(k, "يعمل", "Employed"), L(k, "لا يعمل", "Not employed")]
    LT = [L(k, "حضور", "In person"), L(k, "أون لاين", "Online")]
    ACH = [L(k, "منخفض", "Low"), L(k, "متوسط", "Medium"), L(k, "مرتفع", "High")]
    FAC = [L(k, "إدارة الأعمال", "Business"), L(k, "الهندسة", "Engineering"), L(k, "طب الأسنان", "Dentistry")]
    AGR = [L(k, "غير موافق", "Not agree"), L(k, "موافق", "Agree")]

    def counts(pairs, nr, nc):
        return [[sum(1 for a, b in pairs if a == i and b == j) for j in range(nc)] for i in range(nr)]

    # ---- outputs (verified, see plan) ----
    ex1_x = xtab("gender", "major", MAJ, list(zip(G, counts(EX1, 2, 3))), width=720)
    ex1_c = chi_tests([["Pearson Chi-Square", "2.533ᵃ", "2", ".282"], ["Likelihood Ratio", "3.314", "2", ".191"],
                       ["Linear-by-Linear Association", ".000", "1", "1.000"]], "10",
                      "a. 6 cells (100.0%) have expected count less than 5. The minimum expected count is 1.00.", width=920)
    case_x = xtab("faculty", "q3", AGR, list(zip(FAC, counts(list(zip(CASE, CASE_Q3)), 3, 2))), width=600)
    case_c = chi_tests([["Pearson Chi-Square", "7.143ᵃ", "2", ".028"], ["Likelihood Ratio", "7.925", "2", ".019"],
                        ["Linear-by-Linear Association", "6.786", "1", ".009"]], "20",
                       "a. 6 cells (100.0%) have expected count less than 5. The minimum expected count is 3.00.", width=1000)
    app1_x = xtab("gender", "work", WORK, list(zip(G, counts(APP1, 2, 2))), width=560)
    app1_c = chi_tests([["Pearson Chi-Square", ".278ᵃ", "1", ".598", "", ""], ["Continuity Correctionᵇ", ".000", "1", "1.000", "", ""],
                        ["Likelihood Ratio", ".277", "1", ".599", "", ""], ["Fisher's Exact Test", "", "", "", "1.000", ".548"],
                        ["Linear-by-Linear Association", ".250", "1", ".617", "", ""]], "10",
                       "a. 4 cells (100.0%) have expected count less than 5. The minimum expected count is 1.60. b. Computed only for a 2x2 table.",
                       exact=True, width=1080)
    app2_x = xtab("lecture", "level", ACH, list(zip(LT, counts(APP2, 2, 3))), width=640)
    app2_c = chi_tests([["Pearson Chi-Square", "6.528ᵃ", "2", ".038"], ["Likelihood Ratio", "8.053", "2", ".018"],
                        ["Linear-by-Linear Association", ".833", "1", ".361"]], "10",
                       "a. 6 cells (100.0%) have expected count less than 5. The minimum expected count is .40.", width=980)

    # ================================================================================================
    # 1 cover
    k.cover("cover", L(k, "Computer Application · سكشن 5", "Computer Application · Section 5"),
            L(k, "اختبار كاي تربيع للاستقلالية", "The chi-square test of independence"),
            L(k, "هل يوجد علاقة بين متغيرين وصفيين؟", "Are two qualitative variables related?"),
            "Horus University · 2026/2027",
            section=L(k, "الافتتاح وخطة السكشن", "Opening and plan"))

    # 2 hook
    k.add("hook", f'<div style="width:1500px; align-self:{k.self_start}; display:flex; flex-direction:column; gap:40px">'
          + k.eyebrow(L(k, "قبل أن نبدأ", "Before we start"), "practice", dark=True)
          + f'<h1 style="font-family:{DISPLAY}; font-size:88px; font-weight:700; line-height:1.15; color:{PAPER}">'
          + k.t(L(k, "6 من 7 في إدارة الأعمال، و1 من 7 في طب الأسنان", "6 of 7 in Business, 1 of 7 in Dentistry")) + '</h1>'
          + k.p(L(k, "سألنا طلابًا من ثلاث كليات: هل تفضّل أن تُدرَّس بعض المواد أونلاين بالكامل؟ أغلب طلاب إدارة الأعمال وافقوا، وأغلب طلاب طب الأسنان رفضوا.",
                  "We asked students from three faculties whether they would like some courses taught fully online. Most Business students agreed; most Dentistry students did not."), 38, MIST)
          + k.p(L(k, "هل الرأي مرتبط فعلًا بالكلية، أم أن هذا الفرق صدفة في عينة صغيرة؟",
                  "Is the opinion really related to the faculty, or is the gap just chance in a small sample?"), 40, PAPER, 600)
          + '</div>', bg=INK, dark=True, justify="center",
          notes=L(k, "اسأل الطلاب: لو قررت الإدارة تحويل مواد أونلاين، هل تبدأ بكل الكليات بنفس الطريقة؟ ولو الرأي مرتبط بالكلية، ماذا يتغير في القرار؟ اختبار كاي تربيع هو الذي يحسم هل العلاقة حقيقية.",
                  "Ask: if management moves courses online, should every faculty be treated the same? If opinion depends on faculty, what changes? The chi-square test settles whether the relationship is real."))

    # 3 agenda
    k.agenda("agenda", L(k, "خطة السكشن", "Today"), L(k, "ماذا سنتعلم اليوم؟", "What we cover today"), [
        L(k, "العلاقة بين متغيرين وصفيين: متى نستخدم كاي تربيع؟", "Relationships between qualitative variables: when to use chi-square"),
        L(k, "الفروض وقاعدة القرار", "The hypotheses and the decision rule"),
        L(k, "التطبيق على SPSS من خلال Crosstabs", "Running it in SPSS with Crosstabs"),
        L(k, "تطبيق على دراسة الحالة: هل الرأي في التعليم الأونلاين مرتبط بالكلية؟", "The case: is opinion on online courses related to faculty?"),
        L(k, "قراءة المخرجات وتطبيقات للحل", "Reading the output, and practice"),
    ])

    # 4 divider 1
    k.divider("d1", 1, 3, L(k, "العلاقة بين متغيرين وصفيين", "Relationships between qualitative variables"),
              L(k, "هل الصفتان مستقلتان أم مرتبطتان؟", "Are the two traits independent, or related?"),
              section=L(k, "كاي تربيع للاستقلالية", "The chi-square test of independence"))

    # 5 case
    def ccard(tag, h, d):
        return k.card(k.tag_row([tag]) + k.h3(h, size=36) + k.p(d, 28), gap=14, pad=32)
    k.content("case", L(k, "دراسة الحالة", "Case study"), L(k, "من المتوسطات إلى العلاقات", "From means to relationships"),
              k.cards([
                  ccard(L(k, "ما وصلنا إليه", "Where we are"), L(k, "الطلاب مؤيدون", "Students approve"),
                        L(k, "في سكشن 4 وجدنا أن اتجاه الطلاب نحو التعليم الإلكتروني إيجابي، وأن تجربة الأونلاين حسّنته. الإدارة الآن تخطط لتحويل مواد أونلاين.",
                          "In Section 4, students’ attitude to e-learning was significantly positive, and trying online study improved it. Management now plans to move courses online.")),
                  ccard(L(k, "المتغيران", "The variables"), L(k, "متغيران وصفيان", "Two qualitative variables"),
                        L(k, "الكلية من الجزء (أ) من الاستبيان، وإجابة q3 «أفضّل أن تُدرَّس بعض المواد أونلاين بالكامل» مجمّعة في موافق وغير موافق. الاثنان Nominal.",
                          "Faculty, from Part A of the questionnaire, and q3 “I would like some courses taught fully online”, grouped into agree and not agree. Both are Nominal.")),
                  ccard(L(k, "سؤال الإدارة", "Management asks"), L(k, "هل الرأي مرتبط بالكلية؟", "Does opinion depend on faculty?"),
                        L(k, "لو مرتبط، نبدأ التحويل بالكليات المؤيدة. لو غير مرتبط، نطبق نفس الخطة على كل الكليات.",
                          "If it does, start with the faculties that support it. If not, apply one plan to every faculty.")),
              ], 28) + k.tag(L(k, "المتوسط لا يصلح هنا: نحتاج اختبار كاي تربيع للاستقلالية", "A mean does not work here: we need the chi-square test of independence"), AMBER_TINT, AMBER_INK),
              gap=40,
              notes=L(k, "اختبار T يحتاج متغيرًا كميًا (Scale) نحسب له متوسطًا. هنا الكلية والموافقة صفات وصفية، فلا معنى لمتوسطها، ونعدّ التكرارات بدلًا من ذلك. جمّعنا q3: موافق = 4 أو 5، غير موافق = 1 إلى 3.",
                      "A t-test needs a quantitative (Scale) variable with a mean. Faculty and agreement are qualitative, so we count frequencies instead. q3 grouping: agree = 4 or 5, not agree = 1 to 3."))

    # 6 when
    def ex_line(s):
        return f'<div style="display:flex; flex-direction:{k.row}; gap:16px; align-items:start">{k.num_badge("?", 40, BLUE_TINT, BLUE, 22)}<div style="flex:1">{k.p(s, 28, INK)}</div></div>'
    left = k.card(k.h3(L(k, "أسئلة من هذا النوع", "Questions like these"), size=36)
                  + ex_line(L(k, "هل توجد علاقة بين مستوى الدخل والمستوى التعليمي؟", "Is income level related to education level?"))
                  + ex_line(L(k, "هل توجد علاقة بين لون العينين ولون الشعر في مجتمع ما؟", "Is eye colour related to hair colour in a population?"))
                  + ex_line(L(k, "هل توجد علاقة بين المستوى التحصيلي ودخل الأسرة؟", "Is academic achievement related to family income?")),
                  gap=20, pad=36)
    right = k.card(k.h3(L(k, "متى نستخدم كاي تربيع؟", "When to use chi-square"), size=36)
                   + k.p(L(k, "لاختبار هل توجد علاقة بين متغيرين وصفيين: متغيران اسميان، أو متغير اسمي والآخر ترتيبي.",
                           "To test whether two qualitative variables are related: two nominal variables, or one nominal and one ordinal."), 28)
                   + k.tag_row(["Nominal × Nominal", "Nominal × Ordinal"]),
                   gap=20, pad=36, flex="none", width=720)
    k.content("when", L(k, "التعريف", "Definition"), L(k, "متى نحتاج كاي تربيع للاستقلالية؟", "When do we need the chi-square test?"),
              k.p(L(k, "نحتاج في حالات كثيرة أن نعرف هل توجد علاقة بين صفتين (متغيرين وصفيين) من صفات مجتمع ما.",
                    "We often need to know whether two traits (qualitative variables) of a population are related."), 30, INK)
              + row2(left, right, 32, "stretch"), gap=40,
              notes=L(k, "المتغير الوصفي قيمه فئات وليست أرقامًا حقيقية: النوع، الكلية، الحالة الوظيفية، مستوى التحصيل. حتى لو أدخلناه بأكواد 0 و 1 و 2 فالأكواد أسماء وليست كميات.",
                      "A qualitative variable holds categories, not real numbers: gender, faculty, employment, achievement level. Even coded 0, 1, 2, the codes are names, not amounts."))

    # 7 hypotheses + rule
    def rule(f, h, d, reject):
        fg, bg = (GREEN, GREEN_TINT) if reject else (AMBER_INK, AMBER_TINT)
        return k.card(k.chip(f) + k.h3(h, fg, 32) + k.p(d, 26, INK), bg=bg, border=False, gap=12, pad=28)
    hyps = k.card(k.chip("H0") + k.h3(L(k, "الفرض العدمي", "The null hypothesis"), size=32)
                  + k.p(L(k, "لا توجد علاقة ارتباط معنوية بين المتغيرين (المتغيران مستقلان).", "No significant relationship between the two variables (they are independent)."), 26)
                  + k.chip("H1") + k.h3(L(k, "الفرض البديل", "The alternative hypothesis"), size=32)
                  + k.p(L(k, "توجد علاقة ارتباط معنوية بين المتغيرين (المتغيران غير مستقلين).", "A significant relationship between the two variables (they are not independent)."), 26),
                  gap=14, pad=32)
    mid = col(k.steps([L(k, "تعريف الفروض", "State the hypotheses"), L(k, "التطبيق على برنامج SPSS", "Run the test in SPSS"),
                       L(k, "مقارنة قيمة Sig مع مستوى المعنوية α", "Compare Sig with the significance level α")], 28, INK)
              + rule("Sig ≥ α", L(k, "قبول الفرض العدمي ورفض البديل", "Accept H0, reject H1"), L(k, "لا توجد علاقة معنوية: المتغيران مستقلان.", "No significant relationship: the variables are independent."), False)
              + rule("Sig < α", L(k, "رفض الفرض العدمي وقبول البديل", "Reject H0, accept H1"), L(k, "توجد علاقة معنوية بين المتغيرين.", "The variables are significantly related."), True),
              gap=20, width=860)
    k.content("rule", L(k, "خطوات الاختبار", "The procedure"), L(k, "الفروض وقاعدة القرار", "Hypotheses and the decision rule"),
              row2(hyps, mid, 48), gap=40,
              notes=L(k, "نفس قاعدة القرار التي استخدمناها في سكشن 4. الجديد هو صياغة الفروض: هنا نتكلم عن علاقة واستقلال، وليس عن متوسط. α = 1 − مستوى الثقة، والافتراضي 0.05.",
                      "The same decision rule as Section 4. What changes is the wording: relationship and independence, not a mean. α = 1 − the confidence level; 0.05 by default."))

    # 8 divider 2
    k.divider("d2", 2, 3, L(k, "كاي تربيع على SPSS", "Chi-square in SPSS"),
              L(k, "من خلال Crosstabs: جدول تقاطع واختبار", "Through Crosstabs: a cross-table and a test"),
              section=L(k, "التطبيق على SPSS", "In SPSS"))

    # 9 how
    k.content("how", "Crosstabs · Chi-Square", L(k, "خطوات التطبيق على SPSS", "Steps in SPSS"),
              k.chip_row(["Analyze", "›", "Descriptive Statistics", "›", "Crosstabs"])
              + k.steps([L(k, "أدخل البيانات في SPSS (كل متغير في عمود، وعرّف الأكواد في Values) ثم اختر المسار أعلاه.", "Enter the data (one column per variable, codes defined in Values), then follow the menu path above."),
                         L(k, "ضع المتغير الأول داخل Row(s) والمتغير الثاني داخل Column(s)، أو العكس.", "Put the first variable in Row(s) and the second in Column(s), or the other way round."),
                         L(k, "اضغط على Statistics واختر Chi-square.", "Click Statistics and tick Chi-square."),
                         L(k, "اضغط Continue ثم OK.", "Click Continue, then OK.")], 30, INK), kind="term", gap=44,
              notes=L(k, "لا يهم أي متغير في Row وأيهما في Column: قيمة كاي تربيع و Sig لا تتغيران. لو نسيت اختيار Chi-square من Statistics سيطلع جدول التقاطع فقط بدون اختبار.",
                      "It does not matter which variable goes in Row and which in Column: chi-square and Sig stay the same. Forget to tick Chi-square and you get only the cross-table, no test."))

    # 10 screenshots
    k.content("shots", L(k, "التطبيق على SPSS", "In SPSS"), L(k, "كاي تربيع خطوة بخطوة", "Chi-square step by step"),
              shots([("ct-menu", "Analyze menu, Descriptive Statistics, Crosstabs", "Analyze › Descriptive Statistics › Crosstabs"),
                     ("ct-dialog", "Crosstabs dialog with gender in Rows and major in Columns",
                      L(k, "متغير في Row(s) والآخر في Column(s)", "One variable in Row(s), the other in Column(s)")),
                     ("ct-stats", "Crosstabs Statistics dialog with Chi-square ticked",
                      L(k, "من Statistics اختر Chi-square ثم Continue", "In Statistics, tick Chi-square, then Continue"))]),
              bg=PAPER_ALT, gap=44)

    # 11 example 1 data
    rows1 = [[i + 1, G[g], MAJ[m]] for i, (g, m) in enumerate(EX1)]
    k.content("ex1data", L(k, "مثال 1", "Example 1"), L(k, "النوع والتخصص الدراسي", "Gender and major"),
              row2(vdata([L(k, "رقم الطالب", "Student"), L(k, "النوع (gender)", "Gender (gender)"), L(k, "التخصص الدراسي (major)", "Major (major)")],
                         rows1, [26, 32, 42], 640, 24),
                   col(k.p(L(k, "يرغب أحد الباحثين في دراسة العلاقة بين النوع والتخصص الدراسي لدى 10 طلاب، وقد جُمعت البيانات كما هي موضحة بالجدول.",
                             "A researcher wants to study the relationship between gender and major for 10 students. The data are in the table."), 28, INK)
                       + task_card(L(k, "المطلوب", "Your task"), [
                           L(k, "تطبيق اختبار كاي تربيع للاستقلالية باستخدام SPSS.", "Run the chi-square test of independence in SPSS."),
                           L(k, "كتابة الفرضيات الإحصائية وتفسير النتائج بدقة.", "Write the hypotheses and interpret the results.")])
                       + codes_card([L(k, "النوع: 0 = ذكر، 1 = أنثى", "gender: 0 = male, 1 = female"),
                                     L(k, "التخصص: 0 = محاسبة، 1 = إدارة أعمال، 2 = تسويق", "major: 0 = accounting, 1 = business, 2 = marketing")])),
                   48),
              kind="practice", gap=32, section=L(k, "مثال 1", "Example 1"),
              notes=L(k, "اطلب من الطلاب كتابة الفروض قبل التشغيل. المستوى الافتراضي α = 0.05.", "Have students write the hypotheses before running SPSS. Default α = 0.05."))

    # 12 example 1 answer
    k.content("ex1ans", L(k, "مثال 1 · الحل", "Example 1 · Answer"), L(k, "لا توجد علاقة: النوع والتخصص مستقلان", "Gender and major are independent"),
              hyp_row(L(k, "لا توجد علاقة ارتباط معنوية بين النوع والتخصص", "no significant relationship between gender and major"),
                      L(k, "توجد علاقة ارتباط معنوية بين النوع والتخصص", "a significant relationship between gender and major"))
              + row2(ex1_x, ex1_c, 24, "end")
              + decision([L(k, "Sig = 0.282 أكبر من α = 0.05: قبول الفرض العدمي ورفض الفرض البديل", "Sig = 0.282 > α = 0.05: accept H0, reject H1"),
                          L(k, "لا توجد علاقة معنوية بين النوع والتخصص الدراسي؛ اختلاف التوزيع في العينة يمكن أن يكون صدفة.",
                            "Gender and major are not significantly related; the differences in the table could be chance.")], False),
              kind="practice", gap=28,
              notes=L(k, "نقرأ Sig من صف Pearson Chi-Square فقط، عمود Asymp. Sig. (2-sided). الملاحظة a تقول إن كل الخلايا تكرارها المتوقع أقل من 5 لأن العينة 10 طلاب فقط؛ في بحث حقيقي نحتاج عينة أكبر.",
                      "Read Sig from the Pearson Chi-Square row only, Asymp. Sig. (2-sided). Note a says every cell’s expected count is below 5 because there are only 10 students; a real study needs a bigger sample."))

    # 13 case data (two halves of 10)
    rc = [[i + 1, FAC[f], AGR[a]] for i, (f, a) in enumerate(zip(CASE, CASE_Q3))]
    hdr = [L(k, "الطالب", "No."), L(k, "الكلية (faculty)", "Faculty (faculty)"),
           L(k, "أفضّل أن تُدرَّس بعض المواد أونلاين بالكامل (q3)", "I would like some courses taught fully online (q3)")]
    tables = row2(vdata(hdr, rc[:10], [18, 36, 46], 520, 22, "5px 10px"), vdata(hdr, rc[10:], [18, 36, 46], 520, 22, "5px 10px"), 24)
    k.content("casedata", L(k, "تطبيق على الحالة", "Case study"), L(k, "هل الرأي في التعليم الأونلاين مرتبط بالكلية؟", "Is opinion on online courses related to faculty?"),
              row2(tables, col(task_card(L(k, "المطلوب", "Your task"), [
                        L(k, "أدخل البيانات بالأكواد واختبر العلاقة عند مستوى ثقة 95%.", "Enter the data with codes and test the relationship at 95% confidence."),
                        L(k, "ماذا نقول للإدارة؟", "What do we tell management?")])
                       + codes_card([L(k, "الكلية: 0 = إدارة الأعمال، 1 = الهندسة، 2 = طب الأسنان", "faculty: 0 = Business, 1 = Engineering, 2 = Dentistry"),
                                     L(k, "q3: 0 = غير موافق، 1 = موافق", "q3: 0 = not agree, 1 = agree")])), 40),
              kind="practice", gap=28, section=L(k, "تطبيق على الحالة", "Case application"),
              notes=L(k, "20 طالبًا من ثلاث كليات أجابوا عن q3، وجمّعنا الإجابة: موافق (4 أو 5) وغير موافق (1 إلى 3). لماذا كاي تربيع؟ لأن الكلية والموافقة متغيران وصفيان.",
                      "20 students from three faculties answered q3; answers grouped as agree (4 or 5) and not agree (1 to 3). Why chi-square? Faculty and agreement are both qualitative."))

    # 14 case answer
    k.content("caseans", L(k, "تطبيق على الحالة · الحل", "Case · Answer"), L(k, "الرأي مرتبط بالكلية", "Opinion depends on faculty"),
              hyp_row(L(k, "لا توجد علاقة بين الكلية والموافقة على التدريس أونلاين", "faculty and agreement are not related"),
                      L(k, "توجد علاقة بين الكلية والموافقة على التدريس أونلاين", "faculty and agreement are related"))
              + row2(case_x, case_c, 44, "end")
              + decision([L(k, "Sig = 0.028 أصغر من α = 0.05: رفض الفرض العدمي وقبول الفرض البديل", "Sig = 0.028 < α = 0.05: reject H0, accept H1"),
                          L(k, "الرأي مرتبط بالكلية: 6 من 7 موافقون في إدارة الأعمال مقابل 1 من 7 في طب الأسنان. للإدارة: ابدأوا تحويل المواد أونلاين بالكليات المؤيدة.",
                            "Opinion depends on faculty: 6 of 7 agree in Business against 1 of 7 in Dentistry. For management: start moving courses online in the faculties that support it.")], True),
              kind="practice", gap=28,
              notes=L(k, "كاي تربيع يقول هل توجد علاقة، وجدول Crosstabulation يقول شكلها: من أين جاء الفرق. تفسير مقبول لماذا طب الأسنان أقل تأييدًا: مواده عملية تحتاج معامل. العلاقة لا تعني سببية.",
                      "Chi-square says whether there is a relationship; the Crosstabulation shows its shape. A plausible reason Dentistry is less keen: its courses are practical and lab-based. A relationship is not causation."))

    # 15 statement: read the Pearson row
    k.statement("pearson", L(k, "انتبه", "Watch out"), L(k, "اقرأ Sig من صف Pearson", "Read Sig from the Pearson row"),
                L(k, "جدول Chi-Square Tests فيه أكثر من صف، ولكل صف Sig. القرار يكون من الصف الأول Pearson Chi-Square فقط، عمود Asymp. Sig. (2-sided). في التطبيق 2 صف Linear-by-Linear يعطي Sig = 0.361 بينما Pearson يعطي 0.038 والقرار عكسي.",
                  "The Chi-Square Tests table has several rows, each with a Sig. Decide from the first row, Pearson Chi-Square, column Asymp. Sig. (2-sided), only. In application 2, Linear-by-Linear gives Sig = 0.361 while Pearson gives 0.038: opposite decisions."),
                notes=L(k, "أكثر خطأ شائع: الطالب يقرأ آخر رقم في الجدول أو صف Linear-by-Linear. في جداول 2×2 يظهر أيضًا Fisher's Exact Test و Continuity Correction؛ نلتزم بـ Pearson كما في المحاضرة.",
                        "The most common mistake: reading the last number or the Linear-by-Linear row. 2×2 tables also show Fisher's Exact Test and Continuity Correction; we stick to Pearson, as in the lecture."))

    # 16 divider 3
    k.divider("d3", 3, 3, L(k, "اقرأ المخرجات وطبّق", "Read the output and practise"),
              L(k, "أسئلة اختيار من متعدد، ثم تطبيقان للحل", "Multiple-choice questions, then two applications"),
              section=L(k, "قراءة المخرجات والتطبيقات", "Reading output and practice"))

    # 17–18 example 2 MCQ on example 1's output
    ex2_c = chi_tests([["Pearson Chi-Square", "2.533ᵃ", "2", ".282"], ["Likelihood Ratio", "3.314", "2", ".191"],
                       ["Linear-by-Linear Association", ".000", "1", "1.000"]], "10",
                      "a. 6 cells (100.0%) have expected count less than 5. The minimum expected count is 1.00.", width=880)
    out2 = row2(col(cps("gender * major", "10", 760) + ex1_x, 20, width=760), ex2_c, 24, "start")
    quiz_slide("ex2a", L(k, "مثال 2", "Example 2"), L(k, "أجب من المخرجات", "Answer from the output"), out2, [
        (L(k, "عدد القيم الصالحة:", "Number of valid cases:"), ["10", L(k, "صفر", "0"), "0.282", "100%"]),
        (L(k, "عدد القيم المفقودة:", "Number of missing cases:"), ["10", L(k, "صفر", "0"), "0.282", "100%"]),
    ], 1, [0, 1], L(k, "نقرأ العددين من جدول Case Processing Summary: Valid N = 10 و Missing N = 0.", "Both come from Case Processing Summary: Valid N = 10, Missing N = 0."),
        section=L(k, "مثال 2", "Example 2"))
    quiz_slide("ex2b", L(k, "مثال 2", "Example 2"), L(k, "أجب من المخرجات", "Answer from the output"), out2, [
        (L(k, "عند مقارنة Sig مع مستوى المعنوية، تكون Sig:", "Compared with the significance level, Sig is:"), [L(k, "أكبر", "Larger"), L(k, "أقل", "Smaller")]),
        (L(k, "في هذا الاختبار يتم:", "In this test we:"), [L(k, "قبول الفرض العدمي ورفض البديل", "Accept H0, reject H1"), L(k, "رفض الفرض العدمي وقبول البديل", "Reject H0, accept H1")]),
    ], 3, [0, 0], L(k, "Sig = 0.282 أكبر من 0.05، إذن نقبل الفرض العدمي: لا علاقة معنوية بين النوع والتخصص.", "Sig = 0.282 > 0.05, so accept H0: gender and major are not significantly related."))

    # 19 application 1 data
    rowsa = [[i + 1, G[g], WORK[w]] for i, (g, w) in enumerate(APP1)]
    k.content("app1", L(k, "تطبيق 1", "Application 1"), L(k, "النوع والحالة الوظيفية", "Gender and employment"),
              row2(vdata([L(k, "الشخص", "Person"), L(k, "النوع (gender)", "Gender (gender)"), L(k, "الحالة الوظيفية (work)", "Employment (work)")],
                         rowsa, [26, 32, 42], 640, 24),
                   col(k.p(L(k, "يرغب أحد الباحثين في دراسة العلاقة بين النوع والحالة الوظيفية لدى 10 أشخاص، وقد جُمعت البيانات كما هي موضحة بالجدول.",
                             "A researcher wants to study the relationship between gender and employment for 10 people. The data are in the table."), 28, INK)
                       + task_card(L(k, "المطلوب", "Your task"), [
                           L(k, "تطبيق اختبار كاي تربيع للاستقلالية باستخدام SPSS.", "Run the chi-square test of independence in SPSS."),
                           L(k, "كتابة الفرضيات الإحصائية وتفسير النتائج بدقة.", "Write the hypotheses and interpret the results.")])
                       + codes_card([L(k, "النوع: 0 = ذكر، 1 = أنثى", "gender: 0 = male, 1 = female"),
                                     L(k, "الحالة الوظيفية: 0 = يعمل، 1 = لا يعمل", "work: 0 = employed, 1 = not employed")])), 48),
              kind="practice", gap=32, section=L(k, "تطبيق 1", "Application 1"),
              notes=L(k, "تصحيح من المحاضرة: كود المتغير الثاني مكتوب «التخصص» والصحيح «الحالة الوظيفية»، والصف 8 «لا تعمل» = لا يعمل.",
                      "Lecture fixes: the second variable’s codes were labelled “major”; it is employment. Row 8 “لا تعمل” is the same category as “not employed”."))

    # 20 application 1 answer
    k.content("app1ans", L(k, "تطبيق 1 · الحل", "Application 1 · Answer"), L(k, "لا توجد علاقة بين النوع والعمل", "Gender and employment are not related"),
              hyp_row(L(k, "لا توجد علاقة ارتباط معنوية بين النوع والحالة الوظيفية", "no significant relationship between gender and employment"),
                      L(k, "توجد علاقة ارتباط معنوية بين النوع والحالة الوظيفية", "a significant relationship between gender and employment"))
              + row2(app1_x, app1_c, 24, "end")
              + decision([L(k, "Sig = 0.598 أكبر من α = 0.05: قبول الفرض العدمي ورفض الفرض البديل", "Sig = 0.598 > α = 0.05: accept H0, reject H1"),
                          L(k, "لا توجد علاقة معنوية بين النوع والحالة الوظيفية؛ المتغيران مستقلان.", "Gender and employment are not significantly related; the variables are independent.")], False),
              kind="practice", gap=28,
              notes=L(k, "في جداول 2×2 يضيف SPSS صفي Continuity Correction و Fisher's Exact Test. نقرأ Pearson كما تعلمنا، والقرار هنا واحد في كل الصفوف.",
                      "For 2×2 tables SPSS adds Continuity Correction and Fisher's Exact Test. Read Pearson as usual; here every row gives the same decision."))

    # 21 application 2 data
    rowsb = [[i + 1, LT[t], ACH[a]] for i, (t, a) in enumerate(APP2)]
    k.content("app2", L(k, "تطبيق 2", "Application 2"), L(k, "نوع المحاضرات ومستوى التحصيل", "Lecture type and achievement"),
              row2(vdata([L(k, "الطالب", "Student"), L(k, "نوع المحاضرات (lecture)", "Lecture type (lecture)"), L(k, "مستوى التحصيل (level)", "Achievement (level)")],
                         rowsb, [24, 38, 38], 640, 24),
                   col(k.p(L(k, "يرغب أحد الباحثين في دراسة العلاقة بين نوع المحاضرات ومستوى التحصيل لدى 10 طلاب، وقد جُمعت البيانات كما هي موضحة بالجدول.",
                             "A researcher wants to study the relationship between lecture type and achievement for 10 students. The data are in the table."), 28, INK)
                       + task_card(L(k, "المطلوب", "Your task"), [
                           L(k, "تطبيق اختبار كاي تربيع للاستقلالية باستخدام SPSS.", "Run the chi-square test of independence in SPSS."),
                           L(k, "كتابة الفرضيات الإحصائية وتفسير النتائج بدقة.", "Write the hypotheses and interpret the results.")])
                       + codes_card([L(k, "نوع المحاضرات: 0 = حضور، 1 = أون لاين", "lecture: 0 = in person, 1 = online"),
                                     L(k, "مستوى التحصيل: 0 = منخفض، 1 = متوسط، 2 = مرتفع", "level: 0 = low, 1 = medium, 2 = high")])), 48),
              kind="practice", gap=32, section=L(k, "تطبيق 2", "Application 2"),
              notes=L(k, "لماذا يهمنا؟ هذا سؤال الإدارة في دراسة الحالة: هل التعليم الأونلاين يرتبط بتحصيل الطلاب؟ تصحيحات من المحاضرة: كود «مرتفع» = 2 وليس 3، واسما المتغيرين نوع المحاضرات ومستوى التحصيل (كانا «النوع» و«التخصص»). مستوى التحصيل ترتيبي (Ordinal) ونوع المحاضرات اسمي.",
                      "Why it matters: it is our case’s question too, is online teaching related to achievement? Lecture fixes: “high” is coded 2, not 3, and the code labels read “gender” and “major” instead of lecture type and achievement. Achievement is Ordinal; lecture type is Nominal."))

    # 22 application 2 answer
    k.content("app2ans", L(k, "تطبيق 2 · الحل", "Application 2 · Answer"), L(k, "التحصيل مرتبط بنوع المحاضرات", "Achievement is related to lecture type"),
              hyp_row(L(k, "لا توجد علاقة ارتباط معنوية بين نوع المحاضرات والتحصيل", "no significant relationship between lecture type and achievement"),
                      L(k, "توجد علاقة ارتباط معنوية بين نوع المحاضرات والتحصيل", "a significant relationship between lecture type and achievement"))
              + row2(app2_x, app2_c, 44, "end")
              + decision([L(k, "Sig = 0.038 أصغر من α = 0.05: رفض الفرض العدمي وقبول الفرض البديل", "Sig = 0.038 < α = 0.05: reject H0, accept H1"),
                          L(k, "توجد علاقة معنوية: 5 من 6 طلاب الحضور تحصيلهم مرتفع، و3 من 4 طلاب الأون لاين تحصيلهم متوسط.",
                            "There is a significant relationship: 5 of 6 in-person students scored high, and 3 of 4 online students scored medium.")], True),
              kind="practice", gap=28,
              notes=L(k, "لاحظ صف Linear-by-Linear: Sig = 0.361. لو قرأه الطالب لقبل الفرض العدمي خطأً. للإدارة في دراسة الحالة: مع تحويل مواد أونلاين نحتاج متابعة التحصيل، لكن 10 طلاب عينة صغيرة جدًا للحكم النهائي.",
                      "Note the Linear-by-Linear row: Sig = 0.361. A student reading it would wrongly accept H0. For the case: moving courses online needs achievement monitoring, though 10 students is far too small for a final verdict."))

    # 23 summary
    def sc(n, h, d):
        return k.card(k.num_badge(n, 56, AMBER, INK, 28).replace("flex:none;", f"flex:none; align-self:{k.self_start};", 1) +
                      k.h3(h, PAPER, 40) + k.p(d, 30, MIST), bg=INK_LINE, border=False, gap=20)
    k.add("summary", k.head(L(k, "الخلاصة", "Wrap-up"), L(k, "ما الذي يجب أن تتذكره؟", "What to remember"), "practice", dark=True) + k.cards([
        sc(1, L(k, "متى؟", "When?"), L(k, "علاقة بين متغيرين وصفيين: اسمي × اسمي أو اسمي × ترتيبي.", "A relationship between two qualitative variables: nominal × nominal or nominal × ordinal.")),
        sc(2, L(k, "كيف؟", "How?"), L(k, "Analyze › Descriptive Statistics › Crosstabs، ثم Statistics › Chi-square.", "Analyze › Descriptive Statistics › Crosstabs, then Statistics › Chi-square.")),
        sc(3, L(k, "القرار", "The decision"), L(k, "Sig من صف Pearson. أصغر من α: توجد علاقة. أكبر من أو تساوي α: المتغيران مستقلان.",
                                              "Sig from the Pearson row. Below α: related. At or above α: independent.")),
    ]), bg=INK, dark=True, section=L(k, "الخلاصة", "Wrap-up"))

    title = L(k, "سكشن 5 — اختبار كاي تربيع للاستقلالية", "Section 5 — The chi-square test of independence")
    return k.write(title, ds_record)


if __name__ == "__main__":
    lang, root = sys.argv[1], sys.argv[2]
    rec = json.loads(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3] else None
    blobs = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {}
    d = build(lang, root, rec, blobs)
    print(lang, len(d["order"]), "slides")
