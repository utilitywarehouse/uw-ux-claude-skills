This is the UX team's shared skills repo. It ships purely through GitHub pull request via the `contribute-to-skills-repo` skill — see `plugins/ux/skills/contribute-to-skills-repo/SKILL.md` for the full workflow.

## Working rules

- After editing any `SKILL.md` or `plugin.json` under `plugins/ux/`, don't just report the edit as done and stop there — in the same turn, ask whether to commit and ship it via `contribute-to-skills-repo`. Don't wait to be asked. An edit left sitting uncommitted is easy to miss, and not everyone working in this repo knows to ask for it.
- After a PR opened from this repo is confirmed merged, switch back to `main`, pull the latest changes, and delete the merged branch (locally, and remotely if GitHub hasn't already removed it) — do this automatically, without being asked.

## Writing the docs site (`docs/`)

Follow these rules for any writing in the `docs/` Starlight site:

- **Clarity**: write in simple, clear, unambiguous language.
- **Accuracy**: all information, especially code snippets and technical details, must be correct and up to date.
- **User-centricity**: prioritize the user's goal — every page must help a specific reader do a specific task.
- **Consistency**: keep tone, terminology, and style consistent across all pages.
- **Terminology**: the Glossary (`docs/knowledge-base/glossary`) is the source of truth for naming recurring concepts (Routing Map, Wiki, symlink, etc.). Check it before introducing a new name for something that already has one, and add an entry when a skill introduces a new concept worth naming consistently.
