---
name: figma-craft
version: 1
description: >
  Execution-level craft for building and editing screens or components in Figma —
  a set of hard-won gotchas around effect styles, frame fills, Hearth component
  quirks, and semantic colour choices. Use this skill whenever doing hands-on Figma
  design or build work — creating instances, editing components, assembling
  proposals or mockups — regardless of which underlying Figma tool or skill is
  driving the actual calls (figma-use, figma-generate-design, etc.). This is a
  companion layer on top of those tools, not a replacement: it holds properties of
  Figma and Hearth that are true in anyone's file, not the "how is this specific
  file organised" knowledge that varies from file to file — see `figma-dev-handoff`
  Step 0 for discovering a file's own conventions instead.
---

# Figma Craft

A set of execution mistakes that are easy to repeat because they're silent — the
Plugin API doesn't throw when you get them wrong, so the only signal is a screenshot
that looks subtly off. These all trace back to one property: the Plugin API almost
never errors on a wrong value. A default that's wrong, a property that's silently
unwired, a fill you forgot to clear — all of these run clean and only show up as a
screenshot that's subtly wrong. Treat "the script completed without error" as no
signal at all about whether the result is correct.

Read this alongside whichever tool-level skill is doing the actual work
(`figma-use`, `figma-generate-design`, `figma-code-connect`, etc.) — this skill
doesn't replace those, it adds the judgment calls they don't cover. It also pairs
with `figma-dev-handoff` for the ordered componentise-and-handoff workflow, and with
a personal or team design-principles reference (wherever one exists) for UX/product
judgment calls that go beyond execution.

## Check effect styles, not just variants and text

When replicating an existing Figma card or component in a new file, explicitly
inspect `effectStyleId` on the source node — not just its variant properties
(`componentProperties`) and text styling. Effect styles (shadows, blurs) don't show
up when inspecting component properties or text, and they're easy to miss visually
too, especially at small render sizes. Fetch `effectStyleId` and cross-check with
`figma.getStyleById()` alongside variant and text matching, before treating
discovery as complete. Don't let a screenshot that "looks right" substitute for the
explicit check.

## Holding frames get no fill

A frame created purely to group or lay out design elements — a row of card
instances, for example — should have no background fill (`frame.fills = []`).
Auto-layout frames default to a white fill, which is easy to leave in place by
accident. The rule of thumb: if the frame's job is to hold design content, clear the
fill; if the frame's job is to present written notes, commentary, or tables, a fill
is fine and often clearer.

## Hearth Icon Container at SM-32 only wires Icon-20

Hearth's "Icon Container" component exposes two instance-swap properties —
`Icon-20#...` and `Icon-24#...` — on every variant. But at `Size=SM-32`, only the
`Icon-20` slot is actually wired to a visible node. Setting `Icon-24` at that size
runs without error but has no visual effect — the container keeps rendering
whatever `Icon-20` defaults to, which is very unlikely to be the icon you intended.

At `SM-32`, always set the icon via `Icon-20#...` using the **20px variant** of the
icon (e.g. `Celebration-20`, not `Celebration-24`). If only a 24px version of the
icon exists, check for a 20px sibling in the same icon family before assuming you
have to force it through the 24 slot. More generally: whenever a container exposes
more than one same-purpose instance-swap property, don't trust that setting one of
them worked just because the call didn't throw — screenshot the actual rendered
result before calling an icon swap done.

## Set every property explicitly — don't trust inherited defaults

When creating or importing a component instance via `use_figma`, don't assume an
unset property will default to something sensible. After creating or swapping an
instance, review its *full* `componentProperties` set — not just the one property
you meant to change — and set each one deliberately: variant colours, sizing modes
(e.g. `layoutSizingHorizontal`), anything with a default that could silently carry
through unexamined. "The script ran without error" is not confirmation; a wrong
default doesn't throw.

## Pick tint shades for visible contrast, not for matching the lightest weight

When choosing a shade from a colour scale to tint a UI element — an icon container
background signalling positive/negative, for example — judge the shade by contrast
against what it actually sits on, not by whether a lighter shade exists and
technically fits a pastel aesthetic. It doesn't need to clear an accessibility
contrast bar if the colour isn't load-bearing for understanding, but it does need to
be identifiable at a glance — that's a real bar, just a lower one than AA. Pick the
lightest shade that still clears "can I tell this is green/red at a glance on its
real background," and don't default to the palest available option just because
it's the safest-looking choice.

## Hearth Color Scheme is product-tagged, not decorative

Hearth's card and icon container components expose a `Color Scheme` variant with
options like `Pig`, `Highlight`, `Energy`, `Broadband`, `Mobile`, `Insurance`,
`Cashback`. These read as **product associations**, not a neutral decorative
palette — applying `Energy` to unrelated content implies a product connection that
isn't real.

For single-product or generic content, default to `Pig`. Never leave `Color Scheme`
on an unexamined default — it's exactly the kind of property the "set everything
explicitly" rule above covers. If a view ever needs two distinct colours, avoid
pairing `Cashback` and `Pig` together — they're visually similar enough that using
both reads as an inconsistency rather than a deliberate choice.

## Annotations belong to a node, and don't follow it into an instance

An annotation is attached to one specific node. Componentise a screen and place a
fresh instance and the annotation stays on the master — the instance comes back with
nothing on it. Nothing errors, so the first sign is a developer asking where the
notes went.

