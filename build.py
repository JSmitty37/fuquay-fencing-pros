#!/usr/bin/env python3
"""
Fuquay Fencing Pros — static site generator.
Every page gets: its own lead form, analytics hooks, honeypot, schema, breadcrumbs.
Swap the CONFIG block and re-run to retarget the whole site.
"""
import os, shutil, html, json, re, zlib

# ============================== CONFIG — SWAP THESE ==============================
BRAND        = "Fuquay Fencing Pros"
BRAND_L1     = "Fuquay"
BRAND_L2     = "Fencing Pros"
DOMAIN       = "fuquayfencingpros.com"
BASE         = f"https://{DOMAIN}"
PHONE_TEXT   = "(919) 276-8406"          # CallRail tracking number
PHONE_TEL    = "+19192768406"
GA4_ID       = "G-D8RTHW2GYN"
PIXEL_ID     = "28277699775183703"       # Meta Pixel ID
WEBHOOK      = "https://hooks.zapier.com/hooks/catch/24209228/4dq1xf8/"
CITY         = "Fuquay-Varina"
STATE        = "NC"
OUT          = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
# ================================================================================

BIZ_ID = f"{BASE}/#business"

SERVICES = [
    ("vinyl-fences",           "Vinyl Fences",                    "Vinyl Fence Installation"),
    ("wood-privacy-fences",    "Wood &amp; Privacy Fences",       "Wood &amp; Privacy Fence Installation"),
    ("aluminum-pool-fences",   "Aluminum &amp; Pool-Code Fences", "Aluminum &amp; Pool-Code Fence Installation"),
    ("chain-link-fences",      "Chain Link Fences",               "Chain Link Fence Installation"),
]
AREAS = [
    ("fuquay-varina", "Fuquay-Varina", "27526"),
    ("holly-springs", "Holly Springs", "27540"),
    ("angier",        "Angier",        "27501"),
    ("willow-spring", "Willow Spring", "27592"),
    ("garner",        "Garner",        "27529"),
]

# --------------------------------------------------------------------------- head
def head(title, desc, canon, depth, extra_ld="", og_type="website", extra_meta=""):
    up = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="canonical" href="{canon}" />
<meta name="robots" content="index, follow" />
<meta name="theme-color" content="#14281d" />
<meta property="og:type" content="{og_type}" />
<meta property="og:site_name" content="{BRAND}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="{canon}" />
<meta property="og:image" content="{BASE}/images/og-image.jpg" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{desc}" />
{extra_meta}<link rel="icon" href="{up}favicon.svg" type="image/svg+xml" />
<link rel="stylesheet" href="{up}styles.css" />
{extra_ld}
<!-- GA4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
<script>
  window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}
  gtag('js',new Date());gtag('config','{GA4_ID}');
</script>
<!-- Meta Pixel -->
<script>
!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;
n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,
document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init','{PIXEL_ID}');fbq('track','PageView');
</script>
</head>
<body>
<a class="skip-link" href="#quote">Skip to free estimate form</a>
"""

MARK = ('<svg class="brand-mark" width="34" height="34" viewBox="0 0 32 32" aria-hidden="true" focusable="false">'
        '<g fill="currentColor"><path d="M3 14l3-4 3 4v15H3z"/><path d="M11 14l3-4 3 4v15h-6z"/>'
        '<path d="M19 14l3-4 3 4v15h-6z"/><rect x="1" y="18" width="30" height="2.4"/>'
        '<rect x="1" y="24" width="30" height="2.4"/></g></svg>')

PHONE_SVG = ('<svg width="17" height="17" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
             '<path fill="currentColor" d="M6.6 10.8a15.5 15.5 0 006.6 6.6l2.2-2.2a1 1 0 011-.24 11.4 11.4 0 '
             '003.5.56 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1 11.4 11.4 0 '
             '00.56 3.5 1 1 0 01-.24 1z"/></svg>')

def header(depth):
    up = "../" * depth
    home = up + "index.html" if depth else "#top"
    return f"""<header class="site-header" id="top">
<div class="container header-inner">
  <a class="brand" href="{home}" aria-label="{BRAND} home">{MARK}
    <span class="brand-text"><span class="brand-line1">{BRAND_L1}</span><span class="brand-line2">{BRAND_L2}</span></span></a>
  <nav class="main-nav" aria-label="Primary">
    <a href="{up}services/vinyl-fences.html">Vinyl</a>
    <a href="{up}services/wood-privacy-fences.html">Wood</a>
    <a href="{up}services/aluminum-pool-fences.html">Pool Fences</a>
    <a href="{up}areas/fuquay-varina.html">Service Area</a>
    <a href="{up}faq.html">FAQ</a>
    <a href="{up}blog/">Blog</a>
  </nav>
  <div class="header-actions">
    <a class="phone-link" data-call href="tel:{PHONE_TEL}" aria-label="Call {BRAND} at {PHONE_TEXT}">{PHONE_SVG}<span>{PHONE_TEXT}</span></a>
    <a class="btn btn-primary btn-sm" href="#quote">Free Estimate</a>
    <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false" aria-controls="mobile-nav"><span></span><span></span><span></span></button>
  </div>
</div>
<nav class="mobile-nav" id="mobile-nav" aria-label="Mobile">
  <a href="{up}services/vinyl-fences.html">Vinyl Fences</a>
  <a href="{up}services/wood-privacy-fences.html">Wood &amp; Privacy</a>
  <a href="{up}services/aluminum-pool-fences.html">Aluminum &amp; Pool-Code</a>
  <a href="{up}services/chain-link-fences.html">Chain Link</a>
  <a href="{up}areas/fuquay-varina.html">Service Area</a>
  <a href="{up}faq.html">FAQ</a>
  <a href="{up}blog/">Blog</a>
  <a href="#quote">Get a Quote</a>
  <a class="phone-link" data-call href="tel:{PHONE_TEL}">Call {PHONE_TEXT}</a>
</nav>
</header>
"""

def crumbs(depth, trail):
    """trail: list of (label, href|None). Renders visible breadcrumbs + BreadcrumbList JSON-LD."""
    if not trail: return "", ""
    up = "../" * depth
    parts, items = [f'<a href="{up}index.html">Home</a>'], [
        {"name": "Home", "url": f"{BASE}/"}]
    for i, (label, href) in enumerate(trail):
        if href:
            parts.append(f'<a href="{up}{href}">{label}</a>')
            items.append({"name": label, "url": f"{BASE}/{href}"})
        else:
            parts.append(f'<span aria-current="page">{label}</span>')
            items.append({"name": label, "url": None})
    nav = ('<nav class="crumbs" aria-label="Breadcrumb"><div class="container">'
           + ' <span class="sep">/</span> '.join(parts) + '</div></nav>')
    li = []
    for i, it in enumerate(items, 1):
        u = f',"item":"{it["url"]}"' if it["url"] else ""
        li.append(f'{{"@type":"ListItem","position":{i},"name":"{it["name"]}"{u}}}')
    ld = ('<script type="application/ld+json">{"@context":"https://schema.org",'
          '"@type":"BreadcrumbList","itemListElement":[' + ",".join(li) + ']}</script>')
    return nav, ld

def _form_anchor(page_source):
    """Stable heading id. Pages that already shipped keep their existing ids."""
    pinned = {
        "home": 7031,
        "faq": 1490,
        "services/vinyl-fences": 444,
        "services/wood-privacy-fences": 3930,
        "services/aluminum-pool-fences": 6018,
        "services/chain-link-fences": 5973,
        "areas/fuquay-varina": 5179,
        "areas/holly-springs": 9683,
        "areas/angier": 9328,
        "areas/willow-spring": 2443,
        "areas/garner": 8371,
    }
    if page_source in pinned:
        return pinned[page_source]
    return zlib.crc32(page_source.encode("utf-8")) % 9999

def form(page_source, heading="Get Your Free Fence Estimate", depth=0):
    up = "../" * depth
    qid = _form_anchor(page_source)
    return f"""<section class="section quote" id="quote" aria-labelledby="q-{qid}">
<div class="container quote-inner">
  <div class="quote-intro">
    <p class="eyebrow eyebrow-light">Free Estimate</p>
    <h2 id="q-{qid}">{heading}</h2>
    <p>Tell us about your project and we'll reach out to schedule a free, no-obligation estimate.
       Prefer to talk now? <a class="quote-phone" data-call href="tel:{PHONE_TEL}">Call {PHONE_TEXT}</a>.</p>
    <ul class="quote-points">
      <li>Free on-site measurement</li>
      <li>No obligation, no pressure</li>
      <li>Local crew, {CITY} and nearby</li>
    </ul>
  </div>
  <div class="quote-form-wrap">
    <form class="lead-form" data-lead-form data-page-source="{page_source}" novalidate>
      <div class="field"><label for="n-{page_source}">Full Name</label>
        <input type="text" id="n-{page_source}" name="fullName" autocomplete="name" required /></div>
      <div class="field-row">
        <div class="field"><label for="p-{page_source}">Phone</label>
          <input type="tel" id="p-{page_source}" name="phone" autocomplete="tel" inputmode="tel" required /></div>
        <div class="field"><label for="z-{page_source}">Zip Code</label>
          <input type="text" id="z-{page_source}" name="zip" autocomplete="postal-code" inputmode="numeric" maxlength="5" pattern="[0-9]{{5}}" required /></div>
      </div>
      <div class="field"><label for="e-{page_source}">Email</label>
        <input type="email" id="e-{page_source}" name="email" autocomplete="email" required /></div>
      <div class="field"><label for="a-{page_source}">Property Address</label>
        <input type="text" id="a-{page_source}" name="address" autocomplete="street-address" placeholder="Where would the fence go?" required />
        <span class="hint">27526 covers a lot of ground &mdash; the street address tells us if we can reach you.</span></div>
      <div class="field-row">
        <div class="field"><label for="f-{page_source}">Fence Type</label>
          <select id="f-{page_source}" name="fenceType" required>
            <option value="" disabled selected>Choose one&hellip;</option>
            <option>Vinyl</option><option>Wood</option><option>Aluminum</option>
            <option>Chain Link</option><option>Not sure yet</option></select></div>
        <div class="field"><label for="t-{page_source}">Timeline</label>
          <select id="t-{page_source}" name="timeline" required>
            <option value="" disabled selected>Choose one&hellip;</option>
            <option>ASAP</option><option>1-3 months</option><option>Just getting quotes</option></select></div>
      </div>
      <!-- honeypot: hidden from humans, irresistible to bots -->
      <div class="hp" aria-hidden="true"><label for="co-{page_source}">Company</label>
        <input type="text" id="co-{page_source}" name="company" tabindex="-1" autocomplete="off" /></div>
      <button type="submit" class="btn btn-primary btn-block btn-lg">Get My Free Estimate</button>
      <p class="consent">By submitting, you agree to be contacted by {BRAND} by call or text at the number provided about your request. Msg &amp; data rates may apply. Reply STOP to opt out. See our <a href="{up}terms.html">Terms</a> and <a href="{up}privacy.html">Privacy Policy</a>.</p>
      <div class="form-status form-success" role="status" hidden>
        <strong>Thanks! We'll reach out shortly.</strong>
        <span>Want to talk sooner? Call <a data-call href="tel:{PHONE_TEL}">{PHONE_TEXT}</a>.</span></div>
      <div class="form-status form-error" role="alert" hidden>
        Something went wrong. Please call <a data-call href="tel:{PHONE_TEL}">{PHONE_TEXT}</a> or try again.</div>
    </form>
  </div>
</div></section>
"""

def footer(depth):
    up = "../" * depth
    svc = " &middot; ".join(f'<a href="{up}services/{s}.html">{n}</a>' for s, n, _ in SERVICES)
    ar  = " &middot; ".join(f'<a href="{up}areas/{s}.html">{n}</a>' for s, n, _ in AREAS)
    return f"""<footer class="site-footer">
<div class="container footer-inner">
  <div class="footer-brand">
    <span class="brand-text"><span class="brand-line1">{BRAND_L1}</span><span class="brand-line2">{BRAND_L2}</span></span>
    <p class="footer-tag">Residential fence installation for {CITY} and southern Wake County.</p>
  </div>
  <div class="footer-col"><h2 class="footer-h">Contact</h2>
    <p><a data-call href="tel:{PHONE_TEL}">{PHONE_TEXT}</a></p>
    <p class="footer-hours">Call or text for your free estimate.</p></div>
  <div class="footer-col"><h2 class="footer-h">Fence Services</h2><p>{svc}</p>
    <p><a href="{up}faq.html">Fence FAQ</a> &middot; <a href="{up}blog/">Blog</a></p></div>
  <div class="footer-col"><h2 class="footer-h">Service Area</h2><p>{ar}</p>
    <p class="footer-zip">27526 &middot; 27540 &middot; 27501 &middot; 27592 &middot; 27529</p></div>
