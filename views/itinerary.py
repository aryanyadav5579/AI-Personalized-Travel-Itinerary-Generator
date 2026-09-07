"""
=============================================================
Itinerary Dashboard  —  Day-by-Day View
=============================================================
Day 3  |  Part 3D

Sub-parts:
  3D-i    Trip overview card
  3D-ii   Quick action buttons bar
  3D-iii  Day-by-day accordion (expandable cards)
  3D-iv   Individual day controls (regenerate / add / remove)
  3D-v    Day cost summary row (metrics)
  3D-vi   Packing list & tips tabs
=============================================================
"""

import streamlit as st

from utils.helpers    import (
    get_day_emoji, format_currency, INTEREST_ICONS,
    STYLE_ICONS, safe_get, interests_to_string,
)
from utils.validators import validate_itinerary_json


def render():
    """Render the Itinerary Dashboard page."""

    # ── Guard: no itinerary yet ───────────────────────────────
    if not st.session_state.get("itinerary"):
        st.markdown("## 📅 My Itinerary")
        st.info(
            "**No itinerary generated yet.**  \n"
            "Go to **Plan Trip** to fill in your preferences and generate one.",
            icon="ℹ️",
        )
        if st.button("🗺️ Go to Plan Trip", type="primary"):
            st.session_state.current_page = "Plan Trip"
            st.rerun()
        return

    itinerary   = st.session_state.itinerary
    user_inputs = st.session_state.user_inputs
    currency    = user_inputs.get("currency", "INR")
    days        = itinerary.get("days", [])

    # ==========================================================
    # SUB-PART 3D-i  |  TRIP OVERVIEW CARD
    # ==========================================================
    summary = itinerary.get("trip_summary", {})

    dest         = summary.get("destination", user_inputs.get("destination", ""))
    duration     = summary.get("duration_days", user_inputs.get("num_days", 0))
    travelers    = summary.get("num_travelers", user_inputs.get("num_travelers", 1))
    budget       = summary.get("total_budget", user_inputs.get("budget", 0))
    style        = summary.get("travel_style", user_inputs.get("travel_style", ""))
    start_date   = summary.get("start_date", user_inputs.get("start_date", ""))
    end_date     = summary.get("end_date", "")
    overview_txt = summary.get("overview", "")
    accomm       = summary.get("accommodation_type", user_inputs.get("accommodation", ""))
    transport    = summary.get("transportation_mode", user_inputs.get("transportation", ""))
    top_interests = summary.get("top_interests", user_inputs.get("interests", []))

    style_emoji = STYLE_ICONS.get(style, "⭐")

    st.markdown(f"""
    <div class="ai-card">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:1rem;">
            <div>
                <h2 style="margin:0; color:#2d3748;">✈️ {dest}</h2>
                <div style="color:#718096; font-size:0.9rem; margin-top:0.3rem;">
                    {start_date} → {end_date} &nbsp;|&nbsp;
                    {duration} days &nbsp;|&nbsp;
                    {travelers} traveler{'s' if travelers > 1 else ''} &nbsp;|&nbsp;
                    {style_emoji} {style}
                </div>
                {f'<p style="color:#4a5568; margin-top:0.7rem; font-size:0.9rem;">{overview_txt}</p>' if overview_txt else ''}
            </div>
            <div style="text-align:right;">
                <div style="font-size:0.8rem; color:#94a3b8; margin-bottom:0.3rem;">Total Budget</div>
                <div style="font-size:1.5rem; font-weight:700; color:#667eea;">
                    {format_currency(budget, currency)}
                </div>
            </div>
        </div>
        <div style="margin-top:1rem; display:flex; gap:0.5rem; flex-wrap:wrap;">
            <span style="background:#eef2ff;color:#4338ca;border-radius:5px;padding:3px 10px;font-size:0.8rem;">🏨 {accomm}</span>
            <span style="background:#f0fdf4;color:#166534;border-radius:5px;padding:3px 10px;font-size:0.8rem;">🚗 {transport}</span>
            {"".join(f'<span style="background:#fdf4ff;color:#7e22ce;border-radius:5px;padding:3px 10px;font-size:0.8rem;">{INTEREST_ICONS.get(i,"🎯")} {i}</span>' for i in top_interests[:5])}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Show budget status if available
    if st.session_state.get("budget_status"):
        bs = st.session_state.budget_status
        color_map = {"under": "budget-ok", "tight": "budget-tight", "over": "budget-over"}
        cls = color_map.get(bs["status"], "budget-ok")
        st.markdown(
            f'<span class="{cls}">{bs["emoji"]} {bs["message"]}</span>',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================================
    # SUB-PART 3D-ii  |  QUICK ACTION BUTTONS BAR
    # ==========================================================
    st.markdown("#### ⚡ Quick Actions")
    btn_cols = st.columns(5)

    with btn_cols[0]:
        if st.button("🔄 Regenerate Trip", use_container_width=True,
                     help="Generate a completely new itinerary for the same preferences."):
            _apply_modification("regenerate_entire")

    with btn_cols[1]:
        if st.button("💰 Make Cheaper", use_container_width=True,
                     help="Optimize the itinerary to reduce costs."):
            _apply_modification("make_cheaper")

    with btn_cols[2]:
        if st.button("🧗 More Adventure", use_container_width=True,
                     help="Replace activities with more adventurous options."):
            _apply_modification("make_adventurous")

    with btn_cols[3]:
        if st.button("😌 More Relaxed", use_container_width=True,
                     help="Slow down the pace and reduce activity count."):
            _apply_modification("make_relaxed")

    with btn_cols[4]:
        if st.button("📄 Download PDF", use_container_width=True,
                     help="Download the itinerary as a PDF file."):
            _download_pdf()

    # Additional actions row
    btn_cols2 = st.columns(4)
    with btn_cols2[0]:
        if st.button("🍽️ More Food Options", use_container_width=True):
            _apply_modification("add_food")
    with btn_cols2[1]:
        if st.button("🚗 Reduce Travel Time", use_container_width=True):
            _apply_modification("reduce_travel_time")
    with btn_cols2[2]:
        if st.button("➕ Add a Day", use_container_width=True):
            _apply_modification("add_day")
    with btn_cols2[3]:
        if st.button("🤖 Open AI Chat", use_container_width=True):
            st.session_state.current_page = "AI Assistant"
            st.rerun()

    st.divider()

    # ==========================================================
    # SUB-PART 3D-iii  |  DAY-BY-DAY ACCORDION
    # ==========================================================
    st.markdown("#### 📅 Day-by-Day Itinerary")

    for day_data in days:
        day_num  = day_data.get("day", 0)
        day_date = day_data.get("date", f"Day {day_num}")
        day_cost = day_data.get("day_total_cost", 0)
        day_tips = day_data.get("tips", [])
        emoji    = get_day_emoji(day_num - 1)

        with st.expander(
            f"{emoji}  Day {day_num}  —  {day_date}  |  "
            f"Est. cost: {format_currency(day_cost, currency)}",
            expanded=(day_num == 1),   # first day open by default
        ):
            # ── Three time-slot columns ────────────────────────
            m_col, a_col, e_col = st.columns(3, gap="small")

            for col, slot_key, slot_label, slot_emoji in [
                (m_col, "morning",   "Morning",   "🌅"),
                (a_col, "afternoon", "Afternoon", "🌞"),
                (e_col, "evening",   "Evening",   "🌙"),
            ]:
                slot = day_data.get(slot_key, {})
                acts = slot.get("activities", [])
                food = slot.get("food", "")
                trans = slot.get("transport", "")
                cost  = slot.get("estimated_cost", 0)
                time_range = slot.get("time", "")
                notes = slot.get("notes", "")
                attraction = slot.get("attraction", "")

                with col:
                    st.markdown(f"""
                    <div class="slot-card">
                        <div class="slot-title">{slot_emoji} {slot_label}</div>
                        <div style="font-size:0.78rem;color:#94a3b8;margin-bottom:0.5rem;">{time_range}</div>
                        {"".join(f'<div style="font-size:0.85rem;color:#2d3748;margin-bottom:0.2rem;">• {a}</div>' for a in acts)}
                        {f'<div style="margin-top:0.5rem; font-size:0.82rem; color:#667eea; font-weight:600;">📍 {attraction}</div>' if attraction else ''}
                        <div style="margin-top:0.6rem; font-size:0.82rem; color:#e67e22;">🍽️ {food}</div>
                        <div style="margin-top:0.3rem; font-size:0.8rem; color:#718096;">🚗 {trans}</div>
                        <div style="margin-top:0.5rem; background:#f0f4ff; border-radius:5px;
                                    padding:3px 8px; display:inline-block;
                                    font-size:0.78rem; color:#4338ca; font-weight:600;">
                            {format_currency(cost, currency)}
                        </div>
                        {f'<div style="margin-top:0.5rem; font-size:0.78rem; color:#718096; font-style:italic;">💡 {notes}</div>' if notes else ''}
                    </div>
                    """, unsafe_allow_html=True)

            # ── SUB-PART 3D-v  |  Day cost summary row ────────
            st.markdown("<br>", unsafe_allow_html=True)
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Day Total",     format_currency(day_cost, currency))
            m2.metric("Morning",       format_currency(safe_get(day_data, "morning", "estimated_cost", default=0), currency))
            m3.metric("Afternoon",     format_currency(safe_get(day_data, "afternoon", "estimated_cost", default=0), currency))
            m4.metric("Evening",       format_currency(safe_get(day_data, "evening", "estimated_cost", default=0), currency))

            # ── Day tips ───────────────────────────────────────
            if day_tips:
                st.markdown("**💡 Tips for this day:**")
                for tip in day_tips:
                    st.markdown(f"  - {tip}")

            # ── SUB-PART 3D-iv  |  Individual day controls ────
            st.markdown("---")
            dc1, dc2, dc3, _ = st.columns([1, 1, 1, 2])

            with dc1:
                if st.button(
                    f"↺ Regenerate Day {day_num}",
                    key=f"regen_day_{day_num}",
                    use_container_width=True,
                    help=f"Generate fresh activities for Day {day_num} only.",
                ):
                    _apply_modification("regenerate_day", day_num=day_num)

            with dc2:
                if st.button(
                    "➕ Add Next Day",
                    key=f"add_after_{day_num}",
                    use_container_width=True,
                    help="Extend the trip by adding one more day.",
                ):
                    _apply_modification("add_day")

            with dc3:
                if len(days) > 1:
                    if st.button(
                        f"✕ Remove Day {day_num}",
                        key=f"remove_day_{day_num}",
                        use_container_width=True,
                        help=f"Remove Day {day_num} from the itinerary.",
                    ):
                        _apply_modification("remove_day", day_num=day_num)

    st.divider()

    # ==========================================================
    # SUB-PART 3D-vi  |  PACKING LIST & TIPS TABS
    # ==========================================================
    packing_list    = itinerary.get("packing_list", [])
    important_tips  = itinerary.get("important_tips", [])

    tab_pack, tab_tips = st.tabs(["🎒 Packing List", "📌 Important Tips"])

    with tab_pack:
        if packing_list:
            cols_per_row = 2
            for i in range(0, len(packing_list), cols_per_row):
                pack_cols = st.columns(cols_per_row)
                for j, col in enumerate(pack_cols):
                    if i + j < len(packing_list):
                        with col:
                            st.markdown(f"☑️ {packing_list[i + j]}")
        else:
            st.info("No packing list generated.")

    with tab_tips:
        if important_tips:
            for tip in important_tips:
                st.markdown(f"📌 {tip}")
        else:
            st.info("No travel tips generated.")


# =============================================================
# INTERNAL HELPERS
# =============================================================

def _apply_modification(action: str, **kwargs):
    """
    Call the itinerary service to apply a modification and update session state.
    Shows a spinner during the AI call.
    """
    from services.llm_service import is_api_configured
    from services.itinerary_service import modify_itinerary, get_budget_comparison

    if not is_api_configured():
        st.error("API key missing — cannot apply modifications. Check your .env file.")
        return

    itinerary   = st.session_state.itinerary
    user_inputs = st.session_state.user_inputs
    currency    = user_inputs.get("currency", "INR")

    action_labels = {
        "regenerate_entire": "Generating a brand-new itinerary...",
        "make_cheaper":      "Optimizing your budget...",
        "make_adventurous":  "Adding adventure activities...",
        "make_relaxed":      "Creating a more relaxed pace...",
        "add_food":          "Enhancing food recommendations...",
        "reduce_travel_time": "Rearranging for less travel time...",
        "regenerate_day":    f"Regenerating Day {kwargs.get('day_num', '')}...",
        "add_day":           "Adding a new day to your trip...",
        "remove_day":        f"Removing Day {kwargs.get('day_num', '')}...",
    }
    label = action_labels.get(action, "Updating your itinerary...")

    with st.spinner(label):
        try:
            updated = modify_itinerary(action, itinerary, user_inputs, **kwargs)
            budget_status = get_budget_comparison(
                updated, user_inputs["budget"], currency
            )
            st.session_state.itinerary     = updated
            st.session_state.budget_status = budget_status
            st.success("✅ Itinerary updated!")
            st.rerun()

        except ValueError as e:
            st.error(f"Could not apply modification: {e}")
        except RuntimeError as e:
            st.error(f"API Error: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")


def _download_pdf():
    """Generate and offer PDF download."""
    itinerary   = st.session_state.itinerary
    user_inputs = st.session_state.user_inputs

    try:
        from services.pdf_service import generate_pdf
        pdf_bytes = generate_pdf(itinerary, user_inputs)
        dest = user_inputs.get("destination", "trip").replace(" ", "_")
        st.download_button(
            label="📄 Click to Download PDF",
            data=pdf_bytes,
            file_name=f"itinerary_{dest}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    except ImportError:
        st.warning("PDF service not yet available. Coming soon!")
    except Exception as e:
        st.error(f"PDF generation failed: {e}")
