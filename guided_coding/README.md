# Maintaining the Guided Coding website and download

The User Guide has one maintained source: `docs/GUIDED_CODING_USER_GUIDE.md` in the kit. The builder puts that exact file in the ZIP and renders it as `getting-started.html`. Edit it in the source project, not in generated HTML. The detailed registration and command reference is a separate document, rendered at the existing `user-guide.html` URL. Its `#one-time-registration` link is retained.

The website introduction is maintained in `main-page.md`. It links to the writing prompt and Helper on Guided Workflow. Keep those links when changing the page. `index.template.html` and `docs.template.html` supply the site layout. The general setup card is optional.

## Rebuild

From the website checkout, with Python 3.10 or newer, Git, Bash and `shasum`:

```bash
python3 guided_coding/build_package.py --ref FULL_SOURCE_COMMIT
```

Without `--ref`, the builder reads the source project's current master. Prefer an accepted full commit when preparing a publication. Add `--check-only` to run the build and checks without replacing website outputs. Network access to the source hosting service is required. The script never commits, pushes, changes your personal setup or connects to project servers.

To check a documentation update before it is published in the source repository:

```bash
python3 guided_coding/build_package.py --ref FULL_BASELINE_COMMIT --source-dir /path/to/guided_coding
```

This route labels the result as a local documentation update. It compares the working source with the fetched baseline and refuses changes to tools, tests, contracts or procedure files. The one skill-file change it permits is the command-reference filename. It records the input and baseline separately; the baseline commit does not identify unpublished text changes.

## What the builder checks

Before it runs source code, the builder checks the complete inventory, manifest hashes, Git file identities, license, required entry points and dependencies. It freezes names, contents and file modes, then checks for changes after each stage. It runs the checking tools with temporary fake clients and runs all four shipped test files.

The download uses a separate copy with its own manifest and recorded before/after hashes. Local paths and manual commands are adapted there. The maintained User Guide is unchanged. The approved cloud and project section and the clearly labeled historical record retain their relevant source names; unrelated project commands elsewhere still fail the build. All download checks and tests run on that copy too.

The five documentation pages are rendered from the Markdown in the ZIP. The other source files appear as exact text in `reference-files.html`. The package metadata records the source hashes used for each page. Unsupported Markdown, missing adaptation passages or changed tool interfaces stop the build for inspection. Do not bypass a refusal just to make a new revision build.

Fake-client checks are not native Mac registration or a real coding task. Historical client observations apply only to the versions they name. Browser, live-page and download checks are separate from the build.

## Outputs and checks

Review and save the complete matching output set: the ZIP, its checksum, `package.json`, `index.html`, `getting-started.html`, `user-guide.html`, `overview.html`, `architecture.html`, `verification.html`, `documentation.html` and `reference-files.html`. Keep the builder, templates, main-page copy, setup card and tests too. Update the site map if a page is added.

Run the generator tests from the website checkout:

```bash
python3 -B -m unittest discover -s guided_coding/tests -v
```

These tests use temporary directories without network access or real credentials. The actual build records the package-test results and every skip. A skipped check is not a pass for that case.

## A failed output replacement

Downloads and checks finish before any output is replaced. The builder saves every previous output, its hash and mode, plus records of absent files. It stages the new outputs and writes the main page last. A lock prevents two output replacements at once.

If a write fails, it tries to restore every affected output. If restoration also fails, it keeps all recovery copies, `RECOVERY.md`, `RECOVERY.json` and the lock. Follow those instructions and verify the restored files or recorded absences before removing the lock or rebuilding. A stopped process or system failure can also leave unfinished work; inspect it before clearing anything. This is recovery from caught write errors, not an indivisible multi-file save.

Publish only a matching set. After publication, check the live pages, writing and Helper links, guide, command-reference anchor, and download checksum. ZIP entries use fixed timestamps, but recorded test-output hashes can vary between runs; use the checksum from the actual build.
