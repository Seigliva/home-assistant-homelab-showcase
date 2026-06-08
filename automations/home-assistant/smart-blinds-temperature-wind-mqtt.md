# Smart blinds: temperature, wind and MQTT tilt control

## Problem

Blinds should help with heat management, but they should also protect themselves during high wind.

## Pattern

- close or tilt blinds when indoor/outdoor temperature is high
- open/retract blinds when wind is too high
- use MQTT for tilt/position commands where the integration exposes better control through topics
- keep wind protection as a higher-priority automation than comfort shading

## Entities to adapt

```yaml
cover.living_room_blinds
sensor.outdoor_temperature
sensor.wind_speed
```

## Notes

This is a good candidate for a Home Assistant package because it usually needs helpers, thresholds and multiple automations.
