# Evidence for Guided Coding

Guided Coding is based on a simple idea: use the checking steps that actually help, and make them part of an easy
procedure. We tested several ways of working with Claude Code to see which steps reduced errors in finished code.

## What we tested

We repeated 37 earlier bug-fixing tasks from the PHENIX and cctbx scientific software projects. We asked Claude Code to do
them with different checking steps, then examined the resulting code for errors. Some follow-up tests used 18
selected harder tasks from that set.

## What helped

| Checking step | What we found |
| --- | --- |
| **Review the code once after the fix** | Across all 37 tasks, missed program errors fell from 0.81 to 0.47 per job when one review was added to plain Claude Code. This was the clearest result. |
| **Ask a different AI assistant for a second opinion on hard work** | When added to Guided Coding on 18 harder tasks (38 runs), an outside review reduced major errors left per run from 1.00 to 0.83. The net gain came from four tasks, and some reviews introduced errors. When added to ordinary Claude Code with one review, the change from 0.85 to 0.76 was not a clear benefit. |
| **Test the problem before and after fixing it** | Requiring such a test made it more likely that a job ended with one. We did not measure how much this step alone reduced errors. |

Additional review steps did not consistently improve the result. In particular, a second ordinary review showed no
clear additional benefit over one review.

## What happened when we replayed Guided Coding itself?

We also replayed an earlier version of Guided Coding (1.3) on the 18 harder tasks, in 38 runs. It left 0.97 major
errors per run, compared with 0.79 for Claude Code with one review and 0.90 for plain Claude Code. Counting outside reviews that Guided Coding
requested in four runs, its figure was 0.90. By the rule chosen before testing, the difference was not clear,
although the result leaned against Guided Coding.

Many of these errors had been identified but left as questions for the person using the software. A strict rule
about staying within the exact request had reversed some fixes found during review. Of the 33 major errors left,
18 had been raised at least partly as questions, compared with 1 of 29 for Claude Code with one review. If the
suggested fixes had been accepted and worked, the estimated rate would have been 0.74, about the same as Claude Code with one review. That estimate was not
tested.

The rule was then narrowed: Guided Coding now fixes real defects in code it changes, while still asking before
changing interfaces, defaults, file formats, or behaviour other code relies on. The updated instructions were
checked in a small trial and targeted behaviour tests. Those checks are not another comparative replay; details
are in the technical evidence record linked below.

## How this shaped Guided Coding

Guided Coding asks Claude to test a fix, review it once, and explain what remains uncertain. It asks for an outside
review when a change is hard to check or could have important consequences. It leaves the final decision with you.
That is the practical procedure built from the study.

Some other steps, such as asking permission before publishing and writing a clear final report, are there for
control and understanding. Their separate effect on errors was not measured.

## How much can we conclude?

The study used a limited set of tasks from one developer's projects. The harder tasks were selected because they
had exposed problems before; they were not a random sample. Results can differ with other code, models, and
developers. Even a good review can miss an error or introduce one.

A more elaborate earlier procedure caught additional serious errors on some harder tasks, but required much more
work. We do not know which of its many extra steps were responsible. These are useful limits on how to interpret
the results.

## Full results

You can read the [complete study report](https://www.thomasterwilliger.org/guided_coding/GuidedCoding_study_final_report.md),
the [description of the methods](https://www.thomasterwilliger.org/guided_coding/GuidedCoding_study_methods.md),
and the [technical evidence record](https://github.com/cctbx/guided_coding/blob/17e6bb8953bba5f5ffd41e9fb907281a51cf3e85/EVIDENCE.md).

For the practical steps, see [How Guided Coding works](how-it-works.html). To try it, see [Get started](quick-start.html).
