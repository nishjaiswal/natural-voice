#!/usr/bin/env python3
"""Change the Natural Voice version in every file at once.

Run from the repository root:
    python3 scripts/bump_version.py 1.0.1
    python3 scripts/bump_version.py 1.1.0 --date 2026-11-08

It reads .version-bump.json, which lists every file that holds the version, and
updates each one. In SKILL.md it also sets metadata.released to the date (today
unless you give --date). In CHANGELOG.md it adds a new heading at the top with a
placeholder line for you to replace, or updates the date if the heading for this
version is already there. scripts/validate.py fails until the placeholder is gone.

Which number to change:
  patch (1.0.0 to 1.0.1)  a content refresh: new or faded patterns, updated sources, fixes
  minor (1.0.0 to 1.1.0)  a new feature, job or mode
  major (1.0.0 to 2.0.0)  a change that breaks existing voice files or installs
"""
import argparse
import datetime
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONFIG = ROOT / ".version-bump.json"
sys.path.insert(0, str(ROOT / "scripts"))

import build  # noqa: E402  (same folder; shares the frontmatter reader)

SEMVER = re.compile(r"\d+\.\d+\.\d+")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
CHANGELOG_HEADING = re.compile(r"^## (\d+\.\d+\.\d+) \((\d{4}-\d{2}-\d{2})\)\s*$")
PLACEHOLDER = "Describe what changed, in plain words."


class VersionError(Exception):
    pass


# ---------------------------------------------------------------- reading

def load_config():
    if not CONFIG.is_file():
        raise VersionError(".version-bump.json is missing from the repository root.")
    try:
        entries = json.loads(CONFIG.read_text(encoding="utf-8"))["files"]
    except (ValueError, KeyError) as error:
        raise VersionError(f".version-bump.json can't be read: {error}") from None
    for entry in entries:
        if entry.get("format") not in ("json", "frontmatter", "changelog") or not entry.get("path"):
            raise VersionError(f".version-bump.json has an entry it doesn't understand: {entry}")
    return entries


def _get(data, dotted):
    for part in dotted.split("."):
        if not isinstance(data, dict) or part not in data:
            return None
        data = data[part]
    return data


def _set(data, dotted, value):
    parts = dotted.split(".")
    for part in parts[:-1]:
        data = data.setdefault(part, {})
    data[parts[-1]] = value


