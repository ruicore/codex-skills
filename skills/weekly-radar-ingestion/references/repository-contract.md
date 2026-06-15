# Repository Contract

Use this reference when ingesting a reviewed weekly AI Systems Engineering Radar
report into `ai-signal-radar`.

## Source of Truth

The reviewed report is the canonical human-approved signal record. Preserve its
content under `radars/YYYY/YYYY-MM-DD.md`; derive structured files from it.

This repository is a long-term personal signal repository for future AI agents,
not a news archive. Optimize for retrieval, trend analysis, recurring signal
detection, and idea generation.

## Date Rules

Use exactly one ISO date for every ingestion. Required paths:

- `radars/YYYY/YYYY-MM-DD.md`
- `data/YYYY/YYYY-MM-DD.json`

If the input says "this week" but no date is present, ask for the date. Do not
use the current date silently.

## Metadata Compatibility

Ray's neutral metadata preference is:

```json
{
  "date": "",
  "week": "",
  "title": "",
  "status": "reviewed",
  "reviewed_by": "Ray",
  "themes": [],
  "importance": 0,
  "top_signals": [],
  "action_items": []
}
```

When the repository has a JSON schema, that schema wins. Map neutral fields to
schema fields without losing information:

- `top_signals` can map to `signals` when the schema models full signal objects.
- `action_items` can stay empty if the schema has no action item field.
- `importance` can stay `0` or be omitted when unsupported.
- source provenance should record that the report was reviewed before ingestion.

Never add unsupported JSON fields to a schema with `additionalProperties: false`
unless the schema is intentionally updated in the same change.

## Theme Files

Create or update `themes/<theme>.md` for each explicit theme.

Required sections:

```markdown
# <theme>

## Summary

<One stable description of the theme. Leave empty if unknown.>

## Related Reports

- YYYY-MM-DD: [Report title](../radars/YYYY/YYYY-MM-DD.md)

## Notable Recurring Signals

- <Signal that recurs across reports. Leave empty if not established yet.>
```

Use additive updates. Do not rewrite a theme summary unless the existing summary
is wrong or stale. Do not invent recurrence from a single report; a first
appearance can be noted as a related report with an empty recurring signal.

## Indexes

Prefer checked-in scripts that rebuild indexes from `data/`. If no script
exists, maintain:

- `indexes/reports.json`: chronological report entries with date, title,
  themes, markdown path, and data path.
- `indexes/themes.json`: map from theme slug to related reports.

Use stable sorted order: dates ascending and theme slugs alphabetically.
