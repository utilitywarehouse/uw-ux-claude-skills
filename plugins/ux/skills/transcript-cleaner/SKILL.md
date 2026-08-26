---
name: transcript-cleaner
version: 2
description: Clean video transcripts from UX research sessions — moderated interviews, usability tests, and unmoderated test recordings — into a coding-ready markdown file for your knowledge base. Use this skill whenever the user provides a raw transcript (pasted text, uploaded file, or referenced from Drive/Dovetail) and wants it tidied up for analysis. Trigger on phrases like "clean this transcript", "tidy up this session", "prep this for coding", "remove the fillers", "intelligent verbatim", or when they upload a .vtt, .srt, .txt, .docx, or messy interview text and asks for it to be made readable. Also trigger when they share a Userlytics, Dovetail, Google Meet, Zoom, or Teams transcript export with any framing that suggests it's headed for thematic analysis — even if they don't say the word "clean". When in doubt, this skill is what they mean.
---

# UX Transcript Cleaner

Turn raw transcripts from user research sessions into coding-ready markdown files for your knowledge base. The skill applies **intelligent verbatim** cleanup — meaning hesitation and meaning are preserved, but noise and inconsistency are removed — without rewriting what participants actually said.

## What "clean" means here

Intelligent verbatim is the industry standard for UX thematic coding. It reads cleanly enough to code in Dovetail, but still preserves the participant's actual words, hesitation, and emotional signals.

**Removed or standardised:**
- Fillers ("um", "uh", "er", "ah", non-meaningful "like" and "you know")
- Stutters and repeated false starts ("I-I-I went to" → "I went to")
- Standalone backchannel turns from the moderator that carry no information ("MOD: Yeah. Yeah.", "MOD: Mhm.", "MOD: Yep. Right."). These exist to keep the participant talking on the recording but add nothing on the page — strip the entire turn. Keep the turn if MOD adds anything substantive ("Yeah, that's interesting — say more?" stays).
- Inconsistent speaker labels
- Inconsistent product/UI/jargon spelling
- Inconsistent formatting (timestamps, dashes, contractions, numbers)

**Preserved at all costs:**
- Hedges that change certainty: "I think", "maybe", "kind of", "sort of", "probably"
- Meaningful false starts that show changing thoughts ("I went to the — actually I clicked the menu")
- Self-corrections and contradictions (these often matter analytically)
- Negations — never delete a "not"
- Emotional/prosodic markers when the source notes them ("[laughs]", "[sighs]", "[long pause]")
- The participant's actual word choice — never replace "angry" with "frustrated" or similar

**The "do no harm" rule:** if removing or changing something could affect *what was said*, *who said it*, or *how certain they sounded*, leave it alone. When tempted to "fix" something, pause and ask whether you're cleaning or rewriting.

## Workflow

### 0. Locate the transcript

If a transcript was pasted into the message or uploaded as a file, use it directly and skip to step 1.

If no transcript was provided, look for one in the active project's inputs folder. Raw transcripts are stored at:

```
1-Projects/[Project]/01-Inputs/Interview transcripts/
```

List any `.vtt`, `.srt`, `.txt`, or `.docx` files found there and ask the user which one to clean. If the project isn't clear from context, ask which project this is for before searching.

If no files are found and nothing was provided, ask the user to paste or upload the transcript.

### 1. Confirm session metadata

Before doing anything else, use `AskUserQuestion` to ask three things in a single call:

1. **Cohort**: *"Is this a single-cohort study or a multi-cohort study?"*
   - **Single-cohort**: set `cohort: N/A (single-cohort study)` in the frontmatter.
   - **Multi-cohort**: follow up with *"What's the cohort label for this participant?"* and wait for the user to type it. Use exactly what they provide as the `cohort` value — with one exception below.
   - **Match the spelling already in use.** Before writing the value, check the `cohort` field on other cleaned sessions in the same study. If this group already has a label there, reuse that exact string even if the user typed a variant this time ("Partner" vs "Partners", "Active customers" vs "Active Customer cohort"). This is about spelling, not classification: you still take the cohort itself from the user's answer and never infer it. But a study with eight spellings of four cohorts can't be filtered or grouped, and the drift is invisible until synthesis, when someone has to reconcile it by hand. If the user's answer looks like a genuinely new cohort rather than a variant spelling, use their wording and mention that it's new.

