#!/usr/bin/env python3
"""Measure someone's writing habits, and compare a draft with them.

Usage:
  python3 scripts/voice_stats.py profile FILE [FILE ...] [--json | --markdown]
  python3 scripts/voice_stats.py compare DRAFT --voice-file VOICE.md [--json]
  python3 scripts/voice_stats.py compare DRAFT --fingerprint FILE.json [--json]

profile  measures writing samples (plain text or Markdown) and prints a Fingerprint:
         sentence length, punctuation, contractions, I or we, favourite sentence
         starters, spelling and more. --markdown prints a block ready to paste into a
         voice file; --json prints the numbers only.
compare  measures a draft and lists the biggest differences from the Fingerprint, in
         plain English, plus a distance score for everyday small words.

Offline, Python standard library only, and the same input always gives the same output.
These are rough style measures. They describe habits, not quality, and they say nothing
about who wrote a text. Use only the person's own unassisted writing as samples.
FILE or DRAFT can be "-" to read standard input. Exit codes: 0 done, 2 problem.
"""

import argparse
from collections import Counter
import html
import json
import math
from pathlib import Path
import re
import sys


VERSION = "1.0.0"
FORMAT_NAME = "natural-voice-fingerprint"
FORMAT_VERSION = 1
MARKER = "<!-- natural-voice:fingerprint -->"
MAX_BYTES = 5 * 1024 * 1024
MAX_FINGERPRINT_JSON = 200_000
MIN_COMPARE_WORDS = 150
CHUNK_WORDS = 250
MAX_DIFFERENCES = 8
SHOW_THRESHOLD = 3.0       # differences need a "surprise" of at least this to be shown
EXIT_OK, EXIT_USAGE = 0, 2

SAMPLE_NOTE = ("Samples should be the person's own unassisted writing. These are rough "
               "measures of habit, not of quality.")

# About fifty common English function words (Burrows-style), used for the distance score.
FUNCTION_WORDS = (
    "the", "and", "of", "to", "a", "in", "i", "it", "that", "is",
    "was", "for", "on", "with", "as", "but", "this", "be", "at", "by",
    "not", "are", "from", "or", "have", "an", "we", "you", "they", "which",
    "so", "if", "all", "there", "would", "their", "my", "our", "can", "about",
    "what", "when", "more", "just", "been", "one", "will", "has", "into", "than",
)
FUNCTION_SET = frozenset(FUNCTION_WORDS)

# Words: abbreviations like "e.g.", numbers like "3.5" or "1,000", or letter runs joined
# by apostrophes or hyphens ("don't", "well-known").
WORD_RE = re.compile(r"(?:[A-Za-z]\.){2,}|\d+(?:[.,]\d+)+|[^\W_]+(?:[-'’][^\W_]+)*")

TITLES = frozenset("mr mrs ms dr prof sr jr st mt rev hon gen col capt lt sgt".split())
NO_SPLIT = frozenset("e.g i.e eg ie cf vs viz approx ca al".split())
BEFORE_NUMBER = frozenset("no nos vol vols p pp fig figs ch sec art para".split())

CONTRACTION_PAIRS = (
    ("do not", "don't"), ("does not", "doesn't"), ("did not", "didn't"), ("is not", "isn't"),
    ("are not", "aren't"), ("was not", "wasn't"), ("were not", "weren't"), ("has not", "hasn't"),
    ("have not", "haven't"), ("had not", "hadn't"), ("will not", "won't"), ("would not", "wouldn't"),
    ("could not", "couldn't"), ("should not", "shouldn't"), ("cannot", "can't"), ("can not", "can't"),
    ("i am", "i'm"), ("i will", "i'll"), ("i would", "i'd"), ("we are", "we're"),
    ("you are", "you're"), ("they are", "they're"), ("we will", "we'll"), ("you will", "you'll"),
    ("they will", "they'll"), ("it is", "it's"), ("that is", "that's"), ("there is", "there's"),
    ("what is", "what's"),
)
EXPANDED_BIGRAMS = frozenset(tuple(e.split()) for e, _ in CONTRACTION_PAIRS if " " in e)
CONTRACTED_FORMS = frozenset(c for _, c in CONTRACTION_PAIRS)
S_CONTRACTION_HEADS = frozenset("it that there here what who where he she let how when why".split())

FIRST_SINGULAR = frozenset("i me my mine myself i'm i've i'll i'd".split())
FIRST_PLURAL = frozenset("we us our ours ourselves we're we've we'll we'd let's".split())
HEDGE_WORDS = frozenset("perhaps maybe might probably arguably possibly".split())
HEDGE_BIGRAMS = frozenset({("i", "think"), ("sort", "of"), ("kind", "of"), ("i", "guess"), ("i", "suppose")})
INTENSIFIERS = frozenset("really very incredibly truly genuinely quite".split())
SO_NOT_INTENSIFYING = frozenset((
    "i we you they he she it that the a an this these those there far on to as called what "
    "if when then now let do did does is was are were will would can could should my our "
    "your their his her its i'm it's we're you're they're that's there's"
).split())
ING_STOP = frozenset("during nothing something anything everything morning evening string spring "
                     "bring ceiling darling sibling pudding wedding".split())
NOMINAL_RE = re.compile(r"^[a-z]{3,}(?:tion|sion|ment|ness)(?:s|es)?$")
NOMINAL_STOP = frozenset("business witness harness wilderness moment moments comment comments element "
                         "elements segment segments fragment fragments garment cement nation nations "
                         "station stations".split())

# Spelling signals. British and American forms are counted separately; the person's own
# mix is what matters, so nothing here is "right".
OUR_STEMS = ("colo", "favo", "behavio", "hono", "labo", "neighbo", "humo", "flavo", "harbo", "rumo",
             "savo", "endeavo", "vapo", "armo", "odo", "rigo", "vigo", "parlo", "cando", "clamo", "splendo")
OUR_SUFFIX = r"(?:s|ed|ing|ful|fully|ite|ites|able|ably|less|er|ers|y|hood|hoods)?"
OUR_BRITISH = re.compile(r"\b(?:" + "|".join(OUR_STEMS) + r")ur" + OUR_SUFFIX + r"\b")
OUR_AMERICAN = re.compile(r"\b(?:" + "|".join(OUR_STEMS) + r")r" + OUR_SUFFIX + r"\b")
RE_STEMS = ("cent", "theat", "fib", "calib", "somb", "spect", "lust", "meag", "sab", "lit")
RE_BRITISH = re.compile(r"\b(?:" + "|".join(RE_STEMS) + r")re(?:s|d)?\b")
RE_AMERICAN = re.compile(r"\b(?:" + "|".join(RE_STEMS) + r")er(?:s|ed)?\b")
OTHER_BRITISH = frozenset((
    "travelled travelling traveller travellers cancelled cancelling labelled labelling modelled "
    "modelling fuelled fuelling levelled signalled grey greys whilst amongst defence offence pretence "
    "catalogue catalogues jewellery aluminium sceptical sceptic programme programmes cheque cheques "
    "tyre tyres"
).split())
OTHER_AMERICAN = frozenset((
    "traveled traveling traveler travelers canceled canceling labeled labeling modeled modeling "
    "fueled fueling leveled signaled gray grays defense offense pretense catalog catalogs jewelry "
    "aluminum skeptical skeptic"
).split())
ISE_RE = re.compile(r"\b([a-z]{3,})is(?:e|es|ed|ing|ation|ations|er|ers)\b")
IZE_RE = re.compile(r"\b([a-z]{3,})iz(?:e|es|ed|ing|ation|ations|er|ers)\b")
YSE_RE = re.compile(r"\b(?:anal|paral|catal|dial)ys(?:e|ed|ing)\b")
YZE_RE = re.compile(r"\b(?:anal|paral|catal|dial)yz(?:e|es|ed|ing)\b")
ISE_ALWAYS = frozenset((
    "advise arise chastise circumcise comprise compromise concise demise despise devise disguise "
    "enterprise excise exercise expertise franchise improvise incise merchandise otherwise likewise "
    "clockwise precise imprecise premise promise revise supervise surmise surprise televise treatise "
    "praise braise cruise bruise paradise porpoise tortoise anise mortise valise apprise reprise "
    "advertise appraise sunrise moonrise unwise streetwise edgewise lengthwise noise poise raise "
    "guise wise rise"
).split())
IZE_ALWAYS = frozenset("seize prize capsize maize baize assize resize downsize upsize oversize outsize".split())


