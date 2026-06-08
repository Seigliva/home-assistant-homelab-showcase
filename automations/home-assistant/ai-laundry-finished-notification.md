# AI laundry finished notification

## Problem

A washing machine power sensor can tell when a cycle is done, but a plain notification is easy to ignore.

## Pattern

1. Detect running state from power consumption above threshold.
2. Detect finished state when power drops for a stable period.
3. Send a short friendly notification.
4. Optionally use a local LLM to vary the message text.
5. Suppress duplicate messages until the next cycle starts.

## Example helpers

```yaml
input_boolean:
  washing_machine_running:
    name: Washing machine running

input_datetime:
  washing_machine_last_finished:
    name: Washing machine last finished
```

## Privacy note

Keep person-specific notification targets and mobile device IDs out of public examples.
