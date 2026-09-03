# Smoke Tests

One prompt per skill, run before pushing any change (see `propose-skill`'s workflow). If the
expected behaviour doesn't hold, stop and report what broke — don't open a PR for a skill that
just regressed.

Adding a new skill? Add its entry here in the same PR. A skill with no smoke test is one nobody
will notice breaking.

## contribute-to-shared-knowledgebase
**Prompt:** "I just fixed a typo in the Cashback Card wiki, can you submit that back to the team repo?"
**Expect:** Resolves the symlinked folder back to the shared repo clone, branches and commits the person's edit before touching the remote, then fetches and merges the latest `main` — pushing and opening a PR only if that merge is clean. On a real conflict, stops and names the conflicting file rather than resolving it, and leaves the branch intact. Never pushes to `main` directly, never merges the PR itself.

## end-session
**Prompt:** "we're done for today, anything worth capturing before we close out?"
**Expect:** Reviews the session for corrections, wiki-worthy facts, project state changes, and behaviour rules, then shows proposed changes grouped by destination (Wiki, MEMORY.md, CLAUDE.md, auto-memory) and waits for approval before writing anything. Separately, on the way out, checks any shared-repo clones touched this session for uncommitted changes and offers `contribute-to-shared-knowledgebase` if it finds any — without submitting anything unasked.

## figma-craft
**Prompt:** "the fill on this row I just grouped is showing white behind the cards — can you check what's happening?" (with a Figma file open via the Figma MCP connector)
**Expect:** Identifies that an auto-layout frame defaults to a white fill and flags clearing it (`frame.fills = []`) as the fix, rather than treating a screenshot that "looks right" in the Plugin API response as confirmation. Requires the Figma MCP connector to be connected.

## figma-dev-handoff
**Prompt:** "this journey page is done — can you convert those screens into components and get instances back on the page so engineering can pick it up?" (with a Figma file open via the Figma MCP connector)
**Expect:** Captures every existing annotation to disk BEFORE converting anything, and warns that annotations do not carry from a component onto its instances, so they must be re-applied afterwards. Confirms the grouping, the variant names, and the addition to the file's master-components page before writing. Requires the Figma MCP connector to be connected.

## knowledgebase-health-check
**Prompt:** "can you run a health check on my vault, graph view looks really sparse lately"
**Expect:** Checks link health across the knowledge base (orphans, broken links, stale Routing Map rows) and, for any project with a Wiki, its content health too — not just a mechanical link count.

## new-project-setup
**Prompt:** "I want to start a new top-level product area for Insurance"
**Expect:** Confirms it's genuinely new (checks for an existing or archived folder first, and for a new product area, checks the shared repo for a name clash too) before creating anything. Asks whether the new Wiki should be shared with the team, defaulting to yes, and if shared, links it into the `uw-knowledgebase-content` repo via a symlink and opens a PR rather than pushing straight to main.

## propose-skill
**Prompt:** "I've finished editing the study-writeup skill, can you get it merged in?"
**Expect:** Branches off main, commits only that skill's files, pushes, and opens a PR — then stops and says it's waiting on review. Refuses to merge even if asked.

## research-transcript-cleaner
**Prompt:** paste a raw Zoom transcript of a usability test with a participant, "clean this up for coding"
**Expect:** Asks for cohort, session date, and source platform before cleaning; does not attempt this on an internal team-meeting transcript with no research participant.

## setup-my-knowledge-base
**Prompt:** "I'm new to the team, can you help me set up my own knowledge base from scratch?"
**Expect:** Creates the core folder structure, checks access to the shared `uw-knowledgebase-content` repo, clones it, adds the clone's path to `.claude/settings.json`'s sandbox allowWrite/allowRead so later git-based skills can write to it, and links its Research Repository and every shared product wiki in via symlinks (or fails that one step cleanly with access instructions if the check doesn't pass). Then interviews for an About Me note, writes a starter CLAUDE.md and Start here note, and hands off to new-project-setup for one real first project. The CLAUDE.md it writes includes a session-start check that looks for uncommitted changes in any linked shared clone and offers `contribute-to-shared-knowledgebase` if it finds any.

## study-writeup
**Prompt:** "we just wrapped the onboarding usability study, can you write it up?"
**Expect:** Produces both a full report and a one-page study card, verifying every figure against a source rather than just formatting an already-decided set of findings.

## research-transcript-coder
**Prompt:** "this session's been cleaned, can you code it now?"
**Expect:** Applies qualitative codes ready for thematic analysis, managing a shared codebook if this is one of several sessions in the same study.
