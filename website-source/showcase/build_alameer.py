#!/usr/bin/env python3
"""Builds the Al Ameer case study in both languages: /alameer/ and /ar/alameer/ with privacy and delete-account pages.

  python3 website-source/showcase/build_alameer.py
"""
import re, pathlib, json, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import shared

SITE_DIR = pathlib.Path(__file__).resolve().parents[2]
root = SITE_DIR / 'alameer'
ar_root = SITE_DIR / 'ar' / 'alameer'
ORIGIN = 'https://inturp.com'
UPDATED = '2026-10-12'
V = '20261030'
CSS = f'/alameer/assets/css/site.css?v={V}'
JS = f'/alameer/assets/js/site.js?v={V}'
PLAY = 'https://play.google.com/store/apps/details?id=com.h1apps.alameer_hydraulics'
APPLE = 'https://apps.apple.com/us/app/alameer-hydraulics/id6748326392'
LINKS = {'/alameer/privacy/': '/ar/alameer/privacy/', '/alameer/delete-account/': '/ar/alameer/delete-account/', '/alameer/': '/ar/alameer/'}


def chrome_head():
    return shared.header('alameer')


def chrome_foot():
    return shared.footer('alameer', ('/alameer/privacy/', '/ar/alameer/privacy/'), ('/alameer/delete-account/', '/ar/alameer/delete-account/'),
                         'خصوصية تطبيق الأمير', 'Al Ameer app privacy') + f'\n<script src="{JS}"></script>'


def localize(html):
    for en, ar in LINKS.items():
        html = html.replace(f'href="{en}"', f'href="{en}" data-ar-href="{ar}" data-en-href="{en}" data-attrs="href"')
    return html


def emit(rel, title, desc, body_dual, ld_fn=None, extra_end=''):
    for lang in ('en', 'ar'):
        en_path, ar_path = '/alameer/' + rel, '/ar/alameer/' + rel
        ld = ('<script type="application/ld+json">' + json.dumps(ld_fn(lang), ensure_ascii=False) + '</script>\n') if ld_fn else ''
        html = shared.head(lang=lang, title=title[lang], desc=desc[lang], en_path=en_path, ar_path=ar_path, css=CSS,
                           og_image='/alameer/assets/img/og.jpg', og_alt='Al Ameer Hydraulics app screens' if lang == 'en' else 'شاشات تطبيق محلات الأمير', extra=ld)
        html += chrome_head() + body_dual + chrome_foot() + extra_end + '\n</body>\n</html>\n'
        html = shared.single(localize(html), lang)
        out = (root if lang == 'en' else ar_root) / rel / 'index.html'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding='utf-8')


def page(title_ar, title_en, desc, canonical, body, page_id, desc_ar=None):
    extra = ''
    m = re.search(r'<script>\s*\(function\(\)\{.*?</script>\s*$', body, re.S)
    if m:
        extra, body = m.group(0), body[:m.start()]
    emit(canonical, {'en': title_en, 'ar': title_ar}, {'en': desc, 'ar': desc_ar or DESC_AR[page_id]},
         '<main id="main">\n' + body + '\n</main>', None, extra)


DESC_AR = {
    'privacy': 'سياسة خصوصية تطبيق محلات الأمير: البيانات التي يجمعها ولماذا ومع من تُشارَك وكيف تحذفها.',
    'delete': 'كيف تحذف حسابك في تطبيق محلات الأمير: من داخل التطبيق أو بطلب، وما الذي يُحذف وما الذي يبقى.',
}


def sec(n, ar_t, en_t, ar_b, en_b):
    return f'''<section id="s{n}">
<h2><span class="n">{n}</span><span class="ar">{ar_t}</span><span class="en">{en_t}</span></h2>
<div class="ar">{ar_b}</div><div class="en">{en_b}</div>
</section>'''


# ---------------------------------------------------------------- PRIVACY
P = []
P.append(sec(1, 'من نحن', 'Who we are',
 '''<p>تطبيق <b>محلات الأمير (Alameer Hydraulics)</b> هو تطبيق متجر لقطع غيار المعدات الثقيلة والهيدروليك والآليات، تشغّله شركة الأمير وفروعها في فلسطين والأردن ومصر. صُمّم التطبيق وطُوّر بواسطة <b>Inturp</b>، وتخضع هذه السياسة لكل ما يجمعه التطبيق ويعالجه.</p>
<p>في هذه السياسة تعني «نحن» شركة الأمير بصفتها صاحبة التطبيق، ومعها Inturp بصفتها الجهة المطوّرة التي تدعم تشغيله تقنياً.</p>''',
 '''<p>The <b>Al Ameer Hydraulics</b> app is a store for heavy-equipment spare parts, hydraulics and machines, run by Al Ameer and its branches in Palestine, Jordan and Egypt. The app was designed and built by <b>Inturp</b>. This policy covers what the app collects and how it is handled.</p>
<p>“We” means Al Ameer as the owner of the app, together with Inturp as the developer that supports its technical operation.</p>'''))

