# Copy-paste Home Assistant examples

Reviewed against fresh read-only live configuration on **2026-11-18**. These are
sanitized adaptations, not backups and not a claim that every example has been
physically tested. Nothing in production was changed for this publication.

## Install one package at a time

1. Back up Home Assistant. Read the feature's dependencies and caveats below.
2. Download the linked YAML, replace every external entity/topic/area, and put it
   in `/config/packages/example_name.yaml`. Do not paste an entire package into
   the automation UI. Helpers and scripts belong to their own domains.
3. Merge (do not duplicate) this into the existing `homeassistant:` section:

   ```yaml
   homeassistant:
     packages: !include_dir_named packages
   ```

4. Use Home Assistant's configuration check, then restart to load new helper
   domains. All new example automations have `initial_state: false`: they load
   **disabled**, including on subsequent restarts. Enable only the selected test
   automation in the UI. After commissioning, remove that line if you want HA to
   restore your chosen enabled state on restart. Do not install overlapping
   production and example controllers on the same actuators.
5. Replace actuators with test lights/helpers and notifications with a test phone.
   Exercise real triggers: **Run actions** skips trigger/condition checks and is
   not a safe test for event-dependent templates. Check traces and actual device
   state, not just service success. Restore test devices afterward.
6. Roll back by disabling the example, removing its package, checking config and
   restarting. Restore any affected light/device manually if a run was interrupted.

## Replacement checklist and shared dependencies

- Replace `notify.mobile_app_example_phone` with an existing notification action
  from Developer Tools → Actions. This placeholder is **not** a built-in service.
- External sensors, lights, covers, persons and media players come from your own
  integrations; confirm state names, units, features and availability.
- For bedroom/toilet, create Schedule helpers in Settings → Devices & services →
  Helpers with entity IDs `schedule.night_mode` and (bedroom) `schedule.evening_mode`.
  Set your own weekly intervals; no household schedule is exported.
- For bedroom, create a YAML legacy person group named `adults` (or substitute an
  existing home/away group). Example: `group: {adults: {entities: [person.adult_one,
  person.adult_two]}}`. Do not set `all: true`; any adult home should satisfy it.
  Persons must already be configured. The alarm entity is read-only here; replace
  it with your integration's actual disarmed/armed_home state source.
- For doorbell, replace the five **area IDs** inside its template as well as all
  person entities. Area display names alone are not sufficient. Remove unused
  child entries. Use the whole-room presence sensor, not a sub-zone.
- Internal helpers/scripts are declared inside each package; dynamic `scene.*`
  targets are created by `scene.create`, not missing static scene dependencies.
  Do not duplicate helpers that you already created in the UI; choose one owner.
- AI is optional and disabled by default. Replace `conversation.local_assistant`
  before opting in. No LLM is allowed to choose device actions here.
- Motion on actions preserve already-on brightness. Temporary alerts intentionally
  affect lights and restore snapshots; snapshots disappear on HA restart, and a
  restore can overwrite concurrent manual changes. Use separate indicator lamps
  where that conflict matters.
- Helpers without `initial` restore prior values. Enable the bedroom master and
  EV schedule intentionally; neither should be assumed on at first install.

## Coverage of the original ten documents

| Original document | Runnable implementation |
| --- | --- |
| [ai-laundry-finished-notification.md](../../automations/home-assistant/ai-laundry-finished-notification.md) | [ai-laundry-finished-notification.yaml](ai-laundry-finished-notification.yaml) |
| [air-quality-light-feedback.md](../../automations/home-assistant/air-quality-light-feedback.md) | [air-quality-light-feedback.yaml](air-quality-light-feedback.yaml) |
| [car-heater-scheduling.md](../../automations/home-assistant/car-heater-scheduling.md) | [car-heater-scheduling.yaml](car-heater-scheduling.yaml) |
| [dishwasher-finished-helper.md](../../automations/home-assistant/dishwasher-finished-helper.md) | [dishwasher-finished-helper.yaml](dishwasher-finished-helper.yaml) |
| [garage-door-actionable-notification.md](../../automations/home-assistant/garage-door-actionable-notification.md) | [garage-door-actionable-notification.yaml](garage-door-actionable-notification.yaml) |
| [media-movie-mode.md](../../automations/home-assistant/media-movie-mode.md) | [media-movie-mode.yaml](media-movie-mode.yaml) |
| [robot-mower-weather-gated.md](../../automations/home-assistant/robot-mower-weather-gated.md) | [Existing mower blueprint](../../blueprints/automation/robot-mower-weather-gated.md) |
| [smart-blinds-temperature-wind-mqtt.md](../../automations/home-assistant/smart-blinds-temperature-wind-mqtt.md) | [smart-blinds-temperature-wind-mqtt.yaml](smart-blinds-temperature-wind-mqtt.yaml) |
| [trash-day-ai-reminder.md](../../automations/home-assistant/trash-day-ai-reminder.md) | [trash-day-ai-reminder.yaml](trash-day-ai-reminder.yaml) |
| [water-leak-critical-alert.md](../../automations/home-assistant/water-leak-critical-alert.md) | [water-leak-critical-alert.yaml](water-leak-critical-alert.yaml) |

