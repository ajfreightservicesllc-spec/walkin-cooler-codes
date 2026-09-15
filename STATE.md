# STATE.md - Walk-In Cooler Codes session log

Newest at the top.

---

## 2026-09-14 (late - GA check)

- **Done:** Checked for Google Analytics. None anywhere: 0 hits for gtag / googletagmanager / G- / GTM- / UA- in the repo (generate_site.py, data, site/), and 0 on the live /, /carel/, /guides/walk-in-cooler-not-cooling/ (all HTTP 200). No other analytics either. No files changed except this log.
- **Half-finished:** nothing.
- **Next:** If Rufus sends a GA4 measurement ID (G-XXXXXXX), add the gtag snippet to the page head template in generate_site.py, rebuild, commit, hand him the deploy command.
- **Blocked / waiting on Rufus:** GA4 property + measurement ID (only he can create it). Never insert a placeholder ID.

---

## 2026-09-14 (session closed ~6:40 PM; Rufus back in the morning)

- **Done:** Read-only checks of the gsc-qc job for this site (sc-domain:walkincoolercodes.com). Only file changed in this repo: STATE.md (created today - it did not exist before).
  - **Clicks/impressions:** 0 clicks, 0 impressions this week (GSC window 2026-09-05 to 09-11) and last week. Every row since tracking began 2026-09-01 is 0/0. Report card: GRADE NEW, day 16 of 180.
  - **Fresh index sweep, 17:05-17:08** (Rufus ran `full_index_sweep.py --only sc-domain:walkincoolercodes.com`): status OK, 24 of 24 inspected. 4 indexed (/, /carel/, /guides/walk-in-cooler-maintenance-checklist/, /guides/walk-in-cooler-not-cooling/), 1 crawled-not-indexed (/guides/walk-in-freezer-ice-buildup/), 19 "URL is unknown to Google" = 17%. Change vs previous sweep: +0 (4 -> 4), won 0, lost 0. Identical to 2026-09-12. Still under the 30% publish gate (next gate check 2026-10-08).
  - Bing IndexNow on the 2 PM run: 24 URLs sent, HTTP 200 OK.
  - Live sitemap checked this session: HTTP 200, 24 URLs.
- **Failures found (gsc-qc job, not this repo):**
  - The 2026-09-13 11 PM scheduled run and a manual ~2 PM run on 09-14 both reached 14/14 and the report card read this site's sitemap fine, but the index sweep lost DNS (`getaddrinfo failed`) before reaching this site - at 00:54 and 15:27. `index_sweep_history.csv` has all-zero rows for this site on 09-13 and 09-14; those are failures, not real zeros.
  - There was NO morning run on 09-14 (Rufus thought there was). Task Scheduler "GSC Nightly QC" last ran 2026-09-13 23:00; next run 2026-09-14 23:00.
  - Cause, per `C:\gsc-qc\STATE.md` (another session; not verified by me): the PC's Wi-Fi hops between "Ruff Dogg" and "Woodspring_GUEST", and the old sweep had no retry. That session patched the job's scripts to wait out drops. Tonight's run is the first real run on the patched code.
  - The `--only` mode by design writes only `index_status_latest.csv` and `sweep_status_latest.csv`; it does not add a row to `index_sweep_history.csv` or the report files.
- **Half-finished:** nothing.
- **Next:** Morning of 2026-09-15: check that the 09-14 23:00 run worked for this site. (1) `C:\gsc-qc\reports\nightly_log.txt` tail - no "no readable sitemap" / `getaddrinfo` for walkincoolercodes. (2) `index_sweep_history.csv` has a 2026-09-15-dated walkincooler row (or 09-14 second row) with total_urls = 24, not 0. (3) `gsc_history.csv` new row - clicks/impressions for the window ~09-06 to 09-12. (4) Compare index states against today's 4 indexed / 1 rejected / 19 unknown baseline. Check file timestamps first; if not from last night, say the data may be stale.
- **Blocked / waiting on Rufus:**
  - Wi-Fi fix (his to do): plug in Ethernet, or run `netsh wlan set profileparameter name="Woodspring_GUEST" connectionmode=manual`. Not confirmed done as of session close.
  - Loose files in this repo, left untouched: `CLAUDE.md` has uncommitted edits (not made this session), and `CLAUDE.md.pre-statelog` is untracked. Needs his call whether to commit/delete.
