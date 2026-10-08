# Job: Calibrate (make it sound more like them)

1. Load the voice file and the most recent drafts or notes, if you can reach them. Read both Learned sections: they show what has gone wrong before.
2. If the person has already said what they want (pasted an edited draft, pasted a transcript, attached new samples), go straight to that branch. Otherwise ask one question: what feels off? Options:
   - "Tone is off (too formal, too casual, or I can't say why)"
   - "Here's how I edited your draft"
   - "Wrong words or structure"
   - "More..." → "I have new samples or a transcript" / "Retake part of the interview" / "Add or change a mode"
3. Follow the branch.

## Tone

2 or 3 taste-test rounds, as in `setup.md` step 5. Use sentences from their recent drafts, so they react to real output. Update the Voice table.

## Here's how I edited your draft

This is the strongest signal there is: what they changed is what you got wrong.

1. Ask for both versions if you don't have them: the draft you gave them and their edited version.
2. Compare them and list the **patterns** in their changes, not every single edit. For example: "You cut every 'really' and 'just'", "You split sentences longer than about 20 words", "You changed 'users' to 'people'", "You removed the closing line each time", "You added a contraction in 6 places".
3. Show the list (at most 6 items) as a multiple-choice question where they can pick several: "Which of these should I always do?" Add "None, these were one-offs".
4. Save the picked ones as dated Learned entries: in the core, or in a mode's Learned section if the edits were all in one mode and only make sense there. Use their own wording where possible.
5. **Never learn a claim change.** If they added a fact, a number or a result, that's content for that piece, not a style rule. Say so in one line if you leave something out for that reason.
6. Don't add their edited version to the fingerprint: an edited draft still carries the model's habits. The fingerprint only changes when they give new writing they did without AI help (see below).

## Wrong words or structure

- **Words:** show 3 to 6 terms or phrases from recent drafts next to alternatives; they pick. Update *My terms* and the word lists in *My rules*. Refuse a term that would change status, scale or evidence ("tried it with a few people" → "validated with users"), and say why in one line.
- **Structure:** show the current mode's shape (its file in `modes/`, or the custom description in the voice file) and ask what to move, add or drop. Update that mode's section.

## New samples or a transcript

- **New samples** they wrote themselves without AI help: run the sample analysis again (`roles/sample-analyst.md`) and add the passages to the matching modes' Examples. If a job already holds 8, replace the weakest older ones. Re-measure the fingerprint if you can. Never add text that Natural Voice or another AI produced: it would teach the model's style, not theirs.
- **A transcript** of them talking (a voice note, a meeting, dictation): use `speech-to-writing.md` to find their speech patterns and update *How I talk* and *Stories and phrases I reuse*. Quote briefly; leave out other people's words and anything private.

## Retake part of the interview

Run the round they choose from `interview.md` and update the matching sections.

## Add or change a mode

Hand over to the Voices job (`voices.md`, "Modes").

## Save

1. Copy the current file to `<name>.voice.backup.md`, then update the voice file. Don't delete earlier Voice, rules or Learned entries; mark replaced ones "(replaced <date>)". Writers skip rows marked replaced. Update "Last updated".
2. Tell them in 2 or 3 lines what changed. In a chat app, hand over the updated voice file.
