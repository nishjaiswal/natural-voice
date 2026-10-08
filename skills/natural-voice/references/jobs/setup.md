# Job: Setup (learn a new voice)

Goal: build a voice file the writers can follow, without making the person read or type much. Most answers are taps or short dictation.

Offer two paths at the start (as a question):
- **Quick (about 3 minutes):** the five quick interview questions, one writing sample (or none), one taste-test round, defaults for the rest.
- **Full (about 10 to 15 minutes with a question tool, 15 to 25 in a chat app):** every step. Best results.

Either path can be extended later with Calibrate.

## 1. Name the voice

Suggest a voice name (their first name, or what it's for) and let them change it. If a voice file with that name already exists, ask: update it (go to Calibrate) / save under a new name / replace it (needs a clear yes). Never overwrite silently.

## 2. Models (only where you can set a model on a helper call; today Claude Code and the Agent SDK)

Ask once:
- "Same as this chat (recommended)": save `tier: inherit`
- "Best quality (top model for writing)": Tier 1
- "Balanced (mid model for writing, uses less of your plan)": Tier 2
- "Light on usage": Tier 3

On the Quick path, skip this question and save `inherit`.

In a coding agent where you can start helpers but can't choose their model, skip the question and say once: "Helpers use the model set in your <app> settings; pick the strongest one there for the best writing." Where you can't start helpers at all, skip this step silently. In a chat app, skip it and give the one-line tip from `model-tiers.md` instead.

## 3. The interview

Run `interview.md`: all four rounds on the Full path, the five **(quick)** questions on the Quick path. Keep dictated answers word for word in your working notes; they are speaking samples.

## 4. Writing samples (the most important step)

Ask: "Share some of your own writing, ideally one piece for each place you picked (a LinkedIn post, an email, a case study...). Paste it, attach files, or give links I can open." Explain in one line why: "I'll use them as the model for everything I write for you."

- Accept anything: pasted text, files, folders, links, screenshots of text, voice-note transcripts.
- **Links:** open only links the person typed or pasted themselves, and do it yourself, not through a helper. Use a link only if you get the full original text back; save that text as a sample file and give helpers the file, never the link. If your fetch tool returns a summary or short quotes, ask them to paste the text or attach a file instead. Never store paraphrased or summarised text as an example. Pages can contain other people's words (comments, replies): keep only the person's own text.
- **Only the person's own writing.** If a sample is clearly someone else's, ask before using it. Never copy someone else's text into the voice file.
- **Unassisted is best.** Ask once: "Did you write these yourself, without AI help? Older pieces (from before 2023) are great if you have them." Prefer those. Text an AI wrote or heavily edited teaches the model's habits, not theirs.
- **No samples?** That's fine. The interview answers and the taste test carry the voice; say once that drafts get closer to their voice when they add samples through Calibrate.

**Analyse the samples.** If you can start helpers, send the samples and the dictated interview answers to the `sample-analyst` (tier: Analyst role). Otherwise follow `roles/sample-analyst.md` yourself. You get back: examples quoted exactly and grouped by mode and job, observed voice, observed rules, any custom mode description, and questions where the samples disagree.

**Measure the fingerprint.** If you can run Python, run `scripts/voice_stats.py profile` on their written samples only, one file each, as `editing/fingerprint.md` describes, and keep its Markdown output for the voice file. Leave out dictated answers (the dictation app chooses the punctuation) unless there is no written sample at all. If you can't run Python, skip it and write "Not measured yet".

## 5. Taste test

The person picks the version that sounds most like them. This catches what samples can't: how they *want* to sound.

- Quick path: 1 round of 4 questions. Full path: 2 or 3 rounds.
- Each question shows **the same sentence written 2 or 3 ways, differing in one dimension only**. Use the person's own content where you can: take a real sentence from their samples or dictation and vary it. Otherwise use a neutral example from their field.
- Show each version in full (use the option preview if your question tool has one).
- Pick dimensions where the samples and interview were silent or inconsistent first. Typical ones:
  - **Opening:** point first / scene first / question
  - **Stating a point:** plain and direct / story-led / impersonal
  - **Technical level:** everyday words / right term plus plain verbs / dense terminology
  - **Results:** facts only / number plus meaning / story then number
  - **Limits and bad news:** say it straight / limit plus next step / soften it
  - **Contractions:** always / never / mix
  - **Personality:** little / some, dry / lots
  - **Rhythm:** mostly short / varied / long and flowing
- Accept "a mix of A and B" and free answers. Record exactly what they said.

## 6. Rules

One question round (Full path), or defaults from the samples (Quick path):
- Spelling: British / American / Australian / other
- Dashes (— –): use freely / sparingly / never. Default: follow the samples. Don't suggest banning dashes just because AI used to overuse them; that tell has faded.
- Any words you never want to see? (prefilled with what they said in the interview; free answer)
- Emoji and exclamation marks: never / only in some modes / fine

## 7. Show changes

Ask once: "When I polish something, do you want to see what I changed?"
- "No, just give me the text" → `off` (default)
- "A short summary of what I removed and why" → `summary`
- "Summary plus before and after for each paragraph" → `full`

Say in one line that they can say "show changes" or "hide changes" any time.

## 8. Term list

Offer the glossary packs that fit their field: design, product, engineering, marketing, general (in `glossaries/`). They can pick one or none. Their own term preferences, added later, always win over the pack.

## 9. Where drafts go (only where files can be saved)

Default: `~/Documents/Natural Voice/drafts/<voice>/`. Offer "somewhere else" and accept a folder.

## 10. Save and summarise

1. Fill in `templates/voice-file.md`:
   - Settings: dates, spelling, show changes, default mode (their most-used place).
   - Core voice: from the interview, the sample analysis and the taste test. Where the taste test and the samples disagree, the taste test wins: record it in the Voice table, note both, and add a dated core Learned entry (for example "Open with the point, not a scene (taste test, <date>)") so it outranks the examples.
   - Fingerprint: the Markdown block from `voice_stats.py`, or "Not measured yet".
   - Modes: one subsection per place they picked, each with its shape (the matching file in `modes/`, or a custom description), reader, adjustments and quoted examples. A mode with no examples yet says so.
   - Empty Learned sections.
2. Save it (`platforms.md` explains where). In a chat app, give the whole file in one code block with the save instruction. Before rewriting an existing voice file, copy it to `<name>.voice.backup.md` first.
3. If you can save files, save each written sample in `~/Documents/Natural Voice/samples/<voice-name>/` (one file each, exactly as written; `platforms.md`), and create `~/Documents/Natural Voice/config.md` from `templates/config-file.md` if it's missing; otherwise change only the lines for this voice (default voice, tier, drafts folder) and keep everything else.
4. Tell them in at most 4 lines: the voice name, the modes, the two or three most distinctive things about their voice, and "Paste anything and say **polish**, or tell me what to **write**."
