---
name: radar-analysis
description: Analyze the ai-signal-radar repository history to produce monthly reviews, quarterly reviews, theme analysis, trend synthesis, or idea-mining reports from existing reviewed radar data. Use when Codex is asked to mine signals, summarize periods, identify recurring themes, compare months or quarters, or draft reports based on data/*.json, radars/*.md, indexes/*.json, and reports/monthly/*.md without ingesting new weekly reports.
---

# Radar Analysis

## Source Contract

Treat `data/YYYY/*.json` as the primary source, `radars/YYYY/*.md` as reviewed narrative context, and `indexes/*.json` plus `themes/README.md` as derived navigation. Do not use external sources or OpenAI API calls for repository analysis unless the user explicitly changes the contract.

Before producing an analysis report, run or mentally apply the repository consistency checks:

```bash
uv run python scripts/validate_content.py
```

If indexes are stale and the user asked for a committed artifact, regenerate them first:

```bash
uv run python scripts/update_indexes.py
```

Do not edit reviewed weekly source files under `data/` or `radars/` during analysis. Those files are human-reviewed ingestion outputs.

## Monthly Reviews

For a deterministic monthly scaffold, use:

```bash
uv run python scripts/generate_monthly_review.py YYYY-MM
```

The generated file belongs at `reports/monthly/YYYY-MM.md`. It should contain only deterministic extraction and counts from reviewed data and indexes. If adding interpretive prose, keep it explicitly grounded in cited dates, signal titles, and themes from the repository.

## Quarterly Reviews

For a quarter such as `2026-Q2`:

1. Read `indexes/weekly_radars.json`, `indexes/themes.json`, and `indexes/summary.json`.
2. Load only records whose dates fall within the quarter.
3. Group by theme frequency, repeated signal language, recurring product ideas, and evidence links.
4. Compare the quarter against prior quarters only if those records exist locally.
5. Report gaps clearly when the data set is too small for a trend claim.

Use headings such as `Coverage`, `Recurring Themes`, `Signals Worth Rechecking`, `Idea Candidates`, and `Open Questions`.

## Idea Mining

When mining ideas:

1. Start from `ideas` arrays in the JSON records.
2. Add supporting signals from records with overlapping themes.
3. Distinguish repository evidence from your inference.
4. Prefer a short ranked list over a broad brainstorm.
5. Do not create or update files under `ideas/` unless the user explicitly asks for an artifact.

Each idea should include:

- working title
- source dates
- supporting themes
- strongest supporting signals
- why it may matter
- what would falsify or weaken it

## Output Rules

Keep analysis anchored to repository facts:

- Cite dates and file paths for claims.
- Preserve Ray's reviewed framing; do not rewrite weekly reports as news summaries.
- Avoid claiming a trend from a single record unless labeled as an early signal.
- Separate deterministic extraction from interpretation.
- If producing a file, run validation after generation when practical.
