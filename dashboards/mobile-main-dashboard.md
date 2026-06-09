# Mobile-first main dashboard

![Anonymized Home Assistant mobile dashboard](../assets/dashboards/mobile-main-dashboard-anonymized.jpg)

## Goal

A mobile-first Home Assistant dashboard used as the shared daily control surface for the household. The design prioritizes quick status checks, room navigation and frequently used actions over dense raw entity lists.

## Design pattern

- **Mobile-first layout:** large touch targets and stacked rows that work well one-handed.
- **Frosted glass visual style:** dark background with translucent cards, soft shadows and blurred panels.
- **Mushroom + Bubble Card mix:** Mushroom-style entities for compact state display combined with Bubble Card navigation/action rows.
- **Top status strip:** weather, door/garage state and high-level home status are visible before scrolling.
- **Household presence row:** person cards show anonymized presence/home state. Public screenshot redacts faces and names.
- **Room cards:** each room card shows the most important temperature/status signal and acts as a drill-down entry point.
- **Persistent app shell:** weather, status strip and the four primary view icons stay in place while only the center content changes.
- **Bottom dock:** fixed shortcut bar for the most-used operational modes: cleaning, remotes, power/energy, home/security, server/homelab and settings.
- **Overlay-safe navigation:** the bottom dock is given a higher stacking layer so it remains usable even when Bubble Card pop-ups are open.

## Visible sections

- Weather card with current outdoor temperature and condition.
- Door/garage status indicators with color-coded state.
- Main navigation cards: house, calendar, shopping and info.
- Household presence/person row with status badges.
- Room tiles for living room, kitchen, bedroom, hallway/bath, basement, outside and two child/game rooms.
- Persistent bottom navigation dock for common operational modes.

Related room drill-down: [Living-room dashboard](living-room-dashboard.md).

## Navigation pattern

The main dashboard behaves like a small household control app rather than a set of unrelated Home Assistant views:

- **Four primary views:** house, calendar, shopping and info.
- **Stable frame:** weather, status line and the four primary icons remain visible across those views.
- **Changing center:** only the middle content area changes when switching between the primary views.
- **Fixed bottom dock:** secondary actions stay pinned to the bottom of the screen for quick access from anywhere.
- **Bubble Card compatible:** the dock uses `position: fixed` and a high `z-index`, so it stays above opened Bubble Card overlays.

Simplified implementation sketch:

```yaml
type: custom:mod-card
card_mod:
  style: |
    ha-card {
      z-index: 6;
      position: fixed;
      bottom: 10px;
      left: 10px;
      width: calc(100% - 20px);
      border-radius: 100px;
    }
card:
  type: grid
  columns: 6
  cards:
    - type: custom:button-card
      icon: mdi:vacuum-outline
      tap_action:
        action: navigate
        navigation_path: "#cleaning"
    - type: custom:button-card
      icon: mdi:remote
      tap_action:
        action: navigate
        navigation_path: "#media"
    - type: custom:button-card
      icon: mdi:power-plug
      tap_action:
        action: navigate
        navigation_path: "#energy"
    - type: custom:button-card
      icon: mdi:shield-home
      tap_action:
        action: navigate
        navigation_path: "#security"
    - type: custom:button-card
      icon: mdi:server-outline
      tap_action:
        action: navigate
        navigation_path: "#server"
    - type: custom:button-card
      icon: mdi:tune-variant
      tap_action:
        action: navigate
        navigation_path: "#settings"
```

## Why this works well

- The dashboard is not just a control panel; it is a household status overview.
- Status is grouped by how people think: home, people, rooms and quick actions.
- The persistent frame makes navigation predictable because the most important context never disappears.
- The bottom dock keeps operational shortcuts reachable even from pop-ups and deep interaction states.
- Temperature is surfaced at the room level, which makes climate issues visible without opening each room.
- Room-specific controls are moved into drill-down pages so the main dashboard stays clean.

## Privacy note

The public screenshot is anonymized:

- personal faces are obscured
- person names are replaced with placeholders
- child/game-room names are replaced with generic room labels
- exact entity IDs and notification targets are omitted

The original private dashboard may contain household-specific names, photos and room labels that are not published here.
