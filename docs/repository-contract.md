# Repository Contract

This document defines the repository-level contract for `codex-skills`.

It exists to keep future edits grounded while this repository evolves from a
personal Codex skill library into a reusable engineering workflow library.

## 1. Purpose

`codex-skills` stores repeatable Codex engineering workflows: diagnosis,
review, planning, validation, documentation, tool operation, and other
agent-readable procedures that came from real engineering practice.

The repository is not a prompt gallery and not a polished framework. A useful
skill should help a Codex agent perform a concrete kind of work with evidence,
scope control, checkpoints, and validation.

This contract should protect the repository from two opposite failures:

- leaving practice-derived workflows too private, implicit, or unsafe for public
  reuse
- sanding those workflows into generic abstractions that no longer preserve the
  behavior that made them useful

## 2. Target Direction

The long-term direction is a reusable public toolkit of Codex engineering
workflows.

That direction should be reached incrementally:

- preserve proven workflow behavior first
- sanitize and classify practice-derived material before making it public-facing
- add metadata, examples, validation, and portability notes when they clarify
  existing behavior
- generalize only after the repository shows a repeated pattern across skills

Reusable does not mean universal. These skills may continue to encode opinionated
defaults, specific operating disciplines, and practice-derived language when
those details are part of the workflow's value.

## 3. Grounded Evolution Principles

Future changes should follow these principles:

- **Evidence before polish:** edit based on observed skill behavior, repeated
  maintenance needs, user requests, validation failures, or public hygiene risks.
- **Behavior preservation:** existing skill behavior should remain intact unless
  a later issue explicitly asks to change it.
- **Small additive moves first:** prefer new docs, metadata, examples, tests,
  validation, and portability notes before renaming, restructuring, or rewriting
  skills.
- **Practice is signal:** personal or project-derived details may reveal the
  real workflow. Do not remove them merely because they are specific.
- **Contain specificity:** when a detail is useful but local, classify it, mark
  assumptions, or explain how to adapt it instead of pretending it is generic.
- **Reviewable scope:** each change should be understandable from the issue that
  requested it. Avoid opportunistic cleanups across unrelated skills.
- **Validation before confidence:** run available validation after edits. If no
  validation applies, state the manual checks performed.

## 4. Non-Goals

The repository should not try to become these things in the near term:

- a fully generic skill framework
- a complete taxonomy of all possible Codex workflows
- a normalized schema imposed on every existing skill before there is evidence
  that the schema fits
- a marketing-ready package that hides its practice-derived origin
- a place for private project data, credentials, customer details, private URLs,
  raw logs, or sensitive identifiers
- a collection of cosmetic rewrites whose main purpose is consistency rather
  than better agent behavior

Do not rename, flatten, split, merge, or restructure skills just to make the
repository look more polished.

## 5. Personal Practice To Reusable Workflow Lifecycle

Practice-derived material is allowed, but it should move through a clear
lifecycle as it becomes more reusable.

### 1. Personal Practice Seed

A workflow starts as something that worked in a real task, project, tool, or
operating habit.

Acceptable contents:

- concrete steps
- local assumptions
- tool-specific commands
- examples from practice, after sanitization
- opinionated defaults

Expected handling:

- preserve the working behavior
- identify private or brittle details
- avoid presenting local assumptions as universal rules

### 2. Sanitized Practice Skill

The workflow is safe to keep in a public repository, but may still be clearly
personal or project-derived.

Expected handling:

- remove secrets, credentials, private URLs, raw logs, and sensitive identifiers
- replace private examples with neutral or synthetic examples when needed
- keep details that explain the real workflow
- add adaptation notes when a command, tool, or environment assumption is local

### 3. Portable Workflow Candidate

The workflow has enough shape to be reused outside the original context, but it
may still need careful adaptation.

Expected handling:

- separate required behavior from local defaults
- add examples or validation that make the workflow easier to test
- document prerequisites, supported inputs, and expected outputs
- keep original capability intact while broadening wording

### 4. Reusable Public Workflow

The workflow has repeated use, stable behavior, and clear boundaries.

Expected handling:

- keep instructions concise and operational
- maintain validation scripts, examples, or metadata when they exist
- update README or index material only when the public skill surface changes
- avoid expanding the workflow into adjacent responsibilities without a concrete
  repeated pattern

This lifecycle is descriptive, not a required folder structure. Do not add
process overhead unless it helps a specific skill become safer or easier to use.

## 6. Public Repository Sanitization Expectations

All public-facing files should be safe to publish.

Before adding or editing a skill, check for:

- secrets, tokens, API keys, session cookies, passwords, private keys, and
  credential-like placeholders that could be mistaken for real credentials
- private customer, employer, vendor, or project identifiers
- private URLs, internal hostnames, repository paths, issue links, dashboards,
  ticket IDs, and environment names
- raw logs, request bodies, responses, stack traces, screenshots, or datasets
  containing sensitive identifiers
- personal data that is not necessary to understand the workflow
- machine-specific absolute paths in reusable examples

Sanitization should preserve learning value. Prefer neutral substitutions,
synthetic examples, scoped placeholders, or portability notes over deleting the
entire practice-derived section.

If a detail cannot be sanitized without losing the workflow, keep the public
skill narrower and move the private detail out of the repository.

## 7. When Not To Abstract

Do not abstract a skill when:

- there is only one concrete instance of the pattern
- the proposed abstraction would hide important operational steps
- the current specificity is what teaches the agent how to do the work
- a rename would make existing skill behavior harder to recognize
- the change is motivated mainly by visual consistency
- the abstraction would require updating many skills without improving their
  outcomes
- the repository has no validation proving the generalized form still works

Abstraction is appropriate only when it reduces repeated maintenance, clarifies a
real cross-skill pattern, improves safety, or makes validation easier without
changing the workflow's intended behavior.

## 8. How Future Codex Agents Should Use This Contract

Before editing skills in this repository, a Codex agent should:

1. Read this contract.
2. Read the relevant existing skill files, references, scripts, examples, and
   README sections before editing.
3. Identify whether the requested change is behavior-preserving, behavior-
   changing, sanitization-focused, metadata-focused, validation-focused, or
   documentation-only.
4. Preserve existing behavior unless the issue explicitly requests a behavior
   change.
5. Keep practice-derived material when it is useful and safe; classify, contain,
   or add portability notes when it is too local.
6. Avoid broad renames, reorganizations, or schema introductions unless the issue
   asks for them and repository evidence supports them.
7. Check public repository hygiene before finishing.
8. Run available validation. If no validation applies, perform manual checks and
   report them.

When in doubt, prefer the smallest change that makes the current workflow safer,
clearer, or easier for a future Codex agent to use.
