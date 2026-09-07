"""
=============================================================
Prompt Engineering Education Page
=============================================================
Day 4  |  Part 4C

The most academically important page for the college viva.
Shows exactly HOW prompt engineering works in this project.

Sub-parts:
  4C-i    Page header + intro explanation
  4C-ii   7 technique cards (accordion-style)
  4C-iii  3-level prompt comparison (Basic / Standard / Advanced)
  4C-iv   Live prompt inspector — shows the actual prompt generated
           from the user's last trip form submission
  4C-v    Prompt quality metrics bar chart
=============================================================
"""

import streamlit as st
import plotly.graph_objects as go

from services.prompt_service import (
    get_technique_examples,
    get_prompt_stats,
    compare_prompts,
    get_basic_prompt,
    get_standard_prompt,
    get_advanced_prompt,
)


# Colour palette for technique cards
_TECHNIQUE_COLORS = {
    "Role Prompting":               ("#667eea", "#eef2ff"),
    "Context Injection":            ("#e67e22", "#fef9e7"),
    "Few-Shot Prompting":           ("#27ae60", "#eafaf1"),
    "Constraint-Based Prompting":   ("#e74c3c", "#fdf2f2"),
    "Structured Output Prompting":  ("#8e44ad", "#f5eef8"),
    "Zero-Shot Prompting":          ("#16a085", "#e8f8f5"),
    "Iterative Prompt Refinement":  ("#2980b9", "#eaf4fb"),
}


