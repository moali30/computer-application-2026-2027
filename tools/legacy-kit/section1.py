"""Section 1 — Introduction to SPSS. Content for the Arabic and English decks."""
import sys, json
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from sectionkit import *

IMG = {
    "ar": {"vv": "/_blob/92e1cbc44637ee53c3c55b7e9509aaa5", "type": "/_blob/660fcc632e2bd77e8af4b78897db35aa",
           "values": "/_blob/37ca2cb044889ad6354d33cfcd9b04fb", "dv": "/_blob/023caccdb3ba315ec0ce23dbe46ff776"},
    "en": {"vv": "/_blob/27af6946924b44d77e11b21b0d625c7b", "type": "/_blob/1b225d7233fc269bd4b9fed2c101aa7e",
           "values": "/_blob/0f9e4565a4825af3219b3191a5266f2f", "dv": "/_blob/c1f4390a8b9a299ff393eb036bb100e1"},
}

# (ar, en) pairs --------------------------------------------------------------
L = lambda k, ar, en: ar if k.ar else en


def build(lang, root, ds_record=None):
    k = Kit(lang, "Computer Application", L(type("x", (), {"ar": lang == "ar"}), "سكشن 1", "Section 1"), root)
    im = IMG[lang]

    # 1 cover
    k.cover("cover", L(k, "Computer Application · سكشن 1", "Computer Application · Section 1"),
            L(k, "مقدمة في SPSS", "Introduction to SPSS"),
            L(k, "المتغيرات، نوافذ البرنامج، ومحرر البيانات", "Variables, program windows and the Data Editor"),
            L(k, "Horus University · 2026/2027", "Horus University · 2026/2027"),
            section=L(k, "الافتتاح وخطة السكشن", "Opening and plan"))

    # 2 agenda
    k.agenda("agenda", L(k, "خطة السكشن", "Today"), L(k, "ماذا سنتعلم اليوم؟", "What we cover today"), [
        L(k, "مصطلحات إحصائية هامة: المتغير وأنواعه ومقاييسه", "Key statistical terms: variables, types and measures"),
        L(k, "ما هو برنامج SPSS؟", "What is SPSS?"),
        L(k, "نوافذ البرنامج: محرر البيانات وعرض المخرجات", "SPSS windows: Data Editor and Output Viewer"),
        L(k, "خصائص المتغيرات في Variable View وإدخال البيانات في Data View", "Variable properties in Variable View, data entry in Data View"),
        L(k, "ثلاثة تمارين تطبيقية على SPSS", "Three hands-on SPSS exercises"),
    ])

    # 3 divider 1
    k.divider("d1", 1, 3, L(k, "مصطلحات إحصائية هامة", "Key statistical terms"),
              L(k, "المتغير، أنواعه، ومقياس كل نوع", "The variable, its types, and the measure of each type"),
              section=L(k, "المتغير وأنواعه ومقاييسه", "Variables, types and measures"))

    # 4 variable definition
    qual = k.card(k.tag_row([L(k, "اسمي · Nominal", "Nominal"), L(k, "رتبي · Ordinal", "Ordinal")]) +
                  k.h3(L(k, "المتغير الوصفي (النوعي)", "Qualitative (categorical) variable")) +
                  k.p(L(k, "يوجد في شكل كلمات أو أرقام لا تُجرى عليها العمليات الحسابية. وينقسم إلى نوعين: اسمي ورتبي.",
                        "Recorded as words, or as numbers that no arithmetic is done on. It has two types: nominal and ordinal.")))
    quant = k.card(k.tag_row([L(k, "كمي · Scale", "Scale")]) +
                   k.h3(L(k, "المتغير الكمي", "Quantitative variable")) +
                   k.p(L(k, "يعبّر عن مقدار عددي يمكن إجراء العمليات الحسابية عليه، ويكون مقياسه Scale.",
                         "Expresses a numeric amount that arithmetic can be done on. Its measure is Scale.")))
    k.content("variable", L(k, "المصطلح الأول", "Term 1"), L(k, "المتغير", "The variable"),
              k.p(L(k, "خاصية يمكن ملاحظتها أو قياسها، وتختلف من فرد إلى آخر أو من حالة إلى أخرى. تنقسم المتغيرات إلى نوعين رئيسيين:",
                    "A characteristic that can be observed or measured and that differs from one person or case to another. Variables fall into two main types:"),
                  40, INK) + k.cards([qual, quant]),
              notes=L(k, "ابدأ بالتعريف ثم اسأل الطلاب عن أمثلة من حياتهم قبل الانتقال لأنواع المقاييس.",
                      "Start with the definition, then ask students for everyday examples before moving on to measures."))

    # 5 three measures with examples
    def mcard(term, name, desc, ex):
        return k.card(k.chip(term) + k.h3(name, size=40) + k.p(desc, 30) +
                      f'<div style="height:1px; background:{RULE}"></div>' + k.bullets(ex, 30, INK, 10), gap=18)
    k.content("measures", L(k, "مقاييس المتغيرات", "Measurement levels"), L(k, "ثلاثة مقاييس في SPSS", "Three measures in SPSS"), k.cards([
        mcard("Nominal", L(k, "وصفي اسمي", "Nominal (qualitative)"),
              L(k, "صفاته غير قابلة للترتيب، أو أرقام لا تُجرى عليها العمليات الحسابية.", "Categories with no order, or numbers used only as labels."),
              [L(k, "النوع: ذكر / أنثى", "Gender: male / female"), L(k, "الحالة الاجتماعية: أعزب / متزوج", "Marital status: single / married"),
               L(k, "رقم الطالب: 101 / 102 / 103", "Student ID: 101 / 102 / 103")]),
        mcard("Ordinal", L(k, "وصفي رتبي", "Ordinal (qualitative)"),
              L(k, "صفاته قابلة للترتيب تصاعديًا أو تنازليًا.", "Categories that can be ranked in ascending or descending order."),
              [L(k, "مستوى المعيشة: منخفض / متوسط / مرتفع", "Living standard: low / medium / high"), L(k, "تقدير الطالب: A / B / C", "Student grade: A / B / C")]),
        mcard("Scale", L(k, "كمي", "Quantitative"),
              L(k, "مقدار عددي تُجرى عليه العمليات الحسابية.", "A numeric amount that arithmetic can be done on."),
              [L(k, "عدد الموظفين", "Number of employees"), L(k, "عدد الأطفال", "Number of children"), L(k, "الطول", "Height"), L(k, "الوزن", "Weight")]),
    ]))

    # 5b decision map: text vs numbers
    def down(color=RULE, w=36, h=44):
        return (f'<div style="display:flex; justify-content:center"><x-shape kind="arrow-down" '
                f'style="background:{color}; width:{w}px; height:{h}px"></x-shape></div>')
    def node(text, bg, fg, size=32, pad="16px 28px", weight=600):
        return (f'<p style="font-size:{size}px; font-weight:{weight}; line-height:1.35; color:{fg}; background:{bg}; '
                f'padding:{pad}; border-radius:999px; text-align:center; align-self:center">{k.t(text)}</p>')
    def result(title, rule, ex, bg, fg, sub):
        return (f'<div style="flex:none; display:flex; flex-direction:column; gap:10px; background:{bg}; border-radius:16px; padding:28px; text-align:center">'
                f'<h3 style="font-family:{DISPLAY}; font-size:38px; font-weight:700; line-height:1.2; color:{fg}; text-align:center">{k.t(title)}</h3>'
                f'<p style="font-size:26px; line-height:1.4; color:{sub}; text-align:center">{k.t(rule)}</p>'
                f'<p style="font-size:26px; line-height:1.4; font-weight:600; color:{fg}; text-align:center">{k.t(ex)}</p></div>')
    root = node(L(k, "ما نوع القيم داخل المتغير؟", "What values does the variable hold?"), INK, PAPER, 34, "18px 40px")
    text_branch = (f'<div style="flex:1; display:flex; flex-direction:column; gap:14px">'
                   + node(L(k, "نص / كلمات", "Text / words"), BLUE_TINT, BLUE)
                   + down(BLUE, 36, 60)
                   + result(L(k, "متغير وصفي", "Qualitative"), L(k, "أي متغير يحتوي على نص فهو متغير وصفي — دائمًا.", "Any variable that holds text is qualitative. Always."),
                            L(k, "مثال: النوع (ذكر / أنثى)", "e.g. Gender (male / female)"), BLUE_TINT, BLUE, INK_SOFT)
                   + '</div>')
    q = (f'<div style="display:flex; flex-direction:column; gap:6px; background:{CARD}; border:2px solid {AMBER}; border-radius:16px; padding:18px 24px; text-align:center">'
         f'<p style="font-size:28px; font-weight:600; line-height:1.35; color:{INK}; text-align:center">{k.t(L(k, "هل للأرقام مقياس، ويمكن إجراء العمليات الحسابية عليها؟", "Do the numbers have a scale, and can we do arithmetic on them?"))}</p></div>')
    yes_no = (f'<div style="display:flex; flex-direction:{k.row}; gap:20px">'
              + f'<div style="flex:1; display:flex; flex-direction:column; gap:10px">{node(L(k, "نعم", "Yes"), AMBER_TINT, AMBER_INK, 26, "6px 22px")}'
              + result(L(k, "متغير كمي", "Quantitative"), L(k, "مقياسه Scale", "Measure: Scale"), L(k, "عدد الأطفال: 0، 1، 2", "Children: 0, 1, 2"), INK, PAPER, MIST) + '</div>'
              + f'<div style="flex:1; display:flex; flex-direction:column; gap:10px">{node(L(k, "لا", "No"), AMBER_TINT, AMBER_INK, 26, "6px 22px")}'
              + result(L(k, "متغير وصفي", "Qualitative"), L(k, "الرقم مجرد رمز أو معرّف", "The number is only a code or an ID"), L(k, "رقم الطالب: 101، 102", "Student ID: 101, 102"), BLUE_TINT, BLUE, INK_SOFT) + '</div>'
              + '</div>')
    num_branch = (f'<div style="flex:1.6; display:flex; flex-direction:column; gap:14px">'
                  + node(L(k, "أرقام", "Numbers"), AMBER_TINT, AMBER_INK) + down(AMBER, 36, 36) + q + yes_no + '</div>')
    k.content("textnum", L(k, "خريطة القرار", "Decision map"), L(k, "وصفي أم كمي؟", "Qualitative or quantitative?"),
              f'<div style="display:flex; flex-direction:column; gap:20px">{root}'
              f'<div style="display:flex; flex-direction:{k.row}; gap:48px; align-items:start">{text_branch}{num_branch}</div></div>',
              gap=28,
              notes=L(k, "النص وحده يكفي للحكم: المتغير وصفي. أما الأرقام فاسأل: هل لها مقياس وهل لمتوسطها معنى؟ إذا نعم فهو كمي، وإذا كانت مجرد رموز (مثل 1 = ذكر أو رقم الطالب) فهو وصفي.",
                      "Text alone settles it: qualitative. For numbers, ask whether they have a scale and whether their average means anything. If yes, quantitative; if they are only codes (1 = male, a student ID), qualitative."))

    # 6 accent statement
    k.statement("idnote", L(k, "انتبه", "Watch out"), L(k, "ليس كل رقم متغيرًا كميًا", "Not every number is quantitative"),
                L(k, "رقم الطالب 101 / 102 / 103 يُستخدم كمعرّف فقط ولا تُجرى عليه العمليات الحسابية؛ لذلك فهو متغير وصفي اسمي (Nominal).",
                  "Student IDs such as 101 / 102 / 103 only identify students. No arithmetic is done on them, so the variable is nominal."),
                notes=L(k, "اسأل: هل لمتوسط أرقام الطلاب أي معنى؟ الإجابة لا، إذن المتغير Nominal.",
                        "Ask: does the average of student IDs mean anything? No, so the variable is nominal."))

    # 7 divider 2
    k.divider("d2", 2, 3, L(k, "برنامج SPSS ونوافذه", "SPSS and its windows"),
              L(k, "ما هو البرنامج، وأين نعرّف المتغيرات وندخل البيانات", "What the program is, and where we define variables and enter data"),
              section=L(k, "برنامج SPSS ونافذة محرر البيانات", "SPSS and the Data Editor"))

    # 8 what is SPSS
    acr = ""
    for letter, word in [("S", "Statistical"), ("P", "Package"), ("S", "Social"), ("S", "Sciences")]:
        acr += (f'<div style="display:flex; flex-direction:row; align-items:baseline; gap:28px">'
                f'<p style="font-family:{DISPLAY}; font-size:96px; font-weight:700; line-height:1; color:{BLUE}; width:80px">{letter}</p>'
                f'<p style="font-family:{DISPLAY}; font-size:48px; font-weight:500; line-height:1.1; color:{INK}">{word}</p></div>')
    acr_block = (f'<div style="width:620px; flex:none; display:flex; flex-direction:column; gap:20px; text-align:left">{acr}'
                 f'<p style="font-size:28px; color:{MUTED}">Statistical Package for the Social Sciences</p></div>')
    right = (f'<div style="flex:1; display:flex; flex-direction:column; gap:28px">'
             + k.h3(L(k, "الحزمة الإحصائية للعلوم الاجتماعية", "Statistical Package for the Social Sciences"), BLUE)
             + k.p(L(k, "برنامج حاسوبي متكامل يُستخدم لإدخال البيانات وإدارتها وتحليلها، وإجراء مجموعة واسعة من الأساليب الإحصائية.",
                     "An integrated computer program used to enter, manage and analyse data, and to run a wide range of statistical methods."), 36, INK)
             + k.tag_row([L(k, "إدخال البيانات", "Enter data"), L(k, "إدارتها", "Manage data"), L(k, "تحليلها", "Analyse data"),
                          L(k, "أساليب إحصائية متعددة", "Statistical methods")]) + "</div>")
    k.content("spss", L(k, "تعريف", "Definition"), L(k, "ما هو برنامج SPSS؟", "What is SPSS?"),
              f'<div style="display:flex; flex-direction:{k.row}; gap:96px; align-items:center">{acr_block}{right}</div>')

    # 9 windows
    w1 = k.card(k.chip("Data Editor Window") + k.h3(L(k, "نافذة محرر البيانات", "Data Editor window")) +
                k.p(L(k, "تعرض البيانات في صورتين:", "Shows the data in two views:")) +
                k.tag_row([L(k, "Data View · عرض البيانات", "Data View"), L(k, "Variable View · عرض المتغيرات", "Variable View")]))
    w2 = k.card(k.chip("Output Viewer Window") + k.h3(L(k, "نافذة عرض المخرجات", "Output Viewer window")) +
                k.p(L(k, "تعرض نتائج تحليل البيانات: الجداول والرسوم التي ينتجها البرنامج.",
                      "Shows the results of the data analysis: the tables and charts SPSS produces.")))
    k.content("windows", L(k, "نوافذ البرنامج", "SPSS windows"), L(k, "نافذتان رئيسيتان للعمل مع البيانات", "Two main windows for working with data"),
              k.cards([w1, w2]))

    # 10 variable view screenshot
    def vcard(h, d):
        return k.card(k.h3(h, size=32) + k.p(d, 28), pad=28, gap=8, flex="none")
    side = (vcard(L(k, "كل صف = متغير", "Row = variable"), L(k, "في كل صف تُدخل خصائص متغير واحد.", "Each row holds one variable's properties.")) +
            vcard(L(k, "كل عمود = خاصية", "Column = property"), L(k, "من Name حتى Role، ونشرحها واحدة واحدة.", "From Name to Role, covered one by one.")) +
            vcard(L(k, "الوصول إليها", "How to open it"), L(k, "من تبويب Variable View أسفل النافذة.", "The Variable View tab, bottom left.")))
    k.shot_slide("vview", "Variable View", L(k, "نافذة عرض المتغيرات", "The Variable View"), im["vv"],
                 L(k, "نافذة Variable View في SPSS مع أسماء الخصائص", "SPSS Variable View with property columns labelled"), 940, 449, side)

    # 11 Name
    rules = [L(k, "لا مسافات بين الأحرف", "No spaces"), L(k, "لا يبدأ برقم", "Cannot start with a number"),
             L(k, "لا ينتهي بنقطة", "Cannot end with a full stop"), L(k, "لا رموز خاصة مثل:", "No special symbols such as:")]
    rule_rows = "".join(
        f'<div style="display:flex; flex-direction:{k.row}; gap:16px; align-items:center">'
        f'<x-icon name="Warning" style="color:{AMBER_INK}; width:40px; height:40px"></x-icon><div style="flex:1">{k.p(r, 32, INK)}</div></div>'
        for r in rules)
    c_rules = k.card(k.h3(L(k, "قواعد التسمية", "Naming rules"), size=40) + rule_rows + k.chip_row(["&amp;", "!", "?", "'", "*"]), flex="1.2")
    c_def = k.card(k.h3(L(k, "الاسم الافتراضي", "Default name"), size=40) +
                   f'<p style="font-family:{MONO}; font-size:56px; font-weight:600; color:{BLUE}; line-height:1.2">VAR00001</p>' +
                   k.p(L(k, "يُعطى تلقائيًا إذا لم يكتب المستخدم اسمًا، ثم VAR00002 للمتغير الثاني، وهكذا.",
                         "Given automatically when no name is typed; the second variable gets VAR00002, and so on."), 30))
    k.content("name", "Name", L(k, "اسم المتغير", "Variable name"),
              k.p(L(k, "الاسم الذي يختاره المستخدم للمتغير، ويمكن كتابته بالعربية أو الإنجليزية.",
                    "The name the user chooses for the variable. It can be written in Arabic or English."), 36, INK) + k.cards([c_rules, c_def]),
              kind="term", gap=40,
              notes=L(k, "أمثلة سريعة للسبورة: gender صحيح، monthly income خطأ (مسافة)، 2income خطأ (يبدأ برقم).",
                      "Quick board examples: gender is valid; monthly income is not (space); 2income is not (starts with a number)."))

    # 12 Type
    opts = (k.card(k.chip("Numeric") + k.p(L(k, "إذا كان المتغير رقميًا — وهو النوع الافتراضي.", "The variable is numeric. This is the default."), 30), pad=28, gap=12, flex="none") +
            k.card(k.chip("String") + k.p(L(k, "إذا كان المتغير نصيًا.", "The variable is text."), 30), pad=28, gap=12, flex="none"))
    side = (k.p(L(k, "انقر النقاط الثلاث في خانة Type فيظهر مربع الحوار Variable Type.",
                  "Click the three dots in the Type cell to open the Variable Type dialog."), 32, INK) +
            k.p(L(k, "يعرض عدة أنواع، ونركّز على نوعين رئيسيين:", "It lists several types; we focus on two:"), 30) + opts)
    k.shot_slide("type", "Type", L(k, "نوع المتغير", "Variable type"), im["type"],
                 L(k, "مربع الحوار Variable Type في SPSS", "The SPSS Variable Type dialog"), 960, 536, side)

    # 13 Width / Decimals / Label
    def pcard(term, name, desc, default=None):
        inner = k.chip(term) + k.h3(name, size=40) + k.p(desc, 30)
        if default:
            inner += '<div style="flex:1"></div>' + k.tag(default, PAPER_ALT, INK)
        return k.card(inner, gap=18)
    k.content("wdl", L(k, "خصائص المتغيرات", "Variable properties"), L(k, "العرض والمنازل العشرية والوصف", "Width, decimals and label"), k.cards([
        pcard("Width", L(k, "عرض المتغير", "Width"),
              L(k, "يحدد عدد الأحرف التي يسمح برنامج SPSS بإدخالها للمتغير.", "Sets how many characters SPSS lets you enter for the variable.")),
        pcard("Decimals", L(k, "المنازل العشرية", "Decimal places"),
              L(k, "عدد الخانات العشرية المرغوبة للأعداد، وتكون عادةً صفرًا للأعداد الصحيحة.", "The number of decimal places shown. Usually 0 for whole numbers."),
              L(k, "الافتراضي: 2", "Default: 2")),
        pcard("Label", L(k, "وصف المتغير", "Label"),
              L(k, "وصف يوضح ما يمثله المتغير؛ يُكتب بالعربية وبمسافات ورموز بلا قيود، ويظهر بدل اسم المتغير في نتائج التحليل.",
                "Describes what the variable stands for. Spaces and symbols are allowed, and it replaces the name in the output."),
              L(k, "الافتراضي: فارغ", "Default: empty")),
    ]))

    # 14 Values
    side = (k.p(L(k, "توضّح الأرقام التي تمثل كل فئة عندما يكون المتغير فئويًا.", "Explains which number stands for each category of a categorical variable."), 32, INK) +
            k.steps([L(k, "انقر النقاط الثلاث في خانة Values ليظهر مربع Value Labels.", "Click the three dots in the Values cell to open Value Labels."),
                     L(k, "في خانة Value اكتب الرقم، وفي خانة Label اكتب اسم الفئة.", "Type the number in Value and the category name in Label."),
                     L(k, "اضغط Add، ثم OK بعد إضافة كل القيم.", "Press Add for each one, then OK.")]) +
            k.tag(L(k, "مثال: 1 = ذكر · 2 = أنثى", "Example: 1 = male · 2 = female"), PAPER, INK))
    k.shot_slide("values", "Values", L(k, "تسميات القيم", "Value labels"), im["values"],
                 L(k, "مربع الحوار Value Labels في SPSS", "The SPSS Value Labels dialog"), 940, 541, side)

    # 15 Missing
    k.content("missing", "Missing", L(k, "القيم المفقودة", "Missing values"),
              k.p(L(k, "تُستخدم لتعريف القيم المفقودة كما يرغب المستخدم، والتمييز بين أسبابها — كما في الاستبيانات:",
                    "Lets you define missing values and tell their causes apart, as in questionnaires:"), 36, INK) +
              k.cards([k.card(k.h3(L(k, "مفقودة فعليًا", "Truly missing"), size=40) +
                              k.p(L(k, "مثل فقد بعض استمارات الاستبيان.", "For example, some questionnaire forms were lost."))),
                       k.card(k.h3(L(k, "عدم الاستجابة", "Non-response"), size=40) +
                              k.p(L(k, "المستجيب لا يرغب في الإجابة عن سؤال معيّن.", "The respondent chose not to answer a question.")))]) +
              k.tag(L(k, "إذا لم توجد قيم مفقودة تظهر الخانة: None", "No missing values defined: the cell shows None"), PAPER_ALT, INK),
              kind="term", gap=40)

    # 16 Columns / Align / Measure
    meas = k.card(k.chip("Measure") + k.h3(L(k, "مقياس المتغير", "Measure"), size=40) +
                  k.tag_row([L(k, "Scale · كمي", "Scale"), L(k, "Ordinal · رتبي", "Ordinal"), L(k, "Nominal · اسمي", "Nominal")]) +
                  k.p(L(k, "إذا لم يحدده المستخدم يظهر Unknown.", "If you don't set it, SPSS shows Unknown."), 30), gap=18)
    k.content("cam", L(k, "خصائص المتغيرات", "Variable properties"), L(k, "عرض العمود والمحاذاة والمقياس", "Columns, alignment and measure"), k.cards([
        pcard("Columns", L(k, "عرض العمود", "Column width"),
              L(k, "المساحة التي تشغلها قيم المتغير داخل العمود؛ خيار شكلي لا يغيّر القيم.", "How wide the column is on screen. It is cosmetic and never changes the values."),
              L(k, "الافتراضي: 8", "Default: 8")),
        pcard("Align", L(k, "محاذاة القيم", "Alignment"),
              L(k, "محاذاة قيم المتغير داخل العمود: Right أو Left أو Center.", "How values sit in the column: Right, Left or Center."),
              L(k, "الافتراضي: Right", "Default: Right")),
        meas,
    ]))

    # 17 Data View
    side = (k.p(L(k, "المكان الذي يتم فيه إدخال البيانات.", "Where the data are entered."), 32, INK) +
            k.card(k.chip("Rows") + k.p(L(k, "تمثل الحالات أو السجلات (Cases).", "Represent the cases (records)."), 30), pad=28, gap=12, flex="none") +
            k.card(k.chip("Columns") + k.p(L(k, "تمثل المتغيرات (Variables).", "Represent the variables."), 30), pad=28, gap=12, flex="none"))
    k.shot_slide("dview", "Data View", L(k, "نافذة عرض البيانات", "The Data View"), im["dv"],
                 L(k, "نافذة Data View في SPSS", "SPSS Data View with rows and columns labelled"), 1040, 541, side)

    # 18 divider 3
    k.divider("d3", 3, 3, L(k, "تمارين تطبيقية", "Hands-on exercises"),
              L(k, "حدّد نوع كل متغير ومقياسه، ثم أدخل البيانات في SPSS", "Identify each variable's type and measure, then enter the data in SPSS"),
              section=L(k, "التمارين التطبيقية", "Exercises"))

    # exercises ---------------------------------------------------------------
    Q = L(k, "متغير {v} عبارة عن متغير ........ ومقياسه ........", "The variable {v} is a ........ variable, and its measure is ........")
    def qv(v):
        return v if k.ar or v.startswith("ID") else v[0].lower() + v[1:]
    Q = type("Q", (), {"format": staticmethod(lambda v, _q=Q: _q.format(v=qv(v)))})
    QUAL, QUANT = L(k, "وصفي", "Qualitative"), L(k, "كمي", "Quantitative")
    def o(t, m):
        return f"{t}، {m}" if k.ar else f"{t}, {m}"

    def exercise(n, data_title, data_desc, header, rows, widths, center, qs, answers, qsplit=None, tsize=28):
        req = k.card(k.h3(L(k, "المطلوب", "Your task"), AMBER_INK, 36) +
                     k.steps([L(k, "حدّد نوع كل متغير ومقياسه.", "Identify each variable's type and measure."),
                              L(k, "أدخل البيانات في SPSS.", "Enter the data in SPSS."),
                              L(k, "خذ لقطتي شاشة: Variable View و Data View.", "Take two screenshots: Variable View and Data View.")], 28),
                     bg=AMBER_TINT, border=False, flex="none", pad=36, gap=20, width=480)
        k.content(f"ex{n}data", L(k, f"تمرين {n}", f"Exercise {n}"), data_title,
                  k.p(data_desc, 32) +
                  f'<div style="display:flex; flex-direction:{k.row}; gap:48px; align-items:start">'
                  f'<div style="flex:1">{k.table(header, rows, widths, tsize, 1136, center)}</div>{req}</div>',
                  kind="practice", gap=36,
                  section=L(k, f"تمرين {n}", f"Exercise {n}"))
        parts = qsplit or [len(qs)]
        start = 0
        for pi, cnt in enumerate(parts):
            suffix = "" if len(parts) == 1 else f"-{pi + 1}"
            notes = " | ".join(f"{start + i + 1}: {answers[start + i][3]}" for i in range(cnt))
            k.mcq(f"ex{n}q{suffix}", L(k, f"تمرين {n} · الأسئلة", f"Exercise {n} · Questions"),
                  L(k, "حدّد نوع المتغير ومقياسه", "Identify the type and the measure"), qs[start:start + cnt], start + 1,
                  notes=L(k, "الإجابات: ", "Answers: ") + notes)
            start += cnt
        ans_rows = [[a[0], a[1], a[2], a[3]] for a in answers]
        task = k.card(k.h3(L(k, "تطبيق عملي على SPSS", "Now in SPSS"), AMBER_INK, 36) +
                      k.steps([L(k, "أدخل خصائص المتغيرات في Variable View، ثم خذ لقطة شاشة واضحة.", "Define the variables in Variable View, then take a clear screenshot."),
                               L(k, "أدخل البيانات في Data View، ثم خذ لقطة شاشة واضحة.", "Enter the data in Data View, then take a clear screenshot.")], 28),
                      bg=AMBER_TINT, border=False, flex="none", pad=36, gap=20, width=560)
        k.content(f"ex{n}ans", L(k, f"تمرين {n} · الحل", f"Exercise {n} · Answers"), L(k, "الإجابات والتطبيق العملي", "Answers and SPSS practice"),
                  f'<div style="display:flex; flex-direction:{k.row}; gap:48px; align-items:start">'
                  f'<div style="flex:1">{k.table([L(k, "المتغير", "Variable"), L(k, "النوع", "Type"), L(k, "المقياس", "Measure"), L(k, "الاختيار", "Answer")], ans_rows, [34, 22, 26, 18], 28, 1056, (3,))}</div>{task}</div>',
                  kind="practice")

    G = L(k, "النوع", "Gender")
    M, F_ = L(k, "ذكر", "Male"), L(k, "أنثى", "Female")
    S, NS = L(k, "مدخن", "Smoker"), L(k, "غير مدخن", "Non-smoker")
    exercise(1, L(k, "بيانات 7 موظفين", "Data on 7 employees"),
             L(k, "بيانات 7 موظفين في إحدى الشركات: النوع، عدد الأطفال، الدخل الشهري، وحالة التدخين.",
               "Data on 7 employees at a company: gender, number of children, monthly income and smoking status."),
             [L(k, "رقم الموظف", "Employee"), G, L(k, "عدد الأطفال", "Children"), L(k, "الدخل الشهري", "Monthly income"), L(k, "التدخين", "Smoking")],
             [[1, M, 2, 5000, S], [2, F_, 1, 4500, NS], [3, M, 3, 6500, NS], [4, F_, 2, 5500, S], [5, M, 0, 4000, NS], [6, F_, 3, 7000, NS], [7, M, 2, 6000, S]],
             [16, 18, 18, 24, 24], (0, 2, 3),
             [(Q.format(v=G), [o(QUAL, "Nominal"), o(QUAL, "Ordinal"), o(QUANT, "Scale"), o(QUANT, "Ordinal")]),
              (Q.format(v=L(k, "عدد الأطفال", "number of children")), [o(QUAL, "Nominal"), o(QUANT, "Scale"), o(QUAL, "Ordinal"), o(QUANT, "Nominal")]),
              (Q.format(v=L(k, "الدخل الشهري", "monthly income")), [o(QUAL, "Ordinal"), o(QUAL, "Nominal"), o(QUANT, "Scale"), o(QUANT, "Nominal")]),
              (Q.format(v=L(k, "التدخين", "smoking")), [o(QUANT, "Scale"), o(QUAL, "Ordinal"), o(QUAL, "Nominal"), o(QUANT, "Nominal")])],
             [(G, QUAL, "Nominal", "a"), (L(k, "عدد الأطفال", "Children"), QUANT, "Scale", "b"),
              (L(k, "الدخل الشهري", "Monthly income"), QUANT, "Scale", "c"), (L(k, "التدخين", "Smoking"), QUAL, "Nominal", "c")])

    DEP = L(k, "القسم", "Department")
    ADM, ACC, MKT = L(k, "إدارة", "Management"), L(k, "محاسبة", "Accounting"), L(k, "تسويق", "Marketing")
    SP = L(k, "المصروف الشهري", "Monthly allowance")
    exercise(2, L(k, "بيانات 7 طلاب", "Data on 7 students"),
             L(k, "بيانات 7 طلاب في إحدى الكليات: رقم الطالب (ID)، النوع، القسم، والمصروف الشهري.",
               "Data on 7 students at a college: student ID, gender, department and monthly allowance."),
             [L(k, "رقم الطالب (ID)", "Student ID"), G, DEP, SP],
             [[1, M, ADM, 2500], [2, F_, ACC, 3000], [3, M, MKT, 2800], [4, F_, ADM, 3500], [5, M, ACC, 2200], [6, F_, MKT, 3200], [7, M, ADM, 2700]],
             [22, 22, 28, 28], (0, 3),
             [(Q.format(v="ID"), [o(QUANT, "Scale"), o(QUAL, "Nominal"), o(QUANT, "Ordinal"), o(QUAL, "Ordinal")]),
              (Q.format(v=G), [o(QUANT, "Scale"), o(QUAL, "Nominal"), o(QUAL, "Ordinal"), o(QUANT, "Nominal")]),
              (Q.format(v=DEP), [o(QUANT, "Scale"), o(QUAL, "Ordinal"), o(QUAL, "Nominal"), o(QUANT, "Nominal")]),
              (Q.format(v=SP), [o(QUAL, "Nominal"), o(QUAL, "Ordinal"), o(QUANT, "Scale"), o(QUANT, "Nominal")])],
             [("ID", QUAL, "Nominal", "b"), (G, QUAL, "Nominal", "b"), (DEP, QUAL, "Nominal", "c"), (SP, QUANT, "Scale", "c")])

    MAJ = L(k, "التخصص", "Major")
    SCI, ART, COM = L(k, "علوم", "Science"), L(k, "آداب", "Arts"), L(k, "تجارة", "Commerce")
    HRS = L(k, "عدد ساعات الدراسة أسبوعيًا", "Weekly study hours")
    ACH = L(k, "مستوى التحصيل الدراسي", "Achievement level")
    MID, LOW, HIGH = L(k, "متوسط", "Medium"), L(k, "منخفض", "Low"), L(k, "مرتفع", "High")
    exercise(3, L(k, "التحصيل الدراسي لـ 7 طلاب", "Achievement of 7 students"),
             L(k, "رقم الطالب (ID)، التخصص، عدد ساعات الدراسة أسبوعيًا، المصروف الشهري، ومستوى التحصيل الدراسي.",
               "Student ID, major, weekly study hours, monthly allowance and achievement level."),
             [L(k, "رقم الطالب (ID)", "ID"), MAJ, L(k, "ساعات الدراسة", "Study hours"), SP, L(k, "مستوى التحصيل", "Achievement")],
             [[1, SCI, 12, 2000, MID], [2, ART, 8, 2500, LOW], [3, COM, 15, 3000, HIGH], [4, SCI, 18, 2200, HIGH], [5, ART, 10, 2800, MID], [6, COM, 14, 3500, HIGH], [7, SCI, 9, 1800, MID]],
             [14, 18, 22, 22, 24], (0, 2, 3),
             [(Q.format(v=L(k, "رقم الطالب (ID)", "student ID")), [o(QUANT, "Scale"), o(QUAL, "Nominal"), o(QUANT, "Ordinal"), o(QUAL, "Ordinal")]),
              (Q.format(v=MAJ), [o(QUANT, "Scale"), o(QUAL, "Ordinal"), o(QUAL, "Nominal"), o(QUANT, "Nominal")]),
              (Q.format(v=L(k, "عدد ساعات الدراسة أسبوعيًا", "weekly study hours")), [o(QUAL, "Nominal"), o(QUANT, "Scale"), o(QUAL, "Ordinal"), o(QUANT, "Nominal")]),
              (Q.format(v=SP), [o(QUAL, "Nominal"), o(QUAL, "Ordinal"), o(QUANT, "Scale"), o(QUANT, "Nominal")]),
              (Q.format(v=ACH), [o(QUANT, "Scale"), o(QUAL, "Nominal"), o(QUAL, "Ordinal"), o(QUANT, "Nominal")])],
             [("ID", QUAL, "Nominal", "b"), (MAJ, QUAL, "Nominal", "c"), (HRS, QUANT, "Scale", "b"), (SP, QUANT, "Scale", "c"), (ACH, QUAL, "Ordinal", "c")],
             qsplit=[3, 2], tsize=26)

    # closing
    def sc(n, h, d):
        return k.card(k.num_badge(n, 56, AMBER, INK, 28).replace("flex:none;", f"flex:none; align-self:{k.self_start};", 1) +
                      k.h3(h, PAPER, 40) + k.p(d, 30, MIST), bg=INK_LINE, border=False, gap=20)
    k.add("summary", k.head(L(k, "الخلاصة", "Wrap-up"), L(k, "ما الذي يجب أن تتذكره؟", "What to remember"), "practice", dark=True) + k.cards([
        sc(1, L(k, "المتغير", "Variables"), L(k, "وصفي (Nominal أو Ordinal) أو كمي (Scale). الأرقام التعريفية مثل ID متغيرات اسمية.",
                                               "Qualitative (Nominal or Ordinal) or quantitative (Scale). ID numbers are nominal.")),
        sc(2, L(k, "برنامج SPSS", "SPSS"), L(k, "نافذة محرر البيانات لإدخال البيانات، ونافذة عرض المخرجات للنتائج.",
                                              "The Data Editor holds the data; the Output Viewer shows the results.")),
        sc(3, L(k, "محرر البيانات", "Data Editor"), L(k, "Variable View لتعريف خصائص المتغيرات، وData View لإدخال البيانات: الصفوف حالات والأعمدة متغيرات.",
                                                     "Variable View defines the properties; Data View holds the data. Rows are cases, columns are variables.")),
    ]), bg=INK, dark=True, section=L(k, "الخلاصة", "Wrap-up"))

    title = L(k, "سكشن 1 — مقدمة في SPSS", "Section 1 — Introduction to SPSS")
    return k.write(title, ds_record)


if __name__ == "__main__":
    lang, root = sys.argv[1], sys.argv[2]
    rec = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
    d = build(lang, root, rec)
    print(lang, len(d["order"]), "slides")
