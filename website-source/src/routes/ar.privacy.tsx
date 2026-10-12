import { createFileRoute } from "@tanstack/react-router";
import { PrivacyContent } from "@/components/privacy-content";
export const Route = createFileRoute("/ar/privacy")({
  component: PrivacyContent,
  head: () => ({
    meta: [
      { title: "خصوصية الموقع | انتيرب" },
      { name: "description", content: "كيف يتعامل موقع انتيرب مع رسائل التواصل وتفضيلات المتصفح." },
      { property: "og:url", content: "https://inturp.com/ar/privacy/" },
    ],
    links: [
      { rel: "canonical", href: "https://inturp.com/ar/privacy/" },
      { rel: "alternate", hrefLang: "en", href: "https://inturp.com/privacy/" },
      { rel: "alternate", hrefLang: "ar", href: "https://inturp.com/ar/privacy/" },
      { rel: "alternate", hrefLang: "x-default", href: "https://inturp.com/privacy/" },
    ],
  }),
});
