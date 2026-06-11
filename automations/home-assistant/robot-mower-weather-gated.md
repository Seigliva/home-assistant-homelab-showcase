# Robot mower: every second day if dry

## Problem

A robot mower should run regularly in season, but not blindly during bad weather or while the lawn is still wet.

## Pattern

Core idea:

- Trigger at a fixed time.
- Use a date modulo check to run every second day.
- Block execution when the weather entity reports wet/bad weather.
- Track whether the run was automation-started with an `input_boolean`.
- Send completion notifications only for automation-started runs.

The full blueprint expands this into a reusable Home Assistant UI-driven automation with optional rain amount checks, wet-weather dry-out, same-day retry, stale-run alerts and stale active-run cleanup.

## Recommended version

Use the Home Assistant blueprint if you want the reusable version:

- Blueprint YAML: [`../../blueprints/automation/robot-mower-weather-gated.yaml`](../../blueprints/automation/robot-mower-weather-gated.yaml)
- Blueprint documentation: [`../../blueprints/automation/robot-mower-weather-gated.md`](../../blueprints/automation/robot-mower-weather-gated.md)

Import URL:

```text
https://github.com/Seigliva/home-assistant-homelab-showcase/blob/main/blueprints/automation/robot-mower-weather-gated.yaml
```

## Simple YAML version

The package-style YAML remains as a smaller reference implementation:

- Package-style YAML example: [`../../packages/robot-mower-weather-gated.yaml`](../../packages/robot-mower-weather-gated.yaml)

It demonstrates the basic pattern without all optional blueprint features. Keep it if you want to understand or adapt the core automation manually.

## Blueprint features

The blueprint asks for inputs in the Home Assistant UI:

- robot mower entity
- weather entity
- required active-run `input_boolean`
- start time and first eligible date
- weather states that block mowing
- optional rain amount sensor and threshold
- optional last wet-weather `input_datetime`
- optional dry-out hours after wet weather
- optional same-day retry window
- optional notification when the scheduled run is skipped
- optional notification when a delayed retry actually starts
- optional stale active-run cleanup
- optional stale-run alert if no automatic run has happened recently
- notification service and message text

## Helpers

Minimum helper:

```yaml
input_boolean:
  robot_mower_active_run:
    name: Robot Mower active run
    icon: mdi:robot-mower
```

Useful optional helpers:

```yaml
input_datetime:
  last_wet_weather_helper:
    name: Last wet weather helper
    has_date: true
    has_time: true
    icon: mdi:weather-rainy

  robot_mower_last_automatic_run:
    name: Robot Mower last automatic run
    has_date: true
    has_time: true
    icon: mdi:robot-mower-outline
```

## Tested with

Tested with a Navimow/Navimov mower via Home Assistant's `lawn_mower` domain.

It should work with other robot mowers that support `lawn_mower.start_mowing` and report `docked` when finished.