</div>
<div class="footer-bottom"><div class="container footer-bottom-inner">
  <p>&copy; <span id="year">2026</span> {BRAND}. All rights reserved.</p>
  <p><a href="{up}privacy.html">Privacy Policy</a> &middot; <a href="{up}terms.html">Terms</a></p>
</div></div>
</footer>
<a class="mobile-call-bar" data-call href="tel:{PHONE_TEL}" aria-label="Call {BRAND}">{PHONE_SVG} Call {PHONE_TEXT}</a>
<script src="{up}main.js" defer></script>
</body></html>
"""

def biz_ld():
    areas = ",".join(f'{{"@type":"City","name":"{n}, NC"}}' for _, n, _ in AREAS)
    # Names are stored with HTML entities for the visible nav. JSON-LD needs the raw "&".
    offers = ",".join(
        f'{{"@type":"Offer","itemOffered":{{"@type":"Service","name":"{html.unescape(h)}"}}}}'
        for _, _, h in SERVICES)
    return f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":["HomeAndConstructionBusiness","GeneralContractor"],
"@id":"{BIZ_ID}","name":"{BRAND}","url":"{BASE}/","telephone":"{PHONE_TEL}",
"image":"{BASE}/images/og-image.jpg","priceRange":"$$",
"description":"Residential fence installation in {CITY}, NC and southern Wake County. Vinyl, wood privacy, aluminum pool-code and chain link fencing.",
"areaServed":[{areas}],
"address":{{"@type":"PostalAddress","addressLocality":"{CITY}","addressRegion":"{STATE}","postalCode":"27526","addressCountry":"US"}},
"hasOfferCatalog":{{"@type":"OfferCatalog","name":"Fence Installation Services","itemListElement":[{offers}]}}}}
</script>"""

def ref_ld():
    """Lightweight reference to the same business entity — prevents duplicate-entity confusion."""
    return f'<script type="application/ld+json">{{"@context":"https://schema.org","@id":"{BIZ_ID}"}}</script>'

def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

# =============================== PAGE CONTENT ===============================

SERVICE_BODY = {
"vinyl-fences": ("""
<h2>Why vinyl works well in Fuquay-Varina</h2>
<p>Vinyl is the most-requested fence material around Fuquay-Varina, and the reason is maintenance. Central
North Carolina gets about <strong>47 inches of rain a year</strong> across roughly 105 rainy days, with
humidity that stays uncomfortable from June into September. Wood in that climate needs staining and
sealing on a cycle. Vinyl does not &mdash; no painting, no staining, no rot.</p>
<h2>What nobody tells you about white vinyl here: red clay</h2>
<p>Our soil is <strong>Cecil series</strong> &mdash; North Carolina's official state soil &mdash; and it is
iron-rich. When rain hits bare clay it splashes upward, and the iron oxide in it <em>chemically bonds</em>
to surfaces rather than sitting on top like ordinary dirt. That is why the bottom 12 to 18 inches of a
white vinyl fence is the first part to discolor, especially along a new-construction lot or a mulch bed
where soil is still exposed.</p>
<p>Two things fix it, and neither is a pressure washer on full blast:</p>
<ul class="prose-list">
  <li><strong>Get something growing along the fence line.</strong> Grass or mulch stops the splash at the
      source. This prevents more staining than any cleaning product removes.</li>
  <li><strong>Clean it with the right chemistry, not high pressure.</strong> Vinyl is non-porous, so the
      stain sits at the surface and lifts with the correct cleaner. High PSI can scar the panel and force
      water into joints.</li>
</ul>
<p>And a local timing note: <strong>pine pollen peaks from late March into early April</strong> here. Every
white fence in town looks dirty for a few weeks. Wash after the pollen drops, not during.</p>
<h2>Styles we install</h2>
<ul class="prose-list">
  <li><strong>Vinyl privacy</strong> &mdash; 6 ft solid panels, the standard choice for backyards in town limits</li>
  <li><strong>Vinyl picket</strong> &mdash; a better fit for the older streets near the historic districts</li>
  <li><strong>Semi-privacy and lattice-top</strong> &mdash; privacy with some light through</li>
</ul>
<p>Ask about UV-inhibited formulations. With <strong>216 sunny days</strong> and about 35 days over 90&deg;F
a year, a south- or west-facing run takes noticeably more sun than the same fence on the north side.</p>
""", "Vinyl fence installation in Fuquay-Varina, NC. Low-maintenance privacy and picket vinyl built for Piedmont humidity, red clay and sun. Free estimates."),

"wood-privacy-fences": ("""
<h2>Wood privacy fencing, built for Piedmont conditions</h2>
<p>A wood privacy fence is still the most common request in Fuquay-Varina backyards, and done properly it
holds up well here. Done carelessly it does not &mdash; and the failure points in central North Carolina
are specific.</p>
<h2>What actually breaks a wood fence here</h2>
<ul class="prose-list">
  <li><strong>Humidity and 47 inches of rain a year.</strong> The north-facing side of a board fence stays
      damp longest and mildews first. Pressure-treated or naturally rot-resistant species in ground contact
      is not optional in this climate.</li>
  <li><strong>Ground contact.</strong> Fuquay-Varina's ordinance already requires a <strong>2-inch minimum
      clearance</strong> between the bottom of the fence and finished grade, for stormwater drainage. That
      rule also happens to be exactly what keeps the bottom board from wicking moisture year-round.</li>
  <li><strong>Freeze-thaw ratcheting.</strong> We average a January low near 30&deg;F but only about 3
      inches of snow. That means dozens of shallow freeze-thaw cycles a season rather than one deep freeze.
      In high-clay soil that cycling works a post loose over time &mdash; arguably harder on a fence than a
      northern winter.</li>
  <li><strong>Native subterranean termites</strong> are a year-round concern statewide. Any untreated wood
      in ground contact is at risk.</li>
</ul>
<h2>Posts are where the job is won or lost</h2>
<p>Under about eight inches of friendly sandy loam, Fuquay-Varina is <strong>dense red clay</strong> &mdash;
35 to 70 percent clay content. Essentially every post hole in this town is a clay hole. A few consequences
worth knowing before you compare quotes:</p>
<ul class="prose-list">
  <li><strong>Auger refusal is normal.</strong> Our clay formed over weathered rock, so on slopes and eroded
      lots a hole or two in a run will hit saprolite. That is the ground, not a bad crew.</li>
  <li><strong>A clay hole holds water.</strong> Gravel at the base and a concrete collar crowned to shed
      water away from the post are what keep the post from sitting in a bathtub.</li>
  <li><strong>New-construction lots are different.</strong> On recently built lots the native soil profile
      has been stripped, graded and compacted, so we're working in disturbed subsoil &mdash; denser and less
      predictable than an established yard.</li>
</ul>
<p>Industry practice in this soil is roughly <strong>one third of post length below grade</strong> &mdash;
about 24 to 36 inches for a 6-foot fence. That is a practice standard, not a code requirement; the state
building code's 12-inch footing minimum applies to structures, and Fuquay-Varina does not require a permit
or inspection for a residential fence at all.</p>
""", "Wood privacy fence installation in Fuquay-Varina, NC. Board-on-board and shadowbox privacy fencing set properly in Piedmont red clay. Free estimates."),

"aluminum-pool-fences": ("""
<h2>Aluminum fencing and North Carolina pool-barrier code</h2>
<p>Powder-coated aluminum is the go-to for pool enclosures and for open yards where you want a boundary
without blocking the view. It does not rust, it does not need painting, and it handles our humidity
without complaint.</p>
<h2>If it's going around a pool, the code is specific</h2>
<p>Pool barriers in North Carolina fall under the <strong>2024 NC Residential Code, Appendix NC-A</strong>,
which took effect January 1, 2025. The requirements that most often cause a failed inspection:</p>
<ul class="prose-list">
  <li><strong>48 inches minimum height</strong>, measured from grade on the pool side</li>
  <li><strong>2-inch maximum gap</strong> between grade and the bottom of the barrier over a non-solid
      surface &mdash; 4 inches over a solid surface like concrete</li>
  <li><strong>No opening may pass a 4-inch sphere</strong></li>
  <li><strong>Gates must be self-closing and self-latching</strong></li>
  <li>The latch release rule runs in <em>opposite directions</em> depending on hardware: a non-self-locking
      release must sit <strong>at least 54 inches</strong> above the surface, while a self-locking release
      must sit <strong>no more than 54 inches</strong> above it. This is the single most commonly missed
      detail on a pool gate.</li>
  <li>Pool equipment stays <strong>at least 36 inches</strong> outside the barrier</li>
</ul>
<h2>The Fuquay-Varina wrinkle</h2>
<p>A fence alone needs no permit in Fuquay-Varina. <strong>A pool does</strong> &mdash; and the Town runs its
own Inspections Department rather than deferring to Wake County, so your barrier gets inspected locally at
134 N. Main Street. If your address is on the Harnett County side of the 27526 zip, that inspection is
Harnett County's instead.</p>
<p>One conflict worth planning around: the Town caps <strong>front-yard fences at 4 feet</strong> and
prohibits opaque fencing in front yards. Since the pool-barrier minimum is 48 inches &mdash; exactly 4 feet
&mdash; a front-yard pool enclosure sits precisely at the ceiling with no margin. Most pools here are better
sited where the 6-foot side and rear yard limit applies.</p>
<p>We'll confirm current requirements with the Town before we build. Codes change, and we would rather make
a phone call than fail an inspection.</p>
""", "Aluminum and pool-code fence installation in Fuquay-Varina, NC. Rust-proof powder-coated aluminum built to NC 2024 pool barrier code. Free estimates."),

"chain-link-fences": ("""
<h2>Chain link &mdash; the practical option</h2>
<p>When the job is containing a dog, marking a property line, or enclosing a large back lot on a budget,
chain link still does it better per dollar than anything else. Galvanized or black vinyl-coated, and the
coated version disappears against a treeline far better than most people expect.</p>
<h2>What Fuquay-Varina's ordinance says about chain link specifically</h2>
<p>The Town's Land Development Ordinance calls chain link out by name. Inside the corporate limits,
<strong>chain link must be black or green coated</strong> &mdash; bare galvanized is not an approved
material. In nonresidential zones it is prohibited in front yards entirely.</p>
<p>Out in the <strong>ETJ</strong>, the rules loosen considerably: the ordinance states that no fence
material is prohibited and there is no maximum height in side and rear yards. Same mailing address,
different rules. We'll tell you which applies to your lot before we quote it.</p>
<h2>Where chain link makes sense here</h2>
<ul class="prose-list">
  <li><strong>Larger lots</strong> in the ETJ and out toward the Harnett County line, where you're fencing
      real acreage and cost per foot decides the project</li>
  <li><strong>Dog runs and pet containment</strong> &mdash; fast, durable, and you can see through it</li>
  <li><strong>Back and side boundary lines</strong> where appearance from the street isn't a factor</li>
  <li><strong>Around outbuildings</strong> and equipment</li>
</ul>
<p>The same ordinance details apply as any other fence: finished side facing outward, a 2-inch clearance at
grade for drainage, and keep it about 3 inches inside the property line so there's no boundary dispute
later.</p>
""", "Chain link fence installation in Fuquay-Varina, NC. Galvanized and black vinyl-coated chain link for pets, property lines and large lots. Free estimates."),
}

