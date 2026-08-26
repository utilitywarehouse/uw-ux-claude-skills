# Study card format

The canonical structure for a one-page study card. This is the source of truth for the format — don't defer to a knowledge base's own `Research Repository/CLAUDE.md` for structure, only for the tag taxonomy (see below).

## Structure

```markdown
---
tags: [type, product, method, segment, year tags — see Tag taxonomy]
---

# [Study title]

**Summary:** [one or two sentences]
**Sources:** [markdown links to raw data, coded transcripts, or other source material](path/to/source.md)
**Full report:** [markdown link to the report](path/to/report.md), or a plain statement that none exists and why
**Last updated:** YYYY-MM-DD

---

## Method
[Survey / interview / usability test / workshop / diary study, plus:]
**Fielded:** [exact dates, from raw data where possible]
**Sample:** [how many answered, how many skipped, who they were]
**Run by:** [person or team — "Unknown" is fine, silence is not]
**Raw data:** [path to it, or an explicit statement it isn't held]
**Verify mode:** [Recount / Transcribe-check / Second-hand — see the skill's process for how this gets chosen]

## Sample
[Detail beyond the Method block if useful — demographics, response rate, exclusions]

## Findings
[Headlines only when a report exists — one line per finding, detail lives in the report.
Full detail when no report exists — nothing else holds it.]

## Limitations
[Sample size, self-selection, age of the study, anything that's changed since]

## Corrections
[Optional. Only present if a figure was corrected against its own cited source. Table: what it said, what it was corrected to, why.]

## PII
[Optional. Only present if the raw data or report carries participant-identifying information worth flagging — e.g. a column in a CSV, a name in an appendix.]

## Related pages
[Markdown links to Topics pages, other study cards, or product Wiki pages this connects to]
```

No other headings. If something doesn't fit one of these, it doesn't belong on the card — see `routing-examples.md` for where it actually goes.

## Required fields

Method, Fielded, Sample, Run by, Raw data, Full report, Findings, Limitations.

"Not recorded" is an acceptable answer for any of these. Leaving one out silently is not — a missing field reads as an oversight, not a considered gap.

## Citation format

Cite every factual claim as `(source: [Source Name](path/to/source.md))`. Use markdown links, never bare filenames — a markdown link keeps the file extension (`.md`, `.pdf`, `.csv`), since it points at a real file path, not a page-name lookup. Path-qualify any link to a file that exists in many places in the knowledge base (a `CLAUDE.md`, `MEMORY.md`, or `index.md` by bare name resolves unpredictably).

## The no-participant-names rule

A study card never names a participant, under any circumstance — even when the report behind it does. This is what keeps a card shareable anywhere the knowledge base is shared, while the report stays restricted.

Colleague attribution is fine and expected: `**Run by:** [name]`, or a source citation naming whoever ran the study. The rule is about participants, not colleagues.

## Sealing

A card is sealed the moment it's written. No edits, no additions, no tidying afterward. New data about the same topic is a new card, never a change to this one.

The one exception: a figure that was mistyped from the source it already cites. That's a correction, not new data — fix it and record what it was corrected from and why, under `## Corrections`. New data is never filed as a correction.

## Tag taxonomy — the one locally-owned part

Everything above is fixed by this skill. Tags are the exception, because they depend on which product or team the knowledge base belongs to — a taxonomy built for one product area won't fit another team's, different, product area.

Before tagging a card, check the knowledge base's own `Research Repository/CLAUDE.md` for an existing tag taxonomy. If one exists, use it as-is — don't invent variants. If none exists, ask what tags to use rather than guessing; propose a starting taxonomy (type, product, method, segment, year fielded) if none exists and the user wants a starting point.
