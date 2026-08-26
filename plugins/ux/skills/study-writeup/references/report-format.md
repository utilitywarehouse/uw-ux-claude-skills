# Report format

The canonical structure for a full research report. This is the source of truth — follow it exactly, every time, for every team member. Don't adapt it to match whatever an individual knowledge base already has on file; a shared structure is the point, and matching local habit lets reports drift apart again.

## Structure

```markdown
**Study:** [title]
**Author:** [person or team who wrote this report]
**Completed:** [the date the study finished — not the date this report was written]
**Audience:** UW-internal only (reports may name participants; study cards, downstream of this, may not)

---

## Executive Summary
[Half a page, no more: the objective, the method in 1-2 sentences, the top 3 findings,
the primary recommendation. Written so a stakeholder who reads nothing else still has
the shape of the study.]

## What we set out to learn
[The research question(s) and why they mattered at the time]

## Methodology
[Method, sample, recruitment, timeline, analysis approach. State plainly whether synthesis
in this report was AI-assisted and human-reviewed before publication — see "Methodology
disclosure" below.]

## Summary
[A short narrative summary of what was found, ahead of the detailed findings below]

## Findings
[One heading per theme. Each theme carries its evidence — quotes, counts, frequency —
directly under it, not gathered separately.]

### [Theme 1 name]
...

### [Theme 2 name]
...

## Methodological notes
[Anything a reader needs to correctly weigh the findings: sample caveats, contamination,
things that went differently than planned]

## Recommendations
| Priority | Recommendation | Rationale | Effort |
|---|---|---|---|
| High | ... | ... | L/M/H |

[Every row stays in research's lane — see analysis-discipline.md. A recommendation proposes
investigating or testing something further. It never prescribes the specific copy, design,
or engineering fix; that decision belongs to whoever owns that discipline, not to this report.]

## Next Steps
[Immediate follow-up actions and open questions — written from the vantage point of the day
the study finished, not as a status update on today. See report-writing-rules.md.]

## Appendix
[Discussion guide or survey instrument, anonymized participant details, full quote bank]
```

## Filing

Write the report into the owning project's synthesis folder first. Then file a sealed copy into the knowledge base's `Research Repository/Reports/` — the two are permitted duplicates of the same sealed content, not a drift risk, because neither is ever edited after writing.

## Methodology disclosure

State in the Methodology section whether this report's synthesis was AI-assisted, and that findings were reviewed by a person before the report was sealed. This isn't optional flavour text — a report is read long after the session that produced it, and a future reader has no other way to know how the findings were produced.

## Sealing

A report is sealed the moment it's written, with one pause: hold before sealing for the author to approve it (see the skill's process for what gets specifically flagged at that point). Once approved and sealed, no edits, no additions, no tidying. New data is a new report, never a change to this one — the one exception is a figure mistyped from the source it already cites, corrected and recorded as such, same as a study card.
