# Fixture: 2026 Claude Opus 5.5 style

- **Tests:** the 2026 model phrasing measured for Claude Opus 5.5 (Graphite, Oct 2026): importance flags, "more than X" upgrades, corrective framing, look-ahead bridges and calm evaluative words.
- **Voice file:** none. Use the general rules. Spelling: British English (last-resort default).
- **Expected flags:**
  - NV-M01: "Why the new check-in flow matters", "This matters."
  - NV-M02: "is more than a form, it is..."
  - NV-M03: "Rather than simply moving fields around"
  - NV-M06: "adds another layer", "Looking ahead", "what comes next"
  - NV-M07 (cluster): "steady", "dependable", "In practice", "thoughtful", "meaningful"
  - NV-S03: "the first promise the library makes to a visitor"
- **Must not change:** "we" did the rebuild; the order of the screens changed; visitors see their return date before they confirm; the testing is planned ("will test"), with volunteers, at two branches; which branch goes first is still open.
- **Pass if:** every fact above survives, nothing is added, and the over-correction guard stays quiet (no new one-line closers, no run of same-length sentences).

## Input

```text
Why the new check-in flow matters

This matters. The check-in flow is more than a form, it is the first promise the library makes to a visitor. Rather than simply moving fields around, we rebuilt the order of the screens so staff can follow a steady, dependable routine. In practice, the change adds another layer of trust: visitors now see their return date before they confirm. Looking ahead, the team will test the flow with volunteers at two branches, and what comes next is a thoughtful, meaningful conversation about which branch goes first.
```

## One acceptable result

Not the only good answer. It shows the facts kept and the phrasing gone.

```text
The new check-in flow

We rebuilt the order of the check-in screens so staff can follow one routine. Visitors now see their return date before they confirm. Next, the team will test the flow with volunteers at two branches, then talk about which branch goes first.
```
