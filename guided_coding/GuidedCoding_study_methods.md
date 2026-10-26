# Protocol of the replay study: GuidedCoding Plus, GuidedCoding and plain Claude Code

Attachment to the final report (`walkthrough/final_report/FINAL_REPORT.md`). Written 2026-10-24 by a Claude Code
session for the Developer, from the study's record, plans, briefs and tools; round 6b and the GC 1.4 trial added
2026-10-26. It states the protocol of every stage and round as planned, and then checks it against what the record
and the tools show was done (section 9).

## How to read this document

- **Names** are the final report's: **GC+** is the earlier GuidedCoding kit (revisions up to 21), **GC** is the
  `/gc` skill replayed in rounds 6 and 6b, version 1.3 (cctbx/guided_coding 14b8371; superseded by 1.4), **P** is a plain Claude Code run, **P+R** is P
  resumed for one `/code-review --fix` pass, **P+2R** is P+R resumed for a second such pass, and **P+R+S** is P+R
  resumed for a structured reviewer step. **GC+O** is a round-6 GC run resumed with an outside review's reply. In
  round 6b, step O, **P+R+O** is a P+R session forked once and given a script-built outside review of its final
  change, and **GC+O\*** is a round-6 GC session (before any round-6 outside review) forked once and given one built
  the same way. In the older files, GC+ appears as "GC" or "G", P+2R as "R2" and P+R+S as "PRS"; in the step-O tools
  GC+O\* is "GCOS" and P+R+O is "PRO".
- **`<rec>`** is `phenix/.claude/records/2026-10-15-gc-replay-protocol/` in the Developer's build_39 checkout. Paths
  without a prefix are relative to `<rec>`.
- **Citations.** "R123" means line 123 of `<rec>/RECORD.md` as it stood on 2026-10-24 (1,731 lines). The final
  report's frozen copy (Src28, `RECORD_snapshot.md`, 1,712 lines) holds the same entries up to its freeze; its line
  numbers differ slightly near the end. Labels Src1 to Src38 are the final report's source index. The record is
  only appended to, so line numbers above 1,731 (round 6b and the GC 1.4 trial, R1889–R1942) refer to it as it
  stood on 2026-10-26 (1,942 lines) and leave the earlier numbers unchanged.
- **People.** The Developer is the PHENIX developer whose jobs these are (they/them). The Guide is the Claude Code
  session that ran the study. Bug reporters are called "a user". Every worker, scorer, reader, tagger and checker
  was a Claude model unless a line says otherwise.
- **Round 6 is finished** (2026-10-25). Its protocol is given as planned (`walkthrough/round6/PLAN_ROUND6.md`, draft
  4, with decisions in §10); §1.9 records how it ended, and section 9 compares it with what was done. Its results are
  in `walkthrough/round6/REPORT_R6_RESULTS.md`. Earlier text that described round 6 while it ran is kept, marked as
  of its date.
- **Round 6b, step O, is finished** (2026-10-26), and is the study's last step. Its protocol is given as planned
  (`walkthrough/round6b/PLAN_ROUND6B_O.md`, draft 2, with decisions O-0 to O-12 in §10); §1.11 records how it
  ended, and rows 67–83 of section 9 compare it with what was done. Its results are in
  `walkthrough/round6b/REPORT_R6B_O_RESULTS.md` (draft 3). The full round-6b plan (`PLAN_ROUND6B.md`, draft 3, step
  D) was not run. The trial of GC 1.4 that followed (§1.12) is an implementation check, not part of the experiment.

## Overview

| stage or round | dates (2026) | jobs | arms run | main plan | report |
|---|---|---|---|---|---|
| Tally | 10-15 | 85 GC+ task records | none (catch counts) | — | Src2 |
| Stage 1 | 10-15 to 10-16 | case 1 (and a calibration case 0) | P, P+R × 4 runs | `packet-7/REPLAY_PROTOCOL.md` (draft 6); PLAN_4.md | `stage1_results/STAGE1_RESULTS.md` |
| Stage 2 | 10-16 | cases 2 to 5 | P, P+R × 2 runs each | `packet-8/STAGE2_ADDENDUM.md` | `stage2_results/STAGE2_RESULTS.md` |
| Stage 3 | 10-16 to 10-17 | cases 6 to 10 | P, P+R × 2 runs each | packet-9, packet-10, `stage3_prep/BRIEF_STAGE3.md` | `stage3_results/STAGE3_RESULTS.md`; Src1 |
| Walk-through | 10-19 | the ten | none (analysis only) | `WALKTHROUGH_PLAN.md` (draft 5) | `walkthrough/STEP1`–`STEP5`, `REPORT_FULL_GC_vs_plain.md` |
| Round 4 | 10-19 to 10-21 | 27 new + the ten | P, P+R × 2 runs (new jobs only) | `walkthrough/REPLAY_ALL_PLAN.md` (draft 2) | `REPORT_R4_RESULTS.md` (draft 1) |
| Round 4b | 10-21 | all 37 | none (new instruments on all arms) | R1066–R1068, R1070–R1077, `r4_ledger/BRIEF_R4B_CROSS.md` | Src4 (draft 3) |
| Round 5 | 10-21 to 10-22 | the 18 "caught-any" jobs | P+2R, P+R+S on 38 runs | Src8 (`PLAN_MIDDLE_GROUND.md`, draft 3, frozen) | Src9, Src11, Src12 |
| Triage | 10-23 | all 37 (no runs) | none | `walkthrough/triage/` | Src15, Src16 |
| Round 6 | 10-24 to 10-25 | the 18 caught-any jobs (+1 for mechanics) | GC, GC+O, fresh, 38 counted runs | `walkthrough/round6/PLAN_ROUND6.md` (draft 4) | `walkthrough/round6/REPORT_R6_RESULTS.md` |
| Round 6b, step O | 10-25 to 10-26 | the 18 caught-any jobs | P+R+O, GC+O\*, resumed (forked), 76 runs | `walkthrough/round6b/PLAN_ROUND6B_O.md` (draft 2) | `walkthrough/round6b/REPORT_R6B_O_RESULTS.md` (draft 3) |
| GC 1.4 trial | 10-26 | 3 caught-any jobs and 1 routine job | fresh: 4 runs of an earlier 1.4 draft (trigger check), 3 runs of the full 1.4 text (resumed with an outside review) | none (R1936–R1937) | `walkthrough/gc_rev23/TRIAL_1.4.md` |

The ten original cases are numbered 1 to 10: 1 GUI output folder (o01-gui-output), 2 atomic writes (o02-atomic), 3
map manager follow-ups, 4 anisotropy, 5 Windows stop, 6 publication precheck, 7 reply cut-off, 8 sequence from map,
9 EBADF, 10 elbow (Src4, Terms).

---

## 1. Purpose and questions

### 1.1 Tally (2026-10-15)
GC+'s 85 task records were tallied for the defects each review layer caught (Src2). A catch count cannot show what
plain Claude Code would have done, so a replay was designed (R1–R3; `PLAN.md`).

### 1.2 Stages 1 to 3 (2026-10-15 to 10-17)
- **Question** (`packet-7/REPLAY_PROTOCOL.md` §1): "On the same task, from the same starting commit and with the same
  request, does plain Claude Code finish with the defects that GC's review layers caught still present?"
- **Stage 1** was framed as an indication only: whether the method works, and what P, P+R and GC+ did on case 1
  (protocol §5.7; PLAN_4.md).
- **Stages 2 and 3** asked the same question on four and then five more cases (R116–R120, R139–R141).
- **Reporting** (protocol §5.5, after OUTSIDE_READING_1 B2): three results per arm, never one combined score:
  program correctness (main), test adequacy, task completion.
- **Changed from the tally:** a counterfactual (the plain runs) instead of catch counts.

### 1.3 Walk-through (2026-10-19)
- **Aim** (`WALKTHROUGH_PLAN.md`, "The aim"): a fair, defensible comparison of the ten cases, with limits stated,
  using no new runs. Two questions: what the study shows on the ten tasks, and how far it generalises (selection).
- **Changed from stages 1–3:** analysis only; selection examined (step 2); GC+'s own remaining errors looked for
  (open reading, the Developer's commit audit); later, per-run rates and a full error ledger at the Developer's
  request (R262–R287).

### 1.4 Round 4 (2026-10-19 to 10-21)
- **Goal** (`REPLAY_ALL_PLAN.md`): "Remove the bias from how the ten cases were chosen, by replaying every remaining
  GC bug-fix job that can be replayed," and check GC+'s final version and the plain runs the same way.
- **Changed from the walk-through:** new runs on every remaining suitable job; probes written from the task alone, run
  on every arm.

### 1.5 Round 4b (2026-10-21)
- **Question** (R1055–R1068): do the 27 new jobs, and then all 37, need a different measurement to catch errors evenly?
- **Changed from round 4:** a second, checklist-driven blind reading; cross-arm probes of every candidate error on
  every arm; test-adequacy runs; the commit audit applied both ways; blind severity tagging; the hard / medium / easy
  frame (R1117–R1124).

### 1.6 Round 5 (2026-10-21 to 10-22)
- **Question** (Src8 §1): "does adding this structured, evidence-based review step after one ordinary review leave
  materially fewer major errors in the code than adding another ordinary review, and is the gain worth the time?"
- **Hypothesis and rules** fixed before the pilot (Src8 §8).
- **Changed from round 4b:** a pre-registered comparison of two added arms (P+R+S, P+2R) resumed from existing P+R
  sessions, on the 18 jobs where GC+'s layers caught something.

### 1.7 Triage (2026-10-23)
- **Question:** can a job be routed to the thorough procedure in advance? A permutation power check and a descriptive
  check of start screens on existing results; no new replays (Src15, Src16; R1601–R1613).

### 1.8 Round 6 (2026-10-24 to 10-25; as planned)
- **Question** (PLAN_ROUND6 §1–§2): compare the current GC with P and P+R, keeping the existing runs and adding fresh
  GC runs.
  - **Q1 (primary):** on the 18 caught-any jobs, confirmed major program errors left in the code (missed plus
    disclosed), GC+O against P+R.
  - **Q2:** recovery of GC+'s lead, (P+R − GC+O) ÷ (P+R − GC+).
  - **Q3 (optional stage 3):** GC against P+R on all 37 jobs, as non-inferiority.
- **Expected result, stated in advance:** "The most likely result is 'no clear difference'" (§1).
- **What each reading leads to** is fixed in advance (§2, decision 9).
- **Changed from round 5:** fresh runs, not resumed sessions; a different-model outside review simulated through the
  OpenAI API; a bootstrap interval in the reading rule.

### 1.9 Round 6: how it ended (added 2026-10-25)
- **Runs.** 38 GC runs counted, all valid with a reviewed leak verdict, none void; 4 wrote an outside review and were
  resumed as GC+O (case 1 g4, case 6 g1 and g2, gc-next-revision g2). Optional stage 3 (Q3) was not run.
- **Reruns.** The first full set was discarded (decision G, Bash refused); six runs were rerun because their
  bug-report file was missing (decision H); the four GC+O steps were re-validated, not rerun, after a clock artefact
  (decision I).
- **Scoring.** As planned (probes on every arm, a blind reading, row workers under labels L1/L2), with decisions J
  (earlier rulings bind; a sensitivity line), K (the blind reading's labels unreliable; every candidate ruled on every
  arm), L (a summary-script bug fixed before first use), M (supplementary blind severity tags, after the first
  summary was read; no figure changed), the strict disclosure rule (adopted while ruling; re-applied to the earlier
  jobs afterwards) and N (a descriptive count of the decisions GC put to the stand-in Developer, after the outside
  readings: of GC+O's 33 major errors left, 11 were put to the developer as a question and 7 in part; P+R asked about
  1 of 29). An internal checker sampled 32 rulings (30 agree, 0 disagree, 2 unsure).
- **Result** (`walkthrough/round6/R6_SUMMARY.md`): Q1 GC+O − P+R +0.111 per run (90% interval −0.194 to +0.417), no
  clear difference; Q2 recovery −0.32. By the rule fixed in advance this leads to keeping GC as it is.

### 1.10 Round 6b, step O (2026-10-25 to 10-26; as planned)
- **Origin.** After the round-6 readings the Developer asked for a follow-up in which the developer follows GC's
  recommendations ("yes let's do that", R1889). The full round-6b plan (`PLAN_ROUND6B.md`, draft 3; packet-28) had
  two steps: O, an outside review given to every run, and D, the same developer answer given to every run (primary
  a difference-in-differences of GC+D and P+R+D). The Developer chose step O first and to decide on D afterwards
  ("can we do O first, then decide whether anything else is needed?"; R1895–R1896). The proving-test step stayed
  untested (R1895).
- **Aim** (PLAN_ROUND6B_O §1): the final GC should contain the parts shown to do something, and leave out or make
  optional the parts not shown. The outside review by a different model was the part left unresolved by rounds 5
  and 6.
- **Questions** (§1), on the 18 caught-any jobs, on confirmed major program errors left in the code (missed plus
  disclosed), per run:
  - **O-P (primary for plain):** P+R+O − P+R, paired by run.
  - **O-GC (primary for GC):** GC+O\* − GC, paired by run.
  - **Level (descriptive):** GC+O\* − P+R+O. **Harm (descriptive):** errors the outside-review step brought in
    (origin "outside"), per arm.
- **Power and ceiling, stated in advance** (§1): −0.10 over 18 jobs is about 4 run-level removals of a major error;
  7 of the 18 jobs have no counted major error in either arm. O-P's ceiling was computed from the round-6 rows before
  any run (`ceiling/CEILING.md`): P+R's own replies named 4 of its 29 counted major rows (2 more in part), a ceiling
  of −0.111 on all jobs and −0.059 without case 6; O-P "no clear difference" was the expected result.
- **What each reading leads to** was fixed in advance (§2): O-GC decides the core step; O-P is supporting evidence;
  O-P adding without O-GC points to step D; then the Developer decides whether step D is needed.
- **Changed from round 6:** resumed (forked) sessions of both arms, not fresh runs; the treatment is the only new
  step, so the noise of the original draws cancels in the paired difference; one review recipe (task text and final
  diff) for both arms; a seeded line that is a condition of the reading, not only a report.

### 1.11 Round 6b, step O: how it ended (added 2026-10-26)
- **Runs.** 39 packets sent by the Developer (38 GC, 1 masked P+R resend), all replies from gpt-6.1-sol; 37 P+R
  replies reused from round 6's P+R search. Pilot 12 runs (one setup failure, rerun under a build lock, decision
  O-6), stage 2 64 runs: all 76 valid, none void after leak review, no time limit hit, no compaction. 11 O versions
  made no code change (2 P+R+O, 9 GC+O\*). Median 8.0 minutes per P+R+O run and 6.7 per GC+O\* run; $431 and $430
  recorded (notional, Max plan) (`PILOT_R6B_O.md`; R1899–R1906).
