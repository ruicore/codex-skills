## Public Safety Gate

- [ ] I kept private intake and derivation records under ignored `.manifest` storage.
- [ ] Public content was written from an abstract capability in a clean-room process.
- [ ] Domain, actors, terminology, data, fixtures, filenames, workflow expression, and implementation were independently designed or justified by cited public sources.
- [ ] An isolated reviewer applied `docs/clean-room-review.md` without private source material or a private-to-public mapping.
- [ ] The review outcome is `pass`; any public-facing rewrite requirement is resolved.
- [ ] `python scripts/validate_skills.py --require-denylist` passes locally.
- [ ] The complete introduced commit range passes protected public-hygiene scanning.
- [ ] No screenshots, PDFs, Office files, archives, databases, dumps, or other unreviewed binary assets are included.

Public PR checks without the private denylist are not an authoritative approval.
The repository owner must complete the protected local gate before merge.

## Change Summary

Describe only the public capability and public artifacts changed. Do not record
private provenance or a private-to-public mapping.

- What changed:
- Public capability or problem addressed:

## Scope

- Intended category:
- Maturity level:
- Side-effect level:
- Non-goals:

For tiny fixes, it is fine to keep this section to "no category, maturity, or
side-effect change."

## Repository Surface

- Examples added or intentionally deferred:
- Registry/schema updates:
- Docs updates:

## Validation Evidence

- Automated validation:
- Manual or semantic review:
- Skipped checks and reason:
