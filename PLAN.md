# Fault-Code Directory Network — 6-Month / 3-Year Plan

Written 2026-08-23. Owner: Rufus. Three sites, one model, one shared engine.

## The model (why this isn't another map-pack fight)

Someone standing in front of a broken machine googles the code on its display:
"manitowoc e01", "hoshizaki 3 beeps", "atlas copco elektronikon error",
"walk-in cooler HA alarm". Google answers those with plain web results — no
map pack, no local incumbents. Nobody has built clean, sourced pages for most
of these codes. We catch the searcher at the highest-intent moment that exists
(equipment down, money bleeding) and route them to the money layer.

## Question-led, not directory-led (core principle, set 2026-08-23)

These are NOT regular directories. Every content page is framed as the
question a real person types, and the page is the direct answer:

- H1 and title tag ARE the question: "What does E01 mean on a Manitowoc
  Indigo NXT ice machine?", "Why is my Hoshizaki ice machine beeping
  3 times?", "Why is the red wrench light on on my Manitowoc NEO?"
- The page opens with a short answer, then earns depth: what it means,
  which machines show it (new vs old), what causes it, can you fix it
  yourself and how, and when/why it takes a technician.
- Question headings throughout + FAQPage structured data matching the
  visible content — built for People Also Ask boxes and AI answers, the
  exact real estate the map pack can't touch.
- No generic "call a technician now" buttons on content pages. City-page
  links live in prose, in context. Google punishes doorway-style CTAs;
  the money layer earns clicks by being genuinely next.
- Non-code signals get natural question phrasing (beep counts, lights,
  flashes) because that's literally what people type.

When adding brands or verticals: write the question first, then the page.

## The three sites

| Site | Brands covered | Status |
|---|---|---|
| Ice machines | Manitowoc, Hoshizaki (Scotsman later) | 117 pages built |
| Air compressors | Atlas Copco, Ingersoll Rand, Kaeser, Sullair | 134 pages built |
| Walk-in coolers | Heatcraft, KE2 Therm, Dixell, Norlake | 76 pages built |

Money markets for all three: **Nashville, TN** and **Birmingham, AL**.

## How it makes money (in order of activation)

1. **Exclusive local partner per metro per vertical** — the dumpster model.
   The city pages list real service companies today; the pitch to ONE of them:
   "I own the page your customers land on when their machine throws a code —
   want every call from it?" CallRail number + monthly fee or per-call price.
   The city-page company lists ARE the prospect list (contact info already
   researched, in `*-source/data/cities.json`).
2. **Parts affiliate** on every code page (PARTS_LINK config) — parts-buying
   intent is native to code searches.
3. **Featured placement** on city pages once traffic is provable.

## 6-month gate (fail criteria set 2026-08-23)

By 2027-02-23 the network must show:
- All three sites live on real domains, fully indexed (Search Console
  coverage report showing the code pages in the index)
- Ranking data: top-10 positions for a meaningful set of long-tail code
  queries (this is winnable; "#1 for repair nashville" is NOT the metric)
- A money path in motion: at least one signed (or actively negotiating)
  exclusive partner OR affiliate revenue > $0 OR CallRail ringing
If none of that is true at 6 months, kill it and take the lesson.

## Month-by-month

**Month 0 (now, done in this session)**
- Ice site built: 105 code pages, 6 guides, 2 city pages, 21 verified companies
- Compressor + walk-in sites: engine scaffolded, code research running

**Month 1 (Sept) — cost: ~$30-40 domains, $0 hosting**
- Buy 3 domains (short, brandable, keyword-adjacent)
- Decide hosting (new Firebase targets in a NEW project/repo per deploy-safety
  rules, or Cloudflare Pages — either is $0)
- Deploy all three; submit sitemaps in Google Search Console DAY ONE
- Request indexing on the top 20 pages per site manually

**Month 2-3 — cost: $0 plus time**
- Watch Search Console: which codes get impressions first → write 2-3 more
  guides per site targeting whatever Google is already showing us demand for
- Add Scotsman (ice) as third brand — same JSON schema, re-run generator
- Start partner conversations in whichever vertical shows impressions first,
  using Search Console screenshots as the pitch deck

**Month 4-6 — first money**
- CallRail number (~$45/mo when activated) goes live on the site with the
  most traffic; set CTA_PHONE, regenerate, redeploy
- Sign exclusive partner #1 (target: Nashville ice or Birmingham ice — the
  service companies there already sell PM contracts and know lead value)
- Parts affiliate links live (Parts Town has an affiliate program via networks)

**Year 1-3 — the compounding phase**
- More brands per site (Scotsman, Ice-O-Matic; Quincy, Gardner Denner;
  more controllers) — every brand multiplies long-tail coverage
- More metros: Memphis, Huntsville, Chattanooga, Atlanta — city pages are
  cheap once a vertical has a working partner playbook
- The 3-year asset: a network ranking for thousands of code queries with an
  exclusive partner per metro per vertical, each paying monthly. That's also
  a sellable asset — code-content sites with lead revenue have real resale
  value.

## Costs so far (this session)

- $0 cash. Research + build done in Claude Code session (subscription).
- Ongoing: $0 until domains (~$12 each) and CallRail (only when a partner
  deal justifies it).

## Hard rules carried over

- Every NEW controller/brand added gets five of its codes spot-checked
  directly against the cited primary sources before the pages count as done
  (standing rule, 2026-08-23).

- Every fault code verified against service documentation, source URL stored.
- Company listings: real businesses only, phones verified on their own sites,
  no pay-to-play claims, brokers/lead-gen fakes excluded.
- No deploys from this repo except bigrigrescue.co (deploy-safety rule) —
  these sites get their own hosting, decision pending with Rufus.
