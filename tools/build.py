#!/usr/bin/env python3
"""يولّد موقع Mind الثابت (عربي + إنجليزي) في المجلد الرئيسي. التشغيل: python3 tools/build.py
النصوص القانونية بتتنسخ من assets/legal (نسخة من مشروع التطبيق) وبتتحول HTML."""
import markdown, os, shutil, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_LEGAL = os.path.join(ROOT, "legal")

T = {
"ar": dict(dir="rtl", lang="ar", prefix="", other="/en/", other_label="English", home="/",
  title="Mind — إدارة السناتر والدروس الخصوصية في تطبيق واحد",
  desc="تطبيق Mind لإدارة السناتر ومراكز التدريب والمدرس الفردي: حضور بالـ QR والباركود، فواتير ومدفوعات، امتحانات ودرجات، وتقارير لولي الأمر.",
  nav=[("#features","المميزات"),("#faq","الأسئلة الشائعة")],
  h1="إدارة السنتر كلها في تطبيق واحد",
  sub="حضور بالـ QR والباركود، فواتير ومدفوعات، امتحانات ودرجات، وتقارير لولي الأمر. من غير ورق ومن غير لخبطة.",
  cta1="شوف المميزات", cta2="",
  who_h="مين بيستفيد؟",
  who=[("السناتر ومراكز التدريب","تنظيم المجموعات والمواعيد والقاعات والفريق في مكان واحد."),
       ("المدرس الفردي","نفس الأدوات من غير تعقيد وبسعر أقل."),
       ("ولي الأمر","يتابع حضور ابنه ودرجاته ومصروفاته ويستلم الإشعارات.")],
  feat_h="المميزات",
  feats=[("حضور بالـ QR","المدرس يعرض كود الحصة والطالب أو ولي الأمر يمسحه. الموقع بيتقارن بنطاق السنتر لحظة التسجيل بس ومابيتخزنش."),
         ("حضور بكارت الباركود","كارت لكل طالب والمدرس يمسحه بالكاميرا، حتى لو الطالب معهوش موبايل."),
         ("الفواتير والمدفوعات","فواتير شهرية وأقساط وإيصالات بأرقام متسلسلة وخصومات. الفلوس بتتدفع للسنتر مباشرة والتطبيق بيسجّلها."),
         ("رسائل واتساب جاهزة","رسالة غياب أو تأخير أو تذكير بالمصروفات تفتح في واتساب بضغطة، وتراجعها قبل الإرسال."),
         ("امتحانات ودرجات وشهادات","شهادات إتمام يقدر أي حد يتحقق منها بالكود."),
         ("جداول وقاعات وإجازات","تغيير المواعيد والتعويض والإجازات وإشعار فوري للطلاب وأولياء الأمور."),
         ("تقارير ورسوم بيانية","حضور وإيرادات وطلاب جدد ومتوسط الدرجات."),
         ("واجبات وإعلانات ومواد","المدرس ينشر واجب أو مادة (برابط) أو إعلان لمجموعة أو للسنتر، ويتابع مين قرأ ومين سلّم."),
         ("نقاط وشارات","تحفيز الطلاب بنقاط وشارات، وولي الأمر يشوف تقدم ابنه بس."),
         ("حجز مواعيد مع المدرس","المدرس يفتح مواعيد وولي الأمر يحجز ويلغي بسهولة."),
         ("مصروفات وأرباح السنتر","سجّل مصروفات السنتر وشوف الربح الشهري بوضوح."),
         ("صلاحيات للفريق","مدرس ومساعد واستقبال ومحاسب، وكل واحد يشوف اللي يخصه بس."),
         ("عربي وإنجليزي","والتطبيق بيفتح باللغة اللي تختارها.")],
  priv_h="الخصوصية",
  priv=["بياناتك مابتتباعش ومابنستخدمها في استهداف إعلاني.","مفيش تتبع للموقع: بيتقارن بنطاق السنتر لحظة الحضور فقط.","الطفل أقل من 18 سنة بيتفعّل حسابه بموافقة ولي أمره، وولي الأمر يقدر يسحبها في أي وقت."],
  plans_h="الباقات والأسعار",
  plans_intro="ثلاث باقات للسنتر وثلاث للمدرس الفردي، وكل باقة فيها اللي قبلها. الأسعار بالجنيه المصري في الشهر، والاشتراك السنوي بسعر 10 شهور (شهرين مجانًا). الأسعار قابلة للتغيير بإشعار مسبق 30 يومًا على الأقل.",
  th_center=["الباقة","شهريًا","سنويًا","الطلاب","المدرسون","اللي فيها"],
  center=[("اقتصادية","149","1490","حتى 100","حتى 2","الحضور والانصراف، الحضور بالـ QR والباركود، الفواتير والمدفوعات، رسائل واتساب، الإجازات والتعويض وتغيير المواعيد، إعلانات السنتر والمجموعات"),
          ("أساسية","299","2990","حتى 400","حتى 10","كل اللي في الاقتصادية + الشات، الامتحانات والدرجات والشهادات، الواجبات والمواد، النقاط والشارات للطلاب، حجز مواعيد مع المدرس، المصروفات وأرباح السنتر، قاعات متعددة، الخصومات، تقارير بسيطة"),
          ("احترافية","549","5490","بلا حد","بلا حد","كل اللي في الأساسية + صلاحيات مخصصة للفريق، تسويات المدرسين، تقارير كاملة وتصدير المصروفات CSV، بدون إعلانات")],
  solo_h="للمدرس الفردي", th_solo=["الباقة","شهريًا","سنويًا","الطلاب"],
  solo=[("اقتصادية","99","990","حتى 50"),("أساسية","199","1990","حتى 300"),("احترافية","349","3490","بلا حد")],
  solo_note="مميزات كل باقة للمدرس الفردي هي نفس مميزات باقة السنتر المقابلة.",
  parent_h="لولي الأمر",
  parent=["50 جنيه في الشهر أو 500 جنيه في السنة، لكل طفل في كل سنتر.","الشهر الأول مجاني من أول تسجيل للطفل في السنتر.","لو السنتر على الباقة الاقتصادية فولي الأمر مجاني (متابعة الحضور والمدفوعات).","لو الاشتراك انتهى: بيانات الطفل والفواتير والمدفوعات بتفضل محفوظة، ومتابعة الحصص والدرجات والحضور والشهادات بتتوقف لحد التجديد."],
  trial="كل سنتر جديد بيبدأ بفترة تجربة مجانية بكل مميزات الباقة الاحترافية.",
  pay="الدفع: اشتراكات المنصة بتتدفع بوسائل الدفع الإلكتروني المتاحة في مصر عبر مزود دفع مرخّص، وبالتحويل في المرحلة الأولى. بنوضّح كل الرسوم قبل الدفع، وبتوصلك رسالة بتأكيد الاشتراك.",
  faq_h="الأسئلة الشائعة",
  faq=[("هل التطبيق بياخد مدفوعات الطلاب أونلاين؟","فلوس الطلاب بتتدفع للسنتر مباشرة، والتطبيق بيسجّل المدفوعات ويطلّع الإيصالات. مابنستلمش ولا بنحفظ بيانات بطاقات الدفع."),
       ("مين يقدر يشوف بيانات الطلاب؟","السنتر والمدرس يشوفوا طلابهم هم بس، وولي الأمر يشوف أبناءه بس، ومفيش سنتر يشوف بيانات سنتر تاني."),
       ("هل التطبيق بيتتبع موقعي؟","لا. الموقع بيتقارن بنطاق السنتر لحظة تسجيل الحضور فقط ومابيتخزنش."),
       ("هل بتبيعوا بياناتنا؟","لا. مابنبيع ولا بنؤجّر البيانات ولا بنستخدمها في الاستهداف الإعلاني."),
       ("هل الطفل محتاج حساب؟","الطفل أقل من 18 سنة بيتفعّل حسابه بموافقة ولي أمره، وولي الأمر يقدر يسحب الموافقة في أي وقت."),
       ("لو الاشتراك خلص هيحصل إيه في بياناتي؟","بياناتك بتفضل محفوظة، والخدمات بترجع بعد التجديد. وعند إغلاق الحساب بتتاح البيانات للتصدير 30 يومًا.")],
  contact_h="تواصل معنا",
  contact="للدعم والاستفسارات والاشتراكات وطلبات حذف أو تصحيح البيانات:",
  op="Mind مشروع يملكه ويديره شخص طبيعي في جمهورية مصر العربية.",
  foot=[("/privacy/","سياسة الخصوصية"),("/terms/","شروط الاستخدام"),("/delete-account/","حذف الحساب"),("/center-agreement/","اتفاقية السنتر")],
  legal_src="", ),
"en": dict(dir="ltr", lang="en", prefix="/en", other="/", other_label="العربية", home="/en/",
  title="Mind — run your center and private lessons in one app",
  desc="Mind helps tutoring centers, training centers and solo teachers manage attendance by QR and barcode, invoices and payments, exams and grades, and parent updates.",
  nav=[("#features","Features"),("#faq","FAQ")],
  h1="Run your whole center from one app",
  sub="QR and barcode attendance, invoices and payments, exams and grades, and updates for parents. No paper, no chaos.",
  cta1="See features", cta2="",
  who_h="Who is it for?",
  who=[("Centers and training centers","Groups, schedules, rooms and staff in one place."),
       ("Solo teachers","The same tools, simpler and cheaper."),
       ("Parents","Follow attendance, grades and fees, and get notifications.")],
  feat_h="Features",
  feats=[("QR attendance","The teacher shows the session code, the student or parent scans it. Location is compared to the center area at check-in only and never stored."),
         ("Barcode card attendance","A card per student that the teacher scans with the camera, even if the student has no phone."),
         ("Invoices and payments","Monthly invoices, installments, numbered receipts and discounts. Fees are paid to the center directly and the app records them."),
         ("Ready WhatsApp messages","Absence, late or fee reminders open in WhatsApp in one tap, and you review them before sending."),
         ("Exams, grades and certificates","Completion certificates anyone can verify with a code."),
         ("Schedules, rooms and holidays","Schedule changes, make-ups and holidays with instant notifications."),
         ("Reports and charts","Attendance, revenue, new students and average grades."),
         ("Homework, announcements and materials","Teachers post homework, materials (as links) or announcements to a group or the whole center, and see who read and who submitted."),
         ("Points and badges","Motivate students with points and badges; a parent only sees their own child's progress."),
         ("Teacher appointment booking","Teachers open slots; parents book and cancel easily."),
         ("Center expenses and profit","Record expenses and see monthly profit clearly."),
         ("Staff permissions","Teacher, assistant, reception and accountant, each sees only what they need."),
         ("Arabic and English","The app opens in the language you choose.")],
  priv_h="Privacy",
  priv=["We do not sell your data or use it for advertising targeting.","No location tracking: location is compared to the center area at check-in only.","A child under 18 is activated with a parent's consent, which the parent can withdraw at any time."],
  plans_h="Plans and pricing",
  plans_intro="Three plans for centers and three for solo teachers; each includes everything in the plan before it. Prices are in Egyptian pounds per month; yearly billing costs 10 months (two free). Prices may change with at least 30 days' notice.",
  th_center=["Plan","Monthly","Yearly","Students","Teachers","What is included"],
  center=[("Lite","149","1,490","up to 100","up to 2","Attendance, QR and barcode check-in, invoices and payments, WhatsApp messages, holidays, make-ups and schedule changes, center and group announcements"),
          ("Basic","299","2,990","up to 400","up to 10","Everything in Lite, plus chat, exams, grades and certificates, homework and materials, student points and badges, teacher appointment booking, expenses and profit, multiple rooms, discounts, basic reports"),
          ("Pro","549","5,490","unlimited","unlimited","Everything in Basic, plus custom staff permissions, teacher settlements, full reports with expenses CSV export, no ads")],
  solo_h="Solo teachers", th_solo=["Plan","Monthly","Yearly","Students"],
  solo=[("Lite","99","990","up to 50"),("Basic","199","1,990","up to 300"),("Pro","349","3,490","unlimited")],
  solo_note="Solo plans include the same features as the matching center plan.",
  parent_h="Parents",
  parent=["EGP 50 per month or EGP 500 per year, per child per center.","The first month is free from the child's first enrollment at the center.","If the center is on Lite, parents use the app for free (attendance and payments).","If the subscription ends, the child's data, invoices and payments stay, but sessions, grades, attendance and certificates pause until renewal."],
  trial="Every new center starts with a free trial that includes all Pro features.",
  pay="Payment: Mind subscriptions are paid with the online payment methods available in Egypt through a licensed payment provider, and by bank transfer in the first phase. All fees are shown before you pay, and you receive a confirmation of your subscription.",
  faq_h="FAQ",
  faq=[("Does the app take student payments online?","Fees are paid to the center directly. The app records payments and issues receipts. We never receive or store card details."),
       ("Who can see student data?","Centers and teachers see their own students only, parents see their own children only, and no center sees another center's data."),
       ("Does the app track my location?","No. Location is compared to the center area at check-in only and is not stored."),
       ("Do you sell our data?","No. We do not sell or rent data and we do not use it for advertising targeting."),
       ("Does a child need an account?","A child under 18 is activated only with a parent's consent, which the parent can withdraw at any time."),
       ("What happens to my data if the subscription ends?","Your data stays saved and the services return after renewal. If an account is closed, data stays available for export for 30 days.")],
  contact_h="Contact",
  contact="For support, questions, subscriptions, and requests to delete or correct data:",
  op="Mind is a project owned and run by an individual in the Arab Republic of Egypt.",
  foot=[("/en/privacy/","Privacy Policy"),("/en/terms/","Terms of Use"),("/en/delete-account/","Delete your account"),("/en/center-agreement/","Center agreement")],
  ),
}

