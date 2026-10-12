import { createFileRoute } from "@tanstack/react-router";
import { VetChartedPage } from "./vetcharted";
import { pageSeo } from "@/lib/seo";
export const Route = createFileRoute("/ar/vetcharted")({
  component: VetChartedPage,
  head: () => pageSeo("product", "ar"),
});
