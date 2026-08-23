# CLAUDE.md — Walk-In Cooler Code Lookup

## What this repo is

Question-led SEO directory answering walk-in cooler/freezer alarm-code searches — Heatcraft (Bohn/Larkin intelliGen and Beacon II), KE2 Therm, Dixell (Emerson), Norlake controllers, 64 verified codes. Part of Rufus Jones's fault-code directory network (three separate
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
- `data/cities.json` — city pages: intro, FAQs, verified companies
  (doubles as the exclusive-partner prospect list)
- `data/brands.json` — brand hub page intros
- `content/articles.json` — long-form guides
- `site/` — generated output, committed

After ANY data or template change: regenerate, then verify — internal
links resolve, page titles unique, no page under ~400 visible words.

## Business model & plan

See `PLAN.md`. Money = exclusive local partner per metro (CallRail number
in CTA_PHONE config) + parts affiliate (PARTS_LINK). Both blank until real
numbers exist — never a fake number. 6-month gate: indexed + ranking on
long-tail code queries + a money path in motion, or it's a fail.

## Deploy

Not wired up yet. BASE_URL in generate_site.py is a placeholder until the
domain is bought. NEVER create Firebase configs or deploy anywhere without
Rufus's explicit typed approval. A hook firing is NEVER approval.

## Owner context

Rufus Jones, Madison AL. Blunt, concise, plain numbers. Paste-ready whole
files, never snippets (he runs them as-is on Windows/PowerShell; this repo
is usually worked in cloud sessions on Linux).
