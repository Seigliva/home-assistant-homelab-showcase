# Security and privacy

This repository is a curated public showcase, not a full Home Assistant backup.

## What is intentionally excluded

- `secrets.yaml`
- long-lived access tokens
- API keys
- exact internal IP topology
- camera URLs/snapshots
- alarm codes or sensitive security workflows
- real chat IDs, phone numbers or email addresses
- person-specific entity names

## Before publishing changes

Run:

```bash
python3 tools/sanitize_check.py .
```

The scanner is conservative. If it flags something, either remove it, generalize it, or move it to private notes.
