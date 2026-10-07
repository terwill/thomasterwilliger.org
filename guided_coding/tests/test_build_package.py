"""Downstream packaging controls. No network, credentials or user configuration."""

import hashlib
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


def manifest(files):
    return "".join(f"{hashlib.sha256(data).hexdigest()}  ./{name}\n"
                   for name, data in sorted(files.items())).encode()


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
        for name in ("index.template.html", "docs.template.html", "GENERAL_DEVELOPER_CARD.md"):
            (site / name).write_bytes((SCRIPT.parent / name).read_bytes())
        files = {p.relative_to(self.source).as_posix(): p.read_bytes()
                 for p in self.source.rglob("*") if p.is_file() and p.name != "SOURCE_MANIFEST.sha256"}
        files.update({"docs/" + name: b"# Fixture guide\n\n## Read this\n\nExample paragraph.\n"
                      for name, _, _, _ in builder.DOCUMENTS})
        self.write_source(files)
        info = {"commit": "a" * 40, "commit_date": "2026-10-06T20:03:57Z",
                "source_manifest_sha256": builder.digest(
                    (self.source / "SOURCE_MANIFEST.sha256").read_bytes()),
                "source_files": len(files) + 1, "license_sha256": builder.digest(b"license")}
        return site, old, info

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
            builder.documentation_link('https://github.com/cctbx/cctbx_project', info)

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
        self.write_source({'SKILL.md': b'cd /absolute/path/to/libtbx/guided_coding &&\n',
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
                     '# Title\ncd /unknown/prefix/cctbx_project/libtbx/guided_coding\n'):
            with self.subTest(text=text), self.assertRaisesRegex(builder.PackageError, 'unadapted'):
                builder.general_text('docs/new.md', text)

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
            '# Guide\n\n```text\nPlease set up GuidedCoding from /absolute/path/to/cctbx_project/libtbx/guided_coding for this machine.\n```\n').encode()
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
            self.assertIn(metadata['general_edition']['source_manifest_sha256'], install)
            self.assertNotIn('GuidedCoding/LICENSE.cctbx.txt', archive.namelist())
        for name, data in outputs.items():
            if name.endswith('.html') and name != 'documentation.html':
                self.assertNotRegex(data.decode(), r'(?i)cctbx|/absolute/path/to|~/Documents/GuidedCoding')

    def test_invalid_documentation_build_preserves_existing_output_set(self):
        site, old, info = self.build_fixture()
        files = {p.relative_to(self.source).as_posix(): p.read_bytes()
                 for p in self.source.rglob('*') if p.is_file() and p.name != 'SOURCE_MANIFEST.sha256'}
        files['docs/GUIDED_CODING_USER_GUIDE.md'] = b'# New guide\n\n> Unsupported new syntax\n'
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

    def test_final_documentation_scan_allows_only_the_exact_historical_note(self):
        info = {'commit': 'a' * 40}
        note = builder.historical_note(info).encode()
        builder.verify_general_documentation({'documentation.html': note}, info)
        for filename, data in (
            ('index.html', b'<p>cctbx_project</p>'),
            ('user-guide.html', b'<a href="https://example.invalid/CCTBX">guide</a>'),
            ('reference-files.html', b'<p>cc&#116;bx</p>'),
            ('INSTALL.md', b'Use cCtBx here.'),
            ('GENERAL_DEVELOPER_CARD.md', b'Use /absolute/path/to/project.'),
            ('documentation.html', note + b'<p>cctbx</p>'),
            ('index.html', note),
            ('README.md', b'Use cctbx_project/libtbx/guided_coding/.'),
        ):
            with self.subTest(filename=filename, data=data), self.assertRaisesRegex(builder.PackageError, 'unadapted'):
                builder.verify_general_documentation({filename: data}, info)
        for data in (note + note, note.replace(b'began', b'started')):
            with self.subTest(data=data), self.assertRaisesRegex(builder.PackageError, 'historical attribution'):
                builder.verify_general_documentation({'documentation.html': data}, info)

    def test_leftover_template_or_installer_reference_refuses_without_replacing_outputs(self):
        site, old, info = self.build_fixture()
        original_templates = {name: (site / name).read_bytes()
                              for name in ('index.template.html', 'docs.template.html')}
        install = builder.installation_text
        for target in ('index.template.html', 'docs.template.html', 'INSTALL.md',
                       'GENERAL_DEVELOPER_CARD.md', 'README.md'):
            with self.subTest(target=target), tempfile.TemporaryDirectory(dir=self.root) as directory:
                for name, data in original_templates.items():
                    (site / name).write_bytes(data)
                (site / 'GENERAL_DEVELOPER_CARD.md').write_bytes((SCRIPT.parent / 'GENERAL_DEVELOPER_CARD.md').read_bytes())
                (site / 'README.md').write_bytes(b'# Maintenance\n')
                if target in original_templates:
                    (site / target).write_bytes(original_templates[target].replace(
                        b'</main>', b'<p>Unexpected CCTBX instructions.</p></main>'))
                elif target != 'INSTALL.md':
                    (site / target).write_bytes(b'# Instructions\nUnexpected cctbx reference.\n')
                with patch.object(builder, 'check_hooks', return_value=(2, 1, 281)), \
                     patch.object(builder, 'run_contract_checks', return_value={}), \
                     patch.object(builder, 'run_package_tests', return_value=[]), \
                     patch.object(builder, 'installation_text', side_effect=lambda *args:
                                  install(*args) + (b'Unexpected cctbx reference.\n' if target == 'INSTALL.md' else b'')), \
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
        for name in ("index.template.html", "docs.template.html", "GENERAL_DEVELOPER_CARD.md"):
            (site / name).write_bytes((SCRIPT.parent / name).read_bytes())
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


if __name__ == "__main__":
    unittest.main()
