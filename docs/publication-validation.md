# Validation and publication boundary

The 2026-11-18 refresh used fresh Home Assistant REST state/config reads, a
read-only SMB download of automation/script configuration, and the active default
Hermes profile's cron records and selected scripts. Raw sources remained outside
the repository. No Home Assistant services, reloads, automation runs, cron runs,
schedule edits or other-profile changes were performed.

## Reproduce the offline checks

From the repository root, using a disposable Python environment outside the checkout:

```sh
python3 -m venv "$HOME/.cache/showcase-check"
"$HOME/.cache/showcase-check/bin/pip" install PyYAML Jinja2
"$HOME/.cache/showcase-check/bin/python" tools/validate_examples.py
python3 tools/sanitize_check.py .
git diff --check
```

The validator checks YAML (including blueprint `!input` tags), duplicate mapping
keys, embedded Jinja syntax, local Markdown file links, coverage of the original ten
automation documents, unique example automation IDs, safe disabled startup, helper
time fields, and offline decision cases using the actual example templates.

Decision cases cover ordinary/overnight/equal charging windows, charging connection
states, bedroom on-gates, toilet night-plus-alarm conditions, doorbell presence/area
selection and event freshness, and AI response fallbacks. Fixtures are synthetic and
are **not** presented as production results. The condition evaluator is deliberately
limited; it does not simulate the complete Home Assistant engine or time scheduling.

## What these checks do not prove

- This is not Home Assistant's runtime configuration/schema validator. Run that on
  your adapted package before enabling it.
- Local Markdown targets are checked, not every remote link or anchor fragment.
- No physical light, garage, heater, charger, mower or phone was exercised for this
  publication. Safely commission your own entity mappings.
- Dynamic light snapshots are not durable across Home Assistant restarts.
- A script's scheduler status does not independently prove message delivery or health.
- The doorbell source is specifically **unverified**: the enabled live automation had
  no last-triggered value and its trace list was empty; the source event was still
  dated November 9. A user press was not received. Static package tests do not solve
  that upstream delivery problem.

The repository sanitizer is a heuristic, not a security audit. Publication also
included manual diff review and a local scan against private environment values and
household/network identifiers without printing those values. Public examples use
English generic identifiers; private device IDs, addresses and credentials are not
needed to reproduce the patterns.

See [example installation and coverage](../examples/home-assistant/README.md).
