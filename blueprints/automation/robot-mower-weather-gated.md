# Robot mower weather-gated schedule blueprint

A Home Assistant blueprint for running a robot mower every second day, but only when weather and wet-ground checks say it is safe enough.

This is the reusable blueprint version of the robot mower pattern. The older package-style YAML example in [`../../packages/robot-mower-weather-gated.yaml`](../../packages/robot-mower-weather-gated.yaml) is kept as a simpler reference for people who prefer plain YAML.

## What this blueprint does

The blueprint can:

- start a robot mower at a fixed time every second day
- skip mowing when the weather entity reports wet/bad weather
- optionally block mowing if a rain amount sensor is above a threshold
- optionally wait for a dry-out period after the last wet-weather timestamp
- optionally retry later the same day if the scheduled run was skipped by weather or wet-ground checks
- notify when mowing starts, is skipped, starts later after retry, finishes, or has not run recently
- track whether the run was started by this automation so manual runs do not trigger finish notifications
- clean up a stale active-run helper if manual intervention or integration behavior leaves it stuck on

## Tested with

Tested with a Navimow/Navimov mower through Home Assistant's `lawn_mower` domain.

It should work with any robot mower integration that:

- exposes a `lawn_mower` entity
- supports the `lawn_mower.start_mowing` service
- reports `docked` when the mower returns or finishes

## Import URL

Use this in Home Assistant's **Import Blueprint** dialog:

```text
https://github.com/Seigliva/home-assistant-homelab-showcase/blob/main/blueprints/automation/robot-mower-weather-gated.yaml
```

## Required helper

Create one `input_boolean` helper before creating the automation:

```yaml
input_boolean:
  robot_mower_active_run:
    name: Robot Mower active run
    icon: mdi:robot-mower
```

This helper is turned on when the blueprint starts the mower and turned off when the mower returns to `docked`. It prevents completion notifications from firing after manual mower runs.

## Recommended optional helpers

### Last wet weather helper

Create an `input_datetime` if you want dry-out logic after wet weather:

```yaml
input_datetime:
  last_wet_weather_helper:
    name: Last wet weather helper
    has_date: true
    has_time: true
    icon: mdi:weather-rainy
```

When enabled, the blueprint can update this helper automatically whenever the weather entity enters a blocked wet state. It also refreshes the timestamp every 15 minutes while the weather remains wet, so the dry-out timer starts after wet weather clears.

### Last automatic run helper

Create an `input_datetime` if you want same-day retry and stale-run alerts:

```yaml
input_datetime:
  robot_mower_last_automatic_run:
    name: Robot Mower last automatic run
    has_date: true
    has_time: true
    icon: mdi:robot-mower-outline
```

This records when the blueprint last started the mower automatically. It is used to avoid repeated starts on the same day and to alert if the mower has not run for several days.

## Main inputs

| Input | Purpose |
| --- | --- |
| `Robot mower` | The `lawn_mower` entity to start and monitor. |
| `Weather entity` | Weather source used to block mowing during wet conditions. |
| `Automation active-run helper` | Required `input_boolean` for tracking automation-started runs. |
| `Start time` | Normal daily check/start time. |
| `Start date for every-second-day schedule` | First eligible mowing date. The blueprint runs on dates where days since this date is divisible by 2. |
| `Weather states that block mowing` | Weather states such as `rainy`, `pouring`, or `snowy-rainy`. |
| `Notify service` | Notification target, default `notify.family`. |

## Optional weather and wet-ground checks

| Input | Purpose |
| --- | --- |
| `Optional rain amount sensor` | Sensor representing recent rain amount, for example last 6 hours. |
| `Max rain amount allowed` | Skip if the rain amount sensor is above this value. |
| `Optional last wet weather helper` | `input_datetime` storing when wet weather was last seen. |
| `Update last wet weather helper from weather entity` | Automatically maintain the wet timestamp from the weather entity. |
| `Dry-out hours after wet weather` | Wait this many hours after the wet timestamp before mowing. |

If no optional rain sensor/helper is configured, the blueprint still works as a simple weather-state gate.

## Same-day retry

Enable **Retry later the same day** to let the blueprint try again after a weather/wet-ground skip.

Example:

```text
Start time: 09:00
Retry delay after skipped start: 3 hours
Retry until time: 16:00
```

Flow:

```text
09:00 scheduled start is blocked by wet weather
12:00 retry window opens
Every 15 minutes until 16:00: check again
If weather and dry-out checks pass: start mower and send delayed-start notification
```

Same-day retry requires the last automatic run helper so the mower does not start repeatedly on the same day.

## Notifications

The blueprint supports separate messages for:

- normal automatic start
- scheduled start skipped by weather/wet-ground checks
- delayed same-day retry start
- finished and back in dock
- stale-run alert if no automatic start has happened recently

The default notification service is:

```text
notify.family
```

Change it to your own service, for example `notify.mobile_app_phone` or a Telegram notification service.

## Stale active-run cleanup

Enable **Clean up stale active-run helper** if your mower integration sometimes leaves the active-run helper on after a manual stop/return-to-dock action or after a start command where the mower never actually leaves the dock.

Logic:

```text
If active_run_helper = on
and mower = docked
and helper has been on longer than X minutes
→ turn active_run_helper off
```

This is a safety net for manual intervention and integration edge cases.

## Simple YAML version

The package-style YAML file remains available as a simpler example:

[`../../packages/robot-mower-weather-gated.yaml`](../../packages/robot-mower-weather-gated.yaml)

Use that if you want to understand the core pattern without all optional blueprint features.

## Support

If this blueprint saved you time or gave you ideas, support is appreciated but optional:

[Buy me a coffee](https://buymeacoffee.com/itih_nor)
