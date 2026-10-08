# Evaluate writing and detector claims separately

This protocol supports an honest comparison. It does not make a universal non-detection claim testable.

## Small practical test

1. Define the brief and protect critical claims, labels, numbers, and sources.
2. Save the original. Produce a revision using the skill and save it before viewing detector results. Record the editing model, the Natural Voice version (from `metadata.version` in `SKILL.md`), the date, and any unknowns.
3. Compare source and revision for meaning. Record substantive omissions and unsupported additions. An attractive detector result cannot override a factual error.
4. If detector testing is requested and authorised, use the exact saved texts on the named service. Keep content type and input method consistent. Do not submit unrelated personal material, buy credits, or register accounts merely because testing is useful.
5. Record the vendor's exact metric definition, displayed value, date, version if exposed, and any limitations or minimum-length requirements. Save evidence of a completed result.
6. Distinguish stale results from a fresh scan. Some interfaces leave the previous percentage visible after the text changes. A sign-in prompt, loading failure, or quota message is not a result for the new text.
7. Report all tested candidates and failures. If revising after a score, label that candidate as tuned using feedback; it is no longer an untouched test. Use separate held-out material to assess generalisation.

A single pair is an illustrative case, not a pass rate. An agent-written "human control" is not a human control. A user-supplied AI-edited passage is not a sample of unassisted voice.

## A stronger benchmark

Use licensed/public or expressly authorised texts. Keep genuine unassisted human writing, raw AI output, AI-edited human writing, and AI-edited AI writing in separate categories. Record uncertain origin as unknown. Include the actual target genres and languages, more than one length range, multiple independent documents, and relevant generator families.

Separate development and held-out evaluation by source document and author where practical. Keep all variants of one source in the same partition. Freeze the skill and any decision thresholds before evaluation. Distinguish detector performance at its default threshold from any calibrated research setting.

Judge factual fidelity, task completion, voice, clarity, and formatting separately from detector outcomes. Blind and randomise text order for independent readers where feasible. Use a declared rubric rather than "looks human". Model judges are fallible reviewers, not replacements for human preference evidence.

Report counts and denominators, detection rates at the declared threshold, human false-positive rates, uncertainty intervals where sample size permits, and results by important subgroup. Correlated rewrites of one paragraph are not independent samples. A service's 100% estimated-text metric is not a binary certainty and cannot be averaged with another vendor's probability metric.

Distinguish published research results from results reproduced with this skill. The project's `research/` folder records which tests were run for each release. Do not claim market-leading performance without a suitable controlled comparison.

## Reusable result record

```json
{
  "case_id": "example-01",
  "origin": "user-supplied; prior process unknown",
  "input_sha256": "fill from actual input",
  "candidate_sha256": "fill from actual output",
  "skill_hash": "fill from frozen package",
  "editing_model": "record actual model or unknown",
  "edited_before_scoring": true,
  "fidelity_review": "record observed issues and resolutions",
  "detector": "named service and interface",
  "detector_version": null,
  "observed_at": "actual timestamp",
  "metric": "vendor field or exact displayed meaning",
  "original_value": null,
  "candidate_value": null,
  "status": "not_run",
  "limitations": []
}
```

`null` means unknown or unmeasured; never substitute zero. Keep the source text outside a shared report or distributable skill when it is private.
