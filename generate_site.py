#!/usr/bin/env python3
"""
Walk-In Cooler Code Lookup — Static Site Generator
===================================================
One rich page per CONTROLLER FAMILY: the manufacturer's full code table, a
full section for every verified code, a diagnostic sequence, the parts usually
involved, and primary-source citations. Consolidated 2026-09-10 from one page
per code (thin pages don't index); the 128 retired URLs live in
data/redirects.json and are 301'd to page#code-anchor through firebase.json.

Inputs (all relative to this file):
  data/codes-*.json            verified fault codes -> full per-code sections
  data/supplements.json        causes / fixability / why-technician, per code
  data/families.json           which-machines context, per data family
  data/controller_pages.json   families -> page, full code-table rows,
                               diagnostic sequence, parts, hub copy
  data/sources.json            primary-source registry (every citation)
  data/redirects.json          retired per-code URLs (never delete entries)
  data/brands.json             brand hub intros
  data/cities.json             city pages: intro, FAQs, verified companies
  content/articles.json        long-form guides

Run (Windows or Linux, Python 3 stdlib only):
    python generate_site.py
Output -> ./site/  (and the "redirects" block of firebase.json is re-synced).
The build exits 1 if any check fails: broken internal link or #anchor,
duplicate <title>, a page under MIN_WORDS visible words, a page without a
primary-source citation, a page more than MAX_HUB_CLICKS clicks from a brand
hub, a code sourced to an unregistered URL, or a redirect that won't resolve.
"""

import json
import re
import shutil
import sys
from collections import defaultdict, deque
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

# ---------------------------------------------------------------- CONFIG ---
BASE_URL = "https://walkincoolercodes.com"
SITE_NAME = "Walk-In Cooler Code Lookup"
EQUIPMENT = "walk-in cooler"        # noun used in copy
HOME_H1 = "Walk-in cooler showing an alarm code?"
HOME_SUB = ("{n} documented fault codes across {brands} controllers, taken from "
            "the manufacturers' own manuals — what each one means, what to "
            "check yourself, and when it's a tech call.")
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
CONTENT_UPDATED = "2026-09-10"   # sitemap <lastmod> — bump when page content changes
# The one canonical home of the refrigeration-cycle explanations (superheat,
# subcooling, defrost, condenser, refrigerants). Controller pages link into
# its #anchors instead of re-explaining them.
FUNDAMENTALS_GUIDE = "walk-in-cooler-alarm-codes-guide"
FRAGMENT_REDIRECTS = True   # 301 -> page#code-anchor (Firebase keeps the #)
MIN_WORDS = 400
MAX_HUB_CLICKS = 2
# ------------------------------------------------------------ END CONFIG ---

ROOT = Path(__file__).parent
OUT = ROOT / "site"
DATA = ROOT / "data"
FIREBASE_JSON = ROOT / "firebase.json"
# Files copied verbatim into site/ on every build. main() wipes site/, so
# anything that must survive a rebuild lives here, NOT in site/.
# Holds both Google site-verification tokens and the IndexNow key — deleting
# any of them breaks the service behind it. Never remove them.
STATIC = ROOT / "static"

