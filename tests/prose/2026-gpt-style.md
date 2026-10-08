# Fixture: 2026 GPT-6 style

- **Tests:** the 2026 phrasing measured for GPT-6 Astra (Graphite, Sep and Oct 2026): corrective framing, soft benefit claims, usage hedges, layering bridges, and short sentences of similar length. It also tests that a real limitation survives when its formula is removed.
- **Voice file:** none. Use the general rules.
- **Expected flags:**
  - NV-M03: "is not simply a toggle", "rather than relying on memory", "early signals rather than proof"
  - NV-M05: "may provide", "without requiring extra effort"
  - NV-M06: "Together, these choices", "another dimension"
  - NV-M07 (cluster): "practical", "dependable"
  - NV-M01: "The design matters because"
  - NV-M04: "does not establish", "should be treated as"
  - NV-R02: eight sentences of 6 to 15 words, nearly all the same shape
- **Must not change:** "We ran"; "two-week pilot"; "12 members"; the limitation that the pilot doesn't show whether reminders change behaviour (rephrasing is fine, deleting it fails NV-T02); the results stay uncertain ("early signals"); no claim that reminders work.
- **Pass if:** the limitation is still there in plain words, no benefit is upgraded, no new number appears, and sentence length varies.

## Input

```text
The reminder setting is not simply a toggle. It gives members a practical way to plan their week rather than relying on memory. Together, these choices add another dimension to the app. Weekly reminders may provide more dependable routines without requiring extra effort. The design matters because people forget. We ran a two-week pilot with 12 members. The pilot does not establish that reminders change behaviour. Its results should be treated as early signals rather than proof.
```

## One acceptable result

Not the only good answer. "Not proof" stays because a reader could easily take a pilot as proof, so that contrast carries information.

```text
Members can switch on a weekly reminder to plan their week, because people forget. We ran a two-week pilot with 12 members. It didn't show whether reminders change what people do, so the results are early signals, not proof.
```

## Fails

- "The pilot showed reminders build better habits." (NV-T02, NV-T03)
- Dropping the limitation sentence entirely. (NV-T02, NV-G07)
- "We're confident reminders work for most members." (NV-T02, NV-T05)
