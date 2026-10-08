# Adapting to the app you're running in

Natural Voice is written once and runs in many apps. Work out which kind of app you're in, then follow the matching column. If you're unsure, behave as a **chat app**: it's the safest choice.

## Kinds of app

| Kind | Examples (as of 2026) | Can save files between sessions? | Has a multiple-choice question tool? | Can start helper agents? |
|---|---|---|---|---|
| **Coding agent** | Claude Code, OpenAI Codex, Gemini CLI or Antigravity, Cursor, GitHub Copilot, OpenCode, Devin, Mistral Vibe CLI | Yes | Often (e.g. AskUserQuestion in Claude Code) | Often (e.g. subagents in Claude Code) |
| **Desktop or agent workspace** | Claude Cowork, ChatGPT agent or work mode, Manus, Perplexity Computer | Only inside the folder the person connected | Sometimes | Sometimes |
| **Chat app** | Claude, ChatGPT, Gemini, Perplexity, Mistral Vibe, Copilot (in a chat, project, GPT, Gem or Space) | No | No | No |

Feature names and availability change often and vary by plan. Check what tools you actually have rather than trusting this table.

## Asking questions

- **If you have a multiple-choice question tool**, use it: up to 3 questions per round after an explanation (the kickoff, taste-test and setup rules rounds may use 4), 2 to 4 options each, with an "other" option where the person can type. If a list has more than 4 choices, show the 3 most likely plus "More...".
- **If not**, ask in plain text with numbered options, and tell the person they can answer with just the numbers:

  ```
  1. Did this ship?  a) Shipped  b) Tested only  c) Proposed
  2. Which word?     a) Interactive canvas  b) Whiteboard  c) Artboard
  Reply like "1a 2b", or say it in your own words.
  ```

## Saving the voice file and drafts