def first_changelog_heading(text):
    """(line index, version, date) of the first '## ' heading, or (None, None, None)."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("## "):
            match = CHANGELOG_HEADING.match(line)
            if not match:
                raise VersionError(
                    f"CHANGELOG.md: the first entry heading should look like '## 1.0.0 (2026-10-08)', "
                    f"found '{line.strip()}'."
                )
            return i, match.group(1), match.group(2)
    return None, None, None


def read_entry(entry):
    """(version, date) held by one file. date is None where the file has no date."""
    path = ROOT / entry["path"]
    if not path.is_file():
        raise VersionError(f"{entry['path']} is listed in .version-bump.json but doesn't exist.")
    text = path.read_text(encoding="utf-8")
    kind = entry["format"]
    if kind == "json":
        try:
            data = json.loads(text)
        except ValueError as error:
            raise VersionError(f"{entry['path']} isn't valid JSON: {error}") from None
        return _get(data, entry["field"]), None
    if kind == "frontmatter":
        try:
            data, _ = build.parse_frontmatter(text, entry["path"])
        except build.FrontmatterError as error:
            raise VersionError(str(error)) from None
        date = _get(data, entry["date_field"]) if entry.get("date_field") else None
        return _get(data, entry["field"]), date
    _, version, date = first_changelog_heading(text)
    return version, date


def read_all():
    """[(path, version, date)] for every file in .version-bump.json."""
    return [(entry["path"], *read_entry(entry)) for entry in load_config()]


# ---------------------------------------------------------------- writing

def set_json(text, field, value):
    data = json.loads(text)
    old = _get(data, field)
    key = field.split(".")[-1]
    if isinstance(old, str):
        pattern = re.compile(r'("%s"\s*:\s*)"%s"' % (re.escape(key), re.escape(old)))
        if len(pattern.findall(text)) == 1:
            # Change only that value, so the rest of the file keeps its layout.
            return pattern.sub(lambda m: m.group(1) + json.dumps(value), text)
    _set(data, field, value)
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def set_frontmatter(text, dotted, value):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        raise VersionError("SKILL.md has no frontmatter to update.")
    end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    quoted = json.dumps(value)
    parent, _, child = dotted.rpartition(".")
    if not parent:
        for i in range(1, end):
            if re.match(rf"^{re.escape(child)}:", lines[i]):
                lines[i] = f"{child}: {quoted}"
                return "\n".join(lines)
        lines.insert(end, f"{child}: {quoted}")
        return "\n".join(lines)
    start = next((i for i in range(1, end) if re.match(rf"^{re.escape(parent)}:\s*$", lines[i])), None)
    if start is None:
        lines[end:end] = [f"{parent}:", f"  {child}: {quoted}"]
        return "\n".join(lines)
    last = start
    for i in range(start + 1, end):
        if not lines[i].startswith(" "):
            break
        last = i
        match = re.match(rf"^(\s+){re.escape(child)}:", lines[i])
        if match:
            lines[i] = f"{match.group(1)}{child}: {quoted}"
            return "\n".join(lines)
    lines.insert(last + 1, f"  {child}: {quoted}")
    return "\n".join(lines)


def set_changelog(text, version, date):
    lines = text.split("\n")
    index, current, _ = first_changelog_heading(text)
    heading = f"## {version} ({date})"
    if index is not None and current == version:
        lines[index] = heading
        return "\n".join(lines)
    if index is None:
        # No entries yet: add one under the '# ' title, or at the very top.
        title = next((i for i, line in enumerate(lines) if line.startswith("# ")), None)
        index = title + 2 if title is not None else 0
        while len(lines) < index:
            lines.append("")
    lines[index:index] = [heading, "", f"- {PLACEHOLDER}", ""]
    return "\n".join(lines)


def updated_text(entry, version, date):
    """The file's text with the new version (and date) in place. Writes nothing."""
    text = (ROOT / entry["path"]).read_text(encoding="utf-8")
    kind = entry["format"]
    if kind == "json":
        return set_json(text, entry["field"], version)
    if kind == "frontmatter":
        text = set_frontmatter(text, entry["field"], version)
        if entry.get("date_field"):
            text = set_frontmatter(text, entry["date_field"], date)
        return text
    return set_changelog(text, version, date)


def as_tuple(version):
    return tuple(int(part) for part in version.split("."))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Change the Natural Voice version in every file at once.")
    parser.add_argument("version", help="the new version, for example 1.0.1")
    parser.add_argument("--date", default=datetime.date.today().isoformat(),
                        help="the release date as YYYY-MM-DD (default: today)")
    args = parser.parse_args(argv)

    if not SEMVER.fullmatch(args.version):
        print(f"'{args.version}' isn't a version number. Use three numbers, like 1.0.1.", file=sys.stderr)
        return 1
    if not DATE.fullmatch(args.date):
        print(f"'{args.date}' isn't a date. Use YYYY-MM-DD, like 2026-10-08.", file=sys.stderr)
        return 1

    try:
        entries = load_config()
        current = [read_entry(entry)[0] for entry in entries]
        known = [v for v in current if isinstance(v, str) and SEMVER.fullmatch(v)]
        highest = max(known, key=as_tuple) if known else None
        if highest and as_tuple(args.version) < as_tuple(highest):
            print(
                f"{args.version} is lower than the current version {highest}. "
                "Versions only go up, or people won't get the update.",
                file=sys.stderr,
            )
            return 1
        # Work out every change first, so a problem in one file leaves all of them untouched.
        changes = [(entry, updated_text(entry, args.version, args.date)) for entry in entries]
        for entry, text in changes:
            (ROOT / entry["path"]).write_text(text, encoding="utf-8")
            print(f"updated {entry['path']}")
    except VersionError as error:
        print("Nothing more was changed. Fix this first:\n- " + str(error), file=sys.stderr)
        return 1

    print(f"\nVersion is now {args.version} (released {args.date}) in {len(entries)} files.")
    changelog = (ROOT / "CHANGELOG.md")
    if changelog.is_file() and PLACEHOLDER in changelog.read_text(encoding="utf-8"):
        print(f"Next: open CHANGELOG.md and replace '{PLACEHOLDER}' with what changed.")
    print("Then run: python3 scripts/build.py && python3 scripts/validate.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
