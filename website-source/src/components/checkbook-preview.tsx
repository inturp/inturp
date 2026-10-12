import { useLang } from "@/lib/lang";

const phone =
  "relative w-[44%] max-w-[250px] overflow-hidden rounded-[2.1rem] border border-border bg-[#161616] p-[7px] shadow-[0_40px_70px_-34px_rgba(0,0,0,0.55)]";

export function CheckbookPreview() {
  const { lang } = useLang();
  const ar = lang === "ar";
  return (
    <figure className="mx-auto w-full max-w-[560px]" dir="ltr">
      <div className="relative flex items-center justify-center gap-0 py-6">
        <div className={`${phone} -mr-6 mt-10 -rotate-3`}>
          <img
            src="/product/checkbook-app-2.webp"
            alt={ar ? "تفاصيل الشيك في تطبيق CheckBook" : "Cheque details in the CheckBook app"}
            width="520"
            height="1130"
            loading="lazy"
            className="block h-auto w-full rounded-[1.7rem]"
          />
        </div>
        <div className={`${phone} z-10 -mt-4 rotate-3`}>
          <img
            src="/product/checkbook-app-1.webp"
            alt={ar ? "لوحة CheckBook الرئيسية" : "CheckBook dashboard"}
            width="520"
            height="1130"
            loading="lazy"
            className="block h-auto w-full rounded-[1.7rem]"
          />
        </div>
      </div>
      <figcaption
        className="mt-2 flex items-center justify-center gap-[9px] text-[11px] text-muted-foreground"
        dir={ar ? "rtl" : "ltr"}
      >
        <span className="status-dot" />
        {ar ? "كل شيك وكل موعد. في تطبيق واحد." : "Every cheque and due date. One app."}
      </figcaption>
    </figure>
  );
}
