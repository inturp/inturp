#!/usr/bin/env python3
"""Builds the CheckBook pages: /checkbook/, /checkbook/privacy/, /checkbook/delete-account/ (stdlib + Pillow for the share image).

  python3 website-source/showcase/build_checkbook.py
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import shared  # noqa: E402

SITE_DIR = pathlib.Path(__file__).resolve().parents[2]
ROOT = SITE_DIR / 'checkbook'
AR_ROOT = SITE_DIR / 'ar' / 'checkbook'
PLAY = 'https://play.google.com/store/apps/details?id=com.h1apps.h1checkbook'
APPLE = 'https://apps.apple.com/us/app/h1-checkbook/id6758664380'
UPDATED = '2026-10-12'
V = '20261031'
ORIGIN = 'https://inturp.com'
CSS = f'/checkbook/assets/css/site.css?v={V}'
JS = f'/checkbook/assets/js/site.js?v={V}'

LINKS = {  # internal links that exist in both languages
    '/checkbook/privacy/': '/ar/checkbook/privacy/',
    '/checkbook/delete-account/': '/ar/checkbook/delete-account/',
    '/checkbook/': '/ar/checkbook/',
}


def bi(ar, en):
    return f'<span class="ar">{ar}</span><span class="en">{en}</span>'


def localize(html):
    """Give every internal link its Arabic twin so single() can pick the right one."""
    for en, ar in LINKS.items():
        html = html.replace(f'href="{en}"', f'href="{en}" data-ar-href="{ar}" data-en-href="{en}" data-attrs="href"')
    return html


def emit(rel, title, desc, body_dual, ld_fn=None, extra_end=''):
    """Write /checkbook/<rel> (English) and /ar/checkbook/<rel> (Arabic) from one bilingual body."""
    for lang in ('en', 'ar'):
        en_path = '/checkbook/' + rel
        ar_path = '/ar/checkbook/' + rel
        ld = ('<script type="application/ld+json">' + json.dumps(ld_fn(lang), ensure_ascii=False) + '</script>\n') if ld_fn else ''
        html = shared.head(lang=lang, title=title[lang], desc=desc[lang], en_path=en_path, ar_path=ar_path, css=CSS,
                           og_image='/checkbook/assets/img/og.jpg', og_alt='CheckBook app screens' if lang == 'en' else 'شاشات تطبيق CheckBook', extra=ld)
        html += chrome_head() + body_dual + chrome_foot() + extra_end + '\n</body>\n</html>\n'
        html = shared.single(localize(html), lang)
        out = (ROOT if lang == 'en' else AR_ROOT) / rel / 'index.html'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding='utf-8')


def chrome_head():
    return shared.header('checkbook')


def chrome_foot():
    return shared.footer('checkbook', ('/checkbook/privacy/', '/ar/checkbook/privacy/'), ('/checkbook/delete-account/', '/ar/checkbook/delete-account/'),
                         'خصوصية CheckBook', 'CheckBook privacy') + f'\n<script src="{JS}"></script>'


PLAY_SVG = '<svg class="st" viewBox="0 0 24 24" aria-hidden="true"><path d="M4.2 2.6c-.3.2-.5.6-.5 1.1v16.6c0 .5.2.9.5 1.1l9.3-9.4zM14.8 13.2l2.7 2.7-11.4 6.5zM14.8 10.8 6.1 1.6l11.4 6.5zM18.6 9.3l2.8 1.6c.8.5.8 1.7 0 2.2l-2.8 1.6-3-3z"/></svg>'
APPLE_SVG = '<svg class="st" viewBox="0 0 24 24" aria-hidden="true"><path d="M16.4 12.7c0-2.5 2-3.6 2.1-3.7-1.2-1.7-3-1.9-3.6-1.9-1.5-.2-3 .9-3.8.9-.8 0-2-.9-3.3-.9-1.7 0-3.3 1-4.1 2.5-1.8 3.1-.5 7.6 1.3 10.1.9 1.2 1.9 2.6 3.2 2.5 1.3-.1 1.8-.8 3.3-.8s2 .8 3.3.8c1.4 0 2.3-1.2 3.1-2.4 1-1.4 1.4-2.8 1.4-2.9-.1 0-2.9-1.1-2.9-4.2zM14 5.3c.7-.9 1.2-2.1 1.1-3.3-1 0-2.3.7-3 1.6-.7.8-1.2 2-1.1 3.2 1.1.1 2.3-.6 3-1.5z"/></svg>'


def stores(light=False):
    return (f'<a class="btn btn-solid" href="{PLAY}" target="_blank" rel="noopener">{PLAY_SVG}Google Play</a>\n'
            f'        <a class="btn btn-outline" href="{APPLE}" target="_blank" rel="noopener">{APPLE_SVG}App Store</a>')


def icon(name):
    paths = {
        'status': '<path d="M5 12.5 9.5 17 19 7"/>',
        'plan': '<path d="M4 6h16M4 12h10M4 18h6"/><path d="m16 15 2 2 3-4"/>',
        'bell': '<path d="M6 17V11a6 6 0 0 1 12 0v6l1.5 2h-15zM10 21h4"/>',
        'coin': '<circle cx="12" cy="12" r="8.5"/><path d="M12 7v10M9.5 9.5c0-1.2 1-1.8 2.5-1.8s2.5.6 2.5 1.8-1 1.6-2.5 2-2.5.8-2.5 2 1 1.8 2.5 1.8 2.5-.6 2.5-1.8"/>',
        'doc': '<path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
        'filter': '<path d="M4 5h16l-6 8v6l-4-2v-4z"/>',
        'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
        'lock': '<rect x="5" y="10.500" width="14" height="9.500" rx="2"/><path d="M8 10.500V8a4 4 0 0 1 8 0v2.500"/>',
        'user': '<circle cx="12" cy="8" r="4"/><path d="M4 20c1-4 4-6 8-6s7 2 8 6"/>',
        'check': '<path d="m5 12.500 4.500 4.500L19 7"/>',
    }
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{paths[name]}</svg>'


def feat(ico, t_ar, t_en, p_ar, p_en):
    return (f'<article class="feat" data-reveal><div class="ico">{icon(ico)}</div><h3>{bi(t_ar, t_en)}</h3>'
            f'<p>{bi(p_ar, p_en)}</p></article>')


def step(n, t_ar, t_en, p_ar, p_en, on=False):
    return (f'<button class="step{" on" if on else ""}" type="button" role="listitem" aria-expanded="{"true" if on else "false"}">'
            f'<span class="n">{n:02d}</span><h3>{bi(t_ar, t_en)}</h3><p>{bi(p_ar, p_en)}</p></button>')


def check_li(t_ar, t_en, p_ar, p_en):
    return (f'<li><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7"/></svg>'
            f'<div><b>{bi(t_ar, t_en)}</b><span>{bi(p_ar, p_en)}</span></div></li>')


# ────────────────────────────────────────────────────────────── INDEX
FAQ = [
    ('ما هو CheckBook؟', 'What is CheckBook?',
     'CheckBook تطبيق موبايل لأندرويد وآيفون لمتابعة الشيكات: البنوك والمبالغ ومواعيد الاستحقاق والحالات، مع تذكير قبل كل موعد.',
     'CheckBook is a mobile app for Android and iPhone that keeps track of your cheques: banks, amounts, due dates and states, with a reminder before each due date.'),
    ('كيف تعمل التذكيرات؟', 'How do the reminders work?',
     'لكل شيك يجدول التطبيق ثلاثة إشعارات على هاتفك: قبل الاستحقاق بثلاثة أيام، وقبله بيوم، وفي يوم الاستحقاق، في الساعة التي تختارها من الإعدادات.',
     'For every cheque the app schedules three notifications on your phone: 3 days before, 1 day before and on the due day, at the hour you choose in settings.'),
    ('ما هي الخطة الذكية؟', 'What is the smart plan?',
     'تقسّم مبلغاً كلياً إلى سلسلة تصل إلى 50 شيكاً بتواريخ منتظمة، فلا تدخل كل شيك بيدك. وتستطيع مراجعة المبالغ وتعديلها قبل الحفظ.',
     'It splits a total amount into a series of up to 50 cheques with regular dates, so you do not enter each one by hand. You can review and adjust the amounts before saving.'),
    ('هل بياناتي خاصة؟', 'Is my data private?',
     'تُحفظ شيكاتك تحت حسابك، وقواعد الوصول تسمح لك وحدك بقراءتها وتعديلها. وتستطيع حذف حسابك وكل بياناته من الإعدادات.',
     'Your cheques are stored under your account, and access rules let only you read and change them. You can delete your account and all its data from settings.'),
    ('هل يدعم العربية؟', 'Does it support Arabic?',
     'نعم. التطبيق متوفر بالعربية (من اليمين لليسار) وبالإنجليزية، وتبدّل اللغة من الإعدادات.',
     'Yes. The app is available in Arabic (right-to-left) and in English, and you can switch language from settings.'),
]


def faq_html():
    items = ''.join(f'<details><summary>{bi(qa, qe)}<span aria-hidden="true">+</span></summary><p>{bi(aa, ae)}</p></details>' for qa, qe, aa, ae in FAQ)
    return f'''<section class="bordered section-padding section-space" id="faq">
  <div>
    <div class="sec-head" data-reveal>
      <span class="eyebrow"><i class="status-dot"></i>{bi('أسئلة شائعة', 'Questions')}</span>
      <h2>{bi('أسئلة عن CheckBook.', 'Questions about CheckBook.')}</h2>
    </div>
    <div class="faq-items" data-reveal>{items}</div>
  </div>
</section>'''


def index_ld(lang):
    en_url, ar_url = ORIGIN + '/checkbook/', ORIGIN + '/ar/checkbook/'
    url = ar_url if lang == 'ar' else en_url
    desc = ('تطبيق موبايل لمتابعة الشيكات: المبالغ والبنوك ومواعيد الاستحقاق والحالات، مع تذكيرات قبل كل موعد وخطة ذكية لسلاسل الشيكات.'
            if lang == 'ar' else
            'Mobile app for tracking cheques: amounts, banks, due dates and states, with reminders before each due date and a smart plan for series of cheques.')
    qa = [{"@type": "Question", "name": (q_ar if lang == 'ar' else q_en),
           "acceptedAnswer": {"@type": "Answer", "text": (a_ar if lang == 'ar' else a_en)}} for q_ar, q_en, a_ar, a_en in FAQ]
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url + "#page", "url": url, "name": "CheckBook", "inLanguage": lang,
         "isPartOf": {"@id": ORIGIN + "/#website"}, "about": {"@id": ORIGIN + "/checkbook/#app"}},
        {"@type": "MobileApplication", "@id": ORIGIN + "/checkbook/#app", "name": "CheckBook", "alternateName": "H1 Checkbook",
         "operatingSystem": "Android, iOS", "applicationCategory": "FinanceApplication", "description": desc,
         "image": ORIGIN + "/checkbook/assets/img/og.jpg", "url": en_url, "downloadUrl": [PLAY, APPLE],
         "inLanguage": ["ar", "en"], "author": {"@id": ORIGIN + "/#organization"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inturp", "item": ORIGIN + ("/ar/" if lang == 'ar' else "/")},
            {"@type": "ListItem", "position": 2, "name": "CheckBook", "item": url}]},
        {"@type": "FAQPage", "mainEntity": qa}]}


def build_index():
    body = f'''<main id="main">

<section class="product-intro section-padding">
  <div class="product-page-grid">
    <div class="product-page-copy">
      <nav class="crumbs" aria-label="Breadcrumb" data-ar-aria-label="مسار التنقل" data-en-aria-label="Breadcrumb" data-attrs="aria-label">
        <a href="/" data-ar-href="/ar/" data-en-href="/" data-attrs="href">{bi('إنتيرب', 'Inturp')}</a><span>/</span>
        <a href="/#checkbook" data-ar-href="/ar/#checkbook" data-en-href="/#checkbook" data-attrs="href">{bi('أعمالنا', 'Our work')}</a><span>/</span>
        <span aria-current="page">CheckBook</span>
      </nav>
      <span class="eyebrow"><i class="status-dot"></i>{bi('من أعمالنا · تطبيق موبايل', 'Our work · Mobile app')}</span>
      <h1>
        <span class="ar">كل شيك وكل موعد استحقاق، <em>تحت السيطرة.</em></span>
        <span class="en">Every cheque, every due date, <em>under control.</em></span>
      </h1>
      <p class="lead">{bi('صمّمنا وبنينا CheckBook، تطبيق موبايل لمتابعة الشيكات. سجّل كل شيك ببنكه ومبلغه وتاريخ استحقاقه، وشاهد ما استحق وما تم صرفه، وتلقَّ تذكيراً قبل حلول الموعد.',
                           'We designed and built CheckBook, a mobile app for keeping track of cheques. Record each one with its bank, amount and due date, see what is due and what has been cashed, and get reminded before the day arrives.')}</p>
      <div class="cta-row">
        {stores()}
      </div>
      <div class="meta-row">
        <div>{bi('المنصات', 'Platforms')}<b>Android · iOS</b></div>
        <div>{bi('اللغات', 'Languages')}<b>{bi('العربية · الإنجليزية', 'Arabic · English')}</b></div>
        <div>{bi('ما نفّذناه', 'Scope')}<b>{bi('تصميم · تطبيق · خدمات', 'Design · App · Backend')}</b></div>
      </div>
    </div>
    <div class="hero-art" aria-hidden="true">
      <div class="phone p1"><div class="scr"><img src="/checkbook/assets/img/app-details.webp" alt="" width="520" height="1130"></div></div>
      <div class="phone p2"><div class="scr"><img src="/checkbook/assets/img/app-home.webp" alt="" width="520" height="1130" fetchpriority="high"></div></div>
      <div class="hero-badge">
        <img src="/checkbook/assets/img/app-icon.png" alt="" width="42" height="42">
        <div><b>CheckBook</b><small>{bi('متوفر على أندرويد وآيفون', 'Available on Android and iPhone')}</small></div>
      </div>
    </div>
  </div>
</section>

<section class="stats section-padding" aria-label="At a glance" data-ar-aria-label="نظرة سريعة" data-en-aria-label="At a glance" data-attrs="aria-label">
  <div class="inner">
    <div class="stat" data-reveal><b>53</b><span>{bi('عملة للاختيار من بينها لكل شيك', 'currencies to choose from, per cheque')}</span></div>
    <div class="stat" data-reveal><b>50</b><span>{bi('شيكاً كحد أقصى في الخطة الذكية الواحدة', 'cheques at most in one smart plan')}</span></div>
    <div class="stat" data-reveal><b>3</b><span>{bi('تذكيرات لكل شيك: قبل 3 أيام وقبل يوم ويوم الاستحقاق', 'reminders per cheque: 3 days before, 1 day before, and on the day')}</span></div>
    <div class="stat" data-reveal><b>2</b><span>{bi('لغتان: العربية والإنجليزية مع دعم كامل لليمين لليسار', 'languages: Arabic and English, with full right-to-left')}</span></div>
  </div>
</section>

<section id="brief" class="section-padding section-space">
  <div class="brief">
    <div data-reveal>
      <span class="eyebrow"><i class="status-dot"></i>{bi('عن المشروع', 'The project')}</span>
      <h2>{bi('تفصيل صغير يسهل أن يضيع منك.', 'A small thing that is easy to lose track of.')}</h2>
    </div>
    <div class="cols" data-reveal>
      <div>
        <h3>{bi('المشكلة', 'The problem')}</h3>
        <p>{bi('الشيك هو تاريخ ومبلغ واسم. وحين يصبح عندك عشرة منها، في درج أو في معرض الصور، يصير نسيان موعد استحقاق واحد أمراً سهلاً.',
               'A cheque is a date, an amount and a name. Once you have a dozen of them, in a drawer or a photo gallery, missing one due date is easy.')}</p>
        <div class="state-row">
          <span class="state not"><i></i>{bi('غير مستحق', 'Not due')}</span><span class="state due"><i></i>{bi('مستحق', 'Due')}</span>
          <span class="state cashed"><i></i>{bi('مصروف', 'Cashed')}</span><span class="state ret"><i></i>{bi('راجع', 'Returned')}</span>
        </div>
      </div>
      <div>
        <h3>{bi('ما بنيناه', 'What we built')}</h3>
        <p>{bi('تطبيق مركّز: لوحة بالمجاميع، وبطاقة لكل شيك، وتغيير الحالة بلمسة، وخطة ذكية لسلاسل الشيكات، وتذكيرات تعمل على الهاتف نفسه.',
               'A focused app: a dashboard of totals, a card for each cheque, one-tap state changes, a smart plan for series of cheques, and reminders that run on the phone itself.')}</p>
        <p>{bi('وتُحفظ شيكاتك تحت حسابك، ولا يقرؤها أحد غيرك.', 'Your cheques are stored under your account, and nobody but you can read them.')}</p>
      </div>
    </div>
  </div>
</section>

<section class="tour section-padding section-space" id="tour">
  <div>
    <div class="sec-head" data-reveal>
      <span class="eyebrow"><i class="status-dot"></i>{bi('جولة في التطبيق', 'App tour')}</span>
      <h2>{bi('من اللوحة الرئيسية إلى الخطة الذكية.', 'From the dashboard to the smart plan.')}</h2>
      <p>{bi('لقطات حقيقية من التطبيق. اضغط على أي خطوة لتنتقل إليها.', 'Real screenshots from the app. Select any step to jump to it.')}</p>
    </div>
    <div class="tour-grid">
      <div class="steps" role="list">
        {step(1, 'لوحة تجيب في نظرة واحدة', 'A dashboard that answers at a glance', 'إجمالي المبلغ وعدد الشيكات، وما استحق منه الآن، وعدّاد لكل حالة: مستحق وغير مستحق ومصروف وراجع.', 'The total amount and number of cheques, how much is due now, and a count for each state: due, not due, cashed and returned.', True)}
        {step(2, 'بطاقة لكل شيك', 'A card for every cheque', 'البنك ورقم الشيك والمستفيد والهاتف والمبلغ وتاريخي الكتابة والاستحقاق في بطاقة واحدة ملوّنة بحسب الحالة، مع فلاتر لكل حالة.', 'Bank, cheque number, payee, phone, amount, issue and due dates on one card, coloured by state, with a filter for each state.')}
        {step(3, 'غيّر الحالة بلمسة', 'Change the state in one tap', 'علّم الشيك مصروفاً أو راجعاً أو ملغى، أو أعد فتحه، أو عدّله، أو احذفه.', 'Mark a cheque as cashed, returned or cancelled, reopen it, edit it or delete it.')}
        {step(4, 'أضف شيكاً، أو خطّط لعدة شيكات', 'Add one cheque, or plan many', 'اختر شيكاً عادياً بكل تفاصيله، أو التخطيط الذكي لتقسيم مبلغ وتوزيع تواريخ شيكات.', 'Choose a regular cheque with all its details, or the smart plan to split an amount across several cheques.')}
        {step(5, 'ابدأ الخطة بمبلغ', 'Start the plan with a total', 'أدخل السعر الكلي والعملة ورقم أول شيك وتاريخ الكتابة وتاريخ أول استحقاق.', 'Enter the total price, the currency, the first cheque number, the writing date and the first due date.')}
        {step(6, 'اختر العدد والمدة بين الشيكات', 'Choose how many, and how far apart', 'من شيك واحد إلى 50 شيكاً، وبفارق بالأشهر. ويظهر لك مجموع المدة قبل أن تولّد الشيكات.', 'From 1 to 50 cheques, spaced in months. The total duration is shown before you generate the cheques.')}
        {step(7, 'تذكيرات ولغة وحساب', 'Reminders, language, account', 'شغّل التذكيرات واختر الساعة، بدّل اللغة، سجّل الخروج، أو احذف حسابك.', 'Turn reminders on and pick the hour, switch language, sign out, or delete your account.')}
      </div>
      <div class="tour-phone">
        <div>
          <div class="phone"><div class="scr">
            <img class="on" src="/checkbook/assets/img/app-home.webp" alt="Dashboard" data-ar-alt="لوحة التطبيق" data-en-alt="Dashboard" data-attrs="alt" width="520" height="1130">
            <img src="/checkbook/assets/img/app-list.webp" alt="Cheque cards" data-ar-alt="بطاقات الشيكات" data-en-alt="Cheque cards" data-attrs="alt" width="520" height="1130" loading="lazy">
            <img src="/checkbook/assets/img/app-details.webp" alt="Cheque details" data-ar-alt="تفاصيل الشيك" data-en-alt="Cheque details" data-attrs="alt" width="520" height="1130" loading="lazy">
            <img src="/checkbook/assets/img/app-add.webp" alt="Add a cheque" data-ar-alt="إضافة شيك" data-en-alt="Add a cheque" data-attrs="alt" width="520" height="1130" loading="lazy">
            <img src="/checkbook/assets/img/app-plan-start.webp" alt="Smart plan, start" data-ar-alt="الخطة الذكية: البداية" data-en-alt="Smart plan, start" data-attrs="alt" width="520" height="1130" loading="lazy">
            <img src="/checkbook/assets/img/app-plan-controls.webp" alt="Smart plan, controls" data-ar-alt="الخطة الذكية: التحكم" data-en-alt="Smart plan, controls" data-attrs="alt" width="520" height="1130" loading="lazy">
            <img src="/checkbook/assets/img/app-settings.webp" alt="Settings" data-ar-alt="الإعدادات" data-en-alt="Settings" data-attrs="alt" width="520" height="1130" loading="lazy">
          </div></div>
          <div class="tour-dots" role="group" aria-label="Screens"><button type="button" class="on" aria-label="1"></button><button type="button" aria-label="2"></button><button type="button" aria-label="3"></button><button type="button" aria-label="4"></button><button type="button" aria-label="5"></button><button type="button" aria-label="6"></button><button type="button" aria-label="7"></button></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="features" class="section-padding section-space">
  <div>
    <div class="sec-head" data-reveal>
      <span class="eyebrow"><i class="status-dot"></i>{bi('المزايا', 'Features')}</span>
      <h2>{bi('كل ما يلزم لمتابعة الشيكات، وما يزيد.', 'Everything needed to follow your cheques, and nothing in the way.')}</h2>
    </div>
    <div class="feat-grid">
      {feat('status', 'حالة تتحدّث وحدها', 'A state that updates itself', 'يصبح الشيك «مستحقاً» عند حلول تاريخه دون أن تفعل شيئاً. والصرف والإرجاع والإلغاء على بعد لمسة.', 'A cheque becomes “due” on its due date without you doing anything. Cashed, returned and cancelled are one tap away.')}
      {feat('plan', 'خطة ذكية', 'Smart plan', 'قسّم مبلغاً إلى حتى 50 شيكاً بتواريخ منتظمة، ثم راجع كل شيك وعدّل مبلغه.', 'Split a total into up to 50 cheques with regular dates, then review each one and adjust its amount.')}
      {feat('bell', 'تذكيرات', 'Reminders', 'إشعارات تُجدول على جهازك قبل الاستحقاق بثلاثة أيام وبيوم وفي يوم الاستحقاق، في الساعة التي تختارها.', 'Notifications scheduled on your device 3 days before, 1 day before and on the due day, at the hour you choose.')}
      {feat('coin', '53 عملة', '53 currencies', 'اختر عملة كل شيك من قائمة تضم 53 عملة، بالأسماء العربية والإنجليزية.', 'Pick each cheque’s currency from a list of 53, with Arabic and English names.')}
      {feat('doc', 'كل تفصيل', 'Every detail', 'اسم البنك ورقم الشيك ورقم الحساب واسم المستفيد وهاتفه وتاريخا الكتابة والاستحقاق.', 'Bank name, cheque number, account number, payee name and phone, issue and due dates.')}
      {feat('filter', 'فلاتر بحسب الحالة', 'Filters by state', 'الكل، مستحق، غير مستحق، مصروف، راجع: تبديل واحد وتتغير القائمة.', 'All, due, not due, cashed, returned: one tap and the list follows.')}
      {feat('globe', 'عربي وإنجليزي', 'Arabic and English', 'واجهة كاملة بالعربية من اليمين لليسار وبالإنجليزية، وتبديل من الإعدادات.', 'A full right-to-left Arabic interface and an English one, switchable from settings.')}
      {feat('lock', 'خصوصية من التصميم', 'Private by design', 'تُحفظ الشيكات تحت حسابك، وقواعد الوصول تسمح لك وحدك بقراءتها وتعديلها.', 'Cheques are stored under your account, and access rules let only you read and change them.')}
      {feat('user', 'دخول سريع وحذف حسابك', 'Quick sign-in, and delete your account', 'سجّل الدخول بـ Google أو Apple، واحذف حسابك وكل بياناتك من الإعدادات.', 'Sign in with Google or Apple, and delete your account and all its data from settings.')}
    </div>
  </div>
</section>

<section class="admin alt section-padding section-space" id="plan">
  <div class="admin-grid">
    <div data-reveal>
      <span class="eyebrow"><i class="status-dot"></i>{bi('التخطيط الذكي', 'Smart plan')}</span>
      <h2>{bi('خطّط لسلسلة شيكات كاملة في دقيقة.', 'Plan a whole series of cheques in a minute.')}</h2>
      <p class="lead">{bi('بدل كتابة كل شيك على حدة، حدّد المبلغ والإيقاع ودع التطبيق يولّد القائمة.', 'Instead of entering each cheque one by one, set the amount and the rhythm and let the app generate the list.')}</p>
    </div>
    <ul class="checks" data-reveal>
      {check_li('ابدأ بالمبلغ', 'Start with the total', 'السعر الكلي والعملة إجباريان، ورقم أول شيك اختياري.', 'The total price and currency are required; the first cheque number is optional.')}
      {check_li('اختر الإيقاع', 'Choose the rhythm', 'عدد الشيكات من 1 إلى 50، والفارق بين شيك وآخر بالأشهر.', 'Anywhere from 1 to 50 cheques, with the gap between them in months.')}
      {check_li('اعرف المدة', 'See the duration', 'يعرض التطبيق المدة الكلية بالأشهر وبالسنوات قبل التوليد.', 'The app shows the total duration in months and in years before generating.')}
      {check_li('راجع وعدّل', 'Review and adjust', 'يحصل كل شيك على رقم ومبلغ وتاريخ، وتستطيع تعديل المبالغ، ثم تكمل بيانات المستفيد وتحفظ.', 'Each cheque gets a number, an amount and a date; you can adjust the amounts, then complete the payee details and save.')}
    </ul>
  </div>
</section>

<section class="bordered section-padding section-space" id="stack">
  <div>
    <div class="sec-head" data-reveal style="margin-bottom:30px">
      <span class="eyebrow"><i class="status-dot"></i>{bi('خلف الكواليس', 'Under the hood')}</span>
      <h2>{bi('كود واحد، منصتان، وخدمات موثوقة.', 'One codebase, two platforms, dependable services.')}</h2>
    </div>
    <div class="stack-row" data-reveal>
      <span class="chip">Flutter</span><span class="chip">Firebase Auth</span><span class="chip">Cloud Firestore</span><span class="chip">Cloud Functions</span><span class="chip">Cloud Messaging</span><span class="chip">Local notifications</span><span class="chip">Google AdMob</span><span class="chip">Sign in with Apple</span><span class="chip">Google Sign-In</span>
    </div>
    <p class="stack-note" data-reveal>{bi('التذكيرات تُجدول على الجهاز نفسه، وتنظيف البيانات عند حذف الحساب يجري تلقائياً على الخادم.', 'Reminders are scheduled on the device itself, and cleaning up your data when you delete an account happens automatically on the server.')}</p>
  </div>
</section>

{faq_html()}

<section class="get section-padding section-space" id="get">
  <div data-reveal>
    <img class="ic" src="/checkbook/assets/img/app-icon.png" alt="CheckBook app icon" width="84" height="84">
    <h2>{bi('جرّب CheckBook.', 'Try CheckBook.')}</h2>
    <p>{bi('متوفر على أندرويد وآيفون.', 'Available on Android and iPhone.')}</p>
    <div class="cta-row">
        {stores()}
    </div>
  </div>
</section>

<section class="contact bordered section-padding section-space" id="contact">
  <div class="inner">
    <div data-reveal>
      <span class="eyebrow"><i class="status-dot"></i>{bi('تواصل معنا', 'Contact')}</span>
      <h2>{bi('تريد تطبيقاً مثل هذا لعملك؟', 'Want an app like this for your business?')}</h2>
      <p>{bi('نبني منتجات رقمية من الفكرة إلى الإطلاق. أخبرنا عن عملك ونرجع إليك.', 'We build digital products from idea to launch. Tell us about your business and we’ll get back to you.')}</p>
    </div>
    <div class="links" data-reveal>
      <a href="mailto:info@inturp.com"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="5.5" width="17" height="13" rx="2"/><path d="m4 7 8 6 8-6"/></svg>info@inturp.com</a>
      <a href="https://instagram.com/inturp_" target="_blank" rel="noopener">{shared.INSTAGRAM}@inturp_</a>
    </div>
  </div>
</section>

</main>
'''
    emit('', {'en': 'CheckBook — cheque tracking app with reminders | Inturp', 'ar': 'CheckBook — تطبيق متابعة الشيكات مع تذكير بالاستحقاق | انتيرب'},
         {'en': 'CheckBook is a mobile app by Inturp for tracking cheques: dashboard totals, due-date states, a smart plan for series of cheques and reminders. Arabic and English.',
          'ar': 'CheckBook تطبيق موبايل من انتيرب لمتابعة الشيكات: لوحة مجاميع وحالات الاستحقاق وخطة ذكية لسلاسل الشيكات وتذكيرات. بالعربية والإنجليزية.'},
         body, index_ld)


# ────────────────────────────────────────────────────────────── LEGAL
def sec(n, t_ar, t_en, ar, en):
    return (f'<section id="s{n}"><h2><span class="n">{n}</span>{bi(t_ar, t_en)}</h2>'
            f'<div class="ar">{ar}</div><div class="en">{en}</div></section>')


def legal_body(h1_ar, h1_en, lead_ar, lead_en, toc, sections):
    toc_html = ''.join(f'<li><a href="#s{i + 1}">{bi(a, e)}</a></li>' for i, (a, e) in enumerate(toc))
    return f'''<main id="main">
<section class="legal-hero section-padding">
  <div class="inner">
    <h1>{bi(h1_ar, h1_en)}</h1>
    <p>{bi(lead_ar, lead_en)}</p>
    <div class="meta"><span>{bi('آخر تحديث:', 'Last updated:')} <b class="latin">{UPDATED}</b></span><span>{bi('التطبيق:', 'App:')} <b>CheckBook</b></span></div>
  </div>
</section>
<div class="section-padding"><div class="doc-wrap inner">
  <aside class="toc" aria-label="Contents" data-ar-aria-label="المحتويات" data-en-aria-label="Contents" data-attrs="aria-label"><b>{bi('المحتويات', 'Contents')}</b><ol>{toc_html}</ol></aside>
  <article class="doc">
{chr(10).join(sections)}
  </article>
</div></div>
</main>
'''


def build_privacy():
    S = []
    S.append(sec(1, 'من نحن', 'Who we are',
                 '<p>تطبيق <b>CheckBook</b> (يظهر في المتجر باسم H1 Checkbook) تطبيق لمتابعة الشيكات وتذكيرك بمواعيد استحقاقها. صمّمته وطوّرته <b>Inturp</b>، وتشغّله، وهي الجهة المسؤولة عن بياناتك داخله.</p><p>تشرح هذه السياسة ما يجمعه التطبيق ولماذا ومع من يُشارَك وكيف تتحكم به.</p>',
                 '<p><b>CheckBook</b> (listed in the stores as H1 Checkbook) is an app for tracking cheques and reminding you of their due dates. It was designed and built by <b>Inturp</b>, which also operates it and is responsible for your data inside it.</p><p>This policy explains what the app collects, why, who it is shared with and how you stay in control.</p>'))
    S.append(sec(2, 'البيانات التي نجمعها', 'What we collect',
                 '''<div class="tbl-wrap"><table class="tbl"><thead><tr><th>البيانات</th><th>متى وكيف</th><th>الغرض</th></tr></thead><tbody>
<tr><td>الحساب: الاسم والبريد الإلكتروني ورابط الصورة ومعرّف الحساب وطريقة الدخول</td><td>عند تسجيل الدخول عبر Google أو Apple</td><td>إنشاء حسابك وربط شيكاتك به</td></tr>
<tr><td>الشيكات التي تدخلها: اسم البنك واسم المستفيد والمبلغ والعملة وهاتف المستفيد ورقم الشيك ورقم الحساب وتاريخا الكتابة والاستحقاق والحالة</td><td>تدخلها بنفسك، أو تولّدها الخطة الذكية</td><td>عرضها وتصفيتها وتذكيرك بها</td></tr>
<tr><td>رمز الإشعارات (FCM)</td><td>عند تفعيل الإشعارات</td><td>إيصال الإشعارات إلى جهازك. يُحذف عند تسجيل الخروج</td></tr>
<tr><td>إعدادات الجهاز: تفعيل التذكير وساعته واللغة وآخر عملة</td><td>عند ضبطها</td><td>تخصيص التطبيق. تبقى على جهازك</td></tr>
<tr><td>بيانات الإعلانات: معرّفات الجهاز ومعرّف الإعلانات وعنوان IP وتفاعلك مع الإعلان</td><td>عند عرض إعلان</td><td>تجمعها Google AdMob لتقديم الإعلانات وقياسها (انظر القسم 5)</td></tr>
</tbody></table></div>
<div class="note"><div><b>ما لا نجمعه</b> لا نصل إلى موقعك ولا جهات اتصالك ولا صورك ولا الكاميرا ولا الميكروفون، ولا نعالج مدفوعات داخل التطبيق.</div></div>''',
                 '''<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Data</th><th>When and how</th><th>Purpose</th></tr></thead><tbody>
<tr><td>Account: name, email, photo link, account ID and sign-in method</td><td>When you sign in with Google or Apple</td><td>Create your account and tie your cheques to it</td></tr>
<tr><td>Cheques you enter: bank name, payee name, amount, currency, payee phone, cheque number, account number, issue and due dates, and state</td><td>You type them in, or the smart plan generates them</td><td>Show, filter and remind you about them</td></tr>
<tr><td>Notification token (FCM)</td><td>When you allow notifications</td><td>Deliver notifications to your device. Removed when you sign out</td></tr>
<tr><td>Device settings: reminders on/off, reminder hour, language, last currency</td><td>When you set them</td><td>Personalise the app. They stay on your device</td></tr>
<tr><td>Advertising data: device identifiers, advertising ID, IP address and your interaction with an ad</td><td>When an ad is shown</td><td>Collected by Google AdMob to deliver and measure ads (see section 5)</td></tr>
</tbody></table></div>
<div class="note"><div><b>What we do not collect</b> We do not access your location, contacts, photos, camera or microphone, and we do not process payments in the app.</div></div>'''))
    S.append(sec(3, 'كيف نستخدم بياناتك', 'How we use your data',
                 '<ul class="list"><li>تشغيل حسابك وعرض شيكاتك وحالتها وتجميع مجاميعها.</li><li>جدولة التذكيرات وإرسال الإشعارات.</li><li>توليد شيكات الخطة الذكية.</li><li>حماية الحساب ومنع إساءة الاستخدام.</li><li>عرض الإعلانات عبر Google AdMob.</li></ul><p>لا نبيع بياناتك الشخصية.</p>',
                 '<ul class="list"><li>Run your account and show your cheques, their states and totals.</li><li>Schedule reminders and send notifications.</li><li>Generate the cheques of a smart plan.</li><li>Keep the account secure and prevent abuse.</li><li>Show ads through Google AdMob.</li></ul><p>We do not sell your personal data.</p>'))
    S.append(sec(4, 'مع من نشارك البيانات', 'Who we share it with',
                 '<ul class="list"><li><b>Google (Firebase):</b> المصادقة وقاعدة البيانات والوظائف السحابية وإشعارات الدفع.</li><li><b>Apple:</b> عند تسجيل الدخول عبر Apple.</li><li><b>Google AdMob:</b> لعرض الإعلانات.</li><li><b>جهات قانونية:</b> عند وجود التزام قانوني أو طلب رسمي صحيح.</li></ul><p>تعالج هذه الجهات البيانات بموجب شروطها الخاصة ولتقديم الخدمة. ولا يرى أحد من المستخدمين الآخرين شيكاتك.</p>',
                 '<ul class="list"><li><b>Google (Firebase):</b> authentication, database, cloud functions and push notifications.</li><li><b>Apple:</b> when you sign in with Apple.</li><li><b>Google AdMob:</b> to show ads.</li><li><b>Legal authorities:</b> where we have a legal obligation or a valid official request.</li></ul><p>These providers process data under their own terms and to deliver the service. No other user can see your cheques.</p>'))
    S.append(sec(5, 'الإعلانات', 'Advertising',
                 '<p>يعرض التطبيق إعلانات (شريطية وبينية ومكافِئة) داخل ميزة التخطيط الذكي، تقدّمها <b>Google AdMob</b>. قد تجمع Google معرّفات الجهاز ومعرّف الإعلانات وعنوان IP وبيانات التفاعل لتقديم الإعلانات وقياسها ومنع الاحتيال، وفق سياساتها.</p><p>يمكنك الحدّ من تخصيص الإعلانات من إعدادات جهازك: على أندرويد من <b>الإعدادات ← الخصوصية ← الإعلانات</b>، وعلى iPhone من <b>الإعدادات ← الخصوصية والأمان ← إعلانات Apple</b>.</p>',
                 '<p>The app shows ads (banner, interstitial and rewarded) inside the smart plan feature, served by <b>Google AdMob</b>. Google may collect device identifiers, the advertising ID, IP address and interaction data to deliver and measure ads and prevent fraud, under its own policies.</p><p>You can limit ad personalisation in your device settings: on Android under <b>Settings → Privacy → Ads</b>, on iPhone under <b>Settings → Privacy &amp; Security → Apple Advertising</b>.</p>'))
    S.append(sec(6, 'الأذونات', 'Permissions',
                 '<ul class="list"><li><b>الإشعارات:</b> لتذكيرك بمواعيد الاستحقاق. اختيارية ويمكن إيقافها من الإعدادات.</li><li><b>الإنترنت:</b> لازم لتسجيل الدخول ومزامنة شيكاتك.</li></ul>',
                 '<ul class="list"><li><b>Notifications:</b> to remind you of due dates. Optional and can be turned off in settings.</li><li><b>Internet:</b> required to sign in and sync your cheques.</li></ul>'))
    S.append(sec(7, 'مدة الاحتفاظ والحذف', 'Retention and deletion',
                 '<p>نحتفظ ببياناتك ما دام حسابك قائماً. حين تحذف حسابك من <b>الإعدادات ← حذف الحساب</b> تُحذف شيكاتك وملفك الشخصي وحسابك تلقائياً من الخادم، وتُلغى التذكيرات على جهازك. التفاصيل في <a class="lnk" href="/checkbook/delete-account/">صفحة حذف الحساب</a>. قد تبقى نسخ احتياطية وسجلات تقنية لدى مزوّدي الخدمات السحابية لمدة قصيرة حتى تنتهي دورة حذفها المعتادة.</p>',
                 '<p>We keep your data while your account exists. When you delete your account from <b>Settings → Delete account</b>, your cheques, profile and account are removed automatically from the server, and reminders on your device are cancelled. Details are on the <a class="lnk" href="/checkbook/delete-account/">account deletion page</a>. Backups and technical logs may remain at our cloud providers for a short time until their normal deletion cycle ends.</p>'))
    S.append(sec(8, 'الأمان', 'Security',
                 '<p>تنتقل بياناتك عبر اتصال مشفّر وتُخزَّن لدى مزوّدين سحابيين معروفين. تحصر قواعد الوصول قراءة شيكاتك وتعديلها بحسابك وحده. لا يوجد نظام آمن بالكامل، لكننا نعمل على حماية بياناتك ونراجع ذلك باستمرار.</p>',
                 '<p>Your data travels over encrypted connections and is stored with established cloud providers. Access rules limit reading and changing your cheques to your own account. No system is perfectly secure, but we work to protect your data and review this continuously.</p>'))
    S.append(sec(9, 'حقوقك', 'Your rights',
                 '<p>يحق لك الاطلاع على بياناتك وتصحيحها وحذفها، وسحب موافقتك على الإشعارات في أي وقت. تستطيع تعديل شيكاتك مباشرة من التطبيق وحذف حسابك من الإعدادات. لأي طلب آخر راسلنا.</p>',
                 '<p>You may access, correct and delete your data and withdraw your consent to notifications at any time. You can edit your cheques directly in the app and delete your account from settings. For anything else, write to us.</p>'))
    S.append(sec(10, 'الأطفال', 'Children',
                 '<p>التطبيق موجّه للبالغين وليس للأطفال دون 13 عاماً، ولا نجمع بيانات منهم عن قصد. إن علمتَ أن طفلاً أنشأ حساباً فأخبرنا لنحذفه.</p>',
                 '<p>The app is for adults and not for children under 13, and we do not knowingly collect their data. If you know a child has created an account, tell us and we will delete it.</p>'))
    S.append(sec(11, 'النقل الدولي والتغييرات', 'International transfers and changes',
                 '<p>قد تُعالَج بياناتك على خوادم خارج بلدك لدى مزوّدي الخدمات السحابية. وقد نحدّث هذه السياسة عند تغيّر التطبيق أو القانون ونعدّل تاريخ آخر تحديث أعلى الصفحة. الاستمرار في استخدام التطبيق بعد التحديث يعني قبوله.</p>',
                 '<p>Your data may be processed on servers outside your country with our cloud providers. We may update this policy when the app or the law changes and will change the “last updated” date at the top. Continuing to use the app after an update means you accept it.</p>'))
    S.append(sec(12, 'تواصل معنا', 'Contact us',
                 '<p>لأي سؤال أو طلب يخص الخصوصية أو بياناتك، راسلنا وسنرد عليك.</p><div class="contact-card"><div><b>أسئلة أو طلبات الخصوصية؟</b><p><a class="lnk latin" href="mailto:info@inturp.com">info@inturp.com</a></p></div><a class="btn btn-light" href="mailto:info@inturp.com">راسلنا</a></div>',
                 '<p>For any privacy question or request about your data, write to us and we will reply.</p><div class="contact-card"><div><b>Privacy questions or requests?</b><p><a class="lnk latin" href="mailto:info@inturp.com">info@inturp.com</a></p></div><a class="btn btn-light" href="mailto:info@inturp.com">Email us</a></div>'))
    toc = [('من نحن', 'Who we are'), ('ما نجمعه', 'What we collect'), ('الاستخدام', 'How we use it'), ('المشاركة', 'Sharing'), ('الإعلانات', 'Advertising'),
           ('الأذونات', 'Permissions'), ('الاحتفاظ والحذف', 'Retention'), ('الأمان', 'Security'), ('حقوقك', 'Your rights'), ('الأطفال', 'Children'),
           ('النقل والتغييرات', 'Transfers'), ('التواصل', 'Contact')]
    body = legal_body('سياسة الخصوصية', 'Privacy policy',
        'كيف يتعامل تطبيق CheckBook مع بياناتك: ماذا نجمع، ولماذا، ومع من نشاركه، وكيف تتحكم به.',
        'How the CheckBook app handles your data: what we collect, why, who we share it with, and how you stay in control.', toc, S)
    emit('privacy/', {'en': 'Privacy policy — CheckBook', 'ar': 'سياسة الخصوصية — CheckBook'},
         {'en': 'Privacy policy for the CheckBook app: what data it collects, why, who it is shared with, and how to delete it.',
          'ar': 'سياسة خصوصية تطبيق CheckBook: البيانات التي يجمعها ولماذا ومع من تُشارَك وكيف تحذفها.'}, body)


def build_delete():
    S = []
    S.append(sec(1, 'الطريقة الأسرع: من داخل التطبيق', 'Fastest way: inside the app',
                 '''<p>إن كنتَ تستطيع فتح التطبيق، احذف حسابك بنفسك في أقل من دقيقة:</p>
<ol class="steps-l"><li><b>افتح الإعدادات</b>من الشاشة الرئيسية اضغط أيقونة الإعدادات.</li><li><b>اضغط «حذف الحساب»</b>ثم أكّد في نافذة التأكيد.</li><li><b>أعد تسجيل الدخول إن طُلب منك</b>لحماية حسابك، قد يطلب التطبيق تسجيل الدخول مجدداً عبر Google أو Apple قبل الحذف.</li></ol>
<p>عند نجاح الحذف يُحذف حسابك وتُحذف شيكاتك ويُسجَّل خروجك. لا يمكن التراجع عن العملية.</p>''',
                 '''<p>If you can open the app, you can delete your account yourself in under a minute:</p>
<ol class="steps-l"><li><b>Open Settings</b>Tap the settings icon on the home screen.</li><li><b>Tap “Delete account”</b>Then confirm in the dialog.</li><li><b>Sign in again if asked</b>To protect your account, the app may ask you to sign in again with Google or Apple before deleting.</li></ol>
<p>When deletion succeeds your account and your cheques are deleted and you are signed out. This cannot be undone.</p>'''))
    S.append(sec(2, 'ما الذي يُحذف وما الذي يبقى', 'What is deleted and what stays',
                 '''<div class="two">
<div class="box del"><h3>يُحذف</h3><ul class="list"><li>كل شيكاتك وبياناتها</li><li>ملفك الشخصي: الاسم والبريد والصورة ومعرّف الحساب</li><li>رمز الإشعارات وتذكيرات الجهاز</li><li>حساب تسجيل الدخول نفسه</li></ul></div>
<div class="box keep"><h3>قد يبقى</h3><ul class="list"><li>نسخ احتياطية وسجلات تقنية لدى مزوّدي الخدمات السحابية لمدة قصيرة حتى تنتهي دورة حذفها المعتادة</li><li>بيانات الإعلانات التي جمعتها Google AdMob، وتخضع لسياسات Google</li></ul></div>
</div>
<div class="note"><div>يجري حذف الشيكات والملف الشخصي تلقائياً على الخادم بمجرد حذف حسابك، ولا نحتفظ بسجلات شيكاتك.</div></div>''',
                 '''<div class="two">
<div class="box del"><h3>Deleted</h3><ul class="list"><li>All your cheques and their details</li><li>Your profile: name, email, photo and account ID</li><li>The notification token and the reminders on your device</li><li>The sign-in account itself</li></ul></div>
<div class="box keep"><h3>May stay</h3><ul class="list"><li>Backups and technical logs at our cloud providers for a short time until their normal deletion cycle ends</li><li>Advertising data collected by Google AdMob, which falls under Google’s policies</li></ul></div>
</div>
<div class="note"><div>Cheques and the profile are deleted automatically on the server as soon as your account is deleted, and we do not keep a record of your cheques.</div></div>'''))
    form_ar = '<p>إن لم تستطع فتح التطبيق، أرسل لنا طلباً. عبّئ الحقول وسيفتح بريدك رسالة جاهزة نستلمها على <span class="latin">info@inturp.com</span>.</p>'
    form_en = '<p>If you cannot open the app, send us a request. Fill in the fields and your email app opens a ready message that reaches us at <span class="latin">info@inturp.com</span>.</p>'
    form = '''
<form class="formcard" id="delForm" novalidate>
  <label><span class="ar">البريد الإلكتروني لحسابك</span><span class="en">Your account email</span><input id="delId" type="email" autocomplete="email" required></label>
  <label><span class="ar">الاسم الظاهر في الحساب (اختياري)</span><span class="en">Name on the account (optional)</span><input id="delName" type="text" autocomplete="name"></label>
  <p class="form-note" id="delErr" role="alert" hidden></p>
  <button class="btn btn-solid" type="submit"><span class="ar">افتح رسالة الطلب</span><span class="en">Open request email</span></button>
  <p class="form-note"><span class="ar">لا نرسل شيئاً عبر هذه الصفحة؛ يُنشأ الطلب في تطبيق البريد لديك وترسله أنت.</span><span class="en">Nothing is sent from this page; the request is drafted in your email app and you send it yourself.</span></p>
</form>'''
    S.append(sec(3, 'لا تستطيع الدخول؟ أرسل طلباً', 'Can’t sign in? Send a request', form_ar + form, form_en))
    S.append(sec(4, 'ماذا يحدث بعد طلبك', 'What happens after your request',
                 '<ol class="steps-l"><li><b>نتحقق من هويتك</b>قد نطلب منك تأكيد البريد المرتبط بالحساب حتى لا يحذف أحد حساب غيره.</li><li><b>ننفّذ الحذف</b>نحذف الحساب وكل ما ذُكر أعلاه.</li><li><b>نؤكد لك</b>نرد عليك خلال <b>30 يوماً</b> كحد أقصى، وغالباً أسرع.</li></ol>',
                 '<ol class="steps-l"><li><b>We verify it is you</b>We may ask you to confirm the email linked to the account so nobody can delete someone else’s account.</li><li><b>We carry out the deletion</b>We delete the account and everything listed above.</li><li><b>We confirm</b>We reply within <b>30 days</b> at most, usually sooner.</li></ol>'))
    S.append(sec(5, 'أسئلة؟', 'Questions?',
                 '<p>راسلنا على <a class="lnk latin" href="mailto:info@inturp.com">info@inturp.com</a>. وللتفاصيل عن بياناتنا راجع <a class="lnk" href="/checkbook/privacy/">سياسة الخصوصية</a>.</p>',
                 '<p>Write to <a class="lnk latin" href="mailto:info@inturp.com">info@inturp.com</a>. For details on our data practices see the <a class="lnk" href="/checkbook/privacy/">privacy policy</a>.</p>'))
    toc = [('من داخل التطبيق', 'In the app'), ('ما يُحذف', 'What is deleted'), ('طلب بالبريد', 'Send a request'), ('بعد الطلب', 'After your request'), ('أسئلة', 'Questions')]
    js = """<script>