FUNDAMENTALS = {
    "refrigeration-cycle": "how the refrigeration cycle works",
    "temperature-control": "how a controller holds temperature — and how its sensors are tested",
    "superheat": "what superheat is and why controllers alarm on it",
    "subcooling": "what subcooling is",
    "defrost": "how defrost works and what goes wrong",
    "condenser": "why the condenser matters",
    "refrigerants": "refrigerants and the A2L change",
}
KIND_LABEL = {"signal": "status message", "status": "status",
              "message": "message", "info": "information"}

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
article p,.card p{margin:10px 0}
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
.src{font-size:.8rem;color:var(--sub);margin-top:12px}
.tbl{overflow-x:auto;margin:12px 0}
table.codes,table.parts{border-collapse:collapse;width:100%;font-size:.92rem}
table.codes th,table.codes td,table.parts th,table.parts td{border-bottom:1px solid var(--line);
padding:7px 9px;text-align:left;vertical-align:top}
table.codes th,table.parts th{background:var(--accent);font-size:.84rem}
table.codes td:first-child{white-space:nowrap}
tr:target,section:target{background:#fff8e1}
.kind{display:inline-block;font-size:.72rem;color:var(--sub);border:1px solid var(--line);
border-radius:10px;padding:0 7px;margin-left:6px;white-space:nowrap}
.code-sec{border-top:1px solid var(--line);padding-top:6px;margin-top:20px}
.code-sec h3{font-size:1.08rem}
.applies,.note{font-size:.85rem;color:var(--sub)}
.sources .src-list{padding-left:20px}
.sources li{margin:7px 0;font-size:.9rem}
.sources .doc{color:var(--sub)}
.chips a{display:inline-block;border:1px solid var(--line);border-radius:14px;padding:1px 9px;
margin:3px 2px;text-decoration:none;font-size:.85rem;background:#fff}
footer{border-top:1px solid var(--line);padding:26px 0;font-size:.85rem;color:var(--sub)}
footer .wrap{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
.disclaimer{font-size:.78rem;color:var(--sub);margin-top:8px}
"""

# Populated in main() before any page renders.
NAV_HTML = ""
FOOTER_LINKS_HTML = ""
CITY_LINKS = []    # [(name, state, slug)]
FAMILIES = {}      # model_family -> intro html (data/families.json)
SUPPLEMENTS = {}   # "family||code" -> {causes, fixable, why_tech} (data/supplements.json)
SOURCES = {}       # id -> {publisher, title, doc, url} (data/sources.json)
SOURCE_BY_URL = {}


def esc(s):
    return (str(s or "").replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def slugify(text):
    s = re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")
    return s or "x"


def load_json(rel, default=None):
    f = ROOT / rel
    if not f.exists():
        return default
    return json.loads(f.read_text(encoding="utf-8"))


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


def breadcrumb(items):
    """items: [(label, path or None for the current page)] -> (html, schema)."""
    html = " &rsaquo; ".join(
        f'<a href="{path}">{esc(label)}</a>' if path else esc(label)
        for label, path in items)
    elements = []
    for i, (label, path) in enumerate(items):
        el = {"@type": "ListItem", "position": i + 1, "name": label}
        if path:
            el["item"] = BASE_URL + path
        elements.append(el)
    schema = {"@context": "https://schema.org", "@type": "BreadcrumbList",
              "itemListElement": elements}
    return f'<div class="crumbs">{html}</div>', schema


def cite(sid):
    s = SOURCES[sid]
    return (f'<a href="{esc(s["url"])}">{esc(s["publisher"])} — {esc(s["title"])}</a> '
            f'<span class="doc">({esc(s["doc"])})</span>')


def sources_block(ids, notes=None, lead=""):
    notes = notes or {}
    items = "".join(
        f"<li>{cite(sid)}" + (f" — {esc(notes[sid])}" if notes.get(sid) else "") + "</li>"
        for sid in ids)
    lead_html = f"<p>{esc(lead)}</p>" if lead else ""
    return (f'<div class="card sources"><h2>Sources</h2>{lead_html}'
            f'<ul class="src-list">{items}</ul></div>')


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


def city_prose():
    if not CITY_LINKS:
        return ""
    links = " or ".join(f'<a href="/{slug}/">{esc(n)}, {esc(st)}</a>'
                        for n, st, slug in CITY_LINKS)
    return (f"<p>If it does come to a service call and you're in {links}, we "
            f"maintain independently compiled lists of local companies that "
            f"service {esc(EQUIPMENT)}s — real businesses with verified contact "
            f"information, none of whom paid to be listed.</p>")


def fam_blurb(fam):
    return (FAMILIES.get(fam, "")
            .replace("<p><b>Which machines show this code:</b>", "<p>")
            .replace("<p><b>Which machines show this signal:</b>", "<p>"))


# ------------------------------------------------------ controller pages ---
def build_rows(pg, fam_entries):
    """Full code table for one page: verified entries (with full sections)
    first, in data order, then manual-table rows placed after their 'after'
    code. Assigns a unique #anchor to every row."""
    applies = pg.get("applies", {})
    override = pg.get("applies_override", {})
    rows = []
    for fam in pg["families"]:
        for e in fam_entries[fam]:
            rows.append({"code": e["code"], "title": e["title"], "entry": e,
                         "applies": override.get(e["code"], applies.get(fam, "")),
                         "kind": "alarm"})
    for t in pg.get("table_rows", []):
        row = {"code": t["code"], "title": t["meaning"], "entry": None,
               "applies": t.get("applies", ""), "kind": t.get("kind", "alarm")}
        idx = len(rows)
        if t.get("after"):
            hits = [i for i, r in enumerate(rows) if r["code"] == t["after"]]
            if not hits:
                raise SystemExit(f"{pg['id']}: row {t['code']} is 'after' "
                                 f"{t['after']}, which is not on the page")
            idx = hits[-1] + 1
        rows.insert(idx, row)
    taken = set()
    for r in rows:
        base = "code-" + slugify(r["code"])
        anchor = base
        if anchor in taken:   # e.g. Carel cht vs CHt
            anchor = f"{base}-{slugify(r['title'])[:40]}".rstrip("-")
        n = 2
        while anchor in taken:
            anchor = f"{base}-{n}"
            n += 1
        taken.add(anchor)
        r["anchor"] = anchor
    return rows


def code_section(r):
    e = r["entry"]
    supp = SUPPLEMENTS.get(f"{e['model_family']}||{e['code']}", {})
    src = SOURCE_BY_URL[e["source_url"]]
    out = [f'<section class="code-sec" id="{r["anchor"]}">',
           f"<h3>{esc(e['code'])} — {esc(e['title'])}</h3>"]
    if r["applies"]:
        out.append(f'<p class="applies">Applies to: {esc(r["applies"])}</p>')
    out.append(f"<p>{esc(e['meaning'])}</p>")
    if supp.get("causes"):
        out.append("<p><b>What causes it:</b></p><ul>"
                   + "".join(f"<li>{esc(c)}</li>" for c in supp["causes"]) + "</ul>")
    if supp.get("fixable"):
        out.append(f"<p><b>Can staff fix it?</b> {esc(supp['fixable'])}</p>")
    if e.get("diy_steps"):
        out.append('<p><b>What to check, in order:</b></p><ol class="steps">'
                   + "".join(f"<li>{esc(s)}</li>" for s in e["diy_steps"]) + "</ol>")
    safety = str(e.get("safety_flag") or "")
    if len(safety) > 20:
        out.append(f'<div class="callout"><b>Safety:</b> {esc(safety)}</div>')
    if supp.get("why_tech"):
        out.append(f"<p><b>Why it takes a technician:</b> {esc(supp['why_tech'])}</p>")
    if e.get("when_to_call"):
        out.append(f'<div class="callout"><b>When to call:</b> {esc(e["when_to_call"])}</div>')
    out.append(f'<p class="src">Source: <a href="{esc(e["source_url"])}">'
               f'{esc(src["publisher"])} — {esc(src["title"])}</a> ({esc(src["doc"])})</p>')
    out.append("</section>")
    return "\n".join(out)


def controller_page(pg, rows, brand_pages, hub_path):
    brand, name = pg["brand"], pg["name"]
    path = "/" + pg["path"]
    is_hub = path == hub_path
    anchor_by_code = {r["code"]: r["anchor"] for r in rows}
    extra_cols = pg.get("extra_cols", [])
    show_applies = any(r["applies"] for r in rows)

    head = ("<tr><th>Code</th><th>What it means</th>"
            + ("<th>Applies to</th>" if show_applies else "")
            + "".join(f"<th>{esc(c['label'])}</th>" for c in extra_cols) + "</tr>")
    trs = []
    for r in rows:
        badge = (f' <span class="kind">{KIND_LABEL[r["kind"]]}</span>'
                 if r["kind"] in KIND_LABEL else "")
        if r["entry"]:
            cells = [f'<a href="#{r["anchor"]}"><b>{esc(r["code"])}</b></a>']
            tr = "<tr>"
        else:
            cells = [f"<b>{esc(r['code'])}</b>"]
            tr = f'<tr id="{r["anchor"]}">'
        cells.append(esc(r["title"]) + badge)
        if show_applies:
            cells.append(esc(r["applies"]) or "&mdash;")
        cells += [esc(c["values"].get(r["code"], "")) or "&mdash;" for c in extra_cols]
        trs.append(tr + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
    table = (f'<div class="tbl"><table class="codes"><thead>{head}</thead>'
             f'<tbody>{"".join(trs)}</tbody></table></div>')
    n_detail = sum(1 for r in rows if r["entry"])
    n_listed = len(rows) - n_detail
    note = f"{n_detail} codes link to a full section below."
    if n_listed:
        note += (f" The other {n_listed} are listed as the manufacturer's "
                 f"manual gives them.")
    note += " Every row comes from the manual cited at the end of this page."

    sections = "\n".join(code_section(r) for r in rows if r["entry"])
    diagnosis = ('<ol class="steps">'
                 + "".join(f"<li>{s}</li>" for s in pg["diagnosis"]) + "</ol>")

    prow = []
    for p in pg["parts"]:
        links = []
        for c in p["codes"]:
            if c not in anchor_by_code:
                raise SystemExit(f"{pg['id']}: part '{p['part']}' lists code "
                                 f"{c!r}, which is not on the page")
            links.append(f'<a href="#{anchor_by_code[c]}">{esc(c)}</a>')
        prow.append(f"<tr><td>{esc(p['part'])}</td><td>{', '.join(links) or '&mdash;'}"
                    f"</td><td>{esc(p.get('note', ''))}</td></tr>")
    parts_tbl = ('<div class="tbl"><table class="parts"><thead><tr><th>Part</th>'
                 '<th>Codes that point to it</th><th>Note</th></tr></thead><tbody>'
                 + "".join(prow) + "</tbody></table></div>")

    fund = pg.get("fundamentals", [])
    fund_html = ""
    if fund:
        links = "; ".join(
            f'<a href="/guides/{FUNDAMENTALS_GUIDE}/#{f}">{esc(FUNDAMENTALS[f])}</a>'
            for f in fund)
        fund_html = ("<h2>What refrigeration is behind these codes?</h2>"
                     "<p>Every code here is the controller reporting a reading from "
                     "the refrigeration system. The background is explained once, "
                     f"for every controller on this site: {links}.</p>")

    others = [s for s in brand_pages if s["id"] != pg["id"]]
    sib_html = ""
    if others:
        cards = "".join(
            f'<a href="/{s["path"]}"><span class="c">{esc(s["name"])}</span>'
            f'<div class="t">{esc(s["recognize"])}</div></a>' for s in others)
        sib_html = (f"<h2>Other {esc(brand)} controllers</h2>"
                    f"<div class='grid'>{cards}</div>")

    crumbs = [("Home", "/"), (brand, None)] if is_hub else \
             [("Home", "/"), (brand, hub_path), (name, None)]
    crumbs_html, bc = breadcrumb(crumbs)
    faq = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question",
                           "name": f"What does {r['code']} mean on a {pg['faq_name']}?",
                           "acceptedAnswer": {"@type": "Answer",
                                              "text": f"{r['title']}. {r['entry']['meaning']}"}}
                          for r in rows if r["entry"]]}
    blurbs = "".join(fam_blurb(f) for f in pg["families"])
    body = f"""<main><div class="wrap">
{crumbs_html}
<article class="card">
<span class="family-tag">{esc(brand)} &middot; {len(rows)} codes and messages</span>
<h1 class="page-h1">{esc(pg['h1'])}</h1>
{pg['short_answer']}
<h2>Which machines use it?</h2>
{blurbs}
<h2>How do you read and clear the display?</h2>
{pg['display_html']}
<h2 id="code-table">Every {esc(name)} code at a glance</h2>
{table}
<p class="note">{esc(note)}</p>
<h2>What does each code mean — and what should you do?</h2>
{sections}
<h2>How do you diagnose a {esc(name)} alarm, step by step?</h2>
{diagnosis}
<div class="tipbox"><b>One reset is diagnosis, repeated resets are damage.</b>
If the same fault returns after a single reset, the underlying condition is real —
stop resetting and deal with the cause.</div>
<h2>Which parts are usually involved?</h2>
{parts_tbl}
{fund_html}
{pg.get('extra_html', '')}
{city_prose()}
{parts_block()}
</article>
{sources_block(pg['sources'])}
{sib_html}
</div></main>"""
    return page(pg["title"], pg["meta"][:158], body, BASE_URL + path, [faq, bc])


def hub_page(brand, brand_pages, rows_by_page, cfg, intro):
    hub_path = f"/{slugify(brand)}/"
    crumbs_html, bc = breadcrumb([("Home", "/"), (brand, None)])
    secs, index, srcs = [], [], []
    for pg in brand_pages:
        rows = rows_by_page[pg["id"]]
        blurbs = "".join(fam_blurb(f) for f in pg["families"])
        secs.append(f'<h3><a href="/{pg["path"]}">{esc(pg["name"])}</a></h3>{blurbs}'
                    f'<p><a href="/{pg["path"]}">All {len(rows)} {esc(pg["name"])} '
                    f'codes — meanings, checks, diagnosis and parts &rarr;</a></p>')
        chips = "".join(f'<a href="/{pg["path"]}#{r["anchor"]}">{esc(r["code"])}</a>'
                        for r in rows if r["kind"] == "alarm")
        index.append(f'<p><b>{esc(pg["name"])}:</b></p><div class="chips">{chips}</div>')
        srcs += [s for s in pg["sources"] if s not in srcs]
    body = f"""<main><div class="wrap">
{crumbs_html}
<article class="card">
<h1 class="page-h1">{esc(cfg['h1'])}</h1>
{intro}
<h2>Which {esc(brand)} controller do you have?</h2>
{''.join(secs)}
<h2>Every {esc(brand)} code, by controller</h2>
{''.join(index)}
</article>
{cta_block()}
{sources_block(srcs)}
</div></main>"""
    return page(cfg["title"], cfg["meta"][:158], body, BASE_URL + hub_path, [bc])


# --------------------------------------------------------- other pages ---
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
    schema = [{
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q["q"],
                        "acceptedAnswer": {"@type": "Answer", "text": q["a"]}}
                       for q in faq]
    }] if faq else []
    src_html = (sources_block(city["sources"], city.get("source_notes"))
                if city.get("sources") else "")
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
{src_html}
</div></main>"""
    title = f"{EQUIPMENT.title()} Repair {name} {state} — Commercial Service"
    desc = (f"{EQUIPMENT.title()} repair and service in {name}, {state}: verified "
            f"local companies, plus what to check before you pay for a service call.")
    return page(title, desc[:158], body, f"{BASE_URL}/{slug}/", schema)


def article_page(a, all_articles):
    others = [x for x in all_articles if x is not a][:4]
    more = "".join(f'<a href="/guides/{x["slug"]}/"><span class="c">{esc(x["h1"])}</span>'
                   f'<div class="t">{esc(x.get("teaser",""))}</div></a>' for x in others)
    crumbs_html, bc = breadcrumb([("Home", "/"), ("Guides", "/guides/"), (a["h1"], None)])
    schema = [{
        "@context": "https://schema.org", "@type": "Article",
        "headline": a["h1"],
        "datePublished": a.get("date", str(date.today())),
        "dateModified": CONTENT_UPDATED,
        "author": {"@type": "Organization", "name": SITE_NAME},
        "citation": [SOURCES[s]["url"] for s in a.get("sources", [])],
    }, bc]
    src_html = (sources_block(a["sources"], a.get("source_notes"))
                if a.get("sources") else "")
    body = f"""<main><div class="wrap">
{crumbs_html}
<article class="card"><h1 class="page-h1">{a['h1']}</h1>
{a['body_html']}</article>
{src_html}
{cta_block()}
<h2>More guides</h2><div class="grid">{more}</div>
</div></main>"""
    return page(a["title"], a["meta_desc"][:158], body,
                f"{BASE_URL}/guides/{a['slug']}/", schema)


def guides_index(articles):
    cards = "".join(
        f'<a href="/guides/{a["slug"]}/"><span class="c">{esc(a["h1"])}</span>'
        f'<div class="t">{esc(a.get("teaser",""))}</div></a>' for a in articles)
    srcs = []
    for a in articles:
        srcs += [s for s in a.get("sources", []) if s not in srcs]
    crumbs_html, bc = breadcrumb([("Home", "/"), ("Guides", None)])
    body = f"""<div class="hero"><div class="wrap"><h1>Guides</h1>
