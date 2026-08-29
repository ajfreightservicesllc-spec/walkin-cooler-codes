#!/usr/bin/env python3
"""
Equipment Fault-Code Directory — Static Site Generator (shared engine)
======================================================================
One rich page per documented fault code / error signal for commercial
equipment. SEO play: capture "brand + code" searches — informational queries
with NO Google map pack — and funnel them to city money pages.

Shared engine: only the CONFIG block below differs between site folders.

Inputs (all relative to this file):
  data/codes-*.json     verified fault codes (one file per brand)
  data/cities.json      city pages: intro copy + REAL local companies only
  content/articles.json long-form guides (HTML bodies)

Run (Windows or Linux, Python 3 stdlib only):
    python generate_site.py
Output -> ./site/
"""

import json
import re
import shutil
from collections import defaultdict
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------- CONFIG ---
BASE_URL = "https://walkincoolercodes.com"
SITE_NAME = "Walk-In Cooler Code Lookup"
EQUIPMENT = "walk-in cooler"        # noun used in copy
EQUIPMENT_SHORT = "walk-in cooler"
HOME_H1 = "Walk-in cooler showing an alarm code?"
HOME_SUB = ("{n} documented fault codes across {brands}, verified against "
            "service manuals — what each one means, what to check yourself, "
            "and when it's a tech call.")
# Homepage title and description are FIXED constants, never built from the
# brand list — adding a brand must never be able to blow the title past ~60.
HOME_TITLE = "Walk-In Cooler Fault Codes — Free Lookup by Brand & Code"
HOME_DESC = ("Look up any walk-in cooler or freezer alarm code. Verified against "
             "service manuals: what it means, what to check, when to call a tech.")
CITY_HERO_SUB = ("Who actually fixes commercial walk-in coolers and freezers in "
                 "the {city} area — plus what to check before you pay for a "
                 "service call.")
CTA_REGION_LINE = "If you're in Middle Tennessee or Central Alabama"
DISCLAIMER_BRANDS = "Not affiliated with any equipment manufacturer."
CTA_PHONE = ""        # e.g. "615-555-0100" (CallRail) — blank = hidden
CTA_PHONE_LABEL = "Talk to a technician now"
PARTS_LINK = ""       # parts affiliate URL — blank = hidden
CONTACT_EMAIL = "ajfreightservicesllc@gmail.com"
# ------------------------------------------------------------ END CONFIG ---

ROOT = Path(__file__).parent
OUT = ROOT / "site"

CSS = """
:root{--bg:#f6f9fc;--card:#fff;--ink:#16232e;--sub:#5b6b78;--brand:#0a6ebd;
--accent:#e8f3fb;--warn:#b34700;--line:#dde6ee}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;
background:var(--bg);color:var(--ink);line-height:1.65}
a{color:var(--brand)}
.wrap{max-width:880px;margin:0 auto;padding:0 18px}
header{background:#0d3c61;color:#fff;padding:14px 0}
header .wrap{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
header a{color:#fff;text-decoration:none;font-weight:700;font-size:1.05rem}
header nav a{font-weight:400;font-size:.92rem;margin-left:13px;opacity:.9}
.hero{background:linear-gradient(180deg,#0d3c61,#0a6ebd);color:#fff;padding:44px 0 50px;text-align:center}
.hero h1{font-size:1.9rem;margin-bottom:10px}
.hero p{opacity:.92;max-width:600px;margin:0 auto}
main{padding:30px 0 50px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:24px;margin:16px 0}
.crumbs{font-size:.85rem;color:var(--sub);margin:14px 0 4px}
.crumbs a{color:var(--sub)}
h1.page-h1{font-size:1.55rem;margin:8px 0 2px}
.family-tag{display:inline-block;background:var(--accent);color:var(--brand);
border-radius:20px;padding:2px 12px;font-size:.8rem;font-weight:600;margin-bottom:10px}
.meaning{font-size:1.05rem}
h2{font-size:1.18rem;margin:22px 0 8px}
h3{font-size:1.02rem;margin:16px 0 6px}
article p{margin:10px 0}
article ul,article ol{padding-left:24px;margin:10px 0}
article li{margin:6px 0}
ol.steps{padding-left:22px}
ol.steps li{margin:8px 0}
.callout{border-left:4px solid var(--warn);background:#fdf3ec;padding:12px 16px;border-radius:0 8px 8px 0;margin:18px 0}
.tipbox{border-left:4px solid var(--brand);background:var(--accent);padding:12px 16px;border-radius:0 8px 8px 0;margin:18px 0}
.cta{background:#0d3c61;color:#fff;border-radius:10px;padding:22px;text-align:center;margin:22px 0}
.cta a{color:#cfe6f7}
.cta a.phone{display:inline-block;background:#ffb32c;color:#16232e;font-weight:800;
font-size:1.25rem;text-decoration:none;padding:12px 26px;border-radius:8px;margin-top:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px}
.grid a{display:block;background:var(--card);border:1px solid var(--line);border-radius:8px;
padding:14px;text-decoration:none;color:var(--ink)}
.grid a:hover{border-color:var(--brand)}
.grid .c{font-weight:800;color:var(--brand)}
.grid .t{font-size:.9rem;color:var(--sub)}
.brand-row{display:flex;gap:14px;flex-wrap:wrap;justify-content:center;margin-top:-26px}
.brand-row a{flex:1;min-width:230px;max-width:340px;background:var(--card);border:1px solid var(--line);
border-radius:12px;padding:22px;text-align:center;text-decoration:none;color:var(--ink);
box-shadow:0 4px 14px rgba(13,60,97,.08)}
.brand-row a b{display:block;font-size:1.15rem;color:var(--brand)}
.brand-row.sub{margin-top:0}
.biz{border-top:1px solid var(--line);padding:16px 0}
.biz:first-of-type{border-top:none}
.biz b{font-size:1.05rem}
.biz .svc{font-size:.85rem;color:var(--sub)}
.biz a.tel{font-weight:700;text-decoration:none}
.src{font-size:.78rem;color:var(--sub);margin-top:18px;word-break:break-all}
footer{border-top:1px solid var(--line);padding:26px 0;font-size:.85rem;color:var(--sub)}
footer .wrap{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
.disclaimer{font-size:.78rem;color:var(--sub);margin-top:8px}
"""

