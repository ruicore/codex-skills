# Public Sanitization Policy

This document defines public repository hygiene rules for `codex-skills`.

The repository is allowed to evolve from real personal engineering practice.
Sanitization should make that practice safe to publish without stripping away
the concrete constraints that make a skill useful.

## Scope

Use this policy when adding or editing public repository content, including
skills, references, examples, scripts, README entries, docs, templates, and
generated artifacts that may be committed.

This policy does not require editing existing skills by itself. Apply it when a
future issue touches a file or asks for a public-readiness review.

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

The following material can appear in the public repository when it has been
sanitized and still helps explain the workflow:

- personal workflow names
- example repository names
- tool-specific operating notes
- fictional examples

Sanitized material should be safe for a public reader to see and useful for a
future Codex agent to follow. Prefer neutral examples, synthetic data, scoped
placeholders, and short portability notes over removing every concrete detail.

Tool-specific notes are acceptable when they describe real operating behavior:
commands, preflight checks, confirmation boundaries, validation steps, or failure
modes. They should not expose private accounts, private URLs, private data, or
credential material.

## 3. Project-Specific References

Project-specific references are not automatically wrong. Handle them based on
the intended maturity and reuse boundary of the skill or document.

### Intentionally Personal Skills

Keep project-specific references when the skill is intentionally personal and
the reference is needed to preserve the workflow's meaning.

Requirements:

- mark the skill or note as personal, local, or practice-derived
- remove or replace private identifiers
- avoid presenting local assumptions as universal requirements
- keep mutation or publishing operations behind explicit confirmation rules

### Portable Workflows

Replace project-specific references with placeholders when the workflow is meant
to be portable.

Examples:

- use `<repo>` instead of a private repository name
- use `<ticket_url>` instead of an internal issue link
- use `<service_name>` instead of a customer or employer system name
- use `<account_id>` instead of a real external account identifier

The placeholder should preserve the shape of the workflow. If the distinction
between a repository, service, account, ticket, or environment matters, keep that
distinction in the placeholder.

### Transitional Skills

Add portability notes when a skill is moving from personal practice toward a
portable workflow but still contains local assumptions.

A good portability note states:

- which detail is local or practice-derived
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

When a concrete detail is unsafe to publish, sanitize the detail. When it is too
local for portable reuse, classify it or add an adaptation note. Remove it only
when it is both unsafe and unnecessary to the workflow.

## 5. Checklist For Future Skill Edits

Before committing a future skill edit, check:

1. Have the relevant existing files been read before editing?
2. Does the change preserve current skill behavior unless a behavior change was
   explicitly requested?
3. Are all secrets, API keys, credentials, private URLs, private data, raw logs,
   and sensitive identifiers absent?
4. Are examples synthetic, neutral, or clearly sanitized?
5. Are personal workflow names and tool-specific notes safe to publish?
6. Are project-specific references intentionally kept, replaced with
   placeholders, or explained with portability notes?
7. Does any placeholder preserve the operational meaning of the original
   workflow?
8. Has grounded, concrete workflow language been preserved where it protects
   reliability?
9. Did the edit avoid unrelated renames, restructures, taxonomy changes, and
   broad abstractions?
10. Did validation run where available?
11. If validation is unavailable or not applicable, were manual checks stated?

The preferred outcome is a repository that is safe to publish and still honest
about the real engineering practice that produced the skills.
