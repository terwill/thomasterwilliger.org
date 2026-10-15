# Guided Coding Help and Information

When Claude Code makes a fix for you, you are left with some questions: Do I understand the change it made? How was it tested? What remains uncertain?

Guided Coding helps you answer these questions. You and Claude agree on a plan and a way to check the result. Claude works through the change, prepares tests and a report, and helps you obtain a review from a separate conversation. You decide whether to keep the change and whether to push it to your remote Git repository.

This is the procedure I use in my own software work. You can try the same approach in your own Git project, with settings for your tools and tests.

- [Why Guided Coding and not just Claude Code?](why-not-claude-code.html)
- [Why Guided Coding and not Vibe Coding?](why-not-vibe-coding.html)
- [How Guided Coding works](how-it-works.html)
- [Quick Start with Guided Coding](quick-start.html)

## A small example

Suppose your program crashes when it reads an empty file. You want it to print “The file is empty” and stop. When the file contains data, the program should work as it did before.

You can start Guided Coding and tell Claude about the crash and what you want the program to do. Claude looks for the cause and proposes a plan. The plan includes tests for an empty file and a file with data. You check the plan before Claude makes the fix.

After making the fix, Claude shows you what changed and what happened in the tests. Claude prepares a review message and package. You give both to another AI assistant in a separate chat. You read the report and review, then decide whether to keep the fix.

## What you decide in Guided Coding

For an ordinary task, you first approve a plan that says what Claude will change and how it will test the result. You can ask for a different plan or stop the task.

When the fix is ready, you decide whether to put the tested change into your project. This choice is called **INTEGRATE**. You can ask Claude to revise the fix or discard it instead.

Sending the approved changes to your remote Git repository is a separate choice, called **PUBLISH**. You can keep the changes on your computer without pushing them. The reviewer gives advice; you decide what to do.

## Several tasks while you are away (auto mode)

Auto mode lets Claude work through a list of small tasks one at a time. You give the list and say when the run should end. A task that fails or needs your decision is saved as **Blocked**, with the reason.

Each task has its own Git branch. Claude tests it in a separate copy of your software. Claude saves tested changes for your review, with a short report on each change, its checks and what remains uncertain. Approving a saved change accepts that version. It does not add the change to your project or publish it.

In auto mode, you do not approve each task’s plan, and no outside review happens before a change is saved. Claude decides how to test each change and what counts as passing. Your project’s required checks still apply. Claude’s reviewer and checker agents still examine the work. You can ask for an outside review before approving. To add a change to your project or publish it, you give a later instruction. The usual required review still applies.

Auto mode is new and has had limited use. Auto mode runs only on macOS. On other systems it refuses to run. Your project needs a separate test copy and settings prepared first; see the [User Guide](https://www.thomasterwilliger.org/guided_coding/getting-started.html). Keep the computer powered and awake. If a usage limit interrupts the run, you must resume it yourself.

## Try it in your own project

Use Claude Code on your computer: the Claude app on a Mac, or Terminal on macOS or Linux. Windows is not supported. You need a project managed with Git. The User Guide explains the other tools you need.

[Download Guided Coding](https://www.thomasterwilliger.org/guided_coding/guided_coding.zip). The [User Guide](https://www.thomasterwilliger.org/guided_coding/getting-started.html) tells you how to check the download and make the `/guided_coding` command available. It also tells you how to set up your project so Claude knows which commands to use to build and test your program.

Choose a small bug or change for your first task. Open a new Claude Code conversation in your project:

1. In the Claude app, open the **Code** tab and start a new session.
2. Under **Environment**, choose **Local**, then **My computer**.
3. At the bottom of the page, use the folder selector to choose your project folder. In the Mac folder window, press Cmd+Shift+G and paste the full path.
4. Type your message and send it: `/guided_coding`, your task and any bug report together in one message.

In Terminal, change to your project folder, run `claude` and send the same message.

## Help when you need it

Use `/guided_coding help` to see the commands. Use `/guided_coding status` to check whether Guided Coding and your project are set up.

If a report or a choice is hard to understand, give the relevant text to a [Guided Workflow Helper](https://www.thomasterwilliger.org/guided_workflow/index.html#panel-explain) and ask it to explain. You can ask the coding session to change direction or stop at any time.

## Limits and more documentation

Guided Coding is a pilot; see [Verification and limits](verification.html) for what has been checked. Read the [overview](https://www.thomasterwilliger.org/guided_coding/overview.html) for an explanation of the process and the [implementation details](https://www.thomasterwilliger.org/guided_coding/architecture.html) for how it works. [Browse all documentation](https://www.thomasterwilliger.org/guided_coding/documentation.html).
