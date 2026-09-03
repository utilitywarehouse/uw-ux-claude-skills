---
name: setup-my-knowledge-base
version: 2
description: "Set up a brand-new personal knowledge base from scratch, driven by Claude Code. Use this skill when no knowledge base exists yet and someone says things like \"set up my knowledge base\", \"get me started\", \"I'm new, help me set this up\", or is working through session one of the UX team's onboarding. Creates the core folder structure, turns off Obsidian wikilinks if Obsidian is present, links the person into all of the team's shared content (the Research Repository and every shared product wiki), interviews the person for their own About Me note, writes a starter CLAUDE.md and Start here note, then hands off to `new-project-setup` so they leave with one real project, not a demo. Do not use this on a knowledge base that already exists — that's `new-project-setup`'s job instead."
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
3-Resources/
  About Me/
4-Archives/
```

The Research Repository doesn't get created here — Step 5 links it in from the team's shared repo instead of writing a blank local copy.

Copy these three as-is — they're already written for a newcomer:

- `assets/design-principles-template.md` → `3-Resources/Design Principles.md`
- `assets/mastering-para-template.md` → `3-Resources/Mastering PARA - The Architect's Guide to Digital Organisation.md`
- `assets/ai-writing-guidelines-template.md` → `3-Resources/AI Writing Guidelines.md`

## Step 5 — Link into the team's shared content

The team's shared Research Repository and product wikis live in a separate private GitHub repo, `utilitywarehouse/uw-knowledgebase-content` — not in this knowledge base itself. This step links the new knowledge base straight into that shared content, so the person starts with everything the team has already built (every existing wiki and research finding), instead of an empty shell they'd have to wait to catch up on.

### Check access first

Access has to be approved before this can work. Someone who isn't in the design-team GitHub group and hasn't had an individual "Request access" approved will be blocked — that's expected, not a bug.

Run:
```
git ls-remote https://github.com/utilitywarehouse/uw-knowledgebase-content.git
```

- **Succeeds:** access is confirmed — continue below.
- **Clearly fails on access** (stderr mentions something like "Authentication failed", "Repository not found", or "Permission denied" — GitHub deliberately reports a private repo you can't see as "not found" rather than confirming it exists and denying you): stop here. Tell them plainly: "You don't have access to the shared knowledge-content repo yet. Ask to be added to the `ux-design-team` GitHub group if you're a designer, or use the 'Request access' button on the repo — the repo admin approves these." Skip the rest of this step, but carry on with the rest of setup (About Me, CLAUDE.md, Start here, handoff) — don't block the whole skill on this one piece. Mention they can come back and ask to finish this step once access is approved.
- **The check itself can't run cleanly** (git isn't installed, or the result is genuinely ambiguous — a network or proxy error that isn't clearly about permissions): fall back to asking directly. Use `AskUserQuestion`: "Have you been granted access to the shared knowledge-content repo yet?" with Yes/No options. If yes, continue below and trust their answer — if the clone then fails anyway, report that plainly rather than guessing further. If no, give the same access instructions as above and skip the rest of this step.

### Clone the shared repo

Ask where the clone should live — suggest `~/Documents/Github/uw-knowledgebase-content`, outside the knowledge base folder entirely. It's a separate git repo and must never be git-nested inside the knowledge base (that's what breaks the "no raw git for contributors" design — the linking skill for actually contributing back handles pulling and PRs on their behalf).

- If that folder already exists and is already a clone of this repo, reuse it: run `git pull` to bring it current rather than re-cloning.
- Otherwise, `git clone https://github.com/utilitywarehouse/uw-knowledgebase-content.git` into the folder they chose.

### Link it into the new knowledge base

Use real symlinks (`ln -s`), never macOS Finder aliases. A Finder alias only resolves from Finder itself; a symlink is transparent to every tool that touches the file — Claude Code, `grep`, and other skills like `study-writeup` and `end-session` that read straight through `Research Repository/CLAUDE.md` without knowing (or needing to know) that it's shared.

Walk the clone's actual top-level contents rather than a fixed list, since new shared wikis land in it over time (decision #31) and this step should pick them up automatically:

- The clone's `Research Repository/` folder → symlink to `2-Areas/Research Repository` in the new knowledge base.
- Any other top-level folder in the clone that contains a `Wiki/` subfolder — each one is a shared product area, e.g. `Cashback Card`, `Brand & Design System` — create `1-Projects/<same name>/` if it doesn't already exist, then symlink that folder's `Wiki/` to `1-Projects/<same name>/Wiki`.

Confirm the links resolved by listing one of them before moving on.

## Step 6 — Interview for About Me

Use `assets/about-me-template.md` as the question set — it's already written for a newcomer and needs no changes. Walk through it conversationally rather than dumping the whole template as a form; skip anything they say doesn't apply. Write their answers into `3-Resources/About Me/About Me.md`, keeping the template's structure and frontmatter.

## Step 7 — Write the root CLAUDE.md

Copy `assets/claude-md-template.md` to `CLAUDE.md` at the root of the new knowledge base, unchanged. It already carries its own Routing Map and link-style rule — nothing in it needs to be filled in with this person's specifics. The Routing Map is what `new-project-setup` adds a row to every time a new project or area is created, so it stays accurate as the knowledge base grows. The "Personality and preferences" section at the bottom stays blank; that's deliberate, it fills in as you work together over time.

## Step 8 — Write Start here.md

Copy `assets/start-here-template.md` to `Start here.md` at the root, unchanged.

## Step 9 — Hand off to new-project-setup

Tell them setup is done, briefly summarise what now exists (the folders, the linked shared content, `CLAUDE.md`, their `About Me.md`, `Start here.md`), and then invoke the `new-project-setup` skill so they turn one real, live piece of work into an actual project — not a demo. That's the point of ending the session this way.

## What this skill deliberately doesn't do

- No update or sync path for the personal folders — this is a one-shot setup. It never re-runs against a knowledge base that already has a `CLAUDE.md`. The shared content linked in Step 5 does stay current on its own, through the normal `git pull` habit, since it's a live symlink into a shared repo rather than a copy.
- No OKF folder restructuring, and OKF is never mentioned to the person — frontmatter is added to the content files quietly, as a convention, not taught as a concept here.
- No product-specific tag taxonomy written locally — the person inherits whatever taxonomy the team's shared Research Repository already has, rather than starting from a blank table.
