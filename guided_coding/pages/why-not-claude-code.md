# Why Guided Coding and not just Claude Code?

Claude Code can already fix bugs well. In a replay study, one review pass after the change reduced the errors it
left, and an outside review by a different AI model, added to Guided Coding on 18 harder jobs, reduced them further,
narrowly. Guided Coding includes a
review on every coding job and prepares an outside review when the change needs one. It also asks for a test that
proves the fix, ends with a short report, and asks before changing what other code relies on. You could run each
step yourself with plain Claude Code; Guided Coding does them in order and tells you what is still open.

## What we tested

We replayed 37 real bug fixes in PHENIX and cctbx with Claude Code under different procedures, and counted the errors
left in the finished code. 18 of the jobs were harder ones: jobs where an earlier version of the procedure had caught
errors of its own, not a random sample of difficult work. Most steps were tested on those, so the findings apply to
work like it. The 18 jobs were not chosen with Guided Coding's "hard change" trigger, so the study does not show how
well that trigger picks out the jobs where an outside review helps. Every result was checked by probes run against the code, by blind readings, and by severity ratings
made without knowing which procedure produced the code. Figures below are **major errors left per run on the 18
harder jobs** (lower is better), unless stated otherwise.

### 1. Tested and found to help

| Step | What we found |
|---|---|
| **One review pass** after the change | The clearest effect: 0.90 → 0.79 major errors per run; across all 37 jobs, program errors missed fell from 0.81 to 0.47 per job |
| **An outside review by a different AI model** | Helped on the 18 harder jobs, narrowly: 1.00 → 0.83 in the full procedure. The net gain came from 4 of the 18 jobs, and the review also brought in a few new errors. Added to plain Claude Code with one review, it gave 0.85 → 0.76, not a clear difference |
| **A test that proves the bug** (fails before the fix, passes after) | More runs produced a proving test: about 1 in 7 plain runs ended without one, against 1 of 37 jobs when it was required (all 37 jobs). Its effect on errors left was not measured separately |

### 2. Tested, with no clear benefit found

| Step | What we found |
|---|---|
| **A second review pass** | No clear additional benefit found over one review pass |
| **An independent reviewer step** (a separate, structured review) | Not clearly better than a second ordinary review, at about three times the time |

### 3. Probably hurt (estimated, not tested)

| Step | What we found |
|---|---|
| **A strict scope rule** (undo every fix beyond the literal task, and ask first) | Probably cost errors: fixes the review found were undone and left as questions, and the procedure that used it left more major errors than plain Claude Code with one review (0.97 against 0.79). The size was estimated from those cases, not measured directly |

**Two scorings of the same arms.** Plain Claude Code with one review appears as 0.79 (round 6) and as 0.85 (before the
outside review, round 6b); Guided Coding 1.3 appears as 0.97 and 1.00. Round 6b's instruments found further errors
that the earlier versions also had, which raised those figures. Each comparison uses figures from one scoring.

## What Guided Coding does

The procedure follows from those findings:

1. **Fix the problem** the task describes.
2. **Write a test that proves the bug:** it fails on the old code and passes on the new. Where no such test is
   feasible, the report says why and what evidence was used instead.
3. **Review the change once** (Claude Code's code-review skill, the review the study measured, when it is available;
   otherwise Claude reviews the change itself and says so), and fix what the review finds in the changed code.
4. **For hard or consequential changes, prepare an outside review** for a different AI model, and handle its
   findings when the reply comes back.
   Hard means correctness turns on conditions the tests may not reach: checks and guards, processes and failures,
   defaults and compatibility, shared code with several callers. For other changes it is offered, not required.
5. **Fix real defects** found in the changed code without asking. **Ask first** before changing public interfaces,
   defaults, file formats, behaviour that callers rely on, or the project's scope.
6. **Report** what changed, what proves it, what was not checked, your decisions with recommendations, and the
   recommended next action.

A second review pass is not part of it. The independent reviewer step is available when you ask for it.

## Useful, but not tested

| Step | Why it is included |
|---|---|
| **The short final report** | Says plainly what was changed, what was checked and what is still open, so nothing is silently left |
| **A real check against a live service** (APIs, model names) | Some fixes can only be confirmed against the real service |
| **Exact commands for another platform** | Lets the fix be checked on Windows, Linux or CI |
| **Care with user data and credentials** | Changes that touch existing files or keys get an outside review |
| **Asking before commit, push or install** | Nothing goes out without your go |
| **A plan and a backup for consequential work** | Installations and migrations are prepared reversibly and checked before the irreversible step |

## Limits

The effects are small (about 0.1 to 0.2 major errors per run) next to the variation between runs, and they come from
18 harder jobs and one AI model family doing the work. We did not measure the developer's own time, or whether
Guided Coding as a whole beats plain Claude Code with one review and an outside review. Guided Coding 1.4 has not
itself been replayed; it was checked in a small trial and is being evaluated in real use. The narrower scope rule was
adopted without a test, and the outside review was measured with a scripted review request, not Guided Coding's own
review file. A larger earlier version of the procedure, with several review layers, left fewer major errors on the
harder jobs (0.44 per run, one run per job, and much slower); which of its parts did that is not known.

[Evidence and limits](verification.html) goes through each part of Guided Coding in detail. The
[full report](https://www.thomasterwilliger.org/guided_coding/GuidedCoding_study_final_report.md) of the study, with
every figure traced to its source, and the
[description of the methods](https://www.thomasterwilliger.org/guided_coding/GuidedCoding_study_methods.md) can be
downloaded.

## And the most important part

Guided Coding does not replace your judgement. **Ask until you understand** each change, and **stay in control**:
Claude proposes, you decide. [How Guided Coding works](how-it-works.html) explains each step.
