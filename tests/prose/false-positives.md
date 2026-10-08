# Fixture: false positives (leave it alone)

- **Tests:** human writing that uses flagged-looking words and shapes correctly. Nothing here should change.
- **Voice file excerpt (made up):** *My rules:* Dashes: sparingly. *My terms:* "the dashboard" (always this name). *Learned:* "robust is fine in statistics".
- **Sightings that must be left alone, and why:**
  - "robust to removing...", "robust standard errors": statistical terms (NV-I03 and NV-I07 leave-alone; NV-G04 if swapped).
  - The one dash: allowed by the voice file, and one dash is no evidence of anything (NV-H01).
  - "were associated with": the careful statistical wording (NV-I05 leave-alone).
  - "assumed the export button saves a file. It doesn't.": corrects a belief the readers really hold (NV-S01 leave-alone).
  - "the dashboard" three times: needed repetition and the person's term (NV-G05 if renamed).
  - "can't tell us why": a real limitation in plain words (NV-M04 leave-alone; deleting it fails NV-T02).
- **Expected flags to act on:** none. The weak-alone sightings above don't form a cluster.
- **Must not change:** the whole text, including "twice", "May", "September", "14 responses", "30 days".
- **Pass if:** the text comes back unchanged, or with a one-line note that nothing needs fixing. Any edit is a fail.

## Input

```text
We ran the members survey twice, in May and in September. The drop in completion held up — it was robust to removing the 14 responses we'd marked as duplicates, and to using robust standard errors. Late reminders were associated with more missed returns, but the survey can't tell us why.

A lot of people on the team assumed the export button saves a file. It doesn't. It copies a link to the dashboard, and the dashboard only shows the last 30 days. If you need older data, ask before you open the dashboard.
```
