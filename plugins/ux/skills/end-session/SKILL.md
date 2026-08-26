---
name: end-session
version: 4
description: "End-of-session capture pass over a Claude-Code-driven knowledge base. Reviews the session you have just had for anything that should outlive it, then routes each finding to the right home: durable product knowledge to the area Wiki, changed project facts to MEMORY.md, new behaviour rules to CLAUDE.md, and cross-session facts to auto-memory. Proposes every change for approval before writing anything. Use this skill whenever the user signals the session is wrapping up: 'end session', 'end of session', 'we're done', 'wrap up', 'that's it for today', 'let's close out', 'anything worth capturing?', 'update the wiki before we finish', or when they ask what should be saved from the work you just did together. Also use it when a substantial piece of work lands mid-session (a deliverable shipped, a source ingested, a research question answered, a product rule corrected) and none of it has been written down yet."
---

# End session

A knowledge base only remembers what gets written down. During a session the user corrects your understanding of a product rule, decides something, tells you how they want things done, and answers questions whose answers are genuinely new. If none of that lands in a file, the next session starts from scratch and they have to say it all again.

The reason this is a skill rather than a standing instruction is that you cannot tell when a session is ending. The user has to say so. When they do, this is what you run.

Your job is a review pass, not a writing spree. Most sessions produce one or two things worth keeping, some produce none, and a few produce a lot. Report what you actually find.

It does two things and only two things: find what the session taught that is not yet on disk, and put it in the right file. It is not a tidy-up. No reorganising folders, no linting the wiki, no rewriting pages that are merely imperfect, no progress report on the project. Those are all real jobs the user can ask for separately, and doing them uninvited here buries the one or two findings that actually mattered.

## Step 1: Work out what is in scope

Identify the folder the session was working in, then read every `CLAUDE.md` and `MEMORY.md` on the path from that folder up to the knowledge base's root, plus any `Wiki/` folder you find on that path. A typical shape:

```
1-Projects/Cashback Card/          ← area CLAUDE.md, and the Wiki lives here
  Wiki/                            ← index.md, log.md, one page per concept
  1% Cap Visibility/               ← project CLAUDE.md + MEMORY.md
```

Some projects sit directly under `1-Projects/` with no area layer and no wiki. Skip what is not there rather than inventing it.

If you have an auto-memory directory, read its `MEMORY.md` index too. It is one of the destinations in Step 3.

If the session produced or touched research, also read `2-Areas/Research Repository/CLAUDE.md` and its `index.md`. That repository has its own conventions and its own sealing rule, and they win over this skill.

If the session touched no project at all (a general question, a bit of knowledge-base admin, a skills change), your scope is the root `CLAUDE.md` and auto-memory. Say so, and do not go hunting for a project to attach findings to.

The area `CLAUDE.md` usually defines the wiki's own conventions: page format, citation rules, whether `index.md` and `log.md` must be updated. Follow those rather than anything you assume. They differ between areas and they win over this skill.

## Step 2: Sweep the session

Read the conversation from the top. You are looking for four things, ordered by how easy they are to miss.

**A. Corrections to something already written down.** The user told you a wiki page, a MEMORY.md line, or an auto-memory entry was wrong, incomplete, or out of date. This is the highest-value catch and the easiest to lose, because in the moment it just felt like a conversation. If they said "no, the cap is already tiered by service count" or "that's not what the T&Cs say", something on disk is now wrong and will mislead the next session.

**B. Anything that would belong in a product's living documentation.** Treat the Wiki as the place that should eventually hold everything worth knowing about the product — the way a BA, a PM, a UX designer, and a commercial manager would each maintain their own layer of documentation for it. Concretely, watch for:

- **Business rules & constraints** — the actual mechanic behind a number or limit, what the system will and won't allow, edge cases, exceptions, technical constraints.
- **User flows & behaviour** — how a journey branches, what happens at a dead-end or error state, screens and states, known usability issues.
- **Stakeholders & decisions** — who owns what, positions taken, why a decision landed this way and not another.
- **Commercial & strategic context** — pricing, competitors, market position, why the thing exists commercially.
- **Research findings** — anything learned about users, behaviour, or the product from investigation. Includes good answers produced from reasoning across sources, not just facts the user handed you directly, since the expensive part was the synthesis.

The test is still whether it stays true independent of this project's timeline. This list is a prompt, not a fence — capture anything that fits the spirit even if it doesn't fit a bullet.

**C. Project state that changed.** Status moved, a decision got made, scope narrowed, a date was set, a deliverable landed, a contact appeared, someone's role changed. Anything a future session would need in order to pick up where you left off.

**D. Behaviour rules.** The user told you how to work. Look for "always", "never", "don't", "from now on", "before you do X", "check Y first". Also count the implicit ones: if they rejected your output and you changed approach, the rule behind the change is worth stating explicitly.

The implicit ones in D are where most of the value hides, because nothing in the transcript looks like an instruction. Work backwards from what they changed to the rule that explains it:

- They deleted every em-dash from a draft push notification. The rule: no em-dashes in customer-facing copy, use a comma or full stop.
- They said "check the T&Cs page first" after you asserted a cap figure from memory. The rule: verify product mechanics against the T&Cs wiki pages before stating them.
- They cut your three recommended copy changes down to one line flagging the issue. The rule: flag UI problems in findings, recommend testing rather than prescribing the fix.

Each of those started as a single edit and generalises into something that saves a round trip every future session. State the rule, not the incident.

Then filter hard. Drop anything you already wrote to a file during the session, anything already in the files you read in Step 1, and anything that only mattered to this conversation. A session with nothing to capture is a normal outcome, and saying "clean session, nothing to add" is more useful than padding the list. Do not manufacture findings to look thorough.

