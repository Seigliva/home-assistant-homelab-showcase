# Home Assistant + Homelab Showcase

A curated, privacy-safe collection of practical Home Assistant and homelab automations from a Norwegian self-hosted setup.

This is not a raw backup of my Home Assistant config. It is a cleaned-up showcase of ideas, patterns and reusable examples that may help other smart-home and homelab nerds build better automations.

## Highlights

- Weather-gated robot mower automation
- AI-assisted notifications and morning routines
- Actionable Telegram/mobile notifications
- Smart blinds driven by temperature, wind and MQTT tilt control
- Laundry, dishwasher and trash-day reminders
- Air-quality light feedback
- Unraid Docker watchdog pattern
- CLARA/Hermes Agent research and operations briefings

## Stack

- Home Assistant
- Unraid Docker
- Proxmox
- Telegram/mobile notifications
- Local AI / LLM-assisted automations
- CLARA / Hermes Agent for homelab operations
- MQTT, templates, helpers and package-style YAML

## Repository structure

- `docs/` — hardware, integrations, architecture and design notes
- `automations/home-assistant/` — reusable Home Assistant automation patterns
- `automations/clara-hermes/` — CLARA/Hermes Agent side automations
- `packages/` — cleaned package-style YAML examples
- `tools/` — sanitizing/check scripts used before publishing

## Privacy model

The public repo intentionally avoids raw config dumps. Examples are anonymized and simplified where needed:

- no secrets
- no tokens
- no real notification targets
- no person-specific entity names
- no internal IP map
- no exact alarm/security details

See [SECURITY.md](SECURITY.md).

## Support

If this repo gave you ideas or saved you time, feel free to support the project:

[Buy me a coffee](buymeacoffee.com/itih_nor)
