---
name: transcript-coder
version: 2
description: Code a cleaned UX research transcript with qualitative labels ready for thematic analysis and cross-session synthesis. Use this skill whenever a transcript is ready for analysis and the request is "code this", "apply codes", "tag this session", "analyse this transcript", or when transcript cleaning has just finished and it's time to decide what's next. Also trigger when working through the analysis phase of a research project with one or more sessions to code. Pairs naturally after the transcript-cleaner skill. When multiple sessions are being coded, this skill manages a shared codebook to ensure consistency across the study.
---

# UX Transcript Coder

Turn a cleaned research transcript into a coded document ready for thematic analysis — and maintain a shared codebook across all sessions in a study, so synthesis later is consistent and tractable.

## What this produces

**Per session:**
- A coded transcript — the full transcript with inline code tags on meaningful segments
- A quotes-by-code section — all coded excerpts grouped by code, for easy synthesis

**Per study (shared, updated after each session):**
- A living codebook — every code used across all sessions, with descriptions and cumulative frequency counts

## Before you start

You need:

1. **The transcript** — file path or pasted content
2. **The discussion guide** — to understand what the session was trying to answer. Find it in the project folder if not provided. Note: guides are rarely followed exactly, so some topics may be missing or covered differently.
3. **The existing codebook** (if this isn't the first session) — look for `Codebook.md` in the same research folder. If it exists, load it and use those codes.

## Coding approach

**First session in a study:** Use a hybrid approach. Derive 3–5 seed codes from the discussion guide topics, then add new codes inductively as the data warrants.

**Subsequent sessions:** Load the existing codebook and apply it deductively. Add new codes only when a segment genuinely doesn't fit anything in the codebook — don't create near-duplicates. After coding, update `Codebook.md` with any new codes and updated frequency counts.

If an existing codebook is provided explicitly, always use it as the starting point regardless of session number.

## How to code

Work through the transcript sequentially. For each section or exchange:

1. Read the full section before applying codes
2. Identify the **meaningful segments** — moments where the participant expresses a behaviour, mental model, pain point, workaround, need, motivation, reaction, or decision. Not everything needs coding — facilitator questions, filler phrases, and purely contextual background can be left untagged.
3. Assign codes in `[square-bracket]` format, immediately after the relevant text
4. A segment can carry multiple codes: `[code-one] [code-two]`
5. Keep codes short (1–3 words), descriptive, and consistent. `[pain-point]` means the same thing every time across every session.

**Good codes:** `[pain-point]`, `[workaround]`, `[mental-model]`, `[positive-reaction]`, `[feature-request]`, `[confusion]`, `[trust-barrier]`, `[habit-formation]`, `[motivation]`, `[objection]`, `[use-case]`, `[unmet-need]`

**Code discipline — this is where most coding goes wrong:**

Aim for **8–20 codes per session**. If you're approaching 25+, you're over-coding. More codes doesn't mean more rigour — it means harder synthesis.

Before creating a new code, apply this test: *"Would this code group different quotes than any existing code?"* If the answer is no, use the existing code. `[competitor-reference]`, `[competitor-comparison]`, and `[competitor-mention]` are the same code — pick one and use it consistently.

Treat single-occurrence codes with suspicion. If a code appears only once across the whole transcript, ask whether it's genuinely a distinct concept worth tracking, or whether it could fold into something broader. Singleton codes that represent truly important moments are fine — but a long tail of singletons usually means the codebook is too granular.

When in doubt, go broader. It's always possible to split a code later; merging codes after the fact is harder. `[reaction]` is better than separate codes for `[positive-reaction]`, `[negative-reaction]`, `[neutral-reaction]`, and `[mixed-reaction]` — especially on a first pass.

## Output files

### 1. Coded transcript
Filename: `YYYY-MM-DD [Session Title] — Coded.md`  
Save alongside the cleaned transcript in the project research folder (`03-Research/`).

The `transcript:` and `codebook:` fields matter more than they look. A coded transcript only means something next to the cleaned source it was coded from and the codebook whose codes it applies — but those live in separate files, and without links a reader has to reconstruct the relationship from filenames. Link them and each coded file becomes navigable in both directions: open the codebook and see every session that used it, open a coded file and jump straight to the verbatim it came from. Quote the links so the YAML stays valid. Point `transcript:` at the actual cleaned filename for this session, not the placeholder.

```
---
session: [Title]
participant: [Name or P1/P2 etc.]
date: [date]
method: [interview / usability test / diary study]
coded-by: Claude
codebook-version: [n]
transcript: "[YYYY-MM-DD Session Title — Cleaned Transcript](YYYY-MM-DD%20Session%20Title%20—%20Cleaned%20Transcript.md)"
codebook: "[Codebook](Codebook.md)"
---

## Quotes by code

### [code-name]
- "[Exact quote]" — [Participant name/handle], [timestamp if available]
- "[Exact quote]" — [Participant name/handle]

### [another-code]
- "[Quote]" — [Participant]

---

## Coded transcript

**[Speaker]:** Meaningful segment of text. [code-one] [code-two]

**[Speaker]:** Uncoded passage — not analytically significant.

**[Speaker]:** Another meaningful segment. [mental-model]
```

### 2. Shared codebook
Filename: `Codebook.md`  
Save in `03-Research/` (one file for the whole study, not per-session). Create it on the first session; update it after each subsequent session.

```
# Codebook — [Study Name]

Last updated: [date] after [N] sessions

| Code | Description | Sessions | Total occurrences |
|------|-------------|----------|-------------------|
| pain-point | Participant describes something frustrating, difficult, or broken | P1, P2 | 7 |
| workaround | Participant describes an improvised behaviour to circumvent a problem | P1 | 2 |
| habit-formation | Participant mentions building, breaking, or resisting a behavioural habit | P1, P2, P3 | 9 |
```

## After coding each session

Report back:

- Which session number this is and how the codebook now stands (total codes, any new ones added this session)
- The top codes by frequency in **this session** — and whether they're consistent with or diverging from previous sessions
- Whether the discussion guide topics appear to be covered, and flag any that weren't touched
- Any new codes that emerged, with a recommendation on whether they're distinct enough to keep or should be merged with an existing one

If this is the final session in the study, say so and suggest moving to synthesis.