# Populated in main() before any page renders.
NAV_HTML = ""
FOOTER_LINKS_HTML = ""
CITY_LINKS = []   # [(name, state, slug)]
FAMILIES = {}     # model_family -> intro html (data/families.json)
SUPPLEMENTS = {}  # "family||code" -> {causes, fixable, why_tech} (data/supplements.json)


def esc(s):
    return (str(s or "").replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def slugify(text):
    s = re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")
    return s or "x"


def page(title, desc, body, canonical, schema=None):
    schema_tag = "".join(
        f'<script type="application/ld+json">{json.dumps(s)}</script>'
        for s in (schema or []))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
{schema_tag}
<style>{CSS}</style>
</head>
<body>
<header><div class="wrap">
<a href="/">&#10052; {esc(SITE_NAME)}</a>
<nav>{NAV_HTML}</nav>
</div></header>
{body}
<footer><div class="wrap">
<div>&copy; {date.today().year} {esc(SITE_NAME)}{FOOTER_LINKS_HTML}</div>
<div><a href="mailto:{CONTACT_EMAIL}">Contact</a></div>
</div>
<div class="wrap disclaimer">Reference information compiled from manufacturer service
documentation. {esc(DISCLAIMER_BRANDS)} Repairs involving refrigerant, pressurized
systems, electrical components, or disassembly should be performed by a qualified,
certified technician. Company listings are provided for reference; verify details
before hiring.</div>
</footer>
</body></html>"""


def cta_block(city_links=True):
    if CTA_PHONE:
        tel = re.sub(r"[^0-9+]", "", CTA_PHONE)
        return f"""<div class="cta"><div><b>Equipment still down?</b> Codes tell you what failed —
not always how bad. {esc(CTA_PHONE_LABEL)}.</div>
<a class="phone" href="tel:{tel}">&#9742; {esc(CTA_PHONE)}</a></div>"""
    if city_links and CITY_LINKS:
        links = " &nbsp;&middot;&nbsp; ".join(
            f'<a href="/{slug}/">{esc(name)}, {esc(st)} &rarr;</a>'
            for name, st, slug in CITY_LINKS)
        return (f'<div class="cta"><div><b>Equipment still down?</b> '
                f'{esc(CTA_REGION_LINE)}, see who services {esc(EQUIPMENT)}s '
                f'near you:</div><div style="margin-top:10px">{links}</div></div>')
    return ""


def parts_block():
    if not PARTS_LINK:
        return ""
    return (f'<p><a href="{esc(PARTS_LINK)}" rel="sponsored nofollow">'
            f'Order OEM replacement parts &rarr;</a></p>')


def code_page(entry, related):
    brand, fam, code = entry["brand"], entry.get("model_family", ""), entry["code"]
    title = entry.get("title", "")
    meaning = entry.get("meaning", "")
    when_to_call = entry.get("when_to_call", "")
    diy = entry.get("diy_steps", [])
    h1 = f"{brand} {fam} — {code}: {title}" if fam else f"{brand} {code}: {title}"
    steps = "".join(f"<li>{esc(s)}</li>" for s in diy)
    safety = entry.get("safety_flag", "")
    safety_html = (f'<div class="callout"><b>Safety:</b> {esc(safety)}</div>'
                   if safety and len(str(safety)) > 20 else "")
    rel_html = "".join(
        f'<a href="{r["url"]}"><span class="c">{esc(r["code"])}</span>'
        f'<div class="t">{esc(r.get("title",""))}</div></a>' for r in related[:6])
    related_sec = (f'<h2>Other {esc(brand)} {esc(fam)} codes</h2>'
                   f'<div class="grid">{rel_html}</div>') if rel_html else ""
    src = entry.get("source_url", "")
    src_html = (f'<p class="src">Verified against service documentation: '
                f'<a href="{esc(src)}" rel="nofollow">{esc(src)}</a></p>') if src else ""

    # Depth data: family context + per-code supplements (causes / fixability /
    # why-a-technician). Sections render only where the data exists.
    supp = SUPPLEMENTS.get(f"{fam}||{code}", {})
    fam_html = FAMILIES.get(fam, "")
    causes = supp.get("causes", [])
    fixable = supp.get("fixable", "")
    why_tech = supp.get("why_tech", "")

    # Question-led pages: the H1 and title ARE the question the searcher types.
    fam_short = fam.split("(")[0].strip() if fam else ""
    fam_is_selfdesc = any(w in fam_short.lower() for w in
                          ("control", "series", "model"))
    if fam_short and fam_is_selfdesc:
        default_q = f"What does {code} mean on a {brand} {fam_short}?"
    elif fam_short:
        default_q = f"What does {code} mean on a {brand} {fam_short} {EQUIPMENT_SHORT}?"
    else:
        default_q = f"What does {code} mean on a {brand} {EQUIPMENT_SHORT}?"
    question = supp.get("question") or default_q

    if fam_html:
        blurb = fam_html.replace(
            "<p><b>Which machines show this code:</b>", "<p>").replace(
            "<p><b>Which machines show this signal:</b>", "<p>")
        fam_sec = f"<h2>Which machines show this?</h2>{blurb}"
    else:
        fam_sec = ""
    causes_sec = (f"<h2>What causes it?</h2><ul>" +
                  "".join(f"<li>{esc(c)}</li>" for c in causes) +
                  "</ul>") if causes else ""
    fix_intro = f"<p>{esc(fixable)}</p>" if fixable else ""
    city_prose = ""
    if CITY_LINKS:
        links = " or ".join(f'<a href="/{slug}/">{esc(n)}, {esc(st)}</a>'
                            for n, st, slug in CITY_LINKS)
        city_prose = (f"<p>If it does come to a service call and you're in "
                      f"{links}, we maintain independently compiled lists of "
                      f"local companies that service {esc(EQUIPMENT)}s — real "
                      f"businesses with verified contact information, none of "
                      f"whom paid to be listed.</p>")

    # Per-page FAQ — every answer is built from THIS code's verified data, so
    # each page carries unique content and matching FAQPage structured data.
    first_step = diy[0].rstrip(".") if diy else ""
    q1 = f"What does {code} mean on a {brand} {fam}?".replace("  ", " ")
    a1 = f"{title}. {meaning}"
    q2 = f"Can I fix {code} on a {brand} {fam} myself?".replace("  ", " ")
    if fixable:
        a2 = fixable
    elif first_step:
        a2 = (f"Some causes behind this fault are within reach of on-site staff. "
              f"Start with the documented first steps — {first_step.lower()} — and "
              f"work through the checklist above before paying for a service call. "
              f"Anything involving refrigerant, pressurized components, or the "
              f"electrical cabinet belongs to a qualified technician.")
    else:
        a2 = ("This one is not a do-it-yourself fault — see the guidance above and "
              "have a qualified technician handle it.")
    q3 = f"When does {code} on a {brand} {fam} need a technician?".replace("  ", " ")
    a3 = f"{why_tech} {when_to_call}".strip() if why_tech else when_to_call
    faqs = [(q1, a1), (q2, a2), (q3, a3)]
    # Don't visibly repeat the H1 question inside the FAQ block; it stays in
    # the structured data, where the page itself is its answer.
    faq_html = "".join(f"<h3>{esc(q)}</h3><p>{esc(a)}</p>"
                       for q, a in faqs if a and q != question)
    schema = [{
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}}
                       for q, a in faqs if a]
    }]
    intro = (f"<b>Short answer: {esc(title)}.</b> If your {esc(brand)} "
             f"{esc(fam)} is showing <b>{esc(code)}</b>, the controller has "
             f"logged a specific, documented condition. This page covers what it "
             f"means, what causes it, what you can safely fix yourself, and when "
             f"— and why — it takes a technician.")
    body = f"""<main><div class="wrap">
<div class="crumbs"><a href="/">Home</a> &rsaquo; <a href="/{slugify(brand)}/">{esc(brand)}</a> &rsaquo; {esc(code)}</div>
<div class="card">
<span class="family-tag">{esc(brand)} {esc(fam)} &middot; {esc(code)}</span>
<h1 class="page-h1">{esc(question)}</h1>
<p class="meaning">{intro}</p>
<h2>What exactly is the machine telling you?</h2>
<p>{esc(meaning)}</p>
{fam_sec}
{causes_sec}
<h2>Can you fix it yourself?</h2>
{fix_intro}
<p><b>Step by step — what to try, in order:</b></p>
<ol class="steps">{steps}</ol>
<div class="tipbox"><b>One reset is diagnosis, repeated resets are damage.</b>
If the same fault returns after a single reset, the underlying condition is real —
stop resetting and deal with the cause.</div>
{safety_html}
<h2>When do you need a technician — and why?</h2>
{f'<p>{esc(why_tech)}</p>' if why_tech else ''}
<div class="callout"><b>When to call:</b> {esc(when_to_call)}</div>
{city_prose}
{parts_block()}
<h2>Related questions</h2>
{faq_html}
{src_html}
</div>
{related_sec}
</div></main>"""
    meta = (f"{question} {title}. What causes it, what you can fix yourself, "
            f"and when it takes a technician.")
    return page(question, meta[:158], body, entry["canonical"], schema)


