# Smoke Tests

One prompt per skill, run before pushing any change (see `propose-skill`'s workflow). If the
expected behaviour doesn't hold, stop and report what broke — don't open a PR for a skill that
just regressed.

Adding a new skill? Add its entry here in the same PR. A skill with no smoke test is one nobody
will notice breaking.

## end-session
**Prompt:** "we're done for today, anything worth capturing before we close out?"
**Expect:** Reviews the session for corrections, wiki-worthy facts, project state changes, and behaviour rules, then shows proposed changes grouped by destination (Wiki, MEMORY.md, CLAUDE.md, auto-memory) and waits for approval before writing anything.

## knowledgebase-health-check
**Prompt:** "can you run a health check on my vault, graph view looks really sparse lately"
**Expect:** Checks link health across the knowledge base (orphans, broken links, stale Routing Map rows) and, for any project with a Wiki, its content health too — not just a mechanical link count.

## new-project-setup
**Prompt:** "I want to start a new project looking into checkout drop-off"
**Expect:** Confirms it's genuinely new (checks for an existing or archived folder first) before asking setup questions or creating anything.

## propose-skill
**Prompt:** "I've finished editing the study-writeup skill, can you get it merged in?"
**Expect:** Branches off main, commits only that skill's files, pushes, and opens a PR — then stops and says it's waiting on review. Refuses to merge even if asked.

## research-transcript-cleaner
**Prompt:** paste a raw Zoom transcript of a usability test with a participant, "clean this up for coding"
**Expect:** Asks for cohort, session date, and source platform before cleaning; does not attempt this on an internal team-meeting transcript with no research participant.

## setup-my-knowledge-base
**Prompt:** "I'm new to the team, can you help me set up my own knowledge base from scratch?"
**Expect:** Creates the core folder structure, interviews for an About Me note, writes a starter CLAUDE.md and Start here note, then hands off to new-project-setup for one real first project.

## study-writeup
**Prompt:** "we just wrapped the onboarding usability study, can you write it up?"
**Expect:** Produces both a full report and a one-page study card, verifying every figure against a source rather than just formatting an already-decided set of findings.

## transcript-coder
**Prompt:** "this session's been cleaned, can you code it now?"
**Expect:** Applies qualitative codes ready for thematic analysis, managing a shared codebook if this is one of several sessions in the same study.
