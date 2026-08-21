# Git Baselines And Worktrees

Read this reference when the issue's tested version differs from the current checkout, Git ancestry matters, the worktree is dirty, or the target version must be run separately.

## Capture State

Before changing a checkout, capture at least:

```text
git status --porcelain=v1 --untracked-files=all
git branch --show-current
git rev-parse HEAD
```

Also detect an in-progress merge, rebase, cherry-pick, revert, or bisect. Record the original branch and commit.

Resolve the target ref from rendered version evidence, repository history, tags, branches, or commit ancestry. Do not invent a ref from a product version string.

## Component Baseline Matrix

Before choosing a checkout or interpreting a same-named symbol, record a compact matrix for every component visible in the issue evidence:

| Component | Rendered build evidence | Precision | Owning repository | Ref resolves | Reported entrypoint present |
|---|---|---|---|---|---|

Use `exact commit`, `tag/version only`, `incomplete`, or `unknown` for precision. An incomplete string such as `1.5.0+` does not select the local `v1.5.0` tag. A discovery or resolve version without component build evidence is a version-level clue, not proof of the deployed commit.

Map the reported product action to its historical owner. If the issue action belonged to client application or a separate middleware at the tested version, do not claim that a similar current processing service symbol is the actual entrypoint. Record unavailable repositories and missing historical ownership as blockers, while still allowing ref-qualified inspection of components that are proven.

## Clean Worktree

A clean worktree may switch directly to the verified target branch or commit without another confirmation. Avoid switching when ref-qualified inspection is sufficient and switching would add no value.

After switching, confirm `HEAD` and the relevant file history. Do not automatically return to the original branch if the task is continuing on the target baseline; report the current checkout instead.

## Dirty Worktree

Do not alter or hide the user's changes.

For static inspection, prefer:

```text
git show <target-ref>:<path>
git grep <pattern> <target-ref>
git diff <target-ref>...HEAD -- <path>
```

When the target version must be installed or executed, create a separate worktree at a safe, explicit path. A detached worktree is appropriate when no branch edits are needed:

```text
git worktree add --detach <separate-path> <target-ref>
```

The primary agent owns worktree creation and target selection. Sub-agents should not create competing worktrees unless explicitly assigned.

Do not automatically stash, commit, reset, discard, clean, force-checkout, or overwrite local changes. Do not remove a worktree containing evidence or modifications without explicit cleanup authority.

## Final Disclosure

If a worktree was created, the final answer must state:

- its absolute path;
- target branch or commit;
- whether it is detached;
- whether it contains changes or generated evidence;
- whether it was retained.

Creation does not require an intermediate approval when the user has allowed this workflow, but any destructive cleanup remains separately authorized.

## Comparing Fix Presence

Establish whether a fix exists in the tested baseline through commit ancestry and the actual diff, not branch-name similarity. Distinguish:

- fix authored;
- fix committed on another branch;
- fix merged into the tested baseline;
- fix present in source but absent from the deployed build;
- behavior controlled by configuration or runtime overlays.

If repository history and the screenshot disagree, report the mismatch rather than choosing one silently.
