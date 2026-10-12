import { Instagram } from "lucide-react";
import { SiteFaq } from "@/components/site-faq";
import { pageSeo } from "@/lib/seo";
import { createFileRoute } from "@tanstack/react-router";
import { useEffect } from "react";
import { SiteNav, SiteFooter } from "@/components/site-chrome";
import { useLang } from "@/lib/lang";

import { ProductPreview } from "@/components/product-preview";
import { AlameerPreview } from "@/components/alameer-preview";
import { CheckbookPreview } from "@/components/checkbook-preview";
const vetchartedUrl = "/vetcharted-logo.png";

export const Route = createFileRoute("/")({
  component: Index,
  head: () => pageSeo("home"),
});

type Lang = "en" | "ar";

const content = {
  en: {
    nav: { about: "About", product: "Products", contact: "Contact" },
    hero: {
      title: "We find the gaps and fill them with a product that will make your business flourish",
      subtitle:
        "Inturp is a venture studio focused on turning promising ideas into successful companies, starting with the tools that power them.",
      cta: "Explore what we’re building",
    },
    about: {
      eyebrow: "About Inturp",
      title: "We build the infrastructure behind new businesses.",
      p1: "Inturp was created to do more than launch ideas. We look for meaningful business opportunities, design the software that makes them possible, and support the broader ecosystem required to turn those ideas into lasting products.",
      p2: "Our approach is deliberate: one opportunity at a time, built with care, and scaled with intention. We believe the best products are born from deep understanding, clean execution, and a clear path to real impact.",
    },

    product: {
      eyebrow: "What we’re building",
      name: "VetCharted",
      title: "Veterinary clinic management, all in one place.",
      p1: "VetCharted gives clinics a reliable place to run their day to day operations: appointments, medical records, patient history, and everything in between.",
      p2: "Manage animal records, examinations, vaccinations, invoices and inventory in Arabic and English.",
      cta: "Get in touch",
    },
    alameer: {
      eyebrow: "Our work",
      name: "Al Ameer Hydraulics",
      title: "Heavy-equipment parts and machines, in one app.",
      p1: "We designed and built the Al Ameer Hydraulics app for a business with seven branches across Palestine, Jordan and Egypt.",
      p2: "Customers browse machines and spare parts, order for delivery or branch pickup, and reach the team on WhatsApp.",
      cta: "See the case study",
    },
    checkbook: {
      eyebrow: "Our work",
      name: "CheckBook",
      title: "Every cheque, every due date, under control.",
      p1: "CheckBook is a mobile app for keeping track of cheques: amounts, banks, due dates and states, with a dashboard of totals.",
      p2: "Plan a whole series of cheques in a minute with the smart plan, and get reminded before each one falls due.",
      cta: "See the case study",
    },
    contact: {
      eyebrow: "Contact",
      title: "Let’s talk.",
      p: "Whether you’re exploring a partnership, looking for support, or just want to learn more about what we’re building, we’d love to hear from you.",
    },
    footer: "All rights reserved.",
    menuLabel: "Toggle menu",
  },
  ar: {
    nav: { about: "من نحن", product: "المنتجات", contact: "تواصل معنا" },
    hero: {
      title: "نكتشف الفجوات ونملؤها بمنتج يجعل عملك يزدهر",
      subtitle:
        "إنترب استوديو ريادي يحوّل الأفكار الواعدة إلى شركات ناجحة، بدءاً من الأدوات التي تشغّلها.",
      cta: "اكتشف ما نبنيه",
    },
    about: {
      eyebrow: "عن إنترب",
      title: "نبني البنية البرمجية التي تقوم عليها الأعمال الجديدة.",
      p1: "تأسست إنترب لتفعل ما هو أبعد من إطلاق الأفكار. نبحث عن فرص أعمال حقيقية، ونصمم البرمجيات التي تجعلها ممكنة، وندعم المنظومة الكاملة اللازمة لتحويل تلك الأفكار إلى منتجات راسخة.",
      p2: "نهجنا مدروس: فرصة واحدة في كل مرة، تُبنى بعناية وتنمو بوعي. نؤمن بأن أفضل المنتجات تولد من فهم عميق وتنفيذ نظيف ومسار واضح نحو أثر حقيقي.",
    },

    product: {
      eyebrow: "ما الذي نبنيه",
      name: "VetCharted",
      title: "برنامج إدارة العيادات البيطرية، في مكان واحد.",
      p1: "يمنح VetCharted العيادات مكاناً موثوقاً لإدارة عملياتها اليومية: المواعيد والسجلات الطبية وتاريخ الحالات وكل ما بينها.",
      p2: "أدر ملفات الحيوانات والفحوصات والتطعيمات والفواتير والمخزون بالعربية والإنجليزية.",
      cta: "تواصل معنا",
    },
    alameer: {
      eyebrow: "أعمالنا",
      name: "Al Ameer Hydraulics",
      title: "قطع غيار المعدات الثقيلة والآليات، في تطبيق واحد.",
      p1: "صمّمنا وبنينا تطبيق شركة الأمير للهيدروليك، بسبعة فروع في فلسطين والأردن ومصر.",
      p2: "يتصفح العميل الآليات وقطع الغيار، ويطلب بالتوصيل أو بالاستلام من الفرع، ويتواصل مع الفريق عبر واتساب.",
      cta: "شاهد دراسة الحالة",
    },
    checkbook: {
      eyebrow: "أعمالنا",
      name: "CheckBook",
      title: "كل شيك وكل موعد استحقاق، تحت السيطرة.",
      p1: "CheckBook تطبيق موبايل لمتابعة الشيكات: المبالغ والبنوك ومواعيد الاستحقاق والحالات، مع لوحة بالمجاميع.",
      p2: "خطّط لسلسلة شيكات كاملة في دقيقة بالخطة الذكية، وتلقَّ تذكيراً قبل استحقاق كل شيك.",
      cta: "شاهد دراسة الحالة",
    },
    contact: {
      eyebrow: "تواصل",
      title: "لنتحدث.",
      p: "سواء كنت تبحث عن شراكة أو دعم أو ترغب فقط في معرفة المزيد عما نبنيه، يسعدنا أن نسمع منك.",
    },
    footer: "جميع الحقوق محفوظة.",
    menuLabel: "فتح القائمة",
  },
} as const;

