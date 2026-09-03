---
name: figma-dev-handoff
version: 1
description: >
  Turn a working Figma journey page into a dev-ready one: convert loose screens into
  component sets, file them on the file's own master-components page under a feature
  frame, place instances back on the journey page, and keep every engineering
  annotation visible where developers actually read it. Use this skill whenever
  someone asks to "make the file dev ready", "prep this for engineering", "convert
  these screens to components", "componentise these screens", "hand this over to
  dev", or wants loose frames on a journey page turned into proper components — and
  also when they ask to move local components onto the file's local-components page,
  or to tidy a page before handoff. Do not attempt this by hand: the sequence has
  five silent failure modes that destroy annotations or ship mangled text to
  engineers, and this skill exists to catch them.
---

# Figma dev handoff

Load the `figma-craft` skill alongside this one if it's available in the current
surface — it holds naming and organisation conventions where a file has them, plus
general execution gotchas — and `figma-use` for the Plugin API itself. This skill
holds the ordered workflow for getting a journey page into a state engineering can
build from. If `figma-craft` isn't available, carry on — but expect to work out the
file's conventions from the file itself rather than having them handed to you, which
is exactly what Step 0 below does.

## Read this before you touch anything

**Annotations do not flow from a component to its instances.** They are attached to
a specific node and they stay there. If you componentise a screen and place a fresh
instance, the annotations travel with the master and the instance comes back blank.

This is the single most destructive thing about the job, because nothing errors —
you just quietly hand engineering a page with no notes on it. So the workflow is
built around capturing annotations first and re-applying them last.

Verify this in the file you are working in rather than trusting the claim. Pick a
feature that is already dev-ready, find a master with annotations and an instance of
it, and compare. Files organised around a masters-and-instances convention usually
show the opposite of what you would expect: the masters are clean and the annotations
live on the journey-page instances. That tells you where the team reads them, which
is the answer that actually matters.

## Before starting: agree the shape

Three things need the user's sign-off before any write, because they are expensive
to undo:

1. **Grouping.** One component set per screen with `State` variants, or standalone
   components per screen? Match whatever the file already does. Show them the
   mapping of screens to variants and let them correct it — they will spot a missing
   scenario faster than you will.
2. **Variant names.** Take these from the page's own scenario labels, not from your
   own description of the screen. If the page says "Invalid form submission", the
   variant is `State=Invalid form submission`. A developer reading the set should see
   the same words as the person who wrote the spec.
3. **Adding a frame to the file's master-components page.** That page drives every
   other page in the file. Adding to it is higher-stakes than anything else here, so
   flag it and wait.

Also agree where annotations should end up — on the instances, on the masters, or
both. Follow the file's existing habit unless told otherwise.

## Step 0 — Discover, and copy conventions rather than inventing them

Every file has its own dialect. Find the page that holds master components or
component sets — commonly named something like `Core Views`, `Components`, or
`Master`, but confirm from the file itself rather than assuming — and find a feature
on it that is already done. Read its settings: the feature frame's layout mode,
spacing and padding; a component set's layout settings; the variant property names
it uses. Copy those exact values. A set that does not match its neighbours looks
broken even when it works.

Then list the screens on the journey page and note which are `FRAME` and which are
`INSTANCE`. That distinction changes what happens in step 3.

## Step 1 — Capture every annotation to disk

Walk each screen and record, for every annotated node:

- the full annotation text
- the node's **id suffix** (the id with any leading `I` stripped)
- the node's **index path** from the screen root (the sequence of child indices)
- the node's name and type, and which screen it came from

Save that outside Figma and report the count to the user. Two independent ways to
find the node again matters because the id path is not stable across this workflow
(see step 6) — when one fails the other rescues it.

**Verify:** the count you saved matches the count on the page.

## Step 2 — Create the feature frame on the master-components page

Name it for the feature, taken from the journey page name with the emoji and channel
stripped: `🟠 Cancel CBC (web)` gives `Cancel CBC`. Copy the layout settings from the
model frame you read in step 0. Place it in clear space, well below existing content.

**Verify:** the page's top-level child count went up by exactly one and nothing moved.

## Step 3 — Convert screens to components, one set at a time

Do one set, verify it, then start the next. A mistake in the first set is cheap; the
same mistake replicated across four sets is not.

**Read each screen's x/y immediately before converting it, and store them.** Journey
pages get rearranged while you work — by the user, in another tab, mid-session. A
position you read twenty minutes ago is a guess. These coordinates are what step 5
uses to put the page back.

Two behaviours to expect from `createComponentFromNode`:

