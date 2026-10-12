import { useLang } from "@/lib/lang";
const questions = {
  en: [
    [
      "What does Inturp do?",
      "Inturp builds software products around business needs, from identifying an opportunity to developing the tools that support it.",
    ],
    [
      "What is Vet Charted?",
      "Vet Charted is our veterinary clinic management software. It brings animal records, examinations, vaccinations, appointments, invoices and inventory together.",
    ],
    [
      "Where can I explore Vet Charted?",
      "Visit the Vet Charted product website using the link below to explore the clinic dashboard, owner app and product features.",
    ],
    [
      "How can I contact Inturp?",
      "Email info@inturp.com for product enquiries, partnerships and support. You can also prepare a demo request from the Vet Charted website.",
    ],
  ],
  ar: [
    [
      "ماذا تعمل انتيرب؟",
      "نبني منتجات برمجية انطلاقاً من احتياجات الأعمال، من اكتشاف الفرصة إلى تطوير الأدوات التي تساعد على تشغيلها.",
    ],
    [
      "ما هو Vet Charted؟",
      "برنامجنا لإدارة العيادات البيطرية، يجمع ملفات الحيوانات والفحوصات والتطعيمات والمواعيد والفواتير والمخزون.",
    ],
    [
      "أين أستطيع مشاهدة تفاصيل البرنامج؟",
      "زر موقع Vet Charted من الرابط أدناه لتشاهد لوحة إدارة العيادة وتطبيق المالك ومزايا البرنامج.",
    ],
    [
      "كيف أتواصل مع انتيرب؟",
      "راسل info@inturp.com للاستفسار عن المنتجات أو الشراكات أو الدعم، ويمكنك أيضاً تجهيز طلب عرض من موقع Vet Charted.",
    ],
  ],
};
export function SiteFaq() {
  const { lang } = useLang();
  return (
    <section id="faq" className="site-faq section-padding section-space">
      <div className="mx-auto max-w-3xl">
        <p className="text-sm uppercase tracking-widest text-muted-foreground">
          {lang === "ar" ? "إجابات واضحة" : "Good to know"}
        </p>
        <h2 className="mt-5 text-3xl font-semibold tracking-tight sm:text-4xl">
          {lang === "ar" ? "الأسئلة الشائعة" : "Frequently asked questions"}
        </h2>
        <div className="faq-items">
          {questions[lang].map(([question, answer]) => (
            <details key={question}>
              <summary>
                {question}
                <span aria-hidden="true">+</span>
              </summary>
              <p>{answer}</p>
            </details>
          ))}
        </div>
        <a
          className="nav-link mt-6 inline-flex"
          href={lang === "ar" ? "/vet-charted/" : "/vet-charted/en/"}
        >
          {lang === "ar" ? "اكتشف Vet Charted ←" : "Explore Vet Charted →"}
        </a>
      </div>
    </section>
  );
}
