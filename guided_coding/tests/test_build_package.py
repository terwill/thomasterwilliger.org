"""Downstream packaging controls. No network, credentials or user configuration."""

import hashlib
import html
from html.parser import HTMLParser
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch
import zipfile

SCRIPT = Path(__file__).resolve().parents[1] / "build_package.py"
SPEC = importlib.util.spec_from_file_location("gc_site_packager", SCRIPT)
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)

DOC_CLARIFICATIONS = {
    "docs/GUIDED_CODING_README.md": (
        "`enumcheck-20261002T194333Z` was published to `cctbx_project` on\n"
        "2026-10-02 (commit `c36887c7f489018af4f91773246ecde32d1b4e24`), and its\n"
        "documentation revision `docs-20261003` on 2026-10-03 (commit\n"
        "`b0747a4a55f29db3abe04358480d5867e94cb792`).",
        "`enumcheck-20261002T194333Z` was published in the original upstream source repository on\n"
        "2026-10-02 (upstream commit `c36887c7f489018af4f91773246ecde32d1b4e24`), and its\n"
        "documentation revision `docs-20261003` on 2026-10-03 (upstream commit\n"
        "`b0747a4a55f29db3abe04358480d5867e94cb792`)."),
    "docs/GUIDED_CODING_VERIFICATION.md": (
        "The skill entry `SKILL.md`, whose session-title instructions these observations exercised, "
        "is byte-identical between that revision and the published one;",
        "The skill entry `SKILL.md`, whose session-title instructions these observations exercised, "
        "is byte-identical between that revision and the published upstream revision; "
        "this edition's copy differs from its pinned upstream source only in its example source path and temporary-directory handling, "
        "not in the session-title instructions;"),
    "docs/GUIDED_CODING_ARCHITECTURE.md": (
        "The personal link exposes the current central checkout, not a pinned\n"
        "release. Updating that checkout therefore needs coordination with active\n"
        "work and the repository's integration rules.",
        "The personal link exposes the current central source directory, not a pinned\n"
        "release. Replacing that directory therefore needs coordination with active\n"
        "work; follow the update steps in INSTALL.md."),
}


def manifest(files):
    return "".join(f"{hashlib.sha256(data).hexdigest()}  ./{name}\n"
                   for name, data in sorted(files.items())).encode()


SITE_INPUTS = ("index.template.html", "docs.template.html", "main-page.md", "GENERAL_DEVELOPER_CARD.md",
               *(page[0] for page in builder.SITE_PAGES))


def copy_site_inputs(site):
    for name in SITE_INPUTS:
        (site / name).parent.mkdir(parents=True, exist_ok=True)
        (site / name).write_bytes((SCRIPT.parent / name).read_bytes())

REFERENCE = 'docs/GUIDED_CODING_COMMAND_REFERENCE.md'
REFERENCE_HEADER = '# Guided Coding registration and command reference\n\n## One-time registration\n\n'


def temp_fixture(name):
    """Minimal source prose containing every guarded upstream instruction."""
    text = REFERENCE_HEADER if name == REFERENCE else builder.TEMP_HEADERS[name] + '\n\n'
    for command, count in builder.TEMP_COMMANDS.get(name, ()):
        for _ in range(count):
            text += (command + '\n\n' if command.startswith('`') else
                     '```bash\n' + command + '```\n\n')
    return text.encode()


