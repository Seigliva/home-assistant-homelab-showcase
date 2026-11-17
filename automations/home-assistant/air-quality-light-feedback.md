# Air-quality feedback using lights

## Problem

Air-quality sensors are easy to ignore on dashboards.

## Pattern

Use an existing light as a subtle physical indicator:

- normal: no effect
- elevated CO₂/particles/VOC: brief warm/red pulse
- bad air: repeated smooth red blink
- recovery: optionally return to previous scene

## Example entities

```yaml
sensor.living_room_air_quality
light.living_room_status_light
```

## Why this works

Ambient feedback is more useful than phone spam for slow-moving environmental signals.

## Runnable sanitized example

- [Complete package YAML](../../examples/home-assistant/air-quality-light-feedback.yaml)
- [Installation, dependencies, replacements and safe tests](../../examples/home-assistant/README.md)

The package is the complete implementation; earlier snippets above illustrate the
pattern only. Review the documented adaptation boundaries before enabling it.
