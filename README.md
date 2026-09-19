# Fuquay Fencing Pros — site

Static site. No build step, no runtime. Deploys to GitHub Pages.

## ⚠️ Before this goes live — replace these

Open `build.py`, edit the CONFIG block, re-run `python3 build.py`:

| Constant | Current placeholder | Replace with |
|---|---|---|
| `PHONE_TEXT` / `PHONE_TEL` | `(919) 000-0000` | the real NC 919 call-tracking number |
| `GA4_ID` | `G-XXXXXXXXXX` | real GA4 measurement ID |
| `PIXEL_ID` | `000000000000000` | real Meta Pixel ID |
| `WEBHOOK` | *(blank — demo mode)* | Zapier Catch Hook URL |
| `DOMAIN` | `fuquayfencingpros.com` | final domain if different |

With `WEBHOOK` blank the forms run in demo mode: they show the success state and log the payload to the
console without sending anywhere. Useful for local testing, useless in production — set it before launch.

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

```bash
cd site
git init && git add -A && git commit -m "Initial site"
git branch -M main
git remote add origin https://github.com/<OWNER>/<REPO>.git
git push -u origin main
```

Then: repo **Settings → Pages → Source: main / root**. Add `fuquayfencingpros.com` as the custom domain and enable
**Enforce HTTPS**.

**DNS (apex + www):** four A records for the apex pointing at GitHub Pages —
`185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` — and a CNAME for `www` →
`<OWNER>.github.io`.

## Content accuracy note

The ordinance figures on these pages (6 ft side/rear in corporate limits, 4 ft front, no maximum in the
ETJ, no permit required, 2-inch ground clearance) come from the Town of Fuquay-Varina's own Land
Development Ordinance and FAQ. Third-party fence-law aggregator sites list 8 ft for side/rear — **that is
wrong**. Pool barrier figures come from the 2024 NC Residential Code Appendix NC-A. Re-verify before
launch; codes change.

**No invented reviews, ratings, years in business or job counts appear anywhere on this site.** Keep it
that way — add real ones when you have them.
