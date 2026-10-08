---
title: Notes on the clinic booking redesign
---

# What I learned redesigning clinic bookings

I'll be honest: I didn't want this project at first. Booking flows feel solved — you pick a time, you pay, you're done. But the clinic's numbers told a different story, and I couldn't ignore them.

Half the people who started a booking never finished it. That's not a small leak. It's the whole bucket.

## Where it went wrong

I sat with the front-desk team for two mornings. They kept a paper list of "people who rang because the app confused them", and it was long. Most calls were about the same thing: the colour-coded calendar. Green meant free, amber meant "ask us", and grey meant gone — except nobody knew what amber meant, including me.

> The calendar is the worst bit. I just phone them now.
> (one patient, in a survey)

So I stripped it back. I don't think a calendar needs three states. It needs two, and a clear way to ask for help.

```js
// Code is not prose, so the profile leaves it out.
const slots = getSlots({ clinic: "north", days: 14 });
```

## What we changed

- One list of times, earliest first.
- A plain "Can't see a time that works?" link under the list.
- No colours that need a legend.

I tested the new flow with eight patients in the waiting room. Six finished a booking without help; two asked where to put their insurance number, which I'd hidden behind a toggle. Fair enough. I moved it.

Did it work? Mostly. Calls about the calendar dropped in the first month, though I can't say by how much yet because the front desk stopped keeping the list (they were, understandably, quite pleased to stop). I'm going to ask them to keep it for another fortnight so I've got something better than a feeling.

There's a version of this story where I tell you the redesign doubled bookings. It didn't, or at least I can't show that it did. What it did was make the flow honest about what it couldn't do — and give people a way out when it failed them.

If I did it again, I'd start with the phone calls rather than the screens. The calls were the research; I just didn't know it. See https://example.com/notes for the raw notes, or read the [summary](https://example.com/summary).
