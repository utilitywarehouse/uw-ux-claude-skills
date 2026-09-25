---
name: new-project-setup
version: 15
description: "Set up a new project from scratch. Use this skill when someone says \"new project\", \"start a project\", \"set up a project\", or mentions starting something new. The skill confirms it's actually new (checking for an existing or archived folder first), asks a few focused questions, then either sets up a new top-level product area (with a Wiki shared with the team by default) or a sub-project within an existing area — so the workspace is ready to go immediately."
---

# New Project Setup

Sets up a new project folder inside `1-Projects/` and populates the core documents from the user's answers. Branches based on whether this is a new top-level product area or a sub-project within an existing one.

## Folder map

This skill assumes the default knowledge base layout: `1-Projects/` for active work, `4-Archives/` for retired work. Before creating anything, check the root `CLAUDE.md` for a folder map. If it names these areas differently, use those names throughout instead of the ones written below.

## What this skill does

0. Confirms this is actually a new project, if not already explicit
1. Asks whether this is a top-level product area or a sub-project
2. Asks a few focused questions based on the answer
2a. Checks for an existing or archived folder with that name before creating anything
2b. For a new product area, checks whether its Wiki should be shared with the team (default: yes) and links it into the shared repo if so
3. Creates the folder structure
4. Writes the appropriate CLAUDE.md file(s)
5. Writes a populated MEMORY.md (sub-projects only)
6. Updates the Routing Map

---

## Step 0 — Confirm this is a new project

If the user explicitly asked to set this up ("new project", "start a project", "set up a project"), skip straight to Step 1.

Otherwise — if this skill triggered because someone mentioned starting something new in passing (a feature, an initiative, a piece of work) rather than asking for setup directly — confirm first:

> "Sounds like this might be a new project — want me to set up a folder for it?"

Only proceed past this point if they say yes.

## Step 1 — Ask the project type

Use the `AskUserQuestion` tool with a multiple-choice prompt:

> "Is this a new top-level product area, or a sub-project within an existing one?
>
> - **Top-level product area** — a whole product you'll be working on long-term (e.g. Insurance, Energy, Broadband)
> - **Sub-project** — a specific piece of work within an existing product area (e.g. a research study, a feature redesign)"

Never name a specific existing product area in the question or its options, and never mark either option "Recommended" — present both options neutrally, exactly as scripted above, regardless of what product areas already exist in the vault.

Then follow the appropriate branch below.

---

## Branch A — Top-level product area

### A1 — Ask the questions

Gather the following before creating anything:

- **Product area name** — what should the folder be called? (e.g. Insurance, Energy)
- **Design lead** — who owns this area?
- **PM** — who's the product manager?
- **One-line description** — what is this product area about?

### A1a — Check for an existing or archived folder

Before creating anything:

1. Check whether `1-Projects/[Product Name]` already exists. If it does, this isn't a new area — tell the user and point them to the existing folder instead of creating anything.
2. Search `4-Archives/` for a folder matching [Product Name] (exact or close match, case-insensitive). If found, ask: "Found an archived product area called '[X]' in 4-Archives/ — is this that one restarting, or a genuinely new area?"
   - If restarting: move the archived folder back to `1-Projects/`, preserving its existing content — don't create a fresh structure. Append a line to `Wiki/log.md` noting the reactivation and today's date. Then skip to A6.
   - If genuinely new: proceed to A2.
3. If neither exists, proceed to A2 without comment.

### A2 — Create the folder structure

New wikis are shared with the team by default (decision #31 in the Build Plan) — that's the whole point of the shared repo growing on its own, rather than needing a deliberate decision every time someone starts a new product area.

**Ask whether to keep this one local-only.** Use `AskUserQuestion`, defaulting to shared:

> "This wiki will be shared with the team by default, in the shared `uw-knowledgebase-content` repo — the same way the Cashback Card and Brand and Design System wikis work. Keep it shared (recommended), or keep this one local-only?"

- **Shared (default):**
  1. **Check access.** Same check as `setup-my-knowledge-base`'s Step 5: run `git ls-remote https://github.com/utilitywarehouse/uw-knowledgebase-content.git`. Succeeds → continue. Fails on access (or the check can't run cleanly — fall back to asking directly): don't block project setup over this. Tell them plainly that sharing isn't available right now (missing access), fall through to the **Local-only** branch below instead, and mention they can come back once access is approved.
  2. **Check for a name clash.** Two people could independently start the same product area. Reuse or clone `uw-knowledgebase-content` (suggest `~/Documents/Github/uw-knowledgebase-content`, outside the knowledge base, same convention as `setup-my-knowledge-base`) and check whether `[Product Name]/Wiki/` already exists there. If it does, this isn't a new wiki — treat it like A1a's "restarting" case: tell the user, and symlink in the existing shared wiki instead of creating a duplicate.
  3. **Create the Wiki inside the clone**, not inside the knowledge base: `<clone>/[Product Name]/Wiki/` (empty for now — A4 and A5 below populate it).
  4. **Symlink it in:** `1-Projects/[Product Name]/Wiki` → `<clone>/[Product Name]/Wiki`. Use a real symlink (`ln -s`), never a macOS Finder alias — a Finder alias only resolves from Finder itself, while a symlink is transparent to every tool that reads or writes through it, including the steps below.
