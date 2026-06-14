# AI Greeting Generator blueprint

A Home Assistant blueprint for generating short AI-written greetings and storing them in an `input_text` helper for dashboards, wall tablets, morning routines, or notification flows.

The blueprint is designed for local LLM setups such as Ollama through Home Assistant's Conversation integration, but it also works with cloud-backed Conversation agents that support `conversation.process`.

## What this blueprint does

The blueprint can:

- run on a configurable hourly pattern, for example every hour or every second hour
- limit generation to an active time window, for example 07:00–23:00
- use any Home Assistant Conversation agent selected in the UI
- generate greetings in a flexible free-text language or locale, such as `Norwegian`, `English`, `Nynorsk`, `Spanish`, `de`, or `sv`
- adjust the audience, tone, maximum word count, and emoji use
- add optional extra prompt instructions for household style or dashboard context
- clean up the AI response by trimming whitespace, quote marks, and excessive length
- fall back to a static message if the AI returns an empty response
- optionally write debug details to the Home Assistant system log

## Tested with

Tested locally with a Home Assistant Conversation agent backed by a local Ollama LLM.

It should work with any Conversation agent that:

- appears in Home Assistant's Conversation agent selector
- supports the `conversation.process` action
- returns speech text under the standard Conversation response object

## Import URL

Use this in Home Assistant's **Import Blueprint** dialog:

```text
https://github.com/Seigliva/home-assistant-homelab-showcase/blob/main/blueprints/automation/ai-greeting-generator.yaml
```

## Required helper

Create one `input_text` helper before creating the automation:

```yaml
input_text:
  ai_greeting:
    name: AI greeting
    max: 120
    icon: mdi:robot-happy-outline
```

The blueprint writes the final greeting into this helper. You can then show it on a dashboard card, use it in another automation, or include it in notifications/TTS.

## Main inputs

| Input | Purpose |
| --- | --- |
| `Hour pattern` | Time pattern for generation. `/1` means every hour, `/2` every second hour, `8` daily at 08:00. |
| `Active after` / `Active before` | Time window where generation is allowed. |
| `Conversation agent` | Local or cloud Conversation agent used to generate the greeting. |
| `Greeting language` | Free-text language or locale for the output greeting. |
| `Audience` | Who the greeting is for, for example `the family`, `kids`, or `guests`. |
| `Base tone` | Style guidance such as warm, playful, calm, motivating, or funny. |
| `Maximum words` | Hard word-count trim applied after the AI response. |
| `Allow emoji` | Allows or blocks emoji in the generated greeting. |
| `Extra instructions` | Optional extra prompt rules for the household, display, or situation. |
| `Greeting input_text helper` | Target helper that receives the greeting. |
| `Fallback message` | Used if the AI response is empty. |
| `Write AI response to the system log` | Enables debug logging. |

## Language handling

The blueprint UI is in English, but the generated greeting language is configurable per automation.

The `Greeting language` input accepts free text. Common values are normalized for the Conversation service:

| Input examples | Conversation language code |
| --- | --- |
| `Norwegian`, `Norsk`, `Bokmål`, `Nynorsk`, `no`, `nb`, `nn` | `no` |
| `English`, `en` | `en` |
| `Spanish`, `Español`, `es` | `es` |
| `German`, `Deutsch`, `de` | `de` |
| `French`, `Français`, `fr` | `fr` |
| `Danish`, `Dansk`, `da` | `da` |
| `Swedish`, `Svenska`, `sv` | `sv` |

The full language or locale text is also included in the prompt, so values like `Nynorsk`, `British English`, or `Norwegian Bokmål` can still influence the model even when the service receives a short language code.

## Example configuration

```yaml
use_blueprint:
  path: Seigliva/home-assistant-homelab-showcase/ai-greeting-generator.yaml
  input:
    hours_pattern: /1
    active_after: "07:00:00"
    active_before: "23:00:00"
    conversation_agent: conversation.local_ollama
    language: Norwegian
    audience: the family
    tone: warm, natural, positive, and slightly personal
    max_words: 6
    allow_emoji: true
    extra_instructions: Suitable for a home dashboard. Avoid sounding corporate.
    greeting_text_entity: input_text.ai_greeting
    fallback_message: Have a great day 😊
    debug_log: false
```

## Dashboard idea

A simple Mushroom/template card can show the current greeting:

```yaml
type: markdown
content: |
  ## {{ states('input_text.ai_greeting') }}
```

You can also combine the helper with a weather card, family calendar, chore reminders, or a wall-tablet morning view.

## Notes and pitfalls

- Keep the active time window reasonable so the LLM is not called overnight.
- Local LLMs may occasionally ignore word count; the blueprint trims the final output to the configured maximum.
- If the output language is wrong, make the language more explicit, for example `Norwegian Bokmål` instead of `Norwegian`.
- Enable debug logging only while tuning the prompt, because it writes prompt and response details to the system log.

## Support

If this blueprint saved you time or gave you ideas, support is appreciated but optional:

[Buy me a coffee](https://buymeacoffee.com/itih_nor)