AREA_BODY = {
"fuquay-varina": ("""
<h2>One zip code, two counties, two sets of rules</h2>
<p>Fuquay-Varina has exactly one zip code &mdash; <strong>27526</strong> &mdash; and it covers roughly
<strong>98 square miles</strong> against a town of about 17.6. The zip is nearly five times the size of the
municipality, and it crosses a county line: the Town itself sits entirely in <strong>Wake County</strong>,
while the southern part of the zip is in <strong>Harnett County</strong>.</p>
<p>The practical consequence catches almost everyone: <strong>your mailing address does not tell you which
fence rules apply to your yard.</strong> Two neighbors with identical "Fuquay-Varina, NC 27526" addresses
can be under different height limits, different school districts and different county governments.</p>
<div class="callout">
  <h3>Fence height in Fuquay-Varina</h3>
  <table class="mini-table">
    <thead><tr><th></th><th>Corporate limits</th><th>ETJ</th></tr></thead>
    <tbody>
      <tr><td>Front yard</td><td>4 ft max, opaque fences prohibited</td><td>4 ft</td></tr>
      <tr><td>Side / rear yard</td><td><strong>6 ft max</strong></td><td><strong>No maximum</strong></td></tr>
    </tbody>
  </table>
  <p class="callout-note">You may see other sites claim 8 feet for side and rear yards. The Town's own Land
  Development Ordinance says <strong>six</strong>. We build to the ordinance.</p>
</div>
<h2>You probably don't need a permit &mdash; but you do need your HOA</h2>
<p>Straight from the Town's FAQ: <em>a permit is not required for the installation of a fence in
Fuquay-Varina's corporate limits or ETJ.</em> A pool, a shed or a detached garage does need one. A fence
does not.</p>
<p>What you almost certainly <em>do</em> need is written architectural approval from your HOA. In a town
where a large share of homes sit in newer master-planned communities &mdash; South Lakes, North Lakes,
Serenity, Sunset Bluffs, Brighton Ridge &mdash; the HOA is the real gatekeeper, not the municipality. That
surprises people, because it's the reverse of what they expect. Older pockets like the Fuquay Springs
historic district or the Village of Sippihaw often have no HOA at all.</p>
<h2>Other ordinance details we build to</h2>
<ul class="prose-list">
  <li>Finished side faces outward, toward the street or your neighbor</li>
  <li>Minimum <strong>2-inch clearance</strong> from the bottom of the fence to grade, for stormwater drainage</li>
  <li>Set the fence about <strong>3 inches inside your property line</strong> to avoid boundary disputes</li>
  <li>No fences in public right-of-way or in utility, drainage or stormwater easements; 8 feet off the line
      in landscape buffer easements</li>
  <li>Chain link inside town limits must be black or green coated</li>
</ul>
<h2>The neighborhoods we work in</h2>
<p>From the established side of town &mdash; Bentwinds, Sunset Lake, High Grove, Crooked Creek, Village of
Sippihaw, Northwyck, Prescott Downs &mdash; out to the newer communities off the 401 and 55 corridors:
South Lakes, North Lakes, Serenity, Sunset Bluffs, Lakestone Village, Maggie Run, Rowland's Grant and
Brighton Ridge.</p>
<p>Roughly <strong>48% of the housing in 27526 was built in the last sixteen years</strong>, and builders
here almost never include a fence. If you just closed on a new build and are staring at a bare graded lot,
you're in the majority &mdash; and it's usually worth talking to your neighbors, because fencing a run of
adjoining yards at the same time is cheaper for everyone.</p>
<h2>A little local history, since we're neighbors</h2>
<p>The town is two towns. <strong>Fuquay Springs</strong> grew up around a mineral spring a Fuquay
descendant turned up while plowing a field around 1858 &mdash; the spring house still stands in Fuquay
Mineral Spring Park. <strong>Varina</strong> was named for a woman who signed her letters to a Civil War
soldier named Ballentine that way; he married her and named his store and post office after the signature.
The two merged in 1963, and you can still walk between the two downtowns in about fifteen minutes &mdash;
S. Main on the Fuquay side, Broad Street on the Varina side, where Aviator Brewing sits in the 1903 train
depot.</p>
""", "Fence installation in Fuquay-Varina, NC 27526. Local crew who knows the Town's 6-ft ordinance, ETJ rules, HOA approvals and Piedmont red clay. Free estimates."),

"holly-springs": ("""
<h2>Fence installation in Holly Springs, NC</h2>
<p>Holly Springs sits about five miles northwest of us &mdash; the closest of our neighbor towns and one of
the fastest-growing in Wake County, from roughly 41,000 residents at the 2020 census to over
<strong>50,000</strong> by 2025. One clean zip code, <strong>27540</strong>, which makes life simpler than
it is in our own town.</p>
<h2>What's different here</h2>
<p>Holly Springs is its own municipality with its own ordinance, so fence standards, height limits and any
permit requirements are set by the Town of Holly Springs rather than Fuquay-Varina. If you're in an HOA
neighborhood &mdash; and a lot of Holly Springs is &mdash; architectural approval usually comes before
anything else. We'll confirm the current local requirements before we quote, not after.</p>
<h2>Same soil, same considerations</h2>
<p>You're on the same Piedmont ground we are: <strong>Cecil red clay</strong> starting roughly eight inches
below the surface, the same 47 inches of annual rain, the same late-March pine pollen that makes every
white fence in the county look dirty for three weeks. Everything we do about post drainage, ground
clearance and material choice applies here identically.</p>
<h2>What we install in Holly Springs</h2>
<p>Vinyl privacy and picket, wood privacy, powder-coated aluminum including pool-code enclosures, and
chain link. With the volume of newer construction here, the most common call we get is from someone who
just closed on a house with a bare backyard and a builder who didn't include a fence.</p>
""", "Fence installation in Holly Springs, NC 27540. Vinyl, wood privacy, aluminum pool-code and chain link fencing. Local crew, free estimates."),

"angier": ("""
<h2>Fence installation in Angier, NC</h2>
<p>Angier is about six miles southeast of Fuquay-Varina, and it is growing faster in percentage terms than
anywhere else nearby &mdash; from around 5,300 residents in 2020 to roughly <strong>9,400</strong> by 2025,
a <strong>75% increase in five years</strong>. Zip code <strong>27501</strong>.</p>
<h2>The important difference: Angier is in Harnett County</h2>
<p>This matters more than the six-mile distance suggests. Angier is a <strong>Harnett County</strong>
municipality, not Wake. Different county government, different school system, different permitting
authority. If you've moved here from the Wake County side and assume the rules carry over, they don't
necessarily.</p>
<p>It also cuts the other way: plenty of homes with a <em>Fuquay-Varina</em> mailing address are actually
in Harnett County, because zip 27526 crosses the county line. If you're somewhere in that southern
stretch, it's worth knowing which county you're actually in before you plan a fence.</p>
<h2>Growing fast, on fresh lots</h2>
<p>Angier's growth means a lot of new construction, and new construction means bare graded lots with no
fence, no mature trees and freshly compacted subsoil. We dig those every week. Compacted new-build clay
behaves differently from an established yard &mdash; denser, less predictable &mdash; and it's worth
setting posts accordingly.</p>
<h2>What we install in Angier</h2>
<p>Vinyl privacy, wood privacy, aluminum and pool-code enclosures, and chain link for larger lots &mdash;
and out this way, lots do get larger. Free estimates, same as everywhere we work.</p>
""", "Fence installation in Angier, NC 27501. Harnett County fencing — vinyl, wood privacy, aluminum and chain link. Local crew, free estimates."),

"willow-spring": ("""
<h2>Fence installation in Willow Spring, NC</h2>
<p>Willow Spring is about seven miles east of us, zip code <strong>27592</strong>. It's worth getting the
name right, because locals notice: the community is <strong>Willow Spring, singular</strong>, even though
the high school out here is Willow Springs High School.</p>
<h2>Unincorporated &mdash; which changes the rules</h2>
<p>Willow Spring has <strong>no town government</strong>. It's an unincorporated community, which means
there is no municipal fence ordinance to comply with. Instead, county rules apply &mdash; and Willow Spring
straddles a county line of its own, with the western side in <strong>Wake County</strong> and the eastern
edge in <strong>Johnston County</strong>.</p>
<p>In practice this often means fewer restrictions than in-town Fuquay-Varina, where side and rear fences
cap at six feet. But "fewer municipal rules" is not "no rules" &mdash; easements, setbacks, property lines
and any HOA covenants still govern. We'll sort out which apply to your specific lot.</p>
<h2>Bigger lots, different projects</h2>
<p>Yards out here tend to run larger than in-town lots, which changes what makes sense. Fencing an acre is a
different conversation from fencing a quarter-acre backyard &mdash; chain link and split-rail start to
compete with privacy fence on cost, and partial enclosures around just the area you actually use are often
smarter than ringing the whole property.</p>
<h2>What we install in Willow Spring</h2>
<p>Vinyl, wood privacy, aluminum and pool-code fencing, and chain link. The same Piedmont red clay applies
out here, so the same care with post drainage does too.</p>
""", "Fence installation in Willow Spring, NC 27592. Unincorporated Wake and Johnston County fencing for larger lots. Vinyl, wood, aluminum, chain link. Free estimates."),

"garner": ("""
<h2>Fence installation in Garner, NC</h2>
<p>Garner sits about fourteen miles northeast of Fuquay-Varina on the southern edge of Raleigh &mdash;
roughly <strong>41,500</strong> residents and, conveniently, a single zip code: <strong>27529</strong>.</p>
<h2>An older housing stock, and what that means</h2>
<p>Garner is a different kind of market from the new-build communities closer to us. There's real
established housing here, and established housing means <strong>replacement work</strong> rather than
first-time installation &mdash; fences that went in fifteen or twenty years ago and have reached the end of
their service life.</p>
<p>That's a different job. Old posts have to come out, and in Piedmont clay a post set in concrete two
decades ago does not want to leave. Sometimes the existing line can be reused, sometimes it can't. It's
also a chance to fix whatever the original installer got wrong &mdash; usually ground clearance, usually
drainage at the post base.</p>
<h2>Garner has its own ordinance</h2>
<p>As an incorporated Wake County town, Garner sets its own fence standards, height limits and permit
requirements. They are not Fuquay-Varina's. We'll confirm the current rules with the Town before quoting
your project.</p>
<h2>What we install in Garner</h2>
<p>Vinyl privacy and picket, wood privacy, powder-coated aluminum and pool-code enclosures, chain link, and
replacement of existing fencing. Free estimates.</p>
""", "Fence installation in Garner, NC 27529. New and replacement fencing — vinyl, wood privacy, aluminum pool-code, chain link. Local crew, free estimates."),
}

FAQS = [
 ("Do I need a permit to build a fence in Fuquay-Varina?",
  "No. The Town of Fuquay-Varina does not require a permit to install a fence inside the corporate limits or the ETJ. Pools, sheds, detached garages and other accessory structures do require permits. If your fence is going around a pool, the pool is permitted and the barrier gets inspected."),
 ("How tall can my fence be?",
  "Inside Fuquay-Varina's corporate limits, side and rear yard fences max out at 6 feet and front yard fences at 4 feet, with opaque fences prohibited in front yards. In the ETJ there is no maximum height for side and rear yards. Some websites list 8 feet for Fuquay-Varina — the Town's own Land Development Ordinance says six."),
 ("How do I know if I'm in the town limits or the ETJ?",
  "Your mailing address won't tell you. Zip 27526 covers about 98 square miles across both Wake and Harnett counties, while the Town itself is about 17.6 square miles and entirely in Wake County. The Town's Planning Department can confirm your jurisdiction, and we check it before quoting."),
 ("Does my HOA have to approve the fence?",
  "Almost certainly, and this is the step people skip. HOA covenants can be stricter than the Town's standards, and Town standards still apply on top of them. In Fuquay-Varina the HOA is usually the real gatekeeper, not the municipality — the opposite of what most homeowners expect."),
 ("How deep do fence posts need to go here?",
  "There is no inspected code depth for a residential fence post in Fuquay-Varina, because fences aren't permitted. Industry practice in our soil is roughly one third of the post length below grade — about 24 to 36 inches for a 6-foot fence. In Piedmont clay, drainage at the base of the hole matters as much as depth."),
 ("Why does my white vinyl fence look orange at the bottom?",
  "Red clay. Our Cecil-series soil is iron-rich, and rain splashing off bare ground carries iron oxide that bonds chemically to the surface rather than sitting on it. It concentrates in the bottom 12 to 18 inches. Getting grass or mulch established along the fence line prevents it better than any cleaner removes it, and it should be cleaned with the right chemistry rather than high pressure."),
 ("When is the best time of year to install a fence?",
  "Spring and fall. Piedmont clay is sticky and gums an auger when saturated, and close to concrete when baked in midsummer. We install year-round, but those are the easiest working windows. One scheduling note: pine pollen peaks from late March into early April, so if appearance matters for photos, plan around it."),
 ("What does North Carolina require for a pool fence?",
  "Under the 2024 NC Residential Code Appendix NC-A: a 48-inch minimum barrier height, no more than a 2-inch gap at grade over non-solid surfaces, no opening that passes a 4-inch sphere, and self-closing, self-latching gates. The latch release rule runs opposite directions depending on whether the latch self-locks — at least 54 inches for non-self-locking, no more than 54 inches for self-locking."),
]

def service_page(slug, nav_name, head_name):
    body, desc = SERVICE_BODY[slug]
    plain_name = html.unescape(head_name)
    title = f"{plain_name} in {CITY}, {STATE} | {BRAND}"
    canon = f"{BASE}/services/{slug}.html"
    svc_ld = (f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Service",'
              f'"name":"{plain_name}","serviceType":"{plain_name}",'
              f'"provider":{{"@id":"{BIZ_ID}"}},'
              f'"areaServed":{{"@type":"City","name":"{CITY}, {STATE}"}},'
              f'"description":"{desc}"}}</script>')
    nav, bc_ld = crumbs(1, [("Services", None), (nav_name.replace("&amp;", "&"), None)])
    return (head(title, desc, canon, 1, ref_ld() + svc_ld + bc_ld) + header(1) + nav +
            f'<main><section class="hero hero-inner"><div class="container hero-content">'
            f'<p class="hero-eyebrow">{CITY}, {STATE}</p><h1>{head_name} in {CITY}</h1>'
            f'<p class="hero-sub">Installed by a local crew that knows this town\'s ordinance and this town\'s soil.</p>'
            f'<div class="hero-cta"><a class="btn btn-primary btn-lg" href="#quote">Get My Free Estimate</a>'
            f'<a class="btn btn-ghost btn-lg" data-call href="tel:{PHONE_TEL}">Call {PHONE_TEXT}</a></div>'
            f'</div></section><section class="section"><div class="container prose">{body}'
            f'<p class="prose-cross">Other services: ' +
            " &middot; ".join(f'<a href="{s}.html">{n}</a>' for s, n, _ in SERVICES if s != slug) +
            f'</p></div></section>' + form(f"services/{slug}", depth=1) + '</main>' + footer(1))

