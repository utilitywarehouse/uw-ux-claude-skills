---
name: setup-my-knowledge-base
version: 11
description: "Set up a brand-new personal knowledge base from scratch, driven by Claude Code. Use this skill when no knowledge base exists yet and someone says things like \"set up my knowledge base\", \"get me started\", \"I'm new, help me set this up\", or is working through session one of the UX team's onboarding. Creates the core folder structure, links the person into all of the team's shared content (the Research Repository and every shared product wiki), interviews the person for their own About Me note, writes a starter CLAUDE.md and Start here note, then hands off to `new-project-setup` so they leave with one real project, not a demo. Do not use this on a knowledge base that already exists — that's `new-project-setup`'s job instead."
---

# Set Up My Knowledge Base

Builds a new knowledge base from nothing: the core folders, a starter `CLAUDE.md`, a personal `About Me.md`, and a `Start here.md`. Then hands off to `new-project-setup` so the person leaves with one real piece of work started, not an empty shell.

This only runs once per knowledge base — it's the very first skill someone touches. If a `CLAUDE.md` already exists at the location they name, this isn't the right skill; say so and point at `new-project-setup` instead.

## Step 1 — Check for VS Code and Markdown All in One

Check whether VS Code is installed (`code --version` on the PATH, or `/Applications/Visual Studio Code.app`), and if so whether the Markdown All in One extension is too (`code --list-extensions | grep -i yzhang.markdown-all-in-one`).

- **Both found:** continue to Step 2.
- **Either missing:** ask a yes/no question: "VS Code with the Markdown All in One extension isn't fully set up. Want to install what's missing? It gives you a live markdown preview and easier note-linking — though the knowledge base works fine as plain markdown folders in any editor without it." Use `AskUserQuestion` with Yes/No options, and put the benefit line on the Yes option itself.
  - **Yes:** for VS Code, give them the download link — `https://code.visualstudio.com/download`. For the extension, once VS Code is in, run `code --install-extension yzhang.markdown-all-in-one` or point them at its marketplace page. Ask them to say "done" when ready, then repeat this check.
    - Still missing something: ask again — "Still not showing up — want to try again, or carry on without it?" Loop as many times as they want to keep trying. The moment they choose to carry on without it, treat that the same as a No answer below.
  - **No:** say once that it's recommended but not required, and that the knowledge base works fine as plain markdown folders in any editor, Obsidian included if that's what they already use. Continue to Step 2 either way — never force the install.

## Step 2 — Ask where the knowledge base should live

Ask for a folder path. If they already have a folder they've been using for notes, that's the one to use — don't create a new one nested inside it.

## Step 3 — Create the core folder structure

Create this inside the location from Step 2. Nothing beyond this — no extra folders, no placeholder files beyond what's listed:

```
0-Inbox/
1-Projects/
2-Areas/
3-Resources/
  About Me/
4-Archives/
```

The Research Repository doesn't get created here — Step 4 links it in from the team's shared repo instead of writing a blank local copy.

Copy these three as-is — they're already written for a newcomer:

- `assets/design-principles-template.md` → `3-Resources/Design Principles.md`
- `assets/mastering-para-template.md` → `3-Resources/Mastering PARA - The Architect's Guide to Digital Organisation.md`
- `assets/ai-writing-guidelines-template.md` → `3-Resources/AI Writing Guidelines.md`

## Step 4 — Link into the team's shared content

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

### Add the clone to their VS Code workspace, if they're using the VS Code extension

Skip this if they're running Claude Code from a plain terminal instead — it doesn't apply there.

If Claude Code is running as a VS Code extension, it can only read and write inside the folders VS Code has open. The knowledge base folder is already one of those; this clone isn't, since it lives in a separate folder outside the knowledge base. Without this step, `contribute-to-shared-knowledgebase` will fail later with a sandbox permissions error when it tries to write to the clone.

