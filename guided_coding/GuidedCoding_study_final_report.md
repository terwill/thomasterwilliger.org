# GuidedCoding Plus, GuidedCoding and plain Claude Code: final report of the replay study

Final version, 2026-10-23, after two outside readings (both "accept with changes"; the changes are taken in); updated 2026-10-25 with round 6, the replay of the current GuidedCoding (Part F), after three outside readings of its report; updated 2026-10-26 with round 6b, which measured what an outside review adds, and GuidedCoding 1.4 (2026-10-26) that followed from it (Part G), after an internal check and one outside reading of its report. Prepared by the Guide, a Claude Code session, for the Developer
(Thomas C. Terwilliger), from the study's checked reports and data. It brings together everything the study
measured, from the first replays on 2026-10-15 to the publication of the current GuidedCoding on 2026-10-23, its
replay on 2026-10-24 and 25, round 6b on 2026-10-25 and 26, and the trial of the GuidedCoding 1.4 draft on 2026-10-26. A companion document, the protocol of the whole study and its comparison with what was
done [Src42], goes with this report.

## How to read this report

- **Where the sources are.** The cited files are in the study's evidence bundle, available from the author on
  request; this report alone does not include them.
- **Sources.** Every figure and finding is traced to a file in the study's record, the folder
  `phenix/.claude/records/2026-10-15-gc-replay-protocol/` in the Developer's PHENIX checkout (`<rec>` below).
  Citations in square brackets, such as [Src3], refer to the source index at the end, which gives each file's path and
  SHA-256. Those files are kept in the study's record and are available on request.
- **What is reproduced and what is new.**
  - **New in this report:** the names, the summary, Part A (the study from start to finish), Part D (triage), Part E
    (from GuidedCoding Plus to GuidedCoding), Part F (round 6: GuidedCoding replayed, a summary of its report [Src39]), Part G (round 6b:
    what an outside review adds, a summary of its report [Src45], and GuidedCoding 1.4) and Part H (limits of the whole
    study).
  - **Reproduced:** Part B is the checked round-4/4b report (draft 3) [Src4]; Part C is the checked round-5 report [Src9]
    with its erratum [Src11] and the time-limit check [Src12]. In these parts the only changes are the arm labels,
    the reports' opening paragraphs (left out) and heading levels. The labels were changed by a script
    (`walkthrough/final_report/rename_arms.py`) and checked word by word: GC and G become GC+, PRS becomes P+R+S, and
    R2 becomes P+2R. File paths in Parts B and C are relative to `<rec>/walkthrough/` unless they begin with
    `walkthrough/`, `packet-` or `replay/`.
- **Rates.** Unless a line says otherwise, a rate is **confirmed program errors missed**, per GuidedCoding Plus job
  or per plain run, averaged within each job and then across jobs [Src4, Terms].

## Names used in this report

| name here | in the earlier reports and files | what it is |
|---|---|---|
| **GuidedCoding Plus (GC+)** | GC, G, "the earlier kit", "full GC" | The earlier GuidedCoding kit, revisions up to 21 (2026-09 to 2026-10-23): a Guide session, worker sessions, an internal reviewer subagent, outside readings by another AI assistant, the Developer's approvals at fixed screens, and evidence packets checked by kit code. Retired on 2026-10-23 and kept on the branch `full-kit-rev21` [Src28] of `cctbx/guided_coding`. In the replay, **GC+** is GuidedCoding Plus's own final change. |
| **GuidedCoding (GC)** | lean GC, `LEAN_GC.md`, `/lean`, revision 22 | The procedure replayed in rounds 6 and 6b, `/gc` version 1.3 (superseded by 1.4): a short set of instructions with a proving test, one review pass, added steps only for named triggers, and a short report. Published as `cctbx/guided_coding` revision 22 on 2026-10-23. Replayed in round 6 (Part F) and round 6b (Part G). |
| **GC 1.4** | GuidedCoding 1.4 (2026-10-26), `gc_rev23` | The revision of GC made on 2026-10-26 after round 6b: a "hard change" trigger (H) with an outside review, the outside review offered on every other job, a narrower scope rule, and "finish before you report". Checked in a small trial: 4 runs of an earlier draft (trigger check) and 3 runs of the full 1.4 text, with their resumes after the outside review (Part G). |
| **GC+O** | GCO | In round 6 only: the same GC session continued after an outside review from a different model (gpt-6.1-sol), where GC wrote one; otherwise identical to GC. |
| **P** | P | A plain Claude Code run on the same job, prompted to work autonomously. |
| **P+R** | P+R | The same plain session, resumed for one `/code-review --fix` pass. |
| **P+2R** | R2 | The P+R session resumed for a second ordinary `/code-review --fix` pass (round 5 only). |
| **P+R+O** | PRO | In round 6b only: each counted P+R session resumed once and given an outside review of its final change from gpt-6.1-sol. |
| **GC+O\*** | GCOS | In round 6b only: each counted round-6 GC session, resumed from before any round-6 outside review and given a script-built outside review of its final change from gpt-6.1-sol, whether or not GC had asked for one. |
| **P+R+S** | PRS | The P+R session resumed for a structured reviewer step built from GuidedCoding Plus's reviewer brief (round 5 only); GC's optional independent reviewer (`REVIEWER.md`) is built from this step. |

## Summary

**The question.** Does a layered procedure, GuidedCoding Plus (GC+), leave fewer errors in Claude Code's bug fixes
than plain Claude Code, with or without a review pass, and at what cost? Later: is there a cheaper middle ground,
and what should replace GC+? Last: which parts of the replacement are shown to do something?

**What was done.** 37 past GC+ jobs in PHENIX and cctbx, mostly bug fixes, were replayed with plain Claude Code from
the same starting code and the same inputs: 76 counted plain runs, each scored before and after one review pass.
Errors were found by probes, two blind readings, cross-arm probes run on every arm, and test-adequacy runs, and
were tagged major or minor by a blind tagger (Part B). A pre-registered fifth round tested two middle grounds on the
18 jobs where GC+'s layers had caught something (Part C). Then routing rules were checked (Part D), and GC+ was
replaced by the shorter GuidedCoding (Part E). GC was replayed on the 18 harder jobs (round 6, Part F), and an outside
review of the final change was measured on top of one review pass, in plain and GC runs alike (round 6b, Part G).

**Findings.**

1. **One review pass after plain Claude Code substantially reduced missed errors.** Over all 37 jobs it cut program
   errors missed per job from 0.81 to 0.47, and major errors from 0.33 to 0.24 [Src4 §4]. The review took roughly
   half as long as the plain run itself [Src17 §2.1]. It introduced 7 missed errors (3 confirmed), all in the first
   ten jobs, and no missed errors in the 27 later ones; in three runs there (langchain-cap-fix twice, auto-mmm-a once)
   it made changes the task did not ask for, which the runs disclosed [Src4 §7; Src3].
2. **GC+ and plain + one review pass are level on all errors.** GC+ 0.51 against P+R 0.47 [Src4 §4]. GC+ wrote a test
   that proves the bug in 36 of 37 jobs; plain runs lacked one in about one run in seven [Src4 §5; Src26]. Counting
   problems left in the code, whether missed or disclosed, GC+ had more recorded errors overall (1.16 against 0.74)
   but fewer major ones (0.24 against 0.34); these totals are not directly comparable, because GC+'s code was examined
   more thoroughly and GC+ recorded what it deferred [Src4 §4].
3. **On major errors GC+ leads, but the lead is small and fragile.** Over all 37 jobs: GC+ 0.16, P 0.33, P+R 0.24,
   from 6, 25 and 18 errors [Src4 §4]. Without one job, langchain-model-update, GC+ and P+R are level: 0.167 against
   0.160 [Src15].
4. **Where GC+ leads, it is mostly plain repeating mistakes that GC+'s own layers caught.** In the 18 jobs where
   GC+'s layers caught something, major errors are GC+ 0.28, P 0.62, P+R 0.49. Counting only errors first found by
   instruments that looked at every arm alike, GC+ is not ahead there: GC+ 0.28, P 0.26, P+R 0.18 [Src4 §6]. On the
   19 jobs where GC+'s layers caught nothing, GC+ has no advantage: P+R leaves fewer program errors (0.18 against
   0.32), and major errors are 0.05, 0.05 and 0.00 [Src4, Summary].
5. **A deeper search found more for GC+, and this is unresolved.** Round 5 searched those 18 jobs more deeply. On
   major errors left in the code (missed plus disclosed), GC+'s lead over P+R grew to 0.35, or 0.19 without
   langchain-model-update. Part of the growth is an artefact of where the search started (it was seeded from
   findings in the plain runs) [Src9, "The deeper baselines"]. Before the deeper search, in round 4's data, the lead
   in those jobs without that job was 0.10 on the same measure, and 0.04 on round 4's headline measure (missed only: GC+ 0.29 against P+R 0.34)
   [Src4 §3; Src9, "The deeper baselines"; Src17 §2.2]. This is the main evidence against replacing GC+.
6. **GC+ costs more.** GC+'s Claude time was 2.0 times plain's (median) and 1.3 times plain + review's over all 37
   jobs; 5.5 and 3.5 times in the hardest jobs. The outside readings, publication steps and the Developer's own time
   come on top and were not measured [Src4 §9; Src27].
7. **No middle ground clearly beat a second ordinary review.** In round 5, a GC+-style structured reviewer step
   (P+R+S) left 0.63 major errors per run in the code (missed plus disclosed; 38 runs of the 18 jobs) against 0.71
   for a second ordinary review (P+2R). The difference, −0.083, is smaller than the 0.10 margin set in advance (the
   rule needed −0.10 or lower), so by the pre-registered rule the reading is **against** the hypothesis. On
   major errors missed only, the order reverses (P+2R 0.42, P+R+S 0.46). P+R+S took about three times as long
   (2,189 against 723 minutes in all), and 28 of its 38 runs hit the 60-minute limit, so the result describes "the
   step within an hour" [Src9; Src12]. Neither extra pass fixed any **major** error that only GC+'s outside reviewer
   (3 major occurrences in P+R runs) or the Developer's live probe and the Guide (2) had caught [Src11].
8. **Routing could not be tested on these data.** Even routing chosen with hindsight could not be told apart from
   chance (p = 0.10 at best) [Src15]. A start screen that sends only jobs with a concrete trigger (a live service, another
   platform, publication, data or credentials) to the thorough route picked 12 of 37 jobs; its whole gain came from
   one job [Src16].
9. **The decision.** On 2026-10-23 the Developer replaced GC+ with GuidedCoding (GC), revision 22. It was a
   judgement aimed at a process that is easy for the developer and reliable overall, made with findings 1 to 8 in
   view: after two outside reviews of the proposal, which recommended a trial; three real jobs under drafts of the
   procedure; three outside reviews of the retirement plan, all "proceed with changes", one of which advised waiting
   for the trial's evidence (10 to 15 jobs, with the first later-defect checks due 2026-11-20) before retiring the
   kit and publishing; and three outside reviews of the release. The Developer chose to retire the kit and publish
   the same day [Src17; Src18; Src19; Src35; Src36; Src37; Src24; Src29]. **When the decision was made, the
   data did not show that GC is as useful as GC+: GC had not been replayed** (round 6 later replayed it; finding 11). They show that GC keeps the one measured gain (the review
   pass) and the proving test that GC+ also had; that GC+'s extra layers cost much more; and that their benefit,
   concentrated in harder jobs, is unresolved. GC keeps outside readings and live checks as steps for
   named triggers, the kinds of check that reached errors no review pass reached (Part E).
10. **GC's parts have different support** (Part E, table); round 6 measured GC as a whole on the 18 harder jobs
    (finding 11). Behaviour
    checks in Claude Code show its rules working in specific test cases [Src20; Src21; Src22]. The trial of the procedure
    began on 2026-10-23 with 3 jobs run under earlier drafts of it (`/lean`); later-defect checks are due from
    2026-11-20 [Src20, "Use since"; Src23; Src29].
11. **Round 6: GC replayed, no clear difference from plain + one review pass.** 38 fresh GC runs on the 18 jobs where
    GC+'s layers had caught something; 4 wrote an outside review and were continued with it (GC+O). Confirmed major
    errors left in the code (missed plus disclosed), per run: GC+ 0.44, P 0.90, P+R 0.79, GC 0.97, GC+O 0.90. GC+O −
    P+R = +0.11 (90% interval −0.19 to +0.42): by the rule fixed in advance, **no clear difference**, with the estimate
    leaning against GC+O; GC+O recovered none of GC+'s measured lead [Src39; Src40]. On major errors missed only, GC+O
    is slightly ahead (0.60 against 0.63) [Src40]. GC often left a problem as a question for the developer, which the replay's
    fixed stand-in answered "keep to the task": 11 of GC+O's 33 major errors left were asked and 7 in part, against
    1 of P+R's 29; had the questions been answered as GC recommended, the two would have been about level (0.74
    against 0.79; untested, assuming each fix worked) [Src41]. The outside review, written in 4 of 38 runs, removed 3 major errors [Src39]. By
    the rule fixed in advance, GC is kept as it is [Src43 §2].
12. **Round 6b: an outside review adds something to GC, narrowly, and not clearly to plain + one review pass.** Every
    counted round-6 GC and P+R run was resumed once with a script-built outside review of its final change from
    gpt-6.1-sol. Confirmed major errors left in the code, per run: GC 1.000 against GC+O\* 0.833 (−0.167, 90% interval
    −0.306 to −0.056): by the rule fixed in advance, **adds something**; P+R 0.847 against P+R+O 0.764 (−0.083, −0.222
    to +0.028): **no clear difference** [Src45; Src47]. In GC+O\* there were 9 run-level removals of a major error
    and 3 additions, a net of 6 removals, all of the net in four of the 18 jobs (case 1 had 2 of each and netted
    zero), and one robustness condition is one removal from failing; a single
    severity tag or a single removal decides the reading. After the review, GC is still not better than plain + one
    review + the same outside review (+0.069, −0.167 to +0.319) [Src45].
13. **The decision after round 6b, and GC 1.4.** The Developer made the outside review a standard step for difficult
    or consequential changes and an easy option for routine fixes [Src55]. Narrowing the scope rule without a further
    test, and ending the large experiments, was the Guide's recommendation, and the Developer agreed: after the Guide's analysis the Developer asked "do we need the trial that is running now?" and, after the Guide's plan (finish the trigger check, skip the send step, fold the narrowed scope rule into 1.4, then one small trial of the full 1.4), replied "that sounds good"
    [Src55]. GuidedCoding 1.4 (2026-10-26) does this. Its trial, 4 runs of an earlier draft (trigger check) and 3 runs of the full 1.4 text, with their resumes after the outside review, on
    known jobs, shows its instructions working as intended, which is an implementation check, not a measurement
    [Src52; Src53]. See Part G.

**Bottom line.** In these 37 replayed jobs, plain Claude Code followed by one review pass missed far fewer errors
than plain Claude Code alone, for about half as much again of Claude's time, and matched GC+ on all errors missed. GC+ left fewer major
errors, mostly in jobs where its own layers caught something; how much of that advantage is real is not known;
replayed on the 18 harder jobs, GC recovered none of it (Part F). GC is built on the parts with the best support. Replayed on the harder jobs, it did not leave fewer
major errors than plain + one review pass (no clear difference, leaning slightly against GC); the replay's stand-in
answered every question GC put to the developer "keep to the task", and how much this cost GC is an untested
counterfactual [Src41]. An outside review of the final change by a different model, added to GC, removed some major
errors on the harder jobs: by the rule fixed in advance it adds something, but narrowly, from four jobs, and it
brought in some errors as well (Part G). With it, GC is still not better than plain + one review pass + the same
outside review. GuidedCoding 1.4 (2026-10-26) keeps what was shown to help, makes the outside review standard for hard or
consequential changes, and narrows the scope rule; it has been checked in a small trial (4 runs of an earlier draft for the trigger, 3 runs of the full 1.4 text),
not measured. GC is being
evaluated in use.

**What the final procedure keeps, drops and narrows, and why.** The grouping follows the draft summary for the
website [Src54]; the procedure is GuidedCoding 1.4 (2026-10-26) [Src53].
- **Tested and found to help: kept.** One review pass (finding 1; on the 18 harder jobs, major errors left per run
  0.90 for P against 0.79 for P+R [Src40]). An outside review by a different model, now standard for hard or
  consequential changes and offered on every other job (finding 12). A test that proves the bug: plain runs lacked one
  in about one run in seven, GC+ in 1 of 37 jobs; its effect on errors left was not measured separately [Src4 §5].
- **Tested, with no clear benefit found: not required.** A second ordinary review pass (round 5, finding 7). The
  structured independent reviewer step, not clearly better than a second ordinary review and about three times as
  long; it stays in `REVIEWER.md` only as an option the developer must agree to [Src9; Src53].
- **Not tested; probably hurt: narrowed.** GC 1.3's strict scope rule (revert every review fix beyond the
  literal task and ask). In round 6 GC left 63 review fixes reverted under it, 6 of them fixes of counted major
  errors, each then put to the developer as a question; GC, which used the rule, left more major errors than P+R (0.97
  against 0.79). The cost is estimated from those cases, not measured [Src41]. GC 1.4 fixes real defects in the code
  the job changes and asks only before changing interfaces, defaults, file formats or behaviour callers rely on.
- **Useful but not tested: kept on judgement.** The short final report; checks against a live service; exact
  commands for another platform; care with user data and credentials (an outside review); asking before commit, push
  or install; a plan and a recovery step for consequential work [Src54; Src53].
- **Dropped with GC+** (Part E): the Guide-and-worker structure, the approval screens, the evidence packets and the kit
  code that checked them. They were measured only as part of GC+ as a whole.

**How this changed during the study.** The first report (2026-10-17, ten cases) concluded that plain Claude Code
repeated defects GC+'s layers had caught in 8 of 10 cases, even with a review pass, and supported GC+'s layers
[Src1]. Rounds 4 and 4b showed that this rested on probes built from GC+'s own catches, which can find errors only in
plain code; measured evenly, the arms came out as in findings 2 to 4 [Src4 §4, §6; Src25]. The earlier conclusion is
superseded.

## Part A. The study from start to finish

| dates (2026) | step | what was done | result | sources |
|---|---|---|---|---|
| 10-15 | Tally | GC+'s 85 task records were tallied for the defects each review layer caught. | About 330 real code or test defects caught before integration; the internal reviewer caught most, outside readers caught some the internal layers had passed. A catch count cannot show what plain Claude Code would have done. | [Src1]; [Src2] |
| 10-15 to 10-17 | Stages 1 to 3 | Ten cases where GC+ had caught something; 22 plain runs, each with one review pass, scored against checklists from GC+'s records. | Plain repeated defects GC+ had caught in 8 of 10 cases. Superseded (see the summary). | [Src1] |
| 10-19 to 10-21 | Round 4 | Every remaining suitable GC+ bug-fix job replayed (27 new cases, 37 in all); blind task probes, GC+-catch probes, a blind scorer and a blind open-ended reader. | Draft 1: GC+ 0.14 against P 0.51 and P+R 0.41. Did not stand. | [Src4 §4] |
| 10-21 | Round 4b | All 37 jobs measured alike: a second blind reading, cross-arm probes run on every arm, test-adequacy runs, the commit audit both ways, blind severity tagging. | The figures in findings 1 to 4 [Src3; Src5; Src14]. Drafts 2 and 3; two outside readings of each of drafts 1 and 2, one by a different model family. | [Src4]; [Src6]; [Src7] |
| 10-21 to 10-22 | Round 5 | Pre-registered test of two middle grounds (P+R+S and P+2R) on the 18 jobs where GC+'s layers caught something; plan frozen by hash before the pilot. | Against the hypothesis (finding 7). | [Src8]; [Src9]; [Src10]; [Src11] |
| 10-22 | Time-limit check | Where each P+R+S run stood when it ended. | 26 runs cut off without a final message; the step needs about 55 to 70 minutes. | [Src12] |
| 10-23 | Triage | A power check, and a descriptive check of a start screen and an escalation check. | Routing cannot be tested on these data (finding 8). | [Src15]; [Src16] |
| 10-23 | The case for a shorter procedure | `LEAN_GC.md` and the case for it, read by two outside reviewers; `LEAN_GC.md` was also read by a helper. | Both reviews recommended a trial; the replay study was stopped. | [Src17]; [Src18]; [Src19]; [Src32] |
| 10-23 | GuidedCoding revision 22 | `/gc` version 1.3 written, checked in Claude Code, reviewed three times, and published; GC+ retired. | Published as `cctbx/guided_coding` 852cd21; later commits up to 14b8371 added the outside review on request to `SKILL.md` and revised the README, `EVIDENCE.md` and `REVIEWER.md`. | [Src20]; [Src21]; [Src24]; [Src28] |
| 10-24 to 10-25 | Round 6 | 38 fresh GC runs on the 18 caught-any jobs (4 continued with an outside review, GC+O); every earlier instrument applied to GC, every new candidate probed on every arm; plan and reading rule fixed in advance. | No clear difference between GC+O and P+R (finding 11). Three outside readings of the report, all accepting it (two with changes, taken in). | [Src39]; [Src40]; [Src41]; [Src43]; [Src44] |
| 10-25 to 10-26 | Round 6b (step O) | Every counted P+R and round-6 GC session resumed once with a script-built outside review of its final change (P+R+O, GC+O\*); scored at round 6's depth; reading rules fixed in advance. | Outside review adds something to GC, narrowly; no clear difference for P+R (finding 12). An internal check, "accept with changes" (8 findings); one outside reading, "accept with small changes". | [Src45]; [Src46]; [Src47]; [Src50]; [Src51] |
| 10-26 | GuidedCoding 1.4 (2026-10-26) | The Developer's decisions; trigger H with an outside review; a narrower scope rule; two small trials (4 runs of an earlier draft for the trigger check; 3 runs of the full 1.4 text, with their resumes). | Works as intended on the trial jobs (finding 13). | [Src52]; [Src53]; [Src55] |
| 10-23 onward | Real-use trial | Each job logged, with a later-defect check about four weeks after. | 3 jobs logged on 2026-10-23, run under earlier drafts of the procedure (`/lean`). | [Src23]; [Src29] |

**People and models.** Every worker, scorer, reader, tagger and checker in the study was a Claude model. Drafts 1
and 2 of the round-4 report and the round-5 plan each had one outside reader from a different model family; draft 3
(Part B), the round-5 report and the triage work had Claude checkers only [Src6; Src7; Src30; Src31; Src17 §1]. In round 6
the outside review (GC+O and the P+R search) came from a different model, gpt-6.1-sol [Src39], as did every outside review in
round 6b and in the GC 1.4 trial [Src45; Src52]. The Developer's own judgement entered at the points the
record quotes.

# Part B. Rounds 4 and 4b

Reproduced from report draft 3 [Src4], with the arm labels renamed, its opening paragraph left out and nothing else changed. Section numbers are draft 3's. In its Terms, "(GuidedCoding)" refers to GuidedCoding Plus. The appendix it refers to is Appendix A at the end of this report.

