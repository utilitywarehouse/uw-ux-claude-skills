---
name: knowledgebase-health-check
version: 8
description: Audit the health of the whole knowledgebase — link health across every note in the knowledge base, and, for any project with a Wiki/ folder, its content health too. Covers orphaned notes, broken links, plain-filename citations, stale pages, unprocessed sources, missing cross-links, contradictions, missing stakeholder entries, and page-format violations. Use this skill whenever someone asks about orphans, disconnected notes, graph view looking sparse, broken links, or wants the knowledge base or a wiki checked, audited or linted. Trigger on phrasings like "knowledgebase health check", "health check the vault", "run the health check", "check the health of my notes", "lint the vault", "lint the wiki", "audit the wiki", "why are there so many orphans", "check my links", "are there notes nothing links to", or "run the link check" — all of these should get the full pass, not just the mechanical half. Also use it after a bulk ingest, a folder reorganisation, or any session that created or moved a lot of notes, since those are exactly when link rot appears. Prefer this over a hand-rolled grep: the script already handles the false positives that make naive link-counting untrustworthy.
---

# Knowledgebase Health Check

Find the notes that have fallen out of the knowledge base's link graph, and the reasons they fell out.

## Why this exists

A knowledge base can look healthy and be badly disconnected. One knowledge base had 157 orphaned notes out of 260 while its two wikis were internally immaculate, because the wiki spec told Claude to cite sources as plain filenames (`**Sources**: Workshop summary.md`). That sentence *states* a relationship a reader can follow, but a linked-notes tool only draws an edge for real link syntax (`[[wikilink]]` or `[markdown link](file.md)`), so every cited source read as an orphan.

A previous lint had reported "no orphans found" three months earlier. It was scoped to pages inside one wiki, so it was blind to everything outside it. **Scope the audit to the whole knowledge base, not to a folder** — that single mistake is why the problem ran undetected.

## Running it

```bash
python scripts/vault_lint.py "/path/to/vault"
```