def render():
    """Render the Prompt Engineering education page."""

    # ==========================================================
    # SUB-PART 4C-i  |  PAGE HEADER
    # ==========================================================
    st.markdown("""
    <div class="hero-banner" style="padding:2rem;">
        <div style="font-size:2.5rem; margin-bottom:0.4rem;">🧠</div>
        <h1 style="font-size:2rem; margin-bottom:0.4rem;">Prompt Engineering</h1>
        <p style="font-size:1rem;">
            The science of crafting instructions that get the best results from AI models.<br>
            This page shows every technique used in this application — with real examples.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-banner">
        <strong>What is Prompt Engineering?</strong><br>
        Prompt Engineering is the practice of carefully designing input text (prompts) to guide
        AI language models towards producing accurate, structured, and relevant outputs.
        Instead of hoping the AI does the right thing, we <em>engineer</em> the instructions
        so it reliably does exactly what we need.
        This app uses <strong>7 distinct techniques</strong> across 6 different prompt files.
    </div>
    """, unsafe_allow_html=True)

    # ==========================================================
    # SUB-PART 4C-ii  |  7 TECHNIQUE CARDS
    # ==========================================================
    st.markdown("### 📚 Techniques Used in This Project")
    st.markdown("Expand each card to see the technique definition, a real example from this app, and what it improves.")
    st.markdown("<br>", unsafe_allow_html=True)

    techniques = get_technique_examples()

    for tech_name, info in techniques.items():
        border_color, bg_color = _TECHNIQUE_COLORS.get(tech_name, ("#667eea", "#eef2ff"))

        with st.expander(
            f"{info['icon']}  {tech_name}",
            expanded=(tech_name == "Role Prompting"),   # first one open by default
        ):
            col_def, col_ex = st.columns([1, 1], gap="large")

            with col_def:
                st.markdown(f"""
                <div style="
                    border-left: 4px solid {border_color};
                    padding: 0.8rem 1rem;
                    background: {bg_color};
                    border-radius: 0 8px 8px 0;
                    margin-bottom: 0.8rem;
                ">
                    <div style="font-size:0.8rem; font-weight:700; color:{border_color};
                                text-transform:uppercase; letter-spacing:0.05em; margin-bottom:0.4rem;">
                        Definition
                    </div>
                    <div style="font-size:0.88rem; color:#2d3748; line-height:1.65;">
                        {info['definition']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style="font-size:0.8rem; margin-top:0.6rem;">
                    <span style="font-weight:600; color:#4a5568;">📁 Used in:</span><br>
                    <code style="font-size:0.78rem; color:#667eea; background:#f0f4ff;
                                 padding:2px 6px; border-radius:4px;">
                        {info['where_used'].replace(chr(10), '<br>')}
                    </code>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style="margin-top:0.7rem; background:#f0fdf4; border-radius:6px;
                            padding:0.5rem 0.8rem; font-size:0.83rem; color:#166534;">
                    <strong>✅ Benefit:</strong> {info['benefit']}
                </div>
                """, unsafe_allow_html=True)

            with col_ex:
                st.markdown(
                    f"<div style='font-size:0.8rem; font-weight:700; color:#4a5568; "
                    f"text-transform:uppercase; letter-spacing:0.05em; margin-bottom:0.4rem;'>"
                    f"Real Example from This App</div>",
                    unsafe_allow_html=True,
                )
                # Show example in dark code block style
                example_escaped = (
                    info["example"]
                    .replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                )
                st.markdown(
                    f'<div class="prompt-box">{example_escaped}</div>',
                    unsafe_allow_html=True,
                )

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================================
    # SUB-PART 4C-iii  |  3-LEVEL PROMPT COMPARISON
    # ==========================================================
    st.markdown("### 🔍 Prompt Quality Comparison")
    st.markdown(
        "The same destination — **3 different prompt quality levels**. "
        "See how much more detail the Advanced prompt gives the AI to work with."
    )

    # Use user's last inputs if available, else a sample
    if st.session_state.get("user_inputs"):
        cmp_inputs = st.session_state.user_inputs
    else:
        cmp_inputs = {
            "destination": "Goa", "num_days": 3, "num_travelers": 2,
            "budget": 15000, "currency": "INR",
            "interests": ["Beaches", "Food", "Culture"],
            "travel_style": "Standard", "accommodation": "3-Star Hotel",
            "transportation": "Mixed (Auto + Metro + Cab)",
            "food_preferences": ["Vegetarian"],
            "special_requirements": "Avoid crowded tourist spots",
            "start_date": "2025-03-10",
        }

    comparison = compare_prompts(cmp_inputs)

    tab_basic, tab_standard, tab_advanced = st.tabs([
        "🔴 Basic Prompt",
        "🟡 Standard Prompt",
        "🟢 Advanced Prompt (Used in This App)",
    ])

    _render_prompt_tab(tab_basic,    comparison["basic"],    "🔴", "#fff5f5", "#e53e3e")
    _render_prompt_tab(tab_standard, comparison["standard"], "🟡", "#fffbea", "#d69e2e")
    _render_prompt_tab(tab_advanced, comparison["advanced"], "🟢", "#f0fff4", "#38a169")

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================================
    # SUB-PART 4C-v  |  PROMPT QUALITY METRICS CHART
    # ==========================================================
    st.markdown("### 📊 Prompt Quality at a Glance")
    st.markdown("Comparing the 3 prompts across key quality dimensions:")

    _render_quality_chart(comparison)

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================================
    # SUB-PART 4C-iv  |  LIVE PROMPT INSPECTOR
    # ==========================================================
    st.markdown("### 🔎 Live Prompt Inspector")

    if st.session_state.get("last_prompt"):
        st.markdown("""
        <div style="
            background:#e8f5e9; border-left:4px solid #4caf50;
            border-radius:0 8px 8px 0; padding:0.7rem 1rem; margin-bottom:1rem;
        ">
            <strong>Your Last Generated Prompt</strong><br>
            <span style="font-size:0.85rem; color:#2e7d32;">
                This is the ACTUAL prompt that was sent to Gemini AI when you generated your itinerary.
            </span>
        </div>
        """, unsafe_allow_html=True)

        last_prompt = st.session_state.last_prompt
        stats = get_prompt_stats(last_prompt)

        # Stats row
        lp_c1, lp_c2, lp_c3, lp_c4 = st.columns(4)
        lp_c1.metric("Characters", f"{stats['characters']:,}")
        lp_c2.metric("Words",      f"{stats['words']:,}")
        lp_c3.metric("Lines",      f"{stats['lines']:,}")
        lp_c4.metric("Techniques", sum([
            stats["has_role"],
            stats["has_schema"],
            stats["has_example"],
            stats["has_constraints"],
        ]))

        st.markdown("<br>", unsafe_allow_html=True)

        # Expandable full prompt view
        with st.expander("📄 View Full Prompt Sent to Gemini", expanded=False):
            prompt_escaped = (
                last_prompt
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )
            st.markdown(
                f'<div class="prompt-box" style="max-height:500px; overflow-y:auto;">'
                f'{prompt_escaped}</div>',
                unsafe_allow_html=True,
            )
    else:
        st.info(
            "**No prompt yet.**  \n"
            "Generate an itinerary from the **Plan Trip** page and come back here — "
            "you'll see the actual prompt sent to Gemini, including all your personalized inputs.",
            icon="ℹ️",
        )
        if st.button("🗺️ Go to Plan Trip", type="primary"):
            st.session_state.current_page = "Plan Trip"
            st.rerun()

    st.divider()

    # Key takeaway box
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea22, #764ba222);
        border: 1px solid #667eea44;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        text-align: center;
    ">
        <div style="font-size:1.3rem; margin-bottom:0.5rem;">🎓</div>
        <div style="font-weight:700; font-size:1rem; color:#2d3748; margin-bottom:0.4rem;">
            Key Takeaway
        </div>
        <div style="font-size:0.88rem; color:#4a5568; line-height:1.7;">
            A Basic prompt gives a vague, generic result.<br>
            An Advanced prompt using Role + Context + Few-Shot + Constraints + Structured Output<br>
            gives a <strong>specific, budget-accurate, diet-respecting, structured, usable travel plan</strong>.
            <br><br>
            <em>That difference is Prompt Engineering.</em>
        </div>
    </div>
    """, unsafe_allow_html=True)


# =============================================================
# INTERNAL HELPERS
# =============================================================

def _render_prompt_tab(tab, data: dict, dot: str, bg: str, color: str):
    """Render one prompt comparison tab."""
    with tab:
        stats = data["stats"]

        # Header
        st.markdown(f"""
        <div style="
            background:{bg}; border-left:4px solid {color};
            border-radius:0 8px 8px 0; padding:0.8rem 1rem; margin-bottom:1rem;
        ">
            <div style="font-weight:700; font-size:1rem; color:{color};">
                {dot} {data['label']}
            </div>
            <div style="font-size:0.85rem; color:#4a5568; margin-top:0.2rem;">
                {data['description']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Stats row
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Characters", f"{stats['characters']:,}")
        s2.metric("Words",      f"{stats['words']:,}")
        s3.metric("Has Role?",  "Yes ✅" if stats["has_role"]        else "No ❌")
        s4.metric("Has Schema?","Yes ✅" if stats["has_schema"]       else "No ❌")

        feat1, feat2 = st.columns(2)
        feat1.metric("Has Example?",     "Yes ✅" if stats["has_example"]     else "No ❌")
        feat2.metric("Has Constraints?", "Yes ✅" if stats["has_constraints"] else "No ❌")

        st.markdown("<br>", unsafe_allow_html=True)

        # Prompt text display
        prompt_escaped = (
            data["prompt"]
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        st.markdown(
            f'<div class="prompt-box" style="max-height:400px; overflow-y:auto;">'
            f'{prompt_escaped}</div>',
            unsafe_allow_html=True,
        )


def _render_quality_chart(comparison: dict):
    """Render a grouped bar chart comparing the 3 prompts across quality metrics."""

    levels   = ["Basic", "Standard", "Advanced"]
    prompts  = [comparison["basic"], comparison["standard"], comparison["advanced"]]

    chars    = [d["stats"]["characters"] for d in prompts]
    has_role = [int(d["stats"]["has_role"])        * 100 for d in prompts]
    has_sch  = [int(d["stats"]["has_schema"])       * 100 for d in prompts]
    has_ex   = [int(d["stats"]["has_example"])      * 100 for d in prompts]
    has_con  = [int(d["stats"]["has_constraints"])  * 100 for d in prompts]

    fig = go.Figure()

    # Normalize characters for visual comparison (max = 100%)
    max_chars = max(chars) if max(chars) > 0 else 1
    chars_pct = [round(c / max_chars * 100) for c in chars]

    metrics = [
        ("Prompt Length (relative)", chars_pct, "#667eea"),
        ("Has Role Prompting",       has_role,  "#f093fb"),
        ("Has Structured Schema",    has_sch,   "#4facfe"),
        ("Has Few-Shot Example",     has_ex,    "#43e97b"),
        ("Has Constraints",          has_con,   "#fa709a"),
    ]

    for name, values, color in metrics:
        fig.add_trace(go.Bar(
            name=name,
            x=levels,
            y=values,
            marker_color=color,
            text=[f"{v}%" for v in values],
            textposition="outside",
        ))

    fig.update_layout(
        barmode="group",
        height=380,
        margin=dict(t=20, b=20, l=10, r=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.35,
            x=0.5,
            xanchor="center",
            font=dict(size=11),
        ),
        xaxis_title=None,
        yaxis=dict(
            title="Score (0–100%)",
            range=[0, 120],
            gridcolor="#e2e8f0",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(248,249,255,1)",
        xaxis=dict(gridcolor="rgba(0,0,0,0)"),
    )

    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "💡 The Advanced prompt scores 100% on all quality dimensions, "
        "while Basic scores only on length."
    )
