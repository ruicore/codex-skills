# Agent Metadata

`skills/*/agents/openai.yaml` is optional discovery metadata for agent-facing
interfaces. A skill does not need this file to be valid or useful.

Add or edit this file only when there is a concrete discovery or interface
reason. Do not create `agents/openai.yaml` across every skill just for
uniformity.

## Expected Shape

When a skill has `agents/openai.yaml`, it should include this minimal shape:

```yaml
interface:
  display_name: "Skill Display Name"
  short_description: "Short discovery description"
  default_prompt: "Use $skill-name to perform the workflow."
```

Required `interface` fields:

- `display_name`: human-readable skill name for discovery surfaces.
- `short_description`: concise description of the work the skill performs.
- `default_prompt`: starter prompt that invokes the exact `$skill-name` and
  preserves the skill's existing workflow semantics.

Additional top-level keys are allowed when they describe real, existing
interface behavior. Keep them small and skill-specific.

## Registry Relationship

`skills/index.json` uses `agents_metadata_path` to point at the metadata file
when one exists. Use `null` when the skill has no `agents/openai.yaml`.

Do not add metadata files only to avoid `null`. The registry describes the
current skill package; it is not a requirement that every skill expose the same
files.

## Editing Rules

- Preserve current skill behavior unless the issue explicitly changes it.
- Keep prompts concrete and aligned with the corresponding `SKILL.md`.
- Do not include secrets, credentials, private URLs, raw logs, customer data, or
  sensitive identifiers.
- Fix missing required `interface` fields when a metadata file already exists.
- Avoid broad prompt rewrites or naming changes unless local evidence shows the
  current metadata is misleading.

Run `python scripts/validate_skills.py` after changing agent metadata.
