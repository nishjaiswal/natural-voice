# Model tiers: who runs what

## The principle

Unless the person chose a tier, helpers use the same model as their session. The tiers below are for people who choose one: the strongest model their plan allows for writing, stepping down gracefully when it isn't available, and the fastest model for small mechanical jobs.

**Never pin a model version** in a voice file, config or helper call (no "4.5", no dates). Use the family's short alias, or let the app choose. An alias follows the newest version of its family, so Natural Voice keeps using current models without anyone updating it. When a vendor adds a family above the current top one (as Anthropic did with Fable above Opus), maintainers update the table below.

## Roles

| Role | What it does | Needs |
|---|---|---|
| **Orchestrator** | Talks to the person, reads images, writes read-backs, asks questions | Whatever the person's session is running. You can't change it; it's their choice. |
| **Writer** | Writes each section and assembles the full piece | The session's model, or the most capable model in the chosen tier |
| **Analyst** | Studies writing samples at setup and calibration | The session's model, or the most capable model in the chosen tier |
| **Auditor** | Checks the draft against the rules | A strong mid-tier model is enough |
| **Runner** | Small jobs: find files, count words, search for banned words, list voices | The fastest, cheapest model |

## Tiers

| Role | Tier 1: best | Tier 2: balanced | Tier 3: light |
|---|---|---|---|
| Writer, Analyst | top model, high effort | mid model, high effort | mid model, medium effort (fast model if no mid) |
| Auditor | mid model, high effort | mid model, medium effort | fast model |
| Runner | fast model | fast model | fast model |

- **Inherit** (the default) uses whatever model the person's session runs, for every role.
- **Tier 1** is for plans that include the vendor's top model.
- **Tier 2** is for people who want to save usage: writing on the mid model.
- **Tier 3** is for the lightest plans.

## Model families by vendor

These are aliases or family names, not versions (last checked 2026-10-08). Vendors rename families from time to time, and the maintainer refresh updates this table. If a name here stops working, use the vendor's current equivalents, and maintainers should update this table.

| Vendor | Top | Mid | Fast | How to pick in a helper call |
|---|---|---|---|---|
| Anthropic (Claude Code, Agent SDK) | `fable`, stepping down to `opus` if the plan doesn't include it | `sonnet` | `haiku` | `model: fable` etc. on the subagent; aliases resolve to the newest version of that family |
| OpenAI (Codex) | the current flagship GPT model | the default Codex model | the current "mini" model | Set in the person's Codex config or profile; helpers usually inherit |
| Google (Gemini CLI, Antigravity) | Gemini Pro | Gemini Flash | Gemini Flash-Lite | The app's model setting; helpers usually inherit |
| Mistral (Vibe CLI) | Mistral Large | Mistral Medium | Mistral Small | Vibe settings |
| Chat apps (all vendors) | The person chooses in the app's model menu. You can't switch models from inside a chat. | | | |

## Choosing the tier

At setup, ask once (see `jobs/setup.md`) and save it as `tier:` in `config.md` (chat apps have no tier: the person picks the model in the app). If nothing is saved, or the saved tier is `inherit`, don't set a model or effort for helpers: they inherit the person's own session model, which is always available and is their own choice.

## Stepping down automatically

If starting a helper fails:
1. **The error clearly says the model isn't included in the person's plan or account:** retry one step down for that role (Writer and Analyst: top → second top, where the vendor has one, such as `fable` → `opus` → mid → fast; Auditor: mid → fast), tell the person once ("Your plan doesn't include <model>, so I'm using <model> for the writing. Say *change models* any time to change this.") and save the lower tier.
2. **It's a usage limit, rate limit or overload:** retry once; if it still fails, step down for this session only, say "You've hit your <model> limit, so I'm using <model> until it resets", and save nothing.
3. **The helper type doesn't exist, or it fails for any other reason:** do the step yourself (see `platforms.md`) and leave the tier alone.

Never step up without being asked, because it uses more of the person's plan.

## In chat apps

You can't choose the model. Say once at setup: "Tip: for the best writing, pick the strongest or 'thinking' model in your app's model menu." Then work with what they have. Don't repeat the tip.
