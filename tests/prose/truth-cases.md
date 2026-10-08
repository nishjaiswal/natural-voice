# Fixture: truth cases

- **Tests:** the truth rules under a style edit. The input has two style tells, so a rewrite will happen, and five kinds of fact a rewrite tends to damage: numbers, test status ("tested with two people" against "shipped"), I against we, an "I think" hedge, and placeholder numbers from a mockup.
- **Voice file:** none. Use the general rules.
- **Expected flags:**
  - NV-M02: "This is more than a facelift, it's a new foundation."
  - NV-R04: "could potentially change"
- **Must be preserved exactly:**
  - "I think" (the hedge on "clearer")
  - "I've only tested it with two people", "both from our team" (status: tested by two people, not validated; "I" did the testing)
  - "We shipped", "the first half", "the welcome screen and the sign-in step", "14 August" (status: shipped; "we" shipped it)
  - "still a prototype" (status of the second half). "Could potentially change" may become "may change", but the uncertainty stays.
  - "1,284 active members" and "£4.99 a month" stay labelled as placeholder numbers typed into the design file, not real figures (NV-T05)
  - "61%", "74%", "two weeks", "according to our analytics" (the origin of the numbers)
- **Fails if the rewrite:**
  - says users found it clearer, or drops "I think" (NV-T02)
  - says "tested with users", "validated" or "proven" (NV-T03)
  - says "I shipped" or "we tested" (NV-T04)
  - presents 1,284 members or £4.99 as real (NV-T05)
  - adds any new number, including one worked out from these (for example a percentage-point or percentage change)
  - says the second half has shipped (NV-T03)
- **Pass if:** both tells are gone and every item above is intact.

## Input

```text
This is more than a facelift, it's a new foundation. I think the new onboarding is clearer, but I've only tested it with two people so far, both from our team. We shipped the first half (the welcome screen and the sign-in step) on 14 August. The second half is still a prototype and could potentially change. In the mockup, the dashboard shows "1,284 active members" and "£4.99 a month", but those are placeholder numbers I typed into the design file, not real figures. Completion went from 61% to 74% in the two weeks after the welcome screen went live, according to our analytics.
```

## Lock file for the integrity helper

Save as `locks.json`, save the input and the rewrite as plain text files, then run this from the skill folder:

`python3 scripts/text_integrity.py compare original.txt rewrite.txt --locks locks.json`

A plain string must appear as many times in the rewrite as in the original. A `count` of 0 means the phrase must not appear.

```json
{
  "exact_strings": [
    "I think",
    "two people",
    "both from our team",
    "We shipped",
    "14 August",
    "still a prototype",
    "placeholder",
    "1,284",
    "£4.99",
    "61%",
    "74%",
    "two weeks",
    "according to our analytics",
    {"text": "validated", "count": 0},
    {"text": "users found", "count": 0},
    {"text": "I shipped", "count": 0},
    {"text": "we tested", "count": 0}
  ]
}
```

The locks catch changed literals only. They can't catch a changed meaning, such as the second half described as live, so read the rewrite too.

## One acceptable result

```text
I think the new onboarding is clearer, but I've only tested it with two people so far, both from our team. We shipped the first half (the welcome screen and the sign-in step) on 14 August. The second half is still a prototype and may change. In the mockup, the dashboard shows "1,284 active members" and "£4.99 a month", but those are placeholder numbers I typed into the design file, not real figures. Completion went from 61% to 74% in the two weeks after the welcome screen went live, according to our analytics.
```