- **Scoring.** As planned, with decisions O-7 to O-12: probes on base and both versions of every run; a blind second
  reading of both versions; one row worker per job under labels X1/X2 (GC) and Y1/Y2 (P+R); a checker (36 of 36
  sampled rulings agree; 14 corrections, origin only); blind severity tags of 7 new errors among 20 anchors (17 of
  20 agree), and a supplementary tag of case 1 typed-name (decision O-11, after the first summary was read). The
  workers' rulings of the earlier versions agree with round 6's on every known product or task error (0
  disagreements), so the same-ruler line equals the primary (R1907–R1930).
- **Result** (`R6B_SUMMARY.md`): O-GC −0.167 (90% interval −0.306 to −0.056; without langchain-model-update −0.147;
  without case 6 −0.118; seeded line −0.111): "adds something", by the rule fixed in advance. O-P −0.083 (−0.222 to
  +0.028; without case 6 −0.029): no clear difference, near the ceiling computed before the runs. Level +0.069
  (−0.167 to +0.319). Harm: GC+O\* had 9 run-level removals of a major error and 3 additions, a net of 6 removals, all of
  the net in four jobs (case 3, case 6, case 9, langchain-model-update; case 1 had 2 of each and netted zero); P+R+O brought in 1 and removed 4.
- **Fragility, stated in the report:** the without-case-6 condition is one run-level removal from failing; had
  typed-name been tagged major, or case 3 O1 minor, O-GC would read "no clear difference".
- **Checks.** The report's internal check (8 findings, all taken) and one outside reading of packet-29 (ACCEPT WITH
  SMALL CHANGES; every main figure recomputed independently, no error) (R1931–R1934).
- **What followed.** By §2's rule the outside review becomes a core GC step, at least for the kinds of job where it
  helped. The Developer decided: "Make the outside review a standard GC step for difficult or consequential changes
  (with broader triggers than now) and an easy option for routine fixes; first try the real instructions on a few
  jobs" (R1935). Step D was not run: narrowing GC's scope rule without a further test and running no more large
  experiments was the Guide's recommendation, and the Developer agreed: after the Guide's analysis the Developer asked "do we need the trial that is running now?" and, after the Guide's plan (finish the trigger check, skip the send step, fold the narrowed scope rule into 1.4, then one small trial of the full 1.4), replied "that sounds good" (R1937; row 67).

### 1.12 The GC 1.4 trial (2026-10-26; an implementation check, not an experiment)
- **Purpose** (the outside reader's point 4A; REPORT_R6B_O_RESULTS §5): before changing GC, try the actual proposed
  outside-review instructions on a few representative jobs, to confirm that the packet carries what the reviewer
  needs and that the developer gets a clear account. No arm is compared, no rows are ruled and nothing is counted.
- **What was tried:** the `/gc` 1.4 draft (`walkthrough/gc_rev23/`): a trigger H ("hard change") that makes the
  outside review a standard step, optional and offered for other jobs; after trial 1, a narrowed scope rule (fix real
  defects in the code the job changes and the paths it calls; ask only before changing interfaces, defaults, formats
  or behaviour callers rely on outside that code) and "finish before you report".
- **Trial 1** (trigger check, 1.4 draft without the scope and finish changes): fresh g1 runs of o03-mmm-followups,
  o09-ebadf and langchain-model-update (H expected) and auto-q1-a (routine; H not expected). Send step skipped.
- **Trial 2** (full 1.4 draft): fresh g2 runs of the three H jobs; the Developer's send step; the resumes.
- **Questions asked of it:** does H fire where expected and not on a routine job; does the review file carry the
  task, why the change is hard, the full diff and the tests; does the session end on its final report; are review
  findings handled, with tests; is the developer told plainly what remains.
- **Result** (`TRIAL_1.4.md`; R1939–R1942): H fired in the three H jobs and not in auto-q1-a; trial 1 found three
  faults (a session ended before writing its review file; another left a wait loop running; a packet listed review
  fixes not kept under the old scope rule), which the draft's changes addressed; in trial 2 all three runs wrote the
  review file and ended on the final report, every finding was handled with a test, and the reports name what
  remains. "The 1.4 draft works as intended on these jobs."

---

## 2. Jobs

### 2.1 Stages 1 to 3: the ten original cases
- **Stages 1–2 (cases 1–5) and case 9:** no screen or shortlist is in the record. The five named cases match four of
  the tally's five "examples where a later layer caught what earlier ones passed" plus mmm_followups; ebadf is the
  tally's one direct before/after comparison, used first for calibration (`walkthrough/STEP2_RULES_AS_USED.md`).
- **Stage 3 rule** (`stage3_prep/BRIEF_STAGE3.md` lines 6–13): product code in phenix, phenix_regression or
  cctbx_project (including `libtbx`); a GC+ review layer caught a real behaviour defect in an earlier candidate,
  which was fixed; the defect can be shown offline by a probe through real entry points, independent of GC+'s
  design; the starting commit exists.
- **Exclusion:** zombie was dropped under its pre-declared stop condition: inside the sandbox `/bin/ps` is refused
  (R142–R146). Elbow replaced it, found by trying candidates in a fixed order (`packet-10/SELECTION.md`; R151).
- **Selection bias found later:** six of the ten were the tally's showcase examples; all nine bug-fix cases had a
  subtle defect against 8 of 17 eligible unchosen jobs; direction towards GC+ (`walkthrough/STEP2_SELECTION.md`).
  Case 6 fails the bug-fix filter (new kit tool).

### 2.2 The bug-fix screen (walk-through step 2)
Three blind helpers classified the 85 records under definitions approved with the plan; the Guide merged them and
spot-checked 10 rows. Chain: 85 records → 95 jobs → 45 bug fixes → 44 GC+ jobs → 36 replayable offline and probeable
(40 counting "unclear") → 25 with a GC+ catch in its own work (29) → 8 (9) already replayed (STEP2_SELECTION.md;
R226–R231).

### 2.3 Round 4: every remaining suitable job
- **Planned:** 28 jobs (group A 17 with a GC+ catch, group B 11 without) plus 2 "unclear" (group C), each tried and
  dropped with a reason if it could not run offline (`REPLAY_ALL_PLAN.md`, "Which jobs").
- **Prepared:** 30 (r4_prep/CASES.tsv; R296). Each prep helper reported SUITABLE or UNSUITABLE; the Guide ruled on
  every input question (R298–R596).
- **Excluded, with reasons (3):** gc-app-version-check (needs a live Claude app session; R494–R497); batch4-q4b-a
  (setuid `/bin/ps`, real Linux; R537–R541); gc-linux-container (Linux container only; R543–R545).
- **Result:** 27 new cases plus the 10 originals = 37 jobs, "a census of the suitable jobs, not a random sample"
  (Src4 §1). Frozen in packet-16 (R871–R872).

### 2.4 Hard, medium and easy (round 4b)
- A job's group is the number of draft errors GC+'s layers caught and fixed in it, from GC+'s own record: hard 3 or
  more (9 jobs), medium 1–2 (9), easy none (19) (Src4 §3; R1117–R1123).
- **The cut-offs were chosen after the round-4 figures were seen** (Src4 §3). Later rulings moved
  langchain-cap-fix from medium to easy and left langchain-model-update at exactly 3.
- "Caught any" (hard + medium, 18 jobs) is the steadier split; it is the population of rounds 5 and 6.

### 2.5 Round 5 and round 6
- **Round 5:** the 38 plain runs of the 18 caught-any jobs, fixed in `r5_plan/RUNS.txt` before the pilot (Src8 §2).
  auto-q2m-c is not a caught-any job.
- **Round 6:** the same 18 jobs, 2 fresh GC runs each (4 for case 1): 38 runs; plus 2 runs of langchain-cap-fix for
  mechanics only (PLAN_ROUND6 §3, §7; `r6_tools/RUNS_R6.json`: 40 runs, 19 slugs). The other 19 jobs are an optional
  stage 3.
- **Round 6b, step O:** the same 18 jobs and the same 76 counted runs: the 38 P+R runs of rounds 4–5 and the 38 GC
  runs of round 6 (stage main, or pilot and main), not the 2 pilot-only langchain-cap-fix runs; every counted run
  gets one outside review, whatever its earlier result ("no selection", PLAN_ROUND6B_O §3; `r6b_tools/RUNS_R6B.json`).
  Pilot jobs, chosen for mechanical risk: o06-precheck, langchain-gemini-openai and o10-elbow (§7).
- **GC 1.4 trial:** o03-mmm-followups, o09-ebadf and langchain-model-update (caught-any jobs where H was expected)
  and auto-q1-a (a routine job), from the same starting commits and prompts (`r6c_tools/RUNS_R6C.json`); chosen by
  the Guide, not sampled.

---

## 3. Arms

### 3.1 GC+ (all rounds)
GC+'s own final change, not rerun: each job-final commit diffed against its own parent, limited to the job's files
(protocol §2). In round 4 every GC+ patch was rewritten to one root-relative `G_root.diff` without commit headers, so
a blind reader could not tell it by form (R312–R314). Where a job's commits were squashed with others, only the job's
own approved candidate is used (R474–R477).

### 3.2 P and P+R (stages 1–3 and round 4)

**Command** (`packet-7/tools/run_arm.sh`; identical in `packet-16/tools/run_arm.sh` except the time-limit wrapper and
the disk check):
```
claude -p "<prompt>" --model <model> --effort xhigh --restricted
       --tools "Bash,Read,Edit,Write,Grep,Glob,Agent,Skill" --settings <policy.json>
       --strict-mcp-config --permission-mode dontAsk --verbose --output-format stream-json
```
with `GIT_CONFIG_GLOBAL` and `XDG_CONFIG_HOME` set to run-local files, `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` and
`PYTHONDONTWRITEBYTECODE=1`. The logged-in CLI was used; no API key was set (`apiKeySource: none` in every stage 1–3
stream; R366–R369).

**P+R** resumes the same session (`--resume <session id>`, same flags) with the prompt, word for word:
`Invoke the code-review skill with arguments "high --fix --max-findings default" on the current diff, and apply its fixes.`
The Skill-tool form was chosen because the slash-command form gave an empty result in a probe (protocol §3, item 5).

**Prompts.**
- The Developer's original request, word for word where it stands alone, with the original attachments; otherwise
  reconstructed "under the no-fix rule": state the problem, never the fix (protocol §7; R116–R120).
- Every prompt ends: "Work autonomously; do not commit or push; run PHENIX with ./build/bin/<command>." (all 37
  `packet-16/cases/*/prompt.txt`: 30 as a line of its own, 7 at the end of the last sentence.)
- Round 4: "original inputs the GC session had are attached verbatim even with fix hints"; GC+'s own outputs
  (plans, findings, reply buttons the Guide wrote) are withheld (R300, R442–R444, R522–R524). A sentence-level leak
  review of the 27 prompts removed two GC+-written phrases and declared four mild leaks (R827–R841; Src4 §10).

**Model and effort.** The model GC+'s worker used: Fable 5.1 for case 1, case 6, developer-html-link-fallback and
process-raw-data-reconstructed-f, otherwise Opus 5.5; effort `xhigh` (protocol §1; R561; `packet-16/cases/*/RUN_SPECS.json`;
cases 3, 4, 7, 8 and 10 assume Opus 5.5, a stated limit, STEP1_FAIRNESS.md). Stage 1–3 streams: 12 Fable, 32 Opus, all Claude Code
2.1.284. Round-4 runs: Claude Code 2.1.303, as read from each P stream by `r6_tools/r6_runs.py` for the 8 round-4
caught-any jobs (`RUNS_R6.json`; R1717).

**Time limits.** 90 minutes for P and 45 minutes for P+R; exit 142 marks the limit, recorded as an outcome, not
repeated (protocol §4). Round 4 replaced the `perl alarm` wrapper with `limit_run.py`, which kills the whole process
group (R450–R453). Round-4 rule: a run that hits its limit while the load average was above 8 is rerun alone
(REPLAY_ALL_PLAN, "Parallelism").

**Runs.** Stage 1: 4 runs of case 1, one at a time (`stage1_driver.sh`). Stages 2–3: 2 runs per case. Round 4: 2 runs
per new case (54), up to 8 at a time behind load, memory and disk gates (`packet-16/tools/run_all.py`). The ten
originals' plain runs were not rerun; 76 plain runs are counted in all (Src4 §1).

**Freezing.** `git add -A`; the scored diff is the change under `modules/` only; other changed paths are listed in
`<run>.<arm>.unscored_paths` and reviewed (protocol §4.4).

### 3.3 P+2R and P+R+S (round 5)
- **How** (Src8 §4; `r4_tools/run_prs.sh`): rebuild the installation at the run's original path; pin unpinned
  repositories to the state at P's start (from the reflog); apply the frozen P+R diff and check it byte for byte; then
  `claude -p <prompt> --resume <P+R session> --fork-session` with the run's flags, `DISABLE_AUTOUPDATER=1`, the
  current binary (2.1.303). The two arms of a run never run together; the run's temp folder is restored from a copy
  before each arm.
- **P+2R prompt:** the P+R prompt, word for word.
- **P+R+S prompt:** a six-step wrapper (criteria from the task text first, an evidence folder, one general-purpose
  reviewer subagent briefed from a template, fix or say why for every finding, at most one re-reading, a proving test
  where feasible, findings listed in the final message) with a generic reviewer brief derived from 12 GC+ reviewer
  briefs by an agent that had not seen the ledger (`r5_brief/GENERIC_REVIEWER_BRIEF.md`). The full text is in R1415–R1496
  and its hash in `r5_plan/FROZEN.sha256`.
- **Time limit:** 60 minutes for both arms. **Order:** one random interleaved order of all 76 (run, arm) jobs, seed
  20261021 (`r4_tools/r5_driver.py`). **Concurrency:** 4–6 planned.
- **Pilot:** o10-elbow p1, process-raw-data-reconstructed-f p1, precheck-p1, both arms, mechanics only; pilot diffs
  not opened until all runs were done (Src8 §5).

### 3.4 GC and GC+O (round 6, as planned and as built)
- **Installation:** as P's, with the round-5 pins; the frozen skill and notes are placed before `make_run_r6.sh`
  commits the base, so they are never in a scored diff; `modules/guided_coding` is neither linked nor readable
  (PLAN_ROUND6 §4.1, §4.7b).
- **Binary:** each job's own P binary, 2.1.284 for the ten originals and 2.1.303 for round-4 jobs
  (`RUNS_R6.json`: 22 runs on 2.1.284, 18 on 2.1.303); `DISABLE_AUTOUPDATER=1`. Model and effort as P.
- **Skill:** `/gc` 1.3 at 14b8371, five files, frozen in `r6_tools/gc_frozen/`; loaded as a plugin inside the run
  (`--plugin-dir <run>/.claude/gc_plugin`, decision C) because `--restricted` ignores project skills.
- **Notes** (`gc_frozen/GC_NOTES.md`): scratch folder `work/gc_scratch/`; one session at a time, in-place swaps
  allowed; outside reviewer ChatGPT; no job log, no full suite; never commit or push.
- **Prompt:** `/gc`, then P's prompt word for word, then a fixed paragraph standing in for the Developer
  (`gc_frozen/PROMPT_SUFFIX.txt`): nobody answers questions; take the answer that keeps to the task and say so; never
  approve a change beyond the task, an interface or default change, or an irreversible step; do the whole task as one
  job; do not act on recommendations.
- **Flags:** as P (`--restricted`, same tool list, `dontAsk`, policy by `--settings`), plus `--plugin-dir`. The claude
  process gets a whitelisted environment (`env -i` with HOME, USER, PATH, LANG, TMPDIR and the run-local settings), so
  no provider key reaches it (`r6_tools/run_gc.sh`).
- **Configuration:** the default configuration, as P had; the user-level `/gc` link is moved out of `~/.claude/skills`
  while runs go and restored afterwards (decision A).
- **Time limits:** 240 minutes for GC and 90 minutes for the GC+O resume, "long enough that it is not likely to ever
  get hit" (decision 5; PLAN_ROUND6 §4.7).
- **GC+O** (decision B, `r6_tools/run_gco.sh`, run later by the Developer from a key-loaded Terminal): if GC wrote
  `work/gc_scratch/OUTSIDE_REVIEW.md`, `outside_review.py` replaces personal names and e-mail addresses, refuses
  key-, token-, password- or home-path-shaped content, removes the simulated-Developer paragraph and sends the file to
  the OpenAI API (model `gpt-6.1-sol`, reasoning effort high, output limit 32,000 tokens;
  `outside_review_config.json`). The installation is rebuilt, GC's frozen end state restored and checked, and the
  session resumed with `--fork-session` and a fixed prompt plus the reply. Without an outside review, GC+O = GC.
- **Concurrency:** 3 at a time (R1718, R1721).

### 3.5 Outside reviews inside the arms
- **GC+:** its own jobs had outside readings by Claude or ChatGPT ("Generally, I used chatgpt for consequential
  outside reviews and claude for small ones", R253), and the Developer's live probes. Their catches count for GC+.
- **P, P+R, P+2R, P+R+S:** none.
- **GC+O (round 6):** the simulated outside review above. The same script is also run once on each P+R run's final
  change as a search instrument, not an arm (decision 10; driver mode `prsearch`).
- **P+R+O and GC+O\* (round 6b, step O):** the outside review is the treatment (section 3.6). Both arms get a reply
  built by round 6's `pr` recipe from the task text and the final diff; P+R+O's replies are round 6's P+R search
  replies, given back to the session for the first time.
- **GC 1.4 trial:** GC's own OUTSIDE_REVIEW.md, sent by round 6's `run_gco.sh` (section 3.7).

### 3.6 P+R+O and GC+O\* (round 6b, step O; PLAN_ROUND6B_O §3–§5)
- **The reviews, one recipe for both arms:** round 6's `outside_review.py pr` mode (task text from
  `packet-16/cases/<slug>/prompt.txt`, not GC's `/gc` prompt, and the final diff, in GC's review-file form with GC's
  request; names, home paths and key-shaped text cleaned; gpt-6.1-sol, reasoning effort high, one turn, no tools),
  called through `send_r6b.py`, which adds only a fixed, logged masking step: a span the key filter refuses is
  replaced by `<masked-key-shaped-text-N>` and the packet checked again (`MASKED.json`). Needed once:
  langchain-gemini-openai p2's P+R packet (one span, 19 characters; decision O-4).
  - **P+R:** the 37 replies of round 6's P+R search, copied with their hashes (`r6b_driver.sh prep`); the 38th sent
    with its placeholder masked.
  - **GC:** 38 new replies, built from each GC run's frozen `GC.diff` with the same recipe (not from GC's own
    OUTSIDE_REVIEW.md).
  - **Sending:** `r6b_driver.sh send`, run by the Developer in the key-loaded shell; 39 sent, 0 failed; every
    `sent.txt` equals its dry-built packet (R1902).
