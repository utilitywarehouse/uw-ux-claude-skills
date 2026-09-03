---
name: contribute-to-shared-knowledgebase
version: 1
description: Submit an edit made inside the shared knowledge-content repo (the Research Repository, or any shared product wiki, linked in via symlink) back to the team as a pull request — without the person ever typing a raw git command. Use this whenever someone says they've edited a shared file and want to "submit", "contribute", "send this back", "open a PR for this", "push my changes to the team repo", or asks how to share an edit they just made to a wiki or research page. Do not use this for edits inside a person's own private folders (0-Inbox, personal 1-Projects work) — those never go through a PR, only the shared content does.
---

# Contribute to Shared Knowledgebase

Takes an edit someone has already made inside their symlinked shared-repo folder and turns it into a pull request against `utilitywarehouse/uw-knowledgebase-content`, the private repo that holds the Research Repository and every shared product wiki. The person never runs `git` themselves — this skill does the pull, branch, commit, push, and PR.

## Why this exists

Contributors' local copies of the shared repo are separate clones linked into their own knowledge base by symlink (not git-nested inside it), specifically so nobody needs real git commands day to day. Pulling and PRs are this skill's job, not muscle memory. `main` is a protected branch — even if something tried to push straight to it, GitHub would reject it — so branch-and-PR is the only path in regardless.

## Step 1 — Find the shared repo clone

The person edited a file somewhere under a shared folder — the Research Repository, or a product wiki's `Wiki/` folder. These are symlinks into a separate clone on disk, not real folders inside the knowledge base.

Resolve the real location:

```
readlink -f "<path to the shared folder they edited, e.g. 2-Areas/Research Repository or 1-Projects/[Product]/Wiki>"
```

That resolves to something like `~/Documents/Github/uw-knowledgebase-content/Research Repository`. The clone root is the parent of that (`~/Documents/Github/uw-knowledgebase-content`) — everything from here runs inside the clone, not the knowledge base.

If they didn't say which file, ask which shared folder they were working in, or run `git status` from a likely clone location and check what's actually changed.

## Step 2 — Confirm there's something to contribute

From the clone root, run `git status`. If there's nothing uncommitted and no local commits ahead of `origin/main`, say so plainly and stop — there's nothing to submit.

If there is a change, show them a short summary of what changed (`git status` plus `git diff --stat`) so they can confirm it's what they meant to submit, not a stray edit from something else.

## Step 3 — Branch and commit before touching the remote

Do this *before* pulling the latest `main` — committing the person's work to its own branch first means a later merge conflict (Step 4) only ever touches that one branch, never risks the person's uncommitted edit itself.

1. `git checkout -b contribute-<short-slug>-<YYYY-MM-DD>` off the current branch (a slug from what changed — e.g. `contribute-cbc-wiki-typo-fix-2026-09-03`).
2. Ask for a one-line description of what changed, in their own words, if it isn't already obvious from the diff. Use it as the commit message and, later, the PR title.
3. `git add` the changed files — only the ones the person actually meant to submit, not anything else sitting uncommitted in the clone — then commit.

## Step 4 — Bring in the latest `main`

Shared content has no locking system (someone else could have merged a change to the same file since this clone was last pulled), so this step is expected to occasionally hit a real conflict — that's normal, not a sign something's broken.

1. `git fetch origin`
2. `git merge origin/main`

**If it merges cleanly:** continue to Step 5.

**If it conflicts:** stop. Don't try to resolve it silently or guess which version is right — that's a judgement call for the person, and possibly for whoever else touched the same file. Tell them plainly which file(s) conflict, and suggest asking in the UX team Slack channel if it's not obvious how to resolve it. Leave the branch as-is so nothing is lost; they can come back to it once it's sorted.

## Step 5 — Push and open the PR

1. `git push -u origin contribute-<short-slug>-<YYYY-MM-DD>`
2. `gh pr create` against `utilitywarehouse/uw-knowledgebase-content`, with the one-line description from Step 3 as the title, and a short body — what changed and why, in plain terms. Keep it short; this isn't the skills repo's PR template, just enough for a reviewer to know what they're looking at.

## Step 6 — Hand back the result

Give them the PR URL and say plainly that it's now waiting on review — nothing changes for the rest of the team until someone merges it. Don't imply the edit is live anywhere yet.

## Guardrails

- **Never push to `main` directly, and never merge the PR** — not even if asked. Only the repo admin can approve and merge changes to the shared repo; that's the entire reason this goes through a PR instead of a direct push.
- **Never resolve a merge conflict by guessing.** Surface it and stop, per Step 4.
- **Only stage and commit the files the person meant to submit.** If the clone has other uncommitted changes lying around from something unrelated, ask before including them — don't sweep everything into one PR.
- This skill only ever touches the separate shared-repo clone, never the knowledge base itself — it doesn't edit, move, or commit anything under `0-Inbox/`, personal `1-Projects/` work, or any other private folder.
