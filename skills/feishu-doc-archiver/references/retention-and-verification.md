# Retention and verification

Read this before replacing or deleting existing archive images. A quality decision
and a duplicate decision are separate: neither can be inferred from dimensions alone.

## Compare candidates conservatively

| Evidence | Permitted conclusion | Required caution |
|---|---|---|
| Same file digest | Byte-identical content | Update all references before removing a copy |
| Same decoded pixels | Potentially equivalent visual content | Check animation, orientation, alpha, color profiles, and necessary metadata |
| Same source/version, visibly complete native original | Candidate replacement for a thumbnail | Check small text and clipped edges; do not trust filenames alone |
| Old image is a crop of a larger original | Shared source, different presentation | Retain the crop intent; not an unconditional substitution |
| Similar appearance or larger dimensions only | No duplicate determination | Compare manually or retain both as unresolved variants |

Native quality is preferable to artificial enlargement. A less compressed export
with more useful detail can be preferable even at the same pixel size. Conversely,
a larger image from a different revision is not a higher-quality copy of the old
revision. Do not conflate cropped screenshots, annotated screenshots, themes,
animations, or alternate document versions.

For confirmed duplicates, choose a canonical physical file and point every
document to it using portable relative references. Cross-document reuse should not
require another identical binary. Keep separate logical occurrence records so
deduplication does not erase coverage or provenance.

## Preserve what the reader sees

When replacing a cropped image with its full source, preserve the crop through
supported presentation metadata if it can be rendered correctly offline. If the
reading format cannot express that crop, either retain a necessary presentation
derivative or switch to the complete image with an explicit note. Do not silently
expand or remove content. Under a strict one-file request, use the full source
plus a crop description/link instead of retaining an unacknowledged second image.

Fix stale width/height constraints when the preferred file has a different aspect
ratio. Check HTML attributes, CSS background images, Markdown image syntax, inline
HTML, `srcset`, linked thumbnails, CSS files, indexes, and machine-readable records.
Full-size links must open the retained asset, not a removed thumbnail or remote URL.

Vector PDF and extracted text can be complementary representations, rather than
duplicate raster files. Keep them only when they serve the requested reading,
search, or fidelity goal. If the user requests one representation total, select
the appropriate primary format and explain any resulting limitation.

## Cleanup transaction

1. Resolve the exact archive root and inventory its current files. Do not infer
   targets from loose names or from the user's general Downloads folder.
2. Produce a reviewable cleanup list: obsolete path and digest, retained path and
   digest, evidence of equivalence/improvement, and references that will change.
   A dry-run list is useful even when cleanup is already explicitly authorized.
3. Confirm every retained target exists, fully decodes, and matches its source.
   Repoint references, render the reading copy, and check replacement content.
4. Ensure removal leaves no active reference to an obsolete path. Historical
   provenance may retain that path as a clearly labeled removed-source record.
5. Recheck that each candidate still has its inventoried digest. Stop for changed
   files, a keeper scheduled for deletion, paths outside the root, or symlink /
   reparse-point escapes. Delete only the enumerated files with an available
   recovery path; avoid wildcard or recursive tree deletion.
6. Revalidate remaining assets and links, refresh counts/checksums, and record what
   was removed and any unresolved variants. A recycle-bin recovery path is preferable
   to a second permanent archive copy when the user wants only high-quality images.

Temporary transport copies, download retries, extracted originals, comparison
crops, and QA contact sheets may also duplicate images. Remove only task-owned
disposable files covered by the cleanup authority. Do not leave a redundant backup
tree and report that only one copy remains.

Native document/ZIP containers can still embed lower-quality copies. Inventory
that distinction explicitly. Do not delete an entire document package merely to
remove one image: verify that text, tables, attachments, or other unique material
have a retained counterpart first. If the scope is strictly image files, preserve
the package and disclose its embedded media rather than claiming archive-wide
deduplication. Never silently rewrite a native source document.

## Quality limitations and completion

Preserve the best available sole copy when export is blocked or the source itself
is blurry. Label its quality and the failed route. A transcription or screenshot
can be useful but is not a new source-quality export; uncertain text must remain
explicitly uncertain.

Report distinct logical illustrations, saved canonical files, repeated occurrences,
removed files/bytes, retained complementary formats, and unresolved exceptions
separately. Verify that every document has a local image or an explicit limitation.
Hash/decode/link checks prove integrity and coverage, not that an AI has accurately
understood every number and word in every picture.
