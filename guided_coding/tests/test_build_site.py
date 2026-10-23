"""Tests of build_site.py. They use temporary folders, no network, and a small fake GuidedCoding source.
Run from the website checkout: python3 -B -m unittest discover -s guided_coding/tests -v
"""
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import build_site as b  # noqa: E402

SKILL = """---
name: gc
description: test
disable-model-invocation: true
---

# GuidedCoding (version 1.3)

See BATCH.md section.
"""


def fake_source(root, test_ok=True):
    """A Git repository shaped like cctbx/guided_coding, with one commit. Returns (path, commit)."""
    os.makedirs(os.path.join(root, "guided_coding"))
    files = {"README.md": "# GuidedCoding\n\nSee [EVIDENCE.md](EVIDENCE.md) and [the skill](guided_coding/SKILL.md).\n",
             "EVIDENCE.md": "# Evidence\n\n| a | b |\n|---|---|\n| 1 | 2 |\n",
             "LICENSE.txt": "licence\n",
             "tst_guided_coding.py": "print('OK')\n" if test_ok else "import sys\nprint('FAIL: x')\nsys.exit(1)\n"}
    for name in b.SKILL_FILES:
        files["guided_coding/" + name] = SKILL if name == "SKILL.md" else "# %s\n\nVersion 1.3.\n" % name
    for name, text in files.items():
        with open(os.path.join(root, name), "w") as f:
            f.write(text)
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@localhost", GIT_COMMITTER_NAME="t",
               GIT_COMMITTER_EMAIL="t@localhost", GIT_CONFIG_GLOBAL="/dev/null")
    for args in (["init", "-q"], ["add", "-A"], ["commit", "-q", "-m", "test"],
                 ["update-ref", "refs/remotes/origin/master", "HEAD"]):
        subprocess.run(["git", "-C", root] + args, check=True, env=env)
    commit = subprocess.run(["git", "-C", root, "rev-parse", "HEAD"], capture_output=True, text=True,
                            check=True).stdout.strip()
    return root, commit


class RenderTests(unittest.TestCase):
    def test_lists_with_nested_code(self):
        md = "# T\n\n- **One.** first\n  second line\n\n  ```\n  code here\n  ```\n- Two\n\n1. a\n2. b\n"
        _, body, _ = b.render(md)
        self.assertIn("<ul><li><strong>One.</strong> first second line<pre><code>code here\n</code></pre></li>"
                      "<li>Two</li></ul>", body)
        self.assertIn("<ol><li>a</li><li>b</li></ol>", body)

    def test_table_heading_and_toc(self):
        _, body, toc = b.render("# T\n\n## Part one\n\n| x | y |\n| --- | --- |\n| `a` | b |\n")
        self.assertIn('<h2 id="part-one">', body)
        self.assertIn("<td><code>a</code></td>", body)
        self.assertEqual(len(toc), 1)

    def test_blockquote(self):
        _, body, _ = b.render("# T\n\n> **Bold.** quoted\n>\n> second\n")
        self.assertIn("<blockquote", body)
        self.assertIn("<strong>Bold.</strong>", body)

    def test_html_is_escaped(self):
        _, body, _ = b.render("# T\n\n<script>alert(1)</script>\n")
        self.assertNotIn("<script>", body)

    def test_copy_block_only_on_website_pages(self):
        md = "# T\n\n```copy\ntext\n```\n"
        with self.assertRaises(b.BuildError):
            b.render(md)
        self.assertIn('id="copy-text"', b.render(md, allow_copy=True)[1])

    def test_title_required_and_unsupported_blocks_refused(self):
        with self.assertRaises(b.BuildError):
            b.render("no title\n")
        with self.assertRaises(b.BuildError):
            b.render("# T\n\n    indented code\n")

    def test_stray_hash_lines_and_unsupported_inline_forms_refused(self):
        for md in ("# T\n\n# second title\n", "# T\n\n##### deep\n", "# T\n\n#5 is fixed\n",
                   "# T\n\nsome _emphasis_ here\n", "# T\n\nsee <https://x.org>\n", "# T\n\na &amp; b\n"):
            with self.assertRaises(b.BuildError, msg=md):
                b.render(md)

    def test_list_start_paragraphs_and_escaped_pipe(self):
        _, body, _ = b.render("# T\n\n3. c\n4. d\n\n- a\n\n  second paragraph\n- b\n\n| x |\n| --- |\n| a \\| b |\n")
        self.assertIn('<ol start="3"><li>c</li><li>d</li></ol>', body)
        self.assertIn("<li>a<p>second paragraph</p></li><li>b</li>", body)
        self.assertIn("<td>a | b</td>", body)

    def test_link_targets(self):
        self.assertEqual(b.link_target("EVIDENCE.md"), "verification.html")
        self.assertEqual(b.link_target("guided_coding/SKILL.md"), "reference-files.html#skill-md")
        self.assertEqual(b.link_target("how-it-works.html"), "how-it-works.html")
        self.assertTrue(b.link_target("tst_guided_coding.py").startswith(b.REPO_URL))