def area_page(slug, name, zipc):
    body, desc = AREA_BODY[slug]
    title = f"Fence Company in {name}, {STATE} | {BRAND}"
    canon = f"{BASE}/areas/{slug}.html"
    nav, bc_ld = crumbs(1, [("Service Area", None), (name, None)])
    return (head(title, desc, canon, 1, ref_ld() + bc_ld) + header(1) + nav +
            f'<main><section class="hero hero-inner"><div class="container hero-content">'
            f'<p class="hero-eyebrow">{name}, {STATE} &middot; {zipc}</p>'
            f'<h1>Fence Installation in {name}, {STATE}</h1>'
            f'<p class="hero-sub">Wood, vinyl, aluminum and chain link &mdash; installed by a local crew.</p>'
            f'<div class="hero-cta"><a class="btn btn-primary btn-lg" href="#quote">Get My Free Estimate</a>'
            f'<a class="btn btn-ghost btn-lg" data-call href="tel:{PHONE_TEL}">Call {PHONE_TEXT}</a></div>'
            f'</div></section><section class="section"><div class="container prose">{body}'
            f'<h2>Fence styles we install in {name}</h2><ul class="prose-list">' +
            "".join(f'<li><a href="../services/{s}.html">{n}</a></li>' for s, n, _ in SERVICES) +
            f'</ul><p class="prose-cross">Nearby: ' +
            " &middot; ".join(f'<a href="{s}.html">{n}</a>' for s, n, _ in AREAS if s != slug) +
            f'</p></div></section>' + form(f"areas/{slug}", f"Free Fence Estimate in {name}", depth=1) +
            '</main>' + footer(1))

def home():
    title = f"Fence Company in {CITY}, {STATE} | {BRAND} &mdash; Free Estimates"
    desc = (f"{BRAND} installs vinyl, wood privacy, aluminum pool-code and chain link fences in "
            f"{CITY}, NC 27526 and southern Wake County. Local crew, free estimates.")
    cards = ""
    for s, n, h in SERVICES:
        blurb = {"vinyl-fences":"Low-maintenance privacy and picket vinyl &mdash; no painting, no staining, and it shrugs off Piedmont humidity.",
                 "wood-privacy-fences":"Board-on-board and shadowbox privacy, set deep with proper drainage for red clay.",
                 "aluminum-pool-fences":"Rust-proof powder-coated aluminum, including enclosures built to North Carolina pool-barrier code.",
                 "chain-link-fences":"Affordable and durable for pets, property lines and larger lots. Black or green coated in town limits."}[s]
        cards += (f'<article class="service-card"><div class="service-body"><h3>{n}</h3><p>{blurb}</p>'
                  f'<p class="card-link"><a href="services/{s}.html">{n} details &rarr;</a></p></div></article>')
    zips = "".join(f'<li><strong><a href="areas/{s}.html">{n}</a></strong> <span>{z}</span></li>'
                   for s, n, z in AREAS)
    return (head(title, desc, f"{BASE}/", 0, biz_ld()) + header(0) +
f"""<main>
<section class="hero" aria-labelledby="hero-heading">
  <div class="hero-overlay"></div>
  <div class="container hero-content">
    <p class="hero-eyebrow">{CITY} &amp; Southern Wake County, {STATE}</p>
    <h1 id="hero-heading">Fence Installation in {CITY}, {STATE} &mdash; Done Right the First Time</h1>
    <p class="hero-sub">Vinyl, wood privacy, aluminum and chain link, built for Piedmont clay and Carolina
       humidity. Always a <strong>free estimate</strong>.</p>
    <div class="hero-cta">
      <a class="btn btn-primary btn-lg" href="#quote">Get My Free Estimate</a>
      <a class="btn btn-ghost btn-lg" data-call href="tel:{PHONE_TEL}">{PHONE_SVG} Call {PHONE_TEXT}</a>
    </div>
    <ul class="hero-badges"><li>Free on-site estimates</li><li>Local crew</li><li>We handle the HOA paperwork question</li></ul>
  </div>
</section>

<section class="section services" id="services">
  <div class="container">
    <div class="section-head"><p class="eyebrow">Our Services</p>
      <h2>Fence Installation for {CITY} Homeowners</h2>
      <p class="section-lead">Every style we install is matched to your yard, your HOA, and the ground under it.</p></div>
    <div class="card-grid">{cards}</div>
  </div>
</section>

<section class="section why" id="why">
  <div class="container">
    <div class="section-head"><p class="eyebrow">Why {BRAND}</p>
      <h2>We Actually Know This Town</h2></div>
    <div class="why-grid">
      <div class="why-item"><h3>We know which rules apply to your lot</h3>
        <p>Inside the town limits, side and rear fences cap at 6 feet. In the ETJ there's no maximum. Same
           27526 address, different rules &mdash; we check before we quote.</p></div>
      <div class="why-item"><h3>No permit needed &mdash; but your HOA matters</h3>
        <p>Fuquay-Varina doesn't require a fence permit. Your HOA almost certainly requires written
           approval. We'll tell you what you actually need.</p></div>
      <div class="why-item"><h3>Built for red clay</h3>
        <p>Under about eight inches of topsoil this town is dense Cecil clay. Post drainage and a crowned
           collar are what keep a fence plumb through our freeze-thaw cycles.</p></div>
      <div class="why-item"><h3>Every fence style</h3>
        <p>Vinyl, wood, aluminum and chain link &mdash; one local crew for whatever your property needs.</p></div>
    </div>
  </div>
</section>

<section class="section area" id="area">
  <div class="container area-inner"><div class="area-copy">
    <p class="eyebrow">Service Area</p>
    <h2>Serving {CITY} &amp; Southern Wake County</h2>
    <p>From downtown Fuquay-Varina out to Holly Springs, Angier, Willow Spring and Garner. Zip 27526 covers
       about 98 square miles across two counties, so tell us your street address and we'll confirm we can
       reach you.</p>
    <ul class="zip-list">{zips}</ul>
    <p class="area-note">Not sure if you're in our area?
      <a data-call href="tel:{PHONE_TEL}">Call {PHONE_TEXT}</a> and we'll let you know.</p>
  </div></div>
</section>
""" + form("home", depth=0) + "</main>" + footer(0))

def faq_page():
    title = f"Fence FAQ &mdash; {CITY}, {STATE} | {BRAND}"
    desc = ("Permits, height limits, HOA approval, post depth, red clay staining and NC pool barrier code "
            f"— answered for {CITY} homeowners.")
    qs = ",".join(
        '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
        % (_json(q), _json(a)) for q, a in FAQS)
    faq_ld = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage",'
              '"mainEntity":[' + qs + ']}</script>')
    nav, bc_ld = crumbs(0, [("FAQ", None)])
    body = "".join(f'<div class="faq-item"><h2>{html.escape(q)}</h2><p>{html.escape(a)}</p></div>'
                   for q, a in FAQS)
    return (head(title, desc, f"{BASE}/faq.html", 0, ref_ld() + faq_ld + bc_ld) + header(0) + nav +
            f'<main><section class="hero hero-inner"><div class="container hero-content">'
            f'<p class="hero-eyebrow">Fence FAQ</p><h1>Fence Questions, Answered for {CITY}</h1>'
            f'<p class="hero-sub">Permits, heights, HOAs, clay and pool code &mdash; the questions we get most.</p>'
            f'</div></section><section class="section"><div class="container prose faq-list">{body}</div></section>'
            + form("faq", depth=0) + '</main>' + footer(0))

