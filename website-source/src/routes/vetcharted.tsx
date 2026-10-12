import { pageSeo } from "@/lib/seo";
import { createFileRoute } from "@tanstack/react-router";
import { SiteNav, SiteFooter } from "@/components/site-chrome";
import { useLang } from "@/lib/lang";

import { ProductPreview } from "@/components/product-preview";

const vetchartedUrl = "/vetcharted-logo.png";

export const Route = createFileRoute("/vetcharted")({
  component: VetChartedPage,
  head: () => pageSeo("product"),
});

const copy = {
  en: {
    eyebrow: "Our products",
    title: "Veterinary clinic management, all in one place.",
    paragraphs: [
      "VetCharted gives clinics a reliable place to run their day to day operations: appointments, medical records, patient history, and everything in between.",
      "Manage animal records, examinations, vaccinations, invoices and inventory in Arabic and English.",
      "Explore animal records, appointments, billing and inventory on the Vet Charted product website.",
    ],
    cta: "Explore Vet Charted",
  },
  ar: {
    eyebrow: "منتجاتنا",
    title: "برنامج إدارة العيادات البيطرية، في مكان واحد.",
    paragraphs: [
      "يمنح VetCharted العيادات مكاناً موثوقاً لإدارة عملياتها اليومية: المواعيد والسجلات الطبية وتاريخ الحالات وكل ما بينها.",
      "أدر ملفات الحيوانات والفحوصات والتطعيمات والفواتير والمخزون بالعربية والإنجليزية.",
      "شاهد لوحة العيادة وتطبيق المالك وتفاصيل المزايا على موقع Vet Charted.",
    ],
    cta: "اكتشف Vet Charted",
  },
};

export function VetChartedPage() {
  const { lang, rtl } = useLang();
  const t = copy[lang];

  return (
    <div dir={rtl ? "rtl" : "ltr"} className="min-h-screen bg-background text-foreground">
      <SiteNav />
      <main id="main">
        <section className="product-intro section-padding section-space">
          <div className="product-page-grid">
            <div className="product-page-copy">
              <p className="text-sm font-medium uppercase tracking-widest text-muted-foreground">
                {t.eyebrow}
              </p>
              <div className="mt-8">
                <img
                  src={vetchartedUrl}
                  alt="VetCharted"
                  className="h-28 w-auto sm:h-36 dark:invert"
                />
              </div>
              <h1 className="text-balance mt-6 text-3xl font-semibold leading-snug tracking-tight sm:text-4xl">
                {t.title}
              </h1>
              <div className="mt-10 space-y-6 text-lg leading-relaxed text-muted-foreground">
                {t.paragraphs.map((p) => (
                  <p key={p}>{p}</p>
                ))}
              </div>
              <div className="mt-10">
                <a
                  href={lang === "ar" ? "/vet-charted/" : "/vet-charted/en/"}
                  className="inline-flex items-center justify-center rounded-full border border-foreground bg-foreground px-8 py-3.5 text-sm font-medium text-primary-foreground transition-all duration-300 hover:bg-background hover:text-foreground"
                >
                  {t.cta}
                </a>
              </div>
            </div>
            <ProductPreview />
          </div>
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}