- **Local-only:** create `1-Projects/[Product Name]/Wiki/` directly, as a normal folder. Nothing shared, nothing pushed anywhere.

Either way, also create:

```
1-Projects/[Product Name]/CLAUDE.md
```

### A3 — Write the parent CLAUDE.md and Wiki/Area-Conventions.md

This step writes two files, not one: the product-area half goes to `1-Projects/[Product Name]/CLAUDE.md`, and the Wiki half goes to `Wiki/Area-Conventions.md` (inside the Wiki folder set up in A2 — already the shared clone if the Wiki is shared, so this file is part of the same commit/PR as the rest of the new Wiki).

**If the Wiki is shared** (per A2), insert this section directly after `## Purpose` in the file you write:

```markdown
## This content is shared

This Wiki is not local to one person's knowledge base. It lives in the `utilitywarehouse/uw-knowledgebase-content` repo, cloned locally by each contributor and linked into their own knowledge base via a symlink.

**Pull before editing, every time, without being asked.** Before changing anything under `Wiki/`, resolve it to the real clone it's symlinked from and run `git pull` there first — someone else may have merged a change since this knowledge base last synced. Do this automatically; don't rely on the person remembering.

After editing, the change goes up as a pull request from that clone — never a direct push, and never a self-merge.
```

Skip this section entirely if the Wiki ended up local-only.

Read `assets/product-area-claude-md-template.md` and write its content verbatim to `1-Projects/[Product Name]/CLAUDE.md`, substituting `[Product Name]` throughout.

Read `assets/area-conventions-template.md` now and write its content verbatim to `Wiki/Area-Conventions.md`, substituting `[Product Name]` throughout. If the Wiki is shared, also insert the "This content is shared" section above directly after `## Purpose`. The `## Page format` block is already fenced in the template — copy it exactly as written.

### A4 — Write Wiki/index.md

Read `assets/wiki-index-template.md` and write its content verbatim to `Wiki/index.md`, substituting `[Product Name]` throughout.

### A5 — Write Wiki/log.md