2. **Session date**: *"What date did this session take place? (YYYY-MM-DD)"*
   - Use the confirmed date in the frontmatter `session_date` field and as the `YYYY-MM-DD` prefix in the filename.
   - Never infer or guess the date from the source — always ask.

3. **Source platform**: *"What platform was this recorded on?"* Offer options: Zoom, Teams, Google Meet, Userlytics, Dovetail, or other.
   - Use the confirmed value in the frontmatter `source` field.
   - Never infer the source from the file format. A plain `.txt` or `.md` file strips all platform-specific signals — guessing from file shape alone will produce wrong answers.

Don't skip any of these. Cohort, date, and source are never reliably derivable from a plain transcript file, and all three affect the frontmatter and filename. **Never infer cohort from context, glossaries, participant metadata, or anything in the source.** Even if a participant's role or segment is visible elsewhere, that is not a substitute for a confirmed answer. Always ask directly and wait for the user to respond before proceeding.

### 2. Identify source and session type

Two things shape every other decision in the cleanup, so figure them out before you start editing.

**Source format** — use the value confirmed in Step 1. Do not attempt to infer it from the file. Use the source to inform your cleanup approach:
- **Userlytics export**: Often a single P speaker with task-based segmentation, screen-recording timestamps, and on-screen task prompts mixed in. Common in unmoderated tests.
- **Dovetail export**: Usually already has speaker labels and timestamps; cleaning needed is minimal — mostly fillers and consistency.
- **Google Meet**: Timestamps in `00:00:00.000` format, often messy punctuation, frequent mishearings of UI/product terms.
- **Zoom / Teams**: Frequent jargon errors, sometimes wrong attribution at speaker boundaries.
- **Other**: Treat as plain text — proceed on structure alone.

**Session type:**
- **Moderated interview** — Q&A flow, MOD turns shorter, P turns longer.
- **Moderated usability test** — think-aloud commentary, task boundaries, observed actions in `[brackets]`, emotional/prosodic notes.
- **Unmoderated test** — usually one P throughout, on-screen task prompts, more silent/confused stretches.

If either is unclear from the input, **ask the user before proceeding** — getting these wrong cascades into the wrong cleanup decisions.

### 3. Load project context

Before building the glossary, check whether the project has a wiki or reference area. Check the root `CLAUDE.md`'s folder map for where that lives — look for a `Wiki/` subfolder inside the project folder, or any area it points to for organisational or product reference material. Scan whatever you find for terms, events, people, or internal names that appear in the transcript. Resolve these before flagging them as unclear — if a term is documented there, use the approved spelling and context. This step prevents avoidable `[unclear]` tags on things that are simply documented elsewhere in the knowledge base.

### 4. Apply or build a glossary

Names, product/UI terms, and acronyms create the most search and coding errors because small variants ("Cashback card" vs "cashback card" vs "CBC") look like different concepts in coding tools.

**Before deciding on the glossary approach, ask the user** (using `AskUserQuestion`): is this transcript one of several sessions in the same study, or a standalone? This changes how the glossary is handled.

**If it's one of several sessions in a study:**
- Check the project folder (wherever cleaned transcripts are being saved, e.g. `03-Research/`) for an existing shared glossary file — typically named `[Project Name] — Research Glossary.md` or similar.
- **Shared glossary found**: load it, apply approved spellings throughout this transcript, and extend it with any new terms encountered in this session. Save the updated glossary back to the same file.
- **No shared glossary found**: build one during cleaning and save it to the project folder (not alongside just this transcript). Name it `[Project Name] — Research Glossary.md`. Flag in your chat summary that it's been created and should be applied to all remaining sessions in the study.
- Record the shared glossary as a link in the frontmatter `glossary:` field, quoted so it stays valid YAML: `glossary: "[Project Name — Research Glossary](Project%20Name%20—%20Research%20Glossary.md)"`. Naming it as plain text looks the same to a reader but creates no link, so the glossary ends up orphaned even though every session in the study depends on it — and you lose the ability to open one glossary and see which sessions applied it. Reference it in the cleaning notes too if that reads naturally, but the frontmatter field is what connects them.

**If it's a standalone session:**
- **If the user uploaded or pasted a glossary**: use it. Apply approved spellings throughout.
- **If no glossary is provided**: build one as you go. Track every product name, UI element, person's name, organisation, and acronym. Output it as a separate `[project-name]-glossary.md` file alongside the cleaned transcript.

