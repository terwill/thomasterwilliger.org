# Maintaining the Guided Coding website and download

The Guided Coding pages describe GuidedCoding from the repository `cctbx/guided_coding` (revision 22 and later: five
instruction files for Claude Code). The earlier kit, which this site described up to 2026-10-23, is retired and kept
on that repository's branch `full-kit-rev21`.

## Sources

- **Website-owned text:**
  - `main-page.md`, the main page; it keeps the "Two things matter more than any procedure" section and the link to
    the Guided Workflow Helper;
  - `pages/quick-start.md`, `pages/how-it-works.md`, `pages/why-not-claude-code.md` and
    `pages/why-not-vibe-coding.md`;
  - `pages/evidence.md`, a plain-language account of the replay results, with links to the full technical evidence.

  Their claims must match the revision the site ships. The summary reports the measured effect of individual
  checking steps, without claiming a measured improvement for the complete current procedure. One review pass
  reduced missed program errors from 0.81 to 0.47 per job in the 37-job replay; an outside review added a narrow
  benefit on selected harder jobs. Keep the selection limits and mixed findings in `pages/evidence.md`, and keep
  the full technical record linked. Introductory pages should not lead with revision numbers or internal command
  names. `pages/why-not-claude-code.md` gives the shorter comparison with plain Claude Code.
- **Website-owned downloads:** `GuidedCoding_study_final_report.md` and `GuidedCoding_study_methods.md`, copies of the
  study's final report and methods description (home paths shortened); they are committed with the site.
- **Generated from the repository:**
  - `getting-started.html`, from its `README.md`;
  - `reference-files.html`, which shows its five skill files as text;
  - `documentation.html`, a categorized index.
- **Retired pages:** `overview.html`, `architecture.html` and `user-guide.html` are short stubs pointing to the new
  pages, so that old links keep working. `user-guide.html` keeps its `#one-time-registration` anchor.
- **Layout:** `index.template.html` and `docs.template.html`.

## Reading path

The main navigation is intentionally short: Overview, Get started, How it works, and Documentation. The overview
answers why someone might want Guided Coding and offers one clear first action. Quick Start provides the one-message
installation; How it works gives the procedure; Documentation groups the manual installation, comparisons, evidence,
and exact source instructions.

The longer manual installation page still comes from the published repository README, without changing its commands.
The website adds copy buttons for those command blocks. The evidence summary is website-owned prose with direct
links to the full study and the published technical record. The five instruction files remain generated from the
exact published revision. The comparison and older URLs remain available even though they are not in the main
navigation.

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