def _json(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'

def privacy_page():
    title = f"Privacy Policy | {BRAND}"
    nav, bc_ld = crumbs(0, [("Privacy Policy", None)])
    return (head(title, f"Privacy policy for {BRAND}.", f"{BASE}/privacy.html", 0, ref_ld() + bc_ld)
            + header(0) + nav + f"""<main><section class="section"><div class="container prose">
<h1>Privacy Policy</h1>
<p><em>Last updated: September 2026</em></p>
<h2>What we collect</h2>
<p>When you submit our estimate form we collect the name, phone number, email address, property address and
zip code you provide, along with your selected fence type and timeline. We also collect standard analytics
data such as pages visited and referring source.</p>
<h2>How we use it</h2>
<p>We use your information solely to contact you about your fence estimate and to connect you with the local
fence contractor who will perform the work. We do not sell your personal information.</p>
<h2>Who we share it with</h2>
<p>We share your project details with the licensed local fence contractor serving your area so they can
prepare your estimate. We also use service providers &mdash; including analytics and automation tools
&mdash; that process data on our behalf.</p>
<h2>Advertising</h2>
<p>We advertise on Facebook and Instagram and use the Meta Pixel and Google Analytics to measure performance.
These services may set cookies. You can opt out of personalized advertising through your Meta and Google
account settings.</p>
<h2>Your choices</h2>
<p>You can ask us to delete your information at any time by calling {PHONE_TEXT}. If you no longer wish to be
contacted, tell us and we will stop.</p>
<h2>Text Messaging (SMS)</h2>
<p>If you submit an estimate request, we may text you at the number you provide about that request &mdash;
follow-up on your fence estimate, scheduling, and related project updates. Reply STOP to opt out. You can
also call {PHONE_TEXT}. Program details, including message frequency and help instructions, are in our
<a href="terms.html">Terms and Conditions</a>.</p>
<p>No mobile information will be shared with third parties or affiliates for marketing or promotional
purposes. Text-messaging originator opt-in data and consent will not be shared with any third parties.</p>
<h2>Contact</h2>
<p>Questions about this policy? Call {PHONE_TEXT}.</p>
</div></section></main>""" + footer(0))

def terms_page():
    title = f"Terms and Conditions | {BRAND}"
    nav, bc_ld = crumbs(0, [("Terms and Conditions", None)])
    desc = f"Terms and conditions for {BRAND}, including SMS text messaging terms."
    return (head(title, desc, f"{BASE}/terms.html", 0, ref_ld() + bc_ld)
            + header(0) + nav + f"""<main><section class="section"><div class="container prose">
<h1>Terms and Conditions</h1>
<p><em>Last updated: September 2026</em></p>
<h2>Who operates this site</h2>
<p>This website is operated by Smith Asset Group LLC, doing business as {BRAND} (&ldquo;we&rdquo; or
&ldquo;us&rdquo;). {BRAND} is a referral and lead service for homeowners in {CITY}, North Carolina and
nearby communities.</p>
<h2>We are not the fence contractor</h2>
<p>We connect you with an independent licensed local fence contractor. We are not that contractor, and we
do not install the fence ourselves. If you decide to hire the contractor, your agreement for the work is
with the contractor. The contractor is responsible for its own estimates, scheduling, materials, and the
quality of its work.</p>
<h2>No guarantee of pricing, availability, or work</h2>
<p>Requesting an estimate does not guarantee a price, a start date, or that a contractor is available for
your project. We do not guarantee the contractor&rsquo;s pricing, availability, or the quality of any work
the contractor performs.</p>
<h2>Acceptable use</h2>
<p>You may use this site to learn about fence options in our service area and to request an estimate. Do not
misuse the site &mdash; for example by submitting information you know is false, interfering with the site,
or using it for anything unlawful.</p>
<h2>Estimates</h2>
<p>Estimate requests are free and do not require you to purchase anything. Please give accurate project
details so we can tell whether a local contractor can help.</p>
<h2>Limitation of liability</h2>
<p>This site is provided as-is. To the fullest extent allowed by law, Smith Asset Group LLC is not liable
for indirect, incidental, or consequential damages arising from your use of the site, or for the
contractor&rsquo;s acts, omissions, pricing, scheduling, or workmanship.</p>
<h2>SMS / Text Messaging Terms</h2>
<p><strong>Program name:</strong> {BRAND}.</p>
<p>If you submit a fence estimate request and give us a mobile number &mdash; on this website or on a
Facebook or Instagram form we use for estimate requests &mdash; we may text you about that request.
Messages are follow-up about your fence estimate, scheduling, and related project updates. They are not
marketing blasts.</p>
<p>Message frequency varies. Message and data rates may apply.</p>
<p>Reply <strong>STOP</strong> to opt out of further texts. Reply <strong>HELP</strong> for help, or call
{PHONE_TEXT}.</p>
<p>Carriers are not liable for delayed or undelivered messages.</p>
<p>Consent to receive texts is not a condition of purchase. You can opt out at any time by replying STOP.</p>
<p>How we handle your information, including mobile numbers and text-message consent, is described in our
<a href="privacy.html">Privacy Policy</a>.</p>
<h2>North Carolina law</h2>
<p>These terms are governed by the laws of the State of North Carolina.</p>
<h2>Contact</h2>
<p>Questions about these terms? Call {PHONE_TEXT}.</p>
</div></section></main>""" + footer(0))

# ================================= ASSETS =================================
CSS = """:root{--ink:#14281d;--ink-2:#243a2c;--paper:#fff;--mute:#5d6b62;--line:#dfe6e1;
--accent:#2f7d54;--accent-d:#245f41;--warm:#f6f8f6;--rad:10px}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
color:var(--ink);background:var(--paper);-webkit-font-smoothing:antialiased}
img{max-width:100%;height:auto;display:block}
a{color:var(--accent-d)}
.container{width:min(1120px,92%);margin-inline:auto}
.skip-link{position:absolute;left:-9999px;top:0;background:var(--ink);color:#fff;padding:.7rem 1rem;z-index:99}
.skip-link:focus{left:0}
.btn{display:inline-flex;align-items:center;gap:.5rem;justify-content:center;border:0;border-radius:var(--rad);
font-weight:650;text-decoration:none;cursor:pointer;padding:.7rem 1.15rem;font-size:.95rem;transition:.15s}
.btn-primary{background:var(--accent);color:#fff}.btn-primary:hover{background:var(--accent-d)}
.btn-ghost{background:rgba(255,255,255,.12);color:#fff;border:1.5px solid rgba(255,255,255,.55)}
.btn-ghost:hover{background:rgba(255,255,255,.2)}
.btn-lg{padding:.95rem 1.5rem;font-size:1.02rem}.btn-sm{padding:.55rem .9rem;font-size:.88rem}
.btn-block{width:100%}
.site-header{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.97);border-bottom:1px solid var(--line);
backdrop-filter:saturate(180%) blur(8px)}
.header-inner{display:flex;align-items:center;gap:1.2rem;padding:.7rem 0}
.brand{display:flex;align-items:center;gap:.55rem;text-decoration:none;color:var(--ink)}
.brand-mark{color:var(--accent);flex:none}
.brand-text{display:flex;flex-direction:column;line-height:1.04}
.brand-line1{font-weight:800;font-size:1.06rem;letter-spacing:-.02em}
.brand-line2{font-size:.74rem;letter-spacing:.12em;text-transform:uppercase;color:var(--mute)}
.main-nav{display:flex;gap:1.25rem;margin-left:auto}
.main-nav a{color:var(--ink-2);text-decoration:none;font-size:.93rem;font-weight:550}
.main-nav a:hover{color:var(--accent)}
.header-actions{display:flex;align-items:center;gap:.7rem}
.phone-link{display:inline-flex;align-items:center;gap:.4rem;color:var(--ink);text-decoration:none;
font-weight:700;font-size:.93rem;white-space:nowrap}
.nav-toggle{display:none;flex-direction:column;gap:4px;background:0;border:0;padding:.45rem;cursor:pointer}
.nav-toggle span{width:21px;height:2px;background:var(--ink);border-radius:2px}
.mobile-nav{display:none;flex-direction:column;padding:.4rem 4% 1rem;border-top:1px solid var(--line)}
.mobile-nav.open{display:flex}
.mobile-nav a{padding:.6rem 0;text-decoration:none;color:var(--ink-2);border-bottom:1px solid var(--line)}
.crumbs{background:var(--warm);border-bottom:1px solid var(--line);font-size:.83rem;color:var(--mute)}
.crumbs .container{padding:.55rem 0}
.crumbs a{color:var(--mute)}.crumbs .sep{opacity:.5;margin:0 .1rem}
.hero{position:relative;background:linear-gradient(160deg,#1c3626,#0f2017);color:#fff;padding:4.5rem 0 4rem}
.hero-inner{padding:3rem 0 2.6rem}
.hero-content{position:relative;max-width:760px}
.hero-eyebrow{text-transform:uppercase;letter-spacing:.14em;font-size:.76rem;font-weight:700;
color:#9ed3b4;margin:0 0 .6rem}
.hero h1{font-size:clamp(1.85rem,4.4vw,2.9rem);line-height:1.13;margin:0 0 .9rem;letter-spacing:-.022em}
.hero-sub{font-size:1.08rem;color:#d7e6dd;margin:0 0 1.5rem;max-width:58ch}
.hero-cta{display:flex;flex-wrap:wrap;gap:.7rem}
.hero-badges{display:flex;flex-wrap:wrap;gap:1.2rem;list-style:none;padding:0;margin:1.8rem 0 0;
font-size:.87rem;color:#a9cbb8}
.hero-badges li::before{content:"✓ ";color:#6fc191;font-weight:700}
.section{padding:3.6rem 0}
.services{background:var(--warm)}
.section-head{max-width:640px;margin-bottom:2rem}
.eyebrow{text-transform:uppercase;letter-spacing:.14em;font-size:.76rem;font-weight:700;color:var(--accent);margin:0 0 .5rem}
.eyebrow-light{color:#9ed3b4}
.section-head h2,.why h2,.area h2{font-size:clamp(1.45rem,3vw,2rem);margin:0 0 .6rem;letter-spacing:-.02em}
.section-lead{color:var(--mute);margin:0}
.card-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(245px,1fr));gap:1.1rem}
.service-card{background:#fff;border:1px solid var(--line);border-radius:var(--rad);overflow:hidden}
.service-body{padding:1.15rem}
.service-body h3{margin:0 0 .45rem;font-size:1.08rem}
.service-body p{margin:0 0 .7rem;color:var(--mute);font-size:.93rem}
.card-link a{font-weight:650;font-size:.9rem;text-decoration:none}
.why-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr));gap:1.6rem}
.why-item h3{margin:0 0 .4rem;font-size:1.02rem}
.why-item p{margin:0;color:var(--mute);font-size:.93rem}
.area{background:var(--warm)}
.zip-list{list-style:none;padding:0;margin:1.2rem 0;display:grid;
grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:.55rem}
.zip-list li{display:flex;justify-content:space-between;gap:1rem;padding:.6rem .85rem;background:#fff;
border:1px solid var(--line);border-radius:8px;font-size:.92rem}
.zip-list span{color:var(--mute)}
.zip-list a{text-decoration:none;font-weight:650}
.area-note{color:var(--mute);font-size:.92rem}
.prose{max-width:74ch}
.prose h2{font-size:1.28rem;margin:2rem 0 .6rem;letter-spacing:-.015em}
.prose h2:first-child{margin-top:0}
.prose p{margin:0 0 1rem}
.prose-list{margin:0 0 1.1rem;padding-left:1.15rem}
.prose-list li{margin-bottom:.45rem}
.prose-cross{font-size:.9rem;color:var(--mute);border-top:1px solid var(--line);padding-top:1rem;margin-top:1.8rem}
.callout{background:var(--warm);border:1px solid var(--line);border-left:4px solid var(--accent);
border-radius:var(--rad);padding:1.1rem 1.2rem;margin:1.4rem 0}
.callout h3{margin:0 0 .7rem;font-size:1rem}
.callout-note{font-size:.87rem;color:var(--mute);margin:.7rem 0 0}
.mini-table{width:100%;border-collapse:collapse;font-size:.9rem}
.mini-table th,.mini-table td{text-align:left;padding:.45rem .5rem;border-bottom:1px solid var(--line)}
.mini-table th{font-size:.78rem;text-transform:uppercase;letter-spacing:.06em;color:var(--mute)}
.faq-list{max-width:74ch}
.faq-item{border-bottom:1px solid var(--line);padding:1.1rem 0}
.faq-item h2{font-size:1.05rem;margin:0 0 .45rem}
.faq-item p{margin:0;color:var(--ink-2)}
.quote{background:var(--ink);color:#fff}
.quote-inner{display:grid;grid-template-columns:1fr 1fr;gap:2.6rem;align-items:start}
.quote-intro h2{font-size:clamp(1.45rem,3vw,2rem);margin:0 0 .7rem;letter-spacing:-.02em}
.quote-intro p{color:#cfe0d6;margin:0 0 1rem}
.quote-phone{color:#9ed3b4;font-weight:700}
.quote-points{list-style:none;padding:0;margin:0;font-size:.92rem;color:#a9cbb8}
.quote-points li{padding:.28rem 0}
.quote-points li::before{content:"✓ ";color:#6fc191;font-weight:700}
.quote-form-wrap{background:#fff;color:var(--ink);border-radius:12px;padding:1.5rem}
.field{margin-bottom:.85rem;display:flex;flex-direction:column}
.field-row{display:grid;grid-template-columns:1fr 1fr;gap:.75rem}
.field label{font-size:.83rem;font-weight:650;margin-bottom:.3rem}
.field input,.field select{padding:.65rem .7rem;border:1.5px solid var(--line);border-radius:8px;
font-size:.95rem;font-family:inherit;background:#fff;color:var(--ink)}
.field input:focus,.field select:focus{outline:2px solid var(--accent);outline-offset:1px;border-color:var(--accent)}
.hint{font-size:.78rem;color:var(--mute);margin-top:.25rem}
.hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
.consent{font-size:.78rem;color:var(--mute);margin:.7rem 0 0;text-align:center}
.form-status{margin-top:.9rem;padding:.85rem;border-radius:8px;font-size:.92rem}
.form-success{background:#e8f5ee;border:1px solid #b9dfc9}
.form-success strong{display:block;margin-bottom:.2rem}
.form-error{background:#fdecec;border:1px solid #f3c2c2}
.site-footer{background:#0f2017;color:#b7cbc0;font-size:.9rem}
.footer-inner{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:1.8rem;padding:2.6rem 0 2rem}
.footer-brand .brand-text{color:#fff}
.footer-brand .brand-line2{color:#7f9c8c}
.footer-tag{margin:.7rem 0 0;max-width:34ch}
.footer-h{font-size:.78rem;text-transform:uppercase;letter-spacing:.11em;color:#fff;margin:0 0 .7rem}
.footer-col p{margin:0 0 .45rem}
.site-footer a{color:#b7cbc0;text-decoration:none}
.site-footer a:hover{color:#fff;text-decoration:underline}
.footer-zip{font-size:.8rem;color:#7f9c8c}
.footer-bottom{border-top:1px solid #1d3527}
.footer-bottom-inner{display:flex;justify-content:space-between;gap:1rem;padding:1rem 0;font-size:.82rem}
.footer-bottom p{margin:0}
.mobile-call-bar{display:none;position:fixed;left:0;right:0;bottom:0;z-index:60;background:var(--accent);
color:#fff;text-align:center;padding:.85rem;font-weight:700;text-decoration:none;align-items:center;
justify-content:center;gap:.5rem}
@media(max-width:900px){.quote-inner{grid-template-columns:1fr;gap:1.6rem}
.footer-inner{grid-template-columns:1fr 1fr}}
@media(max-width:760px){.main-nav{display:none}.nav-toggle{display:flex}
.phone-link span{display:none}.hero{padding:3rem 0 2.8rem}
.mobile-call-bar{display:flex}body{padding-bottom:3.4rem}
.footer-inner{grid-template-columns:1fr}.footer-bottom-inner{flex-direction:column}}
@media(max-width:420px){.field-row{grid-template-columns:1fr}}
@media(max-width:1100px){.main-nav{gap:.7rem}.main-nav a{font-size:.86rem}.header-inner{gap:.65rem}}
.blog-post h3{font-size:1.05rem;margin:1.35rem 0 .4rem}
.blog-post .mini-table{margin:0 0 1.1rem}
.blog-card h2{font-size:1.08rem;margin:0 0 .45rem;letter-spacing:-.015em}
.blog-card .post-date{margin:0 0 .35rem;font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;font-weight:700;color:var(--accent)}
"""

JS = """/* Fuquay Fencing Pros — nav, lead forms, analytics events */
const LEAD_WEBHOOK_URL = "%WEBHOOK%"; // Zapier Catch Hook. Blank = demo mode (logs, no send).

/* ---------- mobile nav ---------- */
(function(){
  const t=document.querySelector(".nav-toggle"), m=document.getElementById("mobile-nav");
  if(!t||!m) return;
  t.addEventListener("click",()=>{const o=m.classList.toggle("open");t.setAttribute("aria-expanded",String(o));});
  m.querySelectorAll("a").forEach(a=>a.addEventListener("click",()=>{
    m.classList.remove("open");t.setAttribute("aria-expanded","false");}));
})();

/* ---------- footer year ---------- */
(function(){const y=document.getElementById("year");if(y)y.textContent=new Date().getFullYear();})();

/* ---------- call-click tracking (calls often outnumber form fills) ---------- */
(function(){
  document.querySelectorAll("a[data-call]").forEach(function(a){
    a.addEventListener("click",function(){
      try{ if(window.gtag) gtag("event","click_to_call",{event_category:"lead",
             event_label:location.pathname}); }catch(e){}
      try{ if(window.fbq) fbq("track","Contact",{content_name:"click_to_call",
             page:location.pathname}); }catch(e){}
    });
  });
})();

/* ---------- lead forms (one per page) ---------- */
(function(){
  const LOADED_AT = Date.now();
  document.querySelectorAll("form[data-lead-form]").forEach(function(form){
    const btn = form.querySelector('button[type="submit"]');
    const okBox = form.querySelector(".form-success");
    const errBox = form.querySelector(".form-error");

    form.addEventListener("submit", async function(e){
      e.preventDefault();
      errBox.hidden = true;
      if(!form.checkValidity()){ form.reportValidity(); return; }

      /* spam gates: honeypot + minimum dwell time */
      if(form.company && form.company.value){ okBox.hidden=false; return; }   // silent drop
      if(Date.now() - LOADED_AT < 3000){ okBox.hidden=false; return; }        // too fast to be human

      if(btn.getAttribute("aria-busy")==="true") return;
      btn.setAttribute("aria-busy","true");
      const label = btn.textContent; btn.textContent = "Sending…";

      const payload = {
        fullName: form.fullName.value.trim(),
        phone:    form.phone.value.trim(),
        email:    form.email.value.trim(),
        address:  form.address.value.trim(),
        zip:      form.zip.value.trim(),
        fenceType:form.fenceType.value,
        timeline: form.timeline.value,
        source:   "Website",
        pageSource: form.dataset.pageSource || location.pathname,
        submittedAt: new Date().toISOString(),
        pageUrl:  location.href
      };

      try{
        if(LEAD_WEBHOOK_URL){
          /* Form-urlencoded is CORS-safelisted, so the browser POSTs without a
             preflight. application/json is not: Zapier's Catch Hook omits
             Access-Control-Allow-Headers on OPTIONS, and the browser blocks the
             lead ("content-type is not allowed") before the POST is sent.
             Field names are unchanged so existing Zap maps still match. */
          const r = await fetch(LEAD_WEBHOOK_URL,{method:"POST",
            body: new URLSearchParams(payload)});
          if(!r.ok) throw new Error("HTTP "+r.status);
        } else {
          console.warn("No LEAD_WEBHOOK_URL set — demo mode.", payload);
          await new Promise(r=>setTimeout(r,400));
        }

        /* conversion events */
        try{ if(window.gtag) gtag("event","generate_lead",{event_category:"lead",
               event_label: payload.pageSource, fence_type: payload.fenceType}); }catch(e){}
        try{ if(window.fbq) fbq("track","Lead",{content_name: payload.pageSource,
               content_category: payload.fenceType}); }catch(e){}

        form.querySelectorAll(".field,.field-row,button[type=submit],.consent")
            .forEach(el=>el.style.display="none");
        okBox.hidden = false;
        okBox.scrollIntoView({behavior:"smooth",block:"center"});
      }catch(err){
        console.error("Lead submit failed:",err);
        errBox.hidden = false;
        btn.removeAttribute("aria-busy"); btn.textContent = label;
      }
    });
  });
})();
""".replace("%WEBHOOK%", WEBHOOK)

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="6" '
           'fill="#2f7d54"/><g fill="#fff"><path d="M5 14l3-4 3 4v13H5z"/><path d="M13 14l3-4 3 4v13h-6z"/>'
           '<path d="M21 14l3-4 3 4v13h-6z"/><rect x="3" y="18" width="26" height="2.2"/>'
           '<rect x="3" y="23" width="26" height="2.2"/></g></svg>')

