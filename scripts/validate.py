#!/usr/bin/env python3
"""Check the Natural Voice repository before a release or a pull request.

Run from the repository root:  python3 scripts/validate.py

It uses only Python's standard library and changes nothing. It checks that:
  1. the version is the same in every file listed in .version-bump.json, and the
     CHANGELOG entry for it is written;
  2. SKILL.md follows the Agent Skills rules (allowed keys, name, lengths);
  3. every JSON file parses, and the plugin manifests agree with each other;
  4. no personal data is in the repository (voice files, notes, drafts, settings, folders
     of samples, voices or drafts, real email addresses);
  5. every backticked .md path in the skill, commands and agents points at a real file;
  6. the frontmatter of commands, agents and skills is valid YAML;
  7. dist/ matches what scripts/build.py would build now.

Each problem is explained in plain English. It exits with 1 if there is any problem.
"""
import io
import json
import pathlib
import re
import subprocess
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build  # noqa: E402
import bump_version  # noqa: E402

SKILLS = ROOT / "skills"
DIST = ROOT / "dist"

# Agent Skills specification (https://agentskills.io/specification).
SPEC_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
SPEC_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SPEC_DESCRIPTION_LIMIT = 1024
SPEC_COMPATIBILITY_LIMIT = 500
SKILL_BODY_LINE_LIMIT = 500
REQUIRED_METADATA = ("version", "released")

# Agent Plugins 1.0.0 (https://agent-plugins.org/schemas/1.0.0/plugin.schema.json).
AGENT_PLUGINS_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
AGENT_PLUGINS_KEYS = {"$schema", "name", "version", "description", "author", "homepage",
                      "repository", "license", "keywords", "extensions"}
