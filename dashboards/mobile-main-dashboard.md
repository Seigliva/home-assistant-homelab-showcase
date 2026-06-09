# Mobile-first main dashboard

![Anonymized Home Assistant mobile dashboard](../assets/dashboards/mobile-main-dashboard-anonymized.jpg)

## Goal

A mobile-first Home Assistant dashboard used as the shared daily control surface for the household. The design prioritizes quick status checks, room navigation and frequently used actions over dense raw entity lists.

## Design pattern

- **Mobile-first layout:** large touch targets and stacked rows that work well one-handed.
- **Frosted glass visual style:** dark background with translucent cards, soft shadows and blurred panels.
- **Mushroom + Bubble Card mix:** Mushroom-style entities for compact state display combined with Bubble Card navigation/action rows.
- **Top app header:** a compact grid header combines a menu/kiosk toggle with the current weather state and temperature.
- **Horizontal status rail:** door, garage, open contact sensors and active appliance states appear as pill buttons directly under the header.
- **Conditional status chips:** low-priority items stay hidden until they matter, e.g. open doors, running appliances, finished cycles or active robot vacuum.
- **Household presence row:** person cards show anonymized presence/home state. Public screenshot redacts faces and names.
- **Room cards:** each room card shows the most important temperature/status signal and acts as a drill-down entry point.
- **Persistent app shell:** weather, status strip and the four primary view icons stay in place while only the center content changes.
- **Bottom dock:** fixed shortcut bar for the most-used operational modes: cleaning, remotes, power/energy, home/security, server/homelab and settings.
- **Overlay-safe navigation:** the bottom dock is given a higher stacking layer so it remains usable even when Bubble Card pop-ups are open.

## Visible sections

- Menu/kiosk button on the left and weather summary on the right.
- Weather chip showing localized condition text, icon and current temperature.
- Horizontally scrollable status rail with door/garage state, open contact sensors, appliance state, robot vacuum and light count.
- Main navigation cards: house, calendar, shopping and info.
- Household presence/person row with status badges.
- Room tiles for living room, kitchen, bedroom, hallway/bath, basement, outside and two child/game rooms.
- Persistent bottom navigation dock for common operational modes.

Related room drill-down: [Living-room dashboard](living-room-dashboard.md).

## Header and status rail pattern

The top of the dashboard is a persistent context layer. It gives the household immediate answers before anyone scrolls or opens a room:

- **Left control:** a menu button that can also act as a kiosk-mode toggle on hold.
- **Right weather summary:** localized weather text, current temperature and condition icon.
- **Status rail:** a horizontal `paper-buttons-row` of compact pills for actionable states.
- **Always-visible critical states:** lock and garage state are color-coded red/green.
- **Only-show-when-relevant chips:** doors, appliances and robot vacuum are hidden unless active/open/finished/running.
- **Fast drill-downs:** chips can navigate directly to focused pop-ups such as weather, robot vacuum or lights.

Sanitized implementation sketch:

```yaml
type: vertical-stack
cards:
  - type: custom:gap-card
    height: 12px
  - type: custom:layout-card
    layout_type: custom:grid-layout
    layout:
      grid-template-columns: min-content 1fr max-content
      grid-template-areas: |
        "menu . weather"
    cards:
      - type: custom:button-card
        view_layout:
          grid-area: menu
        icon: mdi:menu
        entity: input_boolean.kiosk_mode
        hold_action:
          action: toggle
        tap_action:
          action: call-service
          service: browser_mod.open_menu
      - type: custom:button-card
        view_layout:
          grid-area: weather
        entity: sensor.weather_now
        show_icon: false
        name: "[[[ return states['sensor.weather_condition_localized'].state; ]]]"
        label: |
          [[[ return `${entity.attributes.temperature.toFixed(1)}°`; ]]]
        custom_fields:
          icon: |
            [[[ return `<ha-icon icon="${entity.attributes.icon}"></ha-icon>`; ]]]
        tap_action:
          action: navigate
          navigation_path: "#weather"
  - type: custom:paper-buttons-row
    styles:
      overflow: scroll
      gap: 8px
    buttons:
      - icon: mdi:door
        name: Front door
        entity: lock.front_door
        state_styles:
          unlocked:
            button:
              color: red
          locked:
            button:
              color: green
      - icon: mdi:garage
        name: Garage
        entity: cover.garage_door
        state_styles:
          open:
            button:
              color: red
          closed:
            button:
              color: green
      - icon: mdi:door-open
        name: Patio
        entity: binary_sensor.patio_door_contact
        styles:
          button:
            display: "{{ 'flex' if is_state(config.entity, 'on') else 'none' }}"
      - icon: mdi:washing-machine
        entity: input_boolean.washing_machine_running
        state: >
          {% if is_state(config.entity, 'on') %}Running{% endif %}
        styles:
          button:
            display: "{{ 'flex' if is_state(config.entity, 'on') else 'none' }}"
      - icon: mdi:lightbulb-group
        entity: sensor.number_of_lights_on
        state: "{{ states(config.entity) }} lights on"
        tap_action:
          action: navigate
          navigation_path: "#lights"
```

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
- The top header answers the two fastest questions first: “where is the menu?” and “what is the weather now?”
- The status rail is quiet by default but becomes prominent when something needs attention.
- Locks, garage, open doors, appliances, vacuum and light count are represented as small actionable chips instead of full cards.
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
