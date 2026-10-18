# Maintaining the Guided Coding website and download

The User Guide has one maintained source: `docs/GUIDED_CODING_USER_GUIDE.md` in the kit. The builder puts that exact file in the ZIP and renders it as `getting-started.html`. Edit it in the source project, not in generated HTML. The detailed registration and command reference is a separate document, rendered at the existing `user-guide.html` URL. Its `#one-time-registration` link is retained.

The website introduction is maintained in `main-page.md`. It links to the Helper on Guided Workflow. Keep that link when changing the page. Four more website pages are maintained as Markdown in `pages/`: Quick Start, How Guided Coding works and the two "Why Guided Coding" pages. The builder renders them with the documentation layout; they may link to other website pages by file name, and Quick Start's ```copy block gets a copy button. Their claims about the kit must match the documentation of the kit revision the site ships (see package.json); recheck them at each rebuild from a new revision. The writing prompt belongs on Guided Workflow. `index.template.html` and `docs.template.html` supply the site layout. The general setup card is optional.

## Rebuild

From the website checkout, with Python 3.10 or newer, Git, Bash and `shasum`:

```bash
python3 guided_coding/build_package.py --ref FULL_SOURCE_COMMIT
```

Run it with a Python that has psutil (since kit revision 16 the auto-mode tests need it; without it they are skipped, and the build records the skips). Without `--ref`, the builder reads the source project's current master. Prefer an accepted full commit when preparing a publication. Add `--check-only` to run the build and checks without replacing website outputs. Network access to the source hosting service is required. The script never commits, pushes, changes your personal setup or connects to project servers.

To check a documentation update before it is published in the source repository:

```bash
python3 guided_coding/build_package.py --ref FULL_BASELINE_COMMIT --source-dir /path/to/guided_coding
```

This route labels the result as a local documentation update. It compares the working source with the fetched baseline and refuses changes to tools, tests, contracts or procedure files. The one skill-file change it permits is the command-reference filename. It records the input and baseline separately; the baseline commit does not identify unpublished text changes.

## What the builder checks

Before it runs source code, the builder checks the complete inventory, manifest hashes, Git file identities, license, required entry points and dependencies. It also checks that the skill's guarded block is exactly the kit's (from kit revision 13: the listed hashes with `shasum`, or `sha256sum` where it is missing, then the downloaded checker, then the release check) and that the skill runs the checker nowhere else. It freezes names, contents and file modes, then checks for changes after each stage. It runs the checking tools with temporary fake clients and runs every shipped test file.

The download uses a separate copy with its own manifest and recorded before/after hashes. Local paths and manual commands are adapted there. Since kit revision 16 the kit names its build's conda Python, `libtbx.python`, in its commands. Kit revision 18 lets any Python 3.10 or newer serve and tells download readers to make a virtual environment with psutil (`~/guided_coding_venv`), so the download's commands name `~/guided_coding_venv/bin/python`; the kit's exact passages about the conda Python get general wording or are dropped. The overview's section "Where Guided Coding is included", which names the other software that includes Guided Coding and which the User Guide links to, ships exactly as approved: the build requires that exact text once, and scans everything around it like any other text. The reference-files page shows the unchanged `auto_queue.py`, `payload/tools/screen_check.py` and `payload/RELEASE` exactly as shipped, including the source names in them; any other file naming the source project still stops the build. Shell-neutral `env` command lines (kit revision 13 and later, also for csh) resolve `TMPDIR` in the same shell-neutral form the kit uses, which sets it to the resolved `/tmp` rather than your own `TMPDIR`; other commands keep the bash prefix. The verification page's historical record keeps the commands it records. A test that compares a tool's exact message keeps quoting it, because the tools ship unchanged. The maintained User Guide is unchanged. The approved cloud and project section and the clearly labeled historical record retain their relevant source names; unrelated project commands elsewhere still fail the build. All download checks and tests run on that copy too.

The five documentation pages are rendered from the Markdown in the ZIP. The other source files appear as exact text in `reference-files.html`. The package metadata records the source hashes used for each page. Unsupported Markdown, missing adaptation passages or changed tool interfaces stop the build for inspection. Do not bypass a refusal just to make a new revision build.

Fake-client checks are not native Mac registration or a real coding task. Historical client observations apply only to the versions they name. Browser, live-page and download checks are separate from the build.

## Outputs and checks

Review and save the complete matching output set: the ZIP, its checksum, `package.json`, `index.html`, `getting-started.html`, `user-guide.html`, `overview.html`, `architecture.html`, `verification.html`, `documentation.html`, `reference-files.html`, `quick-start.html`, `how-it-works.html`, `why-not-claude-code.html` and `why-not-vibe-coding.html`. Keep the builder, templates, main-page copy, `pages/` sources, setup card and tests too. Update the site map if a page is added.

Run the generator tests from the website checkout:

```bash
python3 -B -m unittest discover -s guided_coding/tests -v
```

These tests use temporary directories without network access or real credentials. The actual build records the package-test results and every skip. A skipped check is not a pass for that case.

## A failed output replacement

Downloads and checks finish before any output is replaced. The builder saves every previous output, its hash and mode, plus records of absent files. It stages the new outputs and writes the main page last. A lock prevents two output replacements at once.

If a write fails, it tries to restore every affected output. If restoration also fails, it keeps all recovery copies, `RECOVERY.md`, `RECOVERY.json` and the lock. Follow those instructions and verify the restored files or recorded absences before removing the lock or rebuilding. A stopped process or system failure can also leave unfinished work; inspect it before clearing anything. This is recovery from caught write errors, not an indivisible multi-file save.

Publish only a matching set. After publication, check the live pages, Helper links, guide, command-reference anchor, and download checksum. Check the writing prompt on Guided Workflow. ZIP entries use fixed timestamps, but recorded test-output hashes can vary between runs; use the checksum from the actual build.
