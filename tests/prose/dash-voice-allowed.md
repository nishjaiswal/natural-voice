# Fixture: dashes when the voice file allows them

- **Tests:** NV-H01 under a voice file that allows dashes. Same input as `dash-voice-banned.md`; only the voice-file rule differs.
- **Voice file excerpt (made up):** *My rules:* Dashes: sparingly. Their samples use about one spaced em dash per 100 words, usually for an aside.
- **Expected flags:**
  - NV-H01 is not a tell on its own here. Flag only the excess: the person's own prose (not counting the range and the quotation) uses dashes three times (a pair around an aside counts once), against their rate of about once for a passage this long.
  - Consistency: "the spring – probably in March" uses a spaced en dash as a dash. Change it to their usual form, or to a comma.
- **Must not change:**
  - The quotation, including its dash: "It's quicker — but I miss the chat." (someone else's exact words)
  - The range "9–5" (a range, not a dash habit)
  - Hyphens in "sign-up" and in "library-hours.example.org"
  - The facts: weekdays; bank holidays now included; the form cut the queue at the front desk; the review is in the spring, probably March
- **Pass if:** one dash, or one pair around an aside, remains in the person's own prose (which one is a judgement call; the paired aside is the most like their samples), and everything above is unchanged.
- **Fail if:** every dash is removed (NV-G03), or the quotation is edited (NV-T06).

## Input

```text
The reading room is open 9–5 on weekdays — and yes, that now includes bank holidays. The new sign-up form — the one with the big green button — has cut the queue at the front desk. One volunteer put it this way: "It's quicker — but I miss the chat." We'll review the hours in the spring – probably in March. Details are at library-hours.example.org.
```

## One acceptable result

```text
The reading room is open 9–5 on weekdays, and yes, that now includes bank holidays. The new sign-up form — the one with the big green button — has cut the queue at the front desk. One volunteer put it this way: "It's quicker — but I miss the chat." We'll review the hours in the spring, probably in March. Details are at library-hours.example.org.
```
