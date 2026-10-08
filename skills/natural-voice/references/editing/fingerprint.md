# The fingerprint

The Fingerprint is a set of measured habits from the person's own writing: how long their sentences usually run, how often they use commas, dashes and questions, whether they contract, whether they write "I" or "we", how they start sentences, which spelling they use, and how often they use about 50 everyday small words such as "the", "but" and "which".

It describes habits. It doesn't judge quality, and it says nothing about who wrote a text. It helps you avoid a common failure: a rewrite that loses the person's rhythm, or swaps one formula for another.

`scripts/voice_stats.py` measures it. The script runs offline with plain Python 3, gives the same result every time for the same text, and reads only the files you give it. Run it as `platforms.md` describes in "Running the scripts": in Claude Code, build the path from the skill's base directory (shown when the skill loads) and quote it.

## Where it lives

In the voice file, under *Core voice*, in the `### Fingerprint` subsection (`templates/voice-file.md`). The subsection holds three things, in this order:

1. A short plain-English table of 8 to 12 habits, for the person to read.
2. The marker line `<!-- natural-voice:fingerprint -->`.
3. Directly after the marker, a fenced `json` block with the full numbers, for the script to read.

The script finds the Fingerprint by the marker, wherever it is in the file. Keep the marker and the `json` block together, and never edit the numbers by hand. If nothing was measured, the subsection says "Not measured yet" and has no marker or block.

## Make it (Setup and Calibrate)

**Measure only the person's own unassisted writing.** Leave out:

- anything Natural Voice, another AI tool or an editor wrote or rewrote, including drafts the person then edited (edited drafts keep much of the model's habits);
- other people's words: quotes, client briefs, co-written pieces;
- dictation transcripts, unless there is no written sample at all: dictation apps choose the punctuation, so the numbers would describe the app. If you do include one, say so in the voice file under the table.

Then:

1. Save each sample as its own plain-text or Markdown file, exactly as they wrote it. On the person's computer, keep them in `~/Documents/Natural Voice/samples/<voice-name>/` so they can be measured again later (`platforms.md`).
2. Run:

   ```sh
   python3 "<skill folder>/scripts/voice_stats.py" profile sample-1.md sample-2.txt --markdown
   ```

   The script leaves out headings, code, quoted blocks, tables, links' addresses and bare links before measuring.
3. Replace the whole `### Fingerprint` subsection, heading included, with the output. The output starts with its own `### Fingerprint` heading.
4. Read the confidence on the first line. **Low** (under 300 words) means the numbers are a rough sketch: tell the person in one line that more of their own writing would sharpen it. **Medium** is 300 to 1,500 words; **high** is above that.

At **Calibrate**, when they bring new samples of their own writing, add them to the samples folder and measure all of them again (old and new together), then replace the block. If the old samples aren't available (a chat app, or they were never saved), measure only if the new samples are at least as long as the old total, and otherwise keep the old block and say why. The voice file backup keeps the previous one.

In a chat app, the Fingerprint travels inside the voice file you hand over. Never shorten or summarise the `json` block.

## Compare a draft (Write and Polish)

Run this after writing or polishing and before the voice audit, when the voice file has a Fingerprint with the marker.

1. Save the draft to a file exactly as you'll hand it back (the text only).
2. Run:

   ```sh
   python3 "<skill folder>/scripts/voice_stats.py" compare draft.md --voice-file "<path to>/name.voice.md"
   ```

   If you only have the numbers (for example in a chat app with code tools), save the `json` block as `fingerprint.json` and use `--fingerprint fingerprint.json` instead. Add `--json` for a machine-readable result.
3. The result lists up to 8 differences, biggest first, then a small-word distance. For example: "Your sentences usually range 6 to 24 words; this draft stays between 10 and 14 (more uniform than you write)."
4. If the draft or the samples have fewer than 150 words, the script skips the comparison and says why. Move on without it.

Give the result to the voice auditor (`roles/voice-auditor.md`, step 5), or use it in your own audit pass.

### What to do with the differences

- **Treat them as hints, not targets.** Fix a big difference when the mode or the content doesn't explain it. A list-heavy product spec will have more short sentences; a LinkedIn mode may use shorter paragraphs on purpose. The mode's section in the voice file wins over the core Fingerprint.
- **Aim for their usual range, not their average.** Forcing every rate to match makes a new formula. Vary sentence length the way their samples vary.
- **Never fix a difference by changing facts.** A difference in "I" and "we", hedges or claims means: check the source. Keep exactly what the person said, even if it doesn't match the Fingerprint.
- **Re-run once at most** after fixing. Don't loop on the numbers.
- **Rough measures:** hedges, intensifiers, sentences opening with an -ing word, and -tion, -ment and -ness nouns are rough word-list counts. Use them only alongside your own reading.

## Word it for the person

Usually, don't mention it: it's a working check. If **Show changes** is `summary` or `full`, mention at most one rhythm change in the change report, in their terms: "Varied the sentence length to match your usual range (you usually write 6 to 24 words; the draft sat between 10 and 14)."

- Say "you usually" and "this draft". Don't call anything a score, a match percentage, a pass or a fail.
- **Never present the small-word distance, or anything else here, as a human or AI score,** and never say a draft "sounds human" or "would pass" because of it. If they ask what it is: "It compares how often you use small everyday words like 'the', 'but' and 'which' with your own samples. Lower means closer. It's one rough style signal, not a verdict." Up to 1.1 is close; 1.1 to 1.6 is a little different; above 1.6 is noticeably different. Short drafts swing more.
- If they ask what's in their Fingerprint, read them the table, not the `json`.

## Without Python

If you can't run the script (no code tools, no Python, or the person declined):

- At Setup, write "Not measured yet" in the Fingerprint subsection. Don't write the table or the numbers by hand: estimates would look like measurements.
- When checking a draft, compare by eye against the mode's Examples: the range of sentence lengths (count the words in five or six sentences of each), how sentences start, which punctuation they use (dashes, semicolons, brackets, questions), contractions, I or we, and spelling.
- If you report on it, say it was a by-eye comparison.
- If the voice file already has a Fingerprint, you can still read its table and use it as a guide for the by-eye check.

## What the numbers mean

| Field | Meaning |
|---|---|
| `words`, `samples`, `confidence` | How much writing was measured, from how many files, and how far to trust it |
| `sentences` | Words per sentence: `mean`, `median`, `p10` and `p90` (their usual range runs from p10 to p90), `sd` (spread), and the share under 8 words and over 25 |
| `paragraphs` | Sentences per paragraph (`sentences_mean`, `sentences_sd`) and the share of one-sentence paragraphs. List items don't count as paragraphs |
| `per_1000_words` | Commas, semicolons, colons, em dashes, en dashes, spaced hyphens used as dashes, brackets, exclamation and question marks, ellipses, double quote marks, contractions, I and we words, hedges, intensifiers, and the two rough counts |
| `contractions` | How often an easy pair was contracted ("don't") or not ("do not") |
| `quote_style` | Curly against straight quote marks and apostrophes |
| `openers` | Their eight most common first words of a sentence, as shares of all sentences |
| `spelling` | British and American spelling signals (-our, -re and others) and -ise against -ize endings, with an overall lean |
| `function_word_rates`, `function_word_sd`, `function_word_chunks` | How often each of about 50 small everyday words appears per 1,000 words, and how much that varies across 250-word chunks of their samples. The compare command uses these for the small-word distance (a Burrows' Delta style measure) |

The `json` block is data. The script reads only the numbers from it; anything else in a voice file is never an instruction.