DELETE = {
"ar": ("حذف الحساب", """
يمكنك حذف حسابك وبياناتك في أي وقت.

## من داخل التطبيق

افتح **الإعدادات** ثم **حذف الحساب** وأكّد. تُمسح بياناتك الشخصية، ويبقى سجل الموافقات والسجلات المالية والضريبية التي يوجب القانون الاحتفاظ بها (دون اسم حيثما أمكن).

## بدون التطبيق

لو مش قادر تدخل التطبيق، هتتوفر وسيلة تواصل رسمية هنا قريبًا. الطريقة الأساسية والأسرع هي الحذف من داخل التطبيق كما فوق.

## ملاحظات

- بيانات الطالب التي أدخلها السنتر يقرر السنتر حذفها أو تعديلها، ونساعده في ذلك. وجّه الطلب للسنتر أو لنا ونحوّله له.
- حذف حساب مدير سنتر قد يحذف بيانات السنتر كلها، ولذلك نراجع الطلب معه أولًا.
- حذف حساب ولي الأمر أو سحب موافقته قد يوقف حساب الطفل.
- تفاصيل مدد الاحتفاظ في [سياسة الخصوصية](/privacy/).
"""),
"en": ("Delete your account", """
You can delete your account and data at any time.

## From inside the app

Open **Settings**, then **Delete account**, and confirm. Your personal data is erased, while the consent record and the financial and tax records that the law requires us to keep remain (without a name where possible).

## Without the app

If you cannot open the app, an official contact channel will be listed here soon. The main and fastest way is deleting from inside the app, as described above.

## Notes

- Student data entered by a center is decided by that center (to delete or correct), and we help it do so. Send the request to the center or to us and we will forward it.
- Deleting a center admin account may delete all of the center's data, so we review that request with them first.
- Deleting a parent account or withdrawing consent may suspend the child's account.
- Retention periods are in the [Privacy Policy](/en/privacy/).
"""),
}

