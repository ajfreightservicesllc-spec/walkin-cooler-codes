# Walk-In Cooler Code Lookup

SEO content site: one page per documented walk-in cooler / freezer controller
fault code or alarm signal. The play is to rank for **code searches**
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
2. **PARTS_LINK** — parts affiliate link (Parts Town etc.) on every code page.
3. Later: featured placement on city pages once traffic is provable.

## What's in it

| Brand | Codes |
|---|---|
| Carel (ir33, PJ Easy, PCO5+) | 34 |
| Heatcraft — Bohn / Larkin (intelliGen, Beacon II) | 34 |
| Danfoss (AK-CC, EKC, ERC, Optyma Plus) | 30 |
| KE2 Therm (Evaporator Efficiency) | 12 |
| Dixell / Emerson (XR series) | 12 |
| Norlake | 6 |
| **Total** | **128** |

Plus 7 long-form guides and 2 city pages (Nashville TN, Birmingham AL) listing
13 verified local companies.

## Files

- `data/codes-*.json` — verified fault codes, one file per brand group. Every
  entry was verified against a service manual or manufacturer/authorized-
  distributor documentation and carries its `source_url`.
  **Never add a code without a source.**
- `data/supplements.json` — per-code causes / fixability / why-technician /
  natural-language question, keyed `"model_family||code"`.
- `data/families.json` — which-machines and generation context per family.
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
