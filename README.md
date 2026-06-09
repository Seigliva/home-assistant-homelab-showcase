# ITih — IT i hjemmet

ITih means **IT i hjemmet** — Norwegian for "IT in the home". It also sounds a little like E.T. phoning home, which fits the vibe: nerdy, practical smart-home and homelab automations that make a house feel alive.

This is not a raw backup of my Home Assistant config. It is a cleaned-up showcase of ideas, patterns and reusable examples that may help other smart-home and homelab nerds build better automations — with a little show-off energy.

## Highlights

- Weather-gated robot mower automation
- AI-assisted notifications and morning routines
- Actionable Telegram/mobile notifications
- Smart blinds driven by temperature, wind and MQTT tilt control
- Laundry, dishwasher, water-leak and trash-day reminders
- Air-quality light feedback
- Mobile-first Home Assistant dashboard patterns with anonymized screenshots/video
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
- `dashboards/` — anonymized Home Assistant dashboard patterns and screenshots
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

[Buy me a coffee](https://buymeacoffee.com/itih_nor)