README = f"""# {BRAND} — site

Static site. No build step, no runtime. Deploys to GitHub Pages.

## ⚠️ Before this goes live — replace these

Open `build.py`, edit the CONFIG block, re-run `python3 build.py`:

| Constant | Current placeholder | Replace with |
|---|---|---|
| `PHONE_TEXT` / `PHONE_TEL` | `{PHONE_TEXT}` / `{PHONE_TEL}` | CallRail NC tracking number |
| `GA4_ID` | `{GA4_ID}` | real GA4 measurement ID |
| `PIXEL_ID` | `{PIXEL_ID}` | real Meta Pixel ID |
| `WEBHOOK` | `{WEBHOOK or "*(blank — demo mode)*"}` | Zapier Catch Hook URL |
| `DOMAIN` | `{DOMAIN}` | final domain if different |

`PHONE_TEXT` / `PHONE_TEL` are set to the CallRail tracking number `{PHONE_TEXT}` (`tel:{PHONE_TEL}`). `GA4_ID` is set (`{GA4_ID}`); every page loads gtag with that measurement ID. `WEBHOOK` is set. Lead forms POST `application/x-www-form-urlencoded` fields to that Zapier Catch Hook (same names as before: fullName, phone, email, address, zip, fenceType, timeline, source, pageSource, submittedAt, pageUrl). A JSON content type is not used: it triggers a CORS preflight the Catch Hook rejects. Turn the Zap **On** so submissions are received. If `WEBHOOK` is blank, forms run in demo mode (success state + console log, no send). `PIXEL_ID` is set (`{PIXEL_ID}`); every page loads fbq with that Pixel ID.

## What's in here

- `index.html` — home
- `services/` — 4 service pages (vinyl first: it's the validated 70/mo term)
- `areas/` — 5 city pages, each with genuinely distinct local content
- `faq.html` — 8 Q&As with FAQPage schema
- `blog/` — guides index and articles (`blog/index.html`, `blog/{{slug}}/index.html`)
- `privacy.html` — required for Meta lead forms and business verification
- `terms.html` — terms and conditions, including SMS / text messaging terms
- `styles.css`, `main.js`, `sitemap.xml`, `robots.txt`, `CNAME`, `favicon.svg`
- `images/` — add `og-image.jpg` here (1200×630); pages already reference it

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

`python3 build.py` writes `site/`, then mirrors those files onto the repo root. Pages serves the root, not `site/`.

**GitHub Pages (admin click — API cannot enable this):** Settings → Pages →
Build and deployment → Source: **Deploy from a branch** → Branch **main** / folder **/ (root)** → Save.
Custom domain: `{DOMAIN}` → Save. After DNS is green, enable **Enforce HTTPS**.

Default Pages URL after enable: `https://jsmitty37.github.io/fuquay-fencing-pros/`
Custom domain URL: `https://{DOMAIN}/`

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
"""


# =============================== BLOG =====================================
# Public article bodies only. SEO header blocks and fact-check footers from
# the drafts are not copied into the generated HTML.

_MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_MD_BOLD = re.compile(r"\*\*([^*]+)\*\*")

def _ld(obj):
    """JSON-LD script. json.dumps so '&' stays '&' (never '&amp;') inside JSON."""
    payload = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    return '<script type="application/ld+json">' + payload + "</script>"

def _rewrite_href(url, depth):
    if url.startswith(("http://", "https://", "mailto:", "tel:")):
        return url
    up = "../" * depth
    if url.startswith("/#"):
        return up + "index.html" + url[1:]
    if url.startswith("/"):
        return up + url.lstrip("/")
    return url

def _inline(text, depth):
    """Escape text, then restore markdown links and bold."""
    def link_sub(m):
        label = html.escape(m.group(1), quote=False)
        href = html.escape(_rewrite_href(m.group(2), depth), quote=True)
        return f'<a href="{href}">{label}</a>'
    def bold_sub(m):
        return "<strong>" + html.escape(m.group(1), quote=False) + "</strong>"
    # Links first so a bold marker cannot swallow a URL. Labels in these posts
    # do not themselves contain bold or nested links.
    escaped_links = []
    def hold_link(m):
        escaped_links.append(link_sub(m))
        return f"\x00LINK{len(escaped_links)-1}\x00"
    held = _MD_LINK.sub(hold_link, text)
    held = _MD_BOLD.sub(bold_sub, held)
    # Escape the remaining plain text without touching the tags we just added
    # or the link placeholders.
    parts = re.split(r"(<strong>.*?</strong>|\x00LINK\d+\x00)", held)
    out = []
    for part in parts:
        if part.startswith("<strong>") or part.startswith("\x00LINK"):
            out.append(part)
        else:
            out.append(html.escape(part, quote=False))
    joined = "".join(out)
    for i, tag in enumerate(escaped_links):
        joined = joined.replace(f"\x00LINK{i}\x00", tag)
    return joined

def _md_blocks(md):
    lines = md.strip().splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < n and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            yield ("table", rows)
            continue
        if line.startswith("- "):
            items = []
            while i < n and lines[i].startswith("- "):
                items.append(lines[i][2:])
                i += 1
            yield ("ul", items)
            continue
        if re.match(r"\d+\. ", line):
            items = []
            while i < n and re.match(r"\d+\. ", lines[i]):
                items.append(re.sub(r"^\d+\. ", "", lines[i]))
                i += 1
            yield ("ol", items)
            continue
        if line.startswith("### "):
            yield ("h3", line[4:])
            i += 1
            continue
        if line.startswith("## "):
            yield ("h2", line[3:])
            i += 1
            continue
        yield ("p", line)
        i += 1

def _cells(row):
    return [c.strip() for c in row.strip().strip("|").split("|")]

def md_to_html(md, depth):
    chunks = []
    for kind, data in _md_blocks(md):
        if kind == "h2":
            chunks.append(f"<h2>{_inline(data, depth)}</h2>")
        elif kind == "h3":
            chunks.append(f"<h3>{_inline(data, depth)}</h3>")
        elif kind == "p":
            chunks.append(f"<p>{_inline(data, depth)}</p>")
        elif kind == "ul":
            items = "".join(f"<li>{_inline(item, depth)}</li>" for item in data)
            chunks.append(f'<ul class="prose-list">{items}</ul>')
        elif kind == "ol":
            items = "".join(f"<li>{_inline(item, depth)}</li>" for item in data)
            chunks.append(f'<ol class="prose-list">{items}</ol>')
        elif kind == "table":
            header, body_rows = data[0], data[2:]
            thead = "<thead><tr>" + "".join(f"<th>{_inline(c, depth)}</th>" for c in _cells(header)) + "</tr></thead>"
            tbody = "<tbody>"
            for row in body_rows:
                tbody += "<tr>" + "".join(f"<td>{_inline(c, depth)}</td>" for c in _cells(row)) + "</tr>"
            tbody += "</tbody>"
            chunks.append(f'<table class="mini-table">{thead}{tbody}</table>')
    return "\n".join(chunks)

def extract_faqs(md):
    """Q&A pairs under the post's FAQ heading, for FAQPage JSON-LD."""
    faqs, in_faq, question, buf = [], False, None, []
    for line in md.splitlines():
        if line.startswith("## ") and "FAQ" in line:
            in_faq = True
            continue
        if not in_faq:
            continue
        if line.startswith("### "):
            if question:
                faqs.append((question, " ".join(buf).strip()))
            question, buf = line[4:].strip(), []
        elif line.strip() and question:
            buf.append(line.strip())
    if question:
        faqs.append((question, " ".join(buf).strip()))
    return faqs

