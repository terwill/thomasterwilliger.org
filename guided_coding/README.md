# Maintaining the Guided Coding website and download

The Guided Coding pages describe GuidedCoding from the repository `cctbx/guided_coding` (revision 22 and later: five
instruction files for Claude Code). The earlier kit, which this site described up to 2026-10-23, is retired and kept
on that repository's branch `full-kit-rev21`.

## Sources

- **Website-owned text:**
  - `main-page.md`, the main page; it keeps the "Two things matter more than any procedure" section and the link to
    the Guided Workflow Helper;
  - `pages/quick-start.md`, `pages/how-it-works.md`, `pages/why-not-claude-code.md` and
    `pages/why-not-vibe-coding.md`.

  Their claims must match the revision the site ships. The evidence wording is fixed (version 1.4): one review pass after
  plain Claude Code cut missed program errors per job from 0.81 to 0.47; on 18 harder jobs (selected, not a random
  sample) an outside review removed further major errors when added to GuidedCoding, narrowly; a second review pass
  showed no clear additional benefit; the strict scope rule probably cost errors (estimated, not tested); GuidedCoding
  1.4 as a whole has not itself been measured. `pages/why-not-claude-code.md` holds the study summary.
- **Website-owned downloads:** `GuidedCoding_study_final_report.md` and `GuidedCoding_study_methods.md`, copies of the
  study's final report and methods description (home paths shortened); they are committed with the site.
- **Generated from the repository:**
  - `getting-started.html`, from its `README.md`;
  - `verification.html`, from its `EVIDENCE.md`;
  - `reference-files.html`, which shows its five skill files as text;
  - `documentation.html`, an index.
- **Retired pages:** `overview.html`, `architecture.html` and `user-guide.html` are short stubs pointing to the new
  pages, so that old links keep working. `user-guide.html` keeps its `#one-time-registration` anchor.
- **Layout:** `index.template.html` and `docs.template.html`.

## Rebuild

From the website checkout, with Python 3.10 or newer and Git:

```bash
python3 guided_coding/build_site.py --ref FULL_COMMIT
```

`FULL_COMMIT` is the published `cctbx/guided_coding` commit. Add `--source-dir /path/to/guided_coding` to read it
from a local clone instead of fetching it, and `--check-only` to build and check without replacing anything.

**What the builder does:**
1. It runs the repository's own `tst_guided_coding.py`.
2. It renders the pages, builds `guided_coding.zip` with fixed timestamps, and writes its checksum and
   `package.json` (the source commit and the hashes of every file and page).
3. It checks that every relative link and anchor resolves.
4. Only then does it replace the outputs, keeping the previous ones in `guided_coding/.previous/`.

It never commits or pushes. It refuses a commit that is not on the source's origin/master. Its Markdown renderer
supports a small subset (headings, paragraphs, lists, fenced code, tables, block quotes, code spans, links, `**` and
`*`). It refuses the forms it knows it cannot render, such as underscore emphasis, autolinks and HTML entities. Still,
look at each changed page in a preview.

## Tests

```bash
python3 -B -m unittest discover -s guided_coding/tests -v
```

The tests use temporary folders, no network, and a small fake source repository.

## Publishing

Publish only a matching set of outputs. After publication, check:
- the live pages;
- the download checksum against `guided_coding.zip.sha256`;
- the Guided Workflow Helper links.
