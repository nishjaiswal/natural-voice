# Natural Voice Editor: fresh audit and Claude conversion

Reviewed: 30 September 2026. Standalone release: Natural Voice 1.0.0.

## Verdict

The existing skill is substantially accurate and carefully scoped. We found no fabricated citation or materially false core claim in its detector and watermark reference. Its editing workflow is a defensible set of editorial heuristics, not a scientifically validated recipe. The evidence does not establish an accuracy percentage, superiority over ordinary prompting, reliable personal-voice recovery, or detector evasion.

The most useful changes are portability, explicit dialect precedence, better treatment of dictated voice samples, and clearer boundaries between vendor statements, research findings and observed plugin behaviour. Replacing it with a forbidden-word list would weaken it.

## How the review was divided

Four independent agents reviewed factual evidence, editorial guidance, Claude compatibility and the Python helper. A fifth agent then performed six writing tasks using the revised skill without the audit conclusions. The coordinating agent checked primary sources, reconciled findings, built the package and reviewed test outputs. The local Claude CLI was used for structural validation; authenticated Claude generation and account installation were not available. See `validation.md` for the exact checks and limits.

Direct primary-source retrieval supplied the evidence. Some search-engine queries returned irrelevant results; those results were discarded. An error retrieving a versioned paper URL was resolved through its primary unversioned abstract and PDF, rather than treating an access error as evidence that the paper did not exist.

## Findings and actions

| Area | Finding | Change |
|---|---|---|
| Meaning before style | Strong existing rule. It protects numbers, ownership, negation, uncertainty and outcome status. | Retained; added the force of requests, disagreement, politeness and commitments. |
| Plain language | Audience and purpose should guide clarity. Technical terms can be necessary. Official guidance supports preserving meaning and modal distinctions. [1–2] | Kept contextual guidance; no absolute word, punctuation or sentence-length bans. |
| Locale | A British-English default could conflict with preservation of the source dialect. | Explicit destination requirements first; otherwise preserve a consistent source dialect. British English remains the default for new English prose without another preference. |
| Voice samples | Existing caution is justified. Human post-editing research does not validate this model-driven editing skill. [3] | Made inferred profiles provisional and distinguished spoken disfluency from stable writing preferences. |
| Cultural expression | A 2026 South Asian English study demonstrates dialect loss in its tested model and tasks. It is not a Claude result. [4] | Explicitly preserve dialect and code-switching unless localisation is requested. |
| Claude text watermark | The original claim is real. Anthropic describes SynthID-Text, word-choice patterns and no hidden characters; detection access remains limited. [5–6] | Refreshed the check date and retained a live coverage link. No frozen model list or invented watermark test. |
| Watermark removal | Probabilistic, configuration-dependent detection and rewriting limits remain relevant. A Unicode scan does not inspect the statistical signal. [7] | Labelled the possibility of a rewriting model adding its own watermark as an inference. |
| Detector metrics | Grammarly describes an estimated share of AI-like text. GPTZero says perplexity and burstiness ceased to be its detection method in autumn 2023. [8–9] | Retained the distinctions and attributed statements to the vendors. |
| File provenance | C2PA helps verify provenance and binding; it does not establish factual truth. [10] | Updated the explainer reference from 2.2 to 2.4. |
| Research claims | The cited studies exist, but their methods and tested systems differ from an editing prompt. [11–15] | Added study dates, scope and limitations; identified ARB as a preprint. |
| Standalone packaging | The original depended on parent Design Plugin references and included Codex UI metadata. | Removed those dependencies and created an ordinary Claude plugin manifest. |

## What the research can and cannot establish

Baumler and colleagues studied human post-editing with 81 participants. Their embedding measures found movement towards unassisted style, with remaining differences. Participants' sense of authenticity and model measures sometimes differed. This supports assessing a voice match with the writer; it does not establish that the writer's judgement is wrong or that this plugin recovers a complete voice. [3]

The South Asian English study used Llama 3.3 70B and a 500-sentence diagnostic benchmark. Explicit dialect-aware instructions improved retention in that setup. The portable lesson is to respect the author's language variety; its measured improvements are not this plugin's results. [4]

