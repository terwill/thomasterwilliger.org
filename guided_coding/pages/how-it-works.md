# How Guided Coding works

Guided Coding is a short set of instructions for Claude Code. Claude still writes the code and runs the tests.
Guided Coding tells it how to check and report the change. Other Claude Code conversations are unaffected.

## An ordinary job

1. **You describe one task.** For example, ask Claude to fix a crash when a program reads an empty file.
2. **Claude checks the starting point.** It records the starting state of the code and checks whether the job
   needs any of the extra checks below.
3. **Claude makes the change and tests it.** Where feasible, it writes a test that fails for the original bug and
   passes after the fix. It also runs relevant existing tests. If a before-and-after test is not feasible, it says
   why and gives the best other evidence.
4. **Claude reviews its work.** It runs one review pass, checks any corrections made during review, and runs the
   affected tests again.
5. **Claude reports back.** The report starts by saying whether the change is ready to use. It tells you what
   changed, what passed, what was not checked, any decisions still needed, and the recommended next action.
6. **You decide what happens next.** Ask questions, request another review, accept or reject the change, or ask
   Claude to commit or push it according to your project's rules.

Claude normally fixes genuine defects it finds in the code it changes. It asks before changing a public interface,
default, file format, intended behaviour relied on by other code or users, or the agreed reach of the task.
Each question comes with options and a recommendation.

The review uses Claude Code's code-review skill when available. Otherwise Claude reviews the change itself and
says that it used this fallback. The study measured the code-review skill, not the fallback.

## When extra checks are needed

Most jobs need only the steps above. Some changes need more evidence.

| Situation | Added check |
| --- | --- |
| Correctness depends on a live service, such as an API or model provider | Make a real call with safe test inputs |
| The problem occurs on a different platform | Give exact commands to test there and leave the fix unconfirmed until they are run |
| The result will be installed by other people | Prepare an outside review |
| Existing user files or credentials could be affected | Prepare an outside review |
| The change is hard to test fully | Prepare an outside review |
| An important correctness question remains open | Prepare an outside review |

A hard change includes failure handling, processes and timeouts, defaults and compatibility, checks and validators,
or shared code with several callers when the tests may miss important cases. A routine one-path fix with a convincing
test is not automatically hard. If Claude is unsure whether a live-service, other-platform, or hard-change check
is needed, it treats it as needed.

**What an outside review means.** Claude prepares a file containing the task, full change, tests, results, and
questions. You give that file to another AI assistant and return its comments to Claude. Claude addresses each
finding. The file should exclude credentials and private data, but it contains code: share it only with a service
your project permits. You can ask for an outside review even on a routine job.

## Changes that are hard to undo

An installation, migration, change to shared tooling, or other hard-to-undo action needs these steps before
anything irreversible happens:

1. Claude prepares and tests a reversible change.
2. You approve a short plan.
3. Claude makes a backup and checks that recovery is possible.
4. An outside review of the plan and prepared change is completed, with important findings resolved.
5. You explicitly authorize the step that changes the shared installation or other important state.

The purpose is to let you inspect what will happen before it happens.

## More control and safety

- **Approval and publication.** Claude is instructed not to commit, push, or install without your request, and to
  follow project rules in `CLAUDE.md`, `AGENTS.md`, and any saved notes. Before pushing, it reports unresolved
  checks and asks you to accept anything important that remains open.
- **Optional independent reader.** For subtle work, Claude may recommend a separate in-session reviewer. It runs
  only if you agree. In the study, this was slower than an ordinary review and did not show a clear extra benefit.
- **No unfinished background work.** A job is meant to finish or stop its tests and builds before its final report.
- **Optional job log.** You can keep a one-line history of jobs and check later whether any defects emerged.

## Several tasks in a row

`/gc batch` is for a supervised list of separate tasks. Claude runs them one after another, saves each result as
a patch (a file containing the changes), and restores the project's working files between jobs. Tasks that depend on earlier tasks are left for later. Decisions,
paid live calls, and outside reviews are left pending. Nothing is pushed or installed during a batch.

At the end, you get one summary and decide which patches to keep. This is **not** an unattended overnight mode.
Stay reachable: a batch does not detect other sessions using the same project folder, and only you can interrupt
a job that hangs.

## Setup and notes

`/gc setup` is optional, once per project. Claude reads the project's existing files and fills in what it can
find about build and test commands, the full test suite, commit and push rules, and outside review preferences.
It shows you one short card to confirm or correct, then saves a notes file at `.claude/GC_NOTES.md`.
Your team's instructions take precedence over these personal notes.

## What this cannot guarantee

These are instructions, not a technical sandbox that enforces each step. Claude may make mistakes or fail to follow
them. A passing test checks the cases it covers, not every possible behaviour. The final report is useful because
it tells you what was and was not checked; your judgment still matters.

The [Evidence](verification.html) page describes the study behind individual steps and the checks of
the current procedure. For installation, use [Quick Start](quick-start.html). For every document and the exact
instruction files, see [Documentation](documentation.html).