class UsageError(Exception):
    """A problem with the command or its input (exit code 2)."""


# ---------------------------------------------------------------- reading and preparing text

def read_source(path):
    if path == "-":
        if sys.stdin is None or sys.stdin.isatty():
            raise UsageError("No text given. Give a file path, or pipe text in.")
        data = sys.stdin.buffer.read(MAX_BYTES + 1)
        name = "standard input"
    else:
        source = Path(path)
        if not source.is_file():
            raise UsageError(f"Can't find a file at {path}.")
        with open(source, "rb") as handle:
            data = handle.read(MAX_BYTES + 1)
        name = str(path)
    if len(data) > MAX_BYTES:
        raise UsageError(f"{name} is larger than {MAX_BYTES // (1024 * 1024)} MB; use a shorter sample.")
    return name, data.decode("utf-8", errors="replace").lstrip("﻿")


FENCE_RE = re.compile(r"^(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^#{1,6}(?:\s|$)")
RULE_RE = re.compile(r"^(?:[-*_]\s*){3,}$")
SETEXT_RE = re.compile(r"^(?:=+|-+)$")
REFDEF_RE = re.compile(r"^\[\^?[^\]]{1,200}\]:")
LIST_RE = re.compile(r"^(?:[-*+]|\d{1,3}[.)])\s+")
# Every pattern is bounded, and none can start over inside its own match, so a long run
# of odd characters can't make them slow.
INLINE_PATTERNS = (
    (re.compile(r"!\[[^\[\]\n]{0,300}\]\([^)\n]{0,2000}\)"), ""),        # images
    (re.compile(r"\[([^\[\]\n]{0,300})\]\([^)\n]{0,2000}\)"), r"\1"),    # links: keep the words
    (re.compile(r"\[([^\[\]\n]{1,300})\]\[[^\[\]\n]{0,300}\]"), r"\1"),  # reference links
    (re.compile(r"\[\^[^\[\]\n]{1,100}\]"), ""),                         # footnote references
    (re.compile(r"<https?://[^>\s]{1,2000}>"), ""),                      # autolinks
    (re.compile(r"\b(?:https?://|www\.)\S+", re.IGNORECASE), ""),        # bare links
    (re.compile(r"(?<![\w.+-])[\w.+-]{1,64}@[\w-]{1,63}(?:\.[\w-]{1,63}){1,10}\b"), ""),  # email addresses
    (re.compile(r"`[^`\n]{0,500}`"), ""),                                # inline code
    (re.compile(r"<!--.{0,2000}?-->"), ""),                              # comments on one line
    (re.compile(r"</?[A-Za-z][^<>\n]{0,300}>"), ""),                     # HTML tags
    (re.compile(r"\*\*|__|~~"), ""),                                     # bold, strikethrough
    (re.compile(r"(?<!\w)\*(?=\S)|(?<=\S)\*(?!\w)"), ""),                # *italic*
    (re.compile(r"(?<![\w_])_(?=\S)|(?<=\S)_(?![\w_])"), ""),            # _italic_
)


def strip_html_comments(text):
    out, pos = [], 0
    while True:
        start = text.find("<!--", pos)
        if start < 0:
            out.append(text[pos:])
            return "".join(out)
        end = text.find("-->", start + 4)
        out.append(text[pos:start])
        if end < 0:
            return "".join(out)
        pos = end + 3


