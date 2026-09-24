---
name: new-session
version: 1
description: "Work out which project in the knowledge base a session is about, right at the start, instead of leaving Claude blind to it until the user opens the exact folder or spells out a path. Use this skill whenever a new Claude Code session begins in this Obsidian-vault knowledge base and it isn't yet obvious which project (or product area) is meant — for example 'let's continue working on the knowledge base documentation', 'let's pick up where we left off', 'continue working on Sign-up', or any first message that doesn't already name a project. Also trigger on explicit invocations: 'new session', '/new-session', 'which project am I in', 'let's start', 'what are we working on'. Scans the real 1-Projects/ folder structure directly — never a CLAUDE.md routing table, which can drift stale — lists active projects grouped by product area, offers a 'not working in a project' option for vault-wide work, and falls back to checking 4-Archives/ for something that should be reactivated. If the vault has no projects at all yet, hands off to new-project-setup instead of showing an empty list."
---

# New Session

At the start of a session, Claude only knows the folder it was opened in. If that's the whole vault rather than one project's folder, there's nothing to tell it which of many active projects the user means — and guessing wrong wastes a round trip. This skill closes that gap: it looks at what's actually in `1-Projects/` right now, offers it back as a short list, and loads whichever one the user picks.

## Folder map

This skill assumes the default knowledge base layout: `1-Projects/` for active work, `4-Archives/` for retired work. Before doing anything below, check the root `CLAUDE.md` for a folder map. If it names these areas differently, use those names throughout instead of the ones written here.

## What this skill does

0. Scans `1-Projects/` directly to build the list — not the Vault Navigation table, which can point at folders that moved or were archived
1. If there are no projects yet at all, asks before handing off to `new-project-setup`
2. Skips the list entirely if the opening message already names a project or says it's not project work
3. Otherwise shows the list as plain numbered text, grouped by product area, most recently active first
4. Loads the chosen project's `CLAUDE.md` and `MEMORY.md`, or falls back to `4-Archives/` if what the user wants isn't in the active list
5. Can be re-run any time mid-session to switch

---

## Step 0 — Scan the active projects

Look inside `1-Projects/` and build the list from the folders that are actually there, not from anything written in the root `CLAUDE.md`'s Vault Navigation table — that table is a curated summary and can lag behind the real folder structure.

- List each top-level product-area folder (e.g. `Cashback Card`, `Insurance`).
- A folder only counts as a pickable entry — area or sub-project — if it has its own `CLAUDE.md` directly inside it. That's what separates a real project/area from a resource folder like `Wiki/`, which is a symlink into the shared content repo, not a project, and should never appear in the list.
- A folder under `1-Projects/` that has real content but no `CLAUDE.md` (started before this skill existed, or set up by hand) fails that test too — but don't drop it silently. Note it once, after the list, as something that looks like a project but isn't set up yet, so the user knows it's missing rather than assuming it doesn't exist.
- If a product-area folder has a `CLAUDE.md` of its own (area-wide work, not tied to one sub-project — e.g. `Insurance/CLAUDE.md`), list the area itself as a pickable entry, separate from its sub-projects.
- Sort areas, and sub-projects within each area, by most recent modification time (the folder's own mtime, or its `MEMORY.md`'s if that's more reliable) — most recent first. The project the user is most likely to mean should be near the top, not buried alphabetically.

## Step 1 — If there are no projects yet

If `1-Projects/` doesn't exist, or exists but has no folder that passes the "has its own `CLAUDE.md`" test from Step 0, don't show an empty picker and don't assume the user wants to set one up. Say plainly that there's nothing there yet, then ask:

> "No projects set up yet — want to set one up?"

Only on yes, hand off to `new-project-setup` — and phrase that handoff as an explicit "set up a new project" request (not as something inferred in passing), so `new-project-setup`'s own Step 0 doesn't stop to ask the same confirmation a second time.

If the user says no, carry on without a project loaded, the same way Step 3's "not working in a project" outcome works below.

## Step 1a — Check whether the opening message already answers this

Before showing anything, check whether the user's own first message already settles the question — either by naming a project directly ("continue working on Sign-up"), or by saying outright that they're not working on a project right now ("just checking my Tasks list", "not project work today"). If it does, skip straight to the matching outcome in Step 3 instead of making them read a list they've already answered. Only fall through to Step 2 when the opening message leaves it genuinely open.

## Step 2 — Show the list

Don't use the `AskUserQuestion` tool here — it caps out at a handful of options, and this list is meant to keep working as the vault grows to many areas and sub-projects. Print a plain grouped, numbered list in the reply instead:

```
0. Not working in a project
1. Cashback Card
   1a. Cancellation Journey Review
   1b. Inactive Users
   1c. Sign-up
2. Insurance
   2a. Boiler and Home Cover promo FY27Q2
3. UX Team Knowledge Base Starter
9. Not listed — check Archives
```

Ask the user to reply with a number/letter or just the project's name.

## Step 3 — Handle the reply

**A project or area (e.g. `1b`, or "Inactive Users"):** read that folder's `CLAUDE.md` and `MEMORY.md`. If either is missing, say so plainly and continue anyway — a missing file is a gap to flag, never an error to block on. Confirm to the user what got loaded before moving on to whatever they actually asked for.

**"Not working in a project" (`0`):** acknowledge it and load nothing project-specific. Continue normally — vault-wide and Area-level work (Tasks, Research Repository, Company Knowledge, and so on) still works exactly as the root `CLAUDE.md` already routes it; this skill doesn't change that.

**"Not listed — check Archives" (the last item):** ask for the name or a keyword, then search `4-Archives/` case-insensitively for a match — the same lookup `new-project-setup` already does in its A1a/B1a steps when checking whether something should be reactivated rather than recreated. If a match turns up, ask whether this is that project restarting. If yes, follow `new-project-setup`'s existing restore steps exactly rather than re-deriving them here — move the folder back to `1-Projects/`, log the reactivation and date, and update its `Status` field — then load it as normal per the first bullet above. If no match turns up, say so and offer the same "want to set one up?" question from Step 1.

**Anything unrecognised:** ask again. Don't guess which project was meant — a wrong guess costs more than one more question.

## Step 4 — Switching mid-session

Nothing special to do here. Because this is just a slash command, running it again later in the same session re-scans and re-asks, letting the user switch projects whenever they want.
