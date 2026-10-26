# Release Policy

Skills evolve independently. `skills/index.json` owns each skill's current
`version`; Git history and `CHANGELOG.md` record changes. Repository tags are
optional collection snapshots and do not force unrelated skills to change
version.

## Independent Skill Versions

Versioning starts with the current skill set: every existing skill begins at
`0.1.0`. Do not reconstruct versions for earlier commits or installations. New
skills also start at `0.1.0` unless they explicitly introduce a stable `1.0.0`
contract. Version and maturity are separate: assigning a version does not promote
a skill's maturity.

Maintain the current version only in the skill's `skills/index.json` entry.
It covers the complete package directory: `SKILL.md`, agent metadata, references,
templates, and helper scripts. Do not duplicate it in skill frontmatter or agent
metadata. Registry fields that define a skill's use, such as triggers and output
or side-effect contracts, are also part of its versioned behavior. Repository
tooling and the registry's `schema_version` evolve separately.

Use normal `X.Y.Z` versions without leading zeroes, prerelease labels, or build
metadata. After `1.0.0`, follow [Semantic Versioning](https://semver.org/):

| Change | Version increment |
|---|---|
| Compatible correction or clarification, including package documentation fixes | Patch: `1.2.0` to `1.2.1` |
| Compatible new capability, optional workflow, parameter, or deprecation | Minor: `1.2.1` to `1.3.0` |
| Incompatible trigger, output, path, script interface, or operational authorization change | Major: `1.3.0` to `2.0.0` |

During `0.x`, use patch increments for compatible fixes and minor increments for
new capabilities or breaking changes. Always label breaking changes and describe
migration, even during `0.x`. Adopt `1.0.0` when the skill has a defined, stable
usage contract.

Increment only affected skills when preparing a reviewed update for delivery,
not for each intermediate development commit. Several edits may share one pending
version. Once delivered, do not reuse that version for different package content.
An unchanged skill keeps its version. Repository-only edits and administrative
classification changes do not require a skill bump unless they change its usage
contract.

For each delivered update:

1. Update the affected skill's registry version.
2. Add a `CHANGELOG.md` entry naming the skill, old and new versions, and user-visible
   effect. Include migration instructions when breaking.
3. Run `python scripts/validate_skills.py --require-denylist` and applicable behavior
   checks before delivery.

The installer records `skill_version` alongside the source commit and content
hashes. Receipt `version` is the receipt format number; registry `schema_version`
is the registry format number. Neither is a skill version. Local development
copies can differ from the declared version's delivered content; use hashes and
the source modification flags to identify those copies.

The current installer uses the checked-out source, without version lookup or
remote resolution. To reproduce a delivered version, use its source commit in a
separate checkout and install from there. Per-skill tags can be added later if
named version lookup becomes necessary.

## When To Tag A Release

Tag a collection release when there is a reviewable public checkpoint worth
pointing users to and at least one of these is true:

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

`docs/skill-taxonomy.md` owns the maturity vocabulary, semantics, and promotion
criteria. `skills/index.json` is the sole source of truth for each skill's
current maturity value. A maturity promotion should be evidence-backed and
should not happen only because a skill has been reformatted.

When promoting maturity:

- update the current maturity value in `skills/index.json`
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

- keep maturity vocabulary, semantics, and promotion criteria in
  `docs/skill-taxonomy.md`; record current per-skill maturity values only in
  `skills/index.json`
- update `skills/index.json` when category, maturity, side-effect level,
  supporting files, validation expectations, or portability notes change
- update only affected skill versions according to the independent version rules
- update `schemas/skill-registry.schema.json` when registry field structure or
  allowed values change
- update README tables when the public skill list, categories, or install
  guidance changes
- update docs when policy or authoring expectations change
- run `python scripts/validate_skills.py --require-denylist` after changes to skills, docs,
  registry metadata, schema, or README links

If no automated validation covers a release-policy change, manually check local
Markdown links and confirm no skill content changed unintentionally.
