# Skill Proposal

Use this template when a captured practice is ready to discuss as a reusable
Codex skill. Keep the proposal grounded in observed behavior. Do not promote the
skill based on formatting alone.

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

## Practice-Derived Details To Keep

List concrete details that should remain because they carry workflow semantics.

- `<detail>`

## Details To Sanitize Or Generalize

| Detail | Treatment | Reason |
|---|---|---|
|  |  |  |

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