def clean_inline(text):
    for pattern, replacement in INLINE_PATTERNS:
        text = pattern.sub(replacement, text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def extract_paragraphs(raw):
    """Return [(paragraph text, is_list_item)]: prose only, Markdown syntax removed.

    Leaves out front matter, fenced code, headings, block quotes, tables, rules, link
    definitions, links' addresses, images, inline code and HTML.
    """
    text = raw.replace("\r\n", "\n").replace("\r", "\n")
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if 0 < end < 20000:
            text = text[text.find("\n", end + 4) + 1:] if text.find("\n", end + 4) >= 0 else ""
    text = strip_html_comments(text)
    paragraphs, current, current_is_item, fence = [], [], False, None

    def flush():
        nonlocal current, current_is_item
        if current:
            joined = clean_inline(" ".join(current))
            if joined:
                paragraphs.append((joined, current_is_item))
        current, current_is_item = [], False

    for line in text.split("\n"):
        stripped = line.strip()
        if fence:
            if stripped and set(stripped) == {fence[0]} and len(stripped) >= len(fence):
                fence = None
            continue
        opening = FENCE_RE.match(stripped)
        if opening:
            flush()
            fence = opening.group(1)
            continue
        if not stripped or RULE_RE.match(stripped) and not current:
            flush()
            continue
        if SETEXT_RE.match(stripped) and current:
            current, current_is_item = [], False     # the lines above were a heading
            continue
        if stripped.startswith(">") or HEADING_RE.match(stripped) or stripped.startswith("|"):
            flush()
            continue
        if RULE_RE.match(stripped):
            flush()
            continue
        if REFDEF_RE.match(stripped):
            continue
        item = LIST_RE.match(stripped)
        if item:
            flush()
            current, current_is_item = [stripped[item.end():]], True
            continue
        current.append(stripped)
    flush()
    return paragraphs


# ---------------------------------------------------------------- sentences and words

CLOSERS = "\"'”’)]»"
OPENERS = "\"'“‘([«"
TERMINALS = ".!?…"


def starts_sentence(token):
    core = token.lstrip(OPENERS)
    return bool(core) and (core[0].isupper() or core[0].isdigit())


def split_sentences(paragraph):
    """Split on . ! ? and … when the next word looks like a new sentence.

    Titles (Dr., Mrs.), e.g., i.e., initials (J. K.) and "No. 5" do not end a sentence.
    """
    tokens = paragraph.split()
    sentences, current = [], []
    for i, token in enumerate(tokens):
        current.append(token)
        # The token ends a sentence if, after any closing quotes or brackets, its last
        # character is . ! ? or …. (Checked by hand: a regular expression here was slow on
        # long runs of dots.)
        core = token.rstrip(CLOSERS)
        if not core or core[-1] not in TERMINALS or i + 1 >= len(tokens):
            continue
        following = tokens[i + 1]
        if core.endswith(".") and not core.endswith(".."):
            word = core[:-1].lstrip(OPENERS).lower()
            if word in TITLES or word in NO_SPLIT or re.fullmatch(r"(?:[a-z]\.)+[a-z]", word):
                continue
            if len(word) == 1 and word.isalpha():
                continue
            if word in BEFORE_NUMBER and following[:1].isdigit():
                continue
        if starts_sentence(following):
            sentences.append(" ".join(current))
            current = []
    if current:
        sentences.append(" ".join(current))
    return sentences


def words_of(text):
    return WORD_RE.findall(text)


def normal(token):
    return token.lower().replace("’", "'")


def is_contraction(low):
    if "'" not in low:
        return False
    if low.endswith("n't"):
        return True
    head, _, tail = low.rpartition("'")
    return tail in ("re", "ve", "ll", "d", "m") or (tail == "s" and head in S_CONTRACTION_HEADS)


def so_intensifiers(sentence):
    count = 0
    for match in re.finditer(r"(?<=[A-Za-z'’\"”])\s+so\s+([A-Za-z'’]+)", sentence):
        if normal(match.group(1)) not in SO_NOT_INTENSIFYING:
            count += 1
    return count


# ---------------------------------------------------------------- measuring

def spelling_signals(prose):
    lower_words = [w for w in re.findall(r"[A-Za-z]+", prose)]
    lowered = [w.lower() for w in lower_words]
    found = {"our_british": [], "our_american": [], "re_british": [], "re_american": [],
             "other_british": [], "other_american": [], "ise": [], "ize": []}
    text = " ".join(lowered)
    found["our_british"] = OUR_BRITISH.findall(text)
    found["our_american"] = OUR_AMERICAN.findall(text)
    found["re_british"] = RE_BRITISH.findall(text)
    found["re_american"] = RE_AMERICAN.findall(text)
    found["other_british"] = [w for w in lowered if w in OTHER_BRITISH]
    found["other_american"] = [w for w in lowered if w in OTHER_AMERICAN]
    # -ise/-ize: lower-case words only, so names such as Louise are not counted.
    original = " ".join(w for w in lower_words if w[:1].islower())
    for match in ISE_RE.finditer(original):
        if match.group(1) + "ise" not in ISE_ALWAYS:
            found["ise"].append(match.group())
    found["ise"].extend(YSE_RE.findall(original))
    for match in IZE_RE.finditer(original):
        if match.group(1) + "ize" not in IZE_ALWAYS:
            found["ize"].append(match.group())
    found["ize"].extend(YZE_RE.findall(original))
    return found


def spelling_lean(counts):
    british = counts["our_british"] + counts["re_british"] + counts["other_british"]
    american = counts["our_american"] + counts["re_american"] + counts["other_american"]
    if british + american == 0:
        return "unclear"
    if american == 0:
        return "British"
    if british == 0:
        return "American"
    if british >= 3 * american:
        return "mostly British"
    if american >= 3 * british:
        return "mostly American"
    return "mixed"


def measure(paragraphs):
    """Raw counts for a body of prose."""
    sentence_lengths, paragraph_sizes = [], []
    sentence_tokens, openers = [], Counter()
    ing_starts = so_count = 0
    for text, is_item in paragraphs:
        in_paragraph = 0
        for sentence in split_sentences(text):
            tokens = words_of(sentence)
            if not tokens:
                continue
            in_paragraph += 1
            sentence_lengths.append(len(tokens))
            sentence_tokens.append(tokens)
            first = normal(tokens[0])
            openers[first] += 1
            if len(first) >= 5 and first.endswith("ing") and first not in ING_STOP:
                ing_starts += 1
            so_count += so_intensifiers(sentence)
        if in_paragraph and not is_item:
            paragraph_sizes.append(in_paragraph)
    prose = "\n".join(text for text, _ in paragraphs)
    tokens = [t for sentence in sentence_tokens for t in sentence]
    lowered = [normal(t) for t in tokens]

    contracted = expanded = 0
    hedges = intensifiers = 0
    for sentence in sentence_tokens:
        low = [normal(t) for t in sentence]
        for i, word in enumerate(low):
            following = low[i + 1] if i + 1 < len(low) else None
            if word in CONTRACTED_FORMS:
                contracted += 1
            elif word == "cannot" or (following and (word, following) in EXPANDED_BIGRAMS):
                expanded += 1
            if word in HEDGE_WORDS or (following and (word, following) in HEDGE_BIGRAMS):
                hedges += 1
            if word in INTENSIFIERS:
                intensifiers += 1
    singular = sum(1 for low in lowered if low in FIRST_SINGULAR)
    plural = sum(1 for tok, low in zip(tokens, lowered) if low in FIRST_PLURAL and tok != "US")
    nominal = sum(1 for low in lowered if NOMINAL_RE.match(low) and low not in NOMINAL_STOP)

    function_stream = [low.split("'")[0] for low in lowered]
    function_counts = Counter(w for w in function_stream if w in FUNCTION_SET)
    chunk_rates = []
    for start in range(0, len(function_stream) - CHUNK_WORDS + 1, CHUNK_WORDS):
        chunk = Counter(w for w in function_stream[start:start + CHUNK_WORDS] if w in FUNCTION_SET)
        chunk_rates.append({w: chunk[w] * 1000 / CHUNK_WORDS for w in FUNCTION_WORDS})

    punctuation = {
        "commas": prose.count(","),
        "semicolons": prose.count(";"),
        "colons": len(re.findall(r"(?<!\d):|(?<=\d):(?!\d)", prose)),
        "em_dashes": prose.count("—"),
        "en_dashes": len(re.findall(r"(?<!\d)–|(?<=\d)–(?!\d)", prose)),
        "hyphen_dashes": len(re.findall(r"(?<=\w) -{1,2} (?=\w)|(?<=\w)--(?=\w)", prose)),
        "parentheses": prose.count("("),
        "exclamation_marks": len(re.findall(r"!+", prose)),
        "question_marks": len(re.findall(r"\?+", prose)),
        "ellipses": prose.count("…") + len(re.findall(r"\.{3,}", prose)),
        "quotation_marks": sum(prose.count(c) for c in "\"“”"),
    }
    spelling = spelling_signals(prose)
    return {
        "words": len(tokens), "sentence_lengths": sentence_lengths, "paragraph_sizes": paragraph_sizes,
        "openers": openers, "punctuation": punctuation,
        "curly": sum(prose.count(c) for c in "‘’“”"),
        "straight": prose.count("'") + prose.count('"'),
        "contraction_tokens": sum(1 for low in lowered if is_contraction(low)),
        "contracted": contracted, "expanded": expanded,
        "singular": singular, "plural": plural, "hedges": hedges,
        "intensifiers": intensifiers + so_count, "ing_starts": ing_starts, "nominalisations": nominal,
        "function_counts": function_counts, "chunk_rates": chunk_rates,
        "spelling": spelling,
    }


def percentile(sorted_values, q):
    if not sorted_values:
        return None
    position = (len(sorted_values) - 1) * q
    low, high = math.floor(position), math.ceil(position)
    return sorted_values[low] + (sorted_values[high] - sorted_values[low]) * (position - low)


def mean(values):
    return sum(values) / len(values) if values else None


def sd(values):
    if len(values) < 2:
        return None
    centre = mean(values)
    return math.sqrt(sum((v - centre) ** 2 for v in values) / (len(values) - 1))


def r(value, places=2):
    return None if value is None else round(value, places)


def share(part, whole, places=3):
    return round(part / whole, places) if whole else None


def confidence(words):
    if words < 300:
        return "low"
    return "medium" if words <= 1500 else "high"


def fingerprint_from(measures, samples):
    """The Fingerprint: everything compare needs, as plain numbers."""
    words = measures["words"]
    lengths = sorted(measures["sentence_lengths"])
    sizes = measures["paragraph_sizes"]
    per1000 = (lambda count: round(count * 1000 / words, 2)) if words else (lambda count: None)
    p = measures["punctuation"]
    sentences = len(lengths)
    top = sorted(measures["openers"].items(), key=lambda kv: (-kv[1], kv[0]))[:8]
    spelling = {key: len(found) for key, found in measures["spelling"].items()}
    spelling["lean"] = spelling_lean(spelling)
    chunks = measures["chunk_rates"]
    return {
        "format": FORMAT_NAME,
        "version": FORMAT_VERSION,
        "words": words,
        "samples": samples,
        "confidence": confidence(words),
        "note": SAMPLE_NOTE,
        "sentences": {
            "count": sentences,
            "mean": r(mean(lengths), 1), "median": r(percentile(lengths, 0.5), 1),
            "p10": r(percentile(lengths, 0.1), 1), "p90": r(percentile(lengths, 0.9), 1),
            "sd": r(sd(lengths), 1),
            "under_8_share": share(sum(1 for n in lengths if n < 8), sentences),
            "over_25_share": share(sum(1 for n in lengths if n > 25), sentences),
        },
        "paragraphs": {
            "count": len(sizes), "sentences_mean": r(mean(sizes), 2), "sentences_sd": r(sd(sizes), 2),
            "single_sentence_share": share(sum(1 for n in sizes if n == 1), len(sizes)),
        },
        "per_1000_words": {
            "commas": per1000(p["commas"]), "semicolons": per1000(p["semicolons"]),
            "colons": per1000(p["colons"]), "em_dashes": per1000(p["em_dashes"]),
            "en_dashes": per1000(p["en_dashes"]), "hyphen_dashes": per1000(p["hyphen_dashes"]),
            "parentheses": per1000(p["parentheses"]),
            "exclamation_marks": per1000(p["exclamation_marks"]),
            "question_marks": per1000(p["question_marks"]), "ellipses": per1000(p["ellipses"]),
            "quotation_marks": per1000(p["quotation_marks"]),
            "contractions": per1000(measures["contraction_tokens"]),
            "first_person_singular": per1000(measures["singular"]),
            "first_person_plural": per1000(measures["plural"]),
            "hedges": per1000(measures["hedges"]), "intensifiers": per1000(measures["intensifiers"]),
            "ing_starts_rough": per1000(measures["ing_starts"]),
            "nominalisations_rough": per1000(measures["nominalisations"]),
        },
        "contractions": {
            "contracted": measures["contracted"], "expanded": measures["expanded"],
            "share_contracted": share(measures["contracted"], measures["contracted"] + measures["expanded"])
            if measures["contracted"] + measures["expanded"] >= 3 else None,
        },
        "quote_style": {
            "curly": measures["curly"], "straight": measures["straight"],
            "curly_share": share(measures["curly"], measures["curly"] + measures["straight"])
            if measures["curly"] + measures["straight"] >= 5 else None,
        },
        "openers": {word[:MAX_WORD_LENGTH]: share(count, sentences) for word, count in top},
        "spelling": spelling,
        "function_word_chunks": {"size": CHUNK_WORDS, "count": len(chunks)},
        "function_word_rates": {w: per1000(measures["function_counts"][w]) for w in FUNCTION_WORDS},
        "function_word_sd": ({w: r(sd([c[w] for c in chunks]), 2) for w in FUNCTION_WORDS}
                             if len(chunks) >= 2 else None),
    }


# ---------------------------------------------------------------- plain-English wording

def fmt(value):
    if value is None:
        return "n/a"
    if value == 0:
        return "0"
    if value >= 10:
        return f"{round(value):,}"
    text = f"{value:.1f}"
    return text[:-2] if text.endswith(".0") else text


def pct(value):
    return "n/a" if value is None else f"{round(value * 100)}%"


def display_word(word, limit=40):
    """A sentence starter for the report: capitalised, at most `limit` characters, and with
    anything unprintable written as an escape, so a word can't carry hidden characters."""
    word = "".join(ch if ch.isprintable() and ch not in "\"\\" else
                   (f"\\u{ord(ch):04x}" if ord(ch) <= 0xFFFF else f"\\U{ord(ch):08x}")
                   for ch in str(word)[:limit])
    if word == "i" or word.startswith("i'"):
        return "I" + word[1:]
    return word[:1].upper() + word[1:]


def summary_rows(fp):
    s, para, rate = fp["sentences"], fp["paragraphs"], fp["per_1000_words"]
    rows = []
    if s["count"]:
        rows.append(("Sentence length", f"Usually {fmt(s['p10'])} to {fmt(s['p90'])} words, average {fmt(s['mean'])}"))
        rows.append(("Short and long sentences",
                     f"{pct(s['under_8_share'])} under 8 words, {pct(s['over_25_share'])} over 25"))
    if para["count"]:
        rows.append(("Paragraphs", f"About {fmt(para['sentences_mean'])} sentences each; "
                                   f"{pct(para['single_sentence_share'])} are a single sentence"))
    rows.append(("Commas, semicolons, colons",
                 f"{fmt(rate['commas'])} commas, {fmt(rate['semicolons'])} semicolons and "
                 f"{fmt(rate['colons'])} colons per 1,000 words"))
    dashes = {"em dashes": rate["em_dashes"] or 0, "en dashes": rate["en_dashes"] or 0,
              "spaced hyphens": rate["hyphen_dashes"] or 0}
    total = sum(dashes.values())
    if total:
        kind = max(sorted(dashes), key=lambda k: dashes[k])
        rows.append(("Dashes", f"About {fmt(total)} per 1,000 words, mostly {kind}"))
    else:
        rows.append(("Dashes", "None in the samples"))
    rows.append(("Questions and exclamations",
                 f"{fmt(rate['question_marks'])} question marks and {fmt(rate['exclamation_marks'])} "
                 "exclamation marks per 1,000 words"))
    c = fp["contractions"]["share_contracted"]
    rows.append(("Contractions", (f"Contracted {pct(c)} of the time (don't rather than do not); "
                                  if c is not None else "") + f"{fmt(rate['contractions'])} per 1,000 words"))
    singular, plural = rate["first_person_singular"] or 0, rate["first_person_plural"] or 0
    lead = ("Mostly I" if singular >= 2 * plural and singular else
            "Mostly we" if plural >= 2 * singular and plural else "Both I and we")
    rows.append(("I or we", f"{lead}: I, me, my {fmt(singular)} and we, us, our {fmt(plural)} per 1,000 words"))
    rows.append(("Hedges and intensifiers",
                 f"{fmt(rate['hedges'])} hedges (maybe, I think) and {fmt(rate['intensifiers'])} "
                 "intensifiers (really, very) per 1,000 words, rough"))
    if fp["openers"]:
        starters = ", ".join(f'"{display_word(w)}" ({pct(v)})' for w, v in list(fp["openers"].items())[:4])
        rows.append(("Favourite sentence starters", starters))
    sp = fp["spelling"]
    lean = sp["lean"]
    ending = ("-ise" if sp["ise"] > sp["ize"] else "-ize" if sp["ize"] > sp["ise"] else None)
    spelling_text = ("Not enough signals to tell" if lean == "unclear" else lean[:1].upper() + lean[1:])
    if ending and (sp["ise"] + sp["ize"]) >= 2:
        spelling_text += f"; {ending} endings"
    rows.append(("Spelling", spelling_text))
    curly = fp["quote_style"]["curly_share"]
    rows.append(("Quote marks and apostrophes",
                 "Too few to tell" if curly is None else
                 "Curly (’ “ ”)" if curly >= 0.8 else "Straight (' \")" if curly <= 0.2 else "A mix of curly and straight"))
    return rows


def intro_line(fp):
    samples = fp["samples"]
    line = (f"Measured from {samples} {'sample' if samples == 1 else 'samples'}, {fp['words']:,} words. "
            f"Confidence: {fp['confidence']}. These describe habits, not quality.")
    if fp["confidence"] == "low":
        line += " Add more of their own writing (300 words or more) for a steadier picture."
    return line


def format_json(obj):
    """Stable JSON: one top-level key per line, nested objects one entry per line."""
    def dump(value):
        return json.dumps(value, ensure_ascii=True, separators=(", ", ": "))
    lines, keys = ["{"], list(obj)
    for i, key in enumerate(keys):
        comma = "," if i < len(keys) - 1 else ""
        value = obj[key]
        if isinstance(value, dict) and value:
            lines.append(f"  {dump(key)}: {{")
            entries = [f"{dump(k)}: {dump(v)}" for k, v in value.items()]
            per_line = 8 if len(entries) > 12 else 1      # pack long word lists
            for j in range(0, len(entries), per_line):
                last = j + per_line >= len(entries)
                lines.append("    " + ", ".join(entries[j:j + per_line]) + ("" if last else ","))
            lines.append("  }" + comma)
        else:
            lines.append(f"  {dump(key)}: {dump(value)}{comma}")
    lines.append("}")
    return "\n".join(lines)


def render_profile_markdown(fp):
    lines = ["### Fingerprint", "", intro_line(fp), "", "| Habit | This writer |", "|---|---|"]
    lines.extend(f"| {habit} | {value} |" for habit, value in summary_rows(fp))
    lines.extend(["", MARKER, "```json", format_json(fp), "```"])
    return "\n".join(lines) + "\n"


def render_profile_plain(fp):
    lines = ["Fingerprint", intro_line(fp), ""]
    lines.extend(f"- {habit}: {value}" for habit, value in summary_rows(fp))
    lines.extend(["", "Use --markdown for a block to paste into a voice file, or --json for the numbers."])
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- reading a Fingerprint back

def number(container, key):
    value = container.get(key) if isinstance(container, dict) else None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value) if math.isfinite(value) else None


