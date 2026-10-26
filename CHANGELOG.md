# Changelog

All notable changes to this repository should be recorded here.

Skills have independent versions in `skills/index.json`; repository tags are
optional collection snapshots. Use the `Unreleased` section to summarize
reviewable changes, naming affected skill versions for subsequent updates.

## Unreleased

### Added

- Independent skill versions, initialized at `0.1.0` for all current skills
  without reconstructing historical versions. Listing and installation output
  show versions; new installation receipts record `skill_version` alongside the
  source commit and hashes, plus a registry-modified indicator. Existing receipts
  remain compatible.
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

- `radar-analysis`: aligned source paths, indexes, monthly generation, period
  analysis, and provenance rules with the `systems` / `creation` repository
  contract.
- `decision-trace-writer`: added optional observed skill-application evidence
  for reusable TraceGym metadata without causal scoring or maturity mutation.
- `diagnose`: added a read-only Runtime Visibility Phase 0 for runtime identity,
  correlation, freshness, redaction, and explicit visibility-gap handling.
- `weekly-radar-ingestion`: added explicit `systems` and `creation` track
  selection, multi-track paths and validation, creation observation-window
  requirements, and v2 radar metadata guidance.
- Promoted `decision-trace-writer` to `stable-workflow` after repeated real
  secondary-persistence use established stable decision/trace boundaries and
  validated durable-output behavior.
- Promoted `grill-with-docs` to `portable-candidate` after real docs-grounded
  pressure-testing use demonstrated a reusable workflow while retaining its
  portability caveats.
- Promoted `repository-layout-refactor` to `portable-candidate` after validated
  behavior-preserving layout-refactor use demonstrated a reusable
  concept-owned-package workflow while retaining its portability caveats.
- Promoted `weekly-radar-ingestion` to `portable-candidate` after validated
  recurring weekly ingestion/publish use in its target repository, with its
  repository- and practice-specific caveats retained.
- Added decision-trace UI metadata and removed the duplicated maturity map.
- Updated the README direction, repository guide links, install flow, registry
  notes, category overview, skill outcomes, and validation guidance to reflect
  the current public repository surface.

### Breaking Changes

- Registry schema `0.1.0` to `0.2.0`: every skill entry now requires a normal
  `X.Y.Z` version. Previously, entries could omit it. Custom registries must add
  `version` to each skill before using the updated validator or installer; new
  baselines can start at `0.1.0`. This does not retroactively version existing
  installations or change the receipt format number.
