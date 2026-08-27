---
name: setup-my-knowledge-base
version: 1
description: "Set up a brand-new personal knowledge base from scratch, driven by Claude Code. Use this skill when no knowledge base exists yet and someone says things like \"set up my knowledge base\", \"get me started\", \"I'm new, help me set this up\", or is working through session one of the UX team's onboarding. Creates the core folder structure, turns off Obsidian wikilinks if Obsidian is present, interviews the person for their own About Me note, writes a starter CLAUDE.md and Start here note, then hands off to `new-project-setup` so they leave with one real project, not a demo. Do not use this on a knowledge base that already exists — that's `new-project-setup`'s job instead."
---

# Set Up My Knowledge Base

Builds a new knowledge base from nothing: the core folders, a starter `CLAUDE.md`, a personal `About Me.md`, and a `Start here.md`. Then hands off to `new-project-setup` so the person leaves with one real piece of work started, not an empty shell.

This only runs once per knowledge base — it's the very first skill someone touches. If a `CLAUDE.md` already exists at the location they name, this isn't the right skill; say so and point at `new-project-setup` instead.

## Order matters

The link-style setting has to be handled **before any file is written** — writing files first and fixing the link setting after means redoing everything. Follow the steps in this order.

## Step 1 — Check for Obsidian

Check whether `/Applications/Obsidian.app` exists.

- **Found:** continue to Step 2.
- **Not found:** ask a yes/no question: "Obsidian isn't installed. Want to install it? It makes browsing and linking notes much easier — though the knowledge base works fine as plain markdown folders without it." Use `AskUserQuestion` with Yes/No options, and put the benefit line on the Yes option itself.
  - **Yes:** give them the download link — `https://obsidian.md/download` — and ask them to install it, then say "done" when ready. Once they confirm, repeat this Obsidian check.
    - Found this time: continue to Step 2, and treat Obsidian as present for the rest of this skill (Step 3 applies).
    - Still not found: ask again — "Still not showing up — want to try again, or carry on without it?" Loop as many times as they want to keep trying. The moment they choose to carry on without it, treat that the same as a No answer below.
  - **No:** say once that it's recommended but not required, and that the knowledge base works fine as plain markdown folders in any editor. Continue to Step 2 without Obsidian — never force the install.

## Step 2 — Ask where the knowledge base should live

Ask for a folder path. If they say they already created an empty vault in Obsidian, that folder is the one to use — don't create a new one nested inside it.

## Step 3 — Fix the wikilink setting, if Obsidian is present

Skip this step entirely if Step 1 found no Obsidian.

Check whether `<location>/.obsidian/app.json` exists — that means the folder has already been opened as a vault in Obsidian at least once.

- **It exists:** read the file, set the key `"useMarkdownLinks": true` (this is the actual setting behind the "Use [[Wikilinks]]" toggle in Settings → Files and Links — `true` means Obsidian writes plain markdown links instead of wikilinks), and write the file back with every other key untouched. Tell them this was done automatically.
- **It doesn't exist yet:** the folder hasn't been opened in Obsidian yet, so there's nothing to edit. Ask them to open it as a vault in Obsidian now, then go to Settings → Files and Links and turn off "Use [[Wikilinks]]". Wait for confirmation before moving on — getting this wrong means every file this skill writes next lands in the wrong link style.

## Step 4 — Create the core folder structure

Create this inside the location from Step 2. Nothing beyond this — no extra folders, no placeholder files beyond what's listed:

```
0-Inbox/
1-Projects/
2-Areas/
  Research Repository/
    Studies/
    Reports/
    Topics/
3-Resources/
  About Me/
4-Archives/
```

Write the Research Repository's three starter files from the templates in `assets/research-repository/`:

- `assets/research-repository/claude-md-template.md` → `2-Areas/Research Repository/CLAUDE.md`
- `assets/research-repository/index-template.md` → `2-Areas/Research Repository/index.md`
- `assets/research-repository/log-template.md` → `2-Areas/Research Repository/log.md`

Also copy:

- `assets/design-principles-template.md` → `3-Resources/Design Principles.md`
- `assets/mastering-para-template.md` → `3-Resources/Mastering PARA - The Architect's Guide to Digital Organisation.md`
- `assets/ai-writing-guidelines-template.md` → `3-Resources/AI Writing Guidelines.md`

Copy all six as-is — they're already written for a newcomer.

## Step 5 — Interview for About Me

Use `assets/about-me-template.md` as the question set — it's already written for a newcomer and needs no changes. Walk through it conversationally rather than dumping the whole template as a form; skip anything they say doesn't apply. Write their answers into `3-Resources/About Me/About Me.md`, keeping the template's structure and frontmatter.

## Step 6 — Write the root CLAUDE.md

Copy `assets/claude-md-template.md` to `CLAUDE.md` at the root of the new knowledge base, unchanged. It already carries its own Routing Map and link-style rule — nothing in it needs to be filled in with this person's specifics. The Routing Map is what `new-project-setup` adds a row to every time a new project or area is created, so it stays accurate as the knowledge base grows. The "Personality and preferences" section at the bottom stays blank; that's deliberate, it fills in as you work together over time.

## Step 7 — Write Start here.md

Copy `assets/start-here-template.md` to `Start here.md` at the root, unchanged.

## Step 8 — Hand off to new-project-setup

Tell them setup is done, briefly summarise what now exists (the folders, `CLAUDE.md`, their `About Me.md`, `Start here.md`), and then invoke the `new-project-setup` skill so they turn one real, live piece of work into an actual project — not a demo. That's the point of ending the session this way.

## What this skill deliberately doesn't do

- No update or sync path — this is a one-shot setup. It never re-runs against a knowledge base that already has a `CLAUDE.md`.
- No OKF folder restructuring, and OKF is never mentioned to the person — frontmatter is added to the content files quietly, as a convention, not taught as a concept here.
- No product-specific tag taxonomy in the Research Repository — that table ships blank on purpose, for them to fill in when they run their first real study.
