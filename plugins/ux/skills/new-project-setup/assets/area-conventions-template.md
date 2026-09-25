# Wiki

A shared knowledge base maintained across all [Product Name] projects.

## Purpose

The wiki is the canonical store for [Product Name] product knowledge — concepts, hypotheses, entities, research findings, and competitive intelligence. It compounds over time. Project-specific status, decisions, and actions belong in project MEMORY.md files, not here.

## Default behaviour

- Before answering any question about [Product Name], read `Wiki/index.md` and any relevant pages. If the answer is there, use it. If it's not, say so clearly.
- When searching for context or background, treat the wiki as the first port of call — before project folders or memory.
- When the user shares new information about the product, a stakeholder, or a concept — even in passing — offer to add it to the wiki.
- When a question generates a valuable answer not already in the wiki, offer to save it as a new page.

## Ingest workflow

When the user adds a new source to a project's `01-Inputs/` and asks you to ingest it:

1. Read the full source document
2. Discuss key takeaways with the user before writing anything
3. Create a summary page in `Wiki/` named after the source
4. Create or update concept pages for each major idea or entity
5. Add markdown links (`[Page Title](page-name.md)`) to connect related pages
6. Update `Wiki/index.md` with new pages and one-line descriptions
7. Append an entry to `Wiki/log.md` with the date, source name, and what changed

A single source may touch 10–15 wiki pages. That is normal.

## Question answering

1. Read `Wiki/index.md` to find relevant pages
2. Read those pages and synthesise an answer
3. Cite specific wiki pages in your response
4. If the answer is not in the wiki, say so clearly
5. If the answer is valuable, offer to save it as a new wiki page

## Page format

```markdown
# Page Title

**Summary**: One to two sentences describing this page.

**Sources**: List of raw source files this page draws from, each as a markdown link.

**Last updated**: Date of most recent update.

---

Main content goes here. Use clear headings and short paragraphs.

Link to related concepts using [markdown links](path/to/note.md) throughout the text.

## Related pages

- [Related concept 1](path/to/related-concept-1.md)
- [Related concept 2](path/to/related-concept-2.md)
```

## Citation rules

- Every factual claim should reference its source file
- Use the format `(source: [Source Name](Source%20Name.md))` after the claim, linking the source file rather than naming it as plain text. A plain-text filename doesn't create a link, so the source it points at reads as unconnected even though something cites it
- Always keep the file extension in the link target (`.md`, `.pdf`, whatever the file actually is) — a markdown link points at a real file path, not a page-name lookup
- If `CLAUDE.md`, `MEMORY.md` or `index.md` exists in more than one place in the knowledge base, path-qualify the link so it resolves to the right one, and leave filenames used as ordinary nouns as plain text
- If two sources disagree, note the contradiction explicitly
- If a claim has no source, mark it as needing verification
- If a source lives only in the private vault — not in this shared repo, and not something the team can open through it — cite it as plain text: just the file name, extension included (e.g. `Workshop summary.md`), no link of any kind. If it was previously an aliased wikilink, use the real file name, not the alias text.

## Rules

- Never modify anything in a project's `01-Inputs/` folder
- Always update `Wiki/index.md` and `Wiki/log.md` after changes
- Keep page names lowercase with hyphens (e.g. `machine-learning.md`)
- Write in clear, plain language
- When uncertain about how to categorise something, ask the user
