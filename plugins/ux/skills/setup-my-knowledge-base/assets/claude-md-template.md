This is your briefing on how to work within this knowledge base.

## Routing Map

Work down this table in order when deciding where something goes: which row's "Use when" best matches what's happening right now? Filing by actionability beats filing by topic — a note filed under a subject is a note that won't get seen again when it's needed. As new projects and areas get created (see `new-project-setup`), a new row gets added here automatically. As a project gets archived, its row is meant to go too — `knowledgebase-health-check` catches any row still pointing at a folder that's gone (usually because it moved to `4-Archives/`) and flags it for removal, so this table stays an accurate map instead of only ever growing.

| Folder | Use when... |
|---|---|
| `0-Inbox/` | Quick, unsorted capture. Anything that hasn't been filed yet lands here first. |
| `1-Projects/` | Looking for active work with an end date. |
| `2-Areas/Research Repository/` | Needing a research finding, or adding a new study. See its own `CLAUDE.md`. |
| `1-Projects/Brand & Design System/Wiki/DESIGN.md` | Building any UW-branded output — UI, prototypes, slides, or other assets. The canonical design-system spec, written for AI agents to read and act on directly. |
| `3-Resources/About Me/About Me.md` | Needing personal context about this person — role, working style, preferences. |
| `3-Resources/Design Principles.md` | Making a design or product decision that isn't purely visual — check here for standing heuristics, and add new ones as they emerge. |
| `4-Archives/` | Looking for work that has ended. Don't treat anything here as current status. |

## File naming

- **Point-in-time files** (meeting notes, transcripts, daily notes, dated snapshots) are named `YYYY-MM-DD Description.ext`.
- **Living documents** (plans, guides, trackers, deliverables) are not date-prefixed — they get updated in place.

## Link style

This knowledge base uses **markdown links**, not wikilinks: `[Page Title](page-title.md)`, never `[[Page Title]]`. Every skill in this plugin reads and writes links this way. If Obsidian is in use, "Use [[Wikilinks]]" should be turned off in Settings → Files and Links.

## Shared content freshness

Some folders here aren't local — they're symlinks into a separate clone of the team's shared repo (see `2-Areas/Research Repository/CLAUDE.md`, or any product wiki's own `CLAUDE.md`, for how that works). At the start of a session, check each of those clones for uncommitted local changes: resolve the symlink to find the real clone, then run `git status --short` there. If any clone has changes sitting in it, mention this once near the start of the session and offer to submit them with `contribute-to-shared-knowledgebase` — don't submit anything without being asked, and don't repeat the reminder more than once per session.

## Working rules

- Always ask before making changes to existing files.
- Never delete files without asking first.
- Never write files to the root of this knowledge base, other than `CLAUDE.md` and `Start here.md` themselves — everything else belongs inside one of the folders above.
- If a request is unclear or incomplete, ask rather than guessing.
- Before finalising any substantial written content — notes, comms, customer copy, specs — check it against `3-Resources/AI Writing Guidelines.md` for common AI-tell patterns.
- Before creating any UW-branded output — UI, prototypes, slide decks, or other visual assets — read `1-Projects/Brand & Design System/Wiki/DESIGN.md` first.
- Anything with a second audience — this CLAUDE.md if it's ever shared with a team, or a skill built and shared with others — shouldn't name this person specifically. Use role-based phrasing instead ("the vault owner", "repo admins", "whoever owns this"). A shared document that talks about one specific person by name reads as personal rather than shared, even after it's handed off. Doesn't apply to personal files (About Me, personal-voice writing skills) or private notes only this person reads.

## Personality and preferences

[Blank on purpose. As you work together, add notes here about how this person likes to collaborate — tone, pace, how much detail they want, pet peeves. Keep `3-Resources/About Me/About Me.md` for the fuller picture; keep this section for quick, working-session preferences.]