def reject_constant(name):
    raise ValueError(f"{name} is not allowed")


# What a Fingerprint may hold. A voice file can be edited by anyone, so every value compare
# reads is checked before use: numbers must be finite and in a sensible range, and the few
# words in it must look like what profile writes. Anything else stops with exit code 2.
COUNT = ("count", 0, 10 ** 9)                 # a whole number
SHARE = ("number", 0.0, 1.0)                  # a share of a total
LENGTH = ("number", 0.0, 1e9)                 # words per sentence, sentences per paragraph
RATE = ("number", 0.0, 1000.0)                # per 1,000 words, at most one per word
MARKS = ("number", 0.0, 1e12)                 # punctuation per 1,000 words: can be more than one per word
PUNCTUATION_RATES = ("commas", "semicolons", "colons", "em_dashes", "en_dashes", "hyphen_dashes",
                     "parentheses", "exclamation_marks", "question_marks", "ellipses", "quotation_marks")
WORD_RATES = ("contractions", "first_person_singular", "first_person_plural", "hedges", "intensifiers",
              "ing_starts_rough", "nominalisations_rough")
SECTIONS = {
    "sentences": {"count": COUNT, "mean": LENGTH, "median": LENGTH, "p10": LENGTH, "p90": LENGTH,
                  "sd": LENGTH, "under_8_share": SHARE, "over_25_share": SHARE},
    "paragraphs": {"count": COUNT, "sentences_mean": LENGTH, "sentences_sd": LENGTH,
                   "single_sentence_share": SHARE},
    "per_1000_words": dict({key: MARKS for key in PUNCTUATION_RATES}, **{key: RATE for key in WORD_RATES}),
    "contractions": {"contracted": COUNT, "expanded": COUNT, "share_contracted": SHARE},
    "quote_style": {"curly": COUNT, "straight": COUNT, "curly_share": SHARE},
    "spelling": {key: COUNT for key in ("our_british", "our_american", "re_british", "re_american",
                                        "other_british", "other_american", "ise", "ize")},
    "function_word_chunks": {"size": ("count", 1, 1_000_000), "count": COUNT},
}
REQUIRED_SECTIONS = ("sentences", "paragraphs", "per_1000_words")
CONFIDENCE_LEVELS = ("low", "medium", "high")
SPELLING_LEANS = ("British", "American", "mostly British", "mostly American", "mixed", "unclear")
MAX_OPENERS = 50
MAX_WORD_LENGTH = 1000      # reports show at most the first 40 characters of a word
MAX_NOTE_LENGTH = 1000


