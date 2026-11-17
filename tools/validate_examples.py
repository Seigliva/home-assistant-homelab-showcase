#!/usr/bin/env python3
"""Offline checks, not Home Assistant schema validation or device verification.
Install PyYAML and Jinja2 in a disposable virtual environment, then run this file.
"""
from pathlib import Path
from datetime import datetime, timezone, timedelta
from types import SimpleNamespace
import json
import re
import yaml
from jinja2 import Environment, StrictUndefined
from jinja2.nativetypes import NativeEnvironment

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / 'examples/home-assistant'
ORIGINAL = '''ai-laundry-finished-notification air-quality-light-feedback car-heater-scheduling dishwasher-finished-helper garage-door-actionable-notification media-movie-mode robot-mower-weather-gated smart-blinds-temperature-wind-mqtt trash-day-ai-reminder water-leak-critical-alert'''.split()

class Loader(yaml.SafeLoader):
    pass

def mapping(loader, node, deep=False):
    keys = [loader.construct_object(k, deep=deep) for k, _ in node.value]
    assert len(keys) == len(set(keys)), 'Duplicate YAML key'
    return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)

Loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
Loader.add_constructor('!input', lambda loader, node: loader.construct_scalar(node))

def strings(value):
    if isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)
    elif isinstance(value, str):
        yield value

def load(slug):
    return yaml.load((EXAMPLES / (slug + '.yaml')).read_text(), Loader=Loader)

parsed = templates = links = cases = 0
for path in sorted(ROOT.rglob('*.yaml')):
    data = yaml.load(path.read_text(), Loader=Loader)
    parsed += 1
    for text in strings(data):
        if '{{' in text or '{%' in text:
            Environment().parse(text)
            templates += 1
for path in sorted(ROOT.rglob('*.md')):
    for target in re.findall(r'\]\(([^\s)]+)(?:\s+[^)]*)?\)', path.read_text()):
        if re.match(r'^[a-z]+:', target) or target.startswith('#'):
            continue
        target = target.split('#')[0].split('?')[0]
        assert (path.parent / target).exists(), f'Broken link: {path.relative_to(ROOT)} -> {target}'
        links += 1
for slug in ORIGINAL:
    doc = ROOT / 'automations/home-assistant' / (slug + '.md')
    assert doc.exists()
    expected = 'blueprints/automation/robot-mower-weather-gated' if slug == 'robot-mower-weather-gated' else 'examples/home-assistant/' + slug + '.yaml'
    assert expected in doc.read_text(), f'No implementation link: {slug}'
    assert doc.name in (EXAMPLES/'README.md').read_text()
ids = []
for path in EXAMPLES.glob('*.yaml'):
    data = yaml.load(path.read_text(), Loader=Loader)
    for automation in data['automation']:
        assert automation['initial_state'] is False
        assert automation['triggers'] and automation['actions']
        ids.append(automation['id'])
    for helper in data.get('input_datetime', {}).values():
        assert helper.get('has_date') or helper.get('has_time')
assert len(ids) == len(set(ids)), 'Duplicate automation IDs'

env = NativeEnvironment(undefined=StrictUndefined)
state = {}
attributes = {}
clock = datetime(2026, 1, 1, 3, tzinfo=timezone.utc)
def stamp(value, default=0):
    try:
        return value.timestamp() if isinstance(value, datetime) else datetime.fromisoformat(value).timestamp()
    except (ValueError, TypeError):
        return default
def render(text, **kw):
    result = env.from_string(text).render(**kw)
    # HA strips outer whitespace before converting boolean template results.
    if isinstance(result, str) and result.strip().lower() in ('true', 'false'):
        return result.strip().lower() == 'true'
    return result.strip() if isinstance(result, str) else result

def check(actual, expected):
    global cases
    assert actual == expected, (actual, expected)
    cases += 1
env.globals.update(states=lambda e: state.get(e, 'unknown'), is_state=lambda e,v: state.get(e) == v,
                   state_attr=lambda e,a: attributes.get((e,a)), now=lambda: clock,
                   as_timestamp=stamp, today_at=lambda t: clock.replace(hour=int(t.split(':')[0]), minute=int(t.split(':')[1]), second=0))
env.filters['from_json'] = lambda value, default=None: json.loads(value) if value and value not in ['unknown','unavailable'] else default
env.filters['to_json'] = json.dumps

# Render the actual EV permission templates, including equal/overnight bounds.
ev = load('ev-charging-reconciler')['automation'][0]['actions'][2]['variables']
for start,end,hour,expected in [('02:00:00','07:00:00',3,True),('02:00:00','07:00:00',7,False),('22:00:00','07:00:00',23,True),('22:00:00','07:00:00',3,True),('22:00:00','07:00:00',12,False),('02:00:00','02:00:00',3,False)]:
    state.update({'input_datetime.ev_charge_start':start,'input_datetime.ev_charge_end':end})
    clock = clock.replace(hour=hour)
    check(render(ev['night']),expected)
for status in ['awaiting_start','ready_to_charge','charging','completed','disconnected','unknown','unavailable']:
    state['sensor.charger_status']=status
    check(render(ev['connected']),status in ['awaiting_start','ready_to_charge','charging','completed'])
