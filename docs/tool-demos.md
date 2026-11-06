# Reproduce the workflow tools

Requirements: Python 3.10 or newer, Git, and a checkout of this repository.
No credentials, model calls, external services, or installed personal skills
are needed. From the repository root:

```text
python -B scripts/demo_workflow_tools.py
python -B scripts/demo_workflow_tools.py --demo install
python -B scripts/demo_workflow_tools.py --demo scope
```

The command creates its own temporary directories, calls the real helper CLIs,
checks the results, and removes only its disposable data. It never targets the
user's skill installation or stages changes in the source repository. Output
is JSON containing booleans and selected package metadata, without local paths,
raw receipts, diffs, or logs. Any unexpected behavior makes the command fail.

All demo child processes, including the Python helpers, remove inherited
`GIT_*` overrides and disable global/system Git configuration. The synthetic
commit explicitly disables hooks and signing. This prevents a caller's selected
repository, external index, signing setup, or global hooks from redirecting the
demonstration. Existing repository-local configuration is not rewritten.

## Installation and local-edit protection

The demo installs only `agent-legibility-review` into a temporary target and
checks the receipt's registry version, source commit, and complete file hashes.
It verifies the installed content through the CLI, then modifies that disposable
copy. An overwrite must be refused and the local edit and original receipt must
remain intact. This confirms the tested protection behavior, not that the skill
improves review quality. Receipts are local records, not signed attestations.

Expected result: all installation checks are `true`.

## Commit scope with a pre-existing edit

The demo creates a new synthetic Git repository containing `existing.txt` and
`task.txt`. It changes `existing.txt` before taking the task-start snapshot,
then changes `task.txt` and stages both. The scope check must identify the extra
path and its ambiguous pre-existing content. After unstaging only `existing.txt`
in that synthetic repository, the check must pass for `task.txt`, while the
pre-existing edit remains on disk.

Expected result: the extra path and ambiguity are detected, the narrowed staged
candidate passes, and the pre-existing edit is preserved. The tool does not
attribute individual lines, coordinate concurrent editors, or grant commit
authority. See [full tool contracts](local-workflow-tools.md).

## Interpreting results

The demos test helper behavior, including refusal paths. They do not measure
whether an agent chooses to use the helpers, whether a skill is more effective
than a direct instruction, or whether an unrelated repository is safe to publish.
