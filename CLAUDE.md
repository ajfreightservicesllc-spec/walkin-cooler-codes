# CLAUDE.md — Walk-In Cooler Code Lookup

## What this repo is

Question-led SEO directory answering walk-in cooler/freezer alarm-code searches — Carel (ir33, PJ Easy, PCO5+), Heatcraft (Bohn/Larkin intelliGen and Beacon II), Danfoss (AK-CC, EKC, ERC, Optyma Plus), KE2 Therm, Dixell (Emerson) and Norlake controllers: 10 controller pages carrying 218 code-table
rows, 128 of them with full verified sections. Part of Rufus Jones's fault-code directory network (three separate
repos: ice-machine-codes, air-compressor-codes, walkin-cooler-codes), but
THIS REPO IS ISOLATED — see the isolation rule below.

## ISOLATION RULE (hard rule from Rufus, 2026-08-23)

**Agents working in this repo work ONLY on this vertical.** Do not read
from, write to, copy content between, or make decisions for the other
directory repos. No cross-contamination: each site has its own data, its
own content voice, and its own agents. If a task genuinely spans sites,
stop and tell Rufus — don't reach across.

## Standing rule: 5 spot-checks per new controller (set by Rufus, 2026-08-23)

Whenever a NEW brand or controller's codes are added to this site, five of
its codes MUST be spot-checked directly against the cited primary sources
(the actual manual PDF or manufacturer page) before the pages count as
done. Record what was checked and the result in the commit message. A
research agent's citation is not verification — the spot-check is. If a
spot-check fails, the entry is corrected or removed before anything ships.

## One page per controller family (hard rule, set 2026-09-10)

Never one page per code. On 2026-09-10 the site had 145 URLs — 128 of them
per-code pages — and 0 of 10 sampled pages were indexed. They were
consolidated into 10 controller pages (full manufacturer code table, a full
section per verified code, diagnostic sequence, parts, citations) and the 128
old URLs 301 to `page#code-anchor`. Full audit: `INDEXATION_AUDIT_2026-09-10.md`.

- A new code goes onto its controller's page (a verified entry in
  `data/codes-*.json`, or a transcribed row in `data/controller_pages.json`) —
  never onto its own URL.
- A new controller gets ONE page, added to `data/controller_pages.json`.
- **Publish nothing new** (no controllers, codes, metros or guides) until
  sampled indexation exceeds 30%. First check: 2026-10-08.
- Refrigeration fundamentals (cycle, temperature control, superheat,
  subcooling, defrost, condenser, refrigerants) live ONCE, in
  `/guides/walk-in-cooler-alarm-codes-guide/`; other pages link to its
  #anchors. General compressor theory -> link https://aircompressorcodes.com/;
  ice-making -> https://icemachinecodes.com/ (root links only — the isolation
  rule still applies: never read or copy from those repos).

## Core principles (do not violate)

1. **Question-led, not directory-led.** Every content page's H1 and title
   IS the question a real person types. Write the question first, then the
   page. No generic "call a technician now" buttons on content pages —
   city links live in prose, in context.
2. **Nothing fabricated, ever.** Every fault code is verified against
   manufacturer service manuals or authorized-distributor documentation,
   with source_url stored in the data and cited on-page. Company listings
   are real businesses with phones verified on their own websites. If it
   can't be verified, it doesn't go on the site.
3. **Rich pages only.** Target 500+ visible words per content page, all of
   it real: meaning, which machines, causes, DIY verdict + steps, why a
   technician. Thin pages don't index — that lesson is already paid for.
4. **Test markets: Nashville, TN and Birmingham, AL only** until they
   prove sales. Do not add metros without Rufus's say-so.

## How the site works

- `generate_site.py` — static site generator, Python 3 stdlib only.
  Run `python generate_site.py`; output lands in `site/`.
- `data/codes-*.json` — verified fault codes (per brand)
- `data/supplements.json` — per-code causes / fixability / why-technician
  / natural-language questions (keyed "model_family||code")
- `data/families.json` — which-machines/generation context per family
- `data/controller_pages.json` — one entry per controller page: the families
  it carries, full code-table rows, diagnostic sequence, parts, sources, and
  hub copy for multi-controller brands
- `data/sources.json` — primary-source registry. Every citation resolves
  through it; a code whose source_url isn't registered fails the build
- `data/redirects.json` — the 128 retired per-code URLs. The generator turns
  them into 301 rules in `firebase.json`: never hand-edit that block, never
  delete an entry
- `data/cities.json` — city pages: intro, FAQs, verified companies
  (doubles as the exclusive-partner prospect list)
- `data/brands.json` — brand hub page intros
- `content/articles.json` — long-form guides
- `site/` — generated output, committed. **Wiped by `shutil.rmtree` on
  every build** — never store anything here that must persist.
- `static/` — **NEVER DELETE OR RENAME ANYTHING IN HERE.** Copied verbatim
  into `site/` after every build, which is the only reason its contents
  survive the wipe above. Holds TWO Google site-verification tokens, both
  required, each granting a different account:
    - `googleaf127d96642b3615.html` — account-level token shared across ALL
      of Rufus's sites.
    - `google1f5301e9b5698c58.html` — his reporting service account. The
      first token does NOT grant it access, which is why both must exist.
    - `f148878de6d84ad9ac2f3afe91086fb2.txt` — the IndexNow key. It was live
      but existed only in `site/` (wiped every build) until 2026-09-10; now
      kept here. Byte-exact, no trailing newline.
  Deleting or renaming either one un-verifies that property and cuts off the
  reporting tools behind it. They are independent — removing the "extra" one
  is never a safe cleanup. `static/` is also the durable home for any future
  verification file (Bing `BingSiteAuth.xml`, `ads.txt`).

After ANY data or template change: regenerate. The build verifies itself —
internal links and #anchors resolve, titles unique, no page under 400 visible
words, every page cites a primary source, every page within 2 clicks of a
brand hub, every redirect resolves — and exits 1 if anything fails. Never
deploy a failed build.

## Business model & plan

See `PLAN.md`. Money = exclusive local partner per metro (CallRail number
in CTA_PHONE config) + parts affiliate (PARTS_LINK). Both blank until real
numbers exist — never a fake number. 6-month gate: indexed + ranking on
long-tail code queries + a money path in motion, or it's a fail.

## Deploy

Live as of 2026-08-29. Firebase Hosting, project `aiansweragency-main`, site
`walkincooler-codes`:

```
python generate_site.py
firebase deploy --only hosting:walkincooler-codes --project aiansweragency-main
```

**BASE_URL in generate_site.py is `https://walkincoolercodes.com`** and MUST
NOT be changed unless the domain itself changes. Changing BASE_URL rewrites
every `<link rel="canonical">` tag and every URL entry in sitemap.xml at once
across every deployed page (24 as of 2026-09-10). The deploy also
publishes the 128 redirects in `firebase.json`. Do this only with deliberate intent — never as
a test, never as "resetting a placeholder", never from a stale comment in an
older project.

## Owner context

Rufus Jones, Madison AL. Blunt, concise, plain numbers. Paste-ready whole
files, never snippets (he runs them as-is on Windows/PowerShell; this repo
is usually worked in cloud sessions on Linux).
