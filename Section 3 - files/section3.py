"""Section 3 — Questionnaire reliability (Cronbach's alpha). Content for the Arabic and English decks."""
import sys, json
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from sectionkit import *

# (ar, en) pairs --------------------------------------------------------------
L = lambda k, ar, en: ar if k.ar else en

# Exercise 1 (section document) and Exercise 2 (new data). Output values verified with the SPSS formulas.
EX1_ITEMS = [("q1", "15.50", "16.278", ".660", ".449"), ("q2", "15.40", "14.933", ".829", ".368"),
             ("q3", "15.40", "16.933", ".570", ".489"), ("q4", "15.30", "28.900", "-.279", ".828"),
             ("q5", "15.10", "20.322", ".427", ".562"), ("q6", "15.30", "22.233", ".315", ".601")]
EX1_DATA = [[4, 4, 5, 1, 3, 4], [4, 5, 4, 1, 5, 4], [5, 4, 5, 2, 4, 4], [3, 3, 4, 5, 3, 2], [2, 2, 1, 4, 2, 2],
            [1, 2, 1, 5, 5, 5], [2, 1, 2, 1, 1, 3], [5, 5, 4, 5, 3, 3], [1, 1, 2, 4, 3, 2], [2, 3, 2, 3, 4, 2]]
EX2_DATA = [[5, 4, 4, 4, 5], [4, 3, 4, 3, 4], [2, 3, 3, 2, 1], [3, 4, 2, 4, 3],
            [5, 5, 4, 3, 5], [2, 2, 1, 2, 3], [4, 5, 3, 4, 3], [1, 2, 2, 3, 2]]
EX2_ITEMS = [("q1", "12.75", "13.357", ".959", ".802"), ("q2", "12.50", "17.143", ".751", ".858"),
             ("q3", "13.13", "18.125", ".689", ".872"), ("q4", "12.88", "20.982", ".565", ".899"),
             ("q5", "12.75", "15.929", ".735", ".864")]
ITEM_HDR = ["", "Scale Mean if Item Deleted", "Scale Variance if Item Deleted",
            "Corrected Item-Total Correlation", "Cronbach's Alpha if Item Deleted"]


