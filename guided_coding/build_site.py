#!/usr/bin/env python3
"""Build the Guided Coding web pages and download from a published GuidedCoding commit.

Usage, from the website checkout (Python 3.10 or newer, Git):
    python3 guided_coding/build_site.py --ref FULL_COMMIT [--source-dir DIR] [--check-only]

It fetches https://github.com/cctbx/guided_coding at FULL_COMMIT (or reads that commit from the local clone
--source-dir), runs the repository's own tst_guided_coding.py, renders the website-owned Markdown pages and the
pages generated from the repository, builds guided_coding.zip with fixed timestamps, and writes package.json.
Everything is built in a staging folder first; the website outputs are replaced only after every step succeeded,
and the previous outputs are kept in guided_coding/.previous/. --check-only builds and checks without replacing
anything. The script never commits or pushes.
"""
import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_URL = "https://github.com/cctbx/guided_coding"
ZIP_NAME = "guided_coding.zip"
ZIP_TIME = (2026, 1, 1, 0, 0, 0)
COPY_LABEL = "Copy these instructions"
SKILL_FILES = ["SKILL.md", "BATCH.md", "SETUP.md", "REVIEWER.md", "LOG.md"]
ZIP_FILES = ["README.md", "EVIDENCE.md", "LICENSE.txt", "tst_guided_coding.py"] + [
    "guided_coding/" + name for name in SKILL_FILES]

# Website pages: (output, navigation label, title, description, source).
# source: "pages/<file>" (website-owned), "repo:<file>" (from the repository), or a generator name.
PAGES = [
    ("quick-start.html", "Quick Start", "Quick Start with Guided Coding",
     "Set up Guided Coding by giving Claude Code one message.", "pages/quick-start.md"),
    ("how-it-works.html", "How it works", "How Guided Coding works",
     "What happens in a Guided Coding job, and what you decide.", "pages/how-it-works.md"),
    ("getting-started.html", "Install", "Installing Guided Coding",
     "Install, update, move from the earlier kit, or go back.", "repo:README.md"),
    ("verification.html", "Evidence", "Evidence and limits",
     "What the evidence says about the main parts of /gc, the study behind it, and the behaviour checks.", "repo:EVIDENCE.md"),
    ("why-not-claude-code.html", "Why Guided Coding", "Why Guided Coding and not just Claude Code?",
     "What the replay study found to help, and the procedure Guided Coding follows from it.",
     "pages/why-not-claude-code.md"),
    ("why-not-vibe-coding.html", None, "Why Guided Coding and not Vibe Coding?",
     "Keeping you in control.", "pages/why-not-vibe-coding.md"),
    ("documentation.html", "Documentation", "Guided Coding documentation",
     "Every Guided Coding document, in one place.", "generated:documentation"),
    ("reference-files.html", None, "Guided Coding skill files",
     "The five instruction files Claude Code reads, exactly as published.", "generated:reference"),
]
RETIRED = [
    ("overview.html", "Guided Coding overview (retired)"),
    ("architecture.html", "Guided Coding implementation details (retired)"),
    ("user-guide.html", "Guided Coding User Guide and command reference (retired)"),
]
OUTPUTS = (["index.html", ZIP_NAME, ZIP_NAME + ".sha256", "package.json"]
           + [p[0] for p in PAGES] + [r[0] for r in RETIRED])


class BuildError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise BuildError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


# --- source -------------------------------------------------------------------------------------------------

def run(args, cwd=None):
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    require(result.returncode == 0, "command failed: %s\n%s%s" % (" ".join(args), result.stdout, result.stderr))
    return result.stdout


