# [Product Name]

This is the shared workspace for all [Product Name] projects.

## Folder structure

[Product Name]/
  CLAUDE.md               ← this file (points to Wiki/Area-Conventions.md for wiki rules)
  Wiki/
    Area-Conventions.md   ← shared wiki conventions
    index.md
    log.md
  [Project Name]/         ← one folder per project
    CLAUDE.md
    MEMORY.md
    01-Inputs/    ← source documents for that project (immutable — never modify)
    02-Planning/
    03-Research/
    04-Competitive/
    05-Synthesis/
    06-Deliverables/

## Starting a session

1. Check memory and context to determine which project is active. If it's clear, state it and proceed. If it's ambiguous or memory is absent, ask the user to confirm before continuing.
2. Navigate to that project folder and read its CLAUDE.md.
3. You're ready to respond to the initial question or task.

## Wiki conventions

This area's Wiki has its own shared conventions — purpose, ingest workflow, page format, citation rules — kept in [Wiki/Area-Conventions.md](Wiki/Area-Conventions.md). Read it before making any change under `Wiki/`; it's shared and kept current by the team, not by this file.
