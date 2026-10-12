import { useLang } from "@/lib/lang";
export function ProductPreview() {
  const { lang } = useLang();
  return (
    <figure className="product-preview">
      <div className="preview-bar" aria-hidden="true">
        <span />
        <span />
        <span />
        <b>VetCharted / {lang === "ar" ? "لوحة التحكم" : "Dashboard"}</b>
      </div>
      <img
        src="/product/dashboard.webp"
        alt={
          lang === "ar"
            ? "لوحة تحكم VetCharted لإدارة العيادة"
            : "VetCharted clinic management dashboard"
        }
        width="2880"
        height="1800"
        loading="lazy"
      />
      <figcaption>
        <span className="status-dot" />
        {lang === "ar" ? "كل تفاصيل العيادة. في مكان واحد." : "Your clinic. All in one place."}
      </figcaption>
    </figure>
  );
}