state.update({'input_boolean.ev_charge_now':'off','input_boolean.ev_schedule_enabled':'on'})
check(render(ev['allowed'],night=True,preheat=False),True)
check(render(ev['allowed'],night=False,preheat=False),False)
check(render(ev['preheat']),False)

# Doorbell selection renders real templates with generic test fixtures.
door = load('doorbell-snapshot-alert')['automation'][0]
select = door['actions'][0]['parallel'][1]['sequence'][0]['variables']['alert_lights']
areas = {room:[SimpleNamespace(domain='light',state='on',entity_id='light.'+room),SimpleNamespace(domain='light',state='off',entity_id='light.'+room+'_off')] for room in ['office','laundry','child_one','child_two','child_three']}
env.globals.update(area_entities=lambda a: areas.get(a,[]),expand=lambda a:a)
for a,b,p,child,expected in [('home','not_home','off','not_home',['light.office','light.laundry']),('home','not_home','on','home',[]),('not_home','not_home','off','home',['light.child_one']),('unknown','not_home','off','home',[]),('not_home','unavailable','off','home',[])]:
    state.update({'person.adult_one':a,'person.adult_two':b,'binary_sensor.living_room_presence':p,'person.child_one':child,'person.child_two':'not_home','person.child_three':'not_home'})
    check(render(select),expected)
clock = datetime(2026,1,1,12,tzinfo=timezone.utc)
for age,event,previous,expected in [(1,'ring','valid',True),(31,'ring','valid',False),(1,'ring','unknown',False),(1,'other','valid',False)]:
    trigger=SimpleNamespace(from_state=SimpleNamespace(state=previous),to_state=SimpleNamespace(state=(clock-timedelta(seconds=age)).isoformat(),attributes={'event_type':event}))
    check(render(door['conditions'][0]['value_template'],trigger=trigger),expected)

# Toilet logic is declarative: evaluate its actual combined state conditions.
toilet=load('toilet-night-alarm')['automation'][0]['actions'][0]['choose'][0]
check(toilet['conditions'][1]['state'],'off')
night_conditions=toilet['sequence'][0]['choose'][0]['conditions']
for night,alarm,expected in [('on','armed_home',True),('off','armed_home',False),('on','disarmed',False),('off','disarmed',False)]:
    state.update({'schedule.night_mode':night,'alarm_control_panel.home_alarm':alarm})
    check(all(state.get(c['entity_id'])==c['state'] for c in night_conditions),expected)

# Evaluate bedroom branch conditions from the actual example, not a duplicated policy.
bedroom = load('bedroom-motion-manual-precedence')['automation'][0]
def condition_ok(c, trigger_id):
    if isinstance(c, list):
        return all(condition_ok(x, trigger_id) for x in c)
    if c['condition'] == 'trigger':
        return trigger_id in (c['id'] if isinstance(c['id'], list) else [c['id']])
    if c['condition'] == 'state':
        return state.get(c['entity_id']) == c['state']
    if c['condition'] == 'template':
        return bool(render(c['value_template']))
    if c['condition'] == 'time':
        return clock.strftime('%H:%M:%S') >= c['after']
    raise AssertionError(c)
for hour,evening,night,adult,alarm,block,bedside,expected in [
    (9,'off','off','home','disarmed','off','off',None),
    (11,'off','off','home','disarmed','off','off',1),
    (11,'off','off','not_home','disarmed','off','off',None),
    (11,'off','off','home','armed_home','off','off',None),
    (21,'on','off','home','disarmed','off','off',0),
    (1,'off','on','home','disarmed','off','off',0),
    (1,'off','on','home','armed_home','off','off',None),
    (21,'on','off','home','disarmed','on','off',None),
    (21,'on','off','home','disarmed','off','on',None),
]:
    clock=clock.replace(hour=hour)
    state.update({'schedule.evening_mode':evening,'schedule.night_mode':night,'group.adults':adult,'alarm_control_panel.home_alarm':alarm,'input_boolean.bedroom_motion_enabled':'on','input_boolean.bedroom_manual_block':block,'input_boolean.bedroom_manual_off_night':'off','light.bedroom_bedside':bedside})
    selected=None
    if condition_ok(bedroom['conditions'],'detected'):
        for i,branch in enumerate(bedroom['actions'][0]['choose']):
            if condition_ok(branch['conditions'],'detected'):
                selected=i
                break
    check(selected,expected)

# AI fallback must tolerate missing/empty/error response without fabricated content.
trash=load('trash-day-ai-reminder')['automation'][0]['actions'][2]['variables']['message']
for response in [{},None,{'response':{'response_type':'error'}},{'response':{'speech':{'plain':{'speech':''}}}}]:
    check(render(trash,ai_result=response,fallback='Fallback'), 'Fallback')
check(render(trash,ai_result={'response':{'speech':{'plain':{'speech':'  Reminder  '}}}},fallback='Fallback'),'Reminder')
print(f'PASS: {parsed} YAML files; {templates} embedded Jinja templates parsed; {links} local Markdown links; {len(ORIGINAL)} original topics covered; {len(ids)} example automations initially disabled; {cases} offline decision cases')
print('Boundary: no HA runtime schema check, physical device actuation or delivery test was performed.')
