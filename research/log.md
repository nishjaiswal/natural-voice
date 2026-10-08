# Research log

What each research check found, newest first. Each entry lists findings with their source and date, what was changed in the skill, and questions still open. The sources themselves are in `research/sources.md`. Older notes from before 1.0.0 are in `research/history/`.

## 2026-10-08: Initial research for 1.0.0

Findings:

- **Em dashes are now a historical sign.** Wikipedia's Signs of AI writing moved em dashes to its "historical indicators" on 7 October 2026 (latest revision read: 1379229123, 8 October). An em dash on its own is weak evidence. Source: Wikipedia page history.
- **Newest Claude tells.** Graphite's AI Tells update for Claude Opus 5.5 (1 October 2026, 9,974 topics) found em dashes down 99% from Opus 5 (0.015 against 2.92 per 1,000 words), but total tells down only 4%. New over-used phrases include "this matters" (116 times the human rate), "is more than a ... it" (98 times), "why ... matters" (92 times), "looking ahead the" (40 times) and "dependable" (23 times).
- **Humanizer 3.1.0** (28 September 2026) has 26 patterns, including a new one for replies that re-explain what the reader already knows. In its issue #229, a blind study preferred the rewritten text 16 out of 16 times on quality, but the rewrite did not change AI detection results. The maintainer added to the README that getting past detectors is not a goal.
- **Claude watermarks its text.** Anthropic's text watermark adapts SynthID-Text: it lives in word choices, not hidden characters, and a full rewrite removes it (announced 14 August 2026, updated 1 September 2026). Claude marks text from models launched since 2 August 2026. Detection access is limited. Sources: Anthropic news post and Claude Help article 16266773.
- **OpenAI marks text for EU users.** OpenAI started textGrain text provenance for EU users on 5 October 2026. Its pages refuse automated fetches, so they need a browser to re-check.
- **Google SynthID Text** is documented with clear limits. Whether text from the Gemini API is marked is still unclear.
- **EU AI Act Article 50** (transparency for AI-generated content) applies from 2 August 2026. Systems already on the market before then have until 2 December 2026. The Commission published its Article 50 guidelines and an FAQ on 20 July 2026. The Digital Omnibus did not delay Article 50. A Code of Practice on marking and labelling AI-generated content has signatories; how strongly it is worded still needs checking.
- **Detectors miss style imitation.** Epoch AI (15 July 2026) tested Pangram, GPTZero and Originality.ai. On 495 human passages they wrongly flagged 0, 0 and 3.84%. They caught almost all plainly prompted AI text, but missed 10.1%, 10.8% and 17.9% of AI text that imitated a real author's style, and about 26% of imitated scientific writing.
- **Agent Plugins 1.0.0** launched on 6 August 2026: a root `plugin.json` with a closed schema, skills in `skills/<name>/SKILL.md`. Clients include ChatGPT and Codex, Cursor, GitHub Copilot, Kiro and VS Code. Codex also reads `.agents/plugins/marketplace.json` and, as a fallback, `.claude-plugin/marketplace.json`.
- **Agents moved house.** Google moved Gemini CLI users to Antigravity (`agy`) in June 2026; `agy plugin import gemini` converts old extensions. Antigravity's own `plugin.json` schema is closed (name and description only), so it can't also be an Agent Plugins manifest. Windsurf is now part of Devin.
- **Claude Code packaging.** A `CLAUDE.md` at the plugin root makes `claude plugin validate --strict` fail, so ours lives at `.claude/CLAUDE.md`. Claude Code reads the version from `.claude-plugin/plugin.json` only; it must not be repeated in the marketplace entry.

Changed for 1.0.0: pattern catalogue, detector and watermark guidance, hidden-character cleaner and packaging for each app (see `CHANGELOG.md`).

Open questions:

- Is "Astra" the real name for GPT-6, or a nickname? Check OpenAI's own release notes before using it in `model-tiers.md`.
- The GPT-6 word list comes from a single source. Wait for a second source before adding it to the pattern catalogue.
- Is text from the Gemini API watermarked with SynthID, or only text in Google's own apps?
- How strong is the anti-circumvention clause in the EU Code of Practice, and does it affect editing tools like this one?
- What licence does unslop use? Don't borrow from it until that is clear.
