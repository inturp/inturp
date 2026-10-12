import { createFileRoute, Link } from "@tanstack/react-router";
import { SiteNav, SiteFooter } from "@/components/site-chrome";
import { useLang } from "@/lib/lang";

import { ProductPreview } from "@/components/product-preview";

const vetchartedUrl = "/vetcharted-logo.png";

export const Route = createFileRoute("/vetcharted")({
  component: VetChartedPage,
  head: () => ({
    meta: [
      { title: "VetCharted | Clinic management by Inturp" },
      {
        name: "description",
        content:
          "VetCharted is an affordable, easy to use clinic management app covering appointments, medical records, and patient history for veterinary clinics.",
      },
      { property: "og:title", content: "VetCharted | Clinic management by Inturp" },
      {
        property: "og:description",
        content:
          "VetCharted is an affordable, easy to use clinic management app covering appointments, medical records, and patient history for veterinary clinics.",
      },
      { property: "og:type", content: "website" },
      { property: "og:url", content: "https://inturp.com/vetcharted" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
    links: [{ rel: "canonical", href: "https://inturp.com/vetcharted" }],
  }),
});

const copy = {
  en: {
    eyebrow: "Our products",
    title: "A clinic management app built for the veterinary clinics everyone else overlooks.",
    paragraphs: [
      "VetCharted gives clinics a reliable place to run their day to day operations: appointments, medical records, patient history, and everything in between.",
      "It is affordable and far easier to use than competing solutions, while still covering every key feature a clinic actually needs.",
      "More details about VetCharted will be shared here soon.",
    ],
    cta: "Get in touch",
  },
  ar: {
    eyebrow: "منتجاتنا",
    title: "تطبيق لإدارة العيادات، مصمم للعيادات البيطرية التي يتجاهلها الجميع.",
    paragraphs: [
      "يمنح VetCharted العيادات مكاناً موثوقاً لإدارة عملياتها اليومية: المواعيد والسجلات الطبية وتاريخ الحالات وكل ما بينها.",
      "سعره في متناول الجميع، واستخدامه أسهل بكثير من الحلول المنافسة، مع تغطية كاملة لكل ميزة أساسية تحتاجها العيادة فعلياً.",
      "سنشارك المزيد من التفاصيل حول VetCharted هنا قريباً.",
    ],
    cta: "تواصل معنا",
  },
};

function VetChartedPage() {
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
                <Link
                  to="/"
                  hash="contact"
                  className="inline-flex items-center justify-center rounded-full border border-foreground bg-foreground px-8 py-3.5 text-sm font-medium text-primary-foreground transition-all duration-300 hover:bg-background hover:text-foreground"
                >
                  {t.cta}
                </Link>
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
