# Changelog

What changed in each release of Natural Voice, newest first. Version numbers follow the rule in `scripts/bump_version.py`: the last number for content refreshes and fixes, the middle number for new features.

## 1.0.0 (2026-10-08)

First public release.

- Renamed from Say It Better to Natural Voice.
- Merged in the Natural Voice Editor engine: its editing passes, detector and watermark guidance and evaluation checks now live in `references/editing/`.
- New voice interview: a short set of questions about how you write and talk, alongside your own samples and a quick taste test.
- One voice file holds a core voice plus modes, the places you write for (LinkedIn, email, case study and others).
- A before and after change report shows what was edited and why, when you want it.
- Upgraded hidden-character cleaner: finds Unicode tag characters, leftover citation markers from AI tools and look-alike letters from other alphabets, and leaves the wording alone.
- Voice fingerprint: a small script that measures sentence length, punctuation and favourite words in your samples, so drafts can be checked against them.
- Updated 2026 catalogue of AI writing patterns, with notes on which ones are fading.
- Honest watermark guidance: what rewriting can and can't change, and why no tool can promise "undetectable".
- Packaging for Claude Code (plugin and marketplace), Codex and ChatGPT, Cursor, GitHub Copilot, Gemini CLI and Antigravity, Manus, and chat apps (zip, single-file and starter editions).
- A monthly maintainer refresh (`.claude/commands/refresh-research.md`) checks the sources in `research/sources.md` and proposes updates for approval.
