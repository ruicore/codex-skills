# Delegation For Complex Issues

Read this reference before spawning sub-agents for a Feishu issue investigation.

## When Delegation Helps

Use sub-agents when at least two independent evidence streams can progress in parallel, especially when the issue:

- crosses multiple repositories;
- includes substantial screenshots, logs, configurations, or project data;
- requires version/commit ancestry analysis separate from code tracing;
- has several plausible root causes;
- needs an independent validation design or adversarial review;
- concerns caches, concurrency, model pools, global state, or lifecycle boundaries.

Skip delegation for a narrow single-file issue, a strictly serial investigation, a blocked browser gate, or work that would contend for one mutable production service, GPU, or dataset.

## Sequence

The primary agent must first:

1. complete the preferred in-app Browser login and permission gate, or record why a native external browser fallback was required;
2. establish the exact single-issue or batch scope from rendered issue identifiers;
3. establish the hard read-only Feishu boundary and local write roots;
4. establish read/write and remote-operation boundaries;
5. capture the current repository and worktree state without changing it.

Only then delegate bounded tasks.

For multiple issues, read-only acquisition may run in parallel through the Codex in-app Browser only when every worker has all of the following: one assigned work-item ID, its own agent-created tab or independently controlled tab handle, a `pageAssets` bundle directory returned by that worker's own call, a distinct verified issue evidence root, and no use of a shared download path. Each worker must confirm the bug work-item title or name and its relevant rendered detail fields or narrative, write its issue brief with source-label provenance, promote only proven issue assets, validate them, and clean only its exact bundle directory. Sharing the authenticated profile is acceptable; sharing a tab, bundle directory, final issue root, or download event is not.

If any worker must use a normal download event that writes into a general Downloads directory, serialize those downloads across the coordinated investigation: keep at most one outstanding download, promote and validate it, complete guarded cleanup and the stability recheck, then start the next. This applies to native external browsers and to an in-app Browser fallback that uses the same shared directory. Do not rely on browser-generated suffixes such as `(1)` to establish ownership.

After local evidence has been separated by issue, sub-agents may analyze different issues, repositories, versions, logs, or hypotheses in parallel. For in-app Browser acquisition, the isolation unit is the assigned issue, an independent tab/control handle, a unique returned `pageAssets` bundle, and a distinct final evidence root; a separate authenticated browser profile is not required. Separate final issue directories alone are not sufficient isolation.

A version-baseline agent may map rendered build evidence to branches, commits, and ancestry before any checkout decision. The primary agent keeps ownership of the final target ref and checkout/worktree choice after reviewing that evidence.

## Useful Assignments

- **Version baseline:** map screenshot/build evidence to branches, commits, ancestry, and fix presence.
- **Code path:** trace entrypoints, ownership, ordering, cache/state lifetime, and configuration overlays.
- **Artifacts and timeline:** inspect downloaded logs/configurations and reconstruct the event sequence.
- **Validation design:** define exact acceptance signals, fixtures, runtime requirements, and gaps.
- **Independent challenge:** try to disprove the leading explanation using the authoritative brief and raw evidence paths, without receiving the preferred conclusion when independence matters.

Choose only roles that add distinct evidence. Do not create agents merely to mirror an organization chart.

## Primary-Agent Responsibilities

Keep these with the primary agent:

- browser fallback selection, shared-download coordination, and final interpretation of conflicting issue evidence;
- Git status, target-ref, and worktree decisions;
- permission and scope interpretation;
- task partitioning and production-file ownership;
- resolution of conflicting reports;
- final synthesis and evidence-strength claims;
- remote mutations, commits, pushes, and merge requests.

All agents must keep Feishu issue access read-only under this skill. Sub-agents must not submit issue forms, add comments, upload attachments, change issue state, stash, checkout the shared worktree, reset, push, publish, or modify a remote system. Feishu mutation cannot be delegated within this skill.

## Shared Filesystem Discipline

All agents may see the same files. Avoid overlapping writes. If implementation is authorized:

- assign each production file to one agent;
- serialize changes that share an interface or invariant;
- keep private fixtures and customer data in ignored evidence storage;
- have the primary agent inspect the combined diff and rerun cross-file validation.

## Output Contract

Ask each sub-agent to return:

```text
Task scope:
Confirmed facts:
Evidence locations:
Inferences:
Competing explanations:
Validation performed:
Unverified items:
Files changed:
```

Missing output is not PASS or FAIL evidence. Do not replace an assigned independent validator with the primary agent's opinion. When reports conflict, inspect the cited primary evidence rather than averaging or voting.
