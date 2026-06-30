# Changelog

All notable changes to this repository should be recorded here.

This repository is evolving informally until tagged releases are introduced.
Use the `Unreleased` section to summarize reviewable changes as skills,
metadata, validation, and public documentation mature.

## Unreleased

### Added

- Added Apache-2.0 licensing for public reuse.
- Added a release policy for future tagged releases and maintenance notes.
- Added repository contract and grounded evolution guidance for preserving
  practice-derived skill behavior while improving public reuse.
- Added skill taxonomy and maturity model for classifying current skills without
  requiring directory or behavior changes.
- Added public sanitization policy for secrets, private data, private URLs, raw
  logs, and sensitive identifiers.
- Added side-effect policy covering read-only, local file, Git, external API,
  publishing, and destructive-operation guardrails.
- Added skill authoring guide plus extraction-note and proposal templates for
  turning observed practice into reviewable skills.
- Added agent metadata guidance for optional `skills/*/agents/openai.yaml`
  discovery metadata.
- Added skill registry schema and `skills/index.json` with category, maturity,
  side-effect, validation, supporting-file, and portability metadata.
- Added skill validator and GitHub Actions workflow for registry, metadata,
  Markdown link, script reference, and helper-script checks.
- Added registry-based list and install tooling for discovering and copying
  skills.
- Added reusable examples across skills and a database access audit quick
  reference.

### Changed

- Updated the README direction, repository guide links, install flow, registry
  notes, category overview, skill outcomes, and validation guidance to reflect
  the current public repository surface.
