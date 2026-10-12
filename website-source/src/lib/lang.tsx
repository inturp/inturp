import { createContext, useContext, useEffect, type ReactNode } from "react";
import { useRouterState } from "@tanstack/react-router";
export type Lang = "en" | "ar";
const LangContext = createContext<{ lang: Lang; setLang: (lang: Lang) => void; rtl: boolean }>({
  lang: "en",
  setLang: () => {},
  rtl: false,
});
export function LangProvider({ children }: { children: ReactNode }) {
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  const lang: Lang = /^\/ar(?:\/|$)/.test(pathname) ? "ar" : "en";
  useEffect(() => {
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
  }, [lang]);
  const setLang = (next: Lang) => {
    try {
      window.localStorage.setItem("inturp-lang", next);
    } catch {
      /* ignore */
    }
    const base = pathname.replace(/^\/ar(?=\/|$)/, "") || "/";
    window.location.assign(
      (next === "ar" ? "/ar" + (base === "/" ? "/" : base) : base) + window.location.hash,
    );
  };
  return (
    <LangContext.Provider value={{ lang, setLang, rtl: lang === "ar" }}>
      {children}
    </LangContext.Provider>
  );
}
export function useLang() {
  return useContext(LangContext);
}
