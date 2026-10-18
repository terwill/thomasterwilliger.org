# How Guided Coding works

## You start with Claude Code

Guided Coding runs inside Claude Code, in the Claude app or in Terminal. Claude still reads your code, makes the changes and runs the tests. Guided Coding adds structure and checks to that work: a plan you approve, tests and a report you can read, reviews, and separate decisions for keeping and publishing a change.

It is used only when you ask for it. Start a conversation in your project with `/guided_coding` and your task. Ordinary Claude Code conversations are not affected.

## Fixing a bug: the steps

1. **Startup checks.** Guided Coding checks that its own files are complete and unchanged, that your Claude Code version is new enough, and that your project is set up for Guided Coding and its settings are saved.
2. **Plan.** Claude looks for the cause and shows a one-page plan: the goal, which files will change, how the result will be checked and what could go wrong. You choose **APPROVE**, **REVISE** or **STOP**.
3. **Light or full path.** The plan says which path the task takes. A change takes the light path only if two things are true. It cannot affect how the program behaves, what it requires, its interfaces or an important claim. You also accept the worst case stated in the plan. Every other change takes the full path. The size of the change does not decide this.
4. **Separate working copy.** Claude makes the change on its own Git branch, usually in a separate working folder (a Git worktree). Your own work and your main branch stay untouched.
5. **Tests.** The key check should fail on the old code for the reason in the bug report and pass on the fixed code. Claude also runs a control test. It shows that the check can detect a wrong result.
6. **Reviewer agent (full path).** A separate reviewer agent reads the finished change before its evidence is saved.
7. **Saved evidence.** Claude saves the change, the test logs and a report in an evidence folder and seals it with a list of checksums (a fingerprint of each file's contents). Any later change to that evidence can then be detected.
8. **Checker agent (full path).** A separate checker agent reads the sealed evidence against a checklist.
9. **Outside review (full path).** Claude prepares a message and a review package. You attach both in a separate chat, preferably with a different AI assistant. You copy its reply back, and Claude answers each finding. You can waive this review for one change, in your own words. The waiver covers only adding that exact change to your project, never its publication.
10. **Your decision.** The report shows the complete change, the full code of every new test, the test results and what remains uncertain. While the outside review is still pending, you can **ACCEPT** the exact tested change; this records your acceptance and changes nothing else. After the review, or your recorded waiver, you choose **INTEGRATE** to add the change to your project, **REVISE** or **DISCARD**.
11. **Publication, separately.** Sending the change to your remote Git repository is a later **PUBLISH** or **HOLD** decision. Before it, Claude is instructed to run your project's full test suite and compare it with an earlier run. An outside review of exactly the commits to be sent is also required. You can waive the test suite for one set of commits, in your own words. In this version the outside review before publication cannot be skipped. If your project forbids Claude to push, Claude runs the same checks, gives you the exact push command to run yourself, and then confirms what reached the remote repository.

Each time Claude hands the work back to you, it describes the practical situation first, recommends what to do and lists the complete next steps.

## Building new code: the steps

New code follows the same steps. The difference is in the plan and the tests. The plan says what the new code should do and how that will be checked. The tests show the new behavior working, and the report includes the full code of every new test. If a change has no new test, the report says what check was used instead.

## The technical details

These are the parts Guided Coding adds on top of Claude Code. Some are enforced by small checking tools that come with the Guided Coding files (the kit). Others are instructions that Claude is told to follow. The tools cannot make Claude follow them.

| Part | What it does | Enforced by a tool? |
| --- | --- | --- |
| Source check | Before each use, checks every kit file against the kit's list of checksums. It refuses changed, missing or extra files. | Yes |
| Version check | Requires Claude Code 2.1.281 or newer. In the app, if the version cannot be read, it says so and continues. | Yes |
| Project adoption | Your project's instruction file names the exact version of the rules it uses and where its settings are saved. Without it, Guided Coding does not start a task. | Instruction |
| Project settings | One file in your project records its build and test commands, folders and rules for keeping and publishing changes. | Instruction |
| Branches and worktrees | Each change gets its own Git branch, usually in a separate working folder. This keeps files apart. It does not separate installed programs, servers or shared data. | Instruction |
| Save and restore | When a test must run in your main folder, Claude saves the original files, applies the change, runs the test and puts the originals back. | Instruction |
| Reviewer and checker agents | On full-path tasks, a reviewer agent reads the finished change and a checker agent reads the sealed evidence. | Instruction |
| Sealed evidence | The evidence folder is sealed with a list of checksums. Any later change is detected. Sealing does not make the evidence true. | Yes |
| Screen checker | Checks that the plan, stop, accept, result and publication screens have their required parts, including a recommendation and the next step, and refer to the same evidence. It checks that the report shows the complete change. It requires a matching outside review, or your recorded waiver, before a full-path result, and an outside review before a publication. It checks form, not accuracy. | Yes, form only |
| Publication check | Before a push, compares the planned commits with Git. It accepts only one approved push command, which sends no Git tags. It never pushes by itself. When you push yourself, it confirms afterwards that the remote branch has the planned commit and that no tag changed. | Yes |
| Task records | Each task keeps its decisions, the kit version used and its evidence in your project's `.claude/records` folder. `/guided_coding history` lists them. | Instruction (a tool lists the records) |
| Auto mode | Works through a list of small tasks one at a time while you are away, with a time limit on each run. Outside network access is blocked unless a task is explicitly granted it. Runs only on macOS, and needs the psutil package for Python, installed in a virtual environment as the User Guide shows. | Yes |
| Lock | Auto mode locks its own test copy of your program while it runs. There is no other lock. Separate conversations coordinate through messages. | Yes, auto mode only |

## Limits

Guided Coding is a pilot. Its tools check files, forms and identities. They do not show that a test checks the right thing, that a log is truthful or that a reviewer is independent. The reviewer and checker agents are the same kind of model as the one doing the work. Guided Coding has not established that it produces better fixes than other approaches. The [verification and limits](verification.html) page has the details.

## More information

- [Quick Start](quick-start.html): set up Guided Coding by giving Claude Code one message.
- [Installation and project setup](index.html#install), on the main page.
- [User Guide](getting-started.html): setup and a first task, step by step.
- [Documentation](documentation.html): overview, architecture, verification and the procedure files.
