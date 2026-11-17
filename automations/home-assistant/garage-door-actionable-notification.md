# Garage door actionable notification

## Problem

A garage door left open should produce an actionable alert, not just noise.

## Pattern

- trigger if the door has been open for longer than a threshold
- send a notification with action buttons
- only expose a safe `close` action
- include a second confirmation or cooldown if needed

## Privacy note

The public example intentionally avoids exact security flows, camera snapshots and household presence details.

## Runnable sanitized example

- [Complete package YAML](../../examples/home-assistant/garage-door-actionable-notification.yaml)
- [Installation, dependencies, replacements and safe tests](../../examples/home-assistant/README.md)

The package is the complete implementation; earlier snippets above illustrate the
pattern only. Review the documented adaptation boundaries before enabling it.
