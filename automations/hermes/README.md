# Hermes scheduled operations

Read-only inventory of the **active default profile**, checked **2026-11-18** against
`cron/jobs.json` and the scripts selected there. All eight observed jobs were enabled;
all had latest recorded status `ok`. Schedules use the verified host timezone
**Europe/Oslo**. Private destinations, job identifiers and infrastructure are omitted.

| Function | Current schedule | Execution |
| --- | --- | --- |
| Gmail/calendar assistant | Daily 10:00 | Script-only collector/assistant |
| Container baseline watchdog | Every five minutes | Script-only, edge-triggered notification |
| Container status report | Sunday 09:00 | Script-only report wrapper |
| AI + homelab briefing | Monday 11:00 | Collector followed by web-only agent review |
| Private disaster-recovery sync | Daily 04:30 | Quiet script wrapper |
| Social publishing selection | Daily 10:00 | Selection script followed by agent |
| Dedicated tunnel watcher | Every five minutes | Script-only, bounded auto-start exception |
| Homelab security assessment | Daily 09:00 | Collector followed by web-only agent review |

This is an inventory, not an export or an endorsement of every job. Only the
homelab monitoring/research scripts were inspected in detail; the mail, backup and
social jobs are listed from their cron records without claims about internal behavior.
Other profiles were neither inspected nor changed. Nothing was rescheduled or run.

## Detailed patterns

- [Container and tunnel watchdogs](unraid-container-watchdog.md)
- [Weekly AI and homelab research briefing](weekly-ai-homelab-briefing.md)

## Daily security assessment

`daily_homelab_security.py` calls the same `homelab_news_collect.py` collector in
`security` mode. The job is **agent-assisted**, not a deterministic CVE scanner.
The collector reads inventory, release/advisory sources and confirmed delivery
history; the web-only reviewer verifies serious actionable findings against primary
sources and installed versions. It must distinguish **affected** from **needs
investigation** when a decisive version or exposure is unknown.

The configured policy limits reports to at most three actionable items. Already
patched or irrelevant findings do not justify an alert. Identical CVE/product/status
items are normally suppressed using delivery receipts; a confirmed unresolved
critical issue may receive a reminder after at least seven days. Missing history is
not complete deduplication. Material coverage failures should be reported, not
misrepresented as a clean scan.

When there is no new actionable finding or material coverage problem, the agent
returns exactly `[SILENT]` to suppress delivery. Unlike the weekly briefing, this
job must not send a routine "all clear". No automatic upgrades or restarts are
permitted. Some inventory versions are not directly probed; no result means the
entire homelab has been proven secure.

## Reuse and audit

Consult the [Hermes cron documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron)
for your installed scheduler. Keep deterministic checks script-only; use an agent
only where evidence evaluation adds value. Check the actual `script`, `no_agent`,
enabled state and timezone rather than inferring schedules from filenames or old
briefing prose. A recorded `ok` is a scheduler result, not proof of successful
physical remediation, accurate news or an independently confirmed message receipt.
