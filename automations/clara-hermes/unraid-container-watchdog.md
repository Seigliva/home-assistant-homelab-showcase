---
tags: [automation, unraid, docker, monitoring, clara]
status: living
---
# Unraid Container Watchdog

## Formål
Varsle når containere som var kjørende ved baseline stopper utenfor vedlikeholdsvindu.

## Policy
- Ikke autostart stoppede containere.
- Noen containere er bevisst stoppet/created.
- CLARA skal varsle/spørre før restart.

## Schedule
- Watchdog: hvert 5. minutt.
- Søndag 03:00–07:00: vedlikeholdsvindu, varsler undertrykkes.
- Søndag 09:00: statusrapport.

## Hermes jobs
- `Unraid container watchdog` — script `unraid_container_watchdog.py`
- `Unraid søndag 09 containerstatus` — script `unraid_container_sunday_report.sh`

## Runbook
- [[Runbooks/Unraid container down]]


## Public pattern

This is a CLARA/Hermes Agent watchdog rather than a native HA automation.

Useful design choices:

- baseline only containers that are expected to be running
- suppress alerts during a known maintenance window
- do not auto-start containers without confirmation
- send a weekly post-maintenance status report

This pattern is useful for homelabs where some stopped containers are intentionally off.
