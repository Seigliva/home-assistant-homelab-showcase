# Robot mower: every second day if dry

## Problem

A robot mower should run regularly in season, but not blindly during bad weather.

## Pattern

- Trigger at a fixed time each morning.
- Use a date modulo check to run every second day.
- Block execution when the weather entity reports rain/snow-rain.
- Track whether the run was automation-started with an `input_boolean`.
- Send a completion notification only for automation-started runs.

## Files

- [`../../packages/robot-mower-weather-gated.yaml`](../../packages/robot-mower-weather-gated.yaml)

## Customization

Replace:

- `lawn_mower.robot_mower`
- `weather.home`
- `notify.family`
- start date/time
- weather states that should block mowing

## Improvement ideas

- add rain amount from the last X hours
- add soil moisture sensor
- suppress runs after manual mowing
- alert if no successful mow has happened in X days
