/* Optional analytics. No Google script or event is sent before consent. */
(() => {
  "use strict";
  const measurementId = "G-SSBBVTW4KH"; // Set to the site's GA4 web stream ID.
  const storageKey = "inturp-analytics-consent";
  if (!/^G-[A-Z0-9]+$/.test(measurementId)) return;
  if (window.__inturpAnalyticsInitialized) return;
  window.__inturpAnalyticsInitialized = true;
  const production = /^(www\.)?inturp\.com$/.test(location.hostname);
  let consent = null,
    loaded = false,
    previousPath = "";
  try {
    consent = localStorage.getItem(storageKey);
  } catch (_) {}
  const language = () => (document.documentElement.lang === "ar" ? "ar" : "en");
  function event(name, parameters) {
    if (consent !== "granted" || !window.gtag) return;
    window.gtag("event", name, {
      ...parameters,
      page_location: location.origin + location.pathname,
    });
  }
  function pageview() {
    if (consent !== "granted" || previousPath === location.pathname) return;
    previousPath = location.pathname;
    event("page_view", {
      page_location: location.origin + location.pathname,
      page_title: document.title,
      language: language(),
    });
  }
  function start() {
    if (!production) return;
    if (loaded) {
      pageview();
      return;
    }
    loaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () {
      window.dataLayer.push(arguments);
    };
    window.gtag("consent", "default", {
      analytics_storage: "granted",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
    });
    window.gtag("js", new Date());
    window.gtag("config", measurementId, {
      send_page_view: false,
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
    });
    const script = document.createElement("script");
    script.async = true;
    script.src = "https://www.googletagmanager.com/gtag/js?id=" + measurementId;
    document.head.append(script);
    pageview();
  }
  function choose(value) {
    consent = value;
    try {
      localStorage.setItem(storageKey, value);
    } catch (_) {}
    document.getElementById("analytics-choice")?.remove();
    if (value === "granted") {
      if (window.gtag) window.gtag("consent", "update", { analytics_storage: "granted" });
      previousPath = "";
      start();
    } else {
      if (window.gtag) window.gtag("consent", "update", { analytics_storage: "denied" });
      document.cookie.split(";").forEach((part) => {
        const name = part.trim().split("=")[0];
        if (!/^_ga(?:_|$)/.test(name)) return;
        [undefined, location.hostname, "." + location.hostname].forEach((domain) => {
          document.cookie = name + "=; Max-Age=0; path=/" + (domain ? "; domain=" + domain : "");
        });
      });
    }
  }
  function showChoice() {
    document.getElementById("analytics-choice")?.remove();
    const ar = language() === "ar";
    const box = document.createElement("aside");
    box.id = "analytics-choice";
    box.className = "analytics-choice";
    box.setAttribute("aria-label", ar ? "تفضيلات الإحصائيات" : "Analytics preferences");
    const text = document.createElement("p");
    text.textContent = ar
      ? "نستخدم إحصائيات اختيارية لفهم الزيارات وضغطات التواصل. هل تسمح بها؟"
      : "Optional analytics help us understand visits and contact clicks. Would you like to allow them?";
    const controls = document.createElement("div");
    [
      ["denied", ar ? "بدون إحصائيات" : "No analytics"],
      ["granted", ar ? "السماح" : "Allow analytics"],
    ].forEach(([value, label]) => {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = label;
      button.addEventListener("click", () => choose(value));
      controls.append(button);
    });
    const policy = document.createElement("a");
    policy.href = ar ? "/ar/privacy/" : "/privacy/";
    policy.textContent = ar ? "الخصوصية" : "Privacy";
    controls.append(policy);
    box.append(text, controls);
    document.body.append(box);
  }
  document.addEventListener("click", (e) => {
    if (!(e.target instanceof Element)) return;
    if (e.target.closest("[data-privacy-settings]")) {
      showChoice();
      return;
    }
    const anchor = e.target.closest("a");
    if (!anchor) return;
    const href = anchor.getAttribute("href") || "";
    if (href.startsWith("mailto:"))
      event("contact_click", { contact_method: "email", language: language() });
    else if (href.includes("wa.me/"))
      event("contact_click", { contact_method: "whatsapp", language: language() });
    else if (href.includes("/vet-charted/"))
      event("product_click", { product_name: "Vet Charted", language: language() });
    else if (href.endsWith("#contact")) event("demo_cta_click", { language: language() });
  });
  document.addEventListener("inturp:pageview", pageview);
  new MutationObserver(() => {
    if (document.getElementById("analytics-choice")) showChoice();
  }).observe(document.documentElement, { attributes: true, attributeFilter: ["lang"] });
  if (consent === "granted") start();
  else if (!consent) showChoice();
})();
