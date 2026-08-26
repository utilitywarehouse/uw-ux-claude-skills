---
name: new-project-setup
version: 4
description: "Set up a new project from scratch. Use this skill when someone says \"new project\", \"start a project\", \"set up a project\", or mentions starting something new. The skill confirms it's actually new (checking for an existing or archived folder first), asks a few focused questions, then either sets up a new top-level product area (with Wiki) or a sub-project within an existing area — so the workspace is ready to go immediately."
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

Create the following inside `1-Projects/[Product Name]/`:

```
CLAUDE.md
Wiki/
Wiki/index.md
Wiki/log.md
```

### A3 — Write the parent CLAUDE.md

Write this file to `1-Projects/[Product Name]/CLAUDE.md`:

**Fence the `## Page format` block in the file you write.** It contains placeholder links (`[wiki-links](wiki-links.md)`, `[related-concept-1](related-concept-1.md)`, `[page-name](page-name.md)`) that are illustrations, not real targets. Left unfenced they become live broken links once opened in a linked-notes tool, and clicking one can create an empty note. Wrap that block in a ```` ```markdown ```` fence in the generated file, the same way it's fenced here.

```markdown
# [Product Name]

This is the shared workspace for all [Product Name] projects.

## Folder structure

[Product Name]/
  CLAUDE.md       ← this file
  Wiki/           ← shared knowledge base across all projects
  [Project Name]/ ← one folder per project
    CLAUDE.md
    MEMORY.md
    01-Inputs/    ← source documents for that project (immutable — never modify)
    02-Planning/
    03-Research/
    04-Competitive/
    05-Synthesis/
    06-Deliverables/

## Starting a session

1. Check memory and context to determine which project is active. If it's clear, state it and proceed. If it's ambiguous or memory is absent, ask the user to confirm before continuing.
2. Navigate to that project folder and read its CLAUDE.md.
3. You're ready to respond to the initial question or task.

---

# Wiki

A shared knowledge base maintained across all [Product Name] projects.

## Purpose

The wiki is the canonical store for [Product Name] product knowledge — concepts, hypotheses, entities, research findings, and competitive intelligence. It compounds over time. Project-specific status, decisions, and actions belong in project MEMORY.md files, not here.

## Default behaviour

- Before answering any question about [Product Name], read `Wiki/index.md` and any relevant pages. If the answer is there, use it. If it's not, say so clearly.
- When searching for context or background, treat the wiki as the first port of call — before project folders or memory.
- When the user shares new information about the product, a stakeholder, or a concept — even in passing — offer to add it to the wiki.
- When a question generates a valuable answer not already in the wiki, offer to save it as a new page.

## Ingest workflow

When the user adds a new source to a project's `01-Inputs/` and asks you to ingest it:

1. Read the full source document
2. Discuss key takeaways with the user before writing anything
3. Create a summary page in `Wiki/` named after the source
4. Create or update concept pages for each major idea or entity
5. Add markdown links (`[Page Title](page-name.md)`) to connect related pages
6. Update `Wiki/index.md` with new pages and one-line descriptions
7. Append an entry to `Wiki/log.md` with the date, source name, and what changed

A single source may touch 10–15 wiki pages. That is normal.

## Question answering

1. Read `Wiki/index.md` to find relevant pages
2. Read those pages and synthesise an answer
3. Cite specific wiki pages in your response
4. If the answer is not in the wiki, say so clearly
5. If the answer is valuable, offer to save it as a new wiki page

## Page format

# Page Title

**Summary**: One to two sentences describing this page.

**Sources**: List of raw source files this page draws from, each as a markdown link.

**Last updated**: Date of most recent update.

---

Main content goes here. Use clear headings and short paragraphs.

Link to related concepts using markdown links throughout the text, e.g. `[Related Concept](related-concept.md)`.

## Related pages

- [Related Concept 1](related-concept-1.md)
- [Related Concept 2](related-concept-2.md)

## Citation rules

