import { createFileRoute } from "@tanstack/react-router";
import { Index } from "./index";
import { pageSeo } from "@/lib/seo";
export const Route = createFileRoute("/ar/")({
  component: Index,
  head: () => pageSeo("home", "ar"),
});
