import { pageSeo } from "@/lib/seo";
import { createFileRoute } from "@tanstack/react-router";
import { SiteNav, SiteFooter } from "@/components/site-chrome";
import { useLang } from "@/lib/lang";

const hammamPhoto = "/hammam-alaghbar.jpg";
const hamzaPhoto = "/hamza-saleh.jpg";

export const Route = createFileRoute("/about")({
  component: AboutPage,
  head: () => pageSeo("about"),
});

const copy = {
  en: {
    eyebrow: "About Inturp",
    title: "We build the infrastructure behind new businesses.",
    paragraphs: [
      "Inturp was created to do more than launch ideas. We look for meaningful business opportunities, design the software that makes them possible, and support the broader ecosystem required to turn those ideas into lasting products.",
      "Our approach is deliberate: one opportunity at a time, built with care, and scaled with intention. We believe the best products are born from deep understanding, clean execution, and a clear path to real impact.",
      "Every product we build starts with a gap that others overlook, and ends with a tool that people rely on every day.",
    ],
    foundersTitle: "Meet Our Founders",
    founders: [
      { name: "Hammam Alaghbar", role: "Co-founder, Lead Developer", photo: hammamPhoto },
      { name: "Hamza Saleh", role: "Co-founder, Sales & Product Manager", photo: hamzaPhoto },
    ],
    prev: "Previous founder",
    next: "Next founder",
  },
  ar: {
    eyebrow: "عن إنترب",
    title: "نبني البنية البرمجية التي تقوم عليها الأعمال الجديدة.",
    paragraphs: [
      "تأسست إنترب لتفعل ما هو أبعد من إطلاق الأفكار. نبحث عن فرص أعمال حقيقية، ونصمم البرمجيات التي تجعلها ممكنة، وندعم المنظومة الكاملة اللازمة لتحويل تلك الأفكار إلى منتجات راسخة.",
      "نهجنا مدروس: فرصة واحدة في كل مرة، تُبنى بعناية وتنمو بوعي. نؤمن بأن أفضل المنتجات تولد من فهم عميق وتنفيذ نظيف ومسار واضح نحو أثر حقيقي.",
      "كل منتج نبنيه يبدأ من فجوة يتجاهلها الآخرون، وينتهي بأداة يعتمد عليها الناس كل يوم.",
    ],
    foundersTitle: "تعرّف على مؤسسينا",
    founders: [
      { name: "همام الأغبر", role: "شريك مؤسس، مدير التطوير", photo: hammamPhoto },
      { name: "حمزة صالح", role: "شريك مؤسس، مدير المبيعات والمنتج", photo: hamzaPhoto },
    ],
    prev: "المؤسس السابق",
    next: "المؤسس التالي",
  },
};

type T = typeof copy.en | typeof copy.ar;

export function AboutPage() {
  const { lang, rtl } = useLang();
  const t = copy[lang];

  return (
    <div dir={rtl ? "rtl" : "ltr"} className="min-h-screen bg-background text-foreground">
      <SiteNav />
      <main id="main">
        <section className="page-intro section-padding section-space">
          <div className="mx-auto max-w-3xl">
            <p className="text-sm font-medium uppercase tracking-widest text-muted-foreground">
              {t.eyebrow}
            </p>
            <h1 className="text-balance mt-6 text-4xl font-semibold leading-tight tracking-tight sm:text-5xl">
              {t.title}
            </h1>
            <div className="mt-10 space-y-6 text-lg leading-relaxed text-muted-foreground">
              {t.paragraphs.map((p) => (
                <p key={p}>{p}</p>
              ))}
            </div>
          </div>
        </section>
        <Founders t={t} rtl={rtl} />
      </main>
      <SiteFooter />
    </div>
  );
}

function Founders({ t, rtl }: { t: T; rtl: boolean }) {
  return (
    <section className="founders-section section-padding section-space">
      <div className="mx-auto max-w-6xl">
        <div className="mx-auto flex max-w-3xl items-end justify-between gap-6">
          <h2 className="text-2xl font-semibold tracking-tight sm:text-3xl">{t.foundersTitle}</h2>
        </div>

        <div className="founder-grid">
          {t.founders.map((f) => (
            <figure key={f.name} className="founder-card">
              <img
                src={f.photo}
                alt={f.name}
                loading="lazy"
                className="founder-image"
                width="800"
                height="900"
              />
              <figcaption className={`mt-5 ${rtl ? "text-right" : "text-left"}`}>
                <p className="text-lg font-medium tracking-tight">{f.name}</p>
                <p className="mt-1 text-sm text-muted-foreground">{f.role}</p>
              </figcaption>
            </figure>
          ))}
        </div>
      </div>
    </section>
  );
}