def brand_page(brand, families, brand_intros=None):
    intro = (brand_intros or {}).get(brand, "")
    intro_html = f'<article class="card">{intro}</article>' if intro else ""
    secs = ""
    for fam, entries in sorted(families.items()):
        cards = "".join(
            f'<a href="{e["url"]}"><span class="c">{esc(e["code"])}</span>'
            f'<div class="t">{esc(e.get("title",""))}</div></a>' for e in entries)
        secs += f"<h2>{esc(brand)} {esc(fam)}</h2><div class='grid'>{cards}</div>"
    n = sum(len(v) for v in families.values())
    body = f"""<div class="hero"><div class="wrap"><h1>{esc(brand)} Fault &amp; Error Codes</h1>
<p>{n} documented codes and fault signals, verified against service manuals, with
plain-English fixes.</p></div></div>
<main><div class="wrap">{intro_html}{secs}{cta_block()}</div></main>"""
    return page(f"{brand} Error Codes — Full Documented List",
                f"Every documented {brand} {EQUIPMENT} error code and fault "
                f"signal: what it means, what to check, when to call a tech.",
                body, f"{BASE_URL}/{slugify(brand)}/")


def city_page(city):
    name, state, slug = city["name"], city["state"], city["slug"]
    biz_html = ""
    for c in city.get("companies", []):
        phone = c.get("phone", "")
        tel = re.sub(r"[^0-9+]", "", phone)
        phone_html = (f'<a class="tel" href="tel:{tel}">&#9742; {esc(phone)}</a>'
                      if phone else "")
        site = c.get("website", "")
        site_html = (f' &middot; <a href="{esc(site)}" rel="nofollow">website</a>'
                     if site else "")
        svcs = ", ".join(c.get("services", []))
        brands = ", ".join(c.get("brands_serviced", []))
        brands_html = f" &middot; Brands: {esc(brands)}" if brands else ""
        biz_html += f"""<div class="biz"><b>{esc(c['name'])}</b> — {esc(c.get('city',''))}<br>
{phone_html}{site_html}<br>
<span class="svc">{esc(svcs)}{brands_html}</span><br>
<span class="svc">{esc(c.get('notes',''))}</span></div>"""
    faq = city.get("faq", [])
    faq_html = "".join(f"<h3>{esc(q['q'])}</h3><p>{esc(q['a'])}</p>" for q in faq)
    faq_schema = [{
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q["q"],
                        "acceptedAnswer": {"@type": "Answer", "text": q["a"]}}
                       for q in faq]
    }] if faq else []
    body = f"""<div class="hero"><div class="wrap">
<h1>{esc(EQUIPMENT.title())} Repair &amp; Service in {esc(name)}, {esc(state)}</h1>
<p>{esc(CITY_HERO_SUB.format(city=name))}</p>
</div></div>
<main><div class="wrap">
<article class="card">{city.get('intro_html','')}
<div class="tipbox"><b>Before you call anyone:</b> look up the exact code or fault
signal your equipment is showing — start at the <a href="/">code lookup</a>. A
meaningful share of "breakdowns" are airflow, power, or maintenance problems a
15-minute check can catch before you pay for a service call.</div></article>
{cta_block(city_links=False)}
<div class="card"><h2>Service companies serving {esc(name)}</h2>
<p class="svc" style="color:var(--sub)">Independent listing compiled from each company's
own published information. No company paid to appear here. Verify details when you call.</p>
{biz_html}</div>
<div class="card"><h2>Frequently asked questions</h2>{faq_html}</div>
</div></main>"""
    title = f"{EQUIPMENT.title()} Repair {name} {state} — Commercial Service"
    desc = (f"{EQUIPMENT.title()} repair and service in {name}, {state}: verified "
            f"local companies, plus what to check before you pay for a service call.")
    return page(title, desc[:158], body, f"{BASE_URL}/{slug}/", faq_schema)


