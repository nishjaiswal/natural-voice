"""Tests for the maintainer scripts scripts/validate.py and scripts/build.py.

They check the privacy rules (email addresses and personal file names) and that the
third-party notices ship inside every downloadable copy of the skill.

Run from the repository root:  python3 -m unittest discover -s tests/scripts -v
"""

import io
from pathlib import Path, PurePosixPath
import sys
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True   # keep scripts/ free of __pycache__
sys.path.insert(0, str(ROOT / "scripts"))

import build  # noqa: E402
import validate  # noqa: E402


class EmailAddresses(unittest.TestCase):
    def test_example_domains_and_their_subdomains_are_allowed(self):
        for domain in ("example.com", "mail.example.com", "example.org", "example.net",
                       "users.noreply.github.com", "test.example"):
            with self.subTest(domain=domain):
                self.assertTrue(validate.allowed_email_domain(domain))

    def test_lookalike_domains_are_not_allowed(self):
        for domain in ("notexample.com", "myexample.org", "example.com.evil.net", "gmail.com",
                       "fakeusers.noreply.github.com"):
            with self.subTest(domain=domain):
                self.assertFalse(validate.allowed_email_domain(domain))

    def test_a_real_looking_address_is_reported_and_masked(self):
        lookalike = "name" + "@" + "notexample.com"     # built here so the repository check doesn't flag this file
        problems = validate.email_problems("notes.txt", f"Write to jo@example.com\nor {lookalike}.")
        self.assertEqual(len(problems), 1)
        self.assertIn("line 2", problems[0])
        self.assertIn("n***@notexample.com", problems[0])
        self.assertNotIn("name@", problems[0])


class PersonalFiles(unittest.TestCase):
    def test_personal_file_names_and_folders_are_flagged(self):
        for name in ("notes.md", "draft.md", "config.md", "docs/draft.md", "skills/natural-voice/notes.md",
                     "skills/natural-voice/references/config.md", "kit.voice.md", "old.voice.backup.md",
                     "tests/me.voice.md", "samples/email.txt", "research/samples/a.md",
                     "skills/natural-voice/voices/me.md", "drafts/post.md", "Voices/x.txt"):
            with self.subTest(name=name):
                self.assertIsNotNone(validate.personal_file_problem(name))

    def test_templates_examples_and_test_fixtures_are_allowed(self):
        for name in ("skills/natural-voice/references/templates/notes.md",
                     "skills/natural-voice/references/templates/draft.md",
                     "examples/kit.voice.md", "examples/notes.md", "examples/samples/a.md",
                     "tests/fixtures/voice/sample-notes.md", "tests/fixtures/drafts/a.md",
                     "commands/setup.md", "my-samples.md", "research/sources.md"):
            with self.subTest(name=name):
                self.assertIsNone(validate.personal_file_problem(name))


class ThirdPartyNotices(unittest.TestCase):
    """The notices ship inside the skill folder, so every copy of the skill carries them."""

    @classmethod
    def setUpClass(cls):
        cls.notices = (build.SKILL / "THIRD-PARTY-NOTICES.md").read_bytes()
        cls.outputs = build.build_outputs(quiet=True)

    def test_the_notices_file_is_a_skill_file(self):
        self.assertTrue(build.ships(PurePosixPath("THIRD-PARTY-NOTICES.md")))
        self.assertIn(build.NOTICES, build.skill_files(quiet=True))

    def test_both_zips_carry_the_notices(self):
        for zip_name, member in ((build.ZIP_NAME, "natural-voice/THIRD-PARTY-NOTICES.md"),
                                 (build.FLAT_ZIP_NAME, "THIRD-PARTY-NOTICES.md")):
            with self.subTest(zip=zip_name):
                with zipfile.ZipFile(io.BytesIO(self.outputs[zip_name])) as archive:
                    self.assertEqual(archive.read(member), self.notices)

    def test_the_single_file_edition_ends_with_the_notices(self):
        text = self.outputs[build.SINGLE_FILE_NAME].decode("utf-8")
        licence = text.index("Natural Voice is MIT licensed, copyright (c)")
        notices = text.index("## File: `THIRD-PARTY-NOTICES.md`")
        self.assertLess(licence, notices)
        self.assertTrue(text.rstrip("\n").endswith(self.notices.decode("utf-8").rstrip("\n")))
        self.assertIn("Copyright (c) 2025 Siqi Chen", text[notices:])

    def test_the_wording_says_what_was_reused(self):
        text = self.notices.decode("utf-8")
        self.assertIn("about ten of its pattern headings, reused word for word", text)
        self.assertIn('"Re-explaining what the reader knows"', text)
        self.assertNotIn("a few short group and pattern names", text)

    def test_the_root_file_points_to_the_skill_copy(self):
        root = (ROOT / "THIRD-PARTY-NOTICES.md").read_text(encoding="utf-8")
        self.assertIn("(skills/natural-voice/THIRD-PARTY-NOTICES.md)", root)


if __name__ == "__main__":
    unittest.main()