class BadFingerprint(Exception):
    """A value in the Fingerprint that compare can't trust."""


def single_word(word):
    """True for a sentence starter as profile writes it: one word, number or abbreviation.
    No spaces, double quotes, backslashes or invisible characters, so it can't carry a
    sentence or hidden text into a report."""
    return (0 < len(word) <= MAX_WORD_LENGTH and word.isprintable()
            and not any(ch.isspace() or ch in "\"\\" for ch in word))


def label(path):
    """A key path for a message, made safe to print whatever the keys contain."""
    return ".".join(json.dumps(str(part)[:40], ensure_ascii=True).strip('"') for part in path)


def check_value(value, rule, path):
    kind, low, high = rule
    if value is None:
        return
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise BadFingerprint(f"{label(path)} should be a number")
    if not low <= value <= high:              # also false for NaN and infinity
        raise BadFingerprint(f"{label(path)} is out of range")
    if kind == "count" and value != int(value):
        raise BadFingerprint(f"{label(path)} should be a whole number")


def check_rates(value, path, limit):
    """A word -> number table: function_word_rates and function_word_sd."""
    if value is None:
        return
    if not isinstance(value, dict) or len(value) > 4 * len(FUNCTION_WORDS):
        raise BadFingerprint(f"{label(path)} should be a short table of words and numbers")
    for word, rate in value.items():
        if len(word) > MAX_WORD_LENGTH:
            raise BadFingerprint(f"{label(path)} has a word that is too long")
        check_value(rate, ("number", 0.0, limit), path + [word])


def validate_fingerprint(data):
    """Raise BadFingerprint if anything compare reads is missing, the wrong type or out of range."""
    version = data.get("version")
    if not isinstance(version, int) or isinstance(version, bool) or version < 1:
        raise BadFingerprint("it has no valid version number")
    if version > FORMAT_VERSION:
        raise BadFingerprint("it was made by a newer version of voice_stats.py")
    if data.get("words") is None:
        raise BadFingerprint("it is missing its word count")
    check_value(data.get("words"), COUNT, ["words"])
    check_value(data.get("samples"), COUNT, ["samples"])
    confidence = data.get("confidence")
    if confidence is not None and confidence not in CONFIDENCE_LEVELS:
        raise BadFingerprint("confidence should be low, medium or high")
    note = data.get("note")
    if note is not None and (not isinstance(note, str) or len(note) > MAX_NOTE_LENGTH):
        raise BadFingerprint("note should be a short piece of text")
    for section, rules in SECTIONS.items():
        value = data.get(section)
        if value is None and section not in REQUIRED_SECTIONS:
            continue
        if not isinstance(value, dict):
            raise BadFingerprint(f"'{section}' is missing or isn't a table")
        for key, rule in rules.items():
            check_value(value.get(key), rule, [section, key])
    lean = (data.get("spelling") or {}).get("lean")
    if lean is not None and lean not in SPELLING_LEANS:
        raise BadFingerprint("spelling.lean isn't one of the leans profile writes")
    openers = data.get("openers")
    if openers is not None:
        if not isinstance(openers, dict) or len(openers) > MAX_OPENERS:
            raise BadFingerprint(f"openers should be a table of at most {MAX_OPENERS} words")
        for word, value in openers.items():
            if not single_word(word):
                raise BadFingerprint("openers should hold single words, like the ones profile writes")
            check_value(value, SHARE, ["openers", word])
    check_rates(data.get("function_word_rates"), ["function_word_rates"], 1000.0)
    check_rates(data.get("function_word_sd"), ["function_word_sd"], 1000.0)


