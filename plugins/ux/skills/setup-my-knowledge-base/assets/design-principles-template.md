---
type: reference
title: Design Principles
description: A working record of design heuristics and judgement calls that apply across projects.
tags: []
---

# Design Principles

A working record of design heuristics and judgement calls that apply across projects — separate from any visual design system (colours, components, spacing). This is about *how* to make product design decisions, not visual specification.

Add a new principle whenever a real decision teaches you something worth reusing. Each one should read like a rule you'd want a teammate to know, backed by a concrete example — not an abstract maxim.

---

## Write show-if logic for people, not just engineers

Before treating any show-if rule or scenario logic as finished, check: any time-period term (e.g. "billed month") is defined once and reused consistently rather than drifting into casual phrasing partway through; the comparison baseline is the one that's actually correct (e.g. "beats the highest of all previous periods," not just the immediately preceding one); multi-condition rules spell out "ALL of" / "ANY of" explicitly; every outcome is covered, including ties. This checklist catches real logic bugs before they reach engineering.

Write the logic itself in plain English, not notation — no maths symbols (`>`, `≥`) and no algebraic placeholders, use words and concrete example values with one line saying what the examples stand for. These specs get demoed to PMs and stakeholders, not only built by engineers. Keep the precision-bearing parts though: the ALL-of/ANY-of framing, and tie-covering phrases like "the same as, or less than" — dropping those lets a tie fall through a crack, or an OR get built where an AND was meant.

**Example**: A discount rule written as "if spend > last month" hides two bugs — is "last month" the one just gone, or the best of all previous months, and what happens on a tie? Rewritten as "Show if ALL of the following are true: the customer's spend this month is the same as, or more than, their highest spend in any previous month" removes both ambiguities and reads the same to an engineer and a stakeholder.

*(from a team review of engineering handoff specs)*

---

## [Principle name]

[The rule itself, one or two sentences.]

**Example**: [A real situation where this applied, and what you did.]

*(from [project or note], [date])*
