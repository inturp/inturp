#!/usr/bin/env python3
"""Builds the clinic survey: /clinic-survey/ (English) and /ar/clinic-survey/ (Arabic). noindex, not in the sitemap.

  python3 website-source/showcase/build_survey.py

Edit survey/questions.json to change the questions. Where answers go is set in
clinic-survey/assets/js/survey-config.js (created once, never overwritten by this script).
"""
import json
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import shared  # noqa: E402

SITE = HERE.parents[1]
OUT = {'en': SITE / 'clinic-survey', 'ar': SITE / 'ar' / 'clinic-survey'}
ASSETS = SITE / 'clinic-survey' / 'assets'
V = '20261040'
SURVEY_ID = 'vet-clinics-2026'

UI = {
    'en': dict(next='Continue', send='Send answers', back='Back', minutes='About 3 minutes', count='{n} short questions', private='Anonymous unless you choose otherwise',
               needChoice='Please choose an answer to continue.', needText='Please write a short answer to continue.', badEmail='That email address does not look right.',
               needConsent='Tick the box so we know we may contact you, or clear the contact fields.', upto='Pick up to {n}', selected='{n} selected',
               lastTitle='One last step.', lastLead='Your answers are ready. Send them to us and you are done.', failLead='We could not reach our server. You can still send your answers another way.',
               lastHow='Open an email with your answers already written, or copy them and send them however you like.', openMail='Open email', copy='Copy answers', copied='Copied',
               mailSubject='Veterinary clinics survey: my answers', mailIntro='My answers to the Inturp veterinary clinics survey:', share='Share', keysEnter='Enter'),
    'ar': dict(next='متابعة', send='إرسال الإجابات', back='رجوع', minutes='نحو 3 دقائق', count='{n} سؤالاً قصيراً', private='دون الكشف عن هويتك إلا إن أردت',
               needChoice='اختر إجابة للمتابعة.', needText='اكتب إجابة قصيرة للمتابعة.', badEmail='البريد الإلكتروني غير صحيح.',
               needConsent='فعّل المربع لنعرف أن بإمكاننا التواصل معك، أو امسح بيانات التواصل.', upto='اختر حتى {n}', selected='تم اختيار {n}',
               lastTitle='خطوة أخيرة.', lastLead='إجاباتك جاهزة. أرسلها لنا وننتهي.', failLead='تعذّر الوصول إلى خادمنا، لكن تستطيع إرسال إجاباتك بطريقة أخرى.',
               lastHow='افتح رسالة بريد جاهزة بإجاباتك، أو انسخها وأرسلها كما تحب.', openMail='فتح البريد', copy='نسخ الإجابات', copied='تم النسخ',
               mailSubject='استبيان العيادات البيطرية: إجاباتي', mailIntro='إجاباتي على استبيان انتيرب للعيادات البيطرية:', share='مشاركة', keysEnter='Enter'),
}
META = {
    'en': dict(title='Veterinary clinics survey | Inturp',
               desc='A short survey for veterinary clinics: how you work today and what you need from clinic software. About three minutes.'),
    'ar': dict(title='استبيان العيادات البيطرية | انتيرب',
               desc='استبيان قصير للعيادات البيطرية: كيف تعملون اليوم وماذا تحتاجون من برنامج العيادة. نحو ثلاث دقائق.'),
}
HOME = {'en': '/vet-charted/en/', 'ar': '/vet-charted/'}


def pick(obj, lang):
    """Choose the language of every {ar, en} pair inside obj."""
    if isinstance(obj, dict):
        if set(obj) == {'ar', 'en'}:
            return obj[lang]
        out = {}
        for k, v in obj.items():
            if k in ('label', 'ar', 'en') and isinstance(v, str):
                out[k] = v
            else:
                out[k] = pick(v, lang)
        return out
    if isinstance(obj, list):
        return [pick(x, lang) for x in obj]
    return obj


def lang_data(src, lang):
    d = {'id': SURVEY_ID, 'ui': UI[lang]}
    d['intro'] = pick(src['intro'], lang)
    d['done'] = pick({k: v for k, v in src['done'].items()}, lang)
    d['done']['home_href'] = HOME[lang]
    qs = []
    for q in src['questions']:
        item = {k: v for k, v in q.items() if k not in ('options', 'fields', 'section', 'q', 'hint', 'placeholder', 'min_label', 'max_label', 'consent')}
        for k in ('section', 'q', 'hint', 'placeholder', 'min_label', 'max_label', 'consent'):
            if k in q:
                item[k] = q[k][lang]
        if 'options' in q:
            item['options'] = [{'v': o['v'], 'label': o[lang]} for o in q['options']]
        if 'fields' in q:
            item['fields'] = [{'id': f['id'], 'type': f['type'], 'label': f[lang], 'autocomplete': f.get('autocomplete', 'off')} for f in q['fields']]
        qs.append(item)
    d['questions'] = qs
    return d