def fetch_source(ref, source_dir, scratch):
    """Return a folder holding exactly the files of commit `ref`."""
    require(re.fullmatch(r"[0-9a-f]{40}", ref) is not None, "--ref must be a full 40-character commit id")
    clone = source_dir
    if clone is None:
        clone = os.path.join(scratch, "clone")
        run(["git", "clone", "--quiet", REPO_URL + ".git", clone])
    run(["git", "-C", clone, "cat-file", "-e", ref + "^{commit}"])
    published = subprocess.run(["git", "-C", clone, "merge-base", "--is-ancestor", ref, "refs/remotes/origin/master"],
                               capture_output=True)
    require(published.returncode == 0, "the commit is not on origin/master of the source; publish it first "
            "(with --source-dir, fetch that clone first)")
    tree = os.path.join(scratch, "source")
    os.makedirs(tree)
    archive = os.path.join(scratch, "source.tar")
    run(["git", "-C", clone, "archive", "--format=tar", "-o", archive, ref])
    run(["tar", "-xf", archive, "-C", tree])
    date = run(["git", "-C", clone, "show", "-s", "--format=%cs", ref]).strip()
    return tree, date


def check_source(tree):
    for name in ZIP_FILES:
        require(os.path.isfile(os.path.join(tree, name)), "the published commit lacks " + name)
    result = subprocess.run([sys.executable, "-I", "tst_guided_coding.py"], cwd=tree, capture_output=True, text=True)
    require(result.returncode == 0 and result.stdout.strip().endswith("OK"),
            "the repository's tst_guided_coding.py failed:\n" + result.stdout + result.stderr)


# --- Markdown -----------------------------------------------------------------------------------------------

def link_target(target):
    """Map a link in a repository or website document to a website or GitHub address."""
    if re.match(r"(https?:|mailto:|#)", target):
        return target
    path, _, anchor = target.partition("#")
    if path.endswith(".html"):
        return target
    mapping = {"EVIDENCE.md": "verification.html", "README.md": "getting-started.html",
               "guided_coding": "reference-files.html", "guided_coding/": "reference-files.html"}
    if path in mapping:
        return mapping[path] + ("#" + anchor if anchor else "")
    if path.startswith("guided_coding/") and path[len("guided_coding/"):] in SKILL_FILES:
        return "reference-files.html#" + path[len("guided_coding/"):].lower().replace(".", "-")
    return REPO_URL + "/blob/master/" + path


def inline(text):
    """Inline Markdown: code spans, links, strong and emphasis; everything else is escaped. Forms it does not
    support (underscore emphasis, autolinks, HTML entities) are refused rather than shown wrongly."""
    plain = re.sub(r"`[^`]*`", "", text)
    require(not re.search(r"(^|\W)(__|_)\w", plain) and "<http" not in plain and not re.search(r"&\w+;", plain),
            "unsupported inline form (underscore emphasis, autolink or HTML entity): " + text[:60])
    out, i = [], 0
    while i < len(text):
        c = text[i]
        if c == "`":
            end = text.find("`", i + 1)
            require(end != -1, "unclosed code span: " + text[:60])
            out.append("<code>" + html.escape(text[i + 1:end]) + "</code>")
            i = end + 1
        elif c == "[" and "](" in text[i:]:
            mid = text.find("](", i + 1)
            end = text.find(")", mid + 2)
            require(end != -1, "unclosed link: " + text[:60])
            out.append('<a href="' + html.escape(link_target(text[mid + 2:end]), quote=True) + '">'
                       + inline(text[i + 1:mid]) + "</a>")
            i = end + 1
        elif text.startswith("**", i):
            end = text.find("**", i + 2)
            require(end != -1, "unclosed strong: " + text[:60])
            out.append("<strong>" + inline(text[i + 2:end]) + "</strong>")
            i = end + 2
        elif c == "*" and i + 1 < len(text) and text[i + 1] != " ":
            end = text.find("*", i + 1)
            require(end != -1, "unclosed emphasis: " + text[:60])
            out.append("<em>" + inline(text[i + 1:end]) + "</em>")
            i = end + 1
        else:
            out.append(html.escape(c))
            i += 1
    return "".join(out)


def slug(label, used):
    base = re.sub(r"[^\w -]", "", re.sub(r"<[^>]+>", "", label).lower()).strip().replace(" ", "-")
    n = used.get(base, 0)
    used[base] = n + 1
    return base + ("-" + str(n) if n else "")


