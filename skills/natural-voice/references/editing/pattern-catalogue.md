# Pattern catalogue

How to use it:

- The person's voice file decides style. If their samples or rules use a pattern, it is part of their voice: leave it.
- This catalogue only flags habits. People use every pattern in it, so it can't tell who wrote a text.
- Truth rules always win ([writing-rules.md](../writing-rules.md), section 1). A fix that changes a fact is a mistake.
- **Strong alone:** one clear sighting is enough to edit. **Weak alone:** act only in a cluster (three or more sightings in one paragraph, or the same habit across the piece). **Truth check:** check on every edit.
- Never edit to chase a detector score. See [detectors-and-watermarks.md](detectors-and-watermarks.md).
- Name patterns by ID in fix lists (for example `NV-M01`). A voice file can switch a pattern on or off by ID in *My rules* or a *Learned* entry.

| Group | IDs |
|---|---|
| Staging instead of saying it | NV-S01 to NV-S05 |
| Rhythm on autopilot | NV-R01 to NV-R05 |
| Inflation and borrowed authority | NV-I01 to NV-I08 |
| Formatting by rule | NV-F01 to NV-F03 |
| Chat and draft leftovers | NV-C01 to NV-C05 |
| Writing for the wrong reader | NV-W01 |
| 2026 model phrasing | NV-M01 to NV-M07 |
| Truth risks | NV-T01 to NV-T06 |
| Over-correction guard | NV-G01 to NV-G08 |
| Historical (faded) patterns | NV-H01 to NV-H06 |

"Seen in" gives the models and dates where a source measured or reported the pattern. Ratios such as 116× mean times the rate in human writing, unless a line says otherwise. All examples are made up.

## Staging instead of saying it

### NV-S01 Contrast with no one
**Strong alone.** Seen in: Gemini 3.1 Pro ("is not just a _ it is", 153×, Sep 2026); Claude Opus 5 (Sep 2026); chat output 2024 to 2026. The literal "it's not X, it's Y" is fading in Claude Opus 5.5 (Oct 2026), see NV-M02. Credit: [Humanizer][hz] §1; [Wikipedia][wp], Negative parallelisms; [Graphite, Sep 2026][gr-sep]; [The Economist, Jul 2026][econ] (secondary).
- Looks like: "It's not a form, it's a conversation." "This isn't about speed. It's about trust." "The date fills itself in, no guessing."
- Why it reads as automatic: it invents a view nobody held, so the real point sounds bigger without adding a fact. Better move: state the point.
- Leave it alone when: the reader really holds the first view ("Most people think export saves a file. It copies a link."), or both halves carry a fact.

