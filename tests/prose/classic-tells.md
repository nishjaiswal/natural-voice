# Fixture: classic tells (2023 to 2025)

- **Tests:** the older, well-known patterns, plus chat leftovers and tool artefacts. It also tests that a real list of three is kept and that no number is invented.
- **Voice file:** none. Use the general rules.
- **Expected flags:**
  - NV-C01: "Great question! Here's a polished version...", "I hope this helps!", "Let me know if you'd like..."
  - NV-F02: emoji and Title Case in the heading
  - NV-S04: "In today's fast-paced world", "Let's dive in."
  - NV-S01: "isn't just a catalogue, it's a gateway"
  - NV-R05: "Moreover,"
  - NV-I07 (cluster): "leverages", "empower", "fostering"
  - NV-I03: "seamless", "vibrant"
  - NV-I01: "marked a pivotal moment", "a testament to"
  - NV-I02: ", showcasing our commitment to..."
  - NV-R01: "innovation, accessibility, and excellence"
  - NV-I06: "Experts agree that..."
  - NV-F01: bold labels that repeat their sentence
  - NV-H05: "In conclusion,"
  - NV-C02: `utm_source=chatgpt.com` and the `oaicite` marker
  - NV-H01: the dash is historical. With no voice-file rule it is not a reason to edit on its own; it goes when the NV-S01 sentence is rewritten.
- **Must not change:** "launch in March"; "two taps"; "three branches: North, Riverside and Old Town" (a real list of three, so NV-R01 must not fire here); "Search is faster than before" stays a comparison with no number (adding one fails NV-T02); the link still points to `https://example.org/launch` (dropping the tracking parameter is fine).
- **Pass if:** the wrapper and artefacts are gone, every fact is kept, "Experts agree" is cut or becomes `[ADD: source]`, and nothing new is claimed.

## Input

```text
Great question! Here's a polished version of your update:

## 🚀 Transforming The Borrowing Experience

In today's fast-paced world, libraries must evolve. Let's dive in. Our new app isn't just a catalogue — it's a gateway to discovery. Moreover, it leverages a seamless interface to empower members, fostering a vibrant community of readers. The launch in March marked a pivotal moment for the service, showcasing our commitment to innovation, accessibility, and excellence. Experts agree that digital tools are crucial for modern libraries.

- **Search:** Search is faster than before.
- **Holds:** Holds can be placed in two taps.
- **Branches:** The app works at three branches: North, Riverside and Old Town.

In conclusion, the app is a testament to what a dedicated team can achieve. I hope this helps! Let me know if you'd like a shorter version. [Source](https://example.org/launch?utm_source=chatgpt.com) :contentReference[oaicite:2]{index=2}
```

## One acceptable result

```text
## Our new app

It launched in March. Search is faster than before, holds take two taps, and the app works at three branches: North, Riverside and Old Town. [Source](https://example.org/launch)
```
