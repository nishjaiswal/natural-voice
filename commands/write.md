---
description: "Write something new in your voice: an email, a LinkedIn post, a case study and more."
argument-hint: "[what to write]"
disable-model-invocation: true
---

Use the **natural-voice** skill for the **write** job.

1. Load the skill `natural-voice:natural-voice` with the Skill tool. Its base folder is shown when it loads; read its `SKILL.md`.
2. Then read and follow `references/jobs/write.md` in that folder.
3. You are in Claude Code: you can save files, run the Python scripts in the skill's `scripts/` folder, use AskUserQuestion for questions, and start the plugin's helper agents (`natural-voice:section-writer`, `natural-voice:assembler`, `natural-voice:voice-auditor`, `natural-voice:sample-analyst`). Pass `model` and `effort` from `references/model-tiers.md` (Anthropic row) only when a tier other than `inherit` is saved in `config.md`. Always give helpers the absolute path to the skill's `references/` folder.

Anything the person typed after the command: $ARGUMENTS