def parse_fingerprint(text, source):
    if len(text) > MAX_FINGERPRINT_JSON:
        raise UsageError(f"The Fingerprint in {source} is too large to be a real one.")
    try:
        data = json.loads(text, parse_constant=reject_constant)
    except (ValueError, RecursionError) as error:
        raise UsageError(f"The Fingerprint in {source} isn't valid JSON ({error}).") from None
    if not isinstance(data, dict) or data.get("format") != FORMAT_NAME:
        raise UsageError(f"{source} doesn't contain a Natural Voice Fingerprint.")
    try:
        validate_fingerprint(data)
    except BadFingerprint as problem:
        raise UsageError(f"The Fingerprint in {source} can't be used: {problem}. Run profile again on the "
                         "person's own samples and replace the block, rather than editing the numbers by hand.") from None
    return data


def fingerprint_from_voice_file(text, source):
    lines = text.splitlines()
    markers = [i for i, line in enumerate(lines) if line.strip() == MARKER]
    if not markers:
        raise UsageError(f"No Fingerprint found in {source}. Run profile --markdown on the person's "
                         "own samples and put the block in the voice file's Fingerprint section.")
    i = markers[0] + 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    opening = re.match(r"^\s*(`{3,}|~{3,})\s*(?:json)?\s*$", lines[i], re.IGNORECASE) if i < len(lines) else None
    if not opening:
        raise UsageError(f"In {source}, the Fingerprint marker must be followed by a ```json block.")
    fence, body = opening.group(1), []
    for line in lines[i + 1:]:
        stripped = line.strip()
        if stripped and set(stripped) == {fence[0]} and len(stripped) >= len(fence):
            return parse_fingerprint("\n".join(body), source), len(markers)
        body.append(line)
    raise UsageError(f"In {source}, the Fingerprint's json block has no closing fence.")


def load_fingerprint(voice_file, fingerprint_file):
    if voice_file:
        name, text = read_source(voice_file)
        return fingerprint_from_voice_file(text, name)
    name, text = read_source(fingerprint_file)
    if MARKER in text:
        return fingerprint_from_voice_file(text, name)
    return parse_fingerprint(text, name), 1


# ---------------------------------------------------------------- comparing a draft

def poisson_tail(k, lam, upper):
    """P(X >= k) when upper, else P(X <= k), for a Poisson count with mean lam."""
    lam = max(lam, 1e-9)

    def term(i):
        return math.exp(-lam + i * math.log(lam) - math.lgamma(i + 1))
    if upper:
        if k <= 0:
            return 1.0
        total, i = 0.0, k
        while i < k + 100000:
            t = term(i)
            total += t
            if i > lam and t < 1e-15:
                break
            i += 1
        return min(1.0, total)
    return min(1.0, sum(term(i) for i in range(0, k + 1)))


def binomial_tail(k, n, p, upper):
    p = min(max(p, 1e-6), 1 - 1e-6)

    def term(i):
        return math.exp(math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1)
                        + i * math.log(p) + (n - i) * math.log(1 - p))
    if upper:
        return min(1.0, sum(term(i) for i in range(k, n + 1)))
    return min(1.0, sum(term(i) for i in range(0, k + 1)))


def surprise(p_value):
    return -math.log(max(p_value, 1e-300))


RATE_CHECKS = (
    ("dashes", "dashes"), ("commas", "commas"), ("semicolons", "semicolons"), ("colons", "colons"),
    ("parentheses", "brackets"), ("question_marks", "question marks"),
    ("exclamation_marks", "exclamation marks"), ("ellipses", "ellipses (...)"),
    ("contractions", "contractions (don't, it's)"),
    ("hedges", "hedges such as \"maybe\" or \"I think\""),
    ("intensifiers", "intensifiers such as \"really\" or \"very\""),
    ("ing_starts_rough", "sentences that open with an -ing word (rough count)"),
    ("nominalisations_rough", "-tion, -ment and -ness nouns (rough count)"),
)


def rate_value(rates, key):
    if key == "dashes":
        parts = [number(rates, k) for k in ("em_dashes", "en_dashes", "hyphen_dashes")]
        return None if all(v is None for v in parts) else sum(v or 0 for v in parts)
    return number(rates, key)


def compare_rates(fp, draft, fp_words, n):
    found = []
    for key, thing in RATE_CHECKS:
        fp_rate = rate_value(fp["per_1000_words"], key)
        d_rate = rate_value(draft["per_1000_words"], key)
        if fp_rate is None or d_rate is None:
            continue
        fp_count = fp_rate * fp_words / 1000
        expected_rate = (fp_count + 0.5) / (fp_words + 1) * 1000
        lam = expected_rate * n / 1000
        observed = int(round(d_rate * n / 1000))
        ratio = (d_rate + 0.01) / (expected_rate + 0.01)
        if observed > lam:
            p_value, big_enough = poisson_tail(observed, lam, True), ratio >= 1.8
        else:
            p_value, big_enough = poisson_tail(observed, lam, False), ratio <= 0.55
        size = surprise(p_value)
        if size < SHOW_THRESHOLD or not big_enough:
            continue
        if observed == 0:
            message = f"You use about {fmt(fp_rate)} {thing} per 1,000 words; this draft has none."
        elif fp_count < 0.5:
            message = f"Your samples have no {thing}; this draft has {observed}."
        elif fp_rate < 0.5:
            message = (f"You rarely use {thing} (under 1 per 1,000 words); this draft has {observed} "
                       f"(about {fmt(d_rate)} per 1,000).")
        else:
            message = (f"You use about {fmt(fp_rate)} {thing} per 1,000 words; this draft has about "
                       f"{fmt(d_rate)} ({'more' if d_rate > fp_rate else 'fewer'} than you usually do).")
        found.append({"metric": key, "size": round(size, 2), "message": message})
    return found


def compare_sentences(fp, draft):
    found = []
    fs, ds = fp["sentences"], draft["sentences"]
    count = ds["count"] or 0
    lo, hi, dlo, dhi = (number(fs, "p10"), number(fs, "p90"), number(ds, "p10"), number(ds, "p90"))
    if count >= 6 and None not in (lo, hi, dlo, dhi) and hi - lo > 0:
        ratio = max(dhi - dlo, 0.5) / (hi - lo)
        size = 1.5 * abs(math.log(ratio)) / 0.25 * min(1.0, math.sqrt(count / 10))
        if size >= SHOW_THRESHOLD:
            shape = "more uniform than you write" if ratio < 1 else "more varied than you write"
            verb = "stays between" if ratio < 1 else "swings from"
            joiner = "and" if ratio < 1 else "to"
            found.append({"metric": "sentence_spread", "size": round(size, 2), "message":
                          f"Your sentences usually range {fmt(lo)} to {fmt(hi)} words; this draft "
                          f"{verb} {fmt(dlo)} {joiner} {fmt(dhi)} ({shape})."})
    f_mean, d_mean, f_sd = number(fs, "mean"), number(ds, "mean"), number(fs, "sd")
    if count >= 4 and f_mean and d_mean and f_sd:
        z = (d_mean - f_mean) / (f_sd / math.sqrt(count))
        ratio = d_mean / f_mean
        size = z * z / 2
        if size >= SHOW_THRESHOLD and (ratio >= 1.3 or ratio <= 0.77):
            found.append({"metric": "sentence_length", "size": round(size, 2), "message":
                          f"Your sentences average {fmt(f_mean)} words; this draft's average "
                          f"{fmt(d_mean)} ({'longer' if ratio > 1 else 'shorter'} than you usually write)."})
    fp_par, d_par = fp["paragraphs"], draft["paragraphs"]
    f_pm, d_pm, f_psd = number(fp_par, "sentences_mean"), number(d_par, "sentences_mean"), number(fp_par, "sentences_sd")
    d_count = number(d_par, "count") or 0
    if d_count >= 3 and (number(fp_par, "count") or 0) >= 3 and f_pm and d_pm:
        z = (d_pm - f_pm) / ((f_psd or 1.0) / math.sqrt(d_count) + 0.3)
        ratio = d_pm / f_pm
        size = z * z / 2
        if size >= SHOW_THRESHOLD and (ratio >= 1.5 or ratio <= 0.67):
            found.append({"metric": "paragraph_length", "size": round(size, 2), "message":
                          f"Your paragraphs usually have about {fmt(f_pm)} sentences; this draft's "
                          f"average {fmt(d_pm)}."})
    return found


