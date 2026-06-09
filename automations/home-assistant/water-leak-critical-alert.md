# Water leak critical alert

## Problem

Water leak sensors should be treated differently from normal smart-home notifications. They are rare, high-value and should cut through noise.

## Pattern

```yaml
alias: Water leak alert
triggers:
  - trigger: state
    entity_id:
      - binary_sensor.kitchen_sink_water_leak
    to:
      - "on"
conditions: []
actions:
  - action: notify.adults
    data:
      message: Water detected under the kitchen sink. Check immediately.
      data:
        push:
          sound:
            name: alarm
            critical: 1
            volume: 1
mode: single
```

## Why this pattern works

- no time/person conditions: water alarms must fire at all times
- adult-group notification instead of one phone
- critical push sound for iOS/mobile app delivery when the event is rare but urgent
- simple `single` mode is enough because the trigger is edge-based from dry to wet

## Good additions

- repeat if still wet after 5-10 minutes
- turn on nearby lights
- show a dashboard warning
- if you have a valve integration, close the main water valve
- add a manual test script for the notification path

## Privacy note

The public example avoids exact room layout, real notification target and any camera/security details.