Options: `--quiet` omits the full orphan list (useful when it's long), `--json` emits machine-readable output for further analysis.

The script is read-only. It never edits, moves, or deletes anything, so it's safe to run before you've agreed what to fix.

To verify the script itself still behaves after any edit:

```bash
python scripts/test_vault_lint.py
```

That builds a synthetic knowledge base covering every check plus the known false positives, and asserts each result. If you change detection logic, add a case there first — every check in it exists because an earlier version got that case wrong.

## What it checks, and how to read each result

**Orphans** — no links in or out. Not automatically a problem. Daily notes, morning briefings and agent config files (`CLAUDE.md`, `MEMORY.md`) are reasonable orphans. Judge by whether anything *should* point at the note.

**Broken links** — a link resolving to nothing, wiki- or markdown-style. Worth fixing promptly for a reason beyond tidiness: clicking an unresolved link in Obsidian *creates* an empty note, so broken links quietly manufacture new junk notes. Common causes are a stale path segment after a folder rename, and instructional prose where a link syntax example (`[[wiki-links]]`, `[markdown links](example.md)`) was meant as an illustration rather than a real link (backtick those).

**Citations written as plain text** — usually the highest-value finding. A `**Sources**:` line, a `(source: X.md)` span, or a bullet under a `## Sources ingested` heading, naming a file that exists in the knowledge base but isn't linked. These are relationships already asserted in the prose, so converting most of them is mechanical: the prose already asserts the connection is real, so there's no judgement call about that part.

That third form was a blind spot until 2026-08-14. The check originally scanned only the first two, so a wiki's own `## Sources ingested` inventory — the one place a wiki deliberately lists where its knowledge came from — was the one place it never looked. Four plain-filename citations in the Cashback Card index survived every prior pass, including one that converted 203 citations elsewhere in the same knowledge base. Worth remembering the general shape of that mistake: a check scoped to the syntax you expect will miss the place where the same information is written in a different shape.

The judgement call that remains is whether the source is worth a graph edge at all. Transcripts, PDFs, and structured data exports — anything a *different* page might plausibly cite later — should convert on sight. But a source that's genuinely one-off, like a screenshot captured in `01-Inputs/` to give a single wiki-ingest session something to look at and never touched again (e.g. `tokens-1.jpg` through `tokens-6.jpg` cited by one Storybook-capture page), doesn't gain anything from being linked — nobody will ever navigate to it from the graph, so the edge is noise, not connective value. Flag these in the report so the citation is visible, but don't convert them to links without asking first.

**Frontmatter links resolving to nothing** — usually an unconfigured Obsidian Web Clipper. Its default `author` property is `{{author|split:", "|wikilink|join}}`, and the `wikilink` filter wraps every article author in `[[ ]]`. Article authors never have notes, so every clipping arrives with a permanent dead link. Fix the template, not just the files — and since this knowledge base uses markdown links, point the fix at a markdown-link filter instead of a wikilink one.

**Notes whose only links are inside backticks** — connected when you read them, orphaned to the graph. Changelogs and lint reports show up here legitimately, since they *name* pages rather than navigate to them. A wiki changelog with 33 backticked references and zero real links is honest, not broken; flag it, don't force it.

**Filenames differing only by case** — `About me.md` and `About Me.md` collide on macOS, so a short link can silently resolve to the wrong one. Use a path-qualified link (`[About Me](3-Resources/About%20Me/About%20Me.md)`) or rename one.

**Files in the knowledge base root** — the convention is that nothing lives in the root; everything files into one of the top-level folders. If notes keep appearing there, the cause is usually Obsidian's "Default location for new notes" being unset, which makes the root the default target for every new note including ones created by clicking a broken link.

## Wiki content checks

The checks above are mechanical — they read link syntax, not content, so a script can run them anywhere. When the lint target is (or includes) a project with a `Wiki/` subfolder, e.g. `1-Projects/Cashback Card/`, also read through the wiki's pages and run these seven. They need judgement about what a page says, so there's no script for them — do this as a reading pass, not a step to skip because it isn't automated.

This section replaces what used to live in a project's own `CLAUDE.md` under a `## Lint` heading — a checklist people used to trigger by saying "lint the wiki" before this skill existed. That heading is retired now; this skill is the one place both halves live. If you ever find a `## Lint` section in a project CLAUDE.md, it's a leftover — flag it to the user and offer to remove it.

**Format violations** — every content page should have Summary, Sources, Last updated, and Related pages, per the page format template in the area's `CLAUDE.md`. Flag pages missing any of the four.

**Uningested sources** — cross-reference a project's `01-Inputs/`, `03-Research/`, and `05-Synthesis/` folders against `Wiki/index.md` and existing pages' Sources lines. A source that exists on disk but has no corresponding page and no citation anywhere hasn't been processed yet.

**Stale content** — compare each page's "Last updated" date against what's happened since: a study wrapping up, a decision superseding an earlier framing, a capability going from planned to confirmed. A page can be internally tidy and still describe a state of the world that's moved on. Research pages are the exception — see "Sealed pages" below before flagging one as stale.

**Missing cross-links** — read a page's content for concepts it discusses but doesn't list under Related pages, and pairs of pages that cover the same ground without linking to each other.

**Contradictions** — two pages making incompatible claims about the same fact.

**Missing stakeholder entries** — someone credited with a finding, decision, or quote in page content who isn't listed in `stakeholders.md`.

**Concepts without a page** — an idea or entity that recurs across several pages in passing but has never been given its own page.

Report these under their own headings in the same dated report as the mechanical findings — match the section structure shown in `references/example-report.md`.

## Sealed pages: flag, never repair

Research findings are point-in-time. A study records what people said on a given date, under the customer mix, the marketing, and the version of the product in place then — and those conditions can't be recovered later. That's why a finding is never brought up to date. New data becomes a new record; it doesn't edit an old one.

**Sealed, wherever they sit:** research reports, study pages in `2-Areas/Research Repository/Studies/`, and any dated document reporting what research found.

**Still living:** topic pages in `2-Areas/Research Repository/Topics/`, which restate no figures of their own and so can grow as new studies land, and product wiki pages describing the product rather than a study. A page whose subject is one dated study is sealed even when it sits in a `Wiki/` folder.

Two of the checks above land differently on a sealed page:

- **Stale content.** An old research page isn't a defect — the age *is* the finding. Report it as context worth knowing ("this predates the rebrand, and Apple Pay support"), never as something to fix. Don't bump a "Last updated" date on a sealed page to clear the check; that destroys the only signal a reader has about when the evidence was gathered.
- **Contradictions.** When new data disagrees with an old finding, both are accurate records of their own moment. Report the disagreement and let the user decide whether it warrants a new study page. Reconciling them by rewriting the older page erases evidence, which is the opposite of what this pass is for.

The single edit a sealed page can take is a figure mistyped from the raw source it already cites — that's a correction, and it gets recorded alongside the fix. New data is never a correction.

## Reporting findings

Write the report to `2-Areas/Knowledgebase Maintenance/YYYY-MM-DD Knowledgebase Health Check Report.md` for a knowledge-base-wide run. For a run scoped to one area's wiki rather than the whole knowledge base, name it `2-Areas/Knowledgebase Maintenance/YYYY-MM-DD [Area] Knowledgebase Health Check Report.md` instead (e.g. `2026-06-03 Cashback Card Knowledgebase Health Check Report.md`). `0-Inbox/` is reserved for Obsidian's own daily notes, so these reports don't belong there even though they're dated files — knowledgebase upkeep is an ongoing responsibility, not a day's inbox item. Lead with the counts, then the findings that need a decision.

Reports written before 2026-08-25 use the older `Vault Lint Report` and `[Area] Wiki Lint Report` names. Those are point-in-time records and keep the names they were written under — recognise them as this skill's own output when working out what a new run supersedes, but never rename them.

Two things to get right in the write-up:

- **Give absolute numbers and say what instrument produced them.** If you quote an orphan count, be able to say whether fenced and backticked examples were counted. They shouldn't be, and a scanner that counts them can overstate connectivity enough to hide real orphans.
- **Separate "needs fixing" from "fine as an orphan".** A raw count of orphans invites pointless work. What matters is notes that *should* be reachable and aren't.

Propose fixes; don't apply them unasked. Deletions and renames in particular need the user's explicit approval, per the knowledge base's CLAUDE.md.

**Archive superseded reports.** A new knowledge-base-wide report makes every earlier knowledge-base-wide report stale — nobody needs the orphan count from two runs ago once a current one exists. A new area-scoped report only supersedes earlier reports scoped to that *same* area, not other areas or knowledge-base-wide runs.

After writing the new report, move each report it supersedes into `4-Archives/Knowledgebase Maintenance/`, keeping the filename exactly as it is. Create that folder if it doesn't exist yet. Then say plainly in the session output which files moved and where to — don't leave the move silent.

Three rules that keep this from going wrong:

- **Move, never delete.** The knowledge base's CLAUDE.md's "never delete without asking" rule still stands, and archiving sidesteps it because nothing is lost. That also means deletion is never this skill's job, even when the ask is phrased as "clean up" or "get rid of the old ones" — offer the archive move instead, and let the user delete by hand if they really want to.
- **Check for inbound links first.** If any note in the knowledge base links to a report, leave that report where it is and say why. An archived file that something still points at is a broken link this skill created itself.
- **Never archive the report you just wrote**, and never archive a report from a different scope than the run that just finished.

## When findings point at a generator rather than a file

If the same defect appears in many files, look for what produced them. For example, if two project CLAUDE.md files both mandate plain-text citations because `new-project-setup` carries that spec in its own template, every new project inherits it. Fixing the files without fixing the generator means the next project starts broken again.

Sources worth checking when a defect looks systemic: the `new-project-setup` skill's embedded CLAUDE.md template, the `transcript-cleaner` and `transcript-coder` frontmatter templates, the Obsidian Web Clipper's property template, and Obsidian's own settings.