def render(markdown, allow_copy=False):
    """Render a small Markdown subset: headings, paragraphs, flat lists (with continuation lines and fenced code
    inside an item), fenced code, tables and block quotes. Returns (title, body, toc)."""
    lines = markdown.splitlines()
    require(lines and lines[0].startswith("# "), "a document needs a '# ' title")
    title = lines[0][2:].strip()
    blocks, toc, used, copies, i = [], [], {}, 0, 1
    item_re = re.compile(r"^( *)(-|[0-9]+\.) (.+)$")

    def cells(row):
        return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", row.strip().strip("|"))]

    def code_block(i, indent):
        fence = lines[i][indent:]
        require(re.fullmatch(r"```[a-zA-Z0-9_-]*", fence) is not None, "unsupported code fence: " + fence)
        code, i = [], i + 1
        while i < len(lines) and lines[i][indent:] != "```":
            code.append(lines[i][indent:] if lines[i].startswith(" " * indent) else lines[i])
            i += 1
        require(i < len(lines), "unclosed code fence")
        return fence, "\n".join(code), i + 1

    def list_block(i):
        first = item_re.match(lines[i])
        indent, ordered = len(first.group(1)), first.group(2) != "-"
        items = []
        while i < len(lines):
            m = item_re.match(lines[i])
            if not m or len(m.group(1)) != indent or (m.group(2) != "-") != ordered:
                break
            i += 1
            text, inner = [m.group(3)], []
            while i < len(lines) and (lines[i].startswith(" " * (indent + 2)) or not lines[i].strip()):
                if not lines[i].strip():
                    if i + 1 < len(lines) and lines[i + 1].startswith(" " * (indent + 2)):
                        i += 1
                        if not lines[i][indent + 2:].startswith("```") and not inner:
                            inner.append("")  # what follows is a new paragraph in this item
                        continue
                    break
                stripped = lines[i][indent + 2:]
                if item_re.match(stripped) and len(item_re.match(stripped).group(1)) == 0:
                    sub, i = list_block(i)
                    inner.append(sub)
                elif stripped.startswith("```"):
                    fence, code, i = code_block(i, indent + 2)
                    inner.append("<pre><code>" + html.escape(code + "\n") + "</code></pre>")
                elif inner:
                    if inner[-1] == "":
                        inner[-1] = "<p>" + inline(stripped) + "</p>"
                    elif inner[-1].startswith("<p>"):
                        inner[-1] = inner[-1][:-4] + " " + inline(stripped) + "</p>"
                    else:
                        inner.append("<p>" + inline(stripped) + "</p>")
                    i += 1
                else:
                    text.append(stripped)
                    i += 1
            items.append("<li>" + inline(" ".join(text)) + "".join(x for x in inner if x) + "</li>")
        require(items, "list parsing made no progress")
        tag = "ol" if ordered else "ul"
        start = int(first.group(2)[:-1]) if ordered else 1
        attrs = ' start="%d"' % start if start != 1 else ""
        return "<%s%s>%s</%s>" % (tag, attrs, "".join(items), tag), i

    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("```"):
            fence, code, i = code_block(i, 0)
            if fence == "```copy":
                require(allow_copy and copies == 0, "only one copy block, and only on website pages")
                copies += 1
                blocks.append('<pre class="gc-copy-box" id="copy-text"><code>' + html.escape(code)
                              + '</code></pre><button type="button" data-copy="copy-text">' + COPY_LABEL
                              + '</button><p id="copy-status" class="gc-copy-status gc-small" role="status" '
                              'aria-live="polite"></p>')
            else:
                blocks.append("<pre><code>" + html.escape(code + "\n") + "</code></pre>")
            continue
        heading = re.fullmatch(r"(#{2,4}) (.+)", line)
        require(heading is not None or not line.startswith("#"), "unsupported heading or '#' line: " + line[:60])
        if heading:
            level, label = len(heading.group(1)), heading.group(2)
            anchor = slug(label, used)
            blocks.append('<h%d id="%s">%s</h%d>' % (level, anchor, inline(label), level))
            if level == 2:
                toc.append('<li><a href="#%s">%s</a></li>' % (anchor, inline(label)))
            i += 1
            continue
        if line.startswith("|"):
            header = cells(line)
            require(i + 1 < len(lines) and all(re.fullmatch(r":?-{3,}:?", c) for c in cells(lines[i + 1])),
                    "table without a separator row")
            rows, i = [], i + 2
            while i < len(lines) and lines[i].startswith("|"):
                row = cells(lines[i])
                require(len(row) == len(header), "table row has the wrong number of cells")
                rows.append("<tr>" + "".join("<td>" + inline(c) + "</td>" for c in row) + "</tr>")
                i += 1
            blocks.append('<div class="gc-table-wrap"><table><thead><tr>'
                          + "".join('<th scope="col">' + inline(c) + "</th>" for c in header)
                          + "</tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>")
            continue
        if line.startswith(">"):
            quoted = []
            while i < len(lines) and lines[i].startswith(">"):
                quoted.append(lines[i][1:].lstrip())
                i += 1
            _, inner, _ = render("# q\n" + "\n".join(quoted))
            blocks.append('<blockquote class="gc-panel">' + inner + "</blockquote>")
            continue
        if item_re.match(line):
            block, i = list_block(i)
            blocks.append(block)
            continue
        paragraph = []
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "```", "|", ">")) \
                and not (paragraph and item_re.match(lines[i])):
            require(not lines[i].startswith(("    ", "![", "---", "~~~")), "unsupported block: " + lines[i][:60])
            paragraph.append(lines[i])
            i += 1
        blocks.append("<p>" + inline(" ".join(paragraph)) + "</p>")
    return title, "\n".join(blocks), toc


