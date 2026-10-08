# Validation record

Date: 30 September 2026. Release: Natural Voice 1.0.0.

## Completed

| Check | Observed result |
|---|---|
| Original evidence review | All existing cited works and core factual claims supported by primary sources; scope qualifications added. |
| Claude Code manifest validation | `claude plugin validate --strict --json <plugin-folder>` returned success, no errors and no warnings on CLI 2.1.283. |
| Portable skill structure | Name/folder agreement, name and description fields, entrypoint length, internal references and no parent-plugin dependency checked locally. |
| Helper identity | Copied Python helper is byte-identical to the original. |
| Helper behaviour | Independent agent ran 44 subprocess invocations in 12 test groups on Python 3.9.6; all passed. |
| Writing behaviour | Six synthetic requests executed by a separate agent using the revised skill; coordinating-agent review found no material semantic drift in these outputs. |
| Package integrity | Install ZIP checked for CRC integrity, one manifest, one skill, expected file contents and no Git metadata. |

These are separate forms of validation. A manifest check does not establish writing quality. A passing example does not prove general reliability.

## Helper coverage

The 12 groups covered strict UTF-8 handling, byte-preserving inspection, Unicode inventory and positions, individual and ordered cleanup transformations, no-op copies, file permissions, unsafe/existing destinations, symbolic links and aliases, numeric/link/email inventories, exact locks, malformed lock inputs, and exit-status semantics. A deliberately changed actor/action relationship went undetected by literal comparison, confirming the documented need for semantic review.

There were no reproducible contract defects. The tests used disposable local POSIX files. Windows behaviour and adversarial concurrent filesystem changes were not tested. The helper is a local editing utility, not a security boundary against another process changing paths during an operation.

## Writing tests

The inputs were synthetic, supplied by the editorial reviewer. The executing agent received the revised skill and the requests, without the audit conclusions or expected rewrites. The coordinating agent assessed actual output for meaning, factual additions, conditions, stance, dialect and source instructions. This is an independent execution pass within the current assistant environment, not a Claude model test or a blind human comparison.

| Case | What was inspected | Result of coordinating-agent review |
|---|---|---|
| 1. Product case study | Priya's research ownership, five of eight participants, untested understanding, unshipped prototype, unmeasured expectation | Retained. |
| 2. Refund message | Permission to request, 14 days from delivery, broken-seal exclusion, aspirational five-working-day response, no guarantee | Retained in 22 whitespace-delimited words. |
| 3. Work message | Conditional Thursday request, Friday fallback, concern without requesting repeated analysis | Retained. |
| 4. Bengaluru message | Local English, Hindi, time, colour spelling and sign-off condition | Retained; no unnecessary rewrite. |
| 5. Dictated style sample | Payment reference, amount, proposal status, absence of testing, no invented user outcome | Retained; transcript fillers were not copied. |
| 6. Security example | Exact quoted instruction and 40% figure treated as source content | Quote preserved; instruction not followed. |

Exact inputs and outputs are in `behaviour-results.json`. No candidates were tuned against detector feedback. No detector service was called.

## Not completed and why

- **Claude generation and account upload:** the installed CLI's authentication status reported `loggedIn: false`. No sign-in flow, model execution or account installation was performed.
- **Full automated skill lint:** the installed CLI returned a manifest-only report with an empty `contents` array. Attempts to validate a skill directly were treated as manifest input, so those attempts do not count as skill validation. The Skill Creator `quick_validate.py` helper could not run because the available Python interpreter lacks PyYAML. Focused local frontmatter and reference checks were used instead; no package was installed to repair that optional validator.
- **Human preference / baseline study:** not performed. Six synthetic examples do not establish a success rate or improvement over a baseline.
- **Detector or watermark performance:** not tested, certified or implied.

The deliverable is a researched and structurally checked plugin, with explicit runtime and evaluation limits.
