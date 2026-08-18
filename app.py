import html
import re

import requests
import streamlit as st

from client import collection

API_URL = "http://localhost:8000/ask"
CITATION_PATTERN = re.compile(r"\[(\d+)\]")

st.set_page_config(page_title="NovaTech Reader", page_icon="📄", layout="centered")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,420;9..144,560&family=Newsreader:ital,wght@0,420;0,560;1,420&family=Archivo:wght@450;560;650&display=swap');

    :root {
      --paper: #EDF1EE;
      --panel: #E3E9E4;
      --ink: #161B1A;
      --ink-soft: #4E5952;
      --pine: #2B5C4E;
      --gold: #8C6423;
      --rule: #CDD6CE;
    }

    .stApp { background-color: var(--paper); }
    section[data-testid="stSidebar"] { background-color: var(--panel); border-right: 1px solid var(--rule); }

    .nt-title {
      font-family: 'Fraunces', serif;
      font-size: 2rem;
      font-weight: 560;
      letter-spacing: -0.01em;
      color: var(--ink);
      margin: 0 0 0.35rem 0;
    }
    .nt-subtitle {
      font-family: 'Archivo', sans-serif;
      font-size: 0.95rem;
      color: var(--ink-soft);
      max-width: 60ch;
      margin: 0 0 2rem 0;
    }
    .nt-section-heading {
      font-family: 'Fraunces', serif;
      font-size: 1.1rem;
      font-weight: 560;
      color: var(--ink);
      margin: 0 0 0.7rem 0;
    }
    .nt-question {
      font-family: 'Archivo', sans-serif;
      font-size: 0.9rem;
      color: var(--ink-soft);
      max-width: 68ch;
      margin: 2rem 0 0.6rem 0;
    }
    .nt-answer {
      font-family: 'Newsreader', serif;
      font-size: 1.15rem;
      line-height: 1.65;
      color: var(--ink);
      max-width: 68ch;
      margin-bottom: 0.9rem;
    }
    .nt-mark {
      font-family: 'Archivo', sans-serif;
      font-size: 0.7em;
      font-weight: 650;
      color: var(--pine);
      vertical-align: super;
      margin-left: 1px;
    }
    .nt-caveat {
      font-family: 'Archivo', sans-serif;
      font-style: italic;
      font-size: 0.88rem;
      color: var(--ink-soft);
      max-width: 68ch;
      margin: 0 0 1rem 0;
    }
    .nt-abstain {
      font-family: 'Newsreader', serif;
      font-style: italic;
      font-size: 1.05rem;
      color: var(--ink-soft);
      max-width: 68ch;
    }
    .nt-sources { max-width: 68ch; margin: 0.4rem 0 0.8rem 0; }
    .nt-source {
      display: flex;
      flex-direction: column;
      gap: 0.15rem;
      padding: 0.7rem 0;
      border-top: 1px solid var(--rule);
    }
    .nt-source-ref {
      font-family: 'Archivo', sans-serif;
      font-size: 0.82rem;
      font-weight: 560;
      color: var(--pine);
    }
    .nt-source-quote {
      font-family: 'Newsreader', serif;
      font-style: italic;
      font-size: 0.95rem;
      color: var(--ink-soft);
      line-height: 1.55;
    }
    .nt-confidence {
      font-family: 'Archivo', sans-serif;
      font-size: 0.78rem;
      color: var(--ink-soft);
      margin: 0.3rem 0 1.6rem 0;
    }
    .nt-confidence-high { color: var(--pine); }
    .nt-confidence-medium { color: var(--gold); }
    .nt-confidence-low { color: var(--ink-soft); }
    .nt-docs-list {
      font-family: 'Archivo', sans-serif;
      font-size: 0.85rem;
      color: var(--ink-soft);
      line-height: 1.9;
    }
    [data-testid="stChatInput"] textarea {
      font-family: 'Newsreader', serif !important;
      border-radius: 10px !important;
      border: 1px solid var(--rule) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def get_loaded_documents():
    data = collection.get(include=["metadatas"])
    counts = {}
    for meta in data["metadatas"]:
        name = meta.get("source", "unknown").split("/")[-1]
        counts[name] = counts.get(name, 0) + 1
    return sorted(counts.items())


def style_citation_markers(escaped_text):
    return CITATION_PATTERN.sub(r'<sup class="nt-mark">\1</sup>', escaped_text)


def citation_block_html(citations):
    rows = []
    for i, c in enumerate(citations, start=1):
        doc_name = html.escape(c["document"].split("/")[-1])
        page = html.escape(str(c["page"]))
        quote = html.escape(c["quote"])
        rows.append(
            '<div class="nt-source">'
            f'<span class="nt-source-ref">{i}. {doc_name} — page {page}</span>'
            f'<span class="nt-source-quote">“{quote}”</span>'
            "</div>"
        )
    return f'<div class="nt-sources">{"".join(rows)}</div>'


def render_turn(question, answer):
    st.markdown(
        f'<div class="nt-question">You asked — {html.escape(question)}</div>',
        unsafe_allow_html=True,
    )

    if answer.get("abstained"):
        st.markdown(
            '<p class="nt-abstain">The documents don’t cover this directly — no answer given.</p>',
            unsafe_allow_html=True,
        )
        return

    answer_html = style_citation_markers(html.escape(answer["answer"]))
    st.markdown(f'<div class="nt-answer">{answer_html}</div>', unsafe_allow_html=True)

    if answer.get("caveats"):
        caveat_text = html.escape(" ".join(answer["caveats"]))
        st.markdown(f'<p class="nt-caveat">{caveat_text}</p>', unsafe_allow_html=True)

    citations = answer.get("citations") or []
    if citations:
        st.markdown(citation_block_html(citations), unsafe_allow_html=True)

    confidence = answer.get("confidence", "")
    st.markdown(
        f'<p class="nt-confidence nt-confidence-{confidence}">Confidence — {confidence}</p>',
        unsafe_allow_html=True,
    )


st.markdown('<div class="nt-title">NovaTech Reader</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="nt-subtitle">Ask about leave, conduct, IT, and workplace policy. '
    "Every answer names the document and page it came from.</div>",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown('<div class="nt-section-heading">Documents loaded</div>', unsafe_allow_html=True)
    rows = "".join(f"{name} — {count} chunks<br>" for name, count in get_loaded_documents())
    st.markdown(f'<div class="nt-docs-list">{rows}</div>', unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

for past_question, past_answer in st.session_state.history:
    render_turn(past_question, past_answer)

question = st.chat_input("Ask a question")
if question:
    answer = None
    with st.spinner("Reading the documents…"):
        try:
            response = requests.post(API_URL, json={"text": question}, timeout=60)
            response.raise_for_status()
            answer = response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Couldn't reach the API — is `uvicorn api:app` running? ({e})")

    if answer is not None:
        st.session_state.history.append((question, answer))
        st.rerun()
