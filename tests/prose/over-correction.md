# Fixture: over-correction

- **Tests:** the over-correction guard (NV-G01 to NV-G08). The input is a rewrite that removed the old tells and replaced them with new formulas. The reviewer must catch it and send the text back towards the person's draft.
- **Voice file excerpt (made up):**
  - *My rules:* Dashes: sparingly (their samples use about one spaced dash per 120 words).
  - *My terms:* "booking page" (never "reservation screen").
  - *Fingerprint (illustrative values):* sentence length 7 to 34 words, median 18; no one-line paragraphs; no sayings or slogans in any sample.
- **Expected flags on the input:**
  - NV-G01: ten sentences of 2 to 8 words, against a median of 18
  - NV-G02, NV-S02, NV-S03: "Clarity builds trust." "Price first, always." "That's the real lesson."
  - NV-G04 and NV-G05: "booking page" became "page" and then "reservation screen", against *My terms*
  - NV-G08 and NV-T06: the return date and the late fee were dropped; "before it showed the price" was lost
  - NV-T02: "always" was added; "a card number" became "card details"
  - NV-G03 (minor): the one dash went. At this length either choice fits their rate, so this alone is not a fail.
- **Must not change (from the person's draft):** "booking page"; "card number"; the price used to come after the card number; "so many people left at that step"; "session recordings"; "support inbox"; "we"; the card field stayed where it was; the booking page now shows the total, the return date and the late fee first.
- **Pass if:** the reviewer rejects the input and returns something close to the person's draft, with varied sentence length and every fact restored.

## The person's draft (reference only)

```text
The old booking page asked for a card number before it showed the price, which is why so many people left at that step — we saw it in the session recordings and again in the support inbox. We moved the price to the top of the booking page and left the card field where it was. Now the booking page shows the total, the return date and the late fee before anything else.
```

## Input (the over-edited rewrite to review)

```text
The old page asked for card details first. People left. We saw it in recordings. We saw it in support emails. So we moved the price up. The card field stayed put. Now the reservation screen shows the total first. Clarity builds trust. Price first, always. That's the real lesson.
```