Cheng and colleagues' method uses detector-guided decoding. Their failure appendix reports unsuccessful and counterproductive outcomes. It cannot substantiate a promise that an ordinary rewrite prompt makes arbitrary writing undetectable. [11]

RAID is a 2024 benchmark across generators, domains and attacks. ARB is a July 2026 English-language preprint using four open-weight generators and five detector implementations. These provide context for evaluation design, rather than current performance figures for Claude, Grammarly or GPTZero. [12–13]

Liang and colleagues documented disparities for non-native English writing in the detectors they studied in 2023. MULTITuDE evaluated multilingual detection. Both support examining relevant populations and languages; neither supplies a failure rate for every present-day service. [14–15]

## Installation and compatibility

Anthropic's current documentation supports a single ZIP plugin across Claude chat, Cowork and Claude Code. Skills are supported across those surfaces. This plugin contains one skill, supporting references and an optional local Python helper. It requires no MCP server, connector credentials or hooks. The host still controls tool availability. [16–18]

Upload the delivered ZIP through **Customize → Plugins → Add → Upload plugin**. An account installation can sync into Claude Code on that account; a session-only `--plugin-dir` load does not install it to the account. The full instructions are in the archive's `README.md`. Documentation compatibility is distinct from a successful upload to your account, which was not performed.

## Sources checked

All URLs below were inspected as primary sources for this review on 30 September 2026. Publication years are not claims that these older studies describe every current system.

1. [European Commission: Plain language](https://translation.ec.europa.eu/languages-and-translation-european-commission/plain-language-making-european-commission-texts-clear_en), updated June 2026.
2. [UK Cabinet Office: Functional Standards writing style guide](https://www.gov.uk/government/publications/handbook-for-standard-managers/functional-standards-writing-style-guide).
3. [Baumler et al.: Can You Make It Sound Like You?](https://aclanthology.org/2026.acl-long.2030/), ACL 2026.
4. [Bharati et al.: The American Palimpsest](https://aclanthology.org/2026.c3nlp-1.8/), C3NLP 2026.
5. [Anthropic: How Claude's text watermark works](https://www.anthropic.com/news/claude-text-watermark), 14 August 2026; the coordinating agent also retrieved its 1 September update note.
6. [Claude Help: How Claude marks AI-generated content](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content), live coverage and detection-access documentation.
7. [Google: SynthID Text](https://ai.google.dev/responsible/docs/safeguards/synthid).
8. [Grammarly: AI Detector user guide](https://support.grammarly.com/hc/en-us/articles/28936304999949-AI-Detector-user-guide).
9. [GPTZero: How do I interpret burstiness or perplexity?](https://support.gptzero.me/articles/9585228410-how-do-i-interpret-burstiness-or-perplexity).
10. [C2PA 2.4 Explainer](https://spec.c2pa.org/specifications/specifications/2.4/explainer/Explainer.html).
11. [Cheng et al.: Adversarial Paraphrasing](https://arxiv.org/html/2506.07001v2#A5), version 2, October 2025, including failure cases.
12. [RAID](https://aclanthology.org/2024.acl-long.674/), ACL 2024.
13. [Perrone and Romano: ARB](https://arxiv.org/abs/2607.29539), July 2026 preprint.
14. [Liang et al.: GPT detectors are biased against non-native English writers](https://arxiv.org/abs/2304.02819), 2023.
15. [MULTITuDE](https://aclanthology.org/2023.emnlp-main.616/), EMNLP 2023.
16. [Claude: Plugins overview](https://claude.com/docs/plugins/overview).
17. [Claude: Plugin structure and testing](https://claude.com/docs/plugins/build).
18. [Claude: Platform support](https://claude.com/docs/plugins/platform-support).
19. [Claude Code: Plugin manifest reference](https://code.claude.com/docs/en/plugins-reference).

## Next meaningful check

Use the plugin on a real draft and same-genre writing samples, then judge whether the edit preserves your position and sounds like you. A detector percentage cannot answer that question. No human preference study, blinded baseline comparison or commercial detector benchmark was performed here.
