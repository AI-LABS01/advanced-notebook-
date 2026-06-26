import streamlit as st
import requests

# ----------------------------------------------------------------------------
# 1. Page setup
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Research Index — RAG Assistant",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

BACKEND_URL = "https://advanced-notebook-1.onrender.com"

# ----------------------------------------------------------------------------
# 2. Theme — full dark
# ----------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg: #0E1013;
    --bg-raised: #1B1E24;
    --bg-raised-2: #23262E;
    --line: #343842;
    --text: #EDEEF0;
    --text-dim: #A7ACB6;
    --copper: #D98A42;
    --copper-soft: #F0B97D;
    --good: #4CAE7E;
    --good-bg: #16261F;
    --bad: #E0664A;
    --bad-bg: #2A1815;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp, .stApp p, .stApp span, .stApp label, .stApp div {
    color: var(--text);
}

.stApp {
    background-color: var(--bg);
}

.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5 {
    color: var(--text) !important;
}

header[data-testid="stHeader"] {
    background-color: var(--bg);
}
.block-container {
    background-color: var(--bg);
}

/* ---------- Top masthead ---------- */
.masthead {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    border-bottom: 2px solid var(--line);
    padding-bottom: 0.65rem;
    margin-bottom: 1.6rem;
}
.masthead-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.55rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    color: var(--text) !important;
    margin: 0;
}
.masthead-title span { color: var(--copper) !important; }
.masthead-sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    color: var(--text-dim) !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background-color: var(--bg-raised);
    border-right: 1px solid var(--line);
}
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div {
    color: var(--text) !important;
}
section[data-testid="stSidebar"] h2 {
    font-family: 'IBM Plex Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    font-size: 0.85rem;
    color: var(--copper-soft) !important;
}
.sidebar-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: var(--text-dim) !important;
    letter-spacing: 0.05em;
    margin-bottom: 0.25rem;
    font-weight: 600;
}

section[data-testid="stSidebar"] .stTextInput input {
    background-color: var(--bg-raised-2) !important;
    border: 1px solid var(--line) !important;
    color: var(--text) !important;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.88rem;
    caret-color: var(--text);
}
section[data-testid="stSidebar"] .stTextInput input::placeholder {
    color: var(--text-dim) !important;
}
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
    background-color: var(--bg-raised-2) !important;
    border: 1px solid var(--line) !important;
    color: var(--text) !important;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.88rem;
}
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] svg {
    fill: var(--text) !important;
}
div[data-baseweb="popover"] {
    background-color: var(--bg-raised-2) !important;
}
div[data-baseweb="popover"] li {
    color: var(--text) !important;
    background-color: var(--bg-raised-2) !important;
}
div[data-baseweb="popover"] li:hover {
    background-color: var(--bg-raised) !important;
}

section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] {
    margin-top: 0.5rem;
}
section[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMin"],
section[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMax"] {
    color: var(--text-dim) !important;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
}
section[data-testid="stSidebar"] .stSlider div[data-testid="stThumbValue"] {
    color: #15171C !important;
    background-color: var(--copper-soft) !important;
    font-weight: 600;
}
section[data-testid="stSidebar"] .stSlider div[role="slider"] {
    background-color: var(--copper) !important;
}

section[data-testid="stSidebar"] hr {
    border-color: var(--line);
}
div[data-testid="stExpander"] {
    background-color: var(--bg-raised-2);
    border: 1px solid var(--line);
    border-radius: 4px;
}
div[data-testid="stExpander"] summary {
    color: var(--text) !important;
}

/* Sidebar primary button — copper signal, dark text for contrast on it */
section[data-testid="stSidebar"] .stButton button {
    background-color: var(--copper);
    border: none;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    font-size: 0.8rem;
    border-radius: 3px;
    padding: 0.6rem 1rem;
    transition: background-color 0.15s ease;
}
section[data-testid="stSidebar"] .stButton button,
section[data-testid="stSidebar"] .stButton button p,
section[data-testid="stSidebar"] .stButton button span {
    color: #15171C !important;
}
section[data-testid="stSidebar"] .stButton button:hover {
    background-color: var(--copper-soft);
}

/* Main canvas buttons (e.g. "Clear conversation") */
.stApp .stButton button {
    background-color: var(--bg-raised-2);
    border: 1px solid var(--line);
    color: var(--text) !important;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    border-radius: 3px;
}
.stApp .stButton button:hover {
    border-color: var(--copper);
    color: var(--copper-soft) !important;
}

/* ---------- Pipeline strip (signature element) ---------- */
.pipeline {
    display: flex;
    align-items: center;
    gap: 0;
    margin: 0.9rem 0 0.3rem 0;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.05em;
}
.pipeline-stage {
    flex: 1;
    text-align: center;
    padding: 0.45rem 0.2rem;
    border: 1px solid var(--line);
    border-right: none;
    color: var(--text-dim) !important;
    background-color: var(--bg-raised-2);
    text-transform: uppercase;
}
.pipeline-stage:last-child { border-right: 1px solid var(--line); }
.pipeline-stage.done {
    color: #FFFFFF !important;
    background-color: #2F6B4C;
    border-color: #2F6B4C;
}
.pipeline-stage.active {
    color: #15171C !important;
    background-color: var(--copper);
    border-color: var(--copper);
    font-weight: 700;
}
.pipeline-stage.error {
    color: #FFFFFF !important;
    background-color: #A23E27;
    border-color: #A23E27;
}

/* ---------- Main canvas cards ---------- */
.panel {
    background-color: var(--bg-raised);
    border: 1px solid var(--line);
    border-radius: 6px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 1rem;
    color: var(--text) !important;
}
.panel p, .panel span {
    color: var(--text) !important;
}
.kicker {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--copper-soft) !important;
    margin-bottom: 0.3rem;
    display: block;
}