P.append(sec(2, 'البيانات التي نجمعها', 'What we collect',
 '''<p>نجمع فقط ما يلزم لتشغيل المتجر. يوضح الجدول أدناه كل نوع وسبب جمعه.</p>
<div class="tbl-wrap"><table class="tbl"><thead><tr><th>البيانات</th><th>متى وكيف</th><th>الغرض</th></tr></thead><tbody>
<tr><td>الحساب: الاسم الكامل والبريد الإلكتروني ورقم الهاتف والجنس وصورة الحساب</td><td>عند تسجيل الدخول عبر Google أو Apple أو البريد الإلكتروني، وعند تعبئة ملفك الشخصي</td><td>إنشاء حسابك وتعريفك وتنفيذ طلباتك والتواصل معك</td></tr>
<tr><td>العنوان الكامل: الاسم والهاتف والمنطقة والمدينة وتفاصيل العنوان</td><td>عندما تضيف عنوان توصيل</td><td>توصيل الطلبات</td></tr>
<tr><td>الطلبات: المنتجات والكميات والمبالغ وطريقة التسلّم (توصيل أو استلام من فرع) واسم مستلم الطلب ورقمه</td><td>عند إتمام الطلب</td><td>تجهيز الطلب وتوصيله وحفظ سجل مشترياتك</td></tr>
<tr><td>طريقة تسجيل الدخول: Google أو Apple أو البريد الإلكتروني أو الهاتف</td><td>عند تسجيل الدخول</td><td>التحقق من هويتك وحماية الحساب</td></tr>
<tr><td>السلة والمفضلة</td><td>عند إضافة منتجات إليهما</td><td>حفظ اختياراتك بين الجلسات</td></tr>
<tr><td>رسائل الدعم والصور التي ترسلها في المحادثة</td><td>عند مراسلة فريق الدعم</td><td>الرد عليك وحل مشكلتك</td></tr>
<tr><td>التقييمات التي تكتبها للمنتجات</td><td>بعد استلام الطلب</td><td>تحسين الخدمة والمنتجات</td></tr>
<tr><td>معرّف الإشعارات (push token) ومعلومات الجهاز الأساسية</td><td>عند السماح بالإشعارات</td><td>إرسال إشعارات الطلبات والعروض والرد على الدعم</td></tr>
<tr><td>أحداث استخدام مجمّعة: عرض منتج، إضافة للسلة، استخدام كود خصم، بدء الدفع</td><td>أثناء استخدام التطبيق</td><td>قياس أداء التطبيق والإعلانات (انظر القسم 5)</td></tr>
</tbody></table></div>
<h3>كيف نجمع المعلومات</h3>
<ul class="list"><li>إدخالك المباشر عند التسجيل أو تعديل ملفك الشخصي أو إضافة عنوان.</li><li>مزودو تسجيل الدخول مثل Google وApple، عند اختيارك الدخول بهم.</li><li>تلقائياً عبر Firebase Messaging (رمز الجهاز لإرسال الإشعارات).</li></ul>
<div class="note"><div><b>ما لا نجمعه</b> لا نطلب موقعك الجغرافي من جهازك، ولا جهات اتصالك، ولا ميكروفونك. لا توجد مدفوعات إلكترونية داخل التطبيق: يتم الدفع عند الاستلام أو في الفرع، فلا نجمع أو نخزّن بيانات بطاقات أو معلومات مصرفية.</div></div>''',
 '''<p>We collect only what is needed to run the store. The table shows each type of data and why.</p>
<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Data</th><th>When and how</th><th>Purpose</th></tr></thead><tbody>
<tr><td>Account: full name, email, phone number, gender and profile photo</td><td>When you sign in with Google, Apple or email, and when you fill in your profile</td><td>Create and identify your account, fulfil orders and contact you</td></tr>
<tr><td>Full address: name, phone, region, city and address details</td><td>When you add a delivery address</td><td>Deliver orders</td></tr>
<tr><td>Orders: products, quantities, totals, delivery or branch pickup, and the pickup recipient’s name and phone</td><td>When you place an order</td><td>Prepare and deliver the order and keep your purchase history</td></tr>
<tr><td>Sign-in method: Google, Apple, email or phone</td><td>When you sign in</td><td>Verify who you are and protect the account</td></tr>
<tr><td>Cart and favorites</td><td>When you add products to them</td><td>Keep your selections between sessions</td></tr>
<tr><td>Support messages and photos you send in chat</td><td>When you message the support team</td><td>Reply to you and resolve your issue</td></tr>
<tr><td>Product ratings you write</td><td>After receiving an order</td><td>Improve service and products</td></tr>
<tr><td>Notification token and basic device information</td><td>When you allow notifications</td><td>Send order updates, offers and support replies</td></tr>
<tr><td>Usage events: product views, add to cart, discount-code use, checkout start</td><td>While you use the app</td><td>Measure app and advertising performance (see section 5)</td></tr>
</tbody></table></div>
<h3>How we collect it</h3>
<ul class="list"><li>Directly from you when you register, edit your profile or add an address.</li><li>From sign-in providers such as Google and Apple, when you choose them.</li><li>Automatically through Firebase Messaging (the device token used for notifications).</li></ul>
<div class="note"><div><b>What we do not collect</b> We do not request your device location, your contacts or your microphone. There are no online payments in the app: you pay on delivery or at the branch, so we do not collect or store card or banking details.</div></div>'''))