def compare_shares(fp, draft, draft_measures):
    found = []
    # Contractions: share of easy pairs contracted ("don't" against "do not").
    fp_share = number(fp.get("contractions", {}), "share_contracted")
    eligible = draft_measures["contracted"] + draft_measures["expanded"]
    if fp_share is not None and eligible >= 4:
        d_share = draft_measures["contracted"] / eligible
        p = min(max(fp_share, 0.05), 0.95)
        upper = d_share > p
        p_value = binomial_tail(draft_measures["contracted"], eligible, p, upper)
        size = surprise(p_value)
        if size >= SHOW_THRESHOLD and abs(d_share - fp_share) >= 0.3:
            habit = ("You almost always contract" if fp_share >= 0.95 else
                     "You almost never contract" if fp_share <= 0.05 else
                     f"You contract about {pct(fp_share)} of the time")
            done = ("never does" if d_share == 0 else "always does" if d_share == 1 else
                    f"does it {pct(d_share)} of the time")
            found.append({"metric": "contraction_share", "size": round(size, 2), "message":
                          f"{habit} (don't rather than do not); this draft {done} "
                          f"({draft_measures['contracted']} of {eligible} chances)."})
    # I against we.
    rates = fp["per_1000_words"]
    f_i, f_we = number(rates, "first_person_singular"), number(rates, "first_person_plural")
    d_i, d_we = draft_measures["singular"], draft_measures["plural"]
    if f_i is not None and f_we is not None and (f_i + f_we) > 0 and d_i + d_we >= 5:
        f_share = f_i / (f_i + f_we)
        d_share = d_i / (d_i + d_we)
        p = min(max(f_share, 0.05), 0.95)
        p_value = binomial_tail(d_i, d_i + d_we, p, d_share > p)
        size = surprise(p_value)
        if size >= SHOW_THRESHOLD and abs(d_share - f_share) >= 0.35:
            mostly = "I" if f_share >= 0.5 else "we"
            draft_mostly = "I" if d_share >= 0.5 else "we"
            found.append({"metric": "i_or_we", "size": round(size, 2), "message":
                          f"You mostly write as \"{mostly}\" ({pct(max(f_share, 1 - f_share))} of I and we words); "
                          f"this draft leans to \"{draft_mostly}\" ({pct(max(d_share, 1 - d_share))}). "
                          "Check it matches who did the work."})
    # Sentence starters.
    sentences = draft["sentences"]["count"] or 0
    openers = fp.get("openers") if isinstance(fp.get("openers"), dict) else {}
    fp_sentences = number(fp["sentences"], "count") or 1
    known = {str(k)[:40]: v for k, v in openers.items() if number(openers, k) is not None}
    floor = min(known.values()) if len(known) >= 8 else 0.5 / fp_sentences
    if sentences >= 5:
        for word, count in sorted(draft_measures["openers"].items(), key=lambda kv: (-kv[1], kv[0])):
            if count < 3:
                break
            p = known.get(word, floor)
            d_share = count / sentences
            if d_share < 2 * max(p, 0.01):
                continue
            size = surprise(binomial_tail(count, sentences, max(p, 0.005), True))
            if size < SHOW_THRESHOLD:
                continue
            shown = display_word(word)
            if word in known:
                message = (f"You start about {pct(p)} of sentences with \"{shown}\"; this draft does it "
                           f"{count} times out of {sentences} ({pct(d_share)}).")
            elif floor <= 0.03:
                message = f"You rarely start sentences with \"{shown}\"; this draft does it {count} times."
            else:
                message = (f"\"{shown}\" isn't one of your usual sentence starters; this draft starts "
                           f"{count} sentences with it.")
            found.append({"metric": "opener:" + word, "size": round(size, 2), "message": message})
        for word, p in known.items():
            if p < 0.08:
                continue
            count = draft_measures["openers"].get(word, 0)
            if count / sentences > 0.5 * p:
                continue
            size = surprise(binomial_tail(count, sentences, p, False))
            if size >= SHOW_THRESHOLD:
                found.append({"metric": "opener:" + word, "size": round(size, 2), "message":
                              f"You often start sentences with \"{display_word(word)}\" (about {pct(p)}); "
                              f"this draft does it {count} {'time' if count == 1 else 'times'}."})
    return found


def compare_spelling_and_quotes(fp, draft_measures):
    found = []
    sp = fp.get("spelling") if isinstance(fp.get("spelling"), dict) else {}
    lean = sp.get("lean")
    words = draft_measures["spelling"]
    american = words["our_american"] + words["re_american"] + words["other_american"]
    british = words["our_british"] + words["re_british"] + words["other_british"]

    def examples(items):
        return ", ".join(sorted(set(items))[:3])
    fp_american = sum(number(sp, k) or 0 for k in ("our_american", "re_american", "other_american"))
    fp_british = sum(number(sp, k) or 0 for k in ("our_british", "re_british", "other_british"))
    if lean in ("British", "mostly British") and fp_american == 0 and american:
        found.append({"metric": "spelling", "size": round(3.5 + len(american), 2), "message":
                      f"You use British spellings; this draft has {len(american)} American "
                      f"{'one' if len(american) == 1 else 'ones'} ({examples(american)})."})
    elif lean in ("American", "mostly American") and fp_british == 0 and british:
        found.append({"metric": "spelling", "size": round(3.5 + len(british), 2), "message":
                      f"You use American spellings; this draft has {len(british)} British "
                      f"{'one' if len(british) == 1 else 'ones'} ({examples(british)})."})
    fp_ise, fp_ize = number(sp, "ise") or 0, number(sp, "ize") or 0
    if fp_ise >= 2 and fp_ize == 0 and words["ize"]:
        found.append({"metric": "ise_ize", "size": round(3.2 + len(words["ize"]), 2), "message":
                      f"You write -ise endings (organise); this draft uses -ize ({examples(words['ize'])})."})
    elif fp_ize >= 2 and fp_ise == 0 and words["ise"]:
        found.append({"metric": "ise_ize", "size": round(3.2 + len(words["ise"]), 2), "message":
                      f"You write -ize endings (organize); this draft uses -ise ({examples(words['ise'])})."})
    fp_curly = number(fp.get("quote_style", {}), "curly_share")
    marks = draft_measures["curly"] + draft_measures["straight"]
    if fp_curly is not None and marks >= 3:
        d_curly = draft_measures["curly"] / marks
        if fp_curly >= 0.8 and d_curly <= 0.2:
            found.append({"metric": "quote_style", "size": 3.5, "message":
                          "You type curly quotes and apostrophes (’ “ ”); this draft uses straight ones (' \")."})
        elif fp_curly <= 0.2 and d_curly >= 0.8:
            found.append({"metric": "quote_style", "size": 3.5, "message":
                          "You type straight quotes and apostrophes (' \"); this draft uses curly ones (’ “ ”)."})
    return found


