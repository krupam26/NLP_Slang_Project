import re
from typing import Literal


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
}


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

    slang_ratio = slang_count / len(words)

    if slang_count == 0:
        return "formal"

    if slang_ratio >= 0.5:
        return "slang"

    return "mixed"