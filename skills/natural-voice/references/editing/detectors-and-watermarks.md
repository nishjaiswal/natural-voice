# Detector and watermark claims

Evidence checked: 8 October 2026. Vendor pages change often, so recheck them before telling someone what a product does today. "Secondary" means we read a report about the source, not the source itself. "Unverified" means a single source we could not check. This file is not a detector benchmark and not legal advice. Vendor pages tell you what the vendor says; studies tell you what happened in their tested conditions. Neither has tested Natural Voice.

## Four different questions

| Question | Relevant evidence |
|---|---|
| Is the writing clear, specific and faithful? | Editorial review and comparison with the source |
| Does a classifier label it AI-like? | That classifier's output on the exact input, with date, version and what the score means |
| Does it contain a particular statistical watermark? | The provider's detector, which only the key holder can run |
| Does a file carry provenance information? | Inspection of that format and, for signed credentials, a check of the signature |

Each answer stands on its own. A classifier score is not proof of authorship. A clean scan for hidden characters says nothing about a statistical watermark.

## Statistical watermarks

These steer the model's word choices with a secret key. Nothing is added to the text, and only the key holder can check for the pattern. Detection gets more reliable with length and less reliable with editing, translation, short answers and text where only one wording is correct.

- **Claude (Anthropic).** Announced 14 Aug 2026, updated 1 Sep 2026: an adaptation of Google's SynthID-Text. In Anthropic's words, "Nothing is added to the text and there are no hidden characters." Light editing probably won't remove the mark; a full rewrite of every word will. It is weak on short or factual text, and pure proofreading may change too little to detect. The detection API is in private preview for eligible organisations. A detection estimates that Claude was involved. It can't tell writing from heavy editing, can't confirm human authorship and can't spot other AI systems ([technical post](https://www.anthropic.com/news/claude-text-watermark)). The support page says Claude models launched in the EU on or after 2 Aug 2026 support marking at launch, older models are being added, and marking applies worldwide across the API, the Claude apps, Claude Code, Cowork, Tag and cloud partners. It says a mark "may persist through some editing" ([coverage page](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content), checked 8 Oct 2026). Neither page mentions an opt-out. Anthropic signed the EU Code of Practice in July 2026.
- **ChatGPT and Codex (OpenAI "textGrain").** From 5 Oct 2026, ChatGPT and Codex text in the EU carries a word-choice watermark. API developers anywhere can opt in; it is off by default. Detector access starts with approved researchers and expert organisations. Reported detection at a 1% false-positive rate: about 80% at 200 tokens and about 95% at 400 tokens (psychology answers; maths was worse). On 400-token passages, swapping 10% of words for synonyms cut detection from about 92% to 66%, and 25% cut it to 17%. OpenAI warns that "the absence of a detected watermark does not prove human authorship." Secondary: [BleepingComputer, 5 Oct 2026](https://bleepingcomputer.com/news/artificial-intelligence/openai-is-adding-invisible-watermarks-to-chatgpt-and-codex-text-in-the-eu). OpenAI's own page refused our check ([primary](https://openai.com/index/eu-text-provenance/)).
- **Gemini (Google SynthID-Text).** Published in Nature in October 2024 and open source in Hugging Face Transformers 4.46 and later. Google has used it on Gemini app text since 2024 (Google's 2024 announcement; not rechecked on 8 Oct 2026). Google says it is less effective on factual answers and that confidence drops when text is thoroughly rewritten or translated ([Google docs](https://ai.google.dev/responsible/docs/safeguards/synthid)). Google opened a SynthID Detector portal to early testers from a waitlist in May 2025 (secondary); its 2026 status for text is unverified.
- **What editing does.** Watermarks weaken under paraphrase but often survive given enough text. After strong human paraphrasing, one scheme was still detectable after about 800 tokens on average at a 1 in 100,000 false-positive rate ([Kirchenbauer et al., ICLR 2024](https://arxiv.org/abs/2306.04634)). A paraphrasing model evaded several 2023 detectors, including a watermark ([Krishna et al., NeurIPS 2023](https://arxiv.org/abs/2303.13408)). Nobody outside a provider can test the deployed marks today. A Sep 2026 preprint argues this lack of outside checking is the real gap, and found the open-source SynthID-Text changed prose quality no more than changing the random seed ([Nemecek et al.](https://arxiv.org/abs/2609.09604)).

## File provenance (Content Credentials)

- C2PA Content Credentials are signed records attached to a file. They show where a file came from and how it changed. They can't show that its claims are true. Anthropic adds Content Credentials to files Claude generates in its apps and API, and offers a free checker (support page above).
- C2PA 2.4 (April 2026) can embed a credential inside plain text as a run of invisible Unicode variation selectors (Appendix A.8). The specification says to use this only where no other method is feasible. An implementer's documentation places a U+FEFF marker before the run (secondary). Unlike a statistical watermark, this method does use hidden characters ([C2PA 2.4](https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html)).
- If the helper in [text-integrity.md](text-integrity.md) reports a run of variation selectors after an invisible marker, it may be a credential. The helper keeps it by default. Tell the person what it might be. Remove it only if they understand that and ask: removing it breaks the credential, and some providers' terms forbid removing their marks (secondary, see EU rules below). Natural Voice can't verify a credential's signature.

## Classifier detectors

- **Independent test, Jul 2026.** On 495 human passages written before 2022, Pangram and GPTZero flagged none and Originality.ai flagged 3.8%. On plain AI output all three missed almost nothing. When the model imitated a writer from five samples, misses rose to about 10%, 11% and 18%, and up to 29% for scientific writing ([Epoch AI, 15 Jul 2026](https://epoch.ai/data-insights/ai-detectors-false-negatives); 500-word passages; detector versions from June 2026; one evasion method tested).
- **Vendor claim.** Pangram 4 (29 Jul 2026) reports a 0.0041% false-positive rate on one million English web samples and says it still catches 98.83% of text from 13 commercial "humaniser" tools. These are the vendor's figures, read via [a review site](https://www.eesel.ai/blog/pangram-4-review) (secondary). We have not checked them.
- **Non-native and edited writing.** In 2023, seven detectors flagged 61% of TOEFL essays by non-native writers as AI, on average ([Liang et al.](https://arxiv.org/abs/2304.02819); figure from the paper's results, not rechecked on 8 Oct 2026). An Aug 2026 preprint compared 135,389 manuscripts with their native-speaker edits: false-positive rates on human text ranged from 0% to 100% across 13 detectors, and the same edits raised scores on some detectors and lowered them on others ([Park et al.](https://arxiv.org/abs/2608.26710)).
- **Turnitin** shows no number and no highlights for AI scores from 1% to 19%, only an asterisk, because low scores misfire more often. Only instructors see it, and Turnitin says it shouldn't be the only basis for action against a student ([Turnitin help](https://helpcenter.turnitin.com/hc/en-us/articles/46245332050317-Why-is-the-AI-Writing-Detection-report-score-showing-as)).
- **Grammarly**'s percentage estimates how much of the text looks AI-generated. It is not a percentage certainty of authorship ([user guide](https://support.grammarly.com/hc/en-us/articles/28936304999949-AI-Detector-user-guide), checked 30 Sep 2026).
- **GPTZero** says it stopped using perplexity and burstiness for detection in autumn 2023. Advice built on those two measures is out of date ([clarification](https://support.gptzero.me/articles/9585228410-how-do-i-interpret-burstiness-or-perplexity), checked 30 Sep 2026).
- **Rewrite skills.** In an informal Aug 2026 study, model judges preferred a rewrite skill's output to raw model text 16 times out of 16, yet detection barely moved (100%, then 98.6%, then 97.8%), and a commercial detector still scored every variant 100% AI ([Humanizer issue #229](https://github.com/blader/humanizer/issues/229); 77 of 144 planned trials).

## EU rules (summary, not legal advice)

- AI Act Article 50 has applied since 2 Aug 2026. Providers of generative systems must mark outputs in a machine-readable way. Systems placed on the market before that date have until 2 Dec 2026 for the marking duty, under the Digital Omnibus (Regulation (EU) 2026/1744) ([Commission FAQ](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act), updated 24 Jul 2026).
- The marking duty doesn't apply where the AI performs "an assistive function for standard editing" or doesn't substantially alter the input (Article 50(2)). The Commission's July 2026 guidelines give examples. Whether a given edit counts is a question for providers and regulators. Natural Voice can't decide it.
- The final Code of Practice on Transparency of AI-generated Content was published on 10 Jun 2026. About 190 organisations had signed by the end of July 2026, Anthropic among them ([Commission page](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content)). Law-firm summaries say it asks for at least two layers of marking for most content (with plain text as an exception), and that signatories commit to banning deliberate removal or tampering in their terms and to not offering tools for getting round marks. Secondary: the Commission's summary page doesn't describe these measures, and the summaries differ on how strong the wording is.
- Commentators note that the Act doesn't directly bar third parties from removing marks (secondary).

## What the research supports

- Some rewriting methods reduce detection on tested systems; others fail, and detection sometimes rose after rewriting. The method in "A Universal Attack" uses detector-guided decoding, which an ordinary editing prompt doesn't do ([Cheng et al., 2025, Appendix E](https://arxiv.org/html/2506.07001v2#A5)).
- Results depend on model, genre, length and editing. [RAID](https://aclanthology.org/2024.acl-long.674/) is a 2024 benchmark. The July 2026 [Authorship-Rewriting Benchmark preprint](https://arxiv.org/abs/2607.29539) tested English texts, four open-weight generators and five detectors. Neither tested Natural Voice, Claude, Grammarly or GPTZero.
- Post-editing moves a model draft towards the writer's own style, but the result stays closer to the model's style than the writer's unassisted writing does. Writers often felt it was theirs anyway ([Baumler et al., ACL 2026](https://aclanthology.org/2026.acl-long.2030/), 81 participants). Judge a voice match with the writer, and let them make the last edit.
- People now use some model-favoured words in their own speech ([Yakura et al.](https://arxiv.org/abs/2409.01754)), so word lists flag human writing too.

## If you run Natural Voice on Claude or ChatGPT

- A rewrite is new model output. On Claude (models launched on or after 2 Aug 2026) and on ChatGPT or Codex in the EU, it may carry that provider's watermark, even when the ideas and many of the words are the person's. In other apps, check the provider's pages.
- Natural Voice does not and cannot remove statistical watermarks. It won't try, and it won't advise on how to.
- Removing hidden characters (`scripts/text_integrity.py clean`) has no effect on these watermarks.
- Never show a "human score", an "AI %" or a "passes detectors" claim for any draft.
- If a provider's detector finds its mark, that result is accurate: an AI processed the text. Say so plainly if asked.
- For people wrongly flagged by a detector, their own drafts, notes, dictation recordings and version history are the honest evidence. Suggest they keep them.

## Respond to common requests

"Make it undetectable." Say that nobody can honestly promise that: in 2026, detectors still catch most edited AI text and still flag some human writing. Offer to make it clearer and more like them, then revise for the actual reader and purpose. Don't claim a score without running the test ([evaluation.md](evaluation.md)).

"Remove Claude's (or ChatGPT's) watermark." Explain that the mark is a statistical pattern in word choice, with no hidden characters. Natural Voice won't try to remove it, and a rewrite in the same app may carry a new mark. If they are worried about hidden characters, offer a character inventory and call it exactly that. If they want words that are entirely their own, they can write or rewrite the final version themselves, and Natural Voice can give notes instead of a rewrite.

"It passed one detector." Record the exact result, the date and the version. Don't extend it to other tools or future versions.

"A video proves it works." Look for the complete input and output, the detector version and date, repeat runs, several samples, quality checks and failures. A caption or screenshot records a reported result. It doesn't reproduce it.

"A detector flagged my own writing." Explain that detectors make false positives, more often on non-native and professionally edited writing. Suggest they gather drafts, notes and version history, and ask which detector, version and date produced the score and what the score means. Natural Voice can help them write a short, calm explanation. Don't run a "humanising" pass on their own work to dodge the flag: it changes their writing and removes evidence of how they wrote it.

---

Last reviewed: 2026-10-08.