def build(lang, root, ds_record=None):
    k = Kit(lang, "Computer Application", L(type("x", (), {"ar": lang == "ar"}), "سكشن 3", "Section 3"), root)

    def spss_table(header, rows, widths, size=26, width=None, hl=None, title=None, pad="12px 16px"):
        """An SPSS output table. SPSS prints in English left-to-right, so columns are never reversed."""
        th = "".join(f'<th style="width:{w}%; padding:{pad}; text-align:{"left" if i == 0 else "center"}; color:{PAPER}; font-weight:600">{h}</th>'
                     for i, (h, w) in enumerate(zip(header, widths)))
        body = ""
        for r_i, r in enumerate(rows):
            bg = AMBER_TINT if r_i == hl else (CARD if r_i % 2 == 0 else PAPER_ALT)
            body += f'<tr style="background:{bg}">' + "".join(
                f'<td style="padding:{pad}; text-align:{"left" if i == 0 else "center"}">{c}</td>' for i, c in enumerate(r)) + "</tr>"
        wcss = f" width:{width}px;" if width else ""
        cap = (f'<p style="font-family:{MONO}; font-size:26px; font-weight:600; color:{INK}; text-align:left">{title}</p>' if title else "")
        return (f'<div style="display:flex; flex-direction:column; gap:12px; align-self:{k.self_start}">{cap}'
                f'<table style="{wcss} font-size:{size}px; line-height:1.3; color:{INK}; border:1px solid {RULE}; border-radius:8px; font-variant-numeric:tabular-nums">'
                f'<tr style="background:{INK}">{th}</tr>{body}</table></div>')

    def rel_stats(alpha, n):
        return spss_table(["Cronbach's Alpha", "N of Items"], [[alpha, n]], [60, 40], 30, 520, title="Reliability Statistics")

    def item_table(items, hl=None, size=24, width=1664):
        return spss_table(ITEM_HDR, [list(r) for r in items], [8, 23, 23, 23, 23], size, width, hl, "Item-Total Statistics")

    def task_card(title, steps, width=520):
        return k.card(k.h3(title, AMBER_INK, 36) + k.steps(steps, 28), bg=AMBER_TINT, border=False, flex="none", pad=36, gap=20, width=width)

    def big_num(value, label, bg, fg, sub_fg):
        return k.card(f'<p style="font-family:{DISPLAY}; font-size:140px; font-weight:700; line-height:1; color:{fg}; text-align:center">{value}</p>'
                      + f'<p style="font-size:32px; font-weight:600; line-height:1.35; color:{sub_fg}; text-align:center">{k.t(label)}</p>',
                      bg=bg, border=False, gap=24, pad=48)

    # 1 cover
    k.cover("cover", L(k, "Computer Application · سكشن 3", "Computer Application · Section 3"),
            L(k, "ثبات الاستبيان", "Questionnaire reliability"),
            L(k, "معامل ألفا كرونباخ: هل يمكن الوثوق في إجابات الاستبيان؟", "Cronbach's alpha: can we trust the questionnaire's answers?"),
            L(k, "Horus University · 2026/2027", "Horus University · 2026/2027"),
            section=L(k, "الافتتاح وخطة السكشن", "Opening and plan"))

    # 2 hook
    k.add("hook", f'<div style="width:1500px; align-self:{k.self_start}; display:flex; flex-direction:column; gap:40px">'
          + k.eyebrow(L(k, "قبل أن نبدأ", "Before we start"), "practice", dark=True)
          + f'<h1 style="font-family:{DISPLAY}; font-size:96px; font-weight:700; line-height:1.15; color:{PAPER}">'
          + k.t(L(k, "قرار بملايين الجنيهات مبني على 6 أسئلة", "A decision worth millions, built on 6 questions")) + '</h1>'
          + k.p(L(k, "الجامعة ستقرر تحويل مواد كاملة إلى أونلاين بناءً على رأي الطلاب. لو الاستبيان نفسه لا يقيس بثبات، فالقرار كله سيُبنى على أرقام لا يُعتمد عليها.",
                  "The university will decide whether to move whole courses online based on what students say. If the questionnaire itself is unreliable, the whole decision rests on numbers nobody can trust."), 40, MIST)
          + '</div>', bg=INK, dark=True, justify="center",
          notes=L(k, "اسأل الطلاب: لو الاستبيان طلع غلط، مين يتحمل نتيجة القرار؟ ثم انتقل لخطة السكشن.",
                  "Ask: if the questionnaire is wrong, who pays for the decision? Then move to the plan."))

    # 3 agenda
    k.agenda("agenda", L(k, "خطة السكشن", "Today"), L(k, "ماذا سنتعلم اليوم؟", "What we cover today"), [
        L(k, "دراسة الحالة: استبيان التعليم الإلكتروني وعباراته الست", "The case study: the e-learning questionnaire and its six items"),
        L(k, "لماذا نقيس ثبات الاستبيان قبل تحليله؟", "Why we check a questionnaire's reliability before analysing it"),
        L(k, "معامل ألفا كرونباخ وكيف نحكم على قيمته", "Cronbach's alpha and how to judge its value"),
        L(k, "حساب ألفا في SPSS وقراءة جدول Item-Total Statistics", "Running alpha in SPSS and reading Item-Total Statistics"),
        L(k, "تمرينان تطبيقيان واختبار سريع", "Two hands-on exercises and a quick quiz"),
    ])

    # 3 divider 1
    k.divider("d1", 1, 3, L(k, "الحالة والثبات", "The case and reliability"),
              L(k, "استبيان الجامعة، ولماذا نتأكد من ثباته قبل تحليله", "The university's questionnaire, and why we check its reliability first"),
              section=L(k, "مفهوم الثبات ومعامل ألفا كرونباخ", "Reliability and Cronbach's alpha"))

    # case study (reused in later sections)
    def ccard(tag, h, d):
        return k.card(k.tag_row([tag]) + k.h3(h, size=36) + k.p(d, 28), gap=14, pad=32)
    k.content("case", L(k, "دراسة الحالة", "Case study"), L(k, "هل تتوسع الجامعة في التعليم الإلكتروني؟", "Should the university expand e-learning?"),
              k.cards([
                  ccard(L(k, "القرار", "The decision"), L(k, "إدارة الجامعة", "University management"),
                        L(k, "تريد أن تعرف اتجاه الطلاب نحو التعليم الإلكتروني قبل تحويل بعض المواد إلى أونلاين.",
                          "Wants to know students' attitudes to e-learning before moving some courses online.")),
                  ccard(L(k, "الأداة", "The tool"), L(k, "استبيان من جزأين", "A two-part questionnaire"),
                        L(k, "الجزء (أ): بيانات الطالب (النوع، الكلية، الفرقة). الجزء (ب): 6 عبارات اتجاه بمقياس ليكرت الخماسي.",
                          "Part A: student details (gender, faculty, year). Part B: 6 attitude items on a 5-point Likert scale.")),
                  ccard(L(k, "الخطة", "The plan"), L(k, "عينة صغيرة ثم كبيرة", "Small sample, then large"),
                        L(k, "تجربة على 10 طلاب (عينة استطلاعية) للتأكد من الثبات، ثم التوزيع على 400 طالب.",
                          "Pilot on 10 students to check reliability, then send to 400 students.")),
              ], 28) + k.tag(L(k, "سنعود إلى هذه الحالة في السكاشن القادمة: اليوم نختبر ثبات الجزء (ب)", "We come back to this case in later sections. Today: the reliability of Part B"), AMBER_TINT, AMBER_INK),
              gap=40,
              notes=L(k, "هذه الحالة هي الخيط الذي يربط السكاشن القادمة: الجزء (أ) سنستخدمه لاحقًا في المقارنة بين المجموعات، والجزء (ب) نبدأ به اليوم.",
                      "This case links the coming sections: Part A will be used later to compare groups; Part B is today's focus."))

    irows = [["q1", L(k, "التعليم الإلكتروني يوفر وقتي ومجهودي", "E-learning saves me time and effort")],
             ["q2", L(k, "أفهم المحاضرة المسجلة كما أفهمها في القاعة", "I understand a recorded lecture as well as one in class")],
             ["q3", L(k, "أفضّل أن تُدرَّس بعض المواد أونلاين بالكامل", "I would like some courses taught fully online")],
             ["q4", L(k, "أفضّل المحاضرات التقليدية على التعليم الإلكتروني (عبارة سلبية)", "I prefer traditional lectures to e-learning (negative item)")],
             ["q5", L(k, "منصة الجامعة الإلكترونية سهلة الاستخدام", "The university's e-learning platform is easy to use")],
             ["q6", L(k, "أنصح زملائي بالمواد الإلكترونية", "I recommend online courses to my classmates")]]
    k.content("items", L(k, "دراسة الحالة · الجزء (ب)", "Case study · Part B"), L(k, "العبارات الست التي سنقيسها", "The six items we measure"),
              k.table([L(k, "الرمز", "Code"), L(k, "العبارة", "Item")], irows, [12, 88], 28, 1664, (0,))
              + k.p(L(k, "1 = لا أوافق بشدة · 2 = لا أوافق · 3 = محايد · 4 = أوافق · 5 = أوافق بشدة",
                      "1 = strongly disagree · 2 = disagree · 3 = neutral · 4 = agree · 5 = strongly agree"), 28),
              gap=32,
              notes=L(k, "اطلب من الطلاب ملاحظة أن q4 مكتوبة عكس باقي العبارات: الموافقة عليها تعني اتجاهًا سلبيًا. سنرى أثر ذلك على الثبات في التمرين.",
                      "Point out that q4 is worded the other way round: agreeing with it means a negative attitude. We will see what that does to reliability in the exercise."))

    # why: scale analogy
    scale = k.card(k.tag_row([L(k, "مثال من الحياة", "Everyday example")]) +
                   k.h3(L(k, "ميزان غير ثابت", "An unreliable scale"), size=40) +
                   k.p(L(k, "وقفت على الميزان ثلاث مرات في دقيقة واحدة فأعطاك:", "You step on a scale three times in one minute and it reads:"), 30) +
                   k.chip_row(["70 kg", "75 kg", "68 kg"]) +
                   k.p(L(k, "وزنك لم يتغير، إذن الميزان لا يُعتمد عليه.", "Your weight did not change, so the scale cannot be trusted."), 30, INK, 600))
    survey = k.card(k.tag_row([L(k, "في حالتنا", "In our case")], AMBER_TINT, AMBER_INK) +
                    k.h3(L(k, "استبيان غير ثابت", "An unreliable questionnaire"), size=40) +
                    k.p(L(k, "لو الطالب المتحمس للتعليم الإلكتروني وافق على بعض العبارات ورفض عبارات مشابهة لها، فالعبارات لا تقيس الشيء نفسه.",
                          "If a student who likes e-learning agrees with some items and rejects similar ones, the items are not measuring the same thing."), 30) +
                    k.p(L(k, "هذا ما يكشفه اختبار الثبات قبل التوزيع على 400 طالب.",
                          "That is what a reliability check catches before the survey goes to 400 students."), 30, INK, 600))
    k.content("why", L(k, "الفكرة", "The idea"), L(k, "أداة القياس يجب أن تكون ثابتة", "A measuring tool must be consistent"),
              k.cards([scale, survey]),
              notes=L(k, "ابدأ بسؤال: لو الميزان أعطاك ثلاث قراءات مختلفة هل تثق فيه؟ الاستبيان أداة قياس مثل الميزان، والعينة الصغيرة اسمها عينة استطلاعية (Pilot) نختبر بها الأداة قبل التوزيع الكبير.",
                      "Open with: would you trust a scale that gives three different readings? A questionnaire is a measuring tool like the scale; the small trial group is a pilot sample used to test the tool before the full survey."))

    # 5 alpha: definition + judgement table
    jrows = [["0.90 +", L(k, "ممتاز", "Excellent")], ["0.80 – 0.89", L(k, "جيد", "Good")],
             ["0.70 – 0.79", L(k, "مقبول", "Acceptable")], ["0.60 – 0.69", L(k, "ضعيف", "Weak")],
             [L(k, "أقل من 0.60", "below 0.60"), L(k, "غير مقبول", "Unacceptable")]]
    left = (f'<div style="flex:1; display:flex; flex-direction:column; gap:28px">'
            + k.p(L(k, "الثبات يعني أن عبارات الاستبيان متسقة: الطالب الموافق على عبارة يوافق غالبًا على العبارات المشابهة لها.",
                    "Reliability means the items are consistent: a student who agrees with one item tends to agree with the similar ones."), 32, INK)
            + k.card(k.chip("Cronbach's Alpha") +
                     k.p(L(k, "يقيس الاتساق الداخلي لعبارات مقياس ليكرت، وقيمته بين 0 و 1. كلما اقتربت من 1 زاد الثبات.",
                           "Measures the internal consistency of Likert items. It runs from 0 to 1; the closer to 1, the more reliable."), 30),
                     gap=16, pad=32, flex="none")
            + "</div>")
    right = f'<div style="width:620px; flex:none">{k.table([L(k, "قيمة ألفا", "Alpha"), L(k, "الحكم", "Verdict")], jrows, [55, 45], 30, 620, (0,))}</div>'
    k.content("alpha", L(k, "المقياس", "The measure"), L(k, "معامل ألفا كرونباخ", "Cronbach's alpha"),
              f'<div style="display:flex; flex-direction:{k.row}; gap:64px; align-items:start">{left}{right}</div>'
              + k.tag(L(k, "الحد الأدنى المقبول في أغلب الأبحاث: 0.70", "The usual minimum in research: 0.70"), AMBER_TINT, AMBER_INK),
              gap=40,
              notes=L(k, "ركّز على رقم 0.70 كحد أدنى. الجدول للاسترشاد فقط، وتختلف الحدود قليلًا بين المراجع.",
                      "Stress 0.70 as the minimum. The table is a guide; the cut-offs vary a little between textbooks."))

    # 6 divider 2
    k.divider("d2", 2, 3, L(k, "ألفا كرونباخ في SPSS", "Cronbach's alpha in SPSS"),
              L(k, "خطوات التشغيل، ثم قراءة جدولي المخرجات", "Running it, then reading the two output tables"),
              section=L(k, "خطوات SPSS وقراءة المخرجات", "SPSS steps and output"))

    # 7 steps
    path = k.chip_row(["Analyze", "›", "Scale", "›", "Reliability Analysis"])
    k.content("steps", L(k, "خطوات التشغيل", "Steps"), L(k, "حساب ألفا كرونباخ", "Running Cronbach's alpha"),
              path + k.steps([
                  L(k, "من قائمة Analyze اختر Scale ثم Reliability Analysis.", "From Analyze choose Scale, then Reliability Analysis."),
                  L(k, "انقل العبارات (q1 إلى q6) إلى خانة Items.", "Move the items (q1 to q6) into the Items box."),
                  L(k, "تأكد أن Model مضبوط على Alpha.", "Check that Model is set to Alpha."),
                  L(k, "اضغط Statistics وفعّل Scale if item deleted، ثم Continue.", "Click Statistics, tick Scale if item deleted, then Continue."),
                  L(k, "اضغط OK لتظهر النتائج في نافذة Output.", "Click OK; the results open in the Output window."),
              ], 32), kind="term", gap=40,
              notes=L(k, "الخطوة 4 هي التي تُخرج جدول Item-Total Statistics. بدونها يظهر جدول ألفا فقط.",
                      "Step 4 is what produces the Item-Total Statistics table. Without it you only get the alpha table."))

    # 8 reading the output
    def rcard(term, h, d, rule):
        return k.card(k.chip(term) + k.h3(h, size=36) + k.p(d, 28) + '<div style="flex:1"></div>' + k.tag(rule, AMBER_TINT, AMBER_INK), gap=16, pad=32)
    k.content("read", L(k, "قراءة المخرجات", "Reading the output"), L(k, "جدولان في نافذة Output", "Two tables in the Output window"),
              k.cards([
                  rcard("Cronbach's Alpha", L(k, "جدول Reliability Statistics", "Reliability Statistics"),
                        L(k, "قيمة ألفا للمقياس كله وعدد العبارات.", "Alpha for the whole scale and the number of items."),
                        L(k, "نقارنها بـ 0.70", "Compare with 0.70")),
                  rcard("Corrected Item-Total", L(k, "ارتباط العبارة بالمقياس", "Item-to-scale correlation"),
                        L(k, "هل تسير العبارة في اتجاه باقي العبارات؟", "Does the item move with the rest of the scale?"),
                        L(k, "سالب أو أقل من 0.30 = عبارة ضعيفة", "Negative or below 0.30 = weak item")),
                  rcard("Alpha if Item Deleted", L(k, "ألفا بعد حذف العبارة", "Alpha without the item"),
                        L(k, "قيمة ألفا لو حذفنا هذه العبارة فقط.", "What alpha would be with only this item removed."),
                        L(k, "أكبر من ألفا الحالية = حذفها يفيد", "Higher than current alpha = deleting helps")),
              ], 28))

    # 9 divider 3
    k.divider("d3", 3, 3, L(k, "تمارين تطبيقية", "Hands-on exercises"),
              L(k, "استبيانان حقيقيان: واحد يحتاج تعديلًا وواحد جاهز", "Two real questionnaires: one needs fixing, one is ready"),
              section=L(k, "التمارين التطبيقية", "Exercises"))

    # 10 exercise 1 data (the section document's question)
    side = (k.p(L(k, "إجابات العينة الاستطلاعية في دراسة الحالة: 10 طلاب أجابوا عن عبارات الجزء (ب) الست (q1 إلى q6) بمقياس ليكرت الخماسي.",
                  "The case study's pilot answers: 10 students rated the six Part B items (q1 to q6) on a 5-point Likert scale."), 28, INK) +
            k.p(L(k, "1 = لا أوافق بشدة · 2 = لا أوافق · 3 = محايد · 4 = أوافق · 5 = أوافق بشدة",
                  "1 = strongly disagree · 2 = disagree · 3 = neutral · 4 = agree · 5 = strongly agree"), 26) +
            task_card(L(k, "المطلوب", "Your task"), [
                L(k, "أدخل البيانات في SPSS.", "Enter the data in SPSS."),
                L(k, "احسب ألفا كرونباخ للمقياس ككل.", "Compute Cronbach's alpha for the whole scale."),
                L(k, "إذا كان الثبات منخفضًا: استخرج Item-Total Statistics مع Scale if item deleted وحدد السؤال الذي يرفع حذفه قيمة ألفا.",
                  "If it is low: get Item-Total Statistics with Scale if item deleted and find the question whose removal raises alpha."),
            ], None))
    data1 = spss_table(["#", "q1", "q2", "q3", "q4", "q5", "q6"], [[i + 1] + r for i, r in enumerate(EX1_DATA)],
                       [16, 14, 14, 14, 14, 14, 14], 26, 720, pad="8px 16px")
    k.content("ex1data", L(k, "تمرين 1", "Exercise 1"), L(k, "اتجاهات الطلاب نحو التعليم الإلكتروني", "Attitudes to e-learning"),
              f'<div style="display:flex; flex-direction:{k.row}; gap:56px; align-items:start">{data1}'
              f'<div style="flex:1; display:flex; flex-direction:column; gap:28px">{side}</div></div>',
              kind="practice", bg=PAPER_ALT, section=L(k, "تمرين 1", "Exercise 1"),
              notes=L(k, "يدخل الطلاب البيانات بأنفسهم: في Variable View يعرّفون q1 إلى q6 (Numeric، Decimals = 0، Measure = Ordinal)، ثم يدخلون الصفوف العشرة في Data View. هذه هي العينة الاستطلاعية في دراسة الحالة.",
                      "Students enter the data themselves: in Variable View define q1 to q6 (Numeric, Decimals 0, Measure Ordinal), then type the ten rows in Data View. This is the case study's pilot sample."))

    # 11 exercise 1 questions
    k.mcq("ex1q", L(k, "تمرين 1 · الأسئلة", "Exercise 1 · Questions"), L(k, "شغّل التحليل ثم اختر", "Run the analysis, then choose"), [
        (L(k, "قيمة ألفا كرونباخ للمقياس ككل:", "Cronbach's alpha for the whole scale:"), [".627", ".828", ".368", ".700"]),
        (L(k, "الحكم على ثبات المقياس:", "The scale's reliability is:"),
         [L(k, "ممتاز", "Excellent"), L(k, "جيد", "Good"), L(k, "ضعيف (أقل من 0.70)", "Weak (below 0.70)"), L(k, "مثالي", "Perfect")]),
        (L(k, "السؤال الذي يرفع حذفه قيمة ألفا أكثر:", "The question whose removal raises alpha most:"), ["q1", "q2", "q4", "q6"]),
        (L(k, "قيمة ألفا بعد حذف هذا السؤال:", "Alpha after removing that question:"), [".601", ".749", ".828", ".952"]),
    ], notes=L(k, "الإجابات: 1 a (.627) | 2 c ضعيف | 3 c (q4) | 4 c (.828)", "Answers: 1 a (.627) | 2 c weak | 3 c (q4) | 4 c (.828)"))

    # 12 exercise 1 output: reliability statistics
    verdict = k.card(k.h3(L(k, "القراءة", "Reading it"), AMBER_INK, 36) +
                     k.p(L(k, "ألفا = 0.627، أقل من الحد المقبول 0.70، إذن ثبات المقياس ضعيف.",
                           "Alpha = 0.627, below the 0.70 minimum, so the scale's reliability is weak."), 32, INK) +
                     k.p(L(k, "لا نحذف عبارة عشوائيًا: نفتح جدول Item-Total Statistics لنعرف أي عبارة هي السبب.",
                           "We don't drop an item at random: we open Item-Total Statistics to find which item is the cause."), 30),
                     bg=AMBER_TINT, border=False, pad=40, gap=20)
    k.content("ex1out1", L(k, "تمرين 1 · الحل", "Exercise 1 · Answer"), L(k, "النتيجة الأولى: الثبات ضعيف", "First result: weak reliability"),
              f'<div style="display:flex; flex-direction:{k.row}; gap:64px; align-items:center">{rel_stats(".627", "6")}{verdict}</div>',
              kind="practice")

    # 13 exercise 1 output: item-total statistics
    k.content("ex1out2", L(k, "تمرين 1 · الحل", "Exercise 1 · Answer"), L(k, "من السبب؟ جدول Item-Total Statistics", "Who is to blame? Item-Total Statistics"),
              item_table(EX1_ITEMS, hl=3) +
              k.tag(L(k, "q4: الارتباط سالب (−.279)، وحذفها يرفع ألفا من .627 إلى .828 (أعلى قيمة في العمود)",
                      "q4: negative correlation (−.279); removing it lifts alpha from .627 to .828, the highest in the column"), AMBER_TINT, AMBER_INK),
              kind="practice", gap=36,
              notes=L(k, "باقي العبارات حذفها يخفض ألفا (كل القيم أقل من .627)، إذن هي عبارات جيدة نحتفظ بها.",
                      "Removing any other item lowers alpha (all values are below .627), so those are good items to keep."))

    # 14 statement: the reverse item
    k.statement("reverse", L(k, "لماذا q4؟", "Why q4?"), L(k, "عبارة واحدة معكوسة تكفي لإسقاط الثبات", "One reversed item can sink reliability"),
                L(k, "q4 «أفضّل المحاضرات التقليدية على التعليم الإلكتروني» مكتوبة بشكل سلبي: الطالب المتحمس يوافق على الخمس عبارات الأخرى ويرفضها. الحل: نحذفها، أو نعكس ترميزها (6 − القيمة).",
                  "q4, “I prefer traditional lectures to e-learning”, is worded negatively: an enthusiastic student agrees with the other five and rejects it. The fix: drop it, or reverse its coding (6 − value)."),
                notes=L(k, "لو عكسنا ترميز q4 بدل حذفها تصبح ألفا 0.787. لن نطبق خطوات Recode اليوم. الدرس: عند تصميم الاستبيان انتبه للعبارات السلبية.",
                        "Reverse-coding q4 instead of dropping it gives alpha 0.787. We are not doing the Recode steps today. Lesson: watch for negative items when designing a questionnaire."))

    # 15 exercise 1 decision: before / after
    arrow = f'<x-shape kind="{"arrow-left" if k.ar else "arrow-right"}" style="flex:none; width:120px; height:60px; background:{AMBER}"></x-shape>'
    k.content("ex1decision", L(k, "تمرين 1 · القرار", "Exercise 1 · Decision"), L(k, "قبل حذف q4 وبعده", "Before and after removing q4"),
              f'<div style="display:flex; flex-direction:{k.row}; gap:40px; align-items:center">'
              + big_num(".627", L(k, "6 عبارات · ثبات ضعيف", "6 items · weak"), PAPER_ALT, INK_SOFT, MUTED) + arrow
              + big_num(".828", L(k, "5 عبارات · ثبات جيد", "5 items · good"), INK, AMBER, MIST) + '</div>'
              + k.card(k.p(L(k, "كيف نكتبها في البحث: «بلغ معامل ألفا كرونباخ 0.83 بعد حذف العبارة الرابعة، وهو ما يدل على ثبات جيد للمقياس».",
                             "How to report it: “Cronbach's alpha was 0.83 after removing item 4, indicating good reliability.”"), 30, INK),
                       flex="none", pad=32),
              kind="practice", gap=40)

    # 16 exercise 2 data (new)
    items2 = [L(k, "الشرح في السكشن واضح", "Section explanations are clear"),
              L(k, "التمارين مرتبطة بالمحاضرة", "Exercises match the lecture"),
              L(k, "الوقت كافٍ للتطبيق على SPSS", "There is enough time to practise SPSS"),
              L(k, "المعيد يجيب عن الأسئلة", "The TA answers questions"),
              L(k, "أستطيع تطبيق ما تعلمته وحدي", "I can apply what I learned on my own")]
    item_list = "".join(
        f'<div style="display:flex; flex-direction:{k.row}; gap:16px; align-items:center">'
        f'<p style="font-family:{MONO}; font-size:26px; font-weight:600; color:{BLUE}; width:56px; flex:none">q{i + 1}</p>'
        f'<div style="flex:1">{k.p(t, 26, INK)}</div></div>' for i, t in enumerate(items2))
    data2 = spss_table(["q1", "q2", "q3", "q4", "q5"], EX2_DATA, [20] * 5, 26, 520)
    k.content("ex2data", L(k, "تمرين 2", "Exercise 2"), L(k, "تقييم الطلاب لمادة Computer Application", "Students rate this course"),
              k.p(L(k, "قبل أن يوزع القسم استمارة تقييم المادة على كل الطلاب، جرّبها على 8 طلاب (ليكرت الخماسي).",
                    "Before sending the course evaluation form to every student, the department tries it on 8 students (5-point Likert)."), 30) +
              f'<div style="display:flex; flex-direction:{k.row}; gap:48px; align-items:start">{data2}'
              f'<div style="flex:1; display:flex; flex-direction:column; gap:14px">{item_list}</div>'
              + task_card(L(k, "المطلوب", "Your task"), [
                  L(k, "أدخل البيانات واحسب ألفا.", "Enter the data and compute alpha."),
                  L(k, "هل نحتاج حذف أي عبارة؟", "Do we need to drop any item?")], 420) + '</div>',
              kind="practice", gap=32, section=L(k, "تمرين 2", "Exercise 2"))

    # 17 exercise 2 questions
    k.mcq("ex2q", L(k, "تمرين 2 · الأسئلة", "Exercise 2 · Questions"), L(k, "شغّل التحليل ثم اختر", "Run the analysis, then choose"), [
        (L(k, "قيمة ألفا كرونباخ للاستمارة:", "Cronbach's alpha for the form:"), [".564", ".802", ".888", ".959"]),
        (L(k, "الحكم على ثبات الاستمارة:", "The form's reliability is:"),
         [L(k, "غير مقبول", "Unacceptable"), L(k, "ضعيف", "Weak"), L(k, "مقبول", "Acceptable"), L(k, "جيد", "Good")]),
        (L(k, "هل نحذف عبارة؟", "Should we drop an item?"),
         [L(k, "نعم، q1", "Yes, q1"), L(k, "نعم، q4", "Yes, q4"), L(k, "لا، الاستمارة جاهزة", "No, the form is ready")]),
    ], notes=L(k, "الإجابات: 1 c (.888) | 2 d جيد | 3 c لا نحذف", "Answers: 1 c (.888) | 2 d good | 3 c keep all items"))

    # 18 exercise 2 answers
    k.content("ex2ans", L(k, "تمرين 2 · الحل", "Exercise 2 · Answer"), L(k, "استمارة جاهزة للتوزيع", "A form ready to go"),
              f'<div style="display:flex; flex-direction:{k.row}; gap:48px; align-items:center">{rel_stats(".888", "5")}'
              + k.card(k.p(L(k, "ألفا = 0.888 (ثبات جيد)، وكل العبارات ارتباطها موجب وأعلى من 0.30، إذن لا نحذف شيئًا.",
                             "Alpha = 0.888 (good), and every item correlates positively above 0.30, so nothing is dropped."), 30, INK),
                       bg=AMBER_TINT, border=False, pad=36) + '</div>'
              + item_table(EX2_ITEMS, size=24),
              kind="practice", gap=36,
              notes=L(k, "حذف q4 يرفع ألفا من .888 إلى .899 فقط. فرق صغير لا يستحق خسارة عبارة تقيس جانبًا مهمًا. نحذف فقط عندما يكون الثبات ضعيفًا أو العبارة معكوسة.",
                      "Dropping q4 only moves alpha from .888 to .899. Too small a gain to lose an item that covers something important. We drop items only when reliability is weak or an item is reversed."))

    # 19 quiz
    k.mcq("quiz", L(k, "اختبر نفسك", "Quick quiz"), L(k, "ثلاثة أسئلة سريعة", "Three quick questions"), [
        (L(k, "باحث حصل على ألفا = 0.45. ماذا يفعل؟", "A researcher gets alpha = 0.45. What next?"),
         [L(k, "ينشر النتائج", "Publish the results"), L(k, "يراجع العبارات قبل التوزيع", "Review the items first"), L(k, "يزيد عدد الطلاب فقط", "Just add more students")]),
        (L(k, "ارتباط Corrected Item-Total سالب لعبارة يعني:", "A negative Corrected Item-Total Correlation means:"),
         [L(k, "عبارة ممتازة", "An excellent item"), L(k, "عبارة تسير عكس الباقي", "The item runs against the rest"), L(k, "خطأ في SPSS", "An SPSS error")]),
        (L(k, "ألفا كرونباخ يُحسب على:", "Cronbach's alpha is computed on:"),
         [L(k, "عبارات مقياس ليكرت", "Likert scale items"), L(k, "رقم الطالب (ID)", "Student ID"), L(k, "النوع: ذكر / أنثى", "Gender: male / female")]),
    ], notes=L(k, "الإجابات: 1 b | 2 b | 3 a", "Answers: 1 b | 2 b | 3 a"), section=L(k, "اختبر نفسك والخلاصة", "Quiz and wrap-up"))

    # 20 summary
    def sc(n, h, d):
        return k.card(k.num_badge(n, 56, AMBER, INK, 28).replace("flex:none;", f"flex:none; align-self:{k.self_start};", 1) +
                      k.h3(h, PAPER, 40) + k.p(d, 30, MIST), bg=INK_LINE, border=False, gap=20)
    k.add("summary", k.head(L(k, "الخلاصة", "Wrap-up"), L(k, "ما الذي يجب أن تتذكره؟", "What to remember"), "practice", dark=True) + k.cards([
        sc(1, L(k, "الثبات أولًا", "Reliability first"), L(k, "نتأكد من ثبات الاستبيان على عينة صغيرة قبل توزيعه وتحليله.",
                                                         "Check reliability on a small pilot before sending and analysing the questionnaire.")),
        sc(2, L(k, "ألفا ≥ 0.70", "Alpha ≥ 0.70"), L(k, "Analyze › Scale › Reliability Analysis، ونحكم على القيمة مقابل 0.70.",
                                                    "Analyze › Scale › Reliability Analysis, then judge the value against 0.70.")),
        sc(3, L(k, "العبارة الضعيفة", "The weak item"), L(k, "ارتباط سالب أو ألفا بعد الحذف أعلى من الحالية: غالبًا عبارة معكوسة نحذفها أو نعكسها.",
                                                          "A negative correlation, or higher alpha without it: usually a reversed item to drop or recode.")),
    ]), bg=INK, dark=True)

    title = L(k, "سكشن 3 — ثبات الاستبيان", "Section 3 — Questionnaire reliability")
    return k.write(title, ds_record)


if __name__ == "__main__":
    lang, root = sys.argv[1], sys.argv[2]
    rec = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
    d = build(lang, root, rec)
    print(lang, len(d["order"]), "slides")
