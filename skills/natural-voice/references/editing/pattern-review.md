# Review method

Use this to review any draft, yours or the person's, with [pattern-catalogue.md](pattern-catalogue.md). The catalogue is a set of editing prompts. People use every pattern in it, so a flag says nothing about who wrote the text. Removing every pattern can make prose worse.

## Steps

1. **Read for meaning first.** Read the whole piece once without editing. Note its point, its reader, and every claim: numbers, names, dates, quotes, links, status (done, tested, planned), I and we, and every hedge. These are locked.
2. **Load the person's rules.** Voice file first: both *Learned* sections (core and the current mode's), *My rules*, *My terms*, *Voice*, the mode's *Examples*, and *Fingerprint* if it is filled in. *My rules* and *Learned* can switch catalogue patterns on or off. Spelling follows the voice file ([voice-and-genre.md](voice-and-genre.md)).
3. **Scan with the catalogue.** Mark each sighting with its ID. Check the strong-alone patterns first, then the 2026 model phrasing, then the weak-alone patterns. Look at paragraph shape as well as sentences. Skip anything that matches the pattern's "Leave it alone when".
4. **Count clusters.** A weak-alone pattern counts only in a cluster: three or more sightings in one paragraph, or the same habit across the piece. This threshold is a rule of thumb. Nobody has tested it.
5. **Decide with the voice file.** For each flag, ask: do their Examples or Fingerprint do this, at about this rate? If yes, keep it. If the voice file is silent, edit only strong-alone flags and clusters.
6. **Fix the sentence, not the word.** Rewrite around the sentence's point. Don't swap a flagged word for a synonym. Keep every supported claim and everything the original covered. If a fix needs a fact you don't have, write `[ADD: ...]` or ask.
7. **Run the over-correction guard.** Check the rewrite against NV-G01 to NV-G08 in the catalogue and against the person's Fingerprint. Then scan the rewrite once more, because fixes create new tells.
8. **Truth check, claim by claim.** Compare the rewrite with your notes from step 1. Every number, name, date, quote and link matches. Status, I and we, hedges, negations and must, may or should are unchanged. Nothing new was added. Where scripts can run, use `scripts/text_integrity.py compare` with locks ([text-integrity.md](text-integrity.md)). A truth problem is always must-fix.
9. **Give the person the last edit.** Text that a person post-edits moves towards their own style but stays closer to the model's style than their unassisted writing does ([Baumler et al., ACL 2026](https://aclanthology.org/2026.acl-long.2030/)). Suggest they read it aloud and change anything that doesn't sound like them, then offer to remember those changes.

## Reporting

In a fix list, name the pattern ID in the problem field, for example:

`"This matters." | NV-M01 importance flag | state the consequence instead | should-fix`

Truth items (NV-T01 to NV-T06) are always must-fix or ask the person. End with one line saying how many flags you left alone because the voice file or samples use them.

## Formatting

- Keep navigational headings, required sections, lists and tables that help the reader, and accessible structure.
- Remove decoration only where it doesn't help this reader (NV-F01, NV-F02).
- Don't ban dashes, semicolons, colons, bullets or Oxford commas by default. Follow the voice file and the destination.
- Preserve exact quotations, code, ranges, names, notation, citations and link targets. Keep each citation attached to the claim it supports.
- Inspect invisible characters with [text-integrity.md](text-integrity.md) before deleting any. Some have a job, and a run of them may be a file credential.
- Remove chat scaffolding ("Certainly, here's...") from text meant for a reader (NV-C01).

## When to stop

Stop when each paragraph is useful, each benefit is supported and each commitment is unchanged. Don't chase zero flags, and never chase a detector score ([detectors-and-watermarks.md](detectors-and-watermarks.md)).