def function_word_distance(fp, draft_measures):
    """Burrows' Delta style: mean absolute z-score over the function words.

    Each z compares the draft's rate with the Fingerprint's, scaled by the variation you
    would expect from a text of the draft's length plus the variation between chunks of
    the person's own samples. About 0.8 is typical when the habits match.
    """
    rates = fp.get("function_word_rates")
    if not isinstance(rates, dict):
        return None
    sds = fp.get("function_word_sd") if isinstance(fp.get("function_word_sd"), dict) else {}
    chunk_info = fp.get("function_word_chunks") if isinstance(fp.get("function_word_chunks"), dict) else {}
    chunk = number(chunk_info, "size") or CHUNK_WORDS
    fp_words = number(fp, "words") or 0
    n = draft_measures["words"]
    zs = []
    for word in FUNCTION_WORDS:
        rate = number(rates, word)
        if rate is None:
            continue
        p = (rate * fp_words / 1000 + 0.5) / (fp_words + 1)
        sampling = p * (1 - p) / n
        between = 0.0
        chunk_sd = number(sds, word)
        if chunk_sd is not None:
            between = max(0.0, (chunk_sd / 1000) ** 2 - p * (1 - p) / chunk)
        observed = draft_measures["function_counts"][word] / n
        if sampling + between <= 0:
            continue
        zs.append(abs(observed - rate / 1000) / math.sqrt(sampling + between))
    if len(zs) < 20:
        return None
    score = sum(zs) / len(zs)
    band = ("close to your samples" if score <= 1.1 else
            "a little different from your samples" if score <= 1.6 else
            "noticeably different from your samples")
    return {
        "score": round(score, 2), "band": band, "words_compared": len(zs),
        "explanation": ("It measures how differently this draft uses about 50 everyday words such as "
                        "\"the\", \"and\", \"but\" and \"which\"; lower means closer to your samples, and "
                        "it describes style only."),
    }


def compare_draft(fp, draft_measures):
    draft = fingerprint_from(draft_measures, 1)
    fp_words, n = number(fp, "words") or 0, draft_measures["words"]
    result = {
        "skipped": False, "reason": None, "draft_words": n, "fingerprint_words": int(fp_words),
        "fingerprint_confidence": fp.get("confidence") if isinstance(fp.get("confidence"), str) else None,
        "differences": [], "function_word_distance": None,
        "note": "These are habits, not rules: a difference is worth a look, not an automatic fix.",
    }
    if n < MIN_COMPARE_WORDS or fp_words < MIN_COMPARE_WORDS:
        which = (f"this draft has {n} words" if n < MIN_COMPARE_WORDS
                 else f"the Fingerprint is based on {int(fp_words)} words")
        result["skipped"] = True
        result["reason"] = (f"Skipped: {which}. These measures need at least {MIN_COMPARE_WORDS} words in "
                            "both the draft and the samples to say anything useful.")
        return result
    found = []
    found.extend(compare_sentences(fp, draft))
    found.extend(compare_rates(fp, draft, fp_words, n))
    found.extend(compare_shares(fp, draft, draft_measures))
    found.extend(compare_spelling_and_quotes(fp, draft_measures))
    if any(d["metric"] == "contraction_share" for d in found):
        found = [d for d in found if d["metric"] != "contractions"]   # same habit, say it once
    found.sort(key=lambda d: (-d["size"], d["metric"]))
    result["differences"] = found[:MAX_DIFFERENCES]
    result["function_word_distance"] = function_word_distance(fp, draft_measures)
    return result


def render_compare(result, draft_name):
    if result["skipped"]:
        return result["reason"] + "\n"
    confidence_text = result["fingerprint_confidence"] or "unknown"
    lines = [f"Compared {draft_name} ({result['draft_words']:,} words) with the Fingerprint "
             f"({result['fingerprint_words']:,} words, confidence: {confidence_text}).", ""]
    if confidence_text == "low":
        lines.extend(["The Fingerprint is based on fewer than 300 words, so treat these as rough hints.", ""])
    if result["differences"]:
        lines.append("Biggest differences:")
        lines.extend(f"{i}. {d['message']}" for i, d in enumerate(result["differences"], 1))
    else:
        lines.append("No large differences in the measured habits.")
    distance = result["function_word_distance"]
    if distance:
        lines.extend(["", f"Small-word distance: {distance['score']} ({distance['band']}). "
                          + distance["explanation"]])
    lines.extend(["", result["note"]])
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- command line

def emit(stream, text):
    try:
        stream.write(text)
        stream.flush()
    except UnicodeEncodeError:
        encoding = getattr(stream, "encoding", None) or "ascii"
        stream.buffer.write(text.encode(encoding, "backslashreplace"))
        stream.buffer.flush()


def printable(value, limit=200):
    """Text for an error message: unprintable characters escaped, and cut to `limit`."""
    text = str(value)
    shown = "".join(ch if ch.isprintable() else repr(ch)[1:-1] for ch in text[:limit])
    return shown + ("..." if len(text) > limit else "")


def profile_paths(paths):
    if paths.count("-") > 1:
        raise UsageError("Standard input can only be used once.")
    paragraphs = []
    for path in paths:
        _, text = read_source(path)
        paragraphs.extend(extract_paragraphs(text))
    measures = measure(paragraphs)
    if measures["words"] == 0:
        raise UsageError("No prose found in the samples (after leaving out code, quotes, headings and links).")
    return fingerprint_from(measures, len(paths))


def main(argv=None):
    parser = argparse.ArgumentParser(prog="voice_stats.py", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--version", action="version", version=VERSION)
    commands = parser.add_subparsers(dest="command", metavar="COMMAND")
    commands.required = True
    profile = commands.add_parser("profile", help="measure writing samples and print a Fingerprint")
    profile.add_argument("files", nargs="+", metavar="FILE")
    style = profile.add_mutually_exclusive_group()
    style.add_argument("--json", action="store_true", help="print the numbers as JSON")
    style.add_argument("--markdown", action="store_true", help="print a block to paste into a voice file")
    compare = commands.add_parser("compare", help="compare a draft with a Fingerprint")
    compare.add_argument("draft", metavar="DRAFT")
    source = compare.add_mutually_exclusive_group(required=True)
    source.add_argument("--voice-file", metavar="VOICE.md", help="voice file that contains a Fingerprint")
    source.add_argument("--fingerprint", metavar="FILE.json", help="Fingerprint JSON (from profile --json)")
    compare.add_argument("--json", action="store_true", help="print the result as JSON")
    args = parser.parse_args(argv)
    try:
        if args.command == "profile":
            fp = profile_paths(args.files)
            if args.json:
                output = format_json(fp) + "\n"
            elif args.markdown:
                output = render_profile_markdown(fp)
            else:
                output = render_profile_plain(fp)
        else:
            fp, marker_count = load_fingerprint(args.voice_file, args.fingerprint)
            name, text = read_source(args.draft)
            result = compare_draft(fp, measure(extract_paragraphs(text)))
            if marker_count > 1:
                result["warning"] = "The voice file has more than one Fingerprint; the first one was used."
            output = (json.dumps(result, ensure_ascii=True, indent=2) + "\n" if args.json
                      else render_compare(result, name)
                      + (f"\nNote: {result['warning']}\n" if result.get("warning") else ""))
        emit(sys.stdout, output)
        return EXIT_OK
    except (UsageError, OSError) as error:
        message = printable(error, 600)
    except (ValueError, ArithmeticError) as error:
        message = (f"A number couldn't be worked out ({type(error).__name__}: {printable(error)}). "
                   "If the Fingerprint was edited by hand, run profile again to make a fresh one.")
    except Exception as error:      # a bug; exit 2 with a short message rather than a traceback
        message = (f"Something unexpected went wrong inside the script ({type(error).__name__}: "
                   f"{printable(error)}). Please report it as a bug.")
    emit(sys.stderr, "Problem: " + message + "\n")
    return EXIT_USAGE


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(EXIT_USAGE)