P.append(sec(3, 'كيف نستخدم بياناتك', 'How we use your data',
 '''<ul class="list"><li>تشغيل حسابك وتسجيل دخولك وحماية الحساب.</li><li>معالجة الطلبات وتوصيلها أو تجهيزها للاستلام من الفرع، وتطبيق أكواد الخصم.</li><li>الرد على استفساراتك وطلبات الأسعار ورسائل الدعم.</li><li>إرسال إشعارات تخص طلباتك، وإشعارات عروض تستطيع إيقافها من إعدادات جهازك.</li><li>إرسال عروض وخصومات مخصصة لك، والإعلام بحالة الطلبات والتنبيهات المهمة.</li><li>الحفاظ على سجلات الطلبات لأغراض محاسبية وقانونية.</li><li>تحسين تجربتك وإجراء تحليلات أساسية لتحسين الخدمة، ومنع إساءة الاستخدام.</li></ul>
<p>لا نبيع بياناتك الشخصية.</p>''',
 '''<ul class="list"><li>Run your account, sign you in and keep it secure.</li><li>Process orders, deliver them or prepare them for branch pickup, and apply discount codes.</li><li>Answer your questions, price requests and support messages.</li><li>Send notifications about your orders, and offer notifications that you can turn off in your device settings.</li><li>Send you personalised offers and discounts, and tell you about order status and important notices.</li><li>Keep order records for accounting and legal purposes.</li><li>Improve your experience, run basic analytics and service optimisation, and prevent abuse.</li></ul>
<p>We do not sell your personal data.</p>'''))

P.append(sec(4, 'مع من نشارك البيانات', 'Who we share it with',
 '''<p>نشارك البيانات فقط مع من يلزم لتشغيل الخدمة:</p>
<ul class="list"><li><b>فريق شركة الأمير وفروعها:</b> الذين يعالجون الطلبات ويردّون على الدعم، بحسب صلاحياتهم.</li><li><b>Google (Firebase):</b> للمصادقة وقاعدة البيانات والملفات والوظائف السحابية وإشعارات الدفع.</li><li><b>شركة التوصيل:</b> اسمك ورقم هاتفك وعنوان التوصيل، لغرض تسليم طلبك فقط.</li><li><b>Apple:</b> عند اختيارك تسجيل الدخول عبر Apple.</li><li><b>Cloudinary:</b> لاستضافة صور المنتجات والمحتوى وتقديمها.</li><li><b>Meta:</b> أحداث الاستخدام المذكورة في القسم 5.</li><li><b>جهات قانونية:</b> عند وجود التزام قانوني أو طلب رسمي صحيح.</li></ul>
<p>تعالج هذه الجهات البيانات بموجب شروطها الخاصة وبالنيابة عنا لتقديم الخدمة.</p>''',
 '''<p>We share data only with those needed to run the service:</p>
<ul class="list"><li><b>The Al Ameer team and branches:</b> who process orders and answer support, according to their permissions.</li><li><b>Google (Firebase):</b> for authentication, database, file storage, cloud functions and push notifications.</li><li><b>The delivery service:</b> your name, phone number and delivery address, solely to deliver your order.</li><li><b>Apple:</b> when you choose to sign in with Apple.</li><li><b>Cloudinary:</b> to host and deliver product and content images.</li><li><b>Meta:</b> the usage events described in section 5.</li><li><b>Legal authorities:</b> where we have a legal obligation or a valid official request.</li></ul>
<p>These providers process data under their own terms and on our behalf to deliver the service.</p>'''))

P.append(sec(5, 'التحليلات والإعلانات', 'Analytics and advertising',
 '''<p>يستخدم التطبيق أداة قياس من Meta لتسجيل أحداث استخدام مجمّعة، مثل عرض منتج أو إضافته للسلة أو استخدام كود خصم أو بدء إتمام الطلب، بهدف فهم أداء التطبيق والإعلانات.</p>
<p>على أجهزة iPhone يطلب نظام iOS إذنك قبل أي تتبع عبر التطبيقات، ويمكنك رفضه أو تغيير قرارك لاحقاً من <b>الإعدادات ← الخصوصية والأمان ← التتبع</b>. على أندرويد يمكنك إعادة ضبط معرّف الإعلانات أو إلغاء تخصيص الإعلانات من إعدادات جهازك.</p>''',
 '''<p>The app uses a Meta measurement tool to record aggregated usage events, such as viewing a product, adding to cart, using a discount code or starting checkout, to understand app and advertising performance.</p>
<p>On iPhone, iOS asks for your permission before any cross-app tracking; you can decline or change your decision later in <b>Settings → Privacy &amp; Security → Tracking</b>. On Android you can reset your advertising ID or opt out of ad personalisation in your device settings.</p>'''))

P.append(sec(6, 'أذونات الجهاز', 'Device permissions',
 '''<ul class="list"><li><b>الإشعارات:</b> لإرسال تحديثات الطلبات والعروض. اختيارية.</li><li><b>الصور والكاميرا:</b> فقط عندما تختار إرفاق صورة في محادثة الدعم. يستخدم التطبيق منتقي الصور الخاص بالنظام، ولا يصل إلى مكتبة صورك كاملة.</li><li><b>الإنترنت:</b> لازم لعمل التطبيق.</li></ul>''',
 '''<ul class="list"><li><b>Notifications:</b> to send order updates and offers. Optional.</li><li><b>Photos and camera:</b> only when you choose to attach a picture in support chat. The app uses the system photo picker and cannot browse your whole library.</li><li><b>Internet:</b> required for the app to work.</li></ul>'''))

