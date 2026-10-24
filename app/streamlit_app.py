import sys
from html import escape
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from src.converter import formal_to_slang, slang_to_formal
from src.detector import detect_style
from src.preprocessing import normalize_text


st.set_page_config(
    page_title="Slang ↔ Formal Converter",
    page_icon="💬",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root { --ink:#1b2b25; --muted:#607069; --green:#238344; --line:#dce6df; }
    .stApp, [data-testid="stAppViewContainer"] { background:#f4f8f5; color:var(--ink); }
    [data-testid="stHeader"] { background:transparent; }
    [data-testid="stMainBlockContainer"] { max-width:1320px; padding:1.6rem 2rem 3rem; }
    html, body, [class*="css"] { font-family:'Segoe UI',Arial,sans-serif; color:var(--ink); }
    h1,h2,h3,p,label,[data-testid="stMarkdownContainer"] { color:var(--ink) !important; }
    .brand-row { display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--line); padding:.15rem 0 1rem; margin-bottom:1.2rem; }
    .brand { color:#173d29 !important; font-weight:800; font-size:1.45rem; letter-spacing:-.04em; }
    .brand span { color:var(--green) !important; }
    .brand-note { color:var(--muted) !important; font-size:.9rem; }
    .tool-title { font-size:1.4rem; font-weight:750; letter-spacing:-.03em; margin:.2rem 0 1rem; }
    div[data-testid="stRadio"] > label, div[data-testid="stWidgetLabel"] p { color:#263a30 !important; font-weight:650; }
    div[role="radiogroup"] { gap:.5rem; }
    div[role="radiogroup"] label { background:#fff; color:#24372e !important; border:1px solid var(--line); border-radius:10px; padding:.55rem .85rem; }
    div[role="radiogroup"] label p, div[role="radiogroup"] label span { color:#24372e !important; }
    div[role="radiogroup"] label:has(input:checked) { background:#edf7f0; border-color:#48a465; }
    input[type="radio"], input[type="checkbox"] { accent-color:var(--green) !important; }
    .panel-heading { display:flex; justify-content:space-between; align-items:center; min-height:2rem; margin:.1rem 0 .45rem; }
    .input-heading { padding-left:16px; }
    .panel-title { color:#23372d !important; font-size:1rem; font-weight:750; }
    .panel-subtitle { color:#718078 !important; font-size:.8rem; }
    div[data-testid="stTextArea"] textarea { background:#fff !important; border:1px solid #d5e0d8 !important; border-radius:10px; color:#1b2b25 !important; line-height:1.65; padding:.9rem; }
    div[data-testid="stTextArea"] textarea::placeholder { color:#79867f !important; opacity:1; }
    div[data-testid="stTextArea"] textarea:focus { border-color:#48a465 !important; box-shadow:0 0 0 3px #23834420; }
    div[data-testid="stFormSubmitButton"] button { color:#fff !important; background:#238344 !important; border:0; border-radius:999px; font-size:1rem; font-weight:700; min-height:2.9rem; }
    div[data-testid="stFormSubmitButton"] button p, div[data-testid="stFormSubmitButton"] button span { color:#fff !important; }
    div[data-testid="stButton"] button { color:#23733e !important; background:#fff !important; border:1px solid #62ad77 !important; border-radius:999px; }
    div[data-testid="stButton"] button:hover { background:#edf7f0 !important; }
    .output-box { box-sizing:border-box; height:285px; margin-top:16px; overflow:auto; padding:1rem; background:#fff; border:1px solid #d5e0d8; border-radius:10px; color:#1b2b25 !important; line-height:1.7; white-space:pre-wrap; overflow-wrap:anywhere; }
    .output-box.empty { color:#818d86 !important; }
    .word-count { color:#718078 !important; font-size:.82rem; text-align:right; margin-top:-.55rem; }
    .result-meta { color:#607069 !important; font-size:.84rem; padding-top:.35rem; }
    div[data-testid="stVerticalBlockBorderWrapper"] { background:#fff; border:1px solid var(--line); border-radius:14px; }
    @media(max-width:760px) {
      [data-testid="stMainBlockContainer"] { padding:1rem .8rem 2rem; }
      .brand-note { display:none; }
      .output-box { height:13rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="brand-row"><div class="brand">✦ word<span>shift</span></div><div class="brand-note">A simple slang and formal language converter</div></div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="tool-title">Text converter</div>', unsafe_allow_html=True)

mode = st.radio(
    "Conversion direction",
    ["Slang → Formal", "Formal → Slang"],
    horizontal=True,
    key="conversion_mode",
)
is_slang_to_formal = mode == "Slang → Formal"
sample = (
    "Hey bestie, that fit is fire! I'm gonna call u later lol"
    if is_slang_to_formal
    else "Hello, my best friend. I will call you later."
)
placeholder = (
    "Type or paste your casual text here…"
    if is_slang_to_formal
    else "Type or paste your formal text here…"
)

sample_spacer, sample_action = st.columns([4, 1])
with sample_action:
    if st.button("✦  Try sample text", key="sample_button", use_container_width=True):
        st.session_state["message_input"] = sample

left, right = st.columns(2, gap="large")
with left:
    st.markdown(
        '<div class="panel-heading input-heading"><span class="panel-title">Your text</span><span class="panel-subtitle">Input</span></div>',
        unsafe_allow_html=True,
    )

    with st.form("converter_form"):
        text = st.text_area(
            "Your text",
            height=285,
            placeholder=placeholder,
            key="message_input",
            label_visibility="collapsed",
        )
        st.markdown(f'<div class="word-count">{len(text.split())} words · {len(text)} characters</div>', unsafe_allow_html=True)
        submitted = st.form_submit_button("Convert text  →", type="primary", use_container_width=True)

if submitted:
    if not text.strip():
        st.session_state.pop("conversion_result", None)
        st.warning("Enter some text to convert.")
    else:
        result = slang_to_formal(text) if is_slang_to_formal else formal_to_slang(text)
        # Some recognized filler terms (such as "lol") intentionally convert
        # to an empty string, so an empty result can still be a valid conversion.
        converted = result.casefold() != normalize_text(text).casefold()
        st.session_state["conversion_result"] = {
            "input": text,
            "result": result if converted else "Couldn't find a matching term to convert. Try different wording.",
            "mode": mode,
            "style": detect_style(text),
            "converted": converted,
        }

conversion = st.session_state.get("conversion_result")
with right:
    st.markdown(
        '<div class="panel-heading"><span class="panel-title">Rewritten text</span><span class="panel-subtitle">Output</span></div>',
        unsafe_allow_html=True,
    )
    if conversion:
        output_class = "output-box" if conversion["converted"] else "output-box empty"
        st.markdown(
            f'<div class="{output_class}">{escape(conversion["result"])}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="result-meta">{conversion["style"].capitalize()} tone detected · {conversion["mode"]}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="output-box empty">Your converted text will appear here.</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="result-meta">Output will appear after conversion.</div>', unsafe_allow_html=True)