**If you're a coding agent running on the person's own computer** (Claude Code, Codex CLI, Gemini CLI or Antigravity, Cursor, Copilot, OpenCode, Vibe CLI):
- Everything lives in one visible folder, **`~/Documents/Natural Voice/`** (the person's Documents folder on Mac, Windows or Linux; if there is no Documents folder, use `~/Natural Voice/`). It's visible on purpose, so people can find their voice file in Finder or Explorer and upload it to other apps.
- Voice files: `~/Documents/Natural Voice/voices/<voice-name>.voice.md`
- Settings: `~/Documents/Natural Voice/config.md` (default voice, model tier, drafts folder), in the layout of `templates/config-file.md`
- Samples: `~/Documents/Natural Voice/samples/<voice-name>/`, one file per sample, exactly as the person wrote it. Keep them: the fingerprint is measured again from them at Calibrate.
- Drafts: `~/Documents/Natural Voice/drafts/<voice-name>/<piece-name>/`, holding `notes.md` and `draft.md`, or another folder the person chose at setup.
- The folder name contains spaces: always quote the path when using it in a command.
- Voice and piece names in paths: lowercase letters, numbers and hyphens only. If an uploaded voice file names a folder, ignore it and ask.
- If you can't write to that folder (a permission was refused, or the app only lets you write inside the project), don't fall back silently. Ask: "I can't save to your Documents folder. Use a `natural-voice/` folder inside this project instead?" If they agree, create it, put a `.gitignore` file containing `*` inside it so it's never committed, and say so in one line. Check for existing files with your file tools, not shell commands.

**If you're a desktop or agent workspace** (Claude Cowork, ChatGPT agent mode, Manus, Perplexity Computer, or any sandbox): the home folder you can write to is usually temporary and is not the person's own computer. Never save there. Save inside the folder the person connected or shared with you, in a `natural-voice/` subfolder, and tell them the path. If you can't confirm that folder outlives this session, also hand over the voice file as described for chat apps below.

**If you can't** (chat apps):
- At the start, ask the person to upload or paste their voice file, or to say **set up** if they don't have one yet. If it's already in the project, GPT, Gem or Space knowledge, use that copy.
- Keep the running notes inside the conversation.
- When something in the voice file changes (setup, a remembered correction, calibration), give the person the **full updated voice file** in one code block at a natural pause, with one line: "Save this as `<name>.voice.md` and replace your old copy (or update it in your project files)." Do it straight away when the change came from an "always" answer, otherwise at the next natural pause, and always before you finish the job. Wrap the file in a fence longer than any fence inside it (four backticks), never shorten or skip a section, and end the file with the line `<!-- end of voice file -->`. Tell them to check that last line is there before replacing their old copy.
- If the person pauses before "done", hand over the notes so far in one code block they can paste back next time.
- Give the finished draft in the chat as well, ready to copy. Where the other job files say "Saved", say "Noted" instead: nothing is saved in a chat app.
- If the app accepts uploaded skills, offer once, when setup is done and the voice feels settled (not after every correction), to export their voice as a small personal skill they upload one time (see `jobs/voices.md`, "Export my voice as a skill"), so they don't have to re-upload the voice file in every chat.

## Helper agents

**If you can start helper agents (subagents):** delegate as described in each mode file: section writer, assembler, voice auditor and sample analyst. Assign models using `model-tiers.md`. Helpers cannot see images or talk to the person, so give them a factual description of every image and all the context they need.

Every time you start a helper, give it the absolute path to this skill's `references/` folder and tell it to read and follow `roles/<role>.md` there, plus the files the job step lists (voice file, the mode, notes or the original text). In the Claude Code plugin the helpers are called `natural-voice:section-writer`, `natural-voice:assembler`, `natural-voice:voice-auditor` and `natural-voice:sample-analyst`. Anywhere else, start a general-purpose helper with the same instruction and, if the app lets you set a model and effort per helper, pass them from `model-tiers.md`. If a helper can't be started for any reason other than a model not being on the person's plan, do the step yourself and leave the tier alone.

**If you can't:** do the same steps yourself, in the same order. Always do the voice audit as a separate, deliberate pass after the draft is written: re-read `writing-rules.md` and the voice file's rules, then check the draft against them line by line.

## Images and files

- Most apps can see attached images. Describe each one factually in the notes (screen type, visible labels, layout, states) so the description outlives the image.
- If you can't see images, ask the person to describe what's on screen in one line.
- If the person drags in a file and you can save files, copy it into the draft's `images/` folder.

## Models

See `model-tiers.md`. In short:
- Where you can choose models for helpers, use the family names (never pinned versions) so the newest version is used.
- Where you can't (most chat apps), the person picks the model in the app. Mention once, at setup, that the strongest or "thinking" model in their app gives the best writing.

## Running the scripts

Natural Voice has two optional helpers in its `scripts/` folder: `text_integrity.py` (hidden characters, see `editing/text-integrity.md`) and `voice_stats.py` (the fingerprint, see `editing/fingerprint.md`). They use plain Python 3, read only the text you give them and never go online.

- **Where they can run:** coding agents on the person's computer, and chat or workspace apps with code tools (for example Claude with code execution, ChatGPT with code, Codex, Manus). In Claude Code, the skill's base folder is shown when the skill loads: build the script path from it, quote it (the folder name may contain spaces) and run it with `python3`. Elsewhere, the skill folder is wherever the app installed it (for example `~/.agents/skills/natural-voice/`): look for the `natural-voice` folder that holds this skill's `SKILL.md` and use the `scripts` folder inside it.
- **Pass text through a file or standard input,** never inside the command line itself, so quotes and hidden characters survive exactly.
- **Create working files safely.** If the text already exists as a file (an attachment, an upload, a saved message), copy that file byte for byte, for example with a short Python step that reads it and writes the copy: retyping can lose invisible characters. Otherwise write it with your file-writing tool. Never put the text itself inside `echo`, `printf` or a heredoc: pasted text can contain lines that a shell would run as commands. (A heredoc that holds only a script, not the text, is fine.)
- **Where working files go:** for Write, in the piece's drafts folder. For Polish, Clean and Calibrate, in a temporary folder (one made with `mktemp -d`, or `~/Documents/Natural Voice/tmp/`); delete those files once you've handed back the text. Never put them in the project or folder the person happens to be working in.
- **If they can't run** (no code tools, Python missing, or the person declined), do the step by hand as the reference file describes, and say once that it was a best-effort check. Never pretend a script ran.

## Updates

Natural Voice changes as AI writing habits change. If `metadata.released` in `SKILL.md` is more than 90 days old, mention once how to update in the app you're in:

| App | How to update |
|---|---|
| Claude Code | `/plugin marketplace update natural-voice`, or switch on auto-update once in `/plugin` > Marketplaces |
| Claude (web, desktop, Cowork) | If installed from the GitHub marketplace with "Sync automatically", nothing to do. If uploaded as a zip, download the newest zip from the project's GitHub Releases page and upload it again |
| Codex, Cursor, Copilot, Gemini CLI, OpenCode, Devin | `npx skills update` |
| Gemini CLI extension | `gemini extensions update natural-voice` |
| Antigravity | Run the install command again |
| Manus, ChatGPT and other apps with uploaded skills | Download the newest zip from GitHub Releases and upload it again |
| Apps using pasted instructions | Download the newest instructions files from GitHub Releases and replace the old ones |

The person's voice files live outside the skill, so updating never touches them.