P.append(sec(7, 'مدة الاحتفاظ والحذف', 'Retention and deletion',
 '''<p>نحتفظ بحسابك وبياناته ما دام حسابك قائماً. يمكنك حذف حسابك في أي وقت من داخل التطبيق (الملف الشخصي ← حذف الحساب نهائياً)، أو بطلب منا. التفاصيل الكاملة في <a class="lnk" href="/alameer/delete-account/">صفحة حذف الحساب</a>.</p>
<ul class="list"><li><b>يُحذف فوراً:</b> ملفك الشخصي وعناوينك المحفوظة وسلتك ومفضلتك وحساب الدخول.</li><li><b>قد يُحتفظ به:</b> سجلات الطلبات السابقة لأغراض محاسبية وقانونية، وكذلك رسائل الدعم والتقييمات. يمكنك طلب إزالتها أو إخفاء هويتك منها وسنستجيب إلا حيث يلزمنا القانون بالاحتفاظ بها.</li></ul>''',
 '''<p>We keep your account and its data while your account exists. You can delete your account at any time inside the app (Profile → Delete account permanently) or by asking us. Full details are on the <a class="lnk" href="/alameer/delete-account/">account deletion page</a>.</p>
<ul class="list"><li><b>Deleted immediately:</b> your profile, saved addresses, cart, favorites and sign-in account.</li><li><b>May be kept:</b> past order records for accounting and legal reasons, plus support messages and ratings. You can ask us to remove them or detach your identity from them, and we will, except where the law requires us to keep them.</li></ul>'''))

P.append(sec(8, 'الأمان', 'Security',
 '''<p>تنتقل بياناتك عبر اتصال مشفّر، وتُخزَّن لدى مزوّدي خدمات سحابية معروفين. يُنشأ الطلب ويُتحقق منه على الخادم، وتقيّد قواعد الوصول ما يراه كل مستخدم بحسب صلاحية حسابه. لا يوجد نظام آمن بالكامل، لكننا نعمل على حماية بياناتك ونراجع ذلك باستمرار.</p>''',
 '''<p>Your data travels over encrypted connections and is stored with established cloud providers. Orders are created and checked on the server, and access rules limit what each user can see according to their account role. No system is perfectly secure, but we work to protect your data and review this continuously.</p>'''))

P.append(sec(9, 'حقوقك', 'Your rights',
 '''<p>يحق لك طلب الاطلاع على بياناتك أو تصحيحها أو حذفها، والاعتراض على معالجتها، وسحب موافقتك على الإشعارات والتحليلات في أي وقت. تستطيع تعديل معظم بياناتك من الملف الشخصي مباشرة. لأي طلب آخر راسلنا على العنوان في القسم 12.</p>''',
 '''<p>You may ask to access, correct or delete your data, object to its processing, and withdraw your consent to notifications and analytics at any time. You can edit most of your data directly in your profile. For anything else, write to us at the address in section 12.</p>'''))

P.append(sec(10, 'الأطفال', 'Children',
 '''<p>التطبيق موجّه للبالغين وأصحاب الورش والشركات، وليس للأطفال دون 13 عاماً، ولا نجمع بيانات منهم عن قصد. إن علمتَ أن طفلاً أنشأ حساباً فأخبرنا لنحذفه.</p>''',
 '''<p>The app is for adults, workshops and companies, not for children under 13, and we do not knowingly collect their data. If you know a child has created an account, tell us and we will delete it.</p>'''))

P.append(sec(11, 'النقل الدولي والتغييرات', 'International transfers and changes',
 '''<p>قد تُعالَج بياناتك على خوادم تقع خارج بلدك، ومنها خوادم في أوروبا والولايات المتحدة لدى مزوّدي الخدمات السحابية. وقد نحدّث هذه السياسة عند تغيّر التطبيق أو القانون، ونعدّل تاريخ آخر تحديث أعلى الصفحة. الاستمرار في استخدام التطبيق بعد التحديث يعني قبوله.</p>''',
 '''<p>Your data may be processed on servers outside your country, including in Europe and the United States, with our cloud providers. We may update this policy when the app or the law changes and will change the “last updated” date at the top. Continuing to use the app after an update means you accept it.</p>'''))

