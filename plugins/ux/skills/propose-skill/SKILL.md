---
name: propose-skill
version: 2
description: Ship a finished skill change — a brand-new skill, an edit to an existing one, or retiring one entirely — from this repo (uw-ux-claude-skills) into a pull request for repo admins to review and merge. Use this whenever a team member has just finished writing a new skill (typically with skill-creator), editing an existing one here, or decided a skill should be removed, and now wants to submit it, share it with the team, open a PR, or get it added to (or taken out of) the shared UX skills repo. Trigger on phrases like "propose this skill", "submit my skill", "ship this to the team repo", "send this for review", "open a PR for this skill", "retire this skill", "remove this skill", or "how do I get this merged". This skill NEVER merges anything itself — main is protected and only repo admins approve merges. It runs this repo's smoke test for the skill before every push, but does not package a .skill file or touch Cowork — this repo ships purely via GitHub pull request, nothing else.
---

# Propose Skill

Takes a finished skill change in this repo — a new skill folder, or an edit to an existing one — and turns it into a pull request against `main`, for repo admins to review and merge. It never merges anything itself: `main` is a GitHub-protected branch that requires a PR and a status check, so a direct push is rejected by GitHub regardless. This skill's whole job is getting a clean, reviewable PR in front of the people who own this repo — the actual sign-off happens in the PR itself, not in this chat.

## Before you start

This picks up *after* the skill content is finished. If the SKILL.md still needs writing, editing, or fixing — use `skill-creator` first (it validates that every file a SKILL.md references actually exists, among other checks this skill doesn't repeat). Don't ship a half-finished draft just because someone asked to "submit" it — check the skill actually reads as complete before treating it as ready to ship.

## Workflow

1. **See what actually changed.** Run `git status` and `git diff --stat` from the repo root. Confirm which skill folder(s) under `plugins/ux/skills/` are touched, and whether it's a new skill, an edit to an existing one, or a folder being removed entirely.
2. **Scope the change.** If the diff touches files outside the intended skill folder — something unrelated got picked up, or another in-progress edit is sitting in the working tree — stop and ask before staging anything. A PR should contain one skill's change, not whatever else happens to be lying around.
3. **Branch off `main`.** Never commit directly on `main` — even though GitHub would reject the push anyway, working on a branch from the start avoids the wasted round-trip. Name it for what's happening:
   - New skill: `add-<skill-name>`
   - Update: `update-<skill-name>`
   - Retiring a skill: `retire-<skill-name>`
4. **Bump `plugins/ux/.claude-plugin/plugin.json`'s `version` field** by one patch number, then **stage and commit** — the relevant skill's files, plus that one line. Write a plain, factual commit message describing what changed, matching this repo's existing style (e.g. "Add setup-my-knowledge-base skill", "Rename transcript-cleaner to research-transcript-cleaner and tighten scope"). **For a retirement, the commit message is where the reason for removing it lives** — see the "Retiring a skill" flow below; there's no separate tracking file for this, so a commit message that just says "Remove X" loses the one piece of information anyone will actually want later.
5. **Run the smoke test.** Look up the skill's entry in `smoke-tests.md` at the repo root and run its test prompt against the change before doing anything else. If the expected behaviour doesn't hold, stop and report what broke — don't open a PR for a skill that just regressed. Skip this step for a retirement (there's nothing left to test).
6. **Push the branch**, then **open the PR** with `gh pr create`. Keep the body short and plain — a summary of what changed and a one- or two-sentence why, so it's quick to review:
   ```
   ## Summary
   - [what changed, as 1-2 bullets]

   ## Why
   [one or two plain sentences]
   ```
7. **Report the PR link and stop there.** Say plainly that this is now waiting on review — don't imply the skill is live, updated, or removed for the team yet. None of that is true until a repo admin merges it.

## Guardrails

- **Never push to `main` directly, and never merge, approve, or self-merge the PR** — not even if asked to. If someone asks you to merge it, say that only repo admins can approve and merge changes to this repo, and that's the entire point of routing through a PR.
- **No packaging, no per-skill version tags, no Cowork upload.** This repo has no `scripts/package-skill.sh` and no packaged `.skill` distribution — it ships purely through GitHub. If someone asks about any of that, say plainly that this repo doesn't use that convention; don't invent steps that don't exist here just because another skills repo has them.
- **Bump `version:` in the SKILL.md frontmatter by 1** when proposing an edit to an existing skill (leave it if whoever wrote the edit already bumped it). New skills start at `version: 1`.
- **Bump the plugin version too, every single time** — `plugins/ux/.claude-plugin/plugin.json`'s `version` field, by one patch number (e.g. `0.1.2` → `0.1.3`), in the same commit. This is the number `claude plugin update` actually compares to decide whether there's anything new to fetch — a skill's own `version:` field means nothing to that check. Skip this bump and every installed Claude Code, on every machine, will report "already up to date" and keep serving stale content indefinitely, with no error to say so. This bit everyone the first time `propose-skill` was used: three merged PRs in a row changed real behaviour without anyone noticing the installed copies never updated.

## Three flows

**A. Propose a new skill**
- Confirm `plugins/ux/skills/<name>/SKILL.md` exists and looks complete.
- **Add its entry to `smoke-tests.md` in the same commit.** A skill with no smoke test is one nobody will notice breaking. Base the prompt and expected behaviour on the skill's own description and workflow — a realistic thing someone would actually say to trigger it, and the one or two things it must do in response.
- Stage the skill folder and the `smoke-tests.md` change together.
- Branch: `add-<name>` · PR title: "Add `<name>` skill"

**B. Propose an update to an existing skill**
- Confirm which skill folder(s) changed via `git status`.
- If the change affects what the skill actually does (not just wording), update its `smoke-tests.md` entry to match — a smoke test checking old behaviour will pass while testing the wrong thing.
- Branch: `update-<name>` · PR title: "Update `<name>`: `<one-line of what changed>`"

**C. Propose retiring a skill**
- Confirm with whoever's asking *why* the skill is being retired — superseded by another skill, no longer used, merged into something else, whatever it is. Don't remove a folder on a vague "we don't need this anymore" without pinning down the actual reason; that reason is about to become the only record of why this happened.
- `git rm -r plugins/ux/skills/<name>/` — deleting the folder is correct, git keeps the full content in history, so nothing is actually lost. A retired skill left in place (even renamed or moved) risks still being loaded as live.
- Remove its entry from `smoke-tests.md` in the same commit — a smoke test for a skill that no longer exists is dead weight, and running it would fail for the wrong reason.
- Commit message must state the reason plainly, not just the mechanical fact of removal — e.g. "Retire old-transcript-cleaner: folded into research-transcript-cleaner" tells a future reader something "Remove old-transcript-cleaner" does not.
- Branch: `retire-<name>` · PR title: "Retire `<name>` skill"
- PR body's "Why" section carries the same reason as the commit message — this is the one flow where that section is doing real work, not just a formality, since it's the only place the reason survives.