The mower uses the existing, fully parameterized blueprint rather than a second
controller. Import it, create the required active-run helper, and select your
mower/weather/notification inputs. Optional dry-out and last-run helpers, defaults
and finish confirmation are covered in its linked guide. Keep the new automation
disabled until a safe dry-run review; a real mower can move. Set finish confirmation
longer than normal mid-job charging. The older package is retained as a legacy
reference, not the recommended install. Never install both versions together.

## Validation boundary

See [reproducible offline checks and verification limits](../../docs/publication-validation.md).
The examples require your own Home Assistant configuration check and supervised
commissioning; no production device was operated for this publication.

## Package reference and safe tests

### Power-cycle detection with optional AI

- **YAML:** [ai-laundry-finished-notification.yaml](ai-laundry-finished-notification.yaml)
- **Replace / provide:** sensor.washer_power (watts); notify.mobile_app_example_phone; optional conversation.local_assistant. All four helpers are included.
- **Safe test:** Use a test power sensor: sustain above 10 W for two minutes, then below 3 W for five minutes. Expect one notification; an unknown/unavailable-to-low transition must not announce completion. Adjust thresholds to recorded cycle data, including pauses.
- **Scope / caveat:** AI is disabled by default. Service errors or empty/error responses use deterministic text; an indefinitely stalled integration can still delay the action. Threshold timers reset on restart; this example avoids false reconnect alerts but does not recover a completion missed during downtime.

### Stable dishwasher finished flag

- **YAML:** [dishwasher-finished-helper.yaml](dishwasher-finished-helper.yaml)
- **Replace / provide:** sensor.dishwasher_operation_state with run/finished states. The flag and explicit emptied button are included.
- **Safe test:** Simulate run → finished on a test sensor; verify the flag turns on. Press the included emptied button; verify it clears.
- **Scope / caveat:** The live source detects run → finished. The explicit reset button is a public adaptation; opening the door alone is not assumed to mean emptied.

### Unconditional leak notification

- **YAML:** [water-leak-critical-alert.yaml](water-leak-critical-alert.yaml)
- **Replace / provide:** binary_sensor.kitchen_water_leak; notify.mobile_app_example_phone. No helpers.
- **Safe test:** Use a test input_boolean in place of the sensor and toggle it on. Confirm actual phone receipt, sound, and platform permissions before connecting the real sensor.
- **Scope / caveat:** No occupancy, time or alarm condition suppresses the alert. iOS critical permission is required; Android high-priority transport does not guarantee a critical sound. This does not shut off water and is not a certified alarm system.

### Explicit close-only garage action

- **YAML:** [garage-door-actionable-notification.yaml](garage-door-actionable-notification.yaml)
- **Replace / provide:** cover.garage_door with genuine idempotent close support; notify.mobile_app_example_phone with Companion App action events. No helpers.
- **Safe test:** First replace cover.close_cover with persistent_notification.create and its target with test message data. Check the unique action identifier, timeout and rechecked open state. Only then perform a supervised physical test with an unobstructed doorway.
- **Scope / caveat:** Never point this at a toggle-only relay masquerading as close. Unique per-run actions reduce stale-button reuse; they are not authentication. Keep obstruction protection and restrict mobile access. The public example deliberately omits private presence/security logic.

### CO₂ pulse with exact light restoration

