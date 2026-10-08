# Fixture: dashes when the voice file bans them

- **Tests:** NV-H01 under a voice file that bans dashes. Same input as `dash-voice-allowed.md`; only the voice-file rule differs. It also tests that a truth rule (exact quotations) beats a style rule.
- **Voice file excerpt (made up):** *My rules:* Dashes: never.
- **Expected flags:**
  - NV-H01, always fixed: every em dash (—) and en dash (–) in the person's own prose.
  - The range "9–5" becomes "9 to 5". Don't add "am" or "pm"; they aren't in the source.
- **Must not change:**
  - The quotation, including its dash: "It's quicker — but I miss the chat." It is someone else's exact words, so the truth rule wins over the style rule. Tell the person in one line and offer to paraphrase it without quote marks instead.
  - Hyphens in "sign-up" and in "library-hours.example.org" (hyphens are not dashes)
  - The facts: weekdays; bank holidays now included; the form cut the queue at the front desk; the review is in the spring, probably March
- **Pass if:** no em or en dash remains outside the quotation, the quotation is untouched, and the meaning is unchanged.
- **Fail if:** a dash remains in the person's prose, the quotation is edited without asking (NV-T06), or a hyphen is removed.

## Input

```text
The reading room is open 9–5 on weekdays — and yes, that now includes bank holidays. The new sign-up form — the one with the big green button — has cut the queue at the front desk. One volunteer put it this way: "It's quicker — but I miss the chat." We'll review the hours in the spring – probably in March. Details are at library-hours.example.org.
```

## One acceptable result

```text
The reading room is open 9 to 5 on weekdays, and yes, that now includes bank holidays. The new sign-up form (the one with the big green button) has cut the queue at the front desk. One volunteer put it this way: "It's quicker — but I miss the chat." We'll review the hours in the spring, probably in March. Details are at library-hours.example.org.
```

Note to the person, one line: "I kept the dash inside the volunteer's quote because it's their exact words. Want me to paraphrase it instead?"