P.append(sec(12, 'تواصل معنا', 'Contact us',
 '''<p>لأي سؤال أو طلب يخص الخصوصية أو بياناتك، راسلنا وسنرد عليك.</p>
<div class="contact-card"><div><b>أسئلة أو طلبات الخصوصية؟</b><p><a class="lnk latin" href="mailto:info@inturp.com">info@inturp.com</a> · <a class="lnk latin" href="mailto:ali@alameer.ps">ali@alameer.ps</a> · <a class="lnk latin" href="tel:+972592470352">+972 59-247-0352</a></p></div><a class="btn btn-light" href="mailto:info@inturp.com">راسلنا</a></div>''',
 '''<p>For any privacy question or request about your data, write to us and we will reply.</p>
<div class="contact-card"><div><b>Privacy questions or requests?</b><p><a class="lnk latin" href="mailto:info@inturp.com">info@inturp.com</a> · <a class="lnk latin" href="mailto:ali@alameer.ps">ali@alameer.ps</a> · <a class="lnk latin" href="tel:+972592470352">+972 59-247-0352</a></p></div><a class="btn btn-light" href="mailto:info@inturp.com">Email us</a></div>'''))

toc_titles = [
 ('من نحن', 'Who we are'), ('ما نجمعه', 'What we collect'), ('الاستخدام', 'How we use it'), ('المشاركة', 'Sharing'),
 ('التحليلات', 'Analytics'), ('الأذونات', 'Permissions'), ('الاحتفاظ والحذف', 'Retention'), ('الأمان', 'Security'),
 ('حقوقك', 'Your rights'), ('الأطفال', 'Children'), ('النقل والتغييرات', 'Transfers'), ('التواصل', 'Contact')]
toc = ''.join(f'<li><a href="#s{i+1}"><span class="ar">{a}</span><span class="en">{e}</span></a></li>' for i, (a, e) in enumerate(toc_titles))

privacy_body = f'''<section class="legal-hero section-padding">
  <div class="inner">
    <h1><span class="ar">سياسة الخصوصية</span><span class="en">Privacy policy</span></h1>
    <p><span class="ar">كيف يتعامل تطبيق محلات الأمير مع بياناتك: ماذا نجمع، ولماذا، ومع من نشاركه، وكيف تتحكم به.</span><span class="en">How the Al Ameer Hydraulics app handles your data: what we collect, why, who we share it with, and how you stay in control.</span></p>
    <div class="meta"><span><span class="ar">آخر تحديث:</span><span class="en">Last updated:</span> <b class="latin">{UPDATED}</b></span><span><span class="ar">سارية منذ:</span><span class="en">Effective since:</span> <b class="latin">2025-06-22</b></span><span><span class="ar">التطبيق:</span><span class="en">App:</span> <b><span class="ar">محلات الأمير</span><span class="en">Al Ameer Hydraulics</span></b></span><span><a class="lnk" href="/alameer/delete-account/" style="border-bottom:1px solid var(--muted)"><span class="ar">حذف الحساب ←</span><span class="en">Delete your account →</span></a></span></div>
  </div>
</section>
<div class="section-padding"><div class="doc-wrap inner">
  <aside class="toc" aria-label="Contents" data-ar-aria-label="المحتويات" data-en-aria-label="Contents" data-attrs="aria-label"><b><span class="ar">المحتويات</span><span class="en">Contents</span></b><ol>{toc}</ol></aside>
  <article class="doc">
{chr(10).join(P)}
  </article>
</div></div>'''

page(
    'سياسة الخصوصية — محلات الأمير', 'Privacy policy — Al Ameer Hydraulics',
    'Privacy policy for the Al Ameer Hydraulics app: what data it collects, why, who it is shared with, and how to delete it.',
    'privacy/', privacy_body, 'privacy')

# ---------------------------------------------------------------- DELETE ACCOUNT
D = []
D.append(sec(1, 'الطريقة الأسرع: من داخل التطبيق', 'Fastest way: inside the app',
 '''<p>إن كنتَ تستطيع تسجيل الدخول، فاحذف حسابك بنفسك في أقل من دقيقة:</p>
<ol class="steps-l">
<li><b>افتح التطبيق وسجّل الدخول</b><span>إن كان آخر تسجيل دخول لك قديماً، سجّل الخروج ثم ادخل من جديد. يشترط الحذف تسجيل دخول خلال آخر 5 دقائق لحماية حسابك.</span></li>
<li><b>افتح ملفك الشخصي</b><span>من الإعدادات ثم «الملف الشخصي».</span></li>
<li><b>اضغط «حذف الحساب نهائياً»</b><span>ثم أكّد في نافذة التأكيد.</span></li>
</ol>
<p>عند نجاح الحذف يُسجَّل خروجك ويعود التطبيق إلى الشاشة الرئيسية. لا يمكن التراجع عن العملية.</p>''',
 '''<p>If you can sign in, you can delete your account yourself in under a minute:</p>
<ol class="steps-l">
<li><b>Open the app and sign in</b><span>If your last sign-in was a while ago, sign out and sign back in. Deletion requires a sign-in within the last 5 minutes to protect your account.</span></li>
<li><b>Open your profile</b><span>From Settings, then “Profile”.</span></li>
<li><b>Tap “Delete account permanently”</b><span>Then confirm in the dialog.</span></li>
</ol>
<p>When deletion succeeds you are signed out and the app returns to the home screen. This cannot be undone.</p>'''))

