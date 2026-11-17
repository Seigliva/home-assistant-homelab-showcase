# Unraid container watchdog

Configuration and script review: **2026-11-18**, active default profile. This is a
sanitized description of the installed behavior, not a runnable export of private
SSH configuration or a promise that every container is healthy.

## Current schedules

| Job | Schedule (host timezone: Europe/Oslo) | Execution |
| --- | --- | --- |
| Baseline watchdog | Every five minutes | `unraid_container_watchdog.py`, script-only (`no_agent: true`) |
| Post-maintenance report | Sunday 09:00 | `unraid_container_sunday_report.sh`, script-only |
| Dedicated tunnel watchdog | Every five minutes | `unraid_cloudflared_tunnel_watchdog.py`, script-only |

All three jobs were enabled and their latest recorded scheduler status was `ok`
at inspection. That status is not independent proof of infrastructure health.

## Baseline watchdog

- A curated baseline contains only containers expected to run; intentionally stopped
  containers outside that baseline do not create outage alerts.
- The script queries Docker over SSH. A narrowly matched missing forced-command
  helper error falls back to Home Assistant container entities; arbitrary SSH errors
  do **not** silently take this fallback.
- Alert on an edge: a baseline container newly stops or disappears. Further checks
  of the same outage stay silent. Another newly failed container creates a new alert.
- A complete recovery produces one recovery message. There is no repeated escalation
  timer in the current implementation.
- No automatic start/restart is performed by this baseline watchdog.
- Quiet windows: **daily 05:30–06:30**, plus **Sunday 03:00–07:00**, local host time.
- Per-container expiry suppressions and an expiring manual maintenance marker are
  supported. The manual marker suppresses probing and output, including report mode.
- The weekly wrapper calls the watchdog's `report` mode. It distinguishes healthy,
  unhealthy, running-without-healthcheck, stopped, created and other states. A running
  container is not necessarily healthy; the baseline outage path only tests running.

State is persisted locally for edge detection. Normal silent stdout is intentional;
script stdout is delivered by Hermes rather than summarized by an agent. Errors may
be emitted as alert text with a successful process exit, so inspect the report itself.

## Dedicated tunnel exception

The separate tunnel watcher is explicitly an **auto-start** exception, not evidence
that the general watchdog restarts arbitrary containers. It reads one configured
Home Assistant container switch/status, waits approximately ten minutes after first
observing an unhealthy state, then requests start and reads back the running state.
It supports a read-only `--check` mode. The manual maintenance marker suppresses
both probing and restart. Unlike the baseline watchdog, this script does not contain
the recurring daily/Sunday quiet-window logic; use the explicit maintenance marker
when an intentional outage must also suppress tunnel recovery.

## Reuse safely

Choose your own baseline, SSH account/key, container entity mapping, state directory
and delivery destination. Keep those details outside public repositories. Start with
read-only probes and synthetic status fixtures; do not schedule the auto-start
exception until its scope is explicitly approved. Do not execute a production watcher
just to test documentation: it may update dedupe state or start the dedicated service.

See [current scheduled operations](README.md) for the broader inventory.