# --- pages --------------------------------------------------------------------------------------------------

def fill(template, values, markers):
    for key, value in values.items():
        require(("@@%s@@" % key) in template, "template placeholder missing: " + key)
        template = template.replace("@@%s@@" % key, value)
    for marker, block in markers.items():
        comment = "<!-- %s -->" % marker
        require(template.count(comment) == 1, "template marker missing or repeated: " + marker)
        template = template.replace(comment, block, 1)
    require("@@" not in template, "unfilled template placeholder")
    return template


def doc_page(template, page, title, description, body, toc, note=""):
    nav = "".join('<a href="%s"%s>%s</a>' % (name, ' aria-current="page"' if name == page else "", label)
                  for name, label, _, _, _ in PAGES if label)
    toc_block = ""
    if len(toc) > 1:
        toc_block = ('<details class="gc-panel gc-toc" open><summary>On this page</summary><div><ul>'
                     + "".join(toc) + "</ul></div></details>")
    return fill(template, {"TITLE": html.escape(title), "DESCRIPTION": html.escape(description), "PAGE": page},
                {"DOCUMENT_NAV": nav, "DOCUMENT_TOC": toc_block, "DOCUMENT_CONTENT": body, "DOCUMENT_NOTE": note})


def build(tree, ref, date, staging):
    """Write every output into `staging`. Returns the package metadata."""
    with open(os.path.join(HERE, "docs.template.html")) as f:
        doc_template = f.read()
    with open(os.path.join(HERE, "index.template.html")) as f:
        index_template = f.read()
    source_note = ('<p class="gc-small">Built from <a href="%s/tree/%s">cctbx/guided_coding %s</a> (%s).</p>'
                   % (REPO_URL, ref, ref[:7], date))
    files = {}

    # The download.
    zip_path = os.path.join(staging, ZIP_NAME)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for name in ZIP_FILES:
            with open(os.path.join(tree, name), "rb") as f:
                data = f.read()
            info = zipfile.ZipInfo("guided_coding-" + ref[:7] + "/" + name, ZIP_TIME)
            info.external_attr = 0o644 << 16
            z.writestr(info, data)
            files[name] = sha256(data)
    with open(zip_path, "rb") as f:
        zip_data = f.read()
    zip_sha = sha256(zip_data)
    with open(zip_path + ".sha256", "w") as f:
        f.write("%s  %s\n" % (zip_sha, ZIP_NAME))

    # Documentation pages.
    rendered = {}
    for page, label, title, description, source in PAGES:
        if source.startswith("generated:"):
            continue
        path = os.path.join(HERE, source) if source.startswith("pages/") else os.path.join(tree, source[5:])
        with open(path) as f:
            _, body, toc = render(f.read(), allow_copy=source.startswith("pages/"))
        note = source_note if source.startswith("repo:") else ""
        rendered[page] = doc_page(doc_template, page, title, description, body, toc, note)

    ref_blocks, ref_toc = [], []
    for name in SKILL_FILES:
        with open(os.path.join(tree, "guided_coding", name)) as f:
            text = f.read()
        anchor = name.lower().replace(".", "-")
        ref_toc.append('<li><a href="#%s">%s</a></li>' % (anchor, name))
        ref_blocks.append('<h2 id="%s">%s</h2><pre><code>%s</code></pre>' % (anchor, name, html.escape(text)))
    rendered["reference-files.html"] = doc_page(doc_template, "reference-files.html", PAGES[7][2], PAGES[7][3],
                                                "\n".join(ref_blocks), ref_toc, source_note)

    doc_items = "".join('<li><a href="%s">%s</a>: %s</li>' % (p[0], html.escape(p[2]), html.escape(p[3]))
                        for p in PAGES if p[0] != "documentation.html")
    doc_body = ("<ul>" + doc_items + "</ul><p>The source is the repository "
                '<a href="%s">cctbx/guided_coding</a>. The earlier GuidedCoding kit is kept on its branch '
                '<a href="%s/tree/full-kit-rev21">full-kit-rev21</a>.</p>' % (REPO_URL, REPO_URL))
    rendered["documentation.html"] = doc_page(doc_template, "documentation.html", PAGES[6][2], PAGES[6][3],
                                              doc_body, [], source_note)

    for page, title in RETIRED:
        body = ("<p>This page described the earlier GuidedCoding kit, which was retired on 2026-10-23 and replaced "
                'by a much shorter procedure. See <a href="index.html">Guided Coding</a>, '
                '<a href="how-it-works.html">How it works</a> and <a href="getting-started.html">Installing Guided '
                'Coding</a>. The earlier kit is kept on the branch <a href="%s/tree/full-kit-rev21">'
                "full-kit-rev21</a> of the repository.</p>" % REPO_URL)
        if page == "user-guide.html":
            body = '<p id="one-time-registration"></p>' + body
        rendered[page] = doc_page(doc_template, page, title, "This page has been retired.", body, [])

    # The main page.
    with open(os.path.join(HERE, "main-page.md")) as f:
        _, main_body, _ = render(f.read())
    rendered["index.html"] = fill(index_template, {
        "DOWNLOAD_URL": ZIP_NAME, "DOWNLOAD_LABEL": "Download Guided Coding (ZIP)",
        "COMMIT_URL": REPO_URL + "/tree/" + ref, "COMMIT_SHORT": ref[:7], "COMMIT_DATE": date,
        "ZIP_KB": str(max(1, round(len(zip_data) / 1024))), "ZIP_SHA": zip_sha,
        "REPO_URL": REPO_URL}, {"MAIN_COPY": main_body})

    pages = {}
    for page, text in rendered.items():
        data = text.encode("utf-8")
        with open(os.path.join(staging, page), "wb") as f:
            f.write(data)
        pages[page] = sha256(data)
    meta = {"source": {"repository": REPO_URL, "commit": ref, "date": date, "files": files},
            "archive": {"file": ZIP_NAME, "bytes": len(zip_data), "sha256": zip_sha}, "pages": pages}
    with open(os.path.join(staging, "package.json"), "w") as f:
        json.dump(meta, f, indent=2, sort_keys=True)
        f.write("\n")
    return meta