- Every factual claim should reference its source file
- Use the format `(source: [Source Name](Source%20Name.md))` after the claim, linking the source file rather than naming it as plain text. A plain-text filename doesn't create a link, so the source it points at reads as unconnected even though something cites it
- Always keep the file extension in the link target (`.md`, `.pdf`, whatever the file actually is) — a markdown link points at a real file path, not a page-name lookup
- If `CLAUDE.md`, `MEMORY.md` or `index.md` exists in more than one place in the knowledge base, path-qualify the link so it resolves to the right one, and leave filenames used as ordinary nouns as plain text
- If two sources disagree, note the contradiction explicitly
- If a claim has no source, mark it as needing verification

## Rules

- Never modify anything in a project's `01-Inputs/` folder
- Always update `Wiki/index.md` and `Wiki/log.md` after changes
- Keep page names lowercase with hyphens (e.g. `machine-learning.md`)
- Write in clear, plain language
- When uncertain about how to categorise something, ask the user
```

### A4 — Write Wiki/index.md

```markdown
# [Product Name] Wiki

A shared knowledge base across all [Product Name] projects.

## Pages

_No pages yet. Add pages here as the wiki grows._

## How to use

- Each page covers one concept, entity, or source
- Link between pages using markdown links (`[Page Title](page-title.md)`)
- Update this index whenever a page is added or significantly changed
```

### A5 — Write Wiki/log.md

```markdown
# Wiki Log

A record of all changes to the [Product Name] wiki.

---

- [today's date]: Wiki created.
```

### A6 — Update the Routing Map

Add a new row to the Routing Map in the root `CLAUDE.md` so future sessions load it automatically.

### A7 — Confirm

Tell the user:
- The product area folder has been created
- Where it lives and what's inside
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

Write a lean `CLAUDE.md` into the project folder:

```markdown
## Memory System

At the start of every session, read `MEMORY.md` before responding. Read this to pick up where we left off. Don't announce what you found, just be informed by it. If auto-memory contains relevant project context, reconcile it against the knowledge base's `MEMORY.md` — that file is the source of truth.

When I say "remember this," write the information to `MEMORY.md` in the knowledge base immediately, then mirror it to auto-memory. Confirm you've done both.

**Update it at the end of every session** by appending new entries or updating existing ones. This is how you remember what we've been working on.

**Where things go:** Apply two tests when deciding where to save something. Test 1: Does it prescribe behavior? Look for words like "always," "never," "before doing X, do Y." If yes, add it to this file (CLAUDE.md) under the appropriate section. Test 2: Does it describe a fact about the project that could change? Contact details, project status, decisions, things I've told you to remember. If yes, add it to MEMORY.md. When unsure, suggest which file you think it belongs in and ask me to confirm.

## Transcripts

Raw transcripts (unedited exports from Meet, Zoom, Teams, etc.) live in `01-Inputs/`.

Cleaned transcripts are saved as follows:
- **Meeting transcripts** (internal calls, team meetings): clean in place → `01-Inputs/Meeting transcripts/`
- **Research interview transcripts** (participant sessions): save cleaned version → `03-Research/Transcripts/`

If asked to clean or summarise a transcript, check `01-Inputs/` first for the raw source file.
```

### B4 — Write MEMORY.md

Populate it from the user's answers. Use this structure:

```markdown
# [Project Name]

**Status:** Discovery
**Start:** [today's date YYYY-MM-DD]
**Deadline:** [deadline]
**Design lead:** [designer's name]
**PM:** [PM name]

## The problem

[user's answer]

## The outcome

[user's answer]

## Scope

TBD — to be defined in Week 1.

## Deliverables

TBD

## Timeline

TBD

## Stakeholders

- **PM:** [PM name]
- **Design:** [designer's name]

## Open questions

- TBD

## Log

- [today's date]: Project created.
```

### B5 — Update the Routing Map

Add a new row to the Routing Map in the root `CLAUDE.md` so future sessions load it automatically.

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
