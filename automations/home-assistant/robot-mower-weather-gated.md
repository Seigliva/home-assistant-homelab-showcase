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

- Package-style YAML example: [`../../packages/robot-mower-weather-gated.yaml`](../../packages/robot-mower-weather-gated.yaml)
- Blueprint version: [`../../blueprints/automation/robot-mower-weather-gated.yaml`](../../blueprints/automation/robot-mower-weather-gated.yaml)

## Blueprint version

The blueprint version turns this into a reusable Home Assistant automation. It keeps the same pattern, but asks for inputs in the UI:

- robot mower entity
- weather entity
- `input_boolean` helper for automation-started runs
- start time and first eligible date
- weather states that block mowing
- notification service and messages

Create the helper first, for example `input_boolean.robot_mower_active_run`, then import the blueprint and create an automation from it.

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
