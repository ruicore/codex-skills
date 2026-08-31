# Browser acquisition

Read this when downloading through a browser or resolving media omitted by a
document export. Use the selected browser's installed skill and runtime API as
the authority for supported actions. The notes below are decision rules, not a
stored automation session or a guarantee about current UI labels.

## Discover the content surface

Inspect the document body, outline, media blocks, and export controls. Avoid
collecting unrelated sidebar assets as illustrations. Do not omit images in
comments if comments are in scope; otherwise state the boundary. Native Markdown
can reference assets that still need separate download, and its availability does
not imply that every embedded object is represented.

Classify each rendered item before choosing an action:

| Item | Acquisition route | Evidence to retain locally |
|---|---|---|
| Ordinary image | Open its image viewer and original-size control, then download | Occurrence, asset identity, file dimensions and digest |
| Board or diagram | Enter the board, inspect export choices, export native content | Export option, complete canvas/selection coverage, raster/vector checks |
| Embedded sheet or interactive object | Inspect that object's supported export separately | Native export or an explicitly limited fallback |
| External page illustration | Use the linked image or actual source observed on the page | Source-page relationship, original-size file |

Double-clicking a document image or board may enter a larger view. In other UI
modes, one click opens the viewer and a second click changes it again. Inspect
the result instead of repeating double-clicks blindly. Do not click blank board
space or type in the cloud editor; those actions may create or edit content.

## Verify a preview before saving it

Treat each save as a transaction tied to one illustration:

1. Locate the source occurrence using current DOM or visual evidence.
2. Open the viewer. Observe its item position, asset identity, and loaded image.
3. Select actual size/original/100% when offered. **Then reacquire** the image
   element, source, completion state, and intrinsic dimensions; pre-zoom values
   may describe a thumbnail.
4. Wait until the loaded source corresponds to the selected item. A counter or
   accessible name can update before the actual bytes. Require a corroborating
   identity relationship from the current page or verify a native download against
   the selected image. `complete=true` by itself is insufficient.
5. Save, decode the local file, compute its digest, and associate it with the
   occurrence. Distinguish transient preview dimensions from actual file dimensions.
6. Advance only after the result is recorded. On resume, inspect the current
   position; never assume the viewer restarted at its first item.

Gallery traversal can cover many ordinary images without repeatedly returning to
the document body. Establish its relationship to document order first. Boards and
embedded objects may be absent, while repeated pictures may create extra positions.
A count mismatch is a reconciliation problem, not a reason to drop unmatched items.

## Download attribution

Prefer the application's native download. Register a documented download listener
before clicking when the browser supports one. Use a dedicated task download area
when supported; otherwise compare a narrow before/after file inventory and verify
the candidate's stable size and content. Do not choose whichever file happens to
be newest when another task or the user could be downloading at the same time.

Some exports produce files without a download event. Confirm a completed file
through the supported browser/file surface rather than assuming the event is the
only proof of success. Never consume partial download files.

If native export is permitted but transport fails, consult the browser's current
documented capabilities. Saving an already loaded, DOM-observed resource is a
possible fallback only when supported and allowed by the application. For example,
a documented CDP capability may expose `Page.getResourceTree` and
`Page.getResourceContent`; the resource must belong to the observed page/frame and
match the current image. Do not invent endpoints, alter signed resource URLs,
invoke hidden application APIs, issue arbitrary authenticated fetches, or read
session storage. This fallback must never bypass disabled export permissions.

## Boards and long documents

Inspect native export choices rather than retaining a document thumbnail as the
board's best representation. Choose a large/original PNG when available; keep a
vector PDF when it provides scalable lines or extractable text and fits the user's
retention policy. Verify the selected region includes the intended diagram.

Preserve application watermarks and attribution. A new export may have different
margins or theme colors; compare labels and connections before accepting it as the
same content. A PDF containing a low-resolution bitmap is not automatically better.

For long or virtualized pages, use current outline links, visible block locators,
or moderate scrolls inside the actual document pane. Reinspect after layout changes,
horizontal table movement, reloads, or viewport resizing. Avoid enormous scroll
gestures and hard-coded toolbar coordinates. Keep batches below tool timeouts.
Recover a stale tab through the selected browser's documented tab API; do not
change browser families to work around a failure.

## Public product references

These official sources establish product capabilities and permission distinctions;
inspect the live UI for current export labels and sizes.

- [Feishu Markdown export](https://www.feishu.cn/content/article/7644456827538820052):
  Markdown export can retain image/attachment links that require asset retrieval;
  comments are not part of that export.
- [Feishu diagram downloads](https://www.feishu.cn/hc/zh-CN/articles/980918978289-%E5%9C%A8%E6%96%87%E6%A1%A3%E4%B8%AD%E6%8F%92%E5%85%A5%E6%B5%81%E7%A8%8B%E5%9B%BE%E5%92%8C-uml-%E5%9B%BE):
  diagram download requires document download permission.
- [Feishu board overview](https://www.feishu.cn/content/6-super-simple-efficiency-enhancing-tips):
  boards support image and PDF export.
