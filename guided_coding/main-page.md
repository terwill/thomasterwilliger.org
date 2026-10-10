# Guided Coding

When regular Claude makes a fix for you, you are left with some questions: Do I understand the change it made? How was it tested? What remains uncertain?

Guided Coding organizes that work. You and Claude agree on a plan and a way to check the result. Claude works through the change, prepares tests and a report, and helps you obtain a review from a separate conversation. You decide whether to keep the change and whether to push it to your repository.

This is the procedure I use in my own software work. You can try the same approach in your own Git project, with settings for your tools and tests.

## A small example

Suppose your program crashes when it reads an empty file. You want it to print “The file is empty” and stop. When the file contains data, the program should work as it did before.

Tell Claude about the crash and what you want the program to do. Claude looks for the cause and proposes a plan. The plan includes tests for an empty file and a file with data. You check the plan before Claude makes the fix.

After making the fix, Claude shows you what changed and what happened in the tests. You pass Claude’s review files to another AI assistant in a separate chat. You read the report and review, then decide whether to keep the fix.

## What you decide

First, you approve a plan that says what Claude will change and how it will test the result. You can ask for a different plan or stop the task.

When the fix is ready, you decide whether to put the tested change into your project. This choice is labeled **INTEGRATE**. You can ask Claude to revise the fix or discard it instead.

Sending the approved changes to your Git repository is a separate choice, labeled **PUBLISH**. You can keep the changes on your computer without pushing them. The reviewer gives advice; you decide what to do.

## Try it in your own project

Use Claude Code on your computer. On a Mac, open the Claude app, choose the **Code** tab and select **Local**. You can also use Terminal on macOS or Linux. You need a project managed with Git. The User Guide explains the other tools you need.

[Download Guided Coding](https://www.thomasterwilliger.org/guided_coding/guided_coding.zip). The [User Guide](https://www.thomasterwilliger.org/guided_coding/getting-started.html) tells you how to check the download and make the `/guided_coding` command available. It also tells you how to set up your project so Claude knows which commands to use to build and test your program.

Choose a small bug or change for your first task. Open a new Claude Code conversation in your project. Send `/guided_coding`, your task and any bug report together in one message.

## Fix machine-written text

Use the [writing prompt on Guided Workflow](https://www.thomasterwilliger.org/guided_workflow/index.html#panel-rewrite) to make a draft clear, natural, and as short as possible without losing content or clarity. Add or attach the text, or a link to it. If accuracy depends on code or other sources, include those too.

## Help when you need it

Use `/guided_coding help` to see the commands. Use `/guided_coding status` to check whether Guided Coding and your project are set up.

If a report or a choice is hard to understand, give the relevant text to a [Guided Workflow Helper](https://www.thomasterwilliger.org/guided_workflow/index.html#panel-explain) and ask it to explain. You can ask the coding session to change direction or stop at any time.

## Current status

Guided Coding is still being developed. Its tools check for changed or missing files and for required information in reports. Claude still has to follow the instructions. Tests and outside review can miss mistakes. We have not established that Guided Coding produces better fixes than other approaches.

This page describes the version included in the current download. Read the [overview](https://www.thomasterwilliger.org/guided_coding/overview.html) for an explanation of the process, the [implementation details](https://www.thomasterwilliger.org/guided_coding/architecture.html) for how it works, and the [verification record](https://www.thomasterwilliger.org/guided_coding/verification.html) for what has been checked. [Browse all documentation](https://www.thomasterwilliger.org/guided_coding/documentation.html).
