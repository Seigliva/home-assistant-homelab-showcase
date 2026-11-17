# Media: movie mode on play/pause

## Problem

The room should adapt when a movie starts, pauses or stops.

## Pattern

- when media starts: dim lights, close blinds, set scene
- when paused: raise lights slightly
- when stopped: restore normal scene
- add conditions for time of day and occupancy

## Example entities

```yaml
media_player.living_room_tv
scene.movie_mode
scene.living_room_normal
```

## Runnable sanitized example

- [Complete package YAML](../../examples/home-assistant/media-movie-mode.yaml)
- [Installation, dependencies, replacements and safe tests](../../examples/home-assistant/README.md)

The package is the complete implementation; earlier snippets above illustrate the
pattern only. Review the documented adaptation boundaries before enabling it.