def article_page(a, all_articles):
    others = [x for x in all_articles if x is not a][:4]
    more = "".join(f'<a href="/guides/{x["slug"]}/"><span class="c">{esc(x["h1"])}</span>'
                   f'<div class="t">{esc(x.get("teaser",""))}</div></a>' for x in others)
    schema = [{
        "@context": "https://schema.org", "@type": "Article",
        "headline": a["h1"],
        "datePublished": a.get("date", str(date.today())),
        "author": {"@type": "Organization", "name": SITE_NAME},
    }]
    body = f"""<main><div class="wrap">
<div class="crumbs"><a href="/">Home</a> &rsaquo; <a href="/guides/">Guides</a> &rsaquo; {esc(a['h1'])}</div>
<article class="card"><h1 class="page-h1">{a['h1']}</h1>
{a['body_html']}</article>
{cta_block()}
<h2>More guides</h2><div class="grid">{more}</div>
</div></main>"""
    return page(a["title"], a["meta_desc"][:158], body,
                f"{BASE_URL}/guides/{a['slug']}/", schema)


def guides_index(articles):
    cards = "".join(
        f'<a href="/guides/{a["slug"]}/"><span class="c">{esc(a["h1"])}</span>'
        f'<div class="t">{esc(a.get("teaser",""))}</div></a>' for a in articles)
    body = f"""<div class="hero"><div class="wrap"><h1>Guides</h1>
<p>Troubleshooting, maintenance, and buying guidance for the people who keep
{esc(EQUIPMENT)}s running.</p></div></div>
<main><div class="wrap"><div class="grid">{cards}</div>{cta_block()}</div></main>"""
    return page(f"{EQUIPMENT.title()} Guides & Troubleshooting",
                f"Practical guides for facility and kitchen staff: troubleshooting, "
                f"maintenance, and repair-or-replace decisions for {EQUIPMENT}s.",
                body, f"{BASE_URL}/guides/")


