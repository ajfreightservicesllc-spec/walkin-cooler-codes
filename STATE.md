# STATE.md - Walk-In Cooler Codes session log

Newest at the top.

---

## 2026-09-14

- **Done:** Read-only check of the nightly GSC job for this site (sc-domain:walkincoolercodes.com). No files changed except creating this STATE.md (it did not exist before today).
  - Clicks/impressions: 0 clicks, 0 impressions this week (GSC window 2026-09-05 to 09-11) and last week. Every row since tracking began 2026-09-01 is 0/0.
  - Report card: GRADE NEW, day 16 of 180. Sampled indexation 1 of 16 = 6%.
  - Index status on file: 4 of 24 indexed (/, /carel/, /guides/walk-in-cooler-maintenance-checklist/, /guides/walk-in-cooler-not-cooling/), 1 crawled-not-indexed (/guides/walk-in-freezer-ice-buildup/), 19 "URL is unknown to Google". That is 17% - still under the 30% gate.
  - Bing IndexNow: 24 URLs sent, HTTP 200 OK.
- **Failure found (not ours to fix):** The full index sweep on BOTH 2026-09-13 (night) and 2026-09-14 (a daytime re-run, report 2:02 PM, sweep 3:27 PM) could not read this site's sitemap: `getaddrinfo failed` (DNS) for every site after the first two in the sweep. The sitemap itself is fine: checked live this session, HTTP 200, 24 URLs. So `index_status_latest.csv` rows for this site are carried over from the 2026-09-12 sweep (matches its 4 indexed / 19 not crawled / 1 rejected exactly) and are 2 nights stale.
- **Half-finished:** nothing.
- **Next:** After tonight's run (done ~2:45 AM), check `C:\gsc-qc\reports\index_sweep_history.csv` for a walkincooler row with total_urls = 24 (not 0). If it is 0 again, the DNS drop is recurring. Indexation gate check stays 2026-10-08.
- **Blocked / waiting on Rufus:** The gsc-qc job is his, and read-only to this repo. If the sweep keeps losing DNS partway through, he needs to fix it. Not verified why it happens.