/* ---------- Status line ---------- */
.status-line {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    font-weight: 600;
    padding: 0.6rem 0.85rem;
    border-radius: 4px;
    margin-top: 0.6rem;
    border: 1px solid transparent;
}
.status-ok {
    background-color: var(--good-bg);
    color: var(--good) !important;
    border-color: #2C5240;
}
.status-err {
    background-color: var(--bad-bg);
    color: var(--bad) !important;
    border-color: #5C3026;
}

/* ---------- Chat input box ---------- */
div[data-testid="stChatInput"] {
    background-color: var(--bg-raised) !important;
}
div[data-testid="stChatInput"] textarea {
    color: var(--text) !important;
    background-color: var(--bg-raised) !important;
    border: 1px solid var(--line) !important;
}
div[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-dim) !important;
}

/* ---------- Chat ---------- */
div[data-testid="stChatMessage"] {
    background-color: var(--bg-raised);
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 0.2rem 0.4rem;
}
div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] span {
    color: var(--text) !important;
}
.chat-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 0.15rem;
    display: block;
}
.chat-tag.user { color: var(--text) !important; }
.chat-tag.assistant { color: var(--copper-soft) !important; }

/* Divider rule */
.hairline {
    border: none;
    border-top: 1px solid var(--line);
    margin: 1.4rem 0;
}