In VS Code: **File → Add Folder to Workspace…**, and pick the clone folder from the step above. Don't save the workspace file yet — the skills-repo clone below joins the same workspace, and it only needs saving once.

### Link it into the new knowledge base

Use real symlinks (`ln -s`), never macOS Finder aliases. A Finder alias only resolves from Finder itself; a symlink is transparent to every tool that touches the file — Claude Code, `grep`, and other skills like `study-writeup` and `end-session` that read straight through `Research Repository/CLAUDE.md` without knowing (or needing to know) that it's shared.

Walk the clone's actual top-level contents rather than a fixed list, since new shared wikis land in it over time (decision #31) and this step should pick them up automatically:

- The clone's `Research Repository/` folder → symlink to `2-Areas/Research Repository` in the new knowledge base.
- Any other top-level folder in the clone that contains a `Wiki/` subfolder — each one is a shared product area, e.g. `Cashback Card`, `Brand & Design System` — create `1-Projects/<same name>/` if it doesn't already exist, then symlink that folder's `Wiki/` to `1-Projects/<same name>/Wiki`.

Confirm the links resolved by listing one of them before moving on.

### Clone the shared skills repo too

Everyone gets a local clone of `utilitywarehouse/uw-ux-claude-skills`, the repo these skills themselves ship from — not just the installed plugin. The clone is what lets someone propose a change to a skill later, via `propose-skill`, rather than only ever consuming skills read-only.

Ask where the clone should live — suggest `~/Documents/Github/uw-ux-claude-skills`, the same pattern as the knowledge-content clone above.

- If that folder already exists and is already a clone of this repo, reuse it: run `git pull` to bring it current rather than re-cloning.
- Otherwise, `git clone https://github.com/utilitywarehouse/uw-ux-claude-skills.git` into the folder they chose.
- If the clone fails on access, tell them plainly and skip this step without blocking the rest of setup — same handling as the knowledge-content access check above.

If they're using the VS Code extension, add this clone to the VS Code workspace too — **File → Add Folder to Workspace…**. Same reasoning as the knowledge-content clone: without it, `propose-skill` will hit a sandbox permissions error the first time it tries to write there.

### Save the workspace, if they're using the VS Code extension

Now that the knowledge base folder and both clones are all open together, save that as a workspace file so VS Code remembers the set — otherwise it only lasts for this session.

**File → Save Workspace As…**, save it as `<knowledge base folder name>.code-workspace`, right next to the knowledge base folder itself (a sibling, not inside it — this file isn't part of the PARA structure). E.g. if the knowledge base folder is `~/Documents/Obsidian/Second Brain - Work`, save the workspace file as `~/Documents/Obsidian/Second Brain - Work.code-workspace`.

Tell them to reopen that `.code-workspace` file (instead of just the knowledge base folder) from now on, so all three folders come back together automatically.

### Optional — install the Figma plugin

This is Anthropic's own official plugin (`figma@claude-plugins-official`), not a UW one — no access request needed, anyone can install it. Ask a yes/no question: "Want to install the Figma plugin too? It gives Claude a set of skills for working with Figma files directly — building designs, converting them to code, and going the other way — on top of the design knowledge you just linked in." If yes, walk them through adding it the normal way a Claude Code plugin gets installed (marketplace add + plugin install, or `claude mcp`/`/mcp` if that's how this session installs plugins) and confirm it shows up before moving on. If no, skip it without pushing.

### Optional — install the Hearth AI Toolkit plugin

