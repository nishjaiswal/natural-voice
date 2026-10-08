# Change report

Shown under polished or cleaned text when the voice file's **Show changes** is `summary` or `full`. Keep it short and plain: the person wants to learn what changed, not read an essay. Group similar changes, give counts, and quote one or two real examples per group. Never include a "human score" or a guess about whether the text was AI-written.

## Summary (`summary` and `full`)

```markdown
**What I changed**
- Removed <n> <kind of pattern, in plain words>: "<example>", "<example>"
- Changed <old> → <new> (<n> times), because <one short reason, e.g. "your term list says so">
- Rebuilt <n> sentences that <plain description, e.g. "announced importance instead of saying what happened">
- Split / joined <n> sentences to match your usual rhythm

**Kept on purpose**
- "<phrase>": <why, e.g. "it's the right term in statistics", "you use dashes like this in your own writing">

**Hidden characters** (in the text you pasted)
- Removed <n> <kind> (<n> zero-width spaces, <n> ChatGPT citation markers...), replaced <n> <kind> with normal spaces
- or: none found

**Check these**
- <anything uncertain: an [ADD: ...] gap, a claim you couldn't trace, a term you guessed>
- From the draft you pasted, not from you: <numbers, results, quotes or evidence that only the AI draft gave, when polishing an AI draft>
```

Leave out any heading with nothing under it. If nothing changed in a section, don't mention it.

## Full (`full` only)

After the summary, show each changed paragraph as a before and after, in order. Skip paragraphs that didn't change.

```markdown
**Paragraph 2**
> Before: <original paragraph>

> After: <new paragraph>
```

For long texts (more than about 8 changed paragraphs), show the first 5 and offer the rest: "Show the other <n>?"

## Wording rules

- Describe patterns in plain words, not catalogue IDs ("phrases that announce importance", not "NV-M01"). You may add the ID in brackets if the person has asked for them.
- Use "I" for what you did ("I removed..."), and "you" for their rules ("your term list...").
- Don't apologise for the original text, and don't praise the new version.