/* Empty state */
.empty-state {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    color: var(--text-dim) !important;
    text-align: center;
    padding: 2.2rem 1rem;
    border: 1px dashed var(--line);
    border-radius: 8px;
    background-color: var(--bg-raised);
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# 3. Masthead
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="masthead">
        <p class="masthead-title">## RESEARCH<span>INDEX</span></p>
        <p class="masthead-sub">Retrieval-Augmented Knowledge Base</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# 4. Sidebar — Ingestion Control Panel
# ----------------------------------------------------------------------------
if "last_stage" not in st.session_state:
    st.session_state.last_stage = None

with st.sidebar:
    st.markdown("## Ingestion Panel")
    st.markdown(
        '<p style="color:#A7ACB6 !important; font-size:0.85rem; margin-top:-0.6rem;">'
        "Add a source to the vector store.</p>",
        unsafe_allow_html=True,
    )
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown('<p class="sidebar-eyebrow">SOURCE TYPE</p>', unsafe_allow_html=True)
    data_type = st.selectbox(
        " ",
        options=["url", "pdf", "image"],
        format_func=lambda x: x.upper(),
        label_visibility="collapsed",
    )

    st.markdown('<p class="sidebar-eyebrow">SOURCE PATH</p>', unsafe_allow_html=True)
    source_path = st.text_input(
        " ",
        placeholder="https://example.com or /path/to/doc.pdf",
        label_visibility="collapsed",
    )

    with st.expander("Advanced — text splitting"):
        chunk_size = st.slider("Chunk size", min_value=100, max_value=2000, value=1000, step=100)
        chunk_overlap = st.slider("Chunk overlap", min_value=0, max_value=200, value=10, step=10)

    st.markdown("<br>", unsafe_allow_html=True)
    run_ingest = st.button("Sync to vector store →", use_container_width=True)

    stages = ["source", "parse", "chunk", "embed", "store"]

    def render_pipeline(active_idx=None, done=False, error_idx=None):
        cells = []
        for i, name in enumerate(stages):
            cls = ""
            if error_idx is not None and i == error_idx:
                cls = "error"
            elif done:
                cls = "done"
            elif active_idx is not None and i <= active_idx:
                cls = "active" if i == active_idx else "done"
            cells.append(f'<div class="pipeline-stage {cls}">{name}</div>')
        return f'<div class="pipeline">{"".join(cells)}</div>'

    pipeline_slot = st.empty()
    pipeline_slot.markdown(render_pipeline(), unsafe_allow_html=True)

    status_slot = st.empty()

    if run_ingest:
        if not source_path.strip():
            status_slot.markdown(
                '<div class="status-line status-err">✕ Provide a source path before syncing.</div>',
                unsafe_allow_html=True,
            )
        else:
            import time

            pipeline_slot.markdown(render_pipeline(active_idx=0), unsafe_allow_html=True)
            time.sleep(0.15)
            pipeline_slot.markdown(render_pipeline(active_idx=1), unsafe_allow_html=True)

            try:
                payload = {
                    "data_type": data_type,
                    "source_path": source_path.strip(),
                    "chunk_size": chunk_size,
                    "chunk_overlap": chunk_overlap,
                }
                pipeline_slot.markdown(render_pipeline(active_idx=2), unsafe_allow_html=True)
                response = requests.post(f"{BACKEND_URL}/ingest", json=payload)
                pipeline_slot.markdown(render_pipeline(active_idx=3), unsafe_allow_html=True)

                if response.status_code == 200:
                    res_json = response.json()
                    pipeline_slot.markdown(render_pipeline(done=True), unsafe_allow_html=True)
                    status_slot.markdown(
                        f'<div class="status-line status-ok">✓ Indexed — '
                        f'{res_json.get("chunks_created")} chunks written to /data</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    detail = response.json().get("detail", "Unknown error")
                    pipeline_slot.markdown(render_pipeline(error_idx=3), unsafe_allow_html=True)
                    status_slot.markdown(
                        f'<div class="status-line status-err">✕ Ingestion failed — {detail}</div>',
                        unsafe_allow_html=True,
                    )
            except Exception as e:
                pipeline_slot.markdown(render_pipeline(error_idx=0), unsafe_allow_html=True)
                status_slot.markdown(
                    f'<div class="status-line status-err">✕ Backend unreachable — {e}</div>',
                    unsafe_allow_html=True,
                )

# ----------------------------------------------------------------------------
# 5. Main Canvas — Chat Interface Logic
# ----------------------------------------------------------------------------
left, right = st.columns([0.72, 0.28], gap="large")

with left:
    st.markdown('<span class="kicker">Knowledge Base</span>', unsafe_allow_html=True)
    st.markdown("#### Ask your documents")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display empty state if no log exists
    if not st.session_state.chat_history:
        st.markdown(
            '<div class="empty-state">— no messages yet —<br>'
            "sync a source on the left, then ask a question below</div>",
            unsafe_allow_html=True,
        )
    else:
        # Loop through active session state array
        for message in st.session_state.chat_history:
            role = message["role"]
            with st.chat_message(role):
                tag = "YOU" if role == "user" else "ASSISTANT"
                st.markdown(f'<span class="chat-tag {role}">{tag}</span>', unsafe_allow_html=True)
                st.write(message["content"])

    user_query = st.chat_input("Ask a question about your uploaded documents…")

    if user_query:
        # Append User Input and immediately sync UI state
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        st.rerun()

# ----------------------------------------------------------------------------
# 6. Live RAG API Verification Loop
# ----------------------------------------------------------------------------
if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "user":
    last_query = st.session_state.chat_history[-1]["content"]

    with left:
        with st.chat_message("assistant"):
            st.markdown('<span class="chat-tag assistant">ASSISTANT</span>', unsafe_allow_html=True)
            with st.spinner("Searching index…"):
                try:
                    query_payload = {"question": last_query}
                    response = requests.post(f"{BACKEND_URL}/query", json=query_payload, timeout=30)

                    if response.status_code == 200:
                        data = response.json()
                        answer = data.get("answer", "No answer string parsed.")
                        sources = data.get("sources", [])

                        # Format source attribution if valid matching objects exist
                        if sources:
                            answer += f"\n\n**Sources:** {', '.join(sources)}"

                        st.session_state.chat_history.append({"role": "assistant", "content": answer})
                        st.rerun()
                    else:
                        error_msg = response.json().get("detail", "Unknown server exception handler issue.")
                        st.markdown(
                            f'<div class="status-line status-err">✕ {error_msg}</div>',
                            unsafe_allow_html=True,
                        )
                except Exception as e:
                    st.markdown(
                        f'<div class="status-line status-err">✕ Could not reach backend server connection — {e}</div>',
                        unsafe_allow_html=True,
                    )

# ----------------------------------------------------------------------------
# 7. Sidebar Session Panels — At a glance
# ----------------------------------------------------------------------------
with right:
    st.markdown('<span class="kicker">Session</span>', unsafe_allow_html=True)
    st.markdown("#### At a glance")
    st.markdown(
        f"""
        <div class="panel">
            <p class="sidebar-eyebrow" style="color:#A7ACB6 !important;">MESSAGES</p>
            <p style="font-family:'IBM Plex Mono'; font-size:1.6rem; margin:0; color:#EDEEF0 !important; font-weight:600;">
                {len(st.session_state.get("chat_history", []))}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="panel">
            <p class="sidebar-eyebrow" style="color:#A7ACB6 !important;">BACKEND</p>
            <p style="font-family:'IBM Plex Mono'; font-size:0.85rem; margin:0; color:#EDEEF0 !important; font-weight:600;">
                {BACKEND_URL.replace("https://", "")}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
