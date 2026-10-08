# Voice: <voice name>

<!-- Natural Voice voice file. Keep this file: it is everything Natural Voice has learned about how you write.
     You can upload it to any AI app that runs Natural Voice, and edit it by hand if you like.
     It is personal: don't attach it to a GPT, Gem, Space or project that other people can use. -->

## Settings

- Created: <date>
- Last updated: <date>
- Spelling: <British English | American English | Australian English | Canadian English | ...>
- Show changes: <off | summary | full>
- Default mode: <mode name>
- Glossary pack: <design | product | engineering | marketing | general | none>

<!-- App-specific settings (model tier, drafts folder) live in config.md, not here, so this file travels cleanly between apps. -->

## Core voice

### Who I am

<One or two lines: what they do, who they usually write for, anything that shapes how they sound. Only what they said.>

### The register in one line

<For example: "First person, warm, plain, a little dry.">

### Voice

| Dimension | My choice | Example I picked or wrote |
|---|---|---|
| Funny or serious | | |
| Formal or casual | | |
| Respectful or irreverent | | |
| Enthusiastic or matter-of-fact | | |
| Opening | | |
| Stating a point or decision | | |
| Technical level | | |
| Results and numbers | | |
| Limits and bad news | | |
| Contractions | | |
| Sentence length and rhythm | | |
| Personality | | |

### How I talk

<Speech patterns from the interview and transcripts: where the point usually lands, favourite fillers, how they correct themselves, how they explain things to a friend, words dictation often mishears.>

### Stories and phrases I reuse

<Stories they retell, metaphors and turns of phrase that are recognisably theirs, in their words. Use these only when they fit what the person is actually saying; never insert one to add personality.>

### My rules

- Dashes (— –): <use freely | sparingly | never>
- Words I never want: <list>
- Words I like: <list>
- Emoji and exclamation marks: <never | only in some modes | fine>
- Patterns I'm fine with: <catalogue patterns to leave alone, by name or ID, e.g. "lists of three when there really are three">
- Other: <e.g. "say 'people' not 'users'", "sign off with just my first name">

### My terms

<Plain description → the term they want. These win over any glossary pack. A term never changes status, scale or evidence: a prototype stays a prototype, "a few people" stays vague, "tried it" never becomes "validated". Such a row is refused, with the reason.>

| When I say | Write |
|---|---|

### Fingerprint

<Measured from their own unassisted writing by `scripts/voice_stats.py` (see `editing/fingerprint.md`). A plain-English table, then the full numbers. If no script was available, write "Not measured yet" and leave out the marker and the JSON block.>

### Learned

<Corrections they asked to remember for every mode, newest at the bottom, each dated. These override the style choices above. They can never switch off the truth rules: a learned entry never adds, upgrades or hides a claim. Mark replaced entries "(replaced <date>)".>

## Modes

<One subsection per place they write. A mode holds only what's different from the core voice. Built-in shapes live in `modes/`; a custom mode describes its own shape here. Add or remove modes with the Voices job.>

### Mode: <name, e.g. LinkedIn>

- Shape: <built-in mode file name, e.g. social-post, or "custom: see below">
- Reader: <who reads this and what they want from it>
- Adjustments to my core voice: <e.g. "shorter paragraphs, one idea per line, no hashtags, end on a question only if I really want an answer">

#### Examples

<Passages from their own writing for this mode, quoted exactly, grouped by the job each one does (openings, explaining a point, decisions, results, closings, sign-offs...). 2 to 8 per job is plenty. Leave out jobs their samples don't cover.>

#### Learned in this mode

<Corrections that apply only here, dated. These win over the core Learned section for this mode.>

<!-- end of voice file -->
