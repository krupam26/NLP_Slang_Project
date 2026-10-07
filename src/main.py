from .converter import slang_to_formal, formal_to_slang
from .detector import detect_style


def convert_text(text: str, mode: str) -> str:
    """
    Main conversion function.
    """

    if mode == "slang_to_formal":
        return slang_to_formal(text)

    if mode == "formal_to_slang":
        return formal_to_slang(text)

    raise ValueError(
        "Invalid mode. Use 'slang_to_formal' "
        "or 'formal_to_slang'."
    )


if __name__ == "__main__":

    text = "hey bro what r u doing lol"

    print("Input:", text)
    print("Style:", detect_style(text))
    print("Output:", convert_text(text, "slang_to_formal"))