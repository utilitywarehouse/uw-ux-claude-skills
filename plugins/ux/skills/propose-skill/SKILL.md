---
name: propose-skill
version: 1
description: Ship a finished skill draft — a brand-new skill or an edit to an existing one — from this repo (uw-ux-claude-skills) into a pull request for repo admins to review and merge. Use this whenever a team member has just finished writing a new skill (typically with skill-creator) or editing an existing one here, and now wants to submit it, share it with the team, open a PR, or get it added to the shared UX skills repo. Trigger on phrases like "propose this skill", "submit my skill", "ship this to the team repo", "send this for review", "open a PR for this skill", or "how do I get this merged". This skill NEVER merges anything itself — main is protected and only repo admins approve merges. It also does not package a .skill file, run smoke tests, or touch Cowork — this repo ships purely via GitHub pull request, nothing else.
---

# Propose Skill

Takes a finished skill change in this repo — a new skill folder, or an edit to an existing one — and turns it into a pull request against `main`, for repo admins to review and merge. It never merges anything itself: `main` is a GitHub-protected branch that requires a PR and a status check, so a direct push is rejected by GitHub regardless. This skill's whole job is getting a clean, reviewable PR in front of the people who own this repo — the actual sign-off happens in the PR itself, not in this chat.

## Before you start

This picks up *after* the skill content is finished. If the SKILL.md still needs writing, editing, or fixing — use `skill-creator` first (it validates that every file a SKILL.md references actually exists, among other checks this skill doesn't repeat). Don't ship a half-finished draft just because someone asked to "submit" it — check the skill actually reads as complete before treating it as ready to ship.

## Workflow

1. **See what actually changed.** Run `git status` and `git diff --stat` from the repo root. Confirm which skill folder(s) under `plugins/ux/skills/` are touched, and whether it's a new skill or an edit to an existing one.
2. **Scope the change.** If the diff touches files outside the intended skill folder — something unrelated got picked up, or another in-progress edit is sitting in the working tree — stop and ask before staging anything. A PR should contain one skill's change, not whatever else happens to be lying around.
3. **Branch off `main`.** Never commit directly on `main` — even though GitHub would reject the push anyway, working on a branch from the start avoids the wasted round-trip. Name it for what's happening:
   - New skill: `add-<skill-name>`
   - Update: `update-<skill-name>`
4. **Stage and commit** — only the relevant skill's files. Write a plain, factual commit message describing what changed, matching this repo's existing style (e.g. "Add setup-my-knowledge-base skill", "Rename transcript-cleaner to research-transcript-cleaner and tighten scope").
5. **Push the branch**, then **open the PR** with `gh pr create`. Keep the body short and plain — a summary of what changed and a one- or two-sentence why, so it's quick to review:
   ```
   ## Summary
   - [what changed, as 1-2 bullets]

   ## Why
   [one or two plain sentences]
   ```
6. **Report the PR link and stop there.** Say plainly that this is now waiting on review — don't imply the skill is live or available to the team yet. It isn't, until a repo admin merges it.

## Guardrails

- **Never push to `main` directly, and never merge, approve, or self-merge the PR** — not even if asked to. If someone asks you to merge it, say that only repo admins can approve and merge changes to this repo, and that's the entire point of routing through a PR.
- **No packaging, no smoke tests, no version tags, no Cowork upload.** This repo has no `scripts/package-skill.sh`, no `smoke-tests.md`, and no packaged `.skill` distribution — it ships purely through GitHub. If someone asks about any of that, say plainly that this repo doesn't use that convention; don't invent steps that don't exist here just because another skills repo has them.
- **Bump `version:` in the SKILL.md frontmatter by 1** when proposing an edit to an existing skill (leave it if whoever wrote the edit already bumped it). New skills start at `version: 1`.

## Two flows

**A. Propose a new skill**
- Confirm `plugins/ux/skills/<name>/SKILL.md` exists and looks complete.
- Stage only that folder.
- Branch: `add-<name>` · PR title: "Add `<name>` skill"

**B. Propose an update to an existing skill**
- Confirm which skill folder(s) changed via `git status`.
- Branch: `update-<name>` · PR title: "Update `<name>`: `<one-line of what changed>`"