export function Index() {
  const { lang, rtl } = useLang();
  const t = content[lang];

  useEffect(() => {
    const hash = window.location.hash.slice(1);
    if (!hash) return;
    const el = document.getElementById(hash);
    if (el)
      el.scrollIntoView({
        behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches
          ? "instant"
          : "smooth",
      });
  }, []);

  return (
    <div dir={rtl ? "rtl" : "ltr"} className="min-h-screen bg-background text-foreground">
      <SiteNav />
      <main id="main">
        <Hero t={t} />
        <About t={t} />
        <Product t={t} rtl={rtl} />
        <Alameer t={t} rtl={rtl} />
        <Checkbook t={t} rtl={rtl} />
        <SiteFaq />
        <Contact t={t} />
      </main>
      <SiteFooter />
    </div>
  );
}

type T = typeof content.en | typeof content.ar;

function Hero({ t }: { t: T }) {
  return (
    <section className="home-hero section-padding">
      <div className="hero-content">
        <p className="hero-eyebrow">
          <span className="status-dot" />
          {t === content.ar
            ? "استوديو ريادي · نصمّم ونبني ونطوّر"
            : "VENTURE STUDIO · DESIGN. BUILD. GROW."}
        </p>
        <h1 className="text-balance text-4xl font-semibold leading-[1.15] tracking-tight sm:text-5xl md:text-6xl lg:text-7xl">
          {t.hero.title}
        </h1>
        <p className="text-balance mx-auto mt-8 max-w-2xl text-lg leading-relaxed text-muted-foreground sm:text-xl">
          {t.hero.subtitle}
        </p>
        <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
          <a
            href="#product"
            className="inline-flex items-center justify-center rounded-full border border-foreground bg-foreground px-8 py-3.5 text-sm font-medium text-primary-foreground transition-all duration-300 hover:bg-background hover:text-foreground"
          >
            {t.hero.cta}
          </a>
        </div>
        <div className="hero-signature" aria-hidden="true">
          <span>01 / {t === content.ar ? "فرصة" : "Opportunity"}</span>
          <i />
          <span>02 / {t === content.ar ? "منتج" : "Product"}</span>
          <i />
          <span>03 / {t === content.ar ? "أثر" : "Impact"}</span>
        </div>
      </div>
    </section>
  );
}

