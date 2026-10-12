import { createFileRoute } from "@tanstack/react-router";
import { PrivacyContent } from "@/components/privacy-content";
export const Route = createFileRoute("/privacy")({
  component: PrivacyContent,
  head: () => ({
    meta: [
      { title: "Website privacy | Inturp" },
      {
        name: "description",
        content: "How the Inturp website handles contact enquiries and browser preferences.",
      },
      { property: "og:url", content: "https://inturp.com/privacy/" },
    ],
    links: [
      { rel: "canonical", href: "https://inturp.com/privacy/" },
      { rel: "alternate", hrefLang: "en", href: "https://inturp.com/privacy/" },
      { rel: "alternate", hrefLang: "ar", href: "https://inturp.com/ar/privacy/" },
    ],
  }),
});
