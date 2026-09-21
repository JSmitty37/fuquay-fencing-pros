#!/usr/bin/env python3
"""
Fuquay Fencing Pros — static site generator.
Every page gets: its own lead form, analytics hooks, honeypot, schema, breadcrumbs.
Swap the CONFIG block and re-run to retarget the whole site.
"""
import os, shutil, html

# ============================== CONFIG — SWAP THESE ==============================
BRAND        = "Fuquay Fencing Pros"
BRAND_L1     = "Fuquay"
BRAND_L2     = "Fencing Pros"
DOMAIN       = "fuquayfencingpros.com"
BASE         = f"https://{DOMAIN}"
PHONE_TEXT   = "(919) 276-8406"          # CallRail tracking number
PHONE_TEL    = "+19192768406"
GA4_ID       = "G-D8RTHW2GYN"
PIXEL_ID     = "000000000000000"         # ← REPLACE with real Meta Pixel ID
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
def head(title, desc, canon, depth, extra_ld=""):
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
<meta property="og:type" content="website" />
<meta property="og:site_name" content="{BRAND}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="{canon}" />
<meta property="og:image" content="{BASE}/images/og-image.jpg" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{desc}" />
<link rel="icon" href="{up}favicon.svg" type="image/svg+xml" />
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

def form(page_source, heading="Get Your Free Fence Estimate", depth=0):
    up = "../" * depth
    return f"""<section class="section quote" id="quote" aria-labelledby="q-{abs(hash(page_source))%9999}">
<div class="container quote-inner">
  <div class="quote-intro">
    <p class="eyebrow eyebrow-light">Free Estimate</p>
    <h2 id="q-{abs(hash(page_source))%9999}">{heading}</h2>
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
      <p class="consent">By submitting, you agree to be contacted about your estimate.
         See our <a href="{up}privacy.html">Privacy Policy</a>.</p>
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
    <p><a href="{up}faq.html">Fence FAQ</a></p></div>
  <div class="footer-col"><h2 class="footer-h">Service Area</h2><p>{ar}</p>
    <p class="footer-zip">27526 &middot; 27540 &middot; 27501 &middot; 27592 &middot; 27529</p></div>
</div>
<div class="footer-bottom"><div class="container footer-bottom-inner">
  <p>&copy; <span id="year">2026</span> {BRAND}. All rights reserved.</p>
  <p><a href="{up}privacy.html">Privacy Policy</a></p>
</div></div>
</footer>
<a class="mobile-call-bar" data-call href="tel:{PHONE_TEL}" aria-label="Call {BRAND}">{PHONE_SVG} Call {PHONE_TEXT}</a>
<script src="{up}main.js" defer></script>
</body></html>
"""

def biz_ld():
    areas = ",".join(f'{{"@type":"City","name":"{n}, NC"}}' for _, n, _ in AREAS)
    offers = ",".join(f'{{"@type":"Offer","itemOffered":{{"@type":"Service","name":"{h}"}}}}'
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
    title = f"{head_name.replace('&amp;','&')} in {CITY}, {STATE} | {BRAND}"
    canon = f"{BASE}/services/{slug}.html"
    svc_ld = (f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Service",'
              f'"name":"{head_name}","serviceType":"{head_name}",'
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
<h2>Contact</h2>
<p>Questions about this policy? Call {PHONE_TEXT}.</p>
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
          const r = await fetch(LEAD_WEBHOOK_URL,{method:"POST",
            headers:{"Content-Type":"application/json","Accept":"application/json"},
            body: JSON.stringify(payload)});
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
| `PIXEL_ID` | `000000000000000` | real Meta Pixel ID |
| `WEBHOOK` | `{WEBHOOK or "*(blank — demo mode)*"}` | Zapier Catch Hook URL |
| `DOMAIN` | `{DOMAIN}` | final domain if different |

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

Then: repo **Settings → Pages → Source: main / root**. Add `{DOMAIN}` as the custom domain and enable
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
"""

# ================================== BUILD ==================================
if os.path.isdir(OUT): shutil.rmtree(OUT)
os.makedirs(OUT, exist_ok=True)

write("index.html", home())
for s, n, h in SERVICES: write(f"services/{s}.html", service_page(s, n, h))
for s, n, z in AREAS:    write(f"areas/{s}.html", area_page(s, n, z))
write("faq.html", faq_page())
write("privacy.html", privacy_page())
write("styles.css", CSS)
write("main.js", JS)
write("favicon.svg", FAVICON)
write("CNAME", DOMAIN + "\n")
write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
write("README.md", README)

urls = [("", "1.0"), ("faq.html", "0.6"), ("privacy.html", "0.3")]
urls += [(f"services/{s}.html", "0.9") for s, _, _ in SERVICES]
urls += [(f"areas/{s}.html", "0.9" if s == "fuquay-varina" else "0.7") for s, _, _ in AREAS]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u, p in urls:
    sm += f'  <url><loc>{BASE}/{u}</loc><lastmod>2026-09-14</lastmod><priority>{p}</priority></url>\n'
write("sitemap.xml", sm + "</urlset>\n")

print("built", len([f for _, _, fs in os.walk(OUT) for f in fs]), "files ->", OUT)
