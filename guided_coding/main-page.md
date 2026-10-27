# Guided Coding

## Why try it?

Claude Code can make a useful change very quickly. The harder question is whether the change is right. Did it fix
the problem without breaking something else? What was actually tested? What still needs your attention?

Guided Coding gives Claude Code a short procedure for answering those questions. For each job, it asks Claude to:

- **Check the fix.** Where feasible, run a test that fails for the original problem and passes after the change.
- **Review the change.** Look for mistakes, check the fixes made during review, and prepare an outside review by
  another AI assistant for hard or consequential work.
- **Explain the result.** Give you a short report: what changed, what passed, what was not checked, and any decision
  that remains yours.

You get a more consistent way of working with Claude Code without learning a new programming system. Guided Coding is
five instruction files, not an additional program. I use it in my own software work.

## When should you use it?

Use Guided Coding when you ask Claude to change software you expect to keep: fixing a bug, adding a feature, or
changing code that other people use. It is particularly useful when you want the change checked, reviewed, and
explained without having to request every step yourself.

For a quick experiment that you might throw away, ordinary Claude Code may be enough. If you already have a
dependable testing and review process, Guided Coding may add less.

## How we developed Guided Coding

Guided Coding grew out of a practical question: what extra steps actually reduce errors in the code Claude Code
produces? We tested this by repeating earlier bug-fixing tasks with different checking steps and examining the
finished code.

The clearest improvement came from reviewing the code after a fix. On selected harder tasks, a second opinion
from a different AI assistant helped when added to Guided Coding. The same step did not show a clear extra benefit
when added to ordinary Claude Code with one review. Guided Coding combines the useful steps with a simple
procedure that guides you from the task, through testing and review, to a report you can understand.

You do not have to remember the steps yourself. Guided Coding asks Claude to follow them and to involve you when a
decision is needed.

## Two things matter more than any procedure

**Ask until you understand.** You should be able to say what was wrong, what changed, and why the checks support the
result. If a report is unclear, ask Claude to explain it more simply. You can also use the
[Guided Workflow Helper](https://www.thomasterwilliger.org/guided_workflow/index.html#panel-explain).
Do not accept a change you do not understand.

**You are in control, not the AI.** You choose the task and decide which changes to keep. Guided Coding tells Claude
to ask before changing interfaces, defaults, or other behaviour people rely on, and before committing, pushing, or
installing. You can stop or redirect a job. Because these are instructions, not an enforced sandbox, you should still
read the report and check important changes yourself.

## What do you need?

- Claude Code, in the Claude app or Terminal. If you do not have it, start with
  [Anthropic's Claude Code quickstart](https://code.claude.com/docs/en/quickstart).
- A software project you want to work on. Guided Coding is intended for projects managed with Git.
- Guided Coding has been tested on macOS. Linux should work but has not been tested; Windows has not been tested.

The [Quick Start](quick-start.html) lets Claude Code guide you through installation with one message. After that,
open your project in a new Claude Code conversation and ask Guided Coding to carry out a small task.

## Evidence and limits

The study of earlier bug fixes showed how much a review step helped, when an outside review added something,
and where a direct replay of Guided Coding found problems.
The results and their limitations are explained in plain language on the [Evidence](verification.html) page.

If you want the details before trying it, see [How Guided Coding works](how-it-works.html). The
[Documentation](documentation.html) page has installation, updating, evidence, and the exact instruction files.
