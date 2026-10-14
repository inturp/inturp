# Inturp website search and measurement

## Rebuild

Run `npm ci`, `npm run build`, then `python3 publish-local.py` from `website-source`.
The publish script preserves the product assets and rebuilds the product pages from `vet-promo`.

## Search

- English company pages: `/`, `/about/`, `/vetcharted/`, `/privacy/`.
- Arabic equivalents: `/ar/`, `/ar/about/`, `/ar/vetcharted/`, `/ar/privacy/`.
- Product: Arabic `/vet-charted/`, English `/vet-charted/en/`; legal pages `/vet-charted/privacy/`, `/vet-charted/delete-account/` (old `.html` URLs redirect). Product pages: `/alameer/` and `/checkbook/`, each with `privacy/` and `delete-account/` pages. They are static (not part of the React build): rebuild their legal pages with `python3 showcase/build_alameer.py` and `python3 showcase/build_checkbook.py`; the Products menu for the static pages lives in `showcase/shared.py`.
- Each language uses its own canonical URL and reciprocal hreflang links.
- Sitemap: https://inturp.com/sitemap.xml (12 URLs). Update `public/sitemap.xml` when adding pages.
- Content is prerendered; search crawlers receive actual content without executing JavaScript.
- Company and product JSON-LD describe only known facts. No invented ratings or prices.
- Social preview assets are distinct for company and product.
- Search Console uses an HTML verification tag from the currently signed-in owner's account.

## Analytics

- GA4 web measurement ID: `G-SSBBVTW4KH` (public identifier).
- Property name: Inturp Website. Reporting time zone: Gaza.
- Source: `public/js/analytics.js`.
- Google scripts load only after explicit optional-analytics consent, only on inturp.com/www.inturp.com.
- Advertising storage and personalization are denied. Enhanced automatic measurement is disabled.
- Events: `page_view`, `contact_click`, `product_click`, `demo_cta_click`.
- These are clicks, not completed leads. Email delivery or a sale must not be inferred from a click.
- No form text or contact details are included in custom event payloads.
- Privacy settings allow consent changes. Refusing analytics does not affect website functionality.
- Check reports after actual consented visits; reporting can take time and blockers can suppress analytics.

## Communication

- Contact address: info@inturp.com.
- MX records point to Cloudflare Email Routing. User confirmed receiving email on 12 October 2026.
- The product form prepares an email in the visitor's email client. It does not submit to a server.
- Website privacy and product privacy are separate policies.

## Verification

- TypeScript and production build pass.
- 32 viewport/page combinations: 320, 390, 768, 1440 pixels across company, privacy and product language variants; no horizontal overflow or broken loaded images.
- Language switch keeps the current company page and navigation stays left-to-right.
- Company logos were resized and founder photographs compressed (about 86% less combined image transfer for those four images).
- This does not promise a Google ranking or a specific Lighthouse score.

## Live setup status — 12 October 2026

- Search Console HTTPS URL-prefix property verified in the signed-in owner's account.
- Sitemap submitted. Search Console initially reports "Couldn't fetch" / "Sitemap could not be read" without a detailed error. The public XML responds HTTP 200 with application/xml and validates with 12 URLs. Processing has not been confirmed.
- The company homepage is already indexed; an updated crawl was requested and accepted.
- GA4 property ID: 558524565; web stream ID: 16112185073.
- A consented test visit appeared as one active user in the live Analytics overview.
- Shared analytics script initializes once across client navigation. The script URL is versioned to refresh browser caches.

## Clinic survey

- Pages: `/clinic-survey/` (English) and `/ar/clinic-survey/` (Arabic). Both are `noindex` and left out of the sitemap on purpose; the link is sent directly to clinics.
- Questions live in `showcase/survey/questions.json`. After editing, run `python3 showcase/build_survey.py`.
- Answers are saved as the visitor goes (partial sessions included, with a device summary and click events) by the Firebase function `submitSurvey` (project `vet-charted`, database `survey`), set in `clinic-survey/assets/js/survey-config.js`. See `showcase/survey/functions/README.md` for how it is secured, how to read the answers and how to redeploy. If the endpoint is empty or unreachable the last step offers to send the answers by email. `survey-apps-script.gs` is an alternative Google Sheet destination (`transport: 'script'`).
