"""Build the downloadable versions of Natural Voice.

Run from the repository root:  python3 scripts/build.py

Creates, in dist/:
  natural-voice-plugin.zip       the full plugin: .claude-plugin/plugin.json, the skill, the slash
                                 commands, the helper agents, the licence and the README, for
                                 Claude's "Upload plugin" screen (Customize > Plugins)
  natural-voice.zip              the skill folder (natural-voice/SKILL.md at the top, with its
                                 THIRD-PARTY-NOTICES.md) plus the licence, for apps that accept
                                 uploaded skills (Claude, ChatGPT, Manus, Mistral and others)
  natural-voice-flat.zip         the same files with SKILL.md at the top of the zip,
                                 for apps that want it there (Perplexity)
  natural-voice-instructions.md  the whole skill as one markdown file, for apps that only take
                                 instructions or knowledge files (Gems, GPTs, Projects, Spaces),
                                 ending with the licence line and the third-party notices
  natural-voice-starter.md       a short starter to paste into an app's instructions box;
                                 it points the app at the big file

It checks the source files first. If anything is wrong, it explains what and stops
without writing anything.

The zips are made the same way every time (fixed dates, sorted entries), so
scripts/validate.py can rebuild them in memory and check that dist/ is up to date.
Only the skill folder and the licence are packed: nothing from .claude/, research/,
tests/ or the plugin manifests goes into dist/.
"""
import io
import pathlib
import re
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "natural-voice"
REFS = SKILL / "references"
DIST = ROOT / "dist"
LICENSE = ROOT / "LICENSE"
README = ROOT / "README.md"
# Credits and licence notices for work the skill draws on. It lives inside the skill folder
# so every copy of the skill carries it: both zips, the single-file edition and installs
# that copy only skills/natural-voice/ (such as npx skills).
NOTICES_NAME = "THIRD-PARTY-NOTICES.md"
NOTICES = SKILL / NOTICES_NAME

SKILL_NAME = "natural-voice"
DESCRIPTION_LIMIT = 500  # characters in the SKILL.md description (the spec allows 1024)
STARTER_LIMIT = 6000     # characters in the starter; instruction boxes are small

PLUGIN_ZIP_NAME = "natural-voice-plugin.zip"
ZIP_NAME = "natural-voice.zip"
FLAT_ZIP_NAME = "natural-voice-flat.zip"
SINGLE_FILE_NAME = "natural-voice-instructions.md"
STARTER_NAME = "natural-voice-starter.md"
OUTPUT_NAMES = (PLUGIN_ZIP_NAME, ZIP_NAME, FLAT_ZIP_NAME, SINGLE_FILE_NAME, STARTER_NAME)
# Names used by earlier versions. The build removes them so nobody downloads a stale copy.
OLD_OUTPUT_NAMES = ("natural-voice-skill.zip", "natural-voice-skill-flat.zip")

# Every file inside the zips gets this date, so the same sources always give the same zip.
ZIP_DATE = (2026, 1, 1, 0, 0, 0)

# File names that belong to a person (their voice, notes and drafts). They must never ship.
PERSONAL_SUFFIXES = (".voice.md", ".voice.backup.md")
PERSONAL_NAMES = {"notes.md", "draft.md", "config.md"}
# The notes template has a personal-looking name but is part of the skill.
ALLOWED_PERSONAL_PATHS = {"references/templates/notes.md"}

# File names the skill mentions in backticks that are the person's own files, not skill files.
PERSON_FILE_NAMES = {"config.md", "draft.md"}

# Order of the sections in the single-file edition, after SKILL.md.
# Alphabetical within each group, except where FIRST_IN_GROUP says otherwise.
SECTION_ORDER = [
    "platforms.md",
    "jobs/",            # what to do: setup, write, polish, clean, calibrate, voices
    "roles/",
    "writing-rules.md",
    "editing/",
    "interview.md",
    "speech-to-writing.md",
    "model-tiers.md",
    "modes/",           # places the person writes for: LinkedIn, email, case study and so on
    "templates/",
    "glossaries/",
]
FIRST_IN_GROUP = {
    "editing/": ["editing/pattern-catalogue.md", "editing/text-integrity.md"],
}