D.append(sec(2, 'ما الذي يُحذف وما الذي يبقى', 'What is deleted and what stays',
 '''<div class="two">
<div class="box del"><h3>يُحذف فوراً</h3><ul class="list"><li>ملفك الشخصي: الاسم والبريد والهاتف والصورة</li><li>عناوينك المحفوظة</li><li>سلة المشتريات والمفضلة</li><li>حساب تسجيل الدخول نفسه، فلن تستطيع الدخول به مجدداً</li></ul></div>
<div class="box keep"><h3>قد يبقى</h3><ul class="list"><li>سجلات الطلبات السابقة، لأنها مستندات محاسبية وقانونية للشركة</li><li>رسائل الدعم والتقييمات التي أرسلتها</li><li>سجلات تقنية مؤقتة لدى مزوّدي الخدمات السحابية حتى تنتهي دورة حذفها المعتادة</li></ul></div>
</div>
<div class="note"><div>إن أردتَ إزالة ما قد يبقى أو إخفاء هويتك منه، أرسل لنا طلباً بالطريقة التالية وسنعالجه إلا حيث يلزمنا القانون بالاحتفاظ به.</div></div>''',
 '''<div class="two">
<div class="box del"><h3>Deleted immediately</h3><ul class="list"><li>Your profile: name, email, phone and photo</li><li>Your saved addresses</li><li>Your cart and favorites</li><li>The sign-in account itself, so you cannot sign in with it again</li></ul></div>
<div class="box keep"><h3>May stay</h3><ul class="list"><li>Past order records, because they are accounting and legal documents for the business</li><li>Support messages and ratings you sent</li><li>Temporary technical logs at our cloud providers until their normal deletion cycle ends</li></ul></div>
</div>
<div class="note"><div>If you want what may stay removed, or your identity detached from it, send us a request as described below and we will handle it, except where the law requires us to keep it.</div></div>'''))

form_ar = '''<p>إن لم تستطع تسجيل الدخول، أو أردتَ إزالة بيانات مثل رسائل الدعم والتقييمات، فأرسل لنا طلباً. عبّئ الحقول وسيفتح بريدك رسالة جاهزة نستلمها على <span class="latin">info@inturp.com</span>.</p>'''
form_en = '''<p>If you cannot sign in, or want data such as support messages and ratings removed, send us a request. Fill in the fields and your email app opens a ready message that reaches us at <span class="latin">info@inturp.com</span>.</p>'''
form_html = '''
<form class="formcard" id="delForm" novalidate>
  <label><span class="ar">البريد الإلكتروني أو رقم الهاتف المرتبط بالحساب</span><span class="en">Email or phone linked to the account</span>
    <input id="delId" type="text" autocomplete="email" required></label>
  <label><span class="ar">الاسم الظاهر في الحساب (اختياري)</span><span class="en">Name on the account (optional)</span>
    <input id="delName" type="text" autocomplete="name"></label>
  <label><span class="ar">ماذا تريد أن نحذف؟</span><span class="en">What should we delete?</span>
    <select id="delScope">
      <option value="all" data-ar="الحساب وكل بياناته القابلة للحذف" data-en="The account and all deletable data">الحساب وكل بياناته القابلة للحذف</option>
      <option value="extra" data-ar="إزالة رسائل الدعم والتقييمات أو إخفاء هويتي منها فقط" data-en="Only remove support messages and ratings, or detach my identity from them">إزالة رسائل الدعم والتقييمات أو إخفاء هويتي منها فقط</option>
    </select></label>
  <p class="form-note" id="delErr" role="alert" hidden></p>
  <button class="btn btn-solid" type="submit"><span class="ar">افتح رسالة الطلب</span><span class="en">Open request email</span></button>
  <p class="form-note"><span class="ar">لا نرسل شيئاً عبر هذه الصفحة؛ يُنشأ الطلب في تطبيق البريد لديك وترسله أنت.</span><span class="en">Nothing is sent from this page; the request is drafted in your email app and you send it yourself.</span></p>
</form>'''
D.append(sec(3, 'لا تستطيع الدخول؟ أرسل طلباً', 'Can’t sign in? Send a request',
 form_ar + form_html, form_en))

D.append(sec(4, 'ماذا يحدث بعد طلبك', 'What happens after your request',
 '''<ol class="steps-l">
<li><b>نتحقق من هويتك</b><span>قد نطلب منك تأكيد البريد أو الرقم المرتبط بالحساب حتى لا يحذف أحد حساب غيره.</span></li>
<li><b>ننفّذ الحذف</b><span>نحذف الحساب وبياناته المذكورة أعلاه، ونزيل أو نخفي هوية ما طلبتَ إزالته إن لم يمنعنا القانون.</span></li>
<li><b>نؤكد لك</b><span>نرد عليك خلال <b>30 يوماً</b> كحد أقصى، وغالباً أسرع.</span></li>
</ol>''',
 '''<ol class="steps-l">
<li><b>We verify it is you</b><span>We may ask you to confirm the email or number linked to the account so nobody can delete someone else’s account.</span></li>
<li><b>We carry out the deletion</b><span>We delete the account and the data listed above, and remove or de-identify what you asked us to, where the law allows.</span></li>
<li><b>We confirm</b><span>We reply within <b>30 days</b> at most, usually sooner.</span></li>
</ol>'''))

