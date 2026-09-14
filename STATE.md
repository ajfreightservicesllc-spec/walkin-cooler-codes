# STATE.md - Walk-In Cooler Codes session log

Newest at the top.

---

## 2026-09-14

- **Fresh sweep, 17:08 (Rufus ran `full_index_sweep.py --only` for this site):** status OK, 24 of 24 inspected. 4 indexed (/, /carel/, maintenance-checklist guide, not-cooling guide), 1 crawled-not-indexed (walk-in-freezer-ice-buildup guide), 19 unknown to Google = 17%. Identical to the 2026-09-12 sweep - no movement in 2 days. The `--only` run wrote no row to `index_sweep_history.csv`. Clicks/impressions not re-pulled (report card only runs nightly); last figure still 0/0.
- **Done:** Read-only check of the nightly GSC job for this site (sc-domain:walkincoolercodes.com). No files changed except creating this STATE.md (it did not exist before today).
  - Clicks/impressions: 0 clicks, 0 impressions this week (GSC window 2026-09-05 to 09-11) and last week. Every row since tracking began 2026-09-01 is 0/0.
  - Report card: GRADE NEW, day 16 of 180. Sampled indexation 1 of 16 = 6%.
  - Index status on file: 4 of 24 indexed (/, /carel/, /guides/walk-in-cooler-maintenance-checklist/, /guides/walk-in-cooler-not-cooling/), 1 crawled-not-indexed (/guides/walk-in-freezer-ice-buildup/), 19 "URL is unknown to Google". That is 17% - still under the 30% gate.
  - Bing IndexNow: 24 URLs sent, HTTP 200 OK.
- **Failure found (not ours to fix):** The full index sweep on BOTH 2026-09-13 (night) and 2026-09-14 (a daytime re-run, report 2:02 PM, sweep 3:27 PM) could not read this site's sitemap: `getaddrinfo failed` (DNS) for every site after the first two in the sweep. The sitemap itself is fine: checked live this session, HTTP 200, 24 URLs. So `index_status_latest.csv` rows for this site are carried over from the 2026-09-12 sweep (matches its 4 indexed / 19 not crawled / 1 rejected exactly) and are 2 nights stale.
- **Half-finished:** nothing.
- **Next:** After tonight's run (done ~2:45 AM), check `C:\gsc-qc\reports\index_sweep_history.csv` for a walkincooler row with total_urls = 24 (not 0). If it is 0 again, the DNS drop is recurring. Indexation gate check stays 2026-10-08.
- **Blocked / waiting on Rufus:** The gsc-qc job is his, and read-only to this repo.
- **Update later same day (5 PM):** Rufus thought a full run went through this morning. It did not: Task Scheduler last ran "GSC Nightly QC" at 2026-09-13 23:00, and the log shows only that run plus a manual one starting ~2 PM. Both reached 14/14, and the report card read this site's 24-page sitemap, but the index sweep lost DNS before reaching this site. Cause, per `C:\gsc-qc\STATE.md` (another session; not verified by me): the PC's Wi-Fi hops between two networks and the old sweep had no retry. That session patched the sweep to wait out drops and re-ran it `--only` for Huntsville Tree Removal, NOT this site. Tonight's 11 PM run is the first on the patched code.