function About({ t }: { t: T }) {
  return (
    <section id="about" className="home-about section-padding section-space">
      <div className="mx-auto max-w-3xl">
        <p className="text-sm font-medium uppercase tracking-widest text-muted-foreground">
          {t.about.eyebrow}
        </p>
        <h2 className="text-balance mt-6 text-3xl font-semibold leading-snug tracking-tight sm:text-4xl">
          {t.about.title}
        </h2>
        <div className="mt-8 space-y-6 text-lg leading-relaxed text-muted-foreground">
          <p>{t.about.p1}</p>
          <p>{t.about.p2}</p>
        </div>
      </div>
    </section>
  );
}

function Product({ t, rtl }: { t: T; rtl: boolean }) {
  return (
    <section id="product" className="home-product section-padding section-space">
      <div className="mx-auto max-w-6xl">
        <div className="grid gap-16 lg:grid-cols-2 lg:items-center lg:gap-24">
          <div>
            <p className="text-sm font-medium uppercase tracking-widest text-muted-foreground">
              {t.product.eyebrow}
            </p>
            <div className={`mt-6 flex items-center gap-3 ${rtl ? "justify-start" : ""}`}>
              <img src={vetchartedUrl} alt="VetCharted" className="h-12 w-auto dark:invert" />
              <span className="text-2xl font-semibold tracking-tight" dir="ltr">
                {t.product.name}
              </span>
            </div>
            <h2 className="text-balance mt-6 text-3xl font-semibold leading-snug tracking-tight sm:text-4xl">
              {t.product.title}
            </h2>
            <div className="mt-8 space-y-5 text-lg leading-relaxed text-muted-foreground">
              <p>{t.product.p1}</p>
              <p>{t.product.p2}</p>
            </div>
            <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
              <a
                href={rtl ? "/vet-charted/" : "/vet-charted/en/"}
                className="inline-flex items-center justify-center rounded-full border border-foreground bg-foreground px-8 py-3.5 text-sm font-medium text-primary-foreground transition-all duration-300 hover:bg-background hover:text-foreground"
              >
                {rtl ? "اكتشف VetCharted" : "Explore VetCharted"}
              </a>
            </div>
          </div>
          <ProductPreview />
        </div>
      </div>
    </section>
  );
}

function Alameer({ t, rtl }: { t: T; rtl: boolean }) {
  return (
    <section id="alameer" className="home-alameer section-padding section-space">
      <div className="mx-auto max-w-6xl">
        <div className="grid gap-16 lg:grid-cols-2 lg:items-center lg:gap-24">
          <div className="lg:order-2">
            <p className="text-sm font-medium uppercase tracking-widest text-muted-foreground">
              {t.alameer.eyebrow}
            </p>
            <div className={`mt-6 flex items-center gap-3 ${rtl ? "justify-start" : ""}`}>
              <img
                src="/alameer-icon.png"
                alt="Al Ameer Hydraulics"
                width="48"
                height="48"
                className="h-12 w-12 rounded-xl"
              />
              <span className="text-2xl font-semibold tracking-tight" dir="ltr">
                {t.alameer.name}
              </span>
            </div>
            <h2 className="text-balance mt-6 text-3xl font-semibold leading-snug tracking-tight sm:text-4xl">
              {t.alameer.title}
            </h2>
            <div className="mt-8 space-y-5 text-lg leading-relaxed text-muted-foreground">
              <p>{t.alameer.p1}</p>
              <p>{t.alameer.p2}</p>
            </div>
            <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
              <a
                href={rtl ? "/ar/alameer/" : "/alameer/"}
                className="inline-flex items-center justify-center rounded-full border border-foreground bg-foreground px-8 py-3.5 text-sm font-medium text-primary-foreground transition-all duration-300 hover:bg-background hover:text-foreground"
              >
                {t.alameer.cta}
              </a>
            </div>
          </div>
          <div className="lg:order-1">
            <AlameerPreview />
          </div>
        </div>
      </div>
    </section>
  );
}

