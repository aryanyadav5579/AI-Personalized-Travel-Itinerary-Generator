"""
=============================================================
app.py  —  Main Entry Point
=============================================================
Day 3  |  Part 3A

Sub-parts:
  3A-i   Streamlit page configuration
  3A-ii  Session state initialization
  3A-iii Custom CSS
  3A-iv  Sidebar navigation router
  3A-v   API key warning banner
=============================================================
"""

import streamlit as st
from datetime import date

# ── Page config (must be the VERY FIRST Streamlit call) ───────
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================
# SUB-PART 3A-iii  |  CUSTOM CSS
# =============================================================
def _inject_css():
    st.markdown("""
    <style>
    /* ── Global font & background ─────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Hide default Streamlit chrome ────────────────────── */
    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }
    header    { visibility: hidden; }

    /* ── Sidebar styling ──────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        border-right: 1px solid #2c5364;
    }
    section[data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }
    section[data-testid="stSidebar"] .stRadio label {
        font-size: 0.95rem;
        padding: 4px 0;
        cursor: pointer;
    }

    /* ── Card component ───────────────────────────────────── */
    .ai-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border: 1px solid #f0f0f0;
        margin-bottom: 1rem;
        transition: box-shadow 0.2s ease;
    }
    .ai-card:hover {
        box-shadow: 0 4px 20px rgba(0,0,0,0.13);
    }

    /* ── Hero banner ──────────────────────────────────────── */
    .hero-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 3rem 2.5rem;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .hero-banner h1 {
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: white !important;
    }
    .hero-banner p {
        font-size: 1.15rem;
        opacity: 0.92;
        color: white !important;
    }

    /* ── Feature card ─────────────────────────────────────── */
    .feature-card {
        background: #f8f9ff;
        border-radius: 12px;
        padding: 1.2rem;
        border-left: 4px solid #667eea;
        margin-bottom: 0.8rem;
    }
    .feature-card h4 {
        margin: 0 0 0.3rem 0;
        color: #2d3748;
        font-size: 1rem;
        font-weight: 600;
    }
    .feature-card p {
        margin: 0;
        color: #718096;
        font-size: 0.88rem;
    }

    /* ── Day header ───────────────────────────────────────── */
    .day-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.6rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1.05rem;
        margin-bottom: 0.5rem;
    }

    /* ── Slot card (morning/afternoon/evening) ─────────────── */
    .slot-card {
        background: #fafafa;
        border-radius: 8px;
        padding: 0.9rem 1rem;
        border: 1px solid #e8e8e8;
        height: 100%;
    }
    .slot-title {
        font-weight: 600;
        font-size: 0.9rem;
        color: #4a5568;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .slot-card ul {
        margin: 0;
        padding-left: 1.2rem;
        font-size: 0.88rem;
        color: #2d3748;
    }
    .slot-card li {
        margin-bottom: 0.2rem;
    }

    /* ── Budget status chips ──────────────────────────────── */
    .budget-ok    { background:#e6ffed; color:#1a7431; border-radius:6px; padding:4px 10px; font-weight:600; }
    .budget-tight { background:#fff8e1; color:#b45309; border-radius:6px; padding:4px 10px; font-weight:600; }
    .budget-over  { background:#ffe4e6; color:#be123c; border-radius:6px; padding:4px 10px; font-weight:600; }

    /* ── Destination chip ─────────────────────────────────── */
    .dest-chip {
        display: inline-block;
        background: #eef2ff;
        border: 1px solid #c7d2fe;
        color: #4338ca;
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.85rem;
        margin: 3px;
        cursor: pointer;
        font-weight: 500;
    }

    /* ── Prompt code block ────────────────────────────────── */
    .prompt-box {
        background: #1e1e2e;
        color: #cdd6f4;
        border-radius: 10px;
        padding: 1.2rem;
        font-family: 'Courier New', monospace;
        font-size: 0.82rem;
        line-height: 1.6;
        overflow-x: auto;
        white-space: pre-wrap;
        word-break: break-word;
    }

    /* ── Step badge ───────────────────────────────────────── */
    .step-badge {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-radius: 50%;
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.9rem;
        margin: 0 auto 0.5rem auto;
    }

    /* ── Metric card override ─────────────────────────────── */
    [data-testid="metric-container"] {
        background: #f8f9ff;
        border-radius: 10px;
        padding: 0.8rem;
        border: 1px solid #e2e8f0;
    }

    /* ── Primary button ───────────────────────────────────── */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        transition: opacity 0.2s;
    }
    .stButton > button[kind="primary"]:hover {
        opacity: 0.9;
    }

    /* ── Chat messages ────────────────────────────────────── */
    [data-testid="stChatMessage"] {
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }

    /* ── Info banner ──────────────────────────────────────── */
    .info-banner {
        background: linear-gradient(90deg, #e0f2fe, #f0fdf4);
        border-left: 4px solid #0ea5e9;
        border-radius: 0 8px 8px 0;
        padding: 0.8rem 1rem;
        margin-bottom: 1rem;
        font-size: 0.9rem;
        color: #0c4a6e;
    }
    </style>
    """, unsafe_allow_html=True)


