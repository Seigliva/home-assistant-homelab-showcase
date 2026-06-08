# Architecture overview

This setup combines Home Assistant with a small homelab operations layer.

## Core idea

Home Assistant handles real-time device state, helpers, automations and dashboards. CLARA/Hermes Agent handles higher-level operations where language, summarization or external APIs are useful.

## Pattern

1. Home Assistant owns device control and fast local automations.
2. MQTT and integrations expose state from devices and services.
3. CLARA monitors selected homelab/AI workflows on schedules.
4. Notifications go to Telegram/mobile only when action is useful.
5. Public examples are kept separate from private backup/config.

## Why split it this way?

- HA is reliable for deterministic automations.
- CLARA is useful for research summaries, config documentation and operational triage.
- Public sharing becomes safer when examples are curated instead of copied raw.