def page(lang, data):
    en_path, ar_path = '/clinic-survey/', '/ar/clinic-survey/'
    m = META[lang]
    h = shared.head(lang=lang, title=m['title'], desc=m['desc'], en_path=en_path, ar_path=ar_path,
                    css=f'/clinic-survey/assets/css/site.css?v={V}', og_image='/vet-charted/assets/img/dashboard.webp',
                    og_alt='Vet Charted', robots='noindex, nofollow')
    ui = UI[lang]
    payload = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    back = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>')
    nxt = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')
    body = f'''{shared.single(shared.header(None), lang)}<main class="sv-main" id="main">
  <div class="sv-top" aria-hidden="true"><i id="svBar"></i></div>
  <div class="sv-stage"><div class="sv-card" id="svCard"></div></div>
  <div class="sv-nav" id="svNav" hidden>
    <div class="sv-nav-in">
      <button type="button" class="btn btn-outline" id="svBack">{back}<span>{ui['back']}</span></button>
      <span class="sv-keys"><kbd>{ui['keysEnter']} ↵</kbd></span>
      <button type="button" class="btn btn-solid" id="svNext"><span class="lbl">{ui['next']}</span>{nxt}</button>
    </div>
  </div>
  <noscript><p class="sv-noscript">{'يحتاج الاستبيان إلى تفعيل JavaScript في المتصفح.' if lang == 'ar' else 'This survey needs JavaScript enabled in your browser.'}</p></noscript>
</main>
<footer class="sv-foot"><div class="in">
  <a class="brand-link" href="{ '/ar/' if lang == 'ar' else '/' }" aria-label="Inturp"><img src="/inturp-logo.png" alt="" width="44" height="44" style="width:26px;height:26px"><span style="font-size:20px">inturp.</span></a>
  <a href="{ '/ar/privacy/' if lang == 'ar' else '/privacy/' }">{'الخصوصية' if lang == 'ar' else 'Privacy'}</a>
  <a href="mailto:info@inturp.com" dir="ltr">info@inturp.com</a>
  <span>© <span id="year">2026</span> Inturp</span>
</div></footer>
<script type="application/json" id="sv-data">{payload}</script>
<script src="/clinic-survey/assets/js/survey-config.js?v={V}"></script>
<script src="/clinic-survey/assets/js/survey.js?v={V}"></script>
</body>
</html>
'''
    return h + body


def main():
    src = json.loads((HERE / 'survey' / 'questions.json').read_text(encoding='utf-8'))
    # stylesheet = the shared Inturp styles + the survey styles
    base = (SITE / 'alameer' / 'assets' / 'css' / 'site.css').read_text(encoding='utf-8')
    (ASSETS / 'css').mkdir(parents=True, exist_ok=True)
    (ASSETS / 'js').mkdir(parents=True, exist_ok=True)
    (ASSETS / 'css' / 'site.css').write_text(base + (HERE / 'survey' / 'survey.css').read_text(encoding='utf-8'), encoding='utf-8')
    shutil.copy2(HERE / 'survey' / 'survey.js', ASSETS / 'js' / 'survey.js')
    cfg = ASSETS / 'js' / 'survey-config.js'
    if not cfg.exists():
        shutil.copy2(HERE / 'survey' / 'survey-config.js', cfg)
    # the backend validates answers against the same questions
    schema = {'id': SURVEY_ID, 'questions': []}
    for q in src['questions']:
        item = {'id': q['id'], 'type': q['type'], 'required': q.get('required', True)}
        if 'max' in q: item['max'] = q['max']
        if 'showIf' in q: item['showIf'] = q['showIf']
        if 'options' in q: item['options'] = [o['v'] for o in q['options']]
        if 'fields' in q: item['fields'] = [f['id'] for f in q['fields']]
        schema['questions'].append(item)
    (HERE / 'survey' / 'functions' / 'survey-schema.json').write_text(json.dumps(schema, ensure_ascii=False, indent=1), encoding='utf-8')
    for lang in ('en', 'ar'):
        OUT[lang].mkdir(parents=True, exist_ok=True)
        (OUT[lang] / 'index.html').write_text(page(lang, lang_data(src, lang)), encoding='utf-8')
    n = sum(1 for q in src['questions'] if 'showIf' not in q)
    print(f'survey built: {n} questions (+ conditional)')


if __name__ == '__main__':
    main()
