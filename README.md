# Natural Voice

Writing that sounds like you.

[![Licence: MIT](https://img.shields.io/badge/licence-MIT-blue.svg)](LICENSE)
[![Latest release](https://img.shields.io/github/v/release/nishjaiswal/natural-voice)](https://github.com/nishjaiswal/natural-voice/releases/latest)
[![Open Agent Skill](https://img.shields.io/badge/Agent%20Skill-open%20standard-informational)](https://agentskills.io)
[![skills.sh](https://skills.sh/b/nishjaiswal/natural-voice)](https://skills.sh/nishjaiswal/natural-voice)

[Install](#install) · [What you can say](#what-you-can-say) · [How it learns your voice](#how-it-learns-your-voice) · [Examples](examples/README.md) · [What it won't do](#what-it-wont-do) · [Contribute](#contributing)

Natural Voice learns how you write and how you talk. Then it writes new drafts in your voice, and rewrites anything you paste in (your own rough draft, a ramble, or something an AI wrote for you) so it sounds like you on a good day.

It's a free, open [Agent Skill](https://agentskills.io). It works in Claude, ChatGPT and Codex, Gemini, Cursor, GitHub Copilot, Manus and other AI apps.

## See it work

This is a made-up example. Kit is a fictional designer, Parcelpoint is a fictional delivery app, and the numbers are invented. The rewrite follows the skill's rules and shows the kind of result to expect. It isn't a recorded run.

**What an AI wrote:**

> I'm thrilled to share that we've just launched saved addresses in Parcelpoint! 🚀 Delivering parcels isn't just about speed, it's about trust. Drivers can now save the right entrance for any address, so the next driver doesn't have to hunt for it. Looking ahead, this is only the beginning. The result? Failed first-time deliveries fell from 14% to 9%. Let that sink in.

**After Natural Voice, in Kit's voice** (short, dry, no emoji):

> Drivers can now save the right entrance for an address, so the next driver doesn't have to hunt for it.
>
> Failed first-time deliveries fell from 14% to 9%.

Every fact in the second version was already in the first. If something is missing, Natural Voice leaves a visible `[ADD: ...]` gap for you to fill. More in [`examples/`](examples/README.md).

## Why not just a humanizer?

Most tools in this space remove the habits that make text read as AI. That helps. It also leaves text that sounds like nobody, because nobody's voice was ever put back in.

Natural Voice does both halves. It cleans out the automatic habits, and it writes in a voice it learned from you. Your voice lives in one file you own, so the next piece starts from you and not from a blank page.

It listens first. You can talk it through, and it works out how you sound from what you say.

## What you can say

| Say | What happens |
|---|---|
| **set up** | A short interview (type or talk), a few samples of your writing, and a "which of these sounds like you?" taste test. It saves everything in one voice file. |
| **write** an email / LinkedIn post / case study about... | A new draft in your voice, for that place. For long pieces you can talk it through image by image. |
| **polish** this | Your text back, rewritten in your voice, with AI patterns and hidden characters removed. |
| **clean** this | Hidden characters and AI citation markers removed. Nothing else changes. |
| **show changes** | From now on, polished text comes with a short "what I changed and why" list. Say **hide changes** to turn it off. |
| it doesn't sound like me | Calibrate: retune the tone, or paste the version you edited and it learns from your changes. |

It learns as you go. When you correct a word or a phrase, it asks whether to remember it: always, just in this mode, just this piece, or no.

## Quick start

1. **Install it** in your AI app (see [Install](#install)).
2. **Say "set up Natural Voice".** Answer a few questions. Talking is better than typing.
3. **Say "polish this"** and paste something, or **"write a LinkedIn post about..."** and tell it the story.

## How it learns your voice

- **An interview.** Questions like "tell me about something you worked on, the way you'd tell a friend over dinner" or "what words would make you cringe to see under your name?". Talking is best. Your spoken answers teach it how you actually sound.
- **Your writing.** A few things you wrote yourself, ideally without AI help: a post, an email, a case study.
- **A taste test.** The same sentence written two or three ways. You pick the one that sounds like you.
- **Your edits.** Paste back a draft you changed, and it works out the pattern ("you always cut 'really'", "you split long sentences").
- **A fingerprint.** Where the app can run code, it measures your writing (sentence lengths, punctuation, contractions, common words) and checks every draft against it, so it doesn't just swap one formula for another.

Everything goes into one **voice file** with a **core voice** (who you are and how you sound) and **modes** for each place you write (LinkedIn, email, case study, chat messages and more). See [`examples/kit.voice.md`](examples/kit.voice.md) for a made-up one, and [`examples/polish.md`](examples/polish.md) for a before and after.

## The habits it looks for

The catalogue holds 34 current habits, each with an ID, a plain example, and a note on when to leave it alone. Five of the strongest are:

1. **A contrast with no one:** "It's not a form, it's a conversation."
2. **One-line closers:** "Let that sink in."
3. **Sayings that sound deep:** "At its core, what matters is..."
4. **A staged run-up:** "Here's the thing." "Honestly?"
5. **Arguing with no one:** "I'm not saying X, but..."

It also checks for truth risks (invented experience, a hedge that got dropped, a claim made stronger) and has a guard against over-editing, so a good sentence of yours isn't "fixed" just because it matches a pattern. If your own samples use a habit, it counts as your voice and stays.

The full list is in [`pattern-catalogue.md`](skills/natural-voice/references/editing/pattern-catalogue.md). Writing habits change with every model release, so most entries carry dates, and the ones that have faded are kept in a separate list.

## What it won't do

Natural Voice is a writing tool for your own words. Its limits:

- **It doesn't promise to beat AI detectors.** Removing AI-sounding patterns can make writing read more plainly, but an informal 2026 test of a similar rewrite tool barely moved detector scores, and nobody has tested Natural Voice against them. It never shows a "human score".
- **It can't remove AI watermarks.** Since August 2026, Claude marks the text its newer models write, and OpenAI reportedly started marking ChatGPT and Codex text in the EU in October 2026. These marks are hidden patterns in *which words get chosen*, not hidden characters. Mostly only the company that made them, or partners it has approved, can check for them, and cleaning characters doesn't touch them. If you run Natural Voice on Claude or ChatGPT, its rewrites may carry that company's mark too.
- **It removes hidden *characters*.** Things like zero-width spaces, odd spacing, leftover AI citation markers, look-alike letters and hidden text that tries to give an AI instructions. That's useful, and it's a different thing from a watermark. If text carries a content credential (C2PA, a label saying where it came from), Natural Voice keeps it and tells you; it removes it only if you ask.
- **It's built not to invent.** No made-up facts, numbers, quotes, stories or feelings. Anything missing shows up as a visible `[ADD: ...]` gap.

If an AI detector ever wrongly flags your own writing, your drafts and version history are the honest evidence, so keep them. In Write mode, when it runs on your computer, Natural Voice saves your notes and drafts in your Documents folder.

## Install

### Claude Code

Type these inside a Claude Code chat (not in your computer's Terminal):

```
/plugin marketplace add nishjaiswal/natural-voice
/plugin install natural-voice@natural-voice
```

If it asks where to install, choose "user" so it works in every project. Then type `/natural-voice:setup`. The other commands are `/natural-voice:write`, `:polish`, `:clean`, `:calibrate` and `:voices`. You can also just ask in plain words ("polish this in my voice").

To get updates automatically: type `/plugin`, open **Marketplaces**, pick natural-voice and choose **Enable auto-update**. (It's off by default for marketplaces that aren't Anthropic's.)

### Claude (web and desktop)

Natural Voice is a full plugin (the skill plus slash commands and helper agents). Three ways to add it:

- **Plugin from GitHub (gets updates):** **Customize > Plugins > Add > Add marketplace**, enter `nishjaiswal/natural-voice` and turn on **Sync automatically**.
- **Plugin file:** download `natural-voice-plugin.zip` from the [latest release](https://github.com/nishjaiswal/natural-voice/releases/latest) and upload it in **Customize > Plugins > Upload plugin**.
- **Skill only:** download `natural-voice.zip` and upload it in **Customize > Skills**. You get the skill without the slash commands; plain words like "polish this" still work.

Plugins and skills need a paid plan with code execution turned on. A plugin added in Claude also shows up in Claude Code.

### Codex, Cursor, GitHub Copilot, Gemini CLI, OpenCode, Devin

In your computer's Terminal:

```
npx skills add nishjaiswal/natural-voice
```

It finds the AI apps you have and installs Natural Voice into each one. Update later with `npx skills update`.

Other ways, if you prefer them:
- Codex plugins: `codex plugin marketplace add nishjaiswal/natural-voice`, then `codex plugin add natural-voice@natural-voice` (or find it in the Plugins Directory in the ChatGPT desktop app)
- GitHub Copilot CLI: `copilot plugin install nishjaiswal/natural-voice`
- Gemini CLI extension: `gemini extensions install https://github.com/nishjaiswal/natural-voice --auto-update`
- Antigravity: `agy plugin install https://github.com/nishjaiswal/natural-voice` (run it again to update). If Antigravity refuses the plugin, use `npx skills add nishjaiswal/natural-voice` instead: it puts the same skill in Antigravity's skills folder.

### Manus, ChatGPT and other apps that accept uploaded skills

Download `natural-voice.zip` from the [latest release](https://github.com/nishjaiswal/natural-voice/releases/latest) and add it in the app's skills settings (Manus: **Skills > Add > Upload**). Perplexity wants `natural-voice-flat.zip` instead. Skills support depends on the app and your plan; if you can't find a skills setting, use the next option.

### Apps that only take instructions

For a Gemini Gem, a custom GPT, a Claude or ChatGPT Project, or a Perplexity Space: download `natural-voice-starter.md` and `natural-voice-instructions.md` from the [latest release](https://github.com/nishjaiswal/natural-voice/releases/latest). Paste the starter into the instructions box and add the big file as a knowledge file. In these apps the hidden-character check is a best-effort read, because they can't run the cleaning script.

Then, in any app, say **"set up Natural Voice"**.

## Your data

- Your voice file, samples and drafts stay with you. On your computer they live in a folder you can see, `Documents/Natural Voice` (voice files in `voices`, your writing samples in `samples`, drafts in `drafts`). In chat apps it's a file you download and upload again, or a small personal skill you upload once.
- Your voice file lives outside the skill, so updating Natural Voice never touches it.
- Natural Voice itself sends nothing anywhere. The AI app you run it in sees what you share with it, like any other chat. If you give it links to your own writing, your AI app opens those pages. Check your workplace's rules before sharing confidential work.
- Your voice file is personal. Don't attach it to a GPT, Gem, Space or project that other people use: they can often get its files out.
- It only learns from your own writing. Don't feed it other people's work as samples.

## Staying up to date

AI writing habits change with every model release. "Delve" faded; "this matters" arrived. Em dashes stopped being a reliable sign in late 2026. Natural Voice keeps a dated catalogue of these patterns, and the maintainer reviews the latest research every month: new patterns, ones that have faded, watermark and detector news, and new AI apps. Each release lists what changed in [CHANGELOG.md](CHANGELOG.md). The sources it watches are in [`research/sources.md`](research/sources.md).

Seen a new AI writing habit? [Report it](https://github.com/nishjaiswal/natural-voice/issues/new?template=new-ai-pattern.yml). It takes a minute and needs no code. Please don't paste private writing.

## How it works (for the curious)

```
skills/natural-voice/          the portable skill: works in any app
  SKILL.md                     the main instructions
  references/
    jobs/                      setup, write, polish, clean, calibrate, voices
    modes/                     places you write: case study, LinkedIn, email, chat and more
    editing/                   pattern catalogue, review method, hidden characters,
                               fingerprint, detectors and watermarks
    roles/                     section writer, assembler, voice auditor, sample analyst
    templates/                 voice file, notes, change report
    interview.md               the voice interview
    writing-rules.md           truth rules and the order of authority
  scripts/                     optional Python helpers (hidden characters, fingerprint)
commands/                      Claude Code slash commands
agents/                        Claude Code helper agents
research/                      the sources watched and a dated log of what changed
tests/                         script tests and before/after test texts
dist/                          downloads made by scripts/build.py: the full plugin zip, the skill
                               zip (and a flat copy for Perplexity), and the chat-app instructions
```

## Contributing

Ideas, new modes, new patterns and fixes are welcome. You don't need to write code to help: a new AI habit you've spotted, a mode you wish existed, or a sentence in this README that confused you are all useful. See [AGENTS.md](AGENTS.md) for the rules (they apply to people too).

- Edit files in `skills/natural-voice/`, then run `python3 scripts/build.py`, `python3 scripts/validate.py` and `python3 -m unittest discover -s tests/scripts`.
- Keep instructions in plain language. Most people using this aren't developers.
- Never add anyone's personal writing samples or voice files.
- Every release bumps the version everywhere (`python3 scripts/bump_version.py X.Y.Z`), or apps keep their old copy.

If Natural Voice helped, a star on the repo helps the next person find it.

## Credits

The pattern catalogue draws on Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup), [blader/humanizer](https://github.com/blader/humanizer), Graphite's research on AI writing tells, and the academic work listed in [THIRD-PARTY-NOTICES.md](skills/natural-voice/THIRD-PARTY-NOTICES.md). The editing engine started as Natural Voice Editor; the voice learning started as Say It Better.

## Licence

[MIT](LICENSE). You're free to use and adapt it.

Made by Nishesh Jaiswal, a product designer who explains things better out loud than on a keyboard.