function Checkbook({ t, rtl }: { t: T; rtl: boolean }) {
  return (
    <section id="checkbook" className="home-product section-padding section-space">
      <div className="mx-auto max-w-6xl">
        <div className="grid gap-16 lg:grid-cols-2 lg:items-center lg:gap-24">
          <div>
            <p className="text-sm font-medium uppercase tracking-widest text-muted-foreground">
              {t.checkbook.eyebrow}
            </p>
            <div className={`mt-6 flex items-center gap-3 ${rtl ? "justify-start" : ""}`}>
              <img
                src="/checkbook-icon.png"
                alt="CheckBook"
                width="48"
                height="48"
                className="h-12 w-12 rounded-xl"
              />
              <span className="text-2xl font-semibold tracking-tight" dir="ltr">
                {t.checkbook.name}
              </span>
            </div>
            <h2 className="text-balance mt-6 text-3xl font-semibold leading-snug tracking-tight sm:text-4xl">
              {t.checkbook.title}
            </h2>
            <div className="mt-8 space-y-5 text-lg leading-relaxed text-muted-foreground">
              <p>{t.checkbook.p1}</p>
              <p>{t.checkbook.p2}</p>
            </div>
            <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
              <a
                href={rtl ? "/ar/checkbook/" : "/checkbook/"}
                className="inline-flex items-center justify-center rounded-full border border-foreground bg-foreground px-8 py-3.5 text-sm font-medium text-primary-foreground transition-all duration-300 hover:bg-background hover:text-foreground"
              >
                {t.checkbook.cta}
              </a>
            </div>
          </div>
          <CheckbookPreview />
        </div>
      </div>
    </section>
  );
}

function Contact({ t }: { t: T }) {
  return (
    <section id="contact" className="home-contact section-padding section-space">
      <div className="mx-auto max-w-2xl text-center">
        <p className="text-sm font-medium uppercase tracking-widest text-muted-foreground">
          {t.contact.eyebrow}
        </p>
        <h2 className="text-balance mt-6 text-3xl font-semibold leading-snug tracking-tight sm:text-4xl">
          {t.contact.title}
        </h2>
        <p className="mt-6 text-lg leading-relaxed text-muted-foreground">{t.contact.p}</p>
        <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
          <a
            href="mailto:info@inturp.com"
            dir="ltr"
            className="inline-flex items-center justify-center rounded-full border border-foreground bg-foreground px-8 py-3.5 text-sm font-medium text-primary-foreground transition-all duration-300 hover:bg-background hover:text-foreground"
          >
            info@inturp.com
          </a>
          <a href="https://www.instagram.com/inturp_/" target="_blank" rel="noopener noreferrer" dir="ltr" aria-label="Inturp on Instagram: @inturp_" className="group inline-flex items-center justify-center gap-3 rounded-full border border-foreground/20 px-8 py-3.5 text-sm font-medium transition-all duration-300 hover:border-foreground hover:bg-foreground hover:text-primary-foreground focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4">
            <Instagram size={20} strokeWidth={1.6} aria-hidden="true" className="transition-transform duration-300 group-hover:scale-110 motion-reduce:transform-none" />
            <span>@inturp_</span>
          </a>
        </div>
      </div>
    </section>
  );
}
