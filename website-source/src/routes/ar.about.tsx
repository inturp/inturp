import { createFileRoute } from "@tanstack/react-router";
import { AboutPage } from "./about";
import { pageSeo } from "@/lib/seo";
export const Route = createFileRoute("/ar/about")({
  component: AboutPage,
  head: () => pageSeo("about", "ar"),
});