D.append(sec(5, 'أسئلة؟', 'Questions?',
 '''<p>راسلنا على <a class="lnk latin" href="mailto:info@inturp.com">info@inturp.com</a> أو <a class="lnk latin" href="mailto:ali@alameer.ps">ali@alameer.ps</a>. وللتفاصيل عن بياناتنا راجع <a class="lnk" href="/alameer/privacy/">سياسة الخصوصية</a>.</p>''',
 '''<p>Write to <a class="lnk latin" href="mailto:info@inturp.com">info@inturp.com</a> or <a class="lnk latin" href="mailto:ali@alameer.ps">ali@alameer.ps</a>. For details on our data practices see the <a class="lnk" href="/alameer/privacy/">privacy policy</a>.</p>'''))

toc2 = [('من داخل التطبيق', 'In the app'), ('ما يُحذف', 'What is deleted'), ('طلب بالبريد', 'Send a request'), ('بعد الطلب', 'After your request'), ('أسئلة', 'Questions')]
toc2h = ''.join(f'<li><a href="#s{i+1}"><span class="ar">{a}</span><span class="en">{e}</span></a></li>' for i, (a, e) in enumerate(toc2))

delete_body = f'''<section class="legal-hero section-padding">
  <div class="inner">
    <h1><span class="ar">طلب حذف الحساب</span><span class="en">Delete your account</span></h1>
    <p><span class="ar">احذف حسابك في تطبيق محلات الأمير من داخل التطبيق، أو أرسل لنا طلباً إن لم تستطع تسجيل الدخول. نوضح هنا ما يُحذف وما يبقى وكم يستغرق الأمر.</span><span class="en">Delete your Al Ameer Hydraulics account inside the app, or send us a request if you cannot sign in. Here is what is deleted, what stays and how long it takes.</span></p>
    <div class="meta"><span><span class="ar">آخر تحديث:</span><span class="en">Last updated:</span> <b class="latin">{UPDATED}</b></span><span><span class="ar">التطبيق:</span><span class="en">App:</span> <b><span class="ar">محلات الأمير</span><span class="en">Al Ameer Hydraulics</span></b></span></div>
  </div>
</section>
<div class="section-padding"><div class="doc-wrap inner">
  <aside class="toc" aria-label="Contents" data-ar-aria-label="المحتويات" data-en-aria-label="Contents" data-attrs="aria-label"><b><span class="ar">المحتويات</span><span class="en">Contents</span></b><ol>{toc2h}</ol></aside>
  <article class="doc">
{chr(10).join(D)}
  </article>
</div></div>
<script>
(function(){{
  var f=document.getElementById('delForm');if(!f)return;
  f.addEventListener('submit',function(e){{
    e.preventDefault();
    var en=document.documentElement.lang==='en';
    var id=document.getElementById('delId').value.trim();
    var err=document.getElementById('delErr');
    if(!id){{err.hidden=false;err.textContent=en?'Please enter the email or phone linked to the account.':'يرجى إدخال البريد أو الهاتف المرتبط بالحساب.';return;}}
    err.hidden=true;
    var name=document.getElementById('delName').value.trim();
    var sel=document.getElementById('delScope');
    var scope=sel.options[sel.selectedIndex].getAttribute('data-'+(en?'en':'ar'));
    var subject=en?'Account deletion request — Al Ameer Hydraulics':'طلب حذف حساب — محلات الأمير';
    var body=en
      ?'Hello,\\n\\nI would like to delete my account in the Al Ameer Hydraulics app.\\n\\nAccount (email/phone): '+id+'\\nName: '+(name||'-')+'\\nRequest: '+scope+'\\n\\nThank you.'
      :'مرحباً،\\n\\nأرغب بحذف حسابي في تطبيق محلات الأمير.\\n\\nالحساب (بريد/هاتف): '+id+'\\nالاسم: '+(name||'-')+'\\nالطلب: '+scope+'\\n\\nشكراً.';
    location.href='mailto:info@inturp.com?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(body);
  }});
}})();
</script>'''

page(
    'حذف الحساب — محلات الأمير', 'Delete your account — Al Ameer Hydraulics',
    'How to delete your Al Ameer Hydraulics account: inside the app or by request, what is deleted and what stays.',
    'delete-account/', delete_body, 'delete')
FAQ = [
    ('ما هو تطبيق محلات الأمير؟', 'What is the Al Ameer Hydraulics app?',
     'تطبيق لمحلات الأمير، شركة قطع غيار وهيدروليك وآليات للمعدات الثقيلة بسبعة فروع في فلسطين والأردن ومصر. تتصفح فيه الآليات وقطع الغيار وتطلب وتتواصل مع الفريق.',
     'The app of Al Ameer, a business selling spare parts, hydraulics and machines for heavy equipment, with seven branches in Palestine, Jordan and Egypt. Browse machines and parts, order, and contact the team.'),
    ('هل أستطيع الطلب بالتوصيل أو الاستلام من الفرع؟', 'Can I order for delivery or pick up from a branch?',
     'نعم. عند إتمام الطلب تختار التوصيل إلى عنوانك المحفوظ أو الاستلام من أحد الفروع التي تدعمه: نابلس (شارع الحسبة)، ورام الله (بيتونيا)، وجماعين.',
     'Yes. At checkout you choose delivery to a saved address or pickup from a branch that supports it: Nablus (Al-Hisba Street), Ramallah (Beitunia) or Jammain.'),
    ('كيف أدفع؟', 'How do I pay?',
     'الدفع عند الاستلام أو في الفرع. لا يطلب التطبيق بيانات بطاقات ولا يجري مدفوعات إلكترونية.',
     'You pay on delivery or at the branch. The app does not ask for card details and does not take online payments.'),
    ('هل أستطيع التواصل مع الفريق عبر واتساب؟', 'Can I contact the team on WhatsApp?',
     'نعم. في صفحة كل آلية زر واتساب مباشر، وفي التطبيق محادثة دعم وصفحة تواصل.',
     'Yes. Every machine page has a direct WhatsApp button, and the app has a support chat and a contact page.'),
    ('كيف أحذف حسابي؟', 'How do I delete my account?',
     'من الإعدادات ثم الملف الشخصي ثم «حذف الحساب نهائياً». التفاصيل في صفحة حذف الحساب.',
     'From Settings, then Profile, then “Delete account permanently”. The details are on the account deletion page.'),
]