def home_page(by_brand, cities, articles, total):
    rows = "".join(
        f'<a href="/{slugify(b)}/"><b>{esc(b)}</b>{len(v)} codes documented</a>'
        for b, v in sorted(by_brand.items()))
    city_rows = "".join(
        f'<a href="/{c["slug"]}/"><b>{esc(c["name"])}, {esc(c["state"])}</b>'
        f'Local repair &amp; service</a>' for c in cities)
    city_sec = (f'<h2>Local service</h2><div class="brand-row sub">{city_rows}</div>'
                if cities else "")
    art_rows = "".join(
        f'<a href="/guides/{a["slug"]}/"><span class="c">{esc(a["h1"])}</span>'
        f'<div class="t">{esc(a.get("teaser",""))}</div></a>' for a in articles[:6])
    art_sec = f'<h2>Guides</h2><div class="grid">{art_rows}</div>' if articles else ""
    brands_line = " and ".join(sorted(by_brand))
    sub = HOME_SUB.format(n=total, brands=brands_line)
    body = f"""<div class="hero"><div class="wrap">
<h1>{esc(HOME_H1)}</h1>
<p>{esc(sub)}</p>
</div></div>
<main><div class="wrap">
<div class="brand-row">{rows}</div>
{city_sec}
{art_sec}
{cta_block()}
</div></main>"""
    return page(HOME_TITLE, HOME_DESC, body, f"{BASE_URL}/")