**For uncertain terms** (likely mishearings of UI elements, technical jargon, or names): tag inline preserving BOTH the literal source word and your best guess, in the format `[unclear: "literal-from-source" — best guess?]`. Examples: `[unclear: "nyance program" — loyalty programme?]`, `[unclear: "Spive" — Quidco?]`, `[unclear: "8780" — £87.80?]`. The literal text matters because the user may want to Cmd+F back to that point in the recording; the best guess matters because the transcript still needs to read fluently for thematic coding. If you genuinely can't guess, just `[unclear: "literal-from-source"]` is fine. Surface every unclear segment in the cleaning notes with its timestamp.

### 5. Standardise speaker labels

Default convention:
- `MOD:` — Moderator / interviewer
- `P1:`, `P2:` — Participants (numbered in order of appearance)
- `OBS:` — Observer (rare; only if observers contribute)

Each speaker turn starts on a new line, separated by a blank line for readability. Pick one form and apply it everywhere — drop the dash/colon/bracket variants you sometimes see in raw exports.

**Where the real names go.** In the **transcript body**, only ever use the coded labels (`MOD:`, `P1:`). In the **frontmatter**, expand each label with the real name and any relevant context the source gives you (role, age, demographic, tenure, segment) so the user can recover the mapping at a glance without opening the glossary. Pull this context from the source — interview screeners, attendee headers, observer notes, Userlytics participant metadata. If the source doesn't give you context beyond a name, just include the name. Format examples:

- `participants: P1 (Charlotte Egan, partner, 13 months tenure)`
- `moderator: MOD (Real Name)`
- Multiple participants: `participants: [P1 (Sarah Khan, 38, homeowner), P2 (Tom Davies, 52, renter)]`

This pattern matters more than it looks: if the user has 12 cleaned interviews open in Dovetail, they need to glance at one frontmatter block and know who P1 is without cross-referencing a glossary file. Don't put the name expansion in the glossary — put it in the frontmatter.

### 6. Apply intelligent verbatim rules

Go through the transcript and apply the rules from the "What 'clean' means here" section above. Apply rules **evenly to every speaker** — never clean one participant more than another, as that introduces bias.

