# Content routing

Before writing a line onto a study card, decide where it actually belongs. Most of the real damage in a bad card isn't wrong facts — it's true, useful content filed in the wrong place, where it either clutters the card or never gets found again.

## What's a Topic, for readers who haven't met one yet

A Topic is a living page that synthesizes across multiple studies. It carries no figures of its own — every figure it mentions is sourced back to a study card. It's allowed to grow over time, unlike a sealed card or report.

That's the whole reason cross-study content can't live on a card: a card is sealed the moment it's written, and a comparison across studies needs to keep updating as new studies land.

## What goes on the card

- What was asked, of whom, when, by whom.
- Figures, with counts alongside percentages, not one without the other.
- Limitations specific to this study.

## What doesn't, and where it actually goes

| This kind of content | Goes to |
|---|---|
| A comparison between this study and another | A Topics page — flag the proposed addition, don't write it there directly |
| A definition of a metric, or an explanation of how a product mechanic works | The product Wiki — flag it, don't write it there directly |
| "What should happen next" that's about the product or business, not about this study's own limits | Limitations, if it limits the study itself; otherwise a Topics page's open questions — flag it |
| "What should happen next" that's about this study's own gaps (small sample, self-selection) | Limitations, on the card itself |

Flag means: tell the user what belongs where and show the proposed text. This skill never writes to a Topics page or the product Wiki itself, and never creates a new Topic page even if none exists yet for the subject — that decision, and that edit, stays with the user.

## The one true exception: an incidental finding

Sometimes a finding wasn't the product of its own study — it came up in passing while researching something else entirely, with no dedicated study ever run and no report that will ever exist for it, by design. That's the one case where the card carries the full finding itself, because nothing else ever will hold it.

This is not a fallback for "the report hasn't been written yet." Every real study still gets a report first, always. Before treating a missing report as this exception, confirm with the user that it genuinely was never a dedicated study — don't assume.

## Worked examples

**Wrong:** A card's Findings section includes a table comparing this study's activation rate to a survey run two years earlier.
**Right:** That comparison goes on a Topics page. The card's Findings section states only what this study found.

**Wrong:** A card defines what "the billed month" means for the product, because the finding depends on that definition.
**Right:** The definition goes on the product Wiki, linked from the card. The card states the finding and links to the definition rather than restating it.

**Wrong:** A card's Limitations section recommends a specific UI fix ("the cap-warning banner should say X instead of Y").
**Right:** The card's Limitations section notes the UI issue was flagged as worth investigating further; the specific fix is a design decision, not a research finding — see `analysis-discipline.md`.