- **YAML:** [air-quality-light-feedback.yaml](air-quality-light-feedback.yaml)
- **Replace / provide:** sensor.living_room_co2 in ppm; RGB-capable light.air_quality_indicator. The pulse script is included; scenes are created dynamically.
- **Safe test:** On a test lamp, save its off state and then a chosen color/brightness. Cross 1200 ppm with a test sensor and verify restoration in both cases. Test the second pulse only if still above 1400 ppm after 20 minutes.
- **Scope / caveat:** Matches the observed one-pulse plus conditional reminder pattern. Each pulse takes a fresh snapshot. Runtime scenes disappear on restart; a restart/error during the pulse can prevent restore. Do not overlap alert scripts on the same lamp.

### Bounded temperature-based plug heater

- **YAML:** [car-heater-scheduling.yaml](car-heater-scheduling.yaml)
- **Replace / provide:** sensor.outdoor_temperature in Celsius; sensor.car_heater_power in watts; switch.car_heater rated for the load; binary_sensor.workday from the Workday integration. Helpers are included.
- **Safe test:** Keep automatic mode off and use a test switch first. Set departure ahead, verify the 90/60/30-minute lead bands and unconditional off outside the window. Test unavailable temperature and low power.
- **Scope / caveat:** This is the older generic plug-heater pattern, not the current vehicle climate integration. No claim that this exact package is installed. It assumes same-day morning departure (not a cross-midnight schedule), owns the plug including manual off-window use, and requires an independent hardware timeout. No calendar dependency is hidden.

### Play/pause ambience with snapshot restore

- **YAML:** [media-movie-mode.yaml](media-movie-mode.yaml)
- **Replace / provide:** media_player.living_room_tv; binary_sensor.living_room_presence; dimmable light.living_room. The snapshot flag is included.
- **Safe test:** Use a test media entity and lamp: after 22:00 and with presence on, play → pause → play → idle. Confirm the original state is captured once and restored at idle; no play action outside the gate.
- **Scope / caveat:** The live source uses app-filtered play/pause scripts after 22:00. This simplified public variant adds stop/idle restoration and omits blinds and app allowlists intentionally. It changes an already-on light by design. Runtime snapshots do not survive restart; the flag resets to avoid restoring a missing scene.

### Wind-first shading and MQTT tilt

- **YAML:** [smart-blinds-temperature-wind-mqtt.yaml](smart-blinds-temperature-wind-mqtt.yaml)
- **Replace / provide:** sensor.wind_speed in m/s; sensor.outdoor_temperature in Celsius; cover.exterior_blinds where open means safely retracted; MQTT integration and device topic/payload supporting tilt. Tilt helper included.
- **Safe test:** Use a test cover or replace actuator calls with persistent notifications. Check high wind, missing wind, the 5–7 m/s deadband and heat above 25 °C. Verify MQTT payloads on a test topic before using the motor.
- **Scope / caveat:** This is a safer public adaptation, not an exact export: numeric thresholds replace a fragile exact wind-state trigger. Unknown wind retracts rather than shades. Manufacturer limits override example thresholds; software is not a substitute for local wind safety. Disable competing comfort writers. Periodic reconciliation may repeat the safe command.

### Tomorrow-only waste reminder with optional AI

- **YAML:** [trash-day-ai-reminder.yaml](trash-day-ai-reminder.yaml)
- **Replace / provide:** sensor.paper_collection, sensor.food_collection, sensor.general_collection with numeric days_to_pickup attributes; notify.mobile_app_example_phone; optional conversation.local_assistant. AI toggle included.
- **Safe test:** Use test sensors with days_to_pickup equal to 1, 0, and missing. Only bins due tomorrow belong in the message. Test deterministic output first; then opt in to AI and check failure fallback.
- **Scope / caveat:** Public example sends at 18:30 only; the live source also has a 22:00 reminder and optional spoken delivery. AI text is not a reliable source of collection facts; keep it off if exact wording is required.

### Bedroom motion and manual precedence

