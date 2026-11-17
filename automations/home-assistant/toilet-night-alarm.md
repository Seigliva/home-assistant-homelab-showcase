# Toilet night light only when night and armed home

## Current pattern

Night schedule alone is not bedtime. No alarm commands are sent. This adaptation stores brightness and Kelvin, not arbitrary RGB/effects; fallback is brightness 186 and 2469 K if an off lamp does not expose previous attributes. Select a compatible lamp and tune those defaults. Do not add an initial value to the persistent helper. Vacancy timer does not survive reload.

## Copy-paste implementation

- [Complete package YAML](../../examples/home-assistant/toilet-night-alarm.yaml)
- [Install, replace entities and safely test](../../examples/home-assistant/README.md)

## Dependencies

binary_sensor.toilet_motion; color-temperature light.toilet; schedule.night_mode; alarm_control_panel.home_alarm. Persistent input_text.toilet_before_night is included.

## Safe test

With a test lamp, cover all four combinations of night on/off and alarm armed_home/not armed_home. Only both true uses 10% at 2202 K. Verify an already-on lamp is untouched, ten-minute vacancy turns it off, and next normal on restores then clears stored state.

## Privacy

All entities, areas and notification targets are generic. The example is not a
private configuration export; no credentials, hardware IDs or location data are included.