### NV-S02 One-line closers and dramatic fragments
**Strong alone.** Seen in: all model families; rewrite passes add more of them ([Humanizer #229][hz-229], Aug 2026). Credit: [Humanizer][hz] §2; [writing rules][nv-rules] ("staccato drama").
- Looks like: "That's the difference." "Let that sink in." "It broke. Badly. Again." A line after an example that explains what the example just showed.
- Why it reads as automatic: it asks the reader to pause instead of giving them something new. Better move: cut it, or make it a sentence with a new fact or consequence.
- Leave it alone when: the short line carries new information, or the person's samples use fragments this way.

### NV-S03 Sayings that sound deep
**Strong alone.** Seen in: all model families, 2023 to 2026. Credit: [Humanizer][hz] §3; [Wikipedia][wp], Undue emphasis on significance.
- Looks like: "At its heart, onboarding is about belonging." "The real question is trust." "Good defaults are the grammar of a product."
- Why it reads as automatic: an ordinary point is dressed up as a hidden truth. Better move: say the specific claim and what it rests on.
- Leave it alone when: it is the person's own line from their samples or dictation, or a quotation.

### NV-S04 Staged run-up
**Strong alone.** Seen in: chat-tuned models since 2023; staged candour ("Honestly?") in 2025 to 2026 output. Credit: [Humanizer][hz] §4; [writing rules][nv-rules] ("signposting"); earlier Natural Voice pattern review ("generic openings").
- Looks like: "In a world where attention is scarce..." "Let's break it down." "Here's the thing." "Quick note:" "Honestly? It depends."
- Why it reads as automatic: it announces the point instead of making it. Better move: start with the point or the fact.
- Leave it alone when: "honestly" or "look" sits inside an ordinary spoken sentence, or the piece is a talk script.

### NV-S05 Arguing with no one
**Strong alone.** Seen in: drafts a model has revised several times (Humanizer 3.x, 2026). Credit: [Humanizer][hz] §5.
- Looks like: "To be clear, this isn't a criticism of the old team." "One might be tempted to add a filter, but..." "I'm not saying research is useless."
- Why it reads as automatic: it answers an objection nobody raised, often left over from an earlier draft. Better move: cut the defence and keep any real claim inside it.
- Leave it alone when: the objection is real and named, or the option is one the reader would actually weigh.

## Rhythm on autopilot

### NV-R01 Forced threes
**Weak alone.** Seen in: all model families; Wikipedia examples up to Jun 2026; [The Economist, Jul 2026][econ] (secondary). Credit: [Humanizer][hz] §6; [Wikipedia][wp], Rule of three; [writing rules][nv-rules].
- Looks like: "clear, calm and confident"; three parallel examples followed by a lesson; "faster, simpler, safer" in every paragraph.
- Why it reads as automatic: the list is shaped for rhythm, and the third item often adds nothing. Better move: use the number of items the facts give you.
- Leave it alone when: there really are three things ("three branches: North, Riverside and Old Town").

### NV-R02 Same-shaped sentences
**Weak alone.** Seen in: GPT-6 (sentences held to 8 to 20 words, Sep 2026, unverified); long sentences of even length ([The Economist, Jul 2026][econ], secondary); rewrite passes make rhythm more uniform ([Humanizer #229][hz-229], Aug 2026). Credit: [Humanizer][hz] §7; [Wikipedia][wp]; earlier Natural Voice pattern review.
- Looks like: every sentence 12 to 16 words; three sentences in a row starting "She"; chains of "and... and..." of the same length; every paragraph four sentences; a short punchy line after every long one.
- Why it reads as automatic: the rhythm is set by rule, not by the argument. Better move: vary length the way the person's samples vary (check their Fingerprint).
- Leave it alone when: the repetition is deliberate (numbered steps, a speech), or it matches the person's samples.

### NV-R03 Narrow punctuation
**Weak alone.** Seen in: newest models after dash suppression ([Wikipedia][wp], Oct 2026, uncited); fewer semicolons and brackets ([The Economist, Jul 2026][econ], secondary); GPT-6 Astra uses dashes at about one-eighth of the human rate and Gemini 3.1 Pro almost none ([Graphite, Sep 2026][gr-sep]). Sources disagree on commas: The Economist found fewer, Wikipedia now says more. Credit: as listed.
- Looks like: 500 words with only commas and full stops; no colon, semicolon, bracket or dash anywhere.
- Why it reads as automatic: punctuation chosen by default, not by meaning. Better move: use the mark the sentence needs, at the person's usual rate.
- Leave it alone when: the person writes this way (check their Fingerprint), or the text is UI copy.

### NV-R04 Stacked qualifiers
**Weak alone.** Seen in: GPT-5.6 Sol, where hedging peaked ([Graphite, Sep 2026][gr-sep]); text a model has edited many times. Credit: [Humanizer][hz] §9.
- Looks like: "could potentially help in some cases"; "may arguably suggest"; three hedges on one claim.
- Why it reads as automatic: hedges pile up to repair an earlier overclaim, not to report real doubt. Better move: one hedge that matches the evidence.
- Leave it alone when: the doubt is the person's own ("I think", "so far"). Never remove a hedge they gave you (NV-T02).

### NV-R05 Filler connectors
**Weak alone.** Seen in: GPT-4 era "Additionally" (2023 to 2024); Gemini 3.1 Pro "furthermore the" 43× and "ultimately this" 78× ([Graphite, Sep 2026][gr-sep]). Wikipedia counts connectors on their own as a poor sign. Credit: [Wikipedia][wp], Ineffective indicators; [writing rules][nv-rules].
- Looks like: "Moreover," "Furthermore," "Additionally," "Ultimately, this..." opening sentence after sentence.
- Why it reads as automatic: it marks a sequence without saying how the ideas connect. Better move: drop it, or use "and", "but", "so" or "also".
- Leave it alone when: it appears once where the link is real, or the person uses it in formal writing.

## Inflation and borrowed authority

### NV-I01 Inflated significance
**Strong alone.** Seen in: ChatGPT and Grok more than Claude and Gemini (Wikipedia, citing Sun et al. 2025); still common in mid-2026, often beside hedges. Credit: [Humanizer][hz] §13; [Wikipedia][wp], Undue emphasis on significance.
- Looks like: "marking a pivotal moment for the team"; "a testament to"; "reflects a broader shift"; "Despite these challenges, the app continues to thrive." "The future looks bright." "sparked wider debate".
- Why it reads as automatic: an ordinary detail is promoted to a turning point. Better move: keep the fact, drop the significance, end on the last concrete fact.
- Leave it alone when: the person states the significance and gives the reason or evidence.

### NV-I02 Shallow -ing riders
**Strong alone.** Seen in: instruction-tuned models use present participle clauses at 2 to 5 times the human rate, GPT-4o at 5.3× ([Reinhart et al. 2025][reinhart]); "highlighting" and "showcasing" in GPT-4o and GPT-5 output (2024 to 2026). Credit: [Humanizer][hz] §15; [Wikipedia][wp], Superficial analyses; [writing rules][nv-rules] ("fake depth").
- Looks like: "..., ensuring a smoother experience." "..., highlighting the importance of trust." "..., reflecting the team's values."
- Why it reads as automatic: an unsupported meaning is bolted onto a plain fact. Better move: state the effect as its own sentence with its evidence, or cut it.
- Leave it alone when: the clause says what actually happened ("We tested it on Tuesday, using the old prototype.").

### NV-I03 Sales words, praise and intensifiers
**Strong alone.** Seen in: all model families; Gemini 3.1 Pro "absolutely essential" 32×, "profound" 25×, "immense" 22×, "incredibly" 18× ([Graphite, Sep 2026][gr-sep]); Claude Opus 5 "is genuinely" and "matters enormously", falling in Opus 5.5 ([Graphite, Oct 2026][gr-oct]). Credit: [Humanizer][hz] §16; [Wikipedia][wp], Promotional language; [writing rules][nv-rules].
- Looks like: seamless, transformative, powerful, groundbreaking, vibrant, nestled, stunning, "unparalleled clarity", "incredibly intuitive".
- Why it reads as automatic: it claims value without evidence. Better move: say what the thing does and what supports that.
- Leave it alone when: it is an accurate technical term ("a powerful magnet"), a quotation, or ad copy in the person's own style.

### NV-I04 Avoiding "is" and "has"
**Weak alone.** Seen in: GPT and Gemini models (Wikipedia, citing Huang et al.); "is" and "are" fell by over 10% in academic writing in 2023 ([Geng and Trotta][geng-copula]). Credit: [Humanizer][hz] §18; [Wikipedia][wp], Avoidance of basic copulatives.
- Looks like: "serves as the main entry point"; "stands as"; "boasts three rooms"; "features a search bar"; "began her career as a nurse" (for "was a nurse").
- Why it reads as automatic: a grander verb where "is" or "has" would do. Better move: use "is", "are" or "has".
- Leave it alone when: the verb adds meaning ("the hall serves as a polling station on election days").

### NV-I05 Vague connection
**Weak alone.** Seen in: one of the most common signs in new Wikipedia drafts (Oct 2026). Credit: [Humanizer][hz] §14; [Wikipedia][wp], Vague expression of connection.
- Looks like: "associated with the redesign"; "involved in connection with the launch"; "linked to the research team".
- Why it reads as automatic: it says two things are connected without saying how, and can hide a role. Better move: name the relationship the source gives ("led the redesign"). If the source doesn't say, keep it vague or ask. Never pick a role.
- Leave it alone when: it is the careful term, as in statistics ("late reminders were associated with more missed returns").

### NV-I06 Borrowed authority
**Strong alone.** Seen in: tools released in 2025 or later often pin claims to named outlets (Wikipedia). Credit: [Humanizer][hz] §17; [Wikipedia][wp], Vague attributions and Canned emphasis on notability; earlier Natural Voice pattern review.
- Looks like: "Experts agree..." "Studies show..." "Industry reports suggest..." a list of outlets that "featured" someone; "maintains an active social media presence".
- Why it reads as automatic: a vague authority stands in for evidence. Better move: name the source and what it said, from the person's material. Otherwise cut it or write `[ADD: source]`.
- Leave it alone when: the person supplied the source and the claim matches it.

### NV-I07 Stock AI and corporate words
**Weak alone.** Seen in: varies by model and era, see "Model word lists by era" below. Credit: [Humanizer][hz] §12; [Wikipedia][wp], AI vocabulary; [Kobak et al. 2025][kobak]; [writing rules][nv-rules].
- Looks like: delve, tapestry, testament, pivotal, underscore, showcase, foster, leverage, utilise, facilitate, harness, streamline, elevate, empower, landscape (as an abstract noun), intricate.
- Why it reads as automatic: one is normal; a cluster reads like a template. The lists go stale quickly, and people now say some of these words too ([Yakura et al.][yakura]). Better move: the plain verb (use, help, build, cut, show).
- Leave it alone when: it is the field's precise term ("utilisation rate", "landscape mode") or the person's own word.

### NV-I08 Nominalisations and long words
**Weak alone.** Seen in: instruction-tuned models use nominalisations at 1.5 to 2 times the human rate ([Reinhart et al. 2025][reinhart]); more long, rare words ([The Economist, Jul 2026][econ], secondary).
- Looks like: "the implementation of the optimisation of the flow"; "provide facilitation of"; "make a decision" for "decide".
- Why it reads as automatic: verbs turned into nouns hide who did what. Better move: use the verb and name the actor.
- Leave it alone when: the noun is a defined term ("a deployment", "an assessment"), or the person writes academic prose this way.

## Formatting by rule

### NV-F01 Markup on autopilot
**Strong alone.** Seen in: Markdown was among the most common signs of new AI text on Wikipedia (Oct 2026); bold-label lists common since 2024. Credit: [Humanizer][hz] §19; [Wikipedia][wp], Use of Markdown and Overuse of boldface; [writing rules][nv-rules] ("decoration").
- Looks like: "**Performance:** Performance improved."; bold scattered inside sentences; asterisks or `##` pasted into an email or a social post; emoji bullets; exclamation marks.
- Why it reads as automatic: decoration on every item, not where the reader needs it. Better move: remove it; turn a labelled list into a sentence when the labels add nothing.
- Leave it alone when: the destination shows Markdown and the structure helps the reader, or the person's samples use it.

### NV-F02 Headings by formula
**Weak alone.** Seen in: all model families. Credit: [Humanizer][hz] §20 and §24; [Wikipedia][wp], Title case and Heading errors.
- Looks like: Title Case On Every Word; emoji or arrows in headings; a rule between every section; a heading echoed by its first line ("Speed" followed by "Speed is everything."); headings written for effect.
- Why it reads as automatic: structure by template. Better move: sentence case (or the person's style), a heading that names what the section holds, then straight into the content.
- Leave it alone when: a house style or format requires it.

### NV-F03 Typography on default settings
**Weak alone.** Seen in: curly quotes from ChatGPT (since mid-2025) and DeepSeek, rarely from Claude or Gemini ([Wikipedia][wp], 2026). Credit: [Wikipedia][wp], Curly quotation marks; [Humanizer][hz] §10 and §21.
- Looks like: curly quotes in a text whose other quotes are straight; a mix of straight and curly apostrophes; "the plan is long-term" (a hyphen kept after the noun).
- Why it reads as automatic: punctuation from a tool's defaults, not the writer's. Better move: match the rest of the person's text and the destination.
- Leave it alone when: the text was typeset or auto-corrected (Word, macOS and iOS curl quotes by default).

## Chat and draft leftovers

### NV-C01 Chat wrapper
**Strong alone.** Seen in: all chat apps. Credit: [Humanizer][hz] §22; [Wikipedia][wp], Collaborative communication; earlier Natural Voice pattern review.
- Looks like: "Certainly! Here's a polished version:" "Great question." "I hope this helps!" "Would you like me to make it shorter?"
- Why it reads as automatic: talk aimed at the user is left inside text meant for the reader. Better move: remove the wrapper and keep the content.
- Leave it alone when: it is the greeting or sign-off of a real letter.

### NV-C02 Tool and citation artefacts
**Strong alone** (shows a tool touched the text, not that it wrote it). Seen in: ChatGPT (`oaicite`, `contentReference`, `turn0search0`, `utm_source=chatgpt.com`); Gemini (`[cite: 1]`, `[span_1](start_span)`); Copilot (`utm_source=copilot.com`); Grok (`grok_card`); Perplexity (`attached_file`) ([Wikipedia][wp], up to Oct 2026). Credit: [Wikipedia][wp], Internal formatting and reference markup bugs.
- Looks like: the codes above; broken citation markers; stray invisible characters.
- Why it reads as automatic: machine markup left in prose. Better move: remove the markup and keep the real link or citation it pointed to. Inspect invisible characters with [text-integrity.md](text-integrity.md) before deleting any.
- Leave it alone when: the person needs the link exactly as it is, or an invisible character has a job (emoji joiners, direction marks).

### NV-C03 Source-gap disclaimers and guesses
**Strong alone.** Seen in: chatbots that search the web, 2024 to 2026; one of the most common Wikipedia signs (Oct 2026). Credit: [Humanizer][hz] §23; [Wikipedia][wp], Hedging disclaimers about source availability.
- Looks like: "While details are limited in available sources..." "not widely documented" "based on available information" "she likely studied design, which shaped..." "keeps a low profile".
- Why it reads as automatic: the model reports on its own search, then fills the gap with a guess. Better move: remove the guess. If something is missing, write `[ADD: ...]` or ask.
- Leave it alone when: the person states the gap themselves ("I couldn't find the original brief.").

### NV-C04 Writing about the document
**Weak alone.** Seen in: model drafts and edit notes, 2025 to 2026. Credit: [Humanizer][hz] §25; [Wikipedia][wp], Edit summaries.
- Looks like: "This section was rewritten to replace..." "The figures below were compiled from..." "Nothing unconfirmed was guessed." "The table below compares..." with the table right there.
- Why it reads as automatic: it describes how the text was made, not its subject. Better move: describe the subject; keep a source credit the reader can follow.
- Leave it alone when: the genre is about change (release notes, change logs), or a caveat changes what the reader should do.

### NV-C05 Template leftovers
**Strong alone.** Seen in: all model families. Credit: [Wikipedia][wp], Phrasal templates and placeholder text.
- Looks like: "[Your name]"; "[Insert metric here]"; "Subject:" at the top of a post; "Option 1:" left from a list of drafts; "2026-XX-XX".
- Why it reads as automatic: the frame of a draft shipped as the text. Better move: fill it from the person's material, or turn it into a visible `[ADD: ...]` gap.
- Leave it alone when: it is Natural Voice's own `[ADD: ...]` marker. Those stay until the person fills them.

## Writing for the wrong reader

### NV-W01 Re-explaining what the reader knows
**Strong alone** when you can see the conversation; otherwise ask. Seen in: replies and messages from all model families (Humanizer 3.1.0, 2026). Credit: [Humanizer][hz] §26; earlier Natural Voice pattern review ("overexplaining obvious steps").
- Looks like: a reply to a colleague that restates the problem, walks through the diagnosis and proves the plan before giving the decision; basics spelled out for an expert reader.
- Why it reads as automatic: the model writes for a reader with no context. Better move: lead with the decision and keep only what this reader lacks.
- Leave it alone when: the reader is new to the topic, or the format (a spec, a handover) needs the full record.

## 2026 model phrasing

These come from 2026 corpus studies of web articles written from one fixed prompt. They will change with the next model version ([Graphite, Oct 2026][gr-oct]). Graphite's own advice is not to judge authorship from single tells.

### NV-M01 Importance flags
**Strong alone.** Seen in: Claude Opus 5.5 "this matters" 116×, "why _ matters" 92×, "just as important" 13×, "matters most" 12× (Oct 2026); "matters because" in Claude Opus 5 (132×) and GPT-6 Astra (357×) (Sep 2026). Credit: [Graphite, Sep 2026][gr-sep]; [Graphite, Oct 2026][gr-oct]; [TechCrunch, Oct 2026][tc]; [Wikipedia][wp].
- Looks like: "This matters." "Why the new filter matters" as a heading. "It matters because people forget." "That distinction matters."
- Why it reads as automatic: it tells the reader something is important instead of showing the consequence. Better move: state the consequence from the person's material ("Without the filter, staff check every row by hand.").
- Leave it alone when: the person says it in their own samples or dictation and the consequence follows straight away.

### NV-M02 "More than X" upgrades
**Strong alone.** Seen in: Claude Opus 5.5 "is more than a _ it" 98× (Oct 2026); Claude Opus 5 "less like a _ and more like" 105× (Sep 2026). Opus 5.5 has largely dropped "it's not X, it's Y" ([TechCrunch, Oct 2026][tc]). Credit: [Graphite, Sep 2026][gr-sep]; [Graphite, Oct 2026][gr-oct].
- Looks like: "The checklist is more than a form, it's a promise." "It feels less like a tool and more like a colleague."
- Why it reads as automatic: the same move as NV-S01 in new clothes. Better move: say what the thing does.
- Leave it alone when: the comparison carries real information ("more than a form: it also books the room").

### NV-M03 Corrective framing
**Strong alone** for the stock forms below. A plain "rather than" is ordinary English. Seen in: GPT-6 Astra "the _ is not simply" 576×, "rather than relying" 187×, "not simply" 157× (Sep 2026); Claude Opus 5 "rather than merely" 160× (Sep 2026); Claude Opus 5.5 "rather than simply" 32× (Oct 2026); "Y rather than X" in Wikipedia drafts from Apr 2026. Credit: [Graphite, Sep 2026][gr-sep]; [Graphite, Oct 2026][gr-oct]; [TechCrunch, Oct 2026][tc]; [Wikipedia][wp], Y rather than X.
- Looks like: "Rather than simply moving fields, we rethought the order." "The tool is not simply a tracker." "It uses saved answers rather than relying on memory."
- Why it reads as automatic: every point is framed as a correction of something nobody proposed. Better move: say what was done and why.
- Leave it alone when: the alternative was really considered, or it is what the reader expects.

### NV-M04 Usage and evidence hedges
**Weak alone.** Seen in: GPT-6 Astra "does not establish" at 275× the Claude Opus 5.5 rate and "not necessarily" at 17× (Oct 2026, compared with Opus 5.5, not with people); Wikipedia drafts from Aug and Oct 2026 (ChatGPT or Claude). Credit: [Graphite, Oct 2026][gr-oct]; [Wikipedia][wp], Hedging disclaimers.
- Looks like: "This does not by itself establish that..." "should be treated as an early signal rather than proof" "not necessarily representative".
- Why it reads as automatic: a reflex caution attached to almost every claim. Better move: state the real limit once, in plain words ("Only two people have tried it.").
- Leave it alone when: the limit is real and came from the person. You may rephrase it plainly; never delete it (NV-T02).

### NV-M05 Soft benefit claims
**Weak alone.** Seen in: GPT-6 Astra "may provide" 36× and "can provide" 23× (compared with Claude Opus 5), "without requiring" 70×, "without losing" 22× (Sep 2026); Claude Opus 5.5 helpfulness phrases ("can help you", "makes it easier", "helps you avoid") up against Opus 5 (Oct 2026). Credit: [Graphite, Sep 2026][gr-sep]; [Graphite, Oct 2026][gr-oct]; [TechCrunch, Oct 2026][tc].
- Looks like: "Reminders may provide more dependable routines." "This can help you avoid missed returns." "...without requiring extra setup."
- Why it reads as automatic: a benefit is promised in hedged form with no evidence. Better move: say what happens and who saw it, or write `[ADD: evidence]`.
- Leave it alone when: it describes a real, sourced capability ("Export works without an account.").

### NV-M06 Look-ahead and layering bridges
**Strong alone.** Seen in: Claude Opus 5.5 "looking ahead, the" 40×, "adds another layer" 27×, "what comes next" 24× (Oct 2026); Claude Opus 5 (Sep 2026); GPT-6 Astra "another dimension" 117×, "together these" 95× (Sep 2026). Credit: [Graphite, Sep 2026][gr-sep]; [Graphite, Oct 2026][gr-oct].
- Looks like: "Looking ahead, the team..." "This adds another layer of trust." "Together, these changes..." "What comes next is..."
- Why it reads as automatic: a stock bridge or send-off. Better move: state the plan or the effect directly.
- Leave it alone when: it is literal ("adds another layer of padding"), or the person uses it.

### NV-M07 Calm evaluative words
**Weak alone.** Seen in: Claude Opus 5.5 "dependable" 23×, "steady" 11×, "thoughtful" 9×, "meaningful" 8×, "in practice" 7× (Oct 2026); GPT-6 Astra "dependable" 59×, "practical" 26× (Sep 2026); Claude Opus 5 "deliberate" 26× (Sep 2026). Credit: [Graphite, Sep 2026][gr-sep]; [Graphite, Oct 2026][gr-oct]; [Wikipedia][wp] (GPT-6 list, unverified).
- Looks like: "a steady, dependable routine"; "a thoughtful, meaningful change"; "a practical, deliberate choice"; "quietly".
- Why it reads as automatic: praise that sounds measured but says nothing anyone could check. Better move: describe the behaviour ("the routine is the same every morning").
- Leave it alone when: the word is literal ("a steady connection"), or it is the person's word.

## Truth risks

This group is about facts. Each pattern is a way a rewrite can change what the person said, which breaks section 1 of [writing-rules.md](../writing-rules.md). Check for every one on every edit, in any model's output and in your own. Credit for the group: Natural Voice writing rules and the no-invention rule in [Humanizer][hz].

### NV-T01 Invented experience
**Truth check.** Looks like: "I still remember the moment..." "My heart sank." A quote nobody said. Fake typos or slang added to look human.
- Fix: remove it. Personality comes only from the person's real words and opinions.

### NV-T02 Claim upgrades and lost hedges
**Truth check.** Looks like: "helped" becomes "ensured"; "some people" becomes "everyone"; "really fast" becomes "within seconds"; "I think it's clearer" becomes "It's clearer"; a real limitation deleted along with a formula.
- Fix: restore the person's strength of claim, word for word where it carries meaning.

### NV-T03 Status drift
**Truth check.** Looks like: "tried it with two people" becomes "validated with users"; "proposed" becomes "introduced"; "prototype" becomes "launched".
- Fix: keep done, shipped, tested, planned and proposed exactly as stated.

### NV-T04 Who did it
**Truth check.** Looks like: "I" becomes "we" or the reverse; "the team decided" when the person decided; a passive that hides the actor ("the flow was redesigned"); a dropped subject ("No setup needed."). Credit also: [Humanizer][hz] §11.
- Fix: keep I and we as said; name the actor when the person named one; ask when unclear.

### NV-T05 Evidence with no source
**Truth check.** Looks like: "users loved it"; "research showed"; a number with no origin; numbers or names copied from a mockup as if they were results.
- Fix: keep only evidence the person gave, with its origin. Placeholder data in a design stays labelled as placeholder. Otherwise write `[ADD: ...]`.

### NV-T06 Meaning lost in a reshape
**Truth check.** Looks like: two facts merged into one; a negation flipped; "must" turned into "should"; a sequence turned into "at the same time"; a quotation tidied; a sentence cut with its fact; a link changed.
- Fix: compare the rewrite with the original claim by claim. Where scripts can run, use `scripts/text_integrity.py compare` with locks for names, numbers and quotes ([text-integrity.md](text-integrity.md)).

## Over-correction guard

A fix can create a new formula. In an Aug 2026 test, a rewrite skill removed AI words (70 sightings down to 0) and typographic tells (60 down to 0). Judges then found more uniform rhythm (60 up to 101) and more aphoristic closers (38 up to 61) ([Humanizer #229][hz-229]; model judges, 77 of 144 planned trials). Run this guard after every rewrite.

| ID | Over-correction | Do this |
|---|---|---|
| NV-G01 | Every sentence short and about the same length, few commas | Vary length the way the person's samples do |
| NV-G02 | New punchlines, sayings or one-line closers added "for voice" | Cut them. Voice comes from the person's own lines |
| NV-G03 | All dashes, semicolons or brackets stripped when the person uses them | Restore their usual rate |
| NV-G04 | Thesaurus swaps ("leverage" to "harness", "robust" to "sturdy" in statistics) | Use the plain word or the person's word; keep technical terms |
| NV-G05 | Needed repetition removed ("the dashboard" becomes "the tool", then "the platform") | One name for one thing; use the person's term |
| NV-G06 | Fake spontaneity: typos, slang, "honestly", invented asides | Remove them (NV-T01) |
| NV-G07 | An overclaim swapped for a pile of hedges, or a real limit deleted | One hedge that matches the evidence; keep the limit |
| NV-G08 | Over-cutting: the rewrite is shorter because facts went missing | Restore every supported claim (NV-T06) |

How to check:

1. Compare with the person's Fingerprint, the measured habits of their own writing (sentence length spread, punctuation per 1,000 words, paragraph length, contractions). If `scripts/voice_stats.py` is available, run it on the rewrite and compare. See [fingerprint.md](fingerprint.md). Without a Fingerprint, put the rewrite next to two of their Examples and read both aloud.
2. Scan the rewrite with this catalogue again. Fixes for NV-S01 often produce NV-S02.
3. If the rewrite is more uniform than the person's own writing, it is wrong, even when every flag is gone.

## Historical (faded) patterns

These were common in older models and are no longer strong evidence of anything. A person's voice file can still ban any of them (for example *My rules*, "Dashes: never"), and then they are always fixed.

### NV-H01 Em-dash overuse (2022 to Sep 2026)
Faded. Claude Opus 5.5 uses 0.015 dashes per 1,000 words, against 2.92 for Opus 5 ([Graphite, Oct 2026][gr-oct]). GPT-6 Astra uses about one-eighth of the human rate and Gemini 3.1 Pro almost none ([Graphite, Sep 2026][gr-sep]). Wikipedia moved dashes to its historical signs on 7 Oct 2026. Earlier, The Economist found only Claude above professional writers (Jul 2026, secondary).
- Looked like: spaced dashes (— or –) joining clauses where a comma, colon or full stop fits; paired dashes in every paragraph.
- Now: follow *My rules* (Dashes: use freely, sparingly or never). Under "never", replace each dash in the person's prose with a comma, colon, full stop or brackets, and write ranges as "9 to 5". Keep hyphens, dashes in code and web addresses, and dashes inside exact quotations (truth wins).

### NV-H02 "It's important to note" (Nov 2022 to 2024)
Faded. Didactic asides: "it's worth noting", "it's crucial to remember", "results may vary" ([Wikipedia][wp], Historical indicators). In 2026 the same reflex shows up as NV-M04.

### NV-H03 Knowledge-cutoff and refusal talk (2022 to 2024)
Faded. "As of my last update..." "As an AI language model, I can't..." ([Wikipedia][wp]). If it appears, treat it as chat residue (NV-C01).

### NV-H04 "Delve" era words (2023 to mid-2024)
Faded. Delve, tapestry, testament, intricate. "Delve" fell sharply soon after it was publicly flagged in early 2024 ([Geng and Trotta 2025][geng]); The Economist reports that models no longer overuse it (Jul 2026, secondary). Still worth fixing in clusters (NV-I07).

### NV-H05 Section summaries (2023 to 2024)
Faded. "In summary", "In conclusion", "Overall", and closing paragraphs that restate the section ([Wikipedia][wp]). The send-off survives as NV-I01 and NV-S02.

### NV-H06 Elegant variation (older models)
Faded. Renaming one thing again and again to avoid repeating a word ("the app", "the platform", "the solution"), linked to repetition penalties in older models ([Wikipedia][wp]). Many people are taught to write this way at school, so it is weak evidence. Over-correcting into it is NV-G05.

## Model word lists by era

Use these only to spot clusters (NV-I07, NV-M07). Never flag a single word. A voice file's *Words I never want* always wins, and so does a word the person uses in their samples.

| Era and model | Words and phrases | Confidence | Source |
|---|---|---|---|
| 2023 to mid-2024, GPT-4 | additionally, boasts, bolstered, crucial, delve, emphasizing, enduring, garner, intricate, interplay, key, landscape, meticulously, pivotal, underscore, tapestry, testament, valuable, vibrant | Verified | [Wikipedia][wp] era list, backed by [Kobak et al. 2025][kobak] and [Juzek and Ward 2025][juzek] |
| Mid-2024 to mid-2025, GPT-4o | align with, bolstered, crucial, emphasizing, enhance, enduring, fostering, highlighting, pivotal, showcasing, underscore, vibrant | Secondary | [Wikipedia][wp] era list |
| Mid-2025 to mid-2026, GPT-5 | emphasizing, enhance, highlighting, showcasing, plus canned notability wording (NV-I06) | Secondary | [Wikipedia][wp] era list |
| Mid-2026 on, GPT-6 | challenge, clearer, dependable, echoed, foster, leverage, matters, multifaceted, practical, prioritize, quietly, steady, universally; short sentences of 8 to 20 words | Unverified: one review site (10 Sep 2026), listed by Wikipedia on 7 Oct 2026. "Dependable" and "practical" also appear in Graphite's data | [Wikipedia][wp] |
| Sep 2026, GPT-6 Astra | the _ is not simply 576×, matters because 357×, rather than relying 187×, not simply 157×, another dimension 117×, together these 95×, without requiring 70×, dependable 59×, practical 26×, meaningful 13× | Secondary: one corpus study by a marketing firm, not peer reviewed | [Graphite, Sep 2026][gr-sep] |
| Sep 2026, Claude Opus 5 | rather than merely 160×, matters because 132×, less like a _ and more like 105×, rather than simply 43×, looking ahead the 33×, what comes next 28×, deliberate 26×, steady 6× | Secondary | [Graphite, Sep 2026][gr-sep] |
| Oct 2026, Claude Opus 5.5 | this matters 116×, is more than a _ it 98×, why _ matters 92×, looking ahead the 40×, rather than simply 32×, adds another layer 27×, what comes next 24×, dependable 23×, steady 11×, thoughtful 9×, meaningful 8×, in practice 7× | Secondary | [Graphite, Oct 2026][gr-oct]; [TechCrunch][tc] |
| Sep 2026, Gemini 3.1 Pro | is not just a _ it is 153×, ultimately this 78×, furthermore the 43×, absolutely essential 32×, profound 25×, immense 22×, remarkably 19×, incredibly 18× | Secondary | [Graphite, Sep 2026][gr-sep] |
| 2026, Grok | causal, empirical, correlate, underscore | Unverified (no study cited) | [Wikipedia][wp] |

What the research says about these lists:

- Graphite compares each model with pre-2022 web articles written from the same summaries. Its ratios depend on that corpus and one prompt. Tells move between model versions but don't disappear ([Graphite, Oct 2026][gr-oct]).
- Each model has its own style, and the 2026 models write differently from the 2024 ones ([Rudnicka and Juzek, Aug 2026][rudnicka]).
- Words fade once they are publicly flagged ([Geng and Trotta 2025][geng]), and people pick up model-favoured words in their own speech ([Yakura et al.][yakura]). Both make word lists a poor test of authorship.
- Instruction-tuned models also differ in grammar, not only words: more present participle clauses and nominalisations ([Reinhart et al. 2025][reinhart]). See NV-I02 and NV-I08.

---

Last reviewed: 2026-10-08. Humanizer version folded in: 3.1.0. The monthly maintainer refresh (`/refresh-research` in the project repository, sources in `research/sources.md`) updates this file, including the word lists, ratios and dates.

[hz]: https://github.com/blader/humanizer
[hz-229]: https://github.com/blader/humanizer/issues/229
[wp]: https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
[gr-sep]: https://graphite.io/five-percent/research/ai-tells
[gr-oct]: https://graphite.io/five-percent/research/ai-tells-opus-5-5-update
[tc]: https://techcrunch.com/2026/10/01/opus-5-5-loves-to-tell-you-this-matters-and-other-ai-writing-tells/
[econ]: https://www.economist.com/culture/2026/07/30/how-to-spot-ai-writing
[reinhart]: https://doi.org/10.1073/pnas.2422455122
[kobak]: https://www.science.org/doi/10.1126/sciadv.adt3813
[juzek]: https://aclanthology.org/2025.coling-main.426/
[geng]: https://aclanthology.org/2025.findings-acl.657/
[geng-copula]: https://arxiv.org/abs/2404.08627
[yakura]: https://arxiv.org/abs/2409.01754
[rudnicka]: https://arxiv.org/abs/2608.06589
[nv-rules]: ../writing-rules.md
