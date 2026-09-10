This is your briefing on how to work within this knowledge base.

## Routing Map

Work down this table in order when deciding where something goes: which row's "Use when" best matches what's happening right now? Filing by actionability beats filing by topic — a note filed under a subject is a note that won't get seen again when it's needed. As new projects and areas get created (see `new-project-setup`), a new row gets added here automatically. As a project gets archived, its row is meant to go too — `knowledgebase-health-check` catches any row still pointing at a folder that's gone (usually because it moved to `4-Archives/`) and flags it for removal, so this table stays an accurate map instead of only ever growing.

| Folder | Use when... |
|---|---|
| `0-Inbox/` | Quick, unsorted capture. Anything that hasn't been filed yet lands here first. |
| `1-Projects/` | Looking for active work with an end date. |
| `2-Areas/Research Repository/` | Needing a research finding, or adding a new study. See its own `CLAUDE.md`. |
| `1-Projects/Brand & Design System/DESIGN.md` | Building any UW-branded output — UI, prototypes, slides, or other assets. The canonical design-system spec, written for AI agents to read and act on directly. |
| `1-Projects/Brand & Design System/design-system/` | Building for Claude Design, or an asset type DESIGN.md doesn't cover (decks, social templates, ads, starter React components). A fuller, multi-file repackaging of DESIGN.md. Load its own `design-system/CLAUDE.md` first. |
| `3-Resources/About Me/About Me.md` | Needing personal context about this person — role, working style, preferences. |
| `3-Resources/Design Principles.md` | Making a design or product decision that isn't purely visual — check here for standing heuristics, and add new ones as they emerge. |
| `4-Archives/` | Looking for work that has ended. Don't treat anything here as current status. |

## File naming

- **Point-in-time files** (meeting notes, transcripts, daily notes, dated snapshots) are named `YYYY-MM-DD Description.ext`.
- **Living documents** (plans, guides, trackers, deliverables) are not date-prefixed — they get updated in place.

## Link style

This knowledge base uses **markdown links**, not wikilinks: `[Page Title](page-title.md)`, never `[[Page Title]]`. Every skill in this plugin reads and writes links this way. If Obsidian is in use, `"Use [[Wikilinks]]"` should be turned off in Settings → Files and Links.

## Shared content freshness

Some folders here aren't local — they're symlinks into a separate clone of the team's shared repo (see `2-Areas/Research Repository/CLAUDE.md`, or any product wiki's own `CLAUDE.md`, for how that works). At the start of a session, before responding to the first request, check each of those clones: resolve the symlink to find the real clone, then run `git status --short` there for uncommitted local changes, and `git fetch` plus `git status -sb` to see whether it's behind `origin/main` or sitting on a branch that isn't `main`. If any clone has uncommitted changes, mention this once near the start of the session and offer to submit them with `contribute-to-shared-knowledgebase`. If a clone is behind `main`, name the specific file(s) that changed upstream (e.g. via `git diff --name-only HEAD..origin/main`) rather than just saying it's behind, and offer to switch it to `main` and pull if it's stuck on another branch. Don't act on either without being asked, and don't repeat either reminder more than once per session.

## Working rules

