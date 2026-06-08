---
tags: [automation, clara, research, ai, homelab]
status: living
---
# CLARA Research Briefing

## Formål
Gi kort ukentlig briefing om AI, AI-agenter, Hermes Agent, praktiske integrasjoner og homelab/Home Assistant-muligheter.

## Schedule
- Mandag 11:00 Europe/Oslo.

## Stil
- Norsk.
- Konsist: 3–5 linjer.
- Lenker bare når nyttig.

## Datakilde
- Firecrawl API via CLARA miljøvariabler.

## Hermes job
- `Ukentlig AI + homelab-briefing`
- Script: `weekly_ai_homelab_firecrawl.py`


## Public pattern

A scheduled agent job collects web/research snippets and turns them into a very short, practical briefing.

Good constraints:

- 3-5 lines only
- practical recommendations, not hype
- links only when useful
- no notification if the source material is weak

This keeps research useful without turning into another noisy feed.
