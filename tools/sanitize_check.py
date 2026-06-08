#!/usr/bin/env python3
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
PATTERNS = {
    'private_ipv4': re.compile(r'\b(?:192\.168|10\.|172\.(?:1[6-9]|2\d|3[0-1]))(?:\.\d{1,3}){2}\b'),
    'possible_token_key': re.compile(r'(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*[^\n<][^\n]*'),
    'email': re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'),
    'ha_llat': re.compile(r'(?i)long[-_ ]?lived|access[_-]?token'),
    'telegram_chat_id': re.compile(r'(?i)chat[_-]?id\s*[:=]\s*-?\d+'),
}
ALLOW = [
    'user@example.com',
    '192.168.x.x',
    '!secret redacted',
    'token or secret',
    'long-lived access tokens',
    'no secrets',
    'no tokens',
    'possible_token_key',
]

def allowed(line: str) -> bool:
    return any(a.lower() in line.lower() for a in ALLOW)

findings = []
for path in ROOT.rglob('*'):
    if path.is_dir() or '.git' in path.parts:
        continue
    if path.suffix.lower() not in {'.md', '.yaml', '.yml', '.py', '.txt', ''}:
        continue
    text = path.read_text(errors='ignore')
    for name, rx in PATTERNS.items():
        for m in rx.finditer(text):
            line = text.count('\n', 0, m.start()) + 1
            line_text = text.splitlines()[line - 1] if line - 1 < len(text.splitlines()) else ''
            snippet = text[m.start():m.end()].strip()
            if allowed(snippet) or allowed(line_text):
                continue
            findings.append((str(path.relative_to(ROOT)), line, name, snippet[:120]))

if findings:
    print('Potential private data found:')
    for f in findings:
        print(f'{f[0]}:{f[1]} [{f[2]}] {f[3]}')
    sys.exit(1)
print('OK: no obvious private data patterns found')