<p>Troubleshooting, maintenance, and buying guidance for the people who keep
{esc(EQUIPMENT)}s running.</p></div></div>
<main><div class="wrap">{crumbs_html}<div class="grid">{cards}</div>{cta_block()}
{sources_block(srcs, lead="The guides draw on these manufacturer manuals and the FDA Food Code:")}
</div></main>"""
    return page(f"{EQUIPMENT.title()} Guides & Troubleshooting",
                f"Practical guides for facility and kitchen staff: troubleshooting, "
                f"maintenance, and repair-or-replace decisions for {EQUIPMENT}s.",
                body, f"{BASE_URL}/guides/", [bc])


def home_page(brands, pages_by_brand, rows_by_page, cities, articles):
    def n_codes(pgs):
        return sum(1 for pg in pgs for r in rows_by_page[pg["id"]] if r["kind"] == "alarm")
    rows = "".join(
        f'<a href="/{slugify(b)}/"><b>{esc(b)}</b>{n_codes(pages_by_brand[b])} codes documented</a>'
        for b in brands)
    ctrl = "".join(
        f'<a href="/{pg["path"]}"><span class="c">{esc(pg["name"])}</span>'
        f'<div class="t">{esc(pg["recognize"])}</div></a>'
        for b in brands for pg in pages_by_brand[b])
    city_rows = "".join(
        f'<a href="/{c["slug"]}/"><b>{esc(c["name"])}, {esc(c["state"])}</b>'
        f'Local repair &amp; service</a>' for c in cities)
    city_sec = (f'<h2>Local service</h2><div class="brand-row sub">{city_rows}</div>'
                if cities else "")
    art_rows = "".join(
        f'<a href="/guides/{a["slug"]}/"><span class="c">{esc(a["h1"])}</span>'
        f'<div class="t">{esc(a.get("teaser",""))}</div></a>' for a in articles[:6])
    art_sec = f'<h2>Guides</h2><div class="grid">{art_rows}</div>' if articles else ""
    total = n_codes([pg for b in brands for pg in pages_by_brand[b]])
    sub = HOME_SUB.format(n=total, brands=" and ".join(brands))
    manuals = [k for k in SOURCES if not k.startswith("fda")]
    body = f"""<div class="hero"><div class="wrap">