def page(lang, path, title, body, desc=None, with_home=False):
    t = T[lang]
    url_other = t["other"] if path == "" else (("/en/" if lang == "ar" else "/") + path + "/")
    nav = "".join(f'<a href="{t["home"]}{h}">{html.escape(l)}</a>' for h, l in t["nav"])
    foot = "".join(f'<a href="{h}">{html.escape(l)}</a>' for h, l in t["foot"])
    d = html.escape(desc or t["desc"])
    return f"""<!doctype html>
<html lang="{t['lang']}" dir="{t['dir']}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{d}">
<link rel="icon" href="/assets/favicon.png"><link rel="stylesheet" href="/assets/style.css">
<link rel="alternate" hreflang="{'en' if lang=='ar' else 'ar'}" href="https://mind-egypt.com{url_other}">
</head><body>
<header><div class="wrap"><a href="{t['home']}"><img src="/assets/logo.webp" alt="Mind"></a>
<nav>{nav}<a class="lang" href="{url_other}">{t['other_label']}</a></nav></div></header>
{body}
<footer><div class="wrap"><div>{html.escape(t['op'])}<br>© 2026 Mind</div><div>{foot}</div></div></footer>
</body></html>"""

def home_body(lang):
    t = T[lang]
    e = html.escape
    who = "".join(f'<div class="card"><b>{e(a)}</b>{e(b)}</div>' for a, b in t["who"])
    feats = "".join(f'<div class="card"><b>{e(a)}</b>{e(b)}</div>' for a, b in t["feats"])
    def table(head, rows):
        return "<table><tr>" + "".join(f"<th>{e(h)}</th>" for h in head) + "</tr>" + "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>" for r in rows) + "</table>"
    plans = table(t["th_center"], t["center"]) + f"<h3>{e(t['solo_h'])}</h3>" + table(t["th_solo"], t["solo"]) + f'<p class="note">{e(t["solo_note"])}</p>'
    parent = "<ul>" + "".join(f"<li>{e(x)}</li>" for x in t["parent"]) + "</ul>"
    priv = "<ul>" + "".join(f"<li>{e(x)}</li>" for x in t["priv"]) + "</ul>"
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in t["faq"])
    return f"""<main>
<div class="wrap"><div class="hero"><h1>{e(t['h1'])}</h1><p>{e(t['sub'])}</p>
<a class="btn" href="#features">{e(t['cta1'])}</a></div></div>
<section><div class="wrap"><h2>{e(t['who_h'])}</h2><div class="grid">{who}</div></div></section>
<section id="features"><div class="wrap"><h2>{e(t['feat_h'])}</h2><div class="grid">{feats}</div>
<h3>{e(t['priv_h'])}</h3>{priv}</div></section>
<section id="faq"><div class="wrap"><h2>{e(t['faq_h'])}</h2>{faq}</div></section>
</main>"""

