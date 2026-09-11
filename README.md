# Walk-In Cooler Code Lookup

SEO content site: one page per walk-in cooler / freezer **controller family**
— the manufacturer's full code table, what each fault means, a diagnostic
sequence and the parts involved, all cited to the manufacturer's own manual.
(Until 2026-09-10 it was one page per code; see
`INDEXATION_AUDIT_2026-09-10.md` for why that changed.) The play is to rank for **code searches**
("heatcraft al01", "dixell HA code walk in cooler", "ke2 evaporator efficiency
alarm") — informational queries Google serves with plain web results, **no map
pack** — instead of fighting local repair companies on "walk in cooler repair
near me."

Live: https://walkincoolercodes.com

## Who lands here

Restaurant managers, hotel and grocery maintenance staff, facility techs
standing in front of a cooler throwing an alarm. Highest-intent moment there is.

## How it makes money (in order of activation)

1. **CTA_PHONE** in `generate_site.py` — set a CallRail number routed to ONE
   exclusive walk-in refrigeration company per metro (same model as the
   dumpster deal). Blank = block hidden. No fake numbers, ever.
2. **PARTS_LINK** — parts affiliate link (Parts Town etc.) on every controller page.
3. Later: featured placement on city pages once traffic is provable.

## What's in it

| Brand | Controller pages | Full sections | Table rows |
|---|---|---|---|
| Carel | ir33 / ir33+, PJ Easy (PJEZ) | 34 | 49 |
| Heatcraft — Bohn / Larkin | intelliGen, Beacon II | 34 | 57 |
| Danfoss | ERC 211/213/214, EKC 202 / AK-CC 210, Optyma Plus | 30 | 58 |
| KE2 Therm | Evaporator Efficiency | 12 | 17 |
| Dixell / Emerson | XR06CX / XR60CX | 12 | 15 |
| Norlake | Programmable controller | 6 | 22 |
| **Total** | **10** | **128** | **218** |

Plus 6 brand hubs (Dixell, KE2 and Norlake: the hub is the controller page),
7 long-form guides and 2 city pages (Nashville TN, Birmingham AL) listing 13
verified local companies. 24 URLs in the sitemap.

## Files

- `data/codes-*.json` — verified fault codes, one file per brand group. Every
  entry was verified against a service manual or manufacturer/authorized-
  distributor documentation and carries its `source_url`.
  **Never add a code without a source.**
- `data/supplements.json` — per-code causes / fixability / why-technician /
  natural-language question, keyed `"model_family||code"`.
- `data/families.json` — which-machines and generation context per family.
- `data/controller_pages.json` — the 10 controller pages: families carried,
  full code-table rows, diagnostic sequence, parts, sources, hub copy.
- `data/sources.json` — every primary source cited on the site.
- `data/redirects.json` — the 128 retired per-code URLs (301s are generated
  into `firebase.json`; never delete an entry).
- `data/cities.json` — city pages: intro, FAQs, verified companies. Doubles as
  the exclusive-partner prospect list.
- `data/brands.json` — brand hub page intros.
- `content/articles.json` — long-form guides (HTML bodies).
- `generate_site.py` — static site generator, Python 3 stdlib only. Run
  `python generate_site.py`; output lands in `site/`.
- `site/` — generated output (committed so it can be deployed as-is).

## Config (top of generate_site.py)

- `BASE_URL` — `https://walkincoolercodes.com`. Canonicals and the sitemap use
  it; re-run the generator after any change.
- `HOME_TITLE` / `HOME_DESC` — fixed constants, deliberately NOT built from the
  brand list. Keep the title under ~60 characters and the description under 160
  so adding a brand can never blow out the homepage title.
- `CTA_PHONE`, `PARTS_LINK` — monetization, blank by default.

## Deploy

Firebase Hosting, project `aiansweragency-main`, site `walkincooler-codes`
(hyphenated — the site ID differs from the unhyphenated domain):

```
python generate_site.py
firebase deploy --only hosting:walkincooler-codes --project aiansweragency-main
```

## Open items

- [ ] Submit sitemap in Google Search Console and request indexing on the top
      pages (Rufus does this — Search Console is off-limits to agents).
- [ ] CallRail number + first exclusive repair partner (Nashville or
      Birmingham — the two markets this site covers).
- [ ] Parts affiliate program approval, then set `PARTS_LINK`.