AGENT_PLUGINS_NAME = re.compile(r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
REVERSE_DOMAIN = re.compile(r"^[a-z0-9-]+(\.[a-z0-9-]+)+$")

PLUGIN_NAME = "natural-voice"

EMAIL = re.compile(r"(?<![\w.+-])([A-Za-z0-9._%+-]+)@([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,})")
ALLOWED_EMAIL_DOMAINS = ("example.com", "example.org", "example.net", "users.noreply.github.com")
ALLOWED_EMAIL_LOCALS = ("noreply", "no-reply")
ALLOWED_EMAILS = {"git@github.com"}

# A person's own files: their notes, drafts and settings, and folders of their samples,
# voices or drafts. Only the skill's templates and the made-up files in examples/ and
# tests/ may use these names.
PERSONAL_FOLDERS = {"samples", "voices", "drafts"}
TEMPLATES = "skills/natural-voice/references/templates/"
MADE_UP_FOLDERS = ("examples", "tests")
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yml", ".yaml", ".py", ".toml", ".cfg", ".ini", ".sh", ".html", ""}
SKIP_DIRS = {".git", "dist", "node_modules", "__pycache__"}


class Report:
    def __init__(self):
        self.problems = []

    def add(self, area, message):
        self.problems.append((area, message))


# ---------------------------------------------------------------- helpers

def rel(path):
    return path.relative_to(ROOT).as_posix()


def repo_files():
    """Files git would commit: tracked ones plus new ones that aren't ignored."""
    try:
        out = subprocess.run(
            ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            cwd=ROOT, capture_output=True, check=True,
        ).stdout.decode("utf-8")
        names = sorted(set(filter(None, out.split("\0"))))
        return [ROOT / name for name in names if (ROOT / name).is_file()]
    except (OSError, subprocess.CalledProcessError):
        files = []
        for path in sorted(ROOT.rglob("*")):
            if path.is_file() and not any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
                files.append(path)
        return files


def load_json(path, report, area="JSON"):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        report.add(area, f"{rel(path)} is missing.")
    except ValueError as error:
        report.add(area, f"{rel(path)} isn't valid JSON: {error}.")
    return None


def mask(local, domain):
    return f"{local[:1]}***@{domain}"


# ---------------------------------------------------------------- 1. versions

def check_versions(report):
    area = "Version"
    try:
        found = bump_version.read_all()
    except bump_version.VersionError as error:
        report.add(area, str(error))
        return
    versions = {version for _, version, _ in found}
    if None in versions:
        for path, version, _ in found:
            if version is None:
                report.add(area, f"{path} has no version where .version-bump.json says it should be.")
        return
    if len(versions) > 1:
        listing = "; ".join(f"{path} says {version}" for path, version, _ in found)
        report.add(
            area,
            f"The version isn't the same everywhere ({listing}). "
            "Run: python3 scripts/bump_version.py <new version>",
        )
    for path, version, _ in found:
        if not bump_version.SEMVER.fullmatch(str(version)):
            report.add(area, f"{path} has version '{version}', which isn't three numbers like 1.0.0.")
    dates = {path: date for path, _, date in found if date is not None}
    if len(set(dates.values())) > 1:
        listing = "; ".join(f"{path} says {date}" for path, date in dates.items())
        report.add(area, f"The release date isn't the same everywhere ({listing}).")

    changelog = ROOT / "CHANGELOG.md"
    if changelog.is_file() and bump_version.PLACEHOLDER in changelog.read_text(encoding="utf-8"):
        report.add(area, f"CHANGELOG.md still has the placeholder line '{bump_version.PLACEHOLDER.rstrip('.')}'. Replace it with what changed in this release.")

    # The version lives in plugin.json only, never in the marketplace entry as well.
    market = ROOT / ".claude-plugin" / "marketplace.json"
    data = load_json(market, report) if market.is_file() else None
    if isinstance(data, dict):
        for entry in data.get("plugins", []):
            if isinstance(entry, dict) and "version" in entry:
                report.add(area, ".claude-plugin/marketplace.json sets a version for a plugin. "
                                 "Remove it: Claude Code reads the version from .claude-plugin/plugin.json.")

    # Every manifest that holds a version is listed in .version-bump.json.
    listed = {path for path, _, _ in found}
    for candidate in ("plugin.json", ".claude-plugin/plugin.json", "gemini-extension.json",
                      ".codex-plugin/plugin.json", ".cursor-plugin/plugin.json", "package.json"):
        path = ROOT / candidate
        if path.is_file() and candidate not in listed:
            data = load_json(path, report)
            if isinstance(data, dict) and "version" in data:
                report.add(area, f"{candidate} has a version but isn't listed in .version-bump.json, "
                                 "so a version bump would miss it. Add it there.")


# ---------------------------------------------------------------- 2. SKILL.md

def check_skills(report):
    area = "SKILL.md"
    skill_dirs = sorted(p.parent for p in SKILLS.glob("*/SKILL.md"))
    if not skill_dirs:
        report.add(area, "No skills/<name>/SKILL.md found.")
    for folder in skill_dirs:
        path = folder / "SKILL.md"
        label = rel(path)
        try:
            data, plain_keys = build.frontmatter_of(path)
        except build.FrontmatterError as error:
            report.add(area, str(error))
            continue
        extra = sorted(set(data) - SPEC_KEYS)
        if extra:
            report.add(area, f"{label} has frontmatter keys the Agent Skills format doesn't allow: "
                             f"{', '.join(extra)}. Apps such as claude.ai refuse the upload. "
                             "Move them under metadata, or remove them.")
        name = data.get("name")
        if name != folder.name:
            report.add(area, f"{label}: name is '{name}' but the folder is '{folder.name}'. They must match.")
        elif not SPEC_NAME.fullmatch(name) or len(name) > 64:
            report.add(area, f"{label}: name '{name}' must be lowercase letters, numbers and single hyphens, "
                             "up to 64 characters.")
        description = data.get("description")
        if not isinstance(description, str) or not description.strip():
            report.add(area, f"{label} has no description.")
        else:
            if len(description) > SPEC_DESCRIPTION_LIMIT:
                report.add(area, f"{label}: the description is {len(description)} characters. "
                                 f"The Agent Skills limit is {SPEC_DESCRIPTION_LIMIT}.")
            if len(description) > build.DESCRIPTION_LIMIT:
                report.add(area, f"{label}: the description is {len(description)} characters. "
                                 f"Keep it to {build.DESCRIPTION_LIMIT} so it fits every app.")
        compatibility = data.get("compatibility")
        if compatibility is not None and (not isinstance(compatibility, str) or
                                          len(compatibility) > SPEC_COMPATIBILITY_LIMIT):
            report.add(area, f"{label}: compatibility must be text of {SPEC_COMPATIBILITY_LIMIT} characters or fewer.")
        metadata = data.get("metadata")
        if metadata is not None:
            if not isinstance(metadata, dict):
                report.add(area, f"{label}: metadata must be a list of 'key: \"value\"' lines.")
            else:
                for key, value in metadata.items():
                    plain = f"metadata.{key}" in plain_keys
                    if not isinstance(value, str) or (plain and build.NOT_A_STRING.fullmatch(value)):
                        report.add(area, f"{label}: metadata.{key} must be text. Put the value in double quotes, "
                                         f"like {key}: \"{value}\".")
        if folder.name == PLUGIN_NAME:
            for key in REQUIRED_METADATA:
                if not isinstance(metadata, dict) or key not in metadata:
                    report.add(area, f"{label}: metadata.{key} is missing. The version tools need it.")
        body = build.strip_frontmatter(path.read_text(encoding="utf-8"))
        lines = body.count("\n") + 1
        if lines >= SKILL_BODY_LINE_LIMIT:
            report.add(area, f"{label} is {lines} lines long. Keep it under {SKILL_BODY_LINE_LIMIT} "
                             "and move detail into references/.")


# ---------------------------------------------------------------- 3. JSON and manifests

def check_manifests(report, files):
    area = "Manifests"
    for path in files:
        if path.suffix == ".json":
            load_json(path, report)

    names = {}

    claude = load_json(ROOT / ".claude-plugin" / "plugin.json", report, area)
    if isinstance(claude, dict):
        names[".claude-plugin/plugin.json"] = claude.get("name")
        author = claude.get("author", {})
        if isinstance(author, dict) and "email" in author:
            report.add(area, ".claude-plugin/plugin.json lists an author email. Remove it to keep it private.")

    market = load_json(ROOT / ".claude-plugin" / "marketplace.json", report, area)
    if isinstance(market, dict):
        for i, entry in enumerate(market.get("plugins", [])):
            names[f".claude-plugin/marketplace.json plugins[{i}]"] = entry.get("name")
            if entry.get("source") != "./":
                report.add(area, ".claude-plugin/marketplace.json: the plugin source should be \"./\" "
                                 "(this repository is the plugin).")

    portable = load_json(ROOT / "plugin.json", report, area)
    if isinstance(portable, dict):
        names["plugin.json"] = portable.get("name")
        if portable.get("$schema") != AGENT_PLUGINS_SCHEMA:
            report.add(area, f"plugin.json: $schema must be {AGENT_PLUGINS_SCHEMA}.")
        extra = sorted(set(portable) - AGENT_PLUGINS_KEYS)
        if extra:
            report.add(area, f"plugin.json has keys Agent Plugins 1.0.0 doesn't allow: {', '.join(extra)}. "
                             "Put app-specific settings under extensions.")
        if not AGENT_PLUGINS_NAME.fullmatch(str(portable.get("name", ""))):
            report.add(area, "plugin.json: the name must be lowercase letters, numbers, dots and hyphens.")
        author = portable.get("author", {})
        if not isinstance(author, dict) or set(author) - {"name", "email", "url"}:
            report.add(area, "plugin.json: author may only have name, email and url.")
        elif "email" in author:
            report.add(area, "plugin.json lists an author email. Remove it to keep it private.")
        for key, value in (portable.get("extensions") or {}).items():
            if not REVERSE_DOMAIN.fullmatch(key) or not isinstance(value, dict):
                report.add(area, f"plugin.json: extensions.{key} must be a reverse-domain name holding an object.")

    gemini = load_json(ROOT / "gemini-extension.json", report, area)
    if isinstance(gemini, dict):
        names["gemini-extension.json"] = gemini.get("name")
        context = gemini.get("contextFileName")
        if context and not (ROOT / context).is_file():
            report.add(area, f"gemini-extension.json points at {context}, which doesn't exist.")

    codex = load_json(ROOT / ".agents" / "plugins" / "marketplace.json", report, area)
    if isinstance(codex, dict):
        for i, entry in enumerate(codex.get("plugins", [])):
            label = f".agents/plugins/marketplace.json plugins[{i}]"
            names[label] = entry.get("name")
            policy = entry.get("policy") or {}
            missing = [key for key in ("source", "category") if not entry.get(key)]
            missing += [f"policy.{key}" for key in ("installation", "authentication") if not policy.get(key)]
            if missing:
                report.add(area, f"{label} is missing {', '.join(missing)}. Codex needs them.")

    skill_name = None
    try:
        skill_name = build.frontmatter_of(build.SKILL / "SKILL.md")[0].get("name")
    except (build.FrontmatterError, FileNotFoundError):
        pass
    names["skills/natural-voice/SKILL.md"] = skill_name
    wrong = {where: name for where, name in names.items() if name != PLUGIN_NAME}
    for where, name in wrong.items():
        report.add(area, f"{where} uses the name '{name}'. Every manifest should say '{PLUGIN_NAME}'.")

    openai = build.SKILL / "agents" / "openai.yaml"
    if openai.is_file():
        text = openai.read_text(encoding="utf-8")
        for key in ("interface:", "display_name:", "short_description:", "default_prompt:"):
            if key not in text:
                report.add(area, f"{rel(openai)} is missing '{key}'.")
        if "$" + PLUGIN_NAME not in text:
            report.add(area, f"{rel(openai)}: default_prompt should mention ${PLUGIN_NAME} so Codex picks the skill.")
        if "\t" in text:
            report.add(area, f"{rel(openai)} uses a tab. YAML needs spaces.")
    else:
        report.add(area, f"{rel(openai)} is missing. Codex and ChatGPT use it for the skill's name and prompt.")

    if (ROOT / "bin").is_dir():
        report.add(area, "There is a top-level bin/ folder. claude.ai and Cowork refuse to install a plugin "
                         "that has one. Move it.")
    if (ROOT / "CLAUDE.md").is_file():
        report.add(area, "CLAUDE.md is at the repository root, which makes 'claude plugin validate --strict' fail. "
                         "Keep it at .claude/CLAUDE.md.")


# ---------------------------------------------------------------- 4. personal data

def allowed_email_domain(domain):
    """example.com and its subdomains, but not lookalikes such as notexample.com."""
    return (any(domain == allowed or domain.endswith("." + allowed) for allowed in ALLOWED_EMAIL_DOMAINS)
            or domain.endswith(".example"))


def personal_file_problem(name):
    """Why this repository path looks like someone's own file, or None."""
    parts = name.split("/")
    if parts[-1].endswith(build.PERSONAL_SUFFIXES):
        if parts[0] == "examples":
            return None
        return (f"{name} looks like someone's voice file. Voice files never go in the repository "
                "(only made-up ones in examples/). Remove it.")
    if parts[0] in MADE_UP_FOLDERS:
        return None
    if parts[-1] in build.PERSONAL_NAMES and not name.startswith(TEMPLATES):
        return (f"{name} has the name of someone's own notes, draft or settings file. Those stay on the "
                "person's computer. Remove it, or rename it if it's a real part of the project.")
    folder = next((part for part in parts[:-1] if part.lower() in PERSONAL_FOLDERS), None)
    if folder:
        return (f"{name} is in a '{folder}' folder, which is where someone's own writing or voice files "
                "would live. Remove it (made-up examples go in examples/ or tests/).")
    return None


def check_personal_data(report, files):
    area = "Privacy"
    for path in files:
        name = rel(path)
        top = name.split("/", 1)[0]
        problem = personal_file_problem(name)
        if problem:
            report.add(area, problem)
        if top in SKIP_DIRS or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for problem in email_problems(name, text):
            report.add(area, problem)


def email_problems(name, text):
    """A message for each real-looking email address in the text."""
    problems = []
    for number, line in enumerate(text.splitlines(), 1):
        for match in EMAIL.finditer(line):
            local, domain = match.group(1), match.group(2).lower()
            address = f"{local}@{domain}".lower()
            if address in ALLOWED_EMAILS or local.lower() in ALLOWED_EMAIL_LOCALS or allowed_email_domain(domain):
                continue
            problems.append(f"{name}, line {number}: has an email address ({mask(local, domain)}). "
                            "Remove it, or use an example.com address in examples.")
    return problems


# ---------------------------------------------------------------- 5 and 6. paths and frontmatter

def check_paths_and_frontmatter(report):
    skill_md = sorted(SKILLS.glob("*/SKILL.md"))
    references = sorted(build.REFS.rglob("*.md"))
    commands = sorted((ROOT / "commands").glob("*.md"))
    agents = sorted((ROOT / "agents").glob("*.md"))
    maintainer = sorted((ROOT / ".claude" / "commands").glob("*.md"))
    for problem in build.reference_problems(skill_md + references + commands + agents + maintainer):
        report.add("Paths", problem)
    for problem in build.frontmatter_problems(commands + agents + maintainer + skill_md):
        report.add("Frontmatter", problem)


# ---------------------------------------------------------------- 7. dist

def zip_members(data):
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        return sorted((info.filename, z.read(info)) for info in z.infolist())


def check_dist(report):
    area = "dist"
    try:
        expected = build.build_outputs(quiet=True)
    except build.BuildError as error:
        already = {message for _, message in report.problems}
        lines = [line[2:] if line.startswith("- ") else line for line in str(error).splitlines()]
        new = [line for line in lines if line not in already]
        if new:
            report.add(area, "The build fails, so dist/ can't be checked:\n" + "\n".join("- " + line for line in new))
        else:
            report.add(area, "The build fails because of the problems above, so dist/ can't be checked yet.")
        return
    for name, data in expected.items():
        path = DIST / name
        if not path.is_file():
            report.add(area, f"dist/{name} is missing. Run: python3 scripts/build.py")
            continue
        actual = path.read_bytes()
        if name.endswith(".zip"):
            try:
                same = zip_members(actual) == zip_members(data)
            except zipfile.BadZipFile:
                same = False
        else:
            same = actual == data
        if not same:
            report.add(area, f"dist/{name} is out of date. Run: python3 scripts/build.py")
    for old in build.OLD_OUTPUT_NAMES:
        if (DIST / old).exists():
            report.add(area, f"dist/{old} uses an old name. Delete it (the build does this for you).")


# ---------------------------------------------------------------- main

CHECKS = [
    ("versions match", lambda report, files: check_versions(report)),
    ("SKILL.md follows the Agent Skills rules", lambda report, files: check_skills(report)),
    ("JSON and plugin manifests", check_manifests),
    ("no personal data", check_personal_data),
    ("file paths and frontmatter", lambda report, files: check_paths_and_frontmatter(report)),
    ("dist/ is up to date", lambda report, files: check_dist(report)),
]


def main():
    report = Report()
    files = repo_files()
    for _, check in CHECKS:
        check(report, files)
    if not report.problems:
        print("All checks passed:")
        for label, _ in CHECKS:
            print(f"  ok  {label}")
        return 0
    print(f"Found {len(report.problems)} problem(s). Nothing was changed.\n")
    for area, message in report.problems:
        first, *rest = message.splitlines()
        print(f"- [{area}] {first}")
        for line in rest:
            print(f"    {line}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
