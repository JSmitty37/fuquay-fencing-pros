# Fuquay Fencing Pros — site

Static site. No build step, no runtime. Deploys to GitHub Pages.

## ⚠️ Before this goes live — replace these

Open `build.py`, edit the CONFIG block, re-run `python3 build.py`:

| Constant | Current placeholder | Replace with |
|---|---|---|
| `PHONE_TEXT` / `PHONE_TEL` | `(919) 276-8406` / `+19192768406` | CallRail NC tracking number |
| `GA4_ID` | `G-D8RTHW2GYN` | real GA4 measurement ID |
| `PIXEL_ID` | `000000000000000` | real Meta Pixel ID |
| `WEBHOOK` | `https://hooks.zapier.com/hooks/catch/24209228/4dq1xf8/` | Zapier Catch Hook URL |
| `DOMAIN` | `fuquayfencingpros.com` | final domain if different |

`PHONE_TEXT` / `PHONE_TEL` are set to the CallRail tracking number `(919) 276-8406` (`tel:+19192768406`). `GA4_ID` is set (`G-D8RTHW2GYN`); every page loads gtag with that measurement ID. `WEBHOOK` is set. Lead forms POST JSON to that Zapier Catch Hook. Turn the Zap **On** so submissions are received. If `WEBHOOK` is blank, forms run in demo mode (success state + console log, no send). `PIXEL_ID` is still a placeholder.

## What's in here

- `index.html` — home
- `services/` — 4 service pages (vinyl first: it's the validated 70/mo term)
- `areas/` — 5 city pages, each with genuinely distinct local content
- `faq.html` — 8 Q&As with FAQPage schema
- `privacy.html` — required for Meta lead forms and business verification
- `styles.css`, `main.js`, `sitemap.xml`, `robots.txt`, `CNAME`, `favicon.svg`

## What's different from the Summerville build

1. **A lead form on every page**, not just the home page. Each posts a `pageSource` so you know which page
   produced the lead.
2. **Analytics wired in** — GA4 + Meta Pixel, with `generate_lead` and `Lead` events on submit and
   `click_to_call` / `Contact` events on every phone link.
3. **Spam gates** — honeypot field plus a 3-second minimum dwell time. Bot leads reaching your contractor
   is how you lose a contractor.
4. **Property address is a required field.** Zip 27526 spans ~98 sq mi across two counties, so zip alone
   cannot qualify a lead here.
5. **Schema** — one shared business `@id` across all pages (not duplicate entities), plus BreadcrumbList,
   Service and FAQPage.
6. **Real local content** per area page — ordinance specifics, the Wake/Harnett split, Cecil clay,
   red-clay staining, pollen timing.

## Deploy

Site files live at the repository root (`index.html`, `CNAME`, etc.). Repo:
https://github.com/JSmitty37/fuquay-fencing-pros

**GitHub Pages (admin click — API cannot enable this):** Settings → Pages →
Build and deployment → Source: **Deploy from a branch** → Branch **main** / folder **/ (root)** → Save.
Custom domain: `fuquayfencingpros.com` → Save. After DNS is green, enable **Enforce HTTPS**.

Default Pages URL after enable: `https://jsmitty37.github.io/fuquay-fencing-pros/`
Custom domain URL: `https://fuquayfencingpros.com/`

### Namecheap Advanced DNS (what GitHub Pages displays)

Remove any parking / default URL Redirect / conflicting `@` or `www` records first.

| Type | Host | Value | TTL |
|---|---|---|---|
| A Record | `@` | `185.199.108.153` | Automatic |
| A Record | `@` | `185.199.109.153` | Automatic |
| A Record | `@` | `185.199.110.153` | Automatic |
| A Record | `@` | `185.199.111.153` | Automatic |
| AAAA Record | `@` | `2606:50c0:8000::153` | Automatic |
| AAAA Record | `@` | `2606:50c0:8001::153` | Automatic |
| AAAA Record | `@` | `2606:50c0:8002::153` | Automatic |
| AAAA Record | `@` | `2606:50c0:8003::153` | Automatic |
| CNAME Record | `www` | `jsmitty37.github.io.` | Automatic |

## Content accuracy note

The ordinance figures on these pages (6 ft side/rear in corporate limits, 4 ft front, no maximum in the
ETJ, no permit required, 2-inch ground clearance) come from the Town of Fuquay-Varina's own Land
Development Ordinance and FAQ. Third-party fence-law aggregator sites list 8 ft for side/rear — **that is
wrong**. Pool barrier figures come from the 2024 NC Residential Code Appendix NC-A. Re-verify before
launch; codes change.

**No invented reviews, ratings, years in business or job counts appear anywhere on this site.** Keep it
that way — add real ones when you have them.