def check_links(staging):
    """Every relative link in the outputs points to an output, a page elsewhere on the site, or an anchor that
    exists on the target page."""
    known = set(os.listdir(staging))
    problems = []
    for page in known:
        if not page.endswith(".html"):
            continue
        with open(os.path.join(staging, page)) as f:
            text = f.read()
        for target in re.findall(r'href="([^"]+)"', text):
            if re.match(r"(https?:|mailto:)", target) or target.startswith("../"):
                continue
            path, _, anchor = target.partition("#")
            path = path or page
            if path not in known:
                problems.append("%s: link to missing %s" % (page, path))
                continue
            if anchor and path.endswith(".html"):
                with open(os.path.join(staging, path)) as f:
                    if not re.search(r'\sid="%s"' % re.escape(anchor), f.read()):
                        problems.append("%s: missing anchor %s#%s" % (page, path, anchor))
    require(not problems, "broken links:\n" + "\n".join(sorted(problems)))


def file_hash(path):
    with open(path, "rb") as f:
        return sha256(f.read())


def replace_outputs(staging):
    """Replace all outputs as one set. On any failure, restore the previous set and refuse. Returns the backup folder."""
    import time
    os.makedirs(os.path.join(HERE, ".previous"), exist_ok=True)
    previous = tempfile.mkdtemp(prefix=time.strftime("%Y%m%d-%H%M%S-"), dir=os.path.join(HERE, ".previous"))
    existed = [name for name in OUTPUTS if os.path.exists(os.path.join(HERE, name))]
    for name in existed:
        shutil.copy2(os.path.join(HERE, name), os.path.join(previous, name))
    expected = {name: file_hash(os.path.join(staging, name)) for name in OUTPUTS}
    try:
        for name in OUTPUTS:
            shutil.copy2(os.path.join(staging, name), os.path.join(HERE, name + ".new"))
        for name in OUTPUTS:
            os.replace(os.path.join(HERE, name + ".new"), os.path.join(HERE, name))
        wrong = [name for name in OUTPUTS if file_hash(os.path.join(HERE, name)) != expected[name]]
        require(not wrong, "outputs do not match the built set: %s" % ", ".join(wrong))
    except Exception as error:
        restore_outputs(previous, existed)
        raise BuildError("replacing the outputs failed (%s); the previous outputs were restored from %s"
                         % (error, previous))
    return previous