## Step 3: Route each finding

Five destinations, distinguished by what kind of thing the finding is:

| Destination | It goes here when | Examples |
| :--- | :--- | :--- |
| **Wiki page** | It is a durable fact about the product or domain that compounds over time | A mechanic's actual rules, a stakeholder's position, a competitor's approach, a user flow's actual branching, a business rule or technical constraint |
| **Research Repository** | It is what a study found | A figure, a theme across verbatims, a study that has just run. Goes to `2-Areas/Research Repository/` as a *new* study page, never as an edit to an existing one |
| **Project MEMORY.md** | It is a fact about *this project* that could change | Status, decisions, scope, dates, next step, who is involved |
| **CLAUDE.md** | It prescribes behaviour | "Always check the T&Cs pages before assuming a product rule" |
| **Auto-memory** | It is a fact or preference that matters across sessions and surfaces | Project status worth carrying between chats, feedback on how you work |

The line that catches people out is Wiki versus MEMORY.md. Ask whether the fact would still be true if the project were cancelled tomorrow. The 1% cap tiering by service count is true regardless, so it is wiki. "Step 6 done, step 7 next" is only true this week, so it is MEMORY.md.

The line that does real damage if you get it wrong is anything from research. A study records what people said on a given date, under the customer mix, the marketing, and the version of the product in place then. Those conditions are part of the finding and can't be recovered later, so research is never brought up to date — new data becomes a new record instead. Two consequences for this pass:

- **Never edit a sealed page.** Research reports, study pages in `Studies/`, and any dated document reporting what research found are closed. If the session produced new evidence, propose a new study page, not an amendment to an old one. Topic pages in `Topics/` are the exception and can grow, because they restate no figures of their own — record the shift in a "What changed" section rather than quietly swapping the old reading out.
- **Surface disagreements, don't settle them.** If something this session contradicts an existing finding, both are accurate records of their own moment. Say so in Step 4 and let the user decide. Reconciling them yourself erases evidence.

A product wiki page describing how the product *works* stays living and can be updated with the new citation — the old evidence survives on its own sealed page, so nothing is lost.

For CLAUDE.md findings, prefer the most specific file that covers the behaviour. A rule about how to handle CBC transcripts belongs in the project or area file, not the knowledge base's root.

For auto-memory, follow the format described in your memory instructions, and mirror rather than duplicate: the knowledge base is the source of truth, auto-memory is the pointer that survives into the next chat.

When a finding genuinely could go two places, say which you think it is and why, and let the user decide. Do not silently pick.

## Step 4: Show the user before writing anything

Present findings grouped by destination, with the exact text you propose to write. They need to see the wording, not a description of it, because half the value of this pass is them catching where you have paraphrased something into being subtly wrong.

**Changing a line that already exists** — show it as a diff. A terminal colours the two lines red and green, so the user sees there is a change before they read a word, and the alignment lets them spot what actually moved:

````
**[n]. [The problem, stated as a problem]**
`path/to/file.md` · line N

```diff
- [the text that is there now]
+ [the text you propose]
```

Why: [one plain sentence]
````

Three things about that shape are deliberate. The **heading names the problem**, not the event — "Wiki index oversells a page that got trimmed" tells them what to judge before they read anything, where "Updated the wiki index" makes them hunt for it. The **path sits on its own line**, because it is scanning information rather than prose. And the **why comes last and stays to one sentence**, because by then they have already decided.

**Creating a new file, or rewriting a whole passage** — drop the diff and show one block of the final text. Two walls of red and green with no shared structure are harder to read than the thing itself, and for a new file there is nothing to compare against.

**Write the "Why" the way you would say it out loud.** It is the one line in the report addressed to the user rather than describing a file, and it is where technical register creeps back in. "The rename repointed the link but left the old description" is what to avoid: it names an operation they did not watch you run. "I changed the link but not the description beside it" says the same thing, and they can act on it. No tool names, no command names, no jargon — plain language a non-technical reader can act on, matching whatever tone the knowledge base's own CLAUDE.md asks for.

Split them into two groups. **Recommend** for the clear-cut ones. **Your call** for anything where the routing is arguable, the wording is a judgment call, or you are editing something the user wrote themselves.

For wiki work, be specific about the shape of the change: new page, or an edit to an existing page, and which. If it is a new page, show the full draft, not a sketch — the point of this step is to let the user see exactly what will be written before it exists.

Then stop and wait. Do not write on the assumption they will approve.

## Step 5: Apply what the user approves

Work through the approved findings. Two things are easy to forget and both are load-bearing:

- **Wiki housekeeping.** If you added or changed a page, update `index.md` (with its one-line description) and append to `log.md`, following whatever the area's `CLAUDE.md` specifies. Add links both ways so the new page is reachable, otherwise it is an orphan and the next session will not find it. Match the log's existing date-heading order rather than imposing a new one.
- **Both halves of a correction.** Fixing a wiki page that was wrong often means fixing the MEMORY.md or auto-memory line that repeated the error. Check for the same wrong fact in the other files you read in Step 1.

Follow the knowledge base's own standing rules while you write — check its root `CLAUDE.md` for specifics, but the common ones are: nothing in the root, point-in-time files date-prefixed as `YYYY-MM-DD Description.md`, living documents not date-prefixed.

## Step 6: Confirm and land it

List what you wrote and where, in a few lines. If the user skipped anything, note it once so they know it was dropped rather than quietly lost, and leave it there. No summary of the whole session, no suggestions for next time unless they ask.