## Terms

- **People and process.** The **Developer** is the PHENIX developer whose jobs these are. The **Guide** is the Claude
  session that ran this study. **GC+** (GuidedCoding) is a layered review procedure for Claude Code bug fixes. Its
  **layers** are the reviewers inside a GC+ job: an internal reviewer, outside readings, a helper, and the Developer's
  approvals. A **draft error** is an error in GC+'s own draft that a layer caught and that GC+ fixed before finishing.
- **Arms.** **GC+** is GC+'s final change. **P** is a plain Claude Code run on the same job. **P+R** is the same plain
  session after one `/code-review --fix` pass.
- **Rates.** Unless a line says otherwise, a figure is **confirmed program errors missed**, per GC+ job or per plain
  run, averaged within each case and then across cases.
- **Major and minor.** **Major** errors are those a blind tagger, with arm names removed (§10 lists six
  descriptions that still named one), judged to give wrong
  results or output silently, crash or hang a normal run, lose data, open a real security hole, or leave the reported
  problem unfixed (§2). Every other real error is **minor**.
- **Everything left.** Confirmed program errors an arm missed *plus* those it found, left on purpose and disclosed
  ("deferred"). Test rows and scope items are not in it, and pre-existing faults only on the line that says so.
- **Evidence.** *Confirmed:* shown by a probe, a test or reading the code. *Probable:* strong but not shown, for
  example a call based on a model table rather than a live service. *Undetermined:* could not be decided; never
  counted.
- **Other terms.** The **end point** is the arm's final change. A **scope item** is a design or scope difference, not
  an error; it is never counted. **packet-16** is the frozen set of round-4 inputs and tools, and **packet-17** is the
  review bundle of draft 1. Probe and finding ids such as D1 or E4 are per-case labels from the ledger.
- **The ten original cases** are numbered 1 to 10: 1 GUI output (o01-gui-output), 2 atomic writes (o02-atomic), 3 map
  manager follow-ups (o03-mmm-followups), 4 anisotropy (o04-aniso), 5 Windows stop (o05-win32), 6 publication precheck
  (o06-precheck), 7 reply cut-off (o07-cutoff), 8 sequence from map (o08-sfm), 9 EBADF (o09-ebadf), 10 elbow
  (o10-elbow).

## Summary

The 37 jobs are split by how hard they turned out to be for GC+'s own process: the number of draft errors GC+'s layers
caught and fixed during the job. That count comes from GC+'s record, not from the plain runs. The cut-offs (3 or more,
1–2, none) were chosen after the round-4 figures for each group had been seen, so the groups describe an
association, not a test of a rule fixed in advance (§3 gives other cut-offs, and the simpler split "caught any /
caught none", which the table also shows).

| group | jobs | program errors missed GC+ / P / P+R | **major only** GC+ / P / P+R | everything left GC+ / P / P+R | no test that proves the bug GC+ / P / P+R | GC+ time ÷ P: median (ratio of total minutes) |
|---|---|---|---|---|---|---|
| hard: GC+ caught 3 or more draft errors | 9 | 1.11 / 1.61 / 1.14 | **0.44 / 1.03 / 0.81** | 1.44 / 1.89 / 1.50 | 0.00 / 0.11 / 0.06 | 5.5× (4.8×) |
| medium: caught 1–2 | 9 | 0.33 / 0.61 / 0.39 | **0.11 / 0.22 / 0.17** | 1.00 / 0.83 / 0.61 | 0.00 / 0.22 / 0.22 | 2.3× (3.3×) |
| easy: caught none | 19 | 0.32 / 0.53 / 0.18 | **0.05 / 0.05 / 0.00** | 1.11 / 0.71 / 0.45 | 0.05 / 0.13 / 0.13 | 1.6× (1.3×) |
| *caught any (hard + medium)* | 18 | 0.72 / 1.11 / 0.76 | 0.28 / 0.62 / 0.49 | 1.22 / 1.36 / 1.06 | 0.00 / 0.17 / 0.14 | |
| *all 37 (background)* | 37 | 0.51 / 0.81 / 0.47 | 0.16 / 0.33 / 0.24 | 1.16 / 1.03 / 0.74 | 0.03 / 0.15 / 0.14 | 2.0× (2.6×) |

What this says, within the limits in §10. The counts behind the major-only column are small: 6 GC+ errors in 37 jobs,
against 25 for P and 18 for P+R (hard group: 4, 19, 15).

- **Hard jobs.** Plain Claude Code leaves more errors than GC+: 1.61 against 1.11 per job, and about twice as many
  major errors (1.03 against 0.44).
  - **Against plain + review the picture rests on two cases.** On all errors, P+R (1.14) is level with GC+ (1.11)
    because of case 6, where seven errors are left in GC+'s code (five of them found by round 4b's cross-arm probes); without case 6, GC+ 0.38 against P+R
    1.03. On major errors, P+R (0.81) is above GC+ (0.44) mostly because of langchain-model-update, where both plain
    runs keep three major errors through the review pass; without it, GC+ 0.50 against P+R 0.53.
  - **Where the gap against plain alone comes from.** Mostly from the two new hard jobs, langchain-model-update and
    langchain-test-health: GC+ left no errors in either, and plain left 2.0 per run. In the seven hard original
    cases GC+ and plain are about level (all errors 1.43 against 1.50; major 0.57 against 0.75), and plain + review is
    lower than both (0.96; major 0.54).
  - **Where the errors were first found.** Many of plain's hard-group errors were first found by probes built from
    GC+'s own caught draft errors. Counting only errors first found by instruments that looked at every arm alike, the
    hard group is GC+ 1.11, P 0.72, P+R 0.47 (major 0.44 / 0.53 / 0.36). This is a sensitivity check, not an
    alternative score: those errors are real errors in plain's final code (§6).
  - **Cost.** GC+ took about five times plain's time (3.5× plain + review, medians).
- **Medium jobs.** The same direction, but smaller and on few errors.
  - **Major errors:** 0.11 against 0.22 (P) and 0.17 (P+R), which is 1, 4 and 3 errors.
  - **All errors:** GC+ 0.33, plain 0.61, plain + review 0.39.
  - **Probable errors added in:** GC+ is above plain + review (0.67 against 0.44).
- **Easy jobs.** No advantage for GC+.
  - **Major errors:** one error in 19 jobs, S069, left by GC+ and by both plain runs of auto-q2m-b and fixed by both
    review passes.
  - **All errors:** plain + review leaves fewer than GC+ (0.18 against 0.32).
  - **Cost:** GC+'s Claude time was 1.6× plain's, and about the same as plain + review's (0.8× by medians, 0.9× by
    total minutes). GC+'s uncounted costs (outside readings, publication, the Developer's time) come on top (§9).
- **Tests.** Every GC+ job but one has a test that proves the bug: the test fails on the starting code and passes on
  GC+'s. The exception, gc-rev15-macos-ci, is a CI failure that cannot be reproduced on this Mac, and no arm has a
  proving test there. About one plain run in seven has no such test (§5).
- **Problems left on purpose.** GC+ finds and records many problems that it then leaves, mostly minor ones, stated
  limits or approved follow-ups. Counting everything left in the code, disclosed or not, GC+'s code holds more than
  both plain arms' in the medium and easy groups and over all 37 (1.16 against 1.03 and 0.74); in the hard group it is
  below plain's and about level with plain + review's (1.44 against 1.89 and 1.50; §4).

So, on these jobs: **GC+'s advantage, where it shows, is on major errors against plain Claude Code alone, in jobs
where GC+'s layers caught something. It rests on few errors and a few jobs.** In the 18 jobs where GC+'s layers caught
anything, major errors are GC+ 0.28, P 0.62, P+R 0.49; in the hard group most of the gap against plain alone comes
from two new jobs. **The advantage is mostly plain repeating mistakes that GC+'s layers caught in GC+'s own drafts:**
counting only errors first found by instruments that looked at every arm alike, those 18 jobs are about level on
major errors (GC+ 0.28, P 0.26, P+R 0.18; §6). **Against plain + one review pass, an advantage is not established:** on all errors the two are
level, and on major errors GC+'s lead (4 errors against 15 in the hard group) disappears without one case,
langchain-model-update. **On easy jobs there is no advantage for GC+;** plain + one review pass does as well or better
on errors, for about the same Claude time. These are associations with how much GC+'s layers caught, a number known
only from GC+'s own process; they are not evidence that GC+ would do better on jobs judged hard in advance. A usable
rule would need signs of difficulty visible before the job starts (§10).

## 1. What was done

**Round 4** (draft 1, method unchanged):
- **Jobs.** Every remaining suitable GC+ bug-fix job was replayed, so that the comparison no longer depends on which
  jobs were chosen. Of 30 jobs prepared, 3 were unsuitable:
  - `gc-app-version-check` needs a live Claude app session;
  - `batch4-q4b-a` needs the setuid `/bin/ps` and real Linux;
  - `gc-linux-container` runs only in a Linux container.

  That gives **27 new cases**, plus the **10 original cases**, whose plain runs were not rerun. The 37 jobs are a
  census of the suitable jobs, not a random sample of wider work.
- **Arms.**
  - **GC+:** GC+'s final change, taken from its own parent commit.
  - **P:** a headless `claude -p` run in a sealed installation: Opus 5.5, or Fable 5.1 where GC+'s worker used it;
    effort xhigh; 90 minutes.
  - **P+R:** the same session resumed for one `/code-review --fix` pass (45 minutes).

  Every case has 2 plain runs, except case 1 (an original case), which has 4.
- **Inputs.** Each replay got what the GC+ session got from the Developer, word for word, and nothing GC+ produced.
  Four mild leaks are declared and kept (§10).
- **Round-4 evidence:**
  - **blind task probes,** written from the task alone;
  - **GC+-catch probes,** built from the draft errors GC+'s layers caught (they can only find errors in plain code);
  - **a blind checklist scorer;**
  - **a blind open-ended reader,** which sees all arms' diffs with the labels hidden.

  Workers turned the evidence into ledger rows, and a checker verified a sample.

**Round 4b** (new in this draft; all 37 jobs, both arms alike):
- **A second blind reading.** It is checklist-driven and is given the bug report, the attachments and the starting
  source of every touched file (`r4_out/<case>/readings2/`).
- **Cross-arm probes.**
  - **What:** every candidate error from any source was written as a behaviour probe. Sources include the ledger,
    both readings, the review passes, the commit audit and GC+'s record.
  - **Where it ran:** on the starting code, on GC+ and on every plain arm (`walkthrough/r4_cross/<case>/`).
  - **Why:** this makes the GC+-catch idea two-sided.
- **Test-adequacy runs.** Each arm's own tests were run on four versions: its own code, the starting code, a blind
  seeded correct fix and a blind seeded partial fix (`replay/r4b_tests/`).
- **The commit audit, applied both ways** (`AUDIT_VS_R4.md`). Where a later GC+ commit showed a GC+ error, the matching
  plain rows got the same check.
