# How Guided Coding works

## You start with Claude Code

Guided Coding runs inside Claude Code, in the Claude app or in Terminal. Claude still reads your code, makes the
changes and runs the tests. Guided Coding is a short set of instructions that tells Claude how to do that work and
how to report it. It is used only when you type `/gc`; other conversations are not affected.

All of it is instructions. No tool enforces them. That keeps it short and easy to change, and it means the report is
your main check that the instructions were followed.

## Two things matter more than any procedure

**Ask until you understand.** If you cannot say what was wrong, what changed and how the test shows it is fixed, ask
until you can. If you still do not understand a change, do not accept it. If a second opinion would help, ask for an outside review
(below).

**You are in control, not the AI.** Claude proposes; you decide the task, its reach, what to keep, and whether
anything is pushed or installed. You can redirect or stop it at any time.

## The steps of one job

1. **Start.** Claude restates the task, notes the starting state of each repository it will touch, and checks
   whether the job needs any added steps (the triggers below).
2. **Scope.** Claude does the implementation, tests and documentation the task needs, and fixes without asking any
   real defect it or a review finds in the code the job changes and the paths that code calls. It asks you before
   changing a public interface, a default, a file format, intended behaviour that callers rely on, or the agreed scope
   (such as another repository). Each question comes with the options and a recommendation.
3. **A proving test.** Claude writes a test that fails on the old code for the reason in the task and passes on the
   new code, and runs it both ways. If no such test is possible, it says why and gives the best other evidence.
4. **The existing tests** for the code it touched.
5. **One review pass** over the change, with Claude Code's code-review skill. Claude checks each fix the review
   makes. It keeps a fix that corrects a real defect in the changed code, and reverts a fix that is wrong or that
   changes an interface, a default, a format or behaviour callers rely on, raising it with you instead. If the
   code-review skill is not available, Claude reviews the change itself, and the report says that this fallback was
   used; it is not the review the study measured.
6. **Added steps,** only for the triggers that apply.
7. **A short report.** It says whether the change is ready to use; what changed; the proof; the checks run; what was
   not checked; any changes you did not ask for; your decisions, each with a recommendation; and the recommended next
   action. It is Claude's last message: long tests or builds are finished or stopped first, and nothing it started
   is left running.
8. **Committing and pushing,** only when you ask, following your project's rules. Where your project leaves the
   commit or push to you, Claude gives the exact commands to run, in order, and checks the result when you say they
   are done.

## The triggers

| Trigger | When it applies | What it adds |
| --- | --- | --- |
| Live service | Whether the fix works can only be confirmed against a live service, such as an LLM provider or a model default | A real call for each changed path, with safe test inputs |
| Other platform | The defect is reported for a platform other than your computer | The exact commands to run there; the fix is "not confirmed" until they have been run |
| Install for others | The change goes straight to a place others install from | An outside review |
| Data or credentials | The change writes, moves or deletes existing user files, or handles credentials | An outside review |
| Hard change | Whether the change is correct turns on conditions the tests may not reach: a check, guard or validator, or detecting failure; processes, polling, timeouts, cleanup, or a step failing part-way; defaults or compatibility across versions, models, providers or platforms; shared code with several callers, where behaviour changes beyond the reported path. A routine fix on one path with a convincing test is not a hard change | An outside review |
| Open question | After the review, an important correctness question is still open, or there is no convincing test | An outside review |

If Claude is unsure whether Live service, Other platform or Hard change applies, it treats it as applying.

An outside review means: Claude writes one file with the task, the full change, the tests and their output, and the
question. You paste it into another AI assistant and paste the reply back. Claude answers each finding.
On any other job the outside review is optional: the report offers it in one line, and you can ask for it at any
time; it is then handled in the same way. The
file leaves out keys and private data, but it contains your code: share it only with an assistant your project
allows.

## Consequential work

Installations, migrations, changes to shared tooling or safety mechanisms, and operations that could cause damage that
is hard to undo get more care. Claude first prepares the change as something that can be undone, and tests it. Before
the irreversible step:

1. you approve a short plan;
2. Claude makes a backup and checks it;
3. an outside review of the plan and the prepared change is completed, and its important findings are resolved;
4. nothing touches a shared installation without your explicit go.

## Other rules

- **Large jobs.** If a task bundles changes that can be separated, Claude proposes splitting it, and running the
  parts with `/gc batch`.
- **A second reader, if useful.** When a change is subtle, touches shared code or many callers, or Claude is not
  confident the tests would catch a wrong fix, the report recommends an independent reviewer: a separate Claude
  reviewer that reads the change and its evidence. It runs only if you agree. It takes about three times as long as
  a review pass, and in the study it was not clearly better than simply running a second ordinary review.
- **Before a push.** Claude pushes only when you ask it to. It first names anything important still open (a
  pending step, a failing essential check, an unresolved important correctness finding), and goes ahead only if you
  explicitly accept it. It updates the branch first if needed and reruns the checks the
  update affects. If your notes name a full test suite to run before a push, it offers to prepare it. A release also
  gets a short checklist: where it goes, the test results, your approval, and how to undo it.
- **A job log, if you want one.** If your notes turn it on, each job adds one line to a log file, so that you can
  check later how the jobs turned out.

## Several tasks: `/gc batch`

You give a list of tasks, a stopping time and a time limit per job. Claude runs the tasks one at a time, each with
fresh context. After each job it saves the job's changes as a patch, checks the patch is complete, and restores your
checkout. A job that needs a decision stops and is listed. Tasks that depend on each other are left for afterwards,
and paid live calls and outside reviews are left pending. Nothing is pushed, installed or done irreversibly inside a
batch. At the end you get one summary of all the jobs, and decide which patches to keep. You stay reachable
throughout: a batch cannot notice other sessions working in the same checkout, and only you can interrupt a job that
hangs.

## Setup and notes

`/gc setup` looks at your project and shows one card of settings: the build and test commands, a full test suite to
run before a push (if you have one), your commit and push rules, which AI assistant you use for outside reviews, and
a few others. After you confirm it, it saves them in a short notes file, `.claude/GC_NOTES.md`, that later jobs read.
Your team's own instructions (`CLAUDE.md`, `AGENTS.md`) take precedence over these personal notes.

## Limits

Guided Coding as now written has not itself been measured; [Evidence and limits](verification.html) goes through
its main parts and what the evidence says about each. Its review
pass is done by the same kind of model as the one doing the work. An outside review can use a different
AI assistant, which you choose. The report is only as reliable as
the checks behind it, which is why it says what was not checked, and why asking until you understand matters.

## More information

- [Quick Start](quick-start.html): let Claude Code install Guided Coding with you.
- [Installing Guided Coding](getting-started.html): the commands.
- [Documentation](documentation.html): every document, including the skill files themselves.
