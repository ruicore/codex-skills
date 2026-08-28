# Skill Proposal

Use this template when a captured practice is ready to discuss as a reusable
Codex skill. This is a public clean-room artifact. Draft it from an abstract
capability statement, not from private source material. Do not include a source
task, incident, employer, customer, internal project, or mapping back to private
material. Do not copy, translate, lightly rename, or structurally mirror private
prose, code, schemas, workflows, topology, filenames, fixtures, or examples.

## Proposed Skill

- Name:
- Working directory:
- Primary category:
- Secondary category:
- Proposed maturity:
- Default side-effect level:
- Maximum side-effect level:
- Related existing skills:

## Purpose

What concrete work should this skill perform, and what failure does it prevent?

## Abstract Capability

- Capability:
- Engineering invariants:
- Authorization boundaries:
- Failure modes that must be prevented:

## Independent Public Problem Domain

- Unrelated public or synthetic domain:
- Independently designed actors:
- Independently designed terminology:
- Synthetic data and fixtures:
- Public specifications or official documentation used, if any:

## When To Use

List specific user requests, task shapes, or repository situations that should
trigger the skill.

- `<trigger>`

## When Not To Use

List adjacent work, unsafe cases, missing-input cases, or situations handled by
another skill.

- `<non-goal>`

## Inputs To Infer Or Request

| Input | Infer from | Ask user when | Stop condition |
|---|---|---|---|
| Scope |  |  |  |
| Mode |  |  |  |

## Evidence Hierarchy

1. `<evidence source>`
2. `<evidence source>`
3. `<evidence source>`
4. `<evidence source>`

## Workflow

Write ordered steps. Include branch conditions where the workflow can split.

1. `<step>`
2. `<step>`
3. `<step>`

## Validation Requirements

- Automated validation:
- Manual validation:
- Public sanitization checks:
- Checks that may be skipped, and why:

## Output Contract

The final response or artifact must include:

- `<output requirement>`

## Side-Effect Policy

- Default level:
- Maximum level:
- User instruction required before file edits:
- User instruction required before commits, pushes, PRs, or publication:
- User instruction required before external API writes:
- User instruction required before destructive actions:
- Preview or dry-run requirement:
- Credential handling:
- Rollback or cleanup:

## Failure Modes

| Failure mode | Codex should |
|---|---|
| Required evidence is missing |  |
| Validation fails |  |
| Sensitive data appears in source material |  |
| Target is ambiguous |  |

## Clean-Room Design Declaration

- Private material present in the public authoring workspace: no
- Public draft written from abstract capability only:
- Domain, actors, terminology, data, fixtures, filenames, and workflow expression independently designed:
- Private-to-public mapping included: no
- Structural independence reviewed:
- Reviewer or review method:
- Review result:

## Examples Or Supporting Files Needed

- `examples/`:
- `references/`:
- `scripts/`:
- `templates/`:
- `agents/openai.yaml`:

## Open Questions

- `<question>`

## Recommendation

Choose one:

- Create a new skill directory.
- Keep as proposal until more practice exists.
- Fold into an existing skill.
- Reject as too generic or too private.

Reason:
