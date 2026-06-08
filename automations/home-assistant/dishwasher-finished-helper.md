# Dishwasher finished helper

## Problem

Many appliances expose their own operation state, but the most reusable Home Assistant pattern is often to convert that raw state into a simple helper that dashboards, notifications and routines can depend on.

## Pattern

When the dishwasher reports `finished`, turn on a helper:

```yaml
input_boolean:
  dishwasher_finished:
    name: Dishwasher finished
    icon: mdi:dishwasher-alert
```

```yaml
alias: Dishwasher finished
triggers:
  - trigger: state
    entity_id: sensor.dishwasher_operation_state
    to: finished
conditions: []
actions:
  - action: input_boolean.turn_on
    target:
      entity_id: input_boolean.dishwasher_finished
mode: single
```

## Why this is useful

The helper becomes the stable public interface for the rest of the smart home:

- dashboard badge
- reminder notification
- kitchen display
- evening routine
- reset when the dishwasher door opens

## Extension idea

Add a second automation that resets the helper when the door opens or when someone explicitly marks it as emptied.