`utilitywarehouse/hearth` is a public repo, so installing the plugin itself has no access barrier regardless of how the check above went. But the two MCP connectors it bundles aren't the same: `hearth-react` needs no extra login, while `hearth-react-native` needs a separate Chromatic login for UW's Hearth org that not everyone will already have. Ask a yes/no question: "Want to install the Hearth AI Toolkit plugin too? It gives Claude the component docs and MCP tools for building real UW UI in code — `hearth-react` and `hearth-react-native` — on top of the design knowledge you just linked in." If yes, walk them through adding it the normal way a Claude Code plugin gets installed (marketplace add + plugin install, or `claude mcp`/`/mcp` if that's how this session installs plugins) and confirm it shows up before moving on. Mention plainly that `hearth-react-native` may then ask for a Chromatic login they might not have — that's expected, not a setup failure, and getting one is a request to whoever manages the Hearth design system or the mobile team, not something to troubleshoot here. If they don't build React Native screens, they can just ignore that prompt; `hearth-react` still works fine without it. If no, or if they're not building in code at all, skip the whole plugin without pushing.

### Optional — install the claude-md-management plugin

Another of Anthropic's own official plugins (`claude-md-management@claude-plugins-official`), same as the Figma one above — no access request needed. Unlike Figma or Hearth, this one applies to everyone regardless of what they design or build: Step 6 below writes this person's own `CLAUDE.md`, and it only grows more complex over time as `new-project-setup` adds rows to it. Ask a yes/no question: "Want to install the claude-md-management plugin too? It gives Claude skills for auditing and improving a CLAUDE.md file once it's grown — useful for keeping yours healthy as your knowledge base grows." If yes, walk them through adding it the normal way a Claude Code plugin gets installed (marketplace add + plugin install, or `claude mcp`/`/mcp` if that's how this session installs plugins) and confirm it shows up before moving on. If no, skip it without pushing.

## Step 5 — Interview for About Me

Use `assets/about-me-template.md` as the question set — it's already written for a newcomer and needs no changes. Walk through it conversationally rather than dumping the whole template as a form; skip anything they say doesn't apply. Write their answers into `3-Resources/About Me/About Me.md`, keeping the template's structure and frontmatter.

## Step 6 — Write the root CLAUDE.md

Copy `assets/claude-md-template.md` to `CLAUDE.md` at the root of the new knowledge base. It already carries its own Routing Map and link-style rule — nothing in it needs to be filled in with this person's specifics, and it already has static rows for the content every teammate gets (Research Repository, DESIGN.md).

Then add one Routing Map row for each *product* wiki Step 4 actually linked (e.g. `Cashback Card`) — these vary from one teammate's setup to another and can't be baked into the template as a fixed list. Skip any wiki that already has a static row in the template (Research Repository, Brand & Design System). For each row, use the pattern already in the table: `1-Projects/<Product>/Wiki/` in the folder column, and a one-line "Use when..." pulled from that wiki's own `index.md` summary. If Step 4 was skipped or blocked (no repo access), skip this too — there's nothing linked to add a row for.

The Routing Map is also what `new-project-setup` adds a row to every time a new project or area is created, so it stays accurate as the knowledge base grows. The "Personality and preferences" section at the bottom stays blank; that's deliberate, it fills in as you work together over time.

## Step 7 — Write Start here.md

Copy `assets/start-here-template.md` to `Start here.md` at the root, unchanged.

## Step 8 — Hand off to new-project-setup

Tell them setup is done, briefly summarise what now exists (the folders, the linked shared content, `CLAUDE.md`, their `About Me.md`, `Start here.md`), and then invoke the `new-project-setup` skill so they turn one real, live piece of work into an actual project — not a demo. That's the point of ending the session this way.

## What this skill deliberately doesn't do

- No update or sync path for the personal folders — this is a one-shot setup. It never re-runs against a knowledge base that already has a `CLAUDE.md`. The shared content linked in Step 4 does stay current on its own, through the normal `git pull` habit, since it's a live symlink into a shared repo rather than a copy.
- No OKF folder restructuring, and OKF is never mentioned to the person — frontmatter is added to the content files quietly, as a convention, not taught as a concept here.
- No product-specific tag taxonomy written locally — the person inherits whatever taxonomy the team's shared Research Repository already has, rather than starting from a blank table.