<h1>{esc(HOME_H1)}</h1>
<p>{esc(sub)}</p>
</div></div>
<main><div class="wrap">
<div class="brand-row">{rows}</div>
<h2>Find your controller</h2>
<p>The brand on the box door usually isn't the brand talking — the alarm comes from
the refrigeration controller. Match what's on your display:</p>
<div class="grid">{ctrl}</div>
{city_sec}
{art_sec}
{cta_block()}
{sources_block(manuals, lead="Every code on this site is taken from the manufacturer's own manual:")}
</div></main>"""
    return page(HOME_TITLE, HOME_DESC, body, f"{BASE_URL}/")


# ------------------------------------------------------------ checks ---
class _Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.ids, self.title, self.text = [], set(), "", []
        self._in_title = False
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):
            self._skip += 1
        elif tag == "title":
            self._in_title = True
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip -= 1
        elif tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif not self._skip:
            self.text.append(data)


def validate(hub_paths):
    pages, errors = {}, []
    for f in sorted(OUT.rglob("index.html")):
        rel = f.parent.relative_to(OUT).as_posix()
        s = _Scan()
        s.feed(f.read_text(encoding="utf-8"))
        pages["/" if rel == "." else f"/{rel}/"] = s
    source_urls = {v["url"] for v in SOURCES.values()}
    titles, graph, words = defaultdict(list), {}, {}
    for path, s in pages.items():
        titles[s.title.strip()].append(path)
        words[path] = len(" ".join(s.text).split())
        if words[path] < MIN_WORDS:
            errors.append(f"{path}: only {words[path]} visible words (min {MIN_WORDS})")
        cited, edges = False, set()
        for href in s.links:
            if href in source_urls:
                cited = True
            if href.startswith(("http://", "https://", "mailto:", "tel:")):
                continue
            target, _, frag = href.partition("#")
            target = target or path
            if not target.startswith("/"):
                errors.append(f"{path}: relative link {href}")
            elif target in pages:
                edges.add(target)
                if frag and frag not in pages[target].ids:
                    errors.append(f"{path}: link {href} — no id '{frag}' on {target}")
            elif not (OUT / target.lstrip("/")).is_file():
                errors.append(f"{path}: broken link {href}")
        if not cited:
            errors.append(f"{path}: no primary-source citation")
        graph[path] = edges
    for title, paths in titles.items():
        if len(paths) > 1:
            errors.append(f"duplicate title {title!r}: {paths}")
    for h in hub_paths:
        if h not in pages:
            errors.append(f"brand hub {h} was not generated")
        elif h not in graph.get("/", set()):
            errors.append(f"homepage does not link brand hub {h}")
    dist = {h: 0 for h in hub_paths if h in pages}
    queue = deque(dist)
    while queue:
        cur = queue.popleft()
        for nxt in graph.get(cur, ()):
            if nxt not in dist:
                dist[nxt] = dist[cur] + 1
                queue.append(nxt)
    for path in pages:
        d = dist.get(path)
        if d is None or d > MAX_HUB_CLICKS:
            errors.append(f"{path}: {'unreachable' if d is None else d} clicks from "
                          f"the nearest brand hub (max {MAX_HUB_CLICKS})")
    return pages, words, dist, errors


def sync_redirects(anchor_of, page_of_family, generated):
    """Resolve data/redirects.json to firebase.json 301 rules (regex form —
    matches with or without the trailing slash; glob sources did not)."""
    spec = load_json("data/redirects.json", {"redirects": []})["redirects"]
    rules, errors = [], []
    for r in spec:
        src, fam, code = r["from"], r["family"], r["code"]
        stem = src.rstrip("/")
        if not re.fullmatch(r"/[a-z0-9/-]+", stem):
            errors.append(f"redirect {src}: unexpected characters")
            continue
        if src in generated:
            errors.append(f"redirect {src}: collides with a generated page")
            continue
        pg, anchor = page_of_family.get(fam), anchor_of.get((fam, code))
        if not pg or not anchor:
            errors.append(f"redirect {src}: nothing to point at for {fam} || {code}")
            continue
        dest = "/" + pg["path"] + (f"#{anchor}" if FRAGMENT_REDIRECTS else "")
        rules.append({"regex": f"^{stem}/?$", "destination": dest, "type": 301})
    fb = json.loads(FIREBASE_JSON.read_text(encoding="utf-8"))
    changed = fb["hosting"].get("redirects") != rules
    if changed:
        fb["hosting"]["redirects"] = rules
        FIREBASE_JSON.write_text(json.dumps(fb, indent=2) + "\n", encoding="utf-8")
    return rules, errors, changed


# -------------------------------------------------------------- main ---
def main():
    global NAV_HTML, FOOTER_LINKS_HTML, CITY_LINKS, FAMILIES, SUPPLEMENTS
    global SOURCES, SOURCE_BY_URL

    FAMILIES = load_json("data/families.json", {})
    SUPPLEMENTS = load_json("data/supplements.json", {})
    SOURCES = {k: v for k, v in load_json("data/sources.json", {}).items()
               if not k.startswith("_")}
    SOURCE_BY_URL = {v["url"]: v for v in SOURCES.values()}
    cfg = load_json("data/controller_pages.json")
    pages_cfg, hubs_cfg = cfg["pages"], cfg.get("hubs", {})
    brand_intros = load_json("data/brands.json", {})
    cities = load_json("data/cities.json", [])
    articles = load_json("content/articles.json", [])

    entries = []
    for f in sorted(DATA.glob("codes-*.json")):
        entries += json.loads(f.read_text(encoding="utf-8"))
    fam_entries = defaultdict(list)
    for e in entries:
        fam_entries[e["model_family"]].append(e)
        if e.get("source_url") not in SOURCE_BY_URL:
            raise SystemExit(f"{e['brand']} {e['code']}: source_url is not a "
                             f"registered primary source in data/sources.json")

    page_of_family = {}
    for pg in pages_cfg:
        for fam in pg["families"]:
            if fam in page_of_family:
                raise SystemExit(f"family {fam!r} is on two pages")
            if fam not in fam_entries:
                raise SystemExit(f"{pg['id']}: no codes for family {fam!r}")
            page_of_family[fam] = pg
        for sid in pg["sources"]:
            if sid not in SOURCES:
                raise SystemExit(f"{pg['id']}: unknown source {sid!r}")
        for t in pg.get("table_rows", []):
            if t.get("source") not in pg["sources"]:
                raise SystemExit(f"{pg['id']}: row {t['code']} must cite one of the "
                                 f"page's own sources")
    unplaced = set(fam_entries) - set(page_of_family)
    if unplaced:
        raise SystemExit(f"families with no page: {sorted(unplaced)}")
    for a in articles + cities:
        for sid in a.get("sources", []):
            if sid not in SOURCES:
                raise SystemExit(f"{a.get('slug')}: unknown source {sid!r}")

    rows_by_page = {pg["id"]: build_rows(pg, fam_entries) for pg in pages_cfg}
    anchor_of = {(r["entry"]["model_family"], r["code"]): r["anchor"]
                 for rows in rows_by_page.values() for r in rows if r["entry"]}

    brands = sorted({e["brand"] for e in entries})
    pages_by_brand = defaultdict(list)
    for pg in pages_cfg:
        pages_by_brand[pg["brand"]].append(pg)
    hub_paths = {b: f"/{slugify(b)}/" for b in brands}
    for b in brands:
        at_hub = [pg for pg in pages_by_brand[b] if "/" + pg["path"] == hub_paths[b]]
        if len(pages_by_brand[b]) == 1 and not at_hub:
            raise SystemExit(f"{b}: a brand's only controller page must live at {hub_paths[b]}")
        if len(pages_by_brand[b]) > 1 and (at_hub or b not in hubs_cfg):
            raise SystemExit(f"{b}: multi-controller brand needs hub copy and no page at the hub URL")

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
    urls = []

    def write(path, html):
        d = OUT / path.strip("/")
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(html, encoding="utf-8")
        urls.append(path)

    write("/", home_page(brands, pages_by_brand, rows_by_page, cities, articles))
    for b in brands:
        if len(pages_by_brand[b]) > 1:
            write(hub_paths[b], hub_page(b, pages_by_brand[b], rows_by_page,
                                         hubs_cfg[b], brand_intros.get(b, "")))
        for pg in pages_by_brand[b]:
            write("/" + pg["path"], controller_page(pg, rows_by_page[pg["id"]],
                                                    pages_by_brand[b], hub_paths[b]))
    for c in cities:
        write(f"/{c['slug']}/", city_page(c))
    if articles:
        write("/guides/", guides_index(articles))
        for a in articles:
            write(f"/guides/{a['slug']}/", article_page(a, articles))

    sm = "\n".join(f"<url><loc>{BASE_URL}{u}</loc><lastmod>{CONTENT_UPDATED}</lastmod></url>"
                   for u in urls)
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{sm}\n</urlset>", encoding="utf-8")
    (OUT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n", encoding="utf-8")

    # Verbatim passthrough. site/ was wiped above, so these are re-emitted every
    # build — this is what keeps the verification tokens and IndexNow key alive.
    static_files = []
    if STATIC.is_dir():
        for src in sorted(STATIC.rglob("*")):
            if src.is_file():
                dest = OUT / src.relative_to(STATIC)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
                static_files.append(dest.name)

    rules, errors, fb_changed = sync_redirects(anchor_of, page_of_family, set(urls))
    pages, words, dist, check_errors = validate(set(hub_paths.values()))
    errors += check_errors

    n_rows = sum(len(r) for r in rows_by_page.values())
    n_detail = sum(1 for rows in rows_by_page.values() for r in rows if r["entry"])
    print(f"Generated {len(urls)} pages -> {OUT} (sitemap: {len(urls)} URLs)")
    print(f"  {len(pages_cfg)} controller pages, {n_rows} table rows "
          f"({n_detail} with full sections); {len(cities)} city pages; "
          f"{len(articles)} guides")
    print(f"  {len(rules)} redirects (firebase.json "
          f"{'updated' if fb_changed else 'unchanged'})")
    print(f"  fewest words: {min(words.values())} ({min(words, key=words.get)}); "
          f"farthest from a hub: {max(dist.values())} clicks")
    if static_files:
        print(f"  static passthrough: {', '.join(static_files)}")
    if errors:
        print(f"\nBUILD CHECKS FAILED ({len(errors)}):")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print("  all checks passed: links, anchors, titles, word counts, "
          "citations, hub distance, redirects")


if __name__ == "__main__":
    main()
