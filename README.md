# Walk-In Cooler Code Lookup

SEO content site: one page per documented commercial ice machine error code /
fault signal. The play is to rank for **code searches** ("heatcraft al01", "dixell HA code walk in cooler") — informational queries Google serves
with plain web results, **no map pack** — instead of fighting local repair
companies on "walk in cooler repair near me."

## Who lands here

Hotel maintenance staff, restaurant managers, facility techs standing in front
of a broken machine. Highest-intent moment there is.

## How it makes money (in order of activation)

1. **CTA_PHONE** in `generate_site.py` — set a CallRail number routed to ONE
   exclusive ice machine repair company per metro (same model as the dumpster
   deal). Blank = block hidden. No fake numbers, ever.
2. **PARTS_LINK** — parts affiliate link (Parts Town etc.) on every code page.
3. Later: per-metro landing pages once a repair partner is signed.

## Files

- `data/codes.json` — the entire dataset. Every entry was verified against a
  service manual or manufacturer/service-company documentation and carries its
  `source_url`. **Never add a code without a source.**
- `generate_site.py` — static site generator, Python 3 stdlib only. Run
  `python generate_site.py`; output lands in `site/`.
- `site/` — generated output (committed so it can be deployed as-is).

## Config (top of generate_site.py)

- `BASE_URL` — placeholder until a domain is bought. Re-run the generator
  after changing it (canonicals + sitemap use it).
- `CTA_PHONE`, `PARTS_LINK` — monetization, blank by default.

## Open items

- [ ] Domain (not bought). Candidates: icemachinecodes.com, fixmyicemachine.com.
- [ ] Hosting: this repo may only deploy bigrigrescue.co (see CLAUDE.md hard
      rule) — this site needs its own Firebase target or its own repo. Decision
      needed before any deploy.
- [ ] Scotsman (brand #3) — same JSON schema, drop entries in and re-run.
- [ ] CallRail number + first exclusive repair partner (Huntsville or Nashville
      first — markets Rufus can sell in person).
