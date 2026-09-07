"""
=============================================================
AI Assistant Page  —  Multi-Turn Trip Chat
=============================================================
Day 4  |  Part 4A

Sub-parts:
  4A-i    Chat message display (conversation history)
  4A-ii   Suggested questions chips
  4A-iii  Chat input box + send handler
  4A-iv   Context sidebar (trip summary, quick stats)
  4A-v    Clear chat button
=============================================================
"""

import streamlit as st
from utils.helpers import format_currency


# ── Suggested quick questions ─────────────────────────────────
QUICK_QUESTIONS = [
    "What should I pack for this trip?",
    "Which day has the highest cost and why?",
    "Can you suggest cheaper food options?",
    "What are the best hidden gems at this destination?",
    "Is my budget realistic for this destination?",
    "What's the best time of day to visit the main attraction?",
    "Can you suggest a romantic restaurant for the evening?",
    "What should I do if it rains?",
    "Which activities can I skip to save money?",
    "What local transport tips should I know?",
]


def render():
    """Render the AI Travel Assistant chat page."""

    st.markdown("## 🤖 AI Travel Assistant")
    st.markdown("Ask anything about your trip — the AI knows your full itinerary.")

    # ── Guard: no itinerary ────────────────────────────────────
    if not st.session_state.get("itinerary"):
        st.info(
            "**No itinerary yet.**  \n"
            "Go to **Plan Trip** to generate your itinerary first, then come back here.",
            icon="ℹ️",
        )
        if st.button("🗺️ Go to Plan Trip", type="primary"):
            st.session_state.current_page = "Plan Trip"
            st.rerun()
        return

    itinerary   = st.session_state.itinerary
    user_inputs = st.session_state.user_inputs
    currency    = user_inputs.get("currency", "INR")

    # ==========================================================
    # LAYOUT: chat column (left) + context sidebar (right)
    # ==========================================================
    chat_col, ctx_col = st.columns([2, 1], gap="large")

    # ==========================================================
    # SUB-PART 4A-iv  |  CONTEXT SIDEBAR (right column)
    # ==========================================================
    with ctx_col:
        st.markdown("#### 📋 Your Trip at a Glance")

        summary = itinerary.get("trip_summary", {})
        dest    = summary.get("destination", user_inputs.get("destination", ""))
        days    = summary.get("duration_days", user_inputs.get("num_days", 0))
        budget  = summary.get("total_budget", user_inputs.get("budget", 0))
        style   = summary.get("travel_style", user_inputs.get("travel_style", ""))

        st.markdown(f"""
        <div class="ai-card" style="padding:1rem;">
            <div style="font-size:1.1rem; font-weight:700; color:#2d3748; margin-bottom:0.5rem;">
                ✈️ {dest}
            </div>
            <div style="font-size:0.85rem; color:#718096; line-height:1.8;">
                📅 {days} days<br>
                👥 {summary.get("num_travelers", user_inputs.get("num_travelers", 1))} traveler(s)<br>
                💰 {format_currency(budget, currency)}<br>
                🎒 {style}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Budget breakdown mini-view
        bd = itinerary.get("budget_breakdown", {})
        if bd:
            st.markdown("**💰 Budget Breakdown:**")
            categories = {
                "🏨 Accommodation": "accommodation",
                "🍽️ Food":         "food",
                "🚗 Transport":    "transportation",
                "🎟️ Activities":   "activities_entry_fees",
                "🛍️ Shopping":     "shopping_misc",
            }
            for label, key in categories.items():
                val = bd.get(key, 0)
                if val:
                    st.caption(f"{label}: {format_currency(float(val), currency)}")

        st.divider()

        # Packing list teaser
        packing = itinerary.get("packing_list", [])
        if packing:
            st.markdown("**🎒 Packing Reminders:**")
            for item in packing[:5]:
                st.caption(f"☑️ {item}")
            if len(packing) > 5:
                st.caption(f"*+ {len(packing) - 5} more items...*")

        st.divider()

        # =======================================================
        # SUB-PART 4A-v  |  CLEAR CHAT BUTTON
        # =======================================================
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

        # Show message count
        msg_count = len(st.session_state.get("chat_history", []))
        if msg_count > 0:
            st.caption(f"💬 {msg_count} messages in this conversation")

        st.divider()
        st.markdown("""
        <div style="font-size:0.78rem; color:#94a3b8; text-align:center;">
            Powered by Google Gemini AI<br>
            Context Injection · Multi-Turn Chat
        </div>
        """, unsafe_allow_html=True)

    # ==========================================================
    # CHAT PANEL (left column)
    # ==========================================================
    with chat_col:

        # =======================================================
        # SUB-PART 4A-ii  |  SUGGESTED QUESTIONS CHIPS
        # =======================================================
        st.markdown("**💡 Quick Questions — click any to ask:**")

        # Show chips in rows of 2
        for i in range(0, min(6, len(QUICK_QUESTIONS)), 2):
            q_cols = st.columns(2)
            for j, col in enumerate(q_cols):
                if i + j < len(QUICK_QUESTIONS):
                    q = QUICK_QUESTIONS[i + j]
                    with col:
                        if st.button(
                            q,
                            key=f"quick_q_{i + j}",
                            use_container_width=True,
                            help="Click to send this question",
                        ):
                            _send_message(q, itinerary, user_inputs)

        st.markdown("<br>", unsafe_allow_html=True)

        # =======================================================
        # SUB-PART 4A-i  |  CHAT MESSAGE DISPLAY
        # =======================================================
        chat_history = st.session_state.get("chat_history", [])

        # Welcome message if no history yet
        if not chat_history:
            dest_name = user_inputs.get("destination", "your destination")
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #f0f4ff, #fdf4ff);
                border-radius: 12px;
                padding: 1.2rem;
                border-left: 4px solid #667eea;
                margin-bottom: 1rem;
            ">
                <div style="font-size:1.1rem; font-weight:600; color:#2d3748; margin-bottom:0.5rem;">
                    👋 Hi! I'm your AI travel assistant for your trip to {dest_name}.
                </div>
                <div style="font-size:0.88rem; color:#4a5568; line-height:1.7;">
                    I have your complete itinerary loaded and ready. I can help you with:<br>
                    • Alternative activities or restaurants<br>
                    • Budget tips and cost-cutting ideas<br>
                    • Packing advice for your destination<br>
                    • Local travel tips and cultural info<br>
                    • Weather contingency plans<br><br>
                    <em>Click a quick question above or type anything below!</em>
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:
            # Render chat messages
            for msg in chat_history:
                role    = msg.get("role", "user")
                content = msg.get("content", "")

                if role == "user":
                    with st.chat_message("user"):
                        st.markdown(content)
                else:
                    with st.chat_message("assistant", avatar="✈️"):
                        st.markdown(content)

        # =======================================================
        # SUB-PART 4A-iii  |  CHAT INPUT BOX
        # =======================================================
        user_message = st.chat_input(
            f"Ask me anything about your trip to {user_inputs.get('destination', '')}...",
            key="chat_input",
        )

        if user_message and user_message.strip():
            _send_message(user_message.strip(), itinerary, user_inputs)


# =============================================================
# INTERNAL HELPER
# =============================================================

def _send_message(question: str, itinerary: dict, user_inputs: dict):
    """
    Add the user question to history, call the AI assistant,
    append the response, and rerun to display the updated chat.

    Technique: Context Injection — the entire itinerary is injected
    as system context on every call so the model "remembers" the trip.
    """
    from services.llm_service import is_api_configured
    from services.itinerary_service import ask_assistant

    if not is_api_configured():
        st.error(
            "**API key missing.**  \n"
            "Add your Gemini API key to `.env` and restart the app."
        )
        return

    # Add user message to history
    chat_history = st.session_state.get("chat_history", [])
    chat_history.append({"role": "user", "content": question})
    st.session_state.chat_history = chat_history

    # Get AI response
    with st.spinner("🤖 Thinking..."):
        try:
            reply = ask_assistant(
                question=question,
                itinerary=itinerary,
                user_inputs=user_inputs,
                chat_history=chat_history[:-1],  # exclude current question (already appended)
            )

            # Append assistant reply
            chat_history.append({"role": "model", "content": reply})
            st.session_state.chat_history = chat_history

        except RuntimeError as e:
            error_msg = (
                f"Sorry, I couldn't get a response right now.  \n"
                f"**Error:** {e}  \n"
                "Please try again."
            )
            chat_history.append({"role": "model", "content": error_msg})
            st.session_state.chat_history = chat_history

        except Exception as e:
            chat_history.append({
                "role": "model",
                "content": f"Unexpected error: {e}. Please try again.",
            })
            st.session_state.chat_history = chat_history

    st.rerun()