- **The message** (both arms; `r6b_tools/MESSAGE_O.txt`, frozen): "Here is an outside review of your change. Handle
  each finding as your instructions say, then give your final report. This approves no commit, push, live call or
  other irreversible step.", a blank line, and the reply exactly as received. Each arm's instructions are its own:
  GC's `/gc` with round 6's stand-in paragraph (so its scope rule still applies), P+R's task prompt.
- **GC+O\*** (`r6b_tools/run_gco_all.sh`; new, round 6's `run_gco.sh` not used): forks the stored GC session
  (`<run>.GC.sid`, before any round-6 outside review); rebuilds the installation with `make_run_r6.sh` and decision H's
  attachment; restores GC's frozen end state (`GC.diff`, `GC.scratch`, `GC.tmp.tgz`) and verifies it against
  `GC.diff` with `index` lines ignored; reads only its round-6b reply and refuses to start without it. Binary, model,
  effort, flags, plugin, policy generator, whitelisted environment and guards as round 6's `run_gc.sh`. Outputs
  `<run>.GCOS.{jsonl,diff,stat,scratch,sid}` in `replay/r6b_out/<slug>/`.
- **P+R+O** (`r6b_tools/run_pro.sh`): installation as P+R's (`make_run_pro.sh` = r4's `make_run.sh` without
  `modules/guided_coding`, decision O-3; `setup_extras.sh`; decision H's attachment); P+R's end state restored
  byte-identical to its `pr_diff`, then unstaged (`git reset -q`); the temporary folder from round 5's pre-round-5
  snapshot (`r5_out/tmp_snapshots/<run>.tgz`; not P+R's own end state, a stated limit); forks the stored P+R session
  (round 5's RUNS.json sid) with the run's own binary (2.1.284 for the ten originals, 2.1.303 for round-4 jobs; the
  pilot showed 2.1.284 resumes its own sessions, so no fallback was used). The CENV, flags (no `--plugin-dir`),
  policy generator and guards of `run_gc.sh`.
- **Both arms:** `--resume <sid> --fork-session`; limit 90 minutes (`limit_run.py`); one rebuild at a time under a
  build lock (decision O-6); interleaved in `RUNS_R6B.json`'s order, 3 at a time; `scan_r6b.py` after every batch
  (how each stream ended, sandbox or Bash failures, compactions, cost). Invalid or limit-stopped runs rerun from the
  frozen state; a run not possible after two tries scored as its earlier version and listed (none occurred).
- **Pilot** (§7; `PILOT_R6B_O.md`): 12 runs with acceptance items: precheck-p2's unanswered tool call resumes;
  restore verified; temporary and untracked files present or the gap recorded; stored session unchanged and fork id
  new; the review acted on in the cut-short case-6 sessions; compactions; Bash working; start-up lists the same apart
  from `gc`; no commit or push; validity; the O diff written. Pilot runs count if they pass; their diffs are not read
  for results.

### 3.7 The GC 1.4 trial (implementation check)
`r6c_tools/` holds copies of round 6's `run_gc.sh`, `run_gco.sh` and driver with outputs in `replay/r6c_out/`, the
run list `RUNS_R6C.json` and `gc_frozen/` = the 1.4 draft; "otherwise round 6 unchanged" (driver header). Fresh GC
runs with round 6's binary, model, effort, flags, plugin loading, policy, whitelisted environment and stand-in
paragraph; the outside review is GC's own OUTSIDE_REVIEW.md, sent by the Developer (`r6c_driver.sh gco`) and handed
back by round 6's GC+O resume. Frozen in `r6c_tools/FROZEN_R6C.sha256` (20 entries) before the runs; dry runs passed
(R1936). Trial 1's outside reviews were not sent; the 1.4 draft was changed between trial 1 and trial 2 (row 82).

Outside reviews **of the study itself** are in section 7.

---

## 4. Isolation and fairness

### 4.1 A separate installation per run (all rounds)
- **Why:** PHENIX runs from build_39, which already holds every fix and its tests (STOP_1.md). The Developer chose a
  second installation per case (option A) on 2026-10-15 (R23–R24).
- **What** (`make_run.sh`): a copy of `build_39/build` with every text file rewritten to name the run; `conda_base`
  linked; a snapshot of each changed repository at its starting commit (`git archive`, with LFS content); links to
  build_39 for other modules (from round 4, directories only, so the untracked `modules/CLAUDE.local.md` is not
  linked, R320–R323); one git repository at the run root for the freeze; attachments copied before the base commit.
- **Rebuild** with `libtbx.scons` where compiled code changed after the base (`needs_rebuild`).
- **Feasibility** was shown for case 1 (protocol §3) and, per case, by "ENV_CHECKS" before each case's first run
  (in-process imports, dispatchers, csh job files that source setpaths, multiprocessing workers;
  `stage2_prep/*/ENV_CHECKS.md`).

### 4.2 Read denial (policy)
Written fresh for each run by `make_policy.py` and passed with `--settings` (protocol §3):
- **Sandbox `denyRead`:** all of `~`, `/private/var/folders`, `/Volumes`, every other entry of
  `/private/tmp/claude-501` (listed when the policy is written), the build_39 copies of the changed repositories, and
  `phenix/.claude`; from round 4 also `build_39/modules/.claude` and `modules/CLAUDE.local.md` (R819–R821).
- **Allowed:** the run folder, `conda_base`, `build_39/modules`, the run's own temp subfolder.
- **File tools:** no reads outside the working folder; changed repositories and records denied; web tools removed;
  no network (PROBE_11: `curl` refused, urllib failed).
- **Round 5:** GC+'s kit in cctbx_project denied, except in runs whose change touches the kit (case 6,
  gc-next-revision) (Src8 §4.4; decision 4).
- **Round 6:** additionally `modules/guided_coding` denied; a run refuses a policy over 50 KB (decision G).
- **Round 6b, step O and the GC 1.4 trial:** round 6's policy generator for both arms; in P+R+O the guided_coding deny
  where `kit_changed` is False, as round 5's KITARG; dry-run policies 13.9–14.6 KB (decision O-5).
- **Negative controls** (PROBE_3 to PROBE_12): Read, Grep, Glob, an Agent subagent's shell, writes through links into
  build_39, network and other sessions' temp folders were refused under the final policy; PHENIX ran the snapshot.

### 4.3 Leak checks
- **Every stream** is scanned for successful reads of denied places (void), refused reads (counted) and answer markers
  chosen before the run (judged in context) (protocol §4.5).
- **Round 4:** `leak_check2.py` marks void suspects; markers that occur in the given inputs, match the run's own name
  or already occur in the starting code are dropped and listed (R309–R311, R804–R806, R851–R853). A Guide-side
  `leak_review.py` then reclassifies suspects (REAL / REVIEW); a run is void only on a REAL read of GC+ material
  (R895–R897, R966–R969).
- **Round 5:** `leak_review_r5.py`: void only if a read-like call returned content from GC+'s records, procedure
  texts, this study's outputs, another run or Downloads; kit reads judged on content (decisions 6, 8, 9).
- **Round 6:** `leak_check_r6.py` flags; a reviewed verdict file per run decides (decision D).
- **Round 6b, step O:** GC+O\* as round 6 (`leak_check_r6.py`, a reviewed `.GCOS.leak_review.json` per flagged run).
  P+R+O by round 5's rules: `leak_check_r5.py` with round 5's KITARG, then `leak_review_r6b.py`, a copy of
  `leak_review_r5.py` in which GC material also includes `modules/guided_coding`, the `/gc` skill and its frozen
  copies, and the round-6 and step-O outputs; void only if a read-like call returned content from GC material,
  this study's outputs, another run or Downloads. Results: 4 suspects in 2 pilot GC+O\* runs and 2 in stage 2, all
  inside the run (own tool-results file, empty CLAUDE.md searches, a temporary git experiment, own scratch test
  script), none void; P+R+O ok for all 38 (PILOT_R6B_O.md; R1905).
- **Results:** no run void in stages 1–3, round 4 or round 5. Known exposures: case 7 p2 read a later phenix chat helper
  (judged not a leak, reported); three round-4 runs read git history in a repository the case did not change (kept,
  REVIEW) (`walkthrough/STEP1_FAIRNESS.md`; R892–R894, R967–R969).

### 4.4 The whitelisted environment and keys
- **Stages 1–5:** no API key in the environment; the logged-in CLI; probes run with every proxy variable pointed at a
  dead local port and API-key variables unset (`score_diff.sh`; R588).
- **Round 6:** the OpenAI key exists only in the Developer's Terminal; the driver passes it only to the outside-review
  script and runs every claude process with a whitelisted environment (PLAN_ROUND6 §10, "How the API key is set";
  `run_gc.sh`).
- **Round 6b and the GC 1.4 trial:** as round 6. The send step (`r6b_driver.sh send`, `r6c_driver.sh gco`) was run by
  the Developer in the key-loaded shell; the Guide never saw the key; every claude process of both step-O arms ran
  with round 6's whitelisted environment (P+R+O included, unlike the original P and P+R runs; row 57).

### 4.5 Hidden material
- **From the arms:** GC+'s records, diffs, tests and later code (the changed repositories in build_39), GC+'s kit
  briefs (from round 5), the study's own files, other runs' folders, Downloads.
- **From blind helpers and readers:** which diff is which arm. Probe writers in round 4 saw the task, bug report and
  starting code only (`r4_blind/BRIEF_R4_BLIND.md`; R296); readers saw diffs under random labels; ledger workers in
  rounds 5 and 6 ruled under the labels L1 / L2 with the key in a folder they must not open (Src8 §7.5;
  `round6/BRIEF_R6_ROWS.md`).
- **From the severity tagger:** arm names (stripped from descriptions; section 5.5).
- **Round 6b, step O:** from the row workers, which version of each run is the O version: labels X1/X2 (GC) and
  Y1/Y2 (P+R) in random order, key in `r6b_out/<slug>/blind_key/KEY_R6B_O.json`, which they were told not to open;
  the known-error list without arm, run or end (decision O-7). The g and p runs are named, so the arm is known; the
  question is earlier against O version. Final messages can reveal which version handled the review (accepted, as
  in round 6). From the checker, the same key. From the severity taggers, arm, run and source.

### 4.6 Fairness checks of inputs
- **Walk-through step 1** (`STEP1_FAIRNESS.md`): per case, leaks, model, kit revision, handicaps on plain (48
  permission-mode refusals and a few sandbox refusals over 44 streams), and the prompt against the original request.
  Advantages outside GC+'s rules: to GC+ in cases 4, 5, 8, 10 (the Developer's mid-job decisions; Linux and t96 in case
  10); to plain in cases 6 and 7 (a narrower task; GC+'s framing).
- **Prompt-hint check of the ten originals** (`PROMPT_HINTS_FIRST_TEN.md`; R1276–R1279): no fix, cause or location the
  Developer gave GC+ was withheld from plain.

### 4.7 Run-script guards (round 6b, step O)
Both step-O run scripts (`run_gco_all.sh`, `run_pro.sh`) stop before Claude starts when:
- the run's own step-O reply (`r6b_out/<slug>/<run>.O/reply.txt`) is missing; no other reply is read;
- the user-level `/gc` link is in `~/.claude/skills` (the driver moves it out while runs go and puts it back after);
- the policy is 50,000 bytes or more (decision G);
- a GuidedCoding file is in the run: in P+R+O, `.claude/skills/gc`, `.claude/gc_plugin`, `.claude/GC_NOTES.md` or
  `modules/guided_coding`; in GC+O\*, `modules/guided_coding`;
- the restore does not match the frozen end state (GC+O\*: `GC.diff` with `index` lines ignored; P+R+O:
  byte-identical to `pr_diff`) (exit 5);
- the stored session is missing (exit 8); disk space is short (exit 3); setup, the rebuild or the temporary-folder
  restore fails (exit 4); the run is locked by another attempt (exit 9).
After the session they stop if the stored session's SHA-256 changed or no new fork id appeared (exit 8). They also
take the build lock around scons (decision O-6; the driver removes a stale lock when no scons runs), pass decision
H's attachment (decision O-2), run the fixed-Python sleep check and `validate_r6.py` with the network log, move a
run that hit a limit or failed validation aside (`limit/`, `invalid/`) for a rerun, and write only under
`replay/r6b_out/`. The driver refuses to send or run if any file in round 6's `FROZEN_R6.sha256` or in
`FROZEN_R6B.sha256` differs from its hash (decision O-1).

---

## 5. Scoring

### 5.1 Probes
All probes run in a fresh scoring installation holding the arm's code, never in the run installation. Outcome words
(protocol §5.3): present, absent-handled, absent-by-design, N/A, not-done.

1. **GC+-catch probes (stages 1–3; reused in every later round).** One executable item per defect GC+'s layers caught
   in GC+'s own drafts (`score_<case>.py`), behaviour-only through real entry points and independent of GC+'s design;
   design-dependent items go to the scorer. They can only find errors in plain code, since GC+ fixed them
   (Src4 §6). Calibrated before any run on the known versions (GC+'s candidates, its final, the base and seeded
   controls): every expected call must match (calibration-1, -2, -3; R98–R99, R128–R130, R147–R153).
2. **Blind task probes (round 4; the main round-4 measure).** Written by a helper from the task, the bug report and the
   starting code only; items R (the reported problem) and E (edges and regressions); calibrated to fail on base and
   pass on a correct fix or a seeded alternative; run on GC+ and every plain arm, including the ten originals' frozen
   diffs (REPLAY_ALL_PLAN item 1; `packet-16/blind/<slug>/task_probe.py`, `CALIBRATION.md`). Before freezing, every
   original was cross-checked against the existing ledger and GC+ was scored with every new probe: "no probe is unfair
   to G on an R item" (R843–R849, R857–R861).
3. **Cross-arm probes (round 4b; reused in rounds 5 and 6).** Every candidate error from any source (the ledger, both
   readings, the review passes, the commit audit, GC+'s record) written as a behaviour probe and run on base, GC+ and
   every plain arm; calibrated present where reported and absent where fixed; a code-reading verdict for every arm where
   no probe can show it (`r4_ledger/BRIEF_R4B_CROSS.md`; `walkthrough/r4_cross/<case>/`).
4. **Round 5:** all existing probes on P+2R and P+R+S; every finding of P+R+S's reviewer and of P+2R's review, fixed or
   not, probed on every arm; round-5 cross probes (`r5_rows/<case>/cross_probe_r5.py`) (Src8 §7).
5. **Round 6 (planned):** the task, GC+-catch, round-4b cross and round-5 cross probes on GC and GC+O; new candidates
   from both readings, GC's code-review findings, outside-review findings, problems GC's report names, and the P+R
   outside-review search, probed on every arm (PLAN_ROUND6 §5.1–5.3; `r6_tools/r6_score_driver.py`).
6. **Round 6b, step O:** every round-6 probe (task, GC+-catch, round-4b cross, round-5 cross and each job's
   `cross_probe_r6.py`, each where it exists) run on base, the earlier GC and P+R versions and the O versions **in one
   installation per job** (decision O-8; `r6b_score_driver.py`, `run_on_arms_r6b.py --r6b-read`), so each pair is
   judged by the same probe at the same time. An O version identical to its earlier version (apart from `index`
   lines) is not an arm; it takes that version's calls. New candidates are probed by the row workers in
   `rows/<slug>/cross_probe_r6b.py`, through real entry points, calibrated present where the error is and
   absent-handled where it is fixed, with `run_on_arms_blind_r6b.py`, which reports calls under the run labels.
   The step-O scoring tools are generated from round 6's frozen ones by fixed text changes (`make_r6b_scoring.py`).
- **Network guard:** probes run with proxies dead and keys unset; LLM probes use fakes; a probe that cannot judge a
  design reports "not judged" (R723–R728).

### 5.2 Test adequacy (round 4b on; Src26)
Each arm's own changed test files are run on four versions: its own code, the starting code, a blind seeded correct
fix and a blind seeded partial fix (`r4_tools/test_adequacy.py`; per-test limit 900 s). Only tests that pass on the
arm's own code are judged. **"A test that proves the bug"** = fails on the starting code and passes on the arm's own
code; a base failure caused only by the kit's source-integrity check does not count (from draft 3). The seeded-fix
states are reported as a limit, because most tests bind to their own design. Round 5: own and base only. Round 6
(planned): all four states. Round 6b, step O: all four states on the O versions only (`test_adequacy_r6b.py
--only-r6b`); the earlier versions' tests are round 6's (decision O-8).

### 5.3 Readings
- **Stages 1–3:** a blind checklist scorer per case (stripped checklist, task text, diffs under random labels; it also
  guesses the labels) and an open-ended reader with no checklist (protocol §5.2, §5.6), both Opus 5.5
  (STAGE3_RESULTS.md).
- **Round 4:** a blind open-ended reader of every arm's diff under random labels, and a blind checklist scorer
  (`readings_r4.py`; Opus 5.5, xhigh, Read/Grep/Glob only). Readers get the case's attachments, never GC+'s or the
  record's files (R802–R803).
- **Round 4b: the second blind reading** (`readings2_r4.py`): checklist-driven, given the bug report, attachments and
  the starting source of every touched file (Src4 §1).
- **Round 5:** the same second reading over GC+, every P, P+R, P+R+S and P+2R (`readings2_r5.py`). **Round 6
  (planned):** two blind readings with GC and GC+O added (`readings2_r6.py`). **Round 6b, step O:** one blind second
  reading of each job's earlier GC and P+R versions beside their O versions, under random labels
  (`readings2_r6b.py --r6b-read`); its labels are mapped to the run labels in each job's blind folder.
- **Recall check:** the round-4 blind reader named 55% of the first ten's program errors (77% counting partial
  matches); one blind reading finds about half the errors (`BLIND_RECALL_FIRST_TEN.md`; Src4 §6).

### 5.4 The error ledger and its rules
- **One row per significant error, per arm and run** (`walkthrough/build_error_ledger.py`; `r4_ledger/BRIEF_R4_LEDGER.md`).
  Fields: case | arm | run | id | what | **kind** product / test / task / scope | **origin** pre / own / review |
  found_by | **end** fixed / remains / fixed-later / deferred | **evidence** confirmed / probable / undetermined |
  source.
- **Origin:** pre = already in the starting code; own = made by the arm; review = brought in by a review pass.
- **End:** fixed (in the arm's own process), remains (at the end point), fixed-later (by a later job), deferred (found,
  left on purpose and disclosed: in GC+'s record, or in a plain run's final message).
- **Evidence:** confirmed = shown by a probe, a test or reading the code; probable = strong but not shown (for example
  a model-table call); undetermined = never counted.
- **Kind:** task = the reported problem not fixed; product and test as named; scope = a design or scope difference,
  never counted.
- **Headline count** (from 2026-10-21; Src4 §2): confirmed rows of kind task, or product with origin own or review,
  that remain or were fixed later. Deferred rows, pre-existing faults and scope items are reported apart.
- **Rulings** by the Guide, applied at merge (`r4_ledger/RULINGS.md`, `R4B_RULINGS.tsv`, `R4_CORRECTIONS.tsv`,
  `ORIG_CORRECTIONS.tsv`), among them: disclosure in an arm's own final report counts as deferred for every arm;
  the P → P+R carry-over (a problem P disclosed stays disclosed in P+R unless fixed; `CARRY=0` gives the old rule);
  probe artefacts dropped and listed.
- **Workers** turned evidence into rows in batches (A–F, the originals), confirming reader claims by reading or running
  code; wrong claims were dropped and listed (R980–R998).
- **Rounds 5 and 6:** rows for the new arms ruled under labels L1 / L2 (`r5_plan/BRIEF_R5_ROWS.md`;
  `round6/BRIEF_R6_ROWS.md`); new errors found in old arms are added to those arms ("depth rows"); disclosure from the
  final message only (round-5 decision 13); known errors keep the ledger's origin (decision 14).
- **Round 6b, step O** (`walkthrough/round6b/BRIEF_R6B_ROWS.md`; decisions O-7, O-9, O-12):
  - **One row worker per job** rules both versions of every run, from scratch, under X1/X2 (GC) and Y1/Y2 (P+R),
    against `KNOWN_ERRORS.tsv` (the job's known product and task errors from round 6's updated ledger, without arm,
    run, end or severity) and the probe calls; earlier rounds' probe verdict files map probe items to error ids.
    Earlier rulings bind (round 6 decision J); the strict disclosure rule applies (only a plain statement in that
    version's final message that this specific problem is left).
  - **New candidates** only from: `r6b-read2` (the second reading: major, or minor with medium or high confidence),
    `r6b-out` (the run's outside review), `r6b-rev` (the session's own review pass), `r6b-rep` (problems a final
    message names as left or unchecked); `r6b-probe` for errors a probe found. Duplicates merged, keeping the
    earliest source in that order. New ids `O<k>`; found_by starts with the first source's token.
  - **Origin "outside"** (plan §6): an error in only one version of a run whose cause lies in hunks only that version
    has. From o02-atomic on, and for the earlier jobs through the checker's corrections, also: a version that lacks
    its partner's fix of a base fault (decision O-12). An "outside" error that turns out to be in an earlier version
    counts as that version's own (O-9).
  - **Identical diffs:** where both versions' diffs are equal apart from `index` lines (`LABELS.md` says so), presence
    is the same; disclosure is still read from each final message. 11 O versions were identical (2 P+R+O, 9 GC+O\*; R1906's "12" was a miscount in the record).
  - **Output per job:** `rows/<slug>/ROWS_O.tsv` (one row per error, run and label where present or disclosed),
    `VERDICTS_R6B.tsv` (every verdict, with how judged and an "only in" column), `NOTES.md`, and where needed
    `ROWS_SENSITIVITY.tsv` and the probe with its calls. Workers ran 2 at a time, in the order of `rows/ORDER.txt`,
    and wrote only in their job's rows folder.
  - **Same-ruler check** (O-9; `disagree_r6b.py`): every known product or task error where a worker's ruling of an
    earlier version differs from round 6's ruling of that version, left against not left, goes to the checker.

### 5.5 Severity tagging
- **Rubric** (Src4 §2): **major** = in normal use gives wrong results or output silently, crashes or hangs a normal run,
  loses or overwrites data, is a real security problem, or leaves the reported problem unfixed; for a test, no test
  that would fail if the bug came back. **Minor** = any other real error.
- **Round 4b:** 205 distinct errors that some arm left at the end point. First tagging (R1155–R1159) from `ITEMS.tsv`,
  whose source column named arms; a second tagging from `ITEMS_BLIND.tsv` with arms stripped (49 major, 153 minor, 3
  not an error) became primary (R1197–R1212). Agreement 87%, κ 0.64. Six descriptions that still named an arm were
  re-tagged from neutral wording; three moved to major; no headline figure moved (R1243–R1246).
- **Round 5:** 32 new errors tagged blind once, with 20 anchor items (agreement 80%) (Src9, "Other limits").
- **Round 6 (planned):** new errors tagged once, blind, with anchors (PLAN_ROUND6 §5.7).
- **Round 6b, step O** (`walkthrough/round6b/severity/`): the same rubric and wording as the second tagging
  (`BRIEF_SEVERITY_R6B.md`); the 7 new product and task errors among 20 anchor items (27 items, `ITEMS_R6B.tsv`),
  tagged once by a blind tagger told not to open the key, the rows or any ledger; anchors agree 17 of 20 (85%).
  Known ids keep round 6's tags. Result: major langchain-model-update O1, case 3 O1, case 1 O1; minor case 6 O1 and
  O2, phenix-chat-tools O1 and O2 (R1927).
  - **Supplementary tag** (decision O-11, as round 6's decision M): case 1 typed-name, never tagged (pre-existing
    until the O step made it "outside" in five O versions), tagged after the first summary was read, among 10 anchors
    (`ITEMS_R6Bb.tsv`, seed 202610263, severity words removed), the procedure written before the tag was known and the
    tag used as given: minor ("a defensible convention"; anchors 8 of 10) (R1929–R1930).
- **Not used:** the Developer's own severity pass and an agreement band were explored and left out at the Developer's
  request (R1297–R1312).

### 5.6 Checker samples
- **Round 4 ledger:** a checker read a 30-row sample, consistency and missing rows: five wrong rows, one asymmetric
  rule (R1001–R1012).
- **Round 5 rows:** 37 sampled verdicts re-examined under labels, 36 agree (`r5_plan/CHECK_ROWS.md`; R1583).
- **Round 6 (planned):** at least 30 GC and GC+O rulings re-examined under labels (PLAN_ROUND6 §5.6).
- **Round 6b, step O** (plan §6: at least 30 O rulings and every flagged item; `rows/CHECK_ROWS_R6B.md`): one checker,
  under the labels, from the existing probe output, diffs and final messages, running no probe; (1) every item on the
  checker list the workers and the Guide flagged; (2) 36 randomly drawn rulings of O versions (seed 6, 2 per job;
  the checker saw only the labels): 36 of 36 agree; (3) `ROWS_O.tsv` against `VERDICTS_R6B.tsv` in all 18 jobs: consistent.
  It made 14 corrections, all to the origin of errors present in one version only, applied before the first summary
  (originals kept as `ROWS_O.tsv.before_check`), and three note fixes; no presence or disclosure ruling changed
  (R1928; row 79).

### 5.7 Other instruments
- **The Developer's commit audit** of Sept–Oct fixes (`DEVELOPER_COMMIT_AUDIT_r03_2026-10-19.md`), first a late-stage
  detector on GC+'s committed work (R254–R261), then applied both ways in round 4b (`AUDIT_VS_R4.md`; R1062–R1064).
- **Claude time** of GC+ estimated from transcripts; plain time is the run's clock time (`GC_CLAUDE_TIME.md`,
  `GC_CLAUDE_TIME_R4.md`; Src27).

### 5.8 Outside readings of reports
The reports' readers are listed in section 7. Their dispositions are files beside each review; changes they asked
for are mapped in Src4 §11.

### 5.9 The step-O summary (round 6b; `r6b_tools/r6b_summarize.py`)
- **Written and hashed before its first run on step-O rows,** and tested on synthetic rows (it reproduces round 6's
  P+R 0.792 and GC 0.972); changed once before that first run (O-10) and re-frozen (O-9, O-10).
- **Rows.** Earlier versions: round 6's updated ledger rows for known errors (primary), plus the step-O rows of the
  earlier label for new ids. O versions: the workers' rows of the O label, unmasked with `KEY_R6B_O.json`.
- **Known ids keep round 6's kind and origin** (O-10): a worker's row for a known id takes kind and origin from round
  6's ledger (same run, else the same family, else any arm) and keeps only the worker's presence and end; an O
  version's "outside" origin is kept. An early-label "outside" is counted as own.
- **Identical O versions:** rows copied only for runs marked identical (the guard against round 6's decision-L fault).
- **Given-up runs** are scored as their earlier version and listed (none occurred).
- **Measure** as round 6: confirmed major program errors left (missed plus disclosed), per run, case-weighted (4 runs
  per arm in case 1); a program error is kind task, or product with origin own, review or outside.
- **Lines computed:** O-P and O-GC with 90% bootstrap intervals over jobs (10,000 resamples, seed 6); without
  langchain-model-update; without case 6; the seeded line; without the cut-short runs; even-handed instruments only;
  the same-ruler line (GCe, PRe: the workers' own rulings of the earlier labels); the level line; the noise reference
  (first runs against second runs); the decision-J sensitivity line (`--with-sensitivity`, `ROWS_SENSITIVITY.tsv`);
  harm by origin; also missed only, all errors left, all errors missed; counts of untagged counted rows, compactions,
  reviews with no findings, and missing or invalid runs. Outputs `R6B_SUMMARY[_SENS].md`, `R6B_LEDGER[_SENS].tsv`.

---

## 6. Analysis rules

### 6.1 Stages 1–3 and the walk-through
- **Units:** k/n per item over runs; "no single combined rate" (protocol §5.5). Stage 1 is an indication only.
- **Walk-through draft 5:** definitions fixed before reading (bug fix; significant error = blocking / real-but-minor;
  subtlety); a disagreement rule (a probe beats the reader; a reader-only claim is probable; flat disagreement is
  undetermined); robustness without cases 6 and 10 and on the 8 product-code cases; "no rates; two runs can't support
  them"; no significance tests (WALKTHROUGH_PLAN.md).
- **Later the same day** at the Developer's request: per-run rates averaged within each case, then across cases
  (R274–R287).

### 6.2 Rounds 4 and 4b (descriptive; Src4)
- **Primary measure:** confirmed program errors missed, per GC+ job or per plain run, averaged within each case and
  then across cases. Beside it: major only; "everything left" (missed plus deferred); test gaps; no proving test.
- **Groups:** hard / medium / easy and caught-any / caught-none (section 2.4), as an association.
- **Robustness and sensitivity lines:** without case 6; without langchain-model-update; other cut-offs (1+ to 4+);
  without the carry-over rule; under the first severity tagging; S179 and S078 minor; auto-q2m-c's stopped runs counted
  as missed; symmetric instruments only (errors first found by instruments that looked at every arm alike), "a
  sensitivity check, not an alternative score" (Src4 §3, §6, §10).
- **No margins, intervals or tests** are applied; the report states associations and small counts (Src4 §10).

### 6.3 Round 5 (pre-registered; Src8 §8)
- **Primary:** confirmed major program errors **left** in the code per run (missed plus disclosed), case-weighted, in
  the 38 runs.
- **Central comparison:** P+R+S − P+2R, paired by run.
- **Reading rule (±0.10):** better if −0.10 or lower overall, and without langchain-model-update, and without the
  affected runs; worse if +0.10 or higher; otherwise no clear difference. The same rule for P+R+S − P+R and
  P+2R − P+R. Unrounded values.
- **Recovery** (P+R − P+R+S) ÷ (P+R − GC+), computed only if the gap is at least 0.10.
- **Ordered hypothesis rule:** Against if P+R+S is not better than P+2R or is worse than P+R; Supported if the gap is at
  least 0.10 with and without langchain-model-update and recovery is 0.5 or more in both; else Inconclusive.
- **Also reported, not deciding:** missed only, all errors, share of runs with any major left, minutes, compliance,
  introduced and removed, the direct test by GC+ layer (`r5_plan/TARGETS.txt`).
- **Fixed in advance:** the analysis script `walkthrough/r5_summarize.py` was written and hashed before any result
  was read (R1512–R1515).

### 6.4 Triage (Src15, Src16)
A permutation test of whether outcome-defined routers beat random routing of the same number of jobs; and a descriptive
check of start screens, not a blind test.

### 6.5 Round 6 (pre-registered; PLAN_ROUND6 §2)
- **Q1 better:** GC+O − P+R is −0.10 or lower, **and** a 90% bootstrap interval over jobs (10,000 resamples of the 18)
  lies below 0, **and** the difference stays −0.10 or lower without langchain-model-update, and separately without case
  6. **Worse:** the same with +0.10 and the interval above 0. **Otherwise no clear difference**, which "does not show
  that the arms are equal".
- **Deciding figures** are the updated ones (every arm measured with every round-6 instrument).
- **Noise reference** beside Q1: P run 1 − run 2, P+R run 1 − run 2, GC run 1 − run 2.
- **Q2** recovery, computed only if the gap is at least 0.10. **Q3** non-inferiority (GC − P+R below +0.10, interval
  upper bound below +0.10), only if stage 3 runs.
- **Sensitivity line:** symmetric instruments only; "if Q1 reads 'better' but this line shows no gain, the summary says
  that the gain rests on candidates seeded from GC's own code."
- **Uncut jobs:** Q1 also on jobs where no arm hit a limit. Time and cost reported apart.
- **What the result leads to:** "better" or "no clear difference": keep GC and say so on the Evidence page; "worse":
  reconsider GC (decision 9).
- **Script:** `r6_tools/r6_summarize.py`, frozen; it reproduces round 5's old figures 0.389 / 0.847 / 0.736 exactly
  (R1718).

### 6.6 Round 6b, step O (pre-registered; PLAN_ROUND6B_O §2, frozen as `r6b_tools/frozen_plan_s2.md`)
- **For each of O-P and O-GC separately. "Adds something":** the difference is −0.10 or lower, **and** its 90%
  bootstrap interval over jobs (10,000 resamples, seed 6) lies entirely below 0, **and** the difference is −0.10 or
  lower without langchain-model-update and without case 6, each separately, **and** the seeded line is 0 or below.
  If only the seeded condition fails: "adds only on its own finds". **"Does harm":** the mirror image. **Otherwise no
  clear difference**, which "does not show that the step does nothing".
- **Seeded line:** drop every row whose first source is r6-out-pr, r6-out-gc or a round-6b reply (named in advance:
  case 6 R1 major and R4 minor, from the P+R replies).
- **Cut-short runs,** defined mechanically (the stored session does not end on assistant text, or the run hit its
  limit): o06-precheck p1 and p2. Every line is also reported without them.
- **Rows used:** updated earlier rows (new candidates probed on every version); round 6's published figures are shown
  beside them, not revised.
- **Counting, severity, the strict disclosure rule and decision J** (with its sensitivity line) as round 6.
- **What it leads to:** O-GC "adds something": the outside review becomes a core GC step, at least for the kinds of
  job where it helped (from the per-job table), with the cost stated; O-P is supporting evidence. O-P adds and O-GC
  does not: read as "the review finds, but GC's scope rule blocks the fix", pointing to step D. Neither: the outside
  review stays optional. Then the Developer decides whether step D is needed.
- **Also reported, not deciding:** the level line, harm, missed only, all errors, the noise reference, time and cost.

---

## 7. Reviews and checks of the study itself

| what was read | reader | verdict | where |
|---|---|---|---|
| Protocol drafts 1 and 2 | reviewer subagent | PROCEED IF (4 and 2 blocking) | REVIEW_1.md, REVIEW_2.md, dispositions; R18–R21, R35–R39 |
| Packets 3 to 6 | checker subagents | 2–3 FAIL items each, mostly clerical; all dispositioned | companions-3 to -6/CHECKER.md; R46–R68 |
| Protocol draft 5 (packet-6) | outside reader (sent by the Developer) | PROCEED IF (B1–B3 blocking) | OUTSIDE_READING_1.md; R84–R95 |
| First evidence report | independent fact-check subagent | 37 OK, 8 WRONG, 4 UNSUPPORTED; corrected | EVIDENCE_REPORT_FACTCHECK.md; R160–R176 |
| Walk-through plan drafts 2 and 4 | checkers; four outside readings (reading 2 by Claude Opus 5.5 in claude.ai, reading 5 by the same author) | sound with changes | companions-11, -14; OUTSIDE_READING_2 to 5; R177–R224 |
| Walk-through steps and draft reports | checkers; an independent OpenAI GPT-6 review (non-Claude) and a Claude review | PROCEED WITH CORRECTIONS | companions-15; REPORT_REVIEW_*; CHECK_FULL_REPORT*.md; R238–R287 |
| Round-4 packet-16 | two checker readings (packet, prompt leaks) | 2 blocking, fixed | R813–R841 |
| Round-4 ledger | checker on a 30-row sample | 5 wrong rows, a rule change | R1001–R1014 |
| Round-4 report draft 1 (packet-17) | packet checker; two outside readings (one Claude, one other family) | ACCEPT WITH CORRECTIONS | companions-17; Src30, Src31; R1026–R1053 |
| Draft 2 (packet-18) | checker (three readings); two outside readings | ACCEPT WITH CORRECTIONS | CHECK_DRAFT2.md; companions-18; Src6, Src7; R1195–R1262 |
| Draft 3 | checker only | 0 errors | R1283–R1287 |
| Round-5 plan | internal review (21 findings, 5 blocking); packet-19 checker; two outside readings (Claude; non-Claude); checker of draft 3; script checker | RUN WITH CHANGES | PLAN_MIDDLE_GROUND_REVIEW.md; r5_plan/OUTSIDE_REVIEW_*, CHECK_DRAFT3.md, CHECK_SCRIPTS.md; R1337–R1396 |
| Round-5 rows and report | rows checker; report checker | 36/37 agree; 3 must-fix taken in | CHECK_ROWS.md, CHECK_R5_REPORT.md; R1583–R1588 |
| Round-5 report prose | checker of the lean case | erratum (Src11) | lean/CHECK_LEAN.md K1; R1627 |
| Triage plan and report | internal review; checker | RUN WITH CHANGES; all figures recomputed | triage/PLAN_TRIAGE_REVIEW.md, CHECK_TRIAGE_REPORT.md; R1603, R1613 |
| Final report | checker; two outside readings | ACCEPT WITH CHANGES | CHECK_FINAL_REPORT.md; final_report/reviews/; R1705, R1709 |
| Round-6 plan | internal check (6 errors, 15 should-fix); two outside readings (packet-26) | PROCEED WITH CHANGES | round6/CHECK_PLAN_ROUND6.md; round6/reviews/; R1709–R1716 |
| Round-6 results and this protocol (packet-27) | three outside readings | ACCEPT WITH CHANGES / ACCEPT WITH SMALL CHANGES / ACCEPT | R1865–R1870 |
| Round-6b plan (steps O and D), drafts 1 and 2 | internal check; re-check; two outside readings (packet-28) | NOT YET; RUN AFTER CHANGES; both PROCEED WITH CHANGES | round6b/CHECK_PLAN_ROUND6B.md; R1890–R1896 |
| Step-O plan draft 1 | internal check (0 blocking, 9 should-fix, 3 suggestions) | RUN AFTER CHANGES; all taken in draft 2 | round6b/CHECK_PLAN_ROUND6B_O.md; R1897 |
| Step-O rows | rows checker (36 sampled, the checker list, rows against verdicts) | 36/36 agree; 14 origin corrections | round6b/rows/CHECK_ROWS_R6B.md; R1928 |
| Step-O report draft 1 | internal check (every figure recomputed) | ACCEPT WITH CHANGES (8 findings, all taken) | round6b/CHECK_REPORT_R6B_O.md; R1931 |
| Step-O report draft 2 (packet-29) | one outside reading (figures recomputed independently) | ACCEPT WITH SMALL CHANGES | round6b/READINGS_R6B_O_DISPOSITIONS.md; R1934 |

**Who read.** Drafts 1 and 2 of the round-4 report and the round-5 plan each had one outside reader from a different
model family; draft 3, the round-5 report and the triage work had Claude checkers only (final report, Part A). The
outside readers' models are not always stated (R1629). The step-O plan draft 2 had no outside reading (decision
O-0; row 68); the step-O results had one. The GC 1.4 trial had none: the Developer reviews the 1.4 draft.

---

## 8. Records and freezing

- **The record.** `RECORD.md` is the running log, in time order, with the Developer's words quoted where they decide
  something (Src28 is a frozen copy). Decisions taken while the Developer was away are in
  `walkthrough/r5_plan/DECISIONS_WHILE_AWAY.md`, `walkthrough/triage/DECISIONS_WHILE_AWAY.md`, PLAN_ROUND6 §10 and
  PLAN_ROUND6B_O §10.
- **Packets.** A packet is a folder frozen with a `MANIFEST.sha256`; its identity is the SHA-256 of the manifest. A
  frozen packet is not edited; corrections go into a new packet or a companion folder (`companions-N/`: APPROVALS,
  CHECKER, ERRATA). Review bundles are built from a packet and its companions by `review_bundle.py`, unpacked and
  verified, put in `~/Downloads/`, and sent by the Developer only.

| packet | content | identity / bundle | record |
|---|---|---|---|
| 1 | protocol draft 1 | never frozen or sent | R21 |
| 2 | draft 2 | frozen by mistake; not sent | R40–R41 |
| 3, 4, 5 | drafts 3–5 | frozen; not sent | R42–R62 |
| 6 | draft 5 for outside reading | 442e7239…; REVIEW_BUNDLE.tgz 8a9ee674… | R65–R71 |
| 7 | draft 6, stage-1 tools and probes | 682f1de0… | R96 |
| 8 | stage 2 | a4218a7e… | R126 |
| 9, 10 | stage 3; elbow | 141c732a…; dbdcdf30… | R142, R151 |
| 11, 12, 13 | walk-through plan (13 sent) | 31d982e3…; REVIEW_BUNDLE_WALKTHROUGH.tgz | R188–R196 |
| 14 | walk-through draft 4 | f50060ef… | R217 |
| 15 | draft report for the independent review | 497b96af… | R241 |
| 16 | round-4 inputs and tools (37 cases, 1,861 files) | manifest 7ffe757a…, re-frozen 41840b7d… and 493dfb38… | R871, R883, R923 |
| 17, 18 | round-4 report drafts 1 and 2 | f4b88c97…; 5c3007d0… | R1034, R1250 |
| 19 | round-5 plan | 445da2fc… | R1358 |
| 20–24 | lean GC case, procedure, retirement plan, revision 22, website | as recorded | R1628–R1680 |
| 25 | final report with 34 sources | REVIEW_BUNDLE_FINAL_REPORT.tgz fa1640fa… | R1706 |
| 26 | round-6 plan draft 3 | REVIEW_BUNDLE_ROUND6_PLAN.tgz 59778a8e… | R1713 |
| 27 | round-6 results, this protocol, final report | REVIEW_BUNDLE_ROUND6_RESULTS.tgz (+ .sha256) | R1865 |
| 28 | round-6b plan draft 3 (steps O and D), checks | REVIEW_BUNDLE_ROUND6B_PLAN.tgz | R1892 |
| 29 | step-O results: report draft 2, plan, checks, summary, ledger, summary code | REVIEW_BUNDLE_ROUND6B_O_RESULTS.tgz (105 KB) | R1932 |

- **Hash freezes outside packets.** Round 5: plan, prompts, run list, affected list, targets, brief and scripts hashed in
  `walkthrough/r5_plan/FROZEN.sha256` before the pilot; the analysis and scoring scripts appended before any result was
  read (R1399–R1414, R1506, R1515, R1561). Triage: `triage/CHECK_FROZEN.sha256`. Round 6: `r6_tools/FROZEN_R6.sha256`
  (28 tool files, the plan and the row brief; 30 entries), re-frozen after each tool change (R1718–R1726). Round 6b,
  step O: `r6b_tools/FROZEN_R6B.sha256`, first the run tools, `MESSAGE_O.txt`, the run list and plan §2 and §4 (as
  `frozen_plan_s2.md`, `frozen_plan_s4.md`) before the send step and the pilot; then the scoring tools, the row brief
  and the severity scripts and brief before any O diff was read (26 entries); re-frozen after O-6 and O-10
  (decisions O-1, O-6, O-9, O-10). GC 1.4 trial: `r6c_tools/FROZEN_R6C.sha256` (20 entries, including the 1.4 draft).
- **Raw results** are kept outside the record under `~/unix/PHENIX/replay/` (`streams/`, `r4_out/`, `r4b_tests/`,
  `r5_out/`, `r6_out/`, `r6b_out/`, `r6c_out/`); invalid and discarded attempts are moved aside with a REASON file, never deleted.
- **Usage records** (`rate_limit_event`) are removed from packet copies of streams; unedited copies are in
  `raw_streams_unredacted/` (R53).
- **Final report sources** carry SHA-256 values in its index (Src1–Src38).

---

## 9. Protocol versus what was done

Each row was checked against RECORD.md or the tools, not against a plan alone. "Effect" is the effect on the reported
results as far as the record shows it.

The Guide spot-checked rows 10, 20, 30, 39 and 52–54 against their sources (2026-10-24) and settled two of the
points first left open (row 10 and §9.4).

### 9.1 Deviations

| # | round | planned | done | why | effect on results | source |
|---|---|---|---|---|---|---|
| 1 | Stage 1 | Packet-2 frozen only after a clean edit | Frozen by mistake after a failed edit; kept, not sent | the command did not stop on the error | none (never used) | R40–R41 |
| 2 | Stage 1 | The scorer gets only the checklist, task and diffs (protocol §5.2) | The stage-1 scorer had a write tool; its write was refused, so calls were taken from its final message | tool list not narrowed | none found | R107–R109, R170 |
| 3 | Stage 1 | D1 judged by the frozen GUI probe for every run | p2 and p3 undetermined: the probe imitates the old GUI and cannot judge a GUI-side fix or removed defaults | probe design | two of four runs not judged in stage 1; round 4b later judged them fixed with the hook simulated | R104–R107; STOP_2.md; RULINGS.md "originals 1-4" |
| 4 | Stage 1 | Scoring helpers frozen in packet-7 | `score_arm.sh` and `leak_check.py` written after packet-7 | mechanical wrappers | none (wrap frozen probes) | R110–R111 |
| 5 | Stage 2 | The Developer approves each reconstructed prompt (protocol §2, §4.1) | Prompts accepted by the Guide and shown in updates | the Developer's instruction to proceed straight through | prompts not individually approved | R116–R120; packet-8/STAGE2_ADDENDUM.md |
| 6 | Stage 2 | win32 runs start from the frozen RUN_SPECS | Both failed at start (model field held extra text); rerun with `--model claude-opus-5-5` | clerical error in a frozen file | none (rerun before scoring) | R133; companions-8/ERRATA.md |
| 7 | Stages 1–3 | The kit manifest checked against run times | Kit rev 16 landed during stage 1 and rev 17 between stages 2 and 3; no per-run check | not planned per run | none on plain runs (they do not use the kit) | R170–R171, R185–R187, R212–R214 |
| 8 | Stage 3 | Five cases | zombie dropped (`/bin/ps` refused); elbow added as a replacement | pre-declared stop condition | the ten are not the first five chosen | R142–R153 |
| 9 | Stage 3 | Permission mode allows the listed Bash use | 1–6 shell commands per run refused by `dontAsk` despite the policy's allow | Claude Code behaviour | small handicap on plain (48 refusals in 44 streams) | R157–R158; STEP1_FAIRNESS.md |
| 10 | Stages 2–3 | Scorer guess rate reported (protocol §5.2) | Not in the stage 2 and 3 reports; the scorers' own `source_guesses` (SCORES.json) show that all 9 set G apart (often by its different path roots, `iotbx/` against `modules/cctbx_project/iotbx/`) and 8 of 9 paired every P with its P+R (precheck paired them wrongly) | guess rates recorded but not reported | blinding between G and the plain arms was weak in stages 2–3, as in stage 1 | `stage2_results/scorer_*/`, `stage3_results/scorer_*/` SCORES.json and LABEL_KEY.json (case 8 read with the R271–R273 correction) |
| 11 | Stages 2–3 | Blind scorer labels map correctly | Case 8 LABEL_KEY swapped sfm-p1.P and sfm-p2.P | tooling error | corrected in the ledger (2026-10-19) | R271–R273 |
| 12 | Walk-through | "No rates; two runs can't support them"; no calculated general rate | Per-run rates, averaged per case, and a full error ledger of every significant error | the Developer's request | the frame of every later report | WALKTHROUGH_PLAN.md step 4.7; R262–R287 |
| 13 | Walk-through | Ledger for report claims only | `ERROR_LEDGER.tsv`, 198 rows, one per error per arm and run | the Developer's request | became the basis of LEDGER_R4 | WALKTHROUGH_PLAN.md "Rules"; R264–R267 |
| 14 | Walk-through | Analysis only, no new runs | Round 4 replayed every remaining suitable job | the Developer's request | rounds 4 to 6 | WALKTHROUGH_PLAN.md "Not done"; R288–R296 |
| 15 | Walk-through | Definitions "significant error: blocking / real-but-minor / cosmetic" | Round 4b used the major / minor rubric of a blind tagger instead | blinding; consistency over 37 jobs | the major-only figures use the new rubric | WALKTHROUGH_PLAN.md "Definitions"; Src4 §2 |
| 16 | Round 4 | 28 jobs + 2 unclear (group C) | 30 prepared, 27 suitable; gc-app-version-check (group B) also excluded | unsuitable offline | 37 jobs, not 38 | REPLAY_ALL_PLAN.md; R494–R546, R596 |
| 17 | Round 4 | GC+'s own final regression tests run against each plain result (plan item 2) | Not run as a general step; several prep rulings say GC+'s tests are not used as an oracle; replaced in round 4b by each arm's own tests on four states | GC+'s tests bind to GC+'s design | no one-way GC+-test measure in the results | REPLAY_ALL_PLAN.md item 2; R299, R436–R437, R567; `packet-16/tools/score_diff.sh` |
| 18 | Round 4 | Optional second, non-Claude reader (decision 3) | No answer recorded; round-4/4b readers were Claude Opus 5.5 only | not settled | independence limit stated (Src4 §10) | REPLAY_ALL_PLAN.md "Decisions"; `readings_r4.py`, `readings2_r4.py` |
| 19 | Round 4 | Stop 2: the frozen prep packet read by a checker, then approved or sent out | Two checker readings; the Developer pre-approved starting if checks passed; no outside reading of packet-16 | the Developer's go-ahead | none known | REPLAY_ALL_PLAN.md "Stops"; R791–R796 |
| 20 | Round 4 | Load gate: no start above load 10 | Raised to 16 after the smoke test | the gate held starts with almost nothing running | runs ran 6–7 at a time under load; plain times inflated (median P 19.7 against 13.0 min) | REPLAY_ALL_PLAN.md; R744–R745, R811; Src4 §9 |
| 21 | Round 4 | Disk gate by `df` | `free_gb.sh` counts purgeable space; packet-16 re-frozen after the restart | `df` ignores space held by local snapshots | 7 in-progress runs lost and rerun | R874–R884 |
| 22 | Round 4 | packet-16 frozen and final | Re-frozen twice after the start (disk gate; `stop_all.sh` fix) | tool faults | tools only; probes and cases unchanged | R883–R884, R921–R923 |
| 23 | Round 4 | Smoke test after all fixes | Checker fixes (limit_hit, deny list, void marks, reader attachments) not re-smoked; the first finished run was read instead | time | first run checked valid | R868–R870, R874–R876 |
| 24 | Round 4 | `leak_check2` void marks decide | Guide-side `leak_review.py` (not in the frozen packet) reclassified all 11 void-marked runs | false alarms | no run void | R886–R897, R966–R969 |
| 25 | Round 4 | Blind task probes written blind | The empty-region probe was revised after the Guide had seen GC+'s design (accepting a clear Sorry) | the probe judged design | probe not fully blind; ≤0.04 on any rate | R640–R649; Src4 §10 |
| 26 | Round 4 | Blind helpers see nothing of GC+ | Helpers shared the Guide's scratchpad, which held GC+'s placement-test diffs; one saw a file name and reported not reading it | scratchpad not separated | none found; partial guard by the cross-check | R620–R626 |
| 27 | Round 4 | Case 1's G diff complete | The frozen G diff held GC+'s phenix commit only; round 4b added its phenix_regression test from `r4b_extra/` | assembly gap | case 1 G readings and tests redone | R1126–R1131 |
| 28 | Round 4 | Plain runs that hit the P limit under load are rerun alone | gc-rev15-macos-ci p1 and p2 rerun alone and counted; p2 hit 90 min again with the machine idle | plan rule | reruns counted; loaded runs kept | R899–R904, R958–R964, R978 |
| 29 | Round 4 | Budget about $1,000–1,500 of API use (plan decision 4) | No API use: the logged-in CLI under the Max plan; cost figures are notional | not an API account | none | REPLAY_ALL_PLAN.md; R366–R369 |
| 30 | Round 4b | Headline counted all program errors the arm left | From 2026-10-21, pre-existing faults leave the headline and are reported apart, for both arms | they were counted only when the other arm happened to find them | headline lines changed after results were seen | R1007–R1012 |
| 31 | Round 4b | Disclosure judged per arm | Carry-over P → P+R adopted after the draft-2 checker (24 rows) | P+R is the same session | P+R all-37 0.51 → 0.47; figures without it in Src4 §10 | R1202–R1205; RULINGS.md |
| 32 | Round 4b | Severity: one blind tagging | First tagging not blind (source column named arms); second tagging made primary after the first was seen; six items re-tagged | checker found the unblinding | major-only figures under both are reported | R1155–R1159, R1197–R1212, R1243–R1246 |
| 33 | Round 4b | — (no grouping planned) | Hard / medium / easy groups with cut-offs chosen after round-4 figures | the Developer's question | groups are an association, not a test | R1117–R1124; Src4 §3 |
| 34 | Round 4b | Test adequacy: 900 s per test, four states | gc-rev15-macos-ci rerun with 1500 s and own + base only | its kit test needs about 17 min | seeded-fix states missing for one case | R1111–R1115 |
| 35 | Round 5 | "Affected" runs: scratch written and reused as check inputs | Narrowed before any run to data and `work/` inputs: 0 affected; 18 runs with lost logs listed | logs are re-created by rerunning checks | the "without affected runs" rule had no effect | Src8 §4.6; decision 1 |
| 36 | Round 5 | Each run's temp folder restored before each arm | Three pilot runs' folders deleted by a dry-run script bug; both arms start from the same empty folder | `tar` read a name starting with "-" as options | three runs lost scratch, both arms alike | decision 3; Src9 "Other limits" |
| 37 | Round 5 | Kit denied except in gc-next-revision | Exception widened to every run whose P+R change touches the kit (case 6 too) | the deny would hide code under change | none | decision 4 |
| 38 | Round 5 | Pin unpinned repositories of the originals | All 38 runs pinned by reflog (24 gain pins); compiled build not rebuilt | round-4 runs had moved too | compiled parts may not match pinned sources | decisions 2, 5 |
| 39 | Round 5 | The pilot may change the limit (§5); 60 minutes for both arms | Kept at 60 minutes with no recorded decision; 28 of 38 P+R+S runs hit it | oversight (decision 15) | the result is "the step within an hour"; missed-only measures penalize P+R+S | Src8 §5; decision 15; Src9; Src12 |
| 40 | Round 5 | Automatic leak check voids runs | Replaced by `leak_review_r5.py` after the pilot; revised twice mid-round (timeouts; kit reads by content; a regex bug); two cases rescored | false alarms | no run void; rescoring of case 6 and case 4 | decisions 6, 8, 9; R1504–R1505, R1524–R1527 |
| 41 | Round 5 | 4–6 runs at a time | 6, then 2 for some hours, then 6 again | the Developer's request; a sleep on battery | both arms alike through the random order | Src8 §4.2; decisions 11, 12; R1540–R1558 |
| 42 | Round 5 | Invalid runs retried | 8 invalid attempts on 7 runs redone (one clock jump of about 81 s, one sleep, one sleep with the network down); RECORD first said 6 | sleep rule kept unchanged | none on the comparison | R1564; CHECK_R5_REPORT.md item 3; decision 10 |
| 43 | Round 5 | Nothing in §8 changed after results are seen | After the first summary, case 8 D1/D2 origin set to the ledger's (decision 14); P+R+S − P+R moved from −0.139 to −0.111 | consistency with the ledger, found by the rows checker | P+R+S − P+2R unchanged (−0.083); reading unchanged | R1576–R1585; decision 14 |
| 44 | Round 5 | Severity: new errors tagged blind | Workers' own severity column ignored (script fixed before its first run); case 10 "stale" left untagged and counted not major | consistency | slightly favours P+R+S; reading unchanged | R1561, R1581; Src9 |
| 45 | Round 5 | Rows written to `r4_ledger/ROWS_R5.tsv` (§7.8) | Rows in `walkthrough/r5_rows/<case>/`, merged into `r5_plan/R5_LEDGER.tsv` | file layout | none | Src8 §7.8; Src13 |
| 46 | Round 5 | Blinding of rulings under L1 / L2 | Partial: P+R+S leaves an evidence folder and lists findings; empty final messages point to P+R+S | inherent | stated limit | R1510–R1511; Src9 |
| 47 | Round 5 | Same binary as the sessions were made with | Claude Code 2.1.303 resumed sessions the originals made on 2.1.284 | the old binary was not used | stated limit | Src8 §9 |
| 48 | Round 6 | Skill in the run's `.claude/skills/gc/` (§4.3) | Loaded as a plugin with `--plugin-dir`; first pilot aborted and restarted | `--restricted` ignores project skills | none on scored runs | decision C; R1719 |
| 49 | Round 6 | A separate `CLAUDE_CONFIG_DIR` (decision 6) | Default configuration; the user `/gc` link moved out during runs | a separate folder starts signed out | the Developer's own `/gc` is unavailable during runs | decision A; R1717–R1718 |
| 50 | Round 6 | Outside review sent inside each run, before scoring (§4.6) | Split off: GC+O run later by the Developer (`run_gco.sh`) | the key is only in the Developer's Terminal | GC+O results later than GC | decision B; R1718 |
| 51 | Round 6 | All pilot acceptance checks pass before stage 2 (§7), including the outside-review checks | Stage 2 started with the outside-review checks deferred to the GC+O step | decision B | those checks happened only when GC+O ran | PLAN_ROUND6 §7, decision E; R1721 |
| 52 | Round 6 | Pilot checks show the runs work | Every Bash call in every GC and GC+O session failed (sandbox profile over 64 KB); the pilot accepted it; all 40 GC runs, 20 GC+O attempts and 20 outside reviews discarded; pilot and stage 2 rerun | temp folder had 3,042 entries; the error was misread | no round-6 result from those runs; reruns in progress | decision G; R1726 |
| 53 | Round 6 | GC+O restore verified byte for byte | Four GC+O runs failed the restore (7- against 8-character index lines); batch stopped, one attempt aborted; check changed to ignore index lines | rebuilt installation abbreviates differently | runs later discarded under row 52 | R1725 |
| 54 | Round 6 | Personal names replaced before any send (decision 7) | Two P+R search requests sent a reporter's surname as an attachment file name | the replacement list came from prompt texts only | privacy slip; the list extended before any GC+O send | decision F; R1724 |
| 55 | Round 6 | P+R search on every P+R run (decision 10) | 37 replies; one request refused (key-shaped test placeholder) | the refusal rule | that run has no search reply | decision F; R1724 |
| 56 | Round 6 | Run names `r6-<job>-g<N>` | `r6_runs.py` replaced "-p" inside four names (for example "grovider") | string replacement | cosmetic; names consistent everywhere | R1724 |
| 57 | Round 6 | Everything as for P except what §4 lists | GC's claude processes run with a whitelisted environment (`env -i`); P's inherited the Guide's shell environment | keep the key out | not settled (see 9.4) | `run_gc.sh`; `packet-16/tools/run_arm.sh` |
| 58 | Round 6 | Built-in extras as in P's sessions | Some account-side skills and agents P had are absent today | account-side change | accepted; none bears on bug fixing | decision E |
| 59 | Round 6 | Each run gets the job's files as the plain runs did | Case 1 and case 8 runs lacked the bug-report file the prompt names (the stage drivers had passed it outside RUN_SPECS); the six sessions stopped without a change; rerun with the frozen copy (same SHA-256) | tooling gap | the six reruns are the counted runs | decision H; RECORD 2026-10-24 21:39Z |
| 60 | Round 6 | The sleep check marks a run invalid only after a real sleep | All four GC+O steps flagged "slept" for their whole length: Apple's /usr/bin/python3 in the Developer's shell; pmset showed no sleep; re-validated with sleep 0, no rerun; check now uses a fixed Python | clock artefact | none | decision I; RECORD 2026-10-24 23:55Z |
| 61 | Round 6 | Rulings follow the brief | Earlier rounds' "not an error" rulings kept in every job; findings they excluded (replace refs, pre-push hook, precheck R8) put in a sensitivity line | consistency across rounds and jobs | none on Q1 (all minor); counting them would favour GC+O | decision J |
| 62 | Round 6 | The blind reading's findings name the right arm | The reader filed findings under other arms' labels (quote check in three jobs); every candidate ruled on every arm | reader error | at most the first-source token | decision K |
| 63 | Round 6 | The frozen summary script is used as written | Fixed before its first run on round-6 rows: GC's rows were copied onto a GC+O version with no rows (precheck g2.L2); --with-sensitivity added | script bug | without the fix GC+O − P+R would have read +0.139 | decision L |
| 64 | Round 6 | Every counted error has a blind severity tag | 5 counted rows and the sensitivity-only ids were untagged (never tagged in rounds 4b/5); tagged blind after the first summary was read | gap in earlier tagging | no figure changed; the first summary is kept | decision M |
| 65 | Round 6 | "Disclosed" judged by one rule throughout | The strict rule (only a plain statement that this specific problem is left) was announced while ruling, from langchain-provider-todos on; the five earlier jobs were re-checked under it afterwards: all 11 of their deferred rows pass (none changed) | rule clarified mid-scoring | none on any figure | RECORD 2026-10-25; rows/<slug>/NOTES.md |
| 66 | Round 6 | Descriptive measures of §2 computed | Proving-test rate and errors introduced by the review pass not computed; the decisions put to the stand-in Developer and the scope reverts counted after the outside readings (decision N) | not in the summary script | descriptive only | decision N; walkthrough/round6/decision_count/ |
| 67 | Round 6b | Steps O and D (PLAN_ROUND6B draft 3; packet-28): D gives every run the same developer answer and tests the scope rule (DiD, narrow-rule line) | Step O only; step D planned but not run; GC 1.4 narrows the scope rule without a test | the Developer's decisions: O first, then decide; after O, the Guide's recommendation, which the Developer agreed to ("that sounds good"): narrow the scope rule without a further test, no more large experiments | the scope rule's effect is not measured; the 1.4 change rests on rounds 5–6 and the trial only | R1895–R1896, R1937 |
| 68 | Round 6b | Plans of rounds 5 and 6 read by outside readers before any run | Step-O plan draft 2 had the internal check only | the Developer: "we can start" (decision O-0) | none known; the results had an outside reading (packet-29) | PLAN_ROUND6B_O §10 O-0; R1899 |
| 69 | Round 6b | Frozen before the pilot: §2, §4, run scripts, driver, masking, configuration, policy generator, blind prep, label generator and `r6b_summarize.py` (plan header) | Run tools, message, run list, §2 and §4 frozen before the send step and the pilot; blind prep, labels and summary written and frozen after the pilot, before any O diff was read and before the summary's first run | they do not touch the runs | none; the order guards the same thing | decision O-1; R1901, R1904 |
| 70 | Round 6b | Restore and resume as round 6's `run_gco.sh` and round 5's `run_prs.sh` | Both step-O scripts pass decision H's bug-report attachment, which neither earlier script did. Found in passing: round 6's GC+O step of case1-g4 resumed without that file at the run root (its session had already read it) | every O run has the file its prompt names | none on any figure; noted for round 6 | decision O-2 |
| 71 | Round 6b | P+R+O installation by r4's `make_run.sh` (§5) | `make_run_pro.sh`: the same without linking `modules/guided_coding` | that repository was created on 2026-10-22, after every P+R run; r4's script would now link it | none (P+R's own installation did not have it) | decision O-3 |
| 72 | Round 6b | Pilot runs rerun if the mechanics change after the pilot (§7) | A scons collision on a shared Boost header in `build_39/conda_base` stopped one P+R+O setup; a build lock was added; the other 11 pilot runs kept, the failed run rerun under the lock; tools re-frozen | the lock changes only setup timing, not the sessions | none found; the header checked original twice; a leftover `bc_clustering.hpp.dist`, identical, left in place | decision O-6; PILOT_R6B_O.md; R1903, R1906 |
| 73 | Round 6b | One row worker per job; known errors ruled on every O version (§6) | Workers rule both versions of each run from scratch, under X1/X2 and Y1/Y2, against a known-error list without arm, run or end | ruling only O versions would show which version is the O one | earlier versions ruled twice; the primary keeps round 6's rows for them (O-9) | decision O-7; BRIEF_R6B_ROWS.md |
| 74 | Round 6b | Every round-6 probe and test adequacy on the 76 O versions (§6) | Probes on base, the earlier versions and the O versions in one installation per job; tests on the O versions only | the same probe at the same time for each pair | earlier versions' test results are round 6's | decision O-8 |
| 75 | Round 6b | First-source tokens and origin "outside" as §2 and §6 state | Ids `O<k>` and tokens r6b-read2 / -probe / -out / -rev / -rep fixed; a same-ruler line added; an "outside" error found in an earlier version counted as that version's own | to make the earlier/O pairing explicit before scoring | the same-ruler line equals the primary (0 disagreements) | decision O-9; R1925–R1926 |
| 76 | Round 6b | Summary hashed before its first run on step-O rows (§6) | Changed after rows from 6 of 18 jobs existed (labels masked), before its first run: known ids take round 6's kind and origin; re-frozen | a change of ruler in kind or origin alone could move a row in or out of the measure | O-GC −0.167 with it, −0.222 without; made O-GC smaller | decision O-10; R1912 |
| 77 | Round 6b | Every counted error has a blind severity tag before the summary is read | Case 1 typed-name (five O versions, origin outside) untagged; tagged blind among 10 anchors after the first summary was read (O-GC −0.167, "adds"); tag used as given: minor | it had been pre-existing, so never tagged | no figure changed; had it been major, O-GC −0.125 and "no clear difference" | decision O-11; R1929–R1930 |
| 78 | Round 6b | Origin "outside" = caused by hunks only the O version has (§6) | Extended mid-scoring: a version that lacks its partner's fix of a base fault also counts as "outside"; given to workers from o02-atomic on; earlier jobs through the checker; decided blind to which version is the O one | the langchain-model-update worker gave such a case origin "pre" | O-GC −0.167 with it, about −0.208 without; made O-GC smaller | decision O-12; R1913 |
| 79 | Round 6b | Checker samples rulings and flagged items (§6) | The checker also re-ruled the origin of one-version errors and made 14 corrections, origin only, applied before the first summary; workers had kept "pre" or "own" in some cases | the rule (row 78) applied unevenly by workers | two major E2 rows and langchain-model-update O1 (major) moved to "outside" and counted; no presence or disclosure changed | CHECK_ROWS_R6B.md; R1928 |
| 80 | Round 6b | Label keys unopened until all rows are final and checked | The Guide unmasked o06-precheck's key while testing `disagree_r6b.py`, after that job's rows were final and before the checker ran | testing the tool on real data | no ruling changed; rules were fixed in advance; the checker remained blind | R1925; REPORT_R6B_O §6 |
| 81 | Round 6b | Cut-short runs defined mechanically (§2): session not ending on assistant text, or a limit hit | sfm-p2's P+R and P+R+O sessions both end on an interim status line ("report back when the run finishes"), with no final report; not cut short by the rule, so kept in every line | the rule was fixed in advance; the full 6b plan had listed case 8 p2 as cut short | the same in both versions; no disclosure ruling depends on them; a stated limit | R1920; CHECK_ROWS_R6B.md; PLAN_ROUND6B §2 |
| 82 | GC 1.4 trial | Trial runs of the 1.4 draft, then the send step and resumes (R1936) | Trial 1's outside reviews not sent (old scope rule); the scope rule and "finish before you report" added to the draft after trial 1; trial 2 rerun the three H jobs with the full draft | trial 1's findings | trial 2 tests a draft changed after seeing trial 1; an implementation check only | R1937, R1939–R1940; TRIAL_1.4.md |
| 83 | GC 1.4 trial | GC+O resume continues from GC's frozen end state, as round 6 | The resume rebuilds the installation with a new base commit, so two sessions saw HEAD change; GC's own check caught it; files confirmed unchanged; isolated copies used | harness artefact of round 6's `run_gco.sh` | none on the trial's verdict. The same rebuild is used by round 6's GC+O and step O's run scripts; whether those sessions noticed is not recorded | TRIAL_1.4.md; `r6c_tools/run_gco.sh` |

**Counted: 83 deviations** (58 in the first draft; 59–66 added when round 6 ended; 67–83 added when round 6b, step
O, and the GC 1.4 trial ended, 2026-10-26). The three with the largest effect on what the results can say:
1. **Round 5, the 60-minute limit (row 39).** 28 of 38 P+R+S runs were cut off, so the pre-registered result measures
   "the step within an hour" and its missed-only measures penalize P+R+S.
2. **Round 6, Bash refused in every GC session (row 52).** A whole round of runs, outside reviews and the pilot's
   acceptance were invalid; they were redone (§1.9).
3. **Rounds 4–4b, analysis rules settled after results were seen (rows 30–33).** The pre-existing-fault rule, the
   disclosure carry-over, the choice of the second severity tagging as primary and the hard / medium / easy cut-offs
   were all adopted after figures were seen. Each is disclosed with its alternative figures in Src4, but none was fixed
   in advance.

In round 6b the rules that decide were fixed in advance, and the scoring changes made after rows existed (rows 76,
78) were made with the labels masked and both made O-GC smaller. The one step taken after the first summary was read
(row 77) is the item the result most depends on: step O's "adds something" for GC is one run-level removal from "no
clear difference", and a major tag for typed-name would have changed it. Row 67 limits what the study says about
GC's scope rule: it was not tested.

**What most affects how the final results can be read** (added 2026-10-25, at an outside reader's suggestion; each
is discussed in the reports): the partly post-hoc counting rules of round 4b (rows 30–33); the choice of the 18
harder, caught-any jobs for rounds 5 and 6; the unequal time limits (round 5's 60 minutes, row 39; case 6's 45-minute
P+R limit); the stand-in Developer of round 6, which answered every question GC asked "keep to the task" (row 66,
decision N); and the partial blinding and single model family of the readers, workers and taggers. For round 6b
(added 2026-10-26): resumed sessions, not fresh ones, given one scripted, one-turn outside review that no developer
filtered; a packet recipe (task and final diff) that differs from GC's own OUTSIDE_REVIEW.md; the developer's time to
read a review not measured; a result for GC that rests on four jobs and on single items (row 77; the case 3 O1
tag); and the scope rule left untested (row 67). The GC 1.4 trial checks that the instructions work on four jobs;
it measures nothing.

### 9.2 Changes the Developer approved mid-study

| date (2026) | change | source |
|---|---|---|
| 10-15 | Isolation by a second installation per case (STOP_1 option A) | R23–R24 |
| 10-16 | PLAN_3 approved: stage 1 after the outside reading; the Developer sends bundles | R78–R83 |
| 10-16 | PLAN_4 approved: four case-1 replays with three-part reporting (OUTSIDE_READING_1 conditions 2 and 5) | R101–R103 |
| 10-16 | STOP_2 option A: p2 and p3 undetermined; close stage 1 | R112–R115 |
| 10-16 | Proceed through cases 2–5 without per-case prompt approval | R116–R120 |
| 10-16 | Five more cases (stage 3) | R139–R141 |
| 10-19 | Walk-through: analysis only; bug-fix cut first; then "greatly simplify"; draft 5 approved; a non-Claude reviewer for step 5.2 | R177–R224 |
| 10-19 | The Developer's Sept–Oct commit audit added as a late-stage detector | R197–R204, R254–R261 |
| 10-19 | Report rewritten with a full error ledger; per-run rates; GC+'s disclosed problems counted as deferred, not failures | R262–R295 |
| 10-19 | Replay all remaining suitable jobs, up to 8 at a time; "no need to throttle" | R288–R296, R373 |
| 10-19 | Machine-side: `replay/` excluded from Time Machine; local snapshots cleared | R395–R397, R478 |
| 10-20 | Go-ahead for the full round-4 run if the checks pass | R791–R796 |
| 10-20 to 10-21 | Stops, drains and restarts for the Developer's offline time | R906–R957 |
| 10-21 | Round 4b: test adequacy, cross-arm probes, a second reading, the audit both ways, including the first ten | R1070–R1077, R1124 |
| 10-21 | Hard / medium / easy frame | R1117–R1124 |
| 10-21 | Severity left as the second blind tagging (no Developer re-classification) | R1308–R1312 |
| 10-22 | Round 5 planned, outside review of the plan, then authorized to run while away | R1324–R1378 |
| 10-22 | Lower load for some hours; then two sessions at a time; then full speed after the sleep | R1540–R1558 |
| 10-22 | The time-limit check of round 5 (exploratory, no runs) | R1595 |
| 10-23 | Triage: no retrospective decision test; design and descriptive check only | R1604 |
| 10-23 | Replay study stopped; lean trial set up | R1634 |
| 10-23 | Round 6 decisions 1–5 (scope, ChatGPT API, no drift check, plan reviews, limits); 6–8 (configuration, name replacement, no budget stop); 9–11 | PLAN_ROUND6 §10; R1708–R1716 |
| 10-24 | Standing authority for round 6 ("run straight through ... record it"); model gpt-6.1-sol | R1718 |
| 10-25 | Round 6b planned (GC+D and P+R+D); decisions 1a, 2a, 3a; then step O first, D afterwards if needed | R1889, R1893, R1895–R1896 |
| 10-25 | Step O: "we can start" without an outside reading of plan draft 2 (O-0); the Developer runs the send step | R1899, R1902 |
| 10-26 | After step O: the outside review a standard GC step for difficult or consequential changes and an easy option for routine fixes; first try the real instructions on a few jobs | R1935 |
| 10-26 | On the Guide's recommendation, agreed by the Developer (after the Guide's analysis the Developer asked "do we need the trial that is running now?" and, after the Guide's plan (finish the trigger check, skip the send step, fold the narrowed scope rule into 1.4, then one small trial of the full 1.4), replied "that sounds good"): narrow GC's scope rule without a further test; no more large experiments (step D not run); trial 1's send step skipped, the scope rule and "finish before you report" folded into 1.4, then one small trial of the full draft | R1937 |

### 9.3 Known misses

- **Round 6b: the Guide unmasked one job's labels** (o06-precheck) while testing `disagree_r6b.py`, after that job's
  rows were final; no ruling changed (row 80; R1925).
- **Round 6b: the first pilot setup collided** on a shared Boost header in `build_39/conda_base` (row 72).
- **Round 6b: origin rule applied unevenly** by row workers; 14 corrections by the checker (rows 78–79).
- **Round 6b: report draft 1 gave GC+O\* 10 removals**, corrected to 9 by the internal check (CHECK_REPORT_R6B_O
  finding 1).
- **Round 6: case1-g4's GC+O step ran without the bug-report file** at the run root; found in step O (row 70).
- **Round 6b: elbow-p2's P+R `work/` folder** (untracked, never frozen) was not restored in P+R+O; the session noticed
  and went on (PILOT_R6B_O.md; a stated limit).
- **GC 1.4 trial 1:** a session ended before writing its review file, another left a wait loop running; the draft was
  changed (row 82).
- **Round 6, decision G: runs discarded.** Every Bash call in every round-6 GC and GC+O session failed, because the
  sandbox policy listed 3,042 temp-folder entries (171 KB; macOS refuses profiles over 64 KB). GC could read and edit
  files but run nothing. The pilot showed the error once (langchain-cap-fix g2) and the Guide misread it; the pilot was
  accepted and stage 2 ran to the end. All 40 GC runs, 20 GC+O attempts and their 20 outside reviews were archived
  (`r6_out/_discarded_sandbox_1792854791`); the old entries were moved aside; guards were added (policy size, sandbox
  error = invalid run, a Bash check in pilot acceptance); the pilot and stage 2 were rerun and accepted (decision G;
  R1726 and the 2026-10-24 entries after it). The P+R search was kept, since it did not run in the sandbox.
- **Round 6, decision F: privacy slip.** The name-replacement list was built from the prompt texts only. Two P+R
  search requests for case 8 sent a reporter's surname to the OpenAI API as an attachment file name (the report itself
  was not sent). The names that appear only as attachment file names were added to the list before any GC+O send
  (decision F; R1724). This document does not repeat the names.
- **Round 6: the first pilot ran without the skill** (`--restricted` ignores project skills); stopped within minutes
  and restarted (decision C; R1719).
- **Round 6: GC+O restore mismatch** on four runs, and one aborted resume (R1725).
- **Round 5: the 60-minute limit** was kept without a recorded decision although the pilot showed 2 of 3 P+R+S runs at
  or near it (decision 15).
- **Round 5: overstatement in the report** that neither extra pass reached anything only GC+'s outside reviewer or live
  probe caught; corrected to "no **major** error" in an erratum (Src11; R1627).
- **Round 5: three temp folders deleted** by a dry-run script bug (decision 3).
- **Round 5: invalid-attempt count** recorded as 6, corrected to 8 by the report checker (R1564; CHECK_R5_REPORT.md).
- **Round 4: draft 1's headline did not stand.** GC+ 0.14 against P 0.51 rested on probes built from GC+'s own catches,
  which can find errors only in plain code (Src4 §4, §6; R1051–R1053).
- **Round 4: severity not blind at first** (the source column named arms), and six descriptions still not blind in the
  second tagging (R1197–R1201, R1243).
- **Round 4: a probe made one real HTTPS request** to an outside service with a fake key during probe development,
  before the network guard was added (R585–R587).
- **Round 4: blind helpers shared the Guide's scratchpad** holding GC+'s diffs (R620–R626).
- **Round 4: `stop_all.sh` killed itself** and left two scoring folders (fixed, packet re-frozen) (R921–R923).
- **Stages 1–3: the case-8 scorer's label key swapped two runs** (R271–R273).
- **First evidence report:** 8 wrong and 4 unsupported claims of 49 checked, corrected (R160–R176); two kit-revision
  timing errata (R185–R187, R212–R214).
- **Stage 1: packet-2 frozen by mistake** (R40–R41).

### 9.4 Not settled

- **Round-4 decisions 3 and 5** (a second, non-Claude reader; governance and an outside reading of the prep packet):
  REPLAY_ALL_PLAN.md lists them for the Developer, and RECORD.md holds no answer to either. The tools show only Claude
  readers. Decision 4 (budget) was overtaken by the finding that no API key is used (R366–R369).
- **Scorer guess rates in stages 2 and 3:** settled after the first draft (row 10): the guesses were recorded in each scorer's SCORES.json but not reported.
- **The environment of P's sessions** (row 57): P inherited the Guide's shell environment; GC ran with a whitelist:
  HOME, USER, LOGNAME, PATH (the caller's), LANG, TERM=dumb, TMPDIR, DISABLE_AUTOUPDATER=1,
  CLAUDE_CODE_DISABLE_AUTO_MEMORY=1, GIT_CONFIG_GLOBAL and XDG_CONFIG_HOME (the run's own), PYTHONDONTWRITEBYTECODE=1
  (`r6_tools/run_gc.sh`). P's run script sets the same four run-specific variables (`packet-16/tools/run_arm.sh`).
  Both run PHENIX tests through the installation's own `build/bin`; neither sets PHENIX variables. Whether any other
  inherited variable changed P's behaviour is not recorded.
- **Claude Code version for every round-4 run:** settled after the first draft: every stream with a version field in `replay/streams/` for the 27 round-4 jobs (108 streams) shows 2.1.303; the 46 streams of the first ten show 2.1.284 (read-only tally, 2026-10-24).
- **Timestamps in RECORD.md lines 1703–1726** are not in a consistent order (entries marked 03:30Z to 08:00Z come
  before one marked "02:15Z (10-24)"), so the exact UTC times of round-6 decisions 1–11 cannot be read from the record;
  their dates are taken from PLAN_ROUND6 §10 (2026-10-23).
- **Round 6 itself:** settled when it ended (§1.9). As of the first draft (2026-10-24) the rerun pilot had not
  finished; it, stage 2, GC+O and scoring were then completed as §1.9 and rows 59–66 describe.
- **Round 6b: why GC gained more than P+R from the same kind of review** is not settled; one visible part is that the
  P+R replies named few of P+R's counted major errors (REPORT_R6B_O §4).
- **Rounds 6 and 6b: whether any GC+O, GC+O\* or P+R+O session noticed the rebuilt base commit** (row 83) is not
  recorded.