BANNER = (
    "> **Using this file:** add it to your AI app as instructions or as a knowledge file "
    "(a Gemini Gem, a custom GPT, a Claude or ChatGPT Project, a Perplexity Space, or similar). "
    "This app probably can't save files, so follow the **Chat app** row of the table and the "
    "\"If you can't (chat apps)\" parts of `references/platforms.md` below. "
    "Wherever a file path like `references/...`, `jobs/x.md` (what to do), `modes/x.md` "
    "(places the person writes for), `roles/x.md`, `editing/x.md`, `templates/x.md`, "
    "`glossaries/x.md`, or a bare name like `setup.md` or `writing-rules.md` appears, "
    "it refers to the matching section further down this document.\n"
    ">\n"
    "> **Scripts:** the hidden-character and voice fingerprint checks are small Python scripts "
    "in the skill's `scripts/` folder. They are not in this file and only run in apps that can "
    "run code. Here, do those checks by careful reading instead, as a best effort, and tell the "
    "person that is what you did."
)

STARTER_OPENING = [
    "You are Natural Voice. The attached file `natural-voice-instructions.md` holds your full instructions.",
    "Before replying to any message, read its first section, then the \"Chat app\" row and the "
    "\"If you can't (chat apps)\" parts of `references/platforms.md`, then the section for the job "
    "the person wants (see the Jobs table below), and follow it exactly.",
]

CHAT_APP_MARKER = "**If you can't** (chat apps):"


class BuildError(Exception):
    pass


# ---------------------------------------------------------------- reading the sources

def is_personal(rel):
    """True for a person's own file (voice, notes, draft, config) inside the skill folder."""
    name = rel.name
    return name.endswith(PERSONAL_SUFFIXES) or (
        name in PERSONAL_NAMES and rel.as_posix() not in ALLOWED_PERSONAL_PATHS
    )


def ships(rel):
    """True for the kinds of file that belong in the skill folder."""
    parts = rel.parts
    if rel.as_posix() in ("SKILL.md", NOTICES_NAME, "agents/openai.yaml"):
        return True
    if parts[0] == "references" and rel.suffix == ".md":
        return True
    if parts[0] == "scripts" and len(parts) == 2 and rel.suffix == ".py":
        return True
    return False


