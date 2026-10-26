# Local workflow tools

These standard-library Python tools work on selected local packages and Git
state. The examples use synthetic names. They need Python 3.10 or newer and Git.

## Install and verify selected skills

Run from a checkout of this library:

```bash
python scripts/install_skill.py diagnose --dry-run
python scripts/install_skill.py diagnose tdd
python scripts/install_skill.py diagnose tdd --verify
python scripts/install_skill.py diagnose --overwrite
python scripts/install_skill.py --category review-audit --target /path/to/skills --dry-run
```

The default target is `~/.agents/skills`. A positional name selects exactly that
registry package; several names select several packages. `--category` explicitly
selects all packages in one category. Only selected package directories are
copied, including supporting files and empty directories. Python runtime caches
(`__pycache__`, `*.pyc`, and `*.pyo`) are excluded consistently from copying,
content verification, receipts, and the source-modified indicator. Other ignored
files remain package content; this is not a general `.gitignore` exclusion.
The repository itself,
registry, and unrelated packages are not installed. Package symlinks are rejected.

`python scripts/list_skills.py` shows each skill's independent registry version.
Install plans and successful installs identify packages as `name@version`.
Versions apply to the complete package, including references and scripts; see
[release policy](release-policy.md) for increment rules. Installation always uses
the current checkout; skill names do not accept version selectors.

Each install compares source and destination file SHA-256 values and directory
membership. It prepares a copy before replacing an old installation and verifies
the installed copy again. `--verify` performs the same content comparison against
the **current local source**, without writing. Extra destination files also fail
verification. `--dry-run` checks selection, paths, and overwrite eligibility and
prints its plan without creating target, temporary files, or receipts.

Receipts default to a hidden sibling of the target, for example
`~/.agents/.skills-install-receipts/diagnose.json`. Set `--receipt-dir` to choose
another location outside both the discovery target and source packages. Receipts
record `skill_version`, source commit, package path, whether the local package or
registry differs from HEAD (`package_modified` and `registry_modified`), destination,
per-file SHA-256 values, and directory membership. Receipt `version: 1` describes
the receipt format, independently of `skill_version`. A modified-source receipt
identifies copied content by its hashes; the recorded commit alone does not
reconstruct uncommitted content or registry metadata. `registry_modified` covers
the whole registry and can also reflect changes to other skills. Receipts are
local audit evidence, not signatures or a remote trust guarantee.

Existing receipts without `skill_version` remain eligible for verification and
replacement under the same content checks. They acquire a declared skill version
on the next successful install; earlier installations are not assigned versions
retroactively. `--verify` still compares content with the current source, without
changing a receipt or proving that two declared versions are equal. A version
label never bypasses hash verification or local-edit protection.

Existing destinations require `--overwrite`. Replacement is allowed only when
the destination still matches its prior receipt, or an unmanaged destination
already matches the current source exactly. A local edit, deletion, or extra file
blocks replacement even with `--overwrite`. Preserve or reconcile such changes
manually. All selected packages are checked before copying begins, but a group
installation is not an all-or-nothing transaction. A later filesystem failure
can leave earlier packages successfully installed. For one package, a failed
replacement first moves the new copy aside, then restores the previous directory.
Copied Windows read-only bits are cleared only while removing disposable copies.
If recovery itself fails, the original backup is retained outside automatic
cleanup and its path is reported for manual recovery. A successful install can
also retain an obsolete backup with a warning if ordinary backup cleanup fails;
the installer does not change the old backup's permissions to delete it.
Run installs in an idle target;
this utility does not coordinate concurrent installers or editors.

Exit code is `0` on success and `1` on an install or verification failure;
invalid CLI usage returns `2`.

## Inspect commit scope from a task-start snapshot

Before editing a repository, choose a private snapshot path explicitly. In this
library `.manifest/` is ignored; another repository must supply its own ignored
directory or use a path outside its working tree.

```bash
python scripts/check_commit_scope.py start --repo . --snapshot .manifest/scope/task.json

# Edit and stage only after obtaining authority through the normal workflow.
python scripts/check_commit_scope.py check --repo . --snapshot .manifest/scope/task.json --allow docs/guide.md --allow tests/test_guide.py
```

There is no default snapshot location. A tracked or nonignored in-repository
snapshot path is rejected, as is a Git administrative directory. `start` uses
exclusive creation and will not replace an earlier snapshot. The private JSON
records starting HEAD, staged and unstaged binary-capable Git patches, existing
nonignored untracked paths and their SHA-256 values. Ignored files and directories
are recorded by name only; their contents are not read for the baseline. It may contain sensitive local content;
keep it private and remove it according to your local retention policy.

`check` inspects the current index, which defines the proposed next commit. Each
`--allow` is an exact repository-relative file path, with forward slashes; there
are no directory, recursive, or wildcard grants. Renames are inspected as a
deletion plus addition and require both paths. Files left only in the working
tree are not part of the staged candidate.

The JSON result lists staged paths, extra paths, baseline HEAD, current HEAD,
and a SHA-256 of the inspected staged patch. It fails when staged paths are
outside the allowlist, HEAD changed, conflicts exist, or nothing is staged.
It also requires review whenever a staged path was already staged, modified, or
untracked at task start, or lies in an existing ignored directory. This includes
later force-staged ignored files; a collapsed ignored-directory entry requires
conservative review for any staged descendant. That overlap is deliberately **ambiguous**, even if the
task later changed a different line or reverted the earlier edit. The tool does
not infer authorship or approve overlapping hunks. Compare the saved baseline
patches with the current staged patch and resolve ownership manually. Starting
a new snapshot after edits would erase the useful baseline and is not evidence
that the earlier content belongs to the task.

The tool never stages, commits, resets, checks out, or changes Git configuration.
Git optional index writes are disabled. `start` writes only the explicitly
requested snapshot and its parent directories; `check` writes no files. Run in
an idle worktree and recheck immediately before committing: output describes the
inspected index, not future edits. The tool requires an existing HEAD commit;
unborn repositories, overlapping-path attribution, and concurrent editing need
manual handling. Snapshot files are trusted local evidence, not tamper-proof
attestations. Scope checks do not grant commit authority or replace tests,
public-hygiene validation, or clean-room review.

Exit codes: `0` for a created snapshot or passing scope check, `1` for scope or
attribution issues requiring review, `2` for invalid usage or an operational error.

The behavior tests create only neutral temporary Git repositories; they do not
read private working repositories or conversation artifacts.