- Always ask before making changes to existing files.
- Show a file's contents before creating it (any markdown file — project note, log entry, doc — not just daily notes).
- Draft emails and other messages and show them before sending — never send without approval. Ask before any other external or public-facing action (Slack, publishing, and the like).
- Never delete files without asking first.
- Before deleting a project folder under `1-Projects/`, check whether its `Wiki/` is a symlink (shared with the team) rather than a plain folder (personal). If it's shared, warn before doing anything else: it's linked to the whole team's shared knowledge base, so it might be used by, or belong to, a teammate. Only proceed once they confirm. After a shared project's deletion is confirmed and done, check whether its shared copy (in the linked knowledge-base clone) still exists — if so, offer cleanup in this order: restore from Trash first (safest, nothing lost), or pull a fresh copy back down, and only if they're completely sure it should be gone for good, delete the shared copy via `contribute-to-shared-knowledgebase` (opens a PR, never merges it directly).
- Never write files to the root of this knowledge base, other than `CLAUDE.md` and `Start here.md` themselves — everything else belongs inside one of the folders above.
- If a request is unclear or incomplete, use the `AskUserQuestion` tool rather than filling the gap with generic filler.
- Before finalising any substantial written content — notes, comms, customer copy, specs — check it against `3-Resources/AI Writing Guidelines.md` for common AI-tell patterns.
- Before creating any UW-branded output — UI, prototypes, slide decks, or other visual assets — read `1-Projects/Brand & Design System/DESIGN.md` first.
- When a file needs visual verification via the in-app browser (screenshot), place it in a `00-Scratch/` subfolder inside the active project — files in the session scratchpad render only as static, non-interactive snapshots and can't be screenshotted. Ask before deleting scratch files, same as anywhere else in this knowledge base.
- Cite sources as markdown links, not bare filenames — always keep the file extension in the link target, and only quote a link in frontmatter if the value needs quoting for other YAML reasons. A plain-text citation is invisible to the graph, so the source it names reads as an orphan.
- When writing a fact into a note from an external source — a Miro board, Google Sheet, Figma file, Confluence page, a screenshot or link pasted in chat — record the source's name and its location (local path or URL) alongside the claim. If you can't see a name or URL, ask for it rather than writing an unciteable note.
- Before quoting a count, re-run the query without any filters added just for readability — a narrowed grep will undercount, and the number still reads as authoritative.
- If the same correction shows up a second time — whether it's sitting in a `feedback`-type memory or in a project's own `MEMORY.md` — that's the signal it belongs in a permanent instruction file (this CLAUDE.md, Design Principles.md, etc.), not left to keep accumulating as memory notes.
- Anything with a second audience — this CLAUDE.md if it's ever shared with a team, or a skill built and shared with others — shouldn't name this person specifically. Use role-based phrasing instead ("the vault owner", "repo admins", "whoever owns this"). A shared document that talks about one specific person by name reads as personal rather than shared, even after it's handed off. Doesn't apply to personal files (About Me, personal-voice writing skills) or private notes only this person reads.
- Before running any bash command, explain in plain words what it does.

## New Project Detection

When you're about to create a file for the first time in a session and there's no obvious home for it in `1-Projects/`, pause and ask whether this is a new project that needs a folder structure first. If they say yes, use the `new-project-setup` skill to run the setup flow — it handles confirming, checking for an existing or archived folder, and setup itself.

## Building and updating skills

- To build or improve a skill, use the `skill-creator` skill, working in a checkout of the repo that owns it, rather than in this knowledge base.
- Skills must only be edited in the checkout that owns them. If a skill has been edited anywhere else, flag it and ask for the changes to be moved into the right repo before proceeding.
- To release a change to a shared UX team skill — a new skill, an edit to an existing one, or retiring one — use the `propose-skill` skill. It opens a PR against `uw-ux-claude-skills` and stops there; it never merges, since that repo's `main` needs review and sign-off from whoever owns it.
- GitHub is the source of truth: don't keep permanent skill sources in this knowledge base; any copy here is a distribution artefact and will go stale.
- Eval runs are throwaway. Keep them wherever the session can write, for as long as they're useful. They don't get committed and don't belong in this knowledge base.
- After pushing a skill change, the local plugin cache needs a manual refresh — pushing to GitHub doesn't update what's installed. This always runs in a sandboxed session, so don't run the refresh commands yourself — they fail with an `EPERM`/permission error here. Instead, tell the vault owner to run these two in their own regular terminal: `claude plugin marketplace update <marketplace-name>` then `claude plugin update <plugin-name>@<marketplace-name>`, and check it worked with `claude plugin list`.
- After a PR opened from a skills repo is confirmed merged, switch back to `main`, pull the latest changes, and delete the merged branch (locally, and remotely if GitHub hasn't already removed it) — do this automatically, without being asked.

## Personality and preferences

[Blank on purpose. As you work together, add notes here about how this person likes to collaborate — tone, pace, how much detail they want, pet peeves. Keep `3-Resources/About Me/About Me.md` for the fuller picture; keep this section for quick, working-session preferences.]
