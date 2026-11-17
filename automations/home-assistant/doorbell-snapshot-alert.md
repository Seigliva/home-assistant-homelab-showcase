# Doorbell notification and conditional light blink

## Current pattern

UNVERIFIED SOURCE DELIVERY: observed automation is enabled but has never run (last_triggered is null); the Yale source event was still dated 2026-11-09 at the 2026-11-18 inspection. A real user press was not received. Activation and static checks are not end-to-end verification. Single mode throttles duplicates; in-flight repeats can be dropped. The snapshot is runtime-only and may override manual changes made during the brief alert.

## Copy-paste implementation

- [Complete package YAML](../../examples/home-assistant/doorbell-snapshot-alert.yaml)
- [Install, replace entities and safely test](../../examples/home-assistant/README.md)

## Dependencies

event.front_door_doorbell producing event_type ring and a timestamp state; notify.mobile_app_example_phone; person.adult_one, person.adult_two and person.child_one/child_two/child_three; binary_sensor.living_room_presence (whole-room presence, not one zone); areas office, laundry, child_one, child_two, child_three containing lights. No helpers.

## Safe test

Start with a test event entity and test lamp areas. Confirm phones notify independently of presence. Adults home plus living room explicitly clear selects already-on office/laundry lights; adults explicitly away selects already-on lights in rooms of children home. Unknown adult presence must not take the away path. Verify two slow blinks and original state restoration. Then press the physical doorbell and inspect the source event and trace.

## Privacy

All entities, areas and notification targets are generic. The example is not a
private configuration export; no credentials, hardware IDs or location data are included.
