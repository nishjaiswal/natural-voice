---
description: "Set up your Natural Voice: a short interview, a few samples of your writing and a quick taste test."
argument-hint: "[voice name]"
disable-model-invocation: true
---

Use the **natural-voice** skill for the **setup** job.

1. Load the skill `natural-voice:natural-voice` with the Skill tool. Its base folder is shown when it loads; read its `SKILL.md`.
2. Then read and follow `references/jobs/setup.md` in that folder.
3. You are in Claude Code: you can save files, run the Python scripts in the skill's `scripts/` folder, use AskUserQuestion for questions, and start the plugin's helper agents (`natural-voice:section-writer`, `natural-voice:assembler`, `natural-voice:voice-auditor`, `natural-voice:sample-analyst`). Pass `model` and `effort` from `references/model-tiers.md` (Anthropic row) only when a tier other than `inherit` is saved in `config.md`. Always give helpers the absolute path to the skill's `references/` folder.

Anything the person typed after the command: $ARGUMENTS
