import re

from .preprocessing import normalize_text


SLANG_TO_FORMAL = {
    "u": "you",
    "ur": "your",
    "r": "are",
    "idk": "I don't know",
    "imo": "in my opinion",
    "tbh": "to be honest",
    "brb": "be right back",
    "btw": "by the way",
    "gonna": "going to",
    "wanna": "want to",
    "gotta": "have to",
    "thx": "thanks",
    "pls": "please",
    "plz": "please",
    "cuz": "because",
    "bc": "because",
    "rn": "right now",
    "omg": "oh my goodness",
    "bro": "friend",
    "lol": "",
}


FORMAL_TO_SLANG = {
    "I don't know": "idk",
    "in my opinion": "imo",
    "to be honest": "tbh",
    "be right back": "brb",
    "by the way": "btw",
    "going to": "gonna",
    "want to": "wanna",
    "have to": "gotta",
    "thanks": "thx",
    "please": "pls",
    "because": "cuz",
    "right now": "rn",
    "oh my goodness": "omg",
    "friend": "bro",
}


def _replace_word(text: str, slang: str, formal: str) -> str:
    """
    Replace a complete word while preserving punctuation.
    """

    pattern = rf"\b{re.escape(slang)}\b"

    return re.sub(
        pattern,
        formal,
        text,
        flags=re.IGNORECASE
    )


def slang_to_formal(text: str) -> str:
    """
    Convert slang/informal text into a more formal form.
    """

    text = normalize_text(text)

    # Longer expressions first
    replacements = sorted(
        SLANG_TO_FORMAL.items(),
        key=lambda item: len(item[0]),
        reverse=True
    )

    result = text

    for slang, formal in replacements:
        result = _replace_word(result, slang, formal)

    # Clean spaces left by removed slang such as "lol"
    result = re.sub(r"\s+", " ", result)

    # Remove spaces before punctuation
    result = re.sub(r"\s+([,.!?;:])", r"\1", result)

    return result.strip()


def formal_to_slang(text: str) -> str:
    """
    Convert formal text into casual/slang text.
    """

    text = normalize_text(text)

    replacements = sorted(
        FORMAL_TO_SLANG.items(),
        key=lambda item: len(item[0]),
        reverse=True
    )

    result = text

    for formal, slang in replacements:
        result = re.sub(
            rf"\b{re.escape(formal)}\b",
            slang,
            result,
            flags=re.IGNORECASE
        )

    return result.strip()