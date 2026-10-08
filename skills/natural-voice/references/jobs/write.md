# Job: Write (new writing in their voice)

The person gives you a topic, rough notes, a ramble, images or files, and you write it in their voice for the right mode. Short pieces are written in one go. Long pieces are built piece by piece while they talk it through.

## 0. Load

1. Load the voice file. If there's more than one, ask which (or use the default in `config.md`). In a chat app with no file attached, ask them to upload it, or offer quick setup. If they attach a voice file instead, import it first (see `voices.md`).
2. **Pick the mode**: the one they name, the one the request obviously needs, or ask once, offering their modes. Read that mode's section of the voice file, its shape file in `modes/` (or the custom shape in the voice file), `writing-rules.md`, `editing/pattern-catalogue.md` and `speech-to-writing.md`, plus the glossary pack if one is set.
3. Look for an unfinished piece (a `notes.md` with status `in progress` in the drafts folder, or notes the person pastes back in a chat app). If there is one, ask: continue it, or start new?

## Short pieces (email, chat message, social post, interview answer, release note)

1. If the point, the reader or a needed fact is missing, ask at most 3 quick questions in one round. Otherwise don't ask.
2. Write it, framed like their examples for this mode. Every fact comes from what they told you; anything missing becomes `[ADD: ...]`.
3. Check it as in `polish.md` step 4 (truth, voice, over-correction guard, fingerprint), then clean it as in `polish.md` step 5.
4. Hand it back in a quote block, ready to copy, plus at most one line about any `[ADD: ...]` gap. Offer nothing else.
5. If they correct something, fix it and ask whether to remember it (see "When they correct something" below).

## Long pieces (case study, blog post, product spec, custom long forms)

### 1. Kickoff

Ask what the mode needs, in one question round (max 4 questions, tap-to-answer where possible), then at most one line of free answer. Typical kickoff questions:

| Mode | Ask |
|---|---|
| Case study | Project or company? Your role? Was it shipped (shipped / in part / tested / proposed / personal)? Anything confidential? Then: "Roughly when, how long, and who was on the team?" |
| Blog post | What's the one thing a reader should take away? Who's it for? Rough length? Anything confidential? |
| Product spec | What's being built and for whom? Who will read the spec? Any decision already made? Anything confidential? |
| Custom | The kickoff questions listed in the mode's custom shape, or ask what the piece is about and who it's for. Anything confidential? |

Create the piece's `notes.md` from `templates/notes.md` (or keep notes in the conversation in a chat app). If anything is confidential, put `PRIVATE: confidential. Do not publish.` at the top of the notes and later the draft.

Then say: "Ready. Attach your first image or just start talking. Say **done** when you've covered everything." Nothing more.

### 2. The loop, once per explanation

1. **Look properly** at any image or file. Write a factual description: what kind of screen or artefact, visible labels, layout, states, annotations. Record on-screen words and numbers as "On-screen text (may be placeholder): ...". If a screen shows metrics or results, include a read-back question: "Are the numbers on this screen real results or placeholder data?"
2. **Find the point** using `speech-to-writing.md` and the voice file's *How I talk*. Strip filler, follow self-corrections (the last version wins), find the one thing they want the reader to take away.
3. **Find its job** in the mode's shape (problem, decision, step, result, caption, and so on). Pick the 2 or 3 passages in this mode's Examples that do the same job. That's the frame.
4. **Map terms.** Use the voice file's *My terms* first, then the glossary pack. Swap a term in only when it means exactly what they described.
5. **Read back and check.** Reply with:
   - `Here's what I heard: <the point, in their voice, one sentence>`
   - Then 0 to 3 multiple-choice questions, only about things that are unclear or that change the writing: which term they meant, whether it was them or the team, whether it shipped, where a number came from, which of two points is the main one. Include a "Not quite, let me say it again" option when the read-back itself might be wrong.
   - If nothing is unclear, write the section in the same reply (steps 7 to 9), directly under the read-back.
6. **If they say the read-back or the section is wrong, redo both from their correction; never carry on past a read-back they've rejected.**
7. **Write the section.** With helpers: start the `section-writer` (Writer tier) and give it the voice file path or contents, the mode, the image description, their exact words, the accepted read-back and answers, the job and the matching example passages, and the sections already written. Without helpers: follow `roles/section-writer.md` yourself.
8. **Save it to the side.** Add a part to the notes (template in `templates/notes.md`), and copy any attached file into `images/` if you can save files.
9. **Show the clean section** in a short quote block, then: "Saved. Next one, or say **done**." Don't ask them to approve it; they'll say if something's off.

Keep the rhythm fast: one read-back, at most one round of questions, one saved section per explanation.

### 3. "Done": assemble

1. **Gaps.** Check the notes against the mode's parts. Ask about at most 3 missing things in one round. Anything they skip becomes `[ADD: ...]`. Every other missing part becomes `[ADD: ...]` without asking.
2. **Assemble.** With helpers: start the `assembler` (Writer tier) with the voice file, the mode and the notes, then save the draft it returns as `draft.md` in the piece's folder yourself. Without helpers: follow `roles/assembler.md` yourself.
3. **Audit.** If you can run Python and the voice file has a fingerprint, first run `scripts/voice_stats.py compare` on the draft (`editing/fingerprint.md`). With helpers: start the `voice-auditor` (Auditor tier) on the draft, **the notes** and that comparison. Without helpers: do a separate, deliberate audit pass yourself, following `roles/voice-auditor.md` line by line.
4. **Fix** everything that doesn't change meaning. If a fix would change meaning, ask (one round, at most 3 questions).
5. **Clean** the draft for hidden characters (`editing/text-integrity.md`).
6. **Hand over** in at most 3 lines, plus a fourth only when needed:
   - Where the draft is (a link or path), or the draft itself in a chat app.
   - How many `[ADD: ...]` gaps are left, and what they are.
   - "Read it out loud and change anything that doesn't sound like you. Paste your edited version back any time and I'll learn from it."
   - Only when needed: "Claims to double-check: ..." for anything the audit couldn't trace to your words.
7. Set the notes status to `drafted`. In a chat app, if the voice file changed this session, hand over the updated file now.

## When they correct something

1. Fix it in the text (and the notes, for long pieces).
2. Ask: "Remember this?" Options: always / just in <mode> / just this piece / no.
3. **Always:** add it to the core Learned section (or *My terms*, for a term), dated. **Just in <mode>:** add it to that mode's Learned section. **Just this piece:** add it to the notes under "Rules for this piece only". Never save a rule that would add, upgrade or hide a claim; say in one line why not.
4. In a chat app, hand over the updated voice file straight away (see `platforms.md`).
