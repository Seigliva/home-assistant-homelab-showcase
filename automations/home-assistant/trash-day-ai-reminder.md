# Trash-day reminder with short AI text

## Problem

Trash reminders are useful, but recurring reminders become noise if they are too generic.

## Pattern

- read the next collection date/type from a calendar or waste integration
- notify the evening before and/or morning of pickup
- include only the relevant bin type
- optionally generate a short, varied message with a local LLM

## Example output

> Paper and food waste tomorrow. Put the bins out before bedtime.

## Customization

Replace the calendar/sensor entity with your local waste provider integration.

## Runnable sanitized example

- [Complete package YAML](../../examples/home-assistant/trash-day-ai-reminder.yaml)
- [Installation, dependencies, replacements and safe tests](../../examples/home-assistant/README.md)

The package is the complete implementation; earlier snippets above illustrate the
pattern only. Review the documented adaptation boundaries before enabling it.
