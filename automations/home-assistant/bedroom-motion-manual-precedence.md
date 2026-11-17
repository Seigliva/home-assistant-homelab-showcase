# Bedroom motion and manual precedence

## Current pattern

Fresh live config differs from an older summary: daytime motion starts after 10:00 with night/evening off, adult home and alarm disarmed; evening OR night permits bedside only at 20% while disarmed and not manually blocked. Daytime uses 50%. Vacancy-off has minute recovery and no presence gate. Morning routines do not force bedroom lights on. The public script is an explicit manual-command interface, not an automatic detector of every app/remote command.

## Copy-paste implementation

- [Complete package YAML](../../examples/home-assistant/bedroom-motion-manual-precedence.yaml)
- [Install, replace entities and safely test](../../examples/home-assistant/README.md)

## Dependencies

binary_sensor.bedroom_motion; light.bedroom_main (warm-white support down to 2202 K); light.bedroom_bedside (HS color); group.adults; schedule.night_mode; schedule.evening_mode; alarm_control_panel.home_alarm. Helpers and manual-control script included.

## Safe test

Enable the motion master explicitly. Test daylight before/after 10:00, evening, night, armed/disarmed, absent adults, already-on brightness, and ten minutes vacancy. Route remote/dashboard manual commands through script.bedroom_manual_light, with turn_on true/false and brightness. Verify manual-off night holds until night ends; releasing it must not itself turn lights on.

## Privacy

All entities, areas and notification targets are generic. The example is not a
private configuration export; no credentials, hardware IDs or location data are included.