Read `assets/wiki-log-template.md` and write its content verbatim to `Wiki/log.md`, substituting `[Product Name]` throughout and today's date for `[today's date]`.

A4 and A5 write through the `1-Projects/[Product Name]/Wiki/` path either way — if A2 set that up as a symlink into the shared clone, the files land there automatically, no special handling needed.

### A5a — Push the new wiki, if shared

Skip this step if A2 ended up local-only (either by choice or because access wasn't there).

Also copy `1-Projects/[Product Name]/CLAUDE.md` (written in A3) to `<clone>/[Product Name]/CLAUDE.md`, so the next teammate who sets up their own knowledge base finds a starter CLAUDE.md waiting next to the Wiki, instead of an empty folder. It's already generic — A3 never writes anything personal to this person into it — so it needs no stripping before it goes up. `Wiki/Area-Conventions.md` needs no separate copy step — A3 already wrote it straight into `<clone>/[Product Name]/Wiki/`, so it's already there alongside the rest of the new Wiki, in the same commit and PR.

Branch off `main` in the shared repo clone, commit the new `[Product Name]/Wiki/` folder and that `CLAUDE.md`, push, and open a pull request against `uw-knowledgebase-content` — same rule as everywhere else this repo is touched: never push to `main` directly, and never merge the PR. Tell the user the wiki works locally right away (the symlink resolves immediately), and that it's now up for review in the shared repo before the rest of the team can see it.

### A6 — Update the Routing Map

Add a new row to the "Routing Map" table in the root `CLAUDE.md` so future sessions load it automatically.

Place it among the other product-area rows — the ones sitting directly under `1-Projects/` — in alphabetical order by folder name (e.g. "Insurance" goes before "Sign-up"). Leave every system/resource row above that block untouched.

### A7 — Confirm

Tell the user:
- The product area folder has been created
- Where it lives and what's inside
- Whether the Wiki is shared with the team or local-only, and if shared, that it's live locally now but waiting on PR review before the team sees it
- That the Wiki is ready to grow as they add sources
- Next step: use `new-project-setup` again to add the first sub-project

---

## Branch B — Sub-project

### B1 — Ask the questions

Gather the following before creating anything:

- **Product area** — which existing product area does this live under? (e.g. Insurance, Cashback Card)
- **Project name** — what should the sub-project folder be called?
- **PM** — who's the product manager?
- **Deadline** — when does this need to wrap up?
- **The problem** — one or two sentences: what are we trying to figure out or solve?
- **The outcome** — what does a successful end result look like?
- **Research method** — Qualitative, Quantitative, Mixed, or None/not yet decided?

Don't ask for more than this upfront. Everything else gets filled in as the project develops.

### B1a — Check for an existing or archived folder

Before creating anything:

1. Check whether `1-Projects/[Product Area]/[Project Name]` already exists. If it does, this isn't a new sub-project — tell the user and point them to the existing folder instead of creating anything.
2. Search `4-Archives/` for a folder matching [Project Name] (exact or close match, case-insensitive — an archived sub-project may not sit under the same [Product Area] path it started in, so search broadly). If found, ask: "Found an archived project called '[X]' in 4-Archives/ — is this that one restarting, or a genuinely new project?"
   - If restarting: move the archived folder back to `1-Projects/[Product Area]/`, preserving its existing content — don't create a fresh structure. Append a log entry to its `MEMORY.md` noting the reactivation and today's date, and update its `Status` field. Then skip to B5.
   - If genuinely new: proceed to B2.
3. If neither exists, proceed to B2 without comment.

### B2 — Create the folder structure

Create the base folders inside `1-Projects/[Product Area]/[Project Name]/`:

```
01-Inputs/
02-Planning/
03-Research/
04-Competitive/
05-Synthesis/
06-Deliverables/
```

Then create subfolders based on the research method:

**Qualitative:**
```
01-Inputs/Meeting transcripts/
01-Inputs/Interview transcripts/
03-Research/Transcripts/
03-Research/Discussion Guides/
03-Research/Stimulus/
```

**Quantitative:**
```
01-Inputs/Meeting transcripts/
01-Inputs/Survey data/
```

**Mixed (Qualitative + Quantitative):**
```
01-Inputs/Meeting transcripts/
01-Inputs/Interview transcripts/
01-Inputs/Survey data/
03-Research/Transcripts/
03-Research/Discussion Guides/
03-Research/Stimulus/
```

**None / not yet decided:**
```
01-Inputs/Meeting transcripts/
```

### B3 — Write CLAUDE.md

Read `assets/sub-project-claude-md-template.md` and write its content verbatim to the project folder as `CLAUDE.md`.

### B4 — Write MEMORY.md

Read `assets/sub-project-memory-template.md` and write its content verbatim to the project folder as `MEMORY.md`, substituting the user's answers and today's date throughout.

### B5 — Update the Routing Map

Add a new row to the "Routing Map" table in the root `CLAUDE.md` so future sessions load it automatically.

Find the parent product-area row, then insert the new row directly under it, in alphabetical order relative to any existing sibling sub-project rows for that same area. If the parent has no sub-project rows yet, insert directly below the parent row.

### B5a — Link back from wherever the project came from

New projects almost always start life as a line in a daily note, a task, a meeting transcript, or a Slack message the user pasted in. That origin note usually holds context that never makes it into the project folder — who's involved, what triggered it, what the user's first instinct was. Once the project exists, nothing points at that origin any more and it becomes unreachable.

So before confirming, find the origin and connect the two:

1. Ask the user where this came from, or search `0-Inbox/` and `2-Areas/Tasks.md` for the phrases they used when describing the project.
2. Add a `**Related:** [Project MEMORY](path/to/MEMORY.md)` line to that origin note, using the actual relative path to the new project's `MEMORY.md`. Append it rather than rewriting the captured text — raw capture is worth preserving exactly as the user typed it.
3. If the origin note contains a fact the project folder doesn't have (names of people assigned, a deadline, a ticket reference), surface it to the user and offer to add it to `MEMORY.md`. Don't move it silently; the user decides what's project state and what's just a passing thought.

If the project genuinely has no traceable origin, say so and move on. A wrong link is worse than no link.

### B6 — Confirm

Tell the user:
- The project folder has been created
- Where it lives
- What subfolders were created (and why, if the research method drove the decision)
- That they're ready to start — next step is usually adding sources to `01-Inputs/` or filling in scope and timeline