- **YAML:** [bedroom-motion-manual-precedence.yaml](bedroom-motion-manual-precedence.yaml)
- **Replace / provide:** binary_sensor.bedroom_motion; light.bedroom_main (warm-white support down to 2202 K); light.bedroom_bedside (HS color); group.adults; schedule.night_mode; schedule.evening_mode; alarm_control_panel.home_alarm. Helpers and manual-control script included.
- **Safe test:** Enable the motion master explicitly. Test daylight before/after 10:00, evening, night, armed/disarmed, absent adults, already-on brightness, and ten minutes vacancy. Route remote/dashboard manual commands through script.bedroom_manual_light, with turn_on true/false and brightness. Verify manual-off night holds until night ends; releasing it must not itself turn lights on.
- **Scope / caveat:** Fresh live config differs from an older summary: daytime motion starts after 10:00 with night/evening off, adult home and alarm disarmed; evening OR night permits bedside only at 20% while disarmed and not manually blocked. Daytime uses 50%. Vacancy-off has minute recovery and no presence gate. Morning routines do not force bedroom lights on. The public script is an explicit manual-command interface, not an automatic detector of every app/remote command.

### Toilet night light only when night and armed home

- **YAML:** [toilet-night-alarm.yaml](toilet-night-alarm.yaml)
- **Replace / provide:** binary_sensor.toilet_motion; color-temperature light.toilet; schedule.night_mode; alarm_control_panel.home_alarm. Persistent input_text.toilet_before_night is included.
- **Safe test:** With a test lamp, cover all four combinations of night on/off and alarm armed_home/not armed_home. Only both true uses 10% at 2202 K. Verify an already-on lamp is untouched, ten-minute vacancy turns it off, and next normal on restores then clears stored state.
- **Scope / caveat:** Night schedule alone is not bedtime. No alarm commands are sent. This adaptation stores brightness and Kelvin, not arbitrary RGB/effects; fallback is brightness 186 and 2469 K if an off lamp does not expose previous attributes. Select a compatible lamp and tune those defaults. Do not add an initial value to the persistent helper. Vacancy timer does not survive reload.

### Doorbell notification and conditional light blink

- **YAML:** [doorbell-snapshot-alert.yaml](doorbell-snapshot-alert.yaml)
- **Replace / provide:** event.front_door_doorbell producing event_type ring and a timestamp state; notify.mobile_app_example_phone; person.adult_one, person.adult_two and person.child_one/child_two/child_three; binary_sensor.living_room_presence (whole-room presence, not one zone); areas office, laundry, child_one, child_two, child_three containing lights. No helpers.
- **Safe test:** Start with a test event entity and test lamp areas. Confirm phones notify independently of presence. Adults home plus living room explicitly clear selects already-on office/laundry lights; adults explicitly away selects already-on lights in rooms of children home. Unknown adult presence must not take the away path. Verify two slow blinks and original state restoration. Then press the physical doorbell and inspect the source event and trace.
- **Scope / caveat:** UNVERIFIED SOURCE DELIVERY: observed automation is enabled but has never run (last_triggered is null); the Yale source event was still dated 2026-11-09 at the 2026-11-18 inspection. A real user press was not received. Activation and static checks are not end-to-end verification. Single mode throttles duplicates; in-flight repeats can be dropped. The snapshot is runtime-only and may override manual changes made during the brief alert.

### Single-owner charging permission reconciler

- **YAML:** [ev-charging-reconciler.yaml](ev-charging-reconciler.yaml)
- **Replace / provide:** sensor.charger_status using disconnected/awaiting_start/ready_to_charge/charging/completed; switch.charger_enabled; device_tracker.ev_location. Helpers included. Optional automation.ev_morning_preheat must be a real, running preheat automation exposing current/last_triggered; leave absent to disable this exception.
- **Safe test:** Use a test switch and charger-status sensor. Test ordinary and crossing-midnight windows, equal start/end (disabled window), disconnected, completed, charge-now, unknown status, and both masters off. No physical charging test was run for this publication.
- **Scope / caveat:** Grounded in the current reconciler: connected completed remains allowed inside the window so the car stops drawing power itself, avoiding completed/awaiting_start loops. Charge-now clears on completed/disconnected. Both toggles off release HA control without changing the switch; they do NOT mean force-off. Preheat allowance requires vehicle home, running automation, age under 40 minutes, and time before 08:15. This package does not implement preheating or price optimization. Remove competing OEM/app schedules only after understanding the desired behavior.