# =============================================================
# SUB-PART 3A-ii  |  SESSION STATE INITIALIZATION
# =============================================================
def _init_session_state():
    """Initialize all session state keys with default values."""
    defaults = {
        "current_page":   "Home",
        "itinerary":      None,       # generated itinerary dict
        "user_inputs":    {},         # form inputs saved after submission
        "chat_history":   [],         # list of {"role", "content"} dicts
        "is_generating":  False,      # spinner flag
        "last_prompt":    "",         # last prompt sent (for PE page display)
        "budget_status":  None,       # budget comparison dict
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# =============================================================
# SUB-PART 3A-v  |  API KEY WARNING BANNER
# =============================================================
def _show_api_warning():
    """Show a warning banner at top of page if API key is missing."""
    from services.llm_service import is_api_configured
    if not is_api_configured():
        st.warning(
            "**API Key Missing** — Add your Gemini API key to the `.env` file to use AI features.  \n"
            "Get a free key at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)  \n"
            "Then copy `.env.example` → `.env` and paste your key.",
            icon="⚠️",
        )


# =============================================================
# SUB-PART 3A-iv  |  SIDEBAR NAVIGATION ROUTER
# =============================================================
def _render_sidebar() -> str:
    """Render the sidebar and return the selected page name."""
    with st.sidebar:
        # Logo / title
        st.markdown("""
        <div style="text-align:center; padding: 1rem 0 1.5rem 0;">
            <div style="font-size:2.5rem;">✈️</div>
            <div style="font-size:1.1rem; font-weight:700; color:#fff; margin-top:0.3rem;">
                AI Travel Planner
            </div>
            <div style="font-size:0.75rem; color:#94a3b8; margin-top:0.2rem;">
                Powered by Gemini AI
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        pages = [
            "🏠  Home",
            "🗺️  Plan Trip",
            "📅  My Itinerary",
            "🤖  AI Assistant",
            "💰  Budget",
            "🎓  Prompt Engineering",
            "ℹ️  About Project",
        ]

        selected = st.radio(
            "Navigate",
            pages,
            index=pages.index(
                next(
                    (p for p in pages if st.session_state.current_page in p),
                    pages[0],
                )
            ),
            label_visibility="collapsed",
        )

        # Show itinerary status in sidebar
        st.divider()
        if st.session_state.itinerary:
            dest = st.session_state.user_inputs.get("destination", "")
            days = st.session_state.user_inputs.get("num_days", 0)
            st.markdown(
                f"""<div style="font-size:0.78rem; color:#94a3b8; text-align:center;">
                    ✅ Itinerary ready<br>
                    <b style="color:#e0e0e0">{dest} · {days} days</b>
                </div>""",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div style="font-size:0.78rem; color:#64748b; text-align:center;">'
                "No itinerary yet<br>Go to Plan Trip to start"
                "</div>",
                unsafe_allow_html=True,
            )

        st.divider()
        st.markdown(
            '<div style="font-size:0.72rem; color:#475569; text-align:center;">'
            "Gen AI &amp; Prompt Engineering<br>College Project · 2026"
            "</div>",
            unsafe_allow_html=True,
        )

    # Extract clean page name (strip emoji + spaces)
    clean = selected.split("  ", 1)[-1].strip()
    return clean


# =============================================================
# SUB-PART 3A-i  |  PAGE IMPORTS & ROUTING
# =============================================================
def main():
    _inject_css()
    _init_session_state()

    page = _render_sidebar()

    # Sync sidebar selection to session state
    page_map = {
        "Home":               "Home",
        "Plan Trip":          "Plan Trip",
        "My Itinerary":       "My Itinerary",
        "AI Assistant":       "AI Assistant",
        "Budget":             "Budget",
        "Prompt Engineering": "Prompt Engineering",
        "About Project":      "About Project",
    }
    st.session_state.current_page = page_map.get(page, "Home")

    # Show API key warning on every page
    _show_api_warning()

    # ── Route to the selected page ────────────────────────────
    if page == "Home":
        from views.home import render
        render()

    elif page == "Plan Trip":
        from views.plan_trip import render
        render()

    elif page == "My Itinerary":
        from views.itinerary import render
        render()

    elif page == "AI Assistant":
        from views.assistant import render
        render()

    elif page == "Budget":
        from views.budget import render
        render()

    elif page == "Prompt Engineering":
        from views.prompt_engineering import render
        render()

    elif page == "About Project":
        from views.about import render
        render()


if __name__ == "__main__":
    main()
