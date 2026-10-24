import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from src.converter import formal_to_slang, slang_to_formal
from src.detector import detect_style
from src.phrase_model import MODEL as PHRASE_MODEL, predict


st.set_page_config(
    page_title="Slang ↔ Formal Converter",
    page_icon="💬",
    layout="centered",
)

st.title("💬 Slang ↔ Formal Converter")
st.markdown(
    "Rewrite a message in seconds. Choose a direction, paste your text, and convert."
)

with st.container(border=True):
    mode = st.radio(
        "Conversion direction",
        ["Slang → Formal", "Formal → Slang"],
        horizontal=True,
        label_visibility="visible",
    )

    placeholder = (
        "Try: Hey bro, what r u doing? I'm gonna call u later lol"
        if mode == "Slang → Formal"
        else "Try: I do not know what you are doing right now."
    )

    with st.form("converter_form"):
        text = st.text_area(
            "Your message",
            height=160,
            placeholder=placeholder,
            help="Paste or type the message you want to rewrite.",
        )
        st.caption(f"{len(text)} characters")

        use_model = False
        if mode == "Slang → Formal":
            use_model = st.checkbox(
                "Use phrase model for known examples",
                value=PHRASE_MODEL.exists(),
                disabled=not PHRASE_MODEL.exists(),
                help="The phrase model uses exact examples and falls back to the rule converter for other text.",
            )
            if not PHRASE_MODEL.exists():
                st.caption("Phrase model not trained; the rule converter will be used.")

        submitted = st.form_submit_button(
            "Convert message", type="primary", use_container_width=True
        )

if submitted:
    if not text.strip():
        st.session_state.pop("conversion_result", None)
        st.warning("Enter a message first.")
    else:
        if mode == "Slang → Formal":
            result = predict(text) if use_model and PHRASE_MODEL.exists() else slang_to_formal(text)
        else:
            result = formal_to_slang(text)

        st.session_state["conversion_result"] = {
            "input": text,
            "result": result,
            "mode": mode,
            "style": detect_style(text),
        }

conversion = st.session_state.get("conversion_result")
if conversion:
    st.divider()
    st.subheader("Result")
    left, right = st.columns(2)
    with left:
        st.caption("ORIGINAL MESSAGE")
        st.text(conversion["input"])
    with right:
        st.caption("CONVERTED MESSAGE · " + conversion["mode"].upper())
        # st.code provides a built-in copy button for the converted text.
        st.code(conversion["result"], language=None)

    style_label = conversion["style"].capitalize()
    st.caption(f"Detected style: **{style_label}**")
