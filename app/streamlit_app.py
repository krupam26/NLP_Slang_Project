import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


import streamlit as st

from src.converter import slang_to_formal, formal_to_slang
from src.detector import detect_style


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Slang ↔ Formal Converter",
    page_icon="💬",
    layout="centered",
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("💬 Slang ↔ Formal Text Converter")

st.write(
    "Convert text between informal/slang and formal language "
    "using NLP techniques."
)


# --------------------------------------------------
# MODE
# --------------------------------------------------

mode = st.radio(
    "Choose conversion mode:",
    [
        "Slang → Formal",
        "Formal → Slang",
    ],
    horizontal=True,
)


# --------------------------------------------------
# INPUT
# --------------------------------------------------

text = st.text_area(
    "Enter your text:",
    height=150,
    placeholder=(
        "Example: Hey bro, what r u doing? "
        "I'm gonna call u later lol"
    ),
)


# --------------------------------------------------
# CONVERT
# --------------------------------------------------

if st.button(
    "Convert Text",
    type="primary",
    use_container_width=True,
):

    if not text.strip():

        st.warning("Please enter some text.")

    else:

        # Detect writing style
        detected_style = detect_style(text)

        # Perform conversion
        if mode == "Slang → Formal":

            result = slang_to_formal(text)

        else:

            result = formal_to_slang(text)


        # --------------------------------------------------
        # RESULTS
        # --------------------------------------------------

        st.divider()

        st.subheader("📊 Analysis")

        st.write(
            f"**Detected writing style:** `{detected_style}`"
        )

        st.subheader("📝 Converted Text")

        st.success(result)


        # --------------------------------------------------
        # ORIGINAL TEXT
        # --------------------------------------------------

        with st.expander("View original text"):

            st.write(text)