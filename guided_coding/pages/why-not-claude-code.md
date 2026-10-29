# What difference does Guided Coding make?

Claude Code can write and fix code without Guided Coding. Guided Coding adds a consistent procedure for checking
the result and explaining it to you.

## What changes when you use Guided Coding?

| With ordinary Claude Code | Guided Coding asks Claude to do this on each job |
| --- | --- |
| Tests and reviews depend on the request and the session | Try to reproduce the bug with a test that fails before the fix and passes afterward; run relevant existing tests |
| You may need to request a code review | Review the change once, then check any corrections made during review |
| Important uncertainties can be left in the conversation | End with a short report of what changed, what was checked, and what remains open |
| You decide when to seek another opinion | Prepare an outside review for hard or consequential changes; offer one for other changes |
| You decide how much authority to give the assistant | Ask before changing important existing behaviour, committing, pushing, or installing |

These are instructions to Claude, not technical restrictions on what it can do. You should still read the result,
especially when a mistake would matter.

## When is it useful?

Guided Coding is a good fit for bug fixes, new features, and maintenance work in software you plan to keep.
It helps when you want a repeatable check of the change and a clear account of what was tested and what remains open.

For a throwaway prototype, plain Claude Code may be quicker; see
[Guided Coding and vibe coding](why-not-vibe-coding.html). If you already require useful tests, run a review on
every change, and record open questions, the extra benefit may be smaller. Guided Coding mainly puts these steps
into a repeatable order.

## What did the study find?

In a replay of 37 past bug-fixing jobs in the PHENIX and cctbx scientific software projects, one review pass reduced the program errors missed by
plain Claude Code from 0.81 to 0.47 per job. That is the main measured reason for including a review on every job.

On 18 selected harder jobs, an outside review by a different AI model removed some additional major errors when
added to Guided Coding (1.00 to 0.83 per run). The gain was modest: the net improvement came from four jobs, and
a few new errors were also introduced. The same review did not show a clear benefit when added to ordinary Claude
Code with one review (0.85 to 0.76). Guided Coding therefore reserves this extra step for harder or consequential
work, while letting you request it whenever you want.

Requiring a test that fails before a fix and passes afterward made it more likely that a job ended with such a
test. Its separate effect on remaining errors was not measured.

The [Evidence](verification.html) page explains these comparisons and the direct replay of an earlier Guided
Coding procedure, including results that were inconclusive or unfavorable. It links to the complete report and
methods.

Guided Coding does not replace your judgment, guarantee correctness, or make it safe to share confidential code with an
unapproved outside service. It can take longer than a quick unreviewed edit.

## Related approaches

Guided Coding is one of several ways to make AI-assisted coding easier to check and control.

- **[Claude Code best practices](https://code.claude.com/docs/en/best-practices)** recommends specific requests,
  giving Claude a check it can run, and asking for evidence before accepting that a task is done. Claude Code also
  has a built-in [`/code-review`](https://code.claude.com/docs/en/code-review-local) command, which reviews changes
  in a separate context.
- **[Superpowers](https://github.com/obra/superpowers)** provides a fuller development workflow, including
  planning, test-first development, systematic debugging and review.
- **[GitHub Spec Kit](https://github.com/github/spec-kit)** and **[OpenSpec](https://github.com/Fission-AI/OpenSpec)**
  help developers describe and agree on changes before code is written. Spec Kit also includes a structured
  bug-fixing process.

Guided Coding uses many of the same ideas in a small procedure for changes to existing software. We have not
compared its accuracy, speed or ease of use directly with these alternatives.

## Try it

Read [How Guided Coding works](how-it-works.html) if you want to understand the procedure, or use the
[Quick Start](quick-start.html) to install it with one message.
