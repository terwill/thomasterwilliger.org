# Guided Coding Help and Information

When Claude Code makes a fix for you, you are left with some questions. Do I understand the change it made? How was
it tested? What remains uncertain?

Guided Coding is a short set of instructions for Claude Code that is built to answer those questions for every change. You give
Claude a bug or a bounded change. Claude makes the fix and, where feasible, writes a test that fails on the old code
and passes on the new code; where it is not, the report says why and what evidence was used instead. Claude runs one
review pass over the change, adds further checks only when the change needs them, and ends with a short report. You decide what to keep, and whether and when anything is pushed.

This is the procedure I use in my own software work. You can use it in any project managed with Git.

- [Why Guided Coding and not just Claude Code?](why-not-claude-code.html)
- [Why Guided Coding and not Vibe Coding?](why-not-vibe-coding.html)
- [How Guided Coding works](how-it-works.html)
- [Quick Start with Guided Coding](quick-start.html)

## Start here

Guided Coding runs inside Claude Code, so you need Claude Code first. If you do not have it yet, follow
[Anthropic's Claude Code quickstart](https://code.claude.com/docs/en/quickstart), then come back here. Guided Coding
has been tested on macOS; it should work on Linux, and has not been tested on Windows.

1. **Recommended: let Claude install it with you.** Open [Quick Start](quick-start.html), copy its one message into
   Claude Code, and follow Claude's directions.
2. **Prefer to install it yourself?** [Download the ZIP](#download), or use the [install commands](getting-started.html)
   for Git or the ZIP.
3. **Then use it.** Open Claude Code in the folder of the project you want to change, and type `/gc` followed by
   what you want done. Installing is once per computer; `/gc setup` is optional, once per project, and saves that
   project's build and test commands.

## Two things matter more than any procedure

**Ask until you understand.** Before you accept a change, you should be able to say what was wrong, what changed,
and how the test shows it is fixed. Guided Coding is built to give you short, clear answers to those questions, but
it only works if you ask. If something in a report is unclear, ask again, or ask for it in plainer words. If you
still do not understand it, do not accept it. If you are unsure about a change, or it matters a lot, ask Claude
for an outside review file. Give it to another AI assistant for a second opinion, then paste the reply back to
Claude to address. A second reader, especially a different model, may catch problems that the first one missed.

**You are in control, not the AI.** Claude proposes; you decide. You decide what the task is, how far the change may
reach, what to keep, and whether and when anything is pushed or installed. Guided Coding asks you before it changes
behaviour you did not ask for and before any irreversible step, and it commits or pushes only when you ask. You can
redirect or stop it at any time.

## A small example

Suppose your program crashes when it reads an empty file. You want it to print "The file is empty" and stop. When
the file contains data, the program should work as it did before.

You type `/gc` followed by a description of the crash. Claude finds the cause and fixes it. It writes a test that
reads an empty file: the test fails on the old code with the crash, and passes on the new code. It runs the existing
tests and one review pass. Its report tells you what changed, how the test shows the fix, what it could not check,
and what it recommends you do next. You read the report, ask about anything unclear, and decide whether to keep the
fix.

## What you decide

- **The task and its reach.** Claude does the routine work the task needs, and asks you before it changes intended
  behaviour, an interface, a default or a file format that you did not ask about.
- **The decisions in the report.** Each comes with the background, the options and a recommendation.
- **Committing and pushing.** Claude commits or pushes only when you ask. Your project's own rules apply, for
  example whether an AI assistant may push at all.
- **Consequential work.** For installations, migrations, or changes that could cause damage that is hard to undo,
  Claude first prepares and tests the change. Before the irreversible step it asks for your approval of a short
  plan, checks a backup, and has the change read by an outside reviewer.

## Several tasks in a row

`/gc batch` runs a list of tasks one after another, each as its own job, while you stay reachable. Each job's
changes are kept as a separate patch, and your checkout is restored between jobs. Tasks that depend on each other
are left for afterwards; paid live calls and outside reviews are left pending; nothing is pushed or installed. At the
end you get one summary and decide which patches to keep. It is supervised, not an unattended overnight run.

## Help

Type `/gc` on its own for a short introduction. `/gc setup` saves your project's build and test commands in a short
notes file, so later jobs can use them. If a report or a choice is hard to understand, ask Claude to explain it more
simply. You can also give the text to a [Guided Workflow Helper](https://www.thomasterwilliger.org/guided_workflow/index.html#panel-explain).

## Evidence and limits

In a replay of 37 past bug-fix jobs, adding one review pass to plain Claude Code cut missed program errors per job
from 0.81 to 0.47. Guided Coding always includes a review pass (Claude Code's code-review skill, the review the
study measured, when it is available; otherwise Claude reviews the change itself and says so) and, where feasible,
a test that proves the fix, with further checks when needed. Guided Coding as now written has not itself been measured; it is being evaluated in real use. The study was
small, and it also found evidence for the larger earlier kit on some major errors. See
[Evidence and limits](verification.html), which goes through the main parts of Guided Coding and what the
evidence says about each, including the evidence against.

Guided Coding replaced a much larger earlier kit on 2026-10-23. The earlier kit had approval screens, evidence
packets and an unattended auto mode. It is kept on the repository's branch
[full-kit-rev21](https://github.com/cctbx/guided_coding/tree/full-kit-rev21).
