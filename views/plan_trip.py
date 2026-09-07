"""
=============================================================
Plan Trip Page  —  Trip Planning Form
=============================================================
Day 3  |  Part 3C

Sub-parts:
  3C-i    Form layout (two-column)
  3C-ii   Basic trip details (destination, dates, duration, travelers)
  3C-iii  Budget & style (currency, budget, style, accommodation, transport)
  3C-iv   Interests selection (multiselect + chip display)
  3C-v    Food preference
  3C-vi   Special requirements (free text)
  3C-vii  Generate button, validation, spinner, and generation
=============================================================
"""

import streamlit as st
from datetime import date, timedelta

from data.destinations import (
    INTERESTS_LIST, TRAVEL_STYLES, ACCOMMODATION_OPTIONS,
    TRANSPORTATION_OPTIONS, FOOD_PREFERENCES, CURRENCIES,
    POPULAR_DESTINATIONS,
)
from utils.validators import validate_user_inputs
from utils.helpers    import format_currency, estimate_per_person, INTEREST_ICONS


def render():
    """Render the Trip Planning Form page."""

    st.markdown("## 🗺️ Plan Your Trip")
    st.markdown("Fill in your travel preferences and let AI build your perfect itinerary.")
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Pre-fill destination if user clicked from Home page ──
    prefill_dest = st.session_state.pop("prefill_destination", "")

    # ==========================================================
    # SUB-PART 3C-i  |  QUICK DESTINATION PICKER
    # ==========================================================
    st.markdown("**Quick Pick — Popular Destinations:**")
    dest_cols = st.columns(6)
    for i, dest_info in enumerate(POPULAR_DESTINATIONS[:6]):
        with dest_cols[i]:
            if st.button(
                f"{dest_info['flag']} {dest_info['name']}",
                key=f"quick_{i}",
                use_container_width=True,
            ):
                prefill_dest = dest_info["name"]

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================================
    # THE FORM
    # ==========================================================
    with st.form("trip_planning_form", clear_on_submit=False):

        # ── Two-column layout ─────────────────────────────────
        left_col, right_col = st.columns(2, gap="large")

        # ==================================================
        # SUB-PART 3C-ii  |  BASIC TRIP DETAILS (left column)
        # ==================================================
        with left_col:
            st.markdown("#### 📍 Destination & Dates")

            destination = st.text_input(
                "Destination *",
                value=prefill_dest,
                placeholder="e.g. Goa, Manali, Paris, Bali...",
                help="Enter any city, state, or country you want to visit.",
            )

            col_date, col_days = st.columns(2)
            with col_date:
                start_date = st.date_input(
                    "Start Date *",
                    value=date.today() + timedelta(days=7),
                    min_value=date.today(),
                    help="When does your trip begin?",
                )
            with col_days:
                num_days = st.slider(
                    "Duration (days) *",
                    min_value=1,
                    max_value=30,
                    value=3,
                    help="How many days will you travel?",
                )

            # Live end-date display
            end_date = start_date + timedelta(days=num_days - 1)
            st.caption(
                f"📅 {start_date.strftime('%d %b %Y')} → {end_date.strftime('%d %b %Y')} "
                f"({num_days} day{'s' if num_days > 1 else ''})"
            )

            num_travelers = st.number_input(
                "Number of Travelers *",
                min_value=1,
                max_value=50,
                value=2,
                step=1,
                help="Total number of people traveling together.",
            )

        # ==================================================
        # SUB-PART 3C-iii  |  BUDGET & STYLE (right column)
        # ==================================================
        with right_col:
            st.markdown("#### 💰 Budget & Travel Style")

            # Currency selector
            currency_label = st.selectbox(
                "Currency",
                options=list(CURRENCIES.keys()),
                index=0,
                help="Select your preferred currency for costs.",
            )
            currency = CURRENCIES[currency_label]

            budget = st.number_input(
                "Total Budget *",
                min_value=100,
                max_value=10_000_000,
                value=15000,
                step=500,
                help="Total budget for the entire trip (all travelers combined).",
            )

            # Live per-person calculation
            per_person = estimate_per_person(budget, num_travelers)
            st.caption(
                f"💡 {format_currency(per_person, currency)} per person "
                f"· {format_currency(round(budget / num_days), currency)} per day"
            )

            travel_style = st.selectbox(
                "Travel Style *",
                options=TRAVEL_STYLES,
                index=1,  # Standard
                help="This shapes the pace, accommodation quality, and activity types.",
            )

            accommodation = st.selectbox(
                "Accommodation Preference",
                options=ACCOMMODATION_OPTIONS,
                index=2,  # 3-Star Hotel
            )

            transportation = st.selectbox(
                "Transport Preference",
                options=TRANSPORTATION_OPTIONS,
                index=6,  # Mixed
            )

        st.divider()

        # ==================================================
        # SUB-PART 3C-iv  |  INTERESTS SELECTION
        # ==================================================
        st.markdown("#### 🎯 Your Interests")
        st.caption("Select all that apply — the AI will prioritize these in your itinerary.")

        interests = st.multiselect(
            "Select Interests *",
            options=INTERESTS_LIST,
            default=["Beaches", "Food"],
            help="Choose at least 1 interest.",
        )

        # Display selected interests as colored chips
        if interests:
            chips_html = " ".join(
                f'<span class="dest-chip">{INTEREST_ICONS.get(i, "🎯")} {i}</span>'
                for i in interests
            )
            st.markdown(chips_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ==================================================
        # SUB-PART 3C-v  |  FOOD PREFERENCE
        # ==================================================
        st.markdown("#### 🍽️ Food Preferences")
        food_preferences = st.multiselect(
            "Dietary Preferences",
            options=FOOD_PREFERENCES,
            default=["All Cuisines"],
            help="The AI will strictly respect your dietary needs in all meal suggestions.",
        )

        st.divider()

        # ==================================================
        # SUB-PART 3C-vi  |  SPECIAL REQUIREMENTS
        # ==================================================
        st.markdown("#### 📝 Special Requirements")
        special_requirements = st.text_area(
            "Any special needs or constraints?",
            placeholder=(
                "e.g. Traveling with elderly parents — avoid long walking distances.\n"
                "e.g. Avoid tourist traps, prefer local hidden gems.\n"
                "e.g. Have a toddler — need family-friendly activities only.\n"
                "e.g. Interested in photography locations specifically."
            ),
            height=100,
            help="Optional. The AI will incorporate these into every decision.",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ==================================================
        # SUB-PART 3C-vii  |  GENERATE BUTTON
        # ==================================================
        submitted = st.form_submit_button(
            "🚀  Generate My AI Itinerary",
            type="primary",
            use_container_width=True,
        )

    # ── Form submission handling (outside the form block) ────
    if submitted:
        user_inputs = {
            "destination":          destination.strip(),
            "num_days":             int(num_days),
            "num_travelers":        int(num_travelers),
            "budget":               float(budget),
            "currency":             currency,
            "start_date":           str(start_date),
            "interests":            interests,
            "travel_style":         travel_style,
            "accommodation":        accommodation,
            "transportation":       transportation,
            "food_preferences":     food_preferences if food_preferences else ["All Cuisines"],
            "special_requirements": special_requirements.strip() or "None",
        }

        # Validate inputs
        valid, errors = validate_user_inputs(user_inputs)

        if not valid:
            st.error("**Please fix the following before generating:**")
            for err in errors:
                st.warning(err)
        else:
            _generate_itinerary(user_inputs)


def _generate_itinerary(user_inputs: dict):
    """
    Call the itinerary service and store the result in session state.
    Shows a spinner during generation with progress messages.
    """
    from services.llm_service import is_api_configured
    from services.itinerary_service import generate_itinerary, get_budget_comparison

    # Check API key first
    if not is_api_configured():
        st.error(
            "**Cannot generate itinerary — Gemini API key is missing.**  \n"
            "Please add your key to the `.env` file and restart the app.  \n"
            "Get a free key at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)"
        )
        return

    # Show generation progress
    progress_messages = [
        "🧠 Analysing your preferences...",
        "✍️ Building your personalized prompt...",
        "🤖 Sending to Gemini AI...",
        "📋 Structuring your itinerary...",
        "✅ Almost done — validating your plan...",
    ]

    progress_bar = st.progress(0)
    status_text  = st.empty()

    try:
        for i, msg in enumerate(progress_messages[:3]):
            status_text.info(msg)
            progress_bar.progress((i + 1) * 20)

        itinerary = generate_itinerary(user_inputs)

        status_text.info(progress_messages[3])
        progress_bar.progress(80)

        budget_status = get_budget_comparison(
            itinerary,
            user_inputs["budget"],
            user_inputs["currency"],
        )

        status_text.info(progress_messages[4])
        progress_bar.progress(100)

        # Save to session state
        st.session_state.itinerary     = itinerary
        st.session_state.user_inputs   = user_inputs
        st.session_state.budget_status = budget_status
        st.session_state.chat_history  = []  # reset chat for new trip

        # Build and save the prompt used (for PE page display)
        from prompts.itinerary_prompt import build_itinerary_prompt
        st.session_state.last_prompt = build_itinerary_prompt(user_inputs)

        status_text.success("✅ Your itinerary is ready!")
        progress_bar.empty()

        # Navigate to the itinerary page
        st.session_state.current_page = "My Itinerary"
        st.rerun()

    except ValueError as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"**Could not generate itinerary:**  \n{str(e)}")
        st.info("💡 Try simplifying your requirements or clicking Generate again.")

    except RuntimeError as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"**API Error:**  \n{str(e)}")
        st.info("💡 Check your API key and internet connection, then try again.")

    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"**Unexpected error:**  \n{str(e)}")
        st.info("💡 Please try again. If the issue persists, check your .env file.")
