"""
=============================================================
Home Page  —  Landing Page
=============================================================
Day 3  |  Part 3B

Sub-parts:
  3B-i   Hero section with CTA buttons
  3B-ii  Features grid (6 cards)
  3B-iii How It Works steps
  3B-iv  Prompt Engineering highlight box
  3B-v   Popular destinations strip
=============================================================
"""

import streamlit as st
from data.destinations import POPULAR_DESTINATIONS


def render():
    """Render the Home landing page."""

    # ==========================================================
    # SUB-PART 3B-i  |  HERO SECTION
    # ==========================================================
    st.markdown("""
    <div class="hero-banner">
        <div style="font-size:3.5rem; margin-bottom:0.5rem;">✈️</div>
        <h1>AI Travel Planner</h1>
        <p>Generate a personalized, day-by-day travel itinerary in seconds<br>
        powered by <strong>Google Gemini AI</strong> and advanced <strong>Prompt Engineering</strong></p>
    </div>
    """, unsafe_allow_html=True)

    # CTA buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🗺️  Plan My Trip", type="primary", use_container_width=True):
            st.session_state.current_page = "Plan Trip"
            st.rerun()
    with col2:
        if st.button("📅  View Sample Itinerary", use_container_width=True):
            _load_sample_itinerary()
            st.session_state.current_page = "My Itinerary"
            st.rerun()
    with col3:
        if st.button("🎓  Explore Prompt Engineering", use_container_width=True):
            st.session_state.current_page = "Prompt Engineering"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================================
    # SUB-PART 3B-ii  |  FEATURES GRID
    # ==========================================================
    st.markdown("### ✨ What This App Can Do")
    st.markdown("<br>", unsafe_allow_html=True)

    features = [
        ("🗺️", "Smart Itinerary Generation",
         "AI builds a complete day-by-day plan with morning, afternoon & evening activities tailored to your interests and budget."),
        ("💰", "Budget Optimization",
         "Real-time cost estimates with a visual breakdown. One click to optimize if your plan exceeds budget."),
        ("🤖", "AI Travel Assistant",
         "Ask anything about your trip. The AI knows your full itinerary and gives personalized answers."),
        ("✏️", "Interactive Editing",
         "Regenerate any single day, make it adventurous, relaxed, cheaper, or foodie-focused with one click."),
        ("📄", "PDF Export",
         "Download a clean, professional PDF of your full itinerary including packing list and travel tips."),
        ("🎓", "Prompt Engineering Demo",
         "See exactly how the AI prompts are built — Basic vs Standard vs Advanced prompt comparison."),
    ]

    for i in range(0, len(features), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(features):
                icon, title, desc = features[i + j]
                with col:
                    st.markdown(f"""
                    <div class="feature-card">
                        <h4>{icon} {title}</h4>
                        <p>{desc}</p>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================================
    # SUB-PART 3B-iii  |  HOW IT WORKS
    # ==========================================================
    st.markdown("### 🔄 How It Works")
    st.markdown("<br>", unsafe_allow_html=True)

    steps = [
        ("1", "Fill the Form", "Enter your destination, dates, budget, interests, and preferences."),
        ("2", "AI Builds Prompt", "Your inputs are assembled into a rich, structured AI prompt using 5 engineering techniques."),
        ("3", "Gemini Generates", "Google Gemini processes the prompt and returns a structured JSON itinerary."),
        ("4", "Your Plan is Ready", "View day-by-day cards, edit anything, chat with the AI, and download your PDF."),
    ]

    cols = st.columns(4)
    for col, (num, title, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div style="text-align:center; padding: 1rem;">
                <div class="step-badge">{num}</div>
                <div style="font-weight:600; font-size:0.95rem; color:#2d3748; margin-bottom:0.4rem;">{title}</div>
                <div style="font-size:0.82rem; color:#718096;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # Arrow connectors (visual only)
    st.markdown("""
    <div style="text-align:center; font-size:1.4rem; color:#667eea; margin-top:-0.5rem;">
        ─── ─── ─── ▶
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================================
    # SUB-PART 3B-iv  |  PROMPT ENGINEERING HIGHLIGHT BOX
    # ==========================================================
    st.markdown("### 🧠 Prompt Engineering at the Core")

    st.markdown("""
    <div class="info-banner">
        This is not just a chatbot. Every itinerary is generated using <strong>7 carefully designed
        prompt engineering techniques</strong> that guide the AI to produce structured,
        accurate, budget-aware, and personalized travel plans.
    </div>
    """, unsafe_allow_html=True)

    pe_cols = st.columns(2)
    techniques_left = [
        ("🎭", "Role Prompting", "\"You are an expert travel planner with 20+ years of experience...\""),
        ("💉", "Context Injection", "All 12 user preferences embedded directly into every prompt"),
        ("📚", "Few-Shot Prompting", "A complete example day shown to the model for consistent output"),
        ("🔒", "Constraint-Based", "Strict rules for budget, diet, distance, and pacing"),
    ]
    techniques_right = [
        ("📋", "Structured Output", "Model forced to return exact JSON schema — no free-form text"),
        ("🎯", "Zero-Shot", "Chat assistant answers questions without needing examples"),
        ("🔄", "Iterative Refinement", "Edit prompts pass existing plan as context for targeted changes"),
        ("📊", "Prompt Comparison", "Live demo of Basic → Standard → Advanced prompts on the PE page"),
    ]

    with pe_cols[0]:
        for icon, name, desc in techniques_left:
            st.markdown(f"""
            <div style="display:flex; align-items:flex-start; gap:0.7rem; margin-bottom:0.7rem;">
                <span style="font-size:1.3rem;">{icon}</span>
                <div>
                    <div style="font-weight:600; font-size:0.9rem; color:#2d3748;">{name}</div>
                    <div style="font-size:0.82rem; color:#718096;">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with pe_cols[1]:
        for icon, name, desc in techniques_right:
            st.markdown(f"""
            <div style="display:flex; align-items:flex-start; gap:0.7rem; margin-bottom:0.7rem;">
                <span style="font-size:1.3rem;">{icon}</span>
                <div>
                    <div style="font-weight:600; font-size:0.9rem; color:#2d3748;">{name}</div>
                    <div style="font-size:0.82rem; color:#718096;">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================================
    # SUB-PART 3B-v  |  POPULAR DESTINATIONS STRIP
    # ==========================================================
    st.markdown("### 🌍 Popular Destinations")
    st.markdown("*Click any destination to pre-fill the trip form*")
    st.markdown("<br>", unsafe_allow_html=True)

    # Show 4 destinations per row
    for row_start in range(0, len(POPULAR_DESTINATIONS), 4):
        cols = st.columns(4)
        for j, col in enumerate(cols):
            idx = row_start + j
            if idx < len(POPULAR_DESTINATIONS):
                dest = POPULAR_DESTINATIONS[idx]
                with col:
                    st.markdown(f"""
                    <div class="ai-card" style="text-align:center; padding: 1rem;">
                        <div style="font-size:2rem;">{dest['flag']}</div>
                        <div style="font-weight:600; font-size:0.95rem; color:#2d3748; margin-top:0.3rem;">
                            {dest['name']}
                        </div>
                        <div style="font-size:0.78rem; color:#94a3b8;">{dest['country']}</div>
                        <div style="font-size:0.8rem; color:#667eea; margin-top:0.3rem;">{dest['highlight']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Clickable button per destination
                    if st.button(
                        f"Plan {dest['name']}",
                        key=f"dest_{idx}",
                        use_container_width=True,
                    ):
                        st.session_state.prefill_destination = dest["name"]
                        st.session_state.current_page = "Plan Trip"
                        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="text-align:center; padding: 2rem 0 1rem 0;
                color:#94a3b8; font-size:0.82rem; border-top:1px solid #e2e8f0;">
        AI Travel Planner &nbsp;|&nbsp; Gen AI &amp; Prompt Engineering Project &nbsp;|&nbsp;
        Powered by Google Gemini 2.0 Flash
    </div>
    """, unsafe_allow_html=True)


# =============================================================
# INTERNAL HELPER
# =============================================================
def _load_sample_itinerary():
    """
    Pre-load a sample itinerary into session state so the user can
    preview the itinerary page without needing an API key.
    """
    sample = {
        "trip_summary": {
            "destination": "Goa, India",
            "duration_days": 3,
            "start_date": "10 March 2025",
            "end_date": "12 March 2025",
            "num_travelers": 2,
            "total_budget": 15000,
            "currency": "INR",
            "travel_style": "Standard",
            "accommodation_type": "3-Star Hotel",
            "transportation_mode": "Mixed",
            "top_interests": ["Beaches", "Food", "Culture"],
            "overview": "A perfect 3-day getaway to Goa combining beautiful beaches, "
                        "local Goan cuisine, and Portuguese heritage sites. "
                        "Designed for a couple on a standard budget.",
        },
        "days": [
            {
                "day": 1, "date": "Monday, 10 March 2025",
                "morning": {
                    "time": "7:00 AM – 10:30 AM",
                    "activities": ["Sunrise at Calangute Beach", "Morning beach walk"],
                    "attraction": "Calangute Beach",
                    "food": "Breakfast at a beachside shack — poha & chai (est. INR 150/person)",
                    "transport": "Walk from hotel (5 min)",
                    "estimated_cost": 300,
                    "notes": "Arrive before 7 AM for a peaceful sunrise experience.",
                },
                "afternoon": {
                    "time": "11:30 AM – 3:30 PM",
                    "activities": ["Explore Fort Aguada", "Photography at the lighthouse"],
                    "attraction": "Fort Aguada",
                    "food": "Lunch at Infantaria — veg thali (est. INR 350/person)",
                    "transport": "Auto-rickshaw (est. INR 120, 20 min)",
                    "estimated_cost": 900,
                    "notes": "Fort entry is free. Carry water — hot after noon.",
                },
                "evening": {
                    "time": "4:30 PM – 9:00 PM",
                    "activities": ["Anjuna Flea Market", "Sunset at Vagator Beach"],
                    "attraction": "Anjuna Beach",
                    "food": "Dinner at Thalassa — veg mezze platter (est. INR 600/person)",
                    "transport": "Scooter rental (est. INR 300/day)",
                    "estimated_cost": 1800,
                    "notes": "Book Thalassa in advance. Wednesday is market day at Anjuna.",
                },
                "day_total_cost": 3000,
                "daily_transport": "Auto-rickshaw + Scooter rental",
                "tips": [
                    "Apply sunscreen before stepping out — Goa sun is intense after 10 AM.",
                    "Bargain politely at the flea market.",
                    "Carry small change for autos.",
                ],
            },
            {
                "day": 2, "date": "Tuesday, 11 March 2025",
                "morning": {
                    "time": "8:00 AM – 11:00 AM",
                    "activities": ["Visit Basilica of Bom Jesus", "Old Goa churches heritage walk"],
                    "attraction": "Basilica of Bom Jesus",
                    "food": "Breakfast at local bakery — pão & chai (est. INR 100/person)",
                    "transport": "Bus from Panaji (est. INR 30)",
                    "estimated_cost": 400,
                    "notes": "Entry to Basilica is free. Dress modestly — shoulders covered.",
                },
                "afternoon": {
                    "time": "12:00 PM – 4:00 PM",
                    "activities": ["Explore Panjim Latin Quarter (Fontainhas)", "Colorful streets photography"],
                    "attraction": "Fontainhas Heritage District",
                    "food": "Lunch at Viva Panjim — Goan veg curry rice (est. INR 300/person)",
                    "transport": "Walk within Fontainhas (free)",
                    "estimated_cost": 700,
                    "notes": "Best photography at golden hour but daytime also great.",
                },
                "evening": {
                    "time": "5:00 PM – 9:00 PM",
                    "activities": ["Mandovi River cruise with live music", "Browse Panaji evening market"],
                    "attraction": "Mandovi River",
                    "food": "Dinner at Hotel Venite — veg Goan platter (est. INR 400/person)",
                    "transport": "Walk to jetty (10 min)",
                    "estimated_cost": 1600,
                    "notes": "River cruise tickets: INR 250/person. Book at the jetty.",
                },
                "day_total_cost": 2700,
                "daily_transport": "Bus + Walking",
                "tips": [
                    "Panaji is very walkable — comfortable shoes recommended.",
                    "River cruise is a highlight — don't skip it.",
                ],
            },
            {
                "day": 3, "date": "Wednesday, 12 March 2025",
                "morning": {
                    "time": "7:30 AM – 11:00 AM",
                    "activities": ["Baga Beach morning swim", "Water sports (optional)"],
                    "attraction": "Baga Beach",
                    "food": "Breakfast at Brittos — fruit bowl & toast (est. INR 200/person)",
                    "transport": "Scooter (est. INR 300/day)",
                    "estimated_cost": 700,
                    "notes": "Water sports operators are on the beach. Negotiate price.",
                },
                "afternoon": {
                    "time": "12:00 PM – 3:30 PM",
                    "activities": ["Spice plantation tour", "Elephant interaction"],
                    "attraction": "Sahakari Spice Farm",
                    "food": "Buffet lunch included in plantation tour (est. INR 600/person)",
                    "transport": "Taxi to plantation (est. INR 400 one-way)",
                    "estimated_cost": 2000,
                    "notes": "Tour + lunch + elephant: INR 600/person. Book in advance.",
                },
                "evening": {
                    "time": "4:30 PM – 8:30 PM",
                    "activities": ["Souvenirs shopping at Calangute Market", "Final sunset at Baga"],
                    "attraction": "Calangute Market",
                    "food": "Farewell dinner at Fiesta — veg pasta & dessert (est. INR 500/person)",
                    "transport": "Walk (5 min)",
                    "estimated_cost": 1600,
                    "notes": "Great place to buy cashews, spices, and Goa souvenirs.",
                },
                "day_total_cost": 4300,
                "daily_transport": "Scooter + Taxi",
                "tips": [
                    "Buy Goa cashews and spices as gifts — best quality here.",
                    "Keep departure time in mind for Day 3 evening plans.",
                ],
            },
        ],
        "budget_breakdown": {
            "accommodation": 3000,
            "food": 3500,
            "transportation": 1500,
            "activities_entry_fees": 1200,
            "shopping_misc": 800,
            "total_estimated": 10000,
        },
        "packing_list": [
            "Sunscreen SPF 50+",
            "Sunglasses and hat",
            "Light cotton clothes",
            "Comfortable walking shoes",
            "Waterproof sandals / flip-flops",
            "Small backpack for day trips",
            "Power bank",
            "Reusable water bottle",
            "Valid ID / passport",
            "Cash (INR) for local markets",
        ],
        "important_tips": [
            "March is peak season — book hotels at least 2 weeks in advance.",
            "Scooter rental is the most convenient transport in Goa (INR 300/day).",
            "Carry sunscreen — UV index is very high in March.",
            "Always negotiate prices at local markets.",
            "Respect religious sites — carry a scarf to cover shoulders.",
            "Try local Goan dishes: sol kadi, poha, bebinca (sweet dessert).",
            "Emergency number: 112 | Tourist Helpline: 1800-111-363",
        ],
    }

    st.session_state.itinerary = sample
    st.session_state.user_inputs = {
        "destination": "Goa",
        "num_days": 3,
        "num_travelers": 2,
        "budget": 15000,
        "currency": "INR",
        "start_date": "2025-03-10",
        "interests": ["Beaches", "Food", "Culture"],
        "travel_style": "Standard",
        "accommodation": "3-Star Hotel",
        "transportation": "Mixed",
        "food_preferences": ["Vegetarian"],
        "special_requirements": "None",
    }