- On a **FRAME**, it converts in place. Children and annotation paths are unchanged.
- On an **INSTANCE**, it **wraps** it — you get a component containing that instance.
  The link to the underlying component survives, which is what you want, but every
  annotation inside gains a level, so index paths shift down by one.

Name each component with its full variant string (`State=…, Channel=Web,
Device=Desktop`) before combining. Those names become the variant names.

Then combine them into a set — and know that **`combineAsVariants` tidies nothing**.
It leaves each variant wherever it sat on the canvas, so a set can come out thousands
of pixels tall with the variants scattered inside it. Lay the variants out yourself
in a deliberate order, then apply the layout settings you copied in step 0 so the set
hugs its contents.

**Verify:** variant names, property definitions, the set's dimensions, and the
annotation count inside the set.

## Step 4 — Move the sets into the feature frame

Append them in journey order, not creation order. Someone reading the
master-components page should see the flow left to right.

**Verify:** child order, and that the annotation total across the frame still matches
step 1.

## Step 5 — Place instances back on the journey page

Create an instance of each variant and put it at the coordinates you stored in step
3. The scenario labels, badges and section headers on the page are still sitting
where they were, so correct coordinates make the page reassemble itself.

**Verify:** every instance is at its recorded position with its expected size, and
screenshot a sample.

## Step 6 — Re-apply the annotations, then clear the masters

This step has three traps in it, and all three are silent.

**Straight quotes get escaped.** Figma stores `"` in an annotation label as `&quot;`.
Write character 34 and read it back and you will see the entity. The fix is to use
typographic quotes (`“ ”` and `’`), which are stored exactly as typed and read better
in Dev Mode anyway. Check for `&quot;`, `&amp;` and friends after writing, because
this is how mangled notes reach engineers.

**A write invalidates surrounding node handles — and re-fetching the root inside the
same script is not enough.** On a screen that was *wrapped* (one converted from an
instance), writing an annotation poisons the subtree for the rest of that execution:
the next traversal throws `get_children: Node with id … not found` even though you
re-fetched the root first. Re-running the same work as separate `use_figma` calls
succeeds every time.

So split by how the screen was converted:

- **Converted in place** (was a `FRAME`) — several writes in one script are fine.
- **Wrapped** (was an `INSTANCE`) — one write per script call. Slower, and the only
  thing that reliably works.

Related: reading `.name` on a node you just wrote to can throw even though the write
succeeded, so capture any names you need *before* writing. And don't trust atomicity
here — a script that errors partway has sometimes already persisted its earlier
writes, so check the actual state before retrying rather than assuming nothing
happened.

**Slot id segments disappear from the middle of the path.** A node addressed as
`…;<card>;<slot>;<content>;<child>` before conversion sits at
`…;<card>;<content>;<child>` afterwards — the slot's own segment is gone, and it can
be gone from more than one place in the same path.

The fix is to match on the **tail** of the path — the last two or three segments,
which are the stable component-internal ids — rather than the whole suffix. Keep the
index path as a second fallback, and a content match (find the text node whose
characters start with a known string) as a third. In practice tail-matching resolves
nearly everything.

Then tally what actually landed and compare against step 1.

Once — and only once — the instances are confirmed correct, clear the annotations
from the masters if the file's convention is instances-only. Clearing a master does
not touch its instances, which is the same independence that caused the problem at
the start.

**Verify:** total on instances matches the expected count, no HTML entities anywhere,
and the per-screen distribution is what you agreed.

## Step 7 — File the local components

Any component still sitting loose on the journey page belongs on the file's
local-components page. Decide where by asking whether it could serve another
feature:

- **Used by, or plausibly useful to, more than one feature** → the file's global or
  shared frame (often named something like `Global`).
- **Specific to this feature** → a new frame named for the feature, matching the
  naming you used on the master-components page.

Moving a component between pages does not break its instances.

Before moving anything, apply the test that comes first: **does this need to be a
component at all?** Figma slots accept arbitrary content, so a frame that fills a
slot exactly once does not need to be a component — making it one just creates a
name to collide with and a master to drift from. Componentise when something is used
more than once. See `figma-craft` for the naming rules that follow from this, where
the file has them.

**Verify:** the component's instances still resolve, and the screens that use it
still render.

## Step 8 — Final pass

Screenshot every screen on the journey page and confirm nothing changed visually.
Confirm no components are left loose on the page. Report the annotation count one
last time.

## What to tell the user at the end

Give them the set ids, the frame locations, the annotation count, and — importantly —
anything you could not finish. Deleted Figma nodes sometimes leave orphaned fragments
that the API refuses to remove; say so plainly rather than letting them discover it
later.