def md_body(text):
    h = markdown.markdown(text, extensions=["tables"])
    return f'<main><div class="wrap"><article>{h}</article></div></main>'

def write(rel, content):
    p = os.path.join(ROOT, rel, "index.html")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(content)

def legal(lang, name):
    p = os.path.join(SRC_LEGAL, "en" if lang == "en" else "", name + ".md")
    return open(p, encoding="utf-8").read()

for lang in ("ar", "en"):
    t = T[lang]; pre = t["prefix"].strip("/")
    write(pre, page(lang, "", t["title"], home_body(lang)))
    for slug, name, ttl in (("privacy", "privacy", None), ("terms", "terms", None), ("center-agreement", "center_agreement", None)):
        txt = legal(lang, name)
        title = txt.splitlines()[0].lstrip("# ").strip()
        write(os.path.join(pre, slug), page(lang, slug, title + " — Mind", md_body(txt)))
    ttl, txt = DELETE[lang]
    write(os.path.join(pre, "delete-account"), page(lang, "delete-account", ttl + " — Mind", md_body(f"# {ttl}\n" + txt)))

open(os.path.join(ROOT, "CNAME"), "w").write("mind-egypt.com\n")
open(os.path.join(ROOT, "robots.txt"), "w").write("User-agent: *\nAllow: /\nSitemap: https://mind-egypt.com/sitemap.xml\n")
urls = ["/", "/en/"] + [f"{p}/{s}/" for p in ("", "/en") for s in ("privacy", "terms", "center-agreement", "delete-account")]
open(os.path.join(ROOT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>https://mind-egypt.com{u}</loc></url>\n" for u in urls) + "</urlset>\n")
open(os.path.join(ROOT, ".nojekyll"), "w").write("")
print("built", len(urls), "pages")