Before relying on either behaviour, check what the file actually does: find a feature
that's already dev-ready and compare a master against one of its instances. Files
organised around a masters-and-instances convention usually annotate the
**instances** on the journey page, leaving the masters clean, because that's where
developers look — but confirm from the file rather than assuming. If you're running
the full componentise-and-hand-over sequence, use the `figma-dev-handoff` skill —
it's built around capturing annotations first and restoring them last.

## Replacing a text node's contents flattens its formatting

Assign a new string to a text node's `characters` and the whole block takes on the
style of its **first** character — size, weight, colour. A block that had a large
heading on line one and small body text under it comes back all at heading size.
Nothing errors, and the API response looks fine.

This bites hardest on notes panels and multi-line spec blocks, which are exactly the
places where mixed sizes are the point.

Two ways round it:

- **Change only the part that changed.** Insert and delete character ranges rather
  than assigning the whole block — the surrounding characters keep their own styling.
- **If the whole block must be replaced**, record where each size and weight starts
  and stops before the write, then re-apply those ranges afterwards.

Either way, screenshot the block after writing. This failure is invisible in the API
response and unmissable on screen.

A block that needs several sizes is often several text nodes wearing one node's coat.
If you're fighting to preserve ranges, check whether splitting it is the cleaner fix.

## Figma escapes straight quotes in annotation labels

Write a `"` (character 34) into an annotation and read it back and you get `&quot;`.
The same goes for `&`. Nothing warns you, and the entity is what a developer sees.

Use typographic quotes instead — `“ ”` and `’` — which are stored exactly as typed
and read better in Dev Mode. After writing annotations, scan the labels for `&quot;`,
`&amp;` and similar, since this is easy to introduce and invisible until someone
reads the note.

## Writing an annotation invalidates nearby node handles

After setting `annotations` on a node, handles you collected in the same scan can go
stale, and inside slot content the node ids shift outright. Reading `.name` on the
node you just wrote to can throw even though the write itself succeeded.

So capture anything you need to report *before* the write, then re-fetch the root and
re-walk to find the next target. Writing one annotation per pass is slower and worth
it. Related: the slot's own id segment drops out of descendant id paths once a screen
is converted, so a path-based lookup needs a fallback — an index path from the screen
root, or a name-plus-position match.

## combineAsVariants doesn't lay anything out

It groups components into a set and nothing more. Each variant keeps whatever canvas
position it happened to have, so a set can come out thousands of pixels wide and tall
with the variants scattered inside it — technically correct, visibly broken.

After combining, position the variants deliberately, then copy the layout settings
(direction, spacing, padding, sizing modes) from a set that's already right in the
same file so the set hugs its contents and matches its neighbours.

## createComponentFromNode wraps an instance but converts a frame

On a `FRAME` it converts in place: same children, same paths. On an `INSTANCE` it
wraps, giving you a component containing that instance. The wrap is usually what you
want, because the link to the underlying Hearth component survives — but it adds a
level, so anything addressing nodes by path (annotations especially) shifts down by
one. Check the child count before and after if you need to be sure which happened.

## An "unloaded font" error means just that — not "this font doesn't exist"

The Plugin API throws two different errors that are easy to conflate. `The font
family "X" does not exist` means the font genuinely isn't available. `Cannot write
to node with unloaded font "X"` — or an `appendChild`/`insertChild` complaining about
an unloaded font somewhere in the subtree — means the font is real but hasn't been
loaded with `figma.loadFontAsync()` in *this* script yet. The second one is routine
housekeeping, not evidence of a broken or fake font.

**Wrong:** hitting an "unloaded font" error while trying to move or edit a node, and
reporting the font itself as corrupted, fake, or a placeholder — especially tempting
when the font name sounds unusual (a display or brand font with a playful name is
still a real font).

**Correct:** before concluding a font is broken, call
`figma.loadFontAsync({ family, style })` on it directly, on its own, and check
whether it resolves. If it loads without error, the font is fine — the original
error was just telling you to load it first. Only trust "does not exist" as evidence
of an actual missing font, and even then, check `figma.listAvailableFontsAsync()`
for a near match before ruling it out entirely.

## Read positions immediately before you move something

Canvas coordinates you read earlier in a session are a guess, not a fact. Pages get
rearranged while you work — by the user in another tab, or by your own earlier steps.
When a workflow depends on putting things back where they were, read x/y in the same
script that moves them, and store the values rather than re-deriving them later.

That covers *stale* coordinates, but there's a second way this goes wrong even with
perfectly fresh data: computing a new node's position as an offset from a **single**
sibling, without checking where every other sibling already sits. Fresh coordinates
from the one neighbour you looked at don't tell you the slot is actually empty — they
only tell you where that one neighbour is.

**Wrong:** placing a new row at `anchorRow.y + anchorRow.height + gap` because that's
where it "should" go relative to the row it's meant to sit next to, without listing
the rest of the siblings first. If another row has already been inserted in that gap,
the new node lands on top of it instead of next to its intended neighbour — nothing
errors, the layers panel just quietly reads out of order.

**Correct:** before positioning a new or moved node relative to one sibling,
enumerate every sibling's current position (`parent.children.map(c => ({id, name,
y}))`) so you can see the whole layout and confirm the target slot isn't already
occupied.

This check is moot, though, if the parent is an **auto-layout frame**
(`layoutMode !== 'NONE'`) — manual `x`/`y` assignment has no effect there at all;
only the child's index in `parent.children` controls where it renders. Reordering an
auto-layout child means moving it through `insertChild`/`appendChild`, which in turn
requires every font in the moved subtree to be loadable first (see above) — a real
dead end if one of those fonts can't load in the plugin environment, in which case
the reorder has to happen by hand in the Figma app instead.
