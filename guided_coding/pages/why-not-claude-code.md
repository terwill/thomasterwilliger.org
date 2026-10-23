# Why Guided Coding and not just Claude Code?

Claude Code can already fix bugs well. Guided Coding adds a few habits to every change, so that you can check the
result without reading every line. The step the study measured, a review pass, can also be run with plain
Claude Code; Guided Coding makes it routine, and adds the proving test, the triggered checks, the scope rule and the
report:

- **A review pass, every time.** One code-review pass over the change, with each of its fixes checked, and any fix
  that changes behaviour beyond the task reverted and raised with you. If the code-review skill is missing, Claude
  reviews the change itself, and says so.
- **A test that proves the fix,** where feasible. It fails on the old code for the reason in the task and passes on
  the new code. Where no such test is feasible, the report says why and what evidence was used instead.
- **Further checks only when the change needs them.** These are a live call, commands for another platform, or an
  outside review by another AI assistant.
- **A scope rule.** Claude asks before changing behaviour, interfaces, defaults or formats you did not ask about.
- **A short report.** What changed, what proves it, what was not checked, your decisions with recommendations, and
  the recommended next action.

## What the evidence shows

In a replay of 37 past bug-fix jobs, adding one review pass to plain Claude Code cut missed program errors per job
from 0.81 to 0.47. Guided Coding always includes a review pass (Claude Code's code-review skill, the review the
study measured, when it is available; otherwise Claude reviews the change itself and says so) and, where feasible,
a test that proves the fix, with further checks when needed. Guided Coding as now written has not itself been measured; it is being evaluated in real use.
[Evidence and limits](verification.html) goes through the main parts of Guided Coding and what the evidence says about
each, including the evidence against.

## And the most important part

Guided Coding does not replace your judgement. **Ask until you understand** each change, and **stay in control**:
Claude proposes, you decide. [How Guided Coding works](how-it-works.html) explains each step.
