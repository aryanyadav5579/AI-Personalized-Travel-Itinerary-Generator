"""
=============================================================
Budget Analysis Page  —  Visual Budget Dashboard
=============================================================
Day 4  |  Part 4B

Sub-parts:
  4B-i    Budget status banner (over / tight / under)
  4B-ii   4 metric tiles (budgeted / estimated / per-person / per-day)
  4B-iii  Pie chart — budget breakdown by category
  4B-iv   Bar chart — daily spending across all days
  4B-v    Detailed cost table (per-day morning/afternoon/evening)
  4B-vi   Budget optimization prompt button
=============================================================
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from utils.helpers    import format_currency, calculate_budget_status, estimate_per_person
from services.itinerary_service import (
    extract_budget_data,
    get_budget_comparison,
    get_day_cost_table,
    calculate_total_estimated_cost,
)


def render():
    """Render the Budget Analysis page."""

    st.markdown("## 💰 Budget Analysis")
    st.markdown("Visualize your trip costs and see exactly how your budget is being spent.")

    # ── Guard: no itinerary ────────────────────────────────────
    if not st.session_state.get("itinerary"):
        st.info(
            "**No itinerary yet.**  \n"
            "Go to **Plan Trip** to generate your itinerary first.",
            icon="ℹ️",
        )
        if st.button("🗺️ Go to Plan Trip", type="primary"):
            st.session_state.current_page = "Plan Trip"
            st.rerun()
        return

    itinerary   = st.session_state.itinerary
    user_inputs = st.session_state.user_inputs
    currency    = user_inputs.get("currency", "INR")
    user_budget = user_inputs.get("budget", 0)
    num_days    = user_inputs.get("num_days", 1)
    num_travelers = user_inputs.get("num_travelers", 1)

    # ── Compute numbers ────────────────────────────────────────
    breakdown     = extract_budget_data(itinerary)
    estimated     = calculate_total_estimated_cost(itinerary)
    budget_status = get_budget_comparison(itinerary, user_budget, currency)
    day_table     = get_day_cost_table(itinerary)

    # ==========================================================
    # SUB-PART 4B-i  |  BUDGET STATUS BANNER
    # ==========================================================
    status = budget_status.get("status", "under")
    emoji  = budget_status.get("emoji", "✅")
    msg    = budget_status.get("message", "")
    pct    = budget_status.get("percentage", 0)
    diff   = abs(budget_status.get("difference", 0))

    banner_colors = {
        "under": ("🟢", "#e6ffed", "#1a7431", "#c3e6cb"),
        "tight": ("🟡", "#fff8e1", "#b45309", "#fde68a"),
        "over":  ("🔴", "#ffe4e6", "#be123c", "#fecdd3"),
    }
    _, bg, text_color, border_color = banner_colors.get(status, banner_colors["under"])

    diff_phrase = (
        f"You are {format_currency(diff, currency)} **{'over budget' if status == 'over' else 'under budget'}**."
        if diff > 0 else "You are exactly on budget."
    )

    st.markdown(f"""
    <div style="
        background:{bg}; border:1.5px solid {border_color};
        border-radius:10px; padding:1rem 1.2rem; margin-bottom:1.2rem;
    ">
        <div style="font-size:1.1rem; font-weight:700; color:{text_color};">
            {emoji} {msg}
        </div>
        <div style="font-size:0.88rem; color:{text_color}; margin-top:0.3rem;">
            Your estimated trip cost is <strong>{budget_status.get('estimated_fmt', '')}</strong>
            vs your budget of <strong>{budget_status.get('budget_fmt', '')}</strong>.
            {diff_phrase}
            ({pct:.1f}% of budget used)
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ==========================================================
    # SUB-PART 4B-ii  |  4 METRIC TILES
    # ==========================================================
    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        label="💳 Your Budget",
        value=format_currency(user_budget, currency),
        delta=None,
    )
    delta_val = estimated - user_budget
    m2.metric(
        label="📊 Estimated Cost",
        value=format_currency(estimated, currency),
        delta=f"{'+' if delta_val >= 0 else ''}{format_currency(delta_val, currency)} vs budget",
        delta_color="inverse",
    )
    m3.metric(
        label="👤 Per Person",
        value=format_currency(estimate_per_person(estimated, num_travelers), currency),
    )
    daily_avg = round(estimated / num_days) if num_days > 0 else 0
    m4.metric(
        label="📅 Daily Average",
        value=format_currency(daily_avg, currency),
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================================
    # SUB-PART 4B-iii  |  PIE CHART — Budget Breakdown
    # ==========================================================
    chart_col, table_col = st.columns([1, 1], gap="large")

    with chart_col:
        st.markdown("#### 🥧 Cost by Category")

        pie_labels = ["Accommodation", "Food", "Transport", "Activities", "Shopping & Misc"]
        pie_keys   = ["accommodation", "food", "transportation", "activities_entry_fees", "shopping_misc"]
        pie_values = [float(breakdown.get(k, 0)) for k in pie_keys]

        # Filter out zero categories
        filtered = [(l, v) for l, v in zip(pie_labels, pie_values) if v > 0]
        if filtered:
            f_labels, f_values = zip(*filtered)

            pie_fig = go.Figure(data=[go.Pie(
                labels=f_labels,
                values=f_values,
                hole=0.42,           # donut style
                textinfo="label+percent",
                textfont_size=11,
                marker=dict(colors=[
                    "#667eea", "#f093fb", "#4facfe",
                    "#43e97b", "#fa709a",
                ]),
                hovertemplate="<b>%{label}</b><br>"
                              f"{currency} %{{value:,.0f}}<br>"
                              "(%{percent})<extra></extra>",
            )])

            pie_fig.update_layout(
                margin=dict(t=10, b=10, l=10, r=10),
                height=320,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.25, x=0.5, xanchor="center"),
                annotations=[dict(
                    text=f"<b>{format_currency(estimated, currency)}</b>",
                    x=0.5, y=0.5, font_size=13, showarrow=False,
                )],
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(pie_fig, use_container_width=True)
        else:
            st.info("No cost data to display.")

    # ==========================================================
    # Budget breakdown detail table (right of pie)
    # ==========================================================
    with table_col:
        st.markdown("#### 📋 Category Breakdown")

        cat_rows = []
        cat_info = [
            ("🏨", "Accommodation", "accommodation"),
            ("🍽️", "Food",          "food"),
            ("🚗", "Transportation", "transportation"),
            ("🎟️", "Activities",    "activities_entry_fees"),
            ("🛍️", "Shopping & Misc","shopping_misc"),
        ]
        for icon, label, key in cat_info:
            val = float(breakdown.get(key, 0))
            pct_of_total = round(val / estimated * 100, 1) if estimated > 0 else 0
            pct_of_budget = round(val / user_budget * 100, 1) if user_budget > 0 else 0
            cat_rows.append({
                "Category":   f"{icon} {label}",
                "Cost":       format_currency(val, currency),
                "% of Trip":  f"{pct_of_total}%",
                "% of Budget": f"{pct_of_budget}%",
            })

        cat_df = pd.DataFrame(cat_rows)
        st.dataframe(cat_df, use_container_width=True, hide_index=True)

        # Total row
        st.markdown(f"""
        <div style="
            background:#f0f4ff; border-radius:8px;
            padding:0.5rem 1rem; margin-top:0.5rem;
            display:flex; justify-content:space-between;
        ">
            <span style="font-weight:700; color:#2d3748;">💰 Total Estimated</span>
            <span style="font-weight:700; color:#667eea; font-size:1.05rem;">
                {format_currency(estimated, currency)}
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================================
    # SUB-PART 4B-iv  |  BAR CHART — Daily Spending
    # ==========================================================
    st.markdown("#### 📊 Spending by Day")

    if day_table:
        day_labels  = [f"Day {r['day']}" for r in day_table]
        day_morning = [r["morning_cost"]   for r in day_table]
        day_noon    = [r["afternoon_cost"] for r in day_table]
        day_evening = [r["evening_cost"]   for r in day_table]
        day_totals  = [r["day_total"]      for r in day_table]

        # Daily budget guideline line
        daily_budget_target = user_budget / num_days if num_days > 0 else 0

        bar_fig = go.Figure()

        bar_fig.add_trace(go.Bar(
            name="Morning",
            x=day_labels, y=day_morning,
            marker_color="#4facfe",
            hovertemplate=f"Morning<br>{currency} %{{y:,.0f}}<extra></extra>",
        ))
        bar_fig.add_trace(go.Bar(
            name="Afternoon",
            x=day_labels, y=day_noon,
            marker_color="#667eea",
            hovertemplate=f"Afternoon<br>{currency} %{{y:,.0f}}<extra></extra>",
        ))
        bar_fig.add_trace(go.Bar(
            name="Evening",
            x=day_labels, y=day_evening,
            marker_color="#764ba2",
            hovertemplate=f"Evening<br>{currency} %{{y:,.0f}}<extra></extra>",
        ))

        # Budget guideline line
        if daily_budget_target > 0:
            bar_fig.add_hline(
                y=daily_budget_target,
                line_dash="dash",
                line_color="#e53e3e",
                line_width=2,
                annotation_text=f"Daily budget target ({format_currency(daily_budget_target, currency)})",
                annotation_position="top right",
                annotation_font_color="#e53e3e",
                annotation_font_size=11,
            )

        bar_fig.update_layout(
            barmode="stack",
            height=360,
            margin=dict(t=20, b=30, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0.5, xanchor="center"),
            xaxis_title=None,
            yaxis_title=f"Cost ({currency})",
            yaxis_tickformat=",.0f",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(248,249,255,1)",
            yaxis=dict(gridcolor="#e2e8f0"),
            xaxis=dict(gridcolor="rgba(0,0,0,0)"),
            hovermode="x unified",
        )

        st.plotly_chart(bar_fig, use_container_width=True)

    st.divider()

    # ==========================================================
    # SUB-PART 4B-v  |  DETAILED COST TABLE
    # ==========================================================
    st.markdown("#### 🗓️ Detailed Daily Costs")

    if day_table:
        table_rows = []
        for r in day_table:
            table_rows.append({
                "Day":       f"Day {r['day']}",
                "Date":      r["date"],
                "🌅 Morning":  format_currency(r["morning_cost"],   currency),
                "🌞 Afternoon": format_currency(r["afternoon_cost"], currency),
                "🌙 Evening":  format_currency(r["evening_cost"],   currency),
                "📊 Day Total": format_currency(r["day_total"],     currency),
            })

        cost_df = pd.DataFrame(table_rows)
        st.dataframe(
            cost_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "📊 Day Total": st.column_config.TextColumn(
                    "Day Total", help="Sum of all three time slots"
                ),
            },
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================================
    # SUB-PART 4B-vi  |  BUDGET OPTIMIZATION BUTTON
    # ==========================================================
    if status in ("over", "tight"):
        st.markdown("#### 🔧 Budget Help")

        if status == "over":
            st.warning(
                f"Your trip is **{format_currency(diff, currency)} over budget**. "
                "Use the button below to let AI optimize and reduce costs.",
                icon="⚠️",
            )
        else:
            st.info(
                f"Your budget is **tight** — only {format_currency(diff, currency)} remaining. "
                "You may want to optimize to create more breathing room.",
                icon="💡",
            )

        opt_col1, opt_col2 = st.columns(2)
        with opt_col1:
            if st.button(
                "🤖 Optimize Budget with AI",
                type="primary",
                use_container_width=True,
                help="AI will reduce costs while keeping your top interests.",
            ):
                _run_optimization(itinerary, user_inputs, currency)

        with opt_col2:
            if st.button(
                "📅 View & Edit Itinerary",
                use_container_width=True,
            ):
                st.session_state.current_page = "My Itinerary"
                st.rerun()

    else:
        st.success(
            f"Your budget looks good! "
            f"You have **{format_currency(diff, currency)}** to spare.",
            icon="✅",
        )


# =============================================================
# INTERNAL HELPERS
# =============================================================

def _run_optimization(itinerary: dict, user_inputs: dict, currency: str):
    """Call the AI optimization and refresh session state."""
    from services.llm_service import is_api_configured
    from services.itinerary_service import modify_itinerary, get_budget_comparison

    if not is_api_configured():
        st.error("API key missing — cannot run optimization. Check your .env file.")
        return

    with st.spinner("🤖 AI is optimizing your budget... (this takes ~20-30 seconds)"):
        try:
            updated = modify_itinerary("make_cheaper", itinerary, user_inputs)
            new_status = get_budget_comparison(
                updated, user_inputs["budget"], currency
            )
            st.session_state.itinerary     = updated
            st.session_state.budget_status = new_status

            new_cost = new_status.get("estimated_fmt", "")
            st.success(f"✅ Optimization complete! New estimated cost: **{new_cost}**")
            st.rerun()

        except ValueError as e:
            st.error(f"Optimization failed: {e}")
        except RuntimeError as e:
            st.error(f"API Error: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