class PackagingControls(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.source = self.root / "source"
        self.source.mkdir()
        self.write_source({"SKILL.md": b"original skill\n", "payload/RELEASE": b"test release\n"})

    def write_source(self, files):
        for path in sorted(self.source.rglob("*"), reverse=True):
            if path.is_file() or path.is_symlink():
                path.unlink()
            elif path.is_dir():
                path.rmdir()
        for name, data in files.items():
            path = self.source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        (self.source / "SOURCE_MANIFEST.sha256").write_bytes(manifest(files))

    def test_manifest_refuses_traversal_duplicate_absolute_and_control_paths(self):
        sha = "a" * 64
        for name in ("../outside", "/absolute", "a/../b", "a//b", "a\\b", "a:b", "a\tfile"):
            with self.subTest(name=name), self.assertRaises(builder.PackageError):
                builder.parse_manifest(f"{sha}  ./{name}\n".encode())
        with self.assertRaises(builder.PackageError):
            builder.parse_manifest((f"{sha}  ./same\n" * 2).encode())

    def test_inventory_refuses_missing_extra_and_upstream_unlisted_files(self):
        names = {"SKILL.md", "payload/RELEASE", "SOURCE_MANIFEST.sha256"}
        builder.validate_source(self.source, names)
        with self.assertRaises(builder.PackageError):
            builder.validate_source(self.source, names | {"new-hook.py"})
        (self.source / "extra").write_text("unlisted")
        with self.assertRaises(builder.PackageError):
            builder.validate_source(self.source)
        (self.source / "extra").unlink()
        (self.source / "SKILL.md").unlink()
        with self.assertRaises(builder.PackageError):
            builder.validate_source(self.source)

    def test_checksum_failure_stops_before_any_downloaded_checker_runs(self):
        marker = self.root / "executed"
        poison = ("from pathlib import Path\nPath(" + repr(str(marker)) + ").write_text('ran')\n").encode()
        self.write_source({"SKILL.md": b"unchanged\n", "payload/tools/screen_check.py": poison})
        (self.source / "payload/tools/screen_check.py").write_bytes(poison + b"# changed\n")
        with patch.object(builder, "run_contract_checks") as execute:
            with self.assertRaises(builder.PackageError):
                builder.build_artifacts(self.source, {}, b"license", self.root, self.root)
            execute.assert_not_called()
        self.assertFalse(marker.exists())

    def test_symlink_and_hardlinked_files_refused(self):
        original = self.source / "SKILL.md"
        data = original.read_bytes()
        external = self.root / "external"
        external.write_bytes(data)
        original.unlink()
        original.symlink_to(external)
        with self.assertRaises(builder.PackageError):
            builder.validate_source(self.source)
        original.unlink()
        os.link(external, original)
        with self.assertRaises(builder.PackageError):
            builder.validate_source(self.source)

    def test_missing_required_hooks_refused_before_execution(self):
        with patch.object(builder, "run_contract_checks") as execute:
            with self.assertRaisesRegex(builder.PackageError, "required package files missing"):
                builder.build_artifacts(self.source, {}, b"license", self.root, self.root)
            execute.assert_not_called()

    def test_network_source_inventory_is_checked_before_file_downloads(self):
        fake_commit = {"sha": "a" * 40, "commit": {"tree": {"sha": "b" * 40}}}
        trees = [[{"path": "libtbx", "type": "tree", "sha": "c" * 40}],
                 [{"path": "guided_coding", "type": "tree", "sha": "d" * 40}],
                 [{"path": "SOURCE_MANIFEST.sha256", "type": "blob", "mode": "100644", "sha": "e" * 40},
                  {"path": "SKILL.md", "type": "blob", "mode": "100644", "sha": "f" * 40},
                  {"path": "unlisted.py", "type": "blob", "mode": "100644", "sha": "1" * 40}]]
        destination = self.root / "fetched"
        with patch.object(builder, "api", return_value=fake_commit), \
             patch.object(builder, "tree", side_effect=trees), \
             patch.object(builder, "fetch", return_value=manifest({"SKILL.md": b"skill"})) as fetch:
            with self.assertRaisesRegex(builder.PackageError, "upstream file inventory differs"):
                builder.download_source("master", destination)
            self.assertEqual(fetch.call_count, 1)
        self.assertFalse(destination.exists())

    def test_zip_preserves_core_bytes_and_keeps_additions_outside_core(self):
        core = {p.relative_to(self.source).as_posix(): p.read_bytes()
                for p in self.source.rglob("*") if p.is_file()}
        extras = {"INSTALL.md": b"distribution notes\n", "LICENSE.cctbx.txt": b"license\n"}
        data = builder.make_zip(self.source, extras)
        self.assertEqual(data, builder.make_zip(self.source, extras))
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            self.assertEqual(set(archive.namelist()),
                             {"GuidedCoding/guided_coding/" + x for x in core}
                             | {"GuidedCoding/" + x for x in extras})
            for name, original in core.items():
                self.assertEqual(archive.read("GuidedCoding/guided_coding/" + name), original)
            unpack = self.root / "unpack"
            archive.extractall(unpack)
        builder.validate_source(unpack / "GuidedCoding/guided_coding")

    def test_changed_template_refuses_and_inserted_text_is_escaped(self):
        result = builder.render_page('<textarea>@@MESSAGE@@</textarea>', {"MESSAGE": "</textarea><script>"})
        self.assertIn(b"&lt;/textarea&gt;&lt;script&gt;", result)
        for values in ({}, {"MESSAGE": "ok", "EXTRA": "unused"}):
            with self.assertRaises(builder.PackageError):
                builder.render_page("@@MESSAGE@@", values)
        values = {x: "value" for x in re.findall(r"@@([A-Z_]+)@@",
                     (SCRIPT.parent / "index.template.html").read_text())}
        rendered = builder.render_page((SCRIPT.parent / "index.template.html").read_text(), values)
        self.assertNotIn(b"@@", rendered)

    def test_zip_preserves_an_upstream_executable_bit(self):
        (self.source / "SKILL.md").chmod(0o755)
        with zipfile.ZipFile(io.BytesIO(builder.make_zip(self.source, {}))) as archive:
            item = archive.getinfo("GuidedCoding/guided_coding/SKILL.md")
            self.assertEqual((item.external_attr >> 16) & 0o777, 0o755)

    def make_site_outputs(self):
        site = self.root / "site"
        site.mkdir()
        old = {name: ("OLD " + name).encode() for name in builder.OUTPUTS}
        for name, data in old.items():
            (site / name).write_bytes(data)
        return site, old

    def build_fixture(self):
        site, old = self.make_site_outputs()
        copy_site_inputs(site)
        files = {p.relative_to(self.source).as_posix(): p.read_bytes()
                 for p in self.source.rglob("*") if p.is_file() and p.name != "SOURCE_MANIFEST.sha256"}
        files.update({name: temp_fixture(name) for name in builder.TEMP_HEADERS})
        files[REFERENCE] = temp_fixture(REFERENCE)
        files['payload/tools/check.py'] = b'# immutable tool sentinel\n'
        files['tests/tst_example.py'] = b'# immutable test sentinel\n'
        for name, (before, _) in DOC_CLARIFICATIONS.items():
            files[name] += ("\n" + before + "\n").encode()
        self.write_source(files)
        info = {"commit": "a" * 40, "commit_date": "2026-10-06T20:03:57Z",
                "source_manifest_sha256": builder.digest(
                    (self.source / "SOURCE_MANIFEST.sha256").read_bytes()),
                "source_files": len(files) + 1, "license_sha256": builder.digest(b"license")}
        return site, old, info


    def test_shared_user_guide_is_identical_in_input_download_and_web_source(self):
        site, old, info = self.build_fixture()
        guide = ('# Guided Coding User Guide\n\n' + builder.CLOUD_SECTION +
                 '\n## Publication\n\nOutside review cannot be skipped in this version.\n').encode()
        files = {p.relative_to(self.source).as_posix(): p.read_bytes()
                 for p in self.source.rglob('*') if p.is_file() and p.name != 'SOURCE_MANIFEST.sha256'}
        files['docs/GUIDED_CODING_USER_GUIDE.md'] = guide
        self.write_source(files)
        info['source_manifest_sha256'] = builder.digest((self.source / 'SOURCE_MANIFEST.sha256').read_bytes())
        with patch.object(builder, 'check_hooks', return_value=(2, 1, 281)), \
             patch.object(builder, 'run_contract_checks', return_value={}), \
             patch.object(builder, 'run_package_tests', return_value=[]):
            outputs = builder.build_artifacts(self.source, info, b'license', site, self.root)
        with zipfile.ZipFile(io.BytesIO(outputs['guided_coding.zip'])) as archive:
            self.assertEqual(archive.read('GuidedCoding/guided_coding/docs/GUIDED_CODING_USER_GUIDE.md'), guide)
            self.assertIn('GuidedCoding/guided_coding/docs/GUIDED_CODING_COMMAND_REFERENCE.md', archive.namelist())
        metadata = json.loads(outputs['package.json'])
        record = next(x for x in metadata['documentation']['pages'] if x['page'] == 'getting-started.html')
        self.assertEqual(record['source_sha256'], builder.digest(guide))
        self.assertIn(b'Outside review cannot be skipped', outputs['getting-started.html'])
        self.assertIn(b'id="one-time-registration"', outputs['user-guide.html'])
        self.assertEqual((self.source / 'docs/GUIDED_CODING_USER_GUIDE.md').read_bytes(), guide)

    def test_cloud_exception_does_not_allow_project_commands_elsewhere(self):
        guide = '# Guided Coding User Guide\n\n' + builder.CLOUD_SECTION
        self.assertEqual(builder.general_text('docs/GUIDED_CODING_USER_GUIDE.md', guide), guide)
        with self.assertRaisesRegex(builder.PackageError, 'unadapted'):
            builder.general_text('docs/GUIDED_CODING_USER_GUIDE.md', guide + '\nRun phenix.private_command here.\n')
        with self.assertRaisesRegex(builder.PackageError, 'approved cloud'):
            builder.general_text('docs/GUIDED_CODING_USER_GUIDE.md', guide.replace('phenix.developer', 'phenix.private_command'))

    def test_local_preview_refuses_changed_tool_even_with_regenerated_manifest(self):
        baseline = self.root / 'baseline'
        baseline.mkdir()
        contents = {'SKILL.md': b'read docs/GUIDED_CODING_USER_GUIDE.md\n',
                    'payload/tools/check.py': b'original tool\n'}
        for name, data in contents.items():
            path = baseline / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        (baseline / 'SOURCE_MANIFEST.sha256').write_bytes(manifest(contents))
        self.write_source({**contents, 'payload/tools/check.py': b'changed tool\n'})
        with self.assertRaisesRegex(builder.PackageError, 'executable or procedure'):
            builder.prepare_local_documentation(self.source, baseline,
                {'source_manifest_sha256': builder.digest((baseline / 'SOURCE_MANIFEST.sha256').read_bytes())},
                self.root / 'candidate')
        self.assertFalse((self.root / 'candidate').exists())

    def test_documentation_preserves_examples_and_keeps_references_local(self):
        info = {"commit": "a" * 40}
        markdown = '''# Example guide

## Source and target

Use **`/guided_coding`** and [the checks](GUIDED_CODING_VERIFICATION.md#release-and-source-checks).
Read [setup](../payload/SETUP.md#5-save-a-usable-method-and-a-recoverable-change).
Also read [the checker](../payload/tools/screen_check.py).

1. Preserve this choice,
   including its explanation.
2. Check it.

| Setting | Meaning |
| --- | --- |
| `TARGET` | Keep <literal> text. |

```bash
cd "$HOME/GuidedCoding" &&
printf '<script> & untouched\\n'
```
'''
        rendered, toc = builder.render_document(markdown, info)
        self.assertIn('href="verification.html#release-and-source-checks"', rendered)
        self.assertIn('href="reference-files.html#file-payload-setup-md"', rendered)
        self.assertIn('href="reference-files.html#file-payload-tools-screen-check-py"', rendered)
        self.assertNotIn('github.com', rendered)
        self.assertIn('href="#source-and-target"', toc)
        self.assertIn('<strong><code>/guided_coding</code></strong>', rendered)
        self.assertIn('Preserve this choice, including its explanation.', rendered)
        self.assertNotIn('<literal>', rendered)

        class Code(HTMLParser):
            def __init__(self):
                super().__init__()
                self.in_pre = False
                self.text = ''
            def handle_starttag(self, tag, attrs):
                if tag == 'pre':
                    self.in_pre = True
            def handle_endtag(self, tag):
                if tag == 'pre':
                    self.in_pre = False
            def handle_data(self, text):
                if self.in_pre:
                    self.text += text

        parsed = Code()
        parsed.feed(rendered)
        self.assertEqual(parsed.text, markdown.split('```bash\n')[1].split('```')[0])
        with self.assertRaisesRegex(builder.PackageError, 'unsupported documentation link'):
            builder.render_document('# Title\n\n[bad](javascript:alert)\n', info)
        with self.assertRaisesRegex(builder.PackageError, 'unsupported documentation block'):
            builder.render_document('# Title\n\n> Unsupported quote\n', info)
        with self.assertRaises(builder.PackageError):
            builder.documentation_link('../../tst_guided_coding.py', info)
        with self.assertRaisesRegex(builder.PackageError, 'source-history links'):
            builder.documentation_link('https://github.com/cctbx/cctbx_project/tree/master', info)

    def test_general_paths_and_zip_review_examples_are_adapted_during_each_build(self):
        example = '''# Guide
`cctbx_project/libtbx/guided_coding/`
cd /absolute/path/to/cctbx_project/libtbx/guided_coding &&
cd /path/to/cctbx_project/libtbx/guided_coding &&
cd /absolute/path/to/libtbx/guided_coding &&
mkdir /path/to/empty-gc-review &&
tar -xzf /path/to/reviewed-guided-coding.tgz -C /path/to/empty-gc-review &&
cd /path/to/empty-gc-review/libtbx/guided_coding &&
'''
        adapted = builder.general_text('docs/GUIDED_CODING_USER_GUIDE.md', example)
        self.assertNotRegex(adapted, r'cctbx|libtbx|absolute/path|\.tgz')
        self.assertIn('unzip ~/Downloads/guided_coding.zip', adapted)
        self.assertIn('cd ~/Downloads/guided_coding_review/GuidedCoding/guided_coding', adapted)
        self.assertEqual(adapted.count(builder.INSTALL_ROOT), 4)
        self.assertEqual(builder.general_text('docs/GUIDED_CODING_USER_GUIDE.md', adapted), adapted)

    def test_general_edition_has_separate_manifest_and_preserves_original_and_modes(self):
        self.write_source({'SKILL.md': temp_fixture('SKILL.md') + b'cd /absolute/path/to/libtbx/guided_coding &&\n',
                           'payload/RELEASE': b'test release\n',
                           'payload/tools/check.py': b'print("unchanged tool")\n',
                           'tests/tst_example.py': b'repository = "cctbx"\n'})
        (self.source / 'SKILL.md').chmod(0o755)
        original = builder.source_snapshot(self.source)
        destination = self.root / 'edition'
        edition = builder.general_source(self.source, destination)
        builder.require_unchanged_source(self.source, original)
        builder.validate_source(destination)
        self.assertNotEqual(edition['source_manifest_sha256'], original['SOURCE_MANIFEST.sha256'][0])
        self.assertEqual((destination / 'SKILL.md').stat().st_mode & 0o777, 0o755)
        self.assertEqual((destination / 'payload/tools/check.py').read_bytes(),
                         (self.source / 'payload/tools/check.py').read_bytes())
        self.assertEqual({x['file'] for x in edition['adapted_files']}, {'SKILL.md', 'tests/tst_example.py'})
        for record in edition['adapted_files']:
            self.assertEqual(record['original_sha256'], builder.digest((self.source / record['file']).read_bytes()))
            self.assertEqual(record['packaged_sha256'], builder.digest((destination / record['file']).read_bytes()))

    def test_unrecognized_source_specific_reference_refuses_instead_of_shipping_it(self):
        for text in ('# Title\nUse cctbx.something here.\n', '# Title\ncd /absolute/path/to/new_layout\n',
                     '# Title\ncd /unknown/prefix/cctbx_project/libtbx/guided_coding\n',
                     '# Title\nUse PhEnIx.something here.\n'):
            with self.subTest(text=text), self.assertRaisesRegex(builder.PackageError, 'unadapted'):
                builder.general_text('docs/new.md', text)

    def test_three_required_documentation_clarifications_apply_exactly(self):
        for name, (before, after) in DOC_CLARIFICATIONS.items():
            with self.subTest(name=name):
                text = 'Unchanged text before.\n\n' + before + '\n\nUnchanged text after.\n'
                adapted = builder.general_text(name, text)
                self.assertEqual(adapted, text.replace(before, after, 1))
                self.assertIsNone(builder.GENERAL_REFERENCE.search(adapted))

    def test_changed_missing_or_duplicated_required_passage_stops_build_and_preserves_inputs_and_outputs(self):
        site, old, info = self.build_fixture()
        originals = {p.relative_to(self.source).as_posix(): p.read_bytes()
                     for p in self.source.rglob('*') if p.is_file() and p.name != 'SOURCE_MANIFEST.sha256'}
        for name, (before, _) in DOC_CLARIFICATIONS.items():
            changed = before.replace('published', 'released', 1)
            if changed == before:
                changed = before.replace('current central checkout', 'current central directory', 1)
            self.assertNotEqual(changed, before)
            for replacement in (changed, '', before + '\n\n' + before):
                with self.subTest(name=name, replacement=replacement), \
                     tempfile.TemporaryDirectory(dir=self.root) as scratch:
                    files = dict(originals)
                    files[name] = files[name].decode().replace(before, replacement, 1).encode()
                    self.write_source(files)
                    info['source_manifest_sha256'] = builder.digest((self.source / 'SOURCE_MANIFEST.sha256').read_bytes())
                    frozen = builder.source_snapshot(self.source)
                    with patch.object(builder, 'check_hooks', return_value=(2, 1, 281)), \
                         patch.object(builder, 'run_contract_checks', return_value={}), \
                         patch.object(builder, 'run_package_tests', return_value=[]), \
                         patch.object(builder, 'make_zip', wraps=builder.make_zip) as make_zip, \
                         patch.object(builder, 'publish_local') as publish:
                        with self.assertRaisesRegex(builder.PackageError,
                                'required general-edition passage missing or duplicated; inspect ' + re.escape(name)):
                            builder.build_artifacts(self.source, info, b'license', site, Path(scratch))
                        make_zip.assert_not_called()
                        publish.assert_not_called()
                    builder.require_unchanged_source(self.source, frozen)
                    self.assertEqual(old, {n: (site / n).read_bytes() for n in old})

    def test_project_specific_passages_are_adapted_without_rewriting_history(self):
        overview = builder.general_text('docs/GUIDED_CODING_README.md',
            "The full PHENIX server suite was **not run for this GC-only publication**;\n"
            "the Developer explicitly waived it for that pilot.\n"
            "The package supplies general setup defaults and a method template. It\n"
            "contains no personal PHENIX profile, account, server requirement or `t96`\n"
            "definition. An optional project defaults card can be supplied separately;\n"
            "another developer adapts its paths and permissions to their own environment.\n" +
            DOC_CLARIFICATIONS['docs/GUIDED_CODING_README.md'][0])
        self.assertIn("original project's full server test suite", overview)
        self.assertIn('**not run for this GC-only publication**', overview)
        self.assertIn('explicitly waived it for that pilot', overview)
        self.assertNotIn('t96', overview)
        verification = builder.general_text('docs/GUIDED_CODING_VERIFICATION.md',
            "Records (`phenix/.claude/records/2026-10-04-gc-followups-A/`), not in this file.\n"
            "| PHENIX test discovery (A7, 2026-10-04) | `phenix.find_program search_type=tests "
            "search_text=<function> tests.search_tests_by=function_called` traced `run_autobuild` to "
            "its calling tests; the default mode matched test names; a function newer than the static "
            "index (dated 2026-05-06) produced no entry and no message; `git_affected_tests=True` saw "
            "only uncommitted modifications in the three module directories. Project guidance, "
            "not a package feature. |\n"
            "The full PHENIX server suite was **NOT RUN** under a specific waiver.\n" +
            DOC_CLARIFICATIONS['docs/GUIDED_CODING_VERIFICATION.md'][0])
        self.assertIn("original project's `.claude/records/2026-10-04-gc-followups-A/`", verification)
        self.assertNotIn('Downloads', verification)
        self.assertNotIn('find_program', verification)
        self.assertIn('static index (dated 2026-05-06)', verification)
        self.assertIn('only uncommitted modifications', verification)
        self.assertIn('not included in the general kit', verification)
        self.assertIn('**NOT RUN** under a specific waiver', verification)
        setup = builder.general_text('payload/SETUP.md',
            'Do not introduce PHENIX, named hosts, or suite shorthand into an unrelated\n'
            'project. If no task is requested, complete setup and stop.')
        self.assertIn("another project's commands", setup)
        self.assertIn('If no task is requested, complete setup and stop.', setup)

    def test_example_repository_renames_preserve_distinct_names_and_absolute_path_controls(self):
        fixture = ('repositories = ["phenix", "cctbx"]\n'
                   'remote = "ssh://example.invalid/phenix.git"\n'
                   'invalid_name = "/Users/dev/unix/PHENIX/modules/phenix"\n')
        adapted = builder.general_text('tests/tst_example.py', fixture)
        self.assertIn('["example_project", "companion"]', adapted)
        self.assertIn('ssh://example.invalid/example_project.git', adapted)
        self.assertIn('"/Users/dev/Downloads/example_project"', adapted)
        self.assertNotRegex(adapted, r'(?i)phenix|cctbx')
        self.assertEqual(builder.general_text('tests/tst_example.py', adapted), adapted)

    def test_general_edition_runner_cannot_change_source_and_regenerate_manifest(self):
        site, old, info = self.build_fixture()
        def runner(source, scratch):
            if source.name == 'general-edition':
                (source / 'SKILL.md').write_bytes(b'changed general edition\n')
                files = {p.relative_to(source).as_posix(): p.read_bytes()
                         for p in source.rglob('*') if p.is_file() and p.name != 'SOURCE_MANIFEST.sha256'}
                (source / 'SOURCE_MANIFEST.sha256').write_bytes(manifest(files))
                builder.validate_source(source)
            return []
        with patch.object(builder, 'check_hooks', return_value=(2, 1, 281)), \
             patch.object(builder, 'run_contract_checks', return_value={}), \
             patch.object(builder, 'run_package_tests', side_effect=runner):
            with self.assertRaisesRegex(builder.PackageError, 'source changed'):
                builder.build_artifacts(self.source, info, b'license', site, self.root)
        self.assertEqual(old, {n: (site / n).read_bytes() for n in old})

    def test_package_guide_and_installation_share_downloads_path_and_registration(self):
        site, old, info = self.build_fixture()
        files = {p.relative_to(self.source).as_posix(): p.read_bytes()
                 for p in self.source.rglob('*') if p.is_file() and p.name != 'SOURCE_MANIFEST.sha256'}
        files['docs/GUIDED_CODING_USER_GUIDE.md'] = (
            temp_fixture('docs/GUIDED_CODING_USER_GUIDE.md').decode() + '\n```text\nPlease set up GuidedCoding from /absolute/path/to/cctbx_project/libtbx/guided_coding for this machine.\n```\n').encode()
        self.write_source(files)
        info['source_manifest_sha256'] = builder.digest((self.source / 'SOURCE_MANIFEST.sha256').read_bytes())
        with patch.object(builder, 'check_hooks', return_value=(2, 1, 281)), \
             patch.object(builder, 'run_contract_checks', return_value={}), \
             patch.object(builder, 'run_package_tests', return_value=[]):
            outputs = builder.build_artifacts(self.source, info, b'license', site, self.root)
        with zipfile.ZipFile(io.BytesIO(outputs['guided_coding.zip'])) as archive:
            guide = archive.read('GuidedCoding/guided_coding/docs/GUIDED_CODING_USER_GUIDE.md').decode()
            install = archive.read('GuidedCoding/INSTALL.md').decode()
            metadata = json.loads(archive.read('GuidedCoding/PACKAGE_INFO.json'))
            self.assertIn(builder.REGISTRATION, guide)
            self.assertIn(builder.REGISTRATION, install)
            self.assertIn(builder.REGISTRATION + '\n\n' + builder.SAME_CONVERSATION + '\n', install)
            self.assertIn(builder.CODE_TAB_STEPS, install)
            for step in ('open the Code tab and start a new session', 'choose Local, then My computer',
                         'At the bottom of the page, use the folder selector', 'Cmd+Shift+G',
                         'Type your message and send it'):
                self.assertEqual(install.count(step), 1, step)
            self.assertIn('Guided Coding runs on macOS and Linux', install)
            self.assertIn('Auto\nmode runs only on macOS. Windows is not supported.', install)
            self.assertIn('In Terminal on macOS or Linux, change to the project folder and run claude.', install)
            self.assertIn(metadata['general_edition']['source_manifest_sha256'], install)
            self.assertNotIn('GuidedCoding/LICENSE.cctbx.txt', archive.namelist())
        for name, data in outputs.items():
            if name.endswith('.html') and name != 'documentation.html':
                if name == 'index.html':
                    data = data.replace(builder.package_source_note(info).encode(), b'', 1)
                self.assertNotRegex(data.decode(), r'(?i)cctbx|/absolute/path/to|~/Documents/GuidedCoding')

    def test_main_page_names_the_source_adaptations_and_card_beside_download(self):
        site, old, info = self.build_fixture()
        with patch.object(builder, 'check_hooks', return_value=(2, 1, 281)), \
             patch.object(builder, 'run_contract_checks', return_value={}), \
             patch.object(builder, 'run_package_tests', return_value=[]):
            outputs = builder.build_artifacts(self.source, info, b'license', site, self.root)
        page = outputs['index.html'].decode()
        self.assertEqual(page.count('id="package-source"'), 1)
        self.assertLess(page.index('id="install"'), page.index('id="download"'))
        self.assertLess(page.index('id="download"'), page.index('id="package-source"'))
        self.assertIn('cctbx_project/libtbx/guided_coding</code></a>', page)
        self.assertIn('/' + info['commit'] + '/libtbx/guided_coding', page)
        self.assertIn('edits the documentation and local path examples', page)
        self.assertIn('<code>~/Downloads/GuidedCoding/guided_coding</code>, generalizes project-specific wording', page)
        self.assertIn('href="GENERAL_DEVELOPER_CARD.md" download>general defaults card', page)
        self.assertIn('the license, and which files were adapted with their checksums before and after, '
                      'are recorded with the download', page)
        self.assertNotIn('exact file changes are recorded with the download', page)
        builder.verify_general_documentation({'index.html': outputs['index.html']}, info)
        self.assertEqual(old, {n: (site / n).read_bytes() for n in old})

    def build_outputs(self):
        site, old, info = self.build_fixture()
        with patch.object(builder, 'check_hooks', return_value=(2, 1, 281)), \
             patch.object(builder, 'run_contract_checks', return_value={}), \
             patch.object(builder, 'run_package_tests', return_value=[]):
            outputs = builder.build_artifacts(self.source, info, b'license', site, self.root)
        self.assertEqual(old, {n: (site / n).read_bytes() for n in old})
        return outputs, info

    def test_website_pages_are_rendered_listed_and_linked(self):
        outputs, info = self.build_outputs()
        self.assertEqual(set(outputs), set(builder.OUTPUTS))
        metadata = json.loads(outputs['package.json'])
        recorded = {item['page']: item for item in metadata['documentation']['site_pages']}
        for source, page, description in builder.SITE_PAGES:
            data = (SCRIPT.parent / source).read_bytes()
            title = data.decode().splitlines()[0][2:]
            html_page = outputs[page].decode()
            self.assertIn('<h1 class="gc-document-title">' + html.escape(title) + '</h1>', html_page)
            self.assertIn(html.escape(description), html_page)
            self.assertEqual(html_page.count(builder.SITE_NOTE), 1)
            self.assertNotIn(builder.DOC_NOTE, html_page)
            self.assertEqual(recorded[page]['source_sha256'], builder.digest(data))
            self.assertEqual(recorded[page]['page_sha256'], builder.digest(outputs[page]))
            self.assertIn('<a href="' + page + '">' + html.escape(title) + '</a>',
                          outputs['documentation.html'].decode())
        for page in ('getting-started.html', 'documentation.html', 'reference-files.html'):
            text = outputs[page].decode()
            self.assertEqual(text.count(builder.DOC_NOTE), 1, page)
            self.assertIn('<a href="quick-start.html">Quick Start</a>', text)
            self.assertIn('<a href="how-it-works.html">How it works</a>', text)
        main = outputs['index.html'].decode()
        self.assertIn('<h1>Guided Coding Help and Information</h1>', main)
        self.assertNotIn('Current status', main)
        for page in ('why-not-claude-code.html', 'why-not-vibe-coding.html', 'how-it-works.html',
                     'quick-start.html'):
            self.assertIn('href="' + page + '"', main)
        install = main[main.index('id="install"'):main.index('id="download"')]
        self.assertIn('Claude: perform registration in the current conversation. A new conversation '
                      'is needed only to use the command afterward.', install)
        self.assertEqual(main.count('id="copy-status"'), 1)
        for name, data in outputs.items():
            if name.endswith('.html'):
                builder.verify_general_documentation({name: data}, info)

    def test_quick_start_copy_box_holds_the_exact_instructions(self):
        outputs, _ = self.build_outputs()
        source = (SCRIPT.parent / 'pages/quick-start.md').read_text()
        expected = source.split('```copy\n', 1)[1].split('\n```', 1)[0]
        page = outputs['quick-start.html'].decode()
        match = re.search(r'<pre class="gc-copy-box" id="copy-text"><code>(.*?)</code></pre>', page, re.S)
        self.assertIsNotNone(match)
        self.assertEqual(html.unescape(match[1]), expected)
        self.assertIn('<button type="button" data-copy="copy-text">' + builder.COPY_LABEL + '</button>', page)
        self.assertEqual(page.count('id="copy-status"'), 1)
        self.assertIn('navigator.clipboard.writeText', page)

    def test_site_links_and_copy_blocks_are_limited_to_website_pages(self):
        info = {"commit": "a" * 40}
        with self.assertRaises(builder.PackageError):
            builder.render_document('# Kit\n\nSee [start](quick-start.html).\n', info)
        body, _ = builder.render_document('# Site\n\nSee [start](quick-start.html).\n', info, site=True)
        self.assertIn('<a href="quick-start.html">start</a>', body)
        for link in ('quick-start.html?x=1', 'missing-page.html', '/quick-start.html'):
            with self.assertRaises(builder.PackageError, msg=link):
                builder.render_document('# Site\n\n[x](' + link + ')\n', info, site=True)
        body, _ = builder.render_document('# Kit\n\n```copy\ntext\n```\n', info)
        self.assertEqual(body, '<pre><code>text\n</code></pre>')
        with self.assertRaises(builder.PackageError):
            builder.render_document('# Site\n\n```copy\na\n```\n\n```copy\nb\n```\n', info, site=True)

    def test_temporary_instruction_edits_and_reason_are_in_zip_and_html(self):
        site, old, info = self.build_fixture()
        originals = builder.source_snapshot(self.source)
        with patch.object(builder, 'check_hooks', return_value=(2, 1, 281)), \
             patch.object(builder, 'run_contract_checks', return_value={}), \
             patch.object(builder, 'run_package_tests', return_value=[]):
            outputs = builder.build_artifacts(self.source, info, b'license', site, self.root)
        prefix = builder.TEMP_PREFIX + ' ' + builder.PY
        reason = 'The kit commands resolve `TMPDIR` because macOS temporary paths can pass through symbolic links.'
        doc_pages = {'docs/' + name: page for name, page, _, _ in builder.DOCUMENTS}
        total = 0
        with zipfile.ZipFile(io.BytesIO(outputs['guided_coding.zip'])) as archive:
            for name in builder.TEMP_HEADERS:
                text = archive.read('GuidedCoding/guided_coding/' + name).decode()
                self.assertEqual(text.count(reason), 1, name)
                page = doc_pages.get(name, 'reference-files.html')
                if page == 'reference-files.html':
                    self.assertIn(html.escape(text), outputs[page].decode())
                else:
                    self.assertIn('The kit commands resolve <code>TMPDIR</code> because macOS temporary paths '
                                  'can pass through symbolic links.', outputs[page].decode())
                count = sum(n for _, n in builder.TEMP_COMMANDS.get(name, ()))
                self.assertEqual(text.count(prefix) + text.count(builder.ENV_TEMP + ' ' + builder.PY),
                                 count, name)
                total += count
                for command, n in builder.TEMP_COMMANDS.get(name, ()):
                    resolved = builder.resolve_temporary(command)
                    self.assertEqual(text.count(resolved), n, name)
                    self.assertIn(html.escape(resolved.strip('`\n')), outputs[page].decode(), name)
            self.assertEqual(total, 22)
            self.assertIn(reason.replace('`', ''), archive.read('GuidedCoding/INSTALL.md').decode())
            for name in originals:
                if name.startswith(('payload/tools/', 'tests/')):
                    self.assertEqual(archive.read('GuidedCoding/guided_coding/' + name),
                                     (self.source / name).read_bytes())
        builder.require_unchanged_source(self.source, originals)
        self.assertEqual(old, {n: (site / n).read_bytes() for n in old})

    def test_readable_introductions_keep_their_context_and_commands(self):
        for name in ('docs/GUIDED_CODING_README.md',
                     'docs/GUIDED_CODING_ARCHITECTURE.md',
                     'docs/GUIDED_CODING_VERIFICATION.md'):
            with self.subTest(name=name):
                first_paragraph = 'Guided Coding keeps the procedure and project settings together.'
                text = (builder.READABLE_HEADERS[name] + '\n\n' + first_paragraph + '\n\n'
                        + temp_fixture(name).decode().split('\n\n', 1)[1])
                adapted = builder.temporary_instructions(name, text)
                self.assertTrue(adapted.startswith(builder.READABLE_HEADERS[name] + '\n\n' + first_paragraph))
                self.assertNotIn(builder.TEMP_REASON, adapted)
                self.assertEqual(adapted.count(builder.TEMP_PREFIX + ' ' + builder.GENERAL_PYTHON)
                                 + adapted.count(builder.ENV_TEMP + ' ' + builder.GENERAL_PYTHON),
                                 text.count(builder.GENERAL_PYTHON))
        reference = ('# Guided Coding registration and command reference\n\n'
                     'Use this reference for manual registration.\n\n'
                     + temp_fixture(REFERENCE).decode().split('\n\n', 1)[1])
        adapted = builder.temporary_instructions('docs/GUIDED_CODING_COMMAND_REFERENCE.md', reference)
        self.assertTrue(adapted.startswith('# Guided Coding registration and command reference\n\n'
                                         'Use this reference for manual registration.'))
        self.assertGreater(adapted.index(builder.TEMP_REASON), adapted.index('## One-time registration'))

    def test_changed_missing_or_duplicated_temporary_passage_stops_build(self):
        site, old, info = self.build_fixture()
        originals = {p.relative_to(self.source).as_posix(): p.read_bytes()
                     for p in self.source.rglob('*') if p.is_file() and p.name != 'SOURCE_MANIFEST.sha256'}
        passages = [(name, command, 'instruction') for name, commands in builder.TEMP_COMMANDS.items()
                    for command, _ in commands]
        passages += [(name, header + '\n\n', 'explanation anchor')
                     for name, header in builder.TEMP_HEADERS.items()]
        for name, before, kind in passages:
            changed = (before.replace('-I -B', '-B', 1) if kind == 'instruction'
                       else before.replace('\n\n', ' (changed)\n\n', 1))
            self.assertNotEqual(changed, before)
            for replacement in (changed, '', before + '\n\n' + before):
                with self.subTest(name=name, before=before, replacement=replacement), \
                     tempfile.TemporaryDirectory(dir=self.root) as scratch:
                    files = dict(originals)
                    files[name] = files[name].decode().replace(before, replacement, 1).encode()
                    self.write_source(files)
                    info['source_manifest_sha256'] = builder.digest((self.source / 'SOURCE_MANIFEST.sha256').read_bytes())
                    frozen = builder.source_snapshot(self.source)
                    with patch.object(builder, 'check_hooks', return_value=(2, 1, 281)), \
                         patch.object(builder, 'run_contract_checks', return_value={}), \
                         patch.object(builder, 'run_package_tests', return_value=[]), \
                         patch.object(builder, 'make_zip', wraps=builder.make_zip) as make_zip, \
                         patch.object(builder, 'publish_local') as publish:
                        with self.assertRaisesRegex(builder.PackageError,
                                'required temporary-directory ' + kind + ' missing or duplicated; inspect ' + re.escape(name)):
                            builder.build_artifacts(self.source, info, b'license', site, Path(scratch))
                        make_zip.assert_not_called()
                        publish.assert_not_called()
                    builder.require_unchanged_source(self.source, frozen)
                    self.assertEqual(old, {n: (site / n).read_bytes() for n in old})

    def test_source_resolved_verification_command_is_not_prefixed_twice(self):
        # The case that occurs: the source resolves its own test command (revision 13
        # writes it as a shell-neutral `env TMPDIR=...` line).
        name = "docs/GUIDED_CODING_VERIFICATION.md"
        test_command = builder.PY + " -m unittest discover -s tests -p 'tst_*.py' -v\n"
        resolved = "env " + builder.ENV_TEMP + " " + test_command
        text = temp_fixture(name).decode()
        self.assertEqual(text.count(resolved), 1)
        adapted = builder.temporary_instructions(name, text)
        self.assertNotIn(builder.ENV_TEMP + " " + builder.ENV_TEMP, adapted)
        self.assertNotIn(builder.TEMP_PREFIX, adapted.replace(builder.TEMP_REASON, ""))
        self.assertEqual(adapted.count(resolved), 1)
        for doubled in (resolved.replace(test_command, builder.ENV_TEMP + " " + test_command),
                        resolved + "\n" + resolved):
            with self.assertRaises(builder.PackageError):
                builder.temporary_instructions(name, text.replace(resolved, doubled, 1))

    def test_any_doubled_temporary_prefix_form_is_refused(self):
        # Outside reading 1, finding 1: unquoted and two-space variants of an
        # already-resolved command must not be accepted with a second prefix.
        name = "docs/GUIDED_CODING_VERIFICATION.md"
        test_command = builder.PY + " -m unittest discover -s tests -p 'tst_*.py' -v\n"
        for variant in ('TMPDIR=$(cd "${TMPDIR:-/tmp}" && pwd -P) ',
                        builder.TEMP_PREFIX + "  "):
            with self.subTest(variant=variant):
                text = temp_fixture(name).decode().replace(test_command, variant + test_command, 1)
                with self.assertRaisesRegex(builder.PackageError,
                        "doubled temporary-directory prefix; inspect " + re.escape(name)):
                    builder.temporary_instructions(name, text)

    def test_already_resolved_temporary_instruction_is_not_prefixed_twice(self):
        for name, commands in builder.TEMP_COMMANDS.items():
            with self.subTest(name=name):
                text = temp_fixture(name).decode()
                for command, _ in commands:
                    text = text.replace(command, builder.resolve_temporary(command))
                adapted = builder.temporary_instructions(name, text)
                self.assertNotIn(builder.TEMP_PREFIX + " " + builder.TEMP_PREFIX, adapted)
                self.assertNotIn(builder.ENV_TEMP + " " + builder.ENV_TEMP, adapted)
                for command, count in commands:
                    self.assertEqual(adapted.count(builder.resolve_temporary(command)), count)
        name = "docs/GUIDED_CODING_USER_GUIDE.md"
        command = builder.SOURCE_COMMAND
        resolved = builder.resolve_temporary(command)
        text = temp_fixture(name).decode().replace(command, resolved, 1)
        with self.assertRaisesRegex(builder.PackageError,
                "partly resolved temporary-directory instruction; inspect " + re.escape(name)):
            builder.temporary_instructions(name, text)

    def test_new_unresolved_python_instruction_stops_distribution_adaptation(self):
        site, old, info = self.build_fixture()
        (self.source / 'new-instructions.md').write_text('# New instructions\n\npython3 new_tool.py\n')
        files = {p.relative_to(self.source).as_posix(): p.read_bytes()
                 for p in self.source.rglob('*') if p.is_file() and p.name != 'SOURCE_MANIFEST.sha256'}
        (self.source / 'SOURCE_MANIFEST.sha256').write_bytes(manifest(files))
        with self.assertRaisesRegex(builder.PackageError, 'unresolved temporary-directory instruction; inspect new-instructions.md'):
            builder.general_source(self.source, self.root / 'edition')
        self.assertEqual(old, {n: (site / n).read_bytes() for n in old})

    def test_exact_plain_stop_commands_are_kept_without_prefix(self):
        # The auto-mode stop command must also run in csh, where the prefix fails.
        for name, passage in builder.PLAIN_STOP_COMMANDS.items():
            with self.subTest(name=name):
                text = '# Stop\n\n' + passage + 'More text.\n'
                self.assertEqual(builder.temporary_instructions(name, text), text)

    def test_changed_duplicated_or_extra_plain_stop_command_is_refused(self):
        for name, passage in builder.PLAIN_STOP_COMMANDS.items():
            changed = (passage.replace('auto_queue.py stop', 'auto_queue.py status'),
                       passage.replace("python3' -I -B", "python3' -B"),
                       passage.replace('start screen', 'screen'),
                       passage + passage,
                       passage + 'python3 -I -B other_tool.py\n',
                       'Added text ' + passage)
            for text in changed:
                with self.subTest(name=name, text=text):
                    self.assertNotEqual(text, passage)
                    with self.assertRaisesRegex(builder.PackageError,
                            '(unresolved temporary-directory instruction|plain stop command duplicated|unadapted interpreter command); inspect '
                            + re.escape(name)):
                        builder.temporary_instructions(name, '# Stop\n\n' + text)

    def test_plain_stop_exception_does_not_apply_to_other_files(self):
        passage = builder.PLAIN_STOP_COMMANDS['payload/AUTO.md']
        for name in ('payload/WORKER.md', 'payload/screens/AUTO_REPORT.md', 'SKILL.md'):
            with self.subTest(name=name):
                with self.assertRaises(builder.PackageError):
                    builder.temporary_instructions(name, builder.TEMP_HEADERS.get(name, '# X') + '\n\n' + passage)

    def test_clean_environment_resolves_symbolic_temporary_path(self):
        alias = self.root / 'alias'
        alias.symlink_to(self.root, target_is_directory=True)
        with patch.dict(os.environ, {'TMPDIR': str(alias)}):
            env = builder.clean_environment(alias)
        self.assertEqual(env['TMPDIR'], str(self.root))
        self.assertEqual(env['HOME'], str(self.root))

    def test_kit_test_runner_resolves_symbolic_source_and_temporary_paths(self):
        files = {'SKILL.md': b'original skill\n', 'tests/tst_example.py': b'# immutable test fixture\n'}
        self.write_source(files)
        alias = self.root / 'alias'
        alias.symlink_to(self.root, target_is_directory=True)
        def checked(args, source, env, timeout=None):
            self.assertEqual(source, self.source)
            self.assertEqual(args, [self.source / 'tests/tst_example.py'])
            self.assertEqual(env['TMPDIR'], str(self.root))
            return 'Ran 1 test in 0.001s\n\nOK\n'
        with patch.object(builder, 'run_checked', side_effect=checked):
            result = builder.run_package_tests(alias / 'source', alias)
        self.assertEqual(result[0]['tests'], 1)

    def test_each_kit_test_file_gets_the_longer_time_limit(self):
        # The auto-mode tests take about 330 s per file; other checks keep 180 s.
        self.assertEqual(builder.PACKAGE_TEST_TIMEOUT, 900)
        files = {'SKILL.md': b'original skill\n', 'tests/tst_a.py': b'# a\n', 'tests/tst_b.py': b'# b\n'}
        self.write_source(files)
        limits = []
        def checked(args, source, env, timeout=180):
            limits.append(timeout)
            return 'Ran 1 test in 0.001s\n\nOK\n'
        with patch.object(builder, 'run_checked', side_effect=checked):
            builder.run_package_tests(self.source, self.root)
        self.assertEqual(limits, [900, 900])

    def test_contract_runner_resolves_symbolic_source_and_temporary_paths(self):
        alias = self.root / 'alias'
        alias.symlink_to(self.root, target_is_directory=True)
        def checked(args, source, env, **kwargs):
            self.assertEqual(source, self.source)
            self.assertEqual(args[0], self.source / 'payload/tools/screen_check.py')
            self.assertEqual(env['TMPDIR'], str(self.root))
            self.assertEqual(env['GC_PAYLOAD_ROOT'], str(self.source / 'payload'))
            raise RuntimeError('stopped after verifying physical paths')
        with patch.object(builder, 'run_checked', side_effect=checked), \
             self.assertRaisesRegex(RuntimeError, 'stopped after verifying physical paths'):
            builder.run_contract_checks(alias / 'source', (2, 1, 281), alias)

    def test_invalid_documentation_build_preserves_existing_output_set(self):
        site, old, info = self.build_fixture()
        files = {p.relative_to(self.source).as_posix(): p.read_bytes()
                 for p in self.source.rglob('*') if p.is_file() and p.name != 'SOURCE_MANIFEST.sha256'}
        files['docs/GUIDED_CODING_USER_GUIDE.md'] = temp_fixture('docs/GUIDED_CODING_USER_GUIDE.md') + b'> Unsupported new syntax\n'
        self.write_source(files)
        info['source_manifest_sha256'] = builder.digest((self.source / 'SOURCE_MANIFEST.sha256').read_bytes())
        with patch.object(builder, 'check_hooks', return_value=(2, 1, 281)), \
             patch.object(builder, 'run_contract_checks', return_value={}), \
             patch.object(builder, 'run_package_tests', return_value=[]), \
             patch.object(builder, 'publish_local') as publish:
            with self.assertRaisesRegex(builder.PackageError, 'unsupported documentation block'):
                builder.build_artifacts(self.source, info, b'license', site, self.root)
            publish.assert_not_called()
        self.assertEqual(old, {name: (site / name).read_bytes() for name in old})

    def test_final_documentation_scan_allows_only_the_exact_source_notes(self):
        info = {'commit': 'a' * 40}
        note = builder.historical_note(info).encode()
        main_note = builder.package_source_note(info).encode()
        builder.verify_general_documentation({'documentation.html': note}, info)
        builder.verify_general_documentation({'index.html': main_note}, info)
        for filename, data in (
            ('index.html', main_note + b'<p>cctbx_project</p>'),
            ('user-guide.html', b'<a href="https://example.invalid/CCTBX">guide</a>'),
            ('reference-files.html', b'<p>cc&#116;bx</p>'),
            ('INSTALL.md', b'Use cCtBx here.'),
            ('GENERAL_DEVELOPER_CARD.md', b'Use /absolute/path/to/project.'),
            ('documentation.html', note + b'<p>cctbx</p>'),
            ('index.html', main_note + note),
            ('documentation.html', note + main_note),
            ('README.md', b'Use cctbx_project/libtbx/guided_coding/.'),
        ):
            with self.subTest(filename=filename, data=data), self.assertRaisesRegex(builder.PackageError, 'unadapted'):
                builder.verify_general_documentation({filename: data}, info)

        for filename, data in (('documentation.html', note + note),
                               ('documentation.html', note.replace(b'began', b'started')),
                               ('index.html', main_note + main_note),
                               ('index.html', main_note.replace(b'Source and adaptations.', b'Source.')),
                               ('index.html', note)):
            with self.subTest(filename=filename, data=data), self.assertRaisesRegex(builder.PackageError, 'source attribution'):
                builder.verify_general_documentation({filename: data}, info)

    def test_final_scan_allows_affiliation_only_in_site_header(self):
        info = {'commit': 'a' * 40}
        affiliation = builder.SITE_AFFILIATION.encode()
        header = b'<header class="site-header">' + affiliation + b'</header>'
        builder.verify_general_documentation({'overview.html': header + b'<main>General projects.</main>'}, info)
        for data in (affiliation, b'<main>' + affiliation + b'</main>',
                     header + b'<p>PhEnIx commands</p>', header + b'<p>Ph&#101;nix commands</p>',
                     header + b'<pre><code>&lt;header class="site-header"&gt;' + affiliation + b'</code></pre>',
                     header + header, header.replace(b'Phenix</a>', b'PHENIX</a>')):
            with self.subTest(data=data), self.assertRaisesRegex(builder.PackageError, 'unadapted'):
                builder.verify_general_documentation({'overview.html': data}, info)
        with self.assertRaisesRegex(builder.PackageError, 'unadapted'):
            builder.verify_general_documentation({'INSTALL.md': header}, info)
    def test_leftover_template_or_installer_reference_refuses_without_replacing_outputs(self):
        site, old, info = self.build_fixture()
        original_templates = {name: (site / name).read_bytes()
                              for name in ('index.template.html', 'docs.template.html')}
        install = builder.installation_text
        for target, reference in ((target, reference)
                                 for target in ('index.template.html', 'docs.template.html', 'INSTALL.md',
                                                'GENERAL_DEVELOPER_CARD.md', 'README.md')
                                 for reference in (b'CCTBX', b'PhEnIx')):
            with self.subTest(target=target), tempfile.TemporaryDirectory(dir=self.root) as directory:
                for name, data in original_templates.items():
                    (site / name).write_bytes(data)
                (site / 'GENERAL_DEVELOPER_CARD.md').write_bytes((SCRIPT.parent / 'GENERAL_DEVELOPER_CARD.md').read_bytes())
                (site / 'README.md').write_bytes(b'# Maintenance\n')
                if target in original_templates:
                    (site / target).write_bytes(original_templates[target].replace(
                        b'</main>', b'<p>Unexpected ' + reference + b' instructions.</p></main>'))
                elif target != 'INSTALL.md':
                    (site / target).write_bytes(b'# Instructions\nUnexpected ' + reference + b' reference.\n')
                with patch.object(builder, 'check_hooks', return_value=(2, 1, 281)), \
                     patch.object(builder, 'run_contract_checks', return_value={}), \
                     patch.object(builder, 'run_package_tests', return_value=[]), \
                     patch.object(builder, 'installation_text', side_effect=lambda *args:
                                  install(*args) + (b'Unexpected ' + reference + b' reference.\n' if target == 'INSTALL.md' else b'')), \
                     patch.object(builder, 'publish_local') as publish:
                    with self.assertRaisesRegex(builder.PackageError, 'unadapted'):
                        builder.build_artifacts(self.source, info, b'license', site, Path(directory))
                    publish.assert_not_called()
                self.assertEqual(old, {n: (site / n).read_bytes() for n in old})

    def test_runner_cannot_relabel_changed_source_by_regenerating_manifest(self):
        site, old, info = self.build_fixture()
        original = {p.relative_to(self.source).as_posix(): p.read_bytes()
                    for p in self.source.rglob("*") if p.is_file()}

        def change_source(*args):
            (self.source / "SKILL.md").write_bytes(b"changed during execution\n")
            files = {p.relative_to(self.source).as_posix(): p.read_bytes()
                     for p in self.source.rglob("*")
                     if p.is_file() and p.name != "SOURCE_MANIFEST.sha256"}
            (self.source / "SOURCE_MANIFEST.sha256").write_bytes(manifest(files))
            builder.validate_source(self.source)  # Still internally consistent.
            return {} if runner == "run_contract_checks" else []

        for runner in ("run_contract_checks", "run_package_tests"):
            with self.subTest(runner=runner):
                self.write_source({n: b for n, b in original.items()
                                   if n != "SOURCE_MANIFEST.sha256"})
                with patch.object(builder, "check_hooks", return_value=(2, 1, 281)), \
                     patch.object(builder, "run_contract_checks", return_value={}), \
                     patch.object(builder, "run_package_tests", return_value=[]), \
                     patch.object(builder, runner, side_effect=change_source), \
                     patch.object(builder, "make_zip", wraps=builder.make_zip) as make_zip:
                    with self.assertRaisesRegex(builder.PackageError, "source changed"):
                        builder.build_artifacts(self.source, info, b"license", site, self.root)
                    make_zip.assert_not_called()
                self.assertEqual(old, {n: (site / n).read_bytes() for n in old})

    def test_runner_cannot_add_manifest_listed_source_or_change_mode(self):
        site, old, info = self.build_fixture()
        original = {p.relative_to(self.source).as_posix(): p.read_bytes()
                    for p in self.source.rglob("*") if p.is_file()}

        def change_source(*args):
            if change == "inventory":
                files = {n: b for n, b in original.items() if n != "SOURCE_MANIFEST.sha256"}
                files["new.md"] = b"new source file\n"
                self.write_source(files)
            else:
                (self.source / "SKILL.md").chmod(0o755)
            builder.validate_source(self.source)
            return []

        for change in ("inventory", "mode"):
            with self.subTest(change=change):
                self.write_source({n: b for n, b in original.items()
                                   if n != "SOURCE_MANIFEST.sha256"})
                (self.source / "SKILL.md").chmod(0o644)
                with patch.object(builder, "check_hooks", return_value=(2, 1, 281)), \
                     patch.object(builder, "run_contract_checks", return_value={}), \
                     patch.object(builder, "run_package_tests", side_effect=change_source):
                    with self.assertRaisesRegex(builder.PackageError, "source changed"):
                        builder.build_artifacts(self.source, info, b"license", site, self.root)
                self.assertEqual(old, {n: (site / n).read_bytes() for n in old})

    def test_unchanged_source_builds_with_matching_provenance(self):
        site, old, info = self.build_fixture()
        with patch.object(builder, "check_hooks", return_value=(2, 1, 281)), \
             patch.object(builder, "run_contract_checks", return_value={}), \
             patch.object(builder, "run_package_tests", return_value=[]):
            artifacts = builder.build_artifacts(self.source, info, b"license", site, self.root)
        metadata = json.loads(artifacts["package.json"])
        self.assertEqual(metadata["upstream"], info)
        self.assertEqual(metadata["archive"]["sha256"], builder.digest(artifacts["guided_coding.zip"]))
        self.assertEqual(old, {n: (site / n).read_bytes() for n in old})

    def test_source_change_during_zip_creation_is_rejected(self):
        site, old, info = self.build_fixture()
        real_make_zip = builder.make_zip

        def change_after_zip(*args):
            archive = real_make_zip(*args)
            (self.source / "SKILL.md").chmod(0o755)
            return archive

        with patch.object(builder, "check_hooks", return_value=(2, 1, 281)), \
             patch.object(builder, "run_contract_checks", return_value={}), \
             patch.object(builder, "run_package_tests", return_value=[]), \
             patch.object(builder, "make_zip", side_effect=change_after_zip):
            with self.assertRaisesRegex(builder.PackageError, "source changed"):
                builder.build_artifacts(self.source, info, b"license", site, self.root)
        self.assertEqual(old, {n: (site / n).read_bytes() for n in old})

    def test_download_identity_mismatch_stops_before_execution(self):
        site, old, info = self.build_fixture()
        for field, value in (("source_manifest_sha256", "0" * 64),
                             ("source_files", 4), ("license_sha256", "0" * 64)):
            with self.subTest(field=field), \
                 patch.object(builder, "check_hooks", return_value=(2, 1, 281)), \
                 patch.object(builder, "run_contract_checks") as execute:
                with self.assertRaisesRegex(builder.PackageError, "differs from download metadata"):
                    builder.build_artifacts(self.source, {**info, field: value}, b"license", site, self.root)
                execute.assert_not_called()
        self.assertEqual(old, {n: (site / n).read_bytes() for n in old})

    def test_check_failure_never_calls_output_replacement(self):
        site, old = self.make_site_outputs()
        (site / "index.template.html").write_text("template")
        (site / "docs.template.html").write_text("template")
        (site / "GENERAL_DEVELOPER_CARD.md").write_text("card")
        (site / "main-page.md").write_text("# Guided Coding\n\nIntroduction.\n")
        for source, _, _ in builder.SITE_PAGES:
            (site / source).parent.mkdir(exist_ok=True)
            (site / source).write_text("# Page\n\nText.\n")
        with patch.object(builder, "SITE", site), \
             patch.object(builder, "download_source", side_effect=builder.PackageError("refused")), \
             patch.object(builder, "publish_local") as publish:
            self.assertEqual(builder.main([]), 1)
            publish.assert_not_called()
        self.assertEqual(old, {name: (site / name).read_bytes() for name in old})

    def test_check_only_never_calls_output_replacement(self):
        site, old = self.make_site_outputs()
        (site / "index.template.html").write_text("template")
        (site / "docs.template.html").write_text("template")
        (site / "GENERAL_DEVELOPER_CARD.md").write_text("card")
        (site / "main-page.md").write_text("# Guided Coding\n\nIntroduction.\n")
        for source, _, _ in builder.SITE_PAGES:
            (site / source).parent.mkdir(exist_ok=True)
            (site / source).write_text("# Page\n\nText.\n")
        with patch.object(builder, "SITE", site), \
             patch.object(builder, "download_source", return_value=({}, b"license")), \
             patch.object(builder, "build_artifacts", return_value=old), \
             patch.object(builder, "publish_local") as publish:
            # A valid resolved identity is reported by the real downloader.
            with patch.object(builder, "download_source", return_value=({"commit": "a" * 40}, b"license")):
                self.assertEqual(builder.main(["--check-only"]), 0)
            publish.assert_not_called()
        self.assertEqual(old, {name: (site / name).read_bytes() for name in old})

    def test_symlink_output_refused_without_changing_other_outputs(self):
        site, old = self.make_site_outputs()
        target = self.root / "elsewhere"
        target.write_text("KEEP")
        (site / "index.html").unlink()
        (site / "index.html").symlink_to(target)
        with self.assertRaises(builder.PackageError):
            builder.publish_local(site, {name: b"new" for name in old})
        self.assertEqual(target.read_text(), "KEEP")
        for name in old.keys() - {"index.html"}:
            self.assertEqual((site / name).read_bytes(), old[name])

    def test_output_error_restores_previous_bytes_and_success_replaces_page_last(self):
        site, old = self.make_site_outputs()
        replacement = {name: ("NEW " + name).encode() for name in old}
        real_replace = os.replace
        calls = []

        def failing_replace(source, target):
            calls.append(Path(target).name)
            if len(calls) == 3:
                raise OSError("injected replacement failure")
            return real_replace(source, target)

        with patch.object(builder.os, "replace", side_effect=failing_replace):
            with self.assertRaises(OSError):
                builder.publish_local(site, replacement)
        self.assertEqual(old, {name: (site / name).read_bytes() for name in old})
        with patch.object(builder.os, "replace", wraps=real_replace) as replace:
            builder.publish_local(site, replacement)
            self.assertEqual(Path(replace.call_args_list[-1].args[1]).name, "index.html")
        self.assertEqual(replacement, {name: (site / name).read_bytes() for name in old})

    def test_first_build_error_removes_newly_created_outputs(self):
        site = self.root / "new-site"
        site.mkdir()
        real_replace = os.replace
        calls = []

        def failing_replace(source, target):
            calls.append(Path(target).name)
            if len(calls) == 3:
                raise OSError("injected first-build failure")
            return real_replace(source, target)

        with patch.object(builder.os, "replace", side_effect=failing_replace):
            with self.assertRaises(OSError):
                builder.publish_local(site, {name: b"new" for name in builder.OUTPUTS})
        self.assertEqual(list(site.iterdir()), [])

    def test_failure_at_each_document_page_restores_whole_output_set(self):
        site, old = self.make_site_outputs()
        real_replace = os.replace
        for index, name in enumerate(builder.OUTPUTS, 1):
            if not name.endswith('.html'):
                continue
            calls = []
            def failing_replace(source, target):
                calls.append(Path(target).name)
                if len(calls) == index:
                    raise OSError('injected documentation-page replacement failure')
                return real_replace(source, target)
            with self.subTest(output=name), patch.object(builder.os, 'replace', side_effect=failing_replace):
                with self.assertRaises(OSError):
                    builder.publish_local(site, {n: b'NEW' for n in old})
            self.assertEqual(old, {n: (site / n).read_bytes() for n in old})
            self.assertFalse(list(site.glob('.gc-stage-*')))
            self.assertFalse((site / '.gc-write-lock').exists())

    def test_persistent_rollback_failure_keeps_recovery_copies_and_blocks_next_write(self):
        site, old = self.make_site_outputs()
        (site / "guided_coding.zip").chmod(0o640)
        real_replace = os.replace
        calls = []

        def failing_replace(source, target):
            calls.append(Path(target).name)
            if len(calls) >= 3:
                raise OSError("injected persistent replacement failure")
            return real_replace(source, target)

        with patch.object(builder.os, "replace", side_effect=failing_replace):
            with self.assertRaisesRegex(builder.PackageError, "Recovery copies.*retained at") as caught:
                builder.publish_local(site, {n: b"NEW" for n in old})
        recoveries = list(site.glob(".gc-stage-*"))
        self.assertEqual(len(recoveries), 1)
        recovery = recoveries[0]
        self.assertIn(str(recovery), str(caught.exception))
        for name, data in old.items():
            self.assertEqual((recovery / "originals" / name).read_bytes(), data)
        self.assertEqual((recovery / "originals/guided_coding.zip").stat().st_mode & 0o777, 0o640)
        self.assertTrue((recovery / "RECOVERY.md").is_file())
        self.assertEqual(len(calls), 5)  # Both restorations were attempted.
        self.assertTrue((site / ".gc-write-lock").is_dir())
        with self.assertRaisesRegex(builder.PackageError, "write is locked"):
            builder.publish_local(site, {n: b"NEXT" for n in old})

    def test_rollback_keeps_backups_of_successfully_restored_outputs_too(self):
        site, old = self.make_site_outputs()
        real_replace = os.replace
        calls = []

        def failing_replace(source, target):
            calls.append(Path(target).name)
            if len(calls) in (3, 4):
                raise OSError("injected replacement and one restoration failure")
            return real_replace(source, target)

        with patch.object(builder.os, "replace", side_effect=failing_replace):
            with self.assertRaises(builder.PackageError):
                builder.publish_local(site, {n: b"NEW" for n in old})
        recovery, = site.glob(".gc-stage-*")
        self.assertEqual((site / "guided_coding.zip").read_bytes(), old["guided_coding.zip"])
        self.assertEqual(old, {n: (recovery / "originals" / n).read_bytes() for n in old})

    def test_first_build_failed_removal_records_original_absence(self):
        site = self.root / "new-site"
        site.mkdir()
        real_replace = os.replace
        real_unlink = Path.unlink
        calls = []

        def failing_replace(source, target):
            calls.append(Path(target).name)
            if len(calls) == 3:
                raise OSError("injected replacement failure")
            return real_replace(source, target)

        def failing_unlink(path, *args, **kwargs):
            if path.parent == site and path.name in builder.OUTPUTS:
                raise OSError("injected persistent removal failure")
            return real_unlink(path, *args, **kwargs)

        with patch.object(builder.os, "replace", side_effect=failing_replace), \
             patch.object(Path, "unlink", failing_unlink):
            with self.assertRaisesRegex(builder.PackageError, "retained at"):
                builder.publish_local(site, {n: b"NEW" for n in builder.OUTPUTS})
        recovery, = site.glob(".gc-stage-*")
        record = json.loads((recovery / "RECOVERY.json").read_text())
        self.assertEqual(record["originals"], {n: None for n in builder.OUTPUTS})
        self.assertEqual(list((recovery / "originals").iterdir()), [])

    def test_backup_write_failure_leaves_outputs_untouched(self):
        site, old = self.make_site_outputs()
        real_write = Path.write_bytes

        def failing_write(path, data):
            if path.parent.name == "originals" and path.name == "package.json":
                raise OSError("injected backup-write failure")
            return real_write(path, data)

        with patch.object(Path, "write_bytes", failing_write), \
             patch.object(builder.os, "replace") as replace:
            with self.assertRaisesRegex(OSError, "backup-write failure"):
                builder.publish_local(site, {n: b"NEW" for n in old})
            replace.assert_not_called()
        self.assertEqual(old, {n: (site / n).read_bytes() for n in old})
        self.assertFalse(list(site.glob(".gc-stage-*")))
        self.assertFalse((site / ".gc-write-lock").exists())

    def test_cli_reports_failed_rollback_recovery_path_and_returns_failure(self):
        site, old = self.make_site_outputs()
        copy_site_inputs(site)
        real_replace = os.replace
        calls = []

        def failing_replace(source, target):
            calls.append(Path(target).name)
            if len(calls) >= 3:
                raise OSError("injected persistent replacement failure")
            return real_replace(source, target)

        stderr = io.StringIO()
        with patch.object(builder, "SITE", site), \
             patch.object(builder, "download_source", return_value=({"commit": "a" * 40}, b"license")), \
             patch.object(builder, "build_artifacts", return_value={n: b"NEW" for n in old}), \
             patch.object(builder.os, "replace", side_effect=failing_replace), \
             patch.object(builder.sys, "stderr", stderr):
            self.assertEqual(builder.main([]), 1)
        recovery, = site.glob(".gc-stage-*")
        self.assertIn("NOT PACKAGED:", stderr.getvalue())
        self.assertIn(str(recovery), stderr.getvalue())
        self.assertIn("Outputs may be mismatched", stderr.getvalue())

    def test_existing_write_lock_refuses_without_changing_outputs(self):
        site, old = self.make_site_outputs()
        lock = site / ".gc-write-lock"
        lock.mkdir()
        with self.assertRaisesRegex(builder.PackageError, "write is locked"):
            builder.publish_local(site, {name: b"new" for name in old})
        self.assertEqual(old, {name: (site / name).read_bytes() for name in old})
        self.assertTrue(lock.is_dir())




REVISION_17_GUARD = (
    "cd /absolute/path/to/libtbx/guided_coding &&\n"
    "if command -v shasum >/dev/null 2>&1; then shasum -a 256 -c SOURCE_MANIFEST.sha256; "
    "else sha256sum -c SOURCE_MANIFEST.sha256; fi &&\n"
    'GC_PAYLOAD_ROOT="$(pwd -P)/payload" libtbx.python -I -B payload/tools/screen_check.py verify-source . &&\n'
    "cat payload/RELEASE &&\n"
    "grep -Eq '^guided_coding 2\\.0 pilot r10 rev19 ' payload/RELEASE\n")
REVISION_17_RELEASE = "guided_coding 2.0 pilot r10 rev19 (revision 17, 2026-10-16: test)\n"
# The kit's form: a direct `if not INTERPRETER.fullmatch(...): return False` in stop_line.
STOP_LINE = "def stop_line(line):\n    if not INTERPRETER.fullmatch(line):\n        return False\n    return True\n"


class Revision17Rules(unittest.TestCase):
    """Kit revisions 13-17: guards, interpreter, shell-neutral lines and passages."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.source = Path(self.temporary.name).resolve() / "source"

    def hooks_source(self, guard, release=REVISION_17_RELEASE):
        markers = ("name: gc\ndisable-model-invocation: true\n$ARGUMENTS CLAUDE_SKILL_DIR "
                   "CLAUDE_PROJECT_DIR check-claude-version payload/SETUP.md payload/SETUP_DEFAULTS.md\n")
        files = {name: b"# placeholder\n" for name in builder.REQUIRED_FILES}
        files["SKILL.md"] = (markers + "```bash\n" + guard + "```\n").encode()
        files["payload/RELEASE"] = release.encode()
        for tool, functions in builder.REQUIRED_FUNCTIONS.items():
            body = "".join(f"def {function}():\n    pass\n" for function in sorted(functions))
            if tool == "screen_check.py":
                body = "MIN_CLAUDE_VERSION = (2, 1, 281)\n" + body
            files["payload/tools/" + tool] = body.encode()
        for name, data in files.items():
            (self.source / name).parent.mkdir(parents=True, exist_ok=True)
            (self.source / name).write_bytes(data)

    def test_revision_17_source_and_release_guards_are_accepted(self):
        self.hooks_source(REVISION_17_GUARD)
        self.assertEqual(builder.check_hooks(self.source), (2, 1, 281))
        # The pre-revision-13 form is no longer accepted (checker criterion B1).
        old = ("shasum -a 256 -c SOURCE_MANIFEST.sha256 &&\n"
               'GC_PAYLOAD_ROOT="$(pwd -P)/payload" python3 -I -B payload/tools/screen_check.py verify-source . &&\n'
               "grep -Fq 'guided_coding 2.0 pilot r10 rev19' payload/RELEASE\n")
        self.hooks_source(old)
        with self.assertRaisesRegex(builder.PackageError, "no longer guards source execution"):
            builder.check_hooks(self.source)

    def test_changed_source_guard_is_refused(self):
        for guard in (
                REVISION_17_GUARD.replace("; else sha256sum -c SOURCE_MANIFEST.sha256; fi &&", "; fi;"),
                REVISION_17_GUARD.replace("else sha256sum -c SOURCE_MANIFEST.sha256", "else true"),
                REVISION_17_GUARD.replace("fi &&\n", "fi ||\n"),
                REVISION_17_GUARD.replace("if command -v shasum >/dev/null 2>&1; then shasum -a 256 -c "
                                          "SOURCE_MANIFEST.sha256; else sha256sum -c SOURCE_MANIFEST.sha256; fi &&\n", "")):
            with self.subTest(guard=guard):
                self.assertNotEqual(guard, REVISION_17_GUARD)
                self.hooks_source(guard)
                with self.assertRaisesRegex(builder.PackageError, "no longer guards source execution"):
                    builder.check_hooks(self.source)

    def test_anchored_release_guard_must_match_the_start_of_release(self):
        for guard, release, message in (
                (REVISION_17_GUARD, "guided_coding 2.0 pilot r10 rev20 (later)\n", "does not match"),
                (REVISION_17_GUARD, "note: guided_coding 2.0 pilot r10 rev19 (moved)\n", "does not match"),
                (REVISION_17_GUARD.replace("rev19 '", "rev19'"), REVISION_17_RELEASE, "pattern needs inspection"),
                (REVISION_17_GUARD.replace("pilot r10", "pilot.*r10"), REVISION_17_RELEASE, "pattern needs inspection"),
                (REVISION_17_GUARD.replace("grep -Eq '^guided_coding 2\\.0 pilot r10 rev19 ' payload/RELEASE\n", ""),
                 REVISION_17_RELEASE, None)):
            with self.subTest(guard=guard[-60:], release=release):
                self.hooks_source(guard, release)
                # Without its release line the block is no longer the exact guard block.
                expected = "release guard " + message if message else "no longer guards"
                with self.assertRaisesRegex(builder.PackageError, expected):
                    builder.check_hooks(self.source)

    def test_interpreter_commands_name_a_general_python_and_resolve_tmpdir(self):
        name = "payload/WORKER.md"
        text = (builder.TEMP_HEADERS[name] + "\n\n"
                + "\n\n".join(command.replace("python3 -I -B", "libtbx.python -I -B")
                              for command, _ in builder.TEMP_COMMANDS[name]) + "\n")
        adapted = builder.temporary_instructions(name, text)
        self.assertNotIn("libtbx.python", adapted)
        for command, count in builder.TEMP_COMMANDS[name]:
            self.assertEqual(adapted.count(builder.TEMP_PREFIX + " " + command.lstrip("`")), count)
        # Control: an interpreter call the rules do not know is refused, not shipped.
        with self.assertRaisesRegex(builder.PackageError, "unadapted interpreter command; inspect " + name):
            builder.temporary_instructions(name, text + "\n`libtbx.python -c pass`\n")

    def test_shell_neutral_env_lines_get_the_shell_neutral_tmpdir_form(self):
        name = REFERENCE
        text = temp_fixture(name).decode().replace("python3 -I -B", "libtbx.python -I -B")
        adapted = builder.temporary_instructions(name, text)
        lines = [line for line in adapted.splitlines() if builder.GENERAL_PYTHON in line]
        self.assertEqual(len(lines), 4)
        for line in lines:
            self.assertTrue(line.startswith('env GC_PAYLOAD_ROOT="`pwd -P`/payload" ' + builder.ENV_TEMP
                                            + " " + builder.PY + " "), line)
            self.assertNotIn("$(", line)  # Not bash-only syntax: the block also runs in csh.
        # Control: a bare python3 on an env line is still refused.
        with self.assertRaisesRegex(builder.PackageError, "unresolved temporary-directory instruction"):
            builder.temporary_instructions(name, text + "\nenv A=b python3 -c pass\n")

    def test_interpreter_name_in_prose_is_allowed_but_not_a_bare_command(self):
        name = "payload/WORKER.md"
        text = temp_fixture(name).decode()
        builder.temporary_instructions(name, text + "\nThe tools run with `python3`.\n")
        for extra in ("\nRun `python3 tool.py`.\n", "\npython3 tool.py\n"):
            with self.subTest(extra=extra), \
                 self.assertRaisesRegex(builder.PackageError, "unresolved temporary-directory instruction"):
                builder.temporary_instructions(name, text + extra)

    def test_verification_history_keeps_the_commands_it_records(self):
        name = "docs/GUIDED_CODING_VERIFICATION.md"
        history = ("## Historical record\n\nRevision 16 used `libtbx.python -I -B` instead of "
                   "`python3 -I -B`; its STOP line was `/ABS/libtbx.python -I -B <auto_queue.py> stop`.\n\n")
        body = temp_fixture(name).decode()
        text = body + history + "## Technical reference\n\nMore.\n"
        adapted = builder.temporary_instructions(name, text)
        self.assertIn(history, adapted)
        self.assertEqual(adapted.count(history), 1)
        # Control: the same sentence outside the historical record is refused.
        with self.assertRaisesRegex(builder.PackageError, "inspect " + re.escape(name)):
            builder.temporary_instructions(name, body + history.split("\n\n", 1)[1])
        # Control (checker D5): the exemption ends at the technical reference.
        with self.assertRaisesRegex(builder.PackageError, "unadapted interpreter command"):
            builder.temporary_instructions(name, text + "Run `libtbx.python payload/x.py`.\n")

    def test_each_general_passage_is_replaced_once_and_a_changed_one_is_refused(self):
        for name, passages in builder.GENERAL_PASSAGES.items():
            for before, after in passages:
                with self.subTest(name=name, before=before[:50]):
                    text = "# Title\n\nUses libtbx.python here.\n\n" + "\n\n".join(b for b, _ in passages) + "\n"
                    adapted = builder.general_passages(name, text)
                    if after and after != before:
                        # Exactly once per listed replacement that contains this text.
                        self.assertEqual(adapted.count(after), sum(a.count(after) for _, a in passages))
                    if after != before:
                        self.assertNotIn(before, adapted)
                    for changed in (text.replace(before, before.replace(" ", "  ", 1), 1),
                                    text.replace(before, "", 1),
                                    text.replace(before, before + "\n" + before, 1)):
                        with self.assertRaisesRegex(builder.PackageError,
                                "required general-edition passage missing or duplicated; inspect " + re.escape(name)):
                            builder.general_passages(name, changed)

    def test_general_passages_leave_no_source_reference(self):
        for name, passages in builder.GENERAL_PASSAGES.items():
            for _, after in passages:
                with self.subTest(name=name, after=after[:50]):
                    self.assertIsNone(builder.GENERAL_REFERENCE.search(after))
                    self.assertNotIn("libtbx.python -", after)

    @patch.dict(builder.TOOL_MESSAGE_QUOTES, {"tests/tst_auto_queue_v20.py": (
        '"REFUSED: requires psutil: run with the cctbx conda Python (libtbx.python) or pip "',)})
    def test_quoted_tool_message_is_kept_and_other_test_names_are_renamed(self):
        # Kit revisions 16-17 quoted such a message; revision 18 needs none.
        name = "tests/tst_auto_queue_v20.py"
        (quote,) = builder.TOOL_MESSAGE_QUOTES[name]
        text = ("MESSAGE = (\n    " + quote + "\n    \"install psutil\")\n"
                "REPO = 'cctbx_project'\nOTHER = 'cctbx conda Python'\n")
        adapted = builder.legacy_general_text(name, text)
        self.assertEqual(adapted.count(quote), 1)
        self.assertIn("REPO = 'companion_project'", adapted)
        self.assertIn("OTHER = 'companion conda Python'", adapted)
        # Control: a changed quotation is not silently renamed.
        with self.assertRaisesRegex(builder.PackageError, "quoted tool message changed; inspect " + re.escape(name)):
            builder.legacy_general_text(name, text.replace("or pip", "or  pip"))
        # The exemption is only for that file.
        with self.assertRaisesRegex(builder.PackageError, "unadapted general-edition reference"):
            builder.legacy_general_text("docs/OTHER.md", quote + "\n")

    def test_installation_note_follows_the_shipped_interpreter_rule(self):
        checker = self.source / "payload/tools/screen_check.py"
        checker.parent.mkdir(parents=True)
        checker.write_text("import re\n" + builder.RESTRICTED_INTERPRETER + "\n" + STOP_LINE)
        self.assertEqual(builder.auto_mode_note(self.source), builder.RESTRICTED_AUTO_NOTE)
        checker.write_text("import re\n")
        self.assertEqual(builder.auto_mode_note(self.source), "")
        checker.write_text('import re\nINTERPRETER = re.compile(r"/.+/python3")\n')
        with self.assertRaisesRegex(builder.PackageError, "auto-mode interpreter rule changed"):
            builder.auto_mode_note(self.source)
        text = builder.installation_text({}, "2.1.281", {"source_manifest_sha256": "0" * 64},
                                         builder.RESTRICTED_AUTO_NOTE).decode()
        self.assertIn("Windows is not supported. Auto mode also needs the\npsutil package", text)

    @patch.dict(builder.TOOL_MESSAGE_QUOTES, {"tests/tst_auto_queue_v20.py": (
        '"REFUSED: requires psutil: run with the cctbx conda Python (libtbx.python) or pip "',)})
    def test_reference_page_may_show_unchanged_tools_but_nothing_else_with_source_names(self):
        edition = self.source
        tool = "MESSAGE = 'run with the cctbx conda Python'\n"
        (edition / "payload/tools").mkdir(parents=True)
        (edition / "payload/tools/screen_check.py").write_text(tool)
        (edition / "docs").mkdir()
        (edition / "docs/NOTE.md").write_text("Plain text.\n")
        (edition / "tests").mkdir()
        (edition / "tests/tst_auto_queue_v20.py").write_text(
            "M = " + builder.TOOL_MESSAGE_QUOTES["tests/tst_auto_queue_v20.py"][0] + "\n")
        blocks = builder.verbatim_blocks(edition)
        self.assertEqual(len(blocks), 2)
        page = ("<section><pre><code>" + html.escape(tool) + "</code></pre></section>"
                "<p>" + html.escape(builder.TOOL_MESSAGE_QUOTES["tests/tst_auto_queue_v20.py"][0]) + "</p>")
        builder.verify_general_documentation({"reference-files.html": page.encode()}, {'commit': 'a' * 40}, blocks)
        # Controls: the same text elsewhere on the page, in another page, or a changed
        # tool text is still refused.
        for name, text in (("reference-files.html", page + "<p>cctbx</p>"),
                           ("reference-files.html", page.replace("conda Python", "conda  Python", 1)),
                           ("overview.html", page)):
            with self.subTest(name=name, text=text[-40:]), self.assertRaises(builder.PackageError):
                builder.verify_general_documentation({name: text.encode()}, {'commit': 'a' * 40}, blocks)
        # Adapted Markdown is never exempt.
        (edition / "docs/NOTE.md").write_text("cctbx\n")
        self.assertEqual(builder.verbatim_blocks(edition), blocks)

    def test_weakened_guards_are_refused(self):
        # Reviewer finding 6: a one-word label, a guard made harmless by `||`,
        # and a checksum command without -c.
        for guard, message in (
                (REVISION_17_GUARD.replace("pilot r10 rev19 '", "'").replace("2\\.0 ", ""),
                 "does not match"),
                (REVISION_17_GUARD.replace("' payload/RELEASE\n", "' payload/RELEASE || true\n"),
                 "no longer guards"),
                (REVISION_17_GUARD.replace("' payload/RELEASE\n", "' payload/RELEASE; true\n"),
                 "no longer guards"),
                (REVISION_17_GUARD + "grep -Eq '^guided_coding ' payload/RELEASE || true\n",
                 "no longer guards"),
                ("shasum -a 256 -c SOURCE_MANIFEST.sha256 &&\n"
                 'GC_PAYLOAD_ROOT="$(pwd -P)/payload" python3 -I -B payload/tools/screen_check.py verify-source . &&\n'
                 "grep -Fq 'guided_coding 2.0 pilot r10 rev19' payload/RELEASE || true\n", "no longer guards"),
                ("shasum -a 256 SOURCE_MANIFEST.sha256 &&\n"
                 'GC_PAYLOAD_ROOT="$(pwd -P)/payload" python3 -I -B payload/tools/screen_check.py verify-source . &&\n'
                 "grep -Fq 'guided_coding 2.0 pilot r10 rev19' payload/RELEASE\n", "no longer guards")):
            with self.subTest(guard=guard[-70:]):
                self.assertNotEqual(guard, REVISION_17_GUARD)
                self.hooks_source(guard)
                with self.assertRaisesRegex(builder.PackageError, message):
                    builder.check_hooks(self.source)

    def test_prefix_doubled_by_the_replacement_is_refused(self):
        # Reviewer finding 2: the source sets TMPDIR itself on a listed command line.
        name = "SKILL.md"
        text = temp_fixture(name).decode().replace(builder.SOURCE_COMMAND, "TMPDIR=/tmp " + builder.SOURCE_COMMAND, 1)
        with self.assertRaisesRegex(builder.PackageError, "doubled temporary-directory prefix; inspect SKILL.md"):
            builder.temporary_instructions(name, text)

    def test_other_unresolved_interpreter_forms_are_refused(self):
        # Reviewer findings 4 and 5.
        name = "payload/WORKER.md"
        text = temp_fixture(name).decode()
        for extra, message in (
                ("Run `libtbx.python payload/tools/screen_check.py check X`.", "unadapted interpreter command"),
                ("Run `python3` -I -B payload/tools/screen_check.py check X.", "unresolved temporary-directory"),
                ('TMPDIR="`cd /tmp && pwd -P`" python3 -I -B x.py', "unresolved temporary-directory")):
            with self.subTest(extra=extra), self.assertRaisesRegex(builder.PackageError, message):
                builder.temporary_instructions(name, text + "\n" + extra + "\n")
        guide = builder.READABLE_HEADERS["docs/GUIDED_CODING_USER_GUIDE.md"] + "\n\nCheck `libtbx.python --version`.\n"
        with self.assertRaisesRegex(builder.PackageError, "unadapted interpreter command"):
            builder.temporary_instructions("docs/GUIDED_CODING_USER_GUIDE.md", guide)

    def test_only_listed_files_may_show_source_names_on_the_reference_page(self):
        # Reviewer finding 3.
        note = "cd /path/to/cctbx_project && libtbx.python x\n"
        (self.source / "payload/templates").mkdir(parents=True)
        (self.source / "payload/templates/NOTE.txt").write_text(note)
        blocks = builder.verbatim_blocks(self.source)
        self.assertEqual(blocks, ())
        page = "<pre><code>" + html.escape(note) + "</code></pre>"
        with self.assertRaisesRegex(builder.PackageError, "unadapted general-edition reference"):
            builder.verify_general_documentation({"reference-files.html": page.encode()},
                                                 {"commit": "a" * 40}, blocks)

    def test_installation_note_needs_exactly_the_restricted_rule(self):
        # Reviewer finding 10: a later redefinition is not hidden by the literal.
        checker = self.source / "payload/tools/screen_check.py"
        checker.parent.mkdir(parents=True)
        checker.write_text(builder.RESTRICTED_INTERPRETER + '\nINTERPRETER = re.compile(r"/.+")\n')
        with self.assertRaisesRegex(builder.PackageError, "auto-mode interpreter rule changed"):
            builder.auto_mode_note(self.source)



class Revision18Rules(unittest.TestCase):
    """Kit revision 18: the venv Python, the approved README section and the
    rules deferred from the revision 17 review."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.source = Path(self.temporary.name).resolve() / "source"

    def test_commands_name_the_virtual_environment_python(self):
        name = "payload/WORKER.md"
        for source_form in ("libtbx.python -I -B", "python3 -I -B"):
            with self.subTest(source_form=source_form):
                text = (builder.TEMP_HEADERS[name] + "\n\n" + "\n\n".join(
                    command.replace(builder.PY, source_form) for command, _ in builder.TEMP_COMMANDS[name]) + "\n")
                adapted = builder.temporary_instructions(name, text)
                self.assertNotIn(source_form, adapted.replace(builder.PY, ""))
                for command, count in builder.TEMP_COMMANDS[name]:
                    self.assertEqual(adapted.count(builder.resolve_temporary(command)), count)
        self.assertEqual(builder.GENERAL_PYTHON, "~/guided_coding_venv/bin/python")
        # Control: an unmapped interpreter form is refused, not shipped.
        with self.assertRaisesRegex(builder.PackageError, "unadapted interpreter command"):
            builder.temporary_instructions(name, text + "\n`/usr/bin/python3 -I -B x.py`\n")

    def test_venv_step_is_allowed_but_other_interpreter_forms_are_refused(self):
        name = "payload/WORKER.md"
        text = temp_fixture(name).decode()
        builder.temporary_instructions(name, text + "\nFirst `python3 -m venv ~/guided_coding_venv`.\n")
        for extra, message in (
                ("Run `python -I -B payload/tools/screen_check.py check X`.", "unadapted interpreter command"),
                ("Run `python3.11 -B x.py`.", "unadapted interpreter command"),
                ("Run `python3 -m pip install psutil`.", "unresolved temporary-directory"),
                ("Run `~/guided_coding_venv/bin/python x.py`.", "unresolved temporary-directory")):
            with self.subTest(extra=extra), self.assertRaisesRegex(builder.PackageError, message):
                builder.temporary_instructions(name, text + "\n" + extra + "\n")

    def test_only_the_exact_approved_where_included_section_is_exempt(self):
        name = "docs/GUIDED_CODING_README.md"
        text = builder.READABLE_HEADERS[name] + "\n\nIntro.\n\n" + builder.INCLUDED_SECTION + "\n## Next\n\nMore.\n"
        self.assertNotIn("cctbx", builder.readable_scan_text(name, text))
        for changed in (text.replace("includes Guided Coding.", "bundles Guided Coding.", 1),
                        text.replace(builder.INCLUDED_SECTION, builder.INCLUDED_SECTION * 2, 1)):
            with self.subTest(changed=changed[:40]), \
                 self.assertRaisesRegex(builder.PackageError, "approved where-included section changed"):
                builder.readable_scan_text(name, changed)
        # The same text elsewhere, without its heading, is not exempt.
        loose = builder.READABLE_HEADERS[name] + "\n\n" + builder.INCLUDED_SECTION.split("\n\n", 1)[1]
        self.assertIsNotNone(builder.GENERAL_REFERENCE.search(builder.readable_scan_text(name, loose)))

    def test_rendered_where_included_section_is_exempt_only_on_the_overview(self):
        info = {"commit": "a" * 40}
        body, _ = builder.render_document("# Overview\n\n" + builder.INCLUDED_SECTION, info)
        builder.verify_general_documentation({"overview.html": body.encode()}, info)
        for name, page in (("architecture.html", body), ("overview.html", body + "<p>cctbx</p>")):
            with self.subTest(name=name), self.assertRaises(builder.PackageError):
                builder.verify_general_documentation({name: page.encode()}, info)

    def test_original_host_and_test_wrapper_names_are_refused_outside_exempt_text(self):
        for text in ("a Linux run (anaconda, October 12)", "run `libtbx/tst_guided_coding.py` too"):
            with self.subTest(text=text):
                self.assertIsNotNone(builder.GENERAL_REFERENCE.search(text))
        self.assertIsNone(builder.GENERAL_REFERENCE.search("an Anaconda-style conda install, anacondas"))

    def test_installation_note_follows_the_revision_18_rule_and_refuses_rebinding(self):
        checker = self.source / "payload/tools/screen_check.py"
        checker.parent.mkdir(parents=True)
        checker.write_text("import re\n" + builder.GENERAL_INTERPRETER + "\n" + STOP_LINE)
        self.assertEqual(builder.auto_mode_note(self.source), builder.GENERAL_AUTO_NOTE)
        for extra in ('    INTERPRETER = re.compile(r"/.+")\n', 'globals()["INTERPRETER"] = None\n'):
            with self.subTest(extra=extra):
                checker.write_text("import re\n" + builder.GENERAL_INTERPRETER + "\n" + STOP_LINE + extra)
                with self.assertRaisesRegex(builder.PackageError, "auto-mode interpreter rule changed"):
                    builder.auto_mode_note(self.source)
        # Reviewer finding 3: other forms of rebinding, and a stop_line that ignores the rule.
        for extra in ('INTERPRETER: re.Pattern = re.compile(r"/.+")\n', '(INTERPRETER := None)\n',
                      'INTERPRETER, X = None, None\n', "setattr(object, 'INTER' 'PRETER', None)\n"):
            with self.subTest(extra=extra):
                checker.write_text("import re\n" + builder.GENERAL_INTERPRETER + "\n" + STOP_LINE + extra)
                with self.assertRaisesRegex(builder.PackageError, "auto-mode interpreter rule changed"):
                    builder.auto_mode_note(self.source)
        checker.write_text("import re\n" + builder.GENERAL_INTERPRETER + "\ndef stop_line(x):\n    return True\n")
        with self.assertRaisesRegex(builder.PackageError, "auto-mode interpreter rule changed"):
            builder.auto_mode_note(self.source)

    def test_guard_block_with_a_harmless_checksum_command_is_refused(self):
        guard = REVISION_17_GUARD.replace(
            "if command -v shasum >/dev/null 2>&1; then shasum -a 256 -c SOURCE_MANIFEST.sha256; "
            "else sha256sum -c SOURCE_MANIFEST.sha256; fi &&",
            "if command -v shasum >/dev/null 2>&1; then shasum -a 256 -c x; echo SOURCE_MANIFEST.sha256; "
            "else sha256sum -c SOURCE_MANIFEST.sha256; fi &&")
        self.assertNotEqual(guard, REVISION_17_GUARD)
        Revision17Rules.hooks_source(self, guard)
        with self.assertRaisesRegex(builder.PackageError, "no longer guards"):
            builder.check_hooks(self.source)

    def test_download_form_of_the_guard_block_is_accepted_and_still_exact(self):
        # The builder rechecks the hooks on the adapted download copy.
        fixture = temp_fixture("SKILL.md").decode()
        block = "```bash\n" + builder.SOURCE_COMMAND + "```"
        self.assertEqual(fixture.count(block), 1)
        source = fixture.replace(block, "```bash\n" + REVISION_17_GUARD + "```")
        adapted = builder.temporary_instructions("SKILL.md", builder.legacy_general_text("SKILL.md", source))
        guard = adapted[adapted.index("```bash\n") + 8:adapted.rindex("```\n")]
        self.assertIn("cd " + builder.INSTALL_ROOT + " &&", guard)
        Revision17Rules.hooks_source(self, guard)
        self.assertEqual(builder.check_hooks(self.source), (2, 1, 281))
        Revision17Rules.hooks_source(self, guard.replace("fi &&\n", "fi ||\n"))
        with self.assertRaisesRegex(builder.PackageError, "no longer guards"):
            builder.check_hooks(self.source)

    def test_other_interpreter_paths_and_bare_names_are_refused(self):
        # Reviewer findings 1, 6 and 7: only the exact venv Python may run a tool.
        name = "payload/WORKER.md"
        text = temp_fixture(name).decode()
        for extra, message in (
                ('Run `/usr/bin/python3 -I -B "$GC_PAYLOAD_ROOT/tools/screen_check.py" freeze DIR`.', "unadapted interpreter command"),
                ("use `/opt/build/conda_base/bin/python3 -I -B payload/tools/screen_check.py verify-source .`", "unadapted interpreter command"),
                ("Run `python3 -m venv /tmp/v && /tmp/v/bin/python -I -B x.py`.", "unadapted interpreter command"),
                ("Run `DIR/bin/python -I -B x.py`.", "unadapted interpreter command"),
                ("Run `~/other/bin/python -I -B x.py`.", "unadapted interpreter command"),
                ("Run `python payload/tools/screen_check.py check X`.", "unresolved temporary-directory"),
                ("Then `python3 -m venv v && python x.py`.", "unresolved temporary-directory")):
            with self.subTest(extra=extra), self.assertRaisesRegex(builder.PackageError, message):
                builder.temporary_instructions(name, text + "\n" + extra + "\n")

    def test_guard_block_must_be_exact_whenever_the_release_check_is_present(self):
        # Reviewer finding 2: a checksum that cannot fail, or a second checker run.
        for guard in (
                REVISION_17_GUARD.replace(
                    "if command -v shasum >/dev/null 2>&1; then shasum -a 256 -c SOURCE_MANIFEST.sha256; "
                    "else sha256sum -c SOURCE_MANIFEST.sha256; fi &&", "true || shasum -a 256 -c SOURCE_MANIFEST.sha256 &&"),
                REVISION_17_GUARD + "```\n\n```bash\n"
                'GC_PAYLOAD_ROOT="$(pwd -P)/payload" libtbx.python -I -B payload/tools/screen_check.py verify-source .\n'):
            with self.subTest(guard=guard[-80:]):
                Revision17Rules.hooks_source(self, guard)
                with self.assertRaisesRegex(builder.PackageError, "no longer guards"):
                    builder.check_hooks(self.source)

    def test_test_literals_that_check_the_tool_message_stay_exact(self):
        # Reviewer finding 4: the shipped test checks that the message does not name cctbx.
        name = "tests/tst_auto_queue_v20.py"
        text = ("# no longer names cctbx\n"
                "def test_psutil_message_names_this_python_and_not_cctbx(self):\n"
                '    """... and does not name cctbx."""\n'
                '    self.assertNotIn("cctbx", result.stderr)\n'
                '    self.assertNotIn("cctbx", PSUTIL_MESSAGE)\n'
                "REPO = 'cctbx_project'\n")
        adapted = builder.legacy_general_text(name, text)
        self.assertEqual(adapted.count('self.assertNotIn("cctbx"'), 2)
        self.assertIn("REPO = 'companion_project'", adapted)

    def test_exactly_one_guard_block_and_text_after_the_section_is_scanned(self):
        # Checker gaps M4a and M3b.
        Revision17Rules.hooks_source(self, REVISION_17_GUARD + "```\n\n```bash\n" + REVISION_17_GUARD)
        with self.assertRaisesRegex(builder.PackageError, "no longer guards"):
            builder.check_hooks(self.source)
        name = "docs/GUIDED_CODING_README.md"
        text = (builder.READABLE_HEADERS[name] + "\n\n" + builder.INCLUDED_SECTION
                + "Added: see cctbx_project too.\n\n## Next\n")
        self.assertIsNotNone(builder.GENERAL_REFERENCE.search(builder.readable_scan_text(name, text)))

    def test_short_interpreter_forms_are_mapped_too(self):
        # Checker gaps M1b and M1d: `-B` without `-I`.
        name = "payload/WORKER.md"
        text = temp_fixture(name).decode()
        for source_form in ("libtbx.python -B ", "python3 -B "):
            with self.subTest(source_form=source_form):
                adapted = builder.temporary_instructions(
                    name, text + "\n`" + builder.TEMP_PREFIX + " " + source_form + "-m unittest x`\n")
                self.assertIn(builder.TEMP_PREFIX + " " + builder.GENERAL_PYTHON + " -B -m unittest x", adapted)


class Revision19Checks(unittest.TestCase):
    """Inputs the revision 18 builder accepted that the independent checker
    found unsafe: interpreter forms, pre-revision-13 and second guard blocks,
    and other ways to rebind or bypass the auto-mode interpreter rule."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.source = Path(self.temporary.name).resolve() / "source"

    def test_chained_prefixed_indented_and_path_qualified_python_is_refused(self):
        # Checker criterion A: only the exact venv Python may run a tool.
        name = "payload/WORKER.md"
        text = temp_fixture(name).decode()
        bare = "unresolved temporary-directory instruction; inspect " + re.escape(name)
        qualified = "unadapted interpreter command; inspect " + re.escape(name)
        for extra, message in (
                ("Run `x || python x.py`.", bare),
                ("Run `x | python x.py`.", bare),
                ("Run `$(python x.py)`.", bare),
                ("Run `sudo python x.py`.", bare),
                ("  python x.py", bare),
                ("/usr/bin/python x.py", qualified),
                ("/usr/bin/python -s -I x.py", qualified)):
            with self.subTest(extra=extra), self.assertRaisesRegex(builder.PackageError, message):
                builder.temporary_instructions(name, text + "\n" + extra + "\n")
        # Controls: the venv step and the interpreter named in prose stay accepted.
        for extra in ("Plain harmless line.",
                      "First `python3 -m venv ~/guided_coding_venv`.",
                      "The tools run with `python`.",
                      "The tools run with `python3`.",
                      "It needs a module which <python> does not have.",
                      "Name `DIR/bin/python` (the venv Python)."):
            with self.subTest(control=extra):
                builder.temporary_instructions(name, text + "\n" + extra + "\n")

    def test_pre_revision_13_guard_with_a_checksum_that_cannot_fail_is_refused(self):
        # Checker criterion B1: `true ||` makes the checksum harmless.
        guard = ("true || shasum -a 256 -c SOURCE_MANIFEST.sha256 &&\n"
                 'GC_PAYLOAD_ROOT="$(pwd -P)/payload" python3 -I -B payload/tools/screen_check.py verify-source . &&\n'
                 "grep -Fq 'guided_coding 2.0 pilot r10 rev19' payload/RELEASE\n")
        Revision17Rules.hooks_source(self, guard)
        with self.assertRaisesRegex(builder.PackageError, "no longer guards source execution"):
            builder.check_hooks(self.source)

    def test_second_checker_block_with_other_whitespace_is_refused(self):
        # Checker criterion B2: the exact guard plus a second run spelled with
        # two spaces or a tab before verify-source.
        for gap in ("  ", "\t"):
            guard = (REVISION_17_GUARD + "```\n\n```bash\n"
                     'GC_PAYLOAD_ROOT="$(pwd -P)/payload" libtbx.python -I -B payload/tools/screen_check.py'
                     + gap + "verify-source .\n")
            with self.subTest(gap=gap):
                Revision17Rules.hooks_source(self, guard)
                with self.assertRaisesRegex(builder.PackageError, "no longer guards source execution"):
                    builder.check_hooks(self.source)

    def test_other_rebinding_and_bypassing_stop_line_forms_are_refused(self):
        # Checker criterion B3.
        checker = self.source / "payload/tools/screen_check.py"
        checker.parent.mkdir(parents=True)
        # Controls: the kit's stop_line form with either shipped rule gives its note.
        for rule, note in ((builder.GENERAL_INTERPRETER, builder.GENERAL_AUTO_NOTE),
                           (builder.RESTRICTED_INTERPRETER, builder.RESTRICTED_AUTO_NOTE)):
            with self.subTest(rule=rule[:40]):
                checker.write_text("import re\n" + rule + "\n" + STOP_LINE)
                self.assertEqual(builder.auto_mode_note(self.source), note)
        # Control: early `return False` guards before the check, as in the kit, are accepted.
        checker.write_text("import re\n" + builder.GENERAL_INTERPRETER + "\n"
                           "def stop_line(line):\n    if not line:\n        return False\n"
                           "    if line.startswith('#'):\n        return False\n"
                           "    if not INTERPRETER.fullmatch(line):\n        return False\n    return True\n")
        self.assertEqual(builder.auto_mode_note(self.source), builder.GENERAL_AUTO_NOTE)
        for extra in ("globals().update(INTERPRETER=None)\n",
                      "setattr(mod, 'INTER' + 'PRETER', None)\n",
                      "from re import compile as INTERPRETER\n",
                      "def INTERPRETER():\n    pass\n",
                      "def stop_line(line):\n    return True\n"):
            with self.subTest(extra=extra):
                checker.write_text("import re\n" + builder.GENERAL_INTERPRETER + "\n" + STOP_LINE + extra)
                with self.assertRaisesRegex(builder.PackageError, "auto-mode interpreter rule changed"):
                    builder.auto_mode_note(self.source)
        # A sole stop_line that calls the rule but ignores its result, and one
        # that can return True before the check.
        for stop_line in ("def stop_line(x):\n    INTERPRETER.fullmatch(x)\n    return True\n",
                          "def stop_line(line):\n    if line:\n        return True\n"
                          "    if not INTERPRETER.fullmatch(line):\n        return False\n    return True\n"):
            with self.subTest(stop_line=stop_line):
                checker.write_text("import re\n" + builder.GENERAL_INTERPRETER + "\n" + stop_line)
                with self.assertRaisesRegex(builder.PackageError, "auto-mode interpreter rule changed"):
                    builder.auto_mode_note(self.source)

    def test_bare_interpreter_names_after_any_shell_word_are_refused(self):
        # Reviewer class "bare interpreter name": a bare python, python2, python3,
        # python3.N, pypy or pypy3 is refused wherever it can run.
        name = "payload/WORKER.md"
        text = temp_fixture(name).decode()
        bare = "unresolved temporary-directory instruction; inspect " + re.escape(name)
        qualified = "unadapted interpreter command; inspect " + re.escape(name)
        for extra, message in (
                ("Run `x ||  python x.py`.", bare),
                ("Run `x &&python x.py`.", bare),
                ("Run `x;python x.py`.", bare),
                ("Run `x & python x.py`.", bare),
                ("Run `exec python x.py`.", bare),
                ("Run `env python x.py`.", bare),
                ("Run `/usr/bin/env python x.py`.", bare),
                ("Run `nohup python x.py`.", bare),
                ("Run `command python x.py`.", bare),
                ("Run `time python x.py`.", bare),
                ("Run `xargs python x.py`.", bare),
                ("Run `doas python x.py`.", bare),
                ("Run `sudo -E python x.py`.", bare),
                ("Run `sudo  python x.py`.", bare),
                ("Run `(python x.py)`.", bare),
                ("Run `{ python x.py; }`.", bare),
                ("Run `FOO=1 python x.py`.", bare),
                ("Run `if x; then python x.py; fi`.", bare),
                ("Run `bash -c 'python x.py'`.", bare),
                ('Run `"python" x.py`.', bare),
                ("Run `\\python x.py`.", bare),
                ("Run `python2 x.py`.", bare),
                ("Run `pypy3 x.py`.", bare),
                ("Run `python2.7 x.py`.", bare),
                ("Run `pypy3.10 x.py`.", bare),
                ("Run `python3m x.py`.", bare),
                ("/usr/bin/python2 x.py", qualified),
                ("/opt/pypy3 x.py", qualified),
                ("/usr/bin/python\\\n    x.py", qualified),
                ("/usr/bin/python2.7 x.py", qualified),
                ("/opt/pypy/bin/pypy3.10 x.py", qualified),
                ("/usr/bin/python3m x.py", qualified),
                ("/usr/bin/python\tx.py", qualified)):
            with self.subTest(extra=extra), self.assertRaisesRegex(builder.PackageError, message):
                builder.temporary_instructions(name, text + "\n" + extra + "\n")
        # Controls: the earlier accepted prose and venv step stay accepted.
        for extra in ("Plain harmless line.",
                      "First `python3 -m venv ~/guided_coding_venv`.",
                      "The tools run with `python`.",
                      "The tools run with `python3`.",
                      "It needs a module which <python> does not have.",
                      "Name `DIR/bin/python` (the venv Python)."):
            with self.subTest(control=extra):
                builder.temporary_instructions(name, text + "\n" + extra + "\n")

    def test_only_one_plain_interpreter_rule_and_stop_line_are_accepted(self):
        # Reviewer class "only one plain INTERPRETER and stop_line".
        checker = self.source / "payload/tools/screen_check.py"
        checker.parent.mkdir(parents=True)
        rule = builder.GENERAL_INTERPRETER + "\n"
        for source in (
                "import re\n" + rule + STOP_LINE + "import sys\nsys.modules[__name__].INTERPRETER = re.compile('.*')\n",
                "import re\n" + rule + STOP_LINE + "import __main__ as M\nM.INTERPRETER = re.compile('.*')\n",
                "import re\n" + rule + STOP_LINE + "match re.compile('.*'):\n    case INTERPRETER:\n        pass\n",
                "import re\n" + rule + STOP_LINE + "import builtins\nbuiltins.globals()['INTER' + 'PRETER'] = None\n",
                "import re\n" + rule + STOP_LINE + "import builtins as B\nB.exec('x = 1')\n",
                "import re\n" + rule + STOP_LINE + "import builtins\ngetattr(builtins, 'ex' + 'ec')('x = 1')\n",
                "import re\n" + rule + STOP_LINE + "import sys\nsys._getframe().f_globals['X'] = 1\n",
                # Other bindings of the name stop_line.
                "import re\n" + rule + STOP_LINE + "stop_line = lambda line: True\n",
                "import re\n" + rule + STOP_LINE + "from os import path as stop_line\n",
                "import re\n" + rule + STOP_LINE + "def other(stop_line=None):\n    return stop_line\n",
                "import re\nre.compile = lambda *a: None\n" + rule + STOP_LINE,
                # Frame, module-dictionary and reflection access (checker round 3).
                "import re\n" + rule + STOP_LINE
                + 'import inspect\ninspect.currentframe().f_locals["INTER" + "PRETER"] = re.compile(".*")\n',
                "import re\n" + rule + STOP_LINE + 'import sys\ngetattr(getattr(sys, "modules")[__name__], '
                '"__dict__")["INTER" + "PRETER"] = re.compile(".*")\n',
                "import re\n" + rule + STOP_LINE
                + 'import inspect\ninspect.stack()[0].frame.f_locals.update({"INTER" + "PRETER": None})\n',
                "import re\n" + rule + STOP_LINE + "x = vars()\n",
                "import re\n" + rule + STOP_LINE + 'eval("1")\n',
                "import re\n" + rule + STOP_LINE + "y = object.__dict__\n",
                "import re\n" + rule + STOP_LINE + 'object.__setattr__(object, "a", 1)\n',
                "import re\n" + rule + STOP_LINE + "from builtins import setattr as s\n",
                # A module other than re, or re rebound after the rule.
                "import evil as re\n" + rule + STOP_LINE,
                "import regex as re\n" + rule + STOP_LINE,
                "import re\n" + rule + STOP_LINE + "re = None\n",
                "import re\n" + rule + STOP_LINE + "from os import path as re\n",
                # A single plain rule with a pattern the builder does not know.
                'import re\nINTERPRETER = re.compile(r"/.+/other")\n' + STOP_LINE,
                # stop_line variants: a decorator, a generator and a constant argument.
                "import re\n" + rule + "def always(f):\n    return lambda line: True\n@always\n" + STOP_LINE,
                "import re\n" + rule + STOP_LINE.replace("    return True\n", "    yield line\n    return True\n"),
                "import re\n" + rule + STOP_LINE.replace("fullmatch(line)", "fullmatch('/a/python')"),
                "import re\n" + rule + STOP_LINE.replace("fullmatch(line)", "fullmatch(string=line)"),
                "import re\n" + rule + STOP_LINE.replace("fullmatch(line)", "fullmatch(line, pos=1)")):
            with self.subTest(source=source.replace(rule, "<rule>\n")):
                checker.write_text(source)
                with self.assertRaisesRegex(builder.PackageError, "auto-mode interpreter rule changed"):
                    builder.auto_mode_note(self.source)
        # Control: the plain rule and the kit's stop_line give the note.
        checker.write_text("import re\n" + rule + STOP_LINE)
        self.assertEqual(builder.auto_mode_note(self.source), builder.GENERAL_AUTO_NOTE)
        # Control: a main guard after them, as in the kit, is accepted too.
        checker.write_text("import re\n" + rule + STOP_LINE + 'if __name__ == "__main__":\n    pass\n')
        self.assertEqual(builder.auto_mode_note(self.source), builder.GENERAL_AUTO_NOTE)


class ScriptModeRunsEveryTest(unittest.TestCase):
    def test_no_test_class_follows_the_script_entry_point(self):
        # Reviewer finding 1: a class after the main guard is skipped in script mode.
        import ast
        tree = ast.parse(Path(__file__).read_text())
        guard = next(index for index, node in enumerate(tree.body) if isinstance(node, ast.If))
        self.assertFalse([node.name for node in tree.body[guard:] if isinstance(node, ast.ClassDef)])


if __name__ == "__main__":
    unittest.main()
