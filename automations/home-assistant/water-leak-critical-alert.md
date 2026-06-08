# Water leak critical alert

## Problem

Water leak sensors should be treated differently from normal smart-home notifications. They are rare, high-value and should cut through noise.

## Pattern

```yaml
alias: Water leak alert
triggers:
  - trigger: state
    entity_id: binary_sensor.kitchen_sink_water_leak
    to: "on"
conditions: []
actions:
  - action: notify.family
    data:
      title: Water leak detected
      message: Water detected under the kitchen sink. Check immediately.
mode: single
```

## Good additions

- send to all adults, not only one device
- repeat if still wet after 5-10 minutes
- turn on nearby lights
- show a dashboard warning
- if you have a valve integration, close the main water valve

## Privacy note

The public example avoids exact room layout, real notification target and any camera/security details.
