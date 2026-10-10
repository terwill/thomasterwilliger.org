#!/usr/bin/env python3
"""Fetch, check and package the general Guided Coding edition for this site.

Run from the website checkout: python3 guided_coding/build_package.py
Only generated files beside this script are replaced. No git writes or pushes.
"""

import argparse
import ast
from concurrent.futures import ThreadPoolExecutor
import hashlib
import html
import io
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen
import zipfile

UPSTREAM = "cctbx/cctbx_project"
SOURCE_PATH = "libtbx/guided_coding"
MAX_FILE = 8 * 1024 * 1024
MAX_TOTAL = 32 * 1024 * 1024
SHA = re.compile(r"[0-9a-f]{40}")
SITE = Path(__file__).resolve().parent
INSTALL_ROOT = "~/Downloads/GuidedCoding/guided_coding"
EDITION = "general-downloads-v3"
GENERAL_REFERENCE = re.compile(
    r"cctbx|phenix|/absolute/path/to|/path/to/cctbx|libtbx/guided_coding|/~/Downloads/GuidedCoding", re.I)
SITE_AFFILIATION = '<a href="https://www.phenix-online.org/">Phenix</a> Software Team'
TEMP_PREFIX = 'TMPDIR="$(cd "${TMPDIR:-/tmp}" && pwd -P)"'
TEMP_REASON = "The kit commands resolve `TMPDIR` because macOS temporary paths can pass through symbolic links."
TEMP_HEADERS = {
    "SKILL.md": "# GuidedCoding, by explicit request",
    "docs/GUIDED_CODING_ARCHITECTURE.md": "# GuidedCoding architecture",
    "docs/GUIDED_CODING_VERIFICATION.md": "# GuidedCoding verification and limits",
    "docs/GUIDED_CODING_USER_GUIDE.md": "# GuidedCoding user guide",
    "docs/GUIDED_CODING_README.md": "# GuidedCoding — an opt-in coding procedure",
    "payload/WORKER.md": "# Worker — one bounded local change (GuidedCoding 2.0 pilot)",
    "payload/REVIEW_TRANSPORT.md": "# Outside Reviewer transport, when a gate is due",
}
SOURCE_COMMAND = 'GC_PAYLOAD_ROOT="$(pwd -P)/payload" python3 -I -B payload/tools/screen_check.py verify-source . &&\n'
TEMP_COMMANDS = {
    "SKILL.md": ((SOURCE_COMMAND, 1),
                 ('`python3 -I -B payload/tools/records_history.py <target>/.claude/records`', 1),
                 ('`python3 -I -B payload/tools/screen_check.py check-claude-version`', 1),
                 ('`python3 -I -B`', 1)),
    "docs/GUIDED_CODING_ARCHITECTURE.md": (('`python3 -I -B`', 1),),
    "docs/GUIDED_CODING_VERIFICATION.md": ((SOURCE_COMMAND, 1),
        ("python3 -I -B -m unittest discover -s tests -p 'tst_*.py' -v\n", 1)),
    "docs/GUIDED_CODING_USER_GUIDE.md": ((SOURCE_COMMAND, 2),
        ('GC_PAYLOAD_ROOT="$(pwd -P)/payload" python3 -I -B payload/tools/screen_check.py check-claude-version &&\n', 1),
        ('GC_PAYLOAD_ROOT="$(pwd -P)/payload" python3 -I -B payload/tools/screen_check.py register-skill .\n', 1)),
    "payload/WORKER.md": (
        ('`python3 -I -B "$GC_PAYLOAD_ROOT/tools/screen_check.py" present KIND FILE`', 1),
        ('`python3 -I -B "$GC_PAYLOAD_ROOT/tools/screen_check.py" freeze DIR`', 1),
        ('`python3 -I -B "$GC_PAYLOAD_ROOT/tools/screen_check.py" present result SCREEN --evidence DIR [--reading READING] [--disposition NOTE]`', 1),
        ('`python3 -I -B "$GC_PAYLOAD_ROOT/tools/publication_precheck.py" check REPO OUTGOING.txt --fetch --dry-run`', 1)),
    "payload/REVIEW_TRANSPORT.md": (
        ('`python3 -I -B "$GC_PAYLOAD_ROOT/tools/screen_check.py" freeze PACKET_DIR`', 1),
        ('`python3 -I -B "$GC_PAYLOAD_ROOT/tools/review_bundle.py" PACKET_DIR COMPANIONS_DIR REVIEW_BUNDLE.tgz`', 1)),
}
DOCUMENTS = (
    ("GUIDED_CODING_USER_GUIDE.md", "getting-started.html", "User Guide",
     "Install Guided Coding, set up your project and work through a first task."),
    ("GUIDED_CODING_COMMAND_REFERENCE.md", "user-guide.html", "Command reference",
     "Exact registration commands, source checks, controls, updates and removal."),
    ("GUIDED_CODING_README.md", "overview.html", "Overview",
     "What Guided Coding does, its pilot status and where to find the details."),
    ("GUIDED_CODING_ARCHITECTURE.md", "architecture.html", "Architecture",
     "How the shared procedure, project settings, roles and checking tools fit together."),
    ("GUIDED_CODING_VERIFICATION.md", "verification.html", "Verification and limits",
     "What the tools check, what earlier trials observed and what still needs checking."),
)
OUTPUTS = ("guided_coding.zip", "guided_coding.zip.sha256", "package.json",
           *(document[1] for document in DOCUMENTS), "reference-files.html",
           "documentation.html", "index.html")
REQUIRED_FILES = {
    "SKILL.md", "SOURCE_MANIFEST.sha256",
    "docs/GUIDED_CODING_ARCHITECTURE.md", "docs/GUIDED_CODING_README.md",
    "docs/GUIDED_CODING_USER_GUIDE.md", "docs/GUIDED_CODING_COMMAND_REFERENCE.md",
    "docs/GUIDED_CODING_VERIFICATION.md",
    "payload/DEVELOPER_GUIDE_CONTRACT.md", "payload/GUIDE.md", "payload/HELPER.md",
    "payload/OUTSIDE_REVIEWER_BRIEF.md", "payload/RELEASE", "payload/REVIEW_TRANSPORT.md",
    "payload/ROLES.md", "payload/SETUP.md", "payload/SETUP_DEFAULTS.md", "payload/WORKER.md",
    "payload/screens/PLAN.md", "payload/screens/PUBLICATION.md",
    "payload/screens/RESULT.md", "payload/screens/STOP.md",
    "payload/templates/APPROVAL_REPORT.md", "payload/templates/HELPER_HANDOFF.md",
    "payload/templates/PROJECT_METHOD.md",
    "payload/tools/screen_check.py", "payload/tools/review_bundle.py",
    "payload/tools/publication_precheck.py", "payload/tools/records_history.py",
    "tests/tst_screen_check_v20.py", "tests/tst_review_bundle_v20.py",
    "tests/tst_publication_precheck_v20.py", "tests/tst_records_history_v20.py",
}
REQUIRED_FUNCTIONS = {
    "screen_check.py": {"verify_source", "check_claude_version", "register_skill",
                        "freeze", "verify", "check", "present"},
    "review_bundle.py": {"make_bundle"},
    "publication_precheck.py": {"check_command", "vet_command"},
    "records_history.py": {"entries"},
}


class PackageError(ValueError):
    pass


class RecoveryError(PackageError):
    """An output error also prevented restoration; keep recovery files and lock."""


def require(condition, message):
    if not condition:
        raise PackageError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_name(name):
    require(isinstance(name, str) and bool(name), "empty file name")
    require(not name.startswith("/") and "\\" not in name and ":" not in name
            and all(part not in ("", ".", "..") for part in name.split("/"))
            and all(ord(c) >= 32 and ord(c) != 127 for c in name),
            f"unsafe source path: {name!r}")
    return name


def fetch(url):
    request = Request(url, headers={"User-Agent": "guided-coding-site-packager/1"})
    with urlopen(request, timeout=45) as response:
        data = response.read(MAX_FILE + 1)
    require(len(data) <= MAX_FILE, f"download too large: {url}")
    return data


def api(path):
    return json.loads(fetch("https://api.github.com/repos/" + UPSTREAM + path))


def tree(sha, recursive=False):
    result = api("/git/trees/" + sha + ("?recursive=1" if recursive else ""))
    require(not result.get("truncated"), "GitHub returned a truncated source inventory")
    return result["tree"]


def child_tree(entries, name):
    matches = [x for x in entries if x["path"] == name and x["type"] == "tree"]
    require(len(matches) == 1, f"upstream directory missing: {name}")
    return matches[0]["sha"]


