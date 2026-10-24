import re
from typing import Literal

from .converter import SLANG_TO_FORMAL


Style = Literal["slang", "formal", "mixed", "unknown"]


SLANG_INDICATORS = {
    "lol",
    "lmao",
    "brb",
    "idk",
    "imo",
    "tbh",
    "omg",
    "u",
    "ur",
    "r",
    "gonna",
    "wanna",
    "gotta",
    "bro",
    "btw",
    "thx",
    "pls",
    "plz",
    "cuz",
    "bc",
    "rn",
    "gr8",
    "asap",
    "sus",
    "cant",
    "hru",
    "wbu",
    "wyd",
    "wya",
    "hby",
    "lmk",
    "idc",
    "ik",
    "nvm",
    "ttyl",
    "cya",
    "smh",
    "fyi",
    "ngl",
    "fr",
    "ig",
    "op",
} | {term for term in SLANG_TO_FORMAL if term.isalnum()}


def detect_style(text: str) -> Style:
    """
    Detect whether the text is approximately
    slang, formal, mixed, or unknown.
    """

    if not text or not text.strip():
        return "unknown"

    words = re.findall(r"\b[\w']+\b", text.lower())

    if not words:
        return "unknown"

    slang_count = sum(
        1 for word in words
        if word in SLANG_INDICATORS
    )

    # Count multi-word and punctuation-containing slang phrases (e.g. "no cap", "w/e").
    for term in SLANG_TO_FORMAL:
        if not term.isalnum() and re.search(
            rf"(?<!\w){re.escape(term)}(?!\w)", text, flags=re.IGNORECASE
        ):
            slang_count += len(re.findall(r"\b[\w']+\b", term))

    slang_ratio = slang_count / len(words)

    if slang_count == 0:
        return "formal"

    if slang_ratio >= 0.25:
        return "slang"

    return "mixed"
