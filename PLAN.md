# Walk-In Cooler Code Lookup — 6-Month / 3-Year Plan

Written 2026-08-23. Owner: Rufus. Scope: **this site only.**

> This repo documents walkincoolercodes.com and nothing else. Per the isolation
> rule in CLAUDE.md, the network-level plan covering the sibling directory sites
> lives outside this repo — do not re-add it here.

## The model (why this isn't another map-pack fight)

Someone standing in front of a walk-in throwing an alarm googles what's on the
display: "heatcraft al01", "dixell HA code walk in cooler", "ke2 ext alarm",
"norlake defrost fault". Google answers those with plain web results — no map
pack, no local incumbents. Nobody has built clean, sourced pages for most of
these codes. We catch the searcher at the highest-intent moment that exists
(box down, product warming, money bleeding) and route them to the money layer.

## Question-led, not directory-led (core principle, set 2026-08-23)

This is NOT a regular directory. Every content page is framed as the question a
real person types, and the page is the direct answer:

- H1 and title tag ARE the question. Live examples from this site:
  "What does A1 mean on a Heatcraft (Bohn/Larkin) Beacon II refrigeration
  system walk-in cooler?", "Why does my KE2 controller say EXT ALARM?",
  "What does EA mean on a Dixell (Emerson) XR-series?"
- The page opens with a short answer, then earns depth: what it means, which
  units show it (new vs old), what causes it, can you fix it yourself and how,
  and when/why it takes a technician.
- Question headings throughout + FAQPage structured data matching the visible
  content — built for People Also Ask boxes and AI answers, the exact real
  estate the map pack can't touch.
- No generic "call a technician now" buttons on content pages. City-page links
  live in prose, in context. Google punishes doorway-style CTAs; the money
  layer earns clicks by being genuinely next.
- Non-code signals get natural question phrasing (alarm relays, lights, display
  states) because that's literally what people type.

When adding brands: write the question first, then the page.

## What's built (as of 2026-08-29)

| | |
|---|---|
| Verified fault codes | **128** |
| Brands | Carel 34, Heatcraft (Bohn/Larkin) 34, Danfoss 30, KE2 Therm 12, Dixell (Emerson) 12, Norlake 6 |
| Generated files | **147** (145 URLs in sitemap.xml, plus robots.txt) |
| Brand hubs / city pages / guides | 6 / 2 / 7 |
| Verified local companies | 13 (Nashville 7, Birmingham 6) |
| Live | https://walkincoolercodes.com — deployed 2026-08-29 |

Money markets: **Nashville, TN** and **Birmingham, AL**. No new metros without
Rufus's say-so.

## How it makes money (in order of activation)

1. **Exclusive local partner per metro** — the dumpster model. The city pages
   list real service companies today; the pitch to ONE of them: "I own the page
   your customers land on when their cooler throws a code — want every call
   from it?" CallRail number + monthly fee or per-call price. The city-page
   company lists ARE the prospect list (contact info already researched in
   `data/cities.json`).
2. **Parts affiliate** on every code page (PARTS_LINK config) — parts-buying
   intent is native to code searches.
3. **Featured placement** on city pages once traffic is provable.

Both CTA_PHONE and PARTS_LINK stay blank until real numbers exist. Never a fake
number.

## 6-month gate (fail criteria set 2026-08-23)

By 2027-02-23 this site must show:
- Live on its real domain, fully indexed (Search Console coverage report
  showing the code pages in the index)
- Ranking data: top-10 positions for a meaningful set of long-tail code
  queries (this is winnable; "#1 for walk in cooler repair nashville" is NOT
  the metric)
- A money path in motion: at least one signed (or actively negotiating)
  exclusive partner OR affiliate revenue > $0 OR CallRail ringing

If none of that is true at 6 months, kill it and take the lesson.

## Month-by-month

**Month 0 (done)**
- 128 code pages, 6 brand hubs, 7 guides, 2 city pages, 13 verified companies
- Domain live, Firebase Hosting deployed 2026-08-29

**Month 1 (Sept) — cost: $0 hosting**
- Submit sitemap in Google Search Console; request indexing on the top 20 pages
  manually (Rufus does this — Search Console is off-limits to agents)

**Month 2-3 — cost: $0 plus time**
- Watch Search Console: which codes get impressions first → write 2-3 more
  guides targeting whatever Google already shows demand for
- Add the next controller brand — same JSON schema, re-run the generator
- Start partner conversations in whichever metro shows impressions first,
  using Search Console screenshots as the pitch deck

**Month 4-6 — first money**
- CallRail number (~$45/mo when activated) goes live; set CTA_PHONE,
  regenerate, redeploy
- Sign exclusive partner #1 (Nashville or Birmingham — the refrigeration
  companies there already sell PM contracts and know lead value)
- Parts affiliate links live (Parts Town has an affiliate program via networks)

**Year 1-3 — the compounding phase**
- More controller brands — every brand multiplies long-tail coverage
- More metros: Memphis, Huntsville, Chattanooga, Atlanta — city pages are cheap
  once there's a working partner playbook
- The 3-year asset: a site ranking for thousands of code queries with an
  exclusive partner per metro, each paying monthly. Code-content sites with
  lead revenue have real resale value.

## Costs so far

- $0 cash beyond the domain. Research + build done in Claude Code sessions
  (subscription). Hosting $0 on the existing Firebase project.
- Ongoing: $0 until CallRail (only when a partner deal justifies it).

## Hard rules

- Every NEW controller/brand added gets five of its codes spot-checked directly
  against the cited primary sources before the pages count as done (standing
  rule, 2026-08-23). A research agent's citation is not verification.
- Every fault code verified against service documentation, source URL stored.
- Company listings: real businesses only, phones verified on their own sites,
  no pay-to-play claims, no unverified claims about what a company services,
  brokers/lead-gen fakes excluded.
- Homepage title and meta description are fixed constants, never built from the
  brand list — see HOME_TITLE / HOME_DESC in generate_site.py.
- Deploys go to Firebase project `aiansweragency-main`, hosting site
  `walkincooler-codes`. Never deploy anywhere else without Rufus's explicit
  typed approval.