def parse_manifest(data):
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise PackageError("source manifest is not UTF-8") from error
    expected = {}
    for line in text.splitlines(keepends=True):
        match = re.fullmatch(r"([0-9a-f]{64})  \./([^\r\n]+)\n", line)
        require(match is not None, "malformed source manifest line")
        name = safe_name(match[2])
        require(name not in expected and name != "SOURCE_MANIFEST.sha256",
                "duplicate or self-listed source manifest entry")
        expected[name] = match[1]
    require(bool(expected), "empty source manifest")
    require(len(expected) <= 500, "unexpectedly large source inventory")
    return expected


def validate_source(source, upstream_names=None):
    """Use our own code to check bytes BEFORE any downloaded code can run."""
    files = {}
    require(source.is_dir() and not source.is_symlink(), "source must be an ordinary directory")
    for path in source.rglob("*"):
        require(not path.is_symlink(), "symbolic link in source")
        if path.is_dir():
            continue
        info = path.stat()
        require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
                "non-regular or multiply-linked source file")
        files[safe_name(path.relative_to(source).as_posix())] = path
    require("SOURCE_MANIFEST.sha256" in files, "missing source manifest")
    expected = parse_manifest(files["SOURCE_MANIFEST.sha256"].read_bytes())
    names = set(expected) | {"SOURCE_MANIFEST.sha256"}
    require(set(files) == names, "missing or extra local source files")
    if upstream_names is not None:
        require(set(upstream_names) == names, "upstream file inventory differs from its manifest")
    require(sum(p.stat().st_size for p in files.values()) <= MAX_TOTAL,
            "source package exceeds size limit")
    for name, sha in expected.items():
        require(digest(files[name].read_bytes()) == sha, f"checksum mismatch: {name}")
    return expected


def source_snapshot(source):
    """Freeze verified file names, bytes and modes, including the manifest itself."""
    expected = validate_source(source)
    return {name: (digest((source / name).read_bytes()),
                   stat.S_IMODE((source / name).stat().st_mode))
            for name in sorted(set(expected) | {"SOURCE_MANIFEST.sha256"})}


def require_unchanged_source(source, original):
    try:
        current = source_snapshot(source)
    except (PackageError, OSError) as error:
        raise PackageError("source changed during checks or packaging: " + str(error)) from error
    changed = sorted(name for name in set(original) | set(current)
                     if original.get(name) != current.get(name))
    require(not changed, "source changed during checks or packaging: " + ", ".join(changed))


def download_source(ref, destination):
    commit = api("/commits/" + quote(ref, safe=""))
    sha = commit["sha"]
    require(SHA.fullmatch(sha) is not None, "invalid resolved upstream commit")
    root = tree(commit["commit"]["tree"]["sha"])
    libtbx = tree(child_tree(root, "libtbx"))
    source_tree = child_tree(libtbx, "guided_coding")
    entries = tree(source_tree, recursive=True)
    inventory = {}
    for entry in entries:
        if entry["type"] == "tree":
            continue
        name = safe_name(entry["path"])
        require(entry["type"] == "blob" and entry["mode"] in ("100644", "100755"),
                f"upstream source is not a regular file: {name}")
        require(name not in inventory, "duplicate upstream path")
        inventory[name] = entry
    require("SOURCE_MANIFEST.sha256" in inventory, "upstream source manifest missing")
    base = f"https://raw.githubusercontent.com/{UPSTREAM}/{sha}/"
    manifest = fetch(base + SOURCE_PATH + "/SOURCE_MANIFEST.sha256")
    expected = parse_manifest(manifest)
    require(set(inventory) == set(expected) | {"SOURCE_MANIFEST.sha256"},
            "upstream file inventory differs from its manifest")
    require(sum(entry.get("size", 0) for entry in inventory.values()) <= MAX_TOTAL,
            "upstream source package exceeds size limit")
    destination.mkdir()

    def get_file(name):
        data = manifest if name == "SOURCE_MANIFEST.sha256" else fetch(
            base + SOURCE_PATH + "/" + quote(name, safe="/"))
        if name in expected:
            require(digest(data) == expected[name], f"checksum mismatch: {name}")
        git_sha = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        require(git_sha == inventory[name]["sha"], f"upstream Git blob differs: {name}")
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        path.chmod(0o755 if inventory[name]["mode"] == "100755" else 0o644)

    with ThreadPoolExecutor(max_workers=6) as pool:
        list(pool.map(get_file, sorted(inventory)))
    validate_source(destination, inventory)
    license_data = fetch(base + "LICENSE.txt")
    require(b"Redistribution and use" in license_data, "upstream license needs inspection")
    return {
        "repository": UPSTREAM, "requested_ref": ref, "commit": sha,
        "commit_date": commit["commit"]["committer"]["date"], "source_tree": source_tree,
        "source_path": SOURCE_PATH,
        "source_manifest_sha256": digest(manifest), "source_files": len(inventory),
        "license_sha256": digest(license_data),
    }, license_data


def check_hooks(source):
    actual = {p.relative_to(source).as_posix() for p in source.rglob("*") if p.is_file()}
    missing = REQUIRED_FILES - actual
    require(not missing, "required package files missing: " + ", ".join(sorted(missing)))
    skill = (source / "SKILL.md").read_text()
    for marker in ("name: gc", "disable-model-invocation: true", "$ARGUMENTS",
                   "CLAUDE_SKILL_DIR", "CLAUDE_PROJECT_DIR", "verify-source",
                   "check-claude-version", "payload/SETUP.md", "payload/SETUP_DEFAULTS.md"):
        require(marker in skill, f"required skill hook changed: {marker}")
    require(re.search(r"shasum[^\n]+SOURCE_MANIFEST\.sha256\s*&&\s*"
                      r"GC_PAYLOAD_ROOT[^\n]+verify-source", skill) is not None,
            "skill no longer guards source execution with its listed checksum")
    release_checks = re.findall(r"grep -Fq '([^']+)' payload/RELEASE", skill)
    release = (source / "payload/RELEASE").read_text()
    require(bool(release_checks) and all(label in release for label in release_checks),
            "skill release guard does not match the bundled RELEASE text")
    for name, required in REQUIRED_FUNCTIONS.items():
        path = source / "payload/tools" / name
        parsed = ast.parse(path.read_bytes(), filename=str(path))
        functions = {n.name for n in parsed.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
        require(required <= functions, f"required tool entry point changed: {name}")
        imports = set()
        for node in ast.walk(parsed):
            if isinstance(node, ast.Import):
                imports.update(x.name.split(".")[0] for x in node.names)
            elif isinstance(node, ast.ImportFrom):
                require(not node.level, f"new relative dependency needs inspection: {name}")
                imports.add((node.module or "").split(".")[0])
        require(imports <= sys.stdlib_module_names,
                f"new nonstandard tool dependency needs inspection: {name}: {sorted(imports - sys.stdlib_module_names)}")
    checker_ast = ast.parse((source / "payload/tools/screen_check.py").read_bytes())
    values = [ast.literal_eval(n.value) for n in checker_ast.body
              if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name)
              and t.id == "MIN_CLAUDE_VERSION" for t in n.targets)]
    require(len(values) == 1 and isinstance(values[0], tuple) and len(values[0]) == 3
            and all(type(x) is int and x >= 0 for x in values[0]) and values[0][2] > 0,
            "minimum client version interface changed; inspect before packaging")
    return values[0]