POSTS = [
    {
        "slug": 'fence-permit-fuquay-varina',
        "meta_title": 'Do You Need a Fence Permit in Fuquay-Varina, NC?',
        "meta_desc": "Do you need a fence permit in Fuquay-Varina? Usually not, but height rules, your HOA, and the Harnett County side of 27526 still matter. Here's how.",
        "h1": 'Do You Need a Fence Permit in Fuquay-Varina, NC?',
        "date": "2026-09-26",
        "body": """# Do You Need a Fence Permit in Fuquay-Varina, NC?

**Quick answer:** Usually not. You don't need a fence permit in Fuquay-Varina if your home is inside town limits or the Town's ETJ, which is the area just outside town limits that still follows town zoning rules. You still have to follow the Town's height rules, and your HOA will likely need to approve your fence first. If your home is on the Harnett County side of zip code 27526, check with Harnett County instead.

This guide covers what does matter: which rules cover your lot, how tall you can build, and how HOA approval works. It's general homeowner info, not legal advice, and rules can change, so confirm the details for your own lot before you build.

## Do I need a fence permit in Fuquay-Varina?

The Town's own answer is no: a permit is not required to install a fence inside Fuquay-Varina's town limits or its ETJ. We summarize this on our [fence FAQ page](/faq.html).

Other projects are different, because pools, sheds, detached garages, and other outbuildings all need permits. If your fence goes around a pool, the pool gets the permit and the fence gets inspected as part of it.

So a normal backyard privacy fence in town usually needs no Town permit. For unusual cases, like corner lots, fences near easements, or commercial property, check with the Town's Planning Department first.

## What is the ETJ, and how do I know if I'm in it?

ETJ is short for "extraterritorial jurisdiction." In plain terms, it's the ring of land just outside town limits that still follows the Town's zoning rules, so the Town's fence rules can apply there even though you're not technically in town.

Here's the catch: your mailing address won't tell you if you're in town, in the ETJ, or neither. Fuquay-Varina has one zip code, 27526, and it covers about 98 square miles.

The Town itself is only about 17.6 square miles, and it sits entirely in Wake County. The southern part of the zip reaches into Harnett County.

That means two neighbors with the same "Fuquay-Varina, NC 27526" address can fall under different rules. To find out where you stand:

- Look up your lot on your county's online GIS map, which shows property lines and tax records. Use the Wake County or Harnett County map, depending on where you live.
- Check your property tax bill.
- Call the Town of Fuquay-Varina Planning Department to confirm, or let us check it for you before we quote.

## How tall can a fence be in Fuquay-Varina?

It depends on whether you're inside town limits or in the ETJ, as summarized on our [Fuquay-Varina area page](/areas/fuquay-varina.html):

| Yard | Inside town limits | In the ETJ |
| --- | --- | --- |
| Front yard | 4 ft max; no solid fences | 4 ft |
| Side and back yard | 6 ft max | No Town maximum |

You may see other websites say 8 feet is allowed. The Town's ordinance says 6 feet inside town limits, and that's what we build to.

"No Town maximum" in the ETJ does not mean "no rules." Your HOA rules, easements, and setbacks still apply. A setback is the distance a structure has to stay back from a property line or buffer.

## What if I'm on the Harnett County side of 27526?

If your home is in the southern part of 27526, you may be outside both the town limits and the ETJ. In that case, the Town of Fuquay-Varina's "no permit" answer may not apply to you, and Harnett County (plus your HOA, if you have one) sets the rules.

We won't guess at Harnett County permit rules, fees, or height limits, so please confirm directly with Harnett County before you build. Give us your street address and we'll check which rules apply before we quote.

## Does my HOA have to approve my fence?

If you live in an HOA, almost certainly. In Fuquay-Varina, the HOA is often the real gatekeeper, even though the Town doesn't require a fence permit. That's especially true in newer neighborhoods such as South Lakes, North Lakes, Serenity, Sunset Bluffs, and Brighton Ridge.

HOA rules can be stricter than the Town's, and Town rules still apply on top of them. We are not your HOA, so we can't approve your fence or promise that your HOA will.

Here's how the approval process usually works:

1. Ask your HOA or its architectural review committee (the group that approves outside changes to homes) for its current fence rules and application.
2. Gather what they ask for. That often includes a plat or survey, plus the fence height, material, color, gate locations, and which side faces out. A plat is a map of your lot that shows property lines and easements.
3. Submit it before any work starts. Approval runs on the HOA's schedule, not yours.
4. Wait for written approval before you buy materials.

We can help you understand what details usually go into an application. Some older areas, like parts of the Village of Sippihaw, may have no HOA at all, but Town rules still apply there.

## What should I check before anyone starts digging?

A few details cause most of the costly mistakes:

- **Property lines.** Find your survey pins, the metal markers buried at the corners of your lot. Fences are usually set a few inches inside the line to avoid disputes with neighbors.
- **Easements.** An easement is a strip of your land that others, like utility companies, have the right to use. Fences often can't go in utility, drainage, or stormwater easements, or in the public right-of-way along the street.
- **Finished side.** The nicer side of the fence usually faces out, toward the street or your neighbor.
- **Ground gap.** Leave about 2 inches between the bottom of the fence and the ground so rainwater can drain.
- **Chain link color.** Inside town limits, chain link should be black or green coated.

## Do pool fences follow different rules?

Yes. A pool fence is a safety barrier, not just a privacy fence. Under the 2024 NC Residential Code (Appendix NC-A), a pool barrier must be at least 48 inches tall, with self-closing, self-latching gates and limits on gaps and openings.

The pool gets the permit, and the barrier is inspected as part of it. Our [aluminum and pool-code fence page](/services/aluminum-pool-fences.html) has more detail. The inspector and the code book have the final word.

## What should I do next?

First, confirm whether you're in town limits, the ETJ, or somewhere else, and then pull your HOA guidelines. Picking a material comes next, and our [vinyl vs wood privacy fence guide](/blog/vinyl-vs-wood-privacy-fuquay-varina/) can help. If you live in Holly Springs, the Town rules are different, so see our [Holly Springs new construction fence guide](/blog/holly-springs-new-build-fence/).

When you're ready, [request a free estimate](/#quote) or call or text **(919) 276-8406**. We'll check your address, look at your yard, and talk through your options with no pressure.

## Fence Permit FAQ

### Do I need a permit to build a fence in Fuquay-Varina?

Not inside town limits or the ETJ, where the Town of Fuquay-Varina doesn't require a fence permit. Pools, sheds, and detached garages do need permits.

### Does the "no permit" answer cover all of zip code 27526?

No. The zip covers parts of both Wake and Harnett counties, and much of it is outside town limits and the ETJ, so if you're outside both, check with your county.

### How tall can my backyard fence be in Fuquay-Varina?

Inside town limits, side and back yard fences can be up to 6 feet. In the ETJ, the Town has no maximum for side and back yards. Your HOA may still set its own limit.

### Do I still need HOA approval if the Town doesn't require a permit?

Usually, yes. HOA rules are separate from Town rules, so get written approval from your HOA before any work begins.""",
    },
    {
        "slug": 'vinyl-vs-wood-privacy-fuquay-varina',
        "meta_title": 'Vinyl vs Wood Privacy Fence in Fuquay-Varina, NC',
        "meta_desc": 'Vinyl vs wood privacy fence for a Fuquay-Varina yard: compare upkeep, looks, red clay stains, and HOA rules so you can choose with confidence.',
        "h1": 'Vinyl vs Wood Privacy Fence: Which Is Right for Your Fuquay-Varina Yard?',
        "date": "2026-09-26",
        "body": """# Vinyl vs Wood Privacy Fence: Which Is Right for Your Fuquay-Varina Yard?

**Quick answer:** Both vinyl and wood make a good privacy fence in Fuquay-Varina. Choose vinyl if you want less upkeep and a clean, uniform look. Choose wood if you like a classic look and don't mind staining and sealing it on a regular schedule. Either way, our red clay, humid summers, and your HOA rules should shape the choice as much as the material itself.

Below, we compare the two in plain terms, based on what we see on local lots in southern Wake County. You won't find made-up popularity stats or warranty promises here, just the real tradeoffs.

## Vinyl vs wood privacy fence: how do they compare?

Here's the short version:

| | Vinyl privacy fence | Wood privacy fence |
| --- | --- | --- |
| Routine upkeep | No staining or painting; occasional washing | Stain and seal on a regular schedule |
| Look | Clean, uniform color and panels | Classic wood grain; board-on-board or shadowbox styles |
| Local weak spots | Red clay splash stains on white vinyl; pollen; UV on sunny runs | Moisture, mildew, ground contact, termites |
| Repairs | Panel-based | Single boards can often be swapped |
| HOA fit | Works where the HOA wants a clean, consistent look | Many HOAs already have rules written for it |

Neither one is the "winner." The right pick depends on your yard, your HOA, and how much upkeep you want to take on.

## Is a vinyl privacy fence worth it in Fuquay-Varina?

For many homeowners, yes, mainly because it skips the stain-and-seal routine. Central North Carolina gets about 47 inches of rain a year and stays sticky and humid from June into September, which is hard on wood, while vinyl doesn't need painting or staining.

Vinyl also gives you a clean, even look that many HOAs like. If solid privacy isn't wanted or allowed in part of your yard, it also comes in picket, semi-privacy, and lattice-top styles.

Vinyl does have a few local downsides to plan for:

- **Red clay stains.** Our soil is iron-rich red clay, and when rain splashes it onto white vinyl, it leaves an orange stain on the bottom 12 to 18 inches of the fence.
- **Sun exposure.** Fence runs that face south or west get more sun, so ask about UV-resistant vinyl for those sides.
- **Pine pollen.** From late March into early April, pollen makes every white fence look dirty, so wash it after the pollen drops, not during.
- **Pressure washing.** Don't blast clay stains with a high-pressure washer, because that can scar the panels. Use a cleaner made for the job instead.

The best fix for clay stains is prevention: get grass or mulch growing along the fence line so rain can't splash bare dirt onto it. Our [vinyl fence page](/services/vinyl-fences.html) has more tips.

## Is a wood privacy fence a good choice here?

Yes, if it's built for our conditions and you keep up with it. Wood privacy fences are still a common backyard request around Fuquay-Varina, and popular styles include board-on-board and shadowbox. Board-on-board overlaps the boards so you can't see through, while shadowbox staggers them on both sides of the rails.

Wood has real strengths. It has a warm, familiar look, blends in well with trees and older streets, and can be dressed up with decorative caps and trim. If one board gets damaged, it can often be replaced on its own.

Here's what shortens a wood fence's life in our area:

- **Moisture.** Boards on the north side stay damp longer and tend to mildew first.
- **Ground contact.** Wood that touches the dirt breaks down faster, so the fence should sit about 2 inches above the ground, which helps both drainage and the bottom board.
- **Termites.** Termites are a year-round concern in North Carolina, so wood in the ground should be treated.
- **Upkeep.** Staining and sealing are part of owning a wood fence, not an optional extra.

See our [wood privacy fence page](/services/wood-privacy-fences.html) for style options.

## How does our red clay affect fence posts?

This matters for both materials, because under about eight inches of topsoil, Fuquay-Varina sits on dense red clay. As a common industry practice, about one-third of each post goes below ground, which is roughly 24 to 36 inches deep for a 6-foot fence.

Depth isn't the whole story. Gravel at the bottom of the hole and a sloped collar at the top that sheds water help keep posts from working loose as the ground freezes and thaws. New-build lots are often packed with dense, uneven fill dirt, which makes good post work even more important.

## Do height limits or HOA rules affect which material I can use?

They can. Inside Fuquay-Varina town limits, back and side yard fences generally max out at 6 feet, and front yard fences at 4 feet with no solid fences. In the ETJ, which is the area just outside town limits that still follows town zoning rules, the Town sets no maximum for side and back yards. Our [fence FAQ](/faq.html) and our [Fuquay-Varina fence permit guide](/blog/fence-permit-fuquay-varina/) explain these rules.

Many newer neighborhoods also need written HOA approval before any fence goes in. HOAs often care about color, height, how see-through the fence is, gate placement, and which side faces out, not just vinyl versus wood. We don't claim most HOAs require vinyl or ban wood, so check your own guidelines.

We are not your HOA, and we can't approve a fence or promise your HOA will, but we can help you understand the details that usually go into an application.

## How do I decide?

Vinyl is often the better fit if you:

- Want as little upkeep as possible
- Like a clean, uniform look
- Are willing to keep grass or mulch along the fence line to stop clay stains

Wood is often the better fit if you:

- Love the look of real wood, and your HOA allows it
- Will stain and seal it on a regular schedule
- Want to be able to replace single boards later

If several neighbors are fencing at the same time, matching height and finished side can prevent disputes down the road. The only wrong choice is picking a material from a brochure and finding out about clay, pollen, or HOA rules after the posts are set.

Just bought a new home in Holly Springs? Our [Holly Springs new construction fence guide](/blog/holly-springs-new-build-fence/) covers what's different there.

## Get a free estimate

Want a second opinion on your yard? [Request a free estimate](/#quote) or call or text **(919) 276-8406**. We'll measure, check your sun and soil, and talk through vinyl and wood honestly, with no pressure.

## Vinyl vs Wood FAQ

### Which lasts longer in North Carolina, vinyl or wood?

It depends on the product, how it's installed, and how well it's cared for. Vinyl avoids the stain-and-seal routine, while wood can hold up well if it's treated, kept off the ground, and sealed on schedule.

### Why is the bottom of my white vinyl fence turning orange?

It's red clay: rain splashes iron-rich soil onto the fence, leaving stains on the bottom 12 to 18 inches. Grass or mulch along the fence line helps prevent it, and a proper cleaner works better than a pressure washer.

### Does my HOA have to approve a vinyl or wood fence?

In many Fuquay-Varina neighborhoods, yes, so check your HOA's guidelines and get written approval before work begins.

### How tall can a privacy fence be in Fuquay-Varina?

Inside town limits, side and back yard fences can generally be up to 6 feet. In the ETJ, the Town has no maximum for side and back yards, but your HOA may set its own limit.""",
    },
    {
        "slug": 'holly-springs-new-build-fence',
        "meta_title": 'Holly Springs New Construction Fence: What to Know First',
        "meta_desc": 'Just closed on a new build? Our Holly Springs new construction fence guide covers Town rules, HOA approval, builder fill dirt, and choosing a material.',
        "h1": 'Holly Springs New Construction Fence Guide: What to Do After You Close',
        "date": "2026-09-26",
        "body": """# Holly Springs New Construction Fence Guide: What to Do After You Close

**Quick answer:** Planning a Holly Springs new construction fence for a bare backyard? Don't start with the fence material. Start by checking the Town of Holly Springs fence rules and getting your HOA's approval process going, since that step often takes the longest. Then pick a material that suits our red clay and humid weather, and make sure the posts are set for packed builder fill dirt.

Holly Springs is about five miles northwest of Fuquay-Varina and has its own zip code, 27540. It's close enough that we work there often, but it's a separate town with its own rules. This guide walks you through the steps in order.

## Why do so many new homes in Holly Springs come without a fence?

Holly Springs has been one of the faster-growing towns in Wake County, and that means lots of new homes. Builders here, like in much of southern Wake, often don't include a fence with the house. The most common call we get from Holly Springs is from someone who just closed and has a bare backyard.

A new-build yard usually has a few things in common. The back and sides are wide open to the neighbors, and the sod is fresh or the dirt is still settling. The HOA's review process may still be active while you're unpacking boxes.

## Do Fuquay-Varina fence rules apply in Holly Springs?

No. Holly Springs is its own town, so the Town of Holly Springs sets its own fence standards, height limits, and any permit requirements. Fuquay-Varina's "no Town fence permit" answer is a Fuquay-Varina rule only. Our [Fuquay-Varina fence permit guide](/blog/fence-permit-fuquay-varina/) explains that rule, but don't assume it carries over.

We aren't going to list Holly Springs height limits, permit fees, or a "no permit needed" claim here. Please confirm the current rules with the Town of Holly Springs before you settle on height, style, or timing. We also confirm local requirements before we quote, not after, as noted on our [Holly Springs area page](/areas/holly-springs.html).

A simple way to start is to check the Town of Holly Springs planning or development resources for fence standards. At the same time, pull your HOA guidelines, and bring both to your estimate.

## How long does HOA fence approval take on a new street?

It varies, and it runs on the HOA's schedule, not yours. On a new street, HOA review is often the slowest part of the whole project, so it pays to apply early. HOA rules can be stricter than the Town's, and both apply.

We are not your HOA, and we can't approve your fence or promise that your HOA will. Here's how the process usually works:

1. Ask the HOA's architectural review committee (the group that approves outside changes to homes) what its fence application needs.
2. Gather the details, which often include a plat or survey, the fence height, material, color, gate locations, and which side faces out. A plat is a map of your lot showing property lines and easements.
3. Submit before any digging. Digging first and asking forgiveness later rarely goes well in a new neighborhood.
4. Wait for written approval before buying materials.

If the lots next to you are still open, talk with your neighbors about height and timing. Matching fence lines now can prevent awkward mismatches later. We can help you understand what questions to ask and what details usually go into an application.

## Why does builder fill dirt matter for fence posts?

Holly Springs sits on the same ground as Fuquay-Varina: red clay starting about eight inches down, plus heavy yearly rain. On a new-build lot, the builder often stripped, graded, and packed down the soil. That packed fill is denser and less predictable than the soil in an older yard that has had years to settle.

Here's what that means for your fence:

- **Harder digging.** Hitting dense material is common on new lots. It's not a sign of a "bad" lot.
- **Drainage.** Gravel at the bottom of each post hole and a sloped collar at the top that sheds water matter as much as depth. Water sitting around a post can loosen it as the ground freezes and thaws.
- **Post depth.** A common industry practice is to set about one-third of the post below ground, which is roughly 24 to 36 inches for a 6-foot fence.
- **Groundcover.** Get grass or mulch established along the fence line early, especially with white vinyl, since rain splashing bare clay leaves orange stains.

## What fence material works best for a new-build backyard?

It depends on your goals and your HOA's rules. Here are the common choices:

- **Vinyl privacy.** This is a popular new-build choice for a finished look without staining. Protect it from clay splash, and don't pressure-wash stains, since high pressure can scar the panels.
- **Wood privacy.** Board-on-board or shadowbox wood is a strong look if your HOA allows it. Plan for a gap above the ground, solid post work in clay and fill, and regular sealing.
- **Aluminum (if a pool is coming).** If you plan to add a pool, don't build a privacy fence that fights pool barrier rules later. Our [aluminum and pool-code fence page](/services/aluminum-pool-fences.html) covers pool-code fencing. Confirm Holly Springs and inspector requirements separately, and keep in mind this isn't legal advice.
- **Chain link.** On larger lots, coated chain link can be a practical first fence for pets while your landscaping fills in. Your HOA rules decide whether it can stay long term.

For a side-by-side look at the two most common choices, see our [vinyl vs wood privacy fence guide](/blog/vinyl-vs-wood-privacy-fuquay-varina/).

## When is the best time to install a fence in Holly Springs?

The weather here is the same as in Fuquay-Varina. Spring and fall are usually the easiest times to dig. Clay turns sticky when it's soaked and gets hard as a brick in midsummer, though fences can go in year-round.

Pine pollen also coats white fences from late March into early April. If you want your new fence looking its best for photos, plan around that.

## What's the best order of steps after closing?

1. Confirm the Town of Holly Springs fence rules for your lot.
2. Get your HOA guidelines and start the application early.
3. Find your survey pins, the metal markers buried at your lot corners, and note any easements. An easement is a strip of your land that others, like utility companies, have the right to use, and fences often can't go there.
4. Decide what you need, such as full backyard privacy, a pet area, or room for a future pool.
5. Book an on-site estimate so the material and post plan match your actual soil and slope.

When you're ready, [request a free estimate](/#quote) or call or text **(919) 276-8406**. We serve Holly Springs from nearby Fuquay-Varina, and there's no obligation.

## Holly Springs New Construction Fence FAQ

### Do I need a fence permit in Holly Springs?

Check with the Town of Holly Springs. It's a separate town from Fuquay-Varina with its own rules, so Fuquay-Varina's answer doesn't apply.

### Do I need HOA approval for a fence on my new build?

In many Holly Springs neighborhoods, yes. Get your HOA's written approval before any digging starts.

### Why is digging harder on a new-build lot?

Builders often strip, grade, and pack down the soil. That fill is denser and less predictable than soil in an older yard, so post setting and drainage need extra care.

### Should I plan my fence around a future pool?

Yes. Pool barriers have their own North Carolina code requirements, so plan ahead to avoid replacing part of your fence later.""",
    },
]

