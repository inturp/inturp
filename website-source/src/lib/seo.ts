const origin = "https://inturp.com";
const descriptions = {
  home: {
    en: "Inturp is a venture studio that turns business opportunities into practical software products. Discover Vet Charted, our veterinary clinic management software.",
    ar: "انتيرب تبني منتجات برمجية تعالج احتياجات الأعمال. تعرّف على الشركة وبرنامج Vet Charted لإدارة العيادات البيطرية والمواعيد والسجلات والفواتير.",
  },
  about: {
    en: "Meet Inturp and its founders. We identify business opportunities and build the software and support that turn ideas into useful products.",
    ar: "تعرّف على انتيرب ومؤسسيها وكيف نبني منتجات برمجية انطلاقاً من احتياجات الأعمال، بدءاً من برنامج إدارة العيادات البيطرية Vet Charted.",
  },
  product: {
    en: "Discover Vet Charted by Inturp: veterinary clinic management software for appointments, animal medical records, invoicing and inventory, in Arabic and English.",
    ar: "برنامج Vet Charted من انتيرب لإدارة العيادات البيطرية: المواعيد وملفات الحيوانات والفحوصات والتطعيمات والفواتير والمخزون بالعربية والإنجليزية.",
  },
};
export function pageSeo(page: keyof typeof descriptions, lang: "en" | "ar" = "en") {
  const paths = { home: "/", about: "/about/", product: "/vetcharted/" };
  const path = paths[page];
  const en = origin + path;
  const ar = origin + "/ar" + path;
  const url = lang === "ar" ? ar : en;
  const title =
    page === "home"
      ? lang === "ar"
        ? "انتيرب | منتجات برمجية تبدأ من احتياجات الأعمال"
        : "Inturp | We find the gaps and fill them"
      : page === "about"
        ? lang === "ar"
          ? "عن انتيرب | الشركة والمؤسسون"
          : "About Inturp | Our company and founders"
        : lang === "ar"
          ? "Vet Charted | برنامج إدارة العيادات البيطرية من انتيرب"
          : "Vet Charted | Veterinary clinic management by Inturp";
  const image =
    origin + (page === "product" ? "/vet-charted/assets/img/dashboard.webp" : "/inturp-social.png");
  return {
    meta: [
      { title },
      { name: "description", content: descriptions[page][lang] },
      { property: "og:title", content: title },
      { property: "og:description", content: descriptions[page][lang] },
      { property: "og:url", content: url },
      { property: "og:locale", content: lang === "ar" ? "ar_AR" : "en_US" },
      { property: "og:locale:alternate", content: lang === "ar" ? "en_US" : "ar_AR" },
      { property: "og:image", content: image },
      { name: "twitter:title", content: title },
      { name: "twitter:description", content: descriptions[page][lang] },
      { name: "twitter:image", content: image },
    ],
    links: [
      { rel: "canonical", href: url },
      { rel: "alternate", hrefLang: "en", href: en },
      { rel: "alternate", hrefLang: "ar", href: ar },
      { rel: "alternate", hrefLang: "x-default", href: en },
    ],
    scripts: [
      {
        type: "application/ld+json",
        children: JSON.stringify({
          "@context": "https://schema.org",
          "@type": page === "about" ? "AboutPage" : "WebPage",
          "@id": url + "#webpage",
          url,
          name: title,
          description: descriptions[page][lang],
          inLanguage: lang,
          isPartOf: { "@id": origin + "/#website" },
          about: {
            "@id": origin + (page === "product" ? "/vet-charted/#software" : "/#organization"),
          },
        }),
      },
    ],
  };
}