class BuildTests(unittest.TestCase):
    def build(self, test_ok=True, source=None):
        scratch = tempfile.mkdtemp()
        source, commit = source or fake_source(os.path.join(scratch, "src"), test_ok)
        tree, date = b.fetch_source(commit, source, scratch)
        b.check_source(tree)
        staging = os.path.join(scratch, "staging")
        os.makedirs(staging)
        meta = b.build(tree, commit, date, staging)
        b.check_links(staging)
        return staging, meta

    def test_full_build_and_deterministic_zip(self):
        source = fake_source(os.path.join(tempfile.mkdtemp(), "src"))
        staging, meta = self.build(source=source)
        for name in b.OUTPUTS:
            self.assertTrue(os.path.isfile(os.path.join(staging, name)), name)
        with zipfile.ZipFile(os.path.join(staging, b.ZIP_NAME)) as z:
            self.assertEqual(len(z.namelist()), len(b.ZIP_FILES))
        _, meta2 = self.build(source=source)
        self.assertEqual(meta["archive"]["sha256"], meta2["archive"]["sha256"])

    def test_checksums_agree(self):
        staging, meta = self.build()
        with open(os.path.join(staging, b.ZIP_NAME), "rb") as f:
            actual = b.sha256(f.read())
        with open(os.path.join(staging, b.ZIP_NAME + ".sha256")) as f:
            self.assertTrue(f.read().startswith(actual))
        with open(os.path.join(staging, "index.html")) as f:
            self.assertIn(actual, f.read())
        self.assertEqual(meta["archive"]["sha256"], actual)
        for page, digest in meta["pages"].items():
            with open(os.path.join(staging, page), "rb") as f:
                self.assertEqual(b.sha256(f.read()), digest, page)

    def test_unpublished_commit_refused(self):
        scratch = tempfile.mkdtemp()
        source, commit = fake_source(os.path.join(scratch, "src"))
        subprocess.run(["git", "-C", source, "update-ref", "-d", "refs/remotes/origin/master"], check=True)
        with self.assertRaises(b.BuildError):
            b.fetch_source(commit, source, scratch)

    def test_check_only_end_to_end(self):
        scratch = tempfile.mkdtemp()
        source, commit = fake_source(os.path.join(scratch, "src"))
        site = tempfile.mkdtemp()
        for name in ("docs.template.html", "index.template.html", "main-page.md"):
            with open(os.path.join(b.HERE, name)) as f, open(os.path.join(site, name), "w") as g:
                g.write(f.read())
        os.makedirs(os.path.join(site, "pages"))
        for name in os.listdir(os.path.join(b.HERE, "pages")):
            with open(os.path.join(b.HERE, "pages", name)) as f, open(os.path.join(site, "pages", name), "w") as g:
                g.write(f.read())
        old_here = b.HERE
        try:
            b.HERE = site
            self.assertEqual(b.main(["--ref", commit, "--source-dir", source, "--check-only"]), 0)
            self.assertFalse(os.path.exists(os.path.join(site, "index.html")))
        finally:
            b.HERE = old_here

    def test_failing_source_test_refuses(self):
        with self.assertRaises(b.BuildError):
            self.build(test_ok=False)

    def test_short_ref_refused(self):
        with self.assertRaises(b.BuildError):
            b.fetch_source("abc123", None, tempfile.mkdtemp())

    def test_broken_anchor_is_caught(self):
        staging, _ = self.build()
        with open(os.path.join(staging, "index.html"), "a") as f:
            f.write('<a href="how-it-works.html#no-such-anchor">x</a>')
        with self.assertRaises(b.BuildError):
            b.check_links(staging)

    def test_replace_keeps_previous_outputs(self):
        staging, _ = self.build()
        site = tempfile.mkdtemp()
        old_here = b.HERE
        try:
            b.HERE = site
            with open(os.path.join(site, "index.html"), "w") as f:
                f.write("old")
            b.replace_outputs(staging)
            (generation,) = os.listdir(os.path.join(site, ".previous"))
            with open(os.path.join(site, ".previous", generation, "index.html")) as f:
                self.assertEqual(f.read(), "old")
            with open(os.path.join(site, "index.html")) as f:
                self.assertNotEqual(f.read(), "old")
        finally:
            b.HERE = old_here

    def old_site(self):
        site = tempfile.mkdtemp()
        for name in b.OUTPUTS[:-1]:
            with open(os.path.join(site, name), "w") as f:
                f.write("old " + name)
        return site

    def assert_old_set(self, site):
        for name in b.OUTPUTS[:-1]:
            with open(os.path.join(site, name)) as f:
                self.assertEqual(f.read(), "old " + name, name)
        self.assertFalse(os.path.exists(os.path.join(site, b.OUTPUTS[-1])))
        self.assertFalse([n for n in os.listdir(site) if n.endswith((".new", ".restoring"))])

    def test_interrupted_replacement_restores_previous_set(self):
        staging, _ = self.build()
        site = self.old_site()
        old_here, real_replace = b.HERE, os.replace
        calls = []

        def failing_replace(src, dst):
            calls.append(src)
            if len(calls) == 2:
                raise OSError("injected failure")
            real_replace(src, dst)
        try:
            b.HERE = site
            b.os.replace = failing_replace
            with self.assertRaises(b.BuildError):
                b.replace_outputs(staging)
            b.os.replace = real_replace
            self.assert_old_set(site)
            b.replace_outputs(staging)  # a second run straight after works, with its own backup folder
            b.replace_outputs(staging)
            self.assertEqual(len(os.listdir(os.path.join(site, ".previous"))), 3)
        finally:
            b.HERE, b.os.replace = old_here, real_replace

    def test_mismatched_result_is_restored(self):
        staging, _ = self.build()
        site = self.old_site()
        old_here, real_hash = b.HERE, b.file_hash
        try:
            b.HERE = site
            seen = []

            def wrong_once(path):  # the first check of the new index.html sees a mismatch
                if path == os.path.join(site, "index.html") and not seen:
                    seen.append(path)
                    return "x"
                return real_hash(path)
            b.file_hash = wrong_once
            with self.assertRaises(b.BuildError):
                b.replace_outputs(staging)
            b.file_hash = real_hash
            self.assert_old_set(site)
        finally:
            b.HERE, b.file_hash = old_here, real_hash


if __name__ == "__main__":
    unittest.main()
