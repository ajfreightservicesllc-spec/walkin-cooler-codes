# Indexation audit and consolidation: walkincoolercodes.com

Date: 2026-09-10 (day 12 of the 180-day clock). Scope: this repo only.

## Finding

- 145 URLs in the sitemap. 0 clicks and 0 impressions for the week ending 2026-09-07. 0 of 10 sampled pages indexed.
- **128 of the 145 URLs were one page per code**: the same controller page repeated with one variable changed (the alarm code). That's the same shape diagnosed on the sibling ice-machine site, where the hubs indexed and the deep per-symptom pages did not.

## Step 2: every one-variable page group (all 128 retired)

| # | Brand | Controller family | Pages | Variable | Old URL pattern | Now |
|---|---|---|---|---|---|---|
| 1 | Carel | ir33 / ir33+ | 20 | alarm code | `/carel/ir33-ir33-{code}/` | `/carel/ir33-alarm-codes/` |
| 2 | Carel | PJ Easy (PJEZ) | 14 | alarm code | `/carel/pj-easy-pjez-{code}/` | `/carel/pj-easy-alarm-codes/` |
| 3 | Danfoss | ERC 211/213/214 | 12 | alarm / error code | `/danfoss/erc-211-213-214-{code}/` | `/danfoss/erc-211-213-214-alarm-codes/` |
| 4 | Danfoss | EKC 202 / AK-CC 210 | 8 | alarm / error code | `/danfoss/ekc-202-ak-cc-210-{code}/` | `/danfoss/ekc-202-ak-cc-210-alarm-codes/` |
| 5 | Danfoss | AK-CC 210 (was labelled "AK-CC 210/250") | 4 | alarm / error code | `/danfoss/ak-cc-210-250-{code}/` | same page as #4 |
| 6 | Danfoss | Optyma Plus | 6 | alarm code | `/danfoss/optyma-plus-condensing-unit-controller-{code}/` | `/danfoss/optyma-plus-alarm-codes/` |
| 7 | Heatcraft | intelliGen iF/iRC | 20 | AL / ER / IN code | `/heatcraft-bohn-larkin/intelligen-if-irc-controller-{code}/` | `/heatcraft-bohn-larkin/intelligen-alarm-codes/` |
| 8 | Heatcraft | Beacon II system | 11 | alarm / error code | `/heatcraft-bohn-larkin/beacon-ii-refrigeration-system-{code}/` | `/heatcraft-bohn-larkin/beacon-ii-alarm-codes/` |
| 9 | Heatcraft | Beacon II Smart Controller | 3 | display message | `/heatcraft-bohn-larkin/beacon-ii-smart-controller-lcd-display-module-{msg}/` | same page as #8 |
| 10 | Dixell | XR06CX / XR60CX | 8 | alarm code | `/dixell-emerson/xr-series-xr06cx-xr60cx-{code}/` | `/dixell-emerson/` |
| 11 | Dixell | XR60CX | 4 | alarm code | `/dixell-emerson/xr-series-xr60cx-{code}/` | `/dixell-emerson/` |
| 12 | KE2 Therm | Evaporator Efficiency | 12 | alarm name | `/ke2-therm/ke2-evaporator-efficiency-{alarm}/` | `/ke2-therm/` |
| 13 | Norlake | Programmable controller | 6 | alarm name | `/norlake/programmable-controller-carel-pco5-based-walk-in-control-panel-{alarm}/` | `/norlake/` |
| | | **Total** | **128** | | | **10 controller pages** |

**Checked and kept (not one-variable groups):**
- **7 guides.** Each answers a different question: not cooling, running constantly, ice buildup, water on the floor, how cold, maintenance, alarm codes.
- **2 city pages.** Nashville and Birmingham have different intros, FAQs and company lists, not a city-name swap.
- **Brand hubs, homepage and guides index.**
- **No temperature-threshold or defrost-state variants** existed outside the code pages.

## What changed

