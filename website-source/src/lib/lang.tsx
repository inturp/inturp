import { createContext, useContext, useEffect, useState, type ReactNode } from "react";

export type Lang = "en" | "ar";

type LangContextValue = {
  lang: Lang;
  setLang: (l: Lang) => void;
  rtl: boolean;
};

const LangContext = createContext<LangContextValue>({
  lang: "en",
  setLang: () => {},
  rtl: false,
});

export function LangProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>("en");
  const rtl = lang === "ar";

  useEffect(() => {
    try {
      const stored = window.localStorage.getItem("inturp-lang");
      if (stored === "ar" || stored === "en") setLangState(stored);
    } catch {
      /* Private browsing can disable storage. */
    }
  }, []);

  useEffect(() => {
    document.documentElement.lang = lang;
    document.documentElement.dir = rtl ? "rtl" : "ltr";
  }, [lang, rtl]);

  const setLang = (l: Lang) => {
    setLangState(l);
    try {
      window.localStorage.setItem("inturp-lang", l);
    } catch {
      /* ignore */
    }
  };

  return <LangContext.Provider value={{ lang, setLang, rtl }}>{children}</LangContext.Provider>;
}

export function useLang() {
  return useContext(LangContext);
}