def faq_html():
    items = ''.join(f'<details><summary><span class="ar">{qa}</span><span class="en">{qe}</span><span aria-hidden="true">+</span></summary><p><span class="ar">{aa}</span><span class="en">{ae}</span></p></details>' for qa, qe, aa, ae in FAQ)
    return f'''<section class="bordered section-padding section-space" id="faq">
  <div>
    <div class="sec-head" data-reveal>
      <span class="eyebrow"><i class="status-dot"></i><span class="ar">أسئلة شائعة</span><span class="en">Questions</span></span>
      <h2><span class="ar">أسئلة عن تطبيق محلات الأمير.</span><span class="en">Questions about the Al Ameer app.</span></h2>
    </div>
    <div class="faq-items" data-reveal>{items}</div>
  </div>
</section>'''


def index_ld(lang):
    en_url, ar_url = ORIGIN + '/alameer/', ORIGIN + '/ar/alameer/'
    url = ar_url if lang == 'ar' else en_url
    desc = ('تطبيق لتصفح الآليات الثقيلة وقطع الغيار والطلب بالتوصيل أو بالاستلام من الفرع والتواصل مع فروع محلات الأمير السبعة في فلسطين والأردن ومصر.'
            if lang == 'ar' else
            "Mobile app for browsing heavy machines and spare parts, ordering for delivery or branch pickup, and contacting Al Ameer's seven branches in Palestine, Jordan and Egypt.")
    qa = [{"@type": "Question", "name": (q_ar if lang == 'ar' else q_en), "acceptedAnswer": {"@type": "Answer", "text": (a_ar if lang == 'ar' else a_en)}} for q_ar, q_en, a_ar, a_en in FAQ]
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url + "#page", "url": url, "name": "Al Ameer Hydraulics", "inLanguage": lang,
         "isPartOf": {"@id": ORIGIN + "/#website"}, "about": {"@id": ORIGIN + "/alameer/#app"}},
        {"@type": "MobileApplication", "@id": ORIGIN + "/alameer/#app", "name": "Al Ameer Hydraulics", "alternateName": "محلات الأمير",
         "operatingSystem": "Android, iOS", "applicationCategory": "BusinessApplication", "description": desc,
         "image": ORIGIN + "/alameer/assets/img/og.jpg", "url": en_url, "downloadUrl": [PLAY, APPLE],
         "inLanguage": ["ar"], "author": {"@id": ORIGIN + "/#organization"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inturp", "item": ORIGIN + ("/ar/" if lang == 'ar' else "/")},
            {"@type": "ListItem", "position": 2, "name": "Al Ameer Hydraulics", "item": url}]},
        {"@type": "FAQPage", "mainEntity": qa}]}


def build_index():
    body = (pathlib.Path(__file__).parent / 'alameer.index.body.html').read_text(encoding='utf-8')
    body = body.replace('<section class="get section-padding section-space" id="get">', faq_html() + '\n\n<section class="get section-padding section-space" id="get">', 1)
    emit('', {'en': 'Al Ameer Hydraulics app — heavy-equipment parts and machines | Inturp', 'ar': 'تطبيق محلات الأمير — قطع غيار المعدات الثقيلة والآليات | انتيرب'},
         {'en': 'Case study: the Al Ameer Hydraulics mobile app by Inturp. Browse machines and spare parts, order for delivery or branch pickup, and reach seven branches in Palestine, Jordan and Egypt.',
          'ar': 'دراسة حالة: تطبيق محلات الأمير للهيدروليك من انتيرب. تصفّح الآليات وقطع الغيار، واطلب بالتوصيل أو بالاستلام من الفرع، وتواصل مع سبعة فروع في فلسطين والأردن ومصر.'},
         body, index_ld)


build_index()
for old,new in [('privacy.html','privacy/'),('delete-account.html','delete-account/')]:
    t='https://inturp.com/alameer/'+new
    (root/old).write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Redirecting…</title>'
      f'<link rel="canonical" href="{t}"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url=/alameer/{new}">'
      f'<script>location.replace("/alameer/{new}"+location.search+location.hash)</script></head><body><a href="/alameer/{new}">{t}</a></body></html>',encoding='utf-8')
build_index()
print('alameer built')