Specific decisions:
- **Numbers**: Numerals for everything except sentence-starts ("ten" → "10", but "Ten minutes later").
- **Contractions**: Keep them as the participant used them ("don't" stays "don't"; don't expand to "do not" unless the source uses the long form).
- **Timestamps**: Keep them if present, in `[HH:MM:SS]` format. Drop if absent — don't fabricate.
- **Paragraphing**: Keep speaker turns short. Long monologues are fine as one turn but break for natural pauses.
- **UK spelling**: Default to UK English — "organisation", "behaviour", "colour" — unless the source uses US spelling consistently.

### 7. Apply session-type rules

**Moderated interview**: Standard Q&A. Just the rules above.

**Moderated usability test (think-aloud)**:
- Preserve task boundaries. If the source notes "Task 1: Find the rewards page", keep it as a heading: `### Task 1: Find the rewards page`.
- Preserve observed-action notes in `[brackets]` if they're in the source (e.g. `[clicks Settings icon]`, `[scrolls to bottom]`, `[hovers over CTA]`). Don't fabricate them.
- Preserve emotional/prosodic markers (`[laughs]`, `[long pause]`, `[frustrated tone]`) — these are signals of usability problems and stripping them loses analytical value.
- Don't try to separate think-aloud commentary from direct moderator responses with special tags — both come from P, the surrounding context shows which is which.

**Unmoderated test**:
- Often just `P1:` throughout, no MOD turns.
- Render task prompts as blockquotes so they're visually separate from speech: `> Task 1: Sign up for an account.`
- Expect more silent stretches. Don't try to fill gaps — mark with `[silence]` or `[...]` if the original notes them.
- Don't fabricate task boundaries the source didn't include.

### 8. QA pass

Before writing the output, do a focused sweep on the things that most often break analysis. This is "catch what could break your findings", not full proofreading.

- **Dates**: Confirm month/day order; flag ambiguous like "04/05" with `[?]`.
- **Numbers and quantities**: Verify units (£/$, percentages, durations); watch "thirteen" vs "thirty" confusion in auto-transcripts.
- **Proper nouns**: Names, places, brand names, programme names — check against glossary.
- **Negations**: Scan for missing "not". Auto-transcripts drop them surprisingly often, and a missing "not" flips meaning.
- **Speaker attribution**: Spot-check that strong claims, opinions, or sensitive content are attributed to the right speaker — auto-transcripts sometimes mis-segment at turn boundaries.
- **Stop rule**: If a chunk is too garbled to clean confidently, leave it as `[unclear: original text]` and surface it in cleaning notes. Don't guess.

### 9. Write the markdown output

Save the cleaned transcript to the project's research transcripts folder. Look for a `Transcripts/` subfolder within `03-Research/` inside the active project folder — this is the standard location for cleaned transcripts. If it doesn't exist, ask the user where to save before creating it.

Name the file `YYYY-MM-DD [Participant Name] — Cleaned Transcript.md`, using the date confirmed in Step 1. Match the casing and punctuation of existing files in the folder exactly.

Use this structure for the file contents (use actual values, not placeholders):

```markdown
---
title: [Session title — e.g. "P3 Usability Test — Tiering Research"]
session_type: interview | usability_test | unmoderated_test
project: [Project name — e.g. "Cashback Card / Tiering Research"]
participants: P1 (Real Name, role/age/segment if known) — expand each coded label, body still uses P1 only
moderator: MOD (Real Name) — expand the coded label with the moderator's real name
cohort: [Cohort label — e.g. "Light users" | "N/A (single-cohort study)"]
session_date: [YYYY-MM-DD if knowable, else omit]
duration: [if known, else omit]
source: Userlytics | Dovetail | Google Meet | Zoom | Teams | other
glossary: "[Project Name — Research Glossary](Project%20Name%20—%20Research%20Glossary.md)"
tags: [transcript, ux-research, project-tag, session-type-tag]
---

# [Session title]

## Transcript

MOD: [first turn]

P1: [response]

[... etc, with task headings or blockquoted prompts as appropriate to session type]

## Cleaning notes

- **Cleanup level**: intelligent verbatim
- **Glossary applied**: yes / no [if yes, reference filename]
- **Unclear segments**: [count, with timestamps if available]
- **Things to review**: [e.g. "auto-transcript was poor around 00:24:00 — recommend audio re-check"; "P1 used 'card' interchangeably with 'Cashback Card' — preserved as said"]
```

If a glossary was generated or extended, save it as `[project-name]-glossary.md` alongside, with a simple table:

```markdown
# [Project] Glossary

| Term | Approved spelling | Notes |
|------|-------------------|-------|
| ... | ... | ... |
```

If a glossary was generated or extended during this session, save or update it in `03-Research/` (not in the `Transcripts/` subfolder).

### 10. Present the file(s)

Use `present_files` to make the cleaned `.md` (and glossary, if generated) downloadable. Then in chat, give the user a short summary:
- What was cleaned
- What was flagged as `[unclear]` and where (with timestamps if possible)
- Anything to review before coding (e.g. attribution to verify against the recording, glossary additions to confirm)

Keep this short — the file itself is the detail. The summary just needs to surface anything worth acting on.

## What NOT to over-edit (guardrails)

These mistakes are easy to make and quietly damage the data:

- **Don't replace participant words with "better" ones.** "Frustrated" and "angry" mean different things. So do "confused" and "lost".
- **Don't smooth contradictions or self-corrections.** "I'd never use this — well, maybe for tipping" is more analytically valuable than either half alone.
- **Don't add tone interpretations the source doesn't support.** No inserting `[sarcastic]` or trailing "!" that you can't justify from the source.
- **Don't clean one speaker more than another.** If P1 has more fillers than P2, that's data — don't even it out.
- **Don't fabricate observed actions.** If the source doesn't say `[clicks button]`, don't add it because it sounds like that's what happened.
- **Don't anonymise unless asked.** Names of internal team members or participants stay as-is unless the user requests anonymisation. They use pseudonyms (P1, P2) at the speaker-label level, but content references stay.

## When to ask before proceeding

Pause and ask the user if:
- Source format or session type is unclear from the input.
- They haven't said whether this is one of several sessions in a study — ask before proceeding so the glossary approach is right (see Step 2).
- The transcript has many `[inaudible]` or `[unclear]` segments in high-impact places — flag rather than guess.
- A glossary conflict appears that could be intentional (e.g. transcript consistently says "the card" when glossary has "Cashback Card" — might be the participant's natural shorthand).
- The transcript appears auto-generated and quality is poor enough that cleaning may introduce more errors than it fixes — sometimes the right answer is "this needs re-transcription, not cleaning".
- They didn't specify a project name and there's no obvious one in the source — needed for the frontmatter and glossary filename.