(function(){var f=document.getElementById('delForm');if(!f)return;
f.addEventListener('submit',function(e){e.preventDefault();var en=document.documentElement.lang==='en';
var id=document.getElementById('delId').value.trim(),err=document.getElementById('delErr');
if(!id){err.hidden=false;err.textContent=en?'Please enter the email linked to the account.':'يرجى إدخال البريد المرتبط بالحساب.';return}
err.hidden=true;var name=document.getElementById('delName').value.trim();
var subject=en?'Account deletion request — CheckBook':'طلب حذف حساب — CheckBook';
var body=en?'Hello,\\n\\nI would like to delete my account in the CheckBook app.\\n\\nAccount email: '+id+'\\nName: '+(name||'-')+'\\n\\nThank you.':'مرحباً،\\n\\nأرغب بحذف حسابي في تطبيق CheckBook.\\n\\nبريد الحساب: '+id+'\\nالاسم: '+(name||'-')+'\\n\\nشكراً.';
location.href='mailto:info@inturp.com?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(body)})})();
</script>
"""
    body = legal_body('طلب حذف الحساب', 'Delete your account',
        'احذف حسابك في تطبيق CheckBook من داخل التطبيق، أو أرسل لنا طلباً إن لم تستطع فتحه. نوضح هنا ما يُحذف وما يبقى وكم يستغرق الأمر.',
        'Delete your CheckBook account inside the app, or send us a request if you cannot open it. Here is what is deleted, what stays and how long it takes.', toc, S)
    emit('delete-account/', {'en': 'Delete your account — CheckBook', 'ar': 'حذف الحساب — CheckBook'},
         {'en': 'How to delete your CheckBook account: inside the app or by request, what is deleted and what stays.',
          'ar': 'كيف تحذف حسابك في CheckBook: من داخل التطبيق أو بطلب، وما الذي يُحذف وما الذي يبقى.'}, body, extra_end=js)


def build_stubs():
    for old, new in [('privacy.html', 'privacy/'), ('delete-account.html', 'delete-account/')]:
        t = ORIGIN + '/checkbook/' + new
        (ROOT / old).write_text(
            '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Redirecting…</title>'
            f'<link rel="canonical" href="{t}"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url=/checkbook/{new}">'
            f'<script>location.replace("/checkbook/{new}"+location.search+location.hash)</script></head><body><a href="/checkbook/{new}">{t}</a></body></html>',
            encoding='utf-8')


def build_og():
    from PIL import Image, ImageDraw, ImageFont
    img = ROOT / 'assets' / 'img'
    W, H = 1200, 630
    bg = Image.new('RGB', (W, H), (20, 24, 26))
    d = ImageDraw.Draw(bg)

    def phone(name, h):
        s = Image.open(img / name).convert('RGB')
        w = int(s.width * h / s.height)
        s = s.resize((w, h), Image.LANCZOS)
        pad = 8
        fr = Image.new('RGB', (w + 2 * pad, h + 2 * pad), (40, 46, 48))
        m = Image.new('L', fr.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, fr.width - 1, fr.height - 1), radius=38, fill=255)
        fr.paste(s, (pad, pad))
        out = Image.new('RGBA', fr.size, (0, 0, 0, 0))
        out.paste(fr, (0, 0), m)
        return out
    p1 = phone('app-details.webp', 470).rotate(5, expand=True, resample=Image.BICUBIC)
    p2 = phone('app-home.webp', 500).rotate(-4, expand=True, resample=Image.BICUBIC)
    bg.paste(p1, (700, 150), p1)
    bg.paste(p2, (880, 60), p2)
    ic = Image.open(img / 'app-icon.png').convert('RGB').resize((150, 150))
    m = Image.new('L', ic.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, 149, 149), radius=34, fill=255)
    bg.paste(ic, (76, 110), m)
    f = lambda s: ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', s)
    d.text((76, 330), 'CheckBook', font=f(72), fill=(238, 242, 236))
    d.text((78, 430), 'Every cheque, every due date,', font=f(30), fill=(152, 163, 155))
    d.text((78, 470), 'under control.', font=f(30), fill=(127, 149, 105))
    d.text((78, 560), 'inturp.', font=f(34), fill=(238, 242, 236))
    bg.save(img / 'og.jpg', quality=88)


if __name__ == '__main__':
    ROOT.mkdir(exist_ok=True)
    build_og()
    build_index()
    build_privacy()
    build_delete()
    build_stubs()
    print('checkbook built')