def main():
    global NAV_HTML, FOOTER_LINKS_HTML, CITY_LINKS, FAMILIES, SUPPLEMENTS

    for name, target in (("families.json", "FAMILIES"),
                         ("supplements.json", "SUPPLEMENTS")):
        f = ROOT / "data" / name
        if f.exists():
            globals()[target] = json.loads(f.read_text(encoding="utf-8"))

    entries = []
    for f in sorted((ROOT / "data").glob("codes-*.json")):
        entries += json.loads(f.read_text(encoding="utf-8"))

    brands_file = ROOT / "data" / "brands.json"
    brand_intros = (json.loads(brands_file.read_text(encoding="utf-8"))
                    if brands_file.exists() else {})

    cities_file = ROOT / "data" / "cities.json"
    cities = (json.loads(cities_file.read_text(encoding="utf-8"))
              if cities_file.exists() else [])

    articles_file = ROOT / "content" / "articles.json"
    articles = (json.loads(articles_file.read_text(encoding="utf-8"))
                if articles_file.exists() else [])

    brands = sorted({e["brand"] for e in entries})
    NAV_HTML = "".join(f'<a href="/{slugify(b)}/">{esc(b)}</a>' for b in brands)
    if articles:
        NAV_HTML += '<a href="/guides/">Guides</a>'
    CITY_LINKS = [(c["name"], c["state"], c["slug"]) for c in cities]
    FOOTER_LINKS_HTML = "".join(
        f' &middot; <a href="/{slug}/">{esc(name)}</a>'
        for name, _st, slug in CITY_LINKS)

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    seen = set()
    for e in entries:
        slug = f"{slugify(e.get('model_family',''))}-{slugify(e['code'])}".strip("-")
        while slug in seen:
            slug += "-2"
        seen.add(slug)
        e["path"] = f"{slugify(e['brand'])}/{slug}/"
        e["url"] = f"/{e['path']}"
        e["canonical"] = f"{BASE_URL}/{e['path']}"

    by_brand = defaultdict(list)
    by_family = defaultdict(lambda: defaultdict(list))
    for e in entries:
        by_brand[e["brand"]].append(e)
        by_family[e["brand"]][e.get("model_family", "Other")].append(e)

    urls = [f"{BASE_URL}/"]

    for e in entries:
        related = [r for r in by_family[e["brand"]][e.get("model_family", "Other")]
                   if r is not e]
        d = OUT / e["path"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(code_page(e, related), encoding="utf-8")
        urls.append(e["canonical"])

    for brand, fams in by_family.items():
        d = OUT / slugify(brand)
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(brand_page(brand, fams, brand_intros),
                                      encoding="utf-8")
        urls.append(f"{BASE_URL}/{slugify(brand)}/")

    for c in cities:
        d = OUT / c["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(city_page(c), encoding="utf-8")
        urls.append(f"{BASE_URL}/{c['slug']}/")

    if articles:
        gd = OUT / "guides"
        gd.mkdir(parents=True, exist_ok=True)
        (gd / "index.html").write_text(guides_index(articles), encoding="utf-8")
        urls.append(f"{BASE_URL}/guides/")
        for a in articles:
            d = gd / a["slug"]
            d.mkdir(parents=True, exist_ok=True)
            (d / "index.html").write_text(article_page(a, articles), encoding="utf-8")
            urls.append(f"{BASE_URL}/guides/{a['slug']}/")

    (OUT / "index.html").write_text(
        home_page(by_brand, cities, articles, len(entries)), encoding="utf-8")

    sm = "\n".join(f"<url><loc>{u}</loc></url>" for u in urls)
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{sm}\n</urlset>", encoding="utf-8")
    (OUT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n", encoding="utf-8")

    print(f"Generated: {len(entries)} code pages, {len(by_brand)} brand pages, "
          f"{len(cities)} city pages, {len(articles)} guides -> {OUT}")


if __name__ == "__main__":
    main()