def skill_files(quiet=False):
    """Every file that ships in the skill folder: SKILL.md, THIRD-PARTY-NOTICES.md,
    references/**/*.md, scripts/*.py and agents/openai.yaml. Hidden files, caches and
    personal files are skipped."""
    keep, unexpected = [], []
    for p in sorted(SKILL.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(SKILL)
        if any(part.startswith(".") or part == "__pycache__" for part in rel.parts):
            continue
        if p.suffix == ".pyc":
            continue
        if is_personal(rel):
            if not quiet:
                print(f"skipped {rel.as_posix()}: it looks like someone's personal file, so it is never shipped")
            continue
        if ships(rel):
            keep.append(p)
        else:
            unexpected.append(rel.as_posix())
    if unexpected:
        raise BuildError(
            "These files are in skills/natural-voice but aren't SKILL.md, THIRD-PARTY-NOTICES.md, "
            "references/**/*.md, scripts/*.py or agents/openai.yaml, so they can't ship. "
            "Move or remove them:\n    "
            + "\n    ".join(unexpected)
        )
    return keep


def markdown_files(files):
    """Only the instruction files: SKILL.md and the references. Used for the single-file
    edition, which adds the third-party notices separately at the end."""
    return [p for p in files if p.suffix == ".md" and p != NOTICES]


def read(path):
    return path.read_text(encoding="utf-8")


def strip_frontmatter(text):
    if text.startswith("---"):
        return text.split("---", 2)[2].lstrip()
    return text


def licence_holder():
    """The year and name from LICENSE line 3 ("Copyright (c) <year> <name>")."""
    lines = read(LICENSE).splitlines()
    match = re.match(r"Copyright \(c\) (\d{4}) (.+)", lines[2].strip()) if len(lines) >= 3 else None
    if not match:
        raise BuildError("LICENSE line 3 should read 'Copyright (c) <year> <name>'.")
    return match.group(1), match.group(2).strip()


# ---------------------------------------------------------------- frontmatter (a small, strict YAML subset)

KEY_LINE = re.compile(r"^([A-Za-z0-9_-]+):(?:\s+(.*))?$")
NESTED_LINE = re.compile(r"^( +)([A-Za-z0-9_-]+):(?:\s+(.*))?$")
LIST_LINE = re.compile(r"^( +)- (.*)$")
# A plain (unquoted) value can't start with these characters in YAML.
BAD_PLAIN_START = tuple("@`%&*!|>{}'\"")
NOT_A_STRING = re.compile(
    r"[-+]?(\d[\d_]*(\.\d*)?|\.\d+)([eE][-+]?\d+)?|true|false|yes|no|on|off|null|~",
    re.IGNORECASE,
)


class FrontmatterError(Exception):
    pass


def _scalar(raw, where):
    """Read one YAML value. Returns (value, plain) where plain means it wasn't quoted."""
    raw = raw.strip()
    if raw == "":
        return "", True
    if raw.startswith('"'):
        match = re.fullmatch(r'"((?:[^"\\]|\\.)*)"\s*(#.*)?', raw)
        if not match:
            raise FrontmatterError(f"{where}: the double quotes aren't closed properly.")
        value = match.group(1)
        value = re.sub(r'\\(["\\/])', r"\1", value).replace("\\n", "\n").replace("\\t", "\t")
        return value, False
    if raw.startswith("'"):
        match = re.fullmatch(r"'((?:[^']|'')*)'\s*(#.*)?", raw)
        if not match:
            raise FrontmatterError(f"{where}: the single quotes aren't closed properly.")
        return match.group(1).replace("''", "'"), False
    if raw.startswith("["):
        if not raw.rstrip().endswith("]"):
            raise FrontmatterError(f"{where}: a list that starts with '[' must end with ']'.")
        inner = raw.strip()[1:-1].strip()
        return ([] if not inner else [part.strip().strip("\"'") for part in inner.split(",")]), False
    if raw.startswith(BAD_PLAIN_START):
        raise FrontmatterError(
            f"{where}: the value starts with '{raw[0]}', which YAML doesn't allow without quotes. "
            "Wrap the whole value in double quotes."
        )
    if ": " in raw or raw.endswith(":"):
        raise FrontmatterError(
            f"{where}: the value contains ': ', which breaks YAML. Wrap the whole value in double quotes."
        )
    if " #" in raw:
        raw = raw.split(" #", 1)[0].rstrip()
    return raw, True


def parse_frontmatter(text, label="file"):
    """Parse the frontmatter at the top of a markdown file.

    Returns (data, plain_keys). data maps keys to strings, lists or one level of nested
    maps. plain_keys holds the dotted keys whose values were written without quotes.
    Raises FrontmatterError with a plain-English message when the syntax is wrong.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise FrontmatterError(f"{label}: there is no frontmatter. The file should start with a '---' line.")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        raise FrontmatterError(f"{label}: the frontmatter never ends. Add a closing '---' line.") from None
    body = lines[1:end]
    data, plain_keys = {}, set()
    i = 0
    while i < len(body):
        line = body[i]
        where = f"{label}, frontmatter line {i + 2}"
        if "\t" in line:
            raise FrontmatterError(f"{where}: uses a tab. Use spaces instead.")
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        match = KEY_LINE.match(line)
        if not match:
            raise FrontmatterError(f"{where}: expected 'key: value', found '{line.strip()}'.")
        key, raw = match.group(1), match.group(2) or ""
        if key in data:
            raise FrontmatterError(f"{where}: '{key}' appears twice.")
        i += 1
        if raw.strip() in ("|", ">", "|-", ">-", "|+", ">+"):
            block = []
            while i < len(body) and (body[i].startswith(" ") or not body[i].strip()):
                block.append(body[i].strip())
                i += 1
            joiner = "\n" if raw.strip().startswith("|") else " "
            data[key] = joiner.join(part for part in block if part).strip()
            continue
        if raw.strip() == "":
            nested, items = {}, []
            while i < len(body) and (body[i].startswith(" ") or not body[i].strip()):
                child = body[i]
                child_where = f"{label}, frontmatter line {i + 2}"
                i += 1
                if not child.strip() or child.lstrip().startswith("#"):
                    continue
                list_match = LIST_LINE.match(child)
                if list_match:
                    value, _ = _scalar(list_match.group(2), child_where)
                    items.append(value)
                    continue
                nested_match = NESTED_LINE.match(child)
                if not nested_match:
                    raise FrontmatterError(f"{child_where}: expected '  key: value', found '{child.strip()}'.")
                child_key = nested_match.group(2)
                value, plain = _scalar(nested_match.group(3) or "", child_where)
                nested[child_key] = value
                if plain:
                    plain_keys.add(f"{key}.{child_key}")
            if nested and items:
                raise FrontmatterError(f"{where}: '{key}' mixes a list and keys.")
            data[key] = items if items else nested
            continue
        value, plain = _scalar(raw, where)
        data[key] = value
        if plain:
            plain_keys.add(key)
    return data, plain_keys


def frontmatter_of(path):
    """parse_frontmatter for a file, with its path in any error message."""
    return parse_frontmatter(read(path), str(path.relative_to(ROOT)))


# ---------------------------------------------------------------- checks

def names_a_pattern_or_personal_file(target):
    """True for backticked names that aren't real files: the person's own files, or patterns."""
    name = target.rsplit("/", 1)[-1]
    return (
        target.startswith("~")              # a path on the person's computer
        or any(ch in target for ch in "<*")  # a pattern, such as roles/<role>.md or *.md
        or name.endswith(PERSONAL_SUFFIXES) # a voice file or its backup
        or name in PERSON_FILE_NAMES        # config.md, draft.md
    )


def reference_problems(paths):
    """Check every backticked .md path in these files points at a real file.

    Paths that mention references/ must exist in skills/natural-voice/references/. Short
    forms such as `jobs/setup.md` or a bare `setup.md` must match a reference file. Paths
    to other repository files (for example `research/sources.md`) must exist from the
    repository root.
    """
    ref_paths = {p.relative_to(REFS).as_posix() for p in REFS.rglob("*.md")}
    ref_names = {pathlib.PurePosixPath(r).name for r in ref_paths}
    ref_folders = {r.split("/", 1)[0] for r in ref_paths if "/" in r}
    root_names = {p.name for p in ROOT.glob("*.md")} | {"SKILL.md"}
    problems, seen = [], set()
    for path in paths:
        rel = path.relative_to(ROOT).as_posix()
        for match in re.finditer(r"`([^`\s]+\.md)`", read(path)):
            target = match.group(1)
            if (rel, target) in seen:
                continue  # report each missing file once per file that mentions it
            seen.add((rel, target))
            if names_a_pattern_or_personal_file(target) or "://" in target:
                continue
            clean = re.sub(r"^\$\{[A-Za-z_]+\}/", "", target)  # ${CLAUDE_PLUGIN_ROOT}/...
            if clean.startswith("./"):
                clean = clean[2:]
            if clean.startswith("$"):
                continue  # some other variable we can't resolve
            if "skills/natural-voice/" in clean:
                inside = clean.split("skills/natural-voice/", 1)[1]
                if (SKILL / inside).is_file():
                    continue
                problems.append(f"{rel} mentions `{target}`, but skills/natural-voice/{inside} doesn't exist.")
                continue
            if "references/" in clean:
                inside = clean.rsplit("references/", 1)[1]
                if inside in ref_paths:
                    continue
                problems.append(
                    f"{rel} mentions `{target}`, but there is no {inside} in skills/natural-voice/references/."
                )
                continue
            if "/" in clean:
                if clean.split("/", 1)[0] in ref_folders:
                    if clean in ref_paths:
                        continue
                    problems.append(
                        f"{rel} mentions `{target}`, but there is no {clean} in skills/natural-voice/references/."
                    )
                    continue
                if (ROOT / clean).is_file():
                    continue
                problems.append(f"{rel} mentions `{target}`, but there is no such file in the repository.")
                continue
            if clean in ref_names or clean in root_names:
                continue
            problems.append(f"{rel} mentions `{target}`, but there is no such file in skills/natural-voice/references/.")
    return problems


def frontmatter_problems(paths, need_description=True):
    """Frontmatter that won't parse, or has no description."""
    problems = []
    for path in paths:
        try:
            data, _ = frontmatter_of(path)
        except FrontmatterError as error:
            problems.append(str(error))
            continue
        if need_description and not data.get("description"):
            problems.append(f"{path.relative_to(ROOT)}: the frontmatter has no description.")
    return problems


def check_sources(files):
    problems = []
    main = SKILL / "SKILL.md"

    # 1. SKILL.md frontmatter parses, and the description fits the length apps accept.
    try:
        data, _ = frontmatter_of(main)
        description = data.get("description")
        if not description:
            problems.append("skills/natural-voice/SKILL.md has no description.")
        elif len(description) > DESCRIPTION_LIMIT:
            problems.append(
                f"The SKILL.md description is {len(description)} characters. "
                f"Keep it to {DESCRIPTION_LIMIT} or fewer."
            )
        if data.get("name") != SKILL_NAME:
            problems.append(f"The SKILL.md name should be '{SKILL_NAME}' to match its folder.")
    except FrontmatterError as error:
        problems.append(str(error))

    # 2. The README has no placeholder left in it.
    if README.is_file() and "<your-" in read(README):
        problems.append("README.md still has a '<your-...>' placeholder. Replace it with the real value.")

    # 3. Every backticked .md path in the skill points at a real file.
    problems += reference_problems(markdown_files(files))

    # 4. The helper agents' frontmatter is valid YAML.
    problems += frontmatter_problems(sorted((ROOT / "agents").glob("*.md")))

    # 5. LICENSE is there, and so are the third-party notices, with working paths.
    if not LICENSE.is_file():
        problems.append("LICENSE is missing from the repository root.")
    if NOTICES.is_file():
        problems += reference_problems([NOTICES])
    else:
        problems.append(f"skills/natural-voice/{NOTICES_NAME} is missing. It must ship with the skill, "
                        "because the skill reuses wording that needs its licence notice.")

    if problems:
        raise BuildError("\n".join("- " + problem for problem in problems))


# ---------------------------------------------------------------- building the outputs

def section_key(path):
    """Where a references/ file goes in the single-file edition."""
    rel = path.relative_to(REFS).as_posix()
    for i, entry in enumerate(SECTION_ORDER):
        if rel == entry or (entry.endswith("/") and rel.startswith(entry)):
            first = FIRST_IN_GROUP.get(entry, [])
            rank = first.index(rel) if rel in first else len(first)
            return (i, rank, rel)
    raise BuildError(
        f"references/{rel} has no place in SECTION_ORDER in scripts/build.py. Add it there."
    )


def release_line():
    """'Natural Voice <version>, released <date>.' from SKILL.md metadata."""
    data, _ = frontmatter_of(SKILL / "SKILL.md")
    meta = data.get("metadata") or {}
    version, released = meta.get("version"), meta.get("released")
    if not version or not released:
        raise BuildError("SKILL.md metadata needs both 'version' and 'released'.")
    return f"Natural Voice {version}, released {released}."


def single_file_text(files, year, holder):
    main = SKILL / "SKILL.md"
    parts = [
        "<!-- Natural Voice, single-file edition. Generated by scripts/build.py; edit the skill folder, not this file. -->",
        "",
        release_line(),
        "",
        BANNER,
        "",
        strip_frontmatter(read(main)),
    ]
    for p in sorted((f for f in markdown_files(files) if f != main), key=section_key):
        rel = p.relative_to(SKILL).as_posix()
        text = read(p)
        parts += ["", f"## File: `{rel}`", ""]
        if rel.startswith("references/templates/"):
            # Fence templates so their own headings and lines aren't read as instructions.
            if "````" in text:
                raise BuildError(f"{rel} contains a four-backtick fence, so it can't be wrapped safely.")
            parts += ["````markdown", text.rstrip("\n"), "````"]
        else:
            parts.append(text)
    parts += [
        "",
        f"Natural Voice is MIT licensed, copyright (c) {year} {holder}. "
        "Full licence text: the LICENSE file in the repository.",
        "",
        f"## File: `{NOTICES_NAME}`",
        "",
        read(NOTICES).rstrip("\n"),
        "",
    ]
    return "\n".join(parts)


def markdown_section(text, heading):
    """One '## ' section of a markdown text, heading included."""
    lines = text.splitlines()
    if heading not in lines:
        raise BuildError(f"Couldn't find the heading '{heading}' in SKILL.md.")
    start = lines.index(heading)
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return "\n".join(lines[start:end]).strip()


def chat_app_saving_bullets():
    """The bullets under "If you can't (chat apps)" in platforms.md."""
    lines = read(REFS / "platforms.md").splitlines()
    if CHAT_APP_MARKER not in lines:
        raise BuildError(f"Couldn't find '{CHAT_APP_MARKER}' in references/platforms.md.")
    bullets = []
    for line in lines[lines.index(CHAT_APP_MARKER) + 1:]:
        if line.startswith("- ") or (bullets and line.startswith("  ")):
            bullets.append(line)
        elif not line.strip() and not bullets:
            continue
        else:
            break
    if not bullets:
        raise BuildError("The chat-app saving bullets in references/platforms.md are empty.")
    return "\n".join(bullets)


def starter_text():
    skill_body = strip_frontmatter(read(SKILL / "SKILL.md"))
    text = "\n".join([
        *STARTER_OPENING,
        "",
        markdown_section(skill_body, "## Jobs"),
        "",
        markdown_section(skill_body, "## Always"),
        "",
        "## Saving in a chat app",
        "",
        chat_app_saving_bullets(),
        "",
    ])
    if len(text) >= STARTER_LIMIT:
        raise BuildError(
            f"The starter is {len(text):,} characters. It must stay under {STARTER_LIMIT:,} "
            "to fit instruction boxes. Shorten the Jobs or Always sections in SKILL.md, "
            "or the chat-app saving bullets in platforms.md."
        )
    return text


def zip_bytes(files, folder):
    """A zip of the skill files plus the licence, the same bytes every time for the same sources."""
    prefix = f"{folder}/" if folder else ""
    entries = [(prefix + p.relative_to(SKILL).as_posix(), p.read_bytes()) for p in files]
    entries.append((prefix + "LICENSE", LICENSE.read_bytes()))
    return deterministic_zip(entries)


def plugin_zip_bytes(files):
    """The full Claude plugin: manifest, skill, commands, helper agents, licence and README."""
    manifest = ROOT / ".claude-plugin" / "plugin.json"
    if not manifest.is_file():
        raise BuildError(".claude-plugin/plugin.json is missing, so the plugin zip can't be built.")
    entries = [(".claude-plugin/plugin.json", manifest.read_bytes())]
    entries += [(p.relative_to(ROOT).as_posix(), p.read_bytes()) for p in files]
    for folder in ("commands", "agents"):
        found = sorted((ROOT / folder).glob("*.md"))
        if not found:
            raise BuildError(f"{folder}/ has no .md files, so the plugin zip would be incomplete.")
        entries += [(p.relative_to(ROOT).as_posix(), p.read_bytes()) for p in found]
    entries += [("LICENSE", LICENSE.read_bytes()), ("README.md", README.read_bytes())]
    return deterministic_zip(entries)


def deterministic_zip(entries):
    """Zip (name, bytes) entries with fixed dates and sorted order."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as z:
        for name, data in sorted(entries):
            info = zipfile.ZipInfo(name, date_time=ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3                 # Unix, so the permissions below are read
            info.external_attr = 0o100644 << 16    # an ordinary readable file
            z.writestr(info, data, compresslevel=9)
    return buffer.getvalue()


def build_outputs(quiet=False):
    """Check the sources and return every dist/ file as {name: bytes}. Writes nothing."""
    files = skill_files(quiet=quiet)
    check_sources(files)
    year, holder = licence_holder()
    return {
        PLUGIN_ZIP_NAME: plugin_zip_bytes(files),
        ZIP_NAME: zip_bytes(files, SKILL_NAME),
        FLAT_ZIP_NAME: zip_bytes(files, ""),
        SINGLE_FILE_NAME: single_file_text(files, year, holder).encode("utf-8"),
        STARTER_NAME: starter_text().encode("utf-8"),
    }


def main():
    try:
        outputs = build_outputs()
    except BuildError as error:
        print("Build stopped. Nothing was written. Fix this first:\n" + str(error), file=sys.stderr)
        sys.exit(1)

    DIST.mkdir(exist_ok=True)
    for old in OLD_OUTPUT_NAMES:
        if (DIST / old).exists():
            (DIST / old).unlink()
            print(f"removed dist/{old}: that name is no longer used")
    for name, data in outputs.items():
        out = DIST / name
        out.write_bytes(data)
        print(f"built {out.relative_to(ROOT)} ({max(1, len(data) // 1024)} KB)")
    print(f"starter: {len(outputs[STARTER_NAME].decode('utf-8')):,} characters (limit {STARTER_LIMIT:,})")


if __name__ == "__main__":
    main()
