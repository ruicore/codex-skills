# Public Sanitization Policy

This document defines public repository hygiene rules for `codex-skills`.

The repository is allowed to evolve from real personal engineering practice.
Sanitization should make that practice safe to publish without stripping away
the concrete constraints that make a skill useful.

## Scope

Use this policy when adding or editing public repository content, including
skills, references, examples, scripts, README entries, docs, templates, and
generated artifacts that may be committed.

Apply this policy to every new or changed public file and to every commit being
introduced to a public remote. Existing content does not create an exception.

## 1. Material That Must Never Appear

The public repository must never contain:

- secrets
- API keys
- credentials
- private customer or project data
- raw private logs
- private URLs
- sensitive identifiers

Examples include passwords, tokens, session cookies, private keys, account IDs,
internal hostnames, real customer names, private issue links, internal dashboard
links, production request bodies, unsanitized stack traces, and raw exports from
private systems.

Do not keep real sensitive values as "examples." Replace them with clear
placeholders such as `<api_key>`, `<customer_name>`, `<private_url>`,
`<project_id>`, or `<internal_hostname>`.

## 2. Material That Can Appear If Sanitized

The following material can appear when it is independently written for public
use and still helps explain the workflow:

- neutral or synthetic workflow and repository names
- public tool-specific operating notes
- fictional examples

Sanitized material should be safe for a public reader to see and useful for a
future Codex agent to follow. Prefer neutral examples, synthetic data, scoped
placeholders, and short portability notes over removing every concrete detail.

Tool-specific notes are acceptable when they describe real operating behavior:
commands, preflight checks, confirmation boundaries, validation steps, or failure
modes. They should not expose private accounts, private URLs, private data, or
credential material.

## 3. Private Sources And Clean-Room Derivation

Employer, customer, and internal project material may establish that a general
capability or engineering invariant matters. It must not be converted directly
into public repository content. Public work derived from that experience must
be written clean-room from the abstract capability, using unrelated or
synthetic terminology, actors, data, fixtures, and examples.

Do not copy, translate, lightly rename, or structurally mirror private code,
prose, schemas, workflows, topology, filenames, identifiers, or artifacts. A
project name replaced with a generic noun is not sufficient when the surrounding
material still reproduces the private project.

Public third-party product, protocol, library, and API names may remain when
they are necessary for correct use. Employer, customer, internal product,
repository, service, issue, host, URL, account, and environment identifiers may
not remain, even in a skill described as personal or practice-derived.

Use placeholders only when the operational role matters:

Examples:

- use `<repo>` instead of a private repository name
- use `<ticket_url>` instead of an internal issue link
- use `<service_name>` instead of a customer or employer system name
- use `<account_id>` instead of a real external account identifier

The placeholder should preserve the generic role, not a private implementation's
distinctive structure. If a useful rule cannot be expressed without private
context, exclude it from the public repository.

Portability notes may explain public tool assumptions or which generic role an
adopter must substitute. They must not preserve private provenance.

Use this mandatory authoring boundary:

1. Capture private practice only in ignored `.manifest/skill-intake/` storage.
2. Reduce it to an abstract capability, invariants, authorization boundaries,
   and failure modes.
3. Close the private material before public authoring begins.
4. Design an unrelated public or synthetic domain, actors, terminology, data,
   fixtures, filenames, workflow expression, and tests.
5. Have an independent reviewer assess the public draft without access to the
   private source or a private-to-public mapping.

Public issues, proposals, review notes, and commit messages must not identify or
summarize the private source. The private derivation record remains ignored.
Use `docs/clean-room-review.md` for the required semantic-independence review.

Tracked public content must be regular UTF-8 text. Symlinks, binary files, and non-UTF-8 content
are rejected by default, including screenshots, PDFs, Office documents,
archives, databases, dumps, and opaque generated artifacts. Introduce a future
binary asset only after a separate reviewed allowlist and metadata-cleaning
workflow exists; do not bypass the scanner for an individual file.

A good portability note states:

- which public tool or generic role is environment-specific
- what a future adopter should substitute
- which behavior must stay unchanged for the workflow to remain reliable

Do not hide the transition by rewriting the skill into vague generic language.

## 4. How Not To Over-Generalize

Public hygiene is not the same as de-personalizing every workflow.

Do not:

- rewrite a grounded skill into vague generic language
- remove concrete constraints that make the workflow reliable
- delete practice-derived steps only because they mention a specific tool
- broaden triggers beyond observed use
- rename, split, merge, or restructure skills for polish alone
- replace operational checklists with abstract advice
- invent generic examples that no longer exercise the real workflow

Concrete constraints are often the point of a skill. Preserve steps that protect
against known failure modes, define confirmation boundaries, enforce read-only
passes, identify validation commands, or prevent unsafe mutations.

When a concrete detail comes from private work, extract only the capability or
invariant and express it independently. Classification or an adaptation note
does not make a private identifier or implementation safe to publish.

## 5. Checklist For Future Skill Edits

Before committing a future skill edit, check:

1. Have the relevant existing files been read before editing?
2. Does the change preserve current skill behavior unless a behavior change was
   explicitly requested?
3. Are all secrets, API keys, credentials, private URLs, private data, raw logs,
   and sensitive identifiers absent?
4. Are examples synthetic, neutral, or clearly sanitized?
5. Are tool-specific names limited to necessary public third-party products?
6. Was any private source reduced to abstract capabilities and invariants before
   clean-room writing began?
7. Does every placeholder preserve only a generic operational role rather than
   a private implementation's distinctive structure?
8. Has grounded, concrete workflow language been preserved where it protects
   reliability?
9. Did the edit avoid unrelated renames, restructures, taxonomy changes, and
   broad abstractions?
10. Did `python scripts/validate_skills.py --require-denylist` run successfully
    with the private local denylist available?
11. Was every commit in the proposed push range scanned, including intermediate
    commits whose prohibited content was later removed?
12. If validation is unavailable or not applicable, were manual checks stated?
13. Was the private extraction note kept under ignored `.manifest` storage and
    closed before public authoring began?
14. Did an independent semantic review confirm that domain, actors,
    terminology, data, fixtures, filenames, and workflow expression were
    independently designed?

The preferred outcome is a repository that is safe to publish and still honest
about the real engineering practice that produced the skills.