def clean_environment(home):
    home = home.resolve(strict=True)
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("CLAUDE", "ANTHROPIC", "GC_", "PYTHON", "GIT_"))}
    env.update(HOME=str(home), TMPDIR=str(home), PYTHONDONTWRITEBYTECODE="1",
               GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    return env


def run_checked(args, source, env, expected_success=True, required_text=None, timeout=180):
    result = subprocess.run([sys.executable, "-I", "-B", *map(str, args)],
                            cwd=source, env=env, capture_output=True, text=True, timeout=timeout)
    output = result.stdout + result.stderr
    require((result.returncode == 0) == expected_success,
            f"check failed: {' '.join(map(str, args))}\n{output[-5000:]}")
    if required_text:
        require(required_text in output, f"check did not report {required_text!r}: {output[-2000:]}")
    return output


def fake_client(path, version):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("#!/bin/sh\nprintf '%s\\n' '" + version + " (Claude Code)'\n")
    path.chmod(0o755)
    return path


def run_contract_checks(source, minimum, scratch):
    """Check current client-selection and registration interfaces with fake clients."""
    source = source.resolve(strict=True)
    scratch = scratch.resolve(strict=True)
    tool = source / "payload/tools/screen_check.py"
    env = clean_environment(scratch)
    env["GC_PAYLOAD_ROOT"] = str(source / "payload")
    run_checked([tool, "verify-source", source], source, env,
                required_text="VERIFIED complete source")
    for file in REQUIRED_FUNCTIONS:
        run_checked([source / "payload/tools" / file, "--help"], source, env)
    current = ".".join(map(str, minimum))
    previous = ".".join(map(str, (minimum[0], minimum[1], minimum[2] - 1)))
    good = fake_client(scratch / "good-cli/claude", current)
    old = fake_client(scratch / "old-cli/claude", previous)
    good_engine = fake_client(scratch / "app engine/current", current)
    old_engine = fake_client(scratch / "app engine/old", previous)
    args = [tool, "check-claude-version"]
    base = {**env, "PATH": ""}
    run_checked(args, source, base, expected_success=False)
    run_checked(args, source, {**base, "PATH": str(good.parent)}, required_text="VERIFIED")
    run_checked(args, source, {**base, "PATH": str(old.parent)}, expected_success=False)
    run_checked(args, source, {**base, "CLAUDE_CODE_ENTRYPOINT": "sdk-cli",
                "CLAUDE_CODE_EXECPATH": str(good_engine)}, expected_success=False)
    app = {**base, "CLAUDE_CODE_ENTRYPOINT": "claude-desktop"}
    try:
        unchecked = run_checked(args, source, app, required_text="NOT CHECKED")
        require(unchecked.count("NOT CHECKED") == 1 and "VERIFIED" not in unchecked,
                "unreadable app engine must report one unchecked notice")
        bad_engine = fake_client(scratch / "app engine/unparseable", "not-a-version")
        unchecked = run_checked(args, source, {**app, "CLAUDE_CODE_EXECPATH": str(bad_engine),
                                "PATH": str(good.parent)}, required_text="NOT CHECKED")
        require(unchecked.count("NOT CHECKED") == 1 and "VERIFIED" not in unchecked,
                "an unreadable app engine must not fall back to a verified PATH CLI")
        run_checked(args, source, {**app, "CLAUDE_CODE_EXECPATH": str(good_engine)},
                    required_text="VERIFIED")
        run_checked(args, source, {**app, "CLAUDE_CODE_EXECPATH": str(good_engine),
                    "PATH": str(old.parent)}, required_text="VERIFIED")
        run_checked(args, source, {**app, "CLAUDE_CODE_EXECPATH": str(old_engine),
                    "PATH": str(good.parent)}, expected_success=False)
    except PackageError as error:
        raise PackageError("App-engine contract failed. The upstream app version-check fix may "
                           "not be published yet, or its interface changed. No site outputs were replaced.\n"
                           + str(error)) from error
    config = scratch / "private-config"
    registered_env = {**app, "CLAUDE_CODE_EXECPATH": str(good_engine),
                      "CLAUDE_CONFIG_DIR": str(config)}
    run_checked([tool, "register-skill", source], source, registered_env, required_text="REGISTERED")
    link = config / "skills/guided_coding"
    require(link.is_symlink() and link.resolve() == source.resolve(),
            "standalone registration did not create the expected central link")
    run_checked([tool, "register-skill", source], source, registered_env, expected_success=False)
    require(link.is_symlink() and link.resolve() == source.resolve(), "registration refusal changed the link")
    validate_source(source)
    return {"source_guard": "passed", "tool_commands": "passed",
            "client_selection": "passed (fake clients; no native app session)",
            "standalone_registration": "passed (private configuration)",
            "app_marker": "CLAUDE_CODE_ENTRYPOINT=claude-desktop",
            "app_engine_path": "CLAUDE_CODE_EXECPATH"}


def run_package_tests(source, scratch):
    source = source.resolve(strict=True)
    scratch = scratch.resolve(strict=True)
    env = clean_environment(scratch)
    results = []
    tests = sorted(source.glob("tests/tst_*.py"))
    require(bool(tests), "no upstream tests found")
    for path in tests:
        output = run_checked([path], source, env)
        match = re.search(r"Ran (\d+) tests? in", output)
        require(match is not None, f"test runner returned no test count: {path.name}")
        require(int(match[1]) > 0, f"test runner executed no tests: {path.name}")
        skipped = re.search(r"skipped=(\d+)", output)
        results.append({"file": path.relative_to(source).as_posix(),
                        "tests": int(match[1]), "skipped": int(skipped[1]) if skipped else 0,
                        "output_sha256": digest(output.encode())})
    validate_source(source)
    return results


REGISTRATION = f"""Please set up GuidedCoding from {INSTALL_ROOT} for this Claude Code configuration. Read docs/GUIDED_CODING_COMMAND_REFERENCE.md there. Verify the source and release, check the Claude Code version for this session, and inspect the existing personal skill. If a working shared Guided Coding registration already exists, keep it and show its resolved source. Otherwise register the central link only if the destination is unoccupied. Show what changed. Do not connect to servers, change permission settings, or start a coding task."""
TASK = "/guided_coding Describe the change you want to make, your requirements, and how you would check the result."


def legacy_general_text(name, text):
    """Adapt the distribution copy, never the verified input, on every build."""
    if name == "docs/GUIDED_CODING_USER_GUIDE.md":
        text = re.sub(r"(?m)^Please set up GuidedCoding from .+$", lambda _: REGISTRATION, text)
        text = text.replace("replacing the example with your actual absolute path:",
                            "using the Downloads location below, or the stable location you chose:")
        text = text.replace("`libtbx/guided_coding/`, without an enclosing release-named folder.",
                            "`GuidedCoding/guided_coding/` inside `guided_coding.zip`.")
        text = text.replace("Use an empty staging directory. Replace the paths and run this **whole\nBash block**, not separate commands:",
                            "Use an empty staging directory in Downloads. Run this **whole Bash\nblock**, not separate commands; it refuses an existing review directory:")
        text = text.replace("mkdir /path/to/empty-gc-review &&\n"
                            "tar -xzf /path/to/reviewed-guided-coding.tgz -C /path/to/empty-gc-review &&\n"
                            "cd /path/to/empty-gc-review/libtbx/guided_coding &&",
                            "mkdir ~/Downloads/guided_coding_review &&\n"
                            "unzip ~/Downloads/guided_coding.zip -d ~/Downloads/guided_coding_review &&\n"
                            "cd ~/Downloads/guided_coding_review/GuidedCoding/guided_coding &&")
        text = text.replace("Loading the procedure from `cctbx_project` does not\nmake that repository the target.",
                            f"Loading the procedure from `{INSTALL_ROOT}` does not\nmake that directory the target.")
        text = text.replace("They contain no universal server, PHENIX command or account.",
                            "They contain no universal server, project-specific command or account.")
        text = text.replace("You may supply a separate project card, such as a PHENIX defaults card.",
                            "Supply `GENERAL_DEVELOPER_CARD.md` from the kit, or a card for your project.")
        text = text.replace("such as `t96`", "such as `run_checks`")
        text = text.replace("PHENIX-specific values", "project-specific values")
        text = text.replace("Because the personal link points at a checkout, changing the source there",
                            "Because the personal link points at a source directory, changing the source there")
        text = text.replace("For publication to `cctbx_project`, tags are reserved for repository releases.\n"
                            "Do not recreate the removed GC pilot tag or create another development tag.\n"
                            "Keep pilot status in these docs and refer to the publication commit and\n"
                            "manifest. Other destinations have their own repository conventions.",
                            "Follow your project's publication and release conventions. Do not create\n"
                            "a development or recovery tag. Record the accepted source revision and\n"
                            "manifest with the work; any release tag needs the project's own authorization.")
    elif name == "docs/GUIDED_CODING_README.md":
        before = ("`enumcheck-20261002T194333Z` was published to `cctbx_project` on\n"
                  "2026-10-02 (commit `c36887c7f489018af4f91773246ecde32d1b4e24`), and its\n"
                  "documentation revision `docs-20261003` on 2026-10-03 (commit\n"
                  "`b0747a4a55f29db3abe04358480d5867e94cb792`).")
        after = ("`enumcheck-20261002T194333Z` was published in the original upstream source repository on\n"
                 "2026-10-02 (upstream commit `c36887c7f489018af4f91773246ecde32d1b4e24`), and its\n"
                 "documentation revision `docs-20261003` on 2026-10-03 (upstream commit\n"
                 "`b0747a4a55f29db3abe04358480d5867e94cb792`).")
        require(text.count(before) == 1, "required general-edition passage missing or duplicated; inspect " + name)
        text = text.replace(before, after, 1)
        text = text.replace("The full PHENIX server suite", "The original project's full server test suite")
        text = text.replace(
            "contains no personal PHENIX profile, account, server requirement or `t96`\n"
            "definition. An optional project defaults card can be supplied separately;\n"
            "another developer adapts its paths and permissions to their own environment.",
            "contains no personal project profile, account, required server or predefined\n"
            "test shortcut. You may supply a separate project defaults card; adapt its\n"
            "paths and permissions to your own environment.")
    elif name == "docs/GUIDED_CODING_VERIFICATION.md":
        before = ("The skill entry `SKILL.md`, whose session-title instructions these observations exercised, "
                  "is byte-identical between that revision and the published one;")
        after = ("The skill entry `SKILL.md`, whose session-title instructions these observations exercised, "
                 "is byte-identical between that revision and the published upstream revision; "
                 "this edition's copy differs from its pinned upstream source only in its example source path "
                 "and temporary-directory handling, "
                 "not in the session-title instructions;")
        require(text.count(before) == 1, "required general-edition passage missing or duplicated; inspect " + name)
        text = text.replace(before, after, 1)
        # These are historical project-relative records, not new Downloads records.
        text = text.replace("(`phenix/.claude/records/2026-10-04-gc-followups-A/`)",
                            "(in the original project's `.claude/records/2026-10-04-gc-followups-A/`)")
        text = text.replace("record\n`phenix/.claude/records/2026-10-06-gc-app-version-check/`",
                            "record in the original project's\n`.claude/records/2026-10-06-gc-app-version-check/`")
        text = text.replace("record `phenix/.claude/records/2026-10-06-gc-app-version-check/`",
                            "record in the original project's `.claude/records/2026-10-06-gc-app-version-check/`")
        text = text.replace("This was not a PHENIX full-suite run.",
                            "This did not run the original project's full test suite.")
        text = text.replace("not a PHENIX suite", "not the original project's full test suite")
        # Summarize an out-of-scope historical tool; do not invent a general command.
        text = text.replace(
            "| PHENIX test discovery (A7, 2026-10-04) | `phenix.find_program search_type=tests "
            "search_text=<function> tests.search_tests_by=function_called` traced `run_autobuild` to "
            "its calling tests; the default mode matched test names; a function newer than the static "
            "index (dated 2026-05-06) produced no entry and no message; `git_affected_tests=True` saw "
            "only uncommitted modifications in the three module directories. Project guidance, "
            "not a package feature. |",
            "| Historical project test lookup (A7, 2026-10-04) | A project-specific lookup tool "
            "found calling tests in a trial in the original project; its default mode matched test names. "
            "Its static index (dated 2026-05-06) missed a newer function without a message, and its "
            "changed-file mode considered only uncommitted modifications in three module directories. "
            "This tool is not included in the general kit. |")
        text = text.replace("The full PHENIX server suite",
                            "The original project's full server test suite")
        text = text.replace("PHENIX project during October 2026", "original development project during October 2026")
        text = text.replace("| Test isolation in the repository | [`libtbx/tst_guided_coding.py`](../../tst_guided_coding.py) | Complete source verification of arbitrary unlisted files in the original installation |",
                            "| Standalone test runners | [`tests/tst_screen_check_v20.py`](../tests/tst_screen_check_v20.py) and the other shipped runners | Complete source verification of arbitrary unlisted files in the installation |")
        start = text.find("From an appropriate cctbx environment, the repository wrapper is:")
        if start != -1:
            end = text.find("For native validation,", start)
            require(end != -1, "verification wrapper section changed; inspect the adaptation")
            text = (text[:start] + "This standalone kit includes all four test runners. Use the command above\n"
                    "from the verified source directory; it is a separate authorized check,\n"
                    "not a command to continue after a failed source guard. Report every skip.\n"
                    "The repository-wrapper and precompiler observations in the historical\n"
                    "trials describe the earlier development environment, not additional\n"
                    "requirements or tools shipped with this installer.\n\n" + text[end:])
        text = text.replace("python3 -I -B -m unittest discover -s tests -p 'tst_*.py' -v",
                            f"cd {INSTALL_ROOT} &&\npython3 -I -B -m unittest discover -s tests -p 'tst_*.py' -v")
    elif name == "docs/GUIDED_CODING_ARCHITECTURE.md":
        before = ("The personal link exposes the current central checkout, not a pinned\n"
                  "release. Updating that checkout therefore needs coordination with active\n"
                  "work and the repository's integration rules.")
        after = ("The personal link exposes the current central source directory, not a pinned\n"
                 "release. Replacing that directory therefore needs coordination with active\n"
                 "work; follow the update steps in INSTALL.md.")
        require(text.count(before) == 1, "required general-edition passage missing or duplicated; inspect " + name)
        text = text.replace(before, after, 1)
    elif name == "payload/GUIDE.md":
        text = text.replace("own release convention, read before proposing it: cctbx_project reserves\n"
                            "  tags for releases, and a pilot tag was removed there on 2026-10-03.",
                            "own release convention, read before proposing it. Development and\n"
                            "  recovery records use commit ids and branches, not release tags.")
    elif name == "payload/SETUP.md":
        text = text.replace("Do not introduce PHENIX, named hosts, or suite shorthand into an unrelated\n"
                            "project.",
                            "Do not introduce another project's commands, named hosts or test-suite\n"
                            "shortcuts into an unrelated project.")
    paths = ("/absolute/path/to/cctbx_project/libtbx/guided_coding",
             "/path/to/cctbx_project/libtbx/guided_coding",
             "/absolute/path/to/libtbx/guided_coding",
             "cctbx_project/libtbx/guided_coding/", "cctbx_project/libtbx/guided_coding",
             "libtbx/guided_coding")
    for path in paths:
        text = text.replace(path, INSTALL_ROOT)
    # Test repository names are arbitrary fixtures; preserve the same relationships.
    if name.startswith("tests/") and name.endswith(".py"):
        text = text.replace("cctbx_project", "companion_project").replace("cctbx", "companion")
        text = text.replace("/Users/dev/unix/PHENIX/modules/phenix", "/Users/dev/Downloads/example_project")
        text = re.sub("phenix", "example_project", text, flags=re.I)
    if name.endswith(".md") or name.startswith("tests/"):
        require(not GENERAL_REFERENCE.search(text),
                "unadapted general-edition reference; inspect " + name)
    return text



READABLE_HEADERS = {
    "docs/GUIDED_CODING_README.md": "# Guided Coding overview",
    "docs/GUIDED_CODING_ARCHITECTURE.md": "# Guided Coding architecture",
    "docs/GUIDED_CODING_VERIFICATION.md": "# Guided Coding verification and limits",
    "docs/GUIDED_CODING_USER_GUIDE.md": "# Guided Coding User Guide",
}
CLOUD_SECTION = """## Using Guided Coding in the cloud or with cctbx_project or PHENIX

A cloud session cannot use the link on your computer. It can obtain its own copy from the [source repository](https://github.com/cctbx/cctbx_project/tree/master/libtbx/guided_coding); this guide does not cover cloud setup.

[cctbx_project](https://github.com/cctbx/cctbx_project) includes the Guided Coding source. If you use your own copy, follow the one-time setup below with the path to its `libtbx/guided_coding` folder instead of downloading the kit.

[PHENIX](https://www.phenix-online.org) includes Guided Coding. Run `phenix.developer` to open the instructions and default settings for using it with PHENIX.
"""
SOURCE_LINKS = {
    "https://github.com/cctbx/cctbx_project",
    "https://github.com/cctbx/cctbx_project/tree/master/libtbx/guided_coding",
}
READABLE_PASSAGES = {
    "docs/GUIDED_CODING_README.md": (
        "It normally lives in `cctbx_project/libtbx/guided_coding/`, or in the `guided_coding/` folder inside the downloaded `GuidedCoding/` folder.",
        "In this download it lives in the `guided_coding/` folder inside `GuidedCoding/`."),
    "docs/GUIDED_CODING_ARCHITECTURE.md": (
        "The personal link points to the current contents of the shared kit's folder. It does not hold a fixed copy of an older release. Updating that folder can therefore affect every project using it, and must be coordinated with active tasks and the repository's integration rules.",
        "The personal link points to the current contents of the shared kit's folder. It does not hold a fixed copy of an older release. Updating that folder can therefore affect every project using it. Finish active tasks and follow the User Guide's update instructions."),
    "docs/GUIDED_CODING_VERIFICATION.md": (
        "Its `SKILL.md` title instructions matched those in the recorded published revision, but later changes affected the tools, tests and some texts.",
        "Its `SKILL.md` title instructions matched those in the recorded published revision, but later changes affected the tools, tests and some texts. The downloaded edition also adapts the skill's example source path and temporary-directory handling; it keeps those title instructions."),
}


def readable_scan_text(name, text):
    """Exempt the exact approved cloud section and labeled historical evidence."""
    if name == "docs/GUIDED_CODING_USER_GUIDE.md":
        require(text.count(CLOUD_SECTION.strip()) == 1,
                "approved cloud and project section changed; inspect " + name)
        return text.replace(CLOUD_SECTION.strip(), "", 1)
    if name == "docs/GUIDED_CODING_VERIFICATION.md":
        text = re.sub(r"(?s)## Historical record\n.*?(?=## Technical reference\n)", "", text, count=1)
    return text


def general_text(name, text):
    if name == "docs/GUIDED_CODING_COMMAND_REFERENCE.md":
        # This reference retains the former manual commands, with a new title.
        text = legacy_general_text("docs/GUIDED_CODING_USER_GUIDE.md", text)
        return text
    header = READABLE_HEADERS.get(name)
    if not header or text.splitlines()[0:1] != [header]:
        return legacy_general_text(name, text)
    if name == "docs/GUIDED_CODING_USER_GUIDE.md":
        require(not GENERAL_REFERENCE.search(readable_scan_text(name, text)),
                "unadapted general-edition reference; inspect " + name)
        return text  # Exactly the maintained guide: no second edited version.
    before, after = READABLE_PASSAGES[name]
    require(text.count(before) == 1,
            "required general-edition passage missing or duplicated; inspect " + name)
    text = text.replace(before, after, 1)
    if name == "docs/GUIDED_CODING_VERIFICATION.md":
        start = text.find("### Repository test wrapper\n")
        end = text.find("### Historical source identities\n", start)
        require(start != -1 and end != -1, "verification wrapper section changed; inspect the adaptation")
        text = text[:start] + """### Repository test wrapper

The original development repository has an additional test wrapper outside this kit. Its earlier results and skipped precompilation branch describe that development environment. The download does not include or require that wrapper. Run the four shipped test files from the clean copy described above and report every skip.

""" + text[end:]
        text = text.replace("The full PHENIX server test suite", "The original project's full server test suite")
        for record in ("2026-10-04-gc-followups-A", "2026-10-06-gc-app-version-check"):
            text = text.replace("phenix/.claude/records/" + record, ".claude/records/" + record)
        text = text.replace("These paths identify historical records.",
                            "These paths identify historical records relative to the original project.")
    for path in ("/absolute/path/to/libtbx/guided_coding", "cctbx_project/libtbx/guided_coding/"):
        text = text.replace(path, INSTALL_ROOT)
    require(not GENERAL_REFERENCE.search(readable_scan_text(name, text)),
            "unadapted general-edition reference; inspect " + name)
    return text


def temporary_instructions(name, text):
    """Resolve temporary paths in known instructions; refuse changed source passages."""
    if not name.endswith(".md"):
        return text
    if name == "docs/GUIDED_CODING_USER_GUIDE.md" and text.startswith(READABLE_HEADERS[name] + "\n"):
        return text
    commands = TEMP_COMMANDS.get(name, ())
    if name == "docs/GUIDED_CODING_COMMAND_REFERENCE.md":
        commands = TEMP_COMMANDS["docs/GUIDED_CODING_USER_GUIDE.md"]
    if name == "docs/GUIDED_CODING_ARCHITECTURE.md" and text.startswith(READABLE_HEADERS[name] + "\n"):
        commands = (('`python3 -I -B`', 2),)
    if name == "docs/GUIDED_CODING_VERIFICATION.md" and text.startswith(READABLE_HEADERS[name] + "\n"):
        commands = commands + (('`python3 -I -B`', 1),)
    for before, count in commands:
        resolved = before.replace("python3 -I -B", TEMP_PREFIX + " python3 -I -B")
        already = text.count(resolved)
        if already == count:
            continue  # The source itself already resolves TMPDIR here.
        require(already < count,
                "required temporary-directory instruction missing or duplicated; inspect " + name)
        require(already == 0,
                "partly resolved temporary-directory instruction; inspect " + name)
        require(text.count(before) == count,
                "required temporary-directory instruction missing or duplicated; inspect " + name)
        text = text.replace(before, resolved)
    if name in TEMP_HEADERS or name == "docs/GUIDED_CODING_COMMAND_REFERENCE.md":
        header = TEMP_HEADERS.get(name, "# Guided Coding registration and command reference")
        if name in READABLE_HEADERS and text.startswith(READABLE_HEADERS[name] + "\n"):
            header = READABLE_HEADERS[name]
        before = header + "\n\n"
        require(text.count(before) == 1,
                "required temporary-directory explanation anchor missing or duplicated; inspect " + name)
        text = text.replace(before, before + TEMP_REASON + "\n\n", 1)
    for line in text.splitlines():
        command = line.find("python3")
        require(command == -1 or line[:command].count("TMPDIR=") < 2,
                "doubled temporary-directory prefix; inspect " + name)
    for match in re.finditer("python3", text):
        require(text[max(0, match.start() - len(TEMP_PREFIX) - 1):match.start()] == TEMP_PREFIX + " ",
                "unresolved temporary-directory instruction; inspect " + name)
    return text


def general_source(source, destination):
    """Build a separately identified derivative with its own complete manifest."""
    shutil.copytree(source, destination)
    changes = []
    for path in sorted(destination.rglob("*")):
        if not path.is_file() or path.name == "SOURCE_MANIFEST.sha256":
            continue
        name = path.relative_to(destination).as_posix()
        before = path.read_bytes()
        after = (temporary_instructions(name, general_text(name, before.decode("utf-8"))).encode("utf-8")
                 if path.suffix == ".md" or name.startswith("tests/") else before)
        if after != before:
            path.write_bytes(after)
            changes.append({"file": name, "original_sha256": digest(before),
                            "packaged_sha256": digest(after)})
    manifest = "".join(digest(p.read_bytes()) + "  ./" + p.relative_to(destination).as_posix() + "\n"
                       for p in sorted(destination.rglob("*"))
                       if p.is_file() and p.name != "SOURCE_MANIFEST.sha256").encode()
    (destination / "SOURCE_MANIFEST.sha256").write_bytes(manifest)
    validate_source(destination)
    return {"edition": EDITION, "installation_root": INSTALL_ROOT,
            "source_manifest_sha256": digest(manifest),
            "source_files": len(parse_manifest(manifest)) + 1, "adapted_files": changes}


def installation_text(info, minimum, edition):
    return f"""# Guided Coding: installation and first task

Start with `guided_coding/docs/GUIDED_CODING_USER_GUIDE.md` in this folder.
It is the same User Guide shown on the website. It tells you how to check
this download, make the command available, set up your project and try a task.
The general setup card is optional. Keep project settings and task records
in your project, outside the verified kit.

For the one-time setup, open ordinary Claude Code on your computer and send:

{REGISTRATION}

Then open a fresh conversation in your Git project, enter /guided_coding help,
and follow the User Guide. Start each new task with /guided_coding and the
task together in one message. For outside review, use a separate chat,
preferably with a different AI assistant. You decide whether to keep or publish.

The client minimum is {minimum}. The app checks its own engine and reports
NOT CHECKED when that version cannot be read; Terminal checks its PATH client.
A cloud session can obtain its own source copy; creating this local link does
not set up that session.

For updates and removal, follow the User Guide. Finish active tasks, extract
an update separately and keep the old folder until the new link is checked.
Do not edit or add files inside guided_coding/.

{TEMP_REASON.replace('`', '')}
The exact source and adaptations are in PACKAGE_INFO.json.
General-edition source manifest SHA-256: {edition['source_manifest_sha256']}
""".encode()


def make_zip(source, extras):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        members = {"GuidedCoding/guided_coding/" + p.relative_to(source).as_posix():
                   (p.read_bytes(), 0o755 if p.stat().st_mode & 0o111 else 0o644)
                   for p in source.rglob("*") if p.is_file()}
        members.update({"GuidedCoding/" + safe_name(name): (data, 0o644) for name, data in extras.items()})
        for name, (data, mode) in sorted(members.items()):
            item = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            item.create_system = 3
            item.external_attr = (stat.S_IFREG | mode) << 16
            item.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(item, data)
    return buffer.getvalue()


def render_page(template, replacements):
    required = set(re.findall(r"@@([A-Z_]+)@@", template))
    require(required == set(replacements), "page template placeholders changed; inspect the generator")
    return re.sub(r"@@([A-Z_]+)@@", lambda match: html.escape(str(replacements[match[1]]), quote=True),
                  template).encode()


def documentation_link(destination, info):
    """Keep all procedure references in this edition's local documentation."""
    url = urlsplit(destination)
    if url.scheme:
        require(url.scheme in ("https", "http") and bool(url.netloc),
                "unsupported documentation link: " + destination)
        require("cctbx" not in destination.lower() or destination in SOURCE_LINKS,
                "source-history links belong only in the historical note")
        return destination
    require(not url.netloc and not url.query and not url.path.startswith("/"),
            "unsupported documentation link: " + destination)
    if not url.path:
        require(bool(url.fragment), "empty documentation link")
        return destination
    source_path = posixpath.normpath(posixpath.join("docs", url.path))
    safe_name(source_path)
    local = {"docs/" + name: page for name, page, _, _ in DOCUMENTS}
    if source_path in local:
        return local[source_path] + ("#" + url.fragment if url.fragment else "")
    require(source_path in REQUIRED_FILES, "reference not included in the standalone kit: " + destination)
    return "reference-files.html#" + reference_id(source_path)


def reference_id(path):
    return "file-" + re.sub(r"[^a-z0-9]+", "-", path.lower()).strip("-")


def historical_note(info):
    """The source attribution in the documentation index."""
    if info.get("input_kind") == "local-documentation-preview":
        plain = dict(info)
        plain.pop("input_kind")
        return historical_note(plain) + '<p>This download also includes a local documentation update based on that revision. The updated documentation has not yet been published in the source repository. Its input manifest and file changes are recorded in the package metadata.</p>'
    return ('<h2 id="historical-origin">Historical origin</h2>'
            '<p>Guided Coding began in the cctbx project. This standalone edition adapts its documentation '
            'and examples for general projects. The '
            f'<a href="https://github.com/{UPSTREAM}/tree/{info["commit"]}/{SOURCE_PATH}">historical source revision '
            + info['commit'][:12] + '</a>, original license and file changes are recorded with the download. '
            'This edition has its own source manifest; it is not a byte-for-byte copy of that historical revision.</p>')


def package_source_note(info):
    """Explain the package's origin and general adaptations beside the download."""
    if info.get("input_kind") == "local-documentation-preview":
        plain = dict(info)
        plain.pop("input_kind")
        return package_source_note(plain) + '<p class="gc-small">This build includes a local documentation update. The source repository has not yet received those text changes. The checking tools and contract match the selected baseline.</p>'
    return ('<p class="gc-small" id="package-source"><strong>Source and adaptations.</strong> '
            'The material comes from '
            f'<a href="https://github.com/{UPSTREAM}/tree/{info["commit"]}/{SOURCE_PATH}">'
            '<code>cctbx_project/libtbx/guided_coding</code></a>. '
            'The packager edits the documentation and local path examples to use '
            '<code>~/Downloads/GuidedCoding/guided_coding</code>, generalizes project-specific wording '
            'and examples, and supplies a '
            '<a href="GENERAL_DEVELOPER_CARD.md" download>general defaults card</a> for your own projects. '
            'Checking tools and the Developer–Guide Contract are unchanged; the license, and which files '
            'were adapted with their checksums before and after, are recorded with the download.</p>')


def verify_general_documentation(documents, info):
    """Reject leftover references in final pages and installer notes before saving."""
    for name, data in documents.items():
        text = data.decode("utf-8")
        notes = {"documentation.html": historical_note(info), "index.html": package_source_note(info)}
        if name in notes:
            note = notes[name]
            require(text.count(note) == 1, "source attribution changed or duplicated; inspect " + name)
            text = text.replace(note, "", 1)
        if name == "getting-started.html":
            cloud, cloud_toc = render_document("# Cloud section\n\n" + CLOUD_SECTION, info)
            if cloud in text:
                text = text.replace(cloud, "", 1)
                for entry in re.findall(r'<li>.*?</li>', cloud_toc):
                    text = text.replace(entry, "", 1)
        if name == "verification.html":
            text = re.sub(r'(?s)<h2 id="historical-record">.*?(?=<h2 id="technical-reference">)',
                          "", text, count=1)
        if name.endswith(".html"):
            # Preserve the real author affiliation in the shared site header only.
            header = re.search(r'<header class="site-header">.*?</header>', text, re.S)
            if header:
                text = (text[:header.start()] + header[0].replace(SITE_AFFILIATION, "", 1)
                        + text[header.end():])
            text = html.unescape(text)
        leftover = GENERAL_REFERENCE.search(text)
        require(leftover is None, "unadapted general-edition reference; inspect " + name
                + (": " + leftover[0] if leftover else ""))


def document_inline(text, info):
    """Render the inline Markdown used by the shipped docs, escaping all HTML."""
    output = []
    position = 0
    while position < len(text):
        if text[position] == "`":
            end = text.find("`", position + 1)
            require(end != -1, "unclosed documentation code span")
            output.append("<code>" + html.escape(text[position + 1:end]) + "</code>")
            position = end + 1
        elif text[position] == "[" and "](" in text[position:]:
            label_end = text.find("](", position + 1)
            end = text.find(")", label_end + 2)
            require(end != -1, "unclosed documentation link")
            destination = documentation_link(text[label_end + 2:end], info)
            output.append('<a href="' + html.escape(destination, quote=True) + '">'
                          + document_inline(text[position + 1:label_end], info) + "</a>")
            position = end + 1
        elif text.startswith("**", position):
            end = text.find("**", position + 2)
            require(end != -1, "unclosed documentation emphasis")
            output.append("<strong>" + document_inline(text[position + 2:end], info) + "</strong>")
            position = end + 2
        elif text[position] == "*":
            end = text.find("*", position + 1)
            require(end != -1, "unclosed documentation emphasis")
            output.append("<em>" + document_inline(text[position + 1:end], info) + "</em>")
            position = end + 1
        else:
            output.append(html.escape(text[position]))
            position += 1
    return "".join(output)


def render_document(markdown, info):
    """Small standard-library renderer for the four upstream reference documents.

    Handles their paragraphs, ATX headings, fenced code, flat lists and tables.
    Refuse unsupported block syntax rather than silently changing its meaning.
    """
    lines = markdown.splitlines()
    require(bool(lines) and lines[0].startswith("# "), "documentation needs a title")
    blocks, toc, used_ids = [], [], {}
    position = 1  # The title is displayed by the shared website template.
    list_item = re.compile(r"^(-|[0-9]+\.) (.+)$")

    def cells(line):
        return [cell.strip().replace(r"\|", "|")
                for cell in re.split(r"(?<!\\)\|", line.strip().strip("|"))]

    while position < len(lines):
        line = lines[position]
        if not line.strip():
            position += 1
            continue
        if line.startswith("```"):
            require(re.fullmatch(r"```[a-zA-Z0-9_-]*", line) is not None,
                    "unsupported documentation code fence")
            position += 1
            code = []
            while position < len(lines) and lines[position] != "```":
                code.append(lines[position])
                position += 1
            require(position < len(lines), "unclosed documentation code fence")
            blocks.append("<pre><code>" + html.escape("\n".join(code) + "\n") + "</code></pre>")
            position += 1
            continue
        heading = re.fullmatch(r"(#{2,6}) (.+)", line)
        if heading:
            level, label = len(heading[1]), heading[2]
            slug = re.sub(r"[^\w -]", "", label.lower()).replace(" ", "-")
            count = used_ids.get(slug, 0)
            used_ids[slug] = count + 1
            anchor = slug + ("-" + str(count) if count else "")
            blocks.append(f'<h{level} id="{anchor}">' + document_inline(label, info) + f"</h{level}>")
            if level == 2:
                toc.append(f'<li><a href="#{anchor}">' + document_inline(label, info) + "</a></li>")
            position += 1
            continue
        if line.startswith("|"):
            header = cells(line)
            position += 1
            require(position < len(lines)
                    and len(cells(lines[position])) == len(header)
                    and all(re.fullmatch(r":?-{3,}:?", c) for c in cells(lines[position])),
                    "unsupported documentation table header")
            position += 1
            rows = []
            while position < len(lines) and lines[position].startswith("|"):
                row = cells(lines[position])
                require(len(row) == len(header), "documentation table column count differs")
                rows.append("<tr>" + "".join("<td>" + document_inline(c, info) + "</td>"
                                              for c in row) + "</tr>")
                position += 1
            blocks.append('<div class="gc-table-wrap"><table><thead><tr>'
                          + "".join('<th scope="col">' + document_inline(c, info) + "</th>" for c in header)
                          + "</tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>")
            continue
        item = list_item.fullmatch(line)
        if item:
            kind = "ul" if item[1] == "-" else "ol"
            start = '' if kind == "ul" or item[1] == "1." else f' start="{item[1][:-1]}"'
            items = []
            while position < len(lines):
                item = list_item.fullmatch(lines[position])
                if not item or (item[1] == "-") != (kind == "ul"):
                    break
                text = [item[2]]
                position += 1
                while position < len(lines) and lines[position].startswith("  "):
                    continuation = lines[position].lstrip()
                    require(not list_item.fullmatch(continuation)
                            and not continuation.startswith(("```", "|", "#", ">")),
                            "unsupported nested documentation block")
                    text.append(continuation)
                    position += 1
                items.append("<li>" + document_inline(" ".join(text), info) + "</li>")
            blocks.append(f"<{kind}{start}>" + "".join(items) + f"</{kind}>")
            continue
        paragraph = []
        while position < len(lines) and lines[position].strip():
            text = lines[position]
            if paragraph and (text.startswith(("#", "```", "|")) or list_item.fullmatch(text)):
                break
            require(not text.startswith(("#", ">", "    ", "![", "---", "~~~")),
                    "unsupported documentation block: " + text[:80])
            paragraph.append(text)
            position += 1
        blocks.append("<p>" + document_inline(" ".join(paragraph), info) + "</p>")
    return "\n".join(blocks), "<ul>" + "".join(toc) + "</ul>"


def build_documentation(source, info, site, original_source=None):
    template = (site / "docs.template.html").read_text()
    outputs, records = {}, []
    pages = [("index.html", "Guided Coding"), ("getting-started.html", "User Guide"),
             ("user-guide.html", "Command reference"),
             ("documentation.html", "Documentation"), ("overview.html", "Overview"),
             ("architecture.html", "Architecture"), ("verification.html", "Verification"),
             ("reference-files.html", "Reference files")]

    def page_html(page, title, description, source_path, body, toc):
        navigation = "".join('<a href="' + name + '"'
                             + (' aria-current="page"' if name == page else '')
                             + '>' + label + '</a>' for name, label in pages)
        rendered = render_page(template, {
            "PAGE": page, "TITLE": title, "DESCRIPTION": description,
        }).decode()
        for marker, block in (("DOCUMENT_NAV", navigation), ("DOCUMENT_CONTENT", body),
                              ("DOCUMENT_TOC", toc)):
            comment = "<!-- " + marker + " -->"
            require(rendered.count(comment) == 1, "documentation template marker changed: " + marker)
            rendered = rendered.replace(comment, block, 1)
        return rendered.encode()

    cards = []
    for name, page, label, description in DOCUMENTS:
        path = "docs/" + name
        data = (source / path).read_bytes()
        body, toc = render_document(data.decode("utf-8"), info)
        page_title = "Guided Coding " + (label if label == "User Guide" else label.lower())
        outputs[page] = page_html(page, page_title, description,
                                  path, '<article class="gc-document">' + body + '</article>',
                                  '<details class="gc-panel gc-toc" open><summary>On this page</summary><div>'
                                  + toc + '</div></details>')
        records.append({"source": path, "source_sha256": digest(data), "page": page,
                        "original_sha256": digest((original_source / path).read_bytes())
                        if original_source else digest(data),
                        "page_sha256": digest(outputs[page])})
        cards.append('<div class="card"><h2>' + label + '</h2><p>' + description
                     + '</p><a class="card-link" href="' + page + '">Read ' + label.lower() + '</a></div>')
    references = (("payload/DEVELOPER_GUIDE_CONTRACT.md", "Developer–Guide Contract"),
                  ("payload/ROLES.md", "Roles and responsibilities"),
                  ("payload/SETUP.md", "Project setup procedure"),
                  ("payload/SETUP_DEFAULTS.md", "General setup defaults"),
                  ("payload/templates/PROJECT_METHOD.md", "Project method template"),
                  ("payload/GUIDE.md", "Guide instructions"),
                  ("payload/WORKER.md", "Worker instructions"),
                  ("payload/OUTSIDE_REVIEWER_BRIEF.md", "Outside reviewer brief"),
                  ("payload/REVIEW_TRANSPORT.md", "Review package instructions"))
    reference_links = "".join('<li><a href="' + documentation_link("../" + path, info)
                              + '">' + label + '</a></li>' for path, label in references)
    reference_records, reference_blocks, reference_toc = [], [], []
    main_docs = {"docs/" + item[0] for item in DOCUMENTS}
    for path in sorted(p for p in source.rglob("*") if p.is_file()):
        name = path.relative_to(source).as_posix()
        if name in main_docs:
            continue
        data = path.read_bytes()
        anchor = reference_id(name)
        reference_records.append({"source": name, "source_sha256": digest(data), "anchor": anchor})
        reference_toc.append('<li><a href="#' + anchor + '">' + html.escape(name) + '</a></li>')
        reference_blocks.append('<section><h2 id="' + anchor + '">' + html.escape(name)
                                + '</h2><pre><code>' + html.escape(data.decode("utf-8"))
                                + '</code></pre></section>')
    reference_body = ('<p>These are the procedure instructions, tools and tests included in the '
                      'download, shown as exact file text. The user guide explains everyday use.</p>'
                      + ''.join(reference_blocks))
    outputs["reference-files.html"] = page_html("reference-files.html", "Guided Coding reference files",
        "Complete procedure instructions, checking tools, templates and tests for this edition.", "",
        reference_body, '<details class="gc-panel gc-toc" open><summary>Files on this page</summary><div><ul class="gc-reference-list">'
        + ''.join(reference_toc) + '</ul></div></details>')
    body = ('<p>Start with the user guide for everyday use. The other pages explain the procedure, '
            'its implementation and the evidence behind it.</p><div class="card-grid">' + "".join(cards)
            + '</div><h2 id="procedure-files">Procedure and reference files</h2>'
            '<p>These links open the reference files here on the website. The same general-edition '
            'files are included in the ZIP.</p><ul>' + reference_links + '</ul>' + historical_note(info))
    outputs["documentation.html"] = page_html("documentation.html", "Guided Coding documentation",
        "User guide, overview, architecture, verification and procedure reference files.", "docs", body, "")
    return outputs, {"pages": records,
                     "references": {"page": "reference-files.html",
                                    "page_sha256": digest(outputs["reference-files.html"]),
                                    "files": reference_records},
                     "index": {"page": "documentation.html", "page_sha256": digest(outputs["documentation.html"])}}


def build_artifacts(source, info, license_data, site, scratch):
    original = source_snapshot(source)
    minimum = check_hooks(source)
    require(info["source_manifest_sha256"] == original["SOURCE_MANIFEST.sha256"][0]
            and info["source_files"] == len(original), "source identity differs from download metadata")
    require(info["license_sha256"] == digest(license_data), "license differs from download metadata")
    checks = run_contract_checks(source, minimum, scratch)
    require_unchanged_source(source, original)
    tests = run_package_tests(source, scratch)
    require_unchanged_source(source, original)
    adapted = scratch / "general-edition"
    edition = general_source(source, adapted)
    packaged_snapshot = source_snapshot(adapted)
    require(check_hooks(adapted) == minimum, "general edition changed the client version contract")
    (scratch / "edition-checks").mkdir()
    (scratch / "edition-tests").mkdir()
    edition_checks = run_contract_checks(adapted, minimum, scratch / "edition-checks")
    require_unchanged_source(adapted, packaged_snapshot)
    edition_tests = run_package_tests(adapted, scratch / "edition-tests")
    require_unchanged_source(adapted, packaged_snapshot)
    release = (source / "payload/RELEASE").read_text().strip()
    version = ".".join(map(str, minimum))
    documentation, documentation_metadata = build_documentation(adapted, info, site, source)
    metadata = {"package_format": 2, "upstream": info, "general_edition": edition, "release": release,
                "generator": {"script_sha256": digest(Path(__file__).read_bytes()),
                              "template_sha256": digest((site / "index.template.html").read_bytes()),
                              "docs_template_sha256": digest((site / "docs.template.html").read_bytes()),
                              "main_copy_sha256": digest((site / "main-page.md").read_bytes())},
                "documentation": documentation_metadata,
                "minimum_claude_version": version, "checks": edition_checks,
                "package_tests": edition_tests, "historical_source_checks": checks,
                "historical_source_tests": tests,
                "general_card_sha256": digest((site / "GENERAL_DEVELOPER_CARD.md").read_bytes())}
    encoded_metadata = (json.dumps(metadata, indent=2, sort_keys=True) + "\n").encode()
    extras = {
        "PACKAGE_INFO.json": encoded_metadata, "LICENSE.txt": license_data,
        "INSTALL.md": installation_text(info, version, edition),
        "GENERAL_DEVELOPER_CARD.md": (site / "GENERAL_DEVELOPER_CARD.md").read_bytes(),
    }
    archive = make_zip(adapted, extras)
    sha = digest(archive)
    public_metadata = {**metadata, "archive": {"file": "guided_coding.zip", "sha256": sha,
                                              "bytes": len(archive)}}
    page = render_page((site / "index.template.html").read_text(), {
        "COMMIT_SHORT": info["commit"][:12],
        "COMMIT_DATE": info["commit_date"][:10], "ZIP_SHA": sha,
        "ZIP_KB": str(round(len(archive) / 1024)), "MIN_VERSION": version,
        "DOWNLOAD_URL": "guided_coding.zip", "DOWNLOAD_LABEL": "Download Guided Coding",
        "PACKAGE_STATUS": "Complete general-edition kit, setup card and installation notes.",
    })
    copy = (site / "main-page.md").read_text()
    body, _ = render_document(copy, info)
    main_marker = b"<!-- MAIN_COPY -->"
    require(page.count(main_marker) == 1, "main-page copy marker changed; inspect the generator")
    page = page.replace(main_marker, body.encode(), 1)
    marker = b"<!-- PACKAGE_SOURCE -->"
    require(page.count(marker) == 1, "package-source template marker changed; inspect the generator")
    page = page.replace(marker, package_source_note(info).encode(), 1)
    artifacts = {"guided_coding.zip": archive, "guided_coding.zip.sha256": (sha + "  guided_coding.zip\n").encode(),
            "package.json": (json.dumps(public_metadata, indent=2, sort_keys=True) + "\n").encode(),
            "index.html": page, **documentation}
    documents = {name: data for name, data in artifacts.items() if name.endswith(".html")}
    documents.update({name: extras[name] for name in ("INSTALL.md", "GENERAL_DEVELOPER_CARD.md")})
    if (site / "README.md").is_file():
        documents["README.md"] = (site / "README.md").read_bytes()
    verify_general_documentation(documents, info)
    require_unchanged_source(source, original)
    require_unchanged_source(adapted, packaged_snapshot)
    return artifacts


def publish_local(site, artifacts):
    """Serialize short output replacements; never interleave two matching sets."""
    lock = site / ".gc-write-lock"
    try:
        lock.mkdir()
    except FileExistsError as error:
        raise PackageError("site output write is locked; another builder may be writing. "
                           "If a previous builder stopped, inspect it before removing .gc-write-lock") from error
    retain_lock = False
    try:
        _publish_local_locked(site, artifacts)
    except RecoveryError:
        retain_lock = True
        raise
    finally:
        if not retain_lock:
            lock.rmdir()


def _publish_local_locked(site, artifacts):
    """Back up outputs on disk; retain every backup if any restoration fails."""
    require(set(artifacts) == set(OUTPUTS), "unexpected generated output list")
    originals = {}
    for name in OUTPUTS:
        path = site / name
        require(not path.is_symlink() and (not path.exists() or path.is_file()),
                f"output is not an ordinary file: {name}")
        originals[name] = path if path.exists() else None
    staging = Path(tempfile.mkdtemp(prefix=".gc-stage-", dir=site)).resolve()
    retain_recovery = False
    try:
        backups = staging / "originals"
        pending = staging / "new"
        restore = staging / "restore"
        for directory in (backups, pending, restore):
            directory.mkdir()
        record = {}
        for name, path in originals.items():
            if path is None:
                record[name] = None
            else:
                data = path.read_bytes()
                mode = stat.S_IMODE(path.stat().st_mode)
                (backups / name).write_bytes(data)
                (backups / name).chmod(mode)
                record[name] = {"sha256": digest(data), "mode": mode}
        (staging / "RECOVERY.json").write_text(
            json.dumps({"site": str(site.resolve()), "originals": record}, indent=2) + "\n")
        (staging / "RECOVERY.md").write_text(
            "# Recover the previous matching output set\n\n"
            "An output replacement failed and one or more restorations also failed.\n"
            "Do not publish the site or rerun its builder until recovery is complete.\n"
            "The error message names this directory; RECOVERY.json names the site\n"
            "and lists every generated output, its original hash and mode.\n\n"
            "After resolving the filesystem error, copy every file from originals/\n"
            "back to its same name in that site, preserving the recorded mode.\n"
            "For each output recorded as null, remove that output from the site:\n"
            "it did not exist before this build. Verify all recorded hashes and\n"
            "absences. The backups remain valid even for outputs already restored.\n"
            "Then remove the site's empty .gc-write-lock directory and this recovery\n"
            "directory, and rebuild if desired. Leave both in place until verified.\n")
        for name, data in artifacts.items():
            (pending / name).write_bytes(data)
        replaced = []
        try:
            for name in OUTPUTS:  # page last: its download metadata matches this archive
                os.replace(pending / name, site / name)
                replaced.append(name)
        except OSError as replacement_error:
            rollback_errors = []
            for name in reversed(replaced):
                try:
                    if originals[name] is None:
                        (site / name).unlink(missing_ok=True)
                    else:
                        # Replace from a copy, so successful restoration never consumes a backup.
                        shutil.copyfile(backups / name, restore / name)
                        (restore / name).chmod(record[name]["mode"])
                        os.replace(restore / name, site / name)
                except OSError as error:
                    rollback_errors.append(f"{name}: {error}")
            if rollback_errors:
                retain_recovery = True
                raise RecoveryError(
                    f"output replacement failed: {replacement_error}; restoration failed: "
                    + "; ".join(rollback_errors)
                    + f". Outputs may be mismatched. Recovery copies and instructions retained at {staging}. "
                    "The .gc-write-lock is retained; recover before rebuilding or publishing.") from replacement_error
            raise
    finally:
        if not retain_recovery:
            shutil.rmtree(staging)




def prepare_local_documentation(local, baseline, info, destination):
    """Validate a documentation-only working copy against the fetched baseline."""
    original = source_snapshot(baseline)
    proposed = source_snapshot(local)
    allowed = {"SOURCE_MANIFEST.sha256", "SKILL.md",
               *("docs/" + name for name, _, _, _ in DOCUMENTS)}
    for name in set(original) | set(proposed):
        require(name in allowed or original.get(name) == proposed.get(name),
                "local preview changed executable or procedure source: " + name)
    skill = (baseline / "SKILL.md").read_bytes()
    expected = skill.replace(b"docs/GUIDED_CODING_USER_GUIDE.md",
                             b"docs/GUIDED_CODING_COMMAND_REFERENCE.md")
    require((local / "SKILL.md").read_bytes() in (skill, expected),
            "local preview changed the skill beyond the command-reference path")
    shutil.copytree(local, destination)
    require_unchanged_source(local, proposed)
    return {**info, "input_kind": "local-documentation-preview",
            "base_source_manifest_sha256": info["source_manifest_sha256"],
            "source_manifest_sha256": proposed["SOURCE_MANIFEST.sha256"][0],
            "source_files": len(proposed), "source_tree": None}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", default="master", help="upstream ref or accepted commit (default: current master)")
    parser.add_argument("--check-only", action="store_true", help="run all checks without replacing site outputs")
    parser.add_argument("--source-dir", type=Path,
                        help="build a documentation-only local preview; --ref must name its full baseline commit")
    args = parser.parse_args(argv)
    try:
        require(sys.version_info >= (3, 10), "Python 3.10 or newer is required")
        require(os.name == "posix", "the current kit and checks require macOS or Linux")
        require(shutil.which("git") is not None, "Git is needed for the upstream tests")
        require(shutil.which("shasum") is not None, "shasum is needed by the installed skill")
        for name in ("index.template.html", "docs.template.html", "main-page.md", "GENERAL_DEVELOPER_CARD.md"):
            require((SITE / name).is_file(), f"site input missing: {name}")
        with tempfile.TemporaryDirectory(prefix="guided-coding-package-") as temporary:
            root = Path(temporary).resolve()  # Mac /var may alias /private/var
            source = root / "unchanged-source"
            print(f"Fetching {UPSTREAM}:{args.ref} ...", flush=True)
            if args.source_dir is not None:
                require(SHA.fullmatch(args.ref) is not None,
                        "a local preview needs --ref with its full baseline commit")
                baseline = root / "verified-baseline"
                info, license_data = download_source(args.ref, baseline)
                info = prepare_local_documentation(args.source_dir.resolve(strict=True), baseline, info, source)
            else:
                info, license_data = download_source(args.ref, source)
            print(f"Pinned source: {info['commit']}; checking hooks and tests ...", flush=True)
            scratch = root / "checks"
            scratch.mkdir()
            artifacts = build_artifacts(source, info, license_data, SITE, scratch)
            if args.check_only:
                print("CHECKED; no site outputs changed")
            else:
                publish_local(SITE, artifacts)
                print("PACKAGED " + str(SITE / "guided_coding.zip"))
                print("Review git diff, then commit and push the website when ready.")
        return 0
    except (ValueError, KeyError, TypeError, OSError, subprocess.TimeoutExpired, SyntaxError) as error:
        print("NOT PACKAGED: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
