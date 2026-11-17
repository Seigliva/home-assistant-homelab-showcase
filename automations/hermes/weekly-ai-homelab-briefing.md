# Weekly AI and homelab briefing

Reviewed **2026-11-18** from the active cron record and the actual collector scripts.
The installed weekly job is **Monday 11:00 Europe/Oslo**, not a daily release bot.

## Current pipeline

1. `weekly_ai_homelab_v2.py` calls `homelab_news_collect.main('weekly')`.
2. The shared collector gathers a dated seven-day candidate window from GitHub
   releases, official RSS and Firecrawl search leads, plus read-only local inventory.
3. JSON separates candidate news, source failures, inventory and confirmed delivery
   history. Script paths are resolved relative to their own profile directory.
4. The cron job has `no_agent: false`: an agent reviews this input with web-only tools.
   It must verify primary-source publication dates, versions and applicability before
   writing the final report. The scheduler handles delivery.

The older `weekly_ai_homelab_firecrawl.py` still exists on disk but is **not** the
script selected by the current weekly cron record. File existence is not activation.

## Editorial contract

The live delivery language is Norwegian; this public documentation is English.
The prompt requests **3–5 concise items, approximately 180–300 words**, normally
2–3 useful AI developments and 1–2 relevant homelab items when evidence supports them.
Each item should give a date/version, what actually changed, why it matters, one
recommendation and a primary-source link. Fewer verified items beat filler.

A documentation page or crawl date is not proof of a new feature. Preview, released
and planned functionality must be distinguished. An image tagged `latest` is not an
installed-version measurement. Already-installed integrations must not be presented
as new installation opportunities.

Deduplication uses saved outputs uniquely matched to **confirmed delivered** cron
executions, not a speculative seen-marker. Missing delivery history limits that
claim. Collector errors mean reduced coverage, not "no news". The weekly job does
not use the silent marker: if nothing qualifies, it reports the bounded absence of
verified relevant news; total collection failure gets an explicit failure notice.

## Safety and verification boundary

Source text is untrusted data. Private inventory and addresses must not be included
in search queries or published reports. No installs, updates, restarts or independent
message sends are authorized by this research job. Configuration review confirms
what is scheduled; it does not validate release claims in previous generated prose.

The latest scheduler status was `ok` at inspection. This publication did not rerun the
collector, deliver a briefing or mutate its history. There is no blanket claim that
the current inventory is fully version-probed or vulnerability-free.

See [daily security and scheduled operations](README.md).