- **Severity tagging.**
  - **What was tagged:** the 205 distinct errors (case and id) that some arm left at the end point (`r4_severity/`).
  - **First tagging:** its input named the arm in the source column of about 80 rows, and named GC+ in four
    descriptions, so it was not fully blind.
  - **Second tagging, used here:** a fresh tagger working from the same descriptions with arm names removed (six
    descriptions still named an arm or an earlier call; §10). It
    found 49 major errors, 153 minor and 3 not errors.
  - **Agreement:** the two taggings agree on 87% of items (Cohen's κ 0.64; `r4_severity/AGREEMENT.txt`). §10 gives
    the major-only figures under the first tagging.

## 2. Counting rules

- **Counted:** an error that **remains** at the end point or was **fixed later**. Program errors are of two kinds:
  - **task errors,** the reported problem not fixed, whatever their origin;
  - **product errors the arm made itself,** including those a review pass introduced.

  Confirmed and probable evidence are kept apart.
- **Not counted in the headline, shown apart:**
  - **Deferred:** found, left on purpose and disclosed, by either arm. A disclosure in a plain run's final message
    counts. P+R is the P session resumed, so a problem P disclosed stays disclosed for P+R unless P+R fixed it. This
    carry-over rule was adopted after the checker reading (24 P+R rows; `r4_ledger/RULINGS.md`); §10 gives the figures
    without it.
  - **Pre-existing faults:** already in the code and left by an arm. All 37: GC+ 0.46, P 0.61, P+R 0.34.
  - **Scope:** design or scope differences listed for each case, and the three items the blind tagger called not
    errors (S112, S137, S160).
- **auto-q2m-c.** All four plain arms changed no code. Each asked for a behaviour decision about placeholder map
  managers, although the prompt said to work autonomously; GC+'s session settled that question with the Developer.
  - **Reading:** these runs are **incomplete, with a justified request for a decision**.
  - **Counted:** the headline leaves them out. Counted as missed, the all-37 plain rates go 0.81 → 0.84 (P) and
    0.47 → 0.49 (P+R).
- **Severity rubric** (applied blind):
  - **Major:** in normal use it gives wrong results or wrong output silently, crashes or hangs a normal run, loses or
    overwrites data, is a real security problem, or leaves the reported problem unfixed. For a test, there is no test
    that would fail if the bug came back.
  - **Minor:** any other real error.
- **What major and minor look like.** Appendix A lists all 205 errors with both taggings and the second tagger's
  reason. Some examples:
  - **major:**
    - `--dry-run` refuses every SSH or `user@` remote, so it cannot be used in normal work (case 6, plain; S045);
    - an unvalidated remote name lets a record pass `--upload-pack` to `git fetch` (case 6, GC+; S179; but see §10:
    an earlier ruling called this minor);
    - the decision call crashes on the new default model's thinking block (langchain-model-update, plain; S134);
    - a grid passed as a list silently drops the map's symmetry to P1 (auto-q2m-b; S069);
  - **minor:**
    - any `insteadOf` rule makes the precheck refuse: over-strict, but it fails safe (case 6, GC+; S098);
    - a printed push command is not shell-quoted (case 6, GC+);
    - a test fixture's file encoding weakens the setup (case 9; S000).

## 3. Hard, medium and easy jobs

**How the groups are made.** A job's group is the number of draft errors GC+'s layers caught and fixed in it. These
are GC+ rows of origin own or review that ended fixed and are not scope.
- **What is fixed in advance and what is not.** The *count* is a property of the job as GC+ met it, taken from GC+'s
  record, not from the plain runs. The *cut-offs* (3 or more, 1–2, none) were proposed on 2026-10-21 together with
  each group's round-4 figures, so they were chosen after results were seen.
- **Later rulings set two jobs' counts.** Two rulings on langchain-cap-fix (a catch ruled harmless, so scope, and
  another found already in the starting code, so not GC+'s own) moved it from medium to easy, and the scope ruling on langchain-model-update's D3 left that job at exactly 3, on the cut-off.
- **So the groups show an association** between how much GC+'s layers caught and how the arms compare. They are not a
  test of a rule fixed in advance, and they do not show that GC+ would do better on jobs judged hard independently.

**Other cut-offs.** The pattern holds across cut-offs: GC+ is below plain alone on major errors, and plain + review is
about level with GC+ on all errors, except at "4 or more", where it is below GC+ (0.96 against 1.29). "Hard" is not a
sharp line; the steadiest split is "caught any" against "caught
none".

| jobs where GC+'s layers caught | jobs | of which original | all errors GC+ / P / P+R | major only GC+ / P / P+R |
|---|---|---|---|---|
| 1 or more ("caught any") | 18 | 10 | 0.72 / 1.11 / 0.76 | 0.28 / 0.62 / 0.49 |
| 2 or more | 12 | 8 | 1.00 / 1.50 / 1.02 | 0.42 / 0.77 / 0.60 |
| 3 or more (hard) | 9 | 7 | 1.11 / 1.61 / 1.14 | 0.44 / 1.03 / 0.81 |
| 4 or more | 7 | 6 | 1.29 / 1.43 / 0.96 | 0.43 / 0.82 / 0.61 |
| none ("caught none", easy) | 19 | 0 | 0.32 / 0.53 / 0.18 | 0.05 / 0.05 / 0.00 |
| 1 or more, without langchain-model-update | 17 | 10 | 0.76 / 1.00 / 0.63 | 0.29 / 0.49 / 0.34 |

The number of catches per job is listed in `LEDGER_R4_SUMMARY.md` ("Draft-3 additions").

- **Hard (9 jobs):** cases 1, 2, 3, 5, 6, 8 and 9; langchain-model-update; langchain-test-health.
- **Medium (9):** cases 4, 7 and 10; gc-next-revision, langchain-gemini-openai, langchain-provider-todos,
  mmm-cc-star-none, phenix-chat-tools and process-raw-data-reconstructed-f.
- **Easy (19):** the other 19 new cases.

**Full table.** Each cell is GC+ / P / P+R, confirmed unless stated.

| group | program errors missed | major only | confirmed + probable | share of jobs / runs with any | share with any major | ledger test gaps | major, everything left |
|---|---|---|---|---|---|---|---|
| hard | 1.11 / 1.61 / 1.14 | 0.44 / 1.03 / 0.81 | 1.11 / 1.61 / 1.14 | 0.44 / 0.86 / 0.78 | 0.33 / 0.64 / 0.53 | 0.22 / 1.64 / 1.53 | 0.56 / 1.31 / 1.03 |
| medium | 0.33 / 0.61 / 0.39 | 0.11 / 0.22 / 0.17 | 0.67 / 0.83 / 0.44 | 0.22 / 0.44 / 0.33 | 0.11 / 0.22 / 0.17 | 0.11 / 0.50 / 0.44 | 0.22 / 0.33 / 0.28 |
| easy | 0.32 / 0.53 / 0.18 | 0.05 / 0.05 / 0.00 | 0.32 / 0.58 / 0.21 | 0.21 / 0.39 / 0.18 | 0.05 / 0.05 / 0.00 | 0.11 / 0.16 / 0.08 | 0.11 / 0.11 / 0.05 |

**Hard jobs, case by case.** Confirmed program errors missed, with major in brackets; plain figures are per run, and
case 1 has four runs, so 0.2 is 0.25 rounded.

| case | GC+ | P | P+R |
|---|---|---|---|
| 1 GUI output | 1 (0) | 1.0 (0.2) | 0.8 (0.2) |
| 2 atomic writes | 0 | 2.0 (0) | 1.0 (0) |
| 3 map manager follow-ups | 0 | 0.5 (0.5) | 0.5 (0.5) |
| 5 Windows stop | 1 (1) | 1.0 (1.0) | 1.0 (0.5) |
| 6 publication precheck | 7 (2) | 3.5 (2.0) | 2.0 (1.5) |
| 8 sequence from map | 1 (1) | 1.5 (0.5) | 0.5 (0) |
| 9 EBADF | 0 | 1.0 (1.0) | 1.0 (1.0) |
| langchain-model-update | 0 | 3.0 (3.0) | 3.0 (3.0) |
| langchain-test-health | 0 | 1.0 (1.0) | 0.5 (0.5) |

- **The hard group by origin.**

  | hard jobs | jobs | all errors GC+ / P / P+R | major only GC+ / P / P+R |
  |---|---|---|---|
  | original cases (1, 2, 3, 5, 6, 8, 9) | 7 | 1.43 / 1.50 / 0.96 | 0.57 / 0.75 / 0.54 |
  | new cases (langchain-model-update, langchain-test-health) | 2 | 0.00 / 2.00 / 1.75 | 0.00 / 2.00 / 1.75 |

  The hard-group gap against plain alone comes mostly from the two new jobs. In the seven original cases GC+ and plain
  are about level, and plain + review is lowest.
- **Case 6 explains most of GC+'s all-errors figure in the hard group.**
  - **The change:** before the first ten got round 4b, GC+'s hard-group figure was 0.22 (2 errors). It is now 1.11
    (10 errors). Case 6 gave 5 of the 8 added errors; the other three are in cases 1, 5 and 8.
  - **What case 6 is:** the job is GC+'s whole publication-precheck tool. Its seven errors are:
    - the merge commit's second parent is not checked (major);
    - `--fetch` runs before the destination check;
    - the record's remote name is not validated before `--fetch`, so `--upload-pack` can run a command (major);
    - `--fetch` creates local tags;
    - a `push.recurseSubmodules` gitlink is accepted with only a note;
    - any `insteadOf` rule causes an over-strict refusal;
    - the printed command is not quoted.

    Two of the seven (the merge parent and fetch-first) were in the ledger before round 4b. The cross-arm probes found
    the other five.
  - **Without case 6:** the hard group is GC+ 0.38, P 1.38, P+R 1.03 (major 0.25 / 0.91 / 0.72).
- **langchain-model-update weighs most on the plain side.** Both plain runs keep the same three major errors through
  the review pass:
  - a crash on the new default model's thinking block;
  - a log summariser crash on list content;
  - output still capped at 2000 tokens with thinking on.

  A fourth problem, the unfinished provider updates, both P runs disclosed; it now stays disclosed for P+R. Without
  this case the hard group is GC+ 1.25, P 1.44, P+R 0.91 (major 0.50 / 0.78 / 0.53). Without both case 6 and this case
  it is GC+ 0.43, P 1.14, P+R 0.75 (major 0.29 / 0.61 / 0.39).

## 4. Background: all 37, the first ten and the 27 new

| | GC+ | P | P+R |
|---|---|---|---|
| **All 37:** program errors missed | 0.51 | 0.81 | 0.47 |
| major only | 0.16 | 0.33 | 0.24 |
| confirmed + probable | 0.59 | 0.89 | 0.49 |
| share of jobs / runs with any | 0.27 | 0.52 | 0.36 |
| everything left (missed + disclosed) | 1.16 | 1.03 | 0.74 |
| major, everything left | 0.24 | 0.45 | 0.34 |
| everything left, including pre-existing faults | 2.19 | 2.00 | 1.42 |
| same, major only | 0.51 | 0.75 | 0.56 |
| reported problem still present (blind task probe) | 0.00 | 0.05 | 0.05 |
| ledger test gaps (missed edge cases) | 0.14 | 0.60 | 0.52 |
| **First ten:** program errors missed | 1.00 | 1.40 | 0.97 |
| major only | 0.40 | 0.72 | 0.53 |
| **27 new:** program errors missed | 0.33 | 0.59 | 0.28 |
| major only | 0.07 | 0.19 | 0.13 |
| everything left (missed + disclosed) | 1.11 | 0.80 | 0.54 |
| 27 new without langchain-model-update (26 jobs) | 0.35 | 0.50 | 0.17 |
| same, major only | 0.08 | 0.08 | 0.02 |

**What round 4b changed.**

| confirmed program errors missed | draft 1 (round 4) | draft 2 (round 4b) |
|---|---|---|
| 27 new | GC+ 0.15 / P 0.24 / P+R 0.17 | **0.33 / 0.59 / 0.28** |
| first ten | 0.20 / 1.23 / 1.07 | **1.00 / 1.40 / 0.97** |
| all 37 | 0.14 / 0.51 / 0.41 | **0.51 / 0.81 / 0.47** |

Notes on the table:
- The draft-1 figure for the 27 new includes the commit-audit corrections. Draft 1's printed figures were 0.11 /
  0.24 / 0.17, and 0.16 for GC+ over all 37 after the audit (`AUDIT_VS_R4.md`).
- The draft-2 P+R figures use the carry-over rule (§2). Without it they are 0.33 (27 new), 0.97 (first ten) and 0.51
  (all 37).

- **In the 27 new, round 4b about doubled both arms' counts,** as the recall check had predicted (§6): GC+ ×2.2, P
  ×2.5, P+R ×1.9 on the old rule. **In the first ten it raised GC+'s count fivefold and plain's hardly at all,**
  because the GC+-catch probes had already searched plain's code there and nothing had searched GC+'s as hard. Even now
  both arms' counts are probably still too low (§10).
- **Draft 1's headline (0.14 against 0.51) does not stand.** It rested on probes built from GC+'s own catches, which
  look only at plain code. Measured evenly over all 37:
  - **all errors:** GC+ (0.51) and plain + one review pass (0.47) are about level; plain without review leaves more
    (0.81);
  - **major errors:** GC+ 0.16, P 0.33, P+R 0.24, from 6, 25 and 18 errors.

  Of all confirmed missed rows (program and test, all arms), 61 are major and 152 minor.
- **Confirmed + probable** is close to the confirmed line except for GC+ in the medium group (0.33 → 0.67, above
  P+R's 0.44). So the picture does not depend on how the probable rows are called, except there.
- **Everything left.** This counts the problems an arm found and left on purpose as well as the missed ones.
  - **All errors:** GC+'s code holds more than plain + review's: 1.16 against 0.74 over all 37, and 1.11 against 0.54
    in the 27.
  - **Why this is unfair to GC+:** GC+'s reviewers searched GC+'s code hardest, so GC+ has more recorded. Most of GC+'s
    deferrals are minor, stated limits or approved follow-ups.
  - **Major errors:** the everything-left count still favours GC+ (0.24 against 0.45 and 0.34).
  - **With pre-existing faults** (review 2 asked for this "when discussing total remaining problems"): 2.19 / 2.00 /
    1.42 all, 0.51 / 0.75 / 0.56 major.

  Neither count alone says which arm's finished code is better, so both are shown.
- **langchain-model-update is the case that weighs most in the new-case gap.** Without it, the 27 new give GC+ 0.35,
  P 0.50 and P+R 0.17; on major errors 0.08, 0.08 and 0.02. Its blind-probe failures are in simulated model replies,
  not confirmed against live services.
- **Cross-arm probes cut both ways.**
  - Many problems GC+ disclosed and deferred are present, undisclosed, in plain arms.
  - Some errors are in GC+'s version only: case 6's five probe-found errors, and langchain-gemini-openai's Gemini
    list-of-blocks replies read as text (S133, GC+'s one major error in the medium group).
  - Some are left by GC+ and by plain alike: the auto-q2m-a shared-NCS relabel, left by GC+ and both plain runs and
    fixed or disclosed by both review passes.
  - Others are wrong in plain only, such as developer-page-followups' Windows share links.
  - Probe calls judged artefacts were dropped for both arms (§10).

## 5. Tests

**Test adequacy.** Each arm's own tests were run on its own code and on the starting code (`TEST_ADEQUACY.md`).

| share of jobs / runs with **no test that proves the bug** | GC+ | P | P+R |
|---|---|---|---|
| first ten | 0.00 | 0.20 | 0.15 |
| 27 new | 0.04 | 0.13 | 0.13 |
| all 37 | 0.03 | 0.15 | 0.14 |
| hard | 0.00 | 0.11 | 0.06 |
| medium | 0.00 | 0.22 | 0.22 |
| easy | 0.05 | 0.13 | 0.13 |
| caught any (hard + medium) | 0.00 | 0.17 | 0.14 |

- **GC+ added a test that proves the bug in 36 of 37 jobs.**
  - **The exception:** gc-rev15-macos-ci, whose CI failure cannot be reproduced on this Mac. No arm has a proving
    test there.
  - **Corrected from draft 2:** plain p1 (P and P+R) had been credited with a proving test there. Its changed
    `tst_guided_coding.py` fails on the starting code only with "ERROR: changed source file:
    tests/tst_auto_queue_v20.py", the kit's own source-integrity check, not the CI failure. A base failure of that
    kind no longer counts (`ta_summary.py`). This raises plain's all-37 figures from 0.14 to 0.15 (P) and 0.12 to
    0.14 (P+R).
  - **Without this case,** the 27 new give GC+ 0.00, P 0.10, P+R 0.10.
  - **Case 6's third GC+ test.** GC+ changed three test files in case 6. Two pass on GC+'s code and fail on the starting
    code (largely because the precheck module does not exist there), so GC+ is credited. The third, `tst_screen_check_v20.py`, fails on GC+'s own code in the scratch installation
    (19 failures, 43 errors), and fails identically on the starting code and both seeded fixes, which points to the
    installation rather than the code. The failure we read is the kit refusing a symbolic link: the scratch installation links
    unchanged modules, which the kit's check refuses by design. A test that fails on its arm's own code is not judged
    for any arm, so it does not count for or against GC+, but the run was not clean.
- **Plain runs had no proving test in about one run in seven.** In some there was no test at all: auto-q2m-c's
  stopped runs, mmm-cc-star-none, and one run of case 8, both before and after review. In others the tests did not
  fail on the starting code, or the arm's own tests failed.
- **The seeded-fix measures are a limit, not a quality score.** Most arms' tests, about two thirds, fail on the blind
  seeded correct fix, because they test the arm's own design (names, messages, files). Nearly all tests catch the
  seeded partial fix. These measures say little about either arm.
- **Ledger test gaps** are missed edge cases a test should cover: all 37 GC+ 0.14, P 0.60, P+R 0.52; 27 new 0.19 / 0.28
  / 0.19. Few are major (all 37: 0.03 / 0.07 / 0.07), because a test that proves the bug usually exists.

## 6. Why the first ten looked so different, and what the measurement showed

Draft 1 explained the gap between the first ten and the 27 by selection and job mix. Both reviews disputed that.
The corrected account follows (`FIRST_TEN_VS_NEW.md`, `BLIND_RECALL_FIRST_TEN.md`, `FIRST_TEN_VS_NEW_4b.txt`).

- **Measurement.** In the first ten, most of plain's errors were found by GC+-catch probes, which look only at plain.
  In round 4, 22 of plain's 26 confirmed first-ten errors came from them; after round 4b it is 21 of 30.
- **Recall (round-4 figures).** The round-4 blind reader was checked against every first-ten row:
  - it named 55% of program errors (77% counting partial matches) and 35% (47%) of test gaps;
  - its recall for GC+ was similar or higher, but on only 8 GC+ rows;
  - crediting it where it named an error, first-ten plain was 0.88 (P) and 0.68 (P+R), against GC+ 0.20;
  - the blind task probes found none of the first-ten errors beyond the reported symptom.

  So one blind reading finds about half the errors.
- **Symmetric instruments only, after round 4b.** Counting only instruments that looked at every arm alike (task
  probes, the readers, review passes and cross-arm probes), the figures are:
  - first ten: GC+ 1.00, P 0.40, P+R 0.23;
  - all 37: GC+ 0.51, P 0.49, P+R 0.21.

  GC+-catch rows add first-ten P 1.00 and P+R 0.75, and nothing for GC+. That is not a measurement gap on GC+'s side.
  GC+-catch errors are errors GC+ made in its draft and then fixed (20 of the 21 first-ten rows match a fixed GC+ draft
  error), so GC+ has none at the end point. They show what plain repeats of GC+'s caught mistakes.
- **Source of discovery by group** (review 2 of draft 2; `FIRST_TEN_VS_NEW_4b.txt` §7). "Symmetric only" leaves out
  errors first found by GC+-catch probes. It is a sensitivity check, not an alternative score: the GC+-catch errors are
  real errors in plain's final code, and GC+ fixed the same errors in its drafts.

  | group | all instruments GC+ / P / P+R | symmetric only | major, all | major, symmetric only |
  |---|---|---|---|---|
  | hard | 1.11 / 1.61 / 1.14 | 1.11 / 0.72 / 0.47 | 0.44 / 1.03 / 0.81 | 0.44 / 0.53 / 0.36 |
  | medium | 0.33 / 0.61 / 0.39 | 0.33 / 0.17 / 0.00 | 0.11 / 0.22 / 0.17 | 0.11 / 0.00 / 0.00 |
  | easy | 0.32 / 0.53 / 0.18 | 0.32 / 0.53 / 0.18 | 0.05 / 0.05 / 0.00 | 0.05 / 0.05 / 0.00 |

  | caught any (hard + medium) | 0.72 / 1.11 / 0.76 | 0.72 / 0.44 / 0.24 | 0.28 / 0.62 / 0.49 | 0.28 / 0.26 / 0.18 |

  Read together with the bullet above: the GC+-catch errors are real errors left in plain's final code, so they belong
  in the count. But GC+'s advantage in the hard and medium groups comes mostly from them, that is, from plain repeating
  mistakes GC+'s own layers caught and fixed in GC+'s drafts. On errors first found by instruments that looked at every
  arm alike, GC+ is not ahead. So the result shows the value of GC+'s layers as a way to catch those mistakes, more than
  a difference in finished-code quality found independently.
- **The first ten are harder jobs.**
  - All ten had GC+ catches (3.8 per job), against 8 of the 27 (1.9 per job).
  - Seven of the nine hard jobs are from the first ten.
  - Jobs that trip GC+'s reviewers trip plain Claude Code too.
- **Job mix is not the explanation, and the program-bug advantage depends on the first six.**

  | program bug fixes, confirmed program errors missed | jobs | GC+ | P | P+R | P, symmetric instruments only |
  |---|---|---|---|---|---|
  | first ten | 6 | 0.33 | 1.17 | 0.83 | 0.08 |
  | 27 new | 10 | 0.20 | 0.35 | 0.05 | 0.35 |
  | all | 16 | 0.25 | 0.66 | 0.34 | |

  - **The first six:** GC+'s advantage on program bug fixes is large there. Almost all of plain's excess comes from
    GC+-catch probes (0.08 on symmetric instruments).
  - **The new ten:** the advantage is much smaller, and plain + review leaves fewer than GC+ (0.05 against 0.20).
    Counting auto-q2m-c's stopped runs as incomplete brings P+R there closer to GC+ (about 0.15 against 0.20; review 2).
- **Inputs: checked, and not the explanation** (`PROMPT_HINTS_FIRST_TEN.md`). Round 4 gave every new replay the
  Developer's original inputs word for word. The ten original prompts were written in the first study under stricter
  leak rules, so a reviewer asked whether they held back hints. Each of the ten was checked against the GC+ job's
  record and, where needed, the original session transcripts.
  - **The Developer's own input:** in none of the ten did plain's prompt leave out a fix, cause or location the
    Developer gave GC+ at the start. Bug-report attachments are byte-identical. Two pieces of Developer-provided data
    reached plain in another form: in case 6 a reconciliation attachment was left out, but its precheck content is
    restated in the prompt; in case 10 the saved Linux logs, which the Developer let GC+'s worker read, reached plain
    as a text summary of their facts (slight).
  - **GC+'s own earlier output was withheld, as the leak rules require.** In case 2 the writers' file names came from
    the Guide's earlier message; all four plain arms found all three writers anyway. In case 5 the cause had been
    stated by GC+'s own reviewer in an earlier job, and a bullet about a skipped job pointed at the unbounded wait
    (D1) that plain missed in 3 of 4 arms. That is a slight GC+-made advantage; GC+'s first approved plan did not act on
    that bullet either.
  - **The other way:** plain got some small text GC+ wrote before implementing (for example case 6's interface and
    case 7's goal sentence), and none of it names a scored fix.
  - **Larger and already listed:** GC+'s mid-job decisions by the Developer in cases 4, 5, 8 and 10
    (`STEP1_FAIRNESS.md`), which plain could not get.

## 7. GC+'s layers, and one review pass

- **GC+'s own drafts.** GC+'s layers caught and fixed 53 errors in 18 of the 37 jobs: 38 in the first ten and 15 in the
  27. Every plain run made the same error at the end point for 15 of them, some runs for 5, and none for 33.
- **One review pass (P+R against P).**
  - **All 37:** it fixed 67 ledger rows (53 confirmed) and introduced 7 missed rows (3 confirmed), all of them in the
    first ten.
  - **The 27:** it fixed 43 rows (34 confirmed) and introduced none.
  - **langchain-model-update:** it left all three major errors.

## 8. Task categories (description only)

The categories are by task type, set by the Guide (`r4_ledger/CATEGORIES.tsv`). Most hold 4–8 jobs, too few for
conclusions, so the table only describes where the errors fell.

| category | jobs | program errors missed GC+ / P / P+R | ledger test gaps GC+ / P / P+R | GC+ time ÷ P, median |
|---|---|---|---|---|
| program bug fix | 16 | 0.25 / 0.66 / 0.34 | 0.00 / 0.75 / 0.78 | 2.6× |
| GUI bug fix | 4 | 0.25 / 0.50 / 0.31 | 0.00 / 0.69 / 0.44 | 1.9× |
| LLM client or model update | 8 | 0.38 / 0.75 / 0.50 | 0.12 / 0.19 / 0.12 | 0.7× |
| developer page or docs generator | 4 | 1.00 / 1.38 / 0.62 | 0.25 / 0.12 / 0.12 | 1.7× |
| tests, CI and dev tooling | 5 | 1.40 / 1.20 / 0.80 | 0.60 / 1.10 / 0.70 | 8.1× |

- **Program bug fixes** split sharply between the first six and the new ten (§6).
- **LLM client or model update.** Plain's figures here are carried by langchain-model-update. Without it the other 7
  jobs give GC+ 0.43, P 0.43, P+R 0.14. GC+'s 0.38 comes from langchain-gemini-openai and langchain-provider-todos.
- **Tests, CI and tooling** includes GC+'s two whole-release jobs, case 6 and gc-next-revision. Their GC+ time covers
  the whole multi-item job.

## 9. Time

**What is measured.**
- **GC+ time** is Claude's working time in the GC+ session, estimated from transcripts.
- **Plain time** is the run's clock time.
- **Left out of GC+'s time:** the outside review readings (whose catches count for GC+), publication, and the
  Developer's own time and waits. So GC+'s real cost is higher than shown.

The ratios are rough estimates, not a measured difference in cost.

| group | GC+ ÷ P, median | GC+ ÷ (P+R), median | GC+ ÷ P, ratio of total minutes | GC+ ÷ (P+R), ratio of total minutes |
|---|---|---|---|---|
| hard | 5.5× | 3.5× | 4.8× | 2.8× |
| medium | 2.3× | 1.3× | 3.3× | 2.1× |
| easy | 1.6× | 0.8× | 1.3× | 0.9× |
| all 37 | 2.0× | 1.3× | 2.6× | 1.7× |

- **Load.** Round-4 plain runs ran 6–7 at a time on a loaded machine (median P 19.7 minutes, against 13.0 in the
  first ten). Their times are inflated, which makes GC+ look cheaper than it is.
- **Estimates.** Queue jobs shared GC+ sessions, so their GC+ times are apportioned estimates (bounds in
  `GC_CLAUDE_TIME_R4.md`). Leaving out the two whole-release jobs, the all-37 medians are about 1.8× and 1.15×
  (review 2).
- **gc-rev15-macos-ci.** Both plain runs hit the 90-minute limit under load and were rerun alone, and the reruns are
  counted. The time study uses the loaded runs, so their times are a floor. process-raw-data-reconstructed-f uses p1
  only.

## 10. Limits and caveats

- **The groups come from GC+'s own process.**
  - Hard, medium and easy are defined by what GC+'s layers caught. The count does not depend on the plain runs, but the
    cut-offs were chosen after the results were seen (§3), and a developer does not know the count before starting a
    job.
  - Seven of the nine hard jobs are original cases, which were chosen partly because GC+'s layers had caught defects
    in them.
  - A usable rule ("use GC+ for hard jobs") would need signs of difficulty visible at the start. This study does not
    supply them.
- **Small groups, small counts.** The groups hold nine, nine and nineteen jobs.
  - **Few major errors:** the major-only figures rest on 6 GC+, 25 P and 18 P+R errors in all (5 for GC+ with S179
    minor).
  - **One case moves a group:** case 6 for GC+ in the hard group, and langchain-model-update for plain (§3).
- **Severity tagging.**
  - **Input:** both taggings worked from short descriptions. The second tagger read the source code for one item
    only (S058).
  - **Six descriptions were not fully blind.** In the second tagging's input, S055, S070, S077, S092 and S149 still
    named GC+'s or plain's version, and S047 carried an earlier reader's "major" call (found by the packet checker).
    The six were tagged again by a fresh tagger from neutral wording (`r4_severity/ITEMS_BLIND_RECHECK6.tsv`,
    `SEVERITY_RECHECK6.tsv`). Three went from minor to major (S070, S092, S149). Two of those are pre-existing faults
    and one is a test gap that no arm leaves as a confirmed missed row, so no headline or major-only figure changes.
    Only the major line of "everything left, including pre-existing faults" moves: all 37 from 0.51 / 0.75 / 0.56
    to 0.54 / 0.80 / 0.57 (`r4_severity/RECHECK6_EFFECT.txt`). The second tagging's tags are kept, so that one
    tagger's calls are used throughout.
  - **What the tagger did not know:** it did not know the bug reports of the original cases, so "is this the reported
    problem?" was a judgement each time.
  - **Agreement:** 87% (κ 0.64). Of the 27 disagreements, 16 went from minor to major in the second tagging, 9
    from major to minor, and 2 from minor to not an error.
  - **Under the first tagging** (partly unblinded), the major-only figures are: hard GC+ 0.22 / P 0.92 / P+R 0.69;
    medium 0.11 / 0.28 / 0.28; easy 0.05 / 0.05 / 0.00; all 37 0.11 / 0.32 / 0.24. GC+'s hard-group figure doubles
    under the second tagging because it tagged two case-6 errors major: the merge parent (S123) and the `--fetch`
    remote (S179).
  - **Close calls.** S179, and S078 (the same unvalidated remote in gc-next-revision), let a value in the publication
    record run a command through `git fetch --upload-pack`. The blind tagger called this a real security problem. An
    earlier ledger ruling called it minor, because that record is written by GC+'s own tooling, not by an outsider. The
    blind tag is kept, since overriding a blind call with knowledge of the arm would undo the blinding. With S179 and
    S078 minor, GC+'s major figure is 0.33 in the hard group and 0.14 over all 37, and the plain figures do not change
    (`r4_severity/MAJOR_S179_S078_MINOR.txt`). Similarly, the tagger called an unchecked merge-commit second parent
    major in case 6 (S123) but a related merge-commit case in gc-next-revision minor (S039), because S039 needs a
    hand-written record.
- **The carry-over rule.** Without it, P+R would be: all errors hard 1.25, easy 0.21, all 37 0.51; major hard 0.92,
  medium 0.17.
- **Measurement still undercounts.** One blind reading finds about half the errors. Round 4b added a second reading
  and probes, but some errors are surely still unfound, for both arms.
- **combine-focused-maps-empty-region.**
  - GC+'s design stops with a clear Sorry when a focused region is empty; the task asked for a composite map. A clear
    error is not the same as finishing the calculation.
  - The blind probe was revised to accept either outcome after the Guide had seen GC+'s design, so this probe was not
    fully blind.
  - The difference is a scope item for every arm and moves no rate by more than about 0.04.
- **langchain-test-health.**
  - **GC+'s version** leaves the AUTO-STOP suppression bug (`should_stop` stays set). It is a pre-existing fault, also
    left by plain p2, so it is reported apart for both arms and is not in the headline.
  - **Plain p2's** package runner still reports a failing test file as PASSED. That is the reported problem itself,
    so it is a task error and counts; its first form repeats GC+'s own caught draft error D1.
  - This corrects DISPUTED item 6 in packet-17, which said GC+'s bug was "counted as a major remaining error".
- **The disclosure rule rewards writing a problem down.** In dock-in-map-gui-output-dir, GC+ left the command-line
  redirect in full and disclosed it, so it counts as deferred. Plain p2 narrowed the same redirect but left part of
  it, which counts as an error. The effect is small (about 0.02).
- **Probe calls dropped as artefacts:**
  - phenix-chat-tools D2: the fake 400 error is built differently from the real OpenAI SDK's;
  - langchain-model-update E4, a probe of GC+'s code;
  - o07 E3, which failed to run.

  The "E4 folded in" notes on S134 and S151 in the appendix are the same probe's result on the plain arms: it shares
  its cause with those rows, so it was merged into them rather than counted twice (RULINGS.md).
- **Unreproducible failure.** gc-rev15-macos-ci's real CI failure could not be reproduced on this Mac, and its probe
  layout is a guess. Neither arm's fix is verified there.
- **Model-table basis.** Some LLM rows rest on the model table, not a live call, and are marked probable.
- **Declared mild leaks:**
  - the gc-next-revision interface;
  - the dock-in-map file names;
  - the langchain-gemini-openai model goal;
  - the phenix-chat-tools live probe log.

  If anything they favour plain.
- **Inputs of the original cases.** Checked: no fix, cause or location from the Developer was withheld from plain;
  in cases 6 and 10 Developer-provided data reached plain only as text (slight in case 10). GC+ had a slight
  advantage from its own earlier output in case 5, and from the Developer's mid-job decisions in cases 4, 5,
  8 and 10 (§6).
- **Independence.** Every worker, scorer, reader, tagger and checker in this study is a Claude model. One of the two
  reviews came from a different model family.
- **Bounded result.** These 37 jobs are one Developer's bug-fix work over about four weeks in phenix, cctbx and
  phenix_regression. Wider work may differ.

## 11. Corrections from the two reviews of draft 1

| correction asked | where handled |
|---|---|
| Show "everything left, incl. deferred" and the confirmed + probable line (both reviews) | Summary, §3, §4 |
| Include pre-existing faults when discussing total remaining problems (review 2, DISPUTED item 2) | §4 |
| Replace the selection / job-mix explanation with the measurement point, corrected by the recall check (review 1: 1, 2, 4; review 2: B) | §4, §6 |
| Program-bug split, first ten against new, with "large in the original cases, much smaller in the new" (review 2: B) | §6 |
| Name langchain-model-update as the case that weighs most; one-case sensitivity (review 1: 4, 5; review 2: C) | §3, §4 |
| Categories described, not concluded; the LLM category without model-update (review 1: 5, 12; review 2: 12) | §8 |
| Time: Claude working time only, what is left out, total-minute ratios as well as medians, "lean low" reworded, rough estimates (review 1: 6, 10; review 2: D) | §9 |
| combine-focused-maps: a clear error is not a finished calculation, and the probe was revised after seeing GC+'s design (review 1: 7; review 2: §3, items 5 and 7) | §10 |
| auto-q2m-c's stopped runs are incomplete, with a justified request for a decision (review 2: item 1) | §2 |
| DISPUTED item 6 wording (review 1: 6, correction 7) | §10 |
| Make the evenly measured comparison the main one (review 1: correction 1) | Done more fully than asked: round 4b measured all 37 evenly, and the frame is hard / medium / easy (the Developer's decision) |
| Test GC+'s probable leftovers as hard as plain's (review 1, optional) | Done by the cross-arm probes on every arm (§1) |

**Corrections from the two reviews of draft 2** (`r4_reviews/REVIEW_DRAFT2_1_claude.md`, `REVIEW_DRAFT2_2_nonclaude.md`):

| correction asked | where handled |
|---|---|
| Easy jobs: remove "at lower cost"; Claude time is about the same (review 1: 1) | Summary |
| The cut-offs were chosen after the figures were seen, and later rulings set two jobs' counts; add a cut-off table (review 1: 2, disputed item 1) | Summary, §3, §10 |
| The hard-group gap against plain alone comes mostly from the two new hard jobs; reword the conclusion (review 1: 3) | Summary, §3 |
| Check the original cases' prompt notes for withheld hints (review 1: 4) | §6, §10 (`PROMPT_HINTS_FIRST_TEN.md`) |
| Describe the grouping as an association, not a prediction (review 2: A) | Summary, §3, §10 |
| Source-of-discovery comparison, including the hard group and "caught any" (review 2: B) | Summary, §6 |
| gc-rev15-macos-ci p1's test is a source-integrity failure, not the bug (review 2: C) | §5 |
| Explain case 6 GC+'s `tst_screen_check_v20.py` failures (review 2: C) | §5 |
| Missed-only count leads, everything-left beside it (review 1, disputed item 7) | As before (Summary, §4) |

## 12. Files

- **Ledger:** `walkthrough/LEDGER_R4.tsv` (merged, with a severity column) and `LEDGER_R4_SUMMARY.md` (all tables,
  including per case, time by group, one-case sensitivities and the checker additions). Also `r4_ledger/` (rows,
  rulings, corrections, categories), `r4_cross/<case>/` (cross-arm probes) and `r4_severity/` (both taggings,
  `AGREEMENT.txt`, and the major-only tables under the first tagging and without the carry-over rule).
- **Analyses:** `FIRST_TEN_VS_NEW.md`, `FIRST_TEN_VS_NEW_4b.txt`, `BLIND_RECALL_FIRST_TEN.md`, `AUDIT_VS_R4.md` and
  `TEST_ADEQUACY.md`.
- **Reviews of draft 1:** `r4_reviews/REVIEW_1_claude.md` and `r4_reviews/REVIEW_2_nonclaude.md`. **Of draft 2:**
  `r4_reviews/REVIEW_DRAFT2_1_claude.md` and `REVIEW_DRAFT2_2_nonclaude.md`.
- **Prompt hints of the original cases:** `PROMPT_HINTS_FIRST_TEN.md`.
- **Checker reading of this draft:** `CHECK_DRAFT2.md`, with dispositions in `CHECK_DRAFT2_DISPOSITIONS.md`.
- **Severity list:** `SEVERITY_LIST.md` (Appendix A), from `severity_appendix.py`.
- **Raw results:** `~/unix/PHENIX/replay/r4_out/` and `replay/r4b_tests/`.
- **Packet:** `packet-16/` (frozen; MANIFEST.sha256).
- **Time:** `GC_CLAUDE_TIME.md` and `GC_CLAUDE_TIME_R4.md`.

# Part C. Round 5

Reproduced from the round-5 report [Src9], with the arm labels renamed, its opening paragraph left out and headings moved down a level. The erratum [Src11] applies to two of its sentences and is given first. The time-limit check [Src12] follows the report.

## Erratum to the round-5 report (2026-10-23)

Found by the checker of the lean-GC+ case (`lean/CHECK_LEAN.md`, K1). The report itself is left as it was checked.

**The error.** Two sentences contradict the report's own direct-test table:
- "The other catches: neither extra pass reached anything that only GC+'s outside reviewer or the Developer's live
  probe had caught."
- "but none of what GC+'s outside reviewer or the Developer's live probes catch."

**What the table shows.**
- **GC+'s outside-reviewer-only catches** (10 P+R run occurrences, 3 of them major): P+R+S fixed 5 and P+2R fixed 5.
  Neither fixed any of the 3 major ones.
- **The live probe and Guide catches** (3 occurrences, 2 major): neither fixed any.

**Corrected reading.** Neither extra pass reached any **major** error that only GC+'s outside reviewer or the
Developer's live probe had caught. They did fix half of the outside reviewer's catches overall, all of them minor.

**Two more places carry the same overstatement:**
- the report's "Possible next steps" ("the ones neither extra pass reached");
- `r5_timeout/TIMEOUT_CHECK.md`, which says P+R+S would leave about 0.52 "because no P+R+S run fixed an error caught by
  GC+'s outside reviewer or its live probe". Read this as "no **major** error caught by ...". The 0.52 ceiling is about
  major errors and stands.

The same overstatement went into the handoff of 2026-10-22, and from there into the Guide's statements in chat on
2026-10-23. It has been corrected there too.

## The round-5 report

### The question

Does a structured, evidence-based review step, added after one ordinary review, leave fewer major errors in the code
than a second ordinary review? The step is GC+'s reviewer-subagent brief, acceptance criteria written first, an
evidence folder, a fix-or-say-why disposition, one re-reading, and a proving-test step.

- **The arms:**
  - **P+R+S** is the plain session after its review pass (P+R), resumed with the GC+-style step;
  - **P+2R** is the same session resumed with a second ordinary `/code-review --fix` pass (the control).
- **The setup:** both ran on the same 38 runs of the 18 jobs where GC+'s own layers caught something, with the same
  model, sandbox and 60-minute limit, in a random interleaved order.

### The answer, by the rules fixed in advance

**Against the hypothesis.** This means the pre-registered rule was not met. It does not mean P+R+S did worse than P+2R.
P+R+S left somewhat fewer major errors than P+2R on the primary measure, but by less than the margin set in advance, and
not on every measure (see below).

| confirmed major program errors left in the code per run (missed + disclosed) | GC+ | P | P+R | P+2R | P+R+S |
|---|---|---|---|---|---|
| all 18 jobs (38 runs) | 0.39 | 0.85 | 0.74 | 0.71 | 0.63 |
| count (GC+ per job, others over 38 runs) | 7 | 31 | 27 | 26 | 23 |
| without langchain-model-update | 0.35 | 0.66 | 0.54 | 0.51 | 0.43 |
| without case 6 | 0.29 | 0.78 | 0.69 | 0.69 | 0.60 |

| paired comparison (case-weighted, per run) | difference | reading (±0.10 rule) |
|---|---|---|
| P+R+S − P+2R | −0.083 (−0.088 without model-update) | no clear difference |
| P+R+S − P+R | −0.111 (−0.118) | P+R+S better |
| P+2R − P+R | −0.028 (−0.029) | no clear difference |

- **The ordered rule.** P+R+S is not better than P+2R by the rule (−0.083 is not −0.10 or lower), so rule 1 gives
  **Against**. Rule 2 (recovery) is not reached.
- **The size of the difference.** P+R+S − P+2R is a net 3 errors:
  - 4 fewer, across cases 3, 5 and 9 (2 of them in case 9, one an error P+2R introduced);
  - 1 more, in case 8.

  One error in one run moves a rate by about 0.03, and all of the gap is in the hard jobs.
- **Recovery of GC+'s lead,** for reference: (P+R − P+R+S) ÷ (P+R − GC+) = 0.32 (gap 0.35); without
  langchain-model-update 0.62 (gap 0.19).
- **Introduced and removed** (major, against the same run's P+R): P+R+S removed 5 and introduced 1; P+2R removed 2 and
  introduced 1.

### On "missed only", the order reverses

| per run | GC+ | P | P+R | P+2R | P+R+S |
|---|---|---|---|---|---|
| major missed only (the round-4 headline measure) | 0.28 | 0.65 | 0.57 | 0.42 | 0.46 |
| all errors left | 1.44 | 1.67 | 1.47 | 1.33 | 1.28 |
| all errors missed | 0.94 | 1.42 | 1.15 | 0.86 | 0.97 |
| share of runs with any major left | 0.33 | 0.51 | 0.46 | 0.40 | 0.40 |

- **P+2R leaves fewer *undisclosed* errors than P+R+S:** 0.42 against 0.46 on major errors, and 0.86 against 0.97 on all
  errors.
- **Where P+R+S's edge comes from.** P+R+S's advantage on the primary measure comes from P+2R having more *disclosed* major
  errors left: left minus missed is P+2R 0.29, P+R+S 0.17.
- **The likely cause is the time limit.** Disclosure is judged from the final message only (decision 13). Most P+R+S runs
  were cut off at 60 minutes, and 28 of the 76 blind final-message files are empty, nearly all of them P+R+S. So a
  cut-off P+R+S run could disclose only through the carry-over from P and P+R.
- **What this means for the measures.** On missed-only, P+R+S is penalized for not finishing. On the primary measure,
  disclosed and missed count alike, so there it is not.

### The direct test: GC+'s caught errors that plain + review left

| caught in GC+'s drafts by | arm | P+R run occurrences | fixed | of which major | major fixed |
|---|---|---|---|---|---|
| GC+'s internal reviewer (one also caught by the outside reviewer) | P+R+S | 22 | 13 | 8 | 4 |
| | P+2R | 22 | 10 | 8 | 2 |
| GC+'s outside reviewer only | P+R+S | 10 | 5 | 3 | 0 |
| | P+2R | 10 | 5 | 3 | 0 |
| other (the Developer's live probe; the Guide) | P+R+S | 3 | 0 | 2 | 0 |
| | P+2R | 3 | 0 | 2 | 0 |

- **The internal reviewer's catches:** the GC+-style step recovered somewhat more of these than a second review did
  (13 against 10; 4 against 2 major).
- **The other catches:** neither extra pass reached anything that only GC+'s outside reviewer or the Developer's live
  probe had caught.

### Time and cost

- **Time.**
  - **P+R+S:** a median of 60 minutes (2,189 minutes in all). It hit the 60-minute limit in 28 of 38 runs, and 29 runs
    used 59 minutes or more.
  - **P+2R:** a median of 14 minutes (723 in all), with one limit hit.
- **Cost.**
  - **P+R+S:** the 10 runs that finished averaged about $25 each. Cost was recorded for only 12 runs in all, including two
    cut off at the limit, so P+R+S's total ($266 recorded) is understated.
  - **P+2R:** recorded for 37 runs, about $12 each ($429).
- **Compliance.** Every P+R+S run started a reviewer subagent and wrote acceptance criteria. Every P+2R run used the
  code-review skill.

### What this means

- **Within this design, a GC+-style review step is not clearly better than running the review again.**
  - **Primary measure:** it left fewer major errors (0.63 against 0.71), but below the margin set in advance.
  - **Missed-only measures:** it did not do better there.
  - **Cost:** it took about three times the time (2,189 against 723 minutes).
- **A second ordinary review is not clearly better than one** either (P+2R − P+R −0.03, no clear difference).
- **It does reach some of what GC+'s internal reviewer catches** (13 of 22 occurrences, against 10 for a second review),
  but none of what GC+'s outside reviewer or the Developer's live probes catch.
- **GC+ itself leaves fewest major errors** (0.39 against 0.63 and 0.71). Part of that gap comes from where round 5
  searched (see "The deeper baselines").

### The main caveat: the time limit

- **What happened.** P+R+S ran into the 60-minute limit in 28 of 38 runs, so most P+R+S sessions were cut off before
  finishing their reading, fixes and re-reading, and often before writing a final message.
- **What the result measures.** It is "the GC+-style step within an hour". It may understate what the step does when
  it can finish, and it penalizes P+R+S on the missed-only measures.
- **This could have been foreseen.** The pilot showed 2 of 3 P+R+S runs at or near the limit, and plan §5 allowed
  changing the limit after the pilot. The limit was kept for symmetry with P+2R, and no decision about it was recorded
  at the time. That was an oversight.

### The deeper baselines

- **Where the new rows came from.** The round-5 search found 127 new errors in GC+, P and P+R (plan §7.8). They raised
  P+R from round 4's 0.65 to 0.74 on the primary measure; GC+ stayed at 0.39.
- **The overlap with the main result.** Three of the added P+R major occurrences are errors a round-5 arm then fixed
  (case 9 N1 by P+R+S; case 8 N1 and N3 by P+R+S or P+2R). That is the same size as the P+R+S − P+2R difference.
- **Against round 4's baseline,** P+R+S (0.63) is barely below P+R's 0.65, and P+2R (0.71) is above it.
- **GC+'s lead grew** from 0.26 to 0.35 (from 0.10 to 0.19 without langchain-model-update), partly because the search
  was seeded from findings on the plain lineage. This affects "GC+ stays ahead" and both recovery figures.

### Other limits

- **Small numbers.** The primary difference is a net 3 errors, so one case can move it.
- **Rows were checked.** A checker re-examined 37 sampled verdicts under labels, and 36 agree (`r5_plan/CHECK_ROWS.md`).
  - **One consistency fix followed:** in case 8, known errors keep the ledger's origin (decision 14). It changed the
    P+R comparisons but not P+R+S − P+2R.
  - **One borderline disclosure** (langchain-model-update "providers") was left as "deferred"; the carry-over gives
    the same result.
- **Blinding was partial.** Workers ruled under the labels L1 and L2, but P+R+S leaves notes and lists findings, and an
  empty final message points to P+R+S, so a worker could infer the label.
- **Severity.**
  - **The 32 new errors** were tagged blind once. On 20 anchor items the tagger agreed with the earlier tagging 80% of
    the time (`r5_severity/ANCHOR_AGREEMENT.txt`).
  - **Case 10's "stale" error** has no severity tag and counts as not major. That slightly favours P+R+S without
    changing the reading.
- **Run conditions.**
  - **Redone attempts:** 8 invalid attempts, on 7 distinct runs, were redone under the sleep rule. They came from one
    clock jump of about 81 s, one real sleep on a dying battery, and one later sleep with the network down.
  - **Load:** concurrency was lowered for some hours at the Developer's request.
  - Both fall on both arms through the random interleaved order.
- **The affected-run rule was narrowed before any run** to data and `work/` inputs, which gave 0 affected runs. 18 runs
  lost their check logs; these are re-created by rerunning the checks (decision 1).
- **Three pilot runs** lost their original temporary folders to a script bug before any run. Both of their arms
  started from the same empty folder (decision 3).
- **Pinned sources and today's build.** Older sources were pinned with today's compiled build, so compiled parts
  (probe, reduce) may not match their pinned sources (decision 5).
- **The kit deny** made GC+'s kit look deleted to `git` inside the sandbox, so sessions saw spurious deletions in
  `git diff`, in both arms alike. No kit content reached any session outside the cases where the kit is the code under
  change (`r5_out/LEAK_REVIEW_R5.md`, decision 9).
- **Same model throughout,** with no different-model reader.

### Possible next steps (not done; for the Developer)

- **A longer limit.** Rerun P+R+S, and P+2R for symmetry, with a longer limit (for example 120 minutes), as a separately
  labelled exploratory round. It would show what the step does when it can finish, and remove the disclosure artefact.
- **GC+'s other contributors.** Test the ones neither extra pass reached: a different-model outside reading, and live
  probes for API or model changes.

## The time-limit check: where the round-5 P+R+S runs stood when they ended (2026-10-22)

Exploratory and done after the results were known. Not part of the frozen round-5 analysis. It reads only the
existing stream files and evidence folders in `replay/r5_out/`, using `timeout_phase.py`, which writes
`PHASE_PRS.tsv` and the last top-level calls of each run to `PHASE_PRS_LAST_CALLS.txt`. No runs were started, and no
diffs or scores were consulted.

### The counts

Of the 38 P+R+S runs, 26 were cut off with no final message. Two more ran to 60.2 minutes but still returned a
result (aniso-p2, sfm-p2), which gives the report's 28 runs that hit the limit. Twelve runs finished.

| Phase when cut off | Runs | What the limit cost |
|---|---|---|
| B: the first reviewer was still running | 2 (precheck-p2, phenix-chat-tools-p1) | The review had no effect at all |
| C: the first review was back, but nothing was done with it | 2 (gc-next-revision-p1 back at 58.6 min, ebadf-p1 at 58.7) | The findings were never addressed |
| C: the first review was back and the session was still acting on it | 7 (gemini-openai p1/p2, provider-todos-p1, test-health-p2, case1-p1, cutoff-p2, ebadf-p2) | The fixes were incomplete. Most of these runs were editing code or rerunning tests at the cut-off, and ebadf-p2 still had a blocking finding open |
| D: the findings were addressed, and the second reading was still running | 10 | The recheck and the final message were lost. In win32-p1 and mmm_followups-p2 the first review had a blocking finding |
| E: the second reading was back, and the session was finishing | 5 | Mostly the final message (and so the disclosures) was lost |

### Time

The first reviewer started at a median of 13.8 minutes (range 7 to 54). The first review took a median of 18.1
minutes (range 12 to 33). The time before the reviewer started went mostly to writing criteria, gathering evidence and
waiting for long test suites. With a full second reading, the P+R+S procedure as written needs roughly 55 to 70
minutes, so a 60-minute limit cut it short by design.

### What this means

- **For P+R+S against P+2R:** the limit mattered. In 11 runs (B plus C), the review was not acted on, or not fully. In
  15 more (D plus E), the final message was lost, and disclosure is judged from that message. Only 1 of 38 P+2R runs
  hit the limit.
- **For P+R+S against GC+:** the ceiling argument still holds. Even if every remaining internal-reviewer catch were
  fixed, P+R+S would leave about 0.52 major errors per run against GC+'s 0.39, because no P+R+S run fixed an error caught
  by GC+'s outside reviewer or its live probe.

### Options

(a) **Continuation.** Resume each of the 26 cut-off P+R+S sessions, with up to 60 more minutes and a fixed "continue
and finish" prompt, restoring each installation to its state at the cut-off. This gives the same runs with the
limit raised to 120 minutes, without rerolling the first hour. P+2R is not rerun, since it was not limited. The session
files exist; for example, cutoff-p1's is in `~/.claude/projects/...-cutoff-p1/`. The restore would need the cut-off
diff, the `work/` folder and the tmp folder, and that must be checked before planning.

(b) **A fresh rerun of both arms with a 120-minute limit** (P+R+S and P+2R with a 120-minute limit) on all 38 runs. This is the cleanest
design, but it needs more than 10 hours of machine time and adds a new draw of run-to-run variation.

# Part D. Triage: can a job be routed to the thorough procedure in advance?

After round 5, the question was whether GC+ (or a thorough route) could be kept for the jobs that need it, and plain
+ review used for the rest. Two checks were made [Src15; Src16].

- **Power check** [Src15]. A permutation test over the round-4 results asked whether even routing chosen with
  hindsight beats random routing of the same number of jobs.

  | router (jobs sent to GC+) | major missed, all 37 | p | without langchain-model-update | p |
  |---|---|---|---|---|
  | draft-3 "hard" group (9) | 0.149 | 0.10 | 0.153 | 0.41 |
  | draft-3 "caught any" group (18) | 0.135 | 0.14 | 0.139 | 0.29 |
  | all GC+ (37) | 0.162 | n/a | 0.167 | n/a |
  | all P+R (0) | 0.236 | n/a | 0.160 | n/a |

  On all program errors, the hard-group router gives p = 0.46 (0.76 without langchain-model-update). **Reading:**
  even hindsight routing cannot be told apart from chance on these 37 jobs, so a routing rule cannot be tested on
  these data.
- **Descriptive check of two triage points** [Src16]. Not a blind test: the briefs drew on the study's lessons, and the
  outcomes were known when they were written.
  - **A broad start screen** (THOROUGH if any of five risk criteria) sent 64 of 74 calls to the thorough route. In
    this project almost every job meets some broad risk criterion.
  - **A narrow start screen** (thorough only for a live service, another platform, publication, or data or
    credentials) sent 12 of 37 jobs, with every pair of calls agreeing. As a policy it gave 0.155 major errors missed
    per run, against all-GC+ 0.162 and all-P+R 0.236; its whole gain over all-P+R came from one job,
    langchain-model-update (without it, 0.160 against 0.160), and random routing does as well with p = 0.17.
  - **An escalation check after plain + review** escalated all 76 runs, including the 63 whose P+R left no confirmed
    major error, mostly, as the model read the reports, because the review pass left findings open. So a plain +
    review result often still needs someone to decide its open findings. The check was not run on GC+'s results, so
    this is not shown to be specific to plain + review.
- **What this led to.** GC's start triggers are modelled on the narrow screen's concrete reasons, with publication
  narrowed to installing for others (a live service, another platform, installing for others, data or credentials),
  plus an open correctness question after the review [Src16; Src17; Src33]. They add checks
  where a concrete reason exists; they are not a measured routing rule.

# Part E. From GuidedCoding Plus to GuidedCoding

**The Developer's aim**, quoted in the proposal: "making the process easy for the developer and reliable overall"
[Src17].

**The proposal and its reading.** The case for a shorter procedure [Src17] set each element against its evidence,
including the evidence against (finding 5). Two outside reviewers read it with the study's reports. Both recommended
adopting it as a trial; one recommended stopping the replay study, and the other a small retrospective check
first [Src18; Src19]. The Developer stopped the study and started the
trial on 2026-10-23, then, after three real jobs under drafts of it, asked for the procedure to be finalized and the
earlier kit retired; the earlier kit was kept on the branch `full-kit-rev21` [Src29; Src28]. Three outside reviews
of the retirement plan all said to proceed with changes; one advised waiting for the trial's evidence (10 to 15
jobs, first later-defect checks 2026-11-20) before retiring the kit and publishing [Src35; Src36; Src37]. The
Developer chose to go ahead that day, noting that the new repository could be changed without affecting anyone
[Src28]. GuidedCoding revision 22 was published that day after three outside reviews of the release [Src24].

**What GC keeps, drops and adds.**
- **Keeps:** the proving test; one review pass with the code-review skill (the step the study measured); outside
  readings and live checks, now as steps for named triggers; the Developer's decisions on scope, pushes and
  installations.
- **Drops:** the Guide-and-worker structure, the approval screens, the evidence packets and the kit code that checked
  them, and the unattended auto mode. GC is instructions only; no tool enforces them.
- **Adds:** a scope rule for review fixes (each fix the review makes is checked, and a fix that changes behaviour
  beyond the task is reverted and raised); an outside review on request on any job; a supervised batch mode; and the
  rule for consequential work (a plan, a checked recovery step and a completed outside review before an
  irreversible step) [Src33; Src34].

**What the evidence says about each main part of GC** (as published in GC's `EVIDENCE.md` [Src20], checked against
this report):

| part of GC | evidence |
|---|---|
| one review pass with the code-review skill, on every job where the skill is available | **Measured:** P to P+R, 0.81 to 0.47 program errors missed, 0.33 to 0.24 major [Src4 §4]. The main support for GC. |
| the review fallback (Claude reviews the change itself) | Not measured. |
| a proving test that fails on the old code and passes on the new | GC+ also called for this kind of test where there was one; the study did not measure its separate contribution [Src4 §5]. |
| checking each review fix, and reverting fixes that change behaviour beyond the task | Not measured. Prompted by the study: a review pass brought back a major error GC+ had caught (case 3, run 1), and two review passes changed behaviour the task did not ask for (langchain-cap-fix, runs 1 and 2) [Src3]. One behaviour check shows it working [Src21]. In round 6, GC reverted 63 review fixes under this rule and left them reverted; 6 of them fixed counted major errors, and each of those was put to the developer as a question instead [Src41]. |
| added steps for triggers (live calls, other-platform commands, outside review) | Measured only in round 6 and only for the outside review: written in 4 of 38 runs, 3 major errors removed [Src39]; live calls cannot be tested in a replay. GC+'s outside reviewers and live checks made major catches that no review pass recovered [Src11]. |
| an outside review on request, on any job | One behaviour check [Src22]. In round 6 none was requested; GC wrote one on its own trigger in 4 of 38 runs, which removed 3 major errors and added none [Src39]. |
| the optional independent reviewer (`REVIEWER.md`) | Measured as P+R+S: fewer major errors than P+R (0.63 against 0.74), not clearly fewer than P+2R (0.71), about three times as long; most runs hit the time limit [Src9; Src10; Src13]. The step in `REVIEWER.md` is built from it, with at most one re-reading and no time limit. |
| consequential work | Not measured; the study did not cover damage to installations. A precaution set by the Developer. |
| `/gc batch` | Not measured as a procedure; behaviour checks show patch handling and checkout restoration in specific test cases [Src20; Src21]. |

**Behaviour checks of GC.** Before and after release, GC was run in Claude Code (`claude -p`) against scratch
repositories, and the output, Git state, diffs and file hashes were kept [Src20; Src21; Src22]. They cover the
introduction, setup, retired commands, a bounded fix with a proving test and the review, an installation task held
for a plan and outside review, batches (including a new file and a file already modified), and an outside review on
request. Several rules were tightened because of what these runs showed [Src20]. Behaviour checks show what happened
in particular examples; they do not establish reliability across jobs.

**The real-use trial.** Each job is logged, with a check for later defects about four weeks after the job. On
2026-10-23 three jobs were logged, run under earlier drafts of the procedure (`/lean`), and the Developer judged that
it worked well [Src23; Src29; Src20, "Use since"]. No real job under GC version 1.3 itself has been checked yet (round 6 was a replay, Part F).

# Part F. Round 6: GuidedCoding replayed

A summary of the round-6 report [Src39], which was checked against its sources and read by three outside readers
(one of them a Claude model; the others did not state their model; all accepted it, two with changes, which were
taken in) [Src44]. The plan
and its reading rule were fixed before any result was read; every decision made while running is listed in the plan,
§10, A to N [Src43].

**What was done.** 38 fresh runs of GC (`/gc` version 1.3) on the 18 jobs where GC+'s layers had caught something, 2
per job (4 for case 1), with the same Claude Code binaries, pins, model and sandbox as the plain runs, and a fixed
paragraph standing in for the Developer ("keep to the task; never approve scope, interface or default changes"). Four
runs wrote an outside review; a fixed script sent each to a different model (gpt-6.1-sol) and the session was
continued with the reply (GC+O). The same outside-review search was run on every P+R change. Every earlier probe was
run on GC, a blind reading set GC's diff beside the other arms', and every new candidate error was probed or read on
every arm; new errors found in the old arms were added to them. Severity was tagged blind [Src39, "What was done"].

**Result** (confirmed major program errors left in the code, missed plus disclosed, per run; updated figures) [Src40]:

| | GC+ | P | P+R | GC | GC+O |
|---|---|---|---|---|---|
| all 18 jobs | 0.444 | 0.903 | 0.792 | 0.972 | 0.903 |
| without langchain-model-update | 0.412 | 0.721 | 0.603 | 0.794 | 0.721 |
| without case 6 | 0.294 | 0.779 | 0.691 | 0.941 | 0.926 |
| major missed only (all jobs) | 0.333 | 0.708 | 0.625 | 0.653 | 0.597 |

- **Q1:** GC+O − P+R = +0.111 (90% bootstrap interval over jobs −0.194 to +0.417); +0.118 and +0.235 on the two
  robustness lines. By the rule fixed in advance: **no clear difference**. The estimate leans against GC+O, and the
  interval is wide; the result does not show that the arms are equal. Two runs of the same arm differ by up to 0.14
  on average, and by 0.22 to 0.47 per job [Src40; Src39].
- **Q2:** in these runs GC+O recovered none of GC+'s measured lead (recovery −0.32; −0.62 without
  langchain-model-update) [Src40].
- **The outside review**, written in 4 of 38 runs, removed 3 major errors (two in case 6, one in case 1) and added
  none [Src39, "What GC+O changed over GC"].
- **Questions to the developer.** GC put many remaining problems to the developer as numbered decisions, sometimes
  after finding a fix or reverting one under its scope rule; the stand-in answered all of them "keep to the task", so
  the primary measure counts them as left. Of GC+O's 33 major errors left, 11 were asked and 7 asked in part; P+R
  asked about 1 of its 29. Untested counterfactuals: on GC's own recommendations, GC+O 0.736 against P+R 0.792; if
  every fully asked question were answered "fix it" and each fix worked, 0.597 against 0.764 (0.403 if the partial
  questions are included) [Src41].
- **Time and cost.** Median 23.6 minutes per run; $281 over 38 runs; no time limit reached [Src40].

**What it leads to.** Fixed in advance: with "better" or "no clear difference", keep GC as it is and say so on the
Evidence page [Src43 §2]. GC is kept as a way of working with the developer, not as a claim that it produces more
correct code than plain Claude Code with a review [Src44, proposed Evidence wording].

**What went wrong while running it** [Src39; Src43 §10]: the first full set of runs was discarded because the sandbox
refused every shell command (decision G); six runs were rerun because their bug-report file was missing (H); the four
GC+O steps were re-validated after a clock artefact (I); two P+R outside-review search requests named a bug report
whose file name is a user's surname (F). Scoring decisions J to M are listed with their effect; none changed Q1. The protocol document gives
every deviation [Src42].

# Part G. Round 6b: what an outside review adds, and GuidedCoding 1.4

A summary of the step-O report, draft 3 [Src45], checked internally (8 findings, all taken) [Src50] and read by one
outside reader, who recomputed the main figures from the ledger, found no error and accepted it with small changes
[Src51]. The plan and its reading rules were fixed before any run; decisions made while running are in its §10 [Src46].

**Why.** After round 6, the Developer's aim was that the final GC should keep the parts shown to do something and
leave out, or make optional, the parts not shown [Src46 §1]. One part was unresolved: an outside review by a
different model. GC+'s outside readers had caught major errors that no review pass caught, and in round 6 it removed
3 major errors in the only 4 runs that had one (Part F). The Developer chose to measure this first (step O) and to
decide afterwards whether to test answering GC's questions to the developer (step D) [Src46].

**What was run** [Src45 §1; Src49].
- **P+R+O:** each of the 38 counted P+R sessions, resumed once with the outside review of its final change (the
  replies of round 6's P+R search, reused as received; one packet resent with a key-shaped test placeholder masked).
- **GC+O\*:** each of the 38 counted round-6 GC sessions, resumed from before any round-6 outside review, with a new
  review built by the same recipe: the task text and the final diff, sent by script to gpt-6.1-sol (one turn, no
  tools).
- One fixed message for both arms (handle each finding as your instructions say, then report; nothing irreversible is
  approved). GC's scope rule and round 6's stand-in Developer still applied. After a 12-run pilot, all 76 runs were
  valid. Median 8.0 minutes per P+R+O run and 6.7 per GC+O\* run; $431 and $430 (notional), plus 39 API calls.

**How it was scored** [Src45 §2]. As round 6, with the tools frozen by hash before any O diff was read: probes on both
versions of every run; a blind second reading; one row worker per job ruling both versions under random labels; a
checker (36 sampled rulings, all agreeing; 14 corrections, all to origin); blind severity tagging among anchors. The
reading rule [Src46 §2]: "adds something" needs a difference of −0.10 or lower, a 90% interval over jobs wholly below
0, −0.10 or lower without langchain-model-update and without case 6, and 0 or lower on the seeded line (errors first
found by an outside review dropped).

**Results** (confirmed major program errors left in the code, missed plus disclosed, per run) [Src45 §3; Src47]:

| set | P+R | P+R+O | GC | GC+O\* |
|---|---|---|---|---|
| all 18 jobs | 0.847 | 0.764 | 1.000 | 0.833 |
| without langchain-model-update | 0.662 | 0.574 | 0.824 | 0.676 |
| without case 6 | 0.750 | 0.721 | 0.971 | 0.853 |

The earlier arms' figures are a little higher than in Part F (P+R 0.792, GC 0.972) because step O's instruments found
errors that the earlier versions also have; Part F's figures are not revised.

| line | O-P (P+R+O − P+R) | O-GC (GC+O\* − GC) |
|---|---|---|
| difference (90% interval over jobs) | −0.083 (−0.222 to +0.028) | **−0.167 (−0.306 to −0.056)** |
| without langchain-model-update | −0.088 | −0.147 |
| without case 6 | −0.029 | −0.118 |
| seeded line | −0.028 | −0.111 |
| reading | no clear difference | **adds something** |
| if typed-name were major | −0.056, no clear difference | −0.125 (−0.278 to +0.028; without case 6 −0.074): no clear difference |

- O-P was close to its ceiling, computed before any run: the P+R replies named only 4 of P+R's 29 counted major
  errors, so on named errors O-P could reach at most −0.111, and −0.059 without case 6 [Src48].
- **Level:** GC+O\* − P+R+O = +0.069 (−0.167 to +0.319). After the outside review, GC is still not better than plain
  + one review + the same outside review, leaning slightly against GC, as in round 6.

**Where the change came from** [Src45 §4]. In GC+O\*, 9 run-level removals of a major error and 3 additions, a net of
6 removals, all of the net in four jobs (case 1 had 2 of each and netted zero): case 3 (a library fix with an open edge case), case 6 (a safety check on git pushes), case 9 (a
process-handling fix) and langchain-model-update (a model-default update). 13 jobs did not change.
In P+R+O, 4 removals and 1 addition. **Harm:** the O step brought in 7 errors in GC+O\* (3 major, 0.056 major per run)
and 3 in P+R+O (1 major, 0.028). Five of the minor ones are case 1's "typed-name": the reviews asked for a narrower
GUI fix, and the narrower fixes dropped the earlier versions' handling of output names the user types.

**How fragile it is** [Src45, "The answer in brief"; Src50]. The without-case-6 condition is −2.0 case-units over 17
jobs against a threshold of −1.7: losing any single run-level removal in a two-run job gives −0.088 and "no clear
difference". Several single items decide it: the severity of typed-name (minor by a supplementary blind tag, 8 of 10
anchors agreeing; major gives the table's last line); the major tag of case 3 O1, a new error (tagged minor, O-GC
would be −0.139, and −0.088 without case 6); and any one of the removals of case 3 D1, case 9 N1 or either
langchain-model-update E2.

**Decisions made after rows existed, in time order** [Src46 §10; Src45 §2; Src50]. O-10 and O-12 were made while the labels
were masked; O-11 after the first summary had been read.
- **O-10**, after 6 of the 18 jobs' rows existed and before the first summary run: known errors keep round 6's kind
  and origin. Without it, O-GC is −0.222.
- **O-12**, given to the row workers after the langchain-model-update job and applied through the checker's
  corrections: a version that lacks its partner's fix of a fault in the base code counts the fault as brought in by
  its own change. Without it, O-GC is about −0.208.
- **O-11**, after the first summary run had been read (O-GC −0.167, "adds something", with typed-name untagged and so
  not counted as major): typed-name was sent to a supplementary blind tag, decided before the tag was known and used
  as given (minor). The result is the same untagged and tagged; a major tag would have made it "no clear difference".

O-10 and O-12 both made O-GC smaller, not larger.

**The outside reading** [Src51]. The points taken: the rule's decision (a core GC step) is separate from how broadly to
require the review, since the evidence supports its benefit only on the difficult jobs studied, mostly four of them;
the practical limits (a scripted packet, not GC's own `OUTSIDE_REVIEW.md`; the developer's time not measured) are made
prominent; the actual instructions should be tried on a few jobs before GC is changed; and round 6b does not show which
other GC parts are unnecessary. The reader recommended the review as standard for high-risk or difficult changes and
optional for routine bounded fixes, and would not repeat a study this large.

**What it led to.** By the rule fixed in advance, O-GC "adds something" makes the outside review a core GC step, at
least for the kinds of job where it helped; O-P not adding means step D is not pointed to [Src46 §2; Src45]. On
2026-10-26 the Developer decided: "Make the outside review a standard GC step for difficult or consequential changes
(with broader triggers than now) and an easy option for routine fixes; first try the real instructions on a few
jobs." Narrowing the scope rule without a further test, and running no more large experiments, was the Guide's
recommendation, and the Developer agreed: after the Guide's analysis the Developer asked "do we need the trial that is running now?" and, after the Guide's plan (finish the trigger check, skip the send step, fold the narrowed scope rule into 1.4, then one small trial of the full 1.4), replied "that sounds good" [Src55].

**GuidedCoding 1.4 (2026-10-26)** [Src53]:
- a sixth trigger, **H, hard change**: correctness turns on conditions the tests may not reach (checks, guards and
  error detection; processes, timeouts, cleanup and partial failure; defaults or compatibility across versions,
  models, providers or platforms; shared code with several callers). A routine bounded fix is not H; when unsure, H
  applies;
- an outside review for H, as for R, D, Q and consequential work; on any other job the report offers it in one line;
- a **narrower scope rule**: fix real defects in the code the job changes and the paths it calls without asking; ask
  only before changing public interfaces, defaults, file formats, behaviour callers rely on, or the project scope (in
  1.3, every review fix that changed behaviour beyond the task was reverted and raised);
- **finish before you report**: wait for or stop long runs, leave nothing running, end on the final report.

**The trial of the 1.4 draft** [Src52], an implementation check, not an experiment. Trial 1 (4 fresh runs, the H
wording only): H fired in case 3, case 9 and langchain-model-update, three of the four jobs where step O helped, and
not in a routine job. One session ended before writing its review file while a background run was going, and
another left a wait loop running; this led to "finish before you report". Trial 2
(3 fresh runs of the full draft on the three H jobs): each wrote its review file and ended on its report, and the
narrowed rule kept real fixes; after the Developer sent the reviews, every finding (1, 3 and 2) was handled, each fix
with a test. One case was noted: langchain-model-update's fix still sends `temperature` to other Claude 5.x models
named explicitly (step O's O1 there), presented as a design choice. These runs, 4 runs of an earlier draft (trigger check) and 3 runs of the full 1.4 text, with their resumes after the outside review, show the
instructions working as intended on known jobs; they do not measure whether 1.4 leaves fewer errors.

# Part H. Limits of the whole study

The detailed limits are in Part B §10, in Part C ("The main caveat", "Other limits") and in the round-6 report's
"Limits" [Src39] and in the round-6b report's "Limits" [Src45 §6]. The most important:

- **One developer's work.** 37 jobs over about four weeks in phenix, cctbx and phenix_regression; a census of the
  suitable GC+ jobs, not a random sample of wider work [Src4 §1, §10].
- **Small counts.** The major-error comparisons rest on 6 GC+, 25 P and 18 P+R errors over all 37 jobs; one job
  (langchain-model-update) moves the overall major-error comparison, and one (case 6) moves GC+'s all-errors figure
  in the hard group [Src4 §10].
- **Measurement undercounts.** One blind reading finds about half the errors; later rounds found more for every arm
  [Src4 §6, §10; Src9].
- **The groups come from GC+'s own process.** "Hard", "medium" and "easy" are defined by what GC+'s layers caught,
  with cut-offs chosen after the results were seen; they show an association, not a rule usable in advance [Src4 §3].
- **Severity** rests on short descriptions tagged by one blind tagger; agreement with an earlier, partly unblinded
  tagging was 87% (κ 0.64) [Src4 §1, §10].
- **The time limit in round 5** cut most P+R+S runs short [Src9; Src12].
- **Cost** counts Claude's working time only; outside readings, publication and the Developer's time were not
  measured [Src4 §9].
- **Same model family.** Every worker, scorer, reader, tagger and checker was a Claude model; some outside readers
  were not [Src17 §1]. In round 6 the outside review (GC+O and the P+R search) came from a different model,
  gpt-6.1-sol [Src39], as in round 6b [Src45].
- **GC was replayed only on the 18 harder jobs, with a stand-in Developer** (round 6). The stand-in answered every
  question GC asked "keep to the task", so the replay could not show how GC works with a real developer; GC+O
  differs from GC in only 4 runs [Src39; Src41].
- **Round 6b used a scripted review packet.** The task text and the final diff, sent in one turn with no tools, and no
  developer filtering the findings; not GC's own `OUTSIDE_REVIEW.md`, which adds the tests and their output. GC+O\*
  tests "an outside review of the change", not GC's own review step [Src45 §6].
- **The developer's time was not measured in round 6b.** Reading each review and deciding what to accept takes the
  developer's time; the minutes and cost given are the session's only [Src45 §6].
- **The outside review's effect is narrow.** It comes from four of the 18 jobs; the without-case-6 condition is one
  run-level removal from failing; single items (the severity tags of case 1 typed-name and case 3 O1, or any one of
  several removals) decide the reading [Src45, "The answer in brief"].
- **Trigger H reaches beyond the evidence.** Trigger H's coverage (with "when unsure, H applies") is a judgement that
  extends beyond the four kinds of job where the outside review's effect was seen [Src53].
- **The scope rule's effect is estimated, not measured.** The estimate comes from the questions GC put to round 6's
  stand-in Developer, assuming each fix would have worked [Src41]. The narrower rule in GC 1.4 was adopted without a
  further test [Src55].
- **GC 1.4 has not been replayed.** Its trial was 4 runs of an earlier draft (trigger check) and 3 runs of the full 1.4 text, with their resumes after the outside review, on jobs already studied, an
  implementation check [Src52].
- **A security finding in the retired kit.** S179 and S078 (Appendix A) describe a real command-execution path in
  GC+'s publication precheck: `check --fetch` passes the `remote` value of a publication record (`OUTGOING.txt`) to
  `git fetch` unvalidated, so a crafted value such as `--upload-pack=<command>` runs that command. The code is still
  present in the retired kit's two copies: `cctbx_project/libtbx/guided_coding`, kept until users have moved, and the
  branch `full-kit-rev21` of `cctbx/guided_coding` [Src38]. Using it needs a crafted record in the user's own
  publication folder and a run of the old kit's check with `--fetch`. GC does not contain this code. Both copies were
  fixed on 2026-10-26: `check`, `confirm` and `carry-over` now refuse a record whose remote name or URL could be read
  as a git option, or whose URL names a remote helper (`ext::` and the like, which run programs), before any git
  call, as `outgoing` and `vet` already did for the name, with regression tests that fail on the
  old code and pass on the new.

# Source index

Paths are relative to `<rec>` = `phenix/.claude/records/2026-10-15-gc-replay-protocol/` unless they begin with
`modules/`, which means the Developer's `build_39/modules/` folder. SHA-256 values identify the exact files used.

| id | file | what | SHA-256 |
|---|---|---|---|
| Src1 | `EVIDENCE_REPORT_final.md` | First evidence report, stages 1 to 3 (2026-10-17); superseded | `693dab8b4176ffbb498f873cc71bb3e19bce0652da3f70426dd195b80727bd9b` |
| Src2 | `../2026-10-15-gc-review-tally/REVIEW_TALLY_REPORT.md` | Tally of GC+'s 85 task records | `ea1108313f94d00711e1ab34880f175334befb905fc94e623179b911250dcc8b` |
| Src3 | `walkthrough/LEDGER_R4.tsv` | Round-4/4b error ledger, all arms, with severity | `cb49a9ed94ce3e362a7f9a7f8fc2193b1f87c3bc427fd9aa6c6bd85a2daf8dbd` |
| Src4 | `walkthrough/REPORT_R4_RESULTS_draft3.md` | Round 4/4b report, draft 3 (Part B) | `58805f94d7dad2c2134c7271d9e486e0b03f8d6540fecdb0bafc74ad266ef401` |
| Src5 | `walkthrough/LEDGER_R4_SUMMARY.md` | All round-4/4b tables, from summarize_ledger_r4.py | `be7b4a26224ef09af839a3c66635d7a53f6eea312a3903b687c9922e8e5c5f47` |
| Src6 | `walkthrough/r4_reviews/REVIEW_DRAFT2_1_claude.md` | Outside reading 1 of draft 2 (Claude) | `93ba5032d8154eed881472b46beef472a2a296756c742f39aa1217516305a98c` |
| Src7 | `walkthrough/r4_reviews/REVIEW_DRAFT2_2_nonclaude.md` | Outside reading 2 of draft 2 (other model family) | `18edf2f93a1712ddd5478201244896eabd8d7b25acca90e5591703c92ec88c5a` |
| Src8 | `walkthrough/PLAN_MIDDLE_GROUND.md` | Round-5 plan, frozen by hash before the pilot | `f2431a5f7a045db19edfb401d85c4fc58b6b2399ac34a9d9e23bc66d91aa0e23` |
| Src9 | `walkthrough/REPORT_R5_RESULTS.md` | Round-5 report (Part C) | `b6d70a47a712479d142e86ca465921f9b3c9ef7d27721b57d7c29cf768711641` |
| Src10 | `walkthrough/r5_plan/R5_SUMMARY.md` | Round-5 figures, from r5_summarize.py | `87a96357992ff5110fb51055fccd28cde52b55480eb66b696a8a47b2c7ab3e8f` |
| Src11 | `walkthrough/r5_plan/ERRATA_R5_REPORT.md` | Erratum to the round-5 report | `dcfb0703fd9d6681d7982e87c88d144b8b1190c4b1ac8eaa542df717e673c813` |
| Src12 | `walkthrough/r5_timeout/TIMEOUT_CHECK.md` | Where the P+R+S runs stood at the time limit | `21dfecc671e807bfd401c6b2c4a41754c4d25e71151c00665badee90d53f1cd2` |
| Src13 | `walkthrough/r5_plan/R5_LEDGER.tsv` | Round-5 ledger | `2c67c6f996415f73dae7f0da9b348831a9832af51bdee751ed6dc7558765add1` |
| Src14 | `walkthrough/SEVERITY_LIST.md` | Every tagged error and its severity (the same table as Src4's appendix, Appendix A here) | `c324be319a548c73e59a466dc37be4fdad3b98e8e01977ef7c3a828bf0a8f8fd` |
| Src15 | `walkthrough/triage/POWER_CHECK.md` | Triage power check | `555f3ba6e7d6a67d2a7a33053c10b6ef85410b72827a68c3e402ad01d1a0f56a` |
| Src16 | `walkthrough/triage/TRIAGE_CHECK_REPORT.md` | Triage descriptive check | `f290f57ac7b9ab86086c31888b8e73685358d86bda59467fda50d3532de00a92` |
| Src17 | `walkthrough/lean/CASE_FOR_LEAN_GC.md` | The case for the shorter procedure, draft 3 | `e524b9d94dbf443360ce61c6ce6b239e4a79e1d98edb900d3cd1638589528aa5` |
| Src18 | `walkthrough/lean/OUTSIDE_REVIEW_1.md` | Outside review 1 of the proposal (packet-20) | `5ba524c7144d1024050560334a6f557eeeee27ce565c785fb119be7e39c014b5` |
| Src19 | `walkthrough/lean/OUTSIDE_REVIEW_2.md` | Outside review 2 of the proposal (packet-20) | `4c95e17a299036ac6562b814d37b030dc458123ceff26e20f0978ef5e4bc5dda` |
| Src20 | `walkthrough/final_report/sources/EVIDENCE_14b8371.md` | GC's published evidence page (cctbx/guided_coding 14b8371, git show) | `0dd1ecadb53df4efd314bbfa15646bfea4323339156a792f51a87962aa039b33` |
| Src21 | `walkthrough/lean/rename/behaviour_tests_v1_3/DIRECT_EVIDENCE.md` | Behaviour checks of GC version 1.3: Git state, diffs, hashes | `1ecce9aa2f4fe7a46a82e8d4521b1e7bad23a6c657b7b3dd618ea3c1b94f0a33` |
| Src22 | `walkthrough/lean/website/live_reviews/outside_review_wording/behaviour_test/run.json` | Behaviour check: outside review on request | `295d65a3fbed8db3423b595afe0f3f0760eddc22dbbe000d81b3d65fe18127ca` |
| Src23 | `modules/.claude/records/2026-10-23-lean-trial/LEAN_TRIAL_LOG.tsv` | Real-use trial log | `813f70ad35a180fc82580bc50a0bb86d5a22887516e84f9121533431b1af796d` |
| Src24 | `walkthrough/lean/p23/reviews/DISPOSITIONS.md` | Three outside reviews of GC revision 22, and their dispositions | `83f96e5e94326b2977185b281a7b5b230eeb5c086f9344031b210d5a6b1b237c` |
| Src25 | `walkthrough/FIRST_TEN_VS_NEW_4b.txt` | First ten against the 27 new, by source of discovery | `95ce4d35d597bc963103a12e19f174b08ce70e26bc40675722b06d502ad07fe4` |
| Src26 | `walkthrough/TEST_ADEQUACY.md` | Test adequacy of every arm | `99ea6bab9f8e53e6cdfbd341d2ad11f191aac7d19b9c125310619a0e7007041f` |
| Src27 | `walkthrough/GC_CLAUDE_TIME_R4.md` | GC+ Claude time and plain run times | `cc9e7c0244974dfa6610a4101b13b39d7bf90435a2979a06841a6ae68f0f5d34` |
| Src28 | `walkthrough/final_report/RECORD_snapshot.md` | The study's step-by-step record (RECORD.md, a living file; frozen copy) | `34c9df39146c2394962d5434ff8cfb98fdc895ec5a363f2a997edb0b7e44f8f6` |
| Src29 | `modules/.claude/records/2026-10-23-lean-trial/README.md` | The real-use trial: which drafts the first jobs ran | `2096c0f14fe8fa1effaab86e50619b234efd4424edca78fcdf38fc8629476098` |
| Src30 | `walkthrough/r4_reviews/REVIEW_1_claude.md` | Outside reading 1 of draft 1 (Claude) | `ca5373486bfd73b61e672ae76ec990439ccf71303ace7eaa9cdb0c23c164b478` |
| Src31 | `walkthrough/r4_reviews/REVIEW_2_nonclaude.md` | Outside reading 2 of draft 1 (other model family) | `09c753bff442e0eba4b41fc20c29291c04e2327bbd20c203daaffa0fa93144ad` |
| Src32 | `walkthrough/lean/HELPER_READING_P21.md` | The helper's reading of LEAN_GC.md | `b99f0747def441417dc22f66a7f024d66f3137c1f78451f9e9768bd74d5d824a` |
| Src33 | `r6_tools/gc_frozen/skill/SKILL.md` | GC's instructions, version 1.3 (cctbx/guided_coding 14b8371; the frozen copy round 6 ran, identical to it) | `d858eb609455e6757320bc41d0ea71c7e42b820d6967f68e18a3b8d7f767d3e1` |
| Src34 | `r6_tools/gc_frozen/skill/BATCH.md` | GC's supervised batch mode, version 1.3 (frozen copy, identical to 14b8371) | `743e6b721041da72c1d68f197bf51df604bf059f6e3e1cae86c9c52cae6f2377` |
| Src35 | `walkthrough/lean/rename/p22_reviews/REVIEW_1.md` | Outside review 1 of the retirement plan (packet-22) | `ccfc189813f039d4b84162d6bd53d0b4173bbce36cbd90b3963b8408b6cb1382` |
| Src36 | `walkthrough/lean/rename/p22_reviews/REVIEW_2.md` | Outside review 2 of the retirement plan (packet-22) | `36438c1b2f0208c91ab394381e6e52a13731935bced6355c579a8ed63243c5a4` |
| Src37 | `walkthrough/lean/rename/p22_reviews/REVIEW_3.md` | Outside review 3 of the retirement plan (packet-22) | `97d6774ea769cea8b79412ac89857443512c6decdb8854dd336c203a6f7dd634` |
| Src38 | `modules/cctbx_project/libtbx/guided_coding/payload/tools/publication_precheck.py` | The retired kit's publication precheck, as distributed in cctbx_project (identical on full-kit-rev21) | `f7d2c0381c7abd06748b1d5907a606f927389dbe782fe6fbfb89d524412767cc` |
| Src39 | `walkthrough/round6/REPORT_R6_RESULTS.md` | Round-6 report: GC replayed on the 18 caught-any jobs | `ce7deb1e2a7386e2da44c68f40ddf8d23efdbbc8833c222b9ed6591a747fc59c` |
| Src40 | `walkthrough/round6/R6_SUMMARY.md` | Round-6 figures, from r6_summarize.py | `0152614b9ec0c780b8f37b3893a5d8f4f44b841ff14de38fa2bd4be548210a0a` |
| Src41 | `walkthrough/round6/decision_count/DECISION_COUNT.md` | Round 6: decisions GC put to the stand-in Developer (decision N) | `c726d9585a3aae838ee4f419f6e5040b610548e09bb64119bfcd4490cf28190e` |
| Src42 | `walkthrough/final_report/PROTOCOL.md` | Protocol of the whole study, and protocol against what was done | `bc25bac7c7d294349e711f296b5c3874247fa1f2f0eade918c3b74e2937bf8f7` |
| Src43 | `walkthrough/round6/PLAN_ROUND6.md` | Round-6 plan: questions and reading rules (§2), decisions (§10) | `e930a9e16b61817d859ff1f57a8917dce9b6f29cb85eead52b737d8b9f70de38` |
| Src44 | `walkthrough/round6/READINGS_R6_DISPOSITIONS.md` | Three outside readings of the round-6 report and protocol, and their dispositions | `84e6009b89480977049f65b1a1f3909d3b2f0a45c7c31e6a4e5f2df0e6cde025` |
| Src45 | `walkthrough/round6b/REPORT_R6B_O_RESULTS.md` | Round-6b (step O) report, draft 3: what an outside review adds | `f68793b0b9dcb22b22996d92dcf91fa49f692acd2fae53b132f009745f8947ab` |
| Src46 | `walkthrough/round6b/PLAN_ROUND6B_O.md` | Round-6b step-O plan: reading rules (§2), decisions O-0 to O-12 (§10) | `ca83d55b66c2d380c9d6bf0182097bf5df979d50237e0f8dbb00e785cb2d7464` |
| Src47 | `walkthrough/round6b/R6B_SUMMARY.md` | Round-6b figures, from r6b_summarize.py | `1e81ee7c422af9712e2171afba6e37fc580da18cc545f5396eba460d28ea9cc1` |
| Src48 | `walkthrough/round6b/ceiling/CEILING.md` | O-P ceiling, computed before any step-O run | `7ad221b61c6b94380563fb484d6d5446faa32c20b15d4210b25563044a46b9ef` |
| Src49 | `walkthrough/round6b/PILOT_R6B_O.md` | Step-O pilot: acceptance | `ef9f7e895f825ce98c6dc365f474946151919620f6141a3dd8c4018e59d023f5` |
| Src50 | `walkthrough/round6b/CHECK_REPORT_R6B_O.md` | Internal check of the step-O report, draft 1 | `9759197e69d5aed11d97070b04d83f19bced05457bc3fc9b4bcb18a71578847e` |
| Src51 | `walkthrough/round6b/READINGS_R6B_O_DISPOSITIONS.md` | Outside reading of the step-O report (packet-29), and its dispositions | `6662c02e91d464893933e1fcbadad25f4908aef4e15429e6487933f57abc3820` |
| Src52 | `walkthrough/gc_rev23/TRIAL_1.4.md` | Trial of the GC 1.4 draft (implementation check) | `c8d4c99de923a5ffe21420ff936d4c5ecb0c4b0388326bfa56232520f2d4e6af` |
| Src53 | `walkthrough/gc_rev23/GC_1.3_to_1.4.diff` | What changed from GC 1.3 to the GC 1.4 draft | `134f5a9441cc7fb89c3a2df130daf67c10a81ce6ceb669cfbebe16365242a9ce` |
| Src54 | `walkthrough/gc_rev23/WEBSITE_SUMMARY_DRAFT.md` | Draft summary for the website: what helped, what did not, what hurt, what is kept untested (not published) | `6ec00ed061176d8fd881bfd7ce0dcb4144e7aa1d01b367eb65322d6e22cb1632` |
| Src55 | `RECORD.md` | The study's step-by-step record, a living file, as at 2026-10-26 (the Developer's decisions after round 6b) | `7738f6aa2a2d4423deb504e0d2a3964debfed296e0e9fd05cc0a8fe9a88f806a` |

# Appendix A. Every tagged error and its severity

Generated by `severity_appendix.py` from `LEDGER_R4.tsv` and the blind severity tagging (`r4_severity/`). One row per
distinct error (case, id) that some arm left at the end point, 205 in all.

- **severity** and **tagger's reason**: from the second, blind tagging, whose tagger saw only the case, the kind and
  the description, with arm names removed (six descriptions still named an arm or an earlier call: S047, S055,
  S070, S077, S092, S149; see report section 10). **first tagging**: the first tagging's severity, made from the same
  descriptions but with a source column that named the arm for many rows; shown so the two can be compared.
- *Major*: in normal use it gives wrong results or output
  silently, crashes or hangs a normal run, loses or overwrites data, is a real security problem, or leaves the reported
  problem unfixed; for a test, no test would fail if the bug came back. *Minor*: any other real error.
- **kind**: product (an error in program code), task (the reported problem itself), test (a test error or gap).
- **origin**: own (the arm made it), review (a review pass made it), pre (already in the code).
- **left in**: for each arm that has a ledger row, how the error ended: missed (remains or fixed later), disclosed
  (found, left on purpose and disclosed), fixed (found and fixed in the job). Plain counts are runs of that arm.
  An error that no row shows as missed or disclosed for an arm was not present there, or not found.
- **evidence**: confirmed, probable or undetermined. Confirmed task errors of any origin, and confirmed product
  errors of origin own or review, count in the headline when missed; pre-existing product faults are reported apart.
- **disclosed for P+R**: P+R is the P session resumed for one review pass, so a problem P disclosed stays disclosed
  for P+R unless P+R fixed it.

## Hard jobs (27 major, 50 minor)

| item | case | kind | error | severity | tagger's reason | first tagging | origin | left in | evidence |
|---|---|---|---|---|---|---|---|---|---|
| S158 | case 1 | product | explicit GUI output path not honoured: every GUI output is moved into the job directory | **major** | In normal GUI use every explicit output path is silently moved into the job directory. | major | own | P missed 1 of 4; P+R missed 1 of 4 | confirmed |
| S101 | case 3 | task | model-only manager fails check_consistency (two models crash) | **major** | A model-only manager still fails check_consistency with two models, so the reported crash remains. | major | own | GC+ fixed; P missed 1 of 2; P+R fixed 1 of 2 | confirmed |
| S120 | case 3 | product | a model without crystal symmetry next to a symmetric constructor model, or alone under an id other than 'model', still raises AttributeError in check_consistency (already in the code) | **major** | A model without crystal symmetry, a common input, still raises AttributeError in check_consistency. | major | pre | GC+ missed; P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S191 | case 3 | product | review pass introduced the AttributeError GC+ had caught | **major** | The review pass introduced an AttributeError into the product code. | major | own/review | GC+ fixed; P+R missed 1 of 2 | confirmed |
| S150 | case 5 | product | wait-loop stop still raises AssertionError, not Abort | **major** | A stop during the wait loop still ends in AssertionError rather than Abort, so the reported stop problem remains there. | major | own | GC+ missed | confirmed |
| S187 | case 5 | product | stop waits without bound | **major** | A stop that waits without bound can hang the run when a job does not respond. | major | own | GC+ fixed; P missed 2 of 2; P+R fixed 1 of 2, missed 1 of 2 | confirmed |
| S045 | case 6 | product | --dry-run requires the porcelain "To" line to equal remote_url, but git drops user@ there, so SSH or user@ remotes (the Developer's git@github.com origin) are always refused | **major** | Every SSH or user@ remote, including the Developer's own origin, is refused, so the dry run is unusable in normal use. | major | own | P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S123 | case 6 | product | merge commit second parent not checked | **major** | Not checking a merge commit's second parent lets unchecked side-branch commits be published. | minor | own | GC+ missed | confirmed |
| S126 | case 6 | product | failed dry run accepted | **major** | A failed dry run is accepted, so the gate silently passes a push it should refuse. | major | own | GC+ fixed; P missed 1 of 2; P+R missed 1 of 2 | confirmed |
| S179 | case 6 | product | OUTGOING remote value is not validated before --fetch: 'remote: --upload-pack=<cmd>' makes git fetch run that command | **major** | An unvalidated remote value lets --upload-pack run an arbitrary command, a real security problem. | minor | own | GC+ missed | confirmed |
| S197 | case 6 | product | SOURCE_MANIFEST not updated (startup guard fails) | **major** | The stale SOURCE_MANIFEST makes the startup guard fail, stopping every run. | major | own | P missed 1 of 2; P+R fixed 1 of 2 | confirmed |
| S017 | case 8 | product | TypeError when a build has no results | **major** | A build that finds nothing is a plausible outcome of a normal run and here it crashes with TypeError. | major | own | GC+ fixed; P disclosed 1 of 2; P+R disclosed 1 of 2 | confirmed |
| S048 | case 8 | product | two-build run reports output_pdb_file_name sequence_from_map.pdb, a file no build wrote (builds write prefixed names; already in the code) | **major** | A normal two-build run silently reports an output file name that no build wrote. | major | pre | GC+ missed; P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S059 | case 8 | product | supplied-sequence two-build run: optimal sequences not passed up (already in the code) | **major** | A normal supplied-sequence two-build run silently returns no optimal sequences. | major | pre | GC+ missed; P disclosed 1 of 2, missed 1 of 2; P+R disclosed 1 of 2, fixed 1 of 2 | confirmed |
| S064 | case 8 | test | no test reproduces the reported crash | **major** | No test reproduces the reported crash, so its return would go unnoticed. | major | own | P missed 1 of 2; P+R missed 1 of 2 | confirmed |
| S162 | case 8 | product | negative best score reported as 0 (already in the code; kept by the fix) | **major** | A negative best score is silently reported as 0, a wrong value in the results. | major | pre | GC+ missed; P missed 2 of 2; P+R fixed 1 of 2, missed 1 of 2 | confirmed |
| S167 | case 8 | task | reported one-sequence case still fails (not diagnosed) | **major** | The reported one-sequence case still fails. | major | pre | GC+ fixed; P disclosed 1 of 2; P+R disclosed 1 of 2 | confirmed |
| S180 | case 8 | product | best build optimal sequences not passed up (no-sequence run: results.optimal_sequences empty; single-build control has 1) | **major** | A no-sequence run silently returns no optimal sequences from the best build. | major | own | GC+ missed; P disclosed 1 of 2, missed 1 of 2; P+R fixed 2 of 2 | confirmed |
| S091 | case 9 | product | Windows stop_children crashes once the reader returns None | **major** | On Windows, stop_children crashes as soon as the reader returns None at end of output during a normal stop. | minor | own | GC+ fixed; P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S033 | langchain-model-update | product | LangChain (ChatAnthropic) path does not check stop_reason: cut-off reply passes as analysis (present at base) | **major** | A reply cut off at the token limit is silently used as a complete analysis on the LangChain path. | major | pre | GC+ disclosed; P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S134 | langchain-model-update | product | decision call (call_llm_simple, directive fallback) crashes on the thinking block of the new default: content[0].text; same for other 5.x ids (E4 folded in) | **major** | The decision call crashes on the new default model's thinking block in normal use. | major | own | P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S151 | langchain-model-update | product | log summariser crashes on ChatAnthropic list content with the new defaults ('list' has no split); same for other 5.x ids (E4 folded in) | **major** | The log summariser crashes on list content from the new default models in normal use. | major | own | P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S163 | langchain-model-update | task | Gemini/OpenAI defaults and sampling guard, phenix/gui/chat model names not updated (done in a later job) | **major** | Gemini/OpenAI defaults, the sampling guard and chat model names were left unupdated, so part of the task was not done. | major | own | GC+ disclosed; P disclosed 2 of 2; P+R disclosed 2 of 2 | confirmed |
| S176 | langchain-model-update | product | direct path: reply cut off at max_tokens (text block only) returned as a normal answer (already in the code) | **major** | A direct-path reply cut off at max_tokens is silently returned as a normal answer. | major | pre | GC+ fixed; P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S184 | langchain-model-update | product | direct Claude 5.x requests still capped at 2000 output tokens with thinking on | **major** | Direct Claude 5.x requests with thinking on stay capped at 2000 tokens, so normal replies are cut off. | major | own | GC+ fixed; P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S053 | langchain-test-health | task | tst_plan_autostop counted failures still hidden in run_all_tests: in-process it has 6 failing checks and is reported PASSED (shows only via the new standalone-health subprocess when the plant is in) | **major** | The runner still reports tst_plan_autostop as PASSED despite 6 failing checks, which is the problem the job was to fix. | major | own/pre | GC+ fixed; P missed 1 of 2; P+R missed 1 of 2 | confirmed |
| S093 | langchain-test-health | task | runner counts only 'is False' as failure: tst_halfmap_sigmaa_inventory returning 1 still reported PASSED | **major** | A test returning 1 is still reported PASSED, so the runner's hidden-failure problem is unfixed. | major | pre | P missed 1 of 2; P+R fixed 1 of 2 | confirmed |
| S005 | case 1 | test | setup_params hook timing untested | **minor** | Timing of the setup_params hook is a secondary detail whose absence from tests is a coverage gap only. | minor | own | P missed 1 of 4; P+R missed 1 of 4 | probable |
| S016 | case 1 | product | command-line gui.output_dir=X moves explicit output paths in X into the current directory | **minor** | Setting gui.output_dir on the command line is unusual, so moving explicit paths affects only that rare use. | minor | own | GC+ missed | confirmed |
| S031 | case 1 | test | no test starts the program as the GUI does | **minor** | The GUI start path is untested, but tests of the output path logic itself still exist. | minor | own | GC+ fixed; P missed 4 of 4; P+R missed 4 of 4 | confirmed |
| S044 | case 1 | test | half-map placement untested | **minor** | Half-map placement is a side path whose lack of tests is a coverage gap. | minor | own | GC+ disclosed; P missed 3 of 4; P+R missed 3 of 4 | confirmed |
| S065 | case 1 | product | output_files.composite_map_file=None / refined_model_file=None no longer suppresses those outputs; None now means the default name | **minor** | Setting those outputs to None is an uncommon way to suppress them and only extra files are written. | minor | own | P missed 1 of 4; P+R disclosed 1 of 4 | confirmed |
| S083 | case 1 | product | trailing "/" output name | **minor** | A trailing slash in an output name is an input-format edge case. | minor | own | GC+ fixed; P missed 2 of 4; P+R missed 2 of 4 | confirmed |
| S015 | case 2 | product | no Windows rename retry | **minor** | Missing a Windows rename retry only matters when another process holds the file on Windows. | minor | own | GC+ fixed; P missed 2 of 2; P+R fixed 2 of 2 | confirmed |
| S094 | case 2 | test | test does not cover all three writers | **minor** | Covering only some of the three writers is a coverage gap while the shared fix is tested. | minor | own | P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S119 | case 2 | product | predictable, non-exclusive temp file | **minor** | A predictable temp file name in the run directory is a low-risk robustness issue. | minor | own | GC+ fixed; P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S147 | case 2 | product | one_good_model's own INFO_FILE poller still decodes with the locale encoding, so a non-ASCII run directory (written as UTF-8) is misread under a non-UTF-8 locale (already in the code; p1 fixed it) | **minor** | It needs a non-ASCII run directory under a non-UTF-8 locale. | minor | pre | GC+ missed; P missed 1 of 2; P+R missed 1 of 2 | probable |
| S068 | case 3 | test | shift/unit-cell comparison untested | **minor** | The shift and unit-cell comparison is a secondary path without a test. | minor | own | GC+ fixed; P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S169 | case 3 | test | no-symmetry test does not assert that nothing raises | **minor** | The no-symmetry test not asserting no exception is a weak check, but an exception would still fail it. | minor | own | P missed 1 of 2; P+R missed 1 of 2 | confirmed |
| S060 | case 5 | product | a STOPWIZARD write that fails (OSError) ends the stop in that OSError instead of Abort; the pool is never joined and later jobs are not told to stop (already in the code; GC+'s D7/D8) | **minor** | A failing STOPWIZARD write needs an OSError on the run directory, which is rare. | minor | pre | P missed 2 of 2; P+R fixed 1 of 2, missed 1 of 2 | confirmed |
| S170 | case 5 | product | stop deadline uses time.time(), so a wall-clock change moves it | **minor** | A wall-clock change during a stop is rare. | minor | review | GC+ fixed; P+R missed 1 of 2 | confirmed |
| S192 | case 5 | product | after the 60 s wait the pool workers are terminated but a wizard that has not acted on STOPWIZARD keeps running after Abort | **minor** | A wizard that ignores STOPWIZARD keeps running after Abort, a cleanup gap in an uncommon case. | minor | own/review | GC+ disclosed; P+R disclosed 1 of 2 | confirmed |
| S199 | case 5 | test | STOPWIZARD delivery not shown with real files (added by the review pass) | **minor** | No real-file check of STOPWIZARD delivery is a verification gap. | minor | review | GC+ fixed; P+R missed 1 of 2 | confirmed |
| S025 | case 6 | test | positive-control tag test cannot pass | **minor** | A positive-control test that cannot pass is a broken test, but other checks of the tag logic remain. | minor | own | P missed 1 of 2; P+R fixed 1 of 2 | confirmed |
| S082 | case 6 | product | push.recurseSubmodules=on-demand only gives a NOTE: a commit with a gitlink is accepted though the push would also push the submodule | **minor** | Only a NOTE for on-demand submodule recursion is a warning-level gap in a rare configuration. | minor | own | GC+ missed | confirmed |
| S085 | case 6 | test | own test "not inside a Git work tree" fails when the temp dir lies inside a Git work tree (no GIT_CEILING_DIRECTORIES) | **minor** | The test fails falsely only when the temp dir lies inside a Git work tree. | minor | own | P missed 2 of 2; P+R fixed 1 of 2, missed 1 of 2 | confirmed/probable/undetermined |
| S098 | case 6 | product | any url.*.insteadOf rule, even for an unrelated host, makes check refuse (over-strict; fails safe) | **minor** | Refusing on any insteadOf rule is over-strict but fails safe. | minor | own | GC+ missed | confirmed |
| S102 | case 6 | product | --fetch runs a plain 'git fetch <remote>', which creates local tags (task: create no tags) | **minor** | Plain git fetch creating local tags breaks a stated task rule but publishes nothing. | minor | own | GC+ missed | confirmed |
| S135 | case 6 | product | --fetch runs before the destination check, unrestricted | **minor** | Fetching before the destination check only reads from the remote and pushes nothing. | minor | own | GC+ missed | confirmed |
| S136 | case 6 | product | an annotated tag id is accepted as 'commit' (the peeled id is not compared); the dry run shows the tag id going to the branch | **minor** | An annotated tag id passed as a commit is an unusual input. | minor | own | P missed 1 of 2; P+R fixed 1 of 2 | confirmed |
| S138 | case 6 | product | remote.origin.mirror=2 (true to Git) accepted: the truthy test knows only true/yes/on/1 | **minor** | A mirror value of 2 is an unusual spelling of true. | minor | own | P missed 1 of 2; P+R fixed 1 of 2 | confirmed |
| S154 | case 6 | product | check accepts push.followTags=true (task: refuse settings that follow tags; the printed command still overrides it) | **minor** | push.followTags is accepted but the printed command overrides it, so it fails safe. | minor | own | P missed 1 of 2; P+R missed 1 of 2 | confirmed |
| S185 | case 6 | test | no test of a failed config query | **minor** | A failed config query is an untested error path. | minor | own | P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S186 | case 6 | product | printed push command is not shell-quoted: a REPO path with a space splits into two words | **minor** | A REPO path with a space only breaks the printed command for copy-paste. | minor | own | GC+ missed | confirmed |
| S190 | case 6 | test | no test of a failed dry run | **minor** | A missing test of a failed dry run is a coverage gap for a side path. | minor | own | P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S006 | case 8 | product | score 0 reported when nothing scored | **minor** | Reporting 0 when nothing scored is misleading only in the empty edge case. | minor | own | GC+ fixed; P missed 2 of 2; P+R fixed 1 of 2, missed 1 of 2 | confirmed |
| S042 | case 8 | test | combination tests only one sequence | **minor** | Testing combination with only one sequence is a coverage gap, not a missing regression test. | minor | own | P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S164 | case 8 | test | no test of builds that find nothing | **minor** | No test of builds that find nothing is a coverage gap beside the reported case. | minor | own | P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S000 | case 9 | test | fixture encoding | **minor** | A fixture encoding problem weakens the test setup but does not by itself leave the fix unprotected. | minor | own | GC+ fixed; P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S026 | case 9 | product | review change: with ignore_errors_in_subprocess=True an unreadable healthy log plus one failed job aborts the run (Sorry) | **minor** | Aborting needs ignore_errors_in_subprocess plus an unreadable healthy log and a failed job together. | minor | review | P+R disclosed 1 of 2 | confirmed |
| S030 | case 9 | product | collect_runs not retried: one transient INFO_FILE read failure drops a finished run ('SKIPPING RUN ... AS IS MISSING'; already in the code) | **minor** | Dropping a run needs a transient INFO_FILE read failure, which is rare. | major | pre | GC+ missed | confirmed |
| S046 | case 9 | test | Windows stop path untested | **minor** | The Windows stop path is a platform side path without a test. | minor | own | GC+ fixed; P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S110 | case 9 | test | test does not pin the retry policy | **minor** | Not pinning the retry policy leaves the policy free to drift but the retry itself is tested. | minor | own | GC+ fixed; P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S203 | case 9 | product | log read in the same poll unprotected (adjacent, already in the code) | **minor** | The unprotected log read in the same poll is an adjacent robustness gap. | major | pre | GC+ missed; P missed 1 of 2; P+R missed 1 of 2 | confirmed |
| S145 | langchain-model-update | product | 60 s LangChain timeout with larger replies (accepted limit) | **minor** | The 60 s LangChain timeout is an accepted, documented limit. | minor | own | GC+ disclosed | confirmed |
| S198 | langchain-model-update | product | dotted gateway names (claude-opus-4.7) not recognised by the sampling rule (already in the code) | **minor** | Dotted gateway model names are a nonstandard spelling. | minor | pre | GC+ disclosed; P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S002 | langchain-test-health | product | _read_sequence (strict utf-8, catch-all except) returns '' for a FASTA with one Latin-1 header byte, losing the sequence (already in the code on UTF-8 locales) | **minor** | Losing the sequence needs a Latin-1 byte in a FASTA header, which is outside normal UTF-8 input. | minor | pre | GC+ missed | confirmed |
| S040 | langchain-test-health | test | repaired tst_fix_verification check slices to an unchecked find() end and can pass vacuously | **minor** | A vacuous slice in one repaired check weakens it but other checks in the file still run. | minor | own | P missed 2 of 2; P+R disclosed 1 of 2, missed 1 of 2 | confirmed |
| S073 | langchain-test-health | product | after_program AUTO-STOP suppression in graph_nodes.plan leaves should_stop set, so rules-only / LLM-fallback planning stops anyway (already in the code; the repaired test stubs the rules selector around it) | **minor** | Planning stops wrongly only in rules-only or LLM-fallback mode, not the main path. | major | pre | GC+ missed; P missed 1 of 2; P+R missed 1 of 2 | confirmed |
| S121 | langchain-test-health | test | 8 run functions call sys.exit(1), aborting the runner without its summary (already in the code; fixed later in runner-hygiene) | **minor** | sys.exit in run functions cuts the runner summary short but failures are still visible. | minor | pre | GC+ disclosed; P missed 1 of 2; P+R missed 1 of 2 | confirmed |
| S129 | langchain-test-health | product | agent modules import libtbx.langchain.utils.run_utils (and pattern_manager) with no fallback; standalone import fails (already in the code) | **minor** | The standalone import failure only matters outside the normal installed package. | minor | pre | GC+ missed; P disclosed 1 of 2, missed 1 of 2; P+R disclosed 1 of 2, missed 1 of 2 | confirmed |
| S152 | langchain-test-health | test | with phenix ai_agent.py missing, tst_directive_layer_diagnostics raises IOError at import and run_all_tests aborts without its summary | **minor** | The import abort needs phenix ai_agent.py to be missing, an incomplete installation. | minor | own | P missed 1 of 2; P+R fixed 1 of 2 | confirmed |
| S156 | langchain-test-health | test | tst_audit_fixes intermittent (already in the code) | **minor** | An intermittent test is a flakiness problem. | minor | pre | GC+ disclosed | confirmed |
| S161 | langchain-test-health | product | 8 unencoded open() calls in langchain production files outside agent/ (fixed later in runner-hygiene) | **minor** | Unencoded open() calls only matter under a non-UTF-8 locale. | minor | pre | GC+ disclosed; P disclosed 1 of 2, missed 1 of 2; P+R disclosed 1 of 2, missed 1 of 2 | confirmed |
| S171 | langchain-test-health | test | tst_fix_verification tests 10-14 skip silently when $PHENIX is unset (no sibling-module fallback; dispatcher sets PHENIX) (already in the code) | **minor** | Silent skips need $PHENIX unset, which the dispatcher normally sets. | minor | pre | GC+ missed | confirmed |
| S174 | langchain-test-health | test | no end-to-end main() test of the runner; H4 a substring check | **minor** | No end-to-end main() test is a coverage gap while unit checks remain. | minor | own | GC+ disclosed | confirmed |
| S195 | langchain-test-health | test | runner counted {"status":"PASS","failed":N} as a pass (not disclosed; changed in runner-hygiene) | **minor** | The runner miscounting one status format is a test-harness weakness. | minor | own | GC+ missed | confirmed |

## Medium jobs (14 major, 36 minor)

| item | case | kind | error | severity | tagger's reason | first tagging | origin | left in | evidence |
|---|---|---|---|---|---|---|---|---|---|
| S001 | case 4 | product | averaged overall_scale never stored (already in the code) | **major** | The averaged overall_scale is computed but never stored, so the reported value silently differs from the average. | minor | pre | GC+ disclosed; P disclosed 1 of 2, missed 1 of 2; P+R disclosed 2 of 2 | confirmed |
| S194 | case 4 | product | ranking not rotation-invariant; isotropic tensor can win | **major** | The tensor ranking is not rotation-invariant, so an isotropic tensor can be wrongly chosen. | major | own | GC+ fixed; P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S200 | case 4 | product | overall_si missing at one of several locations still breaks the average (already in the code) | **major** | overall_si missing at one of several locations still breaks the average in a normal multi-location run. | minor | pre | GC+ disclosed | confirmed |
| S029 | case 7 | product | one cut-off chunk loses the summary | **major** | A single truncated chunk silently drops the whole log summary in normal long-log use. | minor | own | GC+ fixed; P missed 2 of 2; P+R fixed 1 of 2, missed 1 of 2 | confirmed |
| S075 | case 7 | product | summarizer's per-batch asyncio.wait_for still uses the caller's 60 s: replies over 60 s lose the log summary (run_ai_analysis path) | **major** | Replies longer than 60 s, common with thinking models, silently lose the log summary. | major | own | GC+ disclosed | confirmed |
| S071 | case 10 | task | test still fails on this Mac (0.573 vs 0.572); disclosed with the cause in the final report | **major** | The test still fails on this Mac, so the reported problem is not fixed even though it was disclosed. | major | pre | P disclosed 2 of 2; P+R disclosed 2 of 2 | confirmed |
| S107 | case 10 | product | second get_cc still reads run 1 map (not diagnosed) | **major** | The second get_cc still reads the first run's map, giving a wrong correlation. | major | pre | GC+ fixed; P disclosed 2 of 2; P+R disclosed 2 of 2 | confirmed |
| S078 | gc-next-revision | product | check --fetch passes the record's remote name to git fetch unvalidated (parse_outgoing checks no remote pattern), so a value like --upload-pack=... is read as a git option, before check_destinations runs (already in the code) | **major** | An unvalidated remote name lets a record inject git options such as --upload-pack, a real command-execution hole in a publication gate. | minor | pre | GC+ missed; P disclosed 1 of 2, missed 1 of 2; P+R disclosed 1 of 2, missed 1 of 2 | confirmed |
| S133 | langchain-gemini-openai | product | phenix run_ai_analysis.py (assessment, advice preprocessing, failure diagnosis) reads Gemini 3 list-of-blocks replies as text: log analysis with Google broken | **major** | Log analysis with Google Gemini 3 is broken because list-of-blocks replies are read as text. | major | own | GC+ missed | confirmed |
| S018 | mmm-cc-star-none | test | no test with a missing per-direction CC* list | **major** | With no test for a missing per-direction CC* list, the reported crash could return unnoticed. | minor | own | P disclosed 1 of 2, missed 1 of 2; P+R disclosed 1 of 2, missed 1 of 2 | confirmed |
| S037 | mmm-cc-star-none | product | pre-existing averaging/summary issues: overall_si divided by all locations not n_used, empty list counted in n_used, overall_si unguarded if None (already in the code) | **major** | Dividing overall_si by all locations instead of n_used silently gives a wrong average whenever a location is skipped. | minor | pre | GC+ disclosed; P disclosed 2 of 2; P+R fixed 2 of 2 | confirmed |
| S084 | mmm-cc-star-none | test | no regression test for the reported crash | **major** | There is no regression test for the reported crash. | major | own | P disclosed 1 of 2, missed 1 of 2; P+R disclosed 1 of 2, missed 1 of 2 | confirmed |
| S062 | process-raw-data-reconstructed-f | test | tests do not compare the written F(+)/F(-) values, sigmas and free flags with the input | **major** | Without comparing written F(+)/F(-), sigmas and flags to the input, no test would catch wrongly converted data. | minor | own | GC+ disclosed | confirmed |
| S155 | process-raw-data-reconstructed-f | test | no test through label selection compares the merged F written with the input F column | **major** | No test through label selection compares merged F with the input F, so a wrong column could return unnoticed. | minor | own | GC+ fixed; P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S182 | case 4 | test | no test with isotropic or rotated tensors | **minor** | Isotropic and rotated tensors are untested cases beyond the main fix. | minor | own | P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S004 | case 7 | test | no test of one cut-off chunk | **minor** | The single cut-off chunk case lacks a test, but other cut-off handling tests still exist. | minor | own | P missed 2 of 2; P+R fixed 1 of 2, missed 1 of 2 | confirmed |
| S157 | case 7 | product | Ollama done_reason and content_filter cut-offs not detected | **minor** | Ollama done_reason and content_filter cut-offs are less common provider paths. | minor | own | GC+ disclosed | confirmed |
| S081 | case 10 | product | a missing correlation does not fail the test | **minor** | A missing correlation not failing makes the test weaker in a case that should not happen. | major | own | P missed 1 of 2; P+R missed 1 of 2 | confirmed |
| S124 | case 10 | product | test verdict depends on printed elapsed times | **minor** | A verdict tied to printed elapsed times makes the test flaky rather than wrong. | major | own | GC+ fixed; P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S039 | gc-next-revision | product | check accepts a hand-written one-commit record for a merge commit whose first parent is the base; pushing it also publishes the side branch (already in the code) | **minor** | It needs a hand-written one-commit record for a merge commit, which is not the normal workflow. | minor | pre | GC+ missed; P disclosed 2 of 2; P+R disclosed 2 of 2 | confirmed |
| S051 | gc-next-revision | product | check --dry-run without --fetch passes a multi-commit push when the tracking ref is stale (already in the code; documented that --fetch is required) | **minor** | The stale-ref pass needs omitting --fetch, which the documentation says is required. | minor | pre | GC+ disclosed; P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S096 | gc-next-revision | product | default repository name is the work tree folder name; WORKER.md command has no --repository, so a record made in a staging worktree carries the worktree name | **minor** | A worktree-named repository field is a record labelling inaccuracy that is caught at check time. | minor | own | GC+ missed; P disclosed 1 of 2; P+R disclosed 1 of 2 | probable |
| S142 | gc-next-revision | product | outgoing --fetch runs before check_destinations (insteadOf/pushurl/mirror settings unchecked when it fetches) | **minor** | The fetch only reads from the remote before the push-setting checks run. | minor | own | GC+ missed; P missed 1 of 2; P+R missed 1 of 2 | probable |
| S010 | langchain-gemini-openai | test | old SDK path and ollama/portkey invariance not tested | **minor** | Old SDK and ollama/portkey invariance are side paths whose lack of tests is a coverage gap. | minor | own | GC+ disclosed | confirmed |
| S080 | langchain-gemini-openai | product | test_api_keys.py Google check sends 5 output tokens to a thinking default: empty reply | **minor** | The key-check script misreports Google keys, a developer utility rather than the program. | minor | pre | P missed 1 of 2; P+R fixed 1 of 2 | probable |
| S087 | langchain-gemini-openai | test | new tst_provider_reasoning_models.py not registered in run_all_tests.py, so the package runner never runs it | **minor** | The new test exists and passes standalone; it is only not registered in the package runner. | minor | own | GC+ missed | confirmed |
| S088 | langchain-gemini-openai | product | chat anywhere in the id marks an OpenAI model non-reasoning: a fine-tune id containing "chat" gets temperature and a 400 | **minor** | Only an OpenAI fine-tune id containing "chat" is misclassified. | minor | own | GC+ missed; P missed 2 of 2; P+R fixed 2 of 2 | probable |
| S089 | langchain-gemini-openai | test | tests/llm/framework.py (keyed planning suite) still reads response.content, so Gemini 3 list replies are not parsed | **minor** | The keyed planning test framework misreads Gemini 3 replies, a test-harness limitation. | minor | own | GC+ missed; P missed 1 of 2; P+R missed 1 of 2 | probable |
| S106 | langchain-gemini-openai | product | unversioned Gemini aliases (gemini-flash-latest) get no output floor: thinking alias keeps the 2000 cap and is cut off (now raised) | **minor** | Only unversioned Gemini aliases miss the output floor, and the cap has since been raised. | minor | own | P missed 1 of 2; P+R disclosed 1 of 2 | probable |
| S114 | langchain-gemini-openai | product | tests/test_api_keys.py unchanged: sends max_tokens=5 to gpt-6-luna and 5 output tokens to thinking gemini-3.8-flash, so the key checker likely reports a valid key as failing or empty | **minor** | The key-check script misreports valid keys, a developer utility outside the program. | minor | own | GC+ missed | confirmed |
| S146 | langchain-gemini-openai | product | Portkey/Azure direct path keeps the 2000 cap (same truncation class) | **minor** | The Portkey/Azure path keeping the old cap is a secondary path. | major | pre | GC+ disclosed; P disclosed 2 of 2; P+R disclosed 2 of 2 | confirmed |
| S193 | langchain-gemini-openai | test | the two post-review fixes not run live | **minor** | The two post-review fixes not run live is a verification gap. | minor | own | GC+ disclosed | confirmed |
| S159 | langchain-provider-todos | product | summarizer early returns lack parts_total/parts_skipped | **minor** | Missing parts_total/parts_skipped on early returns is a reporting detail. | minor | own | GC+ disclosed | confirmed |
| S168 | langchain-provider-todos | product | Anthropic stop_reason "refusal" and Gemini SAFETY-type reasons not detected (fixed later in langchain-refusal-signals) | **minor** | Refusal and SAFETY stop reasons are uncommon outcomes. | minor | pre | GC+ disclosed; P missed 2 of 2; P+R disclosed 2 of 2 | confirmed |
| S181 | langchain-provider-todos | product | direct Ollama calls now use openai_reply_text, so an empty Ollama reply raises; on the main directive path extract_directives returns {} instead of its Ollama pattern-extraction fallback | **minor** | An empty Ollama reply is an uncommon case on a secondary provider. | minor | own | GC+ missed | confirmed |
| S032 | mmm-cc-star-none | test | no test mixes valid and missing CC* data (closed by job mmm-cc-star-mixed-test, which exposed two averaging bugs) | **minor** | Mixed valid and missing CC* data is a further case beyond the tested missing-data crash. | minor | own | GC+ disclosed | confirmed |
| S056 | mmm-cc-star-none | product | with a supplied TLS group and every location skipped, _analyze_aniso_replace_with_supplied stops at assert std_values.scaling_info_list (already in the code) | **minor** | The assertion needs a supplied TLS group with every location skipped, an edge case. | minor | pre | GC+ missed; P disclosed 2 of 2; P+R disclosed 2 of 2 | confirmed |
| S008 | phenix-chat-tools | product | a 400 that names another parameter but whose text mentions reasoning_effort is retried with 'none' (loose text match) | **minor** | The loose text match only misfires on a 400 that names another parameter yet mentions reasoning_effort. | minor | own | P missed 1 of 2; P+R fixed 1 of 2 | confirmed |
| S036 | phenix-chat-tools | product | positive thinking budget on Claude Opus 4.7/4.8 still sends budget_tokens, which those models reject (already in the code; minor; disclosed as unchecked) | **minor** | Only a user-set positive thinking budget on Opus 4.7/4.8 triggers the rejection, and it fails loudly. | minor | pre | P disclosed 1 of 2, missed 1 of 2; P+R disclosed 1 of 2, missed 1 of 2 | probable |
| S086 | phenix-chat-tools | product | Azure deployment names without the model name are not matched | **minor** | Azure deployment names without the model name are a configuration edge case. | minor | own | GC+ disclosed | confirmed |
| S099 | phenix-chat-tools | test | no full live chat session | **minor** | No full live chat session is a verification gap. | minor | own | GC+ disclosed | confirmed |
| S100 | phenix-chat-tools | test | thinking test checks only the thinking type, not that thinking text is shown | **minor** | The thinking test checks the request type but not the displayed text, a partial assertion. | minor | own | P missed 1 of 2; P+R missed 1 of 2 | confirmed |
| S105 | phenix-chat-tools | product | tool turns on gpt-6-luna / gpt-5.6-sol run with reasoning off; keeping reasoning needs the Responses API | **minor** | Tool turns running with reasoning off is a documented limit of the Chat Completions path. | minor | own | GC+ disclosed; P disclosed 2 of 2; P+R disclosed 2 of 2 | confirmed |
| S122 | phenix-chat-tools | product | adaptive thinking sent without display "summarized": 5.x streams no thinking text | **minor** | Missing thinking text in the display is a cosmetic chat problem. | minor | own | GC+ fixed; P missed 1 of 2; P+R missed 1 of 2 | confirmed |
| S127 | phenix-chat-tools | test | Azure behind Portkey acceptance of "none" untested | **minor** | Azure behind Portkey accepting "none" is an untested provider path. | minor | own | GC+ disclosed | confirmed |
| S172 | phenix-chat-tools | product | reasoning_effort 'none' remembered before the retry is accepted, so after a refused retry every later tool turn starts from the known-bad request | **minor** | Remembering 'none' early only costs an extra refused request on later turns. | minor | own | P missed 2 of 2; P+R fixed 2 of 2 | confirmed |
| S201 | phenix-chat-tools | product | a turn without tools but with tool history keeps default reasoning (not probed) | **minor** | A turn with tool history but no tools keeping default reasoning is an unprobed corner. | minor | own | GC+ disclosed | confirmed |
| S079 | process-raw-data-reconstructed-f | test | no-ISYM layout, incomplete Bijvoet pairs and the reporter's MTZ not exercised by tests | **minor** | Missing tests for no-ISYM layout and incomplete pairs are coverage gaps beyond the main case. | minor | own | GC+ disclosed; P missed 1 of 2; P+R missed 1 of 2 | confirmed/probable |
| S148 | process-raw-data-reconstructed-f | product | merged SIGF recomputed from the pairs, not taken from the input SIGF (as for native anomalous data) | **minor** | Recomputing merged SIGF from the pairs is a defensible estimate, not a clear error. | minor | pre | GC+ disclosed; P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S173 | process-raw-data-reconstructed-f | product | dead reconstructed branch of data_labels() and stale XXX comment kept | **minor** | Dead code and a stale comment are cleanliness issues. | minor | pre | GC+ disclosed | confirmed |

## Easy jobs (8 major, 67 minor, 3 not-an-error)

| item | case | kind | error | severity | tagger's reason | first tagging | origin | left in | evidence |
|---|---|---|---|---|---|---|---|---|---|
| S069 | auto-q2m-b | product | map built with a list unit_cell_grid and given the same list now drops to P1 (tuple != list); GC+ did not disclose this effect (its __init__ limit names only is_full_size) | **major** | Passing the same grid as a list silently drops the map's symmetry to P1. | major | own | GC+ missed; P missed 2 of 2; P+R fixed 2 of 2 | confirmed |
| S052 | auto-q2m-c | task | stopped for a decision, no change (dummy map_manager question for a strict is_compatible_model); disclosed | **major** | The job stopped for a decision and made no change, so the reported problem stays unfixed. | major | own | P disclosed 2 of 2; P+R disclosed 2 of 2 | confirmed |
| S143 | auto-q3-a | product | target arriving in another frame (or shift_cart None at s != 0) still compared in the wrong frame; label-only fix | **major** | Targets in another frame are still compared in the wrong frame because the fix only changed a label. | major | own | GC+ disclosed | confirmed |
| S125 | developer-html-link-fallback | product | CCTBX API fallback https://cci.lbl.gov/cctbx_docs/index.html (the user's example link) returns 404 (redirect to /docs/cctbx/index.html); disclosed as unverified | **major** | The fallback link for the user's own example goes to a 404 page, so the reported link problem is not resolved there. | minor | own | P disclosed 1 of 2; P+R disclosed 1 of 2 | probable |
| S153 | developer-html-link-fallback | product | page still read/written in the locale encoding; the draft page has U+201D, so on a cp1252 Windows locale the read fails (already in the code; GC+ pre-plan finding P2) | **major** | On a cp1252 Windows locale reading the page fails because it contains U+201D, a common Windows setup. | minor | pre | P missed 2 of 2; P+R fixed 2 of 2 | confirmed |
| S021 | developer-page-followups | product | Windows file URLs stay file://C:\... (already in the code) | **major** | Ordinary Windows installs get malformed file://C:\ links, so local docs links do not open correctly. | minor | pre | GC+ disclosed | confirmed |
| S144 | f9-f6-start-f9 | test | test handler-view asserts check the test's own copy of the pattern and pass on baseline | **major** | The handler asserts check the test's own copy of the pattern and pass on baseline, so they cannot catch the bug's return. | minor | own | GC+ disclosed | confirmed |
| S047 | gc-rev15-macos-ci | test | fixture-vs-real layout assertion removed for every ar (Apple and GNU too, where it passed): now a stderr note only (reader: major) | **major** | Removing the layout assertion for every ar means no test fails if the fixture and real layouts diverge again. | minor | own | GC+ missed | confirmed |
| S007 | auto-mmm-a | product | extra model shifted twice (AssertionError) when the supplied map is already shifted (already in the code; outside criterion A1-A2) | **minor** | The double shift needs an extra model with a pre-shifted supplied map and fails loudly with an assertion. | major | pre | GC+ disclosed | confirmed |
| S149 | auto-mmm-a | product | with ignore_symmetry_conflicts=True and maps already shifted before construction, the supplied NCS is relabelled (set_shift_cart) without being moved, so its centres sit ~74 A from the map; the default path places them correctly (already in the code; GC+ now also copies the misplaced NCS to the half and extra maps) | **minor** | The misplaced NCS needs ignore_symmetry_conflicts=True with pre-shifted maps, a non-default path. | minor | pre | GC+ missed; P missed 2 of 2; P+R disclosed 1 of 2, fixed 1 of 2 | confirmed |
| S058 | auto-mmm-b | product | add_crystal_symmetry_to_model_if_necessary calls non-existent self.any_map_manager() (already in the code; left open by the job front door) | **minor** | The non-existent method is reached only when no map_manager is passed, which the normal callers avoid. | major | pre | GC+ disclosed; P disclosed 2 of 2; P+R disclosed 2 of 2 | confirmed |
| S009 | auto-q1-a | test | test builds the result with hand-copied get_results() field names, so a field rename in the program is not noticed | **minor** | Hand-copied field names make the test brittle to renames but it still exercises the fixed behaviour. | minor | own | GC+ disclosed | confirmed |
| S043 | auto-q1-a | test | any exception importing the launcher makes the new test skip and end OK | **minor** | The skip-on-any-import-error guard can hide breakage but the test runs where the launcher imports. | minor | own | P missed 2 of 2; P+R fixed 2 of 2 | confirmed |
| S115 | auto-q1-a | test | test mocks the program run; dock_in_map and the GUI are not run | **minor** | Mocking the program run limits realism but still tests the fixed logic. | minor | own | GC+ disclosed | confirmed |
| S061 | auto-q1-c | test | mocked test only; whether real runs give all-negative scores not checked | **minor** | The mocked test checks the logic; whether real runs give all-negative scores is a confidence gap. | minor | own | GC+ disclosed | confirmed |
| S130 | auto-q1-c | product | NaN as a build's first score is kept as the combined score (old code took the later score) | **minor** | A NaN first score is an unusual input. | minor | own | GC+ disclosed; P missed 1 of 2; P+R missed 1 of 2 | confirmed |
| S166 | auto-q1-c | test | no test of mixed-sign scores across builds | **minor** | Mixed-sign scores across builds are an untested further case. | minor | own | GC+ disclosed | confirmed |
| S175 | auto-q2m-a | product | relabel changes the caller's ncs_object in place (the constructor keeps the reference), so another map_manager built with the same object is left with a stale NCS shift_cart after one map is re-origined (follows the bug report's smallest fix) | **minor** | The stale shift needs the same ncs_object shared by two map_managers. | minor | own | GC+ missed; P missed 2 of 2; P+R disclosed 1 of 2, fixed 1 of 2 | confirmed |
| S066 | auto-q2m-b | product | list unit_cell_grid kept raw in __init__: resample_on_different_grid(target_grid_spacing) of a wrapped full-size map fails the __init__ is_full_size assert | **minor** | The failing assert needs a list unit_cell_grid combined with resample_on_different_grid on a wrapped map. | minor | pre | GC+ disclosed; P disclosed 1 of 2, missed 1 of 2; P+R fixed 2 of 2 | confirmed |
| S139 | auto-q2m-b | product | pre-existing bare is_similar_symmetry assertion when a full-size non-P1 map is given a larger gridding (outside job B) | **minor** | The assertion needs a larger gridding on a full-size non-P1 map, outside the job. | minor | pre | GC+ disclosed; P disclosed 1 of 2, missed 1 of 2; P+R disclosed 1 of 2, missed 1 of 2 | confirmed |
| S057 | auto-q3-a | test | test case (a) does not assert the generated map is P1 | **minor** | The P1 property is not asserted, but the test still exercises the generated map. | minor | own | GC+ disclosed | confirmed |
| S204 | auto-q3-a | test | test uses only an exact-copy target, so a renamer that renamed nothing would pass | **minor** | An exact-copy-only target lets a do-nothing renamer pass, a weak test of the renaming step rather than of the reported frame bug. | minor | own | GC+ missed | probable |
| S011 | auto-q3-d | product | dock_and_rebuild docked_model_info still carries chain model objects (placements[*].chain_group.model) | **minor** | Leftover chain model references in placements add weight to the result but do not change docking output. | minor | own | GC+ disclosed; P disclosed 2 of 2; P+R disclosed 2 of 2 | confirmed |
| S038 | auto-q3-d | test | test passes if a fix deleted the attribute instead of setting None | **minor** | The test could miss a deletion variant but does check the attribute value in the intended fix. | minor | own | GC+ disclosed | confirmed |
| S074 | combine-focused-maps-empty-region | product | use_first_map_as_template_only with a chain only in model 1 still crashes with float - None TypeError in get_chain_weights (already in the code, adjacent) | **minor** | The crash is in an adjacent option combination outside the reported case. | minor | pre | GC+ missed; P missed 2 of 2; P+R fixed 2 of 2 | confirmed |
| S108 | combine-focused-maps-empty-region | product | get_chain_weights treats a CC of exactly 0.0 as region absent (misleading model-1 Sorry, weights not summing to 1); already in the code, left unchanged | **minor** | A CC of exactly 0.0 is an unlikely value. | minor | pre | GC+ missed; P disclosed 2 of 2; P+R fixed 2 of 2 | confirmed |
| S118 | combine-focused-maps-empty-region | test | new tst_07 catch-all import guard: any import failure prints skipping and passes | **minor** | A catch-all import guard can hide breakage but the test runs normally where imports succeed. | minor | own | GC+ disclosed; P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S132 | combine-focused-maps-empty-region | product | region present only in model 1 with use_first_map_as_template_only now reaches the float - None TypeError instead of a Sorry (chain mode already had it) | **minor** | The TypeError needs a region present only in model 1 with use_first_map_as_template_only. | minor | own | P missed 2 of 2; P+R fixed 2 of 2 | confirmed |
| S003 | developer-html-link-fallback | product | API-card notes inherit the title semi-bold weight (cosmetic) | **minor** | A note inheriting the title's semi-bold weight is purely cosmetic. | minor | own | GC+ disclosed | confirmed |
| S022 | developer-html-link-fallback | test | Windows not run (UTF-8 change addresses portability only) | **minor** | Not running on Windows limits confidence for a portability-only change. | minor | own | GC+ disclosed | confirmed |
| S028 | developer-html-link-fallback | product | a percent-encoded href (chat%20bot.html) is checked undecoded, so an existing local file is not found and the link goes online (latent) | **minor** | No shipped link is percent-encoded, so the undecoded check is latent. | minor | own | GC+ missed; P missed 1 of 2; P+R fixed 1 of 2 | confirmed |
| S034 | developer-html-link-fallback | product | a file:// link carrying #fragment or ?query is treated as missing: with the API built, the API links go to the in-page instructions instead of the local copy (latent: the shipped page has no such link) | **minor** | No shipped link carries a fragment or query, so the misclassification is latent. | minor | own | GC+ missed; P missed 1 of 2; P+R fixed 1 of 2 | confirmed |
| S063 | developer-html-link-fallback | product | a missing link outside any <li> takes the build command of an unrelated later item (latent: all such links are in <li>) | **minor** | All such links sit inside li elements, so the wrong build command is latent. | minor | own | P missed 1 of 2; P+R fixed 1 of 2 | confirmed |
| S076 | developer-html-link-fallback | test | outside reader could not run the shipped test without Phenix | **minor** | Needing Phenix to run the test is an inconvenience for outside readers only. | minor | own | GC+ disclosed | confirmed |
| S092 | developer-html-link-fallback | product | phenix.developer passes None to os.path.isfile when developer.html is missing: TypeError (already in the code; GC+ deferred it) | **minor** | developer.html missing is an incomplete-installation edge case. | minor | pre | P missed 2 of 2; P+R fixed 2 of 2 | confirmed |
| S097 | developer-html-link-fallback | product | build directory path containing ">" defeats the fallback resolution | **minor** | A '>' in the build directory path is very rare. | minor | own | GC+ disclosed | confirmed |
| S116 | developer-html-link-fallback | test | new test also searches the real installation (libtbx.env.under_root), so it fails on a machine where the API docs are built | **minor** | The test fails falsely only on machines where the API docs are built. | minor | own | P missed 1 of 2; P+R missed 1 of 2 | confirmed |
| S140 | developer-html-link-fallback | product | handler markup limits (data-href shadowing, &amp; in href, unclosed <a>, single quotes, ">" inside attribute value) | **minor** | These markup forms do not occur in the generated page. | minor | own | GC+ disclosed; P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S196 | developer-html-link-fallback | product | rebuild_phenix_api run() prints undefined fn; developer.py passes None to os.path.isfile (already in the code) | **minor** | The undefined name and None path are in error paths of a developer tool. | minor | pre | GC+ disclosed | confirmed |
| S020 | developer-page-followups | product | Windows installation on a network share (\\server\share\...): the new file URL file://server/share/... is decoded back to a relative path (server\share\...), so existing local targets fall back; base kept them | **minor** | Installing on a Windows network share is uncommon and the existing target only falls back online. | minor | own | P missed 2 of 2; P+R disclosed 1 of 2, missed 1 of 2 | confirmed |
| S035 | developer-page-followups | product | backslash in a Mac/Linux folder name kept unencoded; kept link opens a wrong path (already in the code) | **minor** | A backslash in a Mac/Linux folder name is a rare path. | minor | pre | GC+ disclosed | confirmed |
| S049 | developer-page-followups | test | real_page_install_paths asserts the real GC+ path needs no encoding, so the test fails on an installation path with a space, non-ASCII, & or + | **minor** | The test falsely fails only on installation paths with special characters. | minor | own | GC+ missed | confirmed |
| S165 | developer-page-followups | product | a file:// link with #fragment or ?query to an existing local file is treated as missing and falls back (latent: the shipped page has no such link) (already in the code) | **minor** | No shipped link carries a fragment or query, so the fallback is latent. | minor | pre | GC+ missed; P missed 2 of 2; P+R fixed 2 of 2 | confirmed |
| S024 | dock-in-map-gui-output-dir | product | command-line run that sets gui.output_dir is redirected | **minor** | A command-line run that sets the GUI-only output_dir parameter is outside normal use. | minor | own | GC+ disclosed; P missed 1 of 2; P+R missed 1 of 2 | confirmed |
| S103 | dock-in-map-gui-output-dir | product | deliberate choice of the project directory is redirected (indistinguishable from the GUI default) | **minor** | A deliberate choice of the project directory cannot be told apart from the GUI default, a rare ambiguity. | minor | own | GC+ disclosed; P disclosed 1 of 2, missed 1 of 2; P+R disclosed 2 of 2 | confirmed |
| S111 | dock-in-map-gui-output-dir | test | bug inferred from code; no GUI click-through | **minor** | No GUI click-through is a verification gap for a code-inferred bug. | minor | own | GC+ disclosed | confirmed |
| S202 | dock-in-map-gui-output-dir | product | launcher sets result.map_data_superposed, not search_map_data_superposed; map array kept in the pickle (already in the code) | **minor** | Setting the wrong attribute only leaves a map array in the pickle, making it larger. | minor | pre | GC+ disclosed; P disclosed 1 of 2, missed 1 of 2; P+R disclosed 1 of 2, missed 1 of 2 | confirmed |
| S012 | f9-f6-start-f9 | product | stray quote outside a quoted value in malformed HTML runs the tag match to the next quote | **minor** | A stray quote outside a value only arises in malformed HTML. | minor | own | GC+ disclosed | confirmed |
| S014 | f9-f6-start-f9 | test | test runs only directly, not in a suite list | **minor** | The test exists and works when run directly; it is just not in a suite list. | minor | own | GC+ disclosed | confirmed |
| S055 | f9-f6-start-f9 | product | '#' or '%' in the docs path: links are HTML-escaped but not percent-encoded, so a browser reads a fragment or an escape and opens another path (already in the code; same limit GC+ deferred) | **minor** | A '#' or '%' in the docs path is an uncommon installation path. | minor | pre | P missed 2 of 2; P+R disclosed 2 of 2 | confirmed |
| S077 | f9-f6-start-f9 | product | CHANGE origin own -> pre for the path-character part: '"', '&', '#' and '%' in the docs path already broke links at base (DOCPATH inserted raw); W1/W2/W3 present on base and GC+; plain arms fixed '"' and '&' by HTML-escaping (W1/W2 absent-handled), none fixed '#'/'%' | **minor** | The path characters that break links are uncommon in installation paths. | minor | pre | GC+ disclosed | confirmed |
| S183 | f9-f6-start-f9 | product | odd number of '"' in the docs path leaves the link unresolved | **minor** | An odd number of quote characters in the docs path is very rare. | minor | own | GC+ disclosed | confirmed |
| S188 | f9-f6-start-f9 | product | pathological input much slower (60 KB of "<a " takes 24 s) | **minor** | The slowdown needs pathological input of tens of kilobytes of "<a ". | minor | own | GC+ disclosed | confirmed |
| S019 | file-url-backslash | product | Windows, docs folder at a drive root (D:\doc): docpath 'D:' is not absolute for PureWindowsPath, the link becomes file://D%3A/... and the existing target falls back | **minor** | A docs folder at a Windows drive root is an uncommon layout and the link only falls back online. | minor | own | GC+ missed | confirmed |
| S070 | file-url-backslash | test | CHANGE kind product -> test: _url_target exists only in GC+'s test file (phenix_regression misc/tst_developer_html_links.py), not in the product code | **minor** | The helper living only in the test file means the test checks its own copy, weakening but not removing coverage. | minor | own | GC+ disclosed | confirmed |
| S095 | file-url-backslash | product | nturl2path and PurePath.as_uri deprecated in Python 3.14; also (open reader) the test helper's pathname2url may give ///path on 3.14 so href checks may fail there, not reproduced | **minor** | Python 3.14 deprecations are a future-compatibility concern. | minor | own | GC+ disclosed | confirmed |
| S117 | file-url-backslash | product | Windows extended-length installation path (\\?\C:\...): link file://%3F/... is kept as local although a browser cannot open it | **minor** | Extended-length \\?\ installation paths are very rare. | minor | own | GC+ missed; P missed 2 of 2; P+R fixed 2 of 2 | confirmed |
| S131 | file-url-backslash | test | windows_link_paths fails on old code only by TypeError | **minor** | The test fails on old code only by TypeError, which still catches the regression. | minor | own | GC+ disclosed | confirmed |
| S141 | file-url-backslash | test | no real Windows run, Python 3.14 run or browser click | **minor** | No real Windows, 3.14 or browser run is a verification gap. | minor | own | GC+ disclosed | confirmed |
| S189 | file-url-backslash | product | possible network lookup on Windows when Guided Coding is absent | **minor** | A possible network lookup on Windows without Guided Coding is a small side effect. | minor | own | GC+ disclosed; P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S027 | gc-rev15-macos-ci | product | real-tool archive check skips (does not fail) when the tools write other member contents, for every ar incl. GNU, and the skip comes before every normalizer check | **minor** | The real-tool archive check skipping instead of failing hides only the case where tools write different member contents. | minor | own | GC+ disclosed; P missed 1 of 2; P+R disclosed 1 of 2 | probable |
| S050 | gc-rev15-macos-ci | test | Apple ar layout comparison demoted to a stderr note on every Mac (GNU kept) | **minor** | The GNU ar layout check is kept, so only the Apple-specific comparison became a note. | minor | own | P missed 1 of 2; P+R disclosed 1 of 2 | confirmed |
| S072 | gc-rev15-macos-ci | test | content-change check can pass via find(b'') without testing anything | **minor** | The find(b'') vacuous pass affects one content-change check only. | minor | own | P missed 1 of 2; P+R fixed 1 of 2 | probable |
| S013 | langchain-cap-fix | product | retired Opus 4/4.1 have an 8192 SDK non-streaming cap that the 16000 floor exceeds (already in the code; comment only) | **minor** | The 8192 cap mismatch affects only retired Opus 4/4.1 models and was handled by a comment. | minor | pre | GC+ disclosed; P disclosed 2 of 2; P+R disclosed 2 of 2 | confirmed |
| S041 | langchain-cap-fix | product | non-integer max_tokens (18000.5) still sent as a float (already in the code; minor) | **minor** | A non-integer max_tokens is not a normal setting. | minor | pre | GC+ fixed; P missed 2 of 2; P+R missed 2 of 2 | confirmed |
| S109 | langchain-cap-fix | test | real API behaviour for model_context_window_exceeded not shown (no live call) | **minor** | No live call for the context-window stop reason is a verification gap. | minor | own | GC+ disclosed | confirmed |
| S067 | phenix-chat-models | test | no live chat session | **minor** | No live chat session is a verification gap, not a code error. | minor | own | GC+ disclosed | confirmed |
| S104 | phenix-chat-models | product | Fable 5.1 (claude-fable-5-1 / fable alias) not offered in the claude_code model list, though the rest of the chat code accepts fable (already in the code) | **minor** | Fable 5.1 missing from one picker list is an omission with other models still usable. | minor | pre | GC+ missed | probable |
| S128 | phenix-chat-models | product | pinned 4.x ids removed from the Claude Code picker against the documented design; a profile pinned to claude-opus-4-8 loses its entry | **minor** | Losing a pinned profile's picker entry is an inconvenience with other ids still available. | minor | own | P missed 1 of 2; P+R missed 1 of 2 | probable |
| S177 | phenix-chat-models | product | --backend anthropic without --model sends the Claude Code alias "opus" (phenix_base.json) to the Messages API, which needs a full id (already in the code) | **minor** | The alias problem needs --backend anthropic without --model and fails loudly. | major | pre | GC+ missed; P disclosed 1 of 2; P+R disclosed 1 of 2 | probable |
| S178 | phenix-chat-models | product | context limit for the haiku alias and claude-haiku-5-5 left at 200K; Haiku 5.5 has a 1M window, so context-pressure warnings come early (already in the code; minor) | **minor** | Early context-pressure warnings for Haiku 5.5 are a message issue. | minor | pre | P disclosed 2 of 2; P+R disclosed 2 of 2 | confirmed/probable |
| S023 | phenix-reply-text | product | module-level import of response_text fails against a cctbx without it (publication order) | **minor** | The import failure only occurs if phenix is published before the matching cctbx change. | minor | own | GC+ disclosed; P disclosed 2 of 2; P+R disclosed 2 of 2 | confirmed |
| S054 | phenix-reply-text | product | try/except fallback to the old extraction offered, not taken | **minor** | Not adding an optional try/except fallback is a robustness choice, not a functional error. | minor | own | GC+ disclosed | confirmed |
| S090 | phenix-reply-text | product | a failed or cut-off assessment leaves the raw template placeholder "_[LLM assessment will be inserted here]_" in the user-facing summary (already in the code for LLM errors; the fix adds cut-off replies) | **minor** | Leaving the placeholder text after a failed assessment is a message problem. | minor | pre | GC+ missed; P disclosed 1 of 2, missed 1 of 2; P+R fixed 2 of 2 | confirmed |
| S113 | phenix-reply-text | test | no live call through the three functions | **minor** | No live call through the three functions is a verification gap. | minor | own | GC+ disclosed | confirmed |
| S160 | auto-q2m-c | product | phenix rename_side_chain_atoms target put in the wrong frame once the fix moves it (result discarded) | **not-an-error** | The wrong-frame target has no effect because the result is discarded. | minor | own | GC+ disclosed | confirmed |
| S112 | file-url-backslash | product | relative Windows paths do not round-trip (not reachable: paths are absolute) | **not-an-error** | Relative Windows paths cannot reach this code because the paths are always absolute. | not-an-error | own | GC+ disclosed | confirmed |
| S137 | phenix-chat-models | product | thinking_budget > 0 would be rejected by Claude 5.x (unguarded, unused; already in the code) | **not-an-error** | The thinking_budget path is unused, so the rejection cannot occur. | minor | pre | GC+ disclosed; P disclosed 1 of 2, missed 1 of 2; P+R disclosed 1 of 2, missed 1 of 2 | confirmed |
