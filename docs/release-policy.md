# Release Policy

This repository currently evolves through Git history and the `Unreleased`
section of `CHANGELOG.md`. Tagged releases should be introduced when there is a
reviewable public surface worth pointing users to, not merely because files have
changed.

## When To Tag A Release

Tag a release when at least one of these is true:

- a skill reaches a stable enough public reuse point that external users should
  install a known version
- registry metadata, schema, or validation behavior changes in a way users may
  need to coordinate with local tooling
- multiple related skill or documentation updates form a coherent maintenance
  checkpoint
- a compatibility boundary changes and users need a named version before and
  after the change

Do not tag a release for cosmetic edits, private maintenance notes, or broad
rewording that does not change the public skill surface.

## Describing Skill Changes

Changelog entries for skill changes should name the skill and describe the user
visible workflow effect. Prefer concrete wording such as:

- `diagnose`: clarified the required repro-before-fix checkpoint
- `buffer-publisher`: added a dry-run expectation before queue mutations
- `weekly-radar-ingestion`: updated validation for generated theme records

Avoid vague entries such as "improved docs" when the affected workflow,
metadata, or validation behavior can be named.

## Breaking Changes

Mark a change as breaking when an existing user or installed skill copy may need
manual action. Examples include:

- renaming or moving a skill directory
- changing a skill trigger or output contract in a non-compatible way
- removing or replacing a script, template, reference file, or registry field
- changing validation behavior so previously accepted skill packages fail
- changing side-effect or confirmation rules in a way that affects operation

Breaking changes should appear under a `Breaking Changes` heading in
`CHANGELOG.md`. Include the affected skill, old behavior, new behavior, and the
expected migration step.

## Maturity Promotions

Use the maturity labels from `docs/skill-taxonomy.md`. A maturity promotion
should be evidence-backed and should not happen only because a skill has been
reformatted.

When promoting maturity:

- update `skills/index.json`
- describe the evidence for the promotion in `CHANGELOG.md`
- update examples, validation expectations, or portability notes when they are
  part of the promotion
- keep the skill's current behavior intact unless the issue explicitly asks for
  a behavior change

## Deprecated Skills

A deprecated skill is retained for compatibility but no longer recommended for
new work. Deprecation should be explicit and reversible while users still depend
on the skill.

When deprecating a skill:

- set its registry maturity to `deprecated`
- add a short reason and replacement path in the registry portability notes or
  related documentation
- add a `Deprecated` changelog entry naming the skill
- keep the skill files available unless a later breaking release removes them
- do not silently redirect a skill to a different workflow

## Keeping Registry, Schema, And Docs In Sync

Changes to skills and public metadata should keep the repository's sources of
truth aligned:

- update `skills/index.json` when category, maturity, side-effect level,
  supporting files, validation expectations, or portability notes change
- update `schemas/skill-registry.schema.json` when registry field structure or
  allowed values change
- update README tables when the public skill list, categories, or install
  guidance changes
- update docs when policy or authoring expectations change
- run `python scripts/validate_skills.py` after changes to skills, docs,
  registry metadata, schema, or README links

If no automated validation covers a release-policy change, manually check local
Markdown links and confirm no skill content changed unintentionally.
