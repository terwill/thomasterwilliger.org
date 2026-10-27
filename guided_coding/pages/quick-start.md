# Get started with Guided Coding

You can install Guided Coding by giving Claude Code one message. Claude explains the steps, asks your permission
before making changes, and helps you try a small task.

## Step 1. Open Claude Code

If you do not have Claude Code yet, follow [Anthropic's setup guide](https://code.claude.com/docs/en/quickstart).
Guided Coding runs inside Claude Code; it is not a separate app.

Open a new Claude Code conversation on your computer. You can use the Claude app's Code tab or run `claude` in
Terminal. If you are not sure where to open it, the message below asks Claude to help.

## Step 2. Copy this message

Use the button below, paste the message into Claude Code, and send it. You can read the message first. It asks
Claude to explain the installation and request your approval before changing anything.

```copy
Instructions to Claude Code for setting up Guided Coding. Read https://www.thomasterwilliger.org/guided_coding/ and the installation page https://www.thomasterwilliger.org/guided_coding/getting-started.html. Briefly summarize how Guided Coding works, including its two main rules (ask until you understand each change; I stay in control), and tell me whether it can help with my work. If it can, offer to install it. Suggest where to clone the repository, then use the installation commands exactly as written, copied from the raw README at https://raw.githubusercontent.com/cctbx/guided_coding/master/README.md (the same commands as the installation page; do not reword or shorten them), which check before they change anything and show the version they register. Before changing anything on my computer, show me all the installation steps, say what each does, and ask for my approval once; then run them, and ask again only if something unexpected comes up. Then tell me when I must open a new conversation, which folder to open it in, and what to type there (`/gc`, then optionally `/gc setup`). Give click-by-click directions for the Claude app's Code tab: the Environment choice (Local, then My computer) and the separate folder selector at the bottom of the page; on a Mac mention Cmd+Shift+G, and mention the Terminal alternative (cd to the folder, then claude). If the app looks different from this, say so and describe what to look for. When installation is complete, suggest a small first task. Use plain sentences, and put every step I must take next in your final message.
```

## Step 3. Try a small change

After installation, start a **new conversation** in Claude Code in the folder of the software project you want to
change. Type `/gc` followed by a specific small task, such as fixing a bug you can reproduce.

When the job finishes, read the report. Ask about anything unclear before you accept the change. You can type
`/gc` by itself to get an introduction. `/gc setup` is optional: it saves your project's build and test commands
for later jobs.

Installing Guided Coding is normally done once per computer. It has been tested on macOS; Linux should work but
has not been tested, and Windows has not been tested. If you prefer to install it yourself, see
[Manual installation and maintenance](getting-started.html).
