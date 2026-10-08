# Mode: custom (learned from the person's samples)

Use this when none of the built-in modes fit. Examples include grant applications, award entries, academic abstracts, client proposals, newsletters, scripts, documentation pages and community posts.

## How the shape gets learned (at setup, calibration or when adding a mode)

The sample analysis (a `sample-analyst` helper, or you, following `roles/sample-analyst.md`) reads 2 or more samples of this kind of writing and returns a shape description, which you write into that mode's section of the voice file (`Shape: custom`), covering:

1. **Purpose and reader**: who reads it and what they need from it.
2. **Parts, in order**: each part's job, typical length and how it opens.
3. **Headings**: whether there are any, and in what style.
4. **Recurring elements**: captions, tables, quotes, lists, calls to action, sign-offs.
5. **Length**: the typical total length.
6. **Kickoff questions**: the 2 to 4 things you need to ask before writing one.
7. **A draft layout** in markdown, like the ones in the other mode files.

The writers then use that description exactly as they would a built-in mode file. If the samples disagree with each other, the person decides which one is the model.

With fewer than 2 samples, ask the person to describe the parts in order (one question, free answer) and build the description from their answers. Mark it "from description, not samples" so Calibrate can replace it later.