def restore_outputs(previous, existed):
    """Put back the outputs saved in previous; remove any .new files, and outputs that did not exist before."""
    for name in OUTPUTS:
        for path in [os.path.join(HERE, name + ".new")] + ([] if name in existed else [os.path.join(HERE, name)]):
            if os.path.exists(path):
                os.remove(path)
    for name in existed:
        shutil.copy2(os.path.join(previous, name), os.path.join(HERE, name + ".restoring"))
        os.replace(os.path.join(HERE, name + ".restoring"), os.path.join(HERE, name))
    wrong = [name for name in existed if file_hash(os.path.join(HERE, name)) != file_hash(os.path.join(previous, name))]
    require(not wrong, "restore incomplete (%s); recover from %s or from Git" % (", ".join(wrong), previous))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--ref", required=True, help="full commit id of cctbx/guided_coding to publish")
    parser.add_argument("--source-dir", help="a local clone to read the commit from, instead of fetching")
    parser.add_argument("--check-only", action="store_true", help="build and check without replacing outputs")
    args = parser.parse_args(argv)
    with tempfile.TemporaryDirectory() as scratch:
        try:
            tree, date = fetch_source(args.ref, args.source_dir, scratch)
            check_source(tree)
            staging = os.path.join(scratch, "staging")
            os.makedirs(staging)
            meta = build(tree, args.ref, date, staging)
            check_links(staging)
            if args.check_only:
                print("check only: %d outputs built and checked; nothing replaced" % len(OUTPUTS))
            else:
                previous = replace_outputs(staging)
                print("outputs replaced and checked against the built set; previous outputs kept in %s"
                      % os.path.relpath(previous, os.path.dirname(HERE)))
            print("ZIP sha256 %s (%d bytes)" % (meta["archive"]["sha256"], meta["archive"]["bytes"]))
        except BuildError as error:
            print("BUILD REFUSED: %s" % error, file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
