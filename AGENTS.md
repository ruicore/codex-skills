# Public Repository Boundary

Everything tracked by this repository, including examples, tests, commit
messages, file paths, and Git history, must be safe for unrestricted public
distribution.

Private work repositories, employer or customer systems, conversations,
tickets, logs, screenshots, datasets, and internal documents may be used only
to identify general capabilities, engineering invariants, authorization
boundaries, and failure modes. They are not source material for public content.

When private practice informs a skill:

- use a clean-room implementation written from the abstract capability;
- use neutral or synthetic domains, actors, data, fixtures, and examples;
- do not copy, translate, lightly rename, or structurally mirror private code,
  prose, schemas, workflows, topology, filenames, identifiers, or artifacts;
- never include employer, customer, internal product, repository, service,
  issue, host, URL, account, or environment identifiers;
- retain public third-party product names only when they are necessary to use
  the public tool or API correctly;
- keep private source material and private identifier lists under ignored local
  storage, never in a commit.

Before committing, run
`python scripts/validate_skills.py --require-denylist`. Before pushing,
configure the repository hook with `git config core.hooksPath .githooks` and
maintain the private local denylist at
`.manifest/public-hygiene-denylist.txt`. The pre-push check must inspect every
commit being introduced to the remote, even when the final tree no longer
contains the prohibited material.

Tracked public content must be regular UTF-8 text. Do not add symlinks, screenshots, PDFs,
archives, Office documents, databases, dumps, or other binary assets. If a
future public skill genuinely requires a generated media asset, establish a
separate reviewed allowlist and metadata-cleaning workflow before adding it.

If public safety cannot be established without relying on private context,
exclude the material and ask the user for direction. Do not weaken or bypass a
public-hygiene check to complete a commit or push.
