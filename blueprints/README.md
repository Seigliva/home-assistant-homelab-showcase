# Home Assistant blueprints

Reusable blueprint versions of selected Home Assistant automation patterns from ITih.

Blueprints are the easiest way to reuse these patterns because Home Assistant exposes the important choices as UI inputs instead of requiring you to edit YAML by hand.

## Automation blueprints

### AI Greeting Generator

- Blueprint: [`automation/ai-greeting-generator.yaml`](automation/ai-greeting-generator.yaml)
- Details: [`automation/ai-greeting-generator.md`](automation/ai-greeting-generator.md)

A local-LLM-friendly greeting generator that writes short AI messages into an `input_text` helper for dashboards, wall tablets, notifications, or routines.

What you get:

- configurable schedule and active time window
- selectable Home Assistant Conversation agent
- flexible free-text output language/locale
- configurable audience, tone, word limit, emoji use, and extra prompt instructions
- fallback message if the AI response is empty
- optional debug logging while tuning prompts

### Robot mower — weather-gated every-second-day mowing

- Blueprint: [`automation/robot-mower-weather-gated.yaml`](automation/robot-mower-weather-gated.yaml)
- Details: [`automation/robot-mower-weather-gated.md`](automation/robot-mower-weather-gated.md)

A robot mower schedule that runs every second day only when conditions are safe enough.

What you get:

- fixed start time with every-second-day scheduling
- weather-state blocking, e.g. rain or snow-rain
- optional rain amount threshold
- optional wet-weather dry-out cooldown using an `input_datetime`
- optional same-day retry after a weather/wet-ground skip
- notifications when the mower starts, is skipped, starts later after retry, finishes after a confirmed docked period, or has not run recently
- `input_boolean` tracking so finish notifications only fire for automation-started runs
- confirmed finish detection for mowers that dock temporarily to recharge before continuing

Tested with a Navimow/Navimov mower through Home Assistant's `lawn_mower` domain. It should work with other robot mowers that support `lawn_mower.start_mowing` and report `docked` when finished.

## Importing from GitHub

In Home Assistant:

1. Go to **Settings → Automations & scenes → Blueprints**.
2. Select **Import Blueprint**.
3. Paste the GitHub URL for the blueprint file.
4. Create an automation from it and fill in the inputs.

Robot mower import URL:

```text
https://github.com/Seigliva/home-assistant-homelab-showcase/blob/main/blueprints/automation/robot-mower-weather-gated.yaml
```

AI Greeting Generator import URL:

```text
https://github.com/Seigliva/home-assistant-homelab-showcase/blob/main/blueprints/automation/ai-greeting-generator.yaml
```

## Companion docs

Each published blueprint should have a short companion document next to the YAML file. The YAML is what Home Assistant imports; the companion doc explains what the blueprint does, which helpers to create, and what the optional features are for.

## Support

If a blueprint saves you time or gives you ideas, support is appreciated but never required:

[Buy me a coffee](https://buymeacoffee.com/itih_nor)
