import { Link, useRouterState } from "@tanstack/react-router";
import { useEffect, useRef, useState } from "react";
import { ArrowUpRight, ChevronDown, Menu, Moon, Sun, X } from "lucide-react";
import { useLang, type Lang } from "@/lib/lang";
import { useTheme } from "@/lib/theme";

const nav = {
  en: {
    products: "Products",
    about: "About us",
    contact: "Let’s talk",
    menu: "Navigation menu",
    footer: "All rights reserved.",
    skip: "Skip to content",
  },
  ar: {
    products: "المنتجات",
    about: "من نحن",
    contact: "لنتحدث",
    menu: "قائمة التنقل",
    footer: "جميع الحقوق محفوظة.",
    skip: "تخطّي إلى المحتوى",
  },
} satisfies Record<Lang, Record<string, string>>;

function Preferences() {
  const { lang, setLang } = useLang();
  const { theme, toggleTheme } = useTheme();
  return (
    <div className="nav-preferences">
      <button
        type="button"
        className="language-control"
        onClick={() => setLang(lang === "ar" ? "en" : "ar")}
        aria-label={lang === "ar" ? "Switch to English" : "التبديل إلى العربية"}
      >
        {lang === "ar" ? "EN" : "عربي"}
      </button>
      <button
        type="button"
        className="icon-control"
        onClick={toggleTheme}
        aria-label={
          lang === "ar"
            ? theme === "dark"
              ? "تفعيل الوضع الفاتح"
              : "تفعيل الوضع الداكن"
            : theme === "dark"
              ? "Switch to light mode"
              : "Switch to dark mode"
        }
      >
        {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
      </button>
    </div>
  );
}

export function SiteNav() {
  const { lang, rtl } = useLang();
  const t = nav[lang];
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  const [menuOpen, setMenuOpen] = useState(false);
  const [productsOpen, setProductsOpen] = useState(false);
  const headerRef = useRef<HTMLElement>(null);
  const menuRef = useRef<HTMLButtonElement>(null);
  useEffect(() => {
    const close = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setMenuOpen(false);
        setProductsOpen(false);
        menuRef.current?.focus();
      }
    };
    const outside = (e: PointerEvent) => {
      if (!headerRef.current?.contains(e.target as Node)) {
        setMenuOpen(false);
        setProductsOpen(false);
      }
    };
    const desktop = matchMedia("(min-width: 900px)");
    const resize = () => setMenuOpen(false);
    document.addEventListener("keydown", close);
    document.addEventListener("pointerdown", outside);
    desktop.addEventListener("change", resize);
    return () => {
      document.removeEventListener("keydown", close);
      document.removeEventListener("pointerdown", outside);
      desktop.removeEventListener("change", resize);
    };
  }, []);
  useEffect(() => {
    const items = document.querySelectorAll("main section > div, .founder-card");
    if (
      matchMedia("(prefers-reduced-motion: reduce)").matches ||
      !("IntersectionObserver" in window)
    )
      return;
    const observer = new IntersectionObserver(
      (entries) =>
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("revealed");
            observer.unobserve(e.target);
          }
        }),
      { threshold: 0.06 },
    );
    items.forEach((el) => {
      if (el.getBoundingClientRect().top < window.innerHeight) return;
      el.classList.add("reveal-ready");
      observer.observe(el);
    });
    return () => {
      observer.disconnect();
      items.forEach((el) => el.classList.remove("reveal-ready"));
    };
  }, [pathname]);
  const closeMenu = () => {
    setMenuOpen(false);
    setProductsOpen(false);
  };
  return (
    <>
      <a href="#main" className="skip-link">
        {t.skip}
      </a>
      <header ref={headerRef} className="site-header" dir={rtl ? "rtl" : "ltr"}>
        <nav className="site-nav" aria-label={t.menu}>
          <Link to="/" onClick={closeMenu} className="brand-link">
            <img
              src="/inturp-logo.png"
              alt="Inturp"
              width="58"
              height="58"
              className="dark:invert"
            />
            <span>
              inturp<span className="brand-dot">.</span>
            </span>
          </Link>
          <div className="desktop-nav">
            <div className="product-menu">
              <button
                type="button"
                aria-expanded={productsOpen}
                aria-controls="product-links"
                onClick={() => setProductsOpen(!productsOpen)}
                className={pathname === "/vetcharted" ? "nav-link active" : "nav-link"}
              >
                {t.products}
                <ChevronDown size={14} className={productsOpen ? "rotate-180" : ""} />
              </button>
              {productsOpen && (
                <div className="product-dropdown" id="product-links">
                  <a href="https://inturp.com/vet-charted/" onClick={closeMenu}>
                    <img
                      src="/vetcharted-logo.png"
                      alt=""
                      width="32"
                      height="32"
                      className="dark:invert"
                    />
                    <span>
                      VetCharted
                      <small>
                        {lang === "ar" ? "إدارة العيادات البيطرية" : "Veterinary clinic management"}
                      </small>
                    </span>
                    <ArrowUpRight size={17} />
                  </a>
                </div>
              )}
            </div>
            <Link
              to="/about"
              onClick={closeMenu}
              className="nav-link"
              activeProps={{ className: "nav-link active", "aria-current": "page" }}
            >
              {t.about}
            </Link>
            <Link to="/" hash="contact" onClick={closeMenu} className="nav-contact">
              {t.contact}
              <ArrowUpRight size={16} />
            </Link>
          </div>
          <div className="nav-end">
            <Preferences />
            <button
              ref={menuRef}
              type="button"
              className="icon-control mobile-toggle"
              aria-label={t.menu}
              aria-expanded={menuOpen}
              aria-controls="mobile-nav"
              onClick={() => setMenuOpen(!menuOpen)}
            >
              {menuOpen ? <X size={22} /> : <Menu size={22} />}
            </button>
          </div>
        </nav>
        {menuOpen && (
          <nav id="mobile-nav" className="mobile-panel" aria-label={t.menu}>
            <a href="https://inturp.com/vet-charted/" onClick={closeMenu}>
              VetCharted <ArrowUpRight size={18} />
            </a>
            <Link to="/about" onClick={closeMenu}>
              {t.about}
              <ArrowUpRight size={18} />
            </Link>
            <Link to="/" hash="contact" onClick={closeMenu}>
              {t.contact}
              <ArrowUpRight size={18} />
            </Link>
          </nav>
        )}
      </header>
    </>
  );
}

export function SiteFooter() {
  const { lang } = useLang();
  return (
    <footer className="site-footer section-padding">
      <div className="footer-inner">
        <Link to="/" className="brand-link">
          <img src="/inturp-logo.png" alt="" width="44" height="44" className="dark:invert" />
          <span>inturp.</span>
        </Link>
        <div className="footer-links">
          <Link to="/about">{nav[lang].about}</Link>
          <a href="https://inturp.com/vet-charted/">VetCharted</a>
          <a href="mailto:info@inturp.com">info@inturp.com</a>
        </div>
        <p>
          © {new Date().getFullYear()} Inturp. {nav[lang].footer}
        </p>
      </div>
    </footer>
  );
}
