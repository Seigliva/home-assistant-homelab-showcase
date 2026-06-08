# Car heater scheduling

## Problem

In cold climates, a car heater should run long enough before departure, but not waste energy.

## Pattern

- use workday/calendar mode to decide if a departure is expected
- adjust lead time by outdoor temperature
- use a smart plug/power sensor for control and verification
- notify only on failure or unexpected power draw

## Example variables

```yaml
sensor.outdoor_temperature
switch.car_heater
input_datetime.next_departure
binary_sensor.workday
```

## Nordic note

This is one of the most practical automations in a Norwegian winter setup.
