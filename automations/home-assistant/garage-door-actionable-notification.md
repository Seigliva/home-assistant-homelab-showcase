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
