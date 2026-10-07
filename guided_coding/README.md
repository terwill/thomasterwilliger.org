# Guided Coding download and website generator

Keep this directory in the website repository beside `guided_workflow/`.
The generator builds a complete general edition of Guided Coding. Installation,
registration and documentation examples use
`~/Downloads/GuidedCoding/guided_coding`. Each target project keeps its own
settings; an existing working shared registration is preserved.

## Rebuild

From the website checkout, with Python 3.10+, Git, Bash and `shasum`:

```bash
python3 guided_coding/build_package.py
```

The default selects the source repository's current `master`. To use an accepted
source revision, or check without replacing site files:

```bash
python3 guided_coding/build_package.py --ref FULL_SOURCE_COMMIT
python3 guided_coding/build_package.py --check-only --ref FULL_SOURCE_COMMIT
```

The script uses the Python standard library and needs GitHub API and raw-file
access. It never stages, commits, pushes or changes your personal configuration.

## Verification and automatic adaptation

The historical source origin is recorded in `package.json` and in the documentation
index's historical note. Before executing any downloaded code, the generator checks
the Git inventory, file hashes, Git blob identities, license, required hooks and
standard-library dependencies. It freezes every file name, SHA-256 and mode,
including the manifest itself, and rejects changes after checks, tests or packaging.
A runner cannot rewrite both a file and its manifest and retain the recorded identity.

The generator first checks and tests that verified source. It then makes a separate
copy and applies `general_text()` on every build. The adaptation updates the
four user documents, local examples in the skill and procedure instructions,
and arbitrary repository names in three test fixtures. Project-specific wording is
generalized; historical record paths are labeled as relative to the original project.
The historical test-lookup observation is summarized without suggesting an unshipped
command. The adaptation changes the archive-review
example to match this ZIP's `GuidedCoding/` layout. The standalone tests replace an
unshipped repository-wrapper command. No checking-tool code, Developer–Guide Contract,
release label or general setup default is changed.

The adapted copy has its **own** `SOURCE_MANIFEST.sha256`. Its edition name,
installation root, manifest hash and exact before/after hashes are recorded under
`general_edition`; the `upstream` metadata describes historical input, not the
adapted files. Both copies are frozen and checked separately. All smoke checks and
four package test runners also run against the adapted copy. Unrecognized source-specific
references fail the build for inspection instead of leaking into the general guide.
After rendering, a second scan checks every generated HTML page, installer notes,
general developer card and maintenance README. It detects references in text and
links, including HTML character escapes. Only the exact generated source/adaptation note beside the download and
historical note in the documentation index are exempt from the source-origin check.
The exact author-affiliation link is allowed only inside the shared site header;
it is not a procedure setting. Original license and provenance records are
preserved separately. Any leftover reports its filename, fails the build and leaves
existing site outputs untouched.

Do not weaken that refusal to accommodate a new source layout without reviewing it.

The four main documentation pages are rendered from the exact adapted Markdown
shipped in the ZIP. `reference-files.html` displays the remaining 27 source files
as exact file text, using the same site header and style. All procedure references
stay on the website. Attribution appears in the source/adaptation note beside the download, the
historical note and source/license records. Original license text is retained.

App/Terminal checks use fake clients and a temporary private configuration; they
are not native app or real coding-task validation. The expected app-engine behavior
uses `CLAUDE_CODE_ENTRYPOINT=claude-desktop` and `CLAUDE_CODE_EXECPATH`. An unreadable
app engine reports `NOT CHECKED`; Terminal requires its PATH client. These are
observed interfaces, not a promised stable client API. Inspect changed interfaces
rather than weakening checks simply to make a new version pass.

## Generated outputs

All ten outputs must be reviewed and saved together:

- `guided_coding.zip`
- `guided_coding.zip.sha256`
- `package.json`
- `user-guide.html`
- `overview.html`
- `architecture.html`
- `verification.html`
- `reference-files.html`
- `documentation.html`
- `index.html`

Keep the generator, both templates, general developer card and generator tests too.
The main page keeps documentation before installation and six top jump links.
All pages use the existing site format and `.85em` inline-code size. Unsupported
Markdown blocks fail rendering for inspection; text is escaped before HTML output.

## Failed replacement and recovery

Failed downloads, source checks, adaptation or tests leave site outputs untouched.
Before replacement, every existing output is copied to disk with its hash and mode;
outputs originally absent are recorded too. New outputs are staged. The main page
is replaced last and a write lock prevents overlapping replacements.

If replacement fails, the generator attempts every restoration. Successful restoration
returns the previous bytes and modes and removes outputs originally absent. If any
restoration also fails, the outputs may be mismatched. The script retains **all**
original copies in its reported `.gc-stage-*` directory, including copies of
successfully restored files, and keeps the write lock. Read `RECOVERY.md` and
`RECOVERY.json`, resolve the filesystem error, restore all ten outputs or their
recorded absence, verify their hashes, then remove the lock before rebuilding.

This protects against caught filesystem errors. It is not an atomic multi-file
transaction or automatic recovery from a killed process or system failure. Inspect
abandoned locks and staging directories before removing them. Publish only a matching set.

## Download layout

```text
GuidedCoding/
  INSTALL.md
  GENERAL_DEVELOPER_CARD.md
  PACKAGE_INFO.json
  LICENSE.txt
  guided_coding/
    SKILL.md
    SOURCE_MANIFEST.sha256
    docs/
    payload/
    tests/
```

Keep `GuidedCoding/` in Downloads, or choose another stable location and adjust the
registration request. Do not edit or add files inside the verified `guided_coding/`
directory. Project settings and task records belong outside it.

## Generator tests

```bash
python3 -B -m unittest discover -s guided_coding/tests -v
```

The 47 methods use private temporary directories and no network. They cover source
and manifest changes, file inventory and modes, adapted-copy integrity, Downloads
and ZIP examples, local documentation links, unsupported references and rendering,
output preservation, rollback failures, recovery copies and CLI reporting. They also
check project wording, distinct fixture repositories, absolute-path controls and
the narrow site-header affiliation exception.

The live builder also executes every manifest-listed package test runner on both
copies and records counts and skips. It resolves temporary paths because macOS
temporary directories can have symbolic-link parents. Native Mac registration, a real coding task,
and browser rendering/clipboard behavior remain owner checks before publication.

ZIP entries are sorted with fixed timestamps. Test-output hashes may vary with runtime
timings, so each actual archive has its own recorded SHA-256. Review the generated
changes before committing or publishing; there is no automatic publication job.
