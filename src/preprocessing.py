import re


def normalize_text(text: str) -> str:
    """
    Clean and normalize input text.
    """

    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Remove spaces at beginning/end
    text = text.strip()

    return text


def tokenize_text(text: str) -> list[str]:
    """
    Tokenize text into words.
    """

    text = normalize_text(text)

    if not text:
        return []

    return text.split()