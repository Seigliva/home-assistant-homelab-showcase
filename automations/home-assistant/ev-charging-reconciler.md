# Single-owner charging permission reconciler

## Current pattern

Grounded in the current reconciler: connected completed remains allowed inside the window so the car stops drawing power itself, avoiding completed/awaiting_start loops. Charge-now clears on completed/disconnected. Both toggles off release HA control without changing the switch; they do NOT mean force-off. Preheat allowance requires vehicle home, running automation, age under 40 minutes, and time before 08:15. This package does not implement preheating or price optimization. Remove competing OEM/app schedules only after understanding the desired behavior.

## Copy-paste implementation

- [Complete package YAML](../../examples/home-assistant/ev-charging-reconciler.yaml)
- [Install, replace entities and safely test](../../examples/home-assistant/README.md)

## Dependencies

sensor.charger_status using disconnected/awaiting_start/ready_to_charge/charging/completed; switch.charger_enabled; device_tracker.ev_location. Helpers included. Optional automation.ev_morning_preheat must be a real, running preheat automation exposing current/last_triggered; leave absent to disable this exception.

## Safe test

Use a test switch and charger-status sensor. Test ordinary and crossing-midnight windows, equal start/end (disabled window), disconnected, completed, charge-now, unknown status, and both masters off. No physical charging test was run for this publication.

## Privacy

All entities, areas and notification targets are generic. The example is not a
private configuration export; no credentials, hardware IDs or location data are included.