- **Sitemap: 145 → 24 URLs** (home, 6 brand hubs, 7 controller pages, guides index, 7 guides, 2 cities). Dixell, KE2 and Norlake each have one controller, so their hub *is* the full controller page.
- **128 retired URLs 301 to `page#code-anchor`**, so an old link lands on the exact code. The rules are regex (matches with or without the trailing slash) and are generated into `firebase.json` from `data/redirects.json`.
- **Each controller page has:**
  - the manufacturer's full code table (218 rows in total: 128 with full sections, 90 transcribed from the manual's table)
  - what each fault means
  - a diagnostic sequence and a parts table, both drawn from the manual
  - primary-source citations
- **Refrigeration fundamentals** are written once, in `/guides/walk-in-cooler-alarm-codes-guide/`, with anchors `#refrigeration-cycle #temperature-control #superheat #subcooling #defrost #condenser #refrigerants`. Controller pages link into them.
- **Sister-site links** (root URLs only; nothing read from or copied from those repos):
  - aircompressorcodes.com for general compressor theory
  - icemachinecodes.com for ice-making
- **The build now fails** if any of these hold:
  - a broken link or anchor
  - a duplicate title
  - a page under 400 words
  - a page without a primary-source citation
  - a page more than 2 clicks from a brand hub
  - a code sourced to an unregistered URL
  - a redirect that doesn't resolve

## Citation audit (step 5)

- **All 16 original source URLs resolved** (HTTP 200, real PDF) on 2026-09-10.
- **All 128 codes were checked against the manual they cite:**
  - 123 found by exact match.
  - 5 confirmed by hand: KE2 "No display", T1–T4 SENSOR and COMMUNICATION ERROR; Beacon II A2/A4, which the PDF prints as "A 2"/"A 4".
- **49 codes re-pointed to primary copies hosted by the manufacturer:**

  | Codes | New source | Replaced |
  |---|---|---|
  | ir33 (20) | Carel's English ir33+ user manual (+0300028EN) | a French/German VCC supplement and a cabinet maker's copy |
  | PJ Easy (14) | Carel's easy/PJEZ user manual (+030220791) | a New Zealand dealer guide and an Easy Freeze (PZD) sheet — a different model line |
  | ERC (12) | Danfoss's ERC 21X series user guide | two guides covering only the ERC 211 and 214 — nothing covered the 213 |
  | Beacon II Smart Controller (3) | Heatcraft-hosted H-IM-80F | a Parts Town copy |

- **KE2 stays on krack.com.** It's KE2's own Q.1.17 document; KE2's own URL returned a web page, not the PDF.
- **Data errors found against the manuals and fixed:**
  1. Carel ir33 E2 said "E3/E4 = probes S4/S5". The manual lists E3 = probe S4 and has no E4.
  2. "AK-CC 210/250": the cited Danfoss manual covers the AK-CC 210 only. The 250 claim is removed.
  3. The PJ Easy door code is "dOr" per Carel, not "dOR". The "'dr' on some models" note appears in no manual and is removed.
- **Sources added:**
  - Heatcraft Unit Coolers IOM (H-IM-UC) and Condensing Units IOM (H-IM-CU)
  - Danfoss ERC 211 and ERC 214 installation guides
  - FDA Food Code 2022, §3-501.16(A)(2) (41°F) and §3-501.19 (4 hours)

  That makes **18 sources, all resolving.**
- **Deliberately not cited:** the USDA FSIS freezing page. It blocks automated fetches, so it couldn't be verified.

## Reachability (step 6)

The homepage links all 6 brand hubs, and every page is within 2 clicks of a brand hub. The build checks both.

## Verification

- **Local `firebase serve`:**
  - 256 of 256 old-URL variants (with and without the trailing slash) return 301 to the correct `page#anchor`.
  - 24 of 24 new URLs return 200.
  - Both Google verification tokens and the IndexNow key serve unchanged.
- **Live:** see the commit message and the decisions log for 2026-09-10.

## Acceptance criteria

| Criterion | Status |
|---|---|
| Sitemap URL count down from 145 | 24 — met |
| Every page carries a resolvable primary-source citation | Met, and the build enforces it |
| Sampled indexation above 30% within 4 weeks | Check on **2026-10-08** |
| At least 10 distinct pages receiving impressions | Check on 2026-10-08 in Search Console, Performance → Pages |

Until sampled indexation passes 30%: **publish nothing new** (no new controllers, codes, metros or guides).