def blog_index():
    title = f"Fence Guides for {CITY} &amp; Southern Wake | {BRAND}"
    desc = ("Fence guides for Fuquay-Varina, Holly Springs, and nearby: town fence permits, "
            "vinyl vs wood privacy fences, and new-construction backyards.")
    canon = f"{BASE}/blog/"
    posts_ld = []
    cards = []
    for p in POSTS:
        url = f"{BASE}/blog/{p['slug']}/"
        posts_ld.append({
            "@type": "BlogPosting",
            "headline": p["h1"],
            "url": url,
            "datePublished": p["date"],
            "image": f"{BASE}/images/og-image.jpg",
        })
        cards.append(
            '<article class="service-card blog-card"><div class="service-body">'
            f'<p class="post-date">September 26, 2026</p>'
            f'<h2>{html.escape(p["h1"], quote=False)}</h2>'
            f'<p>{html.escape(p["meta_desc"], quote=False)}</p>'
            f'<p class="card-link"><a href="{html.escape(p["slug"])}/">Read the guide &rarr;</a></p>'
            "</div></article>"
        )
    blog_ld = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "Fence Guides for Fuquay-Varina & Southern Wake",
        "url": canon,
        "publisher": {"@id": BIZ_ID},
        "blogPost": posts_ld,
    }
    nav, bc_ld = crumbs(1, [("Blog", None)])
    return (head(title, desc, canon, 1, ref_ld() + _ld(blog_ld) + bc_ld) + header(1) + nav +
            f'<main><section class="hero hero-inner"><div class="container hero-content">'
            f'<p class="hero-eyebrow">Fence guides</p>'
            f'<h1>Fence Guides for {CITY} &amp; Southern Wake</h1>'
            f'<p class="hero-sub">Permits, materials, and new-construction yards &mdash; written for homeowners around {CITY}.</p>'
            f'<div class="hero-cta"><a class="btn btn-primary btn-lg" href="#quote">Get My Free Estimate</a>'
            f'<a class="btn btn-ghost btn-lg" data-call href="tel:{PHONE_TEL}">Call {PHONE_TEXT}</a></div>'
            f'</div></section><section class="section"><div class="container">'
            f'<div class="card-grid">{"".join(cards)}</div>'
            f'</div></section>' + form("blog", depth=1) + "</main>" + footer(1))

def blog_post(post):
    slug, depth = post["slug"], 2
    canon = f"{BASE}/blog/{slug}/"
    h1, desc = post["h1"], post["meta_desc"]
    faqs = extract_faqs(post["body"])
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": h1,
        "description": desc,
        "datePublished": post["date"],
        "dateModified": post["date"],
        "image": f"{BASE}/images/og-image.jpg",
        "mainEntityOfPage": {"@type": "WebPage", "@id": canon},
        "author": {"@id": BIZ_ID},
        "publisher": {"@id": BIZ_ID},
    }
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }
    extra_meta = (
        f'<meta property="article:published_time" content="{post["date"]}" />\n'
        f'<meta property="article:modified_time" content="{post["date"]}" />\n'
    )
    nav, bc_ld = crumbs(depth, [("Blog", "blog/"), (h1, None)])
    body = md_to_html(post["body"], depth)
    return (head(post["meta_title"], desc, canon, depth, ref_ld() + _ld(article) + _ld(faq_ld) + bc_ld,
                 og_type="article", extra_meta=extra_meta) + header(depth) + nav +
            f'<main><section class="hero hero-inner"><div class="container hero-content">'
            f'<p class="hero-eyebrow">Fence guide</p><h1>{html.escape(h1, quote=False)}</h1>'
            f'<div class="hero-cta"><a class="btn btn-primary btn-lg" href="#quote">Get My Free Estimate</a>'
            f'<a class="btn btn-ghost btn-lg" data-call href="tel:{PHONE_TEL}">Call {PHONE_TEXT}</a></div>'
            f'</div></section><section class="section"><div class="container prose blog-post">{body}'
            f'</div></section>' + form(f"blog/{slug}", depth=depth) + "</main>" + footer(depth))

# ================================== BUILD ==================================
if os.path.isdir(OUT): shutil.rmtree(OUT)
os.makedirs(OUT, exist_ok=True)

write("index.html", home())
for s, n, h in SERVICES: write(f"services/{s}.html", service_page(s, n, h))
for s, n, z in AREAS:    write(f"areas/{s}.html", area_page(s, n, z))
write("faq.html", faq_page())
write("privacy.html", privacy_page())
write("terms.html", terms_page())
write("blog/index.html", blog_index())
for _post in POSTS:
    write(f"blog/{_post['slug']}/index.html", blog_post(_post))
write("styles.css", CSS)
write("main.js", JS)
write("favicon.svg", FAVICON)
write("CNAME", DOMAIN + "\n")
write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
write("README.md", README)
os.makedirs(os.path.join(OUT, "images"), exist_ok=True)
write("images/README.md", """# Open Graph image

Place `og-image.jpg` here (recommended 1200×630). Every page already references
`/images/og-image.jpg` via `og:image`. This note is a placeholder until the
branded image is added — no binary is committed yet.
""")

urls = [("", "1.0"), ("faq.html", "0.6"), ("privacy.html", "0.3"), ("terms.html", "0.3")]
urls += [(f"services/{s}.html", "0.9") for s, _, _ in SERVICES]
urls += [(f"areas/{s}.html", "0.9" if s == "fuquay-varina" else "0.7") for s, _, _ in AREAS]
urls += [("blog/", "0.7")]
urls += [(f"blog/{p['slug']}/", "0.6") for p in POSTS]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u, p in urls:
    # 2026-09-26: blog launch, Blog nav on every page, and the previous
    # 2026-09-14 sitemap dates were already behind the 2026-09-24 terms update.
    sm += f'  <url><loc>{BASE}/{u}</loc><lastmod>2026-09-26</lastmod><priority>{p}</priority></url>\n'
write("sitemap.xml", sm + "</urlset>\n")

# GitHub Pages serves the repo root. OUT stays site/ so a build can never rmtree
# the repo (and .git). Mirror the generated files up, without deleting files the
# generator does not own — images/og-image.jpg in particular.
_root = os.path.dirname(os.path.abspath(__file__))
if os.path.abspath(OUT) != os.path.abspath(_root):
    for dirpath, _, files in os.walk(OUT):
        rel = os.path.relpath(dirpath, OUT)
        dest_dir = _root if rel == "." else os.path.join(_root, rel)
        os.makedirs(dest_dir, exist_ok=True)
        for fn in files:
            shutil.copy2(os.path.join(dirpath, fn), os.path.join(dest_dir, fn))

print("built", len([f for _, _, fs in os.walk(OUT) for f in fs]), "files ->", OUT)
